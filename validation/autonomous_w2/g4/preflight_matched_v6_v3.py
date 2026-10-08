"""Nonquery fixtures for the exact G4 v3 setup guard and runner stop policy."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import uuid
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

from validation.autonomous_w2.g4 import run_matched_v6_w2_v3 as runner
from validation.autonomous_w2.g4 import v6_w2_worker_v3 as worker
from validation.autonomous_w2.g4 import auer_w2_worker_v3 as auer_worker
from validation.autonomous_w2.g4.matched_v6_common_v3 import (
    canonical_sha256, initial_state_from_task, replay_common_record_semantics, scene_from_task,
)
from validation.g2.rational import Budget, Interval
from validation.g4.common_tube import TubeSegment, check_tube_segments
from validation.autonomous_w2.g4.matched_v6_common_v3 import (
    PLAN_REL, PROJECT, RESULT_REL, common_progress, semantic_sha256,
    replay_common_progress_record, sha256_file, strict_json, write_json,
)
from validation.autonomous_w2.g4.auer_w2_adapter_v3 import proof_object_sha256

FIXTURE_REL = RESULT_REL / "nonquery_fixtures_v5"
PEER_RELEASE_REL = Path("coordination/autonomous_w2/g2/releases/RELEASE_v6.json")
PEER_STATUS_REL = Path("coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_19.json")
G4_PHASE_STATUS_REL = Path("coordination/autonomous_w2/g4/STATUS_W2_SEQUENCE_09.json")
V6_EXPECTED_ROUTES = {
    "v6": "validation.autonomous_w2.g4.v6_w2_worker_v3",
    "auer": "validation.autonomous_w2.g4.auer_w2_worker_v3",
}


def _dump(path: Path, value: Any) -> None:
    write_json(path, value, max_bytes=8_388_608)


def _entry(path: Path) -> dict[str, Any]:
    return {
        "path": path.resolve().relative_to(PROJECT.resolve()).as_posix(),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def _native_binding_sha(binding: dict[str, Any]) -> str:
    raw = json.dumps(binding, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"
    return hashlib.sha256(raw).hexdigest()


def _fixture_documents() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Write an isolated, hash-consistent fixture freeze/receipt/closure trio."""
    fixture_dir = PROJECT / FIXTURE_REL
    fixture_dir.mkdir(parents=True, exist_ok=True)
    plan = PROJECT / PLAN_REL
    protocol_path = plan / "protocol_v3.json"
    protocol = strict_json(protocol_path)
    manifest_path = plan / "auer_input_manifest_v3.json"
    auer_bindings_path = plan / "auer_bindings_v3.json"
    snapshot_path = plan / "native_source_snapshot_v3.json"
    task_path = PROJECT / "research/autonomous_w2/g2/task_protocol_v1.json"
    release_path = PROJECT / "coordination/autonomous_w2/g2/releases/RELEASE_v6.json"
    v6_profile_path = plan / "g2_profile_centered_v6.json"
    auer_profile = strict_json(plan / "auer_profile_v3.json")
    common_profile = strict_json(plan / "common_profile_v3.json")
    v6_profile = strict_json(v6_profile_path)
    manifest = strict_json(manifest_path)
    auer_bindings = strict_json(auer_bindings_path)

    closure_path = fixture_dir / "source_closure_fixture.json"
    closure_rel = closure_path.resolve().relative_to(PROJECT.resolve()).as_posix()
    auer_profile["source_closure_manifest_path"] = closure_rel
    common_profile["source_closure_manifest_path"] = closure_rel
    auer_fixture = fixture_dir / "auer_profile_fixture.json"
    common_fixture = fixture_dir / "common_profile_fixture.json"
    v6_fixture = fixture_dir / "v6_profile_fixture.json"
    auer_bindings_fixture = fixture_dir / "auer_bindings_fixture.json"
    auer_fixture_rel = auer_fixture.resolve().relative_to(PROJECT.resolve()).as_posix()
    auer_fixture_sha_before_bindings = None
    _dump(auer_fixture, auer_profile)
    _dump(common_fixture, common_profile)
    _dump(v6_fixture, v6_profile)

    # Give the copied native binding its own exact fixture profile path/hash.
    # These are nonquery-only documents; the real candidate remains untouched.
    auer_fixture_sha_before_bindings = sha256_file(auer_fixture)
    auer_bindings["native_source_snapshot_path"] = snapshot_path.relative_to(PROJECT).as_posix()
    auer_bindings["native_source_snapshot_sha256"] = sha256_file(snapshot_path)
    for entry in auer_bindings["bindings"]:
        entry["native_binding"]["resource_profile_path"] = auer_fixture_rel
        entry["native_binding"]["resource_profile_sha256"] = auer_fixture_sha_before_bindings
    _dump(auer_bindings_fixture, auer_bindings)
    manifest["task_protocol_path"] = task_path.relative_to(PROJECT).as_posix()
    manifest["task_protocol_sha256"] = sha256_file(task_path)
    manifest["peer_release_path"] = release_path.relative_to(PROJECT).as_posix()
    manifest["peer_release_sha256"] = sha256_file(release_path)
    manifest["benchmark_path"] = (PLAN_REL / "benchmark_v3.json").as_posix()
    manifest["benchmark_sha256"] = sha256_file(plan / "benchmark_v3.json")
    manifest_fixture = fixture_dir / "auer_manifest_fixture.json"
    _dump(manifest_fixture, manifest)
    protocol_for_fixture = copy.deepcopy(protocol)
    protocol_for_fixture["benchmark"] = {
        "path": (PLAN_REL / "benchmark_v3.json").as_posix(),
        "sha256": sha256_file(plan / "benchmark_v3.json"),
    }
    for action in protocol_for_fixture["actions"]:
        row = next(item for item in auer_bindings["bindings"] if item["comparison_id"] == action["auer_id"])
        action["auer_native_binding_sha256"] = _native_binding_sha(row["native_binding"])

    bindings = [strict_json(plan / "v6_bindings" / f"{i:02d}.json") for i in (1, 2, 3)]
    pinned: set[str] = set()
    for binding in bindings:
        pinned.update(binding.get("source_files", {}).keys())
    pinned.update({
        "AGENTS.md",
        "docs/DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2.md",
        "docs/CODEX_TO_LUNA_G4_AUTONOMOUS_COMPLETION_W2.md",
        "docs/CODEX_W2_V6_MATCHED_TASK_FALSIFICATION.md",
        "docs/CODEX_W2_V6_MATCHED_BINDING_CORRECTION_CONTINUATION.md",
        "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_19.json",
        "coordination/autonomous_w2/g4/STATUS_W2_SEQUENCE_09.json",
        "coordination/autonomous_w2/g2/G4_INPUT_CRITERION_SUPPORT_v1.md",
        "coordination/autonomous_w2/g2/G4_WRAPPER_INPUT_SCORER_AUDIT_v1.md",
        "coordination/autonomous_w2/g2/G4_WRAPPER_INPUT_SCORER_AUDIT_v2.md",
        "coordination/autonomous_w2/g2/G4_WRAPPER_INPUT_SCORER_AUDIT_v3.md",
        "coordination/autonomous_w2/g4/G4_TO_G2_V6_MATCHED_INPUT_MAPPING_V5.md",
        "coordination/autonomous_w2/g4/G4_TO_G2_V3_SOURCE_REAUDIT_REQUEST_v1.md",
        "coordination/autonomous_w2/g4/G4_TO_G2_V3_SOURCE_REAUDIT_REQUEST_v2.md",
        "coordination/autonomous_w2/g4/G4_TO_G2_V3_SOURCE_REAUDIT_REQUEST_v3.md",
        protocol_path.relative_to(PROJECT).as_posix(),
        manifest_path.relative_to(PROJECT).as_posix(),
        snapshot_path.relative_to(PROJECT).as_posix(),
        task_path.relative_to(PROJECT).as_posix(),
        release_path.relative_to(PROJECT).as_posix(),
        v6_profile_path.relative_to(PROJECT).as_posix(),
        "research/autonomous_w2/g4/matched_v6_task_development_v3/auer_profile_v3.json",
        "research/autonomous_w2/g4/matched_v6_task_development_v3/common_profile_v3.json",
        (FIXTURE_REL / "auer_profile_fixture.json").as_posix(),
        (FIXTURE_REL / "common_profile_fixture.json").as_posix(),
        (FIXTURE_REL / "v6_profile_fixture.json").as_posix(),
        (FIXTURE_REL / "auer_bindings_fixture.json").as_posix(),
        (FIXTURE_REL / "auer_manifest_fixture.json").as_posix(),
        "validation/autonomous_w2/g4/v6_w2_worker_v3.py",
        "validation/autonomous_w2/g4/auer_w2_worker_v3.py",
        "validation/autonomous_w2/g4/v6_w2_adapter_v3.py",
        "validation/autonomous_w2/g4/auer_w2_adapter_v3.py",
        "validation/autonomous_w2/g4/matched_v6_common_v3.py",
        "validation/autonomous_w2/g4/run_matched_v6_w2_v3.py",
        "validation/autonomous_w2/g4/windows_job_supervisor_v3.py",
        "validation/autonomous_w2/g4/preflight_matched_v6_v3.py",
        "validation/autonomous_w2/g4/finalize_matched_v6_w2_v3.py",
        "validation/autonomous_w2/g4/v6_snapshot_v3/__init__.py",
        "validation/autonomous_w2/g4/v6_snapshot_v3/checker_centered_v6.py",
        "validation/autonomous_w2/g4/v6_snapshot_v3/producer_centered_v6.py",
        "validation/autonomous_w2/g4/v6_snapshot_v3/producer_v4.py",
        "validation/autonomous_w2/g4/v6_snapshot_v3/rational_interval_v3.py",
        "validation/autonomous_w2/g4/auer_snapshot_v3/__init__.py",
        "validation/autonomous_w2/g4/auer_snapshot_v3/solver_r9_w2.py",
        "validation/autonomous_w2/g4/auer_snapshot_v3/replay_r9_w2.py",
        "validation/autonomous_w2/g4/auer_snapshot_v3/rhs.py",
        "validation/autonomous_w2/g4/auer_snapshot_v3/piecewise.py",
    })
    pinned.update(row["native_case_path"] for row in manifest.get("cases", []))
    pinned.add((PLAN_REL / "benchmark_v3.json").as_posix())
    pinned.add(auer_bindings_fixture.resolve().relative_to(PROJECT.resolve()).as_posix())
    closure = {
        "schema": "ddwmr-g4-w2-v3-preflight-source-closure-fixture",
        "status": "NONQUERY_FIXTURE_ONLY",
        "files": sorted((_entry(PROJECT / rel) for rel in pinned), key=lambda row: row["path"]),
    }
    _dump(closure_path, closure)
    closure_sha = sha256_file(closure_path)

    receipt_rel = (FIXTURE_REL / "freeze_receipt_fixture.json").as_posix()
    freeze_rel = (FIXTURE_REL / "freeze_manifest_fixture.json").as_posix()
    actions = protocol["actions"]
    freeze = {
        "schema": "ddwmr-g4-w2-v3-preflight-freeze-fixture",
        "status": "NONQUERY_FIXTURE_ONLY",
        "protocol_path": protocol_path.relative_to(PROJECT).as_posix(),
        "protocol_sha256": sha256_file(protocol_path),
        "source_closure_path": closure_rel,
        "source_closure_sha256": closure_sha,
        "freeze_receipt_path": receipt_rel,
        "benchmark_path": (PLAN_REL / "benchmark_v3.json").as_posix(),
        "benchmark_sha256": sha256_file(plan / "benchmark_v3.json"),
        "auer_manifest_path": manifest_fixture.resolve().relative_to(PROJECT.resolve()).as_posix(),
        "auer_manifest_sha256": sha256_file(manifest_fixture),
        "auer_bindings_path": auer_bindings_fixture.resolve().relative_to(PROJECT.resolve()).as_posix(),
        "auer_bindings_sha256": sha256_file(auer_bindings_fixture),
        "native_source_snapshot_path": snapshot_path.relative_to(PROJECT).as_posix(),
        "native_source_snapshot_sha256": sha256_file(snapshot_path),
        "task_protocol": {"path": task_path.relative_to(PROJECT).as_posix(), "sha256": sha256_file(task_path)},
        "peer_release": {"path": release_path.relative_to(PROJECT).as_posix(), "sha256": sha256_file(release_path)},
        "native_source_snapshot_sha256": sha256_file(snapshot_path),
        "v6_profile_path": v6_fixture.relative_to(PROJECT).as_posix(),
        "auer_profile_path": auer_fixture.relative_to(PROJECT).as_posix(),
        "common_profile_path": common_fixture.relative_to(PROJECT).as_posix(),
        "method_worker_modules": V6_EXPECTED_ROUTES,
        "actions": protocol_for_fixture["actions"],
        "primary_criterion": protocol["primary_criterion"],
        "v6_binding_paths": {row["comparison_id"]: row["binding_path"] for row in bindings},
        "auer_binding_paths": {row["comparison_id"]: auer_bindings_fixture.resolve().relative_to(PROJECT.resolve()).as_posix() for row in auer_bindings["bindings"]},
    }
    freeze_path = fixture_dir / "freeze_manifest_fixture.json"
    _dump(freeze_path, freeze)
    receipt = {
        "schema": "ddwmr-g4-w2-v3-preflight-receipt-fixture",
        "freeze_manifest_path": freeze_rel,
        "freeze_manifest_sha256": sha256_file(freeze_path),
        "protocol_path": freeze["protocol_path"],
        "protocol_sha256": freeze["protocol_sha256"],
        "source_closure_path": closure_rel,
        "source_closure_sha256": closure_sha,
    }
    receipt_path = fixture_dir / "freeze_receipt_fixture.json"
    _dump(receipt_path, receipt)
    return freeze, receipt, closure, {
        "protocol": protocol_for_fixture,
        "manifest": manifest,
        "bindings": auer_bindings,
        "auer_bindings_path": auer_bindings_fixture,
    }


