"""One frozen local-Auer development action with native and common replay."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

from validation.autonomous_w2.g4.auer_snapshot_v2.replay_r9_w2 import replay_native_proof
from validation.autonomous_w2.g4.auer_snapshot_v2.solver_r9_w2 import solve_ddwmr_case
from validation.autonomous_w2.g4.auer_w2_adapter_v2 import canonical_sha256, make_segments
from validation.autonomous_w2.g4.matched_v6_common_v2 import (
    PLAN_REL, PROJECT, configure_integer_string_limit, initial_state_from_task,
    scene_from_task, score_serialize_replay_progress, sha256_file, strict_json,
    summarize_common, verify_source_closure, write_json,
)
from validation.g2.rational import Budget, Interval, ResourceLimit, parse_q

RESULT_REL = Path("results/validation/autonomous_w2/g4/matched_v6_task_development_v2")


def _binding_for(freeze: dict[str, Any], comparison_id: str) -> dict[str, Any]:
    binding_doc = strict_json(PROJECT / freeze["auer_bindings_path"])
    matches = [item["native_binding"] for item in binding_doc["bindings"]
               if item["comparison_id"] == comparison_id]
    if len(matches) != 1:
        raise ValueError("AUER_NATIVE_BINDING_NOT_UNIQUE")
    return matches[0]


def run(comparison_id: str, output_dir: Path) -> int:
    started = time.monotonic()
    output_dir = output_dir.resolve()
    freeze_path = PROJECT / PLAN_REL / "freeze_manifest_v3.json"
    freeze = strict_json(freeze_path)
    freeze_receipt = strict_json(PROJECT / RESULT_REL / "freeze_receipt_v3.json")
    if freeze_receipt.get("freeze_manifest_sha256") != sha256_file(freeze_path):
        raise ValueError("FREEZE_RECEIPT_MANIFEST_HASH_MISMATCH")
    if freeze_receipt.get("protocol_sha256") != freeze.get("protocol_sha256"):
        raise ValueError("FREEZE_RECEIPT_PROTOCOL_HASH_MISMATCH")
    closure = verify_source_closure(freeze)
    closure_sha = freeze["source_closure_sha256"]

    protocol = strict_json(PROJECT / freeze["protocol_path"])
    profile = strict_json(PROJECT / freeze["auer_profile_path"])
    benchmark_path = PROJECT / freeze["benchmark_path"]
    benchmark = strict_json(benchmark_path)
    manifest_path = PROJECT / freeze["auer_manifest_path"]
    manifest = strict_json(manifest_path)
    entries = [row for row in manifest["cases"] if row["comparison_id"] == comparison_id]
    if len(entries) != 1:
        raise ValueError("AUER_CASE_NOT_UNIQUE_IN_FROZEN_THREE_CASE_MANIFEST")
    item = entries[0]
    action = next(row for row in protocol["actions"] if row["auer_id"] == comparison_id)
    if action["physical_input_sha256"] != item["physical_input_sha256"]:
        raise ValueError("AUER_PHYSICAL_DIGEST_BINDING")
    if action["auer_native_input_file_sha256"] != item["native_case_sha256"]:
        raise ValueError("AUER_NATIVE_FILE_DIGEST_BINDING")

    case_path = PROJECT / item["native_case_path"]
    if sha256_file(case_path) != item["native_case_sha256"]:
        raise ValueError("AUER_NATIVE_CASE_BYTES_CHANGED")
    case = strict_json(case_path)
    if case.get("physical_input_sha256") != item["physical_input_sha256"]:
        raise ValueError("AUER_CASE_PHYSICAL_DIGEST_MISMATCH")
    if case.get("canonical_physical_input_sha256") != item["physical_input_sha256"]:
        raise ValueError("AUER_CASE_CANONICAL_PHYSICAL_DIGEST_MISMATCH")
    if case.get("benchmark_sha256") != sha256_file(benchmark_path):
        raise ValueError("AUER_CASE_BENCHMARK_HASH_MISMATCH")
    # Runtime-only file binding fields are not included in the hashed case bytes.
    case["native_input_path"] = item["native_case_path"]
    case["native_input_file_sha256"] = item["native_case_sha256"]

    native_binding = _binding_for(freeze, comparison_id)
    expected_binding_sha = hashlib.sha256(
        json.dumps(native_binding, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"
    ).hexdigest()
    if action.get("auer_native_binding_sha256") != expected_binding_sha:
        raise ValueError("AUER_NATIVE_BINDING_HASH_MISMATCH")
    expected_input = {"input_path": item["native_case_path"], "input_sha256": item["native_case_sha256"]}
    if any(native_binding.get(key) != value for key, value in expected_input.items()):
        raise ValueError("AUER_PROOF_BINDING_INPUT_PATH_OR_HASH")
    if native_binding.get("source_snapshot_manifest_sha256") != freeze["native_source_snapshot_sha256"]:
        raise ValueError("AUER_SOURCE_SNAPSHOT_BINDING")
    if native_binding.get("resource_profile_sha256") != sha256_file(PROJECT / freeze["auer_profile_path"]):
        raise ValueError("AUER_PROFILE_BINDING")

    cap = int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"])
    budget = Budget(
        max_bits=int(profile["max_rational_bits"]), max_operations=cap,
        wall_seconds=Fraction(int(profile["wall_time_seconds_per_ivp"])),
    )
    producer_marker = output_dir / "producer_start.json"
    write_json(producer_marker, {
        "schema": "ddwmr-g4-w2-producer-start-v1",
        "method": "local_auer2013_residual_picard_reconstruction",
        "comparison_id": comparison_id,
        "native_case_sha256": item["native_case_sha256"],
        "producer_invocation_ordinal": 1,
    }, max_bytes=4096, exclusive=True)
    producer_started = time.monotonic()
    proof = solve_ddwmr_case(
        case, benchmark,
        input_path=Path(item["native_case_path"]), input_sha256=item["native_case_sha256"],
        method_sha256=native_binding["method_contract_sha256"],
        backend_sha256=native_binding["arithmetic_backend_manifest_sha256"],
        profile=profile, profile_sha256=native_binding["resource_profile_sha256"],
        snapshot_sha256=native_binding["source_snapshot_manifest_sha256"],
        solver_sha256=native_binding["solver_source_sha256"],
        checker_sha256=native_binding["checker_source_sha256"],
        resource_profile_path=native_binding["resource_profile_path"], budget=budget,
    )
    producer_seconds = time.monotonic() - producer_started
    envelope = {"proof": proof, "proof_sha256": canonical_sha256(proof)}
    proof_path = output_dir / "native_proof.json"
    proof_hash, proof_bytes = write_json(
        proof_path, envelope, max_bytes=int(profile["max_serialized_proof_bytes"]),
    )

    if proof.get("status") != "PROOF_COMPLETE":
        summary = {
            "schema": "ddwmr-g4-w2-auer-result-v2",
            "comparison_id": comparison_id,
            "peer_action_id": item["peer_action_id"],
            "physical_input_sha256": item["physical_input_sha256"],
            "native_input_path": item["native_case_path"],
            "native_input_sha256": item["native_case_sha256"],
            "native_status": proof.get("status"),
            "native_termination": proof.get("termination"),
            "native_proof_path": proof_path.relative_to(PROJECT).as_posix(),
            "native_proof_file_sha256": proof_hash,
            "native_proof_bytes": proof_bytes,
            "native_proof_record_sha256": envelope["proof_sha256"],
            "producer_wall_seconds": producer_seconds,
            "producer_rational_operations": budget.operations,
            "producer_max_observed_rational_bits": budget.max_seen_bits,
            "native_calls_counted": 1,
            "no_retry": True,
            "final_status": proof.get("status"),
        }
        write_json(output_dir / "worker_result.json", summary, max_bytes=1_048_576)
        print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
        return 0

    replay_started = time.monotonic()
    rhs_producer = int(proof.get("work", {}).get("rhs_jacobian_evaluations", 0))
    rhs_counter = {"count": rhs_producer, "limit": int(profile["max_rhs_jacobian_evaluations_per_ivp"])}
    native_replay = replay_native_proof(
        envelope, case=case, benchmark=benchmark, profile=profile, fixture=None,
        expected_binding=native_binding, budget=budget, rhs_eval_counter=rhs_counter,
    )
    replay_seconds = time.monotonic() - replay_started
    if not native_replay.get("replayed"):
        raise ValueError(f"AUER_NATIVE_REPLAY_FAILED:{native_replay}")

    common_profile = strict_json(PROJECT / freeze["common_profile_path"])
    configure_integer_string_limit(int(common_profile["max_integer_string_digits"]))
    adapter_started = time.monotonic()
    segments = make_segments(
        envelope, case, proof_path, budget, source_binding=native_binding,
        source_closure_path=freeze["source_closure_path"], source_closure_sha256=closure_sha,
        benchmark_path=freeze["benchmark_path"], benchmark_sha256=freeze["benchmark_sha256"],
        benchmark=benchmark,
    )
    adapter_seconds = time.monotonic() - adapter_started
    common_started = time.monotonic()
    common_record, common_replay, progress, common_files = score_serialize_replay_progress(
        segments, benchmark, scene_from_task(strict_json(PROJECT / freeze["task_protocol"]["path"])),
        parse_q(case["horizon"], budget), initial_state_from_case(case, budget),
        sqrt_bisections=int(common_profile["sqrt_bisections"]), budget=budget,
        common_record_path=output_dir / "common_record.json", progress_path=output_dir / "progress.json",
        max_record_bytes=int(common_profile["max_common_record_bytes"]),
        max_progress_bytes=int(common_profile["max_progress_record_bytes"]),
    )
    common_seconds = time.monotonic() - common_started
    if not common_replay.get("replayed"):
        raise ValueError(f"AUER_COMMON_REPLAY_FAILED:{common_replay}")
    progress_bounds = [Fraction(int(value["num"]), int(value["den"])) for value in progress["progress_enclosure_m"]]
    safety_pass = common_record.get("predicate_status") == "PASS_ON_SUPPLIED_TUBE"
    eligible = safety_pass and progress_bounds[0] >= Fraction(7, 20)
    final_status = "CERTIFIED" if eligible else (
        "CERTIFIED_SAFETY_TASK_INELIGIBLE" if safety_pass and progress_bounds[1] < Fraction(7, 20) else
        "SAFETY_CERTIFIED_PROGRESS_UNRESOLVED" if safety_pass else "PROOF_COMPLETE_COMMON_UNKNOWN"
    )
    summary = {
        "schema": "ddwmr-g4-w2-auer-result-v2",
        "comparison_id": comparison_id,
        "peer_action_id": item["peer_action_id"],
        "physical_input_sha256": item["physical_input_sha256"],
        "native_input_path": item["native_case_path"],
        "native_input_sha256": item["native_case_sha256"],
        "native_status": proof["status"],
        "native_method_id": proof["method_id"],
        "native_proof_path": proof_path.relative_to(PROJECT).as_posix(),
        "native_proof_file_sha256": proof_hash,
        "native_proof_bytes": proof_bytes,
        "producer_start_path": producer_marker.relative_to(PROJECT).as_posix(),
        "producer_start_sha256": sha256_file(producer_marker),
        "native_proof_record_sha256": envelope["proof_sha256"],
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
        "task_eligible": eligible,
        "progress_lower_meets_threshold": progress_bounds[0] >= Fraction(7, 20),
        "final_status": final_status,
        "resource_work": {
            "producer_rational_operations": proof.get("work", {}).get("rational_operations"),
            "producer_max_observed_rational_bits": proof.get("work", {}).get("max_observed_rational_bits"),
            "native_replay_common_budget_operations_so_far": budget.operations,
            "combined_rational_operation_cap": cap,
            "rhs_jacobian_producer_evaluations": rhs_producer,
            "rhs_jacobian_replay_evaluations": native_replay.get("rhs_jacobian_replay_evaluations"),
            "rhs_jacobian_combined_evaluations": rhs_counter["count"],
            "rhs_jacobian_combined_cap": rhs_counter["limit"],
            "accepted_steps": proof.get("work", {}).get("accepted_steps"),
            "rejected_step_attempts": proof.get("work", {}).get("rejected_step_attempts"),
        },
        "stage_seconds": {
            "producer": producer_seconds,
            "native_replay": replay_seconds,
            "common_adapter": adapter_seconds,
            "common_check_replay_progress": common_seconds,
            "worker_elapsed": time.monotonic() - started,
        },
        "producer_calls_started": 1,
        "native_calls_counted": 1,
        "no_retry": True,
    }
    write_json(output_dir / "worker_result.json", summary, max_bytes=1_048_576)
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
    return 0


def initial_state_from_case(case: dict[str, Any], budget: Budget) -> tuple[Interval, ...]:
    return tuple(Interval.from_json(row, budget) for row in case["initial_state"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--comparison-id", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        return run(args.comparison_id, Path(args.output_dir))
    except ResourceLimit as exc:
        native_started = (Path(args.output_dir) / "producer_start.json").is_file()
        summary = {
            "schema": "ddwmr-g4-w2-auer-result-v2", "comparison_id": args.comparison_id,
            "native_status": "RESOURCE_LIMIT", "termination": {"kind": exc.kind, "detail": exc.detail},
            "producer_calls_started": int(native_started),
            "native_calls_counted": int(native_started),
            "no_retry": True,
        }
        write_json(Path(args.output_dir) / "worker_result.json", summary, max_bytes=1_048_576)
        print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
        return 0
    except Exception as exc:
        native_started = (Path(args.output_dir) / "producer_start.json").is_file()
        summary = {
            "schema": "ddwmr-g4-w2-auer-result-v2", "comparison_id": args.comparison_id,
            "native_status": "IMPLEMENTATION_FAILURE", "termination": f"{type(exc).__name__}:{exc}",
            "producer_calls_started": int(native_started),
            "native_calls_counted": int(native_started),
            "no_retry": True,
        }
        try:
            write_json(Path(args.output_dir) / "worker_result.json", summary, max_bytes=1_048_576)
        except Exception:
            pass
        print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
        return 30


if __name__ == "__main__":
    raise SystemExit(main())
