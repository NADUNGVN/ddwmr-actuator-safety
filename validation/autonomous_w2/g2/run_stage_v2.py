"""Run only the frozen, ordered G2 W2 development rows under Job Object limits."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .windows_job_supervisor import JobGuardError, result_to_json, run_bounded_process


ROOT = Path(__file__).resolve().parents[3]
RUNNER_REL = "validation/autonomous_w2/g2/run_stage_v2.py"
FREEZE_RECEIPT_REL = "results/validation/autonomous_w2/g2/development_v2/freeze_receipt_v2.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any, *, exclusive: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True).encode("utf-8") + b"\n"
    mode = "xb" if exclusive else "wb"
    with path.open(mode) as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def verify_freeze_receipt(plan_path: Path, plan: dict[str, Any]) -> dict[str, Any]:
    receipt_path = ROOT / FREEZE_RECEIPT_REL
    if not receipt_path.is_file():
        raise ValueError("FREEZE_RECEIPT_MISSING")
    receipt = read_json(receipt_path)
    expected_bindings = {item.get("binding_path"): item.get("binding_sha256") for item in plan.get("ordered_attempts", [])}
    if (
        receipt.get("schema") != "G2_W2_FREEZE_RECEIPT_v2"
        or receipt.get("plan_path") != plan.get("plan_path")
        or receipt.get("plan_sha256") != sha(plan_path)
        or receipt.get("native_attempts_at_freeze") != int(plan.get("prior_native_attempts", -1))
        or receipt.get("attempt_count_frozen") != len(plan.get("ordered_attempts", []))
        or receipt.get("binding_sha256") != expected_bindings
    ):
        raise ValueError("FREEZE_RECEIPT_PLAN_BINDING_MISMATCH")
    return receipt


def verify_binding(plan_path: Path, plan: dict[str, Any], item: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    binding_rel = item["binding_path"]
    binding_path = ROOT / binding_rel
    binding = read_json(binding_path)
    if binding.get("schema") != "G2_W2_ROW_BINDING_v2" or binding.get("action_id") != item["action_id"]:
        raise ValueError(f"BINDING_ACTION_OR_SCHEMA_MISMATCH:{binding_rel}")
    if binding.get("attempt") != item["attempt"] or binding.get("binding_path") != binding_rel:
        raise ValueError(f"BINDING_ATTEMPT_OR_PATH_MISMATCH:{binding_rel}")
    if binding.get("plan_id") != plan.get("plan_id") or binding.get("plan_path") != plan.get("plan_path"):
        raise ValueError(f"PLAN_ID_OR_PATH_MISMATCH:{binding_rel}")
    if (
        binding.get("native_attempt_ordinal") != int(plan.get("prior_native_attempts", 0)) + int(item["attempt"])
        or binding.get("native_attempt_ordinal") != item.get("native_attempt_ordinal")
        or binding.get("prior_v1_attempt_path") != item.get("prior_v1_attempt_path")
    ):
        raise ValueError(f"VERSIONED_REPAIR_BINDING_MISMATCH:{binding_rel}")
    if sha(binding_path) != item.get("binding_sha256"):
        raise ValueError(f"BINDING_HASH_MISMATCH:{binding_rel}")
    if binding.get("runner_path") != RUNNER_REL or binding.get("runner_sha256") != sha(ROOT / RUNNER_REL):
        raise ValueError("RUNNER_SOURCE_HASH_MISMATCH")
    if binding.get("protocol_sha256") != plan["protocol_sha256"] or binding.get("profile_sha256") != plan["profile_sha256"]:
        raise ValueError(f"INPUT_HASH_BINDING_MISMATCH:{binding_rel}")
    if binding.get("method") == "signed_vof_candidate":
        protocol = read_json(ROOT / binding["protocol_path"])
        action_matches = [action for action in protocol.get("actions", []) if action.get("id") == binding["action_id"]]
        if len(action_matches) != 1 or binding.get("action") != action_matches[0]:
            raise ValueError(f"ACTION_BINDING_MISMATCH:{binding_rel}")
    elif binding.get("method") == "legacy_r3":
        for hash_key in ("r3_input_sha256", "r3_benchmark_sha256", "r3_profile_sha256"):
            if binding.get(hash_key) != plan.get(hash_key):
                raise ValueError(f"R3_PLAN_BINDING_HASH_MISMATCH:{hash_key}")
        r3_input = read_json(ROOT / binding["r3_input_path"])
        r3_matches = [item["action"] for item in r3_input.get("query_actions", []) if item["action"].get("id") == binding["action_id"]]
        if len(r3_matches) != 1 or binding.get("action") != r3_matches[0]:
            raise ValueError(f"R3_ACTION_BINDING_MISMATCH:{binding_rel}")
        for path_key, hash_key in (("r3_input_path", "r3_input_sha256"), ("r3_benchmark_path", "r3_benchmark_sha256"), ("r3_profile_path", "r3_profile_sha256")):
            if sha(ROOT / binding[path_key]) != binding[hash_key]:
                raise ValueError(f"R3_INPUT_HASH_MISMATCH:{path_key}")
    else:
        raise ValueError(f"UNSUPPORTED_METHOD_BINDING:{binding_rel}")
    if binding.get("source_files") != plan.get("source_files"):
        raise ValueError(f"SOURCE_CLOSURE_BINDING_MISMATCH:{binding_rel}")
    for rel, expected in binding["source_files"].items():
        if sha(ROOT / rel) != expected:
            raise ValueError(f"SOURCE_HASH_MISMATCH:{rel}")
    if sha(ROOT / binding["protocol_path"]) != binding["protocol_sha256"]:
        raise ValueError("PROTOCOL_HASH_MISMATCH")
    if sha(ROOT / binding["profile_path"]) != binding["profile_sha256"]:
        raise ValueError("PROFILE_HASH_MISMATCH")
    return binding_path, binding


def bounded(command: list[str], profile: dict[str, Any]) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONUTF8"] = "1"
    try:
        result = run_bounded_process(
            command,
            cwd=ROOT,
            wall_seconds=float(profile["worker_wall_cap_seconds"]),
            cpu_seconds=float(profile["worker_wall_cap_seconds"]),
            memory_bytes=int(profile["worker_memory_cap_bytes"]),
            max_processes=int(profile["worker_process_cap"]),
            stdout_limit_bytes=int(profile["stdout_cap_bytes"]),
            stderr_limit_bytes=int(profile["stderr_cap_bytes"]),
            environment=env,
        )
        return {"launch_error": None, "job": result_to_json(result)}
    except BaseException as exc:
        return {"launch_error": f"{type(exc).__name__}:{exc}", "job": None}


def save_process(folder: Path, name: str, evidence: dict[str, Any]) -> bytes:
    write_json(folder / f"{name}.job.json", evidence)
    job = evidence.get("job") or {}
    stdout = job.get("stdout") or {}
    stderr = job.get("stderr") or {}
    out_bytes = base64.b64decode(stdout.get("prefix_base64", ""))
    err_bytes = base64.b64decode(stderr.get("prefix_base64", ""))
    (folder / f"{name}.stdout.bin").write_bytes(out_bytes)
    (folder / f"{name}.stderr.bin").write_bytes(err_bytes)
    return out_bytes


def classify_worker(record: Any) -> str:
    if not isinstance(record, dict):
        return "WORKER_OUTPUT_INVALID"
    if record.get("schema") == "G2_W2_VOF_ROW_v2":
        return "PROOF_ROW"
    if record.get("schema") == "G2_W2_R3_BASELINE_ROW_v2":
        return "PROOF_ROW"
    if record.get("schema") != "G2_W2_WORKER_FAILURE_v1":
        return "WORKER_OUTPUT_INVALID"
    return str(record.get("status", "WORKER_FAILURE_UNKNOWN"))


def run_one(plan_path: Path, plan: dict[str, Any], item: dict[str, Any], profile: dict[str, Any], stage_deadline: float) -> dict[str, Any]:
    binding_path, binding = verify_binding(plan_path, plan, item)
    relative_binding = binding_path.relative_to(ROOT).as_posix()
    out_dir = ROOT / plan["result_root"] / f"attempt_{int(item['attempt']):02d}_{item['action_id']}"
    out_dir.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    result: dict[str, Any] = {
        "attempt": item["attempt"],
        "native_attempt_ordinal": item.get("native_attempt_ordinal"),
        "method": item["method"],
        "action_id": item["action_id"],
        "prior_v1_attempt_path": item.get("prior_v1_attempt_path"),
        "binding_path": item["binding_path"],
        "binding_sha256": sha(binding_path),
        "status": "STARTED",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "worker": None,
        "checker": None,
    }
    if time.monotonic() >= stage_deadline:
        result["status"] = "PHASE_WALL_LIMIT_BEFORE_WORKER"
        write_json(out_dir / "attempt_receipt.json", result, exclusive=True)
        return result

    worker_module = "validation.autonomous_w2.g2.worker_v2" if item["method"] == "signed_vof_candidate" else "validation.autonomous_w2.g2.r3_baseline_worker_v2"
    command = [sys.executable, "-m", worker_module, "--binding", relative_binding, "--action-id", item["action_id"]]
    worker_evidence = bounded(command, profile)
    worker_stdout = save_process(out_dir, "worker", worker_evidence)
    worker_record = None
    try:
        worker_record = json.loads(worker_stdout.decode("utf-8").strip())
        write_json(out_dir / "row.json", worker_record, exclusive=True)
    except BaseException as exc:
        result["worker_parse_error"] = f"{type(exc).__name__}:{exc}"
    worker_job = worker_evidence.get("job") or {}
    worker_status = (worker_job.get("status") if worker_job else None) or (
        "LAUNCH_OR_SUPERVISOR_FAILURE" if worker_evidence.get("launch_error") else "NO_JOB_RESULT"
    )
    worker_class = classify_worker(worker_record)
    result["worker"] = {
        "job_status": worker_status,
        "launch_error": worker_evidence.get("launch_error"),
        "returncode": worker_job.get("returncode") if worker_job else None,
        "stdout_sha256": hashlib.sha256(worker_stdout).hexdigest(),
        "stdout_bytes": len(worker_stdout),
        "classification": worker_class,
        "reason_code": worker_record.get("reason_code") if isinstance(worker_record, dict) else None,
    }
    if worker_job.get("stdout", {}).get("overflow") if worker_job else False:
        worker_class = "OUTPUT_LIMIT_UNKNOWN"
    if worker_status != "COMPLETED" or worker_class != "PROOF_ROW":
        result["status"] = worker_class if worker_class != "PROOF_ROW" else worker_status
        result["ended_utc"] = datetime.now(timezone.utc).isoformat()
        result["elapsed_seconds_display_only"] = round(time.monotonic() - started, 6)
        write_json(out_dir / "attempt_receipt.json", result, exclusive=True)
        return result

    if time.monotonic() >= stage_deadline:
        result["status"] = "PHASE_WALL_LIMIT_BEFORE_REPLAY"
        result["ended_utc"] = datetime.now(timezone.utc).isoformat()
        result["elapsed_seconds_display_only"] = round(time.monotonic() - started, 6)
        write_json(out_dir / "attempt_receipt.json", result, exclusive=True)
        return result

    checker_module = "validation.autonomous_w2.g2.checker_v2" if item["method"] == "signed_vof_candidate" else "validation.autonomous_w2.g2.r3_baseline_checker_v2"
    replay_command = [sys.executable, "-m", checker_module, "--binding", relative_binding, "--record", str((out_dir / "row.json").relative_to(ROOT).as_posix())]
    checker_evidence = bounded(replay_command, profile)
    checker_stdout = save_process(out_dir, "checker", checker_evidence)
    checker_record = None
    try:
        checker_record = json.loads(checker_stdout.decode("utf-8").strip())
        write_json(out_dir / "replay.json", checker_record, exclusive=True)
    except BaseException as exc:
        result["checker_parse_error"] = f"{type(exc).__name__}:{exc}"
    checker_job = checker_evidence.get("job") or {}
    result["checker"] = {
        "job_status": (checker_job.get("status") if checker_job else None) or (
            "LAUNCH_OR_SUPERVISOR_FAILURE" if checker_evidence.get("launch_error") else "NO_JOB_RESULT"
        ),
        "launch_error": checker_evidence.get("launch_error"),
        "returncode": checker_job.get("returncode") if checker_job else None,
        "stdout_sha256": hashlib.sha256(checker_stdout).hexdigest(),
        "stdout_bytes": len(checker_stdout),
        "replayed": checker_record.get("replayed") if isinstance(checker_record, dict) else None,
        "audit_valid": checker_record.get("audit_valid") if isinstance(checker_record, dict) else None,
        "rejection": checker_record.get("rejection") if isinstance(checker_record, dict) else None,
    }
    replay_pass = checker_record.get("replayed") is True if isinstance(checker_record, dict) else False
    r3_audit_valid = checker_record.get("audit_valid") is True if isinstance(checker_record, dict) and item["method"] == "legacy_r3" else False
    if checker_job.get("status") == "COMPLETED" and (replay_pass or r3_audit_valid):
        if item["method"] == "legacy_r3":
            safety = worker_record.get("safety_record", {})
            progress = worker_record.get("progress_record", {})
            proof = safety.get("proof", {}) if isinstance(safety, dict) else {}
            collisions = proof.get("collision", []) if isinstance(proof, dict) else []
            result["status"] = "REPLAYED" if replay_pass else "RESOURCE_UNKNOWN_RECORD_AUDITED"
            result["safety_status"] = checker_record.get("safety_status")
            result["task_eligible"] = checker_record.get("task_eligible", False)
            result["reason_codes"] = safety.get("reason_codes", []) if isinstance(safety, dict) else []
            result["progress_enclosure_m"] = checker_record.get("progress_lower_m")
            result["collision_margin_lower_min_m"] = [item.get("margin_lower") for item in collisions]
            result["contact_margin_lower_min_N"] = proof.get("contact_margin_lower") if isinstance(proof, dict) else None
            result["progress_status"] = checker_record.get("progress_status", progress.get("status"))
            result["resource_limited"] = checker_record.get("resource_limited", False)
            result["r3_audit_valid"] = checker_record.get("audit_valid")
        else:
            result["status"] = "REPLAYED"
            result["safety_status"] = worker_record.get("safety_status")
            result["task_eligible"] = worker_record.get("task_eligible")
            result["reason_codes"] = worker_record.get("reason_codes")
            result["progress_enclosure_m"] = worker_record.get("progress_enclosure_m")
            result["collision_margin_lower_min_m"] = worker_record.get("collision_margin_lower_min_m")
            result["contact_margin_lower_min_N"] = worker_record.get("contact_margin_lower_min_N")
    else:
        result["status"] = "AUDIT_FAILURE_OR_RESOURCE_UNKNOWN"
    result["ended_utc"] = datetime.now(timezone.utc).isoformat()
    result["elapsed_seconds_display_only"] = round(time.monotonic() - started, 6)
    write_json(out_dir / "attempt_receipt.json", result, exclusive=True)
    return result


def run_stage(plan_path: Path) -> dict[str, Any]:
    plan_path = plan_path.resolve()
    plan_rel = plan_path.relative_to(ROOT).as_posix()
    plan = read_json(plan_path)
    if plan.get("schema") != "G2_W2_DEVELOPMENT_PLAN_v2" or plan.get("plan_state") != "FROZEN_BEFORE_VERSIONED_REPAIR_ATTEMPTS":
        raise ValueError("PLAN_SCHEMA_OR_STATE")
    if plan.get("plan_path") != plan_rel:
        raise ValueError("PLAN_PATH_MISMATCH")
    freeze_receipt = verify_freeze_receipt(plan_path, plan)
    current_branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    current_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    if current_branch != plan.get("repository_branch") or current_head != plan.get("repository_head"):
        raise ValueError("REPOSITORY_BRANCH_OR_HEAD_CHANGED_AFTER_FREEZE")
    if sha(ROOT / plan["protocol_path"]) != plan["protocol_sha256"] or sha(ROOT / plan["profile_path"]) != plan["profile_sha256"]:
        raise ValueError("FROZEN_PROTOCOL_OR_PROFILE_HASH_MISMATCH")
    for path_key, hash_key in (("r3_input_path", "r3_input_sha256"), ("r3_benchmark_path", "r3_benchmark_sha256"), ("r3_profile_path", "r3_profile_sha256")):
        if sha(ROOT / plan[path_key]) != plan[hash_key]:
            raise ValueError(f"FROZEN_R3_INPUT_HASH_MISMATCH:{path_key}")
    if sha(ROOT / RUNNER_REL) != plan["runner_sha256"]:
        raise ValueError("RUNNER_HASH_MISMATCH")
    for rel, expected in plan["source_files"].items():
        if sha(ROOT / rel) != expected:
            raise ValueError(f"SOURCE_HASH_MISMATCH:{rel}")
    profile = read_json(ROOT / plan["profile_path"])
    lock_path = ROOT / plan["compute_lock_path"]
    lock_token = uuid.uuid4().hex
    lock = {
        "session": "DDWMR | LUNA-G2-SCOPE",
        "pid": os.getpid(),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "plan_path": plan_rel,
        "plan_sha256": sha(plan_path),
        "freeze_receipt_sha256": sha(ROOT / FREEZE_RECEIPT_REL),
        "token": lock_token,
    }
    write_json(lock_path, lock, exclusive=True)
    phase_started = time.monotonic()
    stage_deadline = phase_started + int(profile["phase_wall_cap_seconds"])
    run_results = []
    try:
        attempts = plan.get("ordered_attempts", [])
        prior_attempts = int(plan.get("prior_native_attempts", 0))
        if len(attempts) != int(plan.get("planned_attempt_count", -1)) or prior_attempts + len(attempts) > int(plan.get("attempt_limit", 0)):
            raise ValueError("PLAN_ATTEMPT_COUNT_OR_CAP")
        for item in attempts:
            # Each configuration is counted once the runner attempts its single worker launch; no retry path exists.
            try:
                run_results.append(run_one(plan_path, plan, item, profile, stage_deadline))
            except BaseException as exc:
                run_results.append({
                    "attempt": item.get("attempt"),
                    "native_attempt_ordinal": item.get("native_attempt_ordinal"),
                    "action_id": item.get("action_id"),
                    "prior_v1_attempt_path": item.get("prior_v1_attempt_path"),
                    "binding_path": item.get("binding_path"),
                    "status": "PRELAUNCH_OR_STAGE_FAILURE",
                    "error": f"{type(exc).__name__}:{exc}",
                    "counted_as_configuration_attempt": True,
                    "started_utc": datetime.now(timezone.utc).isoformat(),
                })
                # Do not launch later rows after an integrity/source failure.
                if "HASH_MISMATCH" in str(exc) or "SOURCE_" in str(exc) or "BINDING_" in str(exc):
                    break
        counts: dict[str, int] = {}
        for row in run_results:
            counts[row["status"]] = counts.get(row["status"], 0) + 1
        summary = {
            "schema": "G2_W2_DEVELOPMENT_STAGE_RECEIPT_v2",
            "session": "DDWMR | LUNA-G2-SCOPE",
            "plan_path": plan_rel,
            "plan_sha256": sha(plan_path),
            "protocol_sha256": plan["protocol_sha256"],
            "profile_sha256": plan["profile_sha256"],
            "r3_input_sha256": plan["r3_input_sha256"],
            "r3_benchmark_sha256": plan["r3_benchmark_sha256"],
            "r3_profile_sha256": plan["r3_profile_sha256"],
            "stage_started_utc": lock["started_utc"],
            "stage_ended_utc": datetime.now(timezone.utc).isoformat(),
            "attempts_counted": len(run_results),
            "prior_native_attempts": int(plan.get("prior_native_attempts", 0)),
            "cumulative_native_attempts": int(plan.get("prior_native_attempts", 0)) + len(run_results),
            "planned_attempts": len(plan["ordered_attempts"]),
            "status_counts": counts,
            "attempts": run_results,
            "phase_cap_seconds": int(profile["phase_wall_cap_seconds"]),
            "phase_elapsed_seconds_display_only": round(time.monotonic() - phase_started, 6),
            "no_retries": True,
            "held_out_rows": 0,
            "legacy_800_row_study": "NOT_RUN",
        }
        write_json(ROOT / plan["result_root"] / "stage_receipt.json", summary, exclusive=True)
        return summary
    finally:
        try:
            if read_json(lock_path).get("token") == lock_token:
                lock_path.unlink()
        except FileNotFoundError:
            pass


def run_mutation_audit(binding_path: Path, record_path: Path, report_path: Path) -> dict[str, Any]:
    binding_path = binding_path.resolve()
    record_path = record_path.resolve()
    report_path = report_path.resolve()
    binding_rel = binding_path.relative_to(ROOT).as_posix()
    record_rel = record_path.relative_to(ROOT).as_posix()
    report_rel = report_path.relative_to(ROOT).as_posix()
    binding = read_json(binding_path)
    plan_path = ROOT / binding["plan_path"]
    plan = read_json(plan_path)
    freeze_receipt = verify_freeze_receipt(plan_path, plan)
    if freeze_receipt.get("binding_sha256", {}).get(binding_rel) != sha(binding_path):
        raise ValueError("FREEZE_RECEIPT_BINDING_HASH_MISMATCH")
    profile = read_json(ROOT / binding["profile_path"])
    if binding.get("runner_path") != RUNNER_REL or binding.get("runner_sha256") != sha(ROOT / RUNNER_REL):
        raise ValueError("RUNNER_SOURCE_HASH_MISMATCH")
    for rel, expected in binding["source_files"].items():
        if sha(ROOT / rel) != expected:
            raise ValueError(f"SOURCE_HASH_MISMATCH:{rel}")
    if sha(ROOT / binding["protocol_path"]) != binding["protocol_sha256"] or sha(ROOT / binding["profile_path"]) != binding["profile_sha256"]:
        raise ValueError("FROZEN_INPUT_HASH_MISMATCH")
    if not record_path.is_file() or report_path.exists():
        raise ValueError("MUTATION_RECORD_MISSING_OR_REPORT_ALREADY_EXISTS")
    lock_path = ROOT / "coordination/autonomous_w2/COMPUTE.lock"
    lock_token = uuid.uuid4().hex
    lock = {
        "session": "DDWMR | LUNA-G2-SCOPE",
        "pid": os.getpid(),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "task": "saved-record replay mutation audit; no native query",
        "binding_path": binding_rel,
        "binding_sha256": sha(binding_path),
        "plan_path": binding.get("plan_path"),
        "plan_sha256": sha(plan_path),
        "freeze_receipt_sha256": sha(ROOT / FREEZE_RECEIPT_REL),
        "token": lock_token,
    }
    write_json(lock_path, lock, exclusive=True)
    evidence_dir = report_path.parent / "mutation_audit_process"
    evidence_dir.mkdir(parents=True, exist_ok=False)
    try:
        command = [
            sys.executable,
            "-m",
            "validation.autonomous_w2.g2.audit_mutations_v2",
            "--binding",
            binding_rel,
            "--record",
            record_rel,
            "--report",
            report_rel,
        ]
        process_evidence = bounded(command, profile)
        stdout = save_process(evidence_dir, "mutation_audit", process_evidence)
        process_job = process_evidence.get("job") or {}
        parsed = None
        try:
            parsed = json.loads(stdout.decode("utf-8").strip())
        except BaseException:
            parsed = None
        ok = (
            process_job.get("status") == "COMPLETED"
            and isinstance(parsed, dict)
            and parsed.get("all_required_mutations_rejected") is True
        )
        summary = {
            "schema": "G2_W2_MUTATION_AUDIT_SUPERVISOR_RECEIPT_v1",
            "session": "DDWMR | LUNA-G2-SCOPE",
            "binding_path": binding_rel,
            "binding_sha256": sha(binding_path),
            "record_path": record_rel,
            "record_sha256": sha(record_path),
            "report_path": report_rel,
            "runner_sha256": sha(ROOT / RUNNER_REL),
            "job_status": process_job.get("status"),
            "launch_error": process_evidence.get("launch_error"),
            "returncode": process_job.get("returncode"),
            "mutation_report": parsed,
            "all_required_mutations_rejected": ok,
            "native_attempts_added": 0,
        }
        write_json(evidence_dir / "mutation_audit_receipt.json", summary, exclusive=True)
        return summary
    finally:
        try:
            if read_json(lock_path).get("token") == lock_token:
                lock_path.unlink()
        except FileNotFoundError:
            pass
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan")
    parser.add_argument("--audit-binding")
    parser.add_argument("--audit-record")
    parser.add_argument("--audit-report")
    args = parser.parse_args()
    try:
        if args.plan and not (args.audit_binding or args.audit_record or args.audit_report):
            plan_path = Path(args.plan)
            if not plan_path.is_absolute():
                plan_path = ROOT / plan_path
            summary = run_stage(plan_path)
        elif args.audit_binding and args.audit_record and args.audit_report and not args.plan:
            def rooted(value: str) -> Path:
                path = Path(value)
                return path if path.is_absolute() else ROOT / path
            summary = run_mutation_audit(rooted(args.audit_binding), rooted(args.audit_record), rooted(args.audit_report))
        else:
            raise ValueError("SELECT_ONE_STAGE_OR_MUTATION_AUDIT_MODE")
        print(json.dumps(summary, sort_keys=True, indent=2))
        if summary.get("schema") == "G2_W2_MUTATION_AUDIT_SUPERVISOR_RECEIPT_v1":
            return 0 if summary.get("all_required_mutations_rejected") else 3
        return 0
    except BaseException as exc:
        print(json.dumps({"schema": "G2_W2_STAGE_LAUNCH_FAILURE_v1", "reason": f"{type(exc).__name__}:{exc}"}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