def _rejection(
    name: str, call: Callable[[], Any], expected_fragment: str, *,
    output_dir: Path | None = None, producer_calls: list[str] | None = None,
    calls_before: int | None = None,
) -> dict[str, Any]:
    try:
        call()
    except Exception as exc:
        reason = str(exc)
        passed = expected_fragment in reason
        marker_present = bool(output_dir and (output_dir / "producer_start.json").exists())
        producer_call_delta = (
            len(producer_calls) - calls_before
            if producer_calls is not None and calls_before is not None else None
        )
        if marker_present or producer_call_delta not in (None, 0):
            passed = False
        return {
            "fixture": name,
            "result": "PASS_REJECTED" if passed else "FAIL_WRONG_REJECTION_OR_AFTER_MARKER",
            "reason": reason,
            "producer_marker_present": marker_present,
            "producer_stub_calls_delta": producer_call_delta,
        }
    return {"fixture": name, "result": "FAIL_ACCEPTED_TAMPER", "reason": None}


def _stop_fixtures() -> list[dict[str, Any]]:
    test_cases = [
        ("completed_valid_replayed", {"job_status": "COMPLETED", "worker_result_summary": {
            "native_status": "CERTIFIED", "final_status": "CERTIFIED", "task_eligible": True,
            "native_replay_status": "PASS", "common_replay_status": "PASS"}}, False),
        ("completed_proof_unknown", {"job_status": "COMPLETED", "worker_result_summary": {
            "native_status": "UNKNOWN", "final_status": "UNKNOWN"}}, False),
        ("explicit_arithmetic_or_worker_resource", {"job_status": "COMPLETED", "worker_result_summary": {
            "native_status": "RESOURCE_LIMIT", "final_status": "RESOURCE_LIMIT"}}, False),
        ("explicit_supervisor_wall", {"job_status": "WALL_LIMIT", "worker_result_summary": {}}, False),
        ("explicit_supervisor_cpu", {"job_status": "CPU_LIMIT", "worker_result_summary": {}}, False),
        ("explicit_supervisor_output", {"job_status": "STDOUT_OR_STDERR_LIMIT", "worker_result_summary": {}}, False),
        ("binding_or_replay_failure", {"job_status": "COMPLETED", "worker_result_summary": {
            "native_status": "IMPLEMENTATION_FAILURE"}}, True),
        ("common_replay_missing", {"job_status": "COMPLETED", "worker_result_summary": {
            "native_status": "CERTIFIED", "final_status": "CERTIFIED", "task_eligible": True,
            "native_replay_status": "PASS"}}, True),
        ("ambiguous_child_exit", {"job_status": "JOB_LIMIT_OR_CHILD_FAILURE", "worker_result_summary": {}}, True),
        ("nonzero_exit_even_if_error_mentions_limit", {"job_status": "NONZERO_EXIT", "worker_result_summary": {
            "native_status": "IMPLEMENTATION_FAILURE", "termination": "ValueError:LIMIT"}}, True),
    ]
    results = []
    for name, receipt, expected_stop in test_cases:
        stop, decision = runner.receipt_stop_decision(receipt)
        passed = stop is expected_stop
        results.append({"fixture": name, "result": "PASS" if passed else "FAIL", "stop": stop, "decision": decision})
    return results


