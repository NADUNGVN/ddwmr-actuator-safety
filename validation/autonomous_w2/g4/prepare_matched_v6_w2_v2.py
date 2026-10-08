"""Build the versioned, pre-output W2 development comparison artifacts."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from validation.autonomous_w2.g4.preflight_mapping_v2 import (
    LABELS, PAIRS, PLAN, RELEASE, RELEASE_SHA, ROOT, TASK, TASK_SHA, physical_input, read, sha, canonical_sha,
)


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")
    path.write_bytes(raw)


def build() -> dict[str, Any]:
    task = read(TASK)
    benchmark = read(PLAN / "benchmark_v1.json")
    benchmark_path = PLAN / "benchmark_v2.json"
    benchmark["schema"] = "ddwmr-g4-w2-matched-v6-benchmark-v2"
    benchmark["source_spec"] = (PLAN / "protocol_v2.json").as_posix()
    benchmark["status"] = "FROZEN_DEVELOPMENT_ONLY_W2"
    write(ROOT / benchmark_path, benchmark)
    benchmark_sha = sha(ROOT / benchmark_path)
    g2_protocol_original = ROOT / TASK
    g2_profile_original = ROOT / "validation/autonomous_w2/g2/profile_centered_v6.json"
    g2_release_original = ROOT / RELEASE
    g2_protocol_path = PLAN / "g2_task_protocol_v1.json"
    g2_profile_path = PLAN / "g2_profile_centered_v6.json"
    g2_release_path = PLAN / "g2_release_v6.json"
    for src, dst in ((g2_protocol_original, ROOT / g2_protocol_path),
                     (g2_profile_original, ROOT / g2_profile_path),
                     (g2_release_original, ROOT / g2_release_path)):
        shutil.copyfile(src, dst)
    v6_profile_path = g2_profile_path
    v6_profile_sha = sha(ROOT / v6_profile_path)

    protocol = {
        "schema": "ddwmr-g4-w2-matched-v6-task-protocol-v2",
        "session": "DDWMR | LUNA-G4-AUER",
        "phase": "BOUNDED_DEVELOPMENT_FALSIFICATION",
        "status": "FROZEN_DEVELOPMENT_ONLY_W2",
        "classification": {
            "CERTIFIED": "fresh native proof completed, method-native independent replay passed, common full-hold collision/contact replay passed, and common progress lower bound is >=7/20",
            "PROOF_COMPLETE_COMMON_UNKNOWN": "native proof replay passes but the common full-hold collision/contact check is UNKNOWN",
            "CERTIFIED_SAFETY_TASK_INELIGIBLE": "common collision/contact replay passes and the common progress upper bound is <7/20",
            "SAFETY_CERTIFIED_PROGRESS_UNRESOLVED": "common collision/contact replay passes but the common progress interval straddles 7/20",
            "UNKNOWN": "proof-complete method-native UNKNOWN with no unsafe interpretation",
            "RESOURCE_LIMIT": "frozen worker/replay wall, memory, operation, bit, output, or proof-size cap stops work",
            "INVALID_OR_IMPLEMENTATION_FAILURE": "input, source, proof replay, common replay, binding, or execution defect; comparison conclusion is invalid",
        },
        "question": "On the exact G2 v6 synthetic 2-second task and the same three previously observed voltage actions, does the local Auer reconstruction also produce a replayed useful task certificate?",
        "primary_criterion": "For each method, report the exact set of actions whose independent method-native replay, common full-hold collision/contact replay, and common progress lower bound >=7/20 all pass; compare sets directly.",
        "secondary_metrics": [
            "common progress enclosure and width",
            "minimum common full-hold collision and contact margins",
            "proof byte count",
            "native worker wall/CPU/peak job memory",
            "native replay plus common adapter/check/replay wall/CPU/peak job memory",
            "combined offline validation cost per action",
        ],
        "task_protocol": {"path": TASK.as_posix(), "sha256": TASK_SHA},
        "peer_release": {"path": RELEASE.as_posix(), "sha256": RELEASE_SHA},
        "peer_status_snapshot": {
            "path": "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_18.json",
            "sha256": sha(ROOT / "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_18.json"),
            "sequence": 18,
            "phase": "FINISHED",
        },
        "benchmark": {"path": benchmark_path.as_posix(), "sha256": benchmark_sha},
        "common_target": {
            "hold_s": "2",
            "full_closed_hold_collision_contact": True,
            "collision": "inflated static circle center=(1/2,1/10) m, radius=3/50 m",
            "contact": "MASTER v2.1 algebraic tangential-reaction admissibility on the full hold",
            "progress": "p_x(T)-p_x(0)=integral_0^T u*cos(theta) dt",
            "required_progress_m": "7/20",
            "common_progress_rule": "intersection of same full-slab sum(duration*interval(u*cos(theta))) and common endpoint displacement enclosure for both methods",
        },
        "ordered_actions": [
            {
                "ordinal": ordinal,
                "external_id": v6_id,
                "auer_id": auer_id,
                "peer_action_id": peer_id,
                "voltage": list(voltage),
                "method_pair": ["centered_residual_v6", "local_auer2013_residual_picard_reconstruction"],
            }
            for ordinal, (v6_id, auer_id, peer_id, _native, voltage) in enumerate(PAIRS, 1)
        ],
        "actions": [
            {
                "ordinal": ordinal,
                "external_id": v6_id,
                "comparison_id": v6_id,
                "auer_id": auer_id,
                "peer_action_id": peer_id,
                "voltage": list(voltage),
                "physical_input_sha256": canonical_sha(physical_input(task, voltage)),
            }
            for ordinal, (v6_id, auer_id, peer_id, _native, voltage) in enumerate(PAIRS, 1)
        ],
        "development_data_status": {
            "v6_actions_already_observed_before_this_freeze": [item[2] for item in PAIRS],
            "all_three_are_consumed_development_data": True,
            "held_out_rows": 0,
            "confirmation_rows": 0,
            "not_a_statistical_sample": True,
        },
        "native_call_limits": {"v6": 3, "auer": 3, "per_action": 1, "retries": 0},
        "stop_policy": {
            "ordered_calls": "v6 zero, nominal, alternative; then local Auer zero, nominal, alternative",
            "retry": "forbidden",
            "continue_after": ["proof-complete UNKNOWN", "frozen wall/cpu/memory/arithmetic/output/resource stop"],
            "stop_after": ["input/source/binding defect", "proof replay defect", "common checker defect", "runner integrity defect"],
            "never_continue_as": "baseline method limitation when support or checker is invalid",
        },
        "run_order": "all three v6 producers in frozen order, then all three Auer producers in frozen order; no concurrent method workers",
        "resource_caps": {
            "phase_wall_seconds": 7200,
            "worker_wall_seconds": 60,
            "replay_audit_wall_seconds": 60,
            "worker_cpu_seconds": 60,
            "replay_audit_cpu_seconds": 60,
            "memory_bytes_per_worker_or_replay_audit": 1073741824,
            "processes_per_bounded_child": 1,
            "stdout_bytes": 8388608,
            "stderr_bytes": 1048576,
        },
        "accounting": {
            "g2_native_attempts": "24/24 consumed; no producer launched by G2",
            "g4_w2_v6_native_calls_before_phase": 0,
            "g4_w2_auer_native_calls_before_phase": 0,
            "g4_confirmation_rows_per_method": "0/24",
            "r5_800": "800/800 NOT_RUN",
            "auer_1944": "NOT_RUN",
        },
        "interpretation_policy": {
            "no universal method superiority": True,
            "no generic novelty claim from implementation difference": True,
            "quick UNKNOWN is not equal-coverage speed superiority": True,
            "offline 60-second cap is not a robot deadline": True,
            "Auer unsupported/invalid/resource result is not evidence of v6 mathematical superiority": True,
            "no conditional fresh confirmation in this phase": True,
        },
    }
    protocol_path = PLAN / "protocol_v2.json"
    write(ROOT / protocol_path, protocol)

    # Reuse G2's exact frozen input records, adding a method-independent digest
    # that binds the task protocol and its primary target, not only solver fields.
    original_auer = read(PLAN / "auer_input_manifest.json")
    auer_cases = []
    v6_bindings = []
    for ordinal, (v6_id, auer_id, peer_id, auer_action, voltage) in enumerate(PAIRS, 1):
        old = next(item for item in original_auer["cases"] if item["comparison_id"] == auer_id)
        payload = old["payload"]
        physical = physical_input(task, voltage)
        physical_sha = canonical_sha(physical)
        payload_sha = canonical_sha(payload)
        auer_cases.append({
            "ordinal": ordinal,
            "query_id": auer_id,
            "comparison_id": auer_id,
            "peer_action_id": peer_id,
            "action_id": auer_action,
            "input_sha256": physical_sha,
            "physical_input_sha256": physical_sha,
            "payload_sha256": payload_sha,
            "payload": payload,
            "canonical_physical_input": physical,
        })
        g2_binding_path = Path("research/autonomous_w2/g2/bindings_centered_v6") / f"attempt_{ordinal:02d}.json"
        old_binding = read(g2_binding_path)
        binding_rel = PLAN / "v6_bindings" / f"{ordinal:02d}.json"
        binding = dict(old_binding)
        g4_source_files = {
            "validation/autonomous_w2/g4/v6_snapshot_v2/producer_centered_v6.py": sha(ROOT / "validation/autonomous_w2/g4/v6_snapshot_v2/producer_centered_v6.py"),
            "validation/autonomous_w2/g4/v6_snapshot_v2/producer_v4.py": sha(ROOT / "validation/autonomous_w2/g4/v6_snapshot_v2/producer_v4.py"),
            "validation/autonomous_w2/g4/v6_snapshot_v2/rational_interval_v3.py": sha(ROOT / "validation/autonomous_w2/g4/v6_snapshot_v2/rational_interval_v3.py"),
            "validation/autonomous_w2/g4/v6_snapshot_v2/checker_centered_v6.py": sha(ROOT / "validation/autonomous_w2/g4/v6_snapshot_v2/checker_centered_v6.py"),
            "validation/autonomous_w2/g4/v6_snapshot_v2/__init__.py": sha(ROOT / "validation/autonomous_w2/g4/v6_snapshot_v2/__init__.py"),
            "research/autonomous_w2/g4/matched_v6_task_development_v2/g2_task_protocol_v1.json": sha(ROOT / g2_protocol_path),
            "research/autonomous_w2/g4/matched_v6_task_development_v2/g2_profile_centered_v6.json": sha(ROOT / g2_profile_path),
            "research/autonomous_w2/g4/matched_v6_task_development_v2/g2_release_v6.json": sha(ROOT / g2_release_path),
            "research/autonomous_w2/g4/matched_v6_task_development_v2/benchmark_v2.json": benchmark_sha,
            "research/autonomous_w2/g4/matched_v6_task_development_v2/native_source_snapshot_v2.json": "PENDING_SNAPSHOT_DIGEST",
            "validation/autonomous_w2/g2/producer_centered_v6.py": sha(ROOT / "validation/autonomous_w2/g2/producer_centered_v6.py"),
            "validation/autonomous_w2/g2/producer_v4.py": sha(ROOT / "validation/autonomous_w2/g2/producer_v4.py"),
            "validation/autonomous_w2/g2/rational_interval_v3.py": sha(ROOT / "validation/autonomous_w2/g2/rational_interval_v3.py"),
            "validation/autonomous_w2/g2/checker_centered_v6.py": sha(ROOT / "validation/autonomous_w2/g2/checker_centered_v6.py"),
            "research/autonomous_w2/g2/task_protocol_v1.json": TASK_SHA,
            "validation/autonomous_w2/g2/profile_centered_v6.json": sha(g2_profile_original),
            "coordination/autonomous_w2/g2/releases/RELEASE_v6.json": RELEASE_SHA,
        }
        # The wrapper consumes one exact, historical G2 native binding.  Pin
        # that file in the wrapper closure as well as through the explicit
        # core_binding_sha256 field, so the worker's path/hash check is total.
        g4_source_files[g2_binding_path.as_posix()] = sha(ROOT / g2_binding_path)
        saved_row_path = (
            Path("results/validation/autonomous_w2/g2/development_centered_v6") /
            f"attempt_{ordinal:02d}_{peer_id}" / "row.json"
        )
        saved_row_sha = sha(ROOT / saved_row_path)
        g4_source_files[saved_row_path.as_posix()] = saved_row_sha
        binding.update({
            "binding_path": binding_rel.as_posix(),
            "protocol_path": g2_protocol_path.as_posix(),
            "profile_path": g2_profile_path.as_posix(),
            "source_files": g4_source_files,
            "result_root": (Path("results/validation/autonomous_w2/g4/matched_v6_task_development_v2/v6") / f"{ordinal:02d}_{v6_id}").as_posix(),
            "comparison_id": v6_id,
            "external_input_digest": physical_sha,
            "physical_input_sha256": physical_sha,
            "core_binding_path": g2_binding_path.as_posix(),
            "core_binding_sha256": sha(ROOT / g2_binding_path),
            "peer_release_path": RELEASE.as_posix(),
            "peer_release_sha256": RELEASE_SHA,
            "peer_action_id": peer_id,
            "native_input_sha256": sha(ROOT / g2_binding_path),
            "native_task_protocol_sha256": TASK_SHA,
            "w2_wrapper_snapshot": "validation/autonomous_w2/g4/v6_snapshot_v2",
            "peer_saved_row_path": saved_row_path.as_posix(),
            "peer_saved_row_sha256": saved_row_sha,
        })
        write(ROOT / binding_rel, binding)
        v6_bindings.append({
            "ordinal": ordinal,
            "external_id": v6_id,
            "path": binding_rel.as_posix(),
            "sha256": sha(ROOT / binding_rel),
            "action_id": peer_id,
            "peer_action_id": peer_id,
            "physical_input_sha256": physical_sha,
            "native_input_sha256": sha(ROOT / g2_binding_path),
            "wrapper_binding_sha256": sha(ROOT / binding_rel),
            "peer_saved_row_path": saved_row_path.as_posix(),
            "peer_saved_row_sha256": saved_row_sha,
        })

    auer_manifest = {
        "schema": "ddwmr-g4-w2-auer-input-manifest-v2",
        "status": "FROZEN_DEVELOPMENT_ONLY_W2",
        "session": "DDWMR | LUNA-G4-AUER",
        "task_protocol_path": TASK.as_posix(),
        "task_protocol_sha256": TASK_SHA,
        "peer_release_path": RELEASE.as_posix(),
        "peer_release_sha256": RELEASE_SHA,
        "benchmark_path": benchmark_path.as_posix(),
        "benchmark_sha256": benchmark_sha,
        "parameter_label_order": LABELS,
        "input_digest_contract": "SHA256 canonical JSON of canonical_physical_input, which includes G2 task protocol digest, full nine-state box, independent twelve-label image, fixed constants/maps, clip law, voltage, 2s horizon, static obstacle, progress metric and 7/20 threshold; distinct payload hash binds legacy-native solver fields.",
        "cases": auer_cases,
    }
    auer_manifest_path = PLAN / "auer_input_manifest_v2.json"
    native_cases = []
    for item in auer_cases:
        payload = item["payload"]
        case = {
            "schema": "ddwmr-g4-auer-matched-query-input-v3-r9",
            "query_id": item["query_id"],
            "input_sha256": item["physical_input_sha256"],
            "physical_input_sha256": item["physical_input_sha256"],
            "canonical_physical_input_sha256": item["physical_input_sha256"],
            "candidate_manifest_v2_input_sha256": item["payload_sha256"],
            "benchmark_path": benchmark_path.as_posix(),
            "benchmark_sha256": benchmark_sha,
            "state_order": payload["state_cell"]["coordinates"],
            "initial_state": payload["state_cell"]["box"],
            "fixed_labels": payload["parameter_cell"]["labels"],
            "held_voltage": payload["action"]["V"],
            "horizon": payload["horizon"]["T"],
            "scene": payload["scene"],
            "parameter_cell": payload["parameter_cell"],
        }
        case_rel = PLAN / "auer_native_inputs" / f"{item['ordinal']:02d}_{item['query_id']}.json"
        write(ROOT / case_rel, case)
        item["native_case_path"] = case_rel.as_posix()
        item["native_case_sha256"] = sha(ROOT / case_rel)
        native_cases.append({
            "ordinal": item["ordinal"], "comparison_id": item["comparison_id"],
            "path": item["native_case_path"], "file_sha256": item["native_case_sha256"],
            "semantic_physical_input_sha256": item["physical_input_sha256"],
            "native_payload_sha256": item["payload_sha256"],
        })
    for action in protocol["actions"]:
        v6_item = next(item for item in v6_bindings if item["external_id"] == action["external_id"])
        auer_item = next(item for item in auer_cases if item["comparison_id"] == action["auer_id"])
        action["v6_native_binding_input_sha256"] = v6_item["native_input_sha256"]
        action["v6_native_binding_sha256"] = v6_item["sha256"]
        action["auer_native_input_path"] = auer_item["native_case_path"]
        action["auer_native_input_file_sha256"] = auer_item["native_case_sha256"]
        action["auer_input_digest"] = auer_item["input_sha256"]
    write(ROOT / protocol_path, protocol)
    auer_manifest["cases"] = auer_cases
    write(ROOT / auer_manifest_path, auer_manifest)

    # Adapt the prior R9 caps without increasing them: native exact-rational
    # producer+replay+common-check operation ceiling remains 2,000,000.
    old_auer_profile = read(PLAN / "auer_profile.json")
    auer_profile = dict(old_auer_profile)
    auer_profile.update({
        "profile_id": "AUER_G4_W2_MATCHED_V6_DEVELOPMENT_V2_60S",
        "protocol_candidate": protocol_path.as_posix(),
        "scope": "one canonical v6 W2 task input per frozen action; local Auer/Picard reconstruction, not VALENCIA binary",
        "status": "FROZEN_DEVELOPMENT_ONLY_W2",
        "wall_time_seconds_per_ivp": 60,
        "max_serialized_proof_bytes": 536_870_912,
        "max_serialized_common_record_bytes": 8_388_608,
        "max_serialized_progress_bytes": 1_048_576,
        "external_guard_enforcement": "Windows Job Object worker+replay bounds pinned by W2 G4 runner; child count one, job memory 1GiB, wall and CPU 60s, output caps frozen in protocol",
        "memory_enforcement": {
            "enforcement_probe_required_before_query": True,
            "limit_bytes": 1_073_741_824,
            "mechanism": "Windows Job Object; suspended process assignment before resume; kill-on-job-close",
            "platform": "Windows",
            "scope": "one method worker containing native producer, independent native replay, and common replay; one 60s/1GiB envelope",
            "timeout_mechanism": "parent monotonic deadline; terminate complete Job Object",
            "worker_child_processes": 0,
        },
        "max_rational_operations_per_ivp_combined_producer_replay_and_common_check": 2_000_000,
        "operation_ceiling_is_cross_method_equal_resource_cap": False,
        "source_snapshot_manifest_path": "research/autonomous_w2/g4/matched_v6_task_development_v2/native_source_snapshot_v2.json",
        "input_binding": "one explicit external comparison ID bijected to one peer G2 action and canonical physical-input digest; exact legacy native payload separately hashed",
        "matched_worker": {
            "module": "validation.autonomous_w2.g4.auer_w2_worker_v2",
            "native_solver": "validation.autonomous_w2.g4.auer_snapshot_v2.solver_r9_w2",
            "native_replay": "validation.autonomous_w2.g4.auer_snapshot_v2.replay_r9_w2",
            "common_adapter": "validation.autonomous_w2.g4.auer_w2_adapter_v2",
            "invocation_scope": "one explicit frozen comparison ID per process; no batch enumeration",
            "input_binding": "three-case G4 native input manifest; physical digest and native case file hash both checked",
            "status": "FROZEN_W2_DEVELOPMENT_ONLY",
            "accepted_residual_picard_formulas_changed": False,
            "native_replay_math_changed": False,
        },
    })
    auer_profile_path = PLAN / "auer_profile_v2.json"
    auer_profile["source_closure_manifest_path"] = "results/validation/autonomous_w2/g4/matched_v6_task_development_v2/source_closure_v2.json"
    write(ROOT / auer_profile_path, auer_profile)
    common_profile = read(PLAN / "common_profile.json")
    common_profile.pop("r3_segment_budget_contract", None)
    common_profile["radius_contract"] = {
        "centered_residual_v6": {
            "source": "method-native replayed v6 center/radius full-slab enclosure, then one G4 tube conversion",
            "additional_common_radius_expansion": False,
        },
        "local_auer": {
            "source": "method-native replayed Auer full-slab total hull",
            "additional_common_radius_expansion": False,
        },
    }
    common_profile.update({
        "profile_id": "G4_COMMON_TUBE_W2_MATCHED_V6_60S_V2",
        "protocol_candidate": protocol_path.as_posix(),
        "status": "FROZEN_DEVELOPMENT_ONLY_W2",
        "scope": "one of the same three full-hold action inputs after method-native proof replay",
        "common_progress_rule": "same closed-slab interval integral sum(duration * u * cos(theta)) intersected with same endpoint displacement bound for both methods",
        "max_rational_operations_per_common_stage": 2_000_000,
        "max_common_record_bytes": 8_388_608,
        "max_progress_record_bytes": 1_048_576,
        "max_worker_result_bytes": 1_048_576,
        "max_stdout_bytes": 8_388_608,
        "max_stderr_bytes": 1_048_576,
        "sqrt_bisections": 128,
        "matched_workers": {
            "v6_module": "validation.autonomous_w2.g4.v6_w2_worker_v2",
            "v6_replay_module": "native audit and common replay inside validation.autonomous_w2.g4.v6_w2_worker_v2",
            "auer_module": "validation.autonomous_w2.g4.auer_w2_worker_v2",
            "auer_replay_module": "native audit and common replay inside validation.autonomous_w2.g4.auer_w2_worker_v2",
            "invocation_scope": "one comparison ID per bounded child; no batch mode",
            "common_unknown_preserves_native_proof": True,
            "predicate_unknown_does_not_trigger_native_refinement": True,
        },
    })
    common_profile_path = PLAN / "common_profile_v2.json"
    write(ROOT / common_profile_path, common_profile)

    # W2 copies retain the scientific source bytes. Only these path differences
    # are allowed: G2 ROOT anchor moves one directory deeper; Auer imports point
    # to the G4-owned versioned snapshot. Exact source/copy diff is frozen below.
    source_map = {
        "g2/producer_centered_v6.py": "validation/autonomous_w2/g4/v6_snapshot_v2/producer_centered_v6.py",
        "g2/producer_v4.py": "validation/autonomous_w2/g4/v6_snapshot_v2/producer_v4.py",
        "g2/rational_interval_v3.py": "validation/autonomous_w2/g4/v6_snapshot_v2/rational_interval_v3.py",
        "g2/checker_centered_v6.py": "validation/autonomous_w2/g4/v6_snapshot_v2/checker_centered_v6.py",
        "auer/solver_r9_w2.py": "validation/autonomous_w2/g4/auer_snapshot_v2/solver_r9_w2.py",
        "auer/replay_r9_w2.py": "validation/autonomous_w2/g4/auer_snapshot_v2/replay_r9_w2.py",
        "auer/rhs.py": "validation/autonomous_w2/g4/auer_snapshot_v2/rhs.py",
        "auer/piecewise.py": "validation/autonomous_w2/g4/auer_snapshot_v2/piecewise.py",
    }
    snapshot = {"schema": "ddwmr-g4-w2-native-source-snapshot-map-v2", "copies": []}
    origins = {
        "g2/producer_centered_v6.py": "validation/autonomous_w2/g2/producer_centered_v6.py",
        "g2/producer_v4.py": "validation/autonomous_w2/g2/producer_v4.py",
        "g2/rational_interval_v3.py": "validation/autonomous_w2/g2/rational_interval_v3.py",
        "g2/checker_centered_v6.py": "validation/autonomous_w2/g2/checker_centered_v6.py",
        "auer/solver_r9_w2.py": "validation/baselines/auer2013/residual_ivp_g4_matched_v3_r9.py",
        "auer/replay_r9_w2.py": "validation/baselines/auer2013/replay_ivp.py",
        "auer/rhs.py": "validation/baselines/auer2013/rhs.py",
        "auer/piecewise.py": "validation/baselines/auer2013/piecewise.py",
    }
    for key, destination in source_map.items():
        origin = origins[key]
        snapshot["copies"].append({
            "origin_path": origin,
            "origin_sha256": sha(ROOT / origin),
            "snapshot_path": destination,
            "snapshot_sha256": sha(ROOT / destination),
            "adaptations": (
                ["ROOT anchor only: parents[3] to parents[4]"] if key.startswith("g2/") and key != "g2/rational_interval_v3.py"
                else ["two import paths rewritten to G4-owned snapshot modules"] if key == "auer/solver_r9_w2.py"
                else ["none; byte-identical snapshot"]
            ),
        })
    snapshot_path = PLAN / "native_source_snapshot_v2.json"
    write(ROOT / snapshot_path, snapshot)
    snapshot_sha = sha(ROOT / snapshot_path)

    # Construct one explicit proof-input binding per local Auer action.  These
    # bindings are G4-owned and do not mutate the historical R9 inputs.
    method_contract_path = Path("docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md")
    backend_manifest_path = Path("validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v2.json")
    solver_path = Path("validation/autonomous_w2/g4/auer_snapshot_v2/solver_r9_w2.py")
    checker_path = Path("validation/autonomous_w2/g4/auer_snapshot_v2/replay_r9_w2.py")
    method_sha = sha(ROOT / method_contract_path)
    backend_sha = sha(ROOT / backend_manifest_path)
    solver_sha = sha(ROOT / solver_path)
    checker_sha = sha(ROOT / checker_path)
    auer_bindings = []
    for item in auer_cases:
        native_binding = {
            "input_path": item["native_case_path"],
            "input_sha256": item["native_case_sha256"],
            "method_contract_path": method_contract_path.as_posix(),
            "method_contract_sha256": method_sha,
            "arithmetic_backend_manifest_path": backend_manifest_path.as_posix(),
            "arithmetic_backend_manifest_sha256": backend_sha,
            "resource_profile_path": auer_profile_path.as_posix(),
            "resource_profile_sha256": sha(ROOT / auer_profile_path),
            "source_snapshot_manifest_sha256": snapshot_sha,
            "solver_source_sha256": solver_sha,
            "checker_source_sha256": checker_sha,
            "arithmetic_dependency": "shared validation.g2 exact Fraction/Interval/Budget and Taylor sin/cos; separately disclosed and not an independent arithmetic library",
        }
        auer_bindings.append({
            "ordinal": item["ordinal"],
            "comparison_id": item["comparison_id"],
            "peer_action_id": item["peer_action_id"],
            "physical_input_sha256": item["physical_input_sha256"],
            "native_case_path": item["native_case_path"],
            "native_case_sha256": item["native_case_sha256"],
            "native_binding": native_binding,
        })
    auer_bindings_path = PLAN / "auer_bindings_v2.json"
    write(ROOT / auer_bindings_path, {
        "schema": "ddwmr-g4-w2-auer-native-bindings-v2",
        "session": "DDWMR | LUNA-G4-AUER",
        "status": "FROZEN_DEVELOPMENT_ONLY_W2",
        "native_source_snapshot_path": snapshot_path.as_posix(),
        "native_source_snapshot_sha256": snapshot_sha,
        "bindings": auer_bindings,
    })

    # Bind the finalized native-source inventory into each v6 adapter input.
    snapshot_sha = sha(ROOT / snapshot_path)
    for item in v6_bindings:
        bpath = ROOT / item["path"]
        binding = read(item["path"])
        binding["source_files"]["research/autonomous_w2/g4/matched_v6_task_development_v2/native_source_snapshot_v2.json"] = snapshot_sha
        binding["source_snapshot_manifest_sha256"] = snapshot_sha
        write(bpath, binding)
        item["sha256"] = sha(bpath)
    for action in protocol["actions"]:
        item = next(value for value in v6_bindings if value["external_id"] == action["external_id"])
        action["native_binding_sha256"] = item["sha256"]
        auer_item = next(value for value in auer_bindings if value["comparison_id"] == action["auer_id"])
        auer_binding_bytes = json.dumps(
            auer_item["native_binding"], sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        ).encode("utf-8") + b"\n"
        action["auer_native_binding_sha256"] = hashlib.sha256(auer_binding_bytes).hexdigest()
    write(ROOT / protocol_path, protocol)

    return {
        "protocol_path": protocol_path.as_posix(),
        "protocol_sha256": sha(ROOT / protocol_path),
        "benchmark_path": benchmark_path.as_posix(),
        "benchmark_sha256": benchmark_sha,
        "auer_manifest_path": auer_manifest_path.as_posix(),
        "auer_manifest_sha256": sha(ROOT / auer_manifest_path),
        "auer_profile_path": auer_profile_path.as_posix(),
        "auer_profile_sha256": sha(ROOT / auer_profile_path),
        "common_profile_path": common_profile_path.as_posix(),
        "common_profile_sha256": sha(ROOT / common_profile_path),
        "v6_bindings": v6_bindings,
        "native_source_snapshot_path": snapshot_path.as_posix(),
        "native_source_snapshot_sha256": snapshot_sha,
        "auer_bindings_path": auer_bindings_path.as_posix(),
        "auer_bindings_sha256": sha(ROOT / auer_bindings_path),
        "auer_binding_count": len(auer_bindings),
        "auer_native_cases": native_cases,
        "auer_manifest_input_sha256": [item["input_sha256"] for item in auer_cases],
    }


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, indent=2))
