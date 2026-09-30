"""Replay R3 records, verify run provenance, and produce transition/group summaries."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

from validation.g2.checker import replay_record
from validation.g2.evaluator import ROOT, make_query
from validation.g2.hashing import (
    HASH_PROTOCOL_ID, semantic_json_file_sha256, semantic_jsonl_file_sha256, semantic_json_sha256,
)
from validation.g2.provenance import current_revision, source_commitments, verify_commitment, worktree_status


PILOT_CONFIG = Path("validation/configs/dev_pilot_r3_v1.json")
MANIFEST = Path("results/validation/g2/r3/development_manifest_r3_v1.json")
PREEVAL = Path("results/validation/g2/r3/SHA256SUMS_PRE_EVAL_R3.json")
BENCHMARK = Path("validation/configs/benchmark_v1.json")
R2_RECORDS = Path("results/validation/g2/r2/dev_pilot_records_r2_v1.jsonl")
PILOT_RECORDS = Path("results/validation/g2/r3/dev_pilot_records_r3_v1.jsonl")
PILOT_METADATA = Path("results/validation/g2/r3/dev_pilot_run_metadata_r3_v1.json")
FULL_RECORDS = Path("results/validation/g2/r3/conditional_full_grid_records_r3_v1.jsonl")
FULL_METADATA = Path("results/validation/g2/r3/conditional_full_grid_run_metadata_r3_v1.json")
FULL_GRID_MANIFEST = Path("results/validation/g2/r3/full_grid_continuation_manifest_r3_v1.json")
SPEC_LEDGER = Path("results/validation/g2/r3/specification_content_ledger_r3_v1.json")
CHECKER_PATHS = [
    "validation/g2/checker.py", "validation/g2/rational.py", "validation/g2/interval.py",
    "validation/g2/model.py", "validation/g2/hashing.py", "validation/g2/provenance.py",
    "validation/scripts/verify_records_r3.py",
]
RESOURCE_REASONS = {"RATIONAL_BIT_LIMIT", "RATIONAL_OPERATION_LIMIT", "WALL_TIME_LIMIT"}


def load(path: Path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in (ROOT / path).read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_fraction(value: dict | None) -> Fraction | None:
    if not isinstance(value, dict) or set(value) != {"num", "den"}:
        return None
    return Fraction(int(value["num"]), int(value["den"]))


def qobj(value: Fraction) -> dict[str, str]:
    return {"num": str(value.numerator), "den": str(value.denominator)}


def write_new(path: Path, data: bytes) -> None:
    output = ROOT / path
    if output.exists():
        raise SystemExit(f"refusing to overwrite R3 verifier output: {path}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("pilot", "conditional-full-grid"), default="pilot")
    parser.add_argument("--records", action="append", default=None)
    parser.add_argument("--metadata", action="append", default=None)
    parser.add_argument("--report", default=None)
    parser.add_argument("--summary", default=None)
    parser.add_argument("--transitions", default=None)
    parser.add_argument("--action-groups", default=None)
    args = parser.parse_args()

    manifest = load(MANIFEST)
    pilot = load(PILOT_CONFIG)
    benchmark = load(BENCHMARK)
    phase_files = args.records or ([PILOT_RECORDS.as_posix()] if args.phase == "pilot" else [PILOT_RECORDS.as_posix(), FULL_RECORDS.as_posix()])
    metadata_files = args.metadata or ([PILOT_METADATA.as_posix()] if args.phase == "pilot" else [PILOT_METADATA.as_posix(), FULL_METADATA.as_posix()])
    if len(phase_files) != len(metadata_files):
        raise SystemExit("each R3 records file requires its run metadata file")

    current = current_revision()
    checker_status = worktree_status(CHECKER_PATHS)
    checker_sources = source_commitments(current, CHECKER_PATHS)
    frozen_checker = {item["repository_relative_path"]: item["sha256_git_blob_bytes"] for item in manifest["checker_source_commitments"]}
    checker_sources_match = all(frozen_checker.get(item["repository_relative_path"]) == item["sha256_git_blob_bytes"] for item in checker_sources)
    specification_ledger = manifest["specification_content_ledger"]
    on_disk_specification_ledger = load(SPEC_LEDGER)
    specification_ok = (
        on_disk_specification_ledger == specification_ledger
        and specification_ledger.get("specification_bundle_sha256") == manifest["specification_bundle_sha256"]
        and semantic_json_sha256({key: value for key, value in specification_ledger.items() if key != "specification_bundle_sha256"}) == manifest["specification_bundle_sha256"]
        and all(verify_commitment(item) for item in specification_ledger.get("sources", []))
    )
    preeval = load(PREEVAL)
    frozen_hashes_ok = (
        semantic_json_file_sha256(ROOT / PILOT_CONFIG) == manifest["input_hashes"]["pilot_config_semantic_sha256"]
        and semantic_json_file_sha256(ROOT / BENCHMARK) == manifest["input_hashes"]["benchmark_config_semantic_sha256"]
        and semantic_json_file_sha256(ROOT / FULL_GRID_MANIFEST) == manifest["input_hashes"]["conditional_full_grid_manifest_semantic_sha256"]
        and semantic_json_file_sha256(ROOT / SPEC_LEDGER) == manifest["input_hashes"]["specification_content_ledger_semantic_sha256"]
        and semantic_json_file_sha256(ROOT / MANIFEST) == preeval.get("manifest_semantic_sha256")
        and preeval.get("specification_bundle_sha256") == manifest["specification_bundle_sha256"]
        and preeval.get("input_hashes") == manifest["input_hashes"]
        and preeval.get("profile_semantic_sha256") == manifest["profile_semantic_sha256"]
        and preeval.get("conditional_full_grid_manifest_semantic_sha256") == manifest["input_hashes"]["conditional_full_grid_manifest_semantic_sha256"]
        and all(verify_commitment(item) for item in manifest.get("producer_source_commitments", []))
        and all(verify_commitment(item) for item in manifest.get("checker_source_commitments", []))
        and all(verify_commitment(item) for item in manifest.get("input_blob_commitments", {}).values())
    )

    all_records: list[dict] = []
    records_hashes: dict[str, str] = {}
    metadata_by_path: dict[str, dict] = {}
    producer_provenance_ok = True
    metadata_hashes_ok = True
    run_check_details = []
    for records_rel, metadata_rel in zip(phase_files, metadata_files):
        records_path, metadata_path = Path(records_rel), Path(metadata_rel)
        rows = read_jsonl(records_path)
        metadata = load(metadata_path)
        observed_file_counts = Counter(row.get("status", "MISSING_STATUS") for row in rows)
        records_hash = semantic_jsonl_file_sha256(ROOT / records_path)
        records_hashes[records_path.as_posix()] = records_hash
        metadata_by_path[records_path.as_posix()] = metadata
        records_hash_matches = records_hash == metadata.get("records_semantic_sha256")
        if metadata.get("phase_id") == "R3_PILOT_216":
            phase_expected_ids = manifest["selected_query_ids"]
        elif metadata.get("phase_id") == "R3_CONDITIONAL_REMAINING_1728":
            phase_expected_ids = manifest["not_run_query_ids_before_conditional_continuation"]
        else:
            phase_expected_ids = []
        phase_rows_ids = [row.get("query_id") for row in rows]
        phase_selection_pass = (
            len(phase_rows_ids) == len(phase_expected_ids)
            and len(phase_rows_ids) == len(set(phase_rows_ids))
            and set(phase_rows_ids) == set(phase_expected_ids)
            and hashlib.sha256("\n".join(phase_expected_ids).encode("utf-8")).hexdigest() == metadata.get("selection_ids_sha256_lf")
        )
        metadata_matches = (
            metadata.get("specification_bundle_sha256") == manifest["specification_bundle_sha256"]
            and metadata.get("profile_semantic_sha256") == manifest["profile_semantic_sha256"]
            and metadata.get("benchmark_sha256") == manifest["input_hashes"]["benchmark_config_semantic_sha256"]
            and metadata.get("pilot_config_sha256") == manifest["input_hashes"]["pilot_config_semantic_sha256"]
            and metadata.get("development_manifest_sha256") == semantic_json_file_sha256(ROOT / MANIFEST)
            and metadata.get("source_tree_clean_before_run") is True
            and metadata.get("worktree_status_before_run") == []
            and metadata.get("selected_queries") == len(rows)
            and metadata.get("records_semantic_sha256") == records_hash
            and metadata.get("status_counts") == dict(sorted(observed_file_counts.items()))
            and phase_selection_pass
        )
        source_entries = metadata.get("producer_source_commitments", [])
        each_source_ok = all(verify_commitment(item) for item in source_entries)
        manifest_producer = {item["repository_relative_path"]: item["sha256_git_blob_bytes"] for item in manifest["producer_source_commitments"]}
        sources_match_frozen = (
            {item.get("repository_relative_path") for item in source_entries} == set(manifest_producer)
            and all(manifest_producer.get(item.get("repository_relative_path")) == item.get("sha256_git_blob_bytes") for item in source_entries)
            and all(item.get("source_revision") == metadata.get("producer_revision") for item in source_entries)
            and isinstance(metadata.get("actual_argv"), list)
            and metadata.get("actual_argv") == metadata.get("command", metadata.get("actual_argv"))
            and isinstance(metadata.get("python_executable"), str)
            and Path(metadata.get("working_directory", "")).is_absolute()
        )
        producer_ok = each_source_ok and sources_match_frozen and metadata.get("producer_source_commitments_match_frozen_manifest") is True
        producer_provenance_ok &= producer_ok
        metadata_hashes_ok &= records_hash_matches and metadata_matches
        for row in rows:
            row["_source_records_path"] = records_path.as_posix()
            all_records.append(row)
        run_check_details.append({
            "records_path": records_path.as_posix(),
            "metadata_path": metadata_path.as_posix(),
            "record_count": len(rows),
            "phase_id": metadata.get("phase_id"),
            "producer_revision": metadata.get("producer_revision"),
            "records_semantic_sha256": records_hash,
            "records_hash_matches_metadata": records_hash_matches,
            "metadata_hash_bindings_pass": metadata_matches,
            "phase_selection_binding_pass": phase_selection_pass,
            "producer_source_commitments_replay": each_source_ok,
            "producer_source_commitments_match_frozen_manifest": sources_match_frozen,
        })

    id_list = [record.get("query_id") for record in all_records]
    expected_ids = manifest["selected_query_ids"] if args.phase == "pilot" else manifest["original_query_ids"]
    ids_exact = len(id_list) == len(set(id_list)) and set(id_list) == set(expected_ids)
    replay_results = []
    status_counts: Counter[str] = Counter()
    proof_certified = proof_unknown = resource_unknown = invalid_or_failure = 0
    completed_proofs_all_pass = True
    record_integrity_all_pass = True
    replay_by_id = {}
    for record in all_records:
        status_counts[record.get("status", "MISSING_STATUS")] += 1
        records_rel = record["_source_records_path"]
        metadata = metadata_by_path[records_rel]
        status_ok = record.get("status") in {"CERTIFIED", "UNKNOWN"}
        producer_revision_ok = record.get("producer_revision") == metadata.get("producer_revision")
        phase_ok = record.get("evaluation_phase") == metadata.get("phase_id")
        review_status_ok = record.get("review_status") == "PENDING_INDEPENDENT_AUDIT"
        qid = record.get("query_id")
        query = make_query(
            benchmark, qid, pilot["profile"],
            metadata["development_manifest_sha256"], metadata["benchmark_sha256"],
            HASH_PROTOCOL_ID, manifest["specification_bundle_sha256"],
        )
        result = replay_record(record, query)
        result["query_id"] = qid
        result["producer_revision_binding_pass"] = producer_revision_ok
        result["phase_binding_pass"] = phase_ok
        result["review_status_binding_pass"] = review_status_ok
        replay_by_id[qid] = result
        if record.get("proof") is not None:
            if result.get("replayed"):
                if record["status"] == "CERTIFIED":
                    proof_certified += 1
                else:
                    proof_unknown += 1
            else:
                completed_proofs_all_pass = False
                record_integrity_all_pass = False
        elif record.get("status") == "UNKNOWN" and record.get("reason_codes") and set(record["reason_codes"]) <= RESOURCE_REASONS:
            if result.get("record_integrity_valid") and result.get("resource_limited"):
                resource_unknown += 1
            else:
                record_integrity_all_pass = False
        else:
            invalid_or_failure += 1
            record_integrity_all_pass = False
        if not (status_ok and producer_revision_ok and phase_ok and review_status_ok):
            record_integrity_all_pass = False
        replay_results.append(result)

    manifest_checker_paths = {item["repository_relative_path"] for item in manifest["checker_source_commitments"]}
    checker_provenance_pass = (
        checker_sources_match and not checker_status
        and {item["repository_relative_path"] for item in checker_sources} == manifest_checker_paths
    )
    full_worktree_status = worktree_status()
    full_worktree_dirty_only_by_results = bool(full_worktree_status) and all(
        "results/validation/g2/r3/" in line.replace("\\", "/") for line in full_worktree_status
    )
    provenance_pass = specification_ok and frozen_hashes_ok and metadata_hashes_ok and producer_provenance_ok and checker_provenance_pass
    all_pass = ids_exact and provenance_pass and record_integrity_all_pass and completed_proofs_all_pass and invalid_or_failure == 0
    pilot_conditions = (
        args.phase == "pilot" and all_pass and resource_unknown == 0
        and status_counts.get("INVALID_INPUT", 0) == 0 and status_counts.get("EXECUTION_FAILURE", 0) == 0
        and len(all_records) == 216 and proof_certified + proof_unknown == 216
    )

    r2_by_id = {row["query_id"]: row for row in read_jsonl(R2_RECORDS)}
    transition_rows = []
    for record in sorted(all_records, key=lambda item: item["query_id"]):
        old = r2_by_id.get(record["query_id"])
        new_margin = record.get("collision_margin_lower", [None])[0]
        old_margin = old.get("collision_margin_lower", [None])[0] if old else None
        diagnostic = record.get("resource_diagnostic", {}).get("failure", {})
        transition_rows.append({
            "query_id": record["query_id"],
            "evaluation_phase": record.get("evaluation_phase"),
            "r2_status": old.get("status") if old else "NOT_RUN",
            "r2_reason_codes": old.get("reason_codes") if old else ["NOT_RUN_IN_R2"],
            "r2_collision_margin_lower": old_margin,
            "r3_status": record.get("status"),
            "r3_reason_codes": record.get("reason_codes"),
            "r3_collision_margin_lower": new_margin,
            "r3_resource_stage": diagnostic.get("stage_id"),
            "r3_resource_primitive": diagnostic.get("primitive_id"),
            "r3_resource_estimate_bits": diagnostic.get("estimated_or_observed_bits"),
            "r3_replay_result": replay_by_id[record["query_id"]],
        })

    groups: dict[str, list[dict]] = defaultdict(list)
    for record in all_records:
        key = "__".join(record["query_id"].split("__")[:3])
        groups[key].append(record)
    group_rows = []
    for group_id, rows in sorted(groups.items()):
        rows = sorted(rows, key=lambda item: item["query_id"])
        collision_values = [parse_fraction(row["collision_margin_lower"][0]) for row in rows if row.get("collision_margin_lower")]
        contact_values = [parse_fraction(row["contact_margin_lower"]) for row in rows if row.get("contact_margin_lower")]
        action_status = {row["action_id"]: row["status"] for row in rows}
        group_counts = Counter(row["status"] for row in rows)
        group_rows.append({
            "state_scene_horizon_group_id": group_id,
            "query_count": len(rows),
            "action_count": len(action_status),
            "action_status_vector": action_status,
            "status_counts": dict(sorted(group_counts.items())),
            "mixed_certified_and_noncertified_statuses": bool(group_counts.get("CERTIFIED", 0) and sum(group_counts.values()) > group_counts.get("CERTIFIED", 0)),
            "resource_censored_action_count": sum(1 for row in rows if row.get("proof") is None and row.get("status") == "UNKNOWN"),
            "collision_margin_lower_range": {
                "completed_action_count": len(collision_values),
                "minimum": qobj(min(collision_values)) if collision_values else None,
                "maximum": qobj(max(collision_values)) if collision_values else None,
            },
            "contact_margin_lower_range": {
                "completed_action_count": len(contact_values),
                "minimum": qobj(min(contact_values)) if contact_values else None,
                "maximum": qobj(max(contact_values)) if contact_values else None,
            },
        })

    evaluated = len(all_records)
    summary = {
        "schema": "ddwmr-g2-development-pilot-summary-r3-v1" if args.phase == "pilot" else "ddwmr-g2-development-full-grid-summary-r3-v1",
        "phase": args.phase,
        "method_id": manifest["method_id"],
        "distance_method_id": manifest["distance_method_id"],
        "distance_rounding_precision_bits": manifest["distance_rounding_precision_bits"],
        "specification_bundle_sha256": manifest["specification_bundle_sha256"],
        "original_query_universe": 1944,
        "evaluated_query_count": evaluated,
        "not_run_query_count_after_phase": 1944 - evaluated,
        "status_counts": dict(sorted(status_counts.items())),
        "proof_certified_count": proof_certified,
        "proof_complete_unknown_count": proof_unknown,
        "resource_unknown_count": resource_unknown,
        "invalid_or_execution_failure_count": invalid_or_failure,
        "state_scene_horizon_group_count": len(group_rows),
        "groups_with_at_least_one_certified_action": sum(1 for row in group_rows if row["status_counts"].get("CERTIFIED", 0)),
        "groups_with_mixed_certificate_status": sum(1 for row in group_rows if row["mixed_certified_and_noncertified_statuses"]),
        "records_file_hashes": records_hashes,
        "replay_counts": {
            "completed_proofs": proof_certified + proof_unknown,
            "replayed_proofs": sum(1 for row in replay_results if row.get("proof_replay_pass")),
            "resource_record_integrity_only": resource_unknown,
        },
    }
    report = {
        "schema": "ddwmr-g2-record-check-r3-v1",
        "phase": args.phase,
        "checker_revision": current,
        "checker_command": list(getattr(sys, "orig_argv", [sys.executable, *sys.argv])),
        "checker_environment": sys.version,
        "checker_source_commitments": checker_sources,
        "checker_source_commitments_match_frozen_manifest": checker_sources_match,
        "checker_source_worktree_status": checker_status,
        "checker_full_worktree_status": full_worktree_status,
        "checker_full_worktree_dirty_only_by_r3_evidence_outputs": full_worktree_dirty_only_by_results,
        "specification_bundle_sha256": manifest["specification_bundle_sha256"],
        "profile_semantic_sha256": manifest["profile_semantic_sha256"],
        "frozen_manifest_semantic_sha256": semantic_json_file_sha256(ROOT / MANIFEST),
        "specification_blob_commitments_pass": specification_ok,
        "frozen_input_hashes_pass": frozen_hashes_ok,
        "producer_metadata_hash_and_source_checks": run_check_details,
        "producer_provenance_pass": producer_provenance_ok,
        "records_hash_and_metadata_bindings_pass": metadata_hashes_ok,
        "checker_provenance_pass": checker_provenance_pass,
        "query_id_coverage_exact": ids_exact,
        "expected_query_count": len(expected_ids),
        "actual_query_count": len(all_records),
        "duplicate_or_missing_query_ids": not ids_exact,
        "record_integrity_pass": record_integrity_all_pass,
        "completed_proof_replay_pass": completed_proofs_all_pass,
        "status_counts": dict(sorted(status_counts.items())),
        "proof_certified_count": proof_certified,
        "proof_complete_unknown_count": proof_unknown,
        "resource_unknown_integrity_only_count": resource_unknown,
        "invalid_or_execution_failure_count": invalid_or_failure,
        "replay_results": replay_results,
        "all_pass": all_pass,
        "continuation_allowed": bool(pilot_conditions),
        "continuation_decision": (
            "ALLOW_ONE_FROZEN_1728_QUERY_RUN" if pilot_conditions
            else "STOP; KEEP_1728_NOT_RUN"
        ) if args.phase == "pilot" else "NOT_APPLICABLE_AFTER_SINGLE_CONTINUATION",
    }

    if args.phase == "pilot":
        defaults = {
            "report": "results/validation/g2/r3/dev_pilot_record_check_r3_v1.json",
            "summary": "results/validation/g2/r3/dev_pilot_summary_r3_v1.json",
            "transitions": "results/validation/g2/r3/r2_to_r3_query_transitions_r3_v1.jsonl",
            "action_groups": "results/validation/g2/r3/action_group_summary_r3_v1.json",
        }
    else:
        defaults = {
            "report": "results/validation/g2/r3/full_grid_record_check_r3_v1.json",
            "summary": "results/validation/g2/r3/full_grid_summary_r3_v1.json",
            "transitions": "results/validation/g2/r3/r2_to_r3_full_grid_transitions_r3_v1.jsonl",
            "action_groups": "results/validation/g2/r3/full_grid_action_group_summary_r3_v1.json",
        }
    transition_bytes = b"".join((json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8") for row in transition_rows)
    write_new(Path(args.report or defaults["report"]), json_bytes(report))
    write_new(Path(args.summary or defaults["summary"]), json_bytes(summary))
    write_new(Path(args.transitions or defaults["transitions"]), transition_bytes)
    write_new(Path(args.action_groups or defaults["action_groups"]), json_bytes({
        "schema": "ddwmr-g2-r3-action-group-summary-v1",
        "phase": args.phase,
        "group_count": len(group_rows),
        "groups": group_rows,
    }))
    print(json.dumps({
        "phase": args.phase,
        "all_pass": all_pass,
        "continuation_allowed": report["continuation_allowed"],
        "status_counts": report["status_counts"],
        "proof_certified": proof_certified,
        "proof_complete_unknown": proof_unknown,
        "resource_unknown": resource_unknown,
        "invalid_or_execution_failure": invalid_or_failure,
        "checker_revision": current,
        "report": str(ROOT / (args.report or defaults["report"])),
    }, sort_keys=True))
    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
