#!/usr/bin/env python3
"""Check pilot coverage and independently replay every completed proof record."""

from __future__ import annotations

import hashlib
import argparse
import json
from collections import Counter
from pathlib import Path

from validation.g2.checker import replay_record
from validation.g2.evaluator import ROOT, canonical_hash, make_query


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", default="results/validation/g2/dev_pilot_records_v1.jsonl")
    parser.add_argument("--metadata", default=None)
    parser.add_argument("--report", default=None)
    args = parser.parse_args()
    benchmark_path = ROOT / "validation/configs/benchmark_v1.json"
    pilot_path = ROOT / "validation/configs/dev_pilot_v1.json"
    manifest_path = ROOT / "results/validation/g2/development_manifest_v1.json"
    records_path = ROOT / args.records
    if args.metadata:
        metadata_path = ROOT / args.metadata
    elif args.records == "results/validation/g2/dev_pilot_records_v1.jsonl":
        metadata_path = ROOT / "results/validation/g2/dev_pilot_run_metadata_v1.json"
    else:
        metadata_path = records_path.with_name(records_path.stem + "_run_metadata.json")
    report_path = ROOT / (args.report or (
        "results/validation/g2/dev_pilot_record_check_v1.json"
        if args.records == "results/validation/g2/dev_pilot_records_v1.jsonl"
        else str(records_path.relative_to(ROOT).with_name(records_path.stem + "_record_check.json"))
    ))
    benchmark, pilot, manifest, metadata = map(load, (benchmark_path, pilot_path, manifest_path, metadata_path))
    manifest_hash = digest(manifest_path)
    benchmark_hash = digest(benchmark_path)
    profile = pilot["profile"]

    records = [json.loads(line) for line in records_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    record_ids = [record.get("query_id") for record in records]
    by_id = {record.get("query_id"): record for record in records}
    coverage_ok = len(records) == len(manifest["selected_query_ids"]) and len(by_id) == len(records) and record_ids == manifest["selected_query_ids"]
    code_revision_ok = all(record.get("source_revision") == metadata["source_revision"] for record in records)
    frozen_hashes_ok = (
        metadata["benchmark_sha256"] == benchmark_hash
        and metadata["development_manifest_sha256"] == manifest_hash
        and metadata["pilot_config_sha256"] == digest(pilot_path)
        and manifest["benchmark_config_sha256"] == benchmark_hash
        and manifest["pilot_config_sha256"] == digest(pilot_path)
    )
    results = []
    counts = Counter()
    all_replayed = coverage_ok and code_revision_ok and frozen_hashes_ok
    for record in records:
        counts[record.get("status", "MISSING_STATUS")] += 1
        query_id = record.get("query_id", "")
        query = make_query(benchmark, query_id, profile, manifest_hash, benchmark_hash)
        expected_input_hash = canonical_hash({
            "query_id": query_id, "state_cell": query["state_cell"], "scene": query["scene"],
            "horizon": query["horizon"], "action": query["action"],
            "parameter_cell": query["parameter_cell"], "profile": profile,
        })
        input_hash_ok = record.get("input_sha256") == expected_input_hash
        replay = replay_record(record, query)
        approved_resource_reasons = {"RATIONAL_BIT_LIMIT", "RATIONAL_OPERATION_LIMIT", "WALL_TIME_LIMIT"}
        resource_unknown_ok = (
            record.get("status") == "UNKNOWN" and record.get("proof") is None
            and set(record.get("reason_codes", [])) <= approved_resource_reasons
            and bool(record.get("reason_codes"))
            and record.get("work", {}).get("rational_operations", 0) <= profile["max_rational_operations"] + 1
            and record.get("work", {}).get("max_rational_bits", 0) <= profile["max_rational_bits"]
        )
        replay_ok = replay.get("replayed", False) or resource_unknown_ok
        quantifiers_ok = record.get("quantifiers") == {
            "one_common_voltage_for_all_initial_states_and_labels": True,
            "initial_state_cell_universal": True,
            "parameter_labels_fixed_for_entire_hold": True,
            "time_coverage": "closed [0,T] by whole-hold ranges",
            "coefficient_representation": "named outer interval hull; interval arithmetic may forget rational-map correlations but does not resample a physical label",
            "endpoint_target_requested": False,
        }
        row_ok = (
            input_hash_ok and replay_ok and quantifiers_ok
            and record.get("schema") == "ddwmr-g2-record-v1"
            and record.get("method_id") == "G2_COMP_CLIP_WHOLE_HOLD_INTERVAL_HULL_N1_V1"
            and record.get("review_status") == "PENDING_INDEPENDENT_AUDIT"
            and record.get("source_revision") == metadata["source_revision"]
            and record.get("benchmark_sha256") == benchmark_hash
            and record.get("development_manifest_sha256") == manifest_hash
            and record.get("state_cell_id") == query["state_cell"]["id"]
            and record.get("scene_id") == query["scene"]["id"]
            and record.get("horizon_id") == query["horizon"]["id"]
            and record.get("action_id") == query["action"]["id"]
            and record.get("parameter_cell_id") == query["parameter_cell"]["id"]
        )
        if record.get("proof") is not None:
            row_ok = row_ok and record.get("obstacle_count") == 1
        else:
            row_ok = row_ok and resource_unknown_ok
        if record.get("status") in {"INVALID_INPUT", "EXECUTION_FAILURE"}:
            row_ok = False
        all_replayed = all_replayed and row_ok
        result = {
            "query_id": query_id, "status": record.get("status"),
            "input_hash_valid": input_hash_ok, "quantifiers_valid": quantifiers_ok, "replay": replay,
            "resource_unknown_valid": resource_unknown_ok,
            "record_valid": row_ok,
        }
        results.append(result)

    summary = {
        "schema": "ddwmr-g2-record-check-v1",
        "all_pass": all_replayed and len(records) == 216,
        "manifest_coverage_exact": coverage_ok,
        "source_revision_matches": code_revision_ok,
        "frozen_hashes_match": frozen_hashes_ok,
        "records": len(records),
        "status_counts": dict(sorted(counts.items())),
        "not_run_original_queries": manifest["not_run_query_count"],
        "completed_certificate_replays": sum(bool(x["replay"].get("replayed")) for x in results),
        "resource_limited_unknowns": sum(bool(x["resource_unknown_valid"]) for x in results),
        "invalid_inputs": counts["INVALID_INPUT"],
        "execution_failures": counts["EXECUTION_FAILURE"],
        "records_detail": results,
    }
    report_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "records_detail"}, sort_keys=True))
    if not summary["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
