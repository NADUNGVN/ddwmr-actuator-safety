"""One-row Auer W2 development worker; top-level Job Object enforces caps."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

from validation.baselines.auer2013.replay_ivp import replay_native_proof
from validation.baselines.auer2013.residual_ivp_g4_matched_v3_r9 import solve_ddwmr_case
from validation.g2.interval import interval_cosine
from validation.g2.rational import Budget, Interval, InvalidInput, ResourceLimit, qobj, parse_q
from validation.g4.common_tube import replay_common_check_record
from validation.autonomous_w2.g4.auer_w2_adapter import canonical_sha256, make_segments
from validation.autonomous_w2.g4.matched_v6_common import (
    PLAN_REL, PROJECT, load_protocol_and_freeze, sha256_file, strict_json,
    score_segments, summarize_common, write_json,
)


def _canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def _envelope(proof: dict[str, Any]) -> dict[str, Any]:
    return {"proof": proof, "proof_sha256": canonical_sha256(proof)}


def _progress_intersection(segments, endpoint_start, endpoint_end, *, cosine_degree: int, budget: Budget) -> dict[str, Any]:
    total = Interval.point(Fraction(0), budget)
    for seg in segments:
        duration = seg.t_end - seg.t_start
        total = total + (seg.state_hull[3] * interval_cosine(seg.state_hull[2], cosine_degree)).scale(duration)
    endpoint = Interval(
        endpoint_end[0].lo - endpoint_start[0].hi,
        endpoint_end[0].hi - endpoint_start[0].lo,
        budget,
    )
    lo, hi = max(total.lo, endpoint.lo), min(total.hi, endpoint.hi)
    if lo > hi:
        raise InvalidInput("PROGRESS_ENDPOINT_AND_SLAB_BOUNDS_DISJOINT")
    return {
        "schema": "ddwmr-g4-w2-auer-progress-enclosure-v1",
        "formula": "intersection of endpoint p_x(T)-p_x(0) and full-slab integral of u*cos(theta)",
        "progress_enclosure_m": [qobj(lo), qobj(hi)],
        "slab_integral_enclosure_m": total.to_json(),
        "endpoint_difference_enclosure_m": endpoint.to_json(),
        "cosine_taylor_degree": cosine_degree,
    }


def _native_binding(case: dict[str, Any], freeze: dict[str, Any], benchmark: dict[str, Any], profile: dict[str, Any], closure: dict[str, Any]) -> dict[str, Any]:
    method_path = PROJECT / "docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md"
    backend_path = PROJECT / "validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v2.json"
    solver_path = PROJECT / "validation/baselines/auer2013/residual_ivp_g4_matched_v3_r9.py"
    checker_path = PROJECT / "validation/baselines/auer2013/replay_ivp.py"
    profile_path = PROJECT / PLAN_REL / "auer_profile.json"
    profile_sha = sha256_file(profile_path)
    bench_path = PROJECT / PLAN_REL / "benchmark_v1.json"
    benchmark_sha = sha256_file(bench_path)
    # Every field is passed into the immutable native proof and recomputed by
    # the independent replay below.
    return {
        "input_path": f"{(PLAN_REL / 'auer_input_manifest.json').as_posix()}#query={case['query_id']}",
        "input_sha256": case["input_sha256"],
        "method_contract_path": "docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md",
        "method_contract_sha256": sha256_file(method_path),
        "arithmetic_backend_manifest_path": "validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v2.json",
        "arithmetic_backend_manifest_sha256": sha256_file(backend_path),
        "resource_profile_path": (PLAN_REL / "auer_profile.json").as_posix(),
        "resource_profile_sha256": profile_sha,
        "source_snapshot_manifest_sha256": closure["source_closure_sha256"],
        "solver_source_sha256": sha256_file(solver_path),
        "checker_source_sha256": sha256_file(checker_path),
        "arithmetic_dependency": "shared exact validation.g2 Fraction/Interval/Budget and Taylor sin/cos; no claim of independent arithmetic kernel",
    }


def run_one(case_id: str, output_dir: Path) -> int:
    start = time.monotonic()
    freeze, protocol, benchmark = load_protocol_and_freeze()
    profile = strict_json(PROJECT / PLAN_REL / "auer_profile.json")
    common_profile = strict_json(PROJECT / PLAN_REL / "common_profile.json")
    closure_path = PROJECT / PLAN_REL / "auer_source_closure.json"
    closure = strict_json(closure_path)
    if sha256_file(closure_path) != freeze["source_closure_sha256"]:
        raise InvalidInput("SOURCE_CLOSURE_MANIFEST_SHA_MISMATCH")
    for item in closure["files"]:
        path = PROJECT / item["path"]
        if not path.is_file() or path.stat().st_size != item["size_bytes"] or sha256_file(path) != item["sha256"]:
            raise InvalidInput(f"SOURCE_CLOSURE_FILE_MISMATCH:{item['path']}")
    manifest_path = PROJECT / PLAN_REL / "auer_input_manifest.json"
    manifest = strict_json(manifest_path)
    cases = {item["query_id"]: item for item in manifest["cases"]}
    if case_id not in cases:
        raise InvalidInput("QUERY_ID_NOT_IN_G4_W2_THREE_CASE_MANIFEST")
    source_item = cases[case_id]
    payload = source_item["payload"]
    if canonical_sha256(payload) != source_item["input_sha256"]:
        raise InvalidInput("AUER_INPUT_SEMANTIC_HASH_MISMATCH")
    labels_order = manifest["parameter_label_order"]
    label_map = benchmark["parameter_cell"]["labels"]
    fixed_labels = {name: label_map[name] for name in labels_order}
    if set(fixed_labels) != {item["name"] for item in benchmark["parameter_labels"]}:
        raise InvalidInput("AUER_CASE_LABEL_SET_MISMATCH")
    scene = payload["scene"]
    horizon = payload["horizon"]["T"]
    state = payload["state_cell"]
    action = payload["action"]
    case = {
        "schema": "ddwmr-g4-auer-matched-query-input-v3-r9",
        "query_id": case_id,
        "candidate_manifest_v2_input_sha256": source_item["input_sha256"],
        "benchmark_path": str((PROJECT / PLAN_REL / "benchmark_v1.json").resolve()),
        "benchmark_sha256": sha256_file(PROJECT / PLAN_REL / "benchmark_v1.json"),
        "state_order": state["coordinates"],
        "initial_state": state["box"],
        "fixed_labels": fixed_labels,
        "held_voltage": action["V"],
        "horizon": horizon,
        "scene": scene,
        "parameter_cell": payload["parameter_cell"],
    }
    native_binding = _native_binding(case, freeze, benchmark, profile, closure)
    # Independent before producer input: enforce exact 2 s, three actions,
    # voltage equality, label order/domain, and full state box as frozen.
    expected = next(item for item in protocol["ordered_actions"] if item["comparison_id"].replace("V6", "AUER") == case_id)
    if case["held_voltage"] != [
        {"num": Fraction(s).numerator.__str__(), "den": Fraction(s).denominator.__str__()} for s in expected["voltage"]
    ]:
        raise InvalidInput("AUER_VOLTAGE_MAPPING_MISMATCH")
    if parse_q(case["horizon"]) != 2 or case["state_order"] != list(benchmark["state_cells"][0]["coordinates"]):
        raise InvalidInput("AUER_HORIZON_OR_STATE_ORDER_MISMATCH")
    if fixed_labels != label_map:
        raise InvalidInput("AUER_LABEL_DOMAIN_WAS_NARROWED_OR_REORDERED")

    max_ops = int(profile["max_rational_operations_per_ivp_combined_producer_replay_and_common_check"])
    max_bits = int(profile["max_rational_bits"])
    producer_budget = Budget(max_bits=max_bits, max_operations=max_ops,
                             wall_seconds=Fraction(int(profile["wall_time_seconds_per_ivp"])))
    benchmark_for_solver = benchmark
    native_start = time.monotonic()
    proof = solve_ddwmr_case(
        case, benchmark_for_solver,
        input_path=Path(native_binding["input_path"]), input_sha256=source_item["input_sha256"],
        method_sha256=native_binding["method_contract_sha256"],
        backend_sha256=native_binding["arithmetic_backend_manifest_sha256"],
        profile=profile, profile_sha256=native_binding["resource_profile_sha256"],
        snapshot_sha256=native_binding["source_snapshot_manifest_sha256"],
        solver_sha256=native_binding["solver_source_sha256"], checker_sha256=native_binding["checker_source_sha256"],
        resource_profile_path=native_binding["resource_profile_path"], budget=producer_budget,
    )
    native_seconds = time.monotonic() - native_start
    if proof.get("status") != "PROOF_COMPLETE":
        out = {
            "schema": "ddwmr-g4-w2-auerrun-v1", "query_id": case_id,
            "input_sha256": source_item["input_sha256"], "native_status": proof.get("status"),
            "termination": proof.get("termination"), "worker_status": proof.get("status"),
            "native_producer_seconds": native_seconds,
            "producer_rational_operations": producer_budget.operations,
            "proof": proof, "no_retry": True,
        }
        write_json(output_dir / "result.json", out)
        return 0 if proof.get("status") in {"UNKNOWN", "RESOURCE_LIMIT"} else 10

    envelope = _envelope(proof)
    proof_path = output_dir / "native_proof.json"
    proof_sha, proof_size = write_json(proof_path, envelope, max_bytes=int(profile["max_serialized_proof_bytes"]))
    producer_ops = producer_budget.operations
    if producer_ops >= max_ops:
        raise ResourceLimit("RATIONAL_OPERATION_LIMIT", "no operation budget remains for required native replay/common check")

    rhs_producer = int(proof.get("work", {}).get("rhs_jacobian_evaluations", 0))
    rhs_counter = {"count": rhs_producer, "limit": int(profile["max_rhs_jacobian_evaluations_per_ivp"])}
    replay_budget = Budget(max_bits=max_bits, max_operations=max_ops - producer_ops,
                           wall_seconds=Fraction(int(profile["wall_time_seconds_per_ivp"])))
    replay_start = time.monotonic()
    native_replay = replay_native_proof(
        envelope, case=case, benchmark=benchmark, profile=profile, fixture=None,
        expected_binding=native_binding, budget=replay_budget, rhs_eval_counter=rhs_counter,
    )
    replay_seconds = time.monotonic() - replay_start
    if not native_replay.get("replayed"):
        raise InvalidInput(f"IN_WORKER_NATIVE_REPLAY_FAILED:{native_replay.get('reason')}:{native_replay.get('detail')}")
    used_ops = producer_ops + replay_budget.operations
    if used_ops >= max_ops:
        raise ResourceLimit("RATIONAL_OPERATION_LIMIT", "no operation budget remains for common predicate")

    common_budget = Budget(max_bits=max_bits,
                           max_operations=min(int(common_profile["max_rational_operations_per_common_stage"]), max_ops - used_ops),
                           wall_seconds=Fraction(int(common_profile["wall_seconds"])))
    segments = make_segments(envelope, case, proof_path, common_budget,
                             source_binding={**native_binding, "benchmark": benchmark}, benchmark=benchmark)
    initial_state = tuple(Interval.from_json(row, common_budget) for row in case["initial_state"])
    scene_common = {"id": scene["id"], "p_o": scene["p_o"], "R_s": scene["R_s"]}
    common_start = time.monotonic()
    common_record, common_replay, progress = score_segments(
        segments, benchmark, scene_common, parse_q(case["horizon"], common_budget), initial_state,
        sqrt_bisections=int(common_profile["sqrt_bisections"]), budget=common_budget,
    )
    common_seconds = time.monotonic() - common_start
    if not common_replay.get("replayed"):
        raise InvalidInput(f"IN_WORKER_COMMON_REPLAY_FAILED:{common_replay}")
    progress_path = output_dir / "progress.json"
    progress_sha, _ = write_json(progress_path, progress)
    common_path = output_dir / "common_record.json"
    common_sha, _ = write_json(common_path, common_record)
    threshold = Fraction(7, 20)
    progress_bounds = [Fraction(value["num"], value["den"]) for value in progress["progress_enclosure_m"]]
    safety_pass = common_record["predicate_status"] == "PASS_ON_SUPPLIED_TUBE"
    eligible = safety_pass and progress_bounds[0] >= threshold
    if not safety_pass:
        final_status = "PROOF_COMPLETE_COMMON_UNKNOWN"
    elif not eligible:
        final_status = "CERTIFIED_SAFETY_TASK_INELIGIBLE"
    else:
        final_status = "CERTIFIED"
    out = {
        "schema": "ddwmr-g4-w2-auerrun-v1", "query_id": case_id,
        "input_sha256": source_item["input_sha256"], "peer_action_id": source_item["peer_action_id"],
        "held_voltage": case["held_voltage"], "hold": case["horizon"],
        "method_id": proof["method_id"], "native_status": proof["status"],
        "native_replay": native_replay, "native_replay_status": "PASS",
        "native_proof_path": proof_path.relative_to(PROJECT).as_posix(),
        "native_proof_sha256": proof_sha, "native_proof_bytes": proof_size,
        "native_proof_record_sha256": envelope["proof_sha256"],
        "common_record_path": common_path.relative_to(PROJECT).as_posix(), "common_record_sha256": common_sha,
        "common_replay": common_replay, "common_replay_status": "PASS",
        "common_summary": summarize_common(common_record), "common_progress": progress,
        "progress_sha256": progress_sha, "progress_lower_meets_threshold": progress_bounds[0] >= threshold,
        "task_eligible": eligible, "final_status": final_status,
        "resource_work": {
            "producer_rational_operations": producer_ops,
            "producer_peak_bits": producer_budget.max_bits,
            "native_replay_rational_operations": replay_budget.operations,
            "common_stage_rational_operations": common_budget.operations,
            "combined_rational_operations": used_ops + common_budget.operations,
            "combined_rational_cap": max_ops,
            "rhs_jacobian_producer_evaluations": rhs_producer,
            "rhs_jacobian_replay_evaluations": rhs_counter["count"] - rhs_producer,
            "rhs_jacobian_combined_evaluations": rhs_counter["count"],
            "rhs_jacobian_combined_cap": rhs_counter["limit"],
            "accepted_steps": proof["work"]["accepted_steps"],
            "rejected_step_attempts": proof["work"]["rejected_step_attempts"],
        },
        "stage_seconds": {"native_producer": native_seconds, "in_worker_native_replay": replay_seconds,
                          "common_stage_and_common_replay": common_seconds, "worker_elapsed_before_final_write": time.monotonic() - start},
        "no_retry": True,
    }
    write_json(output_dir / "result.json", out)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query-id", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        return run_one(args.query_id, Path(args.output_dir).resolve())
    except ResourceLimit as exc:
        out = {"schema": "ddwmr-g4-w2-auerrun-v1", "query_id": args.query_id,
               "native_status": "RESOURCE_LIMIT", "termination": {"kind": exc.kind, "detail": exc.detail},
               "no_retry": True}
        try:
            write_json(Path(args.output_dir).resolve() / "result.json", out)
        except Exception:
            pass
        return 20
    except Exception as exc:
        out = {"schema": "ddwmr-g4-w2-auerrun-v1", "query_id": args.query_id,
               "native_status": "IMPLEMENTATION_FAILURE", "termination": f"{type(exc).__name__}:{exc}",
               "no_retry": True}
        try:
            write_json(Path(args.output_dir).resolve() / "result.json", out)
        except Exception:
            pass
        return 30


if __name__ == "__main__":
    raise SystemExit(main())
