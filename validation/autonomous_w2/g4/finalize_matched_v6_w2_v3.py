"""Finalize the G4 v3 source pins and create its immutable W2 freeze."""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validation.autonomous_w2.g4.matched_v6_common_v3 import (
    PLAN_REL, PROJECT, RESULT_REL, canonical_sha256, sha256_file, strict_json, write_json,
)

STATUS_PATH = Path("coordination/autonomous_w2/g4/STATUS_W2_SEQUENCE_09.json")
TASK_PATH = Path("research/autonomous_w2/g2/task_protocol_v1.json")
RELEASE_PATH = Path("coordination/autonomous_w2/g2/releases/RELEASE_v6.json")
G2_STATUS_PATH = Path("coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_19.json")
FIXTURE_REL = RESULT_REL / "nonquery_fixtures_v5"


def _relative(path: Path) -> str:
    return path.resolve().relative_to(PROJECT.resolve()).as_posix()


def _entry(path: Path, role: str) -> dict[str, Any]:
    return {
        "path": _relative(path),
        "role": role,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def _dump(path: Path, value: Any, *, exclusive: bool = False) -> str:
    digest, _ = write_json(path, value, max_bytes=8_388_608, exclusive=exclusive)
    return digest


def _native_binding_sha(value: dict[str, Any]) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"
    return hashlib.sha256(raw).hexdigest()


def _assert_exact_peer_bytes() -> None:
    expected = {
        TASK_PATH: "8bc1c8fd460a62dc3f7ff1c8e4bef2dbaddbcaffbadd75d6c2c487e9e311c15a",
        RELEASE_PATH: "789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55",
        Path("validation/autonomous_w2/g2/profile_centered_v6.json"):
            "8252ceecd3a07c9811fd601945d16b9f33318d120340441c3fff94b117ee03a2",
    }
    for rel, wanted in expected.items():
        if sha256_file(PROJECT / rel) != wanted:
            raise RuntimeError(f"PEER_OWNED_INPUT_CHANGED:{rel.as_posix()}")
    plan = PROJECT / PLAN_REL
    for local_name, source in (
        ("g2_task_protocol_v1.json", TASK_PATH),
        ("g2_release_v6.json", RELEASE_PATH),
        ("g2_profile_centered_v6.json", Path("validation/autonomous_w2/g2/profile_centered_v6.json")),
    ):
        if sha256_file(plan / local_name) != sha256_file(PROJECT / source):
            raise RuntimeError(f"CANDIDATE_PEER_COPY_NOT_BYTE_IDENTICAL:{local_name}")


def _update_bindings() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    plan = PROJECT / PLAN_REL
    protocol_path = plan / "protocol_v3.json"
    manifest_path = plan / "auer_input_manifest_v3.json"
    bindings_path = plan / "auer_bindings_v3.json"
    snapshot_path = plan / "native_source_snapshot_v3.json"
    task_path = PROJECT / TASK_PATH
    release_path = PROJECT / RELEASE_PATH
    profile_path = plan / "auer_profile_v3.json"
    common_profile_path = plan / "common_profile_v3.json"
    benchmark_path = plan / "benchmark_v3.json"

    for path in (protocol_path, manifest_path, bindings_path, snapshot_path, task_path,
                 release_path, profile_path, common_profile_path, benchmark_path):
        if not path.is_file():
            raise FileNotFoundError(f"CANDIDATE_REQUIRED_FILE_MISSING:{_relative(path)}")

    protocol = strict_json(protocol_path)
    manifest = strict_json(manifest_path)
    auer_bindings = strict_json(bindings_path)
    snapshot = strict_json(snapshot_path)
    peer_release = strict_json(release_path)
    g2_status = strict_json(PROJECT / G2_STATUS_PATH)
    profile = strict_json(profile_path)
    common_profile = strict_json(common_profile_path)

    if protocol.get("task_protocol", {}).get("path") != TASK_PATH.as_posix():
        raise RuntimeError("PROTOCOL_TASK_PATH_STALE")
    if protocol.get("task_protocol", {}).get("sha256") != sha256_file(task_path):
        raise RuntimeError("PROTOCOL_TASK_HASH_STALE")
    if protocol.get("peer_release", {}).get("path") != RELEASE_PATH.as_posix():
        raise RuntimeError("PROTOCOL_PEER_RELEASE_PATH_STALE")
    if protocol.get("peer_release", {}).get("sha256") != sha256_file(release_path):
        raise RuntimeError("PROTOCOL_PEER_RELEASE_HASH_STALE")
    if g2_status.get("release", {}).get("sha256") != sha256_file(release_path):
        raise RuntimeError("G2_STATUS_RELEASE_BINDING_MISMATCH")

    # This protocol action refers to the same benchmark bytes that the manifest,
    # native cases, profile, and freeze consume. Refresh both path and digest.
    protocol["benchmark"] = {
        "path": _relative(benchmark_path),
        "sha256": sha256_file(benchmark_path),
    }
    protocol["peer_source_audit"] = {
        "path": "coordination/autonomous_w2/g2/G4_WRAPPER_INPUT_SCORER_AUDIT_v3.md",
        "sha256": sha256_file(PROJECT / "coordination/autonomous_w2/g2/G4_WRAPPER_INPUT_SCORER_AUDIT_v3.md"),
        "disposition": "PARTIAL at the audit snapshot; G4's corrected v3 source set is separately bound to re-audit request v3",
    }
    protocol["peer_reaudit_request"] = {
        "path": "coordination/autonomous_w2/g4/G4_TO_G2_V3_SOURCE_REAUDIT_REQUEST_v3.md",
        "sha256": sha256_file(PROJECT / "coordination/autonomous_w2/g4/G4_TO_G2_V3_SOURCE_REAUDIT_REQUEST_v3.md"),
    }

    profile["protocol_candidate"] = _relative(protocol_path)
    profile["source_closure_manifest_path"] = (RESULT_REL / "source_closure_v4.json").as_posix()
    profile["source_snapshot_manifest_path"] = _relative(snapshot_path)
    profile["external_guard_reference"] = "validation/autonomous_w2/g4/windows_job_supervisor_v3.py"
    profile["external_guard_reference_sha256"] = sha256_file(PROJECT / profile["external_guard_reference"])
    common_profile["protocol_candidate"] = _relative(protocol_path)
    common_profile["source_closure_manifest_path"] = (RESULT_REL / "source_closure_v4.json").as_posix()
    _dump(profile_path, profile)
    _dump(common_profile_path, common_profile)

    copies = snapshot.get("copies")
    if not isinstance(copies, list) or not copies:
        raise RuntimeError("NATIVE_SOURCE_SNAPSHOT_COPY_LIST_INVALID")
    for copy in copies:
        snap_path = PROJECT / copy["snapshot_path"]
        origin_path = PROJECT / copy["origin_path"]
        if not snap_path.is_file() or not origin_path.is_file():
            raise RuntimeError(f"NATIVE_SOURCE_SNAPSHOT_FILE_MISSING:{copy.get('snapshot_path')}")
        actual_snapshot = sha256_file(snap_path)
        if copy.get("snapshot_sha256") != actual_snapshot:
            raise RuntimeError(f"NATIVE_SOURCE_SNAPSHOT_HASH_STALE:{copy['snapshot_path']}")
        if copy.get("origin_sha256") != sha256_file(origin_path):
            raise RuntimeError(f"NATIVE_SOURCE_ORIGIN_HASH_STALE:{copy['origin_path']}")

    actions = protocol.get("actions")
    ordered = protocol.get("ordered_actions")
    cases = manifest.get("cases")
    binding_rows = auer_bindings.get("bindings")
    if (not isinstance(actions, list) or len(actions) != 3
            or not isinstance(ordered, list) or len(ordered) != 3
            or not isinstance(cases, list) or len(cases) != 3
            or not isinstance(binding_rows, list) or len(binding_rows) != 3):
        raise RuntimeError("FROZEN_THREE_ACTION_INPUT_COUNTS_REQUIRED")

    manifest["task_protocol_path"] = TASK_PATH.as_posix()
    manifest["task_protocol_sha256"] = sha256_file(task_path)
    manifest["peer_release_path"] = RELEASE_PATH.as_posix()
    manifest["peer_release_sha256"] = sha256_file(release_path)
    manifest["benchmark_path"] = _relative(benchmark_path)
    manifest["benchmark_sha256"] = sha256_file(benchmark_path)

    # Keep the binding document's top-level source-snapshot pin in agreement
    # with every nested native binding and the freeze manifest.
    auer_bindings["native_source_snapshot_path"] = _relative(snapshot_path)
    auer_bindings["native_source_snapshot_sha256"] = sha256_file(snapshot_path)

    binding_by_id: dict[str, dict[str, Any]] = {}
    for row in binding_rows:
        comparison_id = row.get("comparison_id")
        native = row.get("native_binding")
        if not isinstance(comparison_id, str) or not isinstance(native, dict) or comparison_id in binding_by_id:
            raise RuntimeError("AUER_NATIVE_BINDING_ID_MAP_INVALID")
        binding_by_id[comparison_id] = native
        case = next((item for item in cases if item.get("comparison_id") == comparison_id), None)
        if case is None:
            raise RuntimeError(f"AUER_BINDING_WITHOUT_MANIFEST_CASE:{comparison_id}")
        case_path = PROJECT / case["native_case_path"]
        case_hash = sha256_file(case_path)
        case["native_case_sha256"] = case_hash
        native["input_path"] = case["native_case_path"]
        native["input_sha256"] = case_hash
        native["resource_profile_path"] = _relative(profile_path)
        native["resource_profile_sha256"] = sha256_file(profile_path)
        native["source_snapshot_manifest_sha256"] = sha256_file(snapshot_path)
        native["solver_source_sha256"] = sha256_file(PROJECT / "validation/autonomous_w2/g4/auer_snapshot_v3/solver_r9_w2.py")
        native["checker_source_sha256"] = sha256_file(PROJECT / "validation/autonomous_w2/g4/auer_snapshot_v3/replay_r9_w2.py")
        native["method_contract_sha256"] = sha256_file(PROJECT / native["method_contract_path"])
        native["arithmetic_backend_manifest_sha256"] = sha256_file(PROJECT / native["arithmetic_backend_manifest_path"])
        if native.get("source_snapshot_manifest_sha256") != auer_bindings["native_source_snapshot_sha256"]:
            raise RuntimeError(f"AUER_NESTED_SOURCE_SNAPSHOT_PIN_MISMATCH:{comparison_id}")
        row["native_case_path"] = case["native_case_path"]
        row["native_case_sha256"] = case_hash
        row["physical_input_sha256"] = case["physical_input_sha256"]

    # Preserve peer-owned source pins exactly; refresh only the G4-owned/candidate
    # side of each outer binding, then recompute the protocol's binding hashes.
    peer_roots = ("coordination/autonomous_w2/g2/", "research/autonomous_w2/g2/",
                  "results/validation/autonomous_w2/g2/", "validation/autonomous_w2/g2/")
    local_pins = {
        "validation/autonomous_w2/g4/v6_w2_worker_v3.py",
        "validation/autonomous_w2/g4/auer_w2_worker_v3.py",
        "validation/autonomous_w2/g4/v6_w2_adapter_v3.py",
        "validation/autonomous_w2/g4/auer_w2_adapter_v3.py",
        "validation/autonomous_w2/g4/matched_v6_common_v3.py",
        "validation/autonomous_w2/g4/run_matched_v6_w2_v3.py",
        "validation/autonomous_w2/g4/windows_job_supervisor_v3.py",
        "validation/autonomous_w2/g4/preflight_matched_v6_v3.py",
        "validation/autonomous_w2/g4/finalize_matched_v6_w2_v3.py",
        "coordination/autonomous_w2/g4/G4_TO_G2_V3_SOURCE_REAUDIT_REQUEST_v3.md",
        "validation/g4/common_tube.py", "validation/g2/rational.py", "validation/g2/interval.py",
        "validation/g2/model.py", "validation/g2/polynomial.py", "validation/g2/hashing.py",
        _relative(manifest_path), _relative(bindings_path),
        _relative(snapshot_path), _relative(benchmark_path), _relative(profile_path),
        _relative(common_profile_path), "research/autonomous_w2/g4/matched_v6_task_development_v3/g2_task_protocol_v1.json",
        "research/autonomous_w2/g4/matched_v6_task_development_v3/g2_release_v6.json",
    }
    local_pins.update(_relative(path) for path in (PROJECT / "validation/autonomous_w2/g4/v6_snapshot_v3").rglob("*.py"))
    local_pins.update(_relative(path) for path in (PROJECT / "validation/autonomous_w2/g4/auer_snapshot_v3").rglob("*.py"))
    local_pins.update(case["native_case_path"] for case in cases)
    # Flush these two inputs before refreshing the v6 outer source maps. They
    # are pinned by each outer binding, so writing them afterwards would make
    # the just-written source_files hashes stale.
    _dump(manifest_path, manifest)
    _dump(bindings_path, auer_bindings)

    for ordinal, action in enumerate(actions, 1):
        binding_path = plan / "v6_bindings" / f"{ordinal:02d}.json"
        binding = strict_json(binding_path)
        if binding.get("comparison_id") != action.get("comparison_id"):
            raise RuntimeError(f"V6_OUTER_BINDING_ID_MISMATCH:{ordinal}")
        if binding.get("binding_path") != _relative(binding_path):
            raise RuntimeError(f"V6_OUTER_BINDING_PATH_STALE:{ordinal}")
        if binding.get("peer_release_sha256") != sha256_file(release_path):
            raise RuntimeError(f"V6_OUTER_BINDING_PEER_RELEASE_MISMATCH:{ordinal}")
        if binding.get("native_task_protocol_sha256") != sha256_file(task_path):
            raise RuntimeError(f"V6_OUTER_BINDING_TASK_PROTOCOL_MISMATCH:{ordinal}")
        if binding.get("profile_sha256") != sha256_file(PROJECT / binding["profile_path"]):
            raise RuntimeError(f"V6_OUTER_BINDING_PROFILE_HASH_MISMATCH:{ordinal}")
        sources = binding.get("source_files")
        if not isinstance(sources, dict):
            raise RuntimeError(f"V6_OUTER_BINDING_SOURCE_MAP_MISSING:{ordinal}")
        sources.update({path: sha256_file(PROJECT / path) for path in local_pins})
        for path, wanted in list(sources.items()):
            source_path = PROJECT / path
            actual = sha256_file(source_path)
            if path.startswith(peer_roots):
                if actual != wanted:
                    raise RuntimeError(f"PEER_PIN_CHANGED:{path}")
            else:
                sources[path] = actual
        for path, wanted in ((binding["peer_saved_row_path"], binding["peer_saved_row_sha256"]),
                             (binding["core_binding_path"], binding["core_binding_sha256"])):
            if sources.get(path) != wanted or sha256_file(PROJECT / path) != wanted:
                raise RuntimeError(f"V6_EXPLICIT_PATH_HASH_PAIR_MISMATCH:{ordinal}:{path}")
        _dump(binding_path, binding)
        action["native_binding_sha256"] = sha256_file(binding_path)
        action["v6_native_binding_sha256"] = action["native_binding_sha256"]
        action["v6_native_binding_input_sha256"] = binding["core_binding_sha256"]
        action["v6_native_input_sha256"] = binding["core_binding_sha256"]

    for action in actions:
        auer_id = action["auer_id"]
        case = next(row for row in cases if row["comparison_id"] == auer_id)
        action["auer_native_input_path"] = case["native_case_path"]
        action["auer_native_input_file_sha256"] = case["native_case_sha256"]
        action["auer_input_digest"] = case["physical_input_sha256"]
        action["auer_native_binding_sha256"] = _native_binding_sha(binding_by_id[auer_id])

    if set(binding_by_id) != {action.get("auer_id") for action in actions}:
        raise RuntimeError("AUER_BINDING_ACTION_BIJECTION_MISMATCH")
    _dump(protocol_path, protocol)
    return protocol, manifest, auer_bindings


def _source_closure(protocol: dict[str, Any], manifest: dict[str, Any], auer_bindings: dict[str, Any]) -> list[dict[str, Any]]:
    plan = PROJECT / PLAN_REL
    paths: dict[str, str] = {}

    def add(relative: str, role: str) -> None:
        path = PROJECT / relative
        if not path.is_file():
            raise FileNotFoundError(f"SOURCE_CLOSURE_FILE_MISSING:{relative}")
        paths.setdefault(relative.replace("\\", "/"), role)

    required = {
        "AGENTS.md": "workspace_contract",
        "docs/DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2.md": "workflow",
        "docs/CODEX_TO_LUNA_G4_AUTONOMOUS_COMPLETION_W2.md": "assignment",
        "docs/CODEX_W2_V6_MATCHED_TASK_FALSIFICATION.md": "comparison_assignment",
        "docs/CODEX_W2_V6_MATCHED_BINDING_CORRECTION_CONTINUATION.md": "correction_assignment",
        "research_context/MASTER_RESEARCH_CONTEXT_v2.md": "canonical_model_context",
        "research_context/DECISION_LOG.md": "canonical_decision_context",
        "research_context/LITERATURE_MATRIX.md": "canonical_literature_context",
        "research_context/REVIEW_GATE.md": "canonical_gate_context",
        G2_STATUS_PATH.as_posix(): "peer_status_snapshot",
        STATUS_PATH.as_posix(): "g4_status_phase_start_snapshot",
        "coordination/autonomous_w2/g2/G4_INPUT_CRITERION_SUPPORT_v1.md": "peer_input_and_criterion_support",
        "coordination/autonomous_w2/g2/G4_WRAPPER_INPUT_SCORER_AUDIT_v1.md": "peer_source_audit",
        "coordination/autonomous_w2/g2/G4_WRAPPER_INPUT_SCORER_AUDIT_v2.md": "peer_source_audit_current",
        "coordination/autonomous_w2/g2/G4_WRAPPER_INPUT_SCORER_AUDIT_v3.md": "peer_source_audit_latest",
        "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_19.json": "peer_audit_status_snapshot",
        "coordination/autonomous_w2/g4/G4_TO_G2_V3_SOURCE_REAUDIT_REQUEST_v1.md": "peer_source_reaudit_request_v1",
        "coordination/autonomous_w2/g4/G4_TO_G2_V3_SOURCE_REAUDIT_REQUEST_v2.md": "peer_source_reaudit_request_v2",
        "coordination/autonomous_w2/g4/G4_TO_G2_V3_SOURCE_REAUDIT_REQUEST_v3.md": "peer_source_reaudit_request_v3",
        "coordination/autonomous_w2/g4/G4_TO_G2_V6_MATCHED_INPUT_MAPPING_V5.md": "matched_input_mapping",
        (PLAN_REL / "protocol_v3.json").as_posix(): "frozen_protocol",
        (PLAN_REL / "benchmark_v3.json").as_posix(): "common_benchmark",
        (PLAN_REL / "auer_input_manifest_v3.json").as_posix(): "auer_native_input_manifest",
        (PLAN_REL / "auer_bindings_v3.json").as_posix(): "auer_native_binding_doc",
        (PLAN_REL / "native_source_snapshot_v3.json").as_posix(): "native_source_snapshot_map",
        (PLAN_REL / "g2_task_protocol_v1.json").as_posix(): "peer_task_protocol_copy",
        (PLAN_REL / "g2_release_v6.json").as_posix(): "peer_release_copy",
        (PLAN_REL / "g2_profile_centered_v6.json").as_posix(): "peer_profile_copy",
        (PLAN_REL / "auer_profile_v3.json").as_posix(): "auer_numerical_profile",
        (PLAN_REL / "common_profile_v3.json").as_posix(): "common_scorer_profile",
        (FIXTURE_REL / "preflight_report_v4.json").as_posix(): "nonquery_preproducer_fixture_report",
        (FIXTURE_REL / "common_scorer_valid_record_fixture.json").as_posix(): "common_scorer_nonquery_fixture",
    }
    for rel, role in required.items():
        add(rel, role)
    executable = (
        "validation/autonomous_w2/g4/v6_w2_worker_v3.py",
        "validation/autonomous_w2/g4/auer_w2_worker_v3.py",
        "validation/autonomous_w2/g4/v6_w2_adapter_v3.py",
        "validation/autonomous_w2/g4/auer_w2_adapter_v3.py",
        "validation/autonomous_w2/g4/matched_v6_common_v3.py",
        "validation/autonomous_w2/g4/run_matched_v6_w2_v3.py",
        "validation/autonomous_w2/g4/windows_job_supervisor_v3.py",
        "validation/autonomous_w2/g4/preflight_matched_v6_v3.py",
        "validation/autonomous_w2/g4/finalize_matched_v6_w2_v3.py",
        "coordination/autonomous_w2/g4/G4_TO_G2_V3_SOURCE_REAUDIT_REQUEST_v3.md",
        "validation/g4/common_tube.py", "validation/g2/rational.py", "validation/g2/interval.py",
        "validation/g2/model.py", "validation/g2/polynomial.py", "validation/g2/hashing.py",
        "validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v2.json",
        "docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md",
    )
    for rel in executable:
        add(rel, "executable_or_method_dependency")
    for directory, role in (("validation/autonomous_w2/g4/v6_snapshot_v3", "v6_method_snapshot"),
                            ("validation/autonomous_w2/g4/auer_snapshot_v3", "auer_method_snapshot")):
        for path in sorted((PROJECT / directory).rglob("*.py")):
            add(_relative(path), role)
    for item in manifest["cases"]:
        add(item["native_case_path"], "auer_native_case")
    for ordinal, _action in enumerate(protocol["actions"], 1):
        binding_path = PLAN_REL / "v6_bindings" / f"{ordinal:02d}.json"
        binding_rel = binding_path.as_posix()
        binding = strict_json(PROJECT / binding_path)
        add(binding_rel, "v6_outer_binding")
        for source_rel in binding["source_files"]:
            add(source_rel, "v6_outer_binding_source")
        add(binding["core_binding_path"], "peer_v6_core_binding")
        add(binding["peer_saved_row_path"], "peer_v6_saved_row")
    return [_entry(PROJECT / rel, role) for rel, role in sorted(paths.items())]


def freeze() -> dict[str, Any]:
    plan = PROJECT / PLAN_REL
    result = PROJECT / RESULT_REL
    freeze_path = plan / "freeze_manifest_v4.json"
    closure_path = result / "source_closure_v4.json"
    receipt_path = result / "freeze_receipt_v4.json"
    if any(path.exists() for path in (freeze_path, closure_path, receipt_path)):
        raise FileExistsError("V4_FREEZE_ARTIFACT_ALREADY_EXISTS")
    if (PROJECT / "coordination/autonomous_w2/COMPUTE.lock").exists():
        raise RuntimeError("COMPUTE_LOCK_PRESENT_DURING_FREEZE")
    if not (PROJECT / FIXTURE_REL / "preflight_report_v4.json").is_file():
        raise RuntimeError("NONQUERY_FIXTURE_REPORT_MISSING")
    fixture = strict_json(PROJECT / FIXTURE_REL / "preflight_report_v4.json")
    if fixture.get("result") != "PASS_NONQUERY_FIXTURES" or fixture.get("native_calls") != 0:
        raise RuntimeError("NONQUERY_FIXTURES_NOT_PASS")
    protocol, manifest, auer_bindings = _update_bindings()
    if fixture.get("preflight_source_path") != "validation/autonomous_w2/g4/preflight_matched_v6_v3.py":
        raise RuntimeError("PREFLIGHT_SCRIPT_PATH_NOT_BOUND")
    if fixture.get("preflight_source_sha256") != sha256_file(PROJECT / fixture["preflight_source_path"]):
        raise RuntimeError("PREFLIGHT_SCRIPT_HASH_STALE")
    for field in ("source_hashes", "input_hashes"):
        entries = fixture.get(field)
        if not isinstance(entries, dict) or not entries:
            raise RuntimeError(f"PREFLIGHT_{field.upper()}_MISSING")
        for relative, wanted in entries.items():
            source_path = PROJECT / relative
            if not source_path.is_file() or sha256_file(source_path) != wanted:
                raise RuntimeError(f"PREFLIGHT_{field.upper()}_STALE:{relative}")
    if fixture.get("closure_fixture_sha256") != sha256_file(PROJECT / FIXTURE_REL / "source_closure_fixture.json"):
        raise RuntimeError("PREFLIGHT_FIXTURE_CLOSURE_HASH_STALE")
    closure_entries = _source_closure(protocol, manifest, auer_bindings)
    closure = {
        "schema": "ddwmr-g4-w2-matched-source-closure-v4",
        "session": "DDWMR | LUNA-G4-AUER",
        "status": "FROZEN_DEVELOPMENT_ONLY_W2",
        "method_worker_modules": {
            "v6": "validation.autonomous_w2.g4.v6_w2_worker_v3",
            "auer": "validation.autonomous_w2.g4.auer_w2_worker_v3",
        },
        "files": closure_entries,
        "file_count": len(closure_entries),
        "peer_owned_inputs_are_byte_pinned": True,
        "nonquery_native_calls": 0,
    }
    closure_sha = _dump(closure_path, closure, exclusive=True)

    task_path = PROJECT / TASK_PATH
    release_path = PROJECT / RELEASE_PATH
    g2_status_path = PROJECT / G2_STATUS_PATH
    snapshot_path = plan / "native_source_snapshot_v3.json"
    peer_task = {"path": TASK_PATH.as_posix(), "sha256": sha256_file(task_path)}
    peer_release = {"path": RELEASE_PATH.as_posix(), "sha256": sha256_file(release_path)}
    peer_status = {"path": G2_STATUS_PATH.as_posix(), "sha256": sha256_file(g2_status_path)}
    bindings = strict_json(plan / "auer_bindings_v3.json")
    v6_binding_paths = {
        action["comparison_id"]: (PLAN_REL / "v6_bindings" / f"{ordinal:02d}.json").as_posix()
        for ordinal, action in enumerate(protocol["actions"], 1)
    }
    auer_binding_paths = {
        row["comparison_id"]: (PLAN_REL / "auer_bindings_v3.json").as_posix()
        for row in bindings["bindings"]
    }
    start_utc = strict_json(PROJECT / STATUS_PATH)["phase_started_utc"]
    phase_start = datetime.fromisoformat(start_utc.replace("Z", "+00:00"))
    status = strict_json(PROJECT / STATUS_PATH)
    caps = status["resource_caps"]
    freeze_doc = {
        "schema": "ddwmr-g4-w2-matched-v6-auer-freeze-manifest-v4",
        "session": "DDWMR | LUNA-G4-AUER",
        "status": "FROZEN_DEVELOPMENT_ONLY_W2",
        "phase": "BOUNDED_DEVELOPMENT_FALSIFICATION",
        "protocol_path": (PLAN_REL / "protocol_v3.json").as_posix(),
        "protocol_sha256": sha256_file(plan / "protocol_v3.json"),
        "benchmark_path": (PLAN_REL / "benchmark_v3.json").as_posix(),
        "benchmark_sha256": sha256_file(plan / "benchmark_v3.json"),
        "auer_manifest_path": (PLAN_REL / "auer_input_manifest_v3.json").as_posix(),
        "auer_manifest_sha256": sha256_file(plan / "auer_input_manifest_v3.json"),
        "auer_bindings_path": (PLAN_REL / "auer_bindings_v3.json").as_posix(),
        "auer_bindings_sha256": sha256_file(plan / "auer_bindings_v3.json"),
        "task_protocol": peer_task,
        "peer_release": peer_release,
        "peer_status_snapshot": peer_status,
        "source_closure_path": _relative(closure_path),
        "source_closure_sha256": closure_sha,
        "native_source_snapshot_path": _relative(snapshot_path),
        "native_source_snapshot_sha256": sha256_file(snapshot_path),
        "v6_profile_path": (PLAN_REL / "g2_profile_centered_v6.json").as_posix(),
        "auer_profile_path": (PLAN_REL / "auer_profile_v3.json").as_posix(),
        "common_profile_path": (PLAN_REL / "common_profile_v3.json").as_posix(),
        "compute_lock_path": "coordination/autonomous_w2/COMPUTE.lock",
        "freeze_receipt_path": _relative(receipt_path),
        "primary_criterion": protocol["primary_criterion"],
        "ordered_actions": protocol["ordered_actions"],
        "actions": protocol["actions"],
        "v6_binding_paths": v6_binding_paths,
        "auer_binding_paths": auer_binding_paths,
        "method_worker_modules": {
            "v6": "validation.autonomous_w2.g4.v6_w2_worker_v3",
            "auer": "validation.autonomous_w2.g4.auer_w2_worker_v3",
        },
        "resource_caps": protocol["resource_caps"],
        "native_call_limits": {"v6": 3, "auer": 3, "retries": 0},
        "phase_wall_cap_seconds": caps["phase_wall_seconds"],
        "phase_started_utc": start_utc,
        "phase_started_epoch": phase_start.timestamp(),
        "run_order": "v6 zero, nominal, alternative; then local Auer zero, nominal, alternative; stop on any binding/implementation/audit defect",
        "development_data": "same three consumed G2 v6 development rows; not held-out confirmation",
        "confirmation_rows": {"v6": 0, "auer": 0},
        "no_retry": True,
        "no_800_row_or_1944_batch": True,
        "frozen_utc": datetime.now(timezone.utc).isoformat(),
    }
    freeze_sha = _dump(freeze_path, freeze_doc, exclusive=True)
    receipt_doc = {
        "schema": "ddwmr-g4-w2-matched-freeze-receipt-v4",
        "session": "DDWMR | LUNA-G4-AUER",
        "freeze_manifest_path": _relative(freeze_path),
        "freeze_manifest_sha256": freeze_sha,
        "protocol_path": freeze_doc["protocol_path"],
        "protocol_sha256": freeze_doc["protocol_sha256"],
        "source_closure_path": freeze_doc["source_closure_path"],
        "source_closure_sha256": closure_sha,
        "preflight_fixture_path": (FIXTURE_REL / "preflight_report_v4.json").as_posix(),
        "preflight_fixture_sha256": sha256_file(PROJECT / FIXTURE_REL / "preflight_report_v4.json"),
        "actions_frozen": 3,
        "native_calls_before_execution": {"v6": 0, "auer": 0},
        "native_call_limits": {"v6": 3, "auer": 3, "retries": 0},
        "confirmation_rows_before_execution": {"v6": 0, "auer": 0},
        "legacy_r5_800": "NOT_RUN",
        "auer_1944": "NOT_RUN",
        "source_closure_file_count": len(closure_entries),
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    receipt_sha = _dump(receipt_path, receipt_doc, exclusive=True)
    return {
        "freeze_manifest_path": _relative(freeze_path),
        "freeze_manifest_sha256": freeze_sha,
        "freeze_receipt_path": _relative(receipt_path),
        "freeze_receipt_sha256": receipt_sha,
        "source_closure_path": _relative(closure_path),
        "source_closure_sha256": closure_sha,
        "source_closure_file_count": len(closure_entries),
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--bind-only", action="store_true",
                        help="refresh candidate path/hash pins before the nonquery preflight; do not freeze")
    args = parser.parse_args()
    _assert_exact_peer_bytes()
    if args.bind_only:
        protocol, manifest, _bindings = _update_bindings()
        print(json.dumps({
            "binding_only": True,
            "protocol_sha256": sha256_file(PROJECT / PLAN_REL / "protocol_v3.json"),
            "benchmark_sha256": sha256_file(PROJECT / PLAN_REL / "benchmark_v3.json"),
            "manifest_sha256": sha256_file(PROJECT / PLAN_REL / "auer_input_manifest_v3.json"),
            "actions": len(protocol["actions"]),
            "cases": len(manifest["cases"]),
        }, sort_keys=True, indent=2))
        return 0
    result = freeze()
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
