"""Supervisor for separately bounded, single-replay v5 mutation trials."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import run_stage_v5

ROOT = Path(__file__).resolve().parents[3]
TRIALS = (
    "untouched_baseline",
    "changed_source",
    "changed_protocol_input",
    "omitted_final_slab",
    "reset_fixed_label_hash",
    "altered_contact_inequality",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, value: Any, *, exclusive: bool = False) -> None:
    run_stage_v5.write_json(path, value, exclusive=exclusive)


def run_audit(binding_path: Path, record_path: Path, output_dir: Path) -> dict[str, Any]:
    binding_path = binding_path.resolve()
    record_path = record_path.resolve()
    output_dir = output_dir.resolve()
    binding_rel = binding_path.relative_to(ROOT).as_posix()
    record_rel = record_path.relative_to(ROOT).as_posix()
    binding = run_stage_v5.read_json(binding_path)
    plan_path = ROOT / binding["plan_path"]
    plan = run_stage_v5.read_json(plan_path)
    freeze = run_stage_v5.verify_freeze_receipt(plan_path, plan)
    if freeze.get("binding_sha256", {}).get(binding_rel) != run_stage_v5.sha(binding_path):
        raise ValueError("FREEZE_RECEIPT_BINDING_HASH_MISMATCH")
    for rel, expected in binding["source_files"].items():
        if run_stage_v5.sha(ROOT / rel) != expected:
            raise ValueError(f"SOURCE_HASH_MISMATCH:{rel}")
    if run_stage_v5.sha(ROOT / binding["protocol_path"]) != binding["protocol_sha256"] or run_stage_v5.sha(ROOT / binding["profile_path"]) != binding["profile_sha256"]:
        raise ValueError("FROZEN_INPUT_HASH_MISMATCH")
    profile = run_stage_v5.read_json(ROOT / binding["profile_path"])
    output_dir.mkdir(parents=True, exist_ok=False)
    report_path = output_dir / "mutation_audit_report.json"
    lock_path = ROOT / "coordination/autonomous_w2/COMPUTE.lock"
    lock_token = uuid.uuid4().hex
    lock = {
        "session": "DDWMR | LUNA-G2-SCOPE",
        "pid": os.getpid(),
        "started_utc": utc_now(),
        "task": "v5 saved-proof mutation trials split into per-replay 60 s caps; no native query",
        "binding_path": binding_rel,
        "binding_sha256": run_stage_v5.sha(binding_path),
        "plan_path": binding.get("plan_path"),
        "plan_sha256": run_stage_v5.sha(plan_path),
        "token": lock_token,
    }
    write_json(lock_path, lock, exclusive=True)
    started = time.monotonic()
    trial_results = []
    env = os.environ.copy()
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONUTF8"] = "1"
    try:
        for label in TRIALS:
            trial_dir = output_dir / label
            trial_dir.mkdir()
            scratch_rel = (trial_dir / "scratch").relative_to(ROOT).as_posix()
            command = [
                sys.executable,
                "-m",
                "validation.autonomous_w2.g2.mutation_trial_v5",
                "--trial",
                label,
                "--binding",
                binding_rel,
                "--record",
                record_rel,
                "--scratch-root",
                scratch_rel,
            ]
            process = run_stage_v5.bounded(command, profile)
            stdout = base64.b64decode(((process.get("job") or {}).get("stdout") or {}).get("prefix_base64", ""))
            stderr = base64.b64decode(((process.get("job") or {}).get("stderr") or {}).get("prefix_base64", ""))
            write_json(trial_dir / "job.json", process)
            (trial_dir / "stdout.bin").write_bytes(stdout)
            (trial_dir / "stderr.bin").write_bytes(stderr)
            try:
                parsed = json.loads(stdout.decode("utf-8").strip())
            except BaseException:
                parsed = None
            job = process.get("job") or {}
            trial_ok = (
                job.get("status") == "COMPLETED"
                and isinstance(parsed, dict)
                and parsed.get("status") == ("PASS" if label == "untouched_baseline" else "REJECTED_AS_REQUIRED")
            )
            row = {
                "trial": label,
                "status": "PASS" if trial_ok else (parsed.get("status") if isinstance(parsed, dict) else job.get("status", "NO_JOB_RESULT")),
                "job_status": job.get("status"),
                "elapsed_seconds_display_only": job.get("elapsed_seconds_display_only"),
                "returncode": job.get("returncode"),
                "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
                "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
                "result": parsed,
                "native_attempts_added": 0,
            }
            write_json(trial_dir / "trial_receipt.json", row)
            trial_results.append(row)
        required = len(TRIALS)
        summary = {
            "schema": "G2_W2_V5_SPLIT_MUTATION_AUDIT_v1",
            "session": "DDWMR | LUNA-G2-SCOPE",
            "binding_path": binding_rel,
            "binding_sha256": run_stage_v5.sha(binding_path),
            "record_path": record_rel,
            "record_sha256": run_stage_v5.sha(record_path),
            "audit_runner_sha256": run_stage_v5.sha(Path(__file__)),
            "single_trial_runner_sha256": run_stage_v5.sha(Path(__file__).with_name("mutation_trial_v5.py")),
            "per_trial_wall_cap_seconds": int(profile["worker_wall_cap_seconds"]),
            "per_trial_memory_cap_bytes": int(profile["worker_memory_cap_bytes"]),
            "trial_count": len(trial_results),
            "required_trial_count": required,
            "all_required_mutations_rejected": len(trial_results) == required and all(item["status"] == "PASS" for item in trial_results),
            "native_attempts_added": 0,
            "phase_elapsed_seconds_display_only": round(time.monotonic() - started, 6),
            "trials": trial_results,
        }
        write_json(report_path, summary, exclusive=True)
        return summary
    finally:
        try:
            if run_stage_v5.read_json(lock_path).get("token") == lock_token:
                lock_path.unlink()
        except FileNotFoundError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding", required=True)
    parser.add_argument("--record", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    def rooted(value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else ROOT / path

    try:
        result = run_audit(rooted(args.binding), rooted(args.record), rooted(args.output_dir))
        print(json.dumps(result, sort_keys=True, indent=2))
        return 0 if result["all_required_mutations_rejected"] else 3
    except BaseException as exc:
        print(json.dumps({"schema": "G2_W2_SPLIT_MUTATION_AUDIT_FAILURE_v1", "error": f"{type(exc).__name__}:{exc}"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
