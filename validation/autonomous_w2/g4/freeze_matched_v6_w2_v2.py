"""Create the immutable W2 source closure, freeze manifest and receipt."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validation.autonomous_w2.g4.matched_v6_common_v2 import (
    PROJECT, PLAN_REL, RESULT_REL, sha256_file, strict_json, write_json,
)

LOCK_REL = Path("coordination/autonomous_w2/COMPUTE.lock")


def rel(path: Path) -> str:
    return path.resolve().relative_to(PROJECT.resolve()).as_posix()


def file_entry(path: Path, role: str) -> dict[str, Any]:
    return {"path": rel(path), "role": role, "size_bytes": path.stat().st_size, "sha256": sha256_file(path)}


def main() -> int:
    plan = PROJECT / PLAN_REL
    result = PROJECT / RESULT_REL
    protocol_path = plan / "protocol_v2.json"
    benchmark_path = plan / "benchmark_v2.json"
    manifest_path = plan / "auer_input_manifest_v2.json"
    auer_bindings_path = plan / "auer_bindings_v2.json"
    profile_paths = [plan / name for name in ("g2_profile_centered_v6.json", "auer_profile_v2.json", "common_profile_v2.json")]
    snapshot_path = plan / "native_source_snapshot_v2.json"
    task_path = PROJECT / "research/autonomous_w2/g2/task_protocol_v1.json"
    release_path = PROJECT / "coordination/autonomous_w2/g2/releases/RELEASE_v6.json"
    status_path = PROJECT / "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_18.json"
    mapping_path = result / "mapping_preflight_v3.json"
    saved_preflight_path = result / "saved_replay_preflight_v8.json"
    job_probe_path = result / "resource_probe_v2" / "probe_receipt.json"
    failure_ledger_path = result / "preflight_failure_ledger_v5.json"
    binding_preflight_path = result / "binding_preflight_v4.json"
    required = [protocol_path, benchmark_path, manifest_path, auer_bindings_path, snapshot_path, task_path, release_path, status_path, mapping_path, saved_preflight_path, binding_preflight_path, job_probe_path, failure_ledger_path, *profile_paths]
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(f"FREEZE_REQUIRED_FILE_MISSING:{path}")
    protocol = strict_json(protocol_path)
    benchmark = strict_json(benchmark_path)
    snapshot = strict_json(snapshot_path)
    manifest = strict_json(manifest_path)
    bindings_doc = strict_json(auer_bindings_path)
    mapping = strict_json(mapping_path)
    saved_preflight = strict_json(saved_preflight_path)
    binding_preflight = strict_json(binding_preflight_path)
    job_probe = strict_json(job_probe_path)
    if protocol.get("status") != "FROZEN_DEVELOPMENT_ONLY_W2" or len(protocol.get("actions", [])) != 3:
        raise RuntimeError("PROTOCOL_NOT_THREE_ACTION_FROZEN")
    if mapping.get("result") != "PASS_NONQUERY_MAPPING" or mapping.get("fresh_native_calls") != 0:
        raise RuntimeError("MAPPING_NOT_PASS_NONQUERY")
    if not saved_preflight.get("all_native_saved_replays_pass") or not saved_preflight.get("all_common_replays_pass") or saved_preflight.get("fresh_native_calls") != 0:
        raise RuntimeError("SAVED_REPLAY_PREFLIGHT_NOT_PASS")
    if binding_preflight.get("all_pairs_valid") is not True or binding_preflight.get("fresh_native_calls") != 0 or binding_preflight.get("checked_method_pairs") != 3:
        raise RuntimeError("BINDING_PREFLIGHT_NOT_PASS")
    if (job_probe.get("passed") is not True or job_probe.get("native_calls") != 0
            or not job_probe["result"].get("process_assigned_before_resume")
            or not job_probe["result"].get("process_in_job")
            or job_probe["result"]["job"]["total_processes"] != 1):
        raise RuntimeError("WINDOWS_JOB_OBJECT_PROBE_NOT_PASS")
    if len(manifest.get("cases", [])) != 3 or len(bindings_doc.get("bindings", [])) != 3:
        raise RuntimeError("AUER_NATIVE_BINDING_COUNT")
    action_ids = {item["comparison_id"] for item in protocol["actions"]}
    if action_ids != {"W2_G4_V6_ZERO", "W2_G4_V6_NOMINAL", "W2_G4_V6_ALTERNATIVE"}:
        raise RuntimeError("UNEXPECTED_ACTION_SET")
    # Every frozen input and wrapper binding is checked before being inventoried.
    files: list[dict[str, Any]] = []
    seen: set[str] = set()
    def add(path: Path, role: str) -> None:
        key = rel(path)
        if key in seen:
            return
        if not path.is_file():
            raise FileNotFoundError(f"SOURCE_CLOSURE_FILE_MISSING:{path}")
        files.append(file_entry(path, role)); seen.add(key)

    for path, role in (
        (protocol_path, "frozen_protocol"), (benchmark_path, "common_benchmark"), (manifest_path, "auer_input_manifest"),
        (auer_bindings_path, "auer_native_bindings"), (snapshot_path, "native_source_snapshot"),
        (task_path, "peer_task_protocol"), (release_path, "peer_release"), (status_path, "peer_status_snapshot"),
        (mapping_path, "nonquery_mapping_preflight"), (saved_preflight_path, "nonquery_saved_replay_preflight"),
        (binding_preflight_path, "nonquery_all_path_hash_preflight"),
        (job_probe_path, "nonquery_windows_job_object_probe"),
        (failure_ledger_path, "preserved_nonquery_preflight_failures"),
        (PROJECT / "coordination/autonomous_w2/g4/G4_TO_G2_V6_MATCHED_INPUT_MAPPING_V4.md", "peer_coordination_request"),
        (plan / "prepare_output_v2.json", "candidate_builder_output"),
    ):
        add(path, role)
    for path in profile_paths:
        add(path, "frozen_resource_profile")
    for ordinal in range(1, 4):
        add(plan / "v6_bindings" / f"{ordinal:02d}.json", "v6_outer_binding")
    for case in manifest["cases"]:
        add(PROJECT / case["native_case_path"], "auer_native_case")
    for relpath in (
        "validation/autonomous_w2/g4/v6_w2_worker_v2.py", "validation/autonomous_w2/g4/auer_w2_worker_v2.py",
        "validation/autonomous_w2/g4/v6_w2_adapter_v2.py", "validation/autonomous_w2/g4/auer_w2_adapter_v2.py",
        "validation/autonomous_w2/g4/matched_v6_common_v2.py", "validation/autonomous_w2/g4/windows_job_supervisor_v2.py",
        "validation/autonomous_w2/g4/run_matched_v6_w2_v2.py", "validation/autonomous_w2/g4/probe_windows_job_supervisor_v2.py",
        "validation/autonomous_w2/g4/freeze_matched_v6_w2_v2.py", "validation/autonomous_w2/g4/prepare_matched_v6_w2_v2.py",
        "validation/autonomous_w2/g4/preflight_mapping_v2.py", "validation/autonomous_w2/g4/preflight_mapping_v3.py",
        "validation/autonomous_w2/g4/preflight_bindings_v2.py", "validation/autonomous_w2/g4/preflight_bindings_v3.py",
        "validation/autonomous_w2/g4/preflight_bindings_v4.py",
        "validation/autonomous_w2/g4/preflight_saved_rows_v3.py",
        "validation/autonomous_w2/g4/finalize_saved_rows_preflight_v5.py", "validation/autonomous_w2/g4/replay_saved_v6_worker_v2.py",
        "validation/g4/common_tube.py", "validation/g2/rational.py", "validation/g2/interval.py",
        "validation/g2/model.py", "validation/g2/polynomial.py", "validation/g2/hashing.py",
        "docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md", "validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v2.json",
        "validation/baselines/auer2013/small_case_resource_profile_v2.json",
    ):
        add(PROJECT / relpath, "executable_or_method_dependency")
    for path in (PROJECT / "validation/autonomous_w2/g4/v6_snapshot_v2").glob("*.py"):
        add(path, "v6_source_snapshot")
    for path in (PROJECT / "validation/autonomous_w2/g4/auer_snapshot_v2").glob("*.py"):
        add(path, "auer_source_snapshot")
    for entry in snapshot.get("copies", []):
        add(PROJECT / entry["origin_path"], "historical_source_snapshot_origin")
    # The compact v8 replay summary above binds all three saved rows and
    # independent replay statuses.  The expanded worker artifacts in the
    # preflight_saved_rows_v2-v8 directories are retained in place but excluded
    # from the frozen source closure: they are multi-megabyte replay outputs,
    # not executable dependencies or additional inputs to the new producers.
    # Include the exact peer binding and saved row bytes consumed by each v6
    # replay, since those hashes are semantic inputs even though they are
    # historical G2-owned artifacts.
    for ordinal in range(1, 4):
        binding = strict_json(plan / "v6_bindings" / f"{ordinal:02d}.json")
        add(PROJECT / binding["core_binding_path"], "peer_core_binding")
        add(PROJECT / binding["peer_saved_row_path"], "peer_saved_row")
        for source_rel in binding.get("source_files", {}):
            add(PROJECT / source_rel, "v6_binding_pinned_source")

    closure_path = result / "source_closure_v3.json"
    closure_doc = {
        "schema": "ddwmr-g4-w2-matched-source-closure-v3",
        "session": "DDWMR | LUNA-G4-AUER",
        "status": "FROZEN_DEVELOPMENT_ONLY_W2",
        "files": sorted(files, key=lambda item: item["path"]),
        "file_count": len(files),
        "historical_peer_artifacts_read_only": True,
        "native_query_count": 0,
    }
    write_json(closure_path, closure_doc, max_bytes=8_388_608, exclusive=True)
    closure_sha = sha256_file(closure_path)
    binding_paths = {item["comparison_id"]: f"{PLAN_REL.as_posix()}/v6_bindings/{ordinal:02d}.json" for ordinal, item in enumerate(protocol["actions"], 1)}
    auer_binding_paths = {item["comparison_id"]: f"{PLAN_REL.as_posix()}/auer_bindings_v2.json" for item in bindings_doc["bindings"]}
    freeze_doc = {
        "schema": "ddwmr-g4-w2-matched-v6-auer-freeze-manifest-v3",
        "session": "DDWMR | LUNA-G4-AUER",
        "status": "FROZEN_DEVELOPMENT_ONLY_W2",
        "phase": "BOUNDED_DEVELOPMENT_FALSIFICATION",
        "protocol_path": rel(protocol_path), "protocol_sha256": sha256_file(protocol_path),
        "benchmark_path": rel(benchmark_path), "benchmark_sha256": sha256_file(benchmark_path),
        "auer_manifest_path": rel(manifest_path), "auer_manifest_sha256": sha256_file(manifest_path),
        "auer_bindings_path": rel(auer_bindings_path), "auer_bindings_sha256": sha256_file(auer_bindings_path),
        "task_protocol": {"path": rel(task_path), "sha256": sha256_file(task_path)},
        "peer_release": {"path": rel(release_path), "sha256": sha256_file(release_path)},
        "peer_status_snapshot": {"path": rel(status_path), "sha256": sha256_file(status_path)},
        "source_closure_path": rel(closure_path), "source_closure_sha256": closure_sha,
        "native_source_snapshot_path": rel(snapshot_path), "native_source_snapshot_sha256": sha256_file(snapshot_path),
        "v6_profile_path": rel(profile_paths[0]), "auer_profile_path": rel(profile_paths[1]), "common_profile_path": rel(profile_paths[2]),
        "mapping_preflight_path": rel(mapping_path), "mapping_preflight_sha256": sha256_file(mapping_path),
        "saved_replay_preflight_path": rel(saved_preflight_path), "saved_replay_preflight_sha256": sha256_file(saved_preflight_path),
        "binding_preflight_path": rel(binding_preflight_path), "binding_preflight_sha256": sha256_file(binding_preflight_path),
        "compute_lock_path": LOCK_REL.as_posix(),
        "primary_criterion": protocol["primary_criterion"],
        "ordered_actions": protocol["ordered_actions"],
        "actions": protocol["actions"],
        "v6_binding_paths": binding_paths,
        "auer_binding_paths": auer_binding_paths,
        "method_worker_modules": {
            "v6": "validation.autonomous_w2.g4.v6_w2_worker_v2",
            "auer": "validation.autonomous_w2.g4.auer_w2_worker_v2",
        },
        "resource_caps": protocol["resource_caps"],
        "native_call_limits": protocol["native_call_limits"],
        "run_order": protocol["run_order"],
        "development_data": protocol["development_data_status"],
        "no_confirmation_rows": True,
        "no_batch_1944": True,
        "no_retry": True,
        "frozen_utc": datetime.now(timezone.utc).isoformat(),
    }
    freeze_path = plan / "freeze_manifest_v3.json"
    write_json(freeze_path, freeze_doc, max_bytes=1_048_576, exclusive=True)
    freeze_sha = sha256_file(freeze_path)
    receipt = {
        "schema": "ddwmr-g4-w2-matched-freeze-receipt-v3",
        "session": "DDWMR | LUNA-G4-AUER",
        "freeze_manifest_path": rel(freeze_path), "freeze_manifest_sha256": freeze_sha,
        "protocol_path": rel(protocol_path), "protocol_sha256": sha256_file(protocol_path),
        "source_closure_path": rel(closure_path), "source_closure_sha256": closure_sha,
        "benchmark_sha256": sha256_file(benchmark_path), "auer_manifest_sha256": sha256_file(manifest_path),
        "auer_bindings_sha256": sha256_file(auer_bindings_path),
        "mapping_preflight_sha256": sha256_file(mapping_path), "saved_replay_preflight_sha256": sha256_file(saved_preflight_path),
        "binding_preflight_sha256": sha256_file(binding_preflight_path),
        "actions_frozen": 3, "v6_native_limit": 3, "auer_native_limit": 3,
        "native_calls_before_execution": {"v6": 0, "auer": 0},
        "confirmation_rows_before_execution": {"v6": 0, "auer": 0},
        "held_out_rows": 0, "batch_1944": "NOT_RUN", "legacy_r5_800": "NOT_RUN",
        "source_closure_file_count": len(files), "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(result / "freeze_receipt_v3.json", receipt, max_bytes=1_048_576, exclusive=True)
    print(json.dumps({"freeze_manifest_path": rel(freeze_path), "freeze_manifest_sha256": freeze_sha, "source_closure_sha256": closure_sha, "file_count": len(files)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
