"""G4 W2 conversion of the released v6 slab evidence into common tube hulls."""
from __future__ import annotations

from fractions import Fraction
from typing import Any

from validation.autonomous_w2.g2.producer_v4 import exp_range
from validation.autonomous_w2.g2.producer_centered_v6 import (
    CENTER_LABELS, _center_matrix, interval_hash,
)
from validation.g2.rational import Budget, Interval, InvalidInput, parse_q
from validation.g4.common_tube import TubeSegment


def qtext(value: str) -> Fraction:
    return Fraction(value)


def max_abs(value: Interval) -> Fraction:
    return max(abs(value.lo), abs(value.hi))


def convert_v6_row_to_segments(
    row: dict[str, Any], protocol: dict[str, Any], binding: dict[str, Any], budget: Budget,
) -> tuple[TubeSegment, ...]:
    if row.get("schema") != "G2_W2_CENTERED_RESIDUAL_ROW_v6":
        raise InvalidInput("V6_ROW_SCHEMA")
    action_id = binding["action_id"]
    actions = [item for item in protocol["actions"] if item.get("id") == action_id]
    if len(actions) != 1 or row.get("action_id") != action_id:
        raise InvalidInput("V6_ACTION_BINDING")
    action = actions[0]
    if row.get("held_voltage_V") != action["voltage"]:
        raise InvalidInput("V6_VOLTAGE_BINDING")
    expected_protocol_sha = binding["protocol_sha256"]
    if row.get("protocol_sha256") != expected_protocol_sha or row.get("profile_sha256") != binding["profile_sha256"]:
        raise InvalidInput("V6_ROW_PROTOCOL_PROFILE_BINDING")
    if row.get("parameter_label_order") != protocol["model"]["fixed_label_order"] or row.get("parameter_label_bounds") != protocol["model"]["fixed_label_bounds"]:
        raise InvalidInput("V6_FULL_FIXED_LABEL_IMAGE_CHANGED")
    R = qtext(row["internal_error_radius_full_hold"])
    theta_h = qtext(row["theta_abs_upper_full_hold"])
    ep_x = qtext(row["position_error_x_upper_m"])
    ep_y = qtext(row["position_error_y_upper_m"])
    labels = tuple((name, Interval(Fraction(9999, 10000), Fraction(10001, 10000), budget))
                   for name in protocol["model"]["fixed_label_order"])
    voltage = tuple(Fraction(value) for value in action["voltage"])
    matrix = _center_matrix(voltage)
    current = [Interval.point(Fraction(3, 10), budget), Interval.point(Fraction(1, 4), budget),
               Interval.point(Fraction(0), budget), Interval.point(Fraction(0), budget),
               Interval.point(Fraction(1), budget)]
    profile = binding["profile"]
    slabs = row.get("slabs")
    if not isinstance(slabs, list) or len(slabs) != int(profile["center_time_slabs"]):
        raise InvalidInput("V6_CENTER_SLAB_COUNT")
    segments: list[TubeSegment] = []
    previous_endpoint = None
    horizon = Fraction(protocol["task"]["hold_s"])
    for index, slab in enumerate(slabs):
        t_start, t_end = qtext(slab["start_s"]), qtext(slab["end_s"])
        h = t_end - t_start
        if slab.get("index") != index or h <= 0 or (previous_endpoint is not None and interval_hash(current) != previous_endpoint):
            raise InvalidInput("V6_CENTER_TIME_OR_ENDPOINT_CHAIN")
        if slab.get("start_interval_state_sha256") != interval_hash(current):
            raise InvalidInput("V6_CENTER_START_HASH")
        partial, _ = exp_range(matrix, current, h, int(profile["matrix_taylor_degree"]), partial=True)
        endpoint, _ = exp_range(matrix, current, h, int(profile["matrix_taylor_degree"]), partial=False)
        if slab.get("partial_u_mps") != [str(partial[0].lo), str(partial[0].hi)]:
            raise InvalidInput(f"V6_PARTIAL_U_REPLAY_MISMATCH:{index}")
        if slab.get("partial_wheel_rate_radps") != [str(partial[1].lo), str(partial[1].hi)]:
            raise InvalidInput(f"V6_PARTIAL_WHEEL_REPLAY_MISMATCH:{index}")
        if slab.get("partial_current_A") != [str(partial[2].lo), str(partial[2].hi)]:
            raise InvalidInput(f"V6_PARTIAL_CURRENT_REPLAY_MISMATCH:{index}")
        if slab.get("partial_p_x_m") != [str(partial[3].lo), str(partial[3].hi)]:
            raise InvalidInput(f"V6_PARTIAL_PX_REPLAY_MISMATCH:{index}")
        endpoint_hash = interval_hash(endpoint)
        if slab.get("endpoint_interval_state_sha256") != endpoint_hash:
            raise InvalidInput(f"V6_ENDPOINT_HASH_MISMATCH:{index}")
        # For each physical slab, the centered coordinates are expanded with
        # the v6 full-hold residual radius. The pose expansion uses its frozen
        # derived global position and heading error bounds. These imply closed
        # full-time coverage while retaining v6's proof premises.
        hull = (
            Interval(partial[3].lo - ep_x, partial[3].hi + ep_x, budget),
            Interval(-ep_y, ep_y, budget),
            Interval(-theta_h, theta_h, budget),
            Interval(partial[0].lo - R, partial[0].hi + R, budget),
            Interval(-R, R, budget),
            Interval(partial[1].lo - R, partial[1].hi + R, budget),
            Interval(partial[1].lo - R, partial[1].hi + R, budget),
            Interval(partial[2].lo - R, partial[2].hi + R, budget),
            Interval(partial[2].lo - R, partial[2].hi + R, budget),
        )
        # Reconstruct exact centered endpoint states from the G2 time chain,
        # then expand endpoint uncertainties by the same proven global radius.
        px0 = max(abs(Fraction(protocol["task"]["initial_box"][0][0])), abs(Fraction(protocol["task"]["initial_box"][0][1])))
        py0 = max(abs(Fraction(protocol["task"]["initial_box"][1][0])), abs(Fraction(protocol["task"]["initial_box"][1][1])))
        elapsed0, elapsed1 = t_start, t_end
        end_px_err = min(ep_x, px0 + elapsed1 * R + elapsed1 * qtext(row["center_u_abs_upper"]) * theta_h * theta_h / 2)
        start_px_err = min(ep_x, px0 + elapsed0 * R + elapsed0 * qtext(row["center_u_abs_upper"]) * theta_h * theta_h / 2)
        uc = qtext(row["center_u_abs_upper"])
        end_py_err = min(ep_y, py0 + elapsed1 * (uc + R) * theta_h)
        start_py_err = min(ep_y, py0 + elapsed0 * (uc + R) * theta_h)
        endpoint_start = (
            Interval(current[3].lo - start_px_err, current[3].hi + start_px_err, budget),
            Interval(-start_py_err, start_py_err, budget),
            Interval(-theta_h, theta_h, budget),
            Interval(current[0].lo - R, current[0].hi + R, budget),
            Interval(-R, R, budget),
            Interval(current[1].lo - R, current[1].hi + R, budget),
            Interval(current[1].lo - R, current[1].hi + R, budget),
            Interval(current[2].lo - R, current[2].hi + R, budget),
            Interval(current[2].lo - R, current[2].hi + R, budget),
        )
        endpoint_end = (
            Interval(endpoint[3].lo - end_px_err, endpoint[3].hi + end_px_err, budget),
            Interval(-end_py_err, end_py_err, budget),
            Interval(-theta_h, theta_h, budget),
            Interval(endpoint[0].lo - R, endpoint[0].hi + R, budget),
            Interval(-R, R, budget),
            Interval(endpoint[1].lo - R, endpoint[1].hi + R, budget),
            Interval(endpoint[1].lo - R, endpoint[1].hi + R, budget),
            Interval(endpoint[2].lo - R, endpoint[2].hi + R, budget),
            Interval(endpoint[2].lo - R, endpoint[2].hi + R, budget),
        )
        segments.append(TubeSegment.from_total_hull(
            segment_id=f"V6:{action_id}:{index}", t_start=t_start, t_end=t_end,
            state_hull=hull, labels=labels, endpoint_start=endpoint_start,
            endpoint_end=endpoint_end, radius_expansion_count=0,
            radius_expansion_mode="NATIVE_TOTAL_HULL",
            provenance={
                "method": "v6",
                "peer_release_sha256": binding["peer_release_sha256"],
                "peer_row_sha256": binding["peer_row_sha256"],
                "input_action_id": action_id,
                "enclosure_representation": "CENTER_PARTIAL_SLAB_PLUS_FROZEN_GLOBAL_ERROR_RADIUS",
            },
        ))
        current = endpoint
        previous_endpoint = endpoint_hash
    if segments[0].t_start != 0 or segments[-1].t_end != horizon:
        raise InvalidInput("V6_COMMON_SEGMENTS_DO_NOT_COVER_FULL_HOLD")
    return tuple(segments)
