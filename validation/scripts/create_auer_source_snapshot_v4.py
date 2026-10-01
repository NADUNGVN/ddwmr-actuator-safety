"""Freeze the revised single-record R3 common-adapter profile and runner."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/validation/g4/auer2013"
PREVIOUS = BASE / "source_snapshot_v3"
SNAPSHOT = BASE / "source_snapshot_v4"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_file(relative: str, project: Path) -> None:
    source = ROOT / relative
    if not source.is_file():
        raise SystemExit(f"v4 snapshot input missing: {relative}")
    destination = project / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def main() -> None:
    if SNAPSHOT.exists():
        raise SystemExit(f"refusing to overwrite existing snapshot: {SNAPSHOT}")
    prior_path = PREVIOUS / "snapshot_manifest.json"
    prior_sidecar = PREVIOUS / "snapshot_manifest.sha256"
    prior_bytes = prior_path.read_bytes()
    prior_hash = hashlib.sha256(prior_bytes).hexdigest()
    if prior_sidecar.read_text(encoding="ascii").split()[0] != prior_hash:
        raise SystemExit("v3 source snapshot sidecar mismatch")
    prior = json.loads(prior_bytes)
    for item in prior["members"]:
        member = PREVIOUS / item["snapshot_relative_path"]
        if not member.is_file() or member.stat().st_size != item["bytes"] or sha256(member) != item["sha256"]:
            raise SystemExit(f"v3 snapshot member failed replay: {item['snapshot_relative_path']}")

    SNAPSHOT.mkdir(parents=True)
    shutil.copytree(PREVIOUS / "project", SNAPSHOT / "project")
    shutil.copytree(PREVIOUS / "environment", SNAPSHOT / "environment")
    shutil.copytree(PREVIOUS / "runs", SNAPSHOT / "runs")
    project = SNAPSHOT / "project"
    for relative in ("validation/g4", "validation/scripts"):
        destination = project / relative
        resolved_project = project.resolve()
        resolved_destination = destination.resolve()
        if resolved_project not in resolved_destination.parents:
            raise SystemExit(f"refusing to replace a path outside the v4 snapshot project: {resolved_destination}")
        shutil.rmtree(destination)
        shutil.copytree(
            ROOT / relative, destination,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )
    copy_file("results/validation/g4/auer2013/r3_common_adapter_attempts_v1.json", project)

    branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--short"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.splitlines()
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
        "schema": "ddwmr-g4-auer-local-source-snapshot-v4",
        "status": "LOCAL_UNCOMMITTED_BLOCKED_PARTIAL_REVIEW_PACKAGE",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_git_revision": revision,
        "branch": branch,
        "worktree_status_at_snapshot": status,
        "source_tree_clean": not bool(status),
        "previous_snapshot_manifest_sha256": prior_hash,
        "previous_snapshot_member_count_verified": prior["member_count"],
        "common_adapter_profile": "validation/g4/r3_common_adapter_profile_v1.json",
        "native_r3_evaluator_reruns": 0,
        "matched_query_evaluations": 0,
        "auer_solver_available": False,
        "members": members,
        "manifest_hash_semantics": "SHA-256 over exact UTF-8 bytes of this indented sorted-key JSON plus one LF; manifest and sidecar are excluded from members.",
    }
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    manifest_path = SNAPSHOT / "snapshot_manifest.json"
    manifest_path.write_bytes(manifest_bytes)
    manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
    (SNAPSHOT / "snapshot_manifest.sha256").write_text(
        f"{manifest_hash}  snapshot_manifest.json\n", encoding="ascii", newline="\n",
    )
    print(json.dumps({
        "snapshot_path": str(SNAPSHOT),
        "manifest_sha256": manifest_hash,
        "member_count": len(members),
        "branch": branch,
        "base_git_revision": revision,
        "native_r3_evaluator_reruns": 0,
        "matched_query_evaluations": 0,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
