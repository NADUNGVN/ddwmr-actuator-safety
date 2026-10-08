"""Run fresh, read-only saved-row replays under the frozen W2 child limits."""
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
    PLAN_REL, PROJECT, sha256_file, strict_json, write_json,
)
from validation.autonomous_w2.g4.windows_job_supervisor_v2 import (
    result_to_json, run_bounded_process,
)

RESULT_REL = Path("results/validation/autonomous_w2/g4/matched_v6_task_development_v2")
CAPS = {
    "wall_seconds": 60, "cpu_seconds": 60, "memory_bytes": 1_073_741_824,
    "max_processes": 1, "stdout_bytes": 8_388_608, "stderr_bytes": 1_048_576,
}
LOCK = PROJECT / "coordination/autonomous_w2/COMPUTE.lock"


def run_one(mapping_row: dict[str, Any]) -> dict[str, Any]:
    protocol = strict_json(PROJECT / PLAN_REL / "protocol_v2.json")
    ordinal = next(index for index, item in enumerate(protocol["actions"], 1)
                   if item["comparison_id"] == mapping_row["external_id"])
    output_dir = PROJECT / RESULT_REL / "preflight_saved_rows_v8" / f"{ordinal:02d}_{mapping_row['external_id']}"
    if output_dir.exists():
        raise FileExistsError(f"PREFLIGHT_OUTPUT_ALREADY_EXISTS:{output_dir}")
    output_dir.mkdir(parents=True, exist_ok=False)
    g4_binding_rel = PLAN_REL / "v6_bindings" / f"{ordinal:02d}.json"
    g4_binding = strict_json(PROJECT / g4_binding_rel)
    core_binding = PROJECT / g4_binding["core_binding_path"]
    row = PROJECT / g4_binding["peer_saved_row_path"]
    command = [
        sys.executable, "-B", "-m", "validation.autonomous_w2.g4.replay_saved_v6_worker_v2",
        "--binding", str(core_binding), "--comparison-id", mapping_row["external_id"],
        "--row", str(row), "--output-dir", str(output_dir),
    ]
    env = {**os.environ, "PYTHONHASHSEED": "0", "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    started = time.monotonic()
    result = run_bounded_process(
        command, cwd=PROJECT, wall_seconds=CAPS["wall_seconds"], cpu_seconds=CAPS["cpu_seconds"],
        memory_bytes=CAPS["memory_bytes"], max_processes=CAPS["max_processes"],
        stdout_limit_bytes=CAPS["stdout_bytes"], stderr_limit_bytes=CAPS["stderr_bytes"],
        environment=env,
    )
    encoded = result_to_json(result)
    stdout_path, stderr_path = output_dir / "worker.stdout.bin", output_dir / "worker.stderr.bin"
    stdout_path.write_bytes(result.stdout.prefix)
    stderr_path.write_bytes(result.stderr.prefix)
    write_json(output_dir / "worker.job.json", encoded, max_bytes=1_048_576, exclusive=True)
    if result.status != "COMPLETED" or result.returncode != 0:
        raise RuntimeError(f"SAVED_REPLAY_WORKER_FAILED:{mapping_row['external_id']}:{result.status}:{result.returncode}")
    report = strict_json(output_dir / "saved_replay_result.json")
    if report.get("fresh_native_calls") != 0 or not report.get("read_only_saved_row_replay"):
        raise RuntimeError("PREFLIGHT_WORKER_DID_NOT_PROVE_READ_ONLY_SCOPE")
    return {
        "comparison_id": mapping_row["external_id"],
        "saved_row_path": g4_binding["peer_saved_row_path"],
        "saved_row_sha256": sha256_file(row),
        "saved_binding_path": g4_binding["core_binding_path"],
        "job_summary": {
            "status": encoded["status"],
            "returncode": encoded["returncode"],
            "process_assigned_before_resume": encoded["process_assigned_before_resume"],
            "process_in_job": encoded["process_in_job"],
            "job": encoded["job"],
            "termination_reason": encoded["termination_reason"],
        },
        "command": command,
        "environment_allowlist": {key: env[key] for key in ("PYTHONHASHSEED", "PYTHONUTF8", "PYTHONDONTWRITEBYTECODE")},
        "stdout_path": stdout_path.relative_to(PROJECT).as_posix(),
        "stdout_sha256": sha256_file(stdout_path),
        "stderr_path": stderr_path.relative_to(PROJECT).as_posix(),
        "stderr_sha256": sha256_file(stderr_path),
        "job_path": (output_dir / "worker.job.json").relative_to(PROJECT).as_posix(),
        "job_sha256": sha256_file(output_dir / "worker.job.json"),
        "saved_replay_result_path": (output_dir / "saved_replay_result.json").relative_to(PROJECT).as_posix(),
        "saved_replay_result_sha256": sha256_file(output_dir / "saved_replay_result.json"),
        "worker_wall_seconds": result.elapsed_seconds,
        "worker_cpu_seconds": (result.job_total_user_time_100ns + result.job_total_kernel_time_100ns) / 10_000_000,
        "worker_peak_memory_bytes": result.job_peak_memory_bytes,
        "elapsed_parent_seconds": time.monotonic() - started,
        "native_calls": 0,
    }


def main() -> int:
    started = time.monotonic()
    mapping_path = PROJECT / RESULT_REL / "mapping_preflight_v3.json"
    mapping = strict_json(mapping_path)
    if mapping.get("result") != "PASS_NONQUERY_MAPPING" or mapping.get("fresh_native_calls") != 0:
        raise RuntimeError("MAPPING_PREFLIGHT_NOT_PASS_NONQUERY")
    token = uuid.uuid4().hex
    lock_doc = {
        "schema": "ddwmr-g4-w2-compute-lock-v2",
        "session": "DDWMR | LUNA-G4-AUER",
        "pid": os.getpid(),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "sequential read-only replay of three previously saved G2 development proofs",
        "mapping_preflight_sha256": sha256_file(mapping_path),
        "token": token,
    }
    fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(lock_doc, stream, sort_keys=True, indent=2)
        stream.write("\n"); stream.flush(); os.fsync(stream.fileno())
    try:
        rows = [run_one(item) for item in mapping["rows"]]
    finally:
        if LOCK.is_file():
            try:
                current = strict_json(LOCK)
                if current.get("token") == token:
                    LOCK.unlink()
            except Exception:
                pass
    result = {
        "schema": "ddwmr-g4-w2-saved-v6-readonly-preflight-v8",
        "session": "DDWMR | LUNA-G4-AUER",
        "mapping_preflight_sha256": sha256_file(mapping_path),
        "peer_release_sha256": mapping["peer_release_sha256"],
        "saved_action_count": len(rows),
        "all_native_saved_replays_pass": all(strict_json(PROJECT / row["saved_replay_result_path"]).get("native_replay_status") == "PASS" for row in rows),
        "all_common_replays_pass": all(strict_json(PROJECT / row["saved_replay_result_path"]).get("common_replay_status") == "PASS" for row in rows),
        "fresh_native_calls": 0,
        "compute_lock": lock_doc,
        "compute_lock_released": not LOCK.exists(),
        "rows": rows,
        "wall_seconds": time.monotonic() - started,
    }
    write_json(PROJECT / RESULT_REL / "saved_replay_preflight_v8.json", result, max_bytes=1_048_576, exclusive=True)
    print(json.dumps({key: value for key, value in result.items() if key != "rows"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
