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


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    default_output = "results/validation/g2/dev_pilot_records_v1.jsonl"
    parser.add_argument("--output", default=default_output)
    parser.add_argument("--metadata", default=None)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    output = ROOT / args.output
    benchmark_path = ROOT / "validation/configs/benchmark_v1.json"
    pilot_path = ROOT / "validation/configs/dev_pilot_v1.json"
    manifest_path = ROOT / "results/validation/g2/development_manifest_v1.json"
    benchmark, pilot, manifest = load(benchmark_path), load(pilot_path), load(manifest_path)
    if digest(benchmark_path) != manifest["benchmark_config_sha256"] or digest(pilot_path) != manifest["pilot_config_sha256"]:
        raise SystemExit("frozen benchmark/pilot hash mismatch")
    if output.exists() and not args.overwrite:
        raise SystemExit(f"refusing to overwrite existing output: {output}")
    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, check=True, text=True, capture_output=True).stdout
    if status.strip():
        raise SystemExit("source tree must be clean before evaluator runs; commit the evaluator first")
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip()
    manifest_hash = digest(manifest_path)
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
    metadata = {
        "schema": "ddwmr-g2-pilot-run-metadata-v1",
        "source_revision": revision,
        "benchmark_sha256": digest(benchmark_path),
        "pilot_config_sha256": digest(pilot_path),
        "development_manifest_sha256": manifest_hash,
        "selected_queries": len(selected), "original_denominator": manifest["original_query_count_per_method_profile"],
        "profile_id": profile["id"], "runtime_environment": subprocess.run(
            ["python", "--version"], cwd=ROOT, check=True, text=True, capture_output=True
        ).stdout.strip() or sys.version,
        "platform": {"system": platform.system(), "release": platform.release(), "machine": platform.machine()},
        "command": "python validation/scripts/run_pilot.py",
        "timing_note": "Elapsed seconds are measured per original query on this machine; display-only and not a safety predicate.",
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    counts = Counter()
    with output.open("w", encoding="utf-8", newline="\n") as stream:
        for index, query_id in enumerate(selected, start=1):
            query = make_query(benchmark, query_id, profile, manifest_hash, digest(benchmark_path))
            record = run_query(query, revision)
            counts[record["status"]] += 1
            stream.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
            stream.flush()
            if index % 12 == 0 or index == len(selected):
                print(json.dumps({"completed": index, "total": len(selected), "counts": dict(sorted(counts.items()))}, sort_keys=True), flush=True)
    print(json.dumps({"source_revision": revision, "records": len(selected), "counts": dict(sorted(counts.items())), "output": str(output)}, sort_keys=True))


if __name__ == "__main__":
    main()
