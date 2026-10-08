"""Read-only, resource-capped replay of the three saved G2 v6 records.

This invokes only G2's published checker on immutable saved bindings/rows.
It never imports or invokes the G2 producer and never creates a native query.
Outputs are written only below results/validation/autonomous_w2/g4/.
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

from validation.autonomous_w2.g2.windows_job_supervisor import (
    result_to_json,
    run_bounded_process,
)


RELEASE_REL = "coordination/autonomous_w2/g2/releases/RELEASE_v6.json"
RELEASE_SHA256 = "789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55"
STATUS_REL = "coordination/autonomous_w2/g2/STATUS.json"
INVENTORY_REL = "results/validation/autonomous_w2/g2/development_centered_v6/evidence_inventory_v1.json"
LOCK_REL = "coordination/autonomous_w2/COMPUTE.lock"
OUT_REL = "results/validation/autonomous_w2/g4/replay_g2_v6_saved_789d6b37_r2"
CASES = (
    (
        "zero",
        "research/autonomous_w2/g2/bindings_centered_v6/attempt_01.json",
        "results/validation/autonomous_w2/g2/development_centered_v6/attempt_01_W2_G2_DEV_001_ZERO/row.json",
        "6639ceaac7b87e063fdc6b5b91a686c3d56d7a04202efc6000c1d322630ac6fa",
    ),
    (
        "nominal",
        "research/autonomous_w2/g2/bindings_centered_v6/attempt_02.json",
        "results/validation/autonomous_w2/g2/development_centered_v6/attempt_02_W2_G2_DEV_001_NOMINAL/row.json",
        "c53239caeedab91713ecbf41de7be71d7f8b1e66928d4554f4a819cf204cd171",
    ),
    (
        "alternative",
        "research/autonomous_w2/g2/bindings_centered_v6/attempt_03.json",
        "results/validation/autonomous_w2/g2/development_centered_v6/attempt_03_W2_G2_DEV_001_ALTERNATIVE/row.json",
        "38ba67273d56c798347f37dae16b74e5a3751e52f3eebeb53d6291b3e7b6ad92",
    ),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def root_file(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError(f"PATH_ESCAPES_REPO:{relative}")
    return path


def verify_release_bindings() -> dict[str, Any]:
    release_path = root_file(RELEASE_REL)
    actual_release_hash = sha256(release_path)
    if actual_release_hash != RELEASE_SHA256:
        raise ValueError(f"RELEASE_HASH_MISMATCH:{actual_release_hash}")
    sidecar = root_file(RELEASE_REL + ".sha256").read_text(encoding="ascii").strip().split()[0]
    if sidecar.lower() != RELEASE_SHA256:
        raise ValueError(f"RELEASE_SIDECAR_MISMATCH:{sidecar}")

    release = load(release_path)
    status = load(root_file(STATUS_REL))
    if status.get("release", {}).get("sha256") != RELEASE_SHA256:
        raise ValueError("STATUS_RELEASE_BINDING_MISMATCH")
    inventory_path = root_file(INVENTORY_REL)
    inventory = load(inventory_path)
    if inventory.get("release_sha256") != RELEASE_SHA256:
        raise ValueError("INVENTORY_RELEASE_BINDING_MISMATCH")
    source_pins = release["source_closure"]["sha256_by_path"]
    if len(source_pins) != 31:
        raise ValueError(f"SOURCE_CLOSURE_COUNT:{len(source_pins)}")
    source_issues: list[str] = []
    for relative, expected in source_pins.items():
        path = root_file(relative)
        if not path.is_file() or sha256(path) != expected:
            source_issues.append(relative)

    evidence = inventory.get("files", [])
    if len(evidence) != 139:
        raise ValueError(f"EVIDENCE_INVENTORY_COUNT:{len(evidence)}")
    evidence_issues: list[str] = []
    for entry in evidence:
        path = root_file(entry["path"])
        if not path.is_file() or path.stat().st_size != entry["bytes"] or sha256(path) != entry["sha256"]:
            evidence_issues.append(entry["path"])

    if source_issues or evidence_issues:
        raise ValueError(f"SOURCE_OR_EVIDENCE_MISMATCH:sources={source_issues};evidence={evidence_issues}")
    return {
        "release_path": RELEASE_REL,
        "release_sha256": actual_release_hash,
        "release_sidecar_sha256_value": sidecar,
        "g2_status_sequence": status.get("sequence"),
        "g2_status_release_sha256": status["release"]["sha256"],
        "inventory_path": INVENTORY_REL,
        "inventory_sha256": sha256(inventory_path),
        "source_count": len(source_pins),
        "sources_verified": len(source_pins),
        "evidence_count": len(evidence),
        "evidence_verified": len(evidence),
    }


def bounded_replay(name: str, binding_rel: str, record_rel: str) -> dict[str, Any]:
    command = [
        sys.executable,
        "-B",
        "-m",
        "validation.autonomous_w2.g2.checker_centered_v6",
        "--binding",
        binding_rel,
        "--record",
        record_rel,
    ]
    result = run_bounded_process(
        command,
        cwd=ROOT,
        wall_seconds=60,
        cpu_seconds=60,
        memory_bytes=1_073_741_824,
        max_processes=1,
        stdout_limit_bytes=8_388_608,
        stderr_limit_bytes=1_048_576,
    )
    serialized = result_to_json(result)
    stdout = result.stdout.prefix
    stderr = result.stderr.prefix
    out_root = root_file(OUT_REL)
    (out_root / f"{name}.stdout.bin").write_bytes(stdout)
    (out_root / f"{name}.stderr.bin").write_bytes(stderr)
    (out_root / f"{name}.job.json").write_text(
        json.dumps(serialized, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )

    parsed: dict[str, Any] | None = None
    parse_error: str | None = None
    try:
        value = json.loads(stdout.decode("utf-8"))
        if isinstance(value, dict):
            parsed = value
        else:
            parse_error = "CHECKER_OUTPUT_NOT_OBJECT"
    except Exception as exc:  # Preserve malformed/partial output as a failure record.
        parse_error = f"{type(exc).__name__}:{exc}"
    replayed = (
        result.status == "COMPLETED"
        and result.returncode == 0
        and parsed is not None
        and parsed.get("replayed") is True
        and parsed.get("center_slabs_recomputed") == 256
    )
    return {
        "case": name,
        "command": command,
        "status": result.status,
        "returncode": result.returncode,
        "elapsed_seconds": round(result.elapsed_seconds, 6),
        "peak_memory_bytes": result.job_peak_memory_bytes,
        "total_user_time_100ns": result.job_total_user_time_100ns,
        "total_kernel_time_100ns": result.job_total_kernel_time_100ns,
        "process_count": result.job_total_processes,
        "process_assigned_before_resume": result.process_assigned_before_resume,
        "process_in_job": result.process_in_job,
        "stdout_bytes": result.stdout.bytes_observed,
        "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
        "stderr_bytes": result.stderr.bytes_observed,
        "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
        "saved_binding_sha256": sha256(root_file(binding_rel)),
        "saved_record_sha256": sha256(root_file(record_rel)),
        "checker_replayed": bool(parsed and parsed.get("replayed") is True),
        "proof_fields_recomputed": parsed.get("proof_fields_recomputed") if parsed else None,
        "center_slabs_recomputed": parsed.get("center_slabs_recomputed") if parsed else None,
        "recomputed_safety_status": parsed.get("recomputed_safety_status") if parsed else None,
        "recomputed_task_eligible": parsed.get("recomputed_task_eligible") if parsed else None,
        "shared_trust": parsed.get("shared_trust") if parsed else None,
        "parse_error": parse_error,
        "replay_pass": replayed,
    }


def main() -> int:
    out_root = root_file(OUT_REL)
    out_root.mkdir(parents=True, exist_ok=False)
    lock_path = root_file(LOCK_REL)
    token = uuid.uuid4().hex
    lock_doc = {
        "session": "DDWMR | LUNA-G4-AUER",
        "pid": os.getpid(),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "read-only release-v6 saved checker replay",
        "release_sha256": RELEASE_SHA256,
        "token": token,
    }
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise RuntimeError(f"COMPUTE_LOCK_ALREADY_HELD:{LOCK_REL}")
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(lock_doc, stream, sort_keys=True, indent=2)
        stream.write("\n")

    try:
        integrity = verify_release_bindings()
        replays = [bounded_replay(*case[:3]) for case in CASES]
        summary = {
            "schema": "G4_W2_G2_V6_SAVED_REPLAY_RECEIPT_v1",
            "session": "DDWMR | LUNA-G4-AUER",
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "release_sha256": RELEASE_SHA256,
            "integrity": integrity,
            "read_only_saved_replay": True,
            "native_attempts_added": 0,
            "producer_invocations": 0,
            "cases": replays,
            "replayed_count": sum(row["replay_pass"] for row in replays),
            "case_count": len(replays),
            "all_pass": all(row["replay_pass"] for row in replays),
            "limits": {
                "wall_seconds_per_checker": 60,
                "cpu_seconds_per_checker": 60,
                "memory_bytes_per_checker": 1_073_741_824,
                "processes_per_checker": 1,
                "stdout_bytes": 8_388_608,
                "stderr_bytes": 1_048_576,
            },
        }
        (out_root / "replay_receipt.json").write_text(
            json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(summary, sort_keys=True, indent=2))
        return 0 if summary["all_pass"] else 2
    finally:
        current = None
        try:
            current = json.loads(lock_path.read_text(encoding="utf-8"))
        except Exception:
            pass
        if current and current.get("token") == token:
            lock_path.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
