"""Run the frozen R3 pilot or its one conditional remaining-ID continuation."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from collections import Counter
from pathlib import Path

from validation.g2.evaluator import ROOT, make_query, run_query
from validation.g2.hashing import HASH_PROTOCOL_ID, semantic_json_file_sha256, semantic_jsonl_file_sha256
from validation.g2.provenance import current_revision, source_commitments, verify_commitment, worktree_status


PILOT_CONFIG = Path("validation/configs/dev_pilot_r3_v1.json")
MANIFEST = Path("results/validation/g2/r3/development_manifest_r3_v1.json")
BENCHMARK = Path("validation/configs/benchmark_v1.json")
FULL_GRID_MANIFEST = Path("results/validation/g2/r3/full_grid_continuation_manifest_r3_v1.json")
PILOT_RECORDS = Path("results/validation/g2/r3/dev_pilot_records_r3_v1.jsonl")
PILOT_METADATA = Path("results/validation/g2/r3/dev_pilot_run_metadata_r3_v1.json")
FULL_RECORDS = Path("results/validation/g2/r3/conditional_full_grid_records_r3_v1.jsonl")
FULL_METADATA = Path("results/validation/g2/r3/conditional_full_grid_run_metadata_r3_v1.json")
SPEC_LEDGER = Path("results/validation/g2/r3/specification_content_ledger_r3_v1.json")

PRODUCER_PATHS = [
    "validation/g2/evaluator.py", "validation/g2/rational.py", "validation/g2/interval.py",
    "validation/g2/model.py", "validation/g2/hashing.py", "validation/g2/provenance.py",
    "validation/scripts/run_pilot_r3.py",
]


def load(path: Path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def git_is_tracked(path: Path) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", path.as_posix()], cwd=ROOT,
        capture_output=True,
    )
    return result.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("pilot", "conditional-full-grid"), default="pilot")
    parser.add_argument("--output", default=None)
    parser.add_argument("--metadata", default=None)
    parser.add_argument("--pilot-checker-report", default=None)
    args = parser.parse_args()

    pilot_path = PILOT_CONFIG
    manifest_path = MANIFEST
    benchmark_path = BENCHMARK
    pilot, manifest, benchmark = load(pilot_path), load(manifest_path), load(benchmark_path)
    spec_ledger = load(SPEC_LEDGER)
    if pilot["profile"] != manifest["profile"] or pilot["profile"]["specification_bundle_sha256"] != manifest["specification_bundle_sha256"]:
        raise SystemExit("frozen R3 profile/manifest/specification binding mismatch")
    if semantic_json_file_sha256(ROOT / pilot_path) != manifest["input_hashes"]["pilot_config_semantic_sha256"]:
        raise SystemExit("R3 pilot config semantic hash mismatch")
    if semantic_json_file_sha256(ROOT / benchmark_path) != manifest["input_hashes"]["benchmark_config_semantic_sha256"]:
        raise SystemExit("R3 benchmark semantic hash mismatch")
    if semantic_json_file_sha256(ROOT / FULL_GRID_MANIFEST) != manifest["input_hashes"]["conditional_full_grid_manifest_semantic_sha256"]:
        raise SystemExit("R3 conditional full-grid manifest hash mismatch")
    if spec_ledger.get("specification_bundle_sha256") != manifest["specification_bundle_sha256"]:
        raise SystemExit("R3 specification content bundle mismatch")
    if semantic_json_file_sha256(ROOT / SPEC_LEDGER) != manifest["input_hashes"]["specification_content_ledger_semantic_sha256"]:
        raise SystemExit("R3 specification ledger semantic hash mismatch")
    if not all(verify_commitment(item) for item in spec_ledger["sources"]):
        raise SystemExit("R3 immutable specification blob verification failed")

    revision = current_revision()
    branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    if branch != "luna/g2-validation-v1":
        raise SystemExit(f"R3 evaluation is restricted to luna/g2-validation-v1; current branch is {branch!r}")
    dirty_before = worktree_status()
    if dirty_before:
        raise SystemExit("source tree must be clean before each R3 evaluator phase")
    producer_sources = source_commitments(revision, PRODUCER_PATHS)
    frozen_producer_hashes = {
        item["repository_relative_path"]: item["sha256_git_blob_bytes"]
        for item in manifest["producer_source_commitments"]
    }
    if any(frozen_producer_hashes.get(item["repository_relative_path"]) != item["sha256_git_blob_bytes"] for item in producer_sources):
        raise SystemExit("committed producer code differs from the frozen evaluator source commitments")

    if args.phase == "pilot":
        selected = manifest["selected_query_ids"]
        phase_id = "R3_PILOT_216"
        output_path = ROOT / (args.output or PILOT_RECORDS.as_posix())
        metadata_path = ROOT / (args.metadata or PILOT_METADATA.as_posix())
        if output_path.exists() or metadata_path.exists():
            raise SystemExit("refusing to overwrite existing R3 pilot records or metadata")
    else:
        full_grid = load(FULL_GRID_MANIFEST)
        selected = full_grid["selected_query_ids"]
        phase_id = "R3_CONDITIONAL_REMAINING_1728"
        output_path = ROOT / (args.output or FULL_RECORDS.as_posix())
        metadata_path = ROOT / (args.metadata or FULL_METADATA.as_posix())
        report_path = ROOT / args.pilot_checker_report if args.pilot_checker_report else ROOT / "results/validation/g2/r3/dev_pilot_record_check_r3_v1.json"
        if not report_path.exists() or not git_is_tracked(report_path.relative_to(ROOT)):
            raise SystemExit("conditional full grid requires the committed R3 pilot checker report")
        pilot_report = load(report_path.relative_to(ROOT))
        if not pilot_report.get("continuation_allowed") or not pilot_report.get("all_pass"):
            raise SystemExit("R3 pilot did not satisfy every frozen continuation condition")
        if pilot_report.get("specification_bundle_sha256") != manifest["specification_bundle_sha256"]:
            raise SystemExit("pilot checker report specification bundle mismatch")
        if pilot_report.get("profile_semantic_sha256") != manifest["profile_semantic_sha256"]:
            raise SystemExit("pilot checker report profile mismatch")
        if not git_is_tracked(PILOT_RECORDS) or not git_is_tracked(report_path.relative_to(ROOT)):
            raise SystemExit("R3 pilot outputs must be committed before conditional continuation")
        if output_path.exists() or metadata_path.exists():
            raise SystemExit("refusing to overwrite existing R3 conditional full-grid outputs")

    if len(selected) != (216 if args.phase == "pilot" else 1728):
        raise SystemExit("frozen phase selection has the wrong query count")
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = list(getattr(sys, "orig_argv", [sys.executable, *sys.argv]))
    metadata = {
        "schema": "ddwmr-g2-pilot-run-metadata-r3-v1",
        "phase_id": phase_id,
        "producer_revision": revision,
        "branch": branch,
        "producer_source_commitments": producer_sources,
        "producer_source_commitments_match_frozen_manifest": True,
        "worktree_status_before_run": dirty_before,
        "source_tree_clean_before_run": True,
        "hash_protocol_id": HASH_PROTOCOL_ID,
        "specification_bundle_sha256": manifest["specification_bundle_sha256"],
        "benchmark_sha256": manifest["input_hashes"]["benchmark_config_semantic_sha256"],
        "pilot_config_sha256": manifest["input_hashes"]["pilot_config_semantic_sha256"],
        "development_manifest_sha256": semantic_json_file_sha256(ROOT / manifest_path),
        "profile_semantic_sha256": manifest["profile_semantic_sha256"],
        "frozen_input_set_bundle_sha256": manifest["input_hashes"]["frozen_input_set_bundle_sha256"],
        "selected_queries": len(selected),
        "original_denominator_per_method_profile": manifest["original_query_count_per_method_profile"],
        "not_run_before_phase": len(manifest["not_run_query_ids_before_conditional_continuation"]),
        "selected_query_ids_sha256_lf": manifest["selected_query_ids_sha256_lf"] if args.phase == "pilot" else None,
        "selection_ids_sha256_lf": hashlib.sha256("\n".join(selected).encode("utf-8")).hexdigest(),
        "profile_id": pilot["profile"]["id"],
        "distance_method_id": pilot["profile"]["distance_method_id"],
        "distance_rounding_precision_bits": pilot["profile"]["distance_rounding_precision_bits"],
        "runtime_environment": sys.version,
        "python_executable": sys.executable,
        "actual_argv": command,
        "working_directory": str(ROOT),
        "platform": {"system": platform.system(), "release": platform.release(), "machine": platform.machine()},
        "output_path": output_path.relative_to(ROOT).as_posix(),
        "timing_note": "Elapsed seconds are display-only and not a safety predicate.",
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    counts = Counter()
    with output_path.open("x", encoding="utf-8", newline="\n") as stream:
        for index, query_id in enumerate(selected, start=1):
            query = make_query(
                benchmark, query_id, pilot["profile"],
                metadata["development_manifest_sha256"], metadata["benchmark_sha256"],
                HASH_PROTOCOL_ID, manifest["specification_bundle_sha256"],
            )
            record = run_query(query, revision)
            record["evaluation_phase"] = phase_id
            counts[record["status"]] += 1
            stream.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
            stream.flush()
            if index % 12 == 0 or index == len(selected):
                print(json.dumps({"phase": phase_id, "completed": index, "total": len(selected), "counts": dict(sorted(counts.items()))}, sort_keys=True), flush=True)

    metadata["records_semantic_sha256"] = semantic_jsonl_file_sha256(output_path)
    metadata["status_counts"] = dict(sorted(counts.items()))
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "phase_id": phase_id, "producer_revision": revision,
        "record_count": len(selected), "status_counts": dict(sorted(counts.items())),
        "records_semantic_sha256": metadata["records_semantic_sha256"],
        "records_path": str(output_path), "metadata_path": str(metadata_path),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
