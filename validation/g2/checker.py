"""Independent proof-record replay; shares only exact interval primitives/model map."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Any

from .evaluator import canonical_hash
from .interval import interval_cosine, interval_matrix_exponential, interval_sine, matvec, sqrt_lower, vector_add
from .model import ModelIntervals, build_model, physical_internal_box, physical_radius
from .rational import Budget, Interval, InvalidInput, parse_q, qobj


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


def replay_record(record: dict[str, Any], query: dict[str, Any]) -> dict[str, Any]:
    """Recompute the claim from the serialized proof, never calling run_query/evaluate."""
    status = record.get("status")
    if status in {"INVALID_INPUT", "EXECUTION_FAILURE"}:
        return {"replayed": False, "status": status, "reason": "non-certificate record"}
    proof = record.get("proof")
    if proof is None:
        return {
            "replayed": status == "UNKNOWN" and bool(record.get("reason_codes")),
            "status": status,
            "reason": "bounded resource UNKNOWN without completed proof object",
        }

    profile = query["profile"]
    budget = Budget(profile["max_rational_bits"], profile["max_rational_operations"] * 2)
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
    if differences:
        return {"replayed": False, "status": status, "mismatched_proof_fields": differences}
    if record.get("collision_margin_lower") != [qobj(collision_margin)] or record.get("contact_margin_lower") != qobj(contact_margin):
        return {"replayed": False, "status": status, "mismatched_record_margins": True}
    should_certify = collision_margin >= 0 and contact_margin >= 0
    if (status == "CERTIFIED") != should_certify:
        return {"replayed": False, "status": status, "computed_should_certify": should_certify}
    return {
        "replayed": True, "status": status, "collision_margin": qobj(collision_margin),
        "contact_margin": qobj(contact_margin), "checker_operations": budget.operations,
        "shared_trusted_components": ["exact Fraction interval primitives", "parameter-map and model matrix constructor", "validated exp/trig/root primitives"],
    }
