"""Create a hash-bound local source snapshot for Auer preflight runs."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "results/validation/g4/auer2013/source_snapshot_v1"
FILES = [
    "AGENTS.md",
    "docs/CODEX_TO_LUNA_G4_AUER_PREFLIGHT_v1.md",
    "docs/reviews/GPT_TO_CODEX_G2_VALIDATION_R3_SCIENTIFIC_REVIEW_FULL_HANDOFF.md",
    "docs/reviews/CODEX_G2_VALIDATION_R3_REVIEW.md",
    "docs/reviews/G4_MATCHED_PRIOR_ART_COMPARISON_v1.md",
    "docs/reviews/G4_AUER_SOURCE_AND_APPLICABILITY_v1.md",
    "research_context/MASTER_RESEARCH_CONTEXT_v2.md",
    "research_context/DECISION_LOG.md",
    "research_context/LITERATURE_MATRIX.md",
    "research_context/REVIEW_GATE.md",
    "research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md",
    "research/theorem_notes/G2_FINITE_EVALUATOR_SPEC_v1.md",
    "research/theorem_notes/G4_AUER_BASELINE_CONTRACT_v1.md",
    "research/benchmarks/G2_USEFULNESS_BENCHMARK_SPEC_v1.md",
    "research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v1.md",
    "validation/configs/benchmark_v1.json",
    "validation/scripts/generate_auer_candidate_manifest.py",
    "validation/scripts/create_auer_source_snapshot.py",
    "results/validation/g2/r2/development_manifest_r2_v1.json",
]
DIRECTORIES = [
    "validation/g2",
    "validation/baselines/auer2013",
    "external/valencia-basic",
    "research/third_party/auer2013",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if SNAPSHOT.exists():
        raise SystemExit(f"refusing to overwrite existing snapshot: {SNAPSHOT}")
    project = SNAPSHOT / "project"
    project.mkdir(parents=True)
    for rel in FILES:
        source = ROOT / rel
        if not source.is_file():
            raise SystemExit(f"required snapshot input missing: {rel}")
        destination = project / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    for rel in DIRECTORIES:
        source = ROOT / rel
        if not source.is_dir():
            raise SystemExit(f"required snapshot directory missing: {rel}")
        shutil.copytree(source, project / rel)

    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=True,
                            capture_output=True, text=True).stdout.strip()
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                              capture_output=True, text=True).stdout.strip()
    status = subprocess.run(["git", "status", "--short"], cwd=ROOT,
                            check=True, capture_output=True, text=True).stdout.splitlines()
    members = []
    for path in sorted(project.rglob("*")):
        if path.is_file():
            rel = path.relative_to(project).as_posix()
            members.append({
                "repository_relative_path": rel,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            })
    manifest = {
        "schema": "ddwmr-g4-auer-local-source-snapshot-v1",
        "status": "LOCAL_UNCOMMITTED_SNAPSHOT",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_git_revision": revision,
        "branch": branch,
        "worktree_status_at_snapshot": status,
        "source_tree_clean": not bool(status),
        "member_count": len(members),
        "members": members,
        "manifest_hash_semantics": "SHA-256 over exact UTF-8 bytes of this indented, sorted-key JSON plus one LF; manifest excludes its own file and sidecar.",
    }
    manifest_path = SNAPSHOT / "snapshot_manifest.json"
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    manifest_path.write_bytes(manifest_bytes)
    (SNAPSHOT / "snapshot_manifest.sha256").write_text(
        f"{hashlib.sha256(manifest_bytes).hexdigest()}  snapshot_manifest.json\n",
        encoding="ascii", newline="\n",
    )
    (SNAPSHOT / "runs").mkdir()
    print(json.dumps({
        "snapshot_path": str(SNAPSHOT),
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "member_count": len(members),
        "base_git_revision": revision,
        "branch": branch,
        "source_tree_clean": not bool(status),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
