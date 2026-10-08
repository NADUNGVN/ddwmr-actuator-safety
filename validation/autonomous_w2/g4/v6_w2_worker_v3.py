"""Frozen W2 v3 worker. Setup validation is shared with its nonquery audit."""
from __future__ import annotations

import argparse
import json
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

from validation.g2.rational import Budget, InvalidInput, ResourceLimit
from validation.autonomous_w2.g4.matched_v6_common_v3 import (
    PLAN_REL, PROJECT, canonical_sha256, configure_integer_string_limit, initial_state_from_task,
    load_authoritative_freeze, scene_from_task, score_serialize_replay_progress,
    sha256_file, strict_json, summarize_common, verify_source_closure, write_json,
)
from validation.autonomous_w2.g4.v6_snapshot_v3.checker_centered_v6 import audit as replay_v6_row
from validation.autonomous_w2.g4.v6_snapshot_v3.producer_centered_v6 import evaluate_bound_row
from validation.autonomous_w2.g4.v6_snapshot_v3.rational_interval_v3 import ArithmeticLimit
from validation.autonomous_w2.g4.v6_w2_adapter_v3 import convert_v6_row_to_segments


def _project_file(relative: str, code: str) -> Path:
    path = (PROJECT / relative).resolve()
    try:
        path.relative_to(PROJECT.resolve())
    except ValueError as exc:
        raise InvalidInput(f"PATH_ESCAPES_PROJECT:{code}") from exc
    if not path.is_file():
        raise InvalidInput(f"REQUIRED_FILE_MISSING:{code}")
    return path


def _one(items: list[dict[str, Any]], key: str, value: Any, reason: str) -> dict[str, Any]:
    matches = [item for item in items if item.get(key) == value]
    if len(matches) != 1:
        raise InvalidInput(reason)
    return matches[0]


