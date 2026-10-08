"""Freeze v2 repair attempts after preserving the failed v1 development stage."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PLAN_REL = "research/autonomous_w2/g2/development_plan_v2.json"
BINDING_DIR_REL = "research/autonomous_w2/g2/bindings_v2"
RESULT_ROOT_REL = "results/validation/autonomous_w2/g2/development_v2"
FREEZE_RECEIPT_REL = "results/validation/autonomous_w2/g2/development_v2/freeze_receipt_v2.json"
PROTOCOL_REL = "research/autonomous_w2/g2/task_protocol_v1.json"
PROFILE_REL = "validation/autonomous_w2/g2/profile_v2.json"
RUNNER_REL = "validation/autonomous_w2/g2/run_stage_v2.py"
R3_INPUT_REL = "research/autonomous_w2/g2/r3_baseline_input_v1.json"
R3_BENCHMARK_REL = "research/autonomous_w2/g2/r3_baseline_benchmark_v1.json"
R3_PROFILE_REL = "research/autonomous_w2/g2/r3_baseline_profile_v1.json"

SOURCE_PATHS = [
    "AGENTS.md",
    "docs/DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2.md",
    "docs/CODEX_TO_LUNA_G2_AUTONOMOUS_COMPLETION_W2.md",
    "docs/reviews/CODEX_DDWMR_SCOPE_PROGRESS_VERIFICATION_2026_10_07.md",
    "research_context/MASTER_RESEARCH_CONTEXT_v2.md",
    "research_context/DECISION_LOG.md",
    "research_context/LITERATURE_MATRIX.md",
    "research_context/REVIEW_GATE.md",
    "research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md",
    "docs/reviews/GPT_TO_CODEX_G2_VALIDATION_R3_SCIENTIFIC_REVIEW_FULL_HANDOFF.md",
    "research/benchmarks/G2_DECISION_RELEVANT_STUDY_PROTOCOL_CANDIDATE_v1.md",
    "research/autonomous_w2/g2/HYPOTHESIS_AND_TASK_PREIMPLEMENTATION_v1.md",
    "research/autonomous_w2/g2/ANALYTIC_FEASIBILITY_SCREEN_v1.md",
    "research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v2.md",
    "research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v1.md",
    "docs/reviews/autonomous_w2/g2/W2_V1_DEVELOPMENT_FAILURE_POSTMORTEM.md",
    "research/autonomous_w2/g2/development_plan_v1.json",
    "research/autonomous_w2/g2/bindings_v1/attempt_01.json",
    "research/autonomous_w2/g2/bindings_v1/attempt_02.json",
    "research/autonomous_w2/g2/bindings_v1/attempt_03.json",
    "research/autonomous_w2/g2/bindings_v1/attempt_04.json",
    "research/autonomous_w2/g2/bindings_v1/attempt_05.json",
    "research/autonomous_w2/g2/bindings_v1/attempt_06.json",
    "coordination/autonomous_w2/g2/releases/RELEASE_v1.json",
    "coordination/autonomous_w2/g2/releases/RELEASE_v1.json.sha256",
    "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_02.json",
    "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_03.json",
    "results/validation/autonomous_w2/g2/development_v1/freeze_receipt_v1.json",
    "results/validation/autonomous_w2/g2/development_v1/stage_receipt.json",
    "validation/autonomous_w2/g2/prepare_r3_baseline_v1.py",
    R3_INPUT_REL,
    R3_BENCHMARK_REL,
    R3_PROFILE_REL,
    PROTOCOL_REL,
    PROFILE_REL,
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
    PROFILE_REL,
    "validation/autonomous_w2/g2/__init__.py",
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
for _attempt, _action in enumerate([
    "W2_G2_DEV_001_ZERO",
    "W2_G2_DEV_001_NOMINAL",
    "W2_G2_DEV_001_ALTERNATIVE",
    "W2_G2_DEV_001_ZERO",
    "W2_G2_DEV_001_NOMINAL",
    "W2_G2_DEV_001_ALTERNATIVE",
], start=1):
    _folder = f"results/validation/autonomous_w2/g2/development_v1/attempt_{_attempt:02d}_{_action}"
    SOURCE_PATHS.extend([
        f"{_folder}/attempt_receipt.json",
        f"{_folder}/row.json",
        f"{_folder}/worker.job.json",
        f"{_folder}/worker.stdout.bin",
        f"{_folder}/worker.stderr.bin",
    ])
    if _attempt >= 4:
        SOURCE_PATHS.extend([
            f"{_folder}/replay.json",
            f"{_folder}/checker.job.json",
            f"{_folder}/checker.stdout.bin",
            f"{_folder}/checker.stderr.bin",
        ])
ACTION_IDS = [
    "W2_G2_DEV_001_ZERO",
    "W2_G2_DEV_001_NOMINAL",
    "W2_G2_DEV_001_ALTERNATIVE",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True).encode("utf-8") + b"\n"
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()


def freeze() -> dict[str, Any]:
    plan_path = ROOT / PLAN_REL
    binding_dir = ROOT / BINDING_DIR_REL
    receipt_path = ROOT / FREEZE_RECEIPT_REL
    if plan_path.exists() or binding_dir.exists() or receipt_path.exists():
        raise FileExistsError("FROZEN_PLAN_OR_BINDINGS_ALREADY_EXIST")
    source_files = {rel: sha(ROOT / rel) for rel in SOURCE_PATHS}
    protocol_sha = sha(ROOT / PROTOCOL_REL)
    profile_sha = sha(ROOT / PROFILE_REL)
    runner_sha = source_files[RUNNER_REL]
    freeze_sha = source_files["validation/autonomous_w2/g2/freeze_development_v2.py"]
    attempts = []
    planned = [("signed_vof_candidate", action_id) for action_id in ACTION_IDS]
    planned.extend(("legacy_r3", action_id) for action_id in ACTION_IDS)
    for index, (method, action_id) in enumerate(planned, start=1):
        binding_rel = f"{BINDING_DIR_REL}/attempt_{index:02d}.json"
        prior_index = index if index <= 3 else index
        prior_path = f"results/validation/autonomous_w2/g2/development_v1/attempt_{prior_index:02d}_{action_id}"
        attempts.append({
            "attempt": index,
            "native_attempt_ordinal": 6 + index,
            "method": method,
            "action_id": action_id,
            "binding_path": binding_rel,
            "prior_v1_attempt_path": prior_path,
        })
    action_map = {row["id"]: row for row in json.loads((ROOT / PROTOCOL_REL).read_text(encoding="utf-8"))["actions"]}
    r3_input = json.loads((ROOT / R3_INPUT_REL).read_text(encoding="utf-8"))
    r3_action_map = {row["action"]["id"]: row["action"] for row in r3_input["query_actions"]}
    r3_input_sha = sha(ROOT / R3_INPUT_REL)
    r3_benchmark_sha = sha(ROOT / R3_BENCHMARK_REL)
    r3_profile_sha = sha(ROOT / R3_PROFILE_REL)
    repository_branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    repository_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    if r3_input.get("source_commit") != repository_head:
        raise ValueError("R3_SOURCE_COMMIT_DIFFERS_FROM_CURRENT_HEAD")
    for item in attempts:
        action = action_map[item["action_id"]] if item["method"] == "signed_vof_candidate" else r3_action_map[item["action_id"]]
        binding = {
            "schema": "G2_W2_ROW_BINDING_v2",
            "session": "DDWMR | LUNA-G2-SCOPE",
            "attempt": item["attempt"],
            "method": item["method"],
            "action_id": item["action_id"],
            "action": action,
            "plan_id": "G2_W2_DEV_PLAN_V2",
            "protocol_path": PROTOCOL_REL,
            "protocol_sha256": protocol_sha,
            "profile_path": PROFILE_REL,
            "profile_sha256": profile_sha,
            "plan_path": PLAN_REL,
            "binding_path": item["binding_path"],
            "runner_path": RUNNER_REL,
            "runner_sha256": runner_sha,
            "freeze_script_sha256": freeze_sha,
            "source_files": source_files,
            "result_root": RESULT_ROOT_REL,
            "attempt_kind": "native development row; not held-out confirmation",
            "native_attempt_ordinal": item["native_attempt_ordinal"],
            "prior_native_attempts": 6,
            "prior_v1_attempt_path": item["prior_v1_attempt_path"],
            "versioned_repair_reason": "v1 candidate serialization digit guard; v1 R3 replay used raw benchmark file hash instead of semantic JSON hash",
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
        "schema": "G2_W2_DEVELOPMENT_PLAN_v2",
        "plan_id": "G2_W2_DEV_PLAN_V2",
        "plan_path": PLAN_REL,
        "session": "DDWMR | LUNA-G2-SCOPE",
        "repository_branch": repository_branch,
        "repository_head": repository_head,
        "protocol_id": "G2_W2_VOF_TASK_V1",
        "plan_state": "FROZEN_BEFORE_VERSIONED_REPAIR_ATTEMPTS",
        "attempt_limit": 24,
        "prior_native_attempts": 6,
        "cumulative_native_attempts_after_plan": 12,
        "planned_attempt_count": len(attempts),
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
        "freeze_script_path": "validation/autonomous_w2/g2/freeze_development_v2.py",
        "freeze_script_sha256": freeze_sha,
        "source_files": source_files,
        "result_root": RESULT_ROOT_REL,
        "compute_lock_path": "coordination/autonomous_w2/COMPUTE.lock",
        "ordered_attempts": attempts,
        "retry_policy": "one launch per frozen row; these six rows are versioned repair re-evaluations of the same development IDs after v1's six failed attempts; all six prior attempts remain in the cumulative 24-attempt count; not confirmation",
        "prior_release_path": "coordination/autonomous_w2/g2/releases/RELEASE_v1.json",
        "prior_stage_receipt_path": "results/validation/autonomous_w2/g2/development_v1/stage_receipt.json",
        "failure_postmortem_path": "docs/reviews/autonomous_w2/g2/W2_V1_DEVELOPMENT_FAILURE_POSTMORTEM.md",
        "held_out_or_confirmation_rows": 0,
        "legacy_800_row_study": "NOT_RUN",
    }
    dump(plan_path, plan)
    plan_sha = sha(plan_path)
    receipt = {
        "schema": "G2_W2_FREEZE_RECEIPT_v2",
        "plan_path": PLAN_REL,
        "plan_sha256": plan_sha,
        "source_count": len(source_files),
        "source_files": source_files,
        "binding_paths": [item["binding_path"] for item in attempts],
        "binding_sha256": {item["binding_path"]: sha(ROOT / item["binding_path"]) for item in attempts},
        "attempt_count_frozen": len(attempts),
        "native_attempts_at_freeze": 6,
        "cumulative_attempt_limit": 24,
    }
    dump(receipt_path, receipt)
    return receipt


if __name__ == "__main__":
    print(json.dumps(freeze(), sort_keys=True, indent=2))
