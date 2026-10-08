"""Shared frozen task mapping and scoring helpers for W2 v6 development."""
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
PLAN_REL = Path("research/autonomous_w2/g4/matched_v6_task_development_v1")
G2_TASK_REL = Path("research/autonomous_w2/g2/task_protocol_v1.json")
G2_RELEASE_REL = Path("coordination/autonomous_w2/g2/releases/RELEASE_v6.json")
G2_ACTIONS = (
    "W2_G2_DEV_001_ZERO", "W2_G2_DEV_001_NOMINAL", "W2_G2_DEV_001_ALTERNATIVE",
)
STATE_ORDER = (
    "p_x", "p_y", "theta", "u", "r", "omega_L", "omega_R", "i_L", "i_R",
)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                     allow_nan=False).encode("utf-8")
    return sha256_bytes(raw)


def strict_json(path: Path) -> Any:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise InvalidInput(f"duplicate JSON key {key!r}: {path}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique,
                      parse_constant=lambda value: (_ for _ in ()).throw(
                          InvalidInput(f"non-finite JSON constant {value}: {path}")))


def rooted(path: str | Path) -> Path:
    value = Path(path)
    return value if value.is_absolute() else PROJECT / value


def write_json(path: Path, value: Any, *, max_bytes: int | None = None, exclusive: bool = True) -> tuple[str, int]:
    raw = (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")
    if max_bytes is not None and len(raw) > max_bytes:
        raise InvalidInput(f"SERIALIZED_OUTPUT_CAP:{len(raw)}>{max_bytes}")
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "xb" if exclusive else "wb"
    with path.open(mode) as stream:
        stream.write(raw)
        stream.flush()
    return sha256_bytes(raw), len(raw)


def load_protocol_and_freeze() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    freeze = strict_json(PROJECT / PLAN_REL / "freeze_manifest.json")
    protocol_path = rooted(freeze["protocol_path"])
    protocol = strict_json(protocol_path)
    benchmark_path = rooted(freeze["benchmark_path"])
    benchmark = strict_json(benchmark_path)
    if sha256_file(protocol_path) != freeze["protocol_sha256"]:
        raise InvalidInput("FROZEN_PROTOCOL_HASH_MISMATCH")
    if sha256_file(benchmark_path) != freeze["benchmark_sha256"]:
        raise InvalidInput("FROZEN_BENCHMARK_HASH_MISMATCH")
    release_path = PROJECT / G2_RELEASE_REL
    if sha256_file(release_path) != freeze["peer_release"]["sha256"]:
        raise InvalidInput("G2_V6_RELEASE_HASH_MISMATCH")
    task_path = PROJECT / G2_TASK_REL
    if sha256_file(task_path) != freeze["task_protocol"]["sha256"]:
        raise InvalidInput("G2_V6_TASK_PROTOCOL_HASH_MISMATCH")
    return freeze, protocol, benchmark


def verify_source_closure(freeze: dict[str, Any]) -> None:
    closure_path = rooted(freeze["source_closure_path"])
    if sha256_file(closure_path) != freeze["source_closure_sha256"]:
        raise InvalidInput("FROZEN_SOURCE_CLOSURE_MANIFEST_HASH_MISMATCH")
    closure = strict_json(closure_path)
    for item in closure["files"]:
        path = rooted(item["path"])
        if not path.is_file() or path.stat().st_size != item["size_bytes"] or sha256_file(path) != item["sha256"]:
            raise InvalidInput(f"FROZEN_SOURCE_CLOSURE_MEMBER_MISMATCH:{item['path']}")


def rational(s: str) -> dict[str, str]:
    value = Fraction(s)
    return {"num": str(value.numerator), "den": str(value.denominator)}


def interval_from_rationals(pair: list[str], budget: Budget) -> Interval:
    if not isinstance(pair, list) or len(pair) != 2:
        raise InvalidInput("EXPECTED_TWO_RATIONAL_ENDPOINTS")
    return Interval(Fraction(pair[0]), Fraction(pair[1]), budget)


def common_progress(segments: tuple[TubeSegment, ...], *, cosine_degree: int = 20) -> dict[str, Any]:
    """Identical sound slab integral of u*cos(theta) for both methods."""
    if not segments:
        raise InvalidInput("NO_SEGMENTS_FOR_PROGRESS")
    budget = segments[0].state_hull[0].budget
    total = Interval.point(Fraction(0), budget)
    slab_rows = []
    for segment in segments:
        duration = segment.t_end - segment.t_start
        u = segment.state_hull[3]
        theta = segment.state_hull[2]
        cos_theta = interval_cosine(theta, cosine_degree)
        rate = u * cos_theta
        contribution = rate.scale(duration)
        total = total + contribution
        slab_rows.append({
            "segment_id": segment.segment_id,
            "duration_s": qobj(duration),
            "u_interval_mps": u.to_json(),
            "theta_interval_rad": theta.to_json(),
            "cos_theta_enclosure": cos_theta.to_json(),
            "displacement_contribution_m": contribution.to_json(),
        })
    endpoint = Interval(
        segments[-1].endpoint_end[0].lo - segments[0].endpoint_start[0].hi,
        segments[-1].endpoint_end[0].hi - segments[0].endpoint_start[0].lo,
        budget,
    )
    lo, hi = max(total.lo, endpoint.lo), min(total.hi, endpoint.hi)
    if lo > hi:
        raise InvalidInput("PROGRESS_SLAB_AND_ENDPOINT_BOUNDS_DISJOINT")
    return {
        "schema": "ddwmr-g4-w2-common-integrated-progress-v1",
        "method": segments[0].provenance["method"],
        "formula": "sum over closed slabs of duration * interval(u * cos(theta))",
        "cosine_taylor_degree": cosine_degree,
        "progress_enclosure_m": [qobj(lo), qobj(hi)],
        "slab_integral_enclosure_m": total.to_json(),
        "endpoint_difference_enclosure_m": endpoint.to_json(),
        "slab_count": len(segments),
        "slabs": slab_rows,
    }


def configure_integer_string_limit(max_digits: int) -> None:
    if type(max_digits) is not int or max_digits < 640 or max_digits > 10000:
        raise InvalidInput("COMMON_INTEGER_STRING_DIGIT_CAP_INVALID")
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(max_digits)


def score_segments(
    segments: tuple[TubeSegment, ...], benchmark: dict[str, Any], scene: dict[str, Any],
    horizon: Fraction, initial_state: tuple[Interval, ...], *, sqrt_bisections: int,
    budget: Budget,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    if not segments:
        raise InvalidInput("NO_SEGMENTS_FOR_COMMON_PREDICATE")
    # The same exact-rational operations, scene, full label image and progress
    # scorer are used for both methods. The caller owns the Budget so the
    # segment adapter and scorer share one audited arithmetic resource counter.
    record = check_tube_segments(
        segments, benchmark, scene, horizon, budget,
        initial_state=initial_state, sqrt_bisections=sqrt_bisections,
    )
    replay = replay_common_check_record(
        record, benchmark, scene, budget, sqrt_bisections=sqrt_bisections,
    )
    progress = common_progress(segments)
    return record, replay, progress


def summarize_common(record: dict[str, Any]) -> dict[str, Any]:
    contact = [Fraction(item["contact"]["margin_lower"]["num"], item["contact"]["margin_lower"]["den"])
               for item in record.get("segment_checks", [])]
    collision = [Fraction(item["margin_lower"]["num"], item["margin_lower"]["den"])
                 for slab in record.get("segment_checks", []) for item in slab.get("collision", [])]
    return {
        "predicate_status": record.get("predicate_status"),
        "segment_count": record.get("segment_count"),
        "minimum_contact_margin_lower_N": qobj(min(contact)) if contact else None,
        "minimum_collision_margin_lower_m": qobj(min(collision)) if collision else None,
    }
