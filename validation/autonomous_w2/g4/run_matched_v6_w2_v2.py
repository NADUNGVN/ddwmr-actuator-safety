"""Execute the frozen three-action v6/Auer development comparison once."""
from __future__ import annotations

import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validation.autonomous_w2.g4.matched_v6_common_v2 import (
    PROJECT, PLAN_REL, RESULT_REL, sha256_file, strict_json, verify_source_closure, write_json,
)
from validation.autonomous_w2.g4.windows_job_supervisor_v2 import result_to_json, run_bounded_process

LOCK_REL = Path("coordination/autonomous_w2/COMPUTE.lock")
PHASE_WALL = 7200
CAPS = {
    "wall_seconds": 60, "cpu_seconds": 60, "memory_bytes": 1_073_741_824,
    "max_processes": 1, "stdout_bytes": 8_388_608, "stderr_bytes": 1_048_576,
}


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _lock(path: Path, plan_sha: str) -> dict[str, Any]:
    token = uuid.uuid4().hex
    doc = {
        "schema": "ddwmr-g4-w2-compute-lock-v2",
        "session": "DDWMR | LUNA-G4-AUER",
        "pid": os.getpid(),
        "started_utc": _utc(),
        "purpose": "sequential three-action v6 then local-Auer development comparison",
        "plan_sha256": plan_sha,
        "token": token,
    }
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(doc, stream, sort_keys=True, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    return doc


def _run_one(method: str, ordinal: int, action: dict[str, Any], freeze: dict[str, Any], phase_deadline: float) -> dict[str, Any]:
    comparison_id = action["comparison_id"] if method == "v6" else action["auer_id"]
    output_dir = PROJECT / RESULT_REL / method / f"{ordinal:02d}_{comparison_id}"
    if output_dir.exists():
        raise FileExistsError(f"MATCHED_OUTPUT_ALREADY_EXISTS:{output_dir}")
    output_dir.mkdir(parents=True, exist_ok=False)
    if time.monotonic() >= phase_deadline:
        raise TimeoutError("PHASE_WALL_LIMIT_BEFORE_LAUNCH")
    if method == "v6":
        binding = PROJECT / freeze["v6_binding_paths"][comparison_id]
        command = [sys.executable, "-B", "-m", "validation.autonomous_w2.g4.v6_w2_worker_v2",
                   "--binding", str(binding), "--output-dir", str(output_dir)]
    else:
        command = [sys.executable, "-B", "-m", "validation.autonomous_w2.g4.auer_w2_worker_v2",
                   "--comparison-id", comparison_id, "--output-dir", str(output_dir)]
    env = {**os.environ, "PYTHONHASHSEED": "0", "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    write_json(output_dir / "launch_intent.json", {
        "schema": "ddwmr-g4-w2-matched-launch-intent-v2",
        "method": method,
        "ordinal": ordinal,
        "comparison_id": comparison_id,
        "peer_action_id": action["peer_action_id"],
        "command": command,
        "caps": CAPS,
        "prepared_utc": _utc(),
        "single_invocation": True,
        "retry_allowed": False,
    }, max_bytes=16_384, exclusive=True)
    result = run_bounded_process(
        command, cwd=PROJECT, wall_seconds=CAPS["wall_seconds"], cpu_seconds=CAPS["cpu_seconds"],
        memory_bytes=CAPS["memory_bytes"], max_processes=CAPS["max_processes"],
        stdout_limit_bytes=CAPS["stdout_bytes"], stderr_limit_bytes=CAPS["stderr_bytes"],
        environment=env,
    )
    stdout_path, stderr_path = output_dir / "worker.stdout.bin", output_dir / "worker.stderr.bin"
    stdout_path.write_bytes(result.stdout.prefix)
    stderr_path.write_bytes(result.stderr.prefix)
    job_path = output_dir / "worker.job.json"
    write_json(job_path, result_to_json(result), max_bytes=1_048_576, exclusive=True)
    worker_result_path = output_dir / "worker_result.json"
    worker_result = strict_json(worker_result_path) if worker_result_path.is_file() else None
    summary_keys = (
        "native_status", "final_status", "task_eligible", "progress_lower_meets_threshold",
        "native_row_bytes", "native_proof_bytes", "native_replay_status", "common_replay_status",
        "native_replay_wall_seconds", "common_replay_wall_seconds", "producer_wall_seconds",
        "stage_seconds", "common_summary", "resource_work",
    )
    receipt = {
        "schema": "ddwmr-g4-w2-matched-action-launch-receipt-v2",
        "session": "DDWMR | LUNA-G4-AUER",
        "method": method,
        "ordinal": ordinal,
        "comparison_id": comparison_id,
        "peer_action_id": action["peer_action_id"],
        "voltage": action["voltage"],
        "command": command,
        "environment_allowlist": {key: env[key] for key in ("PYTHONHASHSEED", "PYTHONUTF8", "PYTHONDONTWRITEBYTECODE")},
        "caps": CAPS,
        "job_receipt_path": job_path.relative_to(PROJECT).as_posix(),
        "job_receipt_sha256": sha256_file(job_path),
        "stdout_path": stdout_path.relative_to(PROJECT).as_posix(),
        "stdout_sha256": sha256_file(stdout_path),
        "stdout_bytes_retained": len(result.stdout.prefix),
        "stderr_path": stderr_path.relative_to(PROJECT).as_posix(),
        "stderr_sha256": sha256_file(stderr_path),
        "stderr_bytes_retained": len(result.stderr.prefix),
        "worker_result_path": worker_result_path.relative_to(PROJECT).as_posix() if worker_result_path.is_file() else None,
        "worker_result_sha256": sha256_file(worker_result_path) if worker_result_path.is_file() else None,
        "worker_result_summary": {key: worker_result[key] for key in summary_keys if key in worker_result} if worker_result else None,
        "producer_start_marker_path": (output_dir / "producer_start.json").relative_to(PROJECT).as_posix()
        if (output_dir / "producer_start.json").is_file() else None,
        "producer_start_marker_sha256": sha256_file(output_dir / "producer_start.json")
        if (output_dir / "producer_start.json").is_file() else None,
        "native_calls_counted": int((output_dir / "producer_start.json").is_file()),
        "job_status": result.status,
        "job_returncode": result.returncode,
        "no_retry": True,
        "completed_utc": _utc(),
    }
    write_json(output_dir / "launch_receipt.json", receipt, max_bytes=1_048_576, exclusive=True)
    return receipt


