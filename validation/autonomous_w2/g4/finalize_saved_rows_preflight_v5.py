"""Finalize and check already completed read-only preflight replay records."""
from __future__ import annotations

import json
import time
from pathlib import Path

from validation.autonomous_w2.g4.matched_v6_common_v2 import (
    PROJECT, RESULT_REL, sha256_file, strict_json, write_json,
)


def main() -> int:
    started = time.monotonic()
    result_root = PROJECT / RESULT_REL
    mapping_path = result_root / "mapping_preflight_v2.json"
    mapping = strict_json(mapping_path)
    if mapping.get("result") != "PASS_NONQUERY_MAPPING" or mapping.get("fresh_native_calls") != 0:
        raise RuntimeError("MAPPING_PREFLIGHT_NOT_PASS_NONQUERY")
    rows = []
    for ordinal, item in enumerate(mapping["rows"], 1):
        output = result_root / "preflight_saved_rows_v5" / f"{ordinal:02d}_{item['external_id']}"
        job_path = output / "worker.job.json"
        saved_path = output / "saved_replay_result.json"
        stdout_path, stderr_path = output / "worker.stdout.bin", output / "worker.stderr.bin"
        for required in (job_path, saved_path, stdout_path, stderr_path, output / "common_record.json", output / "progress.json"):
            if not required.is_file():
                raise FileNotFoundError(f"PREFLIGHT_ARTIFACT_MISSING:{required}")
        job = strict_json(job_path)
        saved = strict_json(saved_path)
        if job.get("status") != "COMPLETED" or job.get("returncode") != 0:
            raise RuntimeError(f"PREFLIGHT_JOB_NOT_COMPLETE:{item['external_id']}")
        if not job.get("process_assigned_before_resume") or not job.get("process_in_job"):
            raise RuntimeError(f"PREFLIGHT_JOB_OBJECT_NOT_ENFORCED:{item['external_id']}")
        if job["job"]["peak_memory_bytes"] > 1_073_741_824 or job["elapsed_seconds_display_only"] > 60:
            raise RuntimeError(f"PREFLIGHT_LIMIT_EXCEEDED:{item['external_id']}")
        if saved.get("fresh_native_calls") != 0 or saved.get("read_only_saved_row_replay") is not True:
            raise RuntimeError(f"PREFLIGHT_NOT_READ_ONLY:{item['external_id']}")
        if saved.get("native_replay_status") != "PASS" or saved.get("common_replay_status") != "PASS":
            raise RuntimeError(f"PREFLIGHT_REPLAY_NOT_PASS:{item['external_id']}")
        rows.append({
            "ordinal": ordinal,
            "comparison_id": item["external_id"],
            "saved_row_path": item["peer_action_id"],
            "read_only_saved_row_replay": True,
            "fresh_native_calls": 0,
            "native_replay_status": saved["native_replay_status"],
            "common_replay_status": saved["common_replay_status"],
            "task_eligible": saved["task_eligible"],
            "progress_lower_meets_threshold": saved["progress_lower_meets_threshold"],
            "saved_replay_result_path": saved_path.relative_to(PROJECT).as_posix(),
            "saved_replay_result_sha256": sha256_file(saved_path),
            "common_record_sha256": sha256_file(output / "common_record.json"),
            "progress_sha256": sha256_file(output / "progress.json"),
            "job_receipt_sha256": sha256_file(job_path),
            "stdout_sha256": sha256_file(stdout_path),
            "stderr_sha256": sha256_file(stderr_path),
            "worker_wall_seconds": job["elapsed_seconds_display_only"],
            "worker_cpu_seconds": (job["job"]["total_user_time_100ns"] + job["job"]["total_kernel_time_100ns"]) / 10_000_000,
            "worker_peak_memory_bytes": job["job"]["peak_memory_bytes"],
        })
    result = {
        "schema": "ddwmr-g4-w2-saved-v6-readonly-preflight-v5",
        "session": "DDWMR | LUNA-G4-AUER",
        "mapping_preflight_sha256": sha256_file(mapping_path),
        "peer_release_sha256": mapping["peer_release_sha256"],
        "saved_action_count": len(rows),
        "all_native_saved_replays_pass": all(row["native_replay_status"] == "PASS" for row in rows),
        "all_common_replays_pass": all(row["common_replay_status"] == "PASS" for row in rows),
        "all_actions_task_eligibility_matches_saved_g2_v6": [row["task_eligible"] for row in rows] == [False, False, True],
        "fresh_native_calls": 0,
        "rows": rows,
        "finalizer_wall_seconds": time.monotonic() - started,
    }
    write_json(result_root / "saved_replay_preflight_v5.json", result, max_bytes=1_048_576, exclusive=True)
    print(json.dumps({key: value for key, value in result.items() if key != "rows"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
