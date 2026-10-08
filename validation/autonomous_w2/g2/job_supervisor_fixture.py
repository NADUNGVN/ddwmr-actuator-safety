"""Non-query Windows Job Object launch fixture for the W2 runner boundary."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from .windows_job_supervisor import result_to_json, run_bounded_process


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/validation/autonomous_w2/g2/job_supervisor_fixture_v1.json"


def verify() -> dict[str, object]:
    result = run_bounded_process(
        [sys.executable, "-c", "print('G2_W2_JOB_FIXTURE_OK')"],
        cwd=ROOT,
        wall_seconds=5,
        cpu_seconds=5,
        memory_bytes=512 * 1024 * 1024,
        max_processes=1,
        stdout_limit_bytes=4096,
        stderr_limit_bytes=1024,
        environment={**os.environ, "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"},
    )
    encoded = result_to_json(result)
    stdout = result.stdout.prefix.decode("utf-8", errors="replace").strip()
    job = encoded["job"]
    passed = (
        result.status == "COMPLETED"
        and result.returncode == 0
        and result.process_assigned_before_resume
        and result.process_in_job
        and result.job_total_processes == 1
        and not result.stdout.overflow
        and stdout == "G2_W2_JOB_FIXTURE_OK"
        and result.job_peak_memory_bytes <= 512 * 1024 * 1024
    )
    report: dict[str, object] = {
        "schema": "G2_W2_JOB_OBJECT_NONQUERY_FIXTURE_v1",
        "status": "PASS" if passed else "FAIL",
        "native_development_attempts": 0,
        "command": [sys.executable, "-c", "print('G2_W2_JOB_FIXTURE_OK')"],
        "limits": {"wall_seconds": 5, "cpu_seconds": 5, "memory_bytes": 512 * 1024 * 1024, "max_processes": 1},
        "stdout": stdout,
        "result": job,
        "no_query_or_evaluator_called": True,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        raise FileExistsError("JOB_SUPERVISOR_FIXTURE_RECEIPT_ALREADY_EXISTS")
    OUT.write_text(json.dumps(report, sort_keys=True, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True, indent=2))
