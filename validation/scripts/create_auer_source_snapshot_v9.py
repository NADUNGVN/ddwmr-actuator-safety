"""Freeze the corrected R4 worker and enforceable resource runner as v9."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/validation/g4/auer2013"
PREVIOUS = BASE / "source_snapshot_v8"
SNAPSHOT = BASE / "source_snapshot_v9"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checked_copy_tree(source: Path, target: Path) -> None:
    if target.exists():
        resolved_root, resolved_target = target.parent.resolve(), target.resolve()
        if resolved_root not in resolved_target.parents:
            raise SystemExit(f"refusing to remove path outside snapshot project: {resolved_target}")
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))


def main() -> None:
    if SNAPSHOT.exists():
        raise SystemExit(f"refusing to overwrite existing snapshot: {SNAPSHOT}")
    previous_manifest_path = PREVIOUS / "snapshot_manifest.json"
    previous_bytes = previous_manifest_path.read_bytes()
    previous_hash = hashlib.sha256(previous_bytes).hexdigest()
    sidecar_hash = (PREVIOUS / "snapshot_manifest.sha256").read_text(encoding="ascii").split()[0]
    if previous_hash != sidecar_hash:
        raise SystemExit("v8 source snapshot sidecar mismatch")
    previous = json.loads(previous_bytes)
    previous_members = {}
    for member in previous["members"]:
        path = PREVIOUS / member["snapshot_relative_path"]
        if not path.is_file() or path.stat().st_size != member["bytes"] or sha256(path) != member["sha256"]:
            raise SystemExit(f"v8 source snapshot member failed replay: {member['snapshot_relative_path']}")
        previous_members[member["snapshot_relative_path"]] = member["sha256"]

    SNAPSHOT.mkdir(parents=True)
    for folder in ("project", "environment", "runs"):
        shutil.copytree(PREVIOUS / folder, SNAPSHOT / folder)
    project = SNAPSHOT / "project"
    for relative in ("validation/baselines/auer2013", "validation/g4", "validation/scripts"):
        checked_copy_tree(ROOT / relative, project / relative)
    method_relative = "docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md"
    destination = project / method_relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / method_relative, destination)

    unchanged = (
        "validation/g2/rational.py",
        "validation/g2/interval.py",
        "validation/g2/model.py",
        "validation/configs/benchmark_v1.json",
        "external/valencia-basic/free-source/ValEncIA/ValEncIA-IVP_0.92_2e.cpp",
        "research/third_party/auer2013/auer-kiel-rauh-2013.pdf",
        "research/third_party/auer2013/references/rauh-auer-2011-valencia.pdf",
    )
    for relative in unchanged:
        previous_member = previous_members.get(f"project/{relative}")
        if previous_member is None or previous_member != sha256(ROOT / relative):
            raise SystemExit(f"shared or primary-source input changed since v8: {relative}")

    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    status = subprocess.run(["git", "status", "--short"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.splitlines()
    backend = json.loads((ROOT / "validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v2.json").read_text(encoding="utf-8"))

    members = []
    for path in sorted(item for item in SNAPSHOT.rglob("*") if item.is_file()):
        if path.name in {"snapshot_manifest.json", "snapshot_manifest.sha256"}:
            continue
        members.append({
            "snapshot_relative_path": path.relative_to(SNAPSHOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    manifest = {
        "schema": "ddwmr-g4-auer-local-source-snapshot-v9",
        "status": "R4_SOURCE_FROZEN_BEFORE_IVP_EXECUTION",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_git_revision": revision,
        "branch": branch,
        "worktree_status_at_snapshot": status,
        "source_tree_clean": not bool(status),
        "previous_snapshot_manifest_sha256": previous_hash,
        "previous_snapshot_member_count_verified": len(previous["members"]),
        "method_contract": "project/docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md",
        "active_arithmetic_manifest": "project/validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v2.json",
        "active_resource_profile": "project/validation/baselines/auer2013/small_case_resource_profile_v2.json",
        "selected_ddwmr_input": "project/validation/baselines/auer2013/auer_r4_ddwmr_single_case_input_v1.json",
        "process_limit_runner": "project/validation/baselines/auer2013/process_limiter.py",
        "runtime_executable": backend["python_runtime"]["executable"],
        "runtime_executable_sha256": backend["python_runtime"]["executable_sha256"],
        "runtime_version": backend["python_runtime"]["version"],
        "runtime_compiler": backend["python_runtime"]["compiler_reported_by_interpreter"],
        "native_compile_link_flags": "NOT_APPLICABLE_NO_NATIVE_AUER_EXECUTABLE",
        "pre_snapshot_auer_ivp_runs": 0,
        "pre_snapshot_memory_probe_attempts": 1,
        "native_r3_evaluator_reruns": 0,
        "matched_query_evaluations": 0,
        "member_count": len(members),
        "members": members,
        "manifest_hash_semantics": "SHA-256 over exact UTF-8 bytes of this indented sorted-key JSON plus one LF; manifest and sidecar are excluded from members.",
    }
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    (SNAPSHOT / "snapshot_manifest.json").write_bytes(manifest_bytes)
    manifest_sha = hashlib.sha256(manifest_bytes).hexdigest()
    (SNAPSHOT / "snapshot_manifest.sha256").write_text(f"{manifest_sha}  snapshot_manifest.json\n", encoding="ascii", newline="\n")
    print(json.dumps({
        "snapshot_path": str(SNAPSHOT),
        "manifest_sha256": manifest_sha,
        "member_count": len(members),
        "matched_query_evaluations": 0,
        "pre_snapshot_auer_ivp_runs": 0,
        "pre_snapshot_memory_probe_attempts": 1,
        "previous_snapshot_manifest_sha256": previous_hash,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
