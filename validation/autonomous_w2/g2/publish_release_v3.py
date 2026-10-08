"""Publish the immutable W2 G2 v3 arithmetic-correction candidate release."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PLAN_REL = "research/autonomous_w2/g2/development_plan_v3.json"
RELEASE_REL = "coordination/autonomous_w2/g2/releases/RELEASE_v3.json"
REQUEST_REL = "coordination/autonomous_w2/g2/AUDIT_REQUEST_TO_G4_v3.md"
STATUS_REL = "coordination/autonomous_w2/g2/STATUS.json"
STATUS_VERSIONED_REL = "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_06.json"


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


def publish() -> dict[str, Any]:
    plan = read(PLAN_REL)
    plan_path = ROOT / PLAN_REL
    status_path = ROOT / STATUS_REL
    status_before = read(STATUS_REL)
    if status_before.get("sequence") != 5 or status_before.get("native_attempts", {}).get("count_completed") != 12:
        raise ValueError("STATUS_SEQUENCE_05_OR_PRIOR_ATTEMPT_COUNT_MISMATCH")
    if plan.get("schema") != "G2_W2_DEVELOPMENT_PLAN_v3" or plan.get("planned_attempt_count") != 3 or plan.get("prior_native_attempts") != 12:
        raise ValueError("V3_PLAN_SCHEMA_OR_DENOMINATOR_MISMATCH")
    if plan.get("held_out_or_confirmation_rows") != 0 or plan.get("legacy_800_row_study") != "NOT_RUN":
        raise ValueError("V3_PLAN_CONFIRMATION_OR_LEGACY_SCOPE_MISMATCH")
    current_branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    current_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    if current_branch != plan.get("repository_branch") or current_head != plan.get("repository_head"):
        raise ValueError("REPOSITORY_BRANCH_OR_HEAD_MISMATCH")
    freeze_rel = "results/validation/autonomous_w2/g2/development_v3/freeze_receipt_v3.json"
    freeze = read(freeze_rel)
    if freeze.get("schema") != "G2_W2_FREEZE_RECEIPT_v3" or freeze.get("plan_sha256") != sha(plan_path) or freeze.get("attempt_count_frozen") != 3:
        raise ValueError("V3_FREEZE_RECEIPT_BINDING_MISMATCH")
    for rel, expected in plan["source_files"].items():
        if sha(ROOT / rel) != expected:
            raise ValueError(f"V3_SOURCE_HASH_MISMATCH:{rel}")
    protocol = read(plan["protocol_path"])
    profile = read(plan["profile_path"])
    pre_run_rel = "results/validation/autonomous_w2/g2/pre_run_validation_v3.json"
    pre_run = read(pre_run_rel)
    if pre_run.get("native_attempts_before_v3") != 12 or pre_run.get("legacy_800_row_study") != "NOT_RUN":
        raise ValueError("V3_PRERUN_RECEIPT_SCOPE_MISMATCH")
    peer = peer_snapshot()
    artifacts = {
        PLAN_REL: sha(plan_path),
        plan["profile_path"]: sha(ROOT / plan["profile_path"]),
        plan["protocol_path"]: sha(ROOT / plan["protocol_path"]),
        "research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v3.md": sha(ROOT / "research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v3.md"),
        pre_run_rel: sha(ROOT / pre_run_rel),
        freeze_rel: sha(ROOT / freeze_rel),
        "results/validation/autonomous_w2/g2/development_v1/stage_receipt.json": sha(ROOT / "results/validation/autonomous_w2/g2/development_v1/stage_receipt.json"),
        "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json": sha(ROOT / "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json"),
        "coordination/autonomous_w2/g2/releases/RELEASE_v1.json": sha(ROOT / "coordination/autonomous_w2/g2/releases/RELEASE_v1.json"),
        "coordination/autonomous_w2/g2/releases/RELEASE_v2.json": sha(ROOT / "coordination/autonomous_w2/g2/releases/RELEASE_v2.json"),
    }
    release = {
        "schema": "DDWMR_G2_W2_IMMUTABLE_RELEASE_v3",
        "release_id": "G2_W2_VOF_TASK_V1_RELEASE_3",
        "release_sequence": 3,
        "release_state": "FROZEN_ARITHMETIC_CORRECTION_CANDIDATE_FOR_G4_AUDIT_AND_BOUNDED_DEVELOPMENT",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "workflow": "DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2",
        "published_utc": datetime.now(timezone.utc).isoformat(),
        "repository": {"branch": current_branch, "head": current_head},
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "shell": "Windows PowerShell"},
        "claim": {
            "type": "same signed affine full-hold variation-of-constants enclosure as v2, evaluated using exact outward dyadic interval endpoints",
            "quantifiers": "for every initial state in the frozen positive-width nine-state box and every one execution-fixed label in the positive-width twelve-label image, under that one constant voltage for every time in [0,2]",
            "positive_claim_not_yet_made": "No row result or task-action distinction is claimed at publication. This is a frozen candidate for bounded development and an independent release-bound G4 audit.",
            "candidate_hypothesis": "Outward 96-bit dyadic endpoint rounding will prevent exact-rational denominator growth while preserving a sound interval outer image; it does not repair geometric or model dependency width.",
        },
        "supported_model": {
            "formulation": protocol["model"]["formulation"],
            "traction_law": protocol["model"]["phi"],
            "state_order": protocol["task"]["initial_box_state_order"],
            "parameter_order": protocol["model"]["fixed_label_order"],
            "parameter_bounds": protocol["model"]["fixed_label_bounds"],
            "parameter_maps": protocol["model"]["parameter_maps"],
            "fixed_constants": protocol["model"]["fixed_constants"],
            "full_hold_fixed_label_rule": "same complete label image and hash through all 16 contiguous slabs; no resampling or favorable relabeling",
            "full_hold_fixed_voltage_rule": "same selected ZOH voltage through all 16 slabs",
        },
        "method": {
            "proof_to_code_map_path": "research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v3.md",
            "implementation": {
                "primitive": "validation/autonomous_w2/g2/rational_interval_v3.py",
                "producer": "validation/autonomous_w2/g2/producer_v3.py",
                "checker": "validation/autonomous_w2/g2/checker_v3.py",
                "worker": "validation/autonomous_w2/g2/worker_v3.py",
                "runner": plan["runner_path"],
                "freeze": plan["freeze_script_path"],
                "windows_job_supervisor": "validation/autonomous_w2/g2/windows_job_supervisor.py",
            },
            "source_closure": plan["source_files"],
            "shared_trust": ["Python fractions.Fraction", "rational_interval_v3.I/Budget/sqrt_lower/outward dyadic endpoint rounding; producer and checker share this scalar arithmetic primitive"],
            "precision_and_limits": {"fractional_grid_bits": profile["interval_fractional_bits"], "interval_operation_cap": profile["interval_operation_cap"], "rational_bit_cap": profile["rational_bit_cap"], "worker_wall_seconds": profile["worker_wall_cap_seconds"], "worker_memory_bytes": profile["worker_memory_cap_bytes"], "phase_wall_seconds": profile["phase_wall_cap_seconds"], "matrix_taylor_degree": profile["matrix_taylor_degree"], "time_slabs": profile["time_slabs"], "slab_duration_s": profile["slab_duration_s"]},
            "tail_bit_precheck": {"formula": "(P+8)*(N+2)+8*(N+2)", "P": profile["interval_fractional_bits"], "N": profile["matrix_taylor_degree"], "computed_upper_bound": (int(profile["interval_fractional_bits"])+8)*(int(profile["matrix_taylor_degree"])+2)+8*(int(profile["matrix_taylor_degree"])+2), "cap": profile["rational_bit_cap"]},
            "resource_failure_policy": profile["unknown_policy"],
        },
        "task": {"protocol_path": plan["protocol_path"], "protocol_sha256": plan["protocol_sha256"], "definition": protocol["task"], "actions": protocol["actions"], "selection_rule": protocol["selection_rule"], "threshold_independent_of_evaluator": True},
        "development_plan": {"path": PLAN_REL, "sha256": sha(plan_path), "freeze_receipt_path": freeze_rel, "freeze_receipt_sha256": sha(ROOT / freeze_rel), "bindings": {item["binding_path"]: item["binding_sha256"] for item in plan["ordered_attempts"]}, "ordered_attempts": plan["ordered_attempts"], "prior_native_attempts": 12, "planned_native_attempts": 3, "cumulative_if_complete": 15, "cap": 24, "held_out_or_confirmation_rows": 0, "retry_policy": plan["retry_policy"]},
        "matched_development_context": {"prior_r3_stage_path": "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json", "prior_r3_stage_sha256": sha(ROOT / "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json"), "r3_input_sha256": plan["r3_input_sha256"], "r3_benchmark_sha256": plan["r3_benchmark_sha256"], "r3_profile_sha256": plan["r3_profile_sha256"], "interpretation": "The v2 R3 rows are same-protocol development comparators, already consumed and retained; v3 schedules only the candidate producer, so it will not rerun R3."},
        "pre_run_evidence": artifacts,
        "peer_state_at_release": peer,
        "counts_and_scope": {"attempts_before_v3": 12, "v1_execution_failures": 3, "v1_r3_replay_binding_failures": 3, "v2_candidate_resource_unknown": 3, "v2_r3_replayed_unknown": 3, "v3_attempts_frozen": 3, "cumulative_if_complete": 15, "remaining_after_plan_if_complete": 9, "held_out_confirmation_rows": 0, "g4_confirmation_rows_per_method": 0, "legacy_r5_study": "800/800 NOT_RUN"},
        "limitations": ["Strict clip-interior proof remains a prerequisite; all other clip branches are unsupported by this candidate.", "Interval matrix multiplication still relaxes state/parameter dependency and can remain too wide.", "A `UNKNOWN` row does not prove unsafety, contact loss or task impossibility.", "The task/domain scales are explicit synthetic assumptions, not source-backed hardware operating conditions.", "Validated Taylor propagation and interval reachability are generic methods; novelty is unresolved.", "G2/G3/G4 and physical-platform correspondence remain UNVERIFIED; overall HOLD."],
    }
    release_path = ROOT / RELEASE_REL
    if release_path.exists() or (ROOT / (RELEASE_REL + ".sha256")).exists() or (ROOT / REQUEST_REL).exists() or (ROOT / STATUS_VERSIONED_REL).exists():
        raise FileExistsError("V3_RELEASE_OR_AUDIT_REQUEST_OR_STATUS_ALREADY_EXISTS")
    write_exclusive(RELEASE_REL, release)
    release_sha = sha(release_path)
    (ROOT / (RELEASE_REL + ".sha256")).write_text(f"{release_sha}  {RELEASE_REL}\n", encoding="ascii")
    request = (
        "Session: DDWMR | LUNA-G2-SCOPE\n\n"
        "# G4 release audit request — W2 G2 v3 fixed-grid arithmetic candidate\n\n"
        f"Release: `{RELEASE_REL}`\n\nRelease manifest SHA-256: `{release_sha}`\n\n"
        "Please audit the exact outward-rounding inclusion lemma and implementation, profile-derived tail-bit precheck, source closure, unchanged signed model and fixed-label/voltage slab carry, clip first-exit guard, full-hold contact/collision bounds, endpoint progress, mutation checker and preserved v1/v2 evidence. Check that the fixed-grid arithmetic cannot inward-round any interval and that the serialized status remains independently replayed.\n\n"
        "This release freezes three candidate-only development attempts (ordinals 13–15) after 12 counted attempts. G2 will run them once under the shared compute lock after release publication. The three v2 R3 comparator rows are already replayed on the identical frozen protocol and will not be rerun. No held-out row, G4 confirmation or legacy R5/800 row is included. Please publish any decision in the G4-owned namespace bound to the exact v3 release hash.\n"
    )
    (ROOT / REQUEST_REL).write_text(request, encoding="utf-8")
    now = datetime.now(timezone.utc).isoformat()
    status = {
        "workflow": "DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "owner": "g2",
        "phase": "PUBLISHED",
        "sequence": 6,
        "utc": now,
        "branch": current_branch,
        "head": current_head,
        "working_tree_note": "Shared working tree is retained; G2 writes remain within G2-owned W2 prefixes.",
        "objective": "Complete bounded v3 development, independent replay/mutations and release-bound G4 audit; then issue a qualified G2 W2 disposition.",
        "release": {"path": RELEASE_REL, "sha256": release_sha, "state": release["release_state"]},
        "artifacts": {**artifacts, RELEASE_REL: release_sha, RELEASE_REL + ".sha256": sha(ROOT / (RELEASE_REL + ".sha256")), REQUEST_REL: sha(ROOT / REQUEST_REL)},
        "peer_status_observed": peer,
        "peer_release_consumed": peer.get("release_consumed"),
        "previous_release": {"path": "coordination/autonomous_w2/g2/releases/RELEASE_v2.json", "sha256": sha(ROOT / "coordination/autonomous_w2/g2/releases/RELEASE_v2.json")},
        "previous_stage": {"attempts_counted": 6, "path": "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json", "sha256": sha(ROOT / "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json"), "status_counts": read("results/validation/autonomous_w2/g2/development_v2/stage_receipt.json")["status_counts"]},
        "native_attempts": {"G2_limit": 24, "count_at_release": 12, "frozen_plan_rows": 3, "cumulative_if_complete": 15, "remaining_after_plan_if_complete": 9},
        "constraints": ["No branch switch, reset, clean, commit or push.", "No peer source or manifest edits.", "R5 800/800 remains NOT_RUN.", "No G4 confirmation inputs/outcomes are run or inspected by G2.", "All v1/v2 attempts remain preserved; no retries under those plans.", "V3 is a frozen three-row candidate-only development plan with one launch per row."],
        "next_action": "Run the three immutable v3 candidate rows once; preserve every receipt, then mutation-replay a saved proof row if one exists and consume G4's release-bound audit decision.",
        "blocker": None,
    }
    write_exclusive(STATUS_VERSIONED_REL, status)
    tmp = ROOT / (STATUS_REL + ".sequence_06.tmp")
    tmp.write_text(json.dumps(status, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    tmp.replace(status_path)
    return {"release_path": RELEASE_REL, "release_sha256": release_sha, "status_path": STATUS_REL, "status_sequence": 6, "audit_request_path": REQUEST_REL, "plan_path": PLAN_REL, "source_count": len(plan["source_files"]), "attempt_count": len(plan["ordered_attempts"]), "peer_sequence": peer.get("sequence"), "peer_decision": peer.get("release_audit_decision")}


if __name__ == "__main__":
    print(json.dumps(publish(), sort_keys=True, indent=2))
