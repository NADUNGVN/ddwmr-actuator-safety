"""Shared immutable inputs/scorer helpers for the G4 W2 v6 matched task."""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

from validation.g2.interval import interval_cosine
from validation.g2.rational import Budget, Interval, InvalidInput, qobj, parse_q
from validation.g4.common_tube import TubeSegment, check_tube_segments, replay_common_check_record

PROJECT = Path(__file__).resolve().parents[3]
PLAN_REL = Path("research/autonomous_w2/g4/matched_v6_task_development_v2")
RESULT_REL = Path("results/validation/autonomous_w2/g4/matched_v6_task_development_v2")
STATE_ORDER = ("p_x", "p_y", "theta", "u", "r", "omega_L", "omega_R", "i_L", "i_R")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def strict_json(path: Path) -> Any:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            if key in output:
                raise InvalidInput(f"DUPLICATE_JSON_KEY:{path}:{key}")
            output[key] = value
        return output
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique,
                      parse_constant=lambda value: (_ for _ in ()).throw(InvalidInput(f"NONFINITE_JSON:{path}:{value}")))


def write_json(path: Path, value: Any, *, max_bytes: int | None = None, exclusive: bool = False) -> tuple[str, int]:
    raw = (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")
    if max_bytes is not None and len(raw) > max_bytes:
        raise InvalidInput(f"SERIALIZED_OUTPUT_CAP:{len(raw)}>{max_bytes}")
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "xb" if exclusive else "wb"
    with path.open(mode) as stream:
        stream.write(raw)
        stream.flush()
    return hashlib.sha256(raw).hexdigest(), len(raw)


def common_progress(segments: tuple[TubeSegment, ...], *, cosine_degree: int = 20) -> dict[str, Any]:
    if not segments:
        raise InvalidInput("NO_SEGMENTS_FOR_PROGRESS")
    budget = segments[0].state_hull[0].budget
    total = Interval.point(Fraction(0), budget)
    slab_rows = []
    for segment in segments:
        duration = segment.t_end - segment.t_start
        contribution = (segment.state_hull[3] * interval_cosine(segment.state_hull[2], cosine_degree)).scale(duration)
        total = total + contribution
        slab_rows.append({
            "segment_id": segment.segment_id,
            "duration_s": qobj(duration),
            "u_interval_mps": segment.state_hull[3].to_json(),
            "theta_interval_rad": segment.state_hull[2].to_json(),
            "displacement_contribution_m": contribution.to_json(),
        })
    endpoint = Interval(
        segments[-1].endpoint_end[0].lo - segments[0].endpoint_start[0].hi,
        segments[-1].endpoint_end[0].hi - segments[0].endpoint_start[0].lo,
        budget,
    )
    lo, hi = max(total.lo, endpoint.lo), min(total.hi, endpoint.hi)
    if lo > hi:
        raise InvalidInput("COMMON_PROGRESS_SLAb_AND_ENDPOINT_DISJOINT")
    return {
        "schema": "ddwmr-g4-w2-common-integrated-progress-v2",
        "formula": "intersection of closed-slab sum(duration * interval(u*cos(theta))) and endpoint displacement enclosure",
        "cosine_taylor_degree": cosine_degree,
        "progress_enclosure_m": [qobj(lo), qobj(hi)],
        "slab_integral_enclosure_m": total.to_json(),
        "endpoint_difference_enclosure_m": endpoint.to_json(),
        "slab_count": len(segments),
        "slabs": slab_rows,
    }


def score_segments(
    segments: tuple[TubeSegment, ...], benchmark: dict[str, Any], scene: dict[str, Any],
    horizon: Fraction, initial_state: tuple[Interval, ...], *, sqrt_bisections: int,
    budget: Budget,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    record = check_tube_segments(
        segments, benchmark, scene, horizon, budget,
        initial_state=initial_state, sqrt_bisections=sqrt_bisections,
    )
    replay = replay_common_check_record(record, benchmark, scene, budget, sqrt_bisections=sqrt_bisections)
    progress = common_progress(segments)
    return record, replay, progress


def score_serialize_replay_progress(
    segments: tuple[TubeSegment, ...], benchmark: dict[str, Any], scene: dict[str, Any],
    horizon: Fraction, initial_state: tuple[Interval, ...], *, sqrt_bisections: int,
    budget: Budget, common_record_path: Path, progress_path: Path,
    max_record_bytes: int = 8_388_608, max_progress_bytes: int = 1_048_576,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Score once, serialize/reparse the record, then independently replay its bytes."""
    record = check_tube_segments(
        segments, benchmark, scene, horizon, budget,
        initial_state=initial_state, sqrt_bisections=sqrt_bisections,
    )
    record_sha, record_bytes = write_json(common_record_path, record, max_bytes=max_record_bytes)
    parsed = strict_json(common_record_path)
    replay = replay_common_record_semantics(
        parsed, benchmark, scene, budget, sqrt_bisections=sqrt_bisections,
    )
    expected_progress = common_progress(segments)
    progress_sha, progress_bytes = write_json(progress_path, expected_progress, max_bytes=max_progress_bytes)
    progress = strict_json(progress_path)
    progress_replay = replay_common_progress_record(parsed, progress, benchmark, budget)
    replay["progress_replay"] = progress_replay
    if not progress_replay.get("replayed"):
        raise InvalidInput(f"COMMON_PROGRESS_REPLAY_FAILED:{progress_replay}")
    return parsed, replay, progress, {
        "common_record_sha256": record_sha,
        "common_record_bytes": record_bytes,
        "progress_sha256": progress_sha,
        "progress_bytes": progress_bytes,
        "record_reparsed_before_replay": True,
        "progress_reparsed_before_replay": True,
    }


def replay_common_record_semantics(
    record: dict[str, Any], benchmark: dict[str, Any], scene: dict[str, Any], budget: Budget,
    *, sqrt_bisections: int = 128,
) -> dict[str, Any]:
    """Recompute the common predicate record and compare every semantic field.

    ``work`` is intentionally excluded from equality: it is diagnostic
    accounting that depends on prior operations on a shared Budget instance.
    The replay instead returns its own exact arithmetic counters, while all
    serialized inputs, enclosures, margins and predicate statuses must match.
    """
    if not isinstance(record, dict) or record.get("schema") != "ddwmr-g4-common-tube-check-v1":
        return {"replayed": False, "reason": "invalid_common_check_schema"}
    if not isinstance(record.get("segments"), list):
        return {"replayed": False, "reason": "missing_serialized_segments"}
    try:
        from validation.g4.common_tube import TubeSegment, check_tube_segments
        from validation.g2.model import build_model

        model = build_model(benchmark, budget)
        segments = tuple(TubeSegment.from_json(item, model.parameter_label_order, budget) for item in record["segments"])
        horizon = parse_q(record.get("inputs", {}).get("horizon"), budget)
        initial_raw = record.get("inputs", {}).get("initial_state")
        if not isinstance(initial_raw, list) or len(initial_raw) != len(STATE_ORDER):
            raise InvalidInput("common replay initial-state shape mismatch")
        initial = tuple(Interval.from_json(item, budget) for item in initial_raw)
        expected = check_tube_segments(
            segments, benchmark, scene, horizon, budget,
            initial_state=initial, sqrt_bisections=sqrt_bisections,
        )
    except (InvalidInput, KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        return {"replayed": False, "reason": "invalid_or_tampered_tube", "detail": str(exc)}
    actual_semantic = {key: value for key, value in record.items() if key != "work"}
    expected_semantic = {key: value for key, value in expected.items() if key != "work"}
    if actual_semantic != expected_semantic:
        return {"replayed": False, "reason": "common_semantic_record_mismatch"}
    return {
        "replayed": True,
        "predicate_status": expected["predicate_status"],
        "certificate_emitted": False,
        "semantic_fields_compared": sorted(expected_semantic),
        "recorded_work_counters_trusted": False,
        "replay_work": expected["work"],
    }


def replay_common_progress_record(
    common_record: dict[str, Any], progress_record: dict[str, Any], benchmark: dict[str, Any], budget: Budget,
) -> dict[str, Any]:
    """Recompute the progress enclosure from the serialized common segments."""
    try:
        parameter_order = [item["name"] for item in benchmark["parameter_labels"]]
        # The serialized common record retains all full-hold segment data.  Its
        # method-native proof is independently replayed before this function.
        segments = tuple(TubeSegment.from_json(item, parameter_order, budget)
                         for item in common_record["segments"])
        expected = common_progress(segments)
    except (InvalidInput, KeyError, TypeError, ValueError) as exc:
        return {"replayed": False, "reason": "invalid_serialized_common_segments", "detail": str(exc)}
    if progress_record != expected:
        return {"replayed": False, "reason": "progress_record_mismatch"}
    return {
        "replayed": True,
        "method": "recomputed from serialized full-slab tube segments and endpoint boxes",
        "slab_count": expected["slab_count"],
        "enclosure_m": expected["progress_enclosure_m"],
    }


def summarize_common(record: dict[str, Any]) -> dict[str, Any]:
    contact = [Fraction(int(item["contact"]["margin_lower"]["num"]), int(item["contact"]["margin_lower"]["den"]))
               for item in record.get("segment_checks", [])]
    collision = [Fraction(int(item["margin_lower"]["num"]), int(item["margin_lower"]["den"]))
                 for slab in record.get("segment_checks", []) for item in slab.get("collision", [])]
    return {
        "predicate_status": record.get("predicate_status"),
        "segment_count": record.get("segment_count"),
        "minimum_contact_margin_lower_N": qobj(min(contact)) if contact else None,
        "minimum_collision_margin_lower_m": qobj(min(collision)) if collision else None,
    }


def configure_integer_string_limit(max_digits: int) -> None:
    if type(max_digits) is not int or max_digits < 640 or max_digits > 10000:
        raise InvalidInput("COMMON_INTEGER_STRING_DIGIT_CAP_INVALID")
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(max_digits)


def canonical_q(value: str) -> dict[str, str]:
    rational = Fraction(value)
    return {"num": str(rational.numerator), "den": str(rational.denominator)}


def scene_from_task(task: dict[str, Any]) -> dict[str, Any]:
    obstacle = task["task"]["obstacle"]
    return {
        "id": "scene_v6_static_circle",
        "p_o": [canonical_q(value) for value in obstacle["center_m"]],
        "R_s": canonical_q(obstacle["inflated_radius_m"]),
    }


def initial_state_from_task(task: dict[str, Any], budget: Budget) -> tuple[Interval, ...]:
    return tuple(Interval(Fraction(lower), Fraction(upper), budget)
                 for lower, upper in task["task"]["initial_box"])


def load_freeze() -> tuple[dict[str, Any], dict[str, Any]]:
    receipt = strict_json(PROJECT / RESULT_REL / "freeze_receipt_v2.json")
    manifest_path = PROJECT / receipt["freeze_manifest_path"]
    if sha256_file(manifest_path) != receipt["freeze_manifest_sha256"]:
        raise InvalidInput("FROZEN_MANIFEST_SHA_MISMATCH")
    freeze = strict_json(manifest_path)
    if receipt["protocol_sha256"] != freeze["protocol_sha256"]:
        raise InvalidInput("FREEZE_RECEIPT_PROTOCOL_HASH")
    return freeze, receipt


def verify_source_closure(freeze: dict[str, Any]) -> dict[str, Any]:
    closure_path = PROJECT / freeze["source_closure_path"]
    if sha256_file(closure_path) != freeze["source_closure_sha256"]:
        raise InvalidInput("SOURCE_CLOSURE_HASH_MISMATCH")
    closure = strict_json(closure_path)
    for item in closure["files"]:
        path = PROJECT / item["path"]
        if not path.is_file() or path.stat().st_size != item["size_bytes"] or sha256_file(path) != item["sha256"]:
            raise InvalidInput(f"SOURCE_CLOSURE_FILE_MISMATCH:{item['path']}")
    return closure
