"""Select, replay, and adapt one frozen archived R3 proof without rerunning R3.

The `select` stage must finish and write its selection record before the
`adapt` stage is invoked. This makes the frozen query ID and record hashes
reviewable before any common-check result is produced.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

from validation.g2.checker import replay_record
from validation.g2.evaluator import canonical_hash, make_query, query_hash_payload
from validation.g2.hashing import (
    HASH_PROTOCOL_ID, canonical_json_bytes, semantic_json_file_sha256,
    semantic_json_sha256,
)
from validation.g2.model import build_model
from validation.g2.rational import Budget, Interval, parse_q
from validation.g4.common_tube import (
    TubeSegment, check_tube_segments, r3_record_to_common_segment,
    replay_common_check_record,
)


ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = Path("results/validation/g2/r3/conditional_full_grid_records_r3_v1.jsonl.gz")
ARCHIVE_MANIFEST = Path("results/validation/g2/r3/conditional_full_grid_archive_manifest_r3_v1.json")
RUN_METADATA = Path("results/validation/g2/r3/conditional_full_grid_run_metadata_r3_v1.json")
DEVELOPMENT_MANIFEST = Path("results/validation/g2/r3/development_manifest_r3_v1.json")
FULL_GRID_MANIFEST = Path("results/validation/g2/r3/full_grid_continuation_manifest_r3_v1.json")
BENCHMARK = Path("validation/configs/benchmark_v1.json")
COMMON_PROFILE = Path("validation/g4/r3_common_adapter_profile_v4.json")


def _load(path: Path) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_new(path: Path, value: Any) -> None:
    output = path if path.is_absolute() else ROOT / path
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing R3 adapter evidence: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes((json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))


def _snapshot_manifest_sha256() -> str | None:
    manifest_path = ROOT.parent / "snapshot_manifest.json"
    sidecar_path = ROOT.parent / "snapshot_manifest.sha256"
    if not manifest_path.is_file() or not sidecar_path.is_file():
        return None
    manifest_hash = _sha256_file(manifest_path)
    if sidecar_path.read_text(encoding="ascii").split()[0] != manifest_hash:
        raise SystemExit("source snapshot manifest sidecar does not match its exact bytes")
    return manifest_hash


def _load_common_profile(path: Path) -> tuple[dict[str, Any], str]:
    profile_path = path if path.is_absolute() else ROOT / path
    profile_bytes = profile_path.read_bytes()
    profile = json.loads(profile_bytes.decode("utf-8"))
    if profile.get("schema") != "ddwmr-g4-r3-common-adapter-profile-v1":
        raise SystemExit("unsupported single-record common adapter profile")
    for key in ("max_rational_bits", "max_rational_operations", "sqrt_bisections", "max_integer_string_digits"):
        if not isinstance(profile.get(key), int) or isinstance(profile.get(key), bool) or profile[key] <= 0:
            raise SystemExit(f"common adapter profile has an invalid {key}")
    if profile["sqrt_bisections"] > 256:
        raise SystemExit("common adapter sqrt bisection cap exceeds the checker limit")
    wall = profile.get("wall_seconds")
    if not isinstance(wall, int) or isinstance(wall, bool) or wall <= 0:
        raise SystemExit("common adapter wall cap must be a positive integer")
    required_digits = (profile["max_rational_bits"] * 30103 + 99999) // 100000 + 1
    if profile["max_integer_string_digits"] < required_digits:
        raise SystemExit("integer serialization digit cap cannot represent every configured rational endpoint")
    return profile, _sha256_bytes(profile_bytes)


def _frozen_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    archive_manifest = _load(ARCHIVE_MANIFEST)
    run_metadata = _load(RUN_METADATA)
    development_manifest = _load(DEVELOPMENT_MANIFEST)
    full_grid_manifest = _load(FULL_GRID_MANIFEST)
    benchmark = _load(BENCHMARK)

    archive_path = ROOT / ARCHIVE
    actual_archive_hash = _sha256_file(archive_path)
    expected_archive_hash = archive_manifest.get("archive_raw_bytes_sha256")
    if actual_archive_hash != expected_archive_hash or archive_path.stat().st_size != archive_manifest.get("archive_bytes"):
        raise SystemExit("frozen R3 compressed archive hash/size mismatch")
    if archive_manifest.get("record_count") != 1728 or run_metadata.get("selected_queries") != 1728:
        raise SystemExit("frozen R3 conditional archive is not the declared 1,728-record continuation")
    if run_metadata.get("phase_id") != archive_manifest.get("phase_id"):
        raise SystemExit("R3 run metadata and archive phase IDs differ")
    if run_metadata.get("records_semantic_sha256") != archive_manifest.get("source_semantic_sha256"):
        raise SystemExit("R3 producer and archive semantic hashes differ")

    benchmark_hash = semantic_json_file_sha256(ROOT / BENCHMARK)
    manifest_hash = semantic_json_file_sha256(ROOT / DEVELOPMENT_MANIFEST)
    profile_hash = semantic_json_sha256(development_manifest["profile"])
    expected_hashes = development_manifest["input_hashes"]
    if benchmark_hash != expected_hashes.get("benchmark_config_semantic_sha256"):
        raise SystemExit("benchmark configuration differs from the frozen R3 manifest")
    if manifest_hash != run_metadata.get("development_manifest_sha256"):
        raise SystemExit("R3 run metadata is not bound to the current frozen development manifest")
    if benchmark_hash != run_metadata.get("benchmark_sha256"):
        raise SystemExit("R3 run metadata is not bound to the current benchmark")
    if profile_hash != development_manifest.get("profile_semantic_sha256"):
        raise SystemExit("R3 profile semantic hash mismatch")
    if run_metadata.get("profile_semantic_sha256") != profile_hash:
        raise SystemExit("R3 run metadata and development profile differ")

    frozen_ids = development_manifest.get("not_run_query_ids_before_conditional_continuation")
    if (not isinstance(frozen_ids, list) or len(frozen_ids) != 1728 or
            frozen_ids != full_grid_manifest.get("selected_query_ids")):
        raise SystemExit("conditional R3 ID order differs from the frozen continuation manifest")
    if run_metadata.get("selection_ids_sha256_lf") != hashlib.sha256("\n".join(frozen_ids).encode("utf-8")).hexdigest():
        raise SystemExit("R3 frozen continuation ID-order digest mismatch")
    return archive_manifest, run_metadata, development_manifest, full_grid_manifest, benchmark


def _read_and_verify_archive(
    archive_manifest: dict[str, Any], development_manifest: dict[str, Any],
) -> tuple[dict[str, tuple[dict[str, Any], str, str, int]], dict[str, Any]]:
    semantic_digest = hashlib.sha256()
    raw_digest = hashlib.sha256()
    raw_bytes = 0
    rows: dict[str, tuple[dict[str, Any], str, str, int]] = {}
    with gzip.open(ROOT / ARCHIVE, "rb") as stream:
        for line_index, raw_line in enumerate(stream):
            raw_digest.update(raw_line)
            raw_bytes += len(raw_line)
            payload = raw_line.rstrip(b"\r\n")
            if not payload.strip():
                continue
            record = json.loads(payload.decode("utf-8"))
            semantic_digest.update(canonical_json_bytes(record) + b"\n")
            query_id = record.get("query_id")
            if not isinstance(query_id, str) or query_id in rows:
                raise SystemExit("archived R3 JSONL contains a missing or duplicate query ID")
            rows[query_id] = (record, semantic_json_sha256(record), _sha256_bytes(payload), line_index)
    if len(rows) != archive_manifest.get("record_count"):
        raise SystemExit("R3 archive record count does not match its frozen manifest")
    if raw_bytes != archive_manifest.get("source_bytes"):
        raise SystemExit("decompressed R3 archive byte count mismatch")
    if raw_digest.hexdigest() != archive_manifest.get("source_raw_bytes_sha256"):
        raise SystemExit("decompressed R3 archive raw-byte hash mismatch")
    if semantic_digest.hexdigest() != archive_manifest.get("source_semantic_sha256"):
        raise SystemExit("decompressed R3 archive semantic hash mismatch")
    frozen_ids = development_manifest["not_run_query_ids_before_conditional_continuation"]
    if set(rows) != set(frozen_ids):
        raise SystemExit("R3 archive IDs are not exactly the frozen continuation universe")
    details = {
        "archive_path": ARCHIVE.as_posix(),
        "compressed_sha256": archive_manifest["archive_raw_bytes_sha256"],
        "decompressed_raw_sha256": raw_digest.hexdigest(),
        "semantic_sha256": semantic_digest.hexdigest(),
        "record_count": len(rows),
    }
    return rows, details


def _query_for(query_id: str, development_manifest: dict[str, Any], benchmark: dict[str, Any]) -> dict[str, Any]:
    return make_query(
        benchmark, query_id, development_manifest["profile"],
        semantic_json_file_sha256(ROOT / DEVELOPMENT_MANIFEST),
        semantic_json_file_sha256(ROOT / BENCHMARK),
        HASH_PROTOCOL_ID, development_manifest["specification_bundle_sha256"],
    )


def select_first_replayable(output_path: Path) -> None:
    archive_manifest, _, development_manifest, _, benchmark = _frozen_inputs()
    rows, archive_facts = _read_and_verify_archive(archive_manifest, development_manifest)
    skipped: list[dict[str, Any]] = []
    selected = None
    for frozen_index, query_id in enumerate(development_manifest["not_run_query_ids_before_conditional_continuation"]):
        record, record_hash, line_hash, archive_index = rows[query_id]
        if not isinstance(record.get("proof"), dict):
            skipped.append({"query_id": query_id, "reason": "no_native_proof_object"})
            continue
        query = _query_for(query_id, development_manifest, benchmark)
        expected_input_hash = canonical_hash(query_hash_payload(query))
        if record.get("input_sha256") != expected_input_hash:
            replay = {"replayed": False, "reason": "frozen_query_input_digest_mismatch"}
        else:
            replay = replay_record(record, query)
        if replay.get("replayed"):
            selected = {
                "query_id": query_id,
                "frozen_continuation_index_zero_based": frozen_index,
                "archive_line_index_zero_based": archive_index,
                "record_semantic_sha256": record_hash,
                "record_line_bytes_sha256": line_hash,
                "query_input_sha256": expected_input_hash,
                "method_id": record.get("method_id"),
                "native_status": record.get("status"),
                "native_record_status": record.get("status"),
                "native_record_reason_codes": record.get("reason_codes", []),
                "native_margins": {
                    "collision_margin": replay.get("collision_margin"),
                    "contact_margin": replay.get("contact_margin"),
                },
                "native_work": {
                    "producer_rational_operations": record.get("work", {}).get("rational_operations"),
                    "producer_max_rational_bits": record.get("work", {}).get("max_rational_bits"),
                    "checker_operations": replay.get("checker_operations"),
                },
                "native_replay": replay,
                "query_binding": {
                    "state_cell": query["state_cell"],
                    "scene": query["scene"],
                    "horizon": query["horizon"],
                    "action": query["action"],
                    "parameter_cell": query["parameter_cell"],
                },
            }
            break
        skipped.append({
            "query_id": query_id,
            "reason": "proof_present_but_native_replay_failed",
            "replay_result": replay,
        })
    if selected is None:
        raise SystemExit("no replayable native proof found in the frozen R3 archive")
    result = {
        "schema": "ddwmr-g4-r3-archived-fixture-selection-v1",
        "selection_rule": "first proof-bearing record in frozen R3 continuation ID order whose canonical input binding and independent native proof replay pass",
        "archive": archive_facts,
        "development_manifest_semantic_sha256": semantic_json_file_sha256(ROOT / DEVELOPMENT_MANIFEST),
        "benchmark_semantic_sha256": semantic_json_file_sha256(ROOT / BENCHMARK),
        "profile_semantic_sha256": semantic_json_sha256(development_manifest["profile"]),
        "source_snapshot_manifest_sha256": _snapshot_manifest_sha256(),
        "skipped_prior_candidates": skipped,
        "selected": selected,
        "common_check_generated": False,
    }
    _write_new(output_path, result)
    print(json.dumps({
        "stage": "select",
        "query_id": selected["query_id"],
        "record_semantic_sha256": selected["record_semantic_sha256"],
        "record_line_bytes_sha256": selected["record_line_bytes_sha256"],
        "native_replay": selected["native_replay"],
        "selection_file": str(output_path if output_path.is_absolute() else ROOT / output_path),
        "common_check_generated": False,
    }, sort_keys=True))


def _load_selected_record(selection_path: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    selection_file = selection_path if selection_path.is_absolute() else ROOT / selection_path
    selection_bytes = selection_file.read_bytes()
    selection = json.loads(selection_bytes.decode("utf-8"))
    if selection.get("schema") != "ddwmr-g4-r3-archived-fixture-selection-v1" or selection.get("common_check_generated") is not False:
        raise SystemExit("adapt stage requires the frozen selection artifact from the select-only stage")
    archive_manifest, run_metadata, development_manifest, _, benchmark = _frozen_inputs()
    if selection.get("archive", {}).get("semantic_sha256") != archive_manifest.get("source_semantic_sha256"):
        raise SystemExit("selection artifact is bound to a different R3 archive")
    if selection.get("development_manifest_semantic_sha256") != semantic_json_file_sha256(ROOT / DEVELOPMENT_MANIFEST):
        raise SystemExit("selection artifact is bound to a different R3 manifest")
    if selection.get("source_snapshot_manifest_sha256") != _snapshot_manifest_sha256():
        raise SystemExit("selection artifact was not made from this frozen source snapshot")
    rows, archive_facts = _read_and_verify_archive(archive_manifest, development_manifest)
    selected_meta = selection.get("selected", {})
    query_id = selected_meta.get("query_id")
    if query_id not in rows:
        raise SystemExit("selected R3 query ID is absent from the frozen archive")
    record, record_hash, line_hash, line_index = rows[query_id]
    if (record_hash != selected_meta.get("record_semantic_sha256") or
            line_hash != selected_meta.get("record_line_bytes_sha256") or
            line_index != selected_meta.get("archive_line_index_zero_based")):
        raise SystemExit("selected R3 record bytes changed after the selection was frozen")
    query = _query_for(query_id, development_manifest, benchmark)
    if canonical_hash(query_hash_payload(query)) != selected_meta.get("query_input_sha256"):
        raise SystemExit("selected query canonical input digest changed")
    replay = replay_record(record, query)
    if not replay.get("replayed"):
        raise SystemExit("selected R3 proof no longer replays before common adaptation")
    return selection, record, query, replay, archive_facts, development_manifest, benchmark


def _compose_r3_record(
    selection: dict[str, Any], record: dict[str, Any], query: dict[str, Any],
    segment: TubeSegment, common: dict[str, Any], development_manifest: dict[str, Any],
    archive_facts: dict[str, Any], source_snapshot_sha256: str,
    common_profile: dict[str, Any], common_profile_sha256: str,
) -> dict[str, Any]:
    selected = selection["selected"]
    return {
        "schema": "ddwmr-g4-r3-proof-tube-composition-v1",
        "query_binding": {
            "query_id": query["query_id"],
            "input_sha256": selected["query_input_sha256"],
            "action_id": query["action"]["id"],
            "held_voltage": query["action"]["V"],
            "initial_state_box": query["state_cell"]["box"],
            "fixed_parameter_label_image": query["benchmark"]["parameter_cell"],
            "horizon": query["horizon"],
        },
        "method_binding": {
            "method_id": record["method_id"],
            "specification_bundle_sha256": development_manifest["specification_bundle_sha256"],
            "profile_id": development_manifest["profile"]["id"],
            "profile_semantic_sha256": semantic_json_sha256(development_manifest["profile"]),
            "development_manifest_semantic_sha256": semantic_json_file_sha256(ROOT / DEVELOPMENT_MANIFEST),
            "source_snapshot_manifest_sha256": source_snapshot_sha256,
        },
        "arithmetic_binding": {
            "backend_id": "R3_FROZEN_EXACT_RATIONAL_TAYLOR_INTERVAL_SOURCE_SET",
            "source_revision": record.get("producer_revision"),
            "checker_id": "validation.g2.checker.replay_record",
            "checker_source_commitments": development_manifest["checker_source_commitments"],
            "native_proof_replay": "PASS",
        },
        "resource_binding": {
            "native_r3_profile_id": development_manifest["profile"]["id"],
            "native_r3_profile_semantic_sha256": semantic_json_sha256(development_manifest["profile"]),
            "common_adapter_profile_id": common_profile["profile_id"],
            "common_adapter_profile_sha256": common_profile_sha256,
            "common_adapter_limits": {
                "max_rational_bits": common_profile["max_rational_bits"],
                "max_rational_operations": common_profile["max_rational_operations"],
                "wall_seconds": common_profile["wall_seconds"],
                "sqrt_bisections": common_profile["sqrt_bisections"],
                "max_integer_string_digits": common_profile["max_integer_string_digits"],
            },
        },
        "source_binding": {
            "archive_path": archive_facts["archive_path"],
            "archive_compressed_sha256": archive_facts["compressed_sha256"],
            "record_semantic_sha256": selected["record_semantic_sha256"],
            "record_line_bytes_sha256": selected["record_line_bytes_sha256"],
            "archive_semantic_sha256": archive_facts["semantic_sha256"],
        },
        "native_record": record,
        "segments": [segment.to_json()],
        "common_check": common,
    }


def _replay_r3_composition(
    composition: dict[str, Any], record: dict[str, Any], query: dict[str, Any],
    development_manifest: dict[str, Any], benchmark: dict[str, Any],
    archive_facts: dict[str, Any], selected: dict[str, Any],
    source_snapshot_sha256: str, common_profile: dict[str, Any], common_profile_sha256: str,
) -> tuple[bool, str]:
    try:
        if composition.get("schema") != "ddwmr-g4-r3-proof-tube-composition-v1":
            return False, "composition_schema_mismatch"
        budget = _new_common_budget(common_profile)
        adapter_segment = r3_record_to_common_segment(record, query, budget)
        _reset_budget_work(budget)
        model = build_model(benchmark, budget)
        segment = TubeSegment.from_json(adapter_segment.to_json(), model.parameter_label_order, budget)
        expected_binding = _compose_r3_record(
            {"selected": selected}, record, query,
            segment,
            composition["common_check"], development_manifest, archive_facts,
            source_snapshot_sha256, common_profile, common_profile_sha256,
        )
        for key in ("query_binding", "method_binding", "arithmetic_binding", "resource_binding", "source_binding", "native_record", "segments"):
            if composition.get(key) != expected_binding.get(key):
                return False, f"composition_{key}_mismatch"
        native = replay_record(record, query)
        if not native.get("replayed"):
            return False, "native_proof_replay_failed"
        initial_state = tuple(Interval.from_json(item, budget) for item in query["state_cell"]["box"])
        expected_common = check_tube_segments(
            (segment,), benchmark, query["scene"], parse_q(query["horizon"]["T"], budget), budget,
            initial_state=initial_state,
            sqrt_bisections=common_profile["sqrt_bisections"],
        )
        if composition.get("common_check") != expected_common:
            return False, "common_check_not_bound_to_replayed_segment"
        common_replay = replay_common_check_record(
            composition["common_check"], benchmark, query["scene"], _new_common_budget(common_profile),
            sqrt_bisections=common_profile["sqrt_bisections"],
        )
        if not common_replay.get("replayed"):
            return False, "common_check_replay_failed"
        return True, "replayed"
    except Exception as exc:
        return False, f"invalid_composition:{type(exc).__name__}:{exc}"


def _new_budget(development_manifest: dict[str, Any]) -> Budget:
    profile = development_manifest["profile"]
    wall = parse_q(profile["wall_seconds_per_query"])
    return Budget(profile["max_rational_bits"], profile["max_rational_operations"], wall)


def _new_common_budget(common_profile: dict[str, Any]) -> Budget:
    return Budget(
        common_profile["max_rational_bits"], common_profile["max_rational_operations"],
        Fraction(common_profile["wall_seconds"]),
    )


def _budget_work_summary(budget: Budget) -> dict[str, int]:
    return {
        "operation_attempts": budget.operation_attempts,
        "operations_started": budget.operations,
        "completed_results": budget.completed_results,
        "max_observed_bits": budget.max_seen_bits,
        "max_completed_result_bits": budget.max_completed_result_bits,
        "max_preoperation_estimate_bits": budget.max_preoperation_estimate_bits,
    }


def _reset_budget_work(budget: Budget) -> None:
    """Separate adapter conversion work from replayable common-check work."""
    budget.operations = 0
    budget.operation_attempts = 0
    budget.completed_results = 0
    budget.max_seen_bits = 0
    budget.max_completed_result_bits = 0
    budget.max_preoperation_estimate_bits = 0
    budget.failure_context = None
    budget.stage_id = "common_tube.replay"


def _tamper_rejections(
    composition: dict[str, Any], record: dict[str, Any], query: dict[str, Any],
    development_manifest: dict[str, Any], benchmark: dict[str, Any],
    archive_facts: dict[str, Any], selected: dict[str, Any],
    source_snapshot_sha256: str, common_profile: dict[str, Any], common_profile_sha256: str,
) -> dict[str, Any]:
    cases: dict[str, dict[str, Any]] = {}

    action = copy.deepcopy(composition)
    action["query_binding"]["held_voltage"][0] = {"num": "0", "den": "1"}
    cases["action_or_held_voltage"] = action

    proof_hash = copy.deepcopy(composition)
    proof_hash["source_binding"]["record_semantic_sha256"] = "0" * 64
    cases["native_proof_digest"] = proof_hash

    endpoint = copy.deepcopy(composition)
    endpoint["segments"][0]["endpoint_end"]["state_hull"][0][0]["num"] = "999999"
    cases["certified_endpoint"] = endpoint

    radius_mode = copy.deepcopy(composition)
    radius_mode["segments"][0]["radius_expansion_mode"] = "NATIVE_TOTAL_HULL"
    cases["radius_mode"] = radius_mode

    one_segment = copy.deepcopy(composition)
    one_segment["segments"][0]["state_hull"][0][0]["num"] = "999999"
    cases["segment_hull"] = one_segment

    results = {}
    for name, candidate in cases.items():
        replayed, reason = _replay_r3_composition(
            candidate, record, query, development_manifest, benchmark,
            archive_facts, selected, source_snapshot_sha256,
            common_profile, common_profile_sha256,
        )
        results[name] = {"rejected": not replayed, "reason": reason}
    return {
        "tamper_case_count": len(results),
        "all_tampered_compositions_rejected": all(item["rejected"] for item in results.values()),
        "cases": results,
    }


def adapt_selected(selection_path: Path, output_path: Path, common_profile_path: Path) -> None:
    selection, record, query, native_replay, archive_facts, development_manifest, benchmark = _load_selected_record(selection_path)
    source_snapshot_sha256 = _snapshot_manifest_sha256()
    if source_snapshot_sha256 is None:
        raise SystemExit("adapter run must execute from a hash-bound local source snapshot")
    common_profile, common_profile_sha256 = _load_common_profile(common_profile_path)
    if not hasattr(sys, "set_int_max_str_digits"):
        raise SystemExit("pinned Python runtime lacks the declared bounded integer serialization control")
    sys.set_int_max_str_digits(common_profile["max_integer_string_digits"])
    budget = _new_common_budget(common_profile)
    adapter_segment = r3_record_to_common_segment(record, query, budget)
    adapter_work = _budget_work_summary(budget)
    _reset_budget_work(budget)
    model = build_model(benchmark, budget)
    segment = TubeSegment.from_json(adapter_segment.to_json(), model.parameter_label_order, budget)
    initial_state = tuple(Interval.from_json(item, budget) for item in query["state_cell"]["box"])
    horizon = parse_q(query["horizon"]["T"], budget)
    common = check_tube_segments(
        (segment,), benchmark, query["scene"], horizon, budget,
        initial_state=initial_state,
        sqrt_bisections=common_profile["sqrt_bisections"],
    )
    replay_budget = _new_common_budget(common_profile)
    common_replay = replay_common_check_record(
        common, benchmark, query["scene"], replay_budget,
        sqrt_bisections=common_profile["sqrt_bisections"],
    )
    if not common_replay.get("replayed"):
        raise SystemExit(f"shared common-check result failed independent record replay: {common_replay}")
    composition = _compose_r3_record(
        selection, record, query, segment, common, development_manifest, archive_facts,
        source_snapshot_sha256, common_profile, common_profile_sha256,
    )
    composition_replay, composition_reason = _replay_r3_composition(
        composition, record, query, development_manifest, benchmark,
        archive_facts, selection["selected"], source_snapshot_sha256,
        common_profile, common_profile_sha256,
    )
    if not composition_replay:
        raise SystemExit(f"R3 native-to-common composition failed replay: {composition_reason}")
    tamper = _tamper_rejections(
        composition, record, query, development_manifest, benchmark,
        archive_facts, selection["selected"], source_snapshot_sha256,
        common_profile, common_profile_sha256,
    )
    if not tamper["all_tampered_compositions_rejected"]:
        raise SystemExit("at least one tampered R3 proof-to-tube composition was accepted")
    result = {
        "schema": "ddwmr-g4-r3-archived-adapter-fixture-v1",
        "selection_artifact_path": str(selection_path),
        "selection_artifact_sha256": _sha256_file(selection_path if selection_path.is_absolute() else ROOT / selection_path),
        "selected_query_id": selection["selected"]["query_id"],
        "selected_record_semantic_sha256": selection["selected"]["record_semantic_sha256"],
        "selected_record_line_bytes_sha256": selection["selected"]["record_line_bytes_sha256"],
        "native_result": {
            "status": record["status"],
            "reason_codes": record.get("reason_codes", []),
            "replayed": native_replay["replayed"],
            "proof_replay_pass": native_replay.get("proof_replay_pass"),
            "collision_margin": native_replay.get("collision_margin"),
            "contact_margin": native_replay.get("contact_margin"),
            "producer_work": record.get("work"),
            "checker_operations": native_replay.get("checker_operations"),
        },
        "common_adapter": {
            "resource_profile": common_profile,
            "resource_profile_sha256": common_profile_sha256,
            "adapter_conversion_work": adapter_work,
            "segment": segment.to_json(),
            "predicate_status": common["predicate_status"],
            "certificate_emitted": common["certificate_emitted"],
            "ode_tube_proof_replayed": common["ode_tube_proof_replayed"],
            "closed_time_coverage": common["full_closed_hold_covered"],
            "segment_checks": common["segment_checks"],
            "work": common["work"],
            "check_record_sha256": semantic_json_sha256(common),
            "replay": common_replay,
        },
        "proof_to_common_composition": {
            "record": composition,
            "replayed": composition_replay,
            "reason": composition_reason,
            "tamper_rejection": tamper,
        },
        "batch_comparison_queries_run": 0,
        "r3_native_records_rerun": 0,
    }
    _write_new(output_path, result)
    print(json.dumps({
        "stage": "adapt",
        "query_id": result["selected_query_id"],
        "native_status": result["native_result"]["status"],
        "native_proof_replay": result["native_result"]["proof_replay_pass"],
        "common_status": result["common_adapter"]["predicate_status"],
        "tamper_rejections_pass": tamper["all_tampered_compositions_rejected"],
        "output": str(output_path if output_path.is_absolute() else ROOT / output_path),
        "batch_comparison_queries_run": 0,
    }, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="stage", required=True)
    select_parser = subparsers.add_parser("select")
    select_parser.add_argument(
        "--output", type=Path,
        default=Path("results/validation/g4/auer2013/r3_archived_fixture_selection_v1.json"),
    )
    adapt_parser = subparsers.add_parser("adapt")
    adapt_parser.add_argument(
        "--selection", type=Path,
        default=Path("results/validation/g4/auer2013/r3_archived_fixture_selection_v1.json"),
    )
    adapt_parser.add_argument(
        "--output", type=Path,
        default=Path("results/validation/g4/auer2013/r3_archived_adapter_fixture_v1.json"),
    )
    adapt_parser.add_argument("--common-profile", type=Path, default=COMMON_PROFILE)
    args = parser.parse_args()
    if args.stage == "select":
        select_first_replayable(args.output)
    else:
        adapt_selected(args.selection, args.output, args.common_profile)


if __name__ == "__main__":
    main()
