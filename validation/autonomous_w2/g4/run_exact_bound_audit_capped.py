"""Run the G4 exact-bound audit under the W2 Windows Job Object limits.

This is a read-only mathematical audit of the three already saved G2 v6 rows.
It invokes no producer and does not overwrite the earlier v1 audit artifact.
"""
from __future__ import annotations

import hashlib
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

AUDITOR_REL = "validation/autonomous_w2/g4/audit_g2_v6_exact_bounds.py"
AUDIT_RESULT_REL = "results/validation/autonomous_w2/g4/exact_bound_audit_v2_supervised/audit_result.json"
RECEIPT_REL = "results/validation/autonomous_w2/g4/exact_bound_audit_v2_supervised/audit_receipt.json"
LOCK_REL = "coordination/autonomous_w2/COMPUTE.lock"
RELEASE_SHA256 = "789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55"


def contained(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError(f"PATH_ESCAPES_REPO:{relative}")
    return path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    result_path = contained(AUDIT_RESULT_REL)
    receipt_path = contained(RECEIPT_REL)
    lock_path = contained(LOCK_REL)
    if result_path.exists() or receipt_path.exists():
        raise FileExistsError("SUPERVISED_AUDIT_OUTPUT_ALREADY_EXISTS")
    result_path.parent.mkdir(parents=True, exist_ok=True)
    token = uuid.uuid4().hex
    lock_doc = {
        "session": "DDWMR | LUNA-G4-AUER",
        "pid": os.getpid(),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "read-only capped exact-bound audit of saved G2 v6 records",
        "release_sha256": RELEASE_SHA256,
        "token": token,
    }
    fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(lock_doc, stream, sort_keys=True, indent=2)
        stream.write("\n")

    auditor_path = contained(AUDITOR_REL)
    child_program = "\n".join(
        (
            "import json",
            "from pathlib import Path",
            "import validation.autonomous_w2.g4.audit_g2_v6_exact_bounds as audit",
            "original_root_file = audit.root_file",
            f"target = Path({str(result_path)!r})",
            "audit.root_file = lambda relative: target if relative == 'results/validation/autonomous_w2/g4/exact_bound_audit_v1.json' else original_root_file(relative)",
            "raise SystemExit(audit.main())",
        )
    )
    command = [sys.executable, "-B", "-c", child_program]
    process_json: dict[str, Any] | None = None
    audit_result: dict[str, Any] | None = None
    runner_error: str | None = None
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
        stdout = bounded.stdout.prefix
        try:
            audit_result = json.loads(stdout.decode("utf-8"))
        except Exception as exc:  # retain the raw bounded child evidence below
            runner_error = f"AUDIT_STDOUT_JSON_PARSE_ERROR:{type(exc).__name__}:{exc}"
        if bounded.status != "COMPLETED" or bounded.returncode != 0:
            runner_error = runner_error or f"AUDITOR_PROCESS_NOT_COMPLETED:{bounded.status}:{bounded.returncode}"
        if audit_result is not None:
            result_path.write_text(json.dumps(audit_result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    except BaseException as exc:
        runner_error = f"SUPERVISOR_EXCEPTION:{type(exc).__name__}:{exc}"

    auditor_sha = sha256(auditor_path)
    wrapper_path = Path(__file__).resolve()
    receipt = {
        "schema": "G4_W2_G2_V6_EXACT_BOUND_SUPERVISED_AUDIT_RECEIPT_v1",
        "session": "DDWMR | LUNA-G4-AUER",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "read_only_saved_row_audit": True,
        "producer_invocations": 0,
        "native_attempts_added": 0,
        "release_sha256": RELEASE_SHA256,
        "source": {
            "auditor_path": AUDITOR_REL,
            "auditor_sha256": auditor_sha,
            "runner_path": "validation/autonomous_w2/g4/run_exact_bound_audit_capped.py",
            "runner_sha256": sha256(wrapper_path),
        },
        "command": command,
        "limits": {
            "wall_seconds": 60,
            "cpu_seconds": 60,
            "memory_bytes": 1_073_741_824,
            "processes": 1,
            "stdout_bytes": 8_388_608,
            "stderr_bytes": 1_048_576,
        },
        "process": process_json,
        "audit_result_path": AUDIT_RESULT_REL if audit_result is not None else None,
        "audit_all_pass": audit_result.get("all_pass") if audit_result is not None else None,
        "rows_audited": len(audit_result.get("rows", [])) if audit_result is not None else 0,
        "runner_error": runner_error,
        "status": "COMPLETED" if audit_result and audit_result.get("all_pass") is True and runner_error is None else "FAILED_OR_INCOMPLETE",
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