def _scorer_fixtures() -> list[dict[str, Any]]:
    task = strict_json(PROJECT / "research/autonomous_w2/g2/task_protocol_v1.json")
    benchmark = strict_json(PROJECT / PLAN_REL / "benchmark_v3.json")
    budget = Budget(max_bits=32768, max_operations=2_000_000)
    initial = initial_state_from_task(task, budget)
    parameter_order = [row["name"] for row in benchmark["parameter_labels"]]
    label_ranges = {
        row["name"]: Interval.from_json(row["range"], budget)
        for row in benchmark["parameter_labels"]
    }
    state = initial
    first_start = state
    first_end = list(state)
    first_end[0] = Interval(
        state[0].lo + Fraction(2999, 10000),
        state[0].hi + Fraction(3001, 10000), budget,
    )
    first_hull = list(state)
    first_hull[0] = Interval(state[0].lo, first_end[0].hi, budget)
    second_end = list(first_end)
    second_end[0] = Interval(
        first_end[0].lo + Fraction(2999, 10000),
        first_end[0].hi + Fraction(3001, 10000), budget,
    )
    second_hull = list(state)
    second_hull[0] = Interval(first_end[0].lo, second_end[0].hi, budget)
    first_segment = TubeSegment.from_total_hull(
        segment_id="fixture_constant_first_half",
        t_start=Fraction(0), t_end=Fraction(1), state_hull=tuple(first_hull),
        labels=tuple((name, label_ranges[name]) for name in parameter_order),
        endpoint_start=first_start, endpoint_end=tuple(first_end),
        provenance={"fixture_only": True, "native_ivp_proof": False},
    )
    second_segment = TubeSegment.from_total_hull(
        segment_id="fixture_constant_second_half",
        t_start=Fraction(1), t_end=Fraction(2), state_hull=tuple(second_hull),
        labels=tuple((name, label_ranges[name]) for name in parameter_order),
        endpoint_start=tuple(first_end), endpoint_end=tuple(second_end),
        provenance={"fixture_only": True, "native_ivp_proof": False},
    )
    segments = (first_segment, second_segment)
    record = check_tube_segments(
        segments, benchmark, scene_from_task(task), Fraction(2), budget,
        initial_state=initial, sqrt_bisections=128,
    )
    expected_horizon = Fraction(2)
    valid = replay_common_record_semantics(
        record, benchmark, scene_from_task(task), expected_horizon, initial, budget,
        sqrt_bisections=128,
    )
    results = [{
        "fixture": "common_scorer_valid_record_replay",
        "result": "PASS" if valid.get("replayed") is True else "FAIL",
        "predicate_status": record.get("predicate_status"),
        "replay": valid,
        "native_calls": 0,
    }]
    label_names = [row["name"] for row in benchmark["parameter_labels"]]
    serialized_segments = record["segments"]
    mutated_records: list[tuple[str, dict[str, Any]]] = []
    omitted = copy.deepcopy(record)
    omitted["segments"] = []
    mutated_records.append(("common_scorer_omitted_slab_rejected", omitted))
    gap = copy.deepcopy(record)
    gap["segments"][0]["time_closed"]["end"] = {"num": "1", "den": "2"}
    mutated_records.append(("common_scorer_gap_or_incomplete_hold_rejected", gap))
    labels_changed = copy.deepcopy(record)
    labels_changed["segments"][0]["fixed_labels"].pop(label_names[0])
    mutated_records.append(("common_scorer_altered_label_image_rejected", labels_changed))
    geometry_changed = copy.deepcopy(record)
    geometry_changed["segment_checks"][0]["contact"]["margin_lower"] = {"num": "999", "den": "1"}
    mutated_records.append(("common_scorer_tampered_contact_result_rejected", geometry_changed))
    for name, candidate in mutated_records:
        replay = replay_common_record_semantics(
            candidate, benchmark, scene_from_task(task), expected_horizon, initial, budget,
            sqrt_bisections=128,
        )
        results.append({
            "fixture": name,
            "result": "PASS" if replay.get("replayed") is False else "FAIL",
            "replay": replay,
            "native_calls": 0,
        })
    progress_segments = tuple(
        TubeSegment.from_json(row, label_names, budget) for row in serialized_segments
    )
    valid_progress = common_progress(progress_segments)
    progress_replay = replay_common_progress_record(record, valid_progress, benchmark, budget)
    results.append({
        "fixture": "common_scorer_progress_record_replay",
        "result": "PASS" if progress_replay.get("replayed") is True else "FAIL",
        "replay": progress_replay,
        "native_calls": 0,
    })
    changed_progress = copy.deepcopy(valid_progress)
    changed_progress["progress_enclosure_m"][0] = {"num": "0", "den": "1"}
    changed_replay = replay_common_progress_record(record, changed_progress, benchmark, budget)
    results.append({
        "fixture": "common_scorer_tampered_progress_rejected",
        "result": "PASS" if changed_replay.get("replayed") is False else "FAIL",
        "replay": changed_replay,
        "native_calls": 0,
    })
    wrong_horizon = copy.deepcopy(record)
    wrong_horizon["inputs"]["horizon"] = {"num": "1", "den": "1"}
    horizon_replay = replay_common_record_semantics(
        wrong_horizon, benchmark, scene_from_task(task), expected_horizon, initial, budget,
        sqrt_bisections=128,
    )
    results.append({
        "fixture": "common_scorer_wrong_horizon_rejected",
        "result": "PASS" if horizon_replay.get("replayed") is False
                           and "horizon differs" in horizon_replay.get("detail", "") else "FAIL",
        "replay": horizon_replay, "native_calls": 0,
    })
    wrong_initial = copy.deepcopy(record)
    wrong_initial["inputs"]["initial_state"][3][0]["num"] = "1"
    initial_replay = replay_common_record_semantics(
        wrong_initial, benchmark, scene_from_task(task), expected_horizon, initial, budget,
        sqrt_bisections=128,
    )
    results.append({
        "fixture": "common_scorer_wrong_initial_state_rejected",
        "result": "PASS" if initial_replay.get("replayed") is False
                           and "initial state differs" in initial_replay.get("detail", "") else "FAIL",
        "replay": initial_replay, "native_calls": 0,
    })
    _dump(PROJECT / FIXTURE_REL / "common_scorer_valid_record_fixture.json", record)
    return results


