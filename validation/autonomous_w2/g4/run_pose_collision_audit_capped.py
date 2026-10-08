"""Run the independent G4 pose/collision audit under W2 resource limits."""
from __future__ import annotations

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from validation.autonomous_w2.g2.windows_job_supervisor import (  # noqa: E402
    result_to_json,
    run_bounded_process,
)

LOCK_REL = "coordination/autonomous_w2/COMPUTE.lock"
RESULT_REL = "results/validation/autonomous_w2/g4/pose_collision_audit_v1.json"
RECEIPT_REL = "results/validation/autonomous_w2/g4/pose_collision_audit_receipt_v1.json"
RELEASE_SHA256 = "789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55"


def contained(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError(f"PATH_ESCAPES_REPO:{relative}")
    return path


def main() -> int:
    result_path, receipt_path = contained(RESULT_REL), contained(RECEIPT_REL)
    lock_path = contained(LOCK_REL)
    if result_path.exists() or receipt_path.exists():
        raise FileExistsError("POSE_COLLISION_AUDIT_OUTPUT_ALREADY_EXISTS")
    token = uuid.uuid4().hex
    lock_doc = {
        "session": "DDWMR | LUNA-G4-AUER",
        "pid": os.getpid(),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "read-only independent Fraction audit of saved v6 pose/collision bounds",
        "release_sha256": RELEASE_SHA256,
        "token": token,
    }
    fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(lock_doc, stream, sort_keys=True, indent=2)
        stream.write("\n")

    auditor_rel = "validation/autonomous_w2/g4/audit_g2_v6_pose_collision.py"
    auditor_path = contained(auditor_rel)
    command = [sys.executable, "-B", str(auditor_path)]
    process_json: dict[str, Any] | None = None
    audit_result: dict[str, Any] | None = None
    error: str | None = None
    try:
        bounded = run_bounded_process(
            command,
            cwd=ROOT,
            wall_seconds=60,
            cpu_seconds=60,
            memory_bytes=1_073_741_824,
            max_processes=1,
            stdout_limit_bytes=8_388_608,
            stderr_limit_bytes=1_048_576,
        )
        process_json = result_to_json(bounded)
        try:
            audit_result = json.loads(bounded.stdout.prefix.decode("utf-8"))
        except Exception as exc:
            error = f"AUDIT_STDOUT_JSON_PARSE_ERROR:{type(exc).__name__}:{exc}"
        if bounded.status != "COMPLETED" or bounded.returncode != 0:
            error = error or f"AUDITOR_PROCESS_NOT_COMPLETED:{bounded.status}:{bounded.returncode}"
        if audit_result is not None:
            result_path.write_text(json.dumps(audit_result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    except BaseException as exc:
        error = f"SUPERVISOR_EXCEPTION:{type(exc).__name__}:{exc}"

    receipt = {
        "schema": "G4_W2_G2_V6_POSE_COLLISION_SUPERVISED_AUDIT_RECEIPT_v1",
        "session": "DDWMR | LUNA-G4-AUER",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "release_sha256": RELEASE_SHA256,
        "auditor_path": auditor_rel,
        "auditor_sha256": __import__("hashlib").sha256(auditor_path.read_bytes()).hexdigest(),
        "runner_path": "validation/autonomous_w2/g4/run_pose_collision_audit_capped.py",
        "runner_sha256": __import__("hashlib").sha256(Path(__file__).resolve().read_bytes()).hexdigest(),
        "command": command,
        "read_only_saved_row_audit": True,
        "producer_invocations": 0,
        "native_attempts_added": 0,
        "limits": {
            "wall_seconds": 60,
            "cpu_seconds": 60,
            "memory_bytes": 1_073_741_824,
            "processes": 1,
            "stdout_bytes": 8_388_608,
            "stderr_bytes": 1_048_576,
        },
        "process": process_json,
        "audit_result_path": RESULT_REL if audit_result is not None else None,
        "audit_all_pass": audit_result.get("all_pass") if audit_result is not None else None,
        "rows_audited": len(audit_result.get("rows", [])) if audit_result is not None else 0,
        "error": error,
        "status": "COMPLETED" if audit_result and audit_result.get("all_pass") is True and error is None else "FAILED_OR_INCOMPLETE",
    }
    receipt_path.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    current = None
    try:
        current = json.loads(lock_path.read_text(encoding="utf-8"))
    except Exception:
        pass
    if current and current.get("token") == token:
        lock_path.unlink()
    print(json.dumps(receipt, sort_keys=True, indent=2))
    return 0 if receipt["status"] == "COMPLETED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
