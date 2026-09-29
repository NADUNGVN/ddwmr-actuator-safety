#!/usr/bin/env python3
"""Check query binding, resource-record integrity, and every completed proof replay."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from validation.g2.checker import replay_record
from validation.g2.evaluator import ROOT, canonical_hash, make_query
from validation.g2.hashing import (
    HASH_PROTOCOL_ID, parse_jsonl_records, semantic_json_file_sha256, semantic_jsonl_file_sha256,
)


def raw_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_digest(path: Path, protocol: str, *, jsonl: bool = False) -> str:
    if protocol == HASH_PROTOCOL_ID:
        return semantic_jsonl_file_sha256(path) if jsonl else semantic_json_file_sha256(path)
    return raw_digest(path)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", default="results/validation/g2/dev_pilot_records_v1.jsonl")
    parser.add_argument("--metadata", default=None)
    parser.add_argument("--report", default=None)
    parser.add_argument("--benchmark", default="validation/configs/benchmark_v1.json")
    parser.add_argument("--pilot", default="validation/configs/dev_pilot_v1.json")
    parser.add_argument("--manifest", default="results/validation/g2/development_manifest_v1.json")
    args = parser.parse_args()

    benchmark_path = ROOT / args.benchmark
    pilot_path = ROOT / args.pilot
    manifest_path = ROOT / args.manifest
    records_path = ROOT / args.records
    if args.metadata:
        metadata_path = ROOT / args.metadata
    elif args.records == "results/validation/g2/dev_pilot_records_v1.jsonl":
        metadata_path = ROOT / "results/validation/g2/dev_pilot_run_metadata_v1.json"
    else:
        metadata_path = records_path.with_name(records_path.stem + "_run_metadata.json")
    if args.report:
        report_path = ROOT / args.report
    elif args.records == "results/validation/g2/dev_pilot_records_v1.jsonl":
        report_path = ROOT / "results/validation/g2/dev_pilot_record_check_v1.json"
    else:
        report_path = records_path.with_name(records_path.stem + "_record_check.json")

    if report_path.exists():
        raise SystemExit(f"refusing to overwrite verification report: {report_path}")
    benchmark, pilot, manifest, metadata = map(load, (benchmark_path, pilot_path, manifest_path, metadata_path))
    protocol = metadata.get("hash_protocol_id", "legacy-raw-v1")
    protocol_supported = protocol in {"legacy-raw-v1", HASH_PROTOCOL_ID}
    semantic = protocol == HASH_PROTOCOL_ID
    benchmark_hash = file_digest(benchmark_path, protocol)
    pilot_hash = file_digest(pilot_path, protocol)
    manifest_hash = file_digest(manifest_path, protocol)
    records_hash = file_digest(records_path, protocol, jsonl=True)
    profile = pilot.get("profile", {})
    records = parse_jsonl_records(records_path.read_bytes())
    record_ids = [record.get("query_id") for record in records]
    by_id = {record.get("query_id"): record for record in records}
    coverage_ok = (
        len(records) == manifest.get("selected_query_count")
        and len(by_id) == len(records)
        and record_ids == manifest.get("selected_query_ids")
    )
    code_revision_ok = all(record.get("source_revision") == metadata.get("source_revision") for record in records)
    hash_fields_ok = (
        protocol_supported
        and metadata.get("benchmark_sha256") == benchmark_hash
        and metadata.get("pilot_config_sha256") == pilot_hash
        and metadata.get("development_manifest_sha256") == manifest_hash
        and manifest.get("profile") == profile
    )
    if semantic:
        hash_fields_ok = hash_fields_ok and (
            manifest.get("hash_protocol_id") == HASH_PROTOCOL_ID
            and manifest.get("benchmark_config_semantic_sha256") == benchmark_hash
            and manifest.get("pilot_config_semantic_sha256") == pilot_hash
            and metadata.get("records_semantic_sha256") == records_hash
            and metadata.get("selected_queries") == manifest.get("selected_query_count")
            and metadata.get("original_denominator") == manifest.get("original_query_count_per_method_profile")
            and metadata.get("profile_id") == profile.get("id")
            and metadata.get("specification_sha256") == canonical_hash({
                "hash_protocol_id": HASH_PROTOCOL_ID,
                "benchmark_sha256": benchmark_hash,
                "development_manifest_sha256": manifest_hash,
            })
            and metadata.get("selected_query_ids_sha256") == hashlib.sha256(
                "\n".join(manifest.get("selected_query_ids", [])).encode("utf-8")
            ).hexdigest()
            and isinstance(metadata.get("python_executable"), str) and bool(metadata.get("python_executable"))
            and isinstance(metadata.get("working_directory"), str) and Path(metadata["working_directory"]).is_absolute()
            and isinstance(metadata.get("actual_argv"), list)
            and metadata.get("actual_argv", [None])[0] == metadata.get("python_executable")
            and metadata.get("command") == metadata.get("actual_argv")
        )

    result_rows = []
    counts = Counter()
    proof_record_count = 0
    completed_certificate_replays = 0
    completed_inconclusive_replays = 0
    positive_certificates_checked = 0
    resource_limited_unknowns = 0
    invalid_inputs = 0
    execution_failures = 0
    rows_integrity_ok = True
    rows_proof_ok = True

    for record in records:
        status = record.get("status", "MISSING_STATUS")
        counts[status] += 1
        query_id = record.get("query_id", "")
        row = {"query_id": query_id, "status": status}
        try:
            query = make_query(
                benchmark, query_id, profile, manifest_hash, benchmark_hash,
                HASH_PROTOCOL_ID if semantic else None,
            )
        except Exception as exc:
            row.update({"record_integrity_valid": False, "query_error": f"{type(exc).__name__}: {exc}"})
            rows_integrity_ok = False
            rows_proof_ok = False
            result_rows.append(row)
            continue

        replay = replay_record(record, query)
        has_proof = record.get("proof") is not None
        if has_proof:
            proof_record_count += 1
        if status == "CERTIFIED":
            positive_certificates_checked += 1
        if replay.get("resource_limited") and replay.get("record_integrity_valid"):
            resource_limited_unknowns += 1
        if has_proof and replay.get("replayed") and status == "CERTIFIED":
            completed_certificate_replays += 1
        if has_proof and replay.get("replayed") and status == "UNKNOWN":
            completed_inconclusive_replays += 1
        if status == "INVALID_INPUT":
            invalid_inputs += 1
        if status == "EXECUTION_FAILURE":
            execution_failures += 1

        row_integrity_ok = bool(replay.get("record_integrity_valid"))
        row_integrity_ok = row_integrity_ok and record.get("review_status") == "PENDING_INDEPENDENT_AUDIT"
        row_integrity_ok = row_integrity_ok and record.get("source_revision") == metadata.get("source_revision")
        if status in {"INVALID_INPUT", "EXECUTION_FAILURE"}:
            row_integrity_ok = False
        row_proof_ok = not has_proof or bool(replay.get("replayed"))
        rows_integrity_ok = rows_integrity_ok and row_integrity_ok
        rows_proof_ok = rows_proof_ok and row_proof_ok
        row.update({
            "record_integrity_valid": row_integrity_ok,
            "proof_present": has_proof,
            "proof_replay": replay,
            "resource_unknown_integrity_valid": bool(replay.get("resource_limited") and replay.get("record_integrity_valid")),
        })
        result_rows.append(row)

    record_integrity_pass = coverage_ok and code_revision_ok and hash_fields_ok and rows_integrity_ok
    proof_replay_pass = proof_record_count > 0 and rows_proof_ok
    positive_certificate_replay_pass = positive_certificates_checked > 0 and (
        completed_certificate_replays == positive_certificates_checked
    )
    summary = {
        "schema": "ddwmr-g2-record-check-r2-v1" if semantic else "ddwmr-g2-record-check-v2",
        "hash_protocol_id": protocol,
        "all_pass": record_integrity_pass and proof_replay_pass and positive_certificate_replay_pass,
        "record_integrity_pass": record_integrity_pass,
        "proof_replay_pass": proof_replay_pass,
        "positive_certificate_replay_pass": positive_certificate_replay_pass,
        "manifest_coverage_exact": coverage_ok,
        "source_revision_matches": code_revision_ok,
        "frozen_hashes_match": hash_fields_ok,
        "records_semantic_or_raw_sha256": records_hash,
        "records": len(records),
        "status_counts": dict(sorted(counts.items())),
        "original_denominator": manifest.get("original_query_count_per_method_profile"),
        "selected_denominator": manifest.get("selected_query_count"),
        "not_run_original_queries": manifest.get("not_run_query_count"),
        "proof_records": proof_record_count,
        "completed_certificate_replays": completed_certificate_replays,
        "completed_inconclusive_replays": completed_inconclusive_replays,
        "positive_certificates_checked": positive_certificates_checked,
        "resource_limited_unknowns": resource_limited_unknowns,
        "invalid_inputs": invalid_inputs,
        "execution_failures": execution_failures,
        "records_detail": result_rows,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "records_detail"}, sort_keys=True))
    if not summary["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
