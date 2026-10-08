"""Freeze three v4 candidate-only development attempts after v1-v3 history."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PLAN_REL = "research/autonomous_w2/g2/development_plan_v4.json"
BINDING_DIR_REL = "research/autonomous_w2/g2/bindings_v4"
RESULT_ROOT_REL = "results/validation/autonomous_w2/g2/development_v4"
FREEZE_RECEIPT_REL = f"{RESULT_ROOT_REL}/freeze_receipt_v4.json"
PROTOCOL_REL = "research/autonomous_w2/g2/task_protocol_v1.json"
PROFILE_REL = "validation/autonomous_w2/g2/profile_v4.json"
RUNNER_REL = "validation/autonomous_w2/g2/run_stage_v4.py"
R3_INPUT_REL = "research/autonomous_w2/g2/r3_baseline_input_v1.json"
R3_BENCHMARK_REL = "research/autonomous_w2/g2/r3_baseline_benchmark_v1.json"
R3_PROFILE_REL = "research/autonomous_w2/g2/r3_baseline_profile_v1.json"
ACTION_IDS = ["W2_G2_DEV_001_ZERO", "W2_G2_DEV_001_NOMINAL", "W2_G2_DEV_001_ALTERNATIVE"]

SOURCE_PATHS = [
    "AGENTS.md",
    "docs/DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2.md",
    "docs/CODEX_TO_LUNA_G2_AUTONOMOUS_COMPLETION_W2.md",
    "docs/reviews/CODEX_DDWMR_SCOPE_PROGRESS_VERIFICATION_2026_10_07.md",
    "docs/reviews/GPT_TO_CODEX_G2_VALIDATION_R3_SCIENTIFIC_REVIEW_FULL_HANDOFF.md",
    "docs/reviews/CODEX_G2_R18_TWO_ROW_ENCLOSURE_DIAGNOSIS_REVIEW.md",
    "docs/reviews/LUNA_TO_CODEX_G2_R18_TWO_ROW_ENCLOSURE_DIAGNOSIS.md",
    "docs/reviews/CODEX_G2_R19_STRUCTURE_PRESERVING_ENCLOSURE_REVIEW.md",
    "docs/reviews/CODEX_G2_R20_DEGREE_ZERO_AND_PAIR_FEASIBILITY_REVIEW.md",
    "docs/reviews/CODEX_G2_R21_PAIR_FEASIBILITY_ADVERSARIAL_AUDIT_REVIEW.md",
    "docs/reviews/CODEX_G2_R24_PAIRED_BOUND_AND_THRESHOLD_AUDIT_REVIEW.md",
    "docs/reviews/CODEX_G2_R26_PROSPECTIVE_FORMAL_TASK_SCREEN_REVIEW.md",
    "docs/reviews/CODEX_G4_AUER_R24_ACTION_ORDERING_PRIOR_ART_AUDIT_REVIEW.md",
    "docs/reviews/autonomous_w2/g2/W2_V1_DEVELOPMENT_FAILURE_POSTMORTEM.md",
    "docs/reviews/autonomous_w2/g2/W2_V3_DEVELOPMENT_FAILURE_POSTMORTEM.md",
    "research_context/MASTER_RESEARCH_CONTEXT_v2.md",
    "research_context/DECISION_LOG.md",
    "research_context/LITERATURE_MATRIX.md",
    "research_context/REVIEW_GATE.md",
    "research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md",
    "research/benchmarks/G2_DECISION_RELEVANT_STUDY_PROTOCOL_CANDIDATE_v1.md",
    "research/autonomous_w2/g2/HYPOTHESIS_AND_TASK_PREIMPLEMENTATION_v1.md",
    "research/autonomous_w2/g2/ANALYTIC_FEASIBILITY_SCREEN_v1.md",
    "research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v1.md",
    "research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v2.md",
    "research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v3.md",
    "research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v4.md",
    "research/autonomous_w2/g2/development_plan_v1.json",
    "research/autonomous_w2/g2/development_plan_v2.json",
    "research/autonomous_w2/g2/development_plan_v3.json",
    "research/autonomous_w2/g2/task_protocol_v1.json",
    "research/autonomous_w2/g2/r3_baseline_input_v1.json",
    "research/autonomous_w2/g2/r3_baseline_benchmark_v1.json",
    "research/autonomous_w2/g2/r3_baseline_profile_v1.json",
    "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_02.json",
    "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_03.json",
    "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_04.json",
    "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_05.json",
    "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_06.json",
    "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_07.json",
    "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_08.json",
    "coordination/autonomous_w2/g2/releases/RELEASE_v1.json",
    "coordination/autonomous_w2/g2/releases/RELEASE_v1.json.sha256",
    "coordination/autonomous_w2/g2/releases/RELEASE_v2.json",
    "coordination/autonomous_w2/g2/releases/RELEASE_v2.json.sha256",
    "coordination/autonomous_w2/g2/releases/RELEASE_v3.json",
    "coordination/autonomous_w2/g2/releases/RELEASE_v3.json.sha256",
    "coordination/autonomous_w2/g2/AUDIT_REQUEST_TO_G4_v3.md",
    "results/validation/autonomous_w2/g2/development_v1/freeze_receipt_v1.json",
    "results/validation/autonomous_w2/g2/development_v1/stage_receipt.json",
    "results/validation/autonomous_w2/g2/development_v2/freeze_receipt_v2.json",
    "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json",
    "results/validation/autonomous_w2/g2/development_v3/freeze_receipt_v3.json",
    "results/validation/autonomous_w2/g2/development_v3/stage_receipt.json",
    "results/validation/autonomous_w2/g2/pre_run_validation_v1.json",
    "results/validation/autonomous_w2/g2/pre_run_validation_v2.json",
    "results/validation/autonomous_w2/g2/pre_run_validation_v3.json",
    "results/validation/autonomous_w2/g2/pre_run_validation_v4.json",
    "results/validation/autonomous_w2/g2/fixtures/fixed_grid_arithmetic_v3.json",
    "results/validation/autonomous_w2/g2/fixtures/status_aggregation_v4.json",
    "validation/autonomous_w2/g2/rational_interval.py",
    "validation/autonomous_w2/g2/producer.py",
    "validation/autonomous_w2/g2/checker.py",
    "validation/autonomous_w2/g2/worker.py",
    "validation/autonomous_w2/g2/fixtures.py",
    "validation/autonomous_w2/g2/audit_mutations.py",
    "validation/autonomous_w2/g2/analytic_task_screen.py",
    "validation/autonomous_w2/g2/r3_baseline_worker.py",
    "validation/autonomous_w2/g2/r3_baseline_checker.py",
    "validation/autonomous_w2/g2/r3_input_fixtures.py",
    "validation/autonomous_w2/g2/pre_run_validation.py",
    "validation/autonomous_w2/g2/job_supervisor_fixture.py",
    "validation/autonomous_w2/g2/__init__.py",
    "validation/autonomous_w2/g2/freeze_development_v1.py",
    "validation/autonomous_w2/g2/publish_release_v1.py",
    "validation/autonomous_w2/g2/run_stage.py",
    "validation/autonomous_w2/g2/rational_interval_v2.py",
    "validation/autonomous_w2/g2/producer_v2.py",
    "validation/autonomous_w2/g2/checker_v2.py",
    "validation/autonomous_w2/g2/worker_v2.py",
    "validation/autonomous_w2/g2/r3_baseline_worker_v2.py",
    "validation/autonomous_w2/g2/r3_baseline_checker_v2.py",
    "validation/autonomous_w2/g2/audit_mutations_v2.py",
    "validation/autonomous_w2/g2/integer_serialization_fixture_v2.py",
    "validation/autonomous_w2/g2/pre_run_validation_v2.py",
    "validation/autonomous_w2/g2/freeze_development_v2.py",
    "validation/autonomous_w2/g2/publish_release_v2.py",
    "validation/autonomous_w2/g2/profile_v1.json",
    "validation/autonomous_w2/g2/profile_v2.json",
    "validation/autonomous_w2/g2/rational_interval_v3.py",
    "validation/autonomous_w2/g2/producer_v3.py",
    "validation/autonomous_w2/g2/checker_v3.py",
    "validation/autonomous_w2/g2/worker_v3.py",
    "validation/autonomous_w2/g2/audit_mutations_v3.py",
    "validation/autonomous_w2/g2/fixed_grid_arithmetic_fixtures_v3.py",
    "validation/autonomous_w2/g2/pre_run_validation_v3.py",
    "validation/autonomous_w2/g2/freeze_development_v3.py",
    "validation/autonomous_w2/g2/publish_release_v3.py",
    "validation/autonomous_w2/g2/profile_v3.json",
    "validation/autonomous_w2/g2/run_stage_v3.py",
    "validation/autonomous_w2/g2/producer_v4.py",
    "validation/autonomous_w2/g2/checker_v4.py",
    "validation/autonomous_w2/g2/worker_v4.py",
    "validation/autonomous_w2/g2/audit_mutations_v4.py",
    "validation/autonomous_w2/g2/status_aggregation_fixtures_v4.py",
    "validation/autonomous_w2/g2/pre_run_validation_v4.py",
    "validation/autonomous_w2/g2/freeze_development_v4.py",
    "validation/autonomous_w2/g2/publish_release_v4.py",
    "validation/autonomous_w2/g2/profile_v4.json",
    RUNNER_REL,
    "validation/autonomous_w2/g2/windows_job_supervisor.py",
    "validation/g2/__init__.py",
    "validation/g2/evaluator.py",
    "validation/g2/checker.py",
    "validation/g2/endpoint_r2.py",
    "validation/g2/endpoint_checker_r2.py",
    "validation/g2/model.py",
    "validation/g2/polynomial.py",
    "validation/g2/interval.py",
    "validation/g2/rational.py",
    "validation/g2/hashing.py",
    "validation/configs/benchmark_v1.json",
    "validation/configs/dev_pilot_r3_v1.json",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True).encode("utf-8") + b"\n")
        stream.flush()


def freeze() -> dict[str, Any]:
    plan_path = ROOT / PLAN_REL
    binding_dir = ROOT / BINDING_DIR_REL
    result_root = ROOT / RESULT_ROOT_REL
    receipt_path = ROOT / FREEZE_RECEIPT_REL
    if plan_path.exists() or binding_dir.exists() or result_root.exists():
        raise FileExistsError("V4_FROZEN_PLAN_OR_BINDINGS_OR_RESULTS_ALREADY_EXIST")
    for stage in ("development_v1", "development_v2", "development_v3"):
        base = ROOT / "results/validation/autonomous_w2/g2" / stage
        for file in sorted(base.rglob("*")):
            if file.is_file():
                SOURCE_PATHS.append(file.relative_to(ROOT).as_posix())
    for version in ("v1", "v2", "v3"):
        base = ROOT / "research/autonomous_w2/g2" / f"bindings_{version}"
        for file in sorted(base.glob("*.json")):
            SOURCE_PATHS.append(file.relative_to(ROOT).as_posix())
    source_files = {rel: sha(ROOT / rel) for rel in sorted(set(SOURCE_PATHS))}
    protocol_sha = sha(ROOT / PROTOCOL_REL)
    profile_sha = sha(ROOT / PROFILE_REL)
    runner_sha = source_files[RUNNER_REL]
    freeze_sha = source_files["validation/autonomous_w2/g2/freeze_development_v4.py"]
    publisher_sha = source_files["validation/autonomous_w2/g2/publish_release_v4.py"]
    status8 = json.loads((ROOT / "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_08.json").read_text(encoding="utf-8"))
    if status8.get("sequence") != 8 or status8.get("native_attempts", {}).get("count_completed") != 15:
        raise ValueError("PRIOR_G2_STATUS_OR_ATTEMPT_COUNT_MISMATCH")
    actions = {row["id"]: row for row in json.loads((ROOT / PROTOCOL_REL).read_text(encoding="utf-8"))["actions"]}
    attempts = []
    for index, action_id in enumerate(ACTION_IDS, start=1):
        attempts.append({
            "attempt": index,
            "native_attempt_ordinal": 15 + index,
            "method": "signed_vof_candidate",
            "action_id": action_id,
            "binding_path": f"{BINDING_DIR_REL}/attempt_{index:02d}.json",
            "prior_development_attempt_path": f"results/validation/autonomous_w2/g2/development_v3/attempt_{index:02d}_{action_id}",
        })
    r3_input_sha = sha(ROOT / R3_INPUT_REL)
    r3_benchmark_sha = sha(ROOT / R3_BENCHMARK_REL)
    r3_profile_sha = sha(ROOT / R3_PROFILE_REL)
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    if branch != "main" or head != "94c60f627a2ce1a8d52101050bdc0ce9d2e59afe":
        raise ValueError("REPOSITORY_BRANCH_OR_HEAD_DIFFERS_FROM_W2_BASELINE")
    if json.loads((ROOT / R3_INPUT_REL).read_text(encoding="utf-8")).get("source_commit") != head:
        raise ValueError("R3_INPUT_COMMIT_DIFFERS_FROM_W2_HEAD")
    for item in attempts:
        binding = {
            "schema": "G2_W2_ROW_BINDING_v4",
            "session": "DDWMR | LUNA-G2-SCOPE",
            "attempt": item["attempt"],
            "method": item["method"],
            "action_id": item["action_id"],
            "action": actions[item["action_id"]],
            "plan_id": "G2_W2_DEV_PLAN_V4",
            "protocol_path": PROTOCOL_REL,
            "protocol_sha256": protocol_sha,
            "profile_path": PROFILE_REL,
            "profile_sha256": profile_sha,
            "plan_path": PLAN_REL,
            "binding_path": item["binding_path"],
            "runner_path": RUNNER_REL,
            "runner_sha256": runner_sha,
            "freeze_script_sha256": freeze_sha,
            "publisher_sha256": publisher_sha,
            "source_files": source_files,
            "result_root": RESULT_ROOT_REL,
            "attempt_kind": "counted native development re-evaluation; not held-out confirmation",
            "native_attempt_ordinal": item["native_attempt_ordinal"],
            "prior_native_attempts": 15,
            "prior_development_attempt_path": item["prior_development_attempt_path"],
            "versioned_correction_reason": "v3 computed per-slab ranges but producer status aggregation used flat keys absent from its nested slab proof schema; v4 corrects only those lookups, with pre-run status-path fixtures",
            "r3_input_path": R3_INPUT_REL,
            "r3_input_sha256": r3_input_sha,
            "r3_benchmark_path": R3_BENCHMARK_REL,
            "r3_benchmark_sha256": r3_benchmark_sha,
            "r3_profile_path": R3_PROFILE_REL,
            "r3_profile_sha256": r3_profile_sha,
        }
        dump(ROOT / item["binding_path"], binding)
        item["binding_sha256"] = sha(ROOT / item["binding_path"])
    plan = {
        "schema": "G2_W2_DEVELOPMENT_PLAN_v4",
        "plan_id": "G2_W2_DEV_PLAN_V4",
        "plan_path": PLAN_REL,
        "session": "DDWMR | LUNA-G2-SCOPE",
        "repository_branch": branch,
        "repository_head": head,
        "protocol_id": "G2_W2_VOF_TASK_V1",
        "plan_state": "FROZEN_BEFORE_VERSIONED_REPAIR_ATTEMPTS",
        "attempt_limit": 24,
        "prior_native_attempts": 15,
        "cumulative_native_attempts_after_plan": 18,
        "planned_attempt_count": 3,
        "protocol_path": PROTOCOL_REL,
        "protocol_sha256": protocol_sha,
        "profile_path": PROFILE_REL,
        "profile_sha256": profile_sha,
        "r3_input_path": R3_INPUT_REL,
        "r3_input_sha256": r3_input_sha,
        "r3_benchmark_path": R3_BENCHMARK_REL,
        "r3_benchmark_sha256": r3_benchmark_sha,
        "r3_profile_path": R3_PROFILE_REL,
        "r3_profile_sha256": r3_profile_sha,
        "runner_path": RUNNER_REL,
        "runner_sha256": runner_sha,
        "freeze_script_path": "validation/autonomous_w2/g2/freeze_development_v4.py",
        "freeze_script_sha256": freeze_sha,
        "publisher_path": "validation/autonomous_w2/g2/publish_release_v4.py",
        "publisher_sha256": publisher_sha,
        "source_files": source_files,
        "result_root": RESULT_ROOT_REL,
        "compute_lock_path": "coordination/autonomous_w2/COMPUTE.lock",
        "ordered_attempts": attempts,
        "retry_policy": "one worker launch per frozen action; no retries; all v1-v3 attempts remain counted; these three same-ID rows are development only",
        "prior_release_path": "coordination/autonomous_w2/g2/releases/RELEASE_v3.json",
        "prior_release_sha256": sha(ROOT / "coordination/autonomous_w2/g2/releases/RELEASE_v3.json"),
        "prior_stage_receipt_path": "results/validation/autonomous_w2/g2/development_v3/stage_receipt.json",
        "prior_stage_receipt_sha256": sha(ROOT / "results/validation/autonomous_w2/g2/development_v3/stage_receipt.json"),
        "held_out_or_confirmation_rows": 0,
        "legacy_800_row_study": "NOT_RUN",
    }
    dump(plan_path, plan)
    receipt = {
        "schema": "G2_W2_FREEZE_RECEIPT_v4",
        "plan_path": PLAN_REL,
        "plan_sha256": sha(plan_path),
        "source_count": len(source_files),
        "source_files": source_files,
        "binding_paths": [item["binding_path"] for item in attempts],
        "binding_sha256": {item["binding_path"]: sha(ROOT / item["binding_path"]) for item in attempts},
        "attempt_count_frozen": len(attempts),
        "native_attempts_at_freeze": 15,
        "cumulative_attempt_limit": 24,
    }
    dump(receipt_path, receipt)
    return receipt


if __name__ == "__main__":
    print(json.dumps(freeze(), sort_keys=True, indent=2))
