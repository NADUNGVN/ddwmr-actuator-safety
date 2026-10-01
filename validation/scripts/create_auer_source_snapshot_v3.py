"""Freeze the blocked Auer reconstruction contract and archived-R3 fixture inputs.

This creates a new local review snapshot without editing source_snapshot_v1/v2
or rerunning any R3 evaluator. It does not claim that an Auer solver exists.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/validation/g4/auer2013"
PREVIOUS = BASE / "source_snapshot_v2"
SNAPSHOT = BASE / "source_snapshot_v3"

OVERLAY_FILES = [
    "AGENTS.md",
    "docs/CODEX_TO_LUNA_G4_AUER_R3_PROOF_BACKED_SINGLE_CASE.md",
    "docs/GPT_G4_AUER_R2_STRATEGY_REVIEW_REQUEST.md",
    "docs/reviews/GPT_TO_CODEX_G4_AUER_R2_STRATEGY_FULL_HANDOFF.md",
    "docs/reviews/CODEX_G4_AUER_R2_STRATEGY_DISPOSITION.md",
    "docs/reviews/LUNA_TO_CODEX_G4_AUER_BASELINE_R2_FULL_HANDOFF.md",
    "docs/reviews/CODEX_G4_AUER_BASELINE_R2_REVIEW.md",
    "docs/reviews/G4_AUER_METHOD_CONTRACT_v1.md",
    "docs/reviews/G4_AUER_SOURCE_AND_APPLICABILITY_v2.md",
    "research/theorem_notes/G4_AUER_BASELINE_CONTRACT_v1.md",
    "research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v2.md",
    "research_context/MASTER_RESEARCH_CONTEXT_v2.md",
    "research_context/DECISION_LOG.md",
    "research_context/LITERATURE_MATRIX.md",
    "research_context/REVIEW_GATE.md",
    "validation/baselines/auer2013/ARITHMETIC_BACKEND.md",
    "validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v1.json",
    "validation/baselines/auer2013/small_case_resource_profile_v1.json",
]

OVERLAY_DIRECTORIES = [
    "validation/g2",
    "validation/g4",
    "validation/baselines/auer2013",
    "validation/configs",
    "validation/scripts",
    "external/valencia-basic",
    "research/third_party/auer2013",
]

R3_ARCHIVE_INPUTS = [
    "results/validation/g2/r3/SHA256SUMS_PRE_EVAL_R3.json",
    "results/validation/g2/r3/conditional_full_grid_archive_manifest_r3_v1.json",
    "results/validation/g2/r3/conditional_full_grid_run_metadata_r3_v1.json",
    "results/validation/g2/r3/conditional_full_grid_records_r3_v1.jsonl.gz",
    "results/validation/g2/r3/development_manifest_r3_v1.json",
    "results/validation/g2/r3/full_grid_continuation_manifest_r3_v1.json",
    "results/validation/g2/r3/specification_content_ledger_r3_v1.json",
    "results/validation/g2/r3/full_grid_summary_r3_v1.json",
    "results/validation/g2/r3/full_grid_record_check_r3_v1.json",
]

FREEZE_AND_BLOCKER_INPUTS = [
    "results/validation/g4/auer2013/small_case_freeze_record_v1.json",
    "results/validation/g4/auer2013/auer_single_case_preflight_blocker_v1.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_file(relative: str, destination_root: Path) -> None:
    source = ROOT / relative
    if not source.is_file():
        raise SystemExit(f"snapshot input missing: {relative}")
    destination = destination_root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def remove_snapshot_subtree(path: Path, snapshot_project: Path) -> None:
    resolved_root = snapshot_project.resolve()
    resolved_path = path.resolve()
    if resolved_root not in resolved_path.parents:
        raise SystemExit(f"refusing to replace a path outside the snapshot project: {resolved_path}")

    def retry_writable(function, name, exc):
        os.chmod(name, stat.S_IWRITE)
        function(name)

    shutil.rmtree(resolved_path, onexc=retry_writable)


def main() -> None:
    if SNAPSHOT.exists():
        if (SNAPSHOT / "snapshot_manifest.json").exists():
            raise SystemExit(f"refusing to overwrite an existing completed snapshot: {SNAPSHOT}")
        if not all((SNAPSHOT / item).is_dir() for item in ("project", "environment", "runs")):
            raise SystemExit(f"existing snapshot path is not a recognized resumable partial: {SNAPSHOT}")
    previous_manifest_path = PREVIOUS / "snapshot_manifest.json"
    previous_sidecar_path = PREVIOUS / "snapshot_manifest.sha256"
    if not previous_manifest_path.is_file() or not previous_sidecar_path.is_file():
        raise SystemExit("the prior v2 snapshot and sidecar are required")
    previous_bytes = previous_manifest_path.read_bytes()
    previous_hash = hashlib.sha256(previous_bytes).hexdigest()
    if previous_sidecar_path.read_text(encoding="ascii").split()[0] != previous_hash:
        raise SystemExit("v2 source snapshot manifest sidecar mismatch")
    previous = json.loads(previous_bytes)
    for item in previous["members"]:
        path = PREVIOUS / item["snapshot_relative_path"]
        if not path.is_file() or path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            raise SystemExit(f"v2 snapshot member failed replay: {item['snapshot_relative_path']}")

    if not SNAPSHOT.exists():
        SNAPSHOT.mkdir(parents=True)
        shutil.copytree(
            PREVIOUS / "project", SNAPSHOT / "project",
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )
        shutil.copytree(PREVIOUS / "environment", SNAPSHOT / "environment")
        shutil.copytree(PREVIOUS / "runs", SNAPSHOT / "runs")
    project = SNAPSHOT / "project"
    for relative in OVERLAY_DIRECTORIES:
        source = ROOT / relative
        destination = project / relative
        if destination.exists():
            remove_snapshot_subtree(destination, project)
        shutil.copytree(source, destination, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    for relative in OVERLAY_FILES:
        copy_file(relative, project)
    for relative in R3_ARCHIVE_INPUTS:
        copy_file(relative, project)
    for relative in FREEZE_AND_BLOCKER_INPUTS:
        copy_file(relative, project)

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
        "schema": "ddwmr-g4-auer-local-source-snapshot-v3",
        "status": "LOCAL_UNCOMMITTED_BLOCKED_PARTIAL_REVIEW_PACKAGE",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_git_revision": revision,
        "branch": branch,
        "worktree_status_at_snapshot": status,
        "source_tree_clean": not bool(status),
        "previous_snapshot_manifest_sha256": previous_hash,
        "previous_snapshot_member_count_verified": previous["member_count"],
        "member_count": len(members),
        "matched_query_evaluations": 0,
        "r3_native_evaluator_reruns": 0,
        "auer_solver_available": False,
        "auer_analytic_ivp_runs": 0,
        "auer_ddwmr_ivp_runs": 0,
        "valencia_source_patch": "NONE; pinned source retained unmodified",
        "members": members,
        "manifest_hash_semantics": "SHA-256 over exact UTF-8 bytes of this indented sorted-key JSON plus one LF; the manifest and sidecar are excluded from members.",
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
        "auer_solver_available": False,
        "r3_native_evaluator_reruns": 0,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
