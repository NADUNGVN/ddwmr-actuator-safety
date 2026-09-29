#!/usr/bin/env python3
"""Run frozen plumbing fixtures through evaluator, checker, and tamper rejection."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from pathlib import Path

from validation.g2.checker import replay_record
from validation.g2.evaluator import ROOT, canonical_hash, run_query
from validation.g2.hashing import HASH_PROTOCOL_ID, semantic_json_file_sha256, semantic_jsonl_file_sha256
from validation.g2.rational import parse_q, qobj


FIXTURE_PATH = ROOT / "validation/configs/g2_proof_pipeline_fixture_r2_v1.json"
PILOT_PATH = ROOT / "validation/configs/dev_pilot_r2_v1.json"
BENCHMARK_PATH = ROOT / "validation/configs/benchmark_v1.json"
MANIFEST_PATH = ROOT / "results/validation/g2/r2/development_manifest_r2_v1.json"
OUT = ROOT / "results/validation/g2/r2"
RECORDS_PATH = OUT / "proof_fixture_records_r2_v1.jsonl"
METADATA_PATH = OUT / "proof_fixture_metadata_r2_v1.json"
REPORT_PATH = OUT / "proof_fixture_check_r2_v1.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def make_fixture_query(benchmark, fixture, profile, scene, label, benchmark_hash, manifest_hash):
    query_id = f"r2_fixture__{scene['id']}__{fixture['horizon']['id']}__{fixture['action']['id']}"
    return {
        "query_id": query_id,
        "state_cell": fixture["state_cell"],
        "scene": scene,
        "horizon": fixture["horizon"],
        "action": fixture["action"],
        "parameter_cell": benchmark["parameter_cell"],
        "profile": profile,
        "benchmark": benchmark,
        "benchmark_sha256": benchmark_hash,
        "development_manifest_sha256": manifest_hash,
        "hash_protocol_id": HASH_PROTOCOL_ID,
        "fixture_label": label,
    }


def rejected(record, query) -> bool:
    replay = replay_record(record, query)
    return not replay.get("replayed", False) and replay.get("record_integrity_valid") is False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true", help="check frozen fixture without writing evidence")
    args = parser.parse_args()
    if not args.check_only and any(path.exists() for path in (RECORDS_PATH, METADATA_PATH, REPORT_PATH)):
        raise SystemExit(f"refusing to overwrite proof fixture evidence in {OUT}")

    fixture, pilot, benchmark, manifest = map(load, (FIXTURE_PATH, PILOT_PATH, BENCHMARK_PATH, MANIFEST_PATH))
    profile = copy.deepcopy(pilot["profile"])
    profile.update(fixture["fixture_resource_caps"])
    profile["id"] = "R2_PROOF_PIPELINE_FIXTURE_BITS32768_V1"
    resource_profile = copy.deepcopy(pilot["profile"])
    resource_profile.update(fixture["resource_telemetry_profile"])
    benchmark_hash = semantic_json_file_sha256(BENCHMARK_PATH)
    manifest_hash = semantic_json_file_sha256(MANIFEST_PATH)
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip()

    safe_query = make_fixture_query(benchmark, fixture, profile, fixture["safe_scene"], "safe-positive", benchmark_hash, manifest_hash)
    inconclusive_query = make_fixture_query(benchmark, fixture, profile, fixture["inconclusive_scene"], "collision-inconclusive", benchmark_hash, manifest_hash)
    resource_query = make_fixture_query(benchmark, fixture, resource_profile, fixture["safe_scene"], "operation-limit-telemetry", benchmark_hash, manifest_hash)
    resource_query["query_id"] += "__resource_ops1"
    safe_record = run_query(safe_query, revision)
    inconclusive_record = run_query(inconclusive_query, revision)
    resource_record = run_query(resource_query, revision)
    positive_replay = replay_record(safe_record, safe_query)
    inconclusive_replay = replay_record(inconclusive_record, inconclusive_query)
    resource_replay = replay_record(resource_record, resource_query)
    safe_proof = safe_record.get("proof")
    nonzero_radius = isinstance(safe_proof, dict) and any(
        parse_q(item) > 0 for item in safe_proof.get("eta_scaled", [])
    )

    tamper_results = []

    def add_tamper(name: str, record, query, *, applicable: bool = True) -> None:
        tamper_results.append({
            "name": name,
            "applicable": applicable,
            "rejected": rejected(record, query) if applicable else None,
        })

    has_positive_certificate = safe_record.get("status") == "CERTIFIED" and isinstance(safe_proof, dict)
    if isinstance(safe_proof, dict) and isinstance(safe_proof.get("eta_scaled"), list):
        altered = copy.deepcopy(safe_record)
        radius_index = next((i for i, item in enumerate(altered["proof"]["eta_scaled"]) if parse_q(item) > 0), None)
        if radius_index is not None:
            altered["proof"]["eta_scaled"][radius_index] = qobj(parse_q(altered["proof"]["eta_scaled"][radius_index]) / 2)
        add_tamper("reduce serialized comparison radius", altered, safe_query)

        altered = copy.deepcopy(safe_record)
        if isinstance(altered.get("collision_margin_lower"), list) and altered["collision_margin_lower"]:
            bigger_margin = parse_q(altered["collision_margin_lower"][0]) + 1
            altered["collision_margin_lower"][0] = qobj(bigger_margin)
            collision = altered["proof"].get("collision")
            if isinstance(collision, list) and collision:
                collision[0]["margin_lower"] = qobj(bigger_margin)
        add_tamper("increase serialized collision margin", altered, safe_query)
    else:
        add_tamper("reduce serialized comparison radius", copy.deepcopy(safe_record), safe_query, applicable=False)
        add_tamper("increase serialized collision margin", copy.deepcopy(safe_record), safe_query, applicable=False)

    for name, field, replacement in (
        ("change held voltage alias", "held_voltage", [{"num": "1", "den": "1"}, safe_query["action"]["V"][1]]),
        ("change horizon alias", "horizon", {"num": "1", "den": "25"}),
        ("change query identity", "query_id", safe_query["query_id"] + "_tampered"),
        ("change benchmark hash", "benchmark_sha256", "0" * 64),
        ("change development manifest hash", "development_manifest_sha256", "1" * 64),
        ("change profile hash", "profile_sha256", "2" * 64),
        ("change specification hash", "specification_sha256", "3" * 64),
        ("change coverage state cell", "state_cell_id", "different_state_cell"),
    ):
        altered = copy.deepcopy(safe_record)
        altered[field] = replacement
        add_tamper(name, altered, safe_query)

    altered = copy.deepcopy(safe_record)
    altered["status"] = "UNKNOWN"
    add_tamper("change positive status", altered, safe_query, applicable=has_positive_certificate)

    altered_query = copy.deepcopy(safe_query)
    altered_query["action"]["V"][0] = {"num": "1", "den": "1"}
    altered_record = copy.deepcopy(safe_record)
    altered_record["held_voltage"] = copy.deepcopy(altered_query["action"]["V"])
    add_tamper("change hashed query voltage", altered_record, altered_query)

    altered_query = copy.deepcopy(safe_query)
    altered_query["horizon"]["T"] = {"num": "1", "den": "25"}
    altered_record = copy.deepcopy(safe_record)
    altered_record["horizon"] = copy.deepcopy(altered_query["horizon"]["T"])
    add_tamper("change hashed query horizon", altered_record, altered_query)

    checks = {
        "safe_fixture_certified": safe_record.get("status") == "CERTIFIED",
        "safe_fixture_has_nonzero_radius": nonzero_radius,
        "positive_certificate_replayed": positive_replay.get("replayed", False),
        "completed_inconclusive_fixture": inconclusive_record.get("status") == "UNKNOWN" and inconclusive_record.get("proof") is not None,
        "completed_inconclusive_replayed": inconclusive_replay.get("replayed", False) and inconclusive_replay.get("status") == "UNKNOWN",
        "resource_unknown_has_operation_limit": resource_record.get("status") == "UNKNOWN"
            and resource_record.get("proof") is None
            and resource_record.get("reason_codes") == ["RATIONAL_OPERATION_LIMIT"],
        "resource_telemetry_integrity_replayed": resource_replay.get("resource_limited", False)
            and resource_replay.get("record_integrity_valid", False)
            and not resource_replay.get("replayed", False),
        "tamper_cases_all_rejected": bool(tamper_results) and all(
            item["rejected"] for item in tamper_results if item["applicable"]
        ),
        "positive_certificate_tampers_exercised": all(
            item["applicable"] for item in tamper_results
            if item["name"] in {
                "reduce serialized comparison radius", "increase serialized collision margin", "change positive status",
            }
        ),
        "exact_tamper_case_count": len(tamper_results) == 13,
    }
    report = {
        "schema": "ddwmr-g2-proof-pipeline-check-r2-v1",
        "all_pass": all(checks.values()),
        "checks": checks,
        "positive_certificates_checked": int(safe_record.get("status") == "CERTIFIED"),
        "completed_certificate_replays": int(bool(positive_replay.get("replayed")) and safe_record.get("status") == "CERTIFIED"),
        "completed_inconclusive_records": int(inconclusive_record.get("proof") is not None and inconclusive_record.get("status") == "UNKNOWN"),
        "completed_inconclusive_replays": int(bool(inconclusive_replay.get("replayed")) and inconclusive_record.get("status") == "UNKNOWN"),
        "resource_limited_unknown_records": int(resource_record.get("status") == "UNKNOWN" and resource_record.get("proof") is None),
        "resource_limited_unknown_integrity_records": int(bool(resource_replay.get("resource_limited")) and bool(resource_replay.get("record_integrity_valid"))),
        "statuses": {
            safe_record.get("query_id"): safe_record.get("status"),
            inconclusive_record.get("query_id"): inconclusive_record.get("status"),
            resource_record.get("query_id"): resource_record.get("status"),
        },
        "status_details": {
            "positive_fixture": {key: safe_record[key] for key in ("status", "reason_codes", "reason", "work", "resource_diagnostic") if key in safe_record},
            "inconclusive_fixture": {key: inconclusive_record[key] for key in ("status", "reason_codes", "reason", "work", "resource_diagnostic") if key in inconclusive_record},
            "resource_fixture": {key: resource_record[key] for key in ("status", "reason_codes", "reason", "work", "resource_diagnostic") if key in resource_record},
        },
        "nonzero_comparison_radius": nonzero_radius,
        "resource_failure": resource_record.get("resource_diagnostic", {}).get("failure")
            if isinstance(resource_record.get("resource_diagnostic"), dict) else None,
        "tamper_rejections": tamper_results,
        "positive_replay": positive_replay,
        "inconclusive_replay": inconclusive_replay,
        "resource_replay": resource_replay,
        "fixture_path": FIXTURE_PATH.relative_to(ROOT).as_posix(),
        "records_path": RECORDS_PATH.relative_to(ROOT).as_posix(),
        "metadata_path": METADATA_PATH.relative_to(ROOT).as_posix(),
        "scope": "declared plumbing fixture; does not alter the benchmark or constitute general soundness acceptance",
    }

    if not args.check_only:
        OUT.mkdir(parents=True, exist_ok=True)
        RECORDS_PATH.write_text(
            "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in (safe_record, inconclusive_record, resource_record)),
            encoding="utf-8", newline="\n",
        )
        metadata = {
            "schema": "ddwmr-g2-proof-fixture-run-metadata-r2-v1",
            "hash_protocol_id": HASH_PROTOCOL_ID,
            "source_revision": revision,
            "fixture_id": fixture["fixture_id"],
            "fixture_semantic_sha256": semantic_json_file_sha256(FIXTURE_PATH),
            "benchmark_sha256": benchmark_hash,
            "development_manifest_sha256": manifest_hash,
            "profile_id": profile["id"],
            "profile_sha256": canonical_hash(profile),
            "resource_profile_id": resource_profile["id"],
            "resource_profile_sha256": canonical_hash(resource_profile),
            "fixture_check_disposition": "PASS" if report["all_pass"] else "PARTIAL_RESOURCE_LIMITED",
            "records_semantic_sha256": semantic_jsonl_file_sha256(RECORDS_PATH),
            "python_version": sys.version,
            "python_executable": sys.executable,
            "actual_argv": list(getattr(sys, "orig_argv", [sys.executable, *sys.argv])),
            "working_directory": str(ROOT),
            "fixture_is_not_a_pilot_query": True,
        }
        METADATA_PATH.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: value for key, value in report.items() if key not in {"positive_replay", "inconclusive_replay", "resource_replay", "tamper_rejections"}}, sort_keys=True))
    if not report["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
