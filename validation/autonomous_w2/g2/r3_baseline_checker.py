"""Replay one preserved R3 result and its independent endpoint-progress record."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import traceback
from pathlib import Path
from typing import Any

from validation.g2.checker import replay_record
from validation.g2.endpoint_checker_r2 import replay_progress_record
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


def audit(binding_path: Path, row_path: Path) -> dict[str, Any]:
    binding = json.loads(binding_path.read_text(encoding="utf-8"))
    row = json.loads(row_path.read_text(encoding="utf-8"))
    for rel, expected in binding["source_files"].items():
        if sha(ROOT / rel) != expected:
            raise ValueError(f"SOURCE_HASH_MISMATCH:{rel}")
    for path_key, hash_key in (
        ("r3_input_path", "r3_input_sha256"),
        ("r3_benchmark_path", "r3_benchmark_sha256"),
        ("r3_profile_path", "r3_profile_sha256"),
    ):
        if sha(ROOT / binding[path_key]) != binding[hash_key]:
            raise ValueError(f"FROZEN_R3_INPUT_HASH_MISMATCH:{path_key}")
    if row.get("schema") != "G2_W2_R3_BASELINE_ROW_v1" or row.get("binding_sha256") != sha(binding_path):
        raise ValueError("R3_RESULT_BINDING_OR_SCHEMA")
    if row.get("action_id") != binding["action_id"]:
        raise ValueError("R3_RESULT_ACTION_MISMATCH")
    query = build_query(binding, binding["action_id"])
    expected_query_hash = semantic_json_sha256({
        "query_id": query["query_id"],
        "state_cell": query["state_cell"],
        "scene": query["scene"],
        "horizon": query["horizon"],
        "action": query["action"],
        "parameter_cell": query["parameter_cell"],
        "profile": query["profile"],
        "hash_protocol_id": HASH_PROTOCOL_ID,
        "specification_bundle_sha256": query["specification_bundle_sha256"],
    })
    if row.get("r3_query_sha256") != expected_query_hash:
        raise ValueError("R3_QUERY_SEMANTIC_HASH_MISMATCH")
    safety = row["safety_record"]
    progress = row["progress_record"]
    safety_audit = replay_record(safety, query)
    if safety_audit.get("replayed") is True:
        progress_audit = replay_progress_record(progress, safety, query)
        progress_ok = progress_audit.get("replayed") is True
        progress_record = progress.get("proof", {})
        safety_proof = safety.get("proof", {})
        collision = safety_proof.get("collision", []) if isinstance(safety_proof, dict) else []
        return {
            "schema": "G2_W2_R3_REPLAY_AUDIT_v1",
            "audit_valid": progress_ok,
            "replayed": progress_ok,
            "record_integrity_valid": True,
            "resource_limited": False,
            "safety_status": safety.get("status"),
            "task_eligible": progress.get("task_eligible") if progress_ok else False,
            "progress_status": progress.get("status"),
            "progress_lower_m": progress_record.get("terminal_progress_lower"),
            "required_progress_m": progress_record.get("task_progress_threshold"),
            "contact_margin_lower_N": safety_proof.get("contact_margin_lower"),
            "collision_margin_lower_m": [item.get("margin_lower") for item in collision],
            "internal_full_width": safety_proof.get("full_internal_width"),
            "pose_full_width": safety_proof.get("pose_width"),
            "safety_replay": safety_audit,
            "progress_replay": progress_audit,
        }
    if safety_audit.get("resource_limited") is True and safety_audit.get("record_integrity_valid") is True:
        return {
            "schema": "G2_W2_R3_REPLAY_AUDIT_v1",
            "audit_valid": True,
            "replayed": False,
            "record_integrity_valid": True,
            "resource_limited": True,
            "safety_status": "UNKNOWN",
            "task_eligible": False,
            "reason_codes": safety.get("reason_codes"),
            "safety_replay": safety_audit,
            "progress_replay": {"replayed": False, "reason": "no proof-bearing full-hold range is available"},
        }
    return {
        "schema": "G2_W2_R3_REPLAY_AUDIT_v1",
        "audit_valid": False,
        "replayed": False,
        "record_integrity_valid": safety_audit.get("record_integrity_valid"),
        "resource_limited": False,
        "safety_status": safety.get("status"),
        "task_eligible": False,
        "safety_replay": safety_audit,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding", required=True)
    parser.add_argument("--record", required=True)
    args = parser.parse_args()
    binding = Path(args.binding)
    record = Path(args.record)
    if not binding.is_absolute():
        binding = ROOT / binding
    if not record.is_absolute():
        record = ROOT / record
    try:
        summary = audit(binding, record)
    except BaseException as exc:
        summary = {"schema": "G2_W2_R3_REPLAY_AUDIT_v1", "audit_valid": False, "error": f"{type(exc).__name__}:{exc}", "traceback": traceback.format_exc(limit=8)}
    sys.stdout.write(json.dumps(summary, sort_keys=True, separators=(",", ":")) + "\n")
    sys.stdout.flush()
    return 0 if summary.get("audit_valid") else 3


if __name__ == "__main__":
    raise SystemExit(main())
