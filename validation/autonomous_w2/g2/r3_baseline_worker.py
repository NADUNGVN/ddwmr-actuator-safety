"""Run one W2-declared task row through the preserved R3 evaluator."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import traceback
from pathlib import Path
from typing import Any

from validation.g2.endpoint_r2 import make_progress_record
from validation.g2.evaluator import run_query
from validation.g2.hashing import HASH_PROTOCOL_ID, semantic_json_sha256


ROOT = Path(__file__).resolve().parents[3]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_query(binding: dict[str, Any], action_id: str) -> dict[str, Any]:
    inp = json.loads((ROOT / binding["r3_input_path"]).read_text(encoding="utf-8"))
    benchmark = json.loads((ROOT / binding["r3_benchmark_path"]).read_text(encoding="utf-8"))
    profile = json.loads((ROOT / binding["r3_profile_path"]).read_text(encoding="utf-8"))
    matches = [item for item in inp["query_actions"] if item["action"]["id"] == action_id]
    if len(matches) != 1:
        raise ValueError("R3_ACTION_ID_NOT_UNIQUE")
    action_entry = matches[0]
    return {
        "query_id": action_entry["query_id"],
        "state_cell": inp["state_cell"],
        "scene": inp["scene"],
        "horizon": inp["horizon"],
        "action": action_entry["action"],
        "parameter_cell": benchmark["parameter_cell"],
        "profile": profile,
        "benchmark": benchmark,
        "benchmark_sha256": binding["r3_benchmark_sha256"],
        "development_manifest_sha256": binding["r3_input_sha256"],
        "hash_protocol_id": HASH_PROTOCOL_ID,
        "specification_bundle_sha256": profile["specification_bundle_sha256"],
        "task_progress_threshold": inp["task_progress_threshold"],
    }


def execute(binding_path: Path, action_id: str) -> dict[str, Any]:
    binding = json.loads(binding_path.read_text(encoding="utf-8"))
    for rel, expected in binding["source_files"].items():
        if sha(ROOT / rel) != expected:
            raise ValueError(f"SOURCE_HASH_MISMATCH:{rel}")
    if binding.get("method") != "legacy_r3" or binding.get("action_id") != action_id:
        raise ValueError("R3_BINDING_METHOD_OR_ACTION_MISMATCH")
    for path_key, hash_key in (
        ("r3_input_path", "r3_input_sha256"),
        ("r3_benchmark_path", "r3_benchmark_sha256"),
        ("r3_profile_path", "r3_profile_sha256"),
    ):
        if sha(ROOT / binding[path_key]) != binding[hash_key]:
            raise ValueError(f"FROZEN_R3_INPUT_HASH_MISMATCH:{path_key}")
    query = build_query(binding, action_id)
    source_commit = json.loads((ROOT / binding["r3_input_path"]).read_text(encoding="utf-8"))["source_commit"]
    record = run_query(query, source_commit)
    progress_record = make_progress_record(record, query)
    return {
        "schema": "G2_W2_R3_BASELINE_ROW_v1",
        "method": "R3_COMP_CLIP_WHOLE_HOLD_DYADIC_DISTANCE_V1",
        "action_id": action_id,
        "query_id": query["query_id"],
        "binding_sha256": sha(binding_path),
        "r3_query_sha256": semantic_json_sha256({
            "query_id": query["query_id"],
            "state_cell": query["state_cell"],
            "scene": query["scene"],
            "horizon": query["horizon"],
            "action": query["action"],
            "parameter_cell": query["parameter_cell"],
            "profile": query["profile"],
            "hash_protocol_id": HASH_PROTOCOL_ID,
            "specification_bundle_sha256": query["specification_bundle_sha256"],
        }),
        "safety_record": record,
        "progress_record": progress_record,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding", required=True)
    parser.add_argument("--action-id", required=True)
    args = parser.parse_args()
    path = Path(args.binding)
    if not path.is_absolute():
        path = ROOT / path
    try:
        result = execute(path, args.action_id)
    except BaseException as exc:
        result = {
            "schema": "G2_W2_R3_WORKER_FAILURE_v1",
            "status": "EXECUTION_FAILURE",
            "reason_code": f"{type(exc).__name__}:{exc}",
            "traceback": traceback.format_exc(limit=8),
        }
    sys.stdout.write(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
