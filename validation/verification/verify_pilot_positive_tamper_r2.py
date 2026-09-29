#!/usr/bin/env python3
"""Replay and tamper a completed positive R2 pilot certificate."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from validation.g2.checker import replay_record
from validation.g2.evaluator import ROOT, make_query
from validation.g2.hashing import (
    HASH_PROTOCOL_ID, semantic_json_file_sha256, semantic_jsonl_file_sha256, parse_jsonl_records,
)
from validation.g2.rational import parse_q, qobj


BENCHMARK = ROOT / "validation/configs/benchmark_v1.json"
PILOT = ROOT / "validation/configs/dev_pilot_r2_v1.json"
MANIFEST = ROOT / "results/validation/g2/r2/development_manifest_r2_v1.json"
RECORDS = ROOT / "results/validation/g2/r2/dev_pilot_records_r2_v1.jsonl"
OUTPUT = ROOT / "results/validation/g2/r2/pilot_positive_tamper_check_r2_v1.json"


def rejected(record, query) -> bool:
    result = replay_record(record, query)
    return not result.get("replayed", False) and result.get("record_integrity_valid") is False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true", help="check without writing evidence")
    args = parser.parse_args()
    if not args.check_only and OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite positive tamper evidence: {OUTPUT}")

    benchmark = json.loads(BENCHMARK.read_text(encoding="utf-8"))
    pilot = json.loads(PILOT.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = parse_jsonl_records(RECORDS.read_bytes())
    record = next((row for row in records if row.get("status") == "CERTIFIED"), None)
    if record is None or not isinstance(record.get("proof"), dict):
        raise SystemExit("pilot has no completed positive certificate to tamper")

    benchmark_hash = semantic_json_file_sha256(BENCHMARK)
    pilot_hash = semantic_json_file_sha256(PILOT)
    manifest_hash = semantic_json_file_sha256(MANIFEST)
    query = make_query(
        benchmark, record["query_id"], pilot["profile"], manifest_hash, benchmark_hash, HASH_PROTOCOL_ID,
    )
    baseline = replay_record(record, query)
    radius_index = next((index for index, value in enumerate(record["proof"].get("eta_scaled", [])) if parse_q(value) > 0), None)
    nonzero_radius = radius_index is not None

    radius_tamper = json.loads(json.dumps(record))
    if radius_index is not None:
        old_radius = parse_q(radius_tamper["proof"]["eta_scaled"][radius_index])
        radius_tamper["proof"]["eta_scaled"][radius_index] = qobj(old_radius / 2)
    margin_tamper = json.loads(json.dumps(record))
    old_margin = parse_q(margin_tamper["collision_margin_lower"][0])
    margin_tamper["collision_margin_lower"][0] = qobj(old_margin + 1)
    margin_tamper["proof"]["collision"][0]["margin_lower"] = qobj(old_margin + 1)
    status_tamper = json.loads(json.dumps(record))
    status_tamper["status"] = "UNKNOWN"
    tamper_results = [
        {"name": "reduce serialized comparison radius", "rejected": rejected(radius_tamper, query)},
        {"name": "increase serialized collision margin in record and proof", "rejected": rejected(margin_tamper, query)},
        {"name": "change positive status to UNKNOWN", "rejected": rejected(status_tamper, query)},
    ]
    checks = {
        "positive_record_replayed": baseline.get("replayed", False) and baseline.get("status") == "CERTIFIED",
        "positive_record_has_nonzero_radius": nonzero_radius,
        "all_certificate_tampers_rejected": all(item["rejected"] for item in tamper_results),
    }
    source_revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True,
    ).stdout.strip()
    report = {
        "schema": "ddwmr-g2-pilot-positive-tamper-check-r2-v1",
        "all_pass": all(checks.values()),
        "checks": checks,
        "source_revision": source_revision,
        "hash_protocol_id": HASH_PROTOCOL_ID,
        "benchmark_sha256": benchmark_hash,
        "pilot_config_sha256": pilot_hash,
        "development_manifest_sha256": manifest_hash,
        "records_semantic_sha256": semantic_jsonl_file_sha256(RECORDS),
        "selected_denominator": len(records),
        "profile_id": pilot["profile"]["id"],
        "positive_certificates_checked": 1,
        "completed_certificate_replays": int(checks["positive_record_replayed"]),
        "tested_query_id": record["query_id"],
        "record_input_sha256": record["input_sha256"],
        "nonzero_radius_components": sum(parse_q(value) > 0 for value in record["proof"].get("eta_scaled", [])),
        "tamper_cases": tamper_results,
        "baseline_replay": baseline,
        "python_version": sys.version,
        "python_executable": sys.executable,
        "actual_argv": list(getattr(sys, "orig_argv", [sys.executable, *sys.argv])),
        "working_directory": str(ROOT),
        "scope": "post-pilot independent checker mutation check; does not add an evaluator query or promote the gate",
    }
    if not args.check_only:
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: value for key, value in report.items() if key != "baseline_replay"}, sort_keys=True))
    if not report["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
