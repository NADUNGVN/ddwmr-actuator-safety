"""Independent proof-record replay; shares only exact interval primitives/model map."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Any

from .evaluator import _parse_input_query, _validate_profile, canonical_hash, query_hash_payload
from .hashing import HASH_PROTOCOL_ID
from .interval import interval_cosine, interval_matrix_exponential, interval_sine, matvec, sqrt_lower, vector_add
from .model import ModelIntervals, build_model, physical_internal_box, physical_radius
from .rational import Budget, Interval, InvalidInput, ResourceLimit, parse_q, qobj


def _load_interval(value: Any, budget: Budget) -> Interval:
    return Interval.from_json(value, budget)


def _load_matrix(value: Any, budget: Budget) -> list[list[Interval]]:
    return [[_load_interval(x, budget) for x in row] for row in value]


def _serialize_matrix(A: list[list[Interval]]) -> list[list[list[dict[str, str]]]]:
    return [[x.to_json() for x in row] for row in A]


def _serialize_vector(v: list[Interval]) -> list[list[dict[str, str]]]:
    return [x.to_json() for x in v]


def _abs(value: Interval) -> Interval:
    if value.lo >= 0:
        return value
    if value.hi <= 0:
        return -value
    return Interval(Fraction(0), value.abs_upper(), value.budget)


def _clip(value: Interval) -> Interval:
    return Interval(max(Fraction(-1), min(Fraction(1), value.lo)), max(Fraction(-1), min(Fraction(1), value.hi)), value.budget)


def _replay_picard(
    model: ModelIntervals, E: list[list[Interval]], initial: list[Interval], previous: list[Interval],
    voltage: list[Fraction], T: Fraction,
) -> tuple[list[Interval], list[Interval], list[Interval]]:
    budget = model.A[0][0].budget
    slips = matvec(model.S, previous)
    F = []
    for j, side in enumerate(("L", "R")):
        normalized = slips[j] / model.parameters["v_s"]
        F.append(model.parameters[f"C_{side}"] * _clip(normalized))
    V_intervals = [Interval.point(x, budget) for x in voltage]
    forcing = vector_add(matvec(model.B, V_intervals), matvec(model.D, F))
    complete_integrand = matvec(E, forcing)
    homogeneous = matvec(E, initial)
    duration = Interval(Fraction(0), T, budget)
    candidate = vector_add(homogeneous, [duration * value for value in complete_integrand])
    return candidate, F, complete_integrand


def _replay_residual(model: ModelIntervals, P0: list[Interval], P1: list[Interval]) -> tuple[list[Fraction], list[Fraction]]:
    budget = model.A[0][0].budget
    delta = [(P1[i] - P0[i]).abs_upper() for i in range(6)]
    force_residual = []
    for j, side in enumerate(("L", "R")):
        lipschitz_image = Fraction(0)
        for i in range(6):
            lipschitz_image = budget.add(lipschitz_image, budget.mul(model.QF[j][i].hi, delta[i]))
        amplitude_image = budget.mul(Fraction(2), model.parameters[f"C_{side}"].hi)
        force_residual.append(min(lipschitz_image, amplitude_image))
    return delta, force_residual


def _replay_comparison_matrices(model: ModelIntervals) -> tuple[list[list[Fraction]], list[list[Fraction]], list[list[Fraction]]]:
    budget = model.A[0][0].budget
    D_abs = [[x.abs_upper() for x in row] for row in model.D]
    qf_upper = [[x.hi for x in row] for row in model.QF]
    M_upper = []
    for i in range(6):
        row = []
        for j in range(6):
            value = model.A[i][j] if i == j else _abs(model.A[i][j])
            for k in range(2):
                value = value + Interval.point(budget.mul(D_abs[i][k], qf_upper[k][j]), budget)
            row.append(value.hi)
        M_upper.append(row)
    N = [[max(Fraction(0), x) for x in row] for row in M_upper]
    return M_upper, D_abs, N


def _replay_radius(
    N: list[list[Fraction]], D_abs: list[list[Fraction]], force: list[Fraction], T: Fraction,
    order: int, budget: Budget,
) -> tuple[list[Fraction], list[Fraction], Fraction, Fraction]:
    forcing = []
    for row in D_abs:
        entry = Fraction(0)
        for j in range(2):
            entry = budget.add(entry, budget.mul(row[j], force[j]))
        forcing.append(entry)
    forcing_norm = max(forcing)
    row_norms = []
    for row in N:
        row_sum = Fraction(0)
        for entry in row:
            row_sum = budget.add(row_sum, entry)
        row_norms.append(row_sum)
    Q = budget.mul(max(row_norms), T)
    vector = forcing[:]
    t_over_factorial = T
    partial = [Fraction(0)] * 6
    for k in range(order + 1):
        for i in range(6):
            partial[i] = budget.add(partial[i], budget.mul(t_over_factorial, vector[i]))
        if k < order:
            vector = [
                sum_checked((budget.mul(a, b) for a, b in zip(row, vector)), budget)
                for row in N
            ]
            t_over_factorial = budget.div(budget.mul(t_over_factorial, T), Fraction(k + 2))
    if not Q or not forcing_norm:
        tail = Fraction(0)
    else:
        ceil_q = (Q.numerator + Q.denominator - 1) // Q.denominator
        tail = budget.mul(T, forcing_norm)
        tail = budget.mul(tail, budget.pow(Fraction(3), ceil_q))
        tail = budget.mul(tail, budget.pow(Q, order + 1))
        tail = budget.div(tail, Fraction(math.factorial(order + 2)))
    return [budget.add(x, tail) for x in partial], forcing, Q, tail


def sum_checked(values, budget: Budget) -> Fraction:
    total = Fraction(0)
    for value in values:
        total = budget.add(total, value)
    return total


def _query_binding_errors(record: dict[str, Any], query: dict[str, Any]) -> list[str]:
    protocol = query.get("hash_protocol_id")
    protocol_v2 = protocol == HASH_PROTOCOL_ID
    expected = {
        "schema": "ddwmr-g2-record-v2" if protocol_v2 else "ddwmr-g2-record-v1",
        "query_id": query.get("query_id"),
        "method_id": "G2_COMP_CLIP_WHOLE_HOLD_INTERVAL_HULL_N1_R2" if protocol_v2 else "G2_COMP_CLIP_WHOLE_HOLD_INTERVAL_HULL_N1_V1",
        "profile_id": query.get("profile", {}).get("id"),
        "held_voltage": query.get("action", {}).get("V"),
        "horizon": query.get("horizon", {}).get("T"),
        "state_cell_id": query.get("state_cell", {}).get("id"),
        "scene_id": query.get("scene", {}).get("id"),
        "horizon_id": query.get("horizon", {}).get("id"),
        "action_id": query.get("action", {}).get("id"),
        "parameter_cell_id": query.get("parameter_cell", {}).get("id"),
        "benchmark_sha256": query.get("benchmark_sha256"),
        "development_manifest_sha256": query.get("development_manifest_sha256"),
        "quantifiers": {
            "one_common_voltage_for_all_initial_states_and_labels": True,
            "initial_state_cell_universal": True,
            "parameter_labels_fixed_for_entire_hold": True,
            "time_coverage": "closed [0,T] by whole-hold ranges",
            "coefficient_representation": "named outer interval hull; interval arithmetic may forget rational-map correlations but does not resample a physical label",
            "endpoint_target_requested": False,
        },
    }
    errors = [key for key, value in expected.items() if record.get(key) != value]
    if record.get("input_sha256") != canonical_hash(query_hash_payload(query)):
        errors.append("input_sha256")
    if record.get("status") not in {"CERTIFIED", "UNKNOWN"}:
        errors.append("status_not_replayable")
    if protocol_v2:
        if canonical_hash(query.get("benchmark")) != query.get("benchmark_sha256"):
            errors.append("benchmark_content_sha256")
        expected_specification = canonical_hash({
            "hash_protocol_id": protocol,
            "benchmark_sha256": query.get("benchmark_sha256"),
            "development_manifest_sha256": query.get("development_manifest_sha256"),
        })
        if record.get("hash_protocol_id") != protocol:
            errors.append("hash_protocol_id")
        if record.get("profile_sha256") != canonical_hash(query.get("profile")):
            errors.append("profile_sha256")
        if record.get("specification_sha256") != expected_specification:
            errors.append("specification_sha256")
    return errors


def _validate_effective_query(query: dict[str, Any]) -> tuple[bool, str | None]:
    try:
        for key in ("state_cell", "scene", "horizon", "action", "parameter_cell"):
            value = query.get(key)
            if not isinstance(value, dict) or not isinstance(value.get("id"), str) or not value["id"]:
                raise InvalidInput(f"{key} must have a nonempty string ID")
        benchmark = query["benchmark"]
        if not isinstance(benchmark, dict) or query["parameter_cell"] != benchmark.get("parameter_cell"):
            raise InvalidInput("query parameter cell must match the hashed benchmark parameter cell")
        profile = query["profile"]
        wall = _validate_profile(profile)
        budget = Budget(profile["max_rational_bits"], profile["max_rational_operations"], wall)
        budget.set_stage("checker.query_contract")
        _parse_input_query(
            benchmark, query["state_cell"], query["scene"], query["horizon"],
            query["action"], profile, budget,
        )
    except (InvalidInput, ResourceLimit, KeyError, TypeError, ValueError) as exc:
        return False, f"{type(exc).__name__}: {exc}"
    return True, None


def _replay_record_impl(record: dict[str, Any], query: dict[str, Any]) -> dict[str, Any]:
    """Recompute the claim from the serialized proof, never calling run_query/evaluate."""
    status = record.get("status")
    binding_errors = _query_binding_errors(record, query)
    if binding_errors:
        return {"replayed": False, "record_integrity_valid": False, "status": status, "binding_errors": binding_errors}
    query_valid, query_error = _validate_effective_query(query)
    if not query_valid:
        return {"replayed": False, "record_integrity_valid": False, "status": status, "query_contract_error": query_error}
    proof = record.get("proof")
    if proof is None:
        resource_reasons = {"RATIONAL_BIT_LIMIT", "RATIONAL_OPERATION_LIMIT", "WALL_TIME_LIMIT"}
        reasons = record.get("reason_codes")
        if (
            status != "UNKNOWN" or not isinstance(reasons, list) or not reasons
            or len(reasons) != 1
            or any(not isinstance(reason, str) for reason in reasons)
            or not set(reasons) <= resource_reasons
        ):
            return {"replayed": False, "record_integrity_valid": False, "status": status, "reason": "proof-less record is not a declared resource UNKNOWN"}
        if query.get("hash_protocol_id") == HASH_PROTOCOL_ID:
            diagnostic = record.get("resource_diagnostic")
            work_value = record.get("work")
            work = work_value if isinstance(work_value, dict) else {}
            failure = diagnostic.get("failure") if isinstance(diagnostic, dict) else None
            caps = diagnostic.get("configured_caps") if isinstance(diagnostic, dict) else None
            if reasons[0] == "RATIONAL_BIT_LIMIT":
                expected_cap = ("max_rational_bits", query["profile"]["max_rational_bits"])
            elif reasons[0] == "RATIONAL_OPERATION_LIMIT":
                expected_cap = ("max_rational_operations", query["profile"]["max_rational_operations"])
            elif reasons[0] == "WALL_TIME_LIMIT":
                wall_limit = parse_q(query["profile"]["wall_seconds_per_query"])
                expected_cap = ("wall_seconds_per_query", {"num": str(wall_limit.numerator), "den": str(wall_limit.denominator)})
            else:
                expected_cap = None
            counter_names = (
                "operation_attempts", "operations_started", "completed_results",
                "max_preoperation_estimate_bits", "max_completed_result_bits", "max_observed_result_bits",
            )
            counter_types_valid = isinstance(diagnostic, dict) and all(
                isinstance(diagnostic.get(name), int) and not isinstance(diagnostic.get(name), bool)
                and diagnostic.get(name) >= 0 for name in counter_names
            )
            work_counter_types_valid = all(
                isinstance(work.get(name), int) and not isinstance(work.get(name), bool) and work.get(name) >= 0
                for name in (
                    "rational_operations", "operation_attempts", "completed_results", "max_rational_bits",
                    "max_preoperation_estimate_bits", "max_completed_result_bits",
                )
            )
            operand_widths_valid = isinstance(failure, dict) and isinstance(failure.get("operand_bit_lengths"), list) and all(
                isinstance(width, dict)
                and set(width) == {"numerator_bits", "denominator_bits"}
                and all(isinstance(width.get(name), int) and not isinstance(width.get(name), bool) and width[name] >= 0
                        for name in ("numerator_bits", "denominator_bits"))
                for width in failure.get("operand_bit_lengths", [])
            )
            failure_counters_match = isinstance(failure, dict) and all(
                failure.get(failure_name) == diagnostic.get(diagnostic_name)
                for failure_name, diagnostic_name in (
                    ("operation_attempts", "operation_attempts"), ("operations_started", "operations_started"),
                    ("completed_results", "completed_results"),
                    ("max_preoperation_estimate_bits", "max_preoperation_estimate_bits"),
                    ("max_completed_result_bits", "max_completed_result_bits"),
                    ("max_observed_result_bits", "max_observed_result_bits"),
                )
            )
            failure_limit_valid = False
            if isinstance(failure, dict) and expected_cap is not None:
                if reasons[0] == "RATIONAL_BIT_LIMIT":
                    observed = failure.get("estimated_or_observed_bits")
                    estimate_kind = failure.get("estimate_kind")
                    failure_limit_valid = (
                        estimate_kind in {
                            "preoperation_intermediate_upper_estimate", "reduced_result",
                            "input_digit_width_upper_estimate", "input_observed",
                        }
                        and isinstance(observed, int) and not isinstance(observed, bool)
                        and observed > expected_cap[1]
                        and diagnostic.get("operations_started") <= query["profile"]["max_rational_operations"]
                        and (
                            diagnostic.get("operation_attempts") == diagnostic.get("operations_started") + 1
                            if estimate_kind == "preoperation_intermediate_upper_estimate"
                            else diagnostic.get("operation_attempts") == diagnostic.get("operations_started")
                            if estimate_kind in {"reduced_result", "input_digit_width_upper_estimate", "input_observed"}
                            else False
                        )
                    )
                elif reasons[0] == "RATIONAL_OPERATION_LIMIT":
                    failure_limit_valid = (
                        failure.get("estimate_kind") == "operation_count"
                        and failure.get("estimated_or_observed_bits") is None
                        and diagnostic.get("operation_attempts") == expected_cap[1] + 1
                        and diagnostic.get("operations_started") == expected_cap[1]
                    )
                elif reasons[0] == "WALL_TIME_LIMIT":
                    wall_caps = caps.get("wall_time") if isinstance(caps, dict) else None
                    failure_limit_valid = (
                        failure.get("estimate_kind") == "wall_time"
                        and isinstance(wall_caps, dict)
                        and wall_caps.get("enforced") is True
                        and wall_caps.get("configured_seconds") == expected_cap[1]
                    )
            telemetry_valid = (
                isinstance(diagnostic, dict)
                and diagnostic.get("schema") == "ddwmr-g2-resource-diagnostic-v1"
                and isinstance(failure, dict)
                and failure.get("schema") == "ddwmr-g2-resource-diagnostic-v1"
                and isinstance(diagnostic.get("stage_id"), str) and bool(diagnostic.get("stage_id"))
                and failure.get("stage_id") == diagnostic.get("stage_id")
                and isinstance(failure.get("primitive_id"), str) and bool(failure.get("primitive_id"))
                and isinstance(failure.get("estimate_kind"), str) and bool(failure.get("estimate_kind"))
                and failure.get("kind") == reasons[0]
                and isinstance(caps, dict)
                and caps.get("max_rational_bits") == query["profile"]["max_rational_bits"]
                and caps.get("max_rational_operations") == query["profile"]["max_rational_operations"]
                and expected_cap is not None
                and failure.get("configured_cap_name") == expected_cap[0]
                and failure.get("configured_cap_value") == expected_cap[1]
                and operand_widths_valid
                and counter_types_valid
                and work_counter_types_valid
                and failure_counters_match
                and failure_limit_valid
                and work.get("rational_operations") == diagnostic.get("operations_started")
                and work.get("operation_attempts") == diagnostic.get("operation_attempts")
                and work.get("completed_results") == diagnostic.get("completed_results")
                and work.get("max_rational_bits") == diagnostic.get("max_observed_result_bits")
                and work.get("max_preoperation_estimate_bits") == diagnostic.get("max_preoperation_estimate_bits")
                and work.get("max_completed_result_bits") == diagnostic.get("max_completed_result_bits")
                and diagnostic.get("operation_attempts", -1) >= diagnostic.get("operations_started", 0)
                and diagnostic.get("completed_results", -1) <= diagnostic.get("operation_attempts", 0)
                and diagnostic.get("max_observed_result_bits", 0) >= diagnostic.get("max_completed_result_bits", 0)
            )
            if not telemetry_valid:
                return {"replayed": False, "record_integrity_valid": False, "status": status, "reason": "resource diagnostic does not match the bounded failure record"}
        return {
            "replayed": False,
            "record_integrity_valid": True,
            "resource_limited": True,
            "status": status,
            "reason": "record integrity checked; arithmetic replay not applicable without a proof object",
        }

    if not isinstance(proof, dict):
        return {"replayed": False, "record_integrity_valid": False, "status": status, "reason": "proof object must be a JSON object"}
    profile = query["profile"]
    budget = Budget(profile["max_rational_bits"], profile["max_rational_operations"] * 2)
    budget.set_stage("checker.query_replay")
    T = parse_q(query["horizon"]["T"], budget)
    voltage = [parse_q(x, budget) for x in query["action"]["V"]]
    model = build_model(query["benchmark"], budget)
    X = [Interval.from_json(pair, budget) for pair in query["state_cell"]["box"]]
    indices = [3, 4, 5, 6, 7, 8]
    initial = [X[index] / Interval.point(model.scales[j], budget) for j, index in enumerate(indices)]
    exp_range, exp_q, exp_remainder = interval_matrix_exponential(model.A, T, profile["exp_taylor_degree"])
    P0, Fm1, _ = _replay_picard(model, exp_range, initial, initial, voltage, T)
    P1, F0, _ = _replay_picard(model, exp_range, initial, P0, voltage, T)
    delta, force = _replay_residual(model, P0, P1)
    M_upper, D_abs, N = _replay_comparison_matrices(model)
    eta_scaled, forcing, comparison_Q, tail = _replay_radius(
        N, D_abs, force, T, profile["comparison_series_order"], budget
    )
    eta_physical = physical_radius(eta_scaled, model.scales, budget)
    P1_physical = physical_internal_box(P1, model.scales)
    U = max(abs(P1_physical[0].lo), abs(P1_physical[0].hi))
    R = max(abs(P1_physical[1].lo), abs(P1_physical[1].hi))
    E_theta = budget.mul(T, eta_physical[1])
    E_p = budget.mul(T, budget.add(eta_physical[0], budget.mul(U, min(budget.mul(T, eta_physical[1]), Fraction(2)))))
    duration = Interval(Fraction(0), T, budget)
    heading = X[2] + duration * P1_physical[1]
    cosine = interval_cosine(heading, profile["trig_taylor_degree"])
    sine = interval_sine(heading, profile["trig_taylor_degree"])
    px = X[0] + duration * (P1_physical[0] * cosine)
    py = X[1] + duration * (P1_physical[0] * sine)

    slip = [x / model.parameters["v_s"] for x in matvec(model.S, P1)]
    beta = []
    for side_i in range(2):
        bphi = _clip(slip[side_i]).abs_upper()
        slip_error = Fraction(0)
        for j in range(6):
            slip_error = budget.add(slip_error, budget.mul(model.S[side_i][j].abs_upper(), eta_scaled[j]))
        beta.append(min(Fraction(1), budget.add(bphi, budget.div(slip_error, model.parameters["v_s"].lo))))
    roots = []
    reserve = Fraction(0)
    for side_i, side in enumerate(("L", "R")):
        radicand = budget.add(Fraction(1), -budget.mul(beta[side_i], beta[side_i]))
        lo, hi = sqrt_lower(radicand, profile["sqrt_bisections"], budget)
        roots.append([lo, hi])
        reserve = budget.add(reserve, budget.mul(model.parameters[f"C_{side}"].lo, lo))
    demand = budget.mul(model.parameters["m"].hi, budget.mul(budget.add(U, eta_physical[0]), budget.add(R, eta_physical[1])))
    contact_margin = budget.add(reserve, -demand)

    obstacle = query["scene"]
    ox, oy = [parse_q(x, budget) for x in obstacle["p_o"]]
    dx = max(Fraction(0), budget.add(px.lo, -ox), budget.add(ox, -px.hi))
    dy = max(Fraction(0), budget.add(py.lo, -oy), budget.add(oy, -py.hi))
    distance, distance_hi = sqrt_lower(budget.add(budget.mul(dx, dx), budget.mul(dy, dy)), profile["sqrt_bisections"], budget)
    collision_margin = budget.add(budget.add(distance, -parse_q(obstacle["R_s"], budget)), -E_p)

    internal_center_width = [budget.add(x.hi, -x.lo) for x in P1_physical]
    internal_total_width = [budget.add(width, budget.mul(Fraction(2), radius)) for width, radius in zip(internal_center_width, eta_physical)]
    pose_center_ranges = [px, py, heading]
    pose_errors = [E_p, E_p, E_theta]
    pose_center_width = [budget.add(x.hi, -x.lo) for x in pose_center_ranges]
    pose_total_width = [budget.add(width, budget.mul(Fraction(2), radius)) for width, radius in zip(pose_center_width, pose_errors)]

    # Exact equality checks make the record a replayable arithmetic proof, not a status assertion.
    expected = {
        "parameter_label_order": model.parameter_label_order,
        "parameter_label_cell": {name: value.to_json() for name, value in model.parameter_label_box.items()},
        "fixed_parameter_label_count": len(model.parameter_label_order),
        "nonpoint_coefficient_interval_entries": sum(
            value.lo != value.hi for block in (model.A, model.B, model.D, model.S, model.QF) for row in block for value in row
        ),
        "parameter_intervals": {name: x.to_json() for name, x in model.parameters.items()},
        "A_scaled": [[x.to_json() for x in row] for row in model.A],
        "B_scaled": [[x.to_json() for x in row] for row in model.B],
        "D_scaled": [[x.to_json() for x in row] for row in model.D],
        "S_scaled": [[x.to_json() for x in row] for row in model.S],
        "QF_scaled": [[x.to_json() for x in row] for row in model.QF],
        "internal_initial_scaled": [x.to_json() for x in initial],
        "exp_range": _serialize_matrix(exp_range), "exp_norm_bound": qobj(exp_q), "exp_remainder": qobj(exp_remainder),
        "P0_scaled": _serialize_vector(P0), "P1_scaled": _serialize_vector(P1),
        "force_at_initial_predictor": _serialize_vector(Fm1), "force_at_P0": _serialize_vector(F0),
        "delta_abs_scaled": [qobj(x) for x in delta], "residual_force_upper": [qobj(x) for x in force],
        "M_upper": [[qobj(x) for x in row] for row in M_upper],
        "D_abs_upper": [[qobj(x) for x in row] for row in D_abs],
        "N_nonnegative_majorant": [[qobj(x) for x in row] for row in N],
        "comparison_forcing": [qobj(x) for x in forcing], "comparison_Q": qobj(comparison_Q),
        "comparison_tail": qobj(tail), "eta_scaled": [qobj(x) for x in eta_scaled],
        "eta_physical": [qobj(x) for x in eta_physical],
        "center_heading_range": heading.to_json(), "center_position_x_range": px.to_json(),
        "center_position_y_range": py.to_json(), "E_theta": qobj(E_theta), "E_p": qobj(E_p),
        "beta_upper": [qobj(x) for x in beta],
        "sqrt_lower_upper_brackets": [[qobj(lo), qobj(hi)] for lo, hi in roots],
        "contact_available_lower": qobj(reserve), "contact_demand_upper": qobj(demand),
        "contact_margin_lower": qobj(contact_margin),
        "collision": [{
            "obstacle_id": obstacle["id"], "distance_lower": qobj(distance),
            "distance_upper_bracket": qobj(distance_hi), "margin_lower": qobj(collision_margin),
        }],
    }
    differences = [key for key, value in expected.items() if proof.get(key) != value]
    if set(proof) != set(expected):
        differences.append("proof_field_set")
    if differences:
        return {"replayed": False, "record_integrity_valid": False, "status": status, "mismatched_proof_fields": differences}
    if record.get("collision_margin_lower") != [qobj(collision_margin)] or record.get("contact_margin_lower") != qobj(contact_margin):
        return {"replayed": False, "record_integrity_valid": False, "status": status, "mismatched_record_margins": True}
    annotations = {
        "obstacle_count": 1,
        "center_width_internal_physical": [qobj(x) for x in internal_center_width],
        "error_radius_internal_physical": [qobj(x) for x in eta_physical],
        "total_width_internal_physical": [qobj(x) for x in internal_total_width],
        "center_width_pose": [qobj(x) for x in pose_center_width],
        "error_radius_pose": [qobj(x) for x in pose_errors],
        "total_width_pose": [qobj(x) for x in pose_total_width],
    }
    annotation_mismatches = [key for key, value in annotations.items() if record.get(key) != value]
    if annotation_mismatches:
        return {"replayed": False, "record_integrity_valid": False, "status": status, "mismatched_record_annotations": annotation_mismatches}
    should_certify = collision_margin >= 0 and contact_margin >= 0
    if (status == "CERTIFIED") != should_certify:
        return {"replayed": False, "record_integrity_valid": False, "status": status, "computed_should_certify": should_certify}
    expected_reasons = []
    if contact_margin < 0:
        expected_reasons.append("CONTACT_SUFFICIENT_MARGIN_NEGATIVE")
    if collision_margin < 0:
        expected_reasons.append("COLLISION_SUFFICIENT_MARGIN_NEGATIVE")
    reason_codes = record.get("reason_codes")
    if not isinstance(reason_codes, list) or any(not isinstance(reason, str) for reason in reason_codes) or reason_codes != expected_reasons:
        return {"replayed": False, "record_integrity_valid": False, "status": status, "mismatched_reason_codes": True}
    work_value = record.get("work")
    if not isinstance(work_value, dict):
        return {"replayed": False, "record_integrity_valid": False, "status": status, "reason": "work counters must be a JSON object"}
    work = work_value
    expected_work = {
        "parameter_leaves": 1, "initial_state_leaves": 1,
        "time_slabs": profile["time_slab_count"],
        "whole_hold_hull_reused_on_slabs": profile["time_slab_count"] > 1,
        "exp_degree": profile["exp_taylor_degree"], "trig_degree": profile["trig_taylor_degree"],
        "comparison_order": profile["comparison_series_order"], "sqrt_bisections": profile["sqrt_bisections"],
        "configured_caps": {
            "max_rational_bits": profile["max_rational_bits"],
            "max_rational_operations": profile["max_rational_operations"],
        },
    }
    work_mismatches = [key for key, value in expected_work.items() if work.get(key) != value]
    if work.get("rational_operations", profile["max_rational_operations"] + 1) > profile["max_rational_operations"]:
        work_mismatches.append("rational_operations")
    if work.get("rational_operations", -1) < 0:
        work_mismatches.append("rational_operations")
    if work.get("max_rational_bits", profile["max_rational_bits"] + 1) > profile["max_rational_bits"]:
        work_mismatches.append("max_rational_bits")
    for key in ("operation_attempts", "completed_results", "max_preoperation_estimate_bits", "max_completed_result_bits"):
        if not isinstance(work.get(key), int) or isinstance(work.get(key), bool) or work.get(key, profile["max_rational_operations"] + 1) < 0:
            work_mismatches.append(key)
    if work.get("operation_attempts") != work.get("rational_operations"):
        work_mismatches.append("operation_attempts")
    if work.get("completed_results", profile["max_rational_operations"] + 1) > work.get("operation_attempts", 0):
        work_mismatches.append("completed_results")
    if work.get("max_preoperation_estimate_bits", profile["max_rational_bits"] + 1) > profile["max_rational_bits"]:
        work_mismatches.append("max_preoperation_estimate_bits")
    if work.get("max_completed_result_bits", profile["max_rational_bits"] + 1) > profile["max_rational_bits"]:
        work_mismatches.append("max_completed_result_bits")
    if work.get("max_rational_bits", -1) < work.get("max_completed_result_bits", 0):
        work_mismatches.append("max_rational_bits")
    if work_mismatches:
        return {"replayed": False, "record_integrity_valid": False, "status": status, "mismatched_work_fields": sorted(set(work_mismatches))}
    return {
        "replayed": True, "proof_replay_pass": True, "record_integrity_valid": True,
        "status": status, "collision_margin": qobj(collision_margin),
        "contact_margin": qobj(contact_margin), "checker_operations": budget.operations,
        "shared_trusted_components": ["exact Fraction interval primitives", "parameter-map and model matrix constructor", "validated exp/trig/root primitives"],
    }


def replay_record(record: dict[str, Any], query: dict[str, Any]) -> dict[str, Any]:
    """Return an explicit rejection result for malformed or unbounded replay inputs."""
    status = record.get("status") if isinstance(record, dict) else None
    try:
        return _replay_record_impl(record, query)
    except ResourceLimit as exc:
        return {
            "replayed": False, "record_integrity_valid": False, "status": status,
            "checker_resource_limited": True, "reason": f"{exc.kind}: {exc.detail}",
        }
    except Exception as exc:
        return {
            "replayed": False, "record_integrity_valid": False, "status": status,
            "reason": f"checker rejected malformed or unsupported record/query: {type(exc).__name__}: {exc}",
        }
