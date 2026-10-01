"""Freeze the corrected R3 adapter runner after preserving earlier failures."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/validation/g4/auer2013"
PREVIOUS = BASE / "source_snapshot_v4"
SNAPSHOT = BASE / "source_snapshot_v5"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    if SNAPSHOT.exists():
        if (SNAPSHOT / "snapshot_manifest.json").exists():
            raise SystemExit(f"refusing to overwrite an existing completed snapshot: {SNAPSHOT}")
        if not all((SNAPSHOT / item).is_dir() for item in ("project", "environment", "runs")):
            raise SystemExit(f"existing snapshot path is not a recognized resumable partial: {SNAPSHOT}")
    previous_path = PREVIOUS / "snapshot_manifest.json"
    previous_bytes = previous_path.read_bytes()
    previous_hash = hashlib.sha256(previous_bytes).hexdigest()
    if (PREVIOUS / "snapshot_manifest.sha256").read_text(encoding="ascii").split()[0] != previous_hash:
        raise SystemExit("v4 source snapshot sidecar mismatch")
    previous = json.loads(previous_bytes)
    for item in previous["members"]:
        member = PREVIOUS / item["snapshot_relative_path"]
        if not member.is_file() or member.stat().st_size != item["bytes"] or sha256(member) != item["sha256"]:
            raise SystemExit(f"v4 snapshot member failed replay: {item['snapshot_relative_path']}")

    if not SNAPSHOT.exists():
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
            raise SystemExit(f"refusing to replace a path outside the v5 snapshot project: {resolved_destination}")
        shutil.rmtree(destination)
        shutil.copytree(
            ROOT / relative, destination,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )
    ledger_source = ROOT / "results/validation/g4/auer2013/r3_common_adapter_attempts_v2.json"
    ledger_target = project / "results/validation/g4/auer2013/r3_common_adapter_attempts_v2.json"
    ledger_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ledger_source, ledger_target)

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
        "schema": "ddwmr-g4-auer-local-source-snapshot-v5",
        "status": "LOCAL_UNCOMMITTED_BLOCKED_PARTIAL_REVIEW_PACKAGE",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_git_revision": revision,
        "branch": branch,
        "worktree_status_at_snapshot": status,
        "source_tree_clean": not bool(status),
        "previous_snapshot_manifest_sha256": previous_hash,
        "previous_snapshot_member_count_verified": previous.get("member_count", len(previous["members"])),
        "active_common_adapter_profile": "validation/g4/r3_common_adapter_profile_v2.json",
        "native_r3_evaluator_reruns": 0,
        "matched_query_evaluations": 0,
        "auer_solver_available": False,
        "members": members,
        "manifest_hash_semantics": "SHA-256 over exact UTF-8 bytes of this indented sorted-key JSON plus one LF; manifest and sidecar are excluded from members.",
    }
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    (SNAPSHOT / "snapshot_manifest.json").write_bytes(manifest_bytes)
    manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
    (SNAPSHOT / "snapshot_manifest.sha256").write_text(
        f"{manifest_hash}  snapshot_manifest.json\n", encoding="ascii", newline="\n",
    )
    print(json.dumps({
        "snapshot_path": str(SNAPSHOT),
        "manifest_sha256": manifest_hash,
        "member_count": len(members),
        "native_r3_evaluator_reruns": 0,
        "matched_query_evaluations": 0,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
