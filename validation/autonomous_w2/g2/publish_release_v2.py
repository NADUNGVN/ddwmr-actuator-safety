"""Publish the immutable v2 correction package and peer audit request."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PLAN_REL = "research/autonomous_w2/g2/development_plan_v2.json"
PROTOCOL_REL = "research/autonomous_w2/g2/task_protocol_v1.json"
PROFILE_REL = "validation/autonomous_w2/g2/profile_v2.json"
PROOF_REL = "research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v2.md"
HANDOFF_REL = "coordination/autonomous_w2/g2/AUDIT_REQUEST_TO_G4_v2.md"
STATUS_REL = "coordination/autonomous_w2/g2/STATUS.json"
STATUS_VERSIONED_REL = "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_04.json"
RELEASE_REL = "coordination/autonomous_w2/g2/releases/RELEASE_v2.json"
VALIDATION_REL = "results/validation/autonomous_w2/g2/pre_run_validation_v2.json"
JOB_FIXTURE_REL = "results/validation/autonomous_w2/g2/job_supervisor_fixture_v1.json"
FREEZE_RECEIPT_REL = "results/validation/autonomous_w2/g2/development_v2/freeze_receipt_v2.json"
V1_FAILURE_REL = "docs/reviews/autonomous_w2/g2/W2_V1_DEVELOPMENT_FAILURE_POSTMORTEM.md"
V1_STAGE_REL = "results/validation/autonomous_w2/g2/development_v1/stage_receipt.json"
V1_RELEASE_REL = "coordination/autonomous_w2/g2/releases/RELEASE_v1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_exclusive(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True).encode("utf-8") + b"\n"
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def atomic_replace(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".sequence_04.tmp")
    raw = json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True).encode("utf-8") + b"\n"
    with temp.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def current_peer_state() -> dict[str, Any]:
    status_rel = "coordination/autonomous_w2/g4/STATUS.json"
    audit_rel = "coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v1.json"
    status_path = ROOT / status_rel
    audit_path = ROOT / audit_rel
    status_bytes = status_path.read_bytes() if status_path.is_file() else b""
    audit_bytes = audit_path.read_bytes() if audit_path.is_file() else b""
    status = json.loads(status_bytes.decode("utf-8")) if status_bytes else {}
    audit = json.loads(audit_bytes.decode("utf-8")) if audit_bytes else {}
    return {
        "status_path": status_rel if status_bytes else None,
        "status_sha256": hashlib.sha256(status_bytes).hexdigest() if status_bytes else None,
        "sequence": status.get("sequence"),
        "phase": status.get("phase"),
        "release_audit_path": audit_rel if audit_bytes else None,
        "release_audit_sha256": hashlib.sha256(audit_bytes).hexdigest() if audit_bytes else None,
        "release_audit_decision": audit.get("decision", "NOT_ISSUED"),
        "release_consumed": audit.get("peer_release_manifest_sha256"),
    }


def validate_frozen_inputs(plan: dict[str, Any]) -> dict[str, Any]:
    if plan.get("schema") != "G2_W2_DEVELOPMENT_PLAN_v2" or plan.get("plan_state") != "FROZEN_BEFORE_VERSIONED_REPAIR_ATTEMPTS":
        raise ValueError("DEVELOPMENT_PLAN_SCHEMA_OR_STATE")
    if plan.get("planned_attempt_count") != 6 or len(plan.get("ordered_attempts", [])) != 6:
        raise ValueError("DEVELOPMENT_PLAN_MUST_BIND_EXACTLY_SIX_ROWS")
    if plan.get("prior_native_attempts") != 6 or plan.get("cumulative_native_attempts_after_plan") != 12:
        raise ValueError("VERSIONED_REPAIR_ATTEMPT_ACCOUNTING")
    if plan.get("held_out_or_confirmation_rows") != 0 or plan.get("legacy_800_row_study") != "NOT_RUN":
        raise ValueError("UNEXPECTED_CONFIRMATION_OR_LEGACY_STUDY_STATE")
    if plan.get("repository_branch") != "main" or plan.get("repository_head") != subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip():
        raise ValueError("REPOSITORY_BRANCH_OR_HEAD_CHANGED_AFTER_FREEZE")
    for rel, expected in plan.get("source_files", {}).items():
        path = ROOT / rel
        if not path.is_file() or sha(path) != expected:
            raise ValueError(f"FROZEN_SOURCE_HASH_MISMATCH:{rel}")
    for rel, expected in (
        (PROTOCOL_REL, plan.get("protocol_sha256")),
        (PROFILE_REL, plan.get("profile_sha256")),
        (plan.get("r3_input_path", ""), plan.get("r3_input_sha256")),
        (plan.get("r3_benchmark_path", ""), plan.get("r3_benchmark_sha256")),
        (plan.get("r3_profile_path", ""), plan.get("r3_profile_sha256")),
    ):
        if not rel or not (ROOT / rel).is_file() or sha(ROOT / rel) != expected:
            raise ValueError(f"FROZEN_PROTOCOL_OR_BASELINE_HASH_MISMATCH:{rel}")
    protocol = json.loads((ROOT / PROTOCOL_REL).read_text(encoding="utf-8"))
    declared_action_ids = [item["id"] for item in protocol.get("actions", [])]
    if len(declared_action_ids) != 3:
        raise ValueError("PROTOCOL_ACTION_SET_MUST_HAVE_THREE_ACTIONS")
    expected_action_ids = declared_action_ids + declared_action_ids
    bindings: dict[str, str] = {}
    expected_methods = ["signed_vof_candidate"] * 3 + ["legacy_r3"] * 3
    for index, (item, expected_method, expected_action_id) in enumerate(zip(plan["ordered_attempts"], expected_methods, expected_action_ids), start=1):
        if item.get("attempt") != index or item.get("native_attempt_ordinal") != 6 + index or item.get("method") != expected_method or item.get("action_id") != expected_action_id:
            raise ValueError(f"DEVELOPMENT_ATTEMPT_ORDER_MISMATCH:{index}")
        binding_path = ROOT / item["binding_path"]
        if not binding_path.is_file() or sha(binding_path) != item.get("binding_sha256"):
            raise ValueError(f"FROZEN_BINDING_HASH_MISMATCH:{item.get('binding_path')}")
        binding = json.loads(binding_path.read_text(encoding="utf-8"))
        if binding.get("schema") != "G2_W2_ROW_BINDING_v2" or binding.get("attempt") != index or binding.get("native_attempt_ordinal") != 6 + index or binding.get("method") != expected_method or binding.get("action_id") != item.get("action_id") or binding.get("prior_v1_attempt_path") != item.get("prior_v1_attempt_path"):
            raise ValueError(f"FROZEN_BINDING_CONTENT_MISMATCH:{item.get('binding_path')}")
        if binding.get("source_files") != plan["source_files"]:
            raise ValueError(f"FROZEN_BINDING_SOURCE_CLOSURE_MISMATCH:{item.get('binding_path')}")
        bindings[item["binding_path"]] = sha(binding_path)
    freeze_path = ROOT / FREEZE_RECEIPT_REL
    if not freeze_path.is_file():
        raise FileNotFoundError(f"FREEZE_RECEIPT_MISSING:{FREEZE_RECEIPT_REL}")
    freeze_receipt = json.loads(freeze_path.read_text(encoding="utf-8"))
    if freeze_receipt.get("schema") != "G2_W2_FREEZE_RECEIPT_v2" or freeze_receipt.get("plan_sha256") != sha(ROOT / PLAN_REL) or freeze_receipt.get("native_attempts_at_freeze") != plan.get("prior_native_attempts"):
        raise ValueError("FREEZE_RECEIPT_PLAN_OR_COUNT_MISMATCH")
    for rel in (RELEASE_REL, RELEASE_REL + ".sha256", HANDOFF_REL, STATUS_VERSIONED_REL, STATUS_REL + ".sequence_04.tmp"):
        if (ROOT / rel).exists():
            raise FileExistsError(f"RELEASE_OUTPUT_ALREADY_EXISTS:{rel}")
    validation = json.loads((ROOT / VALIDATION_REL).read_text(encoding="utf-8"))
    job_fixture = json.loads((ROOT / JOB_FIXTURE_REL).read_text(encoding="utf-8"))
    if validation.get("native_attempts_before_receipt") != 6 or validation.get("native_attempts_in_v2_plan") != 0 or validation.get("held_out_rows") != 0 or validation.get("legacy_800_row_study") != "NOT_RUN":
        raise ValueError("PRE_RUN_VALIDATION_COUNT_MISMATCH")
    if job_fixture.get("status") != "PASS" or job_fixture.get("native_development_attempts") != 0 or job_fixture.get("no_query_or_evaluator_called") is not True:
        raise ValueError("JOB_SUPERVISOR_FIXTURE_NOT_PASSED")
    status = json.loads((ROOT / STATUS_REL).read_text(encoding="utf-8"))
    if status.get("sequence") != 3 or status.get("head") != plan.get("repository_head"):
        raise ValueError("G2_STATUS_SEQUENCE_03_OR_HEAD_MISMATCH")
    for rel in (V1_RELEASE_REL, V1_STAGE_REL, V1_FAILURE_REL):
        if not (ROOT / rel).is_file():
            raise FileNotFoundError(f"V1_FAILURE_PROVENANCE_MISSING:{rel}")
    return {"bindings": bindings, "peer_state": current_peer_state(), "freeze_receipt_sha256": sha(freeze_path)}


def publish(*, dry_run: bool = False) -> dict[str, Any]:
    plan_path = ROOT / PLAN_REL
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    protocol_path = ROOT / PROTOCOL_REL
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    profile_path = ROOT / PROFILE_REL
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    validation_path = ROOT / VALIDATION_REL
    job_fixture_path = ROOT / JOB_FIXTURE_REL
    for path in (validation_path, job_fixture_path):
        if not path.is_file():
            raise FileNotFoundError(f"REQUIRED_PRE_RUN_EVIDENCE_MISSING:{path.relative_to(ROOT)}")
    g2_status_path = ROOT / STATUS_REL
    status_before = json.loads(g2_status_path.read_text(encoding="utf-8"))
    frozen = validate_frozen_inputs(plan)
    g4_peer = frozen["peer_state"]
    binding_hashes = {item["binding_path"]: item["binding_sha256"] for item in plan["ordered_attempts"]}
    artifacts = {
        PLAN_REL: sha(plan_path),
        PROTOCOL_REL: sha(protocol_path),
        PROFILE_REL: sha(profile_path),
        PROOF_REL: sha(ROOT / PROOF_REL),
        VALIDATION_REL: sha(validation_path),
        JOB_FIXTURE_REL: sha(job_fixture_path),
        FREEZE_RECEIPT_REL: frozen["freeze_receipt_sha256"],
        V1_FAILURE_REL: sha(ROOT / V1_FAILURE_REL),
        V1_STAGE_REL: sha(ROOT / V1_STAGE_REL),
        V1_RELEASE_REL: sha(ROOT / V1_RELEASE_REL),
    }
    release = {
        "schema": "DDWMR_G2_W2_IMMUTABLE_RELEASE_v2",
        "release_id": "G2_W2_VOF_TASK_V1_RELEASE_2",
        "release_sequence": 2,
        "release_state": "VERSIONED_CORRECTION_PRE_RUN_CANDIDATE_FOR_G4_AUDIT",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "workflow": "DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2",
        "published_utc": datetime.now(timezone.utc).isoformat(),
        "repository": {"branch": plan["repository_branch"], "head": plan["repository_head"]},
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "shell": "Windows PowerShell"},
        "claim": {
            "type": "sound signed interval variation-of-constants full-hold enclosure on a strictly clip-interior affine subclass, with full-hold collision/contact checks and endpoint progress",
            "quantifiers": "for every initial state in the frozen positive-width nine-state box and every one execution-fixed label in the positive-width twelve-label cell, for the same one constant voltage across all slabs and all t in [0,2]",
            "positive_claim_not_yet_made": "No task-action advantage is claimed before the six frozen v2 repair development rows, exact proof replay, and G4 audit. V1's six failed rows are preserved, count against the 24-attempt cap, and are not confirmation data.",
        },
        "method": {
            "supported_law": protocol["model"]["phi"],
            "model_formulation": protocol["model"]["formulation"],
            "state_order": protocol["task"]["initial_box_state_order"],
            "fixed_label_order": protocol["model"]["fixed_label_order"],
            "fixed_parameter_bounds": protocol["model"]["fixed_label_bounds"],
            "parameter_maps": protocol["model"]["parameter_maps"],
            "slab_count": profile["time_slabs"],
            "slab_duration_s": profile["slab_duration_s"],
            "matrix_taylor_degree": profile["matrix_taylor_degree"],
            "tail": profile["tail_bound"],
            "python_int_string_digit_cap": profile["python_int_string_digit_cap"],
            "integer_output_policy": profile["integer_output_policy"],
            "equation_to_code_map_path": PROOF_REL,
            "source_closure": plan["source_files"],
            "shared_trust": ["Python fractions.Fraction", "validation/autonomous_w2/g2/rational_interval_v2.py::I/Budget/sqrt_lower/qs; producer and checker share this exact interval arithmetic and bounded serializer"],
        },
        "task": {
            "protocol_path": PROTOCOL_REL,
            "protocol_sha256": plan["protocol_sha256"],
            "task_definition": protocol["task"],
            "actions_in_order": protocol["actions"],
            "progress_rule": protocol["selection_rule"],
            "candidate_progress_output": "full-hold sum of per-slab integral enclosures for u*cos(theta), with initial p_x cancelled",
            "task_status_semantics": "CERTIFIED requires the same replayed full-hold collision/contact proof and progress lower bound >=7/20 m; UNKNOWN is not unsafety or task infeasibility",
        },
        "r3_comparator": {
            "input_path": plan["r3_input_path"],
            "input_sha256": plan["r3_input_sha256"],
            "benchmark_path": plan["r3_benchmark_path"],
            "benchmark_sha256": plan["r3_benchmark_sha256"],
            "profile_path": plan["r3_profile_path"],
            "profile_sha256": plan["r3_profile_sha256"],
            "method_label": "preserved R3 comparison-radius evaluator; one whole-hold panel; prior pilot approximation orders, same W2 outer 60 s / 1 GiB caps; separate R3 safety and R2 endpoint-progress replay",
            "legacy_archive_changed": False,
        },
        "development_plan": {
            "path": PLAN_REL,
            "sha256": sha(plan_path),
            "bindings": binding_hashes,
            "ordered_attempts": plan["ordered_attempts"],
            "total_native_attempt_cap": plan["attempt_limit"],
            "rows_planned": plan["planned_attempt_count"],
            "worker_and_replay_caps": {"wall_seconds": profile["worker_wall_cap_seconds"], "memory_bytes": profile["worker_memory_cap_bytes"], "processes": profile["worker_process_cap"]},
            "phase_cap_seconds": profile["phase_wall_cap_seconds"],
            "worker_arithmetic_caps": {"interval_operations": profile["interval_operation_cap"], "rational_bits": profile["rational_bit_cap"]},
            "retries": "none within a frozen plan; this v2 plan is a versioned, explicitly counted re-evaluation after v1 implementation failures",
            "prior_native_attempts": plan["prior_native_attempts"],
            "cumulative_native_attempts_after_plan": plan["cumulative_native_attempts_after_plan"],
            "prior_plan_path": "research/autonomous_w2/g2/development_plan_v1.json",
            "prior_plan_sha256": sha(ROOT / "research/autonomous_w2/g2/development_plan_v1.json"),
            "prior_stage_receipt_path": V1_STAGE_REL,
            "prior_stage_receipt_sha256": sha(ROOT / V1_STAGE_REL),
            "freeze_receipt_path": FREEZE_RECEIPT_REL,
            "freeze_receipt_sha256": frozen["freeze_receipt_sha256"],
        },
        "implementation": {
            "producer": "validation/autonomous_w2/g2/producer_v2.py",
            "checker": "validation/autonomous_w2/g2/checker_v2.py",
            "worker": "validation/autonomous_w2/g2/worker_v2.py",
            "runner": plan["runner_path"],
            "windows_job_supervisor": "validation/autonomous_w2/g2/windows_job_supervisor.py",
            "r3_worker": "validation/autonomous_w2/g2/r3_baseline_worker_v2.py",
            "r3_checker": "validation/autonomous_w2/g2/r3_baseline_checker_v2.py",
            "release_publisher": "validation/autonomous_w2/g2/publish_release_v2.py",
            "release_publisher_sha256": plan["source_files"]["validation/autonomous_w2/g2/publish_release_v2.py"],
            "runner_no_retry_and_hash_guards": True,
        },
        "pre_run_evidence": artifacts,
        "counts_at_release": {
            "native_attempts_before_v2_plan": 6,
            "prior_candidate_rows_run": 3,
            "prior_r3_rows_run": 3,
            "prior_v1_status_counts": {"candidate_execution_failure": 3, "r3_replay_binding_failure": 3},
            "v2_rows_planned": 6,
            "cumulative_attempts_if_completed": 12,
            "cumulative_attempt_cap": 24,
            "held_out_confirmation_rows": 0,
            "g4_confirmation_rows_per_method": 0,
            "legacy_r5_study": "800/800 NOT_RUN",
            "historical_r3_archive": "unchanged; consumed records retained as development context",
        },
        "peer_state_at_release": g4_peer,
        "v1_correction_basis": {
            "postmortem_path": V1_FAILURE_REL,
            "postmortem_sha256": sha(ROOT / V1_FAILURE_REL),
            "candidate_failure": "Python's 4,300-digit default integer conversion cap while serializing an exact squared-distance rational; v2 uses a bit-cap-consistent bounded conversion limit and counts scalar serialization against the rational budget.",
            "r3_failure": "R3 replay requires a semantic JSON benchmark hash; v1 passed the byte-level benchmark file hash. V2 keeps both hashes in their separate roles.",
            "task_domain_or_threshold_changed": False,
        },
        "known_limitations": [
            "The method only applies after strict interior of both clip branches is established on every closed slab; otherwise UNKNOWN.",
            "Interval matrix powers can decorrelate the same labels across terms/slabs and grow too wide; fixed labels remain an outer hull, not resampled.",
            "The task and parameter scale are synthetic and are not sourced hardware or CommonRoad operating conditions.",
            "Generic validated Taylor propagation, parameter augmentation, and interval IVP inclusion are established techniques; novelty is unresolved pending G4.",
            "G2/G3/G4 and physical-platform correspondence remain UNVERIFIED; overall disposition remains HOLD.",
        ],
    }
    if dry_run:
        return {
            "dry_run": True,
            "release_id": release["release_id"],
            "repository": release["repository"],
            "source_count": len(plan["source_files"]),
            "binding_count": len(binding_hashes),
            "peer_state": g4_peer,
            "outputs_absent": True,
            "legacy_800_row_study": "NOT_RUN",
        }
    release_path = ROOT / RELEASE_REL
    if release_path.exists() or (ROOT / (RELEASE_REL + ".sha256")).exists():
        raise FileExistsError("RELEASE_V2_ALREADY_EXISTS")
    write_exclusive(release_path, release)
    release_sha = sha(release_path)
    (ROOT / (RELEASE_REL + ".sha256")).write_text(f"{release_sha}  {RELEASE_REL}\n", encoding="ascii")
    request = (
        "Session: DDWMR | LUNA-G2-SCOPE\n\n"
        "# G4 audit request — G2 W2 release v2 (correction after v1 failures)\n\n"
        f"Release: `{RELEASE_REL}`\n\n"
        f"Release manifest SHA-256: `{release_sha}`\n\n"
        f"Development plan: `{PLAN_REL}` (SHA-256 `{sha(plan_path)}`); it freezes six versioned repair attempts after six counted v1 failures.\n\n"
        f"V1 release SHA-256: `{sha(ROOT / V1_RELEASE_REL)}`. V1 failure postmortem: `{V1_FAILURE_REL}` (SHA-256 `{sha(ROOT / V1_FAILURE_REL)}`). The task/domain/threshold are unchanged. Candidate v1 failed only at exact-rational text serialization; R3 v1 replay rejected the byte-hash/semantic-hash mismatch.\n\n"
        "Please independently audit the unchanged signed-flow inclusion and the v2 bounded serializer, replay/hash correction, source closure, task, endpoint progress, fixed-label chaining, runner, and prior-art overlap. Issue your versioned scoped decision in the G4-owned namespace, binding the exact v2 release hash. G2 will run the six frozen v2 development rows once under the shared compute lock; no confirmation input or result is included here.\n\n"
        "The v1 failures remain counted (6/24); if v2 completes, cumulative development attempts will be 12/24. R5 remains 800/800 NOT_RUN. G2 has not run any G4 held-out query.\n"
    )
    handoff_path = ROOT / HANDOFF_REL
    if handoff_path.exists():
        raise FileExistsError("G4_AUDIT_REQUEST_ALREADY_EXISTS")
    handoff_path.parent.mkdir(parents=True, exist_ok=True)
    handoff_path.write_text(request, encoding="utf-8")
    status = {
        "workflow": "DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "owner": "g2",
        "phase": "PUBLISHED",
        "sequence": 4,
        "utc": datetime.now(timezone.utc).isoformat(),
        "branch": plan["repository_branch"],
        "head": plan["repository_head"],
        "working_tree_note": "Shared tree contains pre-existing G4 and project edits; G2 writes remain inside G2-owned W2 prefixes.",
        "objective": "Publish the versioned correction for the two v1 implementation failures, then complete bounded matched development and audit replay.",
        "release": {"path": RELEASE_REL, "sha256": release_sha, "state": release["release_state"]},
        "artifacts": {**artifacts, RELEASE_REL: release_sha, HANDOFF_REL: sha(handoff_path), PLAN_REL: sha(plan_path)},
        "peer_status_observed": g4_peer,
        "peer_release_consumed": g4_peer.get("release_consumed"),
        "previous_release": {"path": V1_RELEASE_REL, "sha256": sha(ROOT / V1_RELEASE_REL)},
        "previous_stage": {"path": V1_STAGE_REL, "sha256": sha(ROOT / V1_STAGE_REL), "attempts_counted": 6, "status_counts": {"EXECUTION_FAILURE": 3, "AUDIT_FAILURE_OR_RESOURCE_UNKNOWN": 3}},
        "native_attempts": {"G2_limit": 24, "count_at_release": 6, "frozen_plan_rows": 6, "cumulative_if_complete": 12},
        "constraints": [
            "No branch switch, reset, clean, commit, or push.",
            "No peer source or manifest edits.",
            "Legacy R5 800-row study remains 800/800 NOT_RUN.",
            "No G4 confirmation outputs inspected or executed by G2.",
            "V1 failed rows remain preserved and count against the 24-attempt cap.",
            "V2 freezes one worker launch per same development ID; these remain development, not confirmation.",
        ],
        "next_action": "Run the six immutable v2 candidate/R3 repair development rows once; then replay mutations and consume G4's release-bound audit decision.",
        "blocker": None,
    }
    status_versioned_path = ROOT / STATUS_VERSIONED_REL
    if status_versioned_path.exists():
        raise FileExistsError("STATUS_SEQUENCE_04_ALREADY_EXISTS")
    write_exclusive(status_versioned_path, status)
    atomic_replace(g2_status_path, status)
    return {"release_path": RELEASE_REL, "release_sha256": release_sha, "status_path": STATUS_REL, "status_sequence": 4, "audit_request_path": HANDOFF_REL}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="validate all release inputs without writing a release")
    args = parser.parse_args()
    print(json.dumps(publish(dry_run=args.dry_run), sort_keys=True, indent=2))
