"""Freeze the R2 Auer preparation package without evaluating benchmark queries."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/validation/g4/auer2013"
SNAPSHOT_V1 = BASE / "source_snapshot_v1"
SNAPSHOT = BASE / "source_snapshot_v2"
WSL_PROBE = BASE / "wsl_probe"

OVERLAY_FILES = [
    "AGENTS.md",
    "docs/CODEX_TO_LUNA_G4_AUER_BASELINE_R2.md",
    "docs/CODEX_TO_LUNA_G4_AUER_PREFLIGHT_v1.md",
    "docs/reviews/CODEX_G4_AUER_PREFLIGHT_REVIEW.md",
    "docs/reviews/LUNA_TO_CODEX_G4_AUER_PREFLIGHT_FULL_HANDOFF.md",
    "docs/reviews/G4_AUER_SOURCE_AND_APPLICABILITY_v1.md",
    "docs/reviews/G4_AUER_SOURCE_AND_APPLICABILITY_v2.md",
    "research_context/MASTER_RESEARCH_CONTEXT_v2.md",
    "research_context/DECISION_LOG.md",
    "research_context/LITERATURE_MATRIX.md",
    "research_context/REVIEW_GATE.md",
    "research/theorem_notes/G4_AUER_BASELINE_CONTRACT_v1.md",
    "research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v1.md",
    "research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v2.md",
    "validation/configs/benchmark_v1.json",
    "validation/g2/__init__.py",
    "validation/g4/__init__.py",
    "validation/g4/common_tube.py",
    "validation/g4/verify_common_tube.py",
    "validation/scripts/create_auer_source_snapshot.py",
    "validation/scripts/create_auer_source_snapshot_v2.py",
    "validation/scripts/generate_auer_candidate_manifest.py",
    "validation/scripts/version_auer_candidate_manifest_v2.py",
    "results/validation/g2/r2/development_manifest_r2_v1.json",
    "results/validation/g4/auer2013/auer_matched_candidate_manifest_v1.json",
    "results/validation/g4/auer2013/auer_matched_candidate_manifest_v2.json",
    "results/validation/g4/auer2013/auer_seed_build_attempt.json",
    "results/validation/g4/auer2013/auer_seed_full_build_disposition_v1.json",
    "results/validation/g4/auer2013/auer_seed_syntax_build.log",
    "results/validation/g4/auer2013/clip_preflight_checks_v1.json",
    "results/validation/g4/auer2013/common_tube_preflight_v2.json",
    "results/validation/g4/auer2013/preflight_run_metadata.json",
    "results/validation/g4/auer2013/reference_eq34_reproduction_v1.json",
    "results/validation/g4/auer2013/source_integrity_post_run.json",
    "results/validation/g4/auer2013/source_integrity_pre_run.json",
]

COPY_DIRECTORIES = [
    "validation/g2",
    "validation/baselines/auer2013",
    "external/valencia-basic",
    "research/third_party/auer2013",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_v1() -> dict[str, Any]:
    manifest_path = SNAPSHOT_V1 / "snapshot_manifest.json"
    sidecar_path = SNAPSHOT_V1 / "snapshot_manifest.sha256"
    if not manifest_path.is_file() or not sidecar_path.is_file():
        raise SystemExit("v1 source snapshot and sidecar are required")
    manifest_bytes = manifest_path.read_bytes()
    manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
    if sidecar_path.read_text(encoding="ascii").split()[0] != manifest_hash:
        raise SystemExit("v1 source snapshot manifest hash does not match its sidecar")
    manifest = json.loads(manifest_bytes)
    if manifest.get("member_count") != len(manifest.get("members", [])):
        raise SystemExit("v1 source snapshot member count is inconsistent")
    for item in manifest["members"]:
        path = SNAPSHOT_V1 / "project" / item["repository_relative_path"]
        if not path.is_file() or path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            raise SystemExit(f"v1 source snapshot member mismatch: {item['repository_relative_path']}")
    return {"manifest_sha256": manifest_hash, "member_count": manifest["member_count"]}


def copy_file(relative: str, destination_root: Path) -> None:
    source = ROOT / relative
    if not source.is_file():
        raise SystemExit(f"required R2 snapshot input missing: {relative}")
    destination = destination_root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def build_environment(project_path: Path) -> dict[str, Any]:
    probe_path = project_path / "environment/wsl_probe/bin/auer_bias_rounding_probe"
    legacy_path = project_path / "environment/wsl_probe/bin/ValEncIA-IVP_0.92_2e-smooth"
    if not probe_path.is_file() or not legacy_path.is_file():
        raise SystemExit("expected WSL probe and legacy smooth binary are missing")
    return {
        "schema": "ddwmr-g4-auer-r2-build-environment-v1",
        "scope": "candidate_dependency_build_and_legacy_smooth_example_only",
        "os": "WSL2 Ubuntu 24.04.3 LTS, x86-64",
        "kernel": "Linux 6.18.33.2-microsoft-standard-WSL2",
        "compiler": "GCC/G++ 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04.1)",
        "libc": "glibc 2.39 (Ubuntu 2.39-0ubuntu8.9)",
        "make": "GNU Make 4.3",
        "dependencies": {
            "PROFIL_BIAS": "2.0.8, project-local build/install",
            "FADBAD_plus_plus": "1.4",
            "VALENCIA_seed": "0.92_2e, commit d1a09ceb3f68deb40357bdc89944b28997e9fb30",
        },
        "flags": ["-O2", "-frounding-math", "-fno-fast-math", "-ffp-contract=off"],
        "additional_link_library_required": "-llr",
        "binary_hashes": {
            "bias_rounding_probe_sha256": sha256(probe_path),
            "valencia_smooth_legacy_sha256": sha256(legacy_path),
        },
        "bias_checks": {
            "finite_check_count": 19,
            "arithmetic": "addition, multiplication, and division against exact rational bounds",
            "transcendentals": "sine/cosine at seven binary64 points and over [-0.25,0.25], checked against rational Taylor enclosures",
            "limit": "finite checks only; no global proof of glibc/libm error bounds or all-input directed transcendental rounding",
        },
        "profil_make_check": "2/2 passed (TBias and TBiasF); narrow dependency smoke check, not the application solver",
        "application_solver_status": "NOT_BUILT; no Auer piecewise DDWMR solver, Picard inclusion replay, or full-time proof record",
    }


def main() -> int:
    if SNAPSHOT.exists():
        raise SystemExit(f"refusing to overwrite existing snapshot: {SNAPSHOT}")
    if not WSL_PROBE.is_dir():
        raise SystemExit(f"required project-local WSL build is missing: {WSL_PROBE}")
    v1 = validate_v1()

    SNAPSHOT.mkdir(parents=True)
    project = SNAPSHOT / "project"
    shutil.copytree(SNAPSHOT_V1 / "project", project)

    # Bring forward current equation adapters and their complete shared arithmetic/model dependency tree.
    for relative in COPY_DIRECTORIES:
        source = ROOT / relative
        if not source.is_dir():
            raise SystemExit(f"required source directory missing: {relative}")
        destination = project / relative
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for relative in OVERLAY_FILES:
        copy_file(relative, project)

    # Include all local build products and logs, without installing software globally.
    shutil.copytree(WSL_PROBE, SNAPSHOT / "environment/wsl_probe", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    env = build_environment(SNAPSHOT)
    env_path = SNAPSHOT / "environment/build_environment.json"
    env_path.write_text(json.dumps(env, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    runs = SNAPSHOT / "runs"
    runs.mkdir()
    run_files = [
        BASE / "auer_seed_build_attempt.json",
        BASE / "auer_seed_full_build_disposition_v1.json",
        BASE / "auer_seed_syntax_build.log",
        BASE / "clip_preflight_checks_v1.json",
        BASE / "common_tube_preflight_v2.json",
        BASE / "preflight_run_metadata.json",
        BASE / "reference_eq34_reproduction_v1.json",
        BASE / "source_integrity_post_run.json",
        BASE / "source_integrity_pre_run.json",
        BASE / "auer_matched_candidate_manifest_v1.json",
        BASE / "auer_matched_candidate_manifest_v2.json",
    ]
    for source in run_files:
        if not source.is_file():
            raise SystemExit(f"required recorded run artifact missing: {source.name}")
        shutil.copy2(source, runs / source.name)

    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=True,
                            capture_output=True, text=True).stdout.strip()
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                              capture_output=True, text=True).stdout.strip()
    status = subprocess.run(["git", "status", "--short"], cwd=ROOT, check=True,
                            capture_output=True, text=True).stdout.splitlines()
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
        "schema": "ddwmr-g4-auer-local-source-snapshot-v2",
        "status": "LOCAL_UNCOMMITTED_BLOCKED_PARTIAL_REVIEW_PACKAGE",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_git_revision": revision,
        "branch": branch,
        "worktree_status_at_snapshot": status,
        "source_tree_clean": not bool(status),
        "v1_snapshot_sha256": v1["manifest_sha256"],
        "v1_snapshot_member_count_verified": v1["member_count"],
        "member_count": len(members),
        "matched_query_evaluations": 0,
        "auer_solver_available": False,
        "members": members,
        "manifest_hash_semantics": "SHA-256 over exact UTF-8 bytes of this indented, sorted-key JSON plus one LF; manifest excludes its own file and sidecar.",
    }
    manifest_path = SNAPSHOT / "snapshot_manifest.json"
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    manifest_path.write_bytes(manifest_bytes)
    manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
    (SNAPSHOT / "snapshot_manifest.sha256").write_text(
        f"{manifest_hash}  snapshot_manifest.json\n", encoding="ascii", newline="\n",
    )
    print(json.dumps({
        "snapshot_path": str(SNAPSHOT),
        "manifest_sha256": manifest_hash,
        "member_count": len(members),
        "base_git_revision": revision,
        "branch": branch,
        "source_tree_clean": not bool(status),
        "matched_query_evaluations": 0,
        "auer_solver_available": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
