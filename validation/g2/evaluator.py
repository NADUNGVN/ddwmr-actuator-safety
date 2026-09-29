"""One-hold rational interval fallback evaluator for G2-COMP-clip."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

from .interval import (
    interval_cosine, interval_matrix_exponential, interval_sine, matvec,
    sqrt_lower, vector_add,
)
from .model import ModelIntervals, build_model, physical_internal_box, physical_radius
from .rational import Budget, Interval, InvalidInput, ResourceLimit, parse_q, qobj, qtext


ROOT = Path(__file__).resolve().parents[2]
STATE_COORDINATES = ["p_x", "p_y", "theta", "u", "r", "omega_L", "omega_R", "i_L", "i_R"]


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_revision() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip()


def _point(value: Fraction, budget: Budget) -> Interval:
    return Interval.point(value, budget)


def _abs_interval(value: Interval) -> Interval:
    if value.lo >= 0:
        return value
    if value.hi <= 0:
        return -value
    return Interval(Fraction(0), value.abs_upper(), value.budget)


def _matrix_upper_abs(A: list[list[Interval]]) -> list[list[Fraction]]:
    return [[x.abs_upper() for x in row] for row in A]


def _bound_model_matrices(model: ModelIntervals) -> tuple[list[list[Fraction]], list[list[Fraction]], list[list[Fraction]]]:
    budget = model.A[0][0].budget
    M_bar: list[list[Fraction]] = []
    D_bar = _matrix_upper_abs(model.D)
    qf_upper = [[x.hi for x in row] for row in model.QF]
    for i in range(6):
        row = []
        for j in range(6):
            a_sharp = model.A[i][j] if i == j else _abs_interval(model.A[i][j])
            value = a_sharp
            for k in range(2):
                product = budget.mul(D_bar[i][k], qf_upper[k][j])
                value = value + _point(product, budget)
            row.append(value.hi)
        M_bar.append(row)
    N = [[max(Fraction(0), value) for value in row] for row in M_bar]
    return M_bar, D_bar, N


def _matvec_positive(A: list[list[Fraction]], x: list[Fraction], budget: Budget) -> list[Fraction]:
    result = []
    for row in A:
        total = Fraction(0)
        for a, value in zip(row, x):
            total = budget.add(total, budget.mul(a, value))
        result.append(total)
    return result


def _matmul_positive(A: list[list[Fraction]], B: list[list[Fraction]], budget: Budget) -> list[list[Fraction]]:
    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            total = Fraction(0)
            for k in range(len(B)):
                total = budget.add(total, budget.mul(A[i][k], B[k][j]))
            row.append(total)
        result.append(row)
    return result


def _radius_series(
    N: list[list[Fraction]], D_bar: list[list[Fraction]], d_bar: list[Fraction], T: Fraction,
    order: int, budget: Budget,
) -> tuple[list[Fraction], list[Fraction], Fraction, Fraction]:
    q_vec = []
    for row in D_bar:
        total = Fraction(0)
        for d, force_bound in zip(row, d_bar):
            total = budget.add(total, budget.mul(d, force_bound))
        q_vec.append(total)
    q_norm = max(q_vec, default=Fraction(0))
    row_norms = []
    for row in N:
        total = Fraction(0)
        for value in row:
            total = budget.add(total, value)
        row_norms.append(total)
    n_norm = max(row_norms, default=Fraction(0))
    Q = budget.mul(n_norm, T)
    partial = [Fraction(0)] * len(N)
    power = [row[:] for row in N]
    vector = q_vec[:]
    t_power = T
    for k in range(order + 1):
        denominator = Fraction(math.factorial(k + 1))
        coeff = budget.div(t_power, denominator)
        for i in range(len(partial)):
            partial[i] = budget.add(partial[i], budget.mul(coeff, vector[i]))
        if k < order:
            vector = _matvec_positive(N, vector, budget)
            t_power = budget.mul(t_power, T)
            t_power = budget.div(t_power, Fraction(k + 2))
    if Q == 0 or q_norm == 0:
        tail = Fraction(0)
    else:
        exp_majorant = budget.pow(Fraction(3), (Q.numerator + Q.denominator - 1) // Q.denominator)
        tail_numerator = budget.mul(T, q_norm)
        tail_numerator = budget.mul(tail_numerator, exp_majorant)
        tail_numerator = budget.mul(tail_numerator, budget.pow(Q, order + 1))
        tail = budget.div(tail_numerator, Fraction(math.factorial(order + 2)))
    total = [budget.add(value, tail) for value in partial]
    return total, q_vec, Q, tail


def _clip_interval(value: Interval) -> Interval:
    lo = max(Fraction(-1), min(Fraction(1), value.lo))
    hi = max(Fraction(-1), min(Fraction(1), value.hi))
    return Interval(lo, hi, value.budget)


def _force_ranges(model: ModelIntervals, P: list[Interval]) -> list[Interval]:
    budget = model.A[0][0].budget
    slip = matvec(model.S, P)
    forces = []
    for side, index in (("L", 0), ("R", 1)):
        normalized_slip = slip[index] / model.parameters["v_s"]
        forces.append(model.parameters[f"C_{side}"] * _clip_interval(normalized_slip))
    return forces


def _predictor_level(
    model: ModelIntervals, E: list[list[Interval]], X: list[Interval], P_previous: list[Interval],
    V: list[Fraction], T: Fraction,
) -> tuple[list[Interval], list[Interval], list[Interval]]:
    budget = model.A[0][0].budget
    forces = _force_ranges(model, P_previous)
    input_vector = vector_add(matvec(model.B, [_point(V[0], budget), _point(V[1], budget)]), matvec(model.D, forces))
    integrand = matvec(E, input_vector)
    homogeneous = matvec(E, X)
    duration = Interval(Fraction(0), T, budget)
    P = vector_add(homogeneous, [duration * value for value in integrand])
    return P, forces, integrand


def _parse_input_query(
    benchmark: dict[str, Any], state_cell: dict[str, Any], scene: dict[str, Any], horizon: dict[str, Any],
    action: dict[str, Any], profile: dict[str, Any], budget: Budget,
) -> tuple[list[Interval], Fraction, list[Fraction], list[dict[str, Fraction]], Fraction]:
    if not isinstance(state_cell, dict) or not isinstance(scene, dict) or not isinstance(horizon, dict) or not isinstance(action, dict):
        raise InvalidInput("state, scene, horizon, and action query records must be objects")
    if state_cell.get("coordinates") != STATE_COORDINATES:
        raise InvalidInput("state coordinates must use the declared nine-state MASTER order")
    if not isinstance(state_cell.get("box"), list):
        raise InvalidInput("state cell must provide a finite rational box")
    X = [Interval.from_json(pair, budget) for pair in state_cell["box"]]
    if len(X) != 9:
        raise InvalidInput("initial state cell must have nine coordinates")
    if "T" not in horizon:
        raise InvalidInput("hold duration is missing")
    T = parse_q(horizon["T"], budget)
    if not isinstance(action.get("V"), list) or len(action["V"]) != 2:
        raise InvalidInput("query voltage must contain two rational components")
    V = [parse_q(x, budget) for x in action["V"]]
    if "V_max" not in benchmark:
        raise InvalidInput("voltage limit is missing")
    V_max = parse_q(benchmark["V_max"], budget)
    if T <= 0 or len(V) != 2 or any(abs(x) > V_max for x in V):
        raise InvalidInput("invalid horizon or voltage")
    if not isinstance(scene.get("p_o"), list) or len(scene["p_o"]) != 2:
        raise InvalidInput("circular obstacle center must have two coordinates")
    if "R_s" not in scene:
        raise InvalidInput("obstacle exclusion radius is missing")
    obstacle = [{
        "id": scene["id"],
        "p_o": [parse_q(x, budget) for x in scene["p_o"]],
        "R_s": parse_q(scene["R_s"], budget),
    }]
    if obstacle[0]["R_s"] <= 0:
        raise InvalidInput("obstacle exclusion radius must be positive")
    degrees = [profile.get("exp_taylor_degree"), profile.get("trig_taylor_degree"), profile.get("comparison_series_order")]
    if any(not isinstance(x, int) or isinstance(x, bool) or x < 0 or x > 40 for x in degrees):
        raise InvalidInput("Taylor and comparison degrees must be integers in [0,40]")
    root_count = profile.get("sqrt_bisections")
    if not isinstance(root_count, int) or isinstance(root_count, bool) or root_count < 0 or root_count > 256:
        raise InvalidInput("square-root bisection count must be in [0,256]")
    if profile.get("predictor_depth") != 1:
        raise InvalidInput("this implementation supports predictor depth n=1 only")
    if any(profile.get(key) != expected for key, expected in (
        ("parameter_split_depth", 0), ("parameter_leaf_limit", 1),
        ("initial_state_split_depth", 0), ("initial_state_leaf_limit", 1),
        ("time_slab_count", 1), ("integration_panels", 1),
    )):
        raise InvalidInput("this implementation supports one unsplit full-hold state/parameter cell and one integral panel")
    return X, T, V, obstacle, V_max


def _validate_profile(profile: Any) -> Fraction:
    if not isinstance(profile, dict) or not isinstance(profile.get("id"), str):
        raise InvalidInput("resource profile must have a string ID")
    for key in ("max_rational_bits", "max_rational_operations"):
        value = profile.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise InvalidInput(f"{key} must be a positive integer")
    wall = parse_q(profile.get("wall_seconds_per_query"))
    if wall <= 0:
        raise InvalidInput("wall-time cap must be positive")
    return wall


def _evaluate_bounds(
    benchmark: dict[str, Any], state_cell: dict[str, Any], scene: dict[str, Any], horizon: dict[str, Any],
    action: dict[str, Any], profile: dict[str, Any], budget: Budget,
) -> dict[str, Any]:
    X_physical, T, V, obstacles, V_max = _parse_input_query(benchmark, state_cell, scene, horizon, action, profile, budget)
    model = build_model(benchmark, budget)
    scales = model.scales
    internal_indices = [3, 4, 5, 6, 7, 8]
    X_scaled = [X_physical[index] / _point(scales[j], budget) for j, index in enumerate(internal_indices)]
    E, exp_q, exp_remainder = interval_matrix_exponential(model.A, T, profile["exp_taylor_degree"])
    P0, force_minus1, integrand0 = _predictor_level(model, E, X_scaled, X_scaled, V, T)
    P1, force0, integrand1 = _predictor_level(model, E, X_scaled, P0, V, T)

    delta = [(P1[i] - P0[i]).abs_upper() for i in range(6)]
    d_bar = []
    for side_idx, side in enumerate(("L", "R")):
        bound = Fraction(0)
        for j in range(6):
            bound = budget.add(bound, budget.mul(model.QF[side_idx][j].hi, delta[j]))
        cap = budget.mul(Fraction(2), model.parameters[f"C_{side}"].hi)
        d_bar.append(min(bound, cap))

    M_bar, D_bar, N = _bound_model_matrices(model)
    eta_scaled, q_vec, comparison_Q, comparison_tail = _radius_series(
        N, D_bar, d_bar, T, profile["comparison_series_order"], budget
    )
    eta_physical = physical_radius(eta_scaled, scales, budget)
    P1_physical = physical_internal_box(P1, scales)
    P0_physical = physical_internal_box(P0, scales)

    U = max(abs(P1_physical[0].lo), abs(P1_physical[0].hi))
    R = max(abs(P1_physical[1].lo), abs(P1_physical[1].hi))
    E_theta = budget.mul(T, eta_physical[1])
    E_p = budget.mul(T, budget.add(eta_physical[0], budget.mul(U, min(budget.mul(T, eta_physical[1]), Fraction(2)))))

    theta_center = X_physical[2] + Interval(Fraction(0), T, budget) * P1_physical[1]
    cos_theta = interval_cosine(theta_center, profile["trig_taylor_degree"])
    sin_theta = interval_sine(theta_center, profile["trig_taylor_degree"])
    duration = Interval(Fraction(0), T, budget)
    px_center = X_physical[0] + duration * (P1_physical[0] * cos_theta)
    py_center = X_physical[1] + duration * (P1_physical[0] * sin_theta)

    # Contact bounds use the full predictor range and the same parameter-cell label hull.
    slip_tilde = [value / model.parameters["v_s"] for value in matvec(model.S, P1)]
    betas: list[Fraction] = []
    for side_idx, side in enumerate(("L", "R")):
        bphi = _clip_interval(slip_tilde[side_idx]).abs_upper()
        radius_slip = Fraction(0)
        for j in range(6):
            radius_slip = budget.add(radius_slip, budget.mul(model.S[side_idx][j].abs_upper(), eta_scaled[j]))
        slope = budget.div(Fraction(1), model.parameters["v_s"].lo)
        beta = min(Fraction(1), budget.add(bphi, budget.mul(slope, radius_slip)))
        betas.append(beta)
    reserves = []
    root_brackets = []
    for side_idx, side in enumerate(("L", "R")):
        radicand = budget.add(Fraction(1), -budget.mul(betas[side_idx], betas[side_idx]))
        root_lo, root_hi = sqrt_lower(radicand, profile["sqrt_bisections"], budget)
        root_brackets.append([root_lo, root_hi])
        reserves.append(budget.mul(model.parameters[f"C_{side}"].lo, root_lo))
    contact_available = budget.add(reserves[0], reserves[1])
    demand_u = budget.add(U, eta_physical[0])
    demand_r = budget.add(R, eta_physical[1])
    contact_demand = budget.mul(model.parameters["m"].hi, budget.mul(demand_u, demand_r))
    contact_margin = budget.add(contact_available, -contact_demand)

    collision = []
    for obstacle in obstacles:
        ox, oy = obstacle["p_o"]
        dx = max(Fraction(0), budget.add(px_center.lo, -ox), budget.add(ox, -px_center.hi))
        dy = max(Fraction(0), budget.add(py_center.lo, -oy), budget.add(oy, -py_center.hi))
        squared_distance = budget.add(budget.mul(dx, dx), budget.mul(dy, dy))
        distance_lo, distance_hi = sqrt_lower(squared_distance, profile["sqrt_bisections"], budget)
        margin = budget.add(budget.add(distance_lo, -obstacle["R_s"]), -E_p)
        collision.append({
            "obstacle_id": obstacle["id"], "distance_lower": distance_lo,
            "distance_upper_bracket": distance_hi, "margin_lower": margin,
        })

    full_internal_width = [budget.add(budget.add(P1_physical[i].hi, -P1_physical[i].lo), budget.mul(Fraction(2), eta_physical[i])) for i in range(6)]
    pose_width = [
        budget.add(budget.add(px_center.hi, -px_center.lo), budget.mul(Fraction(2), E_p)),
        budget.add(budget.add(py_center.hi, -py_center.lo), budget.mul(Fraction(2), E_p)),
        budget.add(budget.add(theta_center.hi, -theta_center.lo), budget.mul(Fraction(2), E_theta)),
    ]
    return {
        "model": model,
        "T": T, "V": V, "X_physical": X_physical, "X_scaled": X_scaled,
        "E": E, "exp_q": exp_q, "exp_remainder": exp_remainder,
        "P0": P0, "P1": P1, "force_minus1": force_minus1, "force0": force0,
        "integrand0": integrand0, "integrand1": integrand1,
        "delta_abs": delta, "d_bar": d_bar, "M_bar": M_bar, "D_bar": D_bar, "N": N,
        "q_vec": q_vec, "comparison_Q": comparison_Q, "comparison_tail": comparison_tail,
        "eta_scaled": eta_scaled, "eta_physical": eta_physical,
        "U": U, "R": R, "E_theta": E_theta, "E_p": E_p,
        "theta_center": theta_center, "px_center": px_center, "py_center": py_center,
        "betas": betas, "root_brackets": root_brackets,
        "contact_available": contact_available, "contact_demand": contact_demand,
        "contact_margin": contact_margin, "collision": collision,
        "full_internal_width": full_internal_width, "pose_width": pose_width,
        "exp_remainder_order": profile["exp_taylor_degree"] + 1,
    }


def _proof_json(result: dict[str, Any]) -> dict[str, Any]:
    model: ModelIntervals = result["model"]
    coefficient_blocks = [model.A, model.B, model.D, model.S, model.QF]
    nonpoint_coefficient_intervals = sum(
        value.lo != value.hi for block in coefficient_blocks for row in block for value in row
    )
    return {
        "parameter_label_order": model.parameter_label_order,
        "parameter_label_cell": {name: value.to_json() for name, value in model.parameter_label_box.items()},
        "fixed_parameter_label_count": len(model.parameter_label_order),
        "nonpoint_coefficient_interval_entries": nonpoint_coefficient_intervals,
        "parameter_intervals": {name: value.to_json() for name, value in model.parameters.items()},
        "A_scaled": [[value.to_json() for value in row] for row in model.A],
        "B_scaled": [[value.to_json() for value in row] for row in model.B],
        "D_scaled": [[value.to_json() for value in row] for row in model.D],
        "S_scaled": [[value.to_json() for value in row] for row in model.S],
        "QF_scaled": [[value.to_json() for value in row] for row in model.QF],
        "internal_initial_scaled": [value.to_json() for value in result["X_scaled"]],
        "exp_range": [[value.to_json() for value in row] for row in result["E"]],
        "exp_norm_bound": qobj(result["exp_q"]),
        "exp_remainder": qobj(result["exp_remainder"]),
        "P0_scaled": [value.to_json() for value in result["P0"]],
        "P1_scaled": [value.to_json() for value in result["P1"]],
        "force_at_initial_predictor": [value.to_json() for value in result["force_minus1"]],
        "force_at_P0": [value.to_json() for value in result["force0"]],
        "delta_abs_scaled": [qobj(x) for x in result["delta_abs"]],
        "residual_force_upper": [qobj(x) for x in result["d_bar"]],
        "M_upper": [[qobj(x) for x in row] for row in result["M_bar"]],
        "D_abs_upper": [[qobj(x) for x in row] for row in result["D_bar"]],
        "N_nonnegative_majorant": [[qobj(x) for x in row] for row in result["N"]],
        "comparison_forcing": [qobj(x) for x in result["q_vec"]],
        "comparison_Q": qobj(result["comparison_Q"]),
        "comparison_tail": qobj(result["comparison_tail"]),
        "eta_scaled": [qobj(x) for x in result["eta_scaled"]],
        "eta_physical": [qobj(x) for x in result["eta_physical"]],
        "center_heading_range": result["theta_center"].to_json(),
        "center_position_x_range": result["px_center"].to_json(),
        "center_position_y_range": result["py_center"].to_json(),
        "E_theta": qobj(result["E_theta"]),
        "E_p": qobj(result["E_p"]),
        "beta_upper": [qobj(x) for x in result["betas"]],
        "sqrt_lower_upper_brackets": [[qobj(lo), qobj(hi)] for lo, hi in result["root_brackets"]],
        "contact_available_lower": qobj(result["contact_available"]),
        "contact_demand_upper": qobj(result["contact_demand"]),
        "contact_margin_lower": qobj(result["contact_margin"]),
        "collision": [{
            "obstacle_id": x["obstacle_id"],
            "distance_lower": qobj(x["distance_lower"]),
            "distance_upper_bracket": qobj(x["distance_upper_bracket"]),
            "margin_lower": qobj(x["margin_lower"]),
        } for x in result["collision"]],
    }


def make_query(
    benchmark: dict[str, Any], query_id: str, profile: dict[str, Any],
    development_manifest_sha256: str, benchmark_sha256: str,
) -> dict[str, Any]:
    parts = query_id.split("__")
    if len(parts) != 4:
        raise InvalidInput("malformed original query id")
    state_id, scene_id, horizon_id, action_id = parts
    state = next((x for x in benchmark["state_cells"] if x["id"] == state_id), None)
    scene = next((x for x in benchmark["scenes"] if x["id"] == scene_id), None)
    horizon = next((x for x in benchmark["horizons"] if x["id"] == horizon_id), None)
    action = next((x for x in benchmark["actions"] if x["id"] == action_id), None)
    if any(x is None for x in (state, scene, horizon, action)):
        raise InvalidInput("query ID does not map to a declared benchmark row")
    return {
        "query_id": query_id, "state_cell": state, "scene": scene, "horizon": horizon,
        "action": action, "parameter_cell": benchmark["parameter_cell"], "profile": profile,
        "benchmark": benchmark,
        "benchmark_sha256": benchmark_sha256,
        "development_manifest_sha256": development_manifest_sha256,
    }


def run_query(query: dict[str, Any], source_commit: str) -> dict[str, Any]:
    started = time.monotonic()
    profile = query.get("profile", {})
    try:
        wall = _validate_profile(profile)
        budget = Budget(profile["max_rational_bits"], profile["max_rational_operations"], wall)
    except InvalidInput as exc:
        return {
            "schema": "ddwmr-g2-record-v1", "query_id": query.get("query_id"),
            "source_revision": source_commit, "status": "INVALID_INPUT",
            "reason_codes": ["INVALID_RESOURCE_PROFILE"], "reason": str(exc),
            "review_status": "PENDING_INDEPENDENT_AUDIT",
            "elapsed_seconds_display_only": round(time.monotonic() - started, 6),
        }
    base = {
        "schema": "ddwmr-g2-record-v1", "query_id": query["query_id"],
        "method_id": "G2_COMP_CLIP_WHOLE_HOLD_INTERVAL_HULL_N1_V1",
        "source_revision": source_commit,
        "benchmark_sha256": query["benchmark_sha256"],
        "development_manifest_sha256": query["development_manifest_sha256"],
        "profile_id": profile["id"],
        "input_sha256": canonical_hash({
            "query_id": query["query_id"], "state_cell": query["state_cell"],
            "scene": query["scene"], "horizon": query["horizon"], "action": query["action"],
            "parameter_cell": query["parameter_cell"], "profile": profile,
        }),
        "state_cell_id": query["state_cell"]["id"], "scene_id": query["scene"]["id"],
        "horizon_id": query["horizon"]["id"], "action_id": query["action"]["id"],
        "held_voltage": query["action"]["V"], "horizon": query["horizon"]["T"],
        "parameter_cell_id": query["parameter_cell"]["id"],
        "quantifiers": {
            "one_common_voltage_for_all_initial_states_and_labels": True,
            "initial_state_cell_universal": True,
            "parameter_labels_fixed_for_entire_hold": True,
            "time_coverage": "closed [0,T] by whole-hold ranges",
            "coefficient_representation": "named outer interval hull; interval arithmetic may forget rational-map correlations but does not resample a physical label",
            "endpoint_target_requested": False,
        },
        "review_status": "PENDING_INDEPENDENT_AUDIT",
    }
    try:
        result = _evaluate_bounds(query["benchmark"], query["state_cell"], query["scene"], query["horizon"], query["action"], profile, budget)
        certified = result["contact_margin"] >= 0 and all(x["margin_lower"] >= 0 for x in result["collision"])
        reasons = []
        if result["contact_margin"] < 0:
            reasons.append("CONTACT_SUFFICIENT_MARGIN_NEGATIVE")
        if any(x["margin_lower"] < 0 for x in result["collision"]):
            reasons.append("COLLISION_SUFFICIENT_MARGIN_NEGATIVE")
        record = {
            **base,
            "status": "CERTIFIED" if certified else "UNKNOWN",
            "reason_codes": reasons,
            "obstacle_count": len(result["collision"]),
            "collision_margin_lower": [qobj(x["margin_lower"]) for x in result["collision"]],
            "contact_margin_lower": qobj(result["contact_margin"]),
            "center_width_internal_physical": [qobj(budget.add(x.hi, -x.lo)) for x in physical_internal_box(result["P1"], result["model"].scales)],
            "error_radius_internal_physical": [qobj(x) for x in result["eta_physical"]],
            "total_width_internal_physical": [qobj(x) for x in result["full_internal_width"]],
            "center_width_pose": [qobj(budget.add(x.hi, -x.lo)) for x in [result["px_center"], result["py_center"], result["theta_center"]]],
            "error_radius_pose": [qobj(result["E_p"]), qobj(result["E_p"]), qobj(result["E_theta"])],
            "total_width_pose": [qobj(x) for x in result["pose_width"]],
            "work": {
                "rational_operations": budget.operations,
                "max_rational_bits": budget.max_seen_bits,
                "parameter_leaves": 1, "initial_state_leaves": 1,
                "time_slabs": profile["time_slab_count"], "whole_hold_hull_reused_on_slabs": profile["time_slab_count"] > 1,
                "exp_degree": profile["exp_taylor_degree"], "trig_degree": profile["trig_taylor_degree"],
                "comparison_order": profile["comparison_series_order"],
                "sqrt_bisections": profile["sqrt_bisections"],
            },
            "elapsed_seconds_display_only": round(time.monotonic() - started, 6),
            "proof": _proof_json(result),
        }
        return record
    except ResourceLimit as exc:
        return {
            **base, "status": "UNKNOWN", "reason_codes": [exc.kind], "reason": exc.detail,
            "work": {"rational_operations": budget.operations, "max_rational_bits": budget.max_seen_bits},
            "elapsed_seconds_display_only": round(time.monotonic() - started, 6),
        }
    except InvalidInput as exc:
        return {
            **base, "status": "INVALID_INPUT", "reason_codes": ["INVALID_EFFECTIVE_INPUT"], "reason": str(exc),
            "work": {"rational_operations": budget.operations, "max_rational_bits": budget.max_seen_bits},
            "elapsed_seconds_display_only": round(time.monotonic() - started, 6),
        }
    except Exception as exc:  # Failures are not recast as mathematical UNKNOWN.
        return {
            **base, "status": "EXECUTION_FAILURE", "reason_codes": ["UNEXPECTED_EXCEPTION"],
            "reason": f"{type(exc).__name__}: {exc}",
            "work": {"rational_operations": budget.operations, "max_rational_bits": budget.max_seen_bits},
            "elapsed_seconds_display_only": round(time.monotonic() - started, 6),
        }


def evaluate_and_record(query: dict[str, Any], source_commit: str) -> dict[str, Any]:
    return run_query(query, source_commit)
