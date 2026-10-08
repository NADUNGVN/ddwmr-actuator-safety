"""Validate and publish the immutable W2 G2 v5 256-slab profile release."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PLAN_REL = "research/autonomous_w2/g2/development_plan_v5.json"
RELEASE_REL = "coordination/autonomous_w2/g2/releases/RELEASE_v5.json"
REQUEST_REL = "coordination/autonomous_w2/g2/AUDIT_REQUEST_TO_G4_v5.md"
STATUS_REL = "coordination/autonomous_w2/g2/STATUS.json"
STATUS_VERSIONED_REL = "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_12.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(rel: str) -> Any:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_exclusive(rel: str, value: Any) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True).encode("utf-8") + b"\n")
        stream.flush()


def peer_snapshot() -> dict[str, Any]:
    status_rel = "coordination/autonomous_w2/g4/STATUS.json"
    audit_rel = "coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v1.json"
    status = read(status_rel)
    audit = read(audit_rel)
    return {
        "status_path": status_rel,
        "status_sha256": sha(ROOT / status_rel),
        "sequence": status.get("sequence"),
        "phase": status.get("phase"),
        "release_audit_path": audit_rel,
        "release_audit_sha256": sha(ROOT / audit_rel),
        "release_audit_decision": audit.get("decision"),
        "release_consumed": status.get("peer_release_consumed"),
    }


def validate_inputs() -> dict[str, Any]:
    plan = read(PLAN_REL)
    plan_path = ROOT / PLAN_REL
    status_before = read(STATUS_REL)
    if status_before.get("sequence") != 11 or status_before.get("native_attempts", {}).get("count_completed") != 18:
        raise ValueError("STATUS_SEQUENCE_11_OR_PRIOR_ATTEMPT_COUNT_MISMATCH")
    if plan.get("schema") != "G2_W2_DEVELOPMENT_PLAN_v5" or plan.get("planned_attempt_count") != 3 or plan.get("prior_native_attempts") != 18:
        raise ValueError("V5_PLAN_SCHEMA_OR_DENOMINATOR_MISMATCH")
    if plan.get("cumulative_native_attempts_after_plan") != 21 or plan.get("attempt_limit") != 24:
        raise ValueError("V5_CUMULATIVE_ATTEMPT_CAP_MISMATCH")
    if plan.get("held_out_or_confirmation_rows") != 0 or plan.get("legacy_800_row_study") != "NOT_RUN":
        raise ValueError("V5_PLAN_CONFIRMATION_OR_LEGACY_SCOPE_MISMATCH")
    expected_ids = ["W2_G2_DEV_001_ZERO", "W2_G2_DEV_001_NOMINAL", "W2_G2_DEV_001_ALTERNATIVE"]
    attempts = plan.get("ordered_attempts", [])
    if [item.get("action_id") for item in attempts] != expected_ids:
        raise ValueError("V5_ACTION_ORDER_MISMATCH")
    if [item.get("native_attempt_ordinal") for item in attempts] != [19, 20, 21]:
        raise ValueError("V5_ATTEMPT_ORDINAL_MISMATCH")
    current_branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    current_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    if current_branch != plan.get("repository_branch") or current_head != plan.get("repository_head"):
        raise ValueError("REPOSITORY_BRANCH_OR_HEAD_MISMATCH")
    freeze_rel = "results/validation/autonomous_w2/g2/development_v5/freeze_receipt_v5.json"
    freeze = read(freeze_rel)
    if freeze.get("schema") != "G2_W2_FREEZE_RECEIPT_v5" or freeze.get("plan_sha256") != sha(plan_path) or freeze.get("attempt_count_frozen") != 3:
        raise ValueError("V5_FREEZE_RECEIPT_BINDING_MISMATCH")
    for rel, expected in plan["source_files"].items():
        if sha(ROOT / rel) != expected:
            raise ValueError(f"V5_SOURCE_HASH_MISMATCH:{rel}")
    protocol = read(plan["protocol_path"])
    profile = read(plan["profile_path"])
    if sha(ROOT / plan["protocol_path"]) != plan.get("protocol_sha256") or sha(ROOT / plan["profile_path"]) != plan.get("profile_sha256"):
        raise ValueError("V5_PROTOCOL_OR_PROFILE_HASH_MISMATCH")
    if profile.get("time_slabs") != 256 or profile.get("slab_duration_s") != "1/128":
        raise ValueError("V5_SLAB_PARTITION_MISMATCH")
    if profile.get("worker_wall_cap_seconds") != 60 or profile.get("worker_memory_cap_bytes") != 1073741824 or profile.get("interval_operation_cap") != 5000000:
        raise ValueError("V5_RESOURCE_CAP_CHANGED")
    pre_run_rel = "results/validation/autonomous_w2/g2/pre_run_validation_v5.json"
    pre_run = read(pre_run_rel)
    if pre_run.get("native_attempts_before_v5") != 18 or pre_run.get("legacy_800_row_study") != "NOT_RUN" or pre_run.get("held_out_rows") != 0:
        raise ValueError("V5_PRERUN_RECEIPT_SCOPE_MISMATCH")
    if pre_run.get("checks", {}).get("native_query_or_worker_called") is not False or pre_run.get("checks", {}).get("center_point_strict_clip_branch_all_actions") is not True:
        raise ValueError("V5_PRERUN_CHECKS_MISMATCH")
    if protocol["task"].get("required_progress_m") != "7/20" or protocol["task"].get("hold_s") != "2":
        raise ValueError("V5_TASK_OR_THRESHOLD_CHANGED")
    peer = peer_snapshot()
    return {
        "plan": plan,
        "plan_path": plan_path,
        "freeze_rel": freeze_rel,
        "current_branch": current_branch,
        "current_head": current_head,
        "protocol": protocol,
        "profile": profile,
        "pre_run_rel": pre_run_rel,
        "peer": peer,
    }


def publish(validate_only: bool = False) -> dict[str, Any]:
    validated = validate_inputs()
    plan = validated["plan"]
    plan_path = validated["plan_path"]
    freeze_rel = validated["freeze_rel"]
    current_branch = validated["current_branch"]
    current_head = validated["current_head"]
    protocol = validated["protocol"]
    profile = validated["profile"]
    pre_run_rel = validated["pre_run_rel"]
    peer = validated["peer"]
    if validate_only:
        return {
            "validated": True,
            "plan_path": PLAN_REL,
            "plan_sha256": sha(plan_path),
            "source_count": len(plan["source_files"]),
            "attempt_count": len(plan["ordered_attempts"]),
            "peer_sequence": peer.get("sequence"),
            "peer_decision": peer.get("release_audit_decision"),
            "prior_native_attempts": plan["prior_native_attempts"],
            "cumulative_if_complete": plan["cumulative_native_attempts_after_plan"],
        }
    artifact_paths = [
        PLAN_REL,
        plan["profile_path"],
        plan["protocol_path"],
        "research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v5.md",
        pre_run_rel,
        "results/validation/autonomous_w2/g2/development_v5/freeze_receipt_v5.json",
        "results/validation/autonomous_w2/g2/development_v4/stage_receipt.json",
        "results/validation/autonomous_w2/g2/development_v4/attempt_01_W2_G2_DEV_001_ZERO/row.json",
        "results/validation/autonomous_w2/g2/development_v4/attempt_02_W2_G2_DEV_001_NOMINAL/row.json",
        "results/validation/autonomous_w2/g2/development_v4/attempt_03_W2_G2_DEV_001_ALTERNATIVE/row.json",
        "results/validation/autonomous_w2/g2/development_v4/attempt_03_W2_G2_DEV_001_ALTERNATIVE/mutation_audit_report.json",
        "results/validation/autonomous_w2/g2/clip_branch_point_witness_v1.json",
        "docs/reviews/autonomous_w2/g2/W2_V3_DEVELOPMENT_FAILURE_POSTMORTEM.md",
        "coordination/autonomous_w2/g2/releases/RELEASE_v4.json",
        "coordination/autonomous_w2/g2/releases/RELEASE_v4.json.sha256",
        "results/validation/autonomous_w2/g2/development_v1/stage_receipt.json",
        "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json",
        "results/validation/autonomous_w2/g2/development_v3/stage_receipt.json",
        "coordination/autonomous_w2/g2/releases/RELEASE_v1.json",
        "coordination/autonomous_w2/g2/releases/RELEASE_v2.json",
        "coordination/autonomous_w2/g2/releases/RELEASE_v3.json",
    ]
    artifacts = {rel: sha(ROOT / rel) for rel in artifact_paths}
    release = {
        "schema": "DDWMR_G2_W2_IMMUTABLE_RELEASE_v5",
        "release_id": "G2_W2_VOF_TASK_V1_RELEASE_5",
        "release_sequence": 5,
        "release_state": "FROZEN_256_SLAB_PROFILE_REFINEMENT_FOR_G4_AUDIT_AND_BOUNDED_DEVELOPMENT",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "workflow": "DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2",
        "published_utc": datetime.now(timezone.utc).isoformat(),
        "repository": {"branch": current_branch, "head": current_head},
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "shell": "Windows PowerShell"},
        "claim": {
            "type": "v4 signed affine full-hold variation-of-constants enclosure with unchanged 96-bit outward interval arithmetic and a prospectively frozen 256-slab profile",
            "quantifiers": "for every state in the unchanged positive-width nine-state box and every one execution-fixed label in the unchanged positive-width twelve-label image, under one constant selected voltage through [0,2]",
            "positive_claim_not_yet_made": "No v5 row outcome, safety certificate or useful action distinction is claimed at publication.",
            "candidate_hypothesis": "Replacing 16 slabs of 1/8 s with 256 slabs of 1/128 s will reduce interval wrapping enough to avoid the late-slab branch and margin failures observed in v4, without changing the theorem, task, threshold, arithmetic precision or worker limits.",
        },
        "supported_model": {
            "formulation": protocol["model"]["formulation"],
            "traction_law": protocol["model"]["phi"],
            "state_order": protocol["task"]["initial_box_state_order"],
            "initial_box": protocol["task"]["initial_box"],
            "parameter_order": protocol["model"]["fixed_label_order"],
            "parameter_bounds": protocol["model"]["fixed_label_bounds"],
            "parameter_maps": protocol["model"]["parameter_maps"],
            "fixed_constants": protocol["model"]["fixed_constants"],
            "full_hold_fixed_label_rule": "same complete label image and hash through all 256 contiguous slabs; no resampling or favorable relabeling",
            "full_hold_fixed_voltage_rule": "same selected ZOH voltage through all 256 slabs",
        },
        "method": {
            "proof_to_code_map_path": "research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v5.md",
            "implementation": {
                "primitive": "validation/autonomous_w2/g2/rational_interval_v3.py",
                "producer": "validation/autonomous_w2/g2/producer_v4.py",
                "checker": "validation/autonomous_w2/g2/checker_v4.py",
                "worker": "validation/autonomous_w2/g2/worker_v4.py",
                "runner": plan["runner_path"],
                "freeze": plan["freeze_script_path"],
                "windows_job_supervisor": "validation/autonomous_w2/g2/windows_job_supervisor.py",
            },
            "source_closure": plan["source_files"],
            "shared_trust": ["Python fractions.Fraction", "rational_interval_v3.I/Budget/sqrt_lower/outward dyadic endpoint rounding shared by producer and checker"],
            "profile": {key: profile[key] for key in ["interval_fractional_bits", "interval_operation_cap", "matrix_taylor_degree", "rational_bit_cap", "worker_wall_cap_seconds", "worker_memory_cap_bytes", "phase_wall_cap_seconds", "time_slabs", "slab_duration_s", "sqrt_bisections", "stdout_cap_bytes", "stderr_cap_bytes"]},
            "resource_failure_policy": profile["unknown_policy"],
        },
        "task": {
            "protocol_path": plan["protocol_path"],
            "protocol_sha256": plan["protocol_sha256"],
            "definition": protocol["task"],
            "actions": protocol["actions"],
            "selection_rule": protocol["selection_rule"],
            "threshold_independent_of_evaluator": True,
        },
        "development_plan": {
            "path": PLAN_REL,
            "sha256": sha(plan_path),
            "freeze_receipt_path": freeze_rel,
            "freeze_receipt_sha256": sha(ROOT / freeze_rel),
            "bindings": {item["binding_path"]: item["binding_sha256"] for item in plan["ordered_attempts"]},
            "ordered_attempts": plan["ordered_attempts"],
            "prior_native_attempts": 18,
            "planned_native_attempts": 3,
            "cumulative_if_complete": 21,
            "remaining_if_complete": 3,
            "cap": 24,
            "held_out_or_confirmation_rows": 0,
            "retry_policy": plan["retry_policy"],
        },
        "matched_development_context": {
            "prior_r3_stage_path": "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json",
            "prior_r3_stage_sha256": sha(ROOT / "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json"),
            "v4_candidate_stage_path": "results/validation/autonomous_w2/g2/development_v4/stage_receipt.json",
            "v4_candidate_stage_sha256": sha(ROOT / "results/validation/autonomous_w2/g2/development_v4/stage_receipt.json"),
            "r3_input_sha256": plan["r3_input_sha256"],
            "r3_benchmark_sha256": plan["r3_benchmark_sha256"],
            "r3_profile_sha256": plan["r3_profile_sha256"],
            "interpretation": "The v2 R3 records and v4 candidate rows use the same frozen protocol/action IDs and are consumed development data. V5 runs only its finer-profile candidate rows; no comparator or held-out data are rerun.",
        },
        "pre_run_evidence": artifacts,
        "peer_state_at_release": peer,
        "counts_and_scope": {
            "attempts_before_v5": 18,
            "v1_attempts": 6,
            "v2_attempts": 6,
            "v3_attempts": 3,
            "v4_attempts": 3,
            "v4_candidate_rows_replayed": 3,
            "v4_task_eligible_rows": 0,
            "v5_attempts_frozen": 3,
            "cumulative_if_complete": 21,
            "remaining_after_plan_if_complete": 3,
            "held_out_confirmation_rows": 0,
            "g4_confirmation_rows_per_method": 0,
            "legacy_r5_study": "800/800 NOT_RUN",
        },
        "limitations": [
            "The center-point clip witness is a single point and is not a full-cell, contact, collision or task certificate.",
            "A failed full-cell strict clip guard makes all later affine margins/progress diagnostics unusable as claims about the clipped plant.",
            "Interval arithmetic can remain too wide despite 256 slabs; resource failures remain UNKNOWN and consume attempts.",
            "Task/domain scales are explicit synthetic assumptions, not hardware operating conditions.",
            "Validated Taylor propagation and interval reachability are generic methods; G4 must assess overlap and useful effect.",
            "G2/G3/G4 and physical-platform correspondence remain UNVERIFIED; overall HOLD.",
        ],
    }
    release_path = ROOT / RELEASE_REL
    release_hash_path = ROOT / (RELEASE_REL + ".sha256")
    request_path = ROOT / REQUEST_REL
    status_versioned_path = ROOT / STATUS_VERSIONED_REL
    if any(path.exists() for path in (release_path, release_hash_path, request_path, status_versioned_path)):
        raise FileExistsError("V5_RELEASE_OR_AUDIT_REQUEST_OR_STATUS_ALREADY_EXISTS")
    write_exclusive(RELEASE_REL, release)
    release_sha = sha(release_path)
    with release_hash_path.open("x", encoding="ascii", newline="\n") as stream:
        stream.write(f"{release_sha}  {RELEASE_REL}\n")
    request = (
        "Session: DDWMR | LUNA-G2-SCOPE\n\n"
        "# G4 release audit request — W2 G2 v5 finer time partition\n\n"
        f"Release: `{RELEASE_REL}`\n\nRelease manifest SHA-256: `{release_sha}`\n\n"
        "Please audit the exact v4 inclusion proof/checker and this profile-only 256-slab refinement. Check the 1/128 s partial-slab Taylor inclusion and tail, unchanged signed matrix and fixed-label/voltage carry, parameter image, clip first-exit guard, contact reserve, pose/collision, endpoint progress, source closure, worker/operation/output limits, and the preserved v4 UNKNOWN result plus exact center-point branch fixture. Confirm the v5 plan has no retries and does not alter task geometry or threshold.\n\n"
        "The three candidate-only attempts are ordinals 19–21 after 18 counted native attempts. G2 will run them once under the shared compute lock. No R3 comparator, held-out confirmation or legacy R5/800 row is included. Please publish any audit decision in the G4-owned namespace bound to this exact v5 release hash.\n"
    )
    with request_path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(request)
    now = datetime.now(timezone.utc).isoformat()
    status = {
        "workflow": "DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "owner": "g2",
        "phase": "PUBLISHED",
        "sequence": 12,
        "utc": now,
        "branch": current_branch,
        "head": current_head,
        "working_tree_note": "Shared working tree retained; G2 writes remain within G2-owned W2 prefixes.",
        "objective": "Run the three frozen v5 finer-profile candidate rows once, preserve complete receipts, mutation-replay a proof row, and consume G4's release-bound audit.",
        "release": {"path": RELEASE_REL, "sha256": release_sha, "state": release["release_state"]},
        "artifacts": {**artifacts, RELEASE_REL: release_sha, RELEASE_REL + ".sha256": sha(release_hash_path), REQUEST_REL: sha(request_path)},
        "peer_status_observed": peer,
        "peer_release_consumed": peer.get("release_consumed"),
        "previous_release": {"path": "coordination/autonomous_w2/g2/releases/RELEASE_v4.json", "sha256": sha(ROOT / "coordination/autonomous_w2/g2/releases/RELEASE_v4.json")},
        "previous_stage": {"attempts_counted": 3, "path": "results/validation/autonomous_w2/g2/development_v4/stage_receipt.json", "sha256": sha(ROOT / "results/validation/autonomous_w2/g2/development_v4/stage_receipt.json"), "status_counts": read("results/validation/autonomous_w2/g2/development_v4/stage_receipt.json")["status_counts"]},
        "native_attempts": {"G2_limit": 24, "count_completed": 18, "count_at_release": 18, "frozen_plan_rows": 3, "cumulative_if_complete": 21, "remaining_after_plan_if_complete": 3, "held_out_rows": 0, "legacy_800_row_study": "800/800 NOT_RUN"},
        "constraints": ["No branch switch, reset, clean, commit or push.", "No peer source or manifest edits.", "R5 remains 800/800 NOT_RUN.", "No G4 confirmation inputs/outcomes are run or inspected by G2.", "All v1-v4 attempts remain preserved; no retries under those plans.", "V5 changes only the fixed time partition to 256 slabs of 1/128 s."],
        "next_action": "Run the three immutable v5 candidate rows once; preserve every receipt, mutation-replay any saved proof row and consume G4's release-bound audit decision.",
        "blocker": None,
    }
    write_exclusive(STATUS_VERSIONED_REL, status)
    tmp = ROOT / (STATUS_REL + ".sequence_12.tmp")
    with tmp.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(status, sort_keys=True, indent=2) + "\n")
        stream.flush()
    tmp.replace(ROOT / STATUS_REL)
    return {"release_path": RELEASE_REL, "release_sha256": release_sha, "status_path": STATUS_REL, "status_sequence": 12, "audit_request_path": REQUEST_REL, "plan_path": PLAN_REL, "source_count": len(plan["source_files"]), "attempt_count": len(plan["ordered_attempts"]), "peer_sequence": peer.get("sequence"), "peer_decision": peer.get("release_audit_decision")}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    print(json.dumps(publish(validate_only=args.validate_only), sort_keys=True, indent=2))