def main() -> int:
    started = time.monotonic()
    plan_path = PROJECT / PLAN_REL / "protocol_v2.json"
    freeze_path = PROJECT / PLAN_REL / "freeze_manifest_v3.json"
    receipt_path = PROJECT / RESULT_REL / "freeze_receipt_v3.json"
    freeze = strict_json(freeze_path)
    freeze_receipt = strict_json(receipt_path)
    if freeze_receipt.get("freeze_manifest_sha256") != sha256_file(freeze_path):
        raise RuntimeError("FREEZE_RECEIPT_MANIFEST_HASH_MISMATCH")
    if freeze_receipt.get("protocol_sha256") != sha256_file(plan_path):
        raise RuntimeError("FREEZE_RECEIPT_PROTOCOL_HASH_MISMATCH")
    verify_source_closure(freeze)
    protocol = strict_json(plan_path)
    actions = protocol["actions"]
    if len(actions) != 3 or len(freeze.get("actions", [])) != 3:
        raise RuntimeError("FROZEN_THREE_ACTION_COUNT_REQUIRED")
    result_root = PROJECT / RESULT_REL
    result_root.mkdir(parents=True, exist_ok=True)
    lock_path = PROJECT / LOCK_REL
    lock_doc = _lock(lock_path, sha256_file(freeze_path))
    results: list[dict[str, Any]] = []
    errors: list[str] = []
    stop_on_defect = False
    phase_deadline = time.monotonic() + PHASE_WALL
    try:
        # The frozen order is v6 zero, nominal, alternative, then Auer in the
        # same order.  No action is retried and no batch enumerator exists.
        for method in ("v6", "auer"):
            for ordinal, action in enumerate(actions, 1):
                try:
                    receipt = _run_one(method, ordinal, action, freeze, phase_deadline)
                except BaseException as exc:
                    errors.append(f"{method}:{ordinal}:{type(exc).__name__}:{exc}")
                    # A launch/binding defect invalidates this comparison arm;
                    # preserve the failure and stop rather than masking it.
                    stop_on_defect = True
                    break
                results.append(receipt)
                worker_result = receipt.get("worker_result_summary") or {}
                invalid = (
                    worker_result.get("native_status") == "IMPLEMENTATION_FAILURE"
                    or receipt.get("job_status") == "NONZERO_EXIT"
                    or receipt.get("job_status") == "JOB_LIMIT_OR_CHILD_FAILURE"
                )
                if invalid:
                    errors.append(f"{method}:{ordinal}:IMPLEMENTATION_OR_EXECUTION_FAILURE")
                    stop_on_defect = True
                    break
            if stop_on_defect:
                break
    finally:
        if lock_path.is_file():
            try:
                existing = strict_json(lock_path)
                if existing.get("token") == lock_doc["token"]:
                    lock_path.unlink()
            except Exception:
                pass
    phase = {
        "schema": "ddwmr-g4-w2-matched-v6-auer-development-phase-v2",
        "session": "DDWMR | LUNA-G4-AUER",
        "freeze_manifest_sha256": sha256_file(freeze_path),
        "freeze_receipt_sha256": sha256_file(receipt_path),
        "protocol_sha256": sha256_file(plan_path),
        "run_order": "v6 all three in frozen order, then Auer all three in frozen order",
        "native_call_limits": {"v6": 3, "auer": 3, "retries": 0},
        "phase_wall_cap_seconds": PHASE_WALL,
        "started_utc": lock_doc["started_utc"],
        "completed_utc": _utc(),
        "elapsed_seconds": time.monotonic() - started,
        "v6_native_calls_counted": sum(row["native_calls_counted"] for row in results if row["method"] == "v6"),
        "auer_native_calls_counted": sum(row["native_calls_counted"] for row in results if row["method"] == "auer"),
        "results": results,
        "errors": errors,
        "lock_released": not lock_path.exists(),
        "no_retry": True,
    }
    write_json(result_root / "matched_phase_receipt_v3.json", phase, max_bytes=8_388_608, exclusive=True)
    print(json.dumps({key: value for key, value in phase.items() if key not in {"results", "errors"}}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
