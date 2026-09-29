#!/usr/bin/env python3
"""Run the precommitted bounded development pilot, preserving every outcome."""

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
from validation.g2.hashing import (
    HASH_PROTOCOL_ID, semantic_json_file_sha256, semantic_jsonl_file_sha256,
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    default_output = "results/validation/g2/dev_pilot_records_v1.jsonl"
    parser.add_argument("--output", default=default_output)
    parser.add_argument("--metadata", default=None)
    parser.add_argument("--benchmark", default="validation/configs/benchmark_v1.json")
    parser.add_argument("--pilot", default="validation/configs/dev_pilot_v1.json")
    parser.add_argument("--manifest", default="results/validation/g2/development_manifest_v1.json")
    parser.add_argument("--hash-protocol", choices=("legacy-raw-v1", HASH_PROTOCOL_ID), default="legacy-raw-v1")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    output = ROOT / args.output
    benchmark_path = ROOT / args.benchmark
    pilot_path = ROOT / args.pilot
    manifest_path = ROOT / args.manifest
    benchmark, pilot, manifest = load(benchmark_path), load(pilot_path), load(manifest_path)
    semantic = args.hash_protocol == HASH_PROTOCOL_ID
    benchmark_hash = semantic_json_file_sha256(benchmark_path) if semantic else digest(benchmark_path)
    pilot_hash = semantic_json_file_sha256(pilot_path) if semantic else digest(pilot_path)
    expected_benchmark_hash = manifest.get("benchmark_config_semantic_sha256") if semantic else manifest.get("benchmark_config_sha256")
    expected_pilot_hash = manifest.get("pilot_config_semantic_sha256") if semantic else manifest.get("pilot_config_sha256")
    if semantic and manifest.get("hash_protocol_id") != HASH_PROTOCOL_ID:
        raise SystemExit("R2 manifest does not declare the requested semantic hash protocol")
    if benchmark_hash != expected_benchmark_hash or pilot_hash != expected_pilot_hash:
        raise SystemExit("frozen benchmark/pilot hash mismatch")
    if output.exists() and not args.overwrite:
        raise SystemExit(f"refusing to overwrite existing output: {output}")
    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, check=True, text=True, capture_output=True).stdout
    if status.strip():
        raise SystemExit("source tree must be clean before evaluator runs; commit the evaluator first")
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip()
    manifest_hash = semantic_json_file_sha256(manifest_path) if semantic else digest(manifest_path)
    profile = pilot["profile"]
    selected = manifest["selected_query_ids"]
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    if args.metadata:
        metadata_path = ROOT / args.metadata
    elif args.output == default_output:
        metadata_path = ROOT / "results/validation/g2/dev_pilot_run_metadata_v1.json"
    else:
        metadata_path = output.with_name(output.stem + "_run_metadata.json")
    if metadata_path.exists() and not args.overwrite:
        raise SystemExit(f"refusing to overwrite existing metadata: {metadata_path}")
    actual_argv = list(getattr(sys, "orig_argv", [sys.executable, *sys.argv]))
    metadata = {
        "schema": "ddwmr-g2-pilot-run-metadata-r2-v1" if semantic else "ddwmr-g2-pilot-run-metadata-v1",
        "source_revision": revision,
        "hash_protocol_id": args.hash_protocol,
        "benchmark_sha256": benchmark_hash,
        "pilot_config_sha256": pilot_hash,
        "development_manifest_sha256": manifest_hash,
        "selected_queries": len(selected), "original_denominator": manifest["original_query_count_per_method_profile"],
        "selected_query_ids_sha256": hashlib.sha256("\n".join(selected).encode("utf-8")).hexdigest(),
        "profile_id": profile["id"], "runtime_environment": sys.version,
        "python_executable": sys.executable,
        "actual_argv": actual_argv,
        "working_directory": str(ROOT),
        "platform": {"system": platform.system(), "release": platform.release(), "machine": platform.machine()},
        "command": actual_argv,
        "timing_note": "Elapsed seconds are measured per original query on this machine; display-only and not a safety predicate.",
    }
    if semantic:
        metadata["specification_sha256"] = hashlib.sha256(json.dumps({
            "hash_protocol_id": args.hash_protocol,
            "benchmark_sha256": benchmark_hash,
            "development_manifest_sha256": manifest_hash,
        }, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")).hexdigest()
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    counts = Counter()
    with output.open("w", encoding="utf-8", newline="\n") as stream:
        for index, query_id in enumerate(selected, start=1):
            query = make_query(benchmark, query_id, profile, manifest_hash, benchmark_hash, args.hash_protocol if semantic else None)
            record = run_query(query, revision)
            counts[record["status"]] += 1
            stream.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
            stream.flush()
            if index % 12 == 0 or index == len(selected):
                print(json.dumps({"completed": index, "total": len(selected), "counts": dict(sorted(counts.items()))}, sort_keys=True), flush=True)
    if semantic:
        metadata["records_semantic_sha256"] = semantic_jsonl_file_sha256(output)
        metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"source_revision": revision, "records": len(selected), "counts": dict(sorted(counts.items())), "output": str(output)}, sort_keys=True))


if __name__ == "__main__":
    main()
