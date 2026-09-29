#!/usr/bin/env python3
"""Freeze R2 profile and unchanged pilot IDs with semantic JSON hashes."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from validation.g2.evaluator import ROOT
from validation.g2.hashing import HASH_PROTOCOL_ID, semantic_json_file_sha256


BENCHMARK = Path("validation/configs/benchmark_v1.json")
V1_PILOT = Path("validation/configs/dev_pilot_v1.json")
PILOT_R2 = Path("validation/configs/dev_pilot_r2_v1.json")
FIXTURE_R2 = Path("validation/configs/g2_proof_pipeline_fixture_r2_v1.json")
MANIFEST_V1 = Path("results/validation/g2/development_manifest_v1.json")
MANIFEST_R2 = Path("results/validation/g2/r2/development_manifest_r2_v1.json")
PREEVAL_R2 = Path("results/validation/g2/r2/SHA256SUMS_PRE_EVAL_R2.json")


def load(relative: Path):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_new(relative: Path, value: dict) -> None:
    path = ROOT / relative
    if path.exists():
        raise SystemExit(f"refusing to overwrite frozen R2 input: {relative}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true", help="validate committed R2 inputs without rewriting")
    args = parser.parse_args()
    old_pilot = load(V1_PILOT)
    old_manifest = load(MANIFEST_V1)
    fixture = load(FIXTURE_R2)
    generator_blob = subprocess.run(
        ["git", "rev-parse", f"HEAD:{Path(__file__).relative_to(ROOT).as_posix()}"],
        cwd=ROOT, check=True, text=True, capture_output=True,
    ).stdout.strip()
    try:
        source_base_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True,
        ).stdout.strip()
    except subprocess.CalledProcessError as exc:
        raise SystemExit("R2 freeze requires an immutable committed source revision") from exc

    pilot_r2 = json.loads(json.dumps(old_pilot))
    pilot_r2["schema"] = "ddwmr-g2-development-pilot-r2-v1"
    pilot_r2["status"] = "FROZEN_R2_DEVELOPMENT_ONLY_NOT_LOCKED"
    pilot_r2["hash_protocol_id"] = HASH_PROTOCOL_ID
    pilot_r2["profile"]["id"] = "DEV_FALLBACK_N1_PILOT_R2_BITS16384_V1"
    pilot_r2["profile"]["max_rational_bits"] = 16384
    pilot_r2["profile"]["resource_diagnostic_schema"] = "ddwmr-g2-resource-diagnostic-v1"
    pilot_r2["profile"]["reason_for_cap"] = (
        "One predeclared bounded diagnostic profile after the radius correctness fix: same 216 original IDs, "
        "physics, scenes, actions, Taylor settings, operation cap and 15-second wall cap as v1; only the "
        "intermediate rational-bit cap is set to 16384 to identify whether completed safety margins can be "
        "reached and to capture the first resource stage. This is one finite attempt, not iterative cap tuning, "
        "not a locked comparison, and not a safety justification for the cap."
    )
    benchmark_hash = semantic_json_file_sha256(ROOT / BENCHMARK)
    fixture_hash = semantic_json_file_sha256(ROOT / FIXTURE_R2)

    manifest = {
        "schema": "ddwmr-g2-development-manifest-r2-v1",
        "hash_protocol_id": HASH_PROTOCOL_ID,
        "status": "IMMUTABLE_R2_INPUTS_FROZEN_BEFORE_EVALUATION; NOT_LOCKED",
        "source_base_commit": source_base_commit,
        "generator_git_blob": generator_blob,
        "benchmark_spec": old_manifest["benchmark_spec"],
        "benchmark_config": BENCHMARK.as_posix(),
        "pilot_config": PILOT_R2.as_posix(),
        "proof_pipeline_fixture": FIXTURE_R2.as_posix(),
        "benchmark_config_semantic_sha256": benchmark_hash,
        "pilot_config_semantic_sha256": None,
        "proof_fixture_semantic_sha256": fixture_hash,
        "profile": pilot_r2["profile"],
        "original_query_count_per_method_profile": old_manifest["original_query_count_per_method_profile"],
        "selected_query_count": old_manifest["selected_query_count"],
        "not_run_query_count": old_manifest["not_run_query_count"],
        "original_query_ids": old_manifest["original_query_ids"],
        "selected_query_ids": old_manifest["selected_query_ids"],
        "not_run_query_ids": old_manifest["not_run_query_ids"],
        "selection_rule": old_manifest["profile"]["selection_rule"],
        "selection_unchanged_from_v1": True,
        "aggregation": old_manifest["aggregation"],
        "disposition": "Correctness-corrected bounded development diagnostic only; no held-out claim, external baseline or G2/G4 promotion.",
    }
    if args.verify:
        stored_pilot = load(PILOT_R2)
        stored_manifest = load(MANIFEST_R2)
        ledger = load(PREEVAL_R2)
        checks = {
            "semantic_hash_protocol": stored_manifest.get("hash_protocol_id") == HASH_PROTOCOL_ID,
            "generator_git_blob_matches": stored_manifest.get("generator_git_blob") == generator_blob,
            "same_selected_ids": stored_manifest.get("selected_query_ids") == old_manifest["selected_query_ids"],
            "same_original_ids": stored_manifest.get("original_query_ids") == old_manifest["original_query_ids"],
            "profile_matches_manifest": stored_manifest.get("profile") == stored_pilot.get("profile"),
            "benchmark_semantic_hash": stored_manifest.get("benchmark_config_semantic_sha256") == benchmark_hash,
            "pilot_semantic_hash": stored_manifest.get("pilot_config_semantic_sha256") == semantic_json_file_sha256(ROOT / PILOT_R2),
            "proof_fixture_semantic_hash": stored_manifest.get("proof_fixture_semantic_sha256") == fixture_hash,
            "preevaluation_ledger_hashes": ledger.get("hashes") == {
                "benchmark_config_semantic_sha256": benchmark_hash,
                "pilot_config_semantic_sha256": semantic_json_file_sha256(ROOT / PILOT_R2),
                "proof_fixture_semantic_sha256": fixture_hash,
                "development_manifest_semantic_sha256": semantic_json_file_sha256(ROOT / MANIFEST_R2),
            },
        }
        result = {"schema": "ddwmr-g2-manifest-r2-check-v1", "all_pass": all(checks.values()), "checks": checks}
        print(json.dumps(result, sort_keys=True))
        if not result["all_pass"]:
            raise SystemExit(1)
        return

    if any((ROOT / rel).exists() for rel in (PILOT_R2, MANIFEST_R2, PREEVAL_R2)):
        raise SystemExit("one or more R2 frozen input files already exist; use --verify instead")
    write_new(PILOT_R2, pilot_r2)
    manifest["pilot_config_semantic_sha256"] = semantic_json_file_sha256(ROOT / PILOT_R2)
    write_new(MANIFEST_R2, manifest)
    manifest_hash = semantic_json_file_sha256(ROOT / MANIFEST_R2)
    ledger = {
        "schema": "ddwmr-g2-preevaluation-semantic-hashes-r2-v1",
        "hash_protocol_id": HASH_PROTOCOL_ID,
        "source_base_commit": source_base_commit,
        "generator_git_blob": generator_blob,
        "hashes": {
            "benchmark_config_semantic_sha256": benchmark_hash,
            "pilot_config_semantic_sha256": semantic_json_file_sha256(ROOT / PILOT_R2),
            "proof_fixture_semantic_sha256": fixture_hash,
            "development_manifest_semantic_sha256": manifest_hash,
        },
        "hash_semantics": "SHA-256 over canonical UTF-8 JSON (sorted keys, compact separators, no insignificant whitespace); independent of LF/CRLF checkout conversion.",
        "frozen_before_any_r2_evaluator_output": True,
    }
    write_new(PREEVAL_R2, ledger)
    print(json.dumps({
        "schema": "ddwmr-g2-manifest-r2-freeze-v1",
        "hash_protocol_id": HASH_PROTOCOL_ID,
        "source_base_commit": source_base_commit,
        "original": manifest["original_query_count_per_method_profile"],
        "selected": manifest["selected_query_count"],
        "not_run": manifest["not_run_query_count"],
        "selection_unchanged_from_v1": manifest["selected_query_ids"] == old_manifest["selected_query_ids"],
        "profile_id": pilot_r2["profile"]["id"],
        "max_rational_bits": pilot_r2["profile"]["max_rational_bits"],
        "benchmark_semantic_sha256": benchmark_hash,
        "pilot_semantic_sha256": semantic_json_file_sha256(ROOT / PILOT_R2),
        "manifest_semantic_sha256": manifest_hash,
        "proof_fixture_semantic_sha256": fixture_hash,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