def _live_candidate_provenance_checks() -> list[dict[str, Any]]:
    """Audit actual on-disk v3 docs before any in-memory fixture adaptation."""
    plan = PROJECT / PLAN_REL
    protocol = strict_json(plan / "protocol_v3.json")
    manifest = strict_json(plan / "auer_input_manifest_v3.json")
    binding_doc = strict_json(plan / "auer_bindings_v3.json")
    snapshot_rel = (PLAN_REL / "native_source_snapshot_v3.json").as_posix()
    snapshot_sha = sha256_file(plan / "native_source_snapshot_v3.json")
    benchmark_rel = (PLAN_REL / "benchmark_v3.json").as_posix()
    benchmark_sha = sha256_file(plan / "benchmark_v3.json")
    cases = {row["comparison_id"]: row for row in manifest["cases"]}
    bindings = {row["comparison_id"]: row["native_binding"] for row in binding_doc["bindings"]}
    actions = {row["auer_id"]: row for row in protocol["actions"]}
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: Any = None) -> None:
        checks.append({"fixture": name, "result": "PASS" if ok else "FAIL", "detail": detail, "native_calls": 0})

    expected_benchmark = {"path": benchmark_rel, "sha256": benchmark_sha}
    case_benchmark_pins_ok = all(
        (PROJECT / row["native_case_path"]).is_file()
        and strict_json(PROJECT / row["native_case_path"]).get("benchmark_path") == benchmark_rel
        and strict_json(PROJECT / row["native_case_path"]).get("benchmark_sha256") == benchmark_sha
        for row in manifest["cases"]
    )
    add("live_protocol_benchmark_path_hash", protocol.get("benchmark") == expected_benchmark,
        {"actual": protocol.get("benchmark"), "expected": expected_benchmark})
    add("live_manifest_benchmark_path_hash",
        manifest.get("benchmark_path") == benchmark_rel and manifest.get("benchmark_sha256") == benchmark_sha,
        {"path": manifest.get("benchmark_path"), "sha256": manifest.get("benchmark_sha256")})
    add("live_binding_document_snapshot_path_hash",
        binding_doc.get("native_source_snapshot_path") == snapshot_rel
        and binding_doc.get("native_source_snapshot_sha256") == snapshot_sha,
        {"path": binding_doc.get("native_source_snapshot_path"),
         "sha256": binding_doc.get("native_source_snapshot_sha256"), "actual_sha256": snapshot_sha})
    add("live_protocol_manifest_case_freeze_benchmark_agreement",
        protocol.get("benchmark") == expected_benchmark
        and manifest.get("benchmark_path") == benchmark_rel
        and manifest.get("benchmark_sha256") == benchmark_sha
        and case_benchmark_pins_ok,
        {"protocol": protocol.get("benchmark"), "manifest_path": manifest.get("benchmark_path"),
         "manifest_sha256": manifest.get("benchmark_sha256"), "native_case_pins_match": case_benchmark_pins_ok,
         "benchmark_sha256": benchmark_sha})
    add("live_three_way_action_mapping", set(actions) == set(cases) == set(bindings) and len(actions) == 3,
        {"protocol_ids": sorted(actions), "manifest_ids": sorted(cases), "binding_ids": sorted(bindings)})
    for auer_id in sorted(actions):
        action, case, binding = actions[auer_id], cases[auer_id], bindings[auer_id]
        case_path = PROJECT / case["native_case_path"]
        case_sha = sha256_file(case_path)
        digest_ok = (
            semantic_sha256(case["canonical_physical_input"]) == case["physical_input_sha256"]
            and semantic_sha256(case["payload"]) == case["payload_sha256"]
            and case["native_case_sha256"] == case_sha
        )
        native_case = strict_json(case_path)
        digest_ok = digest_ok and (
            native_case.get("canonical_physical_input_sha256") == case["physical_input_sha256"]
            and native_case.get("benchmark_path") == benchmark_rel
            and native_case.get("benchmark_sha256") == benchmark_sha
        )
        add(f"live_auer_input_and_case_pins:{auer_id}", digest_ok, {
            "case_path": case["native_case_path"], "case_sha256": case_sha,
            "physical_sha256": case["physical_input_sha256"], "payload_sha256": case["payload_sha256"],
        })
        binding_ok = (
            binding.get("input_path") == case["native_case_path"]
            and binding.get("input_sha256") == case_sha
            and binding.get("source_snapshot_manifest_sha256") == snapshot_sha
            and action.get("auer_native_binding_sha256") == _native_binding_sha(binding)
            and action.get("auer_native_input_file_sha256") == case_sha
            and action.get("auer_native_input_path") == case["native_case_path"]
        )
        add(f"live_auer_binding_path_hash_pair:{auer_id}", binding_ok)
    return checks


