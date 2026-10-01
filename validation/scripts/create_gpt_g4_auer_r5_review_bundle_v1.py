"""Create the source-backed, non-executable GPT G4 Auer R5 review package.

The bundle contains the proof-critical frozen v11 source and the complete R4/R5
output registries. It does not pretend to contain every member of either full
source snapshot; their manifests are included for provenance.
"""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/validation/g4/auer2013"
R5 = BASE / "r5_composition_replay_v1"
V11_PROJECT = R5 / "source_snapshot_v11/project"
OUT = ROOT / "docs/reviews/GPT_G4_AUER_R5_SOURCE_REVIEW_BUNDLE_v1.zip"
MANIFEST = ROOT / "docs/reviews/GPT_G4_AUER_R5_SOURCE_REVIEW_BUNDLE_MANIFEST_v1.json"
SIDECAR = ROOT / "docs/reviews/GPT_G4_AUER_R5_SOURCE_REVIEW_BUNDLE_v1.sha256"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    if any(path.exists() for path in (OUT, MANIFEST, SIDECAR)):
        raise SystemExit("refusing to overwrite an existing GPT review bundle")

    r4_manifest = json.loads((BASE / "r4_output_artifact_manifest_v1.json").read_text(encoding="utf-8"))
    r5_registry = json.loads((R5 / "r5_artifact_manifest_v1.json").read_text(encoding="utf-8"))
    if len(r4_manifest["artifacts"]) != 34 or len(r5_registry["artifacts"]) != 88:
        raise SystemExit("unexpected R4 or R5 artifact count")

    entries: dict[str, Path] = {}

    def add(path: Path, arcname: str | None = None) -> None:
        if not path.is_file():
            raise SystemExit(f"missing bundle input: {path}")
        name = arcname or path.relative_to(ROOT).as_posix()
        if name in entries and entries[name] != path:
            raise SystemExit(f"conflicting bundle member: {name}")
        entries[name] = path

    static = [
        "AGENTS.md",
        "research_context/MASTER_RESEARCH_CONTEXT_v2.md",
        "research_context/DECISION_LOG.md",
        "research_context/LITERATURE_MATRIX.md",
        "research_context/REVIEW_GATE.md",
        "docs/GPT_G4_AUER_R5_SOURCE_REVIEW_REQUEST.md",
        "docs/reviews/GPT_TO_CODEX_G4_AUER_R2_STRATEGY_FULL_HANDOFF.md",
        "docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md",
        "docs/reviews/LUNA_TO_CODEX_G4_AUER_R4_IVP_CORE_FULL_HANDOFF.md",
        "docs/reviews/CODEX_G4_AUER_R4_IVP_CORE_REVIEW.md",
        "docs/reviews/LUNA_TO_CODEX_G4_AUER_R5_COMPOSITION_REPLAY_FULL_HANDOFF.md",
        "docs/reviews/CODEX_G4_AUER_R5_COMPOSITION_REPLAY_REVIEW.md",
        "research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v2.md",
        "research/theorem_notes/G4_AUER_BASELINE_CONTRACT_v1.md",
        "research/third_party/auer2013/auer-kiel-rauh-2013.pdf",
        "research/third_party/auer2013/references/rauh-auer-2011-valencia.pdf",
        "external/valencia-basic/free-source/ValEncIA/ValEncIA-IVP_0.92_2e.cpp",
        "results/validation/g4/auer2013/r4_output_artifact_manifest_v1.json",
        "results/validation/g4/auer2013/r5_composition_replay_v1/r5_artifact_manifest_v1.json",
        "results/validation/g4/auer2013/r5_composition_replay_v1/r5_artifact_manifest_v1.sha256",
        "results/validation/g4/auer2013/source_snapshot_v10/snapshot_manifest.sha256",
        "results/validation/g4/auer2013/r5_composition_replay_v1/source_snapshot_v11/snapshot_manifest.sha256",
        "results/validation/g4/auer2013/auer_matched_candidate_manifest_v2.json",
        "validation/scripts/create_gpt_g4_auer_r5_review_bundle_v1.py",
    ]
    for relative in static:
        add(ROOT / relative)

    for item in r4_manifest["artifacts"]:
        add(BASE / item["path"])
    for item in r5_registry["artifacts"]:
        add(ROOT / item["path"])

    frozen_files = [
        *sorted((V11_PROJECT / "validation/baselines/auer2013").glob("*.py")),
        *sorted((V11_PROJECT / "validation/g2").glob("*.py")),
        *sorted((V11_PROJECT / "validation/g4").glob("*.py")),
        V11_PROJECT / "validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v2.json",
        V11_PROJECT / "validation/baselines/auer2013/analytic_branch_crossing_fixture_v1.json",
        V11_PROJECT / "validation/baselines/auer2013/auer_r4_ddwmr_single_case_input_v1.json",
        V11_PROJECT / "validation/baselines/auer2013/small_case_resource_profile_v2.json",
        V11_PROJECT / "validation/baselines/auer2013/R4_EXECUTION_PROTOCOL.md",
        V11_PROJECT / "validation/baselines/auer2013/R5_COMPOSITION_REPLAY_PROTOCOL_v1.md",
        V11_PROJECT / "validation/configs/benchmark_v1.json",
        V11_PROJECT / "validation/configs/auer_r5_composition_replay_profile_v1.json",
        V11_PROJECT / "validation/scripts/verify_auer_composition_replay_v1.py",
        V11_PROJECT / "validation/scripts/run_auer_composition_mutation_trials_v1.py",
        V11_PROJECT / "validation/scripts/create_auer_source_snapshot_v10.py",
        V11_PROJECT / "validation/scripts/create_auer_source_snapshot_v11.py",
        V11_PROJECT / "validation/scripts/verify_auer_source_snapshot_v10.py",
        V11_PROJECT / "validation/scripts/verify_auer_source_snapshot_v11.py",
        V11_PROJECT / "docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md",
    ]
    for path in frozen_files:
        add(path, "frozen_v11_project/" + path.relative_to(V11_PROJECT).as_posix())

    metadata = {
        "schema": "ddwmr-g4-auer-r5-gpt-source-review-bundle-v1",
        "purpose": "Source-level independent scientific review of one proof-backed Auer R4/R5 case; no matched batch",
        "base_git_revision": "aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46",
        "r4_output_artifact_manifest_sha256": digest(BASE / "r4_output_artifact_manifest_v1.json"),
        "r5_artifact_registry_sha256": digest(R5 / "r5_artifact_manifest_v1.json"),
        "v10_snapshot_manifest_sha256": digest(BASE / "source_snapshot_v10/snapshot_manifest.json"),
        "v11_snapshot_manifest_sha256": digest(R5 / "source_snapshot_v11/snapshot_manifest.json"),
        "full_snapshot_members_omitted": True,
        "scope_note": "The bundle contains all R4/R5 output-registry artifacts and proof-critical frozen v11 source, plus v10/v11 manifests. It does not contain every v10/v11 snapshot member; local Codex audit found 720/720 and 726/726 member hashes matched.",
        "entries": [
            {"path": name, "bytes": path.stat().st_size, "sha256": digest(path)}
            for name, path in sorted(entries.items())
        ],
    }
    manifest_bytes = (json.dumps(metadata, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    MANIFEST.write_bytes(manifest_bytes)

    fixed_time = (2026, 10, 1, 0, 0, 0)
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, path in sorted(entries.items()):
            info = zipfile.ZipInfo(name, fixed_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        info = zipfile.ZipInfo("bundle_manifest.json", fixed_time)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, manifest_bytes, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    SIDECAR.write_text(f"{digest(OUT)}  {OUT.name}\n", encoding="ascii", newline="\n")
    print(json.dumps({"zip": str(OUT), "zip_sha256": digest(OUT), "entries": len(entries) + 1,
                      "manifest_sha256": digest(MANIFEST), "bytes": OUT.stat().st_size}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
