"""Freeze the R3 pilot manifest after code and pilot profile are committed."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from validation.g2.evaluator import ROOT, R3_METHOD_ID
from validation.g2.hashing import HASH_PROTOCOL_ID, semantic_json_file_sha256, semantic_json_sha256
from validation.g2.provenance import (
    current_revision, git_blob_commitment, source_commitments, verify_commitment, worktree_status,
)


BENCHMARK = Path("validation/configs/benchmark_v1.json")
PILOT_R2 = Path("validation/configs/dev_pilot_r2_v1.json")
MANIFEST_R2 = Path("results/validation/g2/r2/development_manifest_r2_v1.json")
PILOT_R3 = Path("validation/configs/dev_pilot_r3_v1.json")
FULL_GRID_R3 = Path("results/validation/g2/r3/full_grid_continuation_manifest_r3_v1.json")
SPEC_LEDGER_R3 = Path("results/validation/g2/r3/specification_content_ledger_r3_v1.json")
MANIFEST_R3 = Path("results/validation/g2/r3/development_manifest_r3_v1.json")
PREEVAL_R3 = Path("results/validation/g2/r3/SHA256SUMS_PRE_EVAL_R3.json")

PRODUCER_PATHS = [
    "validation/g2/evaluator.py", "validation/g2/rational.py", "validation/g2/interval.py",
    "validation/g2/model.py", "validation/g2/hashing.py", "validation/g2/provenance.py",
    "validation/scripts/run_pilot_r3.py",
]
CHECKER_PATHS = [
    "validation/g2/checker.py", "validation/g2/rational.py", "validation/g2/interval.py",
    "validation/g2/model.py", "validation/g2/hashing.py", "validation/g2/provenance.py",
    "validation/scripts/verify_records_r3.py",
]


def load(path: Path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write_new(path: Path, value: dict) -> None:
    output = ROOT / path
    if output.exists():
        raise SystemExit(f"refusing to overwrite frozen R3 artifact: {path}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    if worktree_status():
        raise SystemExit("R3 manifest freeze requires a clean source tree")
    revision = current_revision()
    branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    if branch != "luna/g2-validation-v1":
        raise SystemExit(f"R3 manifest freeze is restricted to luna/g2-validation-v1; current branch is {branch!r}")
    benchmark = load(BENCHMARK)
    pilot = load(PILOT_R3)
    full_grid = load(FULL_GRID_R3)
    spec_ledger = load(SPEC_LEDGER_R3)
    source_r2 = load(MANIFEST_R2)
    if spec_ledger.get("specification_bundle_sha256") != pilot["profile"].get("specification_bundle_sha256"):
        raise SystemExit("specification bundle does not match the committed R3 profile")
    if semantic_json_sha256({key: value for key, value in spec_ledger.items() if key != "specification_bundle_sha256"}) != spec_ledger["specification_bundle_sha256"]:
        raise SystemExit("specification content ledger digest is invalid")
    if not all(verify_commitment(item) for item in spec_ledger["sources"]):
        raise SystemExit("an immutable specification Git-blob commitment did not verify")

    selected = source_r2["selected_query_ids"]
    original = source_r2["original_query_ids"]
    remaining = source_r2["not_run_query_ids"]
    if pilot["pilot_query_count"] != len(selected) or len(original) != 1944 or len(selected) != 216 or len(remaining) != 1728:
        raise SystemExit("R3 counts do not match the original frozen R2 query universe")
    if full_grid["selected_query_ids"] != remaining:
        raise SystemExit("conditional full-grid IDs are not the exact R2 NOT_RUN list")

    producer_sources = source_commitments(revision, PRODUCER_PATHS)
    checker_sources = source_commitments(revision, CHECKER_PATHS)
    input_blobs = {
        name: git_blob_commitment(revision, path)
        for name, path in {
            "benchmark_config": BENCHMARK.as_posix(),
            "pilot_config": PILOT_R3.as_posix(),
            "conditional_full_grid_manifest": FULL_GRID_R3.as_posix(),
            "specification_content_ledger": SPEC_LEDGER_R3.as_posix(),
        }.items()
    }
    input_hashes = {
        "hash_protocol_id": HASH_PROTOCOL_ID,
        "benchmark_config_semantic_sha256": semantic_json_file_sha256(ROOT / BENCHMARK),
        "pilot_config_semantic_sha256": semantic_json_file_sha256(ROOT / PILOT_R3),
        "conditional_full_grid_manifest_semantic_sha256": semantic_json_file_sha256(ROOT / FULL_GRID_R3),
        "specification_content_ledger_semantic_sha256": semantic_json_file_sha256(ROOT / SPEC_LEDGER_R3),
    }
    input_hashes["frozen_input_set_bundle_sha256"] = semantic_json_sha256(input_hashes)
    pilot_ids_digest = hashlib.sha256("\n".join(selected).encode("utf-8")).hexdigest()

    manifest = {
        "schema": "ddwmr-g2-development-manifest-r3-v1",
        "status": "IMMUTABLE_R3_INPUTS_FROZEN_BEFORE_EVALUATION; NOT_LOCKED",
        "method_id": R3_METHOD_ID,
        "distance_method_id": pilot["profile"]["distance_method_id"],
        "distance_rounding_precision_bits": pilot["profile"]["distance_rounding_precision_bits"],
        "hash_protocol_id": HASH_PROTOCOL_ID,
        "freeze_source_commit": revision,
        "branch": branch,
        "generator_git_blob_commitment": git_blob_commitment(revision, "validation/scripts/freeze_r3_manifest.py"),
        "benchmark_spec_path": "research/benchmarks/G2_USEFULNESS_BENCHMARK_SPEC_v1.md",
        "finite_evaluator_spec_path": "research/theorem_notes/G2_FINITE_EVALUATOR_SPEC_v1.md",
        "addendum_path": "docs/LUNA_G2_DISTANCE_ADDENDUM_R3_v1.md",
        "benchmark_config_path": BENCHMARK.as_posix(),
        "pilot_config_path": PILOT_R3.as_posix(),
        "conditional_full_grid_manifest_path": FULL_GRID_R3.as_posix(),
        "specification_content_ledger_path": SPEC_LEDGER_R3.as_posix(),
        "specification_content_ledger": spec_ledger,
        "specification_bundle_sha256": spec_ledger["specification_bundle_sha256"],
        "input_blob_commitments": input_blobs,
        "input_hashes": input_hashes,
        "profile": pilot["profile"],
        "profile_semantic_sha256": semantic_json_sha256(pilot["profile"]),
        "producer_source_commitments": producer_sources,
        "checker_source_commitments": checker_sources,
        "original_query_count_per_method_profile": len(original),
        "pilot_query_count": len(selected),
        "conditional_remaining_query_count": len(remaining),
        "original_query_ids": original,
        "selected_query_ids": selected,
        "not_run_query_ids_before_conditional_continuation": remaining,
        "selected_query_ids_sha256_lf": pilot_ids_digest,
        "selection_rule": source_r2["selection_rule"],
        "selection_unchanged_from_r2": selected == source_r2["selected_query_ids"],
        "physics_query_universe_unchanged": original == source_r2["original_query_ids"],
        "aggregation": source_r2["aggregation"],
        "conditional_continuation_rule": full_grid["rule_frozen_before_pilot"],
        "outputs": {
            "pilot_records": "results/validation/g2/r3/dev_pilot_records_r3_v1.jsonl",
            "pilot_run_metadata": "results/validation/g2/r3/dev_pilot_run_metadata_r3_v1.json",
            "pilot_checker_report": "results/validation/g2/r3/dev_pilot_record_check_r3_v1.json",
            "pilot_summary": "results/validation/g2/r3/dev_pilot_summary_r3_v1.json",
            "query_transitions": "results/validation/g2/r3/r2_to_r3_query_transitions_r3_v1.jsonl",
            "action_group_summary": "results/validation/g2/r3/action_group_summary_r3_v1.json",
            "r2_compatibility_check": "results/validation/g2/r3/r2_compatibility_record_check_r3_v1.json",
            "pilot_hash_ledger": "results/validation/g2/r3/SHA256SUMS_PILOT_R3.json",
            "final_hash_ledger": "results/validation/g2/r3/SHA256SUMS_RESULTS_R3.json",
        },
    }
    write_new(MANIFEST_R3, manifest)
    preeval = {
        "schema": "ddwmr-g2-preevaluation-provenance-r3-v1",
        "hash_protocol_id": HASH_PROTOCOL_ID,
        "frozen_before_any_r3_evaluator_output": True,
        "freeze_source_commit": revision,
        "specification_bundle_sha256": spec_ledger["specification_bundle_sha256"],
        "input_hashes": input_hashes,
        "manifest_semantic_sha256": semantic_json_file_sha256(ROOT / MANIFEST_R3),
        "profile_semantic_sha256": semantic_json_sha256(pilot["profile"]),
        "conditional_full_grid_manifest_semantic_sha256": input_hashes["conditional_full_grid_manifest_semantic_sha256"],
        "selected_query_ids_sha256_lf": pilot_ids_digest,
        "selected_query_count": len(selected),
        "original_query_count": len(original),
        "not_run_query_count_before_conditional_continuation": len(remaining),
        "producer_source_commitments": producer_sources,
        "checker_source_commitments": checker_sources,
        "input_blob_commitments": input_blobs,
        "hash_semantics": "SHA-256 over canonical compact sorted-key UTF-8 JSON; source/spec Markdown uses SHA-256 over immutable Git blob bytes.",
    }
    write_new(PREEVAL_R3, preeval)
    print(json.dumps({
        "schema": "ddwmr-g2-r3-frozen-manifest-v1",
        "freeze_source_commit": revision,
        "method_id": R3_METHOD_ID,
        "selected": len(selected), "original": len(original), "conditional_remaining": len(remaining),
        "pilot_config_semantic_sha256": input_hashes["pilot_config_semantic_sha256"],
        "manifest_semantic_sha256": semantic_json_file_sha256(ROOT / MANIFEST_R3),
        "specification_bundle_sha256": spec_ledger["specification_bundle_sha256"],
        "all_specification_blob_commitments_verified": True,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
