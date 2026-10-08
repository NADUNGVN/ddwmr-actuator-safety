"""Run exactly one frozen G4 v6 development action, replay it, and score it."""
from __future__ import annotations

import argparse
import json
import time
from fractions import Fraction
from pathlib import Path

from validation.g2.rational import Budget
from validation.autonomous_w2.g4.matched_v6_common_v2 import (
    PLAN_REL, PROJECT, configure_integer_string_limit, initial_state_from_task,
    scene_from_task, score_serialize_replay_progress, sha256_file, strict_json,
    summarize_common, verify_source_closure, write_json,
)
from validation.autonomous_w2.g4.v6_snapshot_v2.checker_centered_v6 import audit as replay_v6_row
from validation.autonomous_w2.g4.v6_snapshot_v2.producer_centered_v6 import evaluate_bound_row
from validation.autonomous_w2.g4.v6_w2_adapter_v2 import convert_v6_row_to_segments


def run(binding_path: Path, output_dir: Path) -> int:
    started = time.monotonic()
    binding_path = binding_path.resolve()
    output_dir = output_dir.resolve()
    freeze_path = PROJECT / PLAN_REL / "freeze_manifest_v3.json"
    freeze = strict_json(freeze_path)
    receipt = strict_json(PROJECT / "results/validation/autonomous_w2/g4/matched_v6_task_development_v2/freeze_receipt_v3.json")
    if receipt.get("freeze_manifest_sha256") != sha256_file(freeze_path):
        raise ValueError("FREEZE_RECEIPT_MANIFEST_HASH_MISMATCH")
    if receipt.get("protocol_sha256") != freeze.get("protocol_sha256"):
        raise ValueError("FREEZE_RECEIPT_PROTOCOL_HASH_MISMATCH")
    verify_source_closure(freeze)

    binding = strict_json(binding_path)
    if binding_path.relative_to(PROJECT).as_posix() != binding.get("binding_path"):
        raise ValueError("OUTER_BINDING_PATH_MISMATCH")
    action = next(item for item in freeze["actions"] if item["comparison_id"] == binding["comparison_id"])
    if action["physical_input_sha256"] != binding["physical_input_sha256"]:
        raise ValueError("CANONICAL_PHYSICAL_INPUT_BINDING")
    if action["native_binding_sha256"] != sha256_file(binding_path):
        raise ValueError("FROZEN_WRAPPER_BINDING_HASH")
    if binding.get("source_snapshot_manifest_sha256") != freeze["native_source_snapshot_sha256"]:
        raise ValueError("V6_SOURCE_SNAPSHOT_BINDING")
    if action["peer_saved_row_sha256"] != binding["peer_saved_row_sha256"]:
        raise ValueError("SAVED_DEVELOPMENT_ROW_BINDING")
    if binding.get("peer_release_sha256") != freeze["peer_release"]["sha256"]:
        raise ValueError("PEER_RELEASE_BINDING_MISMATCH")

    core_path = PROJECT / binding["core_binding_path"]
    if sha256_file(core_path) != binding["core_binding_sha256"]:
        raise ValueError("G2_CORE_BINDING_CHANGED")
    if binding["source_files"].get(binding["core_binding_path"]) != binding["core_binding_sha256"]:
        raise ValueError("G2_CORE_BINDING_HASH_RELATION")
    saved_row_path = PROJECT / binding["peer_saved_row_path"]
    if sha256_file(saved_row_path) != binding["peer_saved_row_sha256"]:
        raise ValueError("SAVED_G2_ROW_CHANGED")
    for rel, digest in binding["source_files"].items():
        path = PROJECT / rel
        if not path.is_file() or sha256_file(path) != digest:
            raise ValueError(f"SOURCE_PIN_MISMATCH:{rel}")

    producer_started = time.monotonic()
    write_json(output_dir / "producer_start.json", {
        "schema": "ddwmr-g4-w2-producer-start-v1",
        "method": "centered_residual_v6",
        "comparison_id": binding["comparison_id"],
        "source_binding_sha256": sha256_file(binding_path),
        "producer_invocation_ordinal": 1,
    }, max_bytes=4096, exclusive=True)
    row = evaluate_bound_row(binding, binding["action_id"])
    producer_seconds = time.monotonic() - producer_started
    row_path = output_dir / "native_row.json"
    row_hash, row_bytes = write_json(row_path, row, max_bytes=8_388_608)

    replay_started = time.monotonic()
    native_replay = replay_v6_row(binding_path, row_path)
    replay_seconds = time.monotonic() - replay_started
    if not native_replay.get("replayed"):
        raise ValueError(f"V6_NATIVE_REPLAY_FAILED:{native_replay}")

    task = strict_json(PROJECT / freeze["task_protocol"]["path"])
    protocol = strict_json(PROJECT / freeze["protocol_path"])
    profile = strict_json(PROJECT / freeze["v6_profile_path"])
    benchmark = strict_json(PROJECT / freeze["benchmark_path"])
    common_profile = strict_json(PROJECT / freeze["common_profile_path"])
    common_budget = Budget(
        max_bits=int(common_profile["max_rational_bits"]),
        max_operations=int(common_profile["max_rational_operations_per_common_stage"]),
        wall_seconds=Fraction(int(common_profile["wall_seconds"])),
    )
    configure_integer_string_limit(int(common_profile["max_integer_string_digits"]))
    adapter_started = time.monotonic()
    adapter_binding = dict(binding)
    adapter_binding["native_row_sha256"] = row_hash
    segments, adapter_work = convert_v6_row_to_segments(
        row, task, protocol, adapter_binding, profile, benchmark, common_budget,
    )
    adapter_seconds = time.monotonic() - adapter_started
    common_started = time.monotonic()
    common_record, common_replay, progress, common_files = score_serialize_replay_progress(
        segments, benchmark, scene_from_task(task), Fraction(task["task"]["hold_s"]),
        initial_state_from_task(task, common_budget), sqrt_bisections=int(common_profile["sqrt_bisections"]),
        budget=common_budget, common_record_path=output_dir / "common_record.json",
        progress_path=output_dir / "progress.json",
        max_record_bytes=int(common_profile["max_common_record_bytes"]),
        max_progress_bytes=int(common_profile["max_progress_record_bytes"]),
    )
    common_seconds = time.monotonic() - common_started
    if not common_replay.get("replayed"):
        raise ValueError(f"V6_COMMON_REPLAY_FAILED:{common_replay}")
    bounds = [Fraction(int(item["num"]), int(item["den"])) for item in progress["progress_enclosure_m"]]
    safety_pass = common_record.get("predicate_status") == "PASS_ON_SUPPLIED_TUBE"
    eligible = safety_pass and bounds[0] >= Fraction(7, 20)
    final_status = "CERTIFIED" if eligible else (
        "CERTIFIED_SAFETY_TASK_INELIGIBLE" if safety_pass and bounds[1] < Fraction(7, 20) else
        "SAFETY_CERTIFIED_PROGRESS_UNRESOLVED" if safety_pass else "PROOF_COMPLETE_COMMON_UNKNOWN"
    )
    summary = {
        "schema": "ddwmr-g4-w2-v6-native-result-v2",
        "external_id": binding["comparison_id"],
        "peer_action_id": binding["peer_action_id"],
        "physical_input_sha256": binding["physical_input_sha256"],
        "wrapper_binding_sha256": sha256_file(binding_path),
        "core_binding_sha256": binding["core_binding_sha256"],
        "peer_saved_row_path": binding["peer_saved_row_path"],
        "peer_saved_row_sha256": binding["peer_saved_row_sha256"],
        "native_status": row.get("safety_status"),
        "native_task_eligible": row.get("task_eligible"),
        "native_row_path": row_path.relative_to(PROJECT).as_posix(),
        "native_row_sha256": row_hash,
        "native_row_bytes": row_bytes,
        "native_replay": native_replay,
        "native_replay_status": "PASS",
        "native_replay_wall_seconds": replay_seconds,
        "common_record_path": (output_dir / "common_record.json").relative_to(PROJECT).as_posix(),
        "common_progress_path": (output_dir / "progress.json").relative_to(PROJECT).as_posix(),
        "common_summary": summarize_common(common_record),
        "common_replay": common_replay,
        "common_replay_status": "PASS",
        "common_progress": progress,
        "common_files": common_files,
        "adapter_work": adapter_work,
        "progress_lower_meets_threshold": bounds[0] >= Fraction(7, 20),
        "task_eligible": eligible,
        "final_status": final_status,
        "producer_wall_seconds": producer_seconds,
        "native_replay_wall_seconds": replay_seconds,
        "common_adapter_wall_seconds": adapter_seconds,
        "common_check_replay_progress_wall_seconds": common_seconds,
        "worker_elapsed_wall_seconds": time.monotonic() - started,
        "producer_interval_operations": row.get("arithmetic", {}).get("interval_operations"),
        "producer_peak_rational_bits": row.get("arithmetic", {}).get("max_rational_bits"),
        "native_calls_counted": 1,
        "no_retry": True,
    }
    write_json(output_dir / "worker_result.json", summary, max_bytes=1_048_576)
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    output_dir = Path(args.output_dir).resolve()
    try:
        return run(Path(args.binding), output_dir)
    except Exception as exc:
        # A failure before the producer marker is a binding/setup failure and
        # therefore consumes no native call.  Once the marker exists, the
        # attempted producer counts exactly once and is never retried.
        native_started = (output_dir / "producer_start.json").is_file()
        reason = f"{type(exc).__name__}:{exc}"
        is_resource = type(exc).__name__ in {"ArithmeticLimit", "ResourceLimit"} or "LIMIT" in str(exc)
        summary = {
            "schema": "ddwmr-g4-w2-v6-native-result-v2",
            "native_status": "RESOURCE_LIMIT" if is_resource else "IMPLEMENTATION_FAILURE",
            "termination": reason,
            "native_calls_counted": int(native_started),
            "no_retry": True,
        }
        try:
            write_json(output_dir / "worker_result.json", summary, max_bytes=1_048_576)
        except Exception:
            pass
        print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
        return 0 if is_resource else 30


if __name__ == "__main__":
    raise SystemExit(main())
