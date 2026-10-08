"""Read-only replay adapter for the saved G2 v6 development rows.

The adapter recomputes every center slab with the byte-pinned v6 arithmetic
source, then converts the resulting exact endpoints into the common G4 tube
representation. It never invokes the v6 producer and never widens the label
image or the physical task.
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from typing import Any

from validation.autonomous_w2.g4.v6_snapshot_v3.producer_centered_v6 import (
    _center_matrix, interval_hash,
)
from validation.autonomous_w2.g4.v6_snapshot_v3.producer_v4 import exp_range
from validation.autonomous_w2.g4.v6_snapshot_v3.rational_interval_v3 import (
    Budget as V6Budget, I, activate, configure_fixed_grid, configure_integer_string_limit,
)
from validation.g2.rational import Budget, Interval, InvalidInput
from validation.g4.common_tube import TubeSegment


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
    return sha256_bytes(raw)


def _q(value: str | dict[str, str]) -> Fraction:
    if isinstance(value, str):
        return Fraction(value)
    if isinstance(value, dict) and set(value) == {"num", "den"}:
        return Fraction(int(value["num"]), int(value["den"]))
    raise InvalidInput(f"invalid v6 rational spelling: {value!r}")


def _as_common(value: I, budget: Budget) -> Interval:
    # v6 uses a separate fixed-grid scalar type. The endpoint values are exact
    # rationals after replay; conversion is audited by the common budget.
    return Interval(budget.check_input(value.lo), budget.check_input(value.hi), budget)


def _expanded(center: I, radius: Fraction, budget: Budget) -> Interval:
    if radius < 0:
        raise InvalidInput("negative v6 radius")
    return Interval(budget.add(center.lo, -radius), budget.add(center.hi, radius), budget)


def _labels(benchmark: dict[str, Any], budget: Budget) -> tuple[tuple[str, Interval], ...]:
    labels = benchmark.get("parameter_cell", {}).get("labels")
    names = [item["name"] for item in benchmark.get("parameter_labels", [])]
    if not isinstance(labels, dict) or names != [
        "rho_L", "rho_R", "C_L", "C_R", "lambda_L", "lambda_R", "R_L", "R_R", "B_L", "B_R", "k_L", "k_R",
    ]:
        raise InvalidInput("benchmark label order is not the frozen full image")
    out = []
    for name in names:
        raw = labels[name]
        if len(raw) != 2:
            raise InvalidInput("benchmark label interval malformed")
        lo, hi = _q(raw[0]), _q(raw[1])
        if (lo, hi) != (Fraction(9999, 10000), Fraction(10001, 10000)):
            raise InvalidInput("v6 common adapter narrowed the full label image")
        out.append((name, Interval(lo, hi, budget)))
    return tuple(out)


def convert_v6_row_to_segments(
    row: dict[str, Any], task_protocol: dict[str, Any], protocol: dict[str, Any],
    binding: dict[str, Any], profile: dict[str, Any], benchmark: dict[str, Any],
    budget: Budget,
) -> tuple[tuple[TubeSegment, ...], dict[str, int]]:
    if row.get("schema") != "G2_W2_CENTERED_RESIDUAL_ROW_v6":
        raise InvalidInput("V6_ROW_SCHEMA")
    action_id = binding.get("action_id")
    actions = [item for item in task_protocol.get("actions", []) if item.get("id") == action_id]
    if len(actions) != 1 or row.get("action_id") != action_id:
        raise InvalidInput("V6_ACTION_BINDING")
    action = actions[0]
    if row.get("held_voltage_V") != [f"{Fraction(v).numerator}/{Fraction(v).denominator}" for v in map(Fraction, action["voltage"])] and row.get("held_voltage_V") != action["voltage"]:
        raise InvalidInput("V6_VOLTAGE_BINDING")
    if row.get("protocol_sha256") != binding.get("protocol_sha256") or row.get("profile_sha256") != binding.get("profile_sha256"):
        raise InvalidInput("V6_ROW_PROTOCOL_PROFILE_BINDING")
    if row.get("parameter_label_order") != task_protocol["model"]["fixed_label_order"] or row.get("parameter_label_bounds") != task_protocol["model"]["fixed_label_bounds"]:
        raise InvalidInput("V6_FULL_FIXED_LABEL_IMAGE_CHANGED")
    if task_protocol.get("protocol_id") != "G2_W2_VOF_TASK_V1" or task_protocol.get("protocol_state") != "FROZEN_FOR_DEVELOPMENT_NOT_CONFIRMATION":
        raise InvalidInput("V6_TASK_PROTOCOL_UNSUPPORTED")
    if Fraction(task_protocol["task"]["hold_s"]) != Fraction(2):
        raise InvalidInput("V6_HORIZON_CHANGED")

    radius = _q(row["internal_error_radius_full_hold"])
    theta_h = _q(row["theta_abs_upper_full_hold"])
    ep_x = _q(row["position_error_x_upper_m"])
    ep_y = _q(row["position_error_y_upper_m"])
    labels = _labels(benchmark, budget)
    voltage = tuple(Fraction(v) for v in action["voltage"])
    if voltage[0] != voltage[1]:
        raise InvalidInput("V6_ASYMMETRIC_VOLTAGE_UNSUPPORTED")
    configure_fixed_grid(
        int(profile["interval_fractional_bits"]), int(profile["rational_bit_cap"]),
        int(profile["matrix_taylor_degree"]),
    )
    configure_integer_string_limit(int(profile["python_int_string_digit_cap"]), int(profile["rational_bit_cap"]))
    v6_budget = V6Budget(int(profile["interval_operation_cap"]), int(profile["rational_bit_cap"]))
    activate(v6_budget)
    try:
        segments, replay_work = _recompute_and_convert(
            row, task_protocol, protocol, binding, profile, benchmark, budget,
            voltage=voltage, labels=labels, horizon=Fraction(task_protocol["task"]["hold_s"]),
            radius=radius, theta_h=theta_h, ep_x=ep_x, ep_y=ep_y, uc=_q(row["center_u_abs_upper"]),
            v6_budget=v6_budget,
        )
    finally:
        activate(None)
    return segments, replay_work


def _recompute_and_convert(
    row: dict[str, Any], task_protocol: dict[str, Any], protocol: dict[str, Any],
    binding: dict[str, Any], profile: dict[str, Any], benchmark: dict[str, Any],
    budget: Budget, *, voltage: tuple[Fraction, Fraction], labels: tuple[tuple[str, Interval], ...],
    horizon: Fraction, radius: Fraction, theta_h: Fraction, ep_x: Fraction, ep_y: Fraction,
    uc: Fraction, v6_budget: V6Budget,
) -> tuple[tuple[TubeSegment, ...], dict[str, int]]:
    matrix = _center_matrix(voltage)
    current = [I.point(Fraction(3, 10)), I.point(Fraction(1, 4)), I.point(Fraction(0)), I.point(Fraction(0)), I.point(Fraction(1))]
    slabs = row.get("slabs")
    if not isinstance(slabs, list) or len(slabs) != int(profile["center_time_slabs"]):
        raise InvalidInput("V6_CENTER_SLAB_COUNT")
    segments: list[TubeSegment] = []
    previous_endpoint: str | None = None
    px0 = max(abs(_q(task_protocol["task"]["initial_box"][0][0])), abs(_q(task_protocol["task"]["initial_box"][0][1])))
    py0 = max(abs(_q(task_protocol["task"]["initial_box"][1][0])), abs(_q(task_protocol["task"]["initial_box"][1][1])))
    # The protocol keeps the outer G4 identifier as external_id; native G2
    # identifiers are retained in action_id/peer_action_id.  Match the outer
    # field explicitly instead of expecting a nonexistent comparison_id key.
    expected_action = next(item for item in protocol["ordered_actions"] if item["external_id"] == binding["comparison_id"])
    if tuple(Fraction(v) for v in expected_action["voltage"]) != voltage:
        raise InvalidInput("V6_EXTERNAL_ACTION_MAPPING")
    action_id = binding["action_id"]
    for index, slab in enumerate(slabs):
        t_start, t_end = _q(slab["start_s"]), _q(slab["end_s"])
        h = t_end - t_start
        if slab.get("index") != index or h <= 0 or (previous_endpoint is not None and interval_hash(current) != previous_endpoint):
            raise InvalidInput("V6_CENTER_TIME_OR_ENDPOINT_CHAIN")
        if slab.get("start_interval_state_sha256") != interval_hash(current):
            raise InvalidInput(f"V6_CENTER_START_HASH:{index}")
        partial, _ = exp_range(matrix, current, h, int(profile["matrix_taylor_degree"]), partial=True)
        endpoint, _ = exp_range(matrix, current, h, int(profile["matrix_taylor_degree"]), partial=False)
        expected_fields = {
            "partial_u_mps": partial[0], "partial_wheel_rate_radps": partial[1],
            "partial_current_A": partial[2], "partial_p_x_m": partial[3],
        }
        for field, value in expected_fields.items():
            if slab.get(field) != [str(value.lo), str(value.hi)]:
                raise InvalidInput(f"V6_{field}_REPLAY_MISMATCH:{index}")
        endpoint_hash = interval_hash(endpoint)
        if slab.get("endpoint_interval_state_sha256") != endpoint_hash:
            raise InvalidInput(f"V6_ENDPOINT_HASH_MISMATCH:{index}")

        hull = (
            _expanded(partial[3], ep_x, budget), Interval(-ep_y, ep_y, budget),
            Interval(-theta_h, theta_h, budget), _expanded(partial[0], radius, budget),
            Interval(-radius, radius, budget), _expanded(partial[1], radius, budget),
            _expanded(partial[1], radius, budget), _expanded(partial[2], radius, budget),
            _expanded(partial[2], radius, budget),
        )
        end_px_err = min(ep_x, px0 + t_end * radius + t_end * uc * theta_h * theta_h / 2)
        start_px_err = min(ep_x, px0 + t_start * radius + t_start * uc * theta_h * theta_h / 2)
        end_py_err = min(ep_y, py0 + t_end * (uc + radius) * theta_h)
        start_py_err = min(ep_y, py0 + t_start * (uc + radius) * theta_h)
        endpoint_start = (
            Interval(current[3].lo - start_px_err, current[3].hi + start_px_err, budget),
            Interval(-start_py_err, start_py_err, budget), Interval(-theta_h, theta_h, budget),
            _expanded(current[0], radius, budget), Interval(-radius, radius, budget),
            _expanded(current[1], radius, budget), _expanded(current[1], radius, budget),
            _expanded(current[2], radius, budget), _expanded(current[2], radius, budget),
        )
        endpoint_end = (
            Interval(endpoint[3].lo - end_px_err, endpoint[3].hi + end_px_err, budget),
            Interval(-end_py_err, end_py_err, budget), Interval(-theta_h, theta_h, budget),
            _expanded(endpoint[0], radius, budget), Interval(-radius, radius, budget),
            _expanded(endpoint[1], radius, budget), _expanded(endpoint[1], radius, budget),
            _expanded(endpoint[2], radius, budget), _expanded(endpoint[2], radius, budget),
        )
        segments.append(TubeSegment.from_total_hull(
            segment_id=f"V6:{binding['comparison_id']}:{index}", t_start=t_start, t_end=t_end,
            state_hull=hull, labels=labels, endpoint_start=endpoint_start, endpoint_end=endpoint_end,
            radius_expansion_count=0, radius_expansion_mode="NATIVE_TOTAL_HULL",
            provenance={
                "method": "v6", "peer_release_sha256": binding["peer_release_sha256"],
                "native_row_sha256": binding.get("native_row_sha256", binding.get("peer_saved_row_sha256")), "input_action_id": action_id,
                "external_comparison_id": binding["comparison_id"],
                "enclosure_representation": "CENTER_PARTIAL_SLAB_PLUS_FROZEN_GLOBAL_ERROR_RADIUS",
            },
        ))
        current = endpoint
        previous_endpoint = endpoint_hash
    if not segments or segments[0].t_start != 0 or segments[-1].t_end != horizon:
        raise InvalidInput("V6_COMMON_SEGMENTS_DO_NOT_COVER_FULL_HOLD")
    return tuple(segments), {
        "v6_replay_interval_operations": v6_budget.operations,
        "v6_replay_max_rational_bits": v6_budget.max_observed_bits,
        "v6_replay_rounded_endpoints": v6_budget.rounded_endpoint_count,
    }
