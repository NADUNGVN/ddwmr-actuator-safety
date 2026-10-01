"""Typed full-time tube representation and shared collision/contact checks.

This module checks predicates on supplied enclosures. It does not validate an
ODE tube or emit a safety certificate. Upstream solvers must independently
prove their segment inclusions and outward bounds before a passing predicate
result can be combined with them.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Iterable

from validation.g2.hashing import semantic_json_sha256
from validation.g2.interval import sqrt_lower
from validation.g2.model import ModelIntervals, build_model, physical_internal_box
from validation.g2.rational import Budget, Interval, InvalidInput, parse_q, qobj


STATE_ORDER = (
    "p_x", "p_y", "theta", "u", "r", "omega_L", "omega_R", "i_L", "i_R",
)
TUBE_SCHEMA = "ddwmr-g4-full-time-tube-segment-v1"
CHECK_SCHEMA = "ddwmr-g4-common-tube-check-v1"
AUER_NATIVE_SCHEMA = "auer2013-native-tube-segment-rational-time-binary64-state-v1"


def binary64_hex_fraction(value: Any) -> Fraction:
    """Convert a round-trip hexadecimal binary64 value to its exact rational.

    This conversion preserves the represented float exactly. It does not prove
    that an upstream interval endpoint was outward rounded.
    """
    if not isinstance(value, str):
        raise InvalidInput("binary64 endpoints must be hexadecimal strings")
    try:
        number = float.fromhex(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise InvalidInput("invalid binary64 hexadecimal endpoint") from exc
    if not math.isfinite(number):
        raise InvalidInput("non-finite binary64 endpoints are unsupported")
    numerator, denominator = number.as_integer_ratio()
    return Fraction(numerator, denominator)


def interval_from_binary64_hex(raw: Any, budget: Budget) -> Interval:
    if not isinstance(raw, list) or len(raw) != 2:
        raise InvalidInput("binary64 interval must have lower and upper hex endpoints")
    return Interval(binary64_hex_fraction(raw[0]), binary64_hex_fraction(raw[1]), budget)


def _point(value: Fraction, budget: Budget) -> Interval:
    return Interval.point(value, budget)


def _parse_rational_interval_map(raw: Any, expected_names: Iterable[str], budget: Budget) -> tuple[tuple[str, Interval], ...]:
    names = tuple(expected_names)
    if not isinstance(raw, dict) or set(raw) != set(names):
        raise InvalidInput("fixed-label ranges must cover exactly the declared parameter labels")
    return tuple((name, Interval.from_json(raw[name], budget)) for name in names)


def _parse_state_vector(raw: Any, budget: Budget, *, binary64: bool = False) -> tuple[Interval, ...]:
    if not isinstance(raw, list) or len(raw) != len(STATE_ORDER):
        raise InvalidInput("tube state vector must contain exactly nine intervals")
    parser = interval_from_binary64_hex if binary64 else Interval.from_json
    return tuple(parser(item, budget) for item in raw)


def _subset(inner: Interval, outer: Interval) -> bool:
    inner._same(outer)
    return outer.lo <= inner.lo and inner.hi <= outer.hi


def _same_interval(a: Interval, b: Interval) -> bool:
    a._same(b)
    return a.lo == b.lo and a.hi == b.hi


def clip_value_interval(value: Interval) -> Interval:
    """Exact monotone range of the shared clip(q,-1,1) law."""
    return Interval(
        max(Fraction(-1), min(Fraction(1), value.lo)),
        max(Fraction(-1), min(Fraction(1), value.hi)),
        value.budget,
    )


def _endpoint_json(time: Fraction, state: tuple[Interval, ...]) -> dict[str, Any]:
    return {"time": qobj(time), "state_hull": [part.to_json() for part in state]}


@dataclass(frozen=True)
class TubeSegment:
    """One closed time slab, with a single expanded state hull.

    `state_hull` already includes any native or adapter-applied residual/radius.
    The common checker consumes only this total hull and never expands a radius
    again. `radius_expansion_count` records how the adapter formed the hull.
    """

    segment_id: str
    t_start: Fraction
    t_end: Fraction
    state_hull: tuple[Interval, ...]
    labels: tuple[tuple[str, Interval], ...]
    endpoint_start: tuple[Interval, ...]
    endpoint_end: tuple[Interval, ...]
    radius_expansion_count: int
    radius_expansion_mode: str
    provenance: dict[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.segment_id, str) or not self.segment_id:
            raise InvalidInput("tube segment id must be a nonempty string")
        if self.t_start < 0 or self.t_start >= self.t_end:
            raise InvalidInput("tube segment must have a positive closed time interval")
        if len(self.state_hull) != 9 or len(self.endpoint_start) != 9 or len(self.endpoint_end) != 9:
            raise InvalidInput("tube segment and both endpoints must have nine physical states")
        if not self.labels or len({name for name, _ in self.labels}) != len(self.labels):
            raise InvalidInput("tube segment fixed-label coordinates must be nonempty and unique")
        if not isinstance(self.radius_expansion_count, int) or isinstance(self.radius_expansion_count, bool):
            raise InvalidInput("radius expansion count must be an integer")
        if self.radius_expansion_count not in (0, 1):
            raise InvalidInput("a center/radius expansion may be applied at most once")
        if self.radius_expansion_mode not in {
            "NATIVE_TOTAL_HULL", "CENTER_PLUS_RESIDUAL_ONCE", "CENTER_PLUS_RADIUS_ONCE",
        }:
            raise InvalidInput("unknown radius/enclosure expansion mode")
        if not isinstance(self.provenance, dict):
            raise InvalidInput("tube provenance must be a JSON object")
        expected_count = 0 if self.radius_expansion_mode == "NATIVE_TOTAL_HULL" else 1
        if self.radius_expansion_count != expected_count:
            raise InvalidInput("radius expansion mode and application count disagree")
        budget = self.state_hull[0].budget
        for group in (self.state_hull, self.endpoint_start, self.endpoint_end):
            if any(item.budget is not budget for item in group):
                raise RuntimeError("all segment state intervals must share one resource budget")
        if any(item.budget is not budget for _, item in self.labels):
            raise RuntimeError("segment labels must share the state interval resource budget")
        for endpoint in (self.endpoint_start, self.endpoint_end):
            if any(not _subset(value, hull) for value, hull in zip(endpoint, self.state_hull)):
                raise InvalidInput("closed endpoint enclosure is not contained in its full-time slab hull")

    @classmethod
    def from_total_hull(
        cls,
        *,
        segment_id: str,
        t_start: Fraction,
        t_end: Fraction,
        state_hull: tuple[Interval, ...],
        labels: tuple[tuple[str, Interval], ...],
        endpoint_start: tuple[Interval, ...],
        endpoint_end: tuple[Interval, ...],
        provenance: dict[str, Any],
        radius_expansion_count: int = 0,
        radius_expansion_mode: str = "NATIVE_TOTAL_HULL",
    ) -> "TubeSegment":
        return cls(
            segment_id, t_start, t_end, state_hull, labels, endpoint_start, endpoint_end,
            radius_expansion_count, radius_expansion_mode, provenance,
        )

    @classmethod
    def from_json(
        cls, raw: Any, expected_label_names: Iterable[str], budget: Budget,
    ) -> "TubeSegment":
        required = {
            "schema", "segment_id", "time_closed", "state_order", "enclosure_representation", "state_hull",
            "fixed_labels", "endpoint_start", "endpoint_end", "radius_expansion_count", "radius_expansion_mode",
            "provenance",
        }
        if not isinstance(raw, dict) or set(raw) != required or raw.get("schema") != TUBE_SCHEMA:
            raise InvalidInput("invalid serialized common tube segment")
        if raw.get("state_order") != list(STATE_ORDER) or raw.get("enclosure_representation") != "TOTAL_STATE_HULL":
            raise InvalidInput("common segment must use the canonical expanded nine-state hull")
        if not isinstance(raw.get("radius_expansion_count"), int) or isinstance(raw.get("radius_expansion_count"), bool):
            raise InvalidInput("radius expansion count must be an integer")
        time_raw = raw["time_closed"]
        if not isinstance(time_raw, dict) or set(time_raw) != {"start", "end"}:
            raise InvalidInput("closed time interval must provide exact start and end")
        start_raw = parse_q(time_raw["start"], budget)
        end_raw = parse_q(time_raw["end"], budget)
        labels = _parse_rational_interval_map(raw["fixed_labels"], expected_label_names, budget)
        start_obj, end_obj = raw["endpoint_start"], raw["endpoint_end"]
        if not isinstance(start_obj, dict) or not isinstance(end_obj, dict):
            raise InvalidInput("segment endpoint evidence must be objects")
        if start_obj.get("time") != qobj(start_raw) or end_obj.get("time") != qobj(end_raw):
            raise InvalidInput("endpoint timestamps do not match the closed slab boundaries")
        start_state = _parse_state_vector(start_obj.get("state_hull"), budget)
        end_state = _parse_state_vector(end_obj.get("state_hull"), budget)
        return cls.from_total_hull(
            segment_id=raw["segment_id"], t_start=start_raw, t_end=end_raw,
            state_hull=_parse_state_vector(raw["state_hull"], budget), labels=labels,
            endpoint_start=start_state, endpoint_end=end_state, provenance=raw["provenance"],
            radius_expansion_count=raw["radius_expansion_count"],
            radius_expansion_mode=raw["radius_expansion_mode"],
        )

    def to_json(self) -> dict[str, Any]:
        return {
            "schema": TUBE_SCHEMA,
            "segment_id": self.segment_id,
            "time_closed": {"start": qobj(self.t_start), "end": qobj(self.t_end)},
            "state_order": list(STATE_ORDER),
            "enclosure_representation": "TOTAL_STATE_HULL",
            "state_hull": [part.to_json() for part in self.state_hull],
            "fixed_labels": {name: value.to_json() for name, value in self.labels},
            "endpoint_start": _endpoint_json(self.t_start, self.endpoint_start),
            "endpoint_end": _endpoint_json(self.t_end, self.endpoint_end),
            "radius_expansion_count": self.radius_expansion_count,
            "radius_expansion_mode": self.radius_expansion_mode,
            "provenance": self.provenance,
        }


def center_radius_to_hull(
    center: tuple[Interval, ...], radii: tuple[Fraction, ...], budget: Budget,
) -> tuple[Interval, ...]:
    """Expand a center interval plus nonnegative symmetric radii exactly once."""
    if len(center) != len(radii) or not center:
        raise InvalidInput("center and radius vectors must have the same nonzero length")
    out = []
    for part, radius in zip(center, radii):
        if part.budget is not budget or radius < 0:
            raise InvalidInput("center/radius expansion has a budget mismatch or negative radius")
        out.append(Interval(budget.add(part.lo, -radius), budget.add(part.hi, radius), budget))
    return tuple(out)


def auer_native_segment_to_common(raw: Any, benchmark: dict[str, Any], budget: Budget) -> TubeSegment:
    """Adapt an Auer full-step approximation/residual record to the common hull.

    The input schema requires full-step `x_app` and residual ranges, not the
    legacy VALENCIA text samples (which are endpoint-only and low precision).
    Binary64 hex values are converted to exact rationals before addition.
    """
    required = {
        "schema", "segment_id", "time_start", "time_end", "x_app_step_range_hex",
        "residual_step_range_hex", "labels", "endpoint_start_hex", "endpoint_end_hex",
        "proof_record_sha256", "method_id",
    }
    if not isinstance(raw, dict) or set(raw) != required or raw.get("schema") != AUER_NATIVE_SCHEMA:
        raise InvalidInput("Auer native segment must follow the declared full-time binary64 schema")
    proof_hash = raw.get("proof_record_sha256")
    if not isinstance(proof_hash, str) or len(proof_hash) != 64 or any(ch not in "0123456789abcdef" for ch in proof_hash):
        raise InvalidInput("Auer segment must identify its upstream proof record by SHA-256")
    names = [item["name"] for item in benchmark.get("parameter_labels", [])]
    labels = _parse_rational_interval_map(raw["labels"], names, budget)
    start = parse_q(raw["time_start"], budget)
    end = parse_q(raw["time_end"], budget)
    x_app = _parse_state_vector(raw["x_app_step_range_hex"], budget, binary64=True)
    residual = _parse_state_vector(raw["residual_step_range_hex"], budget, binary64=True)
    total = tuple(a + b for a, b in zip(x_app, residual))
    endpoint_start = _parse_state_vector(raw["endpoint_start_hex"], budget, binary64=True)
    endpoint_end = _parse_state_vector(raw["endpoint_end_hex"], budget, binary64=True)
    return TubeSegment.from_total_hull(
        segment_id=raw["segment_id"], t_start=start, t_end=end, state_hull=total,
        labels=labels, endpoint_start=endpoint_start, endpoint_end=endpoint_end,
        radius_expansion_count=1, radius_expansion_mode="CENTER_PLUS_RESIDUAL_ONCE",
        provenance={
            "method_id": raw["method_id"], "native_proof_record_sha256": proof_hash,
            "native_time_rational_and_state_binary64_hex_bounds": "STATE_ENDPOINTS_CONVERTED_TO_EXACT_RATIONAL",
            "upstream_outward_proof_replayed_here": False,
        },
    )


def r3_record_to_common_segment(record: dict[str, Any], query: dict[str, Any], budget: Budget) -> TubeSegment:
    """Replay an existing R3 native proof, then apply its radius once.

    This adapter is read-only with respect to all native R3 records. The full
    hold enclosure is reused as a coarse endpoint enclosure when the native
    result does not provide a tighter point-at-T range.
    """
    from validation.g2.checker import replay_record

    replay = replay_record(record, query)
    if not replay.get("replayed"):
        raise InvalidInput("native R3 proof replay failed; common adaptation is rejected")
    if not isinstance(record.get("proof"), dict) or not isinstance(query.get("benchmark"), dict):
        raise InvalidInput("R3 adapter requires a replayed proof and its benchmark query")
    proof = record["proof"]
    benchmark = query["benchmark"]
    model = build_model(benchmark, budget)
    if proof.get("parameter_label_order") != model.parameter_label_order:
        raise InvalidInput("R3 proof label order differs from the common model")
    label_hull = _parse_rational_interval_map(
        proof.get("parameter_label_cell"), model.parameter_label_order, budget,
    )
    expected = model.parameter_label_box
    if any(not _same_interval(value, expected[name]) for name, value in label_hull):
        raise InvalidInput("R3 proof does not cover the declared full fixed-label image")

    centers_pose = [
        Interval.from_json(proof.get("center_position_x_range"), budget),
        Interval.from_json(proof.get("center_position_y_range"), budget),
        Interval.from_json(proof.get("center_heading_range"), budget),
    ]
    P1_scaled_raw = proof.get("P1_scaled")
    if not isinstance(P1_scaled_raw, list) or len(P1_scaled_raw) != 6:
        raise InvalidInput("R3 proof lacks its six-coordinate internal full-time range")
    internal_center = physical_internal_box(
        [Interval.from_json(item, budget) for item in P1_scaled_raw], model.scales,
    )
    centers = tuple(centers_pose + internal_center)
    eta = proof.get("eta_physical")
    if not isinstance(eta, list) or len(eta) != 6:
        raise InvalidInput("R3 proof lacks its six internal-state error radii")
    radii = (
        parse_q(proof.get("E_p"), budget), parse_q(proof.get("E_p"), budget),
        parse_q(proof.get("E_theta"), budget), *(parse_q(item, budget) for item in eta),
    )
    state_hull = center_radius_to_hull(centers, tuple(radii), budget)
    start_state = _parse_state_vector(query["state_cell"].get("box"), budget)
    horizon = parse_q(query["horizon"].get("T"), budget)
    if horizon <= 0:
        raise InvalidInput("R3 adapter requires a positive hold duration")
    return TubeSegment.from_total_hull(
        segment_id=f"R3:{record.get('query_id', 'unknown')}:full_hold",
        t_start=Fraction(0), t_end=horizon, state_hull=state_hull,
        labels=label_hull, endpoint_start=start_state, endpoint_end=state_hull,
        radius_expansion_count=1, radius_expansion_mode="CENTER_PLUS_RADIUS_ONCE",
        provenance={
            "method_id": record.get("method_id"), "query_id": record.get("query_id"),
            "native_record_semantic_sha256": semantic_json_sha256(record),
            "native_proof_replay": "PASS",
            "endpoint_enclosure_source": "REUSED_FULL_HOLD_HULL_COARSE_BOUND",
        },
    )


def _expected_labels(benchmark: dict[str, Any], model: ModelIntervals, budget: Budget) -> tuple[tuple[str, Interval], ...]:
    labels = tuple((name, model.parameter_label_box[name]) for name in model.parameter_label_order)
    declared = benchmark.get("parameter_cell", {}).get("labels")
    if not isinstance(declared, dict):
        raise InvalidInput("benchmark lacks its full fixed-label parameter cell")
    for name, value in labels:
        if not _same_interval(value, Interval.from_json(declared[name], budget)):
            raise InvalidInput("model label image changed during common tube checking")
    return labels


def _validate_segment_chain(
    segments: tuple[TubeSegment, ...], benchmark: dict[str, Any], horizon: Fraction,
    model: ModelIntervals, budget: Budget,
) -> None:
    if not segments:
        raise InvalidInput("at least one complete time segment is required")
    expected = _expected_labels(benchmark, model, budget)
    if segments[0].t_start != 0 or segments[-1].t_end != horizon:
        raise InvalidInput("closed segments must cover the entire hold [0,T]")
    for index, segment in enumerate(segments):
        if segment.state_hull[0].budget is not budget:
            raise InvalidInput("tube segments were parsed with a different arithmetic budget")
        if len(segment.labels) != len(expected):
            raise InvalidInput("tube segment omitted fixed parameter labels")
        for (name, actual), (want_name, want) in zip(segment.labels, expected):
            if name != want_name or not _same_interval(actual, want):
                raise InvalidInput("fixed parameter labels were changed, reordered, or narrowed")
        if index:
            previous = segments[index - 1]
            if previous.t_end != segment.t_start:
                raise InvalidInput("closed time segments have a gap or overlap")
            if any(not _same_interval(a, b) for a, b in zip(previous.endpoint_end, segment.endpoint_start)):
                raise InvalidInput("adjacent slabs do not share the same propagated boundary enclosure")


def _scene_obstacles(scene: dict[str, Any], budget: Budget) -> list[dict[str, Any]]:
    raw = scene.get("obstacles")
    if raw is None:
        raw = [{"id": scene.get("id"), "p_o": scene.get("p_o"), "R_s": scene.get("R_s")}]
    if not isinstance(raw, list) or not raw:
        raise InvalidInput("scene must contain at least one static circular obstacle")
    obstacles = []
    for item in raw:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise InvalidInput("each static obstacle requires a string id")
        center = item.get("p_o")
        if not isinstance(center, list) or len(center) != 2:
            raise InvalidInput("each static obstacle requires a two-coordinate center")
        radius = parse_q(item.get("R_s"), budget)
        if radius <= 0:
            raise InvalidInput("obstacle exclusion radius must be positive")
        obstacles.append({
            "id": item["id"], "p_o": [parse_q(value, budget) for value in center], "R_s": radius,
        })
    return obstacles


def _collision_margin(state: tuple[Interval, ...], obstacle: dict[str, Any], sqrt_bisections: int, budget: Budget) -> dict[str, Any]:
    x, y = state[0], state[1]
    ox, oy = obstacle["p_o"]
    dx = max(Fraction(0), budget.add(x.lo, -ox), budget.add(ox, -x.hi))
    dy = max(Fraction(0), budget.add(y.lo, -oy), budget.add(oy, -y.hi))
    squared = budget.add(budget.mul(dx, dx), budget.mul(dy, dy))
    distance_lower, distance_upper = sqrt_lower(squared, sqrt_bisections, budget)
    margin = budget.add(distance_lower, -obstacle["R_s"])
    return {
        "obstacle_id": obstacle["id"],
        "coordinate_gaps": [qobj(dx), qobj(dy)],
        "squared_distance_lower": qobj(squared),
        "sqrt_bracket": [qobj(distance_lower), qobj(distance_upper)],
        "exclusion_radius": qobj(obstacle["R_s"]),
        "margin_lower": qobj(margin),
    }


def _contact_margin(state: tuple[Interval, ...], model: ModelIntervals, budget: Budget, sqrt_bisections: int) -> dict[str, Any]:
    params = model.parameters
    u, r, omega_l, omega_r = state[3], state[4], state[5], state[6]
    slip_l = params["R_w"] * omega_l - u + params["b"] * r
    slip_r = params["R_w"] * omega_r - u - params["b"] * r
    normalized = [slip_l / params["v_s"], slip_r / params["v_s"]]
    clipped = [clip_value_interval(value) for value in normalized]
    beta = [value.abs_upper() for value in clipped]
    reserves = []
    root_brackets = []
    for index, side in enumerate(("L", "R")):
        if beta[index] > 1:
            raise InvalidInput("exact clip range exceeded its unit bound")
        radicand = budget.add(Fraction(1), -budget.mul(beta[index], beta[index]))
        root_lo, root_hi = sqrt_lower(radicand, sqrt_bisections, budget)
        root_brackets.append([qobj(root_lo), qobj(root_hi)])
        reserves.append(budget.mul(params[f"C_{side}"].lo, root_lo))
    available = budget.add(reserves[0], reserves[1])
    demand = budget.mul(
        params["m"].hi,
        budget.mul(u.abs_upper(), r.abs_upper()),
    )
    margin = budget.add(available, -demand)
    return {
        "normalized_slip_ranges": [item.to_json() for item in normalized],
        "clip_ranges": [item.to_json() for item in clipped],
        "beta_upper": [qobj(value) for value in beta],
        "root_lower_upper_brackets": root_brackets,
        "available_lower": qobj(available),
        "demand_upper": qobj(demand),
        "margin_lower": qobj(margin),
    }


def check_tube_segments(
    segments: tuple[TubeSegment, ...],
    benchmark: dict[str, Any],
    scene: dict[str, Any],
    horizon: Fraction,
    budget: Budget,
    *,
    initial_state: tuple[Interval, ...],
    sqrt_bisections: int = 128,
) -> dict[str, Any]:
    """Check full-time collision/contact predicates on every closed slab.

    A passing result means only that the supplied total state hull passes these
    predicates. It never validates the upstream ODE inclusion.
    """
    if not isinstance(horizon, Fraction) or horizon <= 0:
        raise InvalidInput("common tube horizon must be a positive exact rational")
    if not isinstance(sqrt_bisections, int) or isinstance(sqrt_bisections, bool) or not 0 <= sqrt_bisections <= 256:
        raise InvalidInput("square-root bisection count must be in [0,256]")
    model = build_model(benchmark, budget)
    _validate_segment_chain(segments, benchmark, horizon, model, budget)
    if len(initial_state) != len(STATE_ORDER) or any(item.budget is not budget for item in initial_state):
        raise InvalidInput("initial state must be nine intervals using the common arithmetic budget")
    if any(not _subset(value, start) for value, start in zip(initial_state, segments[0].endpoint_start)):
        raise InvalidInput("first closed endpoint enclosure does not contain the full initial state cell")
    obstacles = _scene_obstacles(scene, budget)
    segment_checks = []
    all_margins = []
    for segment in segments:
        contact = _contact_margin(segment.state_hull, model, budget, sqrt_bisections)
        collision = [_collision_margin(segment.state_hull, item, sqrt_bisections, budget) for item in obstacles]
        margins = [parse_q(contact["margin_lower"], budget)] + [parse_q(item["margin_lower"], budget) for item in collision]
        all_margins.extend(margins)
        segment_checks.append({
            "segment_id": segment.segment_id,
            "closed_time": {"start": qobj(segment.t_start), "end": qobj(segment.t_end)},
            "contact": contact,
            "collision": collision,
        })
    passing = all(value >= 0 for value in all_margins)
    serial_segments = [segment.to_json() for segment in segments]
    inputs = {
        "benchmark_sha256": semantic_json_sha256(benchmark),
        "scene_sha256": semantic_json_sha256(scene),
        "horizon": qobj(horizon),
        "initial_state": [item.to_json() for item in initial_state],
    }
    result = {
        "schema": CHECK_SCHEMA,
        "inputs": inputs,
        "segments_sha256": semantic_json_sha256(serial_segments),
        "segments": serial_segments,
        "segment_count": len(segments),
        "full_closed_hold_covered": True,
        "fixed_label_semantics": "ONE_UNCHANGED_FULL_LABEL_IMAGE_ACROSS_ALL_SEGMENTS",
        "collision_pose_semantics": "STATE_HULL_ALREADY_INCLUDES_ANY_NATIVE_OR_ADAPTER_RADIUS; NO_SECOND_EXPANSION",
        "segment_checks": segment_checks,
        "predicate_status": "PASS_ON_SUPPLIED_TUBE" if passing else "UNKNOWN_ON_SUPPLIED_TUBE",
        "certificate_emitted": False,
        "ode_tube_proof_replayed": False,
        "shared_arithmetic": "validation.g2 exact-rational Interval/Budget; sqrt_lower",
        "work": {
            "max_rational_bits": budget.max_bits,
            "max_rational_operations": budget.max_operations,
            "operation_attempts": budget.operation_attempts,
            "operations_started": budget.operations,
            "completed_results": budget.completed_results,
            "max_preoperation_estimate_bits": budget.max_preoperation_estimate_bits,
            "max_completed_result_bits": budget.max_completed_result_bits,
            "max_observed_result_bits": budget.max_seen_bits,
        },
    }
    return result


def replay_common_check_record(
    record: dict[str, Any], benchmark: dict[str, Any], scene: dict[str, Any], budget: Budget,
    *, sqrt_bisections: int = 128,
) -> dict[str, Any]:
    """Reparse all segment fields and recompute the common predicate record."""
    if not isinstance(record, dict) or record.get("schema") != CHECK_SCHEMA:
        return {"replayed": False, "reason": "invalid_common_check_schema"}
    if not isinstance(record.get("segments"), list):
        return {"replayed": False, "reason": "missing_serialized_segments"}
    try:
        model = build_model(benchmark, budget)
        segments = tuple(TubeSegment.from_json(item, model.parameter_label_order, budget) for item in record["segments"])
        horizon = parse_q(record.get("inputs", {}).get("horizon"), budget)
        expected = check_tube_segments(
            segments, benchmark, scene, horizon, budget,
            initial_state=_parse_state_vector(record.get("inputs", {}).get("initial_state"), budget),
            sqrt_bisections=sqrt_bisections,
        )
    except (InvalidInput, KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        return {"replayed": False, "reason": "invalid_or_tampered_tube", "detail": str(exc)}
    if record != expected:
        return {"replayed": False, "reason": "common_check_record_mismatch"}
    return {
        "replayed": True,
        "predicate_status": expected["predicate_status"],
        "certificate_emitted": False,
    }
