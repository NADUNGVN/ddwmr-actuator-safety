"""Isolated worker for one frozen R4 IVP, independent replay and predicate check."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

from validation.baselines.auer2013.replay_ivp import canonical_sha256, replay_native_proof, sha256_file
from validation.baselines.auer2013.residual_ivp import solve_analytic_fixture, solve_ddwmr_case
from validation.g2.hashing import semantic_json_sha256
from validation.g2.rational import Budget, Interval, InvalidInput, ResourceLimit, parse_q, qobj


PROJECT = Path.cwd().resolve()
SNAPSHOT = PROJECT.parent
PROFILE_REL = Path("validation/baselines/auer2013/small_case_resource_profile_v2.json")
METHOD_REL = Path("docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md")
BACKEND_REL = Path("validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v2.json")
FIXTURE_REL = Path("validation/baselines/auer2013/analytic_branch_crossing_fixture_v1.json")
DDWMR_INPUT_REL = Path("validation/baselines/auer2013/auer_r4_ddwmr_single_case_input_v1.json")


def _strict_json(path: Path) -> Any:
    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise InvalidInput(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)


def _write_json(path: Path, value: Any, maximum_bytes: int | None = None) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    if maximum_bytes is not None and len(raw) > maximum_bytes:
        raise ResourceLimit("SERIALIZED_PROOF_SIZE_LIMIT", f"proof record has {len(raw)} bytes; cap is {maximum_bytes}")
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def _binding(
    *, input_rel: Path, profile: dict[str, Any], snapshot_manifest_sha256: str,
) -> dict[str, Any]:
    return {
        "input_path": input_rel.as_posix(),
        "input_sha256": sha256_file(PROJECT / input_rel),
        "method_contract_path": METHOD_REL.as_posix(),
        "method_contract_sha256": sha256_file(PROJECT / METHOD_REL),
        "arithmetic_backend_manifest_path": BACKEND_REL.as_posix(),
        "arithmetic_backend_manifest_sha256": sha256_file(PROJECT / BACKEND_REL),
        "resource_profile_path": PROFILE_REL.as_posix(),
        "resource_profile_sha256": sha256_file(PROJECT / PROFILE_REL),
        "source_snapshot_manifest_sha256": snapshot_manifest_sha256,
        "solver_source_sha256": sha256_file(PROJECT / "validation/baselines/auer2013/residual_ivp.py"),
        "checker_source_sha256": sha256_file(PROJECT / "validation/baselines/auer2013/replay_ivp.py"),
        "arithmetic_dependency": "shared validation.g2 exact Fraction/Interval/Budget and Taylor sin/cos; separately disclosed and not an independent arithmetic library",
    }


def _snapshot_check(expected_hash: str) -> None:
    manifest = SNAPSHOT / "snapshot_manifest.json"
    sidecar = SNAPSHOT / "snapshot_manifest.sha256"
    actual = sha256_file(manifest)
    if actual != expected_hash:
        raise InvalidInput("runtime snapshot manifest hash differs from the frozen launch binding")
    listed = sidecar.read_text(encoding="ascii").split()[0]
    if listed != actual:
        raise InvalidInput("runtime snapshot manifest sidecar mismatch")


def _verify_backend_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("backend_id") != "DDWMR_EXACT_RATIONAL_TAYLOR_INTERVAL_V1":
        raise InvalidInput("unexpected exact-rational backend id")
    for item in manifest.get("proof_critical_source_files", []):
        path = PROJECT / item["path"]
        if sha256_file(path) != item["sha256"]:
            raise InvalidInput(f"arithmetic source hash mismatch: {item['path']}")


def _envelope(proof: dict[str, Any]) -> dict[str, Any]:
    return {"proof": proof, "proof_sha256": canonical_sha256(proof)}


def _rhs_work_record(
    work: dict[str, int], ledger: dict[str, int],
) -> dict[str, Any]:
    return {
        "producer": work["producer"],
        "native_replay": work["native_replay"],
        "tamper_replay": work["tamper_replay"],
        "common_predicate": work["common_predicate"],
        "combined": ledger["count"],
        "cap": ledger["limit"],
        "within_cap": ledger["count"] <= ledger["limit"],
    }


def _rational_work_record(
    work: dict[str, int], profile: dict[str, Any],
) -> dict[str, Any]:
    combined = sum(work.values())
    cap = int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"])
    return {**work, "combined": combined, "cap": cap, "within_cap": combined <= cap}


def _tamper_suite(
    envelope: dict[str, Any], *, case_kind: str, case: dict[str, Any], benchmark: dict[str, Any] | None,
    profile: dict[str, Any], fixture: dict[str, Any] | None, expected_binding: dict[str, Any],
    remaining_operations: int, rhs_eval_counter: dict[str, int],
) -> tuple[list[dict[str, Any]], int, int]:
    trials: list[tuple[str, str]] = []
    if case_kind == "analytic":
        trials = [
            ("fabricated_narrow_hull", "body"),
            ("altered_residual_iterate", "body"),
            ("changed_switch_interval", "body"),
            ("altered_endpoint", "body"),
            ("changed_source_binding", "body"),
            ("changed_profile_binding", "body"),
            ("changed_proof_digest", "digest"),
        ]
    else:
        trials = [
            ("fabricated_narrow_hull", "body"),
            ("altered_residual_iterate", "body"),
            ("altered_endpoint", "body"),
            ("changed_action", "body"),
            ("changed_source_binding", "body"),
            ("changed_profile_binding", "body"),
            ("changed_proof_digest", "digest"),
        ]
    results = []
    spent = 0
    maximum_bits = int(profile["max_rational_bits"])
    for name, mutation_kind in trials:
        altered = copy.deepcopy(envelope)
        body = altered["proof"]
        if name == "changed_proof_digest":
            altered["proof_sha256"] = "0" * 64
        else:
            step = body["step_records"][0]
            if name == "fabricated_narrow_hull":
                key = "full_time_total_hull" if case_kind == "analytic" else "full_time_total_hull_augmented"
                step[key][0] = [{"num": "0", "den": "1"}, {"num": "0", "den": "1"}]
            elif name == "altered_residual_iterate":
                step["residual_iterations"][0]["new_residual_derivative"][1][0]["num"] = "999"
            elif name == "changed_switch_interval":
                step["residual_iterations"][0]["switch_time_interval_from_initial_box"][0]["num"] = "999"
            elif name == "altered_endpoint":
                body["global_endpoint"][0][0]["num"] = "999"
            elif name == "changed_action":
                body["query_action_binding"]["held_voltage"][0]["num"] = "-2"
            elif name == "changed_source_binding":
                body["binding"]["source_snapshot_manifest_sha256"] = "0" * 64
            elif name == "changed_profile_binding":
                body["binding"]["resource_profile_sha256"] = "0" * 64
            if mutation_kind == "body":
                altered["proof_sha256"] = canonical_sha256(body)
        remaining = remaining_operations - spent
        if remaining <= 0:
            results.append({
                "tamper": name,
                "rejected": False,
                "checker_result": {
                    "replayed": False,
                    "reason": "resource_limit",
                    "termination": {
                        "kind": "RATIONAL_OPERATION_LIMIT",
                        "detail": "tamper replay reached the combined frozen operation cap",
                    },
                    "work": {"rational_operations": 0, "rhs_jacobian_replay_evaluations": 0},
                },
            })
            break
        budget = Budget(max_bits=maximum_bits, max_operations=remaining, wall_seconds=Fraction(int(profile["wall_time_seconds_per_ivp"])))
        replay = replay_native_proof(
            altered, case=case, benchmark=benchmark, profile=profile, fixture=fixture,
            expected_binding=expected_binding, budget=budget, rhs_eval_counter=rhs_eval_counter,
        )
        spent += budget.operations
        is_resource_limit = replay.get("reason") == "resource_limit"
        results.append({
            "tamper": name,
            "rejected": not replay.get("replayed", False) and not is_resource_limit,
            "checker_result": replay,
        })
        if is_resource_limit:
            break
    return results, spent, len(trials)


def _composition_valid(composition: dict[str, Any], expected: dict[str, Any]) -> bool:
    return composition == expected


def _common_check(
    envelope: dict[str, Any], proof_file_sha256: str, case: dict[str, Any], benchmark: dict[str, Any],
    profile: dict[str, Any], remaining_operations: int,
) -> tuple[dict[str, Any], int, dict[str, Any]]:
    from validation.g4.common_tube import TubeSegment, check_tube_segments

    if remaining_operations <= 0:
        exc = ResourceLimit("RATIONAL_OPERATION_LIMIT", "no rational operations remain for the common predicate check")
        exc.work = {"rational_operations": 0, "rational_operation_attempts": 0, "max_observed_rational_bits": 0}
        raise exc
    budget = Budget(
        max_bits=int(profile["max_rational_bits"]), max_operations=remaining_operations,
        wall_seconds=Fraction(int(profile["wall_time_seconds_per_ivp"])),
    )
    try:
        labels = tuple((item["name"], Interval.from_json(case["fixed_labels"][item["name"]], budget)) for item in benchmark["parameter_labels"])
        segments = []
        for step in envelope["proof"]["step_records"]:
            t_start = parse_q(step["time_closed"]["start"], budget)
            t_end = parse_q(step["time_closed"]["end"], budget)
            physical_hull = tuple(Interval.from_json(row, budget) for row in step["full_time_total_hull_augmented"][:9])
            endpoint_start = tuple(Interval.from_json(row, budget) for row in step["endpoint_start_augmented"][:9])
            endpoint_end = tuple(Interval.from_json(row, budget) for row in step["endpoint_end_augmented"][:9])
            segments.append(TubeSegment.from_total_hull(
                segment_id=f"AUER:{case['query_id']}:{len(segments)}",
                t_start=t_start, t_end=t_end, state_hull=physical_hull, labels=labels,
                endpoint_start=endpoint_start, endpoint_end=endpoint_end,
                radius_expansion_count=0, radius_expansion_mode="NATIVE_TOTAL_HULL",
                provenance={
                    "native_method_id": envelope["proof"]["method_id"],
                    "native_proof_sha256": envelope["proof_sha256"],
                    "native_proof_file_sha256": proof_file_sha256,
                    "source_snapshot_manifest_sha256": envelope["proof"]["binding"]["source_snapshot_manifest_sha256"],
                },
            ))
        initial_state = tuple(Interval.from_json(row, budget) for row in case["initial_state"])
        horizon = parse_q(case["horizon"], budget)
        scene = {
            "id": case["scene"]["id"],
            "p_o": case["scene"]["p_o"],
            "R_s": case["scene"]["R_s"],
        }
        common_record = check_tube_segments(
            tuple(segments), benchmark, scene, horizon, budget,
            initial_state=initial_state,
            sqrt_bisections=int(profile["transcendental_profile"]["square_root_bisections"]),
        )
    except ResourceLimit as exc:
        exc.work = {
            "rational_operations": budget.operations,
            "rational_operation_attempts": budget.operation_attempts,
            "max_observed_rational_bits": budget.max_seen_bits,
        }
        exc.rational_budget_failure_context = budget.failure_context
        raise
    segments_json = [item.to_json() for item in segments]
    expected_composition = {
        "schema": "ddwmr-g4-auer-r4-proof-to-common-composition-v1",
        "query_id": case["query_id"],
        "candidate_manifest_v2_input_sha256": case["candidate_manifest_v2_input_sha256"],
        "held_voltage": case["held_voltage"],
        "native_proof_sha256": envelope["proof_sha256"],
        "native_proof_file_sha256": proof_file_sha256,
        "source_snapshot_manifest_sha256": envelope["proof"]["binding"]["source_snapshot_manifest_sha256"],
        "radius_expansion_mode": "NATIVE_TOTAL_HULL",
        "radius_expansion_count": 0,
        "segments": segments_json,
        "segments_sha256": semantic_json_sha256(segments_json),
        "common_check_sha256": canonical_sha256(common_record),
        "common_check_predicate_status": common_record["predicate_status"],
        "common_check_certificate_emitted": False,
        "common_check_ode_tube_proof_replayed": False,
    }
    return common_record, budget.operations, expected_composition


def _composition_tamper_trials(composition: dict[str, Any]) -> list[dict[str, Any]]:
    trials = []
    changed = copy.deepcopy(composition)
    changed["radius_expansion_mode"] = "CENTER_PLUS_RESIDUAL_ONCE"
    trials.append({"tamper": "changed_radius_mode", "rejected": not _composition_valid(changed, composition)})
    changed = copy.deepcopy(composition)
    changed["segments"][0]["state_hull"][0][0]["num"] = "999"
    trials.append({"tamper": "changed_segment_hull", "rejected": not _composition_valid(changed, composition)})
    changed = copy.deepcopy(composition)
    changed["native_proof_sha256"] = "0" * 64
    trials.append({"tamper": "changed_native_proof_digest", "rejected": not _composition_valid(changed, composition)})
    return trials


def _run(args: argparse.Namespace) -> int:
    started = time.monotonic()
    output_path = Path(args.proof_output).resolve()
    evidence_path = Path(args.evidence_output).resolve()
    profile = _strict_json(PROJECT / PROFILE_REL)
    method_sha = sha256_file(PROJECT / METHOD_REL)
    backend_path = PROJECT / BACKEND_REL
    backend = _strict_json(backend_path)
    backend_sha = sha256_file(backend_path)
    profile_sha = sha256_file(PROJECT / PROFILE_REL)
    if profile.get("memory_enforcement", {}).get("limit_bytes") != int(profile["memory_limit_mib_per_ivp"]) * 1024 * 1024:
        raise InvalidInput("profile process-memory byte cap is inconsistent with MiB value")
    _snapshot_check(args.snapshot_manifest_sha256)
    _verify_backend_manifest(backend)
    v1_profile_sha = sha256_file(PROJECT / "validation/baselines/auer2013/small_case_resource_profile_v1.json")
    if v1_profile_sha != profile["predecessor_profile_sha256"]:
        raise InvalidInput("frozen v1 profile was changed")

    if args.case == "analytic":
        input_rel = FIXTURE_REL
        fixture = _strict_json(PROJECT / input_rel)
        case = fixture
        benchmark = None
    else:
        input_rel = DDWMR_INPUT_REL
        case = _strict_json(PROJECT / input_rel)
        fixture = None
        benchmark_path = PROJECT / case["benchmark_path"]
        if sha256_file(benchmark_path) != case["benchmark_sha256"]:
            raise InvalidInput("selected benchmark bytes changed")
        benchmark = _strict_json(benchmark_path)
    binding = _binding(input_rel=input_rel, profile=profile, snapshot_manifest_sha256=args.snapshot_manifest_sha256)
    rhs_work = {"producer": 0, "native_replay": 0, "tamper_replay": 0, "common_predicate": 0}
    operation_work = {"producer": 0, "native_replay": 0, "tamper_replay": 0, "common_predicate": 0}
    rhs_ledger = {
        "count": 0,
        "limit": int(profile["max_rhs_jacobian_evaluations_per_ivp"]),
    }
    budget = Budget(
        max_bits=int(profile["max_rational_bits"]),
        max_operations=int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"]),
        wall_seconds=Fraction(int(profile["wall_time_seconds_per_ivp"])),
    )
    evidence: dict[str, Any] = {
        "schema": "ddwmr-g4-auer-r4-worker-evidence-v1",
        "case": args.case,
        "status": "IN_PROGRESS",
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "matched_query_evaluations": 0,
    }
    try:
        if args.case == "analytic":
            proof = solve_analytic_fixture(
                case, input_path=input_rel, input_sha256=binding["input_sha256"],
                method_sha256=method_sha, backend_sha256=backend_sha, profile=profile,
                profile_sha256=profile_sha, snapshot_sha256=args.snapshot_manifest_sha256,
                solver_sha256=binding["solver_source_sha256"], checker_sha256=binding["checker_source_sha256"], budget=budget,
            )
        else:
            assert benchmark is not None
            proof = solve_ddwmr_case(
                case, benchmark, input_path=input_rel, input_sha256=binding["input_sha256"],
                method_sha256=method_sha, backend_sha256=backend_sha, profile=profile,
                profile_sha256=profile_sha, snapshot_sha256=args.snapshot_manifest_sha256,
                solver_sha256=binding["solver_source_sha256"], checker_sha256=binding["checker_source_sha256"], budget=budget,
            )
        proof.setdefault("work", {})["producer_rational_operations"] = budget.operations
        proof["work"]["producer_max_observed_rational_bits"] = budget.max_seen_bits
        operation_work["producer"] = budget.operations
        rhs_work["producer"] = int(proof.get("work", {}).get("rhs_jacobian_evaluations", 0))
        rhs_ledger["count"] = rhs_work["producer"]
        evidence["rhs_jacobian_work"] = _rhs_work_record(rhs_work, rhs_ledger)
        envelope = _envelope(proof)
        proof_file_sha256 = _write_json(output_path, envelope, int(profile["max_serialized_proof_bytes"]))
        evidence["native_proof_path"] = str(output_path)
        evidence["native_proof_file_sha256"] = proof_file_sha256
        evidence["native_proof_sha256"] = envelope["proof_sha256"]
        evidence["producer_work"] = {
            "operations": budget.operations,
            "operation_attempts": budget.operation_attempts,
            "max_rational_bits": budget.max_seen_bits,
            "configured_max_operations": budget.max_operations,
            "configured_max_bits": budget.max_bits,
        }
        if proof.get("status") != "PROOF_COMPLETE":
            evidence["status"] = proof.get("status", "UNKNOWN")
            evidence["termination"] = proof.get("termination", {})
            evidence["accepted_steps"] = len(proof.get("step_records", []))
            evidence["rejected_step_attempts"] = proof.get("rejected_step_attempts", [])
            evidence["rational_budget_failure_context"] = budget.failure_context
            evidence["rhs_jacobian_work"] = _rhs_work_record(rhs_work, rhs_ledger)
            evidence["rational_work"] = _rational_work_record(operation_work, profile)
            _write_json(evidence_path, evidence)
            return 10

        # Replay the exact bytes just written, not the producer's live object.
        frozen_envelope = _strict_json(output_path)
        remaining = int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"]) - budget.operations
        if remaining <= 0:
            raise ResourceLimit("RATIONAL_OPERATION_LIMIT", "producer exhausted the combined rational operation cap")
        checker_budget = Budget(
            max_bits=int(profile["max_rational_bits"]), max_operations=remaining,
            wall_seconds=Fraction(int(profile["wall_time_seconds_per_ivp"])),
        )
        replay = replay_native_proof(
            frozen_envelope, case=case, benchmark=benchmark, profile=profile, fixture=fixture,
            expected_binding=binding, budget=checker_budget, rhs_eval_counter=rhs_ledger,
        )
        rhs_work["native_replay"] += int(replay.get("rhs_jacobian_replay_evaluations", 0))
        operation_work["native_replay"] = checker_budget.operations
        evidence["rhs_jacobian_work"] = _rhs_work_record(rhs_work, rhs_ledger)
        evidence["rational_work"] = _rational_work_record(operation_work, profile)
        spent = budget.operations + checker_budget.operations
        evidence["native_proof_replay"] = replay
        if not replay.get("replayed"):
            if replay.get("reason") == "resource_limit":
                evidence["status"] = "RESOURCE_LIMIT"
                evidence["termination"] = replay.get("termination", {})
                evidence["rational_budget_failure_context"] = replay.get("rational_budget_failure_context")
                evidence["combined_rational_operations"] = spent
                evidence["combined_operation_cap"] = int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"])
                _write_json(evidence_path, evidence)
                return 10
            evidence["status"] = "IMPLEMENTATION_FAILURE"
            evidence["termination"] = {"reason": "INDEPENDENT_NATIVE_REPLAY_REJECTED_PRODUCER_RECORD"}
            evidence["combined_rational_operations"] = spent
            evidence["combined_operation_cap"] = int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"])
            _write_json(evidence_path, evidence)
            return 20
        tamper, tamper_work, tamper_count = _tamper_suite(
            frozen_envelope, case_kind=args.case, case=case, benchmark=benchmark,
            profile=profile, fixture=fixture, expected_binding=binding,
            remaining_operations=int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"]) - spent,
            rhs_eval_counter=rhs_ledger,
        )
        operation_work["tamper_replay"] = tamper_work
        rhs_work["tamper_replay"] += rhs_ledger["count"] - rhs_work["producer"] - rhs_work["native_replay"] - rhs_work["tamper_replay"]
        evidence["rhs_jacobian_work"] = _rhs_work_record(rhs_work, rhs_ledger)
        evidence["rational_work"] = _rational_work_record(operation_work, profile)
        spent += tamper_work
        evidence["tamper_rejections"] = tamper
        evidence["tamper_replay_work_operations"] = tamper_work
        resource_tamper = next((item for item in tamper if item["checker_result"].get("reason") == "resource_limit"), None)
        if resource_tamper is not None:
            evidence["status"] = "RESOURCE_LIMIT"
            evidence["termination"] = resource_tamper["checker_result"].get("termination", {})
            evidence["combined_rational_operations"] = spent
            evidence["combined_operation_cap"] = int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"])
            _write_json(evidence_path, evidence)
            return 10
        if len(tamper) != tamper_count or not all(item["rejected"] for item in tamper):
            evidence["status"] = "IMPLEMENTATION_FAILURE"
            evidence["termination"] = {"reason": "NATIVE_CHECKER_ACCEPTED_A_TAMPERED_PROOF"}
            evidence["combined_rational_operations"] = spent
            evidence["combined_operation_cap"] = int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"])
            _write_json(evidence_path, evidence)
            return 20

        if args.case == "ddwmr":
            assert benchmark is not None
            common_record, common_ops, composition = _common_check(
                frozen_envelope, proof_file_sha256, case, benchmark, profile,
                int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"]) - spent,
            )
            spent += common_ops
            composition_tamper = _composition_tamper_trials(composition)
            evidence["common_predicate_check"] = common_record
            evidence["typed_proof_to_common_composition"] = composition
            evidence["composition_tamper_rejections"] = composition_tamper
            operation_work["common_predicate"] = common_ops
            evidence["rational_work"] = _rational_work_record(operation_work, profile)
            if not all(item["rejected"] for item in composition_tamper):
                evidence["status"] = "IMPLEMENTATION_FAILURE"
                evidence["termination"] = {"reason": "COMPOSITION_CHECK_ACCEPTED_A_TAMPER"}
                _write_json(evidence_path, evidence)
                return 20
        evidence["combined_rational_operations"] = spent
        evidence["combined_operation_cap"] = int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"])
        if spent > evidence["combined_operation_cap"]:
            evidence["status"] = "RESOURCE_LIMIT"
            evidence["termination"] = {"reason": "COMBINED_RATIONAL_OPERATION_LIMIT"}
            _write_json(evidence_path, evidence)
            return 10
        evidence["elapsed_worker_seconds"] = time.monotonic() - started
        evidence["rhs_jacobian_work"] = _rhs_work_record(rhs_work, rhs_ledger)
        evidence["rational_work"] = _rational_work_record(operation_work, profile)
        evidence["status"] = "PROOF_COMPLETE_AND_REPLAYED"
        _write_json(evidence_path, evidence)
        return 0
    except ResourceLimit as exc:
        evidence["status"] = "RESOURCE_LIMIT"
        evidence["termination"] = {"kind": exc.kind, "detail": exc.detail}
        evidence["rational_budget_failure_context"] = budget.failure_context
        evidence["rhs_jacobian_work"] = _rhs_work_record(rhs_work, rhs_ledger)
        evidence["rational_work"] = _rational_work_record(operation_work, profile)
        evidence["combined_rational_operations"] = sum(operation_work.values())
        evidence["combined_operation_cap"] = int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"])
        if hasattr(exc, "work"):
            evidence["failed_stage_work"] = exc.work
            operation_work["common_predicate"] = int(exc.work.get("rational_operations", 0))
            evidence["rational_work"] = _rational_work_record(operation_work, profile)
            evidence["rational_budget_failure_context"] = getattr(exc, "rational_budget_failure_context", budget.failure_context)
        evidence["elapsed_worker_seconds"] = time.monotonic() - started
        _write_json(evidence_path, evidence)
        return 10
    except InvalidInput as exc:
        evidence["status"] = "INVALID_INPUT"
        evidence["termination"] = {"detail": str(exc)}
        evidence["elapsed_worker_seconds"] = time.monotonic() - started
        evidence["rhs_jacobian_work"] = _rhs_work_record(rhs_work, rhs_ledger)
        evidence["rational_work"] = _rational_work_record(operation_work, profile)
        evidence["combined_rational_operations"] = sum(operation_work.values())
        evidence["combined_operation_cap"] = int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"])
        _write_json(evidence_path, evidence)
        return 12
    except Exception as exc:  # preserve implementation faults as distinct outcomes
        evidence["status"] = "IMPLEMENTATION_FAILURE"
        evidence["termination"] = {"exception_type": type(exc).__name__, "detail": str(exc)}
        evidence["elapsed_worker_seconds"] = time.monotonic() - started
        evidence["rhs_jacobian_work"] = _rhs_work_record(rhs_work, rhs_ledger)
        evidence["rational_work"] = _rational_work_record(operation_work, profile)
        evidence["combined_rational_operations"] = sum(operation_work.values())
        evidence["combined_operation_cap"] = int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"])
        _write_json(evidence_path, evidence)
        return 20


def _probe(mebibytes: int) -> int:
    if mebibytes < 1:
        raise InvalidInput("memory probe allocation must be positive")
    requested_bytes = mebibytes * 1024 * 1024
    chunk_bytes = 1024 * 1024
    allocations: list[bytearray] = []
    allocated_bytes = 0
    while allocated_bytes < requested_bytes:
        try:
            block = bytearray(min(chunk_bytes, requested_bytes - allocated_bytes))
        except MemoryError:
            print(json.dumps({
                "memory_probe": "limit_reached",
                "requested_bytes": requested_bytes,
                "allocated_bytes": allocated_bytes,
                "allocation_error": "MemoryError",
            }), flush=True)
            return 23
        for offset in range(0, len(block), 4096):
            block[offset] = 0xA5
        allocations.append(block)
        allocated_bytes += len(block)
    print(json.dumps({"memory_probe": "completed", "allocated_bytes": allocated_bytes}), flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("analytic", "ddwmr"))
    parser.add_argument("--snapshot-manifest-sha256")
    parser.add_argument("--proof-output")
    parser.add_argument("--evidence-output")
    parser.add_argument("--memory-probe-mib", type=int)
    args = parser.parse_args()
    if args.memory_probe_mib is not None:
        return _probe(args.memory_probe_mib)
    if not args.case or not args.snapshot_manifest_sha256 or not args.proof_output or not args.evidence_output:
        parser.error("--case, --snapshot-manifest-sha256, --proof-output and --evidence-output are required")
    return _run(args)


if __name__ == "__main__":
    raise SystemExit(main())
