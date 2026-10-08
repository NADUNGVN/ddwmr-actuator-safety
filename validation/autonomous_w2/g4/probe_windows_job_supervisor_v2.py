"""Non-query enforcement probe for the one-process Windows Job Object runner."""
from __future__ import annotations

import json
import os
import platform
import sys
from pathlib import Path

from validation.autonomous_w2.g4.matched_v6_common_v2 import PROJECT, RESULT_REL, write_json
from validation.autonomous_w2.g4.windows_job_supervisor_v2 import result_to_json, run_bounded_process


def main() -> int:
    if os.name != "nt":
        raise RuntimeError("WINDOWS_JOB_OBJECT_REQUIRED")
    out_dir = PROJECT / RESULT_REL / "resource_probe_v2"
    if out_dir.exists():
        raise FileExistsError(f"RESOURCE_PROBE_OUTPUT_EXISTS:{out_dir}")
    out_dir.mkdir(parents=True, exist_ok=False)
    child = [sys.executable, "-B", "-c", "import json;print(json.dumps({'probe':'JOB_OBJECT_OK','children':1}))"]
    env = {**os.environ, "PYTHONHASHSEED": "0", "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    result = run_bounded_process(
        child, cwd=PROJECT, wall_seconds=60, cpu_seconds=60,
        memory_bytes=1_073_741_824, max_processes=1,
        stdout_limit_bytes=8_388_608, stderr_limit_bytes=1_048_576,
        environment=env,
    )
    stdout = result.stdout.prefix
    stderr = result.stderr.prefix
    (out_dir / "probe.stdout.bin").write_bytes(stdout)
    (out_dir / "probe.stderr.bin").write_bytes(stderr)
    report = {
        "schema": "ddwmr-g4-w2-windows-job-object-probe-v2",
        "session": "DDWMR | LUNA-G4-AUER",
        "command": child,
        "environment_allowlist": {key: env[key] for key in ("PYTHONHASHSEED", "PYTHONUTF8", "PYTHONDONTWRITEBYTECODE")},
        "host": {"os_name": os.name, "platform": platform.platform(), "python": sys.version, "executable": sys.executable},
        "result": result_to_json(result),
        "stdout_json": json.loads(stdout.decode("utf-8")) if stdout else None,
        "passed": result.status == "COMPLETED" and result.returncode == 0 and result.process_assigned_before_resume and result.process_in_job,
        "native_calls": 0,
    }
    write_json(out_dir / "probe_receipt.json", report, max_bytes=1_048_576, exclusive=True)
    print(json.dumps({key: report[key] for key in ("schema", "passed", "native_calls", "host")}, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