def run() -> dict[str, Any]:
    freeze, receipt, fixture_closure, auer_fixture = _fixture_documents()
    results: list[dict[str, Any]] = _live_candidate_provenance_checks()
    digest_semantic = semantic_sha256({"a": 1})
    digest_proof = proof_object_sha256({"a": 1})
    results.append({
        "fixture": "semantic_and_proof_digest_known_answer",
        "result": "PASS" if (
            digest_semantic == "015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862"
            and digest_proof == "e346432021b04179518d9614f3560ccd71354a4ee101ddcb893d6959a9d6301c"
            and digest_semantic != digest_proof
        ) else "FAIL",
        "semantic_json_sha256": digest_semantic,
        "native_proof_json_sha256": digest_proof,
        "newline_convention": "semantic input/payload excludes LF; native proof-object digest includes LF",
        "native_calls": 0,
    })
    producer_calls: list[str] = []
    fixture_run_id = uuid.uuid4().hex[:8]

    def producer_must_not_run(*_args: Any, **_kwargs: Any) -> Any:
        producer_calls.append("called")
        raise AssertionError("FIXTURE_PRODUCER_MUST_NOT_BE_CALLED")

    old_producer = worker.evaluate_bound_row
    worker.evaluate_bound_row = producer_must_not_run
    try:
        for ordinal in (1, 2, 3):
            binding_path = PROJECT / PLAN_REL / "v6_bindings" / f"{ordinal:02d}.json"
            output_dir = PROJECT / FIXTURE_REL / f"worker_boundary_valid_{ordinal:02d}_{fixture_run_id}"
            before = len(producer_calls)
            try:
                worker.run(
                    binding_path, output_dir, freeze_override=freeze,
                    receipt_override=receipt, preflight_fixture=True,
                )
            except AssertionError as exc:
                if str(exc) != "FIXTURE_PRODUCER_MUST_NOT_BE_CALLED":
                    raise
            if len(producer_calls) != before + 1 or not (output_dir / "producer_start.json").is_file():
                raise AssertionError(f"VALID_WORKER_BOUNDARY_NOT_REACHED:{ordinal}")
            setup = worker.validate_v6_setup(
                binding_path, freeze=freeze, receipt=receipt, preflight_fixture=True,
            )
            results.append({
                "fixture": f"valid_worker_route_boundary_{ordinal:02d}", "result": "PASS",
                "comparison_id": setup["binding"]["comparison_id"],
                "binding_sha256": setup["binding_sha256"],
                "saved_row_sha256": setup["saved_row_sha256"],
                "producer_entrypoint_stub_calls": len(producer_calls),
                "numeric_producer_calls": 0,
                "producer_start_marker_fixture_only": True,
            })
        binding_path = PROJECT / PLAN_REL / "v6_bindings/01.json"
        base = strict_json(binding_path)

        def mutated(binding_mutator: Callable[[dict[str, Any]], None] | None = None,
                    freeze_mutator: Callable[[dict[str, Any]], None] | None = None,
                    receipt_mutator: Callable[[dict[str, Any]], None] | None = None,
                    protocol_mutator: Callable[[dict[str, Any]], None] | None = None,
                    expected: str = "") -> tuple[Callable[[], Any], Path]:
            binding = copy.deepcopy(base)
            test_freeze, test_receipt = copy.deepcopy(freeze), copy.deepcopy(receipt)
            protocol = copy.deepcopy(strict_json(PROJECT / PLAN_REL / "protocol_v3.json"))
            if binding_mutator:
                binding_mutator(binding)
            if freeze_mutator:
                freeze_mutator(test_freeze)
            if receipt_mutator:
                receipt_mutator(test_receipt)
            if protocol_mutator:
                protocol_mutator(protocol)
            output_dir = PROJECT / FIXTURE_REL / f"invalid_{expected.replace(':', '_').replace('/', '_')}_{fixture_run_id}"
            return (lambda: worker.run(
                binding_path, output_dir,
                freeze_override=test_freeze, receipt_override=test_receipt,
                binding_override=binding, protocol_override=protocol, preflight_fixture=True,
            ), output_dir)

        mutations: list[tuple[str, Callable[[], Any], str]] = [
            ("missing_required_saved_row_hash", mutated(lambda b: b.pop("peer_saved_row_sha256"), expected="REQUIRED_BINDING_FIELD_MISSING:peer_saved_row_sha256"), "REQUIRED_BINDING_FIELD_MISSING:peer_saved_row_sha256"),
            ("wrong_saved_row_hash_pair", mutated(lambda b: b["source_files"].update({b["peer_saved_row_path"]: "0" * 64}), expected="SAVED_ROW_PATH_HASH_PAIR_MISMATCH"), "SAVED_ROW_PATH_HASH_PAIR_MISMATCH"),
            ("wrong_saved_row_path", mutated(lambda b: b.update(peer_saved_row_path="../../escape.json"), expected="PATH_ESCAPES_PROJECT:PEER_SAVED_ROW"), "PATH_"),
            ("wrong_action_id", mutated(lambda b: b.update(action_id="wrong-action"), expected="OUTER_BINDING_CORE_ACTION_ID_MISMATCH"), "OUTER_BINDING_CORE_ACTION_ID_MISMATCH"),
            ("wrong_physical_input_digest", mutated(lambda b: b.update(physical_input_sha256="0" * 64), expected="CANONICAL_PHYSICAL_INPUT_BINDING"), "CANONICAL_PHYSICAL_INPUT_BINDING"),
            ("changed_peer_release_pin", mutated(lambda b: b.update(peer_release_sha256="0" * 64), expected="PEER_RELEASE_BINDING_MISMATCH"), "PEER_RELEASE_BINDING_MISMATCH"),
            ("changed_core_hash_pin", mutated(lambda b: b.update(core_binding_sha256="0" * 64), expected="CORE_BINDING_PATH_HASH_PAIR_MISMATCH"), "CORE_BINDING_PATH_HASH_PAIR_MISMATCH"),
            ("changed_source_pin", mutated(lambda b: b["source_files"].update({"coordination/autonomous_w2/g2/releases/RELEASE_v6.json": "0" * 64}), expected="SOURCE_PIN_MISMATCH"), "SOURCE_PIN_MISMATCH"),
            ("duplicate_action_mapping", mutated(protocol_mutator=lambda p: p["actions"][1].update(comparison_id=p["actions"][0]["comparison_id"]), expected="DUPLICATE_FROZEN_ACTION_MAPPING"), "DUPLICATE_FROZEN_ACTION_MAPPING"),
            ("missing_action_mapping", mutated(protocol_mutator=lambda p: p["actions"].pop(), expected="FROZEN_ACTION_COUNT_NOT_THREE"), "FROZEN_ACTION_COUNT_NOT_THREE"),
            ("stale_receipt_reference", mutated(freeze_mutator=lambda f: f.update(freeze_receipt_path="results/old_receipt.json"), expected="AUTHORITATIVE_FREEZE_RECEIPT_PATH_MISMATCH"), "AUTHORITATIVE_FREEZE_RECEIPT_PATH_MISMATCH"),
            ("stale_closure_reference", mutated(freeze_mutator=lambda f: f.update(source_closure_path="results/old_closure.json"), expected="RECEIPT_SOURCE_CLOSURE_PATH_MISMATCH"), "RECEIPT_SOURCE_CLOSURE_PATH_MISMATCH"),
            ("stale_receipt_closure_hash", mutated(receipt_mutator=lambda r: r.update(source_closure_sha256="0" * 64), expected="RECEIPT_SOURCE_CLOSURE_HASH_MISMATCH"), "RECEIPT_SOURCE_CLOSURE_HASH_MISMATCH"),
        ]
        for name, call_and_dir, expected in mutations:
            call, output_dir = call_and_dir
            before = len(producer_calls)
            results.append(_rejection(name, call, expected, output_dir=output_dir,
                                      producer_calls=producer_calls, calls_before=before))
    finally:
        worker.evaluate_bound_row = old_producer

    # Exercise the actual frozen module route through both setup guards. Auer's
    # producer is replaced after setup so the fixture proves the real worker
    # reaches its producer boundary without performing a numerical query.
    actual_manifest_path = PROJECT / PLAN_REL / "auer_input_manifest_v3.json"
    actual_manifest_sha = sha256_file(actual_manifest_path)
    auer_calls: list[str] = []

    def auer_producer_must_not_run(*_args: Any, **_kwargs: Any) -> Any:
        auer_calls.append("called")
        raise AssertionError("FIXTURE_AUER_PRODUCER_MUST_NOT_BE_CALLED")

    old_auer_producer = auer_worker.solve_ddwmr_case
    auer_worker.solve_ddwmr_case = auer_producer_must_not_run
    try:
        for action in auer_fixture["protocol"]["actions"]:
            comparison_id = action["auer_id"]
            native_binding = next(row["native_binding"] for row in auer_fixture["bindings"]["bindings"]
                                  if row["comparison_id"] == comparison_id)
            output_dir = PROJECT / FIXTURE_REL / f"auer_worker_boundary_{action['ordinal']:02d}_{fixture_run_id}"
            output_dir.mkdir(parents=True, exist_ok=True)
            before = len(auer_calls)
            try:
                auer_worker.run(
                    comparison_id, output_dir, preflight_fixture=True,
                    setup_overrides={
                        "binding_override": native_binding,
                        "protocol_override": auer_fixture["protocol"],
                        "freeze_override": freeze,
                        "receipt_override": receipt,
                        "manifest_override": auer_fixture["manifest"],
                    },
                )
            except AssertionError as exc:
                if str(exc) != "FIXTURE_AUER_PRODUCER_MUST_NOT_BE_CALLED":
                    raise
            marker = output_dir / "producer_start.json"
            if len(auer_calls) != before + 1 or not marker.is_file():
                raise AssertionError(f"VALID_AUER_WORKER_BOUNDARY_NOT_REACHED:{comparison_id}")
            setup = auer_worker.validate_auer_setup(
                comparison_id, preflight_fixture=True,
                binding_override=native_binding,
                protocol_override=auer_fixture["protocol"],
                freeze_override=freeze,
                receipt_override=receipt,
                manifest_override=auer_fixture["manifest"],
            )
            results.append({
                "fixture": f"valid_auer_worker_route_boundary_{action['ordinal']:02d}",
                "result": "PASS", "comparison_id": comparison_id,
                "peer_action_id": setup["item"]["peer_action_id"],
                "native_case_sha256": setup["item"]["native_case_sha256"],
                "producer_stub_calls": len(auer_calls), "native_calls": 0,
            })

        base_action = auer_fixture["protocol"]["actions"][0]
        base_id = base_action["auer_id"]
        base_binding = copy.deepcopy(next(row["native_binding"] for row in auer_fixture["bindings"]["bindings"]
                                          if row["comparison_id"] == base_id))

        def auer_mutation(
            name: str,
            *,
            protocol_mutator: Callable[[dict[str, Any]], None] | None = None,
            manifest_mutator: Callable[[dict[str, Any]], None] | None = None,
            binding_mutator: Callable[[dict[str, Any]], None] | None = None,
            bindings_doc_mutator: Callable[[dict[str, Any]], None] | None = None,
            receipt_mutator: Callable[[dict[str, Any]], None] | None = None,
            case_mutator: Callable[[dict[str, Any]], None] | None = None,
            binding_rehash: bool = False,
            expected: str,
        ) -> tuple[Callable[[], Any], str, Path]:
            test_freeze = copy.deepcopy(freeze)
            test_protocol = copy.deepcopy(auer_fixture["protocol"])
            test_manifest = copy.deepcopy(auer_fixture["manifest"])
            test_binding = copy.deepcopy(base_binding)
            test_bindings_doc = copy.deepcopy(auer_fixture["bindings"])
            test_receipt = copy.deepcopy(receipt)
            test_case = strict_json(PROJECT / test_manifest["cases"][0]["native_case_path"])
            if protocol_mutator:
                protocol_mutator(test_protocol)
            if manifest_mutator:
                manifest_mutator(test_manifest)
            if binding_mutator:
                binding_mutator(test_binding)
            if bindings_doc_mutator:
                bindings_doc_mutator(test_bindings_doc)
            if receipt_mutator:
                receipt_mutator(test_receipt)
            if case_mutator:
                case_mutator(test_case)
            test_freeze["actions"] = copy.deepcopy(test_protocol["actions"])
            if binding_rehash:
                row = next(row for row in test_protocol["actions"] if row["auer_id"] == base_id)
                row["auer_native_binding_sha256"] = _native_binding_sha(test_binding)
                test_freeze["actions"] = copy.deepcopy(test_protocol["actions"])
            output_dir = PROJECT / FIXTURE_REL / f"auer_invalid_{name}_{fixture_run_id}"
            overrides = {
                "binding_override": test_binding,
                "bindings_doc_override": test_bindings_doc,
                "protocol_override": test_protocol,
                "freeze_override": test_freeze,
                "receipt_override": test_receipt,
                "manifest_override": test_manifest,
                "case_override": test_case if case_mutator else None,
            }
            return (
                lambda: auer_worker.run(
                    base_id, output_dir, preflight_fixture=True, setup_overrides=overrides,
                ),
                expected,
                output_dir,
            )

        def mutate_action(name: str, fn: Callable[[dict[str, Any]], None]) -> Callable[[dict[str, Any]], None]:
            def apply(protocol_doc: dict[str, Any]) -> None:
                row = next(item for item in protocol_doc["actions"] if item["auer_id"] == base_id)
                fn(row)
            return apply

        auer_mutations = [
            ("wrong_action_voltage", *auer_mutation(
                "wrong_action_voltage",
                protocol_mutator=mutate_action("wrong_action_voltage", lambda row: row.update(voltage=["1/2", "1/2"])),
                expected="AUER_ACTION_VOLTAGE_OR_ORDER_MISMATCH")),
            ("wrong_physical_digest", *auer_mutation(
                "wrong_physical_digest",
                protocol_mutator=mutate_action("wrong_physical_digest", lambda row: row.update(physical_input_sha256="0" * 64)),
                expected="AUER_ACTION_PHYSICAL_DIGEST_MISMATCH")),
            ("wrong_peer_action_mapping", *auer_mutation(
                "wrong_peer_action_mapping",
                protocol_mutator=mutate_action("wrong_peer_action_mapping", lambda row: row.update(peer_action_id="W2_G2_DEV_001_NOMINAL")),
                expected="AUER_ACTION_VOLTAGE_OR_ORDER_MISMATCH")),
            ("wrong_native_case_file_digest", *auer_mutation(
                "wrong_native_case_file_digest",
                protocol_mutator=mutate_action("wrong_native_case_file_digest", lambda row: row.update(auer_native_input_file_sha256="0" * 64)),
                expected="AUER_NATIVE_FILE_DIGEST_BINDING")),
            ("stale_protocol_benchmark_pin", *auer_mutation(
                "stale_protocol_benchmark_pin",
                protocol_mutator=lambda doc: doc.update(benchmark={
                    "path": "research/autonomous_w2/g4/matched_v6_task_development_v3/benchmark_v3.json",
                    "sha256": "0" * 64,
                }),
                expected="AUER_PROTOCOL_BENCHMARK_BINDING_MISMATCH")),
            ("duplicate_manifest_mapping", *auer_mutation(
                "duplicate_manifest_mapping",
                manifest_mutator=lambda doc: doc["cases"][1].update(comparison_id=doc["cases"][0]["comparison_id"]),
                expected="AUER_DUPLICATE_MANIFEST_MAPPING")),
            ("missing_manifest_mapping", *auer_mutation(
                "missing_manifest_mapping", manifest_mutator=lambda doc: doc["cases"].pop(),
                expected="AUER_CANONICAL_CASE_COUNT_NOT_THREE")),
            ("native_case_path_escape", *auer_mutation(
                "native_case_path_escape",
                protocol_mutator=mutate_action("native_case_path_escape", lambda row: row.update(auer_native_input_path="../../escape.json")),
                manifest_mutator=lambda doc: doc["cases"][0].update(native_case_path="../../escape.json"),
                expected="AUER_PATH_INVALID:CASE")),
            ("native_case_wrong_voltage", *auer_mutation(
                "native_case_wrong_voltage", case_mutator=lambda doc: doc.update(held_voltage=[{"num": "1", "den": "1"}, {"num": "1", "den": "1"}]),
                expected="AUER_NATIVE_CASE_ACTION_VOLTAGE")),
            ("native_case_wrong_initial_box", *auer_mutation(
                "native_case_wrong_initial_box", case_mutator=lambda doc: doc["initial_state"][0][0].update(num="2"),
                expected="AUER_NATIVE_CASE_INITIAL_BOX")),
            ("native_case_wrong_labels", *auer_mutation(
                "native_case_wrong_labels", case_mutator=lambda doc: doc["fixed_labels"].pop("rho_L"),
                expected="AUER_NATIVE_CASE_FIXED_LABEL_SET")),
            ("native_case_wrong_horizon", *auer_mutation(
                "native_case_wrong_horizon", case_mutator=lambda doc: doc["horizon"].update(num="1"),
                expected="AUER_NATIVE_CASE_HORIZON")),
            ("native_case_wrong_scene", *auer_mutation(
                "native_case_wrong_scene", case_mutator=lambda doc: doc["scene"].update(id="tampered_scene"),
                expected="AUER_NATIVE_CASE_SCENE")),
            ("native_case_wrong_parameter_cell", *auer_mutation(
                "native_case_wrong_parameter_cell", case_mutator=lambda doc: doc["parameter_cell"]["labels"].pop("rho_L"),
                expected="AUER_NATIVE_CASE_PARAMETER_CELL")),
            ("native_binding_missing_required_field", *auer_mutation(
                "native_binding_missing_required_field", binding_mutator=lambda doc: doc.pop("resource_profile_path"),
                binding_rehash=True, expected="AUER_NATIVE_BINDING_FIELD_MISSING:resource_profile_path")),
            ("stale_binding_doc_snapshot_path", *auer_mutation(
                "stale_binding_doc_snapshot_path",
                bindings_doc_mutator=lambda doc: doc.update(native_source_snapshot_path="results/stale_snapshot.json"),
                expected="AUER_BINDING_DOC_SOURCE_SNAPSHOT_PATH_MISMATCH")),
            ("stale_binding_doc_snapshot_hash", *auer_mutation(
                "stale_binding_doc_snapshot_hash",
                bindings_doc_mutator=lambda doc: doc.update(native_source_snapshot_sha256="0" * 64),
                expected="AUER_BINDING_DOC_SOURCE_SNAPSHOT_HASH_MISMATCH")),
            ("stale_receipt_closure_path", *auer_mutation(
                "stale_receipt_closure_path",
                receipt_mutator=lambda doc: doc.update(source_closure_path="results/stale_closure.json"),
                expected="AUER_RECEIPT_CLOSURE_PATH_BINDING")),
            ("stale_receipt_closure_hash", *auer_mutation(
                "stale_receipt_closure_hash",
                receipt_mutator=lambda doc: doc.update(source_closure_sha256="0" * 64),
                expected="AUER_RECEIPT_CLOSURE_HASH_BINDING")),
            ("stale_profile_closure_path", *auer_mutation(
                "stale_profile_closure_path",
                protocol_mutator=None,
                expected="AUER_PROFILE_SOURCE_CLOSURE_PATH_STALE")),
        ]
        for name, call, expected, output_dir in auer_mutations:
            if name == "stale_profile_closure_path":
                # Change only an in-memory profile copy and route it through a
                # hash-consistent fixture freeze; no candidate profile bytes move.
                stale_freeze = copy.deepcopy(freeze)
                stale_profile = strict_json(PROJECT / FIXTURE_REL / "auer_profile_fixture.json")
                stale_profile["source_closure_manifest_path"] = "results/old/source_closure.json"
                profile_fixture = PROJECT / FIXTURE_REL / "auer_profile_stale_path_fixture.json"
                _dump(profile_fixture, stale_profile)
                stale_freeze["auer_profile_path"] = profile_fixture.relative_to(PROJECT).as_posix()
                custom_common = strict_json(PROJECT / FIXTURE_REL / "common_profile_fixture.json")
                custom_common["source_closure_manifest_path"] = (FIXTURE_REL / "source_closure_stale_profile_fixture.json").as_posix()
                custom_common_path = PROJECT / FIXTURE_REL / "common_profile_stale_path_fixture.json"
                _dump(custom_common_path, custom_common)
                stale_freeze["common_profile_path"] = custom_common_path.relative_to(PROJECT).as_posix()
                closure_doc = strict_json(PROJECT / FIXTURE_REL / "source_closure_fixture.json")
                closure_doc["files"].append(_entry(profile_fixture))
                closure_doc["files"].append(_entry(custom_common_path))
                closure_doc["files"].sort(key=lambda item: item["path"])
                closure_path = PROJECT / FIXTURE_REL / "source_closure_stale_profile_fixture.json"
                _dump(closure_path, closure_doc)
                closure_sha = sha256_file(closure_path)
                stale_freeze["source_closure_path"] = closure_path.relative_to(PROJECT).as_posix()
                stale_freeze["source_closure_sha256"] = closure_sha
                stale_receipt = copy.deepcopy(receipt)
                stale_receipt["source_closure_path"] = stale_freeze["source_closure_path"]
                stale_receipt["source_closure_sha256"] = closure_sha
                output_dir = PROJECT / FIXTURE_REL / f"auer_invalid_{name}_{fixture_run_id}"
                stale_call = lambda: auer_worker.run(
                    base_id, output_dir,
                    preflight_fixture=True,
                    setup_overrides={
                        "binding_override": base_binding,
                        "protocol_override": auer_fixture["protocol"],
                        "freeze_override": stale_freeze,
                        "receipt_override": stale_receipt,
                        "manifest_override": auer_fixture["manifest"],
                    },
                )
                before = len(auer_calls)
                results.append(_rejection(name, stale_call, expected, output_dir=output_dir,
                                          producer_calls=auer_calls, calls_before=before))
            else:
                before = len(auer_calls)
                results.append(_rejection(name, call, expected, output_dir=output_dir,
                                          producer_calls=auer_calls, calls_before=before))
        module_commands = {
            "v6": [sys.executable, "-B", "-m", "validation.autonomous_w2.g4.v6_w2_worker_v3", "--help"],
            "auer": [sys.executable, "-B", "-m", "validation.autonomous_w2.g4.auer_w2_worker_v3", "--help"],
        }
        for method, command in module_commands.items():
            process = subprocess.run(command, cwd=PROJECT, capture_output=True, timeout=15, check=False)
            results.append({
                "fixture": f"actual_python_module_entrypoint_{method}",
                "result": "PASS" if process.returncode == 0 else "FAIL",
                "returncode": process.returncode,
                "native_calls": 0,
            })
    finally:
        auer_worker.solve_ddwmr_case = old_auer_producer
    if len(auer_calls) != 3:
        results.append({"fixture": "auer_producer_stub_route_count", "result": "FAIL", "count": len(auer_calls)})
    else:
        results.append({"fixture": "auer_producer_stub_route_count", "result": "PASS", "count": len(auer_calls)})

    if len(producer_calls) != 3:
        results.append({"fixture": "producer_stub_route_count", "result": "FAIL", "count": len(producer_calls)})
    else:
        results.append({"fixture": "producer_stub_route_count", "result": "PASS", "count": len(producer_calls)})
    stop_results = _stop_fixtures()
    results.extend(stop_results)
    results.extend(_scorer_fixtures())
    passed = all(item["result"].startswith("PASS") for item in results)
    source_paths = (
        "validation/autonomous_w2/g4/preflight_matched_v6_v3.py",
        "validation/autonomous_w2/g4/finalize_matched_v6_w2_v3.py",
        "validation/autonomous_w2/g4/v6_w2_worker_v3.py",
        "validation/autonomous_w2/g4/auer_w2_worker_v3.py",
        "validation/autonomous_w2/g4/v6_w2_adapter_v3.py",
        "validation/autonomous_w2/g4/auer_w2_adapter_v3.py",
        "validation/autonomous_w2/g4/matched_v6_common_v3.py",
        "validation/autonomous_w2/g4/run_matched_v6_w2_v3.py",
        "validation/autonomous_w2/g4/windows_job_supervisor_v3.py",
        "validation/g4/common_tube.py",
    )
    source_hashes = {path: sha256_file(PROJECT / path) for path in source_paths}
    input_hashes = {row["path"]: row["sha256"] for row in fixture_closure["files"]}
    report = {
        "schema": "ddwmr-g4-w2-v3-nonquery-setup-and-stop-fixtures",
        "session": "DDWMR | LUNA-G4-AUER",
        "result": "PASS_NONQUERY_FIXTURES" if passed else "FAIL_NONQUERY_FIXTURES",
        "native_calls": 0,
        "numeric_producer_calls": 0,
        "v6_producer_stub_invocations": len(producer_calls),
        "auer_solver_stub_invocations": len(auer_calls),
        "producer_marker_written_by_fixtures_only": True,
        "source_hashes": source_hashes,
        "preflight_source_path": "validation/autonomous_w2/g4/preflight_matched_v6_v3.py",
        "preflight_source_sha256": source_hashes["validation/autonomous_w2/g4/preflight_matched_v6_v3.py"],
        "input_hashes": input_hashes,
        "auer_manifest_preflight_sha256": actual_manifest_sha,
        "checks_count": len(results),
        "pass_count": sum(item["result"].startswith("PASS") for item in results),
        "fail_count": sum(not item["result"].startswith("PASS") for item in results),
        "freeze_fixture_sha256": sha256_file(PROJECT / FIXTURE_REL / "freeze_manifest_fixture.json"),
        "receipt_fixture_sha256": sha256_file(PROJECT / FIXTURE_REL / "freeze_receipt_fixture.json"),
        "closure_fixture_sha256": sha256_file(PROJECT / FIXTURE_REL / "source_closure_fixture.json"),
        "cases": results,
    }
    out = PROJECT / FIXTURE_REL / "preflight_report_v4.json"
    _dump(out, report)
    return report


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
