"""Check every frozen comparison path/hash pair without invoking a producer."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from validation.autonomous_w2.g4.matched_v6_common_v2 import (
    PROJECT, PLAN_REL, RESULT_REL, canonical_sha256, sha256_file, strict_json, write_json,
)


def verify() -> dict[str, Any]:
    plan = PROJECT / PLAN_REL
    result = PROJECT / RESULT_REL
    protocol = strict_json(plan / "protocol_v2.json")
    task = strict_json(PROJECT / "research/autonomous_w2/g2/task_protocol_v1.json")
    benchmark = strict_json(plan / "benchmark_v2.json")
    auer_manifest = strict_json(plan / "auer_input_manifest_v2.json")
    auer_bindings = strict_json(plan / "auer_bindings_v2.json")
    snapshot = strict_json(plan / "native_source_snapshot_v2.json")
    auer_profile_sha = sha256_file(plan / "auer_profile_v2.json")
    snapshot_sha = sha256_file(plan / "native_source_snapshot_v2.json")
    pairs = []
    checked_pairs = 0
    source_hash_checks = 0
    snapshot_hash_checks = 0
    for entry in snapshot["copies"]:
        origin = PROJECT / entry["origin_path"]
        copied = PROJECT / entry["snapshot_path"]
        if sha256_file(origin) != entry["origin_sha256"] or sha256_file(copied) != entry["snapshot_sha256"]:
            raise ValueError(f"NATIVE_SNAPSHOT_HASH_MISMATCH:{entry['snapshot_path']}")
        source_hash_checks += 2
        if entry["adaptations"] == ["none; byte-identical snapshot"] and origin.read_bytes() != copied.read_bytes():
            raise ValueError(f"EXPECTED_IDENTICAL_SNAPSHOT_DIFFERS:{entry['snapshot_path']}")
        snapshot_hash_checks += 1
    auer_by_id = {item["comparison_id"]: item for item in auer_manifest["cases"]}
    native_by_id = {item["comparison_id"]: item for item in auer_bindings["bindings"]}
    for ordinal, action in enumerate(protocol["actions"], 1):
        external = action["comparison_id"]
        v6_path = plan / "v6_bindings" / f"{ordinal:02d}.json"
        v6 = strict_json(v6_path)
        if v6.get("binding_path") != v6_path.relative_to(PROJECT).as_posix():
            raise ValueError(f"V6_BINDING_PATH:{external}")
        if sha256_file(v6_path) != action["native_binding_sha256"]:
            raise ValueError(f"V6_BINDING_HASH:{external}")
        if v6.get("comparison_id") != external or v6.get("physical_input_sha256") != action["physical_input_sha256"]:
            raise ValueError(f"V6_BINDING_ID_OR_PHYSICAL_HASH:{external}")
        if v6.get("source_snapshot_manifest_sha256") != sha256_file(plan / "native_source_snapshot_v2.json"):
            raise ValueError(f"V6_SOURCE_SNAPSHOT_BINDING:{external}")
        core_path = PROJECT / v6["core_binding_path"]
        saved_path = PROJECT / v6["peer_saved_row_path"]
        if sha256_file(core_path) != v6["core_binding_sha256"] or v6["source_files"].get(v6["core_binding_path"]) != v6["core_binding_sha256"]:
            raise ValueError(f"V6_CORE_BINDING_PATH_HASH:{external}")
        if sha256_file(saved_path) != v6["peer_saved_row_sha256"]:
            raise ValueError(f"V6_SAVED_ROW_HASH:{external}")
        for rel, digest in v6["source_files"].items():
            path = PROJECT / rel
            if not path.is_file() or sha256_file(path) != digest:
                raise ValueError(f"V6_SOURCE_PATH_HASH:{external}:{rel}")
            source_hash_checks += 1

        auer_id = action["auer_id"]
        case = auer_by_id.get(auer_id)
        binding = native_by_id.get(auer_id)
        if case is None or binding is None:
            raise ValueError(f"AUER_CASE_BINDING_MISSING:{auer_id}")
        case_path = PROJECT / case["native_case_path"]
        if sha256_file(case_path) != case["native_case_sha256"] or case["physical_input_sha256"] != action["physical_input_sha256"]:
            raise ValueError(f"AUER_NATIVE_CASE_PATH_HASH:{auer_id}")
        if case["native_case_path"] != action["auer_native_input_path"] or case["native_case_sha256"] != action["auer_native_input_file_sha256"]:
            raise ValueError(f"AUER_PROTOCOL_CASE_PATH_HASH:{auer_id}")
        native_binding = binding["native_binding"]
        binding_digest = hashlib.sha256(json.dumps(native_binding, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n").hexdigest()
        if binding_digest != action["auer_native_binding_sha256"]:
            raise ValueError(f"AUER_BINDING_HASH:{auer_id}")
        if native_binding.get("input_path") != case["native_case_path"] or native_binding.get("input_sha256") != case["native_case_sha256"]:
            raise ValueError(f"AUER_BINDING_NATIVE_INPUT:{auer_id}")
        if native_binding.get("resource_profile_sha256") != sha256_file(plan / "auer_profile_v2.json"):
            raise ValueError(f"AUER_BINDING_PROFILE:{auer_id}")
        if native_binding.get("resource_profile_path") != "research/autonomous_w2/g4/matched_v6_task_development_v2/auer_profile_v2.json":
            raise ValueError(f"AUER_PROFILE_PATH:{auer_id}")
        if native_binding.get("source_snapshot_manifest_sha256") != snapshot_sha:
            raise ValueError(f"AUER_BINDING_SNAPSHOT:{auer_id}")
        method_path = PROJECT / native_binding["method_contract_path"]
        backend_path = PROJECT / native_binding["arithmetic_backend_manifest_path"]
        solver_path = PROJECT / "validation/autonomous_w2/g4/auer_snapshot_v2/solver_r9_w2.py"
        checker_path = PROJECT / "validation/autonomous_w2/g4/auer_snapshot_v2/replay_r9_w2.py"
        snapshot_items = {item["snapshot_path"]: item["snapshot_sha256"] for item in snapshot["copies"]}
        if sha256_file(method_path) != native_binding["method_contract_sha256"]:
            raise ValueError(f"AUER_METHOD_CONTRACT_PATH_HASH:{auer_id}")
        if sha256_file(backend_path) != native_binding["arithmetic_backend_manifest_sha256"]:
            raise ValueError(f"AUER_BACKEND_MANIFEST_PATH_HASH:{auer_id}")
        if sha256_file(solver_path) != native_binding["solver_source_sha256"] or snapshot_items.get(solver_path.relative_to(PROJECT).as_posix()) != native_binding["solver_source_sha256"]:
            raise ValueError(f"AUER_SOLVER_SNAPSHOT_HASH:{auer_id}")
        if sha256_file(checker_path) != native_binding["checker_source_sha256"] or snapshot_items.get(checker_path.relative_to(PROJECT).as_posix()) != native_binding["checker_source_sha256"]:
            raise ValueError(f"AUER_CHECKER_SNAPSHOT_HASH:{auer_id}")
        if action["physical_input_sha256"] != canonical_sha256(case["canonical_physical_input"]):
            raise ValueError(f"CANONICAL_PHYSICAL_INPUT_HASH:{external}")
        if v6["physical_input_sha256"] != case["physical_input_sha256"]:
            raise ValueError(f"METHOD_PAIR_PHYSICAL_HASH:{external}")
        if action["peer_action_id"] != v6["peer_action_id"] or action["peer_action_id"] != case["peer_action_id"]:
            raise ValueError(f"PEER_ACTION_BIJECTION:{external}")
        pairs.append({
            "ordinal": ordinal,
            "external_id": external,
            "auer_id": auer_id,
            "peer_action_id": action["peer_action_id"],
            "physical_input_sha256": action["physical_input_sha256"],
            "v6_binding_sha256": sha256_file(v6_path),
            "auer_native_input_sha256": sha256_file(case_path),
            "auer_native_binding_sha256": binding_digest,
            "paths_and_hashes_match": True,
        })
        checked_pairs += 1
    if len(pairs) != 3 or len({row["physical_input_sha256"] for row in pairs}) != 3:
        raise ValueError("COMPARISON_ACTION_BIJECTION_NOT_THREE_DISTINCT_INPUTS")
    return {
        "schema": "ddwmr-g4-w2-comparison-binding-preflight-v2",
        "session": "DDWMR | LUNA-G4-AUER",
        "protocol_sha256": sha256_file(plan / "protocol_v2.json"),
        "benchmark_sha256": sha256_file(plan / "benchmark_v2.json"),
        "task_protocol_sha256": sha256_file(PROJECT / "research/autonomous_w2/g2/task_protocol_v1.json"),
        "peer_release_sha256": sha256_file(PROJECT / "coordination/autonomous_w2/g2/releases/RELEASE_v6.json"),
        "state_count": len(task["task"]["initial_box"]),
        "label_count": len(task["model"]["fixed_label_order"]),
        "checked_method_pairs": checked_pairs,
        "checked_snapshot_entries": snapshot_hash_checks,
        "checked_v6_source_path_hash_pairs": source_hash_checks,
        "checked_auer_source_and_method_path_hash_pairs": 12,
        "auer_profile_worker_path": strict_json(plan / "auer_profile_v2.json")["matched_worker"]["module"],
        "auer_profile_worker_path_expected": "validation.autonomous_w2.g4.auer_w2_worker_v2",
        "auer_profile_uses_expected_worker": strict_json(plan / "auer_profile_v2.json")["matched_worker"]["module"] == "validation.autonomous_w2.g4.auer_w2_worker_v2",
        "fresh_native_calls": 0,
        "all_pairs_valid": True,
        "pairs": pairs,
    }


def main() -> int:
    report = verify()
    out = PROJECT / RESULT_REL / "binding_preflight_v2.json"
    write_json(out, report, max_bytes=1_048_576, exclusive=True)
    print(json.dumps({key: value for key, value in report.items() if key != "pairs"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
