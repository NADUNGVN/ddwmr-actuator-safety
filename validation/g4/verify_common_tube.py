"""Focused synthetic checks for the shared G4 tube interface.

These fixtures test adapters and predicates only. They are not ODE trajectories,
benchmark query outputs, or safety certificates.
"""

from __future__ import annotations

import argparse
import copy
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from validation.g2.hashing import semantic_json_sha256
from validation.g2.model import build_model
from validation.g2.rational import Budget, Interval, InvalidInput, qobj
from validation.g4.common_tube import (
    AUER_NATIVE_SCHEMA,
    TubeSegment,
    auer_native_segment_to_common,
    binary64_hex_fraction,
    center_radius_to_hull,
    check_tube_segments,
    clip_value_interval,
    replay_common_check_record,
)


ROOT = Path(__file__).resolve().parents[2]


def _budget() -> Budget:
    return Budget(max_bits=16384, max_operations=1_000_000)


def _ival(lo: int | Fraction, hi: int | Fraction, budget: Budget) -> Interval:
    return Interval(Fraction(lo), Fraction(hi), budget)


def _zero_state(budget: Budget) -> tuple[Interval, ...]:
    return tuple(Interval.point(Fraction(0), budget) for _ in range(9))


def _labels(benchmark: dict[str, Any], budget: Budget) -> tuple[tuple[str, Interval], ...]:
    model = build_model(benchmark, budget)
    return tuple((name, model.parameter_label_box[name]) for name in model.parameter_label_order)


def _segment(
    segment_id: str,
    start: Fraction,
    end: Fraction,
    hull: tuple[Interval, ...],
    labels: tuple[tuple[str, Interval], ...],
    *,
    endpoint_start: tuple[Interval, ...] | None = None,
    endpoint_end: tuple[Interval, ...] | None = None,
) -> TubeSegment:
    return TubeSegment.from_total_hull(
        segment_id=segment_id,
        t_start=start,
        t_end=end,
        state_hull=hull,
        labels=labels,
        endpoint_start=endpoint_start or hull,
        endpoint_end=endpoint_end or hull,
        radius_expansion_count=0,
        radius_expansion_mode="NATIVE_TOTAL_HULL",
        provenance={"fixture": True, "physical_trajectory_claim": False},
    )


def _expect_invalid(callable_, text: str) -> None:
    try:
        callable_()
    except InvalidInput:
        return
    raise AssertionError(text)


def _scene(identifier: str, x: Fraction, y: Fraction, radius: Fraction = Fraction(1, 2)) -> dict[str, Any]:
    return {"id": identifier, "p_o": [qobj(x), qobj(y)], "R_s": qobj(radius)}


def _hex_point(value: str) -> list[str]:
    return [value, value]


