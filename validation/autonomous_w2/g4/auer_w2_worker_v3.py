"""One frozen local-Auer development action with native and common replay."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

from validation.autonomous_w2.g4.auer_snapshot_v3.replay_r9_w2 import replay_native_proof
from validation.autonomous_w2.g4.auer_snapshot_v3.solver_r9_w2 import solve_ddwmr_case
from validation.autonomous_w2.g4.auer_w2_adapter_v3 import proof_object_sha256 as native_proof_sha256, make_segments
from validation.autonomous_w2.g4.matched_v6_common_v3 import (
    PLAN_REL, PROJECT, semantic_sha256, configure_integer_string_limit, initial_state_from_task, load_authoritative_freeze,
    scene_from_task, score_serialize_replay_progress, sha256_file, strict_json,
    summarize_common, verify_source_closure, write_json,
)
from validation.g2.rational import Budget, Interval, ResourceLimit, parse_q

RESULT_REL = Path("results/validation/autonomous_w2/g4/matched_v6_task_development_v3")


def _binding_for(
    freeze: dict[str, Any], comparison_id: str,
    binding_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if binding_override is not None:
        return binding_override
    binding_doc = strict_json(PROJECT / freeze["auer_bindings_path"])
    matches = [item["native_binding"] for item in binding_doc["bindings"]
               if item["comparison_id"] == comparison_id]
    if len(matches) != 1:
        raise ValueError("AUER_NATIVE_BINDING_NOT_UNIQUE")
    return matches[0]


def _project_file(relative: str, code: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"AUER_PATH_INVALID:{code}")
    path = (PROJECT / rel).resolve()
    try:
        path.relative_to(PROJECT.resolve())
    except ValueError as exc:
        raise ValueError(f"AUER_PATH_ESCAPES_PROJECT:{code}") from exc
    if not path.is_file():
        raise ValueError(f"AUER_REQUIRED_FILE_MISSING:{code}")
    return path


def _qobj(value: str) -> dict[str, str]:
    rational = Fraction(value)
    return {"num": str(rational.numerator), "den": str(rational.denominator)}


def _expected_physical_input(task: dict[str, Any], task_sha: str, voltage: list[str]) -> dict[str, Any]:
    return {
        "schema": "ddwmr-g4-w2-canonical-physical-input-v2",
        "task_protocol_sha256": task_sha,
        "formulation": task["model"]["formulation"],
        "traction_law": task["model"]["phi"],
        "lipschitz_constant": task["model"]["lipschitz_constant"],
        "lipschitz_constant": task["model"]["lipschitz_constant"],
        "fixed_constants": task["model"]["fixed_constants"],
        "parameter_label_order": task["model"]["fixed_label_order"],
        "parameter_label_bounds": task["model"]["fixed_label_bounds"],
        "parameter_maps": task["model"]["parameter_maps"],
        "label_semantics": task["model"]["label_semantics"],
        "state_order": task["task"]["initial_box_state_order"],
        "initial_box": task["task"]["initial_box"],
        "hold_s": task["task"]["hold_s"],
        "voltage": voltage,
        "obstacle": task["task"]["obstacle"],
        "progress_metric": task["task"]["progress_metric"],
        "required_progress_m": task["task"]["required_progress_m"],
    }


def _validate_benchmark_task(benchmark: dict[str, Any], task: dict[str, Any]) -> None:
    """Check the native benchmark's consumed task semantics against G2's protocol."""
    if benchmark.get("state_cells", [{}])[0].get("coordinates") != task["task"]["initial_box_state_order"]:
        raise ValueError("AUER_BENCHMARK_STATE_ORDER")
    if benchmark.get("state_cells", [{}])[0].get("box") != [
        [_qobj(pair[0]), _qobj(pair[1])] for pair in task["task"]["initial_box"]
    ]:
        raise ValueError("AUER_BENCHMARK_INITIAL_BOX")
    labels = benchmark.get("parameter_labels")
    if not isinstance(labels, list) or [row.get("name") for row in labels] != task["model"]["fixed_label_order"]:
        raise ValueError("AUER_BENCHMARK_LABEL_ORDER")
    expected_range = [_qobj(bound) for bound in task["model"]["fixed_label_bounds"]]
    for label in labels:
        if label.get("range") != expected_range:
            raise ValueError(f"AUER_BENCHMARK_LABEL_RANGE:{label.get('name')}")
    expected_label_map = {
        name: expected_range for name in task["model"]["fixed_label_order"]
    }
    if benchmark.get("parameter_cell", {}).get("labels") != expected_label_map:
        raise ValueError("AUER_BENCHMARK_PARAMETER_CELL")
    horizons = benchmark.get("horizons")
    if not isinstance(horizons, list) or len(horizons) != 1 or horizons[0].get("T") != _qobj(task["task"]["hold_s"]):
        raise ValueError("AUER_BENCHMARK_HORIZON")
    if benchmark.get("law") != {"name": "clip", "L_phi": _qobj(task["model"]["lipschitz_constant"])}:
        raise ValueError("AUER_BENCHMARK_CLIP_LAW")
    if benchmark.get("task_target", {}).get("required_progress_m") != _qobj(task["task"]["required_progress_m"]):
        raise ValueError("AUER_BENCHMARK_PROGRESS_TARGET")
    obstacle = task["task"]["obstacle"]
    expected_scene = {
        "id": "scene_v6_static_circle",
        "p_o": [_qobj(item) for item in obstacle["center_m"]],
        "R_s": _qobj(obstacle["inflated_radius_m"]),
    }
    if benchmark.get("scenes") != [expected_scene]:
        raise ValueError("AUER_BENCHMARK_SCENE")
    if benchmark.get("V_max") != _qobj(task["model"]["fixed_constants"]["V_max"]):
        raise ValueError("AUER_BENCHMARK_VOLTAGE_BOUND")
    fixed = benchmark.get("fixed_parameters", {})
    for key, value in task["model"]["fixed_constants"].items():
        if key == "V_max":
            continue
        if fixed.get(key) != {"const": _qobj(value)}:
            raise ValueError(f"AUER_BENCHMARK_FIXED_CONSTANT:{key}")
    for key in ("C_L", "C_R", "R_L", "R_R", "B_L", "B_R", "k_L", "k_R"):
        if fixed.get(key) != {"var": key}:
            raise ValueError(f"AUER_BENCHMARK_PARAMETER_MAP:{key}")
    for side in ("L", "R"):
        if fixed.get(f"J_{side}") != {"op": "div", "args": [{"const": _qobj("1")}, {"var": f"rho_{side}"}]}:
            raise ValueError(f"AUER_BENCHMARK_PARAMETER_MAP:J_{side}")
        if fixed.get(f"L_{side}") != {"var": f"lambda_{side}"}:
            raise ValueError(f"AUER_BENCHMARK_PARAMETER_MAP:L_{side}")


def validate_auer_setup(
    comparison_id: str,
    *,
    preflight_fixture: bool = False,
    binding_override: dict[str, Any] | None = None,
    protocol_override: dict[str, Any] | None = None,
    freeze_override: dict[str, Any] | None = None,
    receipt_override: dict[str, Any] | None = None,
    manifest_override: dict[str, Any] | None = None,
    bindings_doc_override: dict[str, Any] | None = None,
    case_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Exact shared fail-closed setup path used by the worker and fixtures."""
    if preflight_fixture:
        freeze_path = PROJECT / RESULT_REL / "nonquery_fixtures_v5" / "freeze_manifest_fixture.json"
        receipt_path = PROJECT / RESULT_REL / "nonquery_fixtures_v5" / "freeze_receipt_fixture.json"
    else:
        freeze_path = PROJECT / PLAN_REL / "freeze_manifest_v4.json"
        receipt_path = PROJECT / RESULT_REL / "freeze_receipt_v4.json"
    freeze, freeze_receipt = load_authoritative_freeze(
        freeze_path, receipt_path, preflight_fixture=preflight_fixture,
    )
    if freeze_override is not None:
        freeze = freeze_override
    if receipt_override is not None:
        freeze_receipt = receipt_override
    closure = verify_source_closure(freeze)
    closure_sha = freeze["source_closure_sha256"]

    protocol_path = _project_file(freeze["protocol_path"], "PROTOCOL")
    if protocol_override is None:
        protocol = strict_json(protocol_path)
    else:
        protocol = protocol_override
    if sha256_file(protocol_path) != freeze.get("protocol_sha256"):
        raise ValueError("AUER_PROTOCOL_HASH_MISMATCH")
    if freeze.get("task_protocol") != protocol.get("task_protocol"):
        raise ValueError("AUER_FREEZE_TASK_PROTOCOL_BINDING")
    if freeze_receipt.get("source_closure_path") != freeze.get("source_closure_path"):
        raise ValueError("AUER_RECEIPT_CLOSURE_PATH_BINDING")
    if freeze_receipt.get("source_closure_sha256") != freeze.get("source_closure_sha256"):
        raise ValueError("AUER_RECEIPT_CLOSURE_HASH_BINDING")
    if freeze_receipt.get("protocol_sha256") != freeze.get("protocol_sha256"):
        raise ValueError("AUER_RECEIPT_PROTOCOL_HASH_BINDING")
    profile_path = _project_file(freeze["auer_profile_path"], "PROFILE")
    common_profile_path = _project_file(freeze["common_profile_path"], "COMMON_PROFILE")
    profile = strict_json(profile_path)
    common_profile = strict_json(common_profile_path)
    expected_routes = {
        "v6": "validation.autonomous_w2.g4.v6_w2_worker_v3",
        "auer": "validation.autonomous_w2.g4.auer_w2_worker_v3",
    }
    if freeze.get("method_worker_modules") != expected_routes:
        raise ValueError("AUER_FREEZE_ACTUAL_WORKER_ROUTE_MISMATCH")
    if common_profile.get("matched_workers", {}).get("auer_module") != expected_routes["auer"]:
        raise ValueError("AUER_COMMON_PROFILE_WORKER_ROUTE_MISMATCH")
    if common_profile.get("protocol_candidate") != freeze.get("protocol_path"):
        raise ValueError("AUER_COMMON_PROFILE_PROTOCOL_PATH_STALE")
    if common_profile.get("source_closure_manifest_path") != freeze.get("source_closure_path"):
        raise ValueError("AUER_COMMON_PROFILE_CLOSURE_PATH_STALE")
    if profile.get("matched_worker", {}).get("module") != "validation.autonomous_w2.g4.auer_w2_worker_v3":
        raise ValueError("AUER_PROFILE_ACTUAL_WORKER_ROUTE_MISMATCH")
    if freeze.get("method_worker_modules", {}).get("auer") != profile["matched_worker"]["module"]:
        raise ValueError("AUER_FREEZE_PROFILE_WORKER_ROUTE_MISMATCH")
    if profile.get("source_closure_manifest_path") != freeze.get("source_closure_path"):
        raise ValueError("AUER_PROFILE_SOURCE_CLOSURE_PATH_STALE")
    if profile.get("source_snapshot_manifest_path") != freeze.get("native_source_snapshot_path"):
        raise ValueError("AUER_PROFILE_SOURCE_SNAPSHOT_PATH_STALE")
    if profile.get("protocol_candidate") != freeze.get("protocol_path"):
        raise ValueError("AUER_PROFILE_PROTOCOL_PATH_STALE")
    if profile.get("external_guard_reference") != "validation/autonomous_w2/g4/windows_job_supervisor_v3.py":
        raise ValueError("AUER_PROFILE_GUARD_PATH_STALE")
    guard_path = _project_file(profile["external_guard_reference"], "EXTERNAL_GUARD")
    if profile.get("external_guard_reference_sha256") != sha256_file(guard_path):
        raise ValueError("AUER_PROFILE_GUARD_HASH_MISMATCH")
    benchmark_path = _project_file(freeze["benchmark_path"], "BENCHMARK")
    if sha256_file(benchmark_path) != freeze.get("benchmark_sha256"):
        raise ValueError("AUER_FROZEN_BENCHMARK_HASH_MISMATCH")
    if protocol.get("benchmark") != {
        "path": freeze.get("benchmark_path"),
        "sha256": freeze.get("benchmark_sha256"),
    }:
        raise ValueError("AUER_PROTOCOL_BENCHMARK_BINDING_MISMATCH")
    benchmark = strict_json(benchmark_path)
    task_path = _project_file(freeze["task_protocol"]["path"], "TASK_PROTOCOL")
    if sha256_file(task_path) != freeze["task_protocol"]["sha256"]:
        raise ValueError("AUER_FROZEN_TASK_PROTOCOL_HASH")
    task = strict_json(task_path)
    _validate_benchmark_task(benchmark, task)
    manifest_path = _project_file(freeze["auer_manifest_path"], "AUER_MANIFEST")
    if manifest_override is None and sha256_file(manifest_path) != freeze.get("auer_manifest_sha256"):
        raise ValueError("AUER_FROZEN_MANIFEST_HASH_MISMATCH")
    manifest = strict_json(manifest_path) if manifest_override is None else manifest_override
    cases = manifest.get("cases")
    if not isinstance(cases, list) or len(cases) != 3 or not all(isinstance(row, dict) for row in cases):
        raise ValueError("AUER_CANONICAL_CASE_COUNT_NOT_THREE")
    manifest_ids = [row.get("comparison_id") for row in cases]
    if len(set(manifest_ids)) != 3:
        raise ValueError("AUER_DUPLICATE_MANIFEST_MAPPING")
    protocol_actions = protocol.get("actions")
    if not isinstance(protocol_actions, list) or len(protocol_actions) != 3 or not all(isinstance(row, dict) for row in protocol_actions):
        raise ValueError("AUER_PROTOCOL_ACTION_COUNT_NOT_THREE")
    protocol_auer_ids = [row.get("auer_id") for row in protocol_actions]
    if len(set(protocol_auer_ids)) != 3:
        raise ValueError("AUER_DUPLICATE_PROTOCOL_MAPPING")
    if freeze.get("actions") != protocol_actions:
        raise ValueError("AUER_FREEZE_PROTOCOL_ACTION_SET_MISMATCH")
    expected_comparison_ids = {row.get("comparison_id") for row in protocol_actions}
    if set(manifest_ids) != set(protocol_auer_ids):
        raise ValueError("AUER_PROTOCOL_MANIFEST_MAPPING_NOT_BIJECTIVE")
    task_actions = task.get("actions")
    if not isinstance(task_actions, list) or len(task_actions) != 3 or not all(isinstance(row, dict) for row in task_actions):
        raise ValueError("AUER_TASK_ACTION_COUNT_NOT_THREE")
    task_action_ids = [row.get("id") for row in task_actions]
    if len(set(task_action_ids)) != 3:
        raise ValueError("AUER_DUPLICATE_PEER_ACTION_MAPPING")
    ordered_actions = protocol.get("ordered_actions")
    if not isinstance(ordered_actions, list) or len(ordered_actions) != 3 or not all(isinstance(row, dict) for row in ordered_actions):
        raise ValueError("AUER_ORDERED_ACTION_COUNT_NOT_THREE")
    if protocol.get("primary_criterion") != freeze.get("primary_criterion"):
        raise ValueError("AUER_FROZEN_PRIMARY_CRITERION_MISMATCH")

    # Prove the complete three-way ID/action/digest map before any producer can
    # run, not only the requested row. This prevents a unique but cross-wired
    # sibling entry from hiding behind a per-row lookup.
    manifest_by_id = {row["comparison_id"]: row for row in cases}
    ordered_by_id = {row.get("external_id"): row for row in ordered_actions}
    for ordinal, candidate in enumerate(protocol_actions, 1):
        external_id = candidate.get("comparison_id")
        auer_id = candidate.get("auer_id")
        peer_id = candidate.get("peer_action_id")
        if (candidate.get("ordinal") != ordinal or candidate.get("external_id") != external_id
                or external_id not in expected_comparison_ids):
            raise ValueError(f"AUER_PROTOCOL_ORDER_OR_EXTERNAL_ID:{ordinal}")
        case_row = manifest_by_id.get(auer_id)
        order_row = ordered_by_id.get(external_id)
        peer_rows = [row for row in task_actions if row.get("id") == peer_id]
        if case_row is None or order_row is None or len(peer_rows) != 1:
            raise ValueError(f"AUER_ACTION_MAPPING_MISSING:{ordinal}")
        peer_row = peer_rows[0]
        if (candidate.get("voltage") != peer_row.get("voltage")
                or candidate.get("voltage") != case_row.get("canonical_physical_input", {}).get("voltage")
                or case_row.get("ordinal") != ordinal
                or case_row.get("peer_action_id") != peer_id
                or order_row.get("ordinal") != ordinal
                or order_row.get("auer_id") != auer_id
                or order_row.get("peer_action_id") != peer_id
                or order_row.get("voltage") != candidate.get("voltage")):
            raise ValueError(f"AUER_ACTION_VOLTAGE_OR_ORDER_MISMATCH:{ordinal}")
        physical = _expected_physical_input(task, freeze["task_protocol"]["sha256"], peer_row["voltage"])
        digest = semantic_sha256(physical)
        if (case_row.get("canonical_physical_input") != physical
                or case_row.get("physical_input_sha256") != digest
                or case_row.get("input_sha256") != digest
                or candidate.get("physical_input_sha256") != digest
                or candidate.get("auer_input_digest") != digest):
            raise ValueError(f"AUER_ACTION_PHYSICAL_DIGEST_MISMATCH:{ordinal}")

    manifest_bindings = {
        "task_protocol_path": freeze["task_protocol"]["path"],
        "task_protocol_sha256": freeze["task_protocol"]["sha256"],
        "peer_release_path": freeze["peer_release"]["path"],
        "peer_release_sha256": freeze["peer_release"]["sha256"],
        "benchmark_path": freeze["benchmark_path"],
        "benchmark_sha256": freeze["benchmark_sha256"],
    }
    if any(manifest.get(key) != value for key, value in manifest_bindings.items()):
        raise ValueError("AUER_MANIFEST_FROZEN_SOURCE_BINDING")
    entries = [row for row in cases if row.get("comparison_id") == comparison_id]
    if len(entries) != 1:
        raise ValueError("AUER_CASE_NOT_UNIQUE_IN_FROZEN_THREE_CASE_MANIFEST")
    item = entries[0]
    actions = [row for row in protocol_actions if row.get("auer_id") == comparison_id]
    if len(actions) != 1:
        raise ValueError("AUER_PROTOCOL_ACTION_NOT_UNIQUE")
    action = actions[0]
    if (action.get("ordinal") != item.get("ordinal")
            or action.get("auer_id") != item.get("comparison_id")
            or action.get("comparison_id") != action.get("external_id")
            or action.get("peer_action_id") != item.get("peer_action_id")
            or action.get("voltage") != item.get("canonical_physical_input", {}).get("voltage")):
        raise ValueError("AUER_PROTOCOL_MANIFEST_ACTION_MAPPING_MISMATCH")
    task_action_rows = [row for row in task_actions if row.get("id") == item.get("peer_action_id")]
    if len(task_action_rows) != 1:
        raise ValueError("AUER_PEER_ACTION_NOT_UNIQUE")
    peer_action = task_action_rows[0]
    if action.get("voltage") != peer_action.get("voltage"):
        raise ValueError("AUER_PEER_ACTION_VOLTAGE_MISMATCH")
    expected_physical = _expected_physical_input(task, freeze["task_protocol"]["sha256"], peer_action["voltage"])
    expected_digest = semantic_sha256(expected_physical)
    if item.get("canonical_physical_input") != expected_physical:
        raise ValueError("AUER_CANONICAL_INPUT_DOES_NOT_MATCH_TASK")
    if (action.get("physical_input_sha256") != expected_digest
            or action.get("auer_input_digest") != expected_digest
            or item.get("physical_input_sha256") != expected_digest
            or item.get("input_sha256") != expected_digest):
        raise ValueError("AUER_PHYSICAL_DIGEST_BINDING")
    if (action.get("auer_native_input_path") != item.get("native_case_path")
            or action.get("auer_native_input_file_sha256") != item.get("native_case_sha256")):
        raise ValueError("AUER_NATIVE_FILE_DIGEST_BINDING")

    case_path = _project_file(item["native_case_path"], "CASE")
    if case_override is None and sha256_file(case_path) != item["native_case_sha256"]:
        raise ValueError("AUER_NATIVE_CASE_BYTES_CHANGED")
    case = strict_json(case_path) if case_override is None else case_override
    if (case.get("physical_input_sha256") != expected_digest
            or case.get("input_sha256") != expected_digest
            or case.get("canonical_physical_input_sha256") != expected_digest):
        raise ValueError("AUER_CASE_PHYSICAL_DIGEST_MISMATCH")
    if case.get("benchmark_sha256") != sha256_file(benchmark_path):
        raise ValueError("AUER_CASE_BENCHMARK_HASH_MISMATCH")
    payload = item.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("AUER_LEGACY_PAYLOAD_MISSING")
    if item.get("payload_sha256") != semantic_sha256(payload):
        raise ValueError("AUER_LEGACY_PAYLOAD_HASH_MISMATCH")
    state_cell = benchmark["state_cells"][0]
    parameter_cell = benchmark["parameter_cell"]
    horizon = benchmark["horizons"][0]
    scene = benchmark["scenes"][0]
    if (payload.get("action") != benchmark["actions"][item["ordinal"] - 1]
            or payload.get("action", {}).get("id") != item.get("action_id")
            or payload.get("horizon") != horizon
            or payload.get("state_cell") != state_cell
            or payload.get("parameter_cell") != parameter_cell
            or payload.get("scene") != scene):
        raise ValueError("AUER_NATIVE_PAYLOAD_BENCHMARK_MAPPING")
    if (item.get("ordinal") != action.get("ordinal")
            or item.get("action_id") != payload.get("action", {}).get("id")
            or item.get("query_id") != comparison_id
            or case.get("query_id") != item.get("query_id")):
        raise ValueError("AUER_NATIVE_CASE_TASK_SEMANTICS")
    expected_labels = [entry["name"] for entry in benchmark["parameter_labels"]]
    if expected_labels != task["model"]["fixed_label_order"] or set(case.get("fixed_labels", {})) != set(expected_labels):
        raise ValueError("AUER_NATIVE_CASE_FIXED_LABEL_SET")
    expected_fixed_labels = {
        name: [_qobj(bound) for bound in task["model"]["fixed_label_bounds"]]
        for name in expected_labels
    }
    if case.get("fixed_labels") != expected_fixed_labels:
        raise ValueError("AUER_NATIVE_CASE_FIXED_LABEL_IMAGE")
    if case.get("initial_state") != state_cell.get("box"):
        raise ValueError("AUER_NATIVE_CASE_INITIAL_BOX")
    if case.get("horizon") != _qobj(task["task"]["hold_s"]):
        raise ValueError("AUER_NATIVE_CASE_HORIZON")
    if case.get("scene") != scene:
        raise ValueError("AUER_NATIVE_CASE_SCENE")
    if case.get("parameter_cell") != parameter_cell:
        raise ValueError("AUER_NATIVE_CASE_PARAMETER_CELL")
    if case.get("held_voltage") != [_qobj(v) for v in peer_action["voltage"]]:
        raise ValueError("AUER_NATIVE_CASE_ACTION_VOLTAGE")
    if case.get("state_order") != task["task"]["initial_box_state_order"]:
        raise ValueError("AUER_NATIVE_CASE_STATE_ORDER")
    if case.get("parameter_cell") != parameter_cell:
        raise ValueError("AUER_NATIVE_CASE_PARAMETER_CELL")
    if item.get("native_case_path") != action.get("auer_native_input_path"):
        raise ValueError("AUER_CASE_PATH_PROTOCOL_BINDING")
    if item.get("native_case_sha256") != action.get("auer_native_input_file_sha256"):
        raise ValueError("AUER_CASE_HASH_PROTOCOL_BINDING")
    if (item.get("native_case_sha256") != sha256_file(case_path)
            if case_override is None else False):
        raise ValueError("AUER_NATIVE_CASE_FILE_HASH_MISMATCH")
    if case.get("canonical_physical_input_sha256") != expected_digest:
        raise ValueError("AUER_NATIVE_CASE_CANONICAL_DIGEST")
    if case.get("candidate_manifest_v2_input_sha256") != item.get("payload_sha256"):
        raise ValueError("AUER_NATIVE_CASE_PAYLOAD_BINDING")
    if case.get("benchmark_path") != freeze["benchmark_path"]:
        raise ValueError("AUER_NATIVE_CASE_BENCHMARK_PATH")
    if case.get("benchmark_sha256") != freeze["benchmark_sha256"]:
        raise ValueError("AUER_NATIVE_CASE_BENCHMARK_HASH")
    for label in expected_labels:
        if case["fixed_labels"].get(label) != expected_fixed_labels[label]:
            raise ValueError(f"AUER_NATIVE_CASE_FIXED_LABEL:{label}")
    # Runtime-only file binding fields are not included in the hashed case bytes.
    case["native_input_path"] = item["native_case_path"]
    case["native_input_file_sha256"] = item["native_case_sha256"]

    if freeze.get("auer_bindings_path") is None or freeze.get("auer_bindings_sha256") is None:
        raise ValueError("AUER_BINDING_FILE_PIN_MISSING")
    bindings_path = _project_file(freeze["auer_bindings_path"], "AUER_BINDINGS")
    if sha256_file(bindings_path) != freeze["auer_bindings_sha256"]:
        raise ValueError("AUER_BINDINGS_FILE_HASH_MISMATCH")
    binding_doc = strict_json(bindings_path) if bindings_doc_override is None else bindings_doc_override
    expected_snapshot_path = freeze.get("native_source_snapshot_path")
    expected_snapshot_sha = freeze.get("native_source_snapshot_sha256")
    if binding_doc.get("native_source_snapshot_path") != expected_snapshot_path:
        raise ValueError("AUER_BINDING_DOC_SOURCE_SNAPSHOT_PATH_MISMATCH")
    if binding_doc.get("native_source_snapshot_sha256") != expected_snapshot_sha:
        raise ValueError("AUER_BINDING_DOC_SOURCE_SNAPSHOT_HASH_MISMATCH")
    snapshot_path = _project_file(expected_snapshot_path, "SOURCE_SNAPSHOT")
    if sha256_file(snapshot_path) != expected_snapshot_sha:
        raise ValueError("AUER_BINDING_DOC_SOURCE_SNAPSHOT_BYTES_MISMATCH")
    binding_rows = binding_doc.get("bindings")
    if not isinstance(binding_rows, list) or len(binding_rows) != 3 or not all(isinstance(row, dict) for row in binding_rows):
        raise ValueError("AUER_BINDING_COUNT_NOT_THREE")
    binding_ids = [row.get("comparison_id") for row in binding_rows]
    if len(set(binding_ids)) != 3:
        raise ValueError("AUER_DUPLICATE_NATIVE_BINDING_MAPPING")
    if set(binding_ids) != set(protocol_auer_ids):
        raise ValueError("AUER_NATIVE_BINDING_MAPPING_NOT_BIJECTIVE")
    if any(not isinstance(row.get("comparison_id"), str) or not isinstance(row.get("native_binding"), dict)
           for row in binding_rows):
        raise ValueError("AUER_NATIVE_BINDING_SCHEMA_INVALID")
    binding_by_id = {row["comparison_id"]: row["native_binding"] for row in binding_rows}
    for candidate in protocol_actions:
        entry_id = candidate["auer_id"]
        binding = binding_override if binding_override is not None and entry_id == comparison_id else binding_by_id.get(entry_id)
        case_row = manifest_by_id[entry_id]
        if not isinstance(binding, dict):
            raise ValueError(f"AUER_NATIVE_BINDING_MISSING:{entry_id}")
        binding_raw_hash = hashlib.sha256(
            json.dumps(binding, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"
        ).hexdigest()
        if (candidate.get("auer_native_binding_sha256") != binding_raw_hash
                or binding.get("input_path") != case_row.get("native_case_path")
                or binding.get("input_sha256") != case_row.get("native_case_sha256")
                or freeze.get("auer_binding_paths", {}).get(entry_id) != freeze.get("auer_bindings_path")):
            raise ValueError(f"AUER_NATIVE_BINDING_MAP_OR_HASH:{entry_id}")
    if not isinstance(binding_override, dict):
        binding_override = None
    native_binding = _binding_for(freeze, comparison_id, binding_override)
    expected_binding_sha = hashlib.sha256(
        json.dumps(native_binding, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"
    ).hexdigest()
    if action.get("auer_native_binding_sha256") != expected_binding_sha:
        raise ValueError("AUER_NATIVE_BINDING_HASH_MISMATCH")
    if freeze.get("auer_binding_paths", {}).get(comparison_id) != freeze.get("auer_bindings_path"):
        raise ValueError("AUER_FREEZE_BINDING_PATH_MISMATCH")
    for key in (
        "input_path", "input_sha256", "resource_profile_path", "resource_profile_sha256",
        "source_snapshot_manifest_sha256", "solver_source_sha256", "checker_source_sha256",
        "method_contract_path", "method_contract_sha256", "arithmetic_backend_manifest_path",
        "arithmetic_backend_manifest_sha256",
    ):
        if key not in native_binding:
            raise ValueError(f"AUER_NATIVE_BINDING_FIELD_MISSING:{key}")
    expected_input = {"input_path": item["native_case_path"], "input_sha256": item["native_case_sha256"]}
    if any(native_binding.get(key) != value for key, value in expected_input.items()):
        raise ValueError("AUER_PROOF_BINDING_INPUT_PATH_OR_HASH")
    if native_binding.get("source_snapshot_manifest_sha256") != freeze["native_source_snapshot_sha256"]:
        raise ValueError("AUER_SOURCE_SNAPSHOT_BINDING")
    if native_binding.get("resource_profile_path") != freeze.get("auer_profile_path"):
        raise ValueError("AUER_PROFILE_PATH_BINDING")
    if native_binding.get("resource_profile_sha256") != sha256_file(PROJECT / freeze["auer_profile_path"]):
        raise ValueError("AUER_PROFILE_BINDING")
    for key, source_rel in (
        ("solver_source_sha256", "validation/autonomous_w2/g4/auer_snapshot_v3/solver_r9_w2.py"),
        ("checker_source_sha256", "validation/autonomous_w2/g4/auer_snapshot_v3/replay_r9_w2.py"),
        ("method_contract_sha256", "docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md"),
        ("arithmetic_backend_manifest_sha256", "validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v2.json"),
    ):
        if native_binding.get(key) != sha256_file(PROJECT / source_rel):
            raise ValueError(f"AUER_PINNED_SOURCE_HASH_MISMATCH:{key}")

    return {
        "freeze": freeze, "freeze_receipt": freeze_receipt, "closure": closure,
        "closure_sha": closure_sha, "protocol": protocol, "profile": profile,
        "common_profile": common_profile, "benchmark": benchmark, "manifest": manifest,
        "item": item, "action": action, "case": case, "native_binding": native_binding,
        "case_path": case_path, "task": task,
    }


def run(
    comparison_id: str,
    output_dir: Path,
    *,
    preflight_fixture: bool = False,
    setup_overrides: dict[str, Any] | None = None,
) -> int:
    started = time.monotonic()
    output_dir = output_dir.resolve()
    setup = validate_auer_setup(
        comparison_id, preflight_fixture=preflight_fixture, **(setup_overrides or {}),
    )
    freeze, closure, closure_sha = setup["freeze"], setup["closure"], setup["closure_sha"]
    protocol, profile, common_profile, benchmark = (
        setup["protocol"], setup["profile"], setup["common_profile"], setup["benchmark"],
    )
    item, action, case, native_binding = (
        setup["item"], setup["action"], setup["case"], setup["native_binding"],
    )
    # These runtime-only fields are excluded from the hashed native-case bytes.
    case["native_input_path"] = item["native_case_path"]
    case["native_input_file_sha256"] = item["native_case_sha256"]
    cap = int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"])
    budget = Budget(
        max_bits=int(profile["max_rational_bits"]), max_operations=cap,
        wall_seconds=Fraction(int(profile["wall_time_seconds_per_ivp"])),
    )
    producer_marker = output_dir / "producer_start.json"
    write_json(producer_marker, {
        "schema": "ddwmr-g4-w2-producer-start-v1",
        "method": "local_auer2013_residual_picard_reconstruction",
        "comparison_id": comparison_id,
        "native_case_sha256": item["native_case_sha256"],
        "producer_invocation_ordinal": 1,
    }, max_bytes=4096, exclusive=True)
    producer_started = time.monotonic()
    proof = solve_ddwmr_case(
        case, benchmark,
        input_path=Path(item["native_case_path"]), input_sha256=item["native_case_sha256"],
        method_sha256=native_binding["method_contract_sha256"],
        backend_sha256=native_binding["arithmetic_backend_manifest_sha256"],
        profile=profile, profile_sha256=native_binding["resource_profile_sha256"],
        snapshot_sha256=native_binding["source_snapshot_manifest_sha256"],
        solver_sha256=native_binding["solver_source_sha256"],
        checker_sha256=native_binding["checker_source_sha256"],
        resource_profile_path=native_binding["resource_profile_path"], budget=budget,
    )
    producer_seconds = time.monotonic() - producer_started
    envelope = {"proof": proof, "proof_sha256": native_proof_sha256(proof)}
    proof_path = output_dir / "native_proof.json"
    proof_hash, proof_bytes = write_json(
        proof_path, envelope, max_bytes=int(profile["max_serialized_proof_bytes"]),
    )

    if proof.get("status") != "PROOF_COMPLETE":
        summary = {
            "schema": "ddwmr-g4-w2-auer-result-v2",
            "comparison_id": comparison_id,
            "peer_action_id": item["peer_action_id"],
            "physical_input_sha256": item["physical_input_sha256"],
            "native_input_path": item["native_case_path"],
            "native_input_sha256": item["native_case_sha256"],
            "native_status": proof.get("status"),
            "native_termination": proof.get("termination"),
            "native_proof_path": proof_path.relative_to(PROJECT).as_posix(),
            "native_proof_file_sha256": proof_hash,
            "native_proof_bytes": proof_bytes,
            "native_proof_record_sha256": envelope["proof_sha256"],
            "producer_wall_seconds": producer_seconds,
            "producer_rational_operations": budget.operations,
            "producer_max_observed_rational_bits": budget.max_seen_bits,
            "native_calls_counted": 1,
            "no_retry": True,
            "final_status": proof.get("status"),
        }
        write_json(output_dir / "worker_result.json", summary, max_bytes=1_048_576)
        print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
        return 0

    replay_started = time.monotonic()
    rhs_producer = int(proof.get("work", {}).get("rhs_jacobian_evaluations", 0))
    rhs_counter = {"count": rhs_producer, "limit": int(profile["max_rhs_jacobian_evaluations_per_ivp"])}
    native_replay = replay_native_proof(
        envelope, case=case, benchmark=benchmark, profile=profile, fixture=None,
        expected_binding=native_binding, budget=budget, rhs_eval_counter=rhs_counter,
    )
    replay_seconds = time.monotonic() - replay_started
    if not native_replay.get("replayed"):
        raise ValueError(f"AUER_NATIVE_REPLAY_FAILED:{native_replay}")

    common_profile = strict_json(PROJECT / freeze["common_profile_path"])
    configure_integer_string_limit(int(common_profile["max_integer_string_digits"]))
    adapter_started = time.monotonic()
    segments = make_segments(
        envelope, case, proof_path, budget, source_binding=native_binding,
        source_closure_path=freeze["source_closure_path"], source_closure_sha256=closure_sha,
        benchmark_path=freeze["benchmark_path"], benchmark_sha256=freeze["benchmark_sha256"],
        benchmark=benchmark,
    )
    adapter_seconds = time.monotonic() - adapter_started
    common_started = time.monotonic()
    task = setup["task"]
    common_record, common_replay, progress, common_files = score_serialize_replay_progress(
        segments, benchmark, scene_from_task(task),
        Fraction(task["task"]["hold_s"]), initial_state_from_task(task, budget),
        sqrt_bisections=int(common_profile["sqrt_bisections"]), budget=budget,
        common_record_path=output_dir / "common_record.json", progress_path=output_dir / "progress.json",
        max_record_bytes=int(common_profile["max_common_record_bytes"]),
        max_progress_bytes=int(common_profile["max_progress_record_bytes"]),
    )
    common_seconds = time.monotonic() - common_started
    if not common_replay.get("replayed"):
        raise ValueError(f"AUER_COMMON_REPLAY_FAILED:{common_replay}")
    progress_bounds = [Fraction(int(value["num"]), int(value["den"])) for value in progress["progress_enclosure_m"]]
    safety_pass = common_record.get("predicate_status") == "PASS_ON_SUPPLIED_TUBE"
    eligible = safety_pass and progress_bounds[0] >= Fraction(7, 20)
    final_status = "CERTIFIED" if eligible else (
        "CERTIFIED_SAFETY_TASK_INELIGIBLE" if safety_pass and progress_bounds[1] < Fraction(7, 20) else
        "SAFETY_CERTIFIED_PROGRESS_UNRESOLVED" if safety_pass else "PROOF_COMPLETE_COMMON_UNKNOWN"
    )
    summary = {
        "schema": "ddwmr-g4-w2-auer-result-v2",
        "comparison_id": comparison_id,
        "peer_action_id": item["peer_action_id"],
        "physical_input_sha256": item["physical_input_sha256"],
        "native_input_path": item["native_case_path"],
        "native_input_sha256": item["native_case_sha256"],
        "native_status": proof["status"],
        "native_method_id": proof["method_id"],
        "native_proof_path": proof_path.relative_to(PROJECT).as_posix(),
        "native_proof_file_sha256": proof_hash,
        "native_proof_bytes": proof_bytes,
        "producer_start_path": producer_marker.relative_to(PROJECT).as_posix(),
        "producer_start_sha256": sha256_file(producer_marker),
        "native_proof_record_sha256": envelope["proof_sha256"],
        "native_replay": native_replay,
        "native_replay_status": "PASS",
        "native_replay_wall_seconds": replay_seconds,
        "common_record_path": (output_dir / "common_record.json").relative_to(PROJECT).as_posix(),
        "common_progress_path": (output_dir / "progress.json").relative_to(PROJECT).as_posix(),
        "common_summary": summarize_common(common_record),
        "common_replay": common_replay,
        "common_replay_status": "PASS",
        "common_progress": progress,
        "common_files": common_files,
        "task_eligible": eligible,
        "progress_lower_meets_threshold": progress_bounds[0] >= Fraction(7, 20),
        "final_status": final_status,
        "resource_work": {
            "producer_rational_operations": proof.get("work", {}).get("rational_operations"),
            "producer_max_observed_rational_bits": proof.get("work", {}).get("max_observed_rational_bits"),
            "native_replay_common_budget_operations_so_far": budget.operations,
            "combined_rational_operation_cap": cap,
            "rhs_jacobian_producer_evaluations": rhs_producer,
            "rhs_jacobian_replay_evaluations": native_replay.get("rhs_jacobian_replay_evaluations"),
            "rhs_jacobian_combined_evaluations": rhs_counter["count"],
            "rhs_jacobian_combined_cap": rhs_counter["limit"],
            "accepted_steps": proof.get("work", {}).get("accepted_steps"),
            "rejected_step_attempts": proof.get("work", {}).get("rejected_step_attempts"),
        },
        "producer_wall_seconds": producer_seconds,
        "native_replay_wall_seconds": replay_seconds,
        "common_adapter_wall_seconds": adapter_seconds,
        "common_check_replay_progress_wall_seconds": common_seconds,
        "worker_elapsed_wall_seconds": time.monotonic() - started,
        "stage_seconds": {
            "producer": producer_seconds,
            "native_replay": replay_seconds,
            "common_adapter": adapter_seconds,
            "common_check_replay_progress": common_seconds,
            "worker_elapsed": time.monotonic() - started,
        },
        "producer_calls_started": 1,
        "native_calls_counted": 1,
        "no_retry": True,
    }
    write_json(output_dir / "worker_result.json", summary, max_bytes=1_048_576)
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
    return 0


def initial_state_from_case(case: dict[str, Any], budget: Budget) -> tuple[Interval, ...]:
    return tuple(Interval.from_json(row, budget) for row in case["initial_state"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--comparison-id", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        return run(args.comparison_id, Path(args.output_dir))
    except ResourceLimit as exc:
        native_started = (Path(args.output_dir) / "producer_start.json").is_file()
        summary = {
            "schema": "ddwmr-g4-w2-auer-result-v2", "comparison_id": args.comparison_id,
            "native_status": "RESOURCE_LIMIT", "termination": {"kind": exc.kind, "detail": exc.detail},
            "producer_calls_started": int(native_started),
            "native_calls_counted": int(native_started),
            "no_retry": True,
        }
        write_json(Path(args.output_dir) / "worker_result.json", summary, max_bytes=1_048_576)
        print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
        return 0
    except Exception as exc:
        native_started = (Path(args.output_dir) / "producer_start.json").is_file()
        summary = {
            "schema": "ddwmr-g4-w2-auer-result-v2", "comparison_id": args.comparison_id,
            "native_status": "IMPLEMENTATION_FAILURE", "termination": f"{type(exc).__name__}:{exc}",
            "producer_calls_started": int(native_started),
            "native_calls_counted": int(native_started),
            "no_retry": True,
        }
        try:
            write_json(Path(args.output_dir) / "worker_result.json", summary, max_bytes=1_048_576)
        except Exception:
            pass
        print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
        return 30


if __name__ == "__main__":
    raise SystemExit(main())