def validate_v6_setup(
    binding_path: Path,
    *,
    freeze: dict[str, Any] | None = None,
    receipt: dict[str, Any] | None = None,
    binding_override: dict[str, Any] | None = None,
    protocol_override: dict[str, Any] | None = None,
    preflight_fixture: bool = False,
) -> dict[str, Any]:
    """Validate every preproducer pin; has no producer/replay side effects.

    The real worker calls this exact function before its producer marker. The
    nonquery fixtures inject mutations through the optional in-memory inputs.
    """
    if preflight_fixture:
        fixture_root = PROJECT / "results/validation/autonomous_w2/g4/matched_v6_task_development_v3/nonquery_fixtures_v5"
        freeze_path = fixture_root / "freeze_manifest_fixture.json"
        receipt_path = fixture_root / "freeze_receipt_fixture.json"
    else:
        freeze_path = PROJECT / PLAN_REL / "freeze_manifest_v4.json"
        receipt_path = PROJECT / "results/validation/autonomous_w2/g4/matched_v6_task_development_v3/freeze_receipt_v4.json"
    if freeze is None or receipt is None:
        loaded_freeze, loaded_receipt = load_authoritative_freeze(
            freeze_path, receipt_path, preflight_fixture=preflight_fixture,
        )
        freeze = loaded_freeze if freeze is None else freeze
        receipt = loaded_receipt if receipt is None else receipt
    assert freeze is not None and receipt is not None

    if freeze.get("freeze_receipt_path") != receipt_path.relative_to(PROJECT).as_posix():
        raise InvalidInput("AUTHORITATIVE_FREEZE_RECEIPT_PATH_MISMATCH")
    if receipt.get("freeze_manifest_path") != freeze_path.relative_to(PROJECT).as_posix():
        raise InvalidInput("RECEIPT_FREEZE_MANIFEST_PATH_MISMATCH")
    if receipt.get("source_closure_path") != freeze.get("source_closure_path"):
        raise InvalidInput("RECEIPT_SOURCE_CLOSURE_PATH_MISMATCH")
    if receipt.get("source_closure_sha256") != freeze.get("source_closure_sha256"):
        raise InvalidInput("RECEIPT_SOURCE_CLOSURE_HASH_MISMATCH")
    if receipt.get("freeze_manifest_sha256") != sha256_file(freeze_path):
        raise InvalidInput("FREEZE_RECEIPT_MANIFEST_HASH_MISMATCH")
    if receipt.get("protocol_sha256") != freeze.get("protocol_sha256"):
        raise InvalidInput("FREEZE_RECEIPT_PROTOCOL_HASH_MISMATCH")
    if receipt.get("source_closure_sha256") != sha256_file(_project_file(freeze["source_closure_path"], "SOURCE_CLOSURE")):
        raise InvalidInput("FREEZE_RECEIPT_SOURCE_CLOSURE_BYTES_MISMATCH")
    verify_source_closure(freeze)

    protocol_path = _project_file(freeze["protocol_path"], "PROTOCOL")
    if sha256_file(protocol_path) != freeze.get("protocol_sha256"):
        raise InvalidInput("FROZEN_PROTOCOL_BYTES_MISMATCH")
    protocol = strict_json(protocol_path) if protocol_override is None else protocol_override
    v6_profile_path = _project_file(freeze["v6_profile_path"], "V6_PROFILE")
    auer_profile_path = _project_file(freeze["auer_profile_path"], "AUER_PROFILE")
    common_profile_path = _project_file(freeze["common_profile_path"], "COMMON_PROFILE")
    v6_profile = strict_json(v6_profile_path)
    auer_profile = strict_json(auer_profile_path)
    common_profile = strict_json(common_profile_path)
    expected_routes = {
        "v6": "validation.autonomous_w2.g4.v6_w2_worker_v3",
        "auer": "validation.autonomous_w2.g4.auer_w2_worker_v3",
    }
    if freeze.get("method_worker_modules") != expected_routes:
        raise InvalidInput("FREEZE_ACTUAL_WORKER_ROUTE_BINDING")
    if common_profile.get("matched_workers", {}).get("v6_module") != expected_routes["v6"]:
        raise InvalidInput("COMMON_PROFILE_V6_WORKER_ROUTE")
    if common_profile.get("matched_workers", {}).get("auer_module") != expected_routes["auer"]:
        raise InvalidInput("COMMON_PROFILE_AUER_WORKER_ROUTE")
    if common_profile.get("protocol_candidate") != freeze.get("protocol_path"):
        raise InvalidInput("COMMON_PROFILE_PROTOCOL_PATH_STALE")
    if common_profile.get("source_closure_manifest_path") != freeze.get("source_closure_path"):
        raise InvalidInput("COMMON_PROFILE_SOURCE_CLOSURE_PATH_STALE")
    if auer_profile.get("matched_worker", {}).get("module") != expected_routes["auer"]:
        raise InvalidInput("AUER_PROFILE_WORKER_ROUTE")
    if profile_path := v6_profile.get("protocol_candidate"):
        if profile_path != freeze.get("protocol_path"):
            raise InvalidInput("V6_PROFILE_PROTOCOL_PATH_STALE")
    if auer_profile.get("protocol_candidate") != freeze.get("protocol_path"):
        raise InvalidInput("AUER_PROFILE_PROTOCOL_PATH_STALE")
    if auer_profile.get("source_closure_manifest_path") != freeze.get("source_closure_path"):
        raise InvalidInput("AUER_PROFILE_SOURCE_CLOSURE_PATH_STALE")
    if auer_profile.get("source_snapshot_manifest_path") != freeze.get("native_source_snapshot_path"):
        raise InvalidInput("AUER_PROFILE_SOURCE_SNAPSHOT_PATH_STALE")
    actions = protocol.get("actions")
    if not isinstance(actions, list) or len(actions) != 3:
        raise InvalidInput("FROZEN_ACTION_COUNT_NOT_THREE")
    ids = [item.get("comparison_id") for item in actions]
    if len(set(ids)) != 3:
        raise InvalidInput("DUPLICATE_FROZEN_ACTION_MAPPING")
    if len(freeze.get("actions", [])) != 3 or {item.get("comparison_id") for item in freeze["actions"]} != set(ids):
        raise InvalidInput("FREEZE_PROTOCOL_ACTION_BIJECTION")
    ordered = protocol.get("ordered_actions")
    if not isinstance(ordered, list) or len(ordered) != 3:
        raise InvalidInput("FROZEN_ORDERED_ACTION_COUNT_NOT_THREE")
    if [item.get("external_id") for item in ordered] != ids:
        raise InvalidInput("FROZEN_ORDERED_ACTION_ORDER_OR_MAPPING")

    benchmark_path = _project_file(freeze["benchmark_path"], "BENCHMARK")
    manifest_path = _project_file(freeze["auer_manifest_path"], "AUER_MANIFEST")
    if sha256_file(benchmark_path) != freeze.get("benchmark_sha256"):
        raise InvalidInput("FROZEN_BENCHMARK_HASH_MISMATCH")
    if sha256_file(manifest_path) != freeze.get("auer_manifest_sha256"):
        raise InvalidInput("FROZEN_AUER_MANIFEST_HASH_MISMATCH")
    benchmark = strict_json(benchmark_path)
    manifest = strict_json(manifest_path)
    cases = manifest.get("cases")
    if not isinstance(cases, list) or len(cases) != 3:
        raise InvalidInput("AUER_CANONICAL_INPUT_COUNT_NOT_THREE")
    task_path = _project_file(freeze["task_protocol"]["path"], "TASK_PROTOCOL")
    if sha256_file(task_path) != freeze["task_protocol"].get("sha256"):
        raise InvalidInput("FROZEN_TASK_PROTOCOL_HASH_MISMATCH")
    task = strict_json(task_path)
    expected_box = task["task"]["initial_box"]
    expected_labels = task["model"]["fixed_label_order"]
    expected_obstacle = task["task"]["obstacle"]
    for index, (candidate, frozen_order) in enumerate(zip(actions, ordered, strict=True), 1):
        comparison_id = candidate.get("comparison_id")
        case_rows = [row for row in cases if row.get("comparison_id") == candidate.get("auer_id")]
        if len(case_rows) != 1:
            raise InvalidInput(f"AUER_CANONICAL_INPUT_MAPPING:{index}")
        case = case_rows[0]
        canonical_input = case.get("canonical_physical_input")
        digest = canonical_sha256(canonical_input) if isinstance(canonical_input, dict) else None
        if (frozen_order.get("ordinal") != index
                or frozen_order.get("peer_action_id") != candidate.get("peer_action_id")
                or frozen_order.get("voltage") != candidate.get("voltage")
                or frozen_order.get("external_id") != comparison_id
                or frozen_order.get("auer_id") != candidate.get("auer_id")
                or candidate.get("ordinal") != index
                or candidate.get("external_id") != comparison_id
                or candidate.get("auer_input_digest") != candidate.get("physical_input_sha256")
                or candidate.get("physical_input_sha256") != case.get("physical_input_sha256")
                or digest != candidate.get("physical_input_sha256")
                or candidate.get("auer_native_input_path") != case.get("native_case_path")
                or candidate.get("auer_native_input_file_sha256") != case.get("native_case_sha256")
                or case.get("peer_action_id") != candidate.get("peer_action_id")
                or case.get("canonical_physical_input", {}).get("voltage") != candidate.get("voltage")
                or case.get("canonical_physical_input", {}).get("initial_box") != expected_box
                or case.get("canonical_physical_input", {}).get("hold_s") != task["task"]["hold_s"]
                or case.get("canonical_physical_input", {}).get("obstacle") != expected_obstacle
                or case.get("canonical_physical_input", {}).get("parameter_label_order") != expected_labels
                or case.get("canonical_physical_input", {}).get("parameter_label_bounds") != task["model"]["fixed_label_bounds"]
                or case.get("canonical_physical_input", {}).get("formulation") != task["model"]["formulation"]
                or case.get("canonical_physical_input", {}).get("traction_law") != task["model"]["phi"]
                or case.get("canonical_physical_input", {}).get("fixed_constants") != task["model"]["fixed_constants"]
                or case.get("canonical_physical_input", {}).get("parameter_maps") != task["model"]["parameter_maps"]
                or case.get("canonical_physical_input", {}).get("label_semantics") != task["model"]["label_semantics"]
                or case.get("canonical_physical_input", {}).get("progress_metric") != task["task"]["progress_metric"]
                or case.get("canonical_physical_input", {}).get("required_progress_m") != task["task"]["required_progress_m"]
                or case.get("canonical_physical_input", {}).get("task_protocol_sha256") != freeze["task_protocol"]["sha256"]):
            raise InvalidInput(f"FROZEN_ACTION_CANONICAL_INPUT_MISMATCH:{comparison_id}")

    binding_path = binding_path.resolve()
    try:
        binding_rel = binding_path.relative_to(PROJECT.resolve()).as_posix()
    except ValueError as exc:
        raise InvalidInput("OUTER_BINDING_PATH_ESCAPES_PROJECT") from exc
    binding = binding_override if binding_override is not None else strict_json(binding_path)
    if binding_override is None and binding_rel != binding.get("binding_path"):
        raise InvalidInput("OUTER_BINDING_PATH_MISMATCH")
    comparison_id = binding.get("comparison_id")
    action = _one(actions, "comparison_id", comparison_id, "ACTION_MAPPING_MISSING_OR_DUPLICATE")
    frozen_action = _one(freeze["actions"], "comparison_id", comparison_id, "FREEZE_ACTION_MAPPING_MISSING_OR_DUPLICATE")
    expected_binding_path = freeze.get("v6_binding_paths", {}).get(comparison_id)
    if expected_binding_path != binding_rel:
        raise InvalidInput("FROZEN_OUTER_BINDING_PATH_MISMATCH")
    expected_binding_sha = frozen_action.get("native_binding_sha256")
    if binding_override is None and (not expected_binding_sha or sha256_file(binding_path) != expected_binding_sha):
        raise InvalidInput("FROZEN_WRAPPER_BINDING_HASH")
    if action.get("native_binding_sha256") != expected_binding_sha:
        raise InvalidInput("PROTOCOL_FREEZE_BINDING_HASH_MISMATCH")
    for required in (
        "peer_saved_row_path", "peer_saved_row_sha256", "core_binding_path", "core_binding_sha256",
        "source_files", "peer_release_path", "peer_release_sha256", "physical_input_sha256",
    ):
        if required not in binding:
            raise InvalidInput(f"REQUIRED_BINDING_FIELD_MISSING:{required}")
    string_fields = (
        "comparison_id", "binding_path", "action_id", "peer_action_id", "peer_saved_row_path",
        "peer_saved_row_sha256", "core_binding_path", "core_binding_sha256", "peer_release_path",
        "peer_release_sha256", "physical_input_sha256", "external_input_digest",
        "native_task_protocol_sha256", "source_snapshot_manifest_sha256",
    )
    for field in string_fields:
        if not isinstance(binding.get(field), str) or not binding[field]:
            raise InvalidInput(f"REQUIRED_BINDING_FIELD_TYPE:{field}")
    for field in ("peer_saved_row_sha256", "core_binding_sha256", "peer_release_sha256", "physical_input_sha256",
                  "external_input_digest", "native_task_protocol_sha256", "source_snapshot_manifest_sha256"):
        value = binding[field]
        if len(value) != 64 or any(char not in "0123456789abcdef" for char in value.lower()):
            raise InvalidInput(f"REQUIRED_BINDING_SHA256_INVALID:{field}")
    if binding.get("physical_input_sha256") != action.get("physical_input_sha256"):
        raise InvalidInput("CANONICAL_PHYSICAL_INPUT_BINDING")
    if binding.get("external_input_digest") != action.get("physical_input_sha256"):
        raise InvalidInput("OUTER_BINDING_EXTERNAL_INPUT_DIGEST")
    if binding.get("peer_action_id") != action.get("peer_action_id"):
        raise InvalidInput("PEER_ACTION_BINDING_MISMATCH")
    if binding.get("action_id") != action.get("peer_action_id"):
        raise InvalidInput("OUTER_BINDING_CORE_ACTION_ID_MISMATCH")
    if binding.get("action", {}).get("id") != action.get("peer_action_id"):
        raise InvalidInput("OUTER_BINDING_ACTION_OBJECT_MISMATCH")
    if binding.get("action", {}).get("voltage") != action.get("voltage"):
        raise InvalidInput("OUTER_BINDING_VOLTAGE_MISMATCH")
    if binding.get("peer_release_path") != freeze["peer_release"].get("path") or binding.get("peer_release_sha256") != freeze["peer_release"].get("sha256"):
        raise InvalidInput("PEER_RELEASE_BINDING_MISMATCH")
    if binding.get("source_snapshot_manifest_sha256") != freeze.get("native_source_snapshot_sha256"):
        raise InvalidInput("V6_SOURCE_SNAPSHOT_BINDING")

    # Required path/hash values come from the signed outer binding. Never read
    # them from the protocol action, which deliberately does not contain them.
    saved_rel = binding["peer_saved_row_path"]
    saved_sha = binding["peer_saved_row_sha256"]
    core_rel = binding["core_binding_path"]
    core_sha = binding["core_binding_sha256"]
    saved_path = _project_file(saved_rel, "PEER_SAVED_ROW")
    core_path = _project_file(core_rel, "PEER_CORE_BINDING")
    source_files = binding.get("source_files")
    if not isinstance(source_files, dict):
        raise InvalidInput("OUTER_BINDING_SOURCE_FILES_MISSING")
    if source_files.get(saved_rel) != saved_sha:
        raise InvalidInput("SAVED_ROW_PATH_HASH_PAIR_MISMATCH")
    if source_files.get(core_rel) != core_sha:
        raise InvalidInput("CORE_BINDING_PATH_HASH_PAIR_MISMATCH")
    if sha256_file(saved_path) != saved_sha:
        raise InvalidInput("SAVED_G2_ROW_CHANGED")
    if sha256_file(core_path) != core_sha:
        raise InvalidInput("G2_CORE_BINDING_CHANGED")
    saved_row = strict_json(saved_path)
    core_binding = strict_json(core_path)
    if saved_row.get("action_id") != action.get("peer_action_id"):
        raise InvalidInput("SAVED_G2_ROW_ACTION_MISMATCH")
    if saved_row.get("binding_sha256") != core_sha:
        raise InvalidInput("SAVED_G2_ROW_CORE_BINDING_MISMATCH")
    if core_binding.get("action_id") != action.get("peer_action_id"):
        raise InvalidInput("G2_CORE_BINDING_ACTION_MISMATCH")
    if core_binding.get("action", {}).get("id") != action.get("peer_action_id"):
        raise InvalidInput("G2_CORE_BINDING_ACTION_OBJECT_MISMATCH")
    if core_binding.get("action", {}).get("voltage") != action.get("voltage"):
        raise InvalidInput("G2_CORE_BINDING_VOLTAGE_MISMATCH")
    saved_voltage = saved_row.get("held_voltage_V")
    action_voltage = action.get("voltage")
    if (not isinstance(saved_voltage, list) or len(saved_voltage) != 2
            or not isinstance(action_voltage, list) or len(action_voltage) != 2
            or [str(Fraction(value)) for value in saved_voltage]
            != [str(Fraction(value)) for value in action_voltage]):
        raise InvalidInput("SAVED_G2_ROW_VOLTAGE_MISMATCH")
    if saved_row.get("hold_s") != "2/1" or saved_row.get("required_progress_m") != "7/20":
        raise InvalidInput("SAVED_G2_ROW_TASK_TARGET_MISMATCH")
    if saved_row.get("protocol_id") != task.get("protocol_id") or saved_row.get("protocol_sha256") != freeze["task_protocol"].get("sha256"):
        raise InvalidInput("SAVED_G2_ROW_TASK_PROTOCOL_MISMATCH")
    if saved_row.get("profile_sha256") != core_binding.get("profile_sha256"):
        raise InvalidInput("SAVED_G2_ROW_CORE_PROFILE_MISMATCH")
    label_names = [item.get("name") for item in benchmark.get("parameter_labels", [])]
    if saved_row.get("parameter_label_order") != label_names:
        raise InvalidInput("SAVED_G2_ROW_PARAMETER_IMAGE_MISMATCH")
    canonical_case = next(row for row in cases if row["comparison_id"] == action["auer_id"])
    if canonical_case["canonical_physical_input"]["initial_box"] != expected_box:
        raise InvalidInput("CANONICAL_INITIAL_BOX_BENCHMARK_MISMATCH")
    if canonical_case["canonical_physical_input"]["hold_s"] != task["task"]["hold_s"]:
        raise InvalidInput("CANONICAL_HOLD_MISMATCH")
    if canonical_case["canonical_physical_input"]["parameter_label_order"] != label_names:
        raise InvalidInput("CANONICAL_LABEL_ORDER_MISMATCH")
    if canonical_case["canonical_physical_input"]["parameter_label_bounds"] != ["9999/10000", "10001/10000"]:
        raise InvalidInput("CANONICAL_LABEL_BOUNDS_MISMATCH")
    if canonical_case["canonical_physical_input"]["obstacle"] != {
            "center_m": ["1/2", "1/10"], "inflated_radius_m": "3/50", "kind": "static_circle"}:
        raise InvalidInput("CANONICAL_OBSTACLE_MISMATCH")
    if binding.get("native_task_protocol_sha256") != freeze["task_protocol"].get("sha256"):
        raise InvalidInput("PEER_TASK_PROTOCOL_BINDING_MISMATCH")

    for relative, digest in source_files.items():
        source_path = _project_file(relative, "PINNED_SOURCE")
        if not isinstance(digest, str) or len(digest) != 64 or sha256_file(source_path) != digest:
            raise InvalidInput(f"SOURCE_PIN_MISMATCH:{relative}")
    return {
        "binding": binding, "action": action, "freeze_action": frozen_action,
        "protocol": protocol, "freeze": freeze, "receipt": receipt,
        "saved_row_path": saved_path, "saved_row_sha256": saved_sha,
        "core_binding_path": core_path, "core_binding_sha256": core_sha,
        "binding_path": binding_path, "binding_sha256": expected_binding_sha,
    }