def _run(benchmark: dict[str, Any]) -> dict[str, Any]:
    horizon = Fraction(1, 10)
    out: dict[str, Any] = {
        "schema": "ddwmr-g4-common-tube-preflight-v1",
        "scope": "SYNTHETIC_INTERFACE_FIXTURES_ONLY",
        "not_ode_trajectories": True,
        "not_safety_certificates": True,
        "matched_query_evaluations": 0,
        "checks": {},
    }

    # A two-slab positive predicate fixture tests exact shared-boundary handling.
    b_pos = _budget()
    labels_pos = _labels(benchmark, b_pos)
    state_zero = _zero_state(b_pos)
    mid = Fraction(1, 20)
    positive_segments = (
        _segment("pass-0", Fraction(0), mid, state_zero, labels_pos),
        _segment("pass-1", mid, horizon, state_zero, labels_pos),
    )
    far_scene = _scene("fixture-far-obstacle", Fraction(10), Fraction(10))
    positive = check_tube_segments(
        positive_segments, benchmark, far_scene, horizon, b_pos,
        initial_state=state_zero, sqrt_bisections=64,
    )
    assert positive["predicate_status"] == "PASS_ON_SUPPLIED_TUBE"
    assert positive["certificate_emitted"] is False
    b_pos_replay = _budget()
    positive_replay = replay_common_check_record(
        positive, benchmark, far_scene, b_pos_replay, sqrt_bisections=64,
    )
    assert positive_replay["replayed"] is True
    out["checks"]["positive_two_closed_slabs"] = {
        "status": positive["predicate_status"],
        "replay": positive_replay,
        "segment_count": positive["segment_count"],
        "contact_margins": [item["contact"]["margin_lower"] for item in positive["segment_checks"]],
        "collision_margins": [[ob["margin_lower"] for ob in item["collision"]] for item in positive["segment_checks"]],
    }

    # A hull crosses the obstacle although its two endpoint boxes are clear.
    # The full-time checker must therefore return UNKNOWN.
    b_unknown = _budget()
    labels_unknown = _labels(benchmark, b_unknown)
    full_hull = list(_zero_state(b_unknown))
    full_hull[0] = _ival(-2, 2, b_unknown)
    start_state = list(_zero_state(b_unknown))
    start_state[0] = Interval.point(Fraction(-2), b_unknown)
    end_state = list(_zero_state(b_unknown))
    end_state[0] = Interval.point(Fraction(2), b_unknown)
    crossing = _segment(
        "crossing-full-time-hull", Fraction(0), horizon, tuple(full_hull), labels_unknown,
        endpoint_start=tuple(start_state), endpoint_end=tuple(end_state),
    )
    near_scene = _scene("fixture-center-obstacle", Fraction(0), Fraction(0))
    unknown = check_tube_segments(
        (crossing,), benchmark, near_scene, horizon, b_unknown,
        initial_state=tuple(start_state), sqrt_bisections=64,
    )
    assert unknown["predicate_status"] == "UNKNOWN_ON_SUPPLIED_TUBE"
    assert unknown["certificate_emitted"] is False
    unknown_replay = replay_common_check_record(
        unknown, benchmark, near_scene, _budget(), sqrt_bisections=64,
    )
    assert unknown_replay["replayed"] is True
    collision = unknown["segment_checks"][0]["collision"][0]
    endpoint_margin = Fraction(3, 2)
    assert parse_q_local(collision["margin_lower"]) < 0 and endpoint_margin > 0
    out["checks"]["full_time_overrides_clear_endpoints"] = {
        "status": unknown["predicate_status"],
        "replay": unknown_replay,
        "full_hull_collision_margin": collision["margin_lower"],
        "both_endpoint_only_clearance_margins": [qobj(endpoint_margin), qobj(endpoint_margin)],
    }

    # Gaps and any change in the fixed parameter image are rejected.
    b_bad = _budget()
    labels_bad = _labels(benchmark, b_bad)
    zero_bad = _zero_state(b_bad)
    first = _segment("left", Fraction(0), mid, zero_bad, labels_bad)
    gap = _segment("right-gap", Fraction(3, 50), horizon, zero_bad, labels_bad)
    _expect_invalid(
        lambda: check_tube_segments(
            (first, gap), benchmark, far_scene, horizon, b_bad, initial_state=zero_bad,
        ),
        "time gap was not rejected",
    )
    changed = list(labels_bad)
    label_name, label_range = changed[0]
    changed[0] = (label_name, Interval(label_range.lo, label_range.hi - Fraction(1, 100), b_bad))
    altered_labels = _segment("right-label-change", mid, horizon, zero_bad, tuple(changed))
    _expect_invalid(
        lambda: check_tube_segments(
            (first, altered_labels), benchmark, far_scene, horizon, b_bad, initial_state=zero_bad,
        ),
        "parameter label change was not rejected",
    )
    out["checks"]["coverage_gap_rejected"] = True
    out["checks"]["fixed_label_change_rejected"] = True

    # Radius-once and exact binary64 conversion contract.
    b_radius = _budget()
    expanded = center_radius_to_hull((_ival(1, 2, b_radius),), (Fraction(1, 4),), b_radius)[0]
    assert expanded.lo == Fraction(3, 4) and expanded.hi == Fraction(9, 4)
    binary_01 = binary64_hex_fraction("0x1.999999999999ap-4")
    assert binary_01 == Fraction(3602879701896397, 36028797018963968)
    out["checks"]["radius_expanded_once"] = {
        "input_center": [_ival(1, 2, b_radius).to_json()],
        "radius": qobj(Fraction(1, 4)),
        "expanded_hull": expanded.to_json(),
        "expansion_count": 1,
    }
    out["checks"]["binary64_exact_rational_conversion"] = {
        "hex": "0x1.999999999999ap-4",
        "exact_rational": qobj(binary_01),
        "conversion_is_exact_for_represented_float": True,
    }

    # The Auer input adapter adds x_app and the full-step residual once, and
    # refuses the old VALENCIA endpoint text representation by schema.
    b_auer = _budget()
    labels_auer = _labels(benchmark, b_auer)
    labels_json = {name: item.to_json() for name, item in labels_auer}
    zero_hex = [_hex_point("0x0p+0") for _ in range(9)]
    auer_raw = {
        "schema": AUER_NATIVE_SCHEMA,
        "segment_id": "synthetic-auer-adapter-fixture",
        "time_start": qobj(Fraction(0)),
        "time_end": qobj(horizon),
        "x_app_step_range_hex": zero_hex,
        "residual_step_range_hex": zero_hex,
        "labels": labels_json,
        "endpoint_start_hex": zero_hex,
        "endpoint_end_hex": zero_hex,
        "proof_record_sha256": semantic_json_sha256({"fixture": "not-a-proof"}),
        "method_id": "TEST_FIXTURE_ONLY",
    }
    auer_segment = auer_native_segment_to_common(auer_raw, benchmark, b_auer)
    assert auer_segment.radius_expansion_count == 1
    assert all(part.lo == part.hi == 0 for part in auer_segment.state_hull)
    out["checks"]["auer_adapter_full_step_schema"] = {
        "schema": auer_raw["schema"],
        "radius_expansion_count": auer_segment.radius_expansion_count,
        "state_hull_is_total": True,
        "fixture_only": True,
    }

    # The clip value enclosure remains safe at and across saturation corners.
    b_clip = _budget()
    exactly_one = clip_value_interval(Interval.point(Fraction(1), b_clip))
    across_one = clip_value_interval(Interval(Fraction(999, 1000), Fraction(1001, 1000), b_clip))
    assert exactly_one.lo == exactly_one.hi == 1
    assert across_one.lo == Fraction(999, 1000) and across_one.hi == 1
    out["checks"]["saturated_clip_corner"] = {
        "at_one": exactly_one.to_json(),
        "crossing_one": across_one.to_json(),
        "contact_checker_uses_exact_clip_value_range": True,
    }

    # A changed enclosure cannot reuse a formerly replayed predicate record.
    tampered = copy.deepcopy(positive)
    tampered["segments"][0]["state_hull"][0] = [qobj(Fraction(-1)), qobj(Fraction(0))]
    tamper_result = replay_common_check_record(
        tampered, benchmark, far_scene, _budget(), sqrt_bisections=64,
    )
    assert tamper_result["replayed"] is False
    out["checks"]["tampered_enclosure_rejected"] = tamper_result

    out["check_count"] = len(out["checks"])
    out["positive_fixture_record"] = positive
    out["unknown_fixture_record"] = unknown
    return out


def parse_q_local(raw: dict[str, str]) -> Fraction:
    return Fraction(int(raw["num"]), int(raw["den"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", type=Path, default=ROOT / "validation/configs/benchmark_v1.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    benchmark = json.loads(args.benchmark.read_text(encoding="utf-8"))
    result = _run(benchmark)
    payload = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": "PASS_FOR_COMMON_TUBE_INTERFACE_FIXTURES_ONLY",
        "checks": result["check_count"],
        "matched_query_evaluations": result["matched_query_evaluations"],
        "output": str(args.output) if args.output else None,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
