"""G4-owned adapter from the local Auer proof to the common W2 tube contract.

This is a path/input-binding adaptation only. It does not alter the residual
solver or the independent native replay. The adapter reopens exact proof bytes,
checks the semantic envelope digest, and emits native total hulls without a
second radius expansion.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from validation.g2.rational import Budget, InvalidInput, Interval, parse_q
from validation.g4.common_tube import TubeSegment


def canonical_sha256(value: Any) -> str:
    raw = (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_json_bytes(raw: bytes, *, label: str) -> Any:
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_unique(label))


def _unique(label: str):
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise InvalidInput(f"duplicate JSON key {key!r} in {label}")
            result[key] = value
        return result
    return hook


def make_segments(
    envelope: dict[str, Any], case: dict[str, Any], proof_path: Path, budget: Budget,
    *, source_binding: dict[str, Any], benchmark: dict[str, Any], method: str = "auer",
) -> tuple[TubeSegment, ...]:
    path = proof_path.resolve()
    if not path.is_file():
        raise InvalidInput("AUER_PROOF_FILE_MISSING")
    raw = path.read_bytes()
    stored = strict_json_bytes(raw, label=str(path))
    if stored != envelope or set(stored) != {"proof", "proof_sha256"}:
        raise InvalidInput("AUER_PROOF_ENVELOPE_BYTES_CHANGED")
    proof = stored["proof"]
    if not isinstance(proof, dict) or stored["proof_sha256"] != canonical_sha256(proof):
        raise InvalidInput("AUER_PROOF_SEMANTIC_DIGEST_MISMATCH")
    if proof.get("query_id") != case.get("query_id") or proof.get("status") != "PROOF_COMPLETE":
        raise InvalidInput("AUER_PROOF_QUERY_OR_STATUS_BINDING")
    binding = proof.get("binding")
    if not isinstance(binding, dict) or binding != source_binding:
        raise InvalidInput("AUER_PROOF_SOURCE_BINDING_MISMATCH")
    names = [item["name"] for item in benchmark["parameter_labels"]]
    labels = tuple((name, Interval.from_json(case["fixed_labels"][name], budget)) for name in names)
    records = proof.get("step_records")
    if not isinstance(records, list) or not records:
        raise InvalidInput("AUER_PROOF_HAS_NO_FULL_TIME_STEPS")
    file_sha = sha256_file(path)
    segments: list[TubeSegment] = []
    previous_end = None
    for index, step in enumerate(records):
        t_start = parse_q(step["time_closed"]["start"], budget)
        t_end = parse_q(step["time_closed"]["end"], budget)
        if previous_end is not None and previous_end != t_start:
            raise InvalidInput("AUER_STEP_CHAIN_GAP_OR_OVERLAP")
        hull = tuple(Interval.from_json(row, budget) for row in step["full_time_total_hull_augmented"][:9])
        endpoint_start = tuple(Interval.from_json(row, budget) for row in step["endpoint_start_augmented"][:9])
        endpoint_end = tuple(Interval.from_json(row, budget) for row in step["endpoint_end_augmented"][:9])
        segments.append(TubeSegment.from_total_hull(
            segment_id=f"AUER-W2:{case['query_id']}:{index}", t_start=t_start, t_end=t_end,
            state_hull=hull, labels=labels, endpoint_start=endpoint_start, endpoint_end=endpoint_end,
            radius_expansion_count=0, radius_expansion_mode="NATIVE_TOTAL_HULL",
            provenance={
                "method": method,
                "native_method_id": proof["method_id"],
                "native_proof_sha256": stored["proof_sha256"],
                "native_proof_file_sha256": file_sha,
                "w2_source_closure_path": source_binding["source_closure_path"],
                "w2_source_closure_sha256": source_binding["source_closure_sha256"],
                "w2_benchmark_path": source_binding["benchmark_path"],
                "w2_benchmark_sha256": source_binding["benchmark_sha256"],
                "enclosure_representation": "NATIVE_TOTAL_HULL",
            },
        ))
        previous_end = t_end
    if segments[0].t_start != 0 or segments[-1].t_end != parse_q(case["horizon"], budget):
        raise InvalidInput("AUER_STEPS_DO_NOT_COVER_CLOSED_HOLD")
    return tuple(segments)