def run(
    binding_path: Path,
    output_dir: Path,
    *,
    preflight_fixture: bool = False,
    freeze_override: dict[str, Any] | None = None,
    receipt_override: dict[str, Any] | None = None,
    binding_override: dict[str, Any] | None = None,
    protocol_override: dict[str, Any] | None = None,
) -> int:
    started = time.monotonic()
    setup = validate_v6_setup(
        binding_path, freeze=freeze_override, receipt=receipt_override,
        binding_override=binding_override, protocol_override=protocol_override,
        preflight_fixture=preflight_fixture,
    )
    binding, action, freeze = setup["binding"], setup["action"], setup["freeze"]
    output_dir = output_dir.resolve()
    output_dir.relative_to(PROJECT.resolve())

    producer_started = time.monotonic()
    write_json(output_dir / "producer_start.json", {
        "schema": "ddwmr-g4-w2-producer-start-v1", "method": "centered_residual_v6",
        "comparison_id": binding["comparison_id"], "source_binding_sha256": setup["binding_sha256"],
        "peer_saved_row_sha256": setup["saved_row_sha256"], "producer_invocation_ordinal": 1,
    }, max_bytes=4096, exclusive=True)
    row = evaluate_bound_row(binding, binding["action_id"])
    producer_seconds = time.monotonic() - producer_started
    row_path = output_dir / "native_row.json"
    row_hash, row_bytes = write_json(row_path, row, max_bytes=8_388_608)

    replay_started = time.monotonic()
    native_replay = replay_v6_row(setup["binding_path"], row_path)
    replay_seconds = time.monotonic() - replay_started
    if not native_replay.get("replayed"):
        raise InvalidInput(f"V6_NATIVE_REPLAY_FAILED:{native_replay}")

    task_path = _project_file(freeze["task_protocol"]["path"], "TASK_PROTOCOL")
    task = strict_json(task_path)
    profile_path = _project_file(freeze["v6_profile_path"], "V6_PROFILE")
    benchmark_path = _project_file(freeze["benchmark_path"], "BENCHMARK")
    common_profile_path = _project_file(freeze["common_profile_path"], "COMMON_PROFILE")
    protocol = setup["protocol"]
    profile = strict_json(profile_path)
    benchmark = strict_json(benchmark_path)
    common_profile = strict_json(common_profile_path)
    common_budget = Budget(
        max_bits=int(common_profile["max_rational_bits"]),
        max_operations=int(common_profile["max_rational_operations_per_common_stage"]),
        wall_seconds=Fraction(int(common_profile["wall_seconds"])),
    )
    configure_integer_string_limit(int(common_profile["max_integer_string_digits"]))
    adapter_started = time.monotonic()
    adapter_binding = dict(binding)
    adapter_binding["native_row_sha256"] = row_hash
    segments, adapter_work = convert_v6_row_to_segments(
        row, task, protocol, adapter_binding, profile, benchmark, common_budget,
    )
    adapter_seconds = time.monotonic() - adapter_started
    common_started = time.monotonic()
    common_record, common_replay, progress, common_files = score_serialize_replay_progress(
        segments, benchmark, scene_from_task(task), Fraction(task["task"]["hold_s"]),
        initial_state_from_task(task, common_budget), sqrt_bisections=int(common_profile["sqrt_bisections"]),
        budget=common_budget, common_record_path=output_dir / "common_record.json",
        progress_path=output_dir / "progress.json",
        max_record_bytes=int(common_profile["max_common_record_bytes"]),
        max_progress_bytes=int(common_profile["max_progress_record_bytes"]),
    )
    common_seconds = time.monotonic() - common_started
    if not common_replay.get("replayed"):
        raise InvalidInput(f"V6_COMMON_REPLAY_FAILED:{common_replay}")
    bounds = [Fraction(int(item["num"]), int(item["den"])) for item in progress["progress_enclosure_m"]]
    coverage = row.get("center_time_coverage", {})
    native_certificate_valid = (
        native_replay.get("replayed") is True
        and row.get("safety_status") == "CERTIFIED"
        and row.get("clip_strict_interior_proved") is True
        and coverage.get("contiguous") is True
        and coverage.get("covered_start_s") == "0/1"
        and coverage.get("covered_end_s") == "2/1"
        and coverage.get("slab_count") == int(profile["center_time_slabs"])
    )
    safety_pass = (
        native_certificate_valid
        and common_record.get("predicate_status") == "PASS_ON_SUPPLIED_TUBE"
        and common_replay.get("replayed") is True
    )
    eligible = safety_pass and bounds[0] >= Fraction(7, 20)
    final_status = "CERTIFIED" if eligible else (
        "CERTIFIED_SAFETY_TASK_INELIGIBLE" if safety_pass and bounds[1] < Fraction(7, 20) else
        "SAFETY_CERTIFIED_PROGRESS_UNRESOLVED" if safety_pass else
        "PROOF_COMPLETE_COMMON_UNKNOWN" if native_certificate_valid else "NATIVE_UNKNOWN_COMMON_DIAGNOSTIC"
    )
    summary = {
        "schema": "ddwmr-g4-w2-v6-native-result-v3", "external_id": binding["comparison_id"],
        "peer_action_id": binding["peer_action_id"], "physical_input_sha256": binding["physical_input_sha256"],
        "wrapper_binding_sha256": setup["binding_sha256"], "core_binding_sha256": setup["core_binding_sha256"],
        "peer_saved_row_path": binding["peer_saved_row_path"], "peer_saved_row_sha256": setup["saved_row_sha256"],
        "native_status": row.get("safety_status"), "native_row_path": row_path.relative_to(PROJECT).as_posix(),
        "native_certificate_valid": native_certificate_valid,
        "native_clip_strict_interior_proved": row.get("clip_strict_interior_proved"),
        "native_full_hold_coverage": coverage,
        "native_row_sha256": row_hash, "native_row_bytes": row_bytes, "native_replay": native_replay,
        "native_replay_status": "PASS", "native_replay_wall_seconds": replay_seconds,
        "common_record_path": (output_dir / "common_record.json").relative_to(PROJECT).as_posix(),
        "common_progress_path": (output_dir / "progress.json").relative_to(PROJECT).as_posix(),
        "common_summary": summarize_common(common_record), "common_replay": common_replay,
        "common_replay_status": "PASS", "common_progress": progress, "common_files": common_files,
        "adapter_work": adapter_work, "progress_lower_meets_threshold": bounds[0] >= Fraction(7, 20),
        "task_eligible": eligible, "final_status": final_status,
        "producer_wall_seconds": producer_seconds, "native_replay_wall_seconds": replay_seconds,
        "common_adapter_wall_seconds": adapter_seconds, "common_check_replay_progress_wall_seconds": common_seconds,
        "worker_elapsed_wall_seconds": time.monotonic() - started,
        "producer_interval_operations": row.get("arithmetic", {}).get("interval_operations"),
        "producer_peak_rational_bits": row.get("arithmetic", {}).get("max_rational_bits"),
        "native_calls_counted": 1, "no_retry": True,
    }
    write_json(output_dir / "worker_result.json", summary, max_bytes=1_048_576)
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    output_dir = Path(args.output_dir).resolve()
    try:
        return run(Path(args.binding), output_dir)
    except (ArithmeticLimit, ResourceLimit) as exc:
        native_started = (output_dir / "producer_start.json").is_file()
        payload = {"schema": "ddwmr-g4-w2-v6-native-result-v3", "native_status": "RESOURCE_LIMIT",
                   "termination": f"{type(exc).__name__}:{exc}", "native_calls_counted": int(native_started), "no_retry": True}
        write_json(output_dir / "worker_result.json", payload, max_bytes=1_048_576)
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        return 0
    except Exception as exc:
        native_started = (output_dir / "producer_start.json").is_file()
        payload = {"schema": "ddwmr-g4-w2-v6-native-result-v3", "native_status": "IMPLEMENTATION_FAILURE",
                   "termination": f"{type(exc).__name__}:{exc}", "native_calls_counted": int(native_started), "no_retry": True}
        try:
            write_json(output_dir / "worker_result.json", payload, max_bytes=1_048_576)
        except Exception:
            pass
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        return 30


if __name__ == "__main__":
    raise SystemExit(main())
