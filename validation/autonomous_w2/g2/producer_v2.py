"""W2 G2 source-local producer for the signed VOF clip-interior subclass.

No R3, R10, R11, R17, G4, native-query, or controller code is imported.
The method is an exact-rational interval outer enclosure, not floating-point
simulation. A full-hold clip-interior proof is required before the affine
branch enclosure is interpreted as a MASTER trajectory enclosure.
"""
from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

from .rational_interval_v2 import ArithmeticLimit, Budget, I, activate, configure_integer_string_limit, q, qs, sqrt_lower


ROOT = Path(__file__).resolve().parents[3]
STATE_ORDER = ["p_x", "p_y", "theta", "u", "r", "omega_L", "omega_R", "i_L", "i_R"]
LABEL_ORDER = ["rho_L", "rho_R", "C_L", "C_R", "lambda_L", "lambda_R", "R_L", "R_R", "B_L", "B_R", "k_L", "k_R"]
INTERNAL_ORDER = ["u", "r", "omega_L", "omega_R", "i_L", "i_R"]


class InvalidInput(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def parse_protocol(protocol: dict[str, Any]) -> tuple[list[I], dict[str, I], list[dict[str, Any]], Fraction]:
    if protocol.get("protocol_id") != "G2_W2_VOF_TASK_V1":
        raise InvalidInput("UNSUPPORTED_PROTOCOL_ID")
    if protocol.get("protocol_state") != "FROZEN_FOR_DEVELOPMENT_NOT_CONFIRMATION":
        raise InvalidInput("PROTOCOL_STATE_MISMATCH")
    model = protocol.get("model", {})
    if model.get("formulation") != "MASTER v2.1 reduced nine-state DDWMR" or model.get("phi") != "clip(s,-1,1)":
        raise InvalidInput("UNSUPPORTED_MODEL_OR_LAW")
    if model.get("lipschitz_constant") != "1":
        raise InvalidInput("CLIP_LIPSCHITZ_BINDING_MISMATCH")
    if model.get("fixed_label_order") != LABEL_ORDER:
        raise InvalidInput("FIXED_LABEL_ORDER_MISMATCH")
    constants = model.get("fixed_constants", {})
    required_constants = {"m", "I_z", "R_w", "b", "v_s", "c_u", "c_r", "V_max"}
    if set(constants) != required_constants or any(q(constants[k]) != 1 for k in required_constants):
        raise InvalidInput("FIXED_CONSTANT_MAP_MISMATCH")
    fixed_bounds = model.get("fixed_label_bounds")
    if fixed_bounds != ["9999/10000", "10001/10000"]:
        raise InvalidInput("FIXED_LABEL_BOUNDS_MISMATCH")
    lo, hi = q(fixed_bounds[0]), q(fixed_bounds[1])
    if lo <= 0 or lo >= hi:
        raise InvalidInput("LABEL_DOMAIN_NOT_POSITIVE_WIDTH_POSITIVE")
    labels = {name: I(lo, hi) for name in LABEL_ORDER}
    for name, interval in labels.items():
        if interval.lo <= 0 or interval.lo >= interval.hi:
            raise InvalidInput(f"LABEL_DOMAIN_INVALID:{name}")
    if model.get("parameter_maps") != {"J_j": "1/rho_j", "L_j": "lambda_j"}:
        raise InvalidInput("PARAMETER_IMAGE_MAP_MISMATCH")
    if labels["lambda_L"].lo <= 0 or labels["lambda_R"].lo <= 0:
        raise InvalidInput("INDUCTANCE_NOT_POSITIVE")
    # Check the declared ideal gear witness for all labels by exact endpoint inequalities.
    # J_motor=(1/rho-1/10)/100 is positive because 1/rho >= 10000/10001 > 1/10.
    rho_hi = labels["rho_L"].hi
    if 1 / rho_hi <= Fraction(1, 10):
        raise InvalidInput("GEAR_WITNESS_MOTOR_INERTIA_NOT_POSITIVE")
    if model.get("parameter_maps", {}).get("J_j") != "1/rho_j":
        raise InvalidInput("RECIPROCAL_INERTIA_MAP_MISMATCH")

    task = protocol.get("task", {})
    if task.get("initial_box_state_order") != STATE_ORDER:
        raise InvalidInput("STATE_ORDER_MISMATCH")
    raw_box = task.get("initial_box")
    if not isinstance(raw_box, list) or len(raw_box) != 9:
        raise InvalidInput("INITIAL_BOX_DIMENSION")
    state = [I(q(pair[0]), q(pair[1])) for pair in raw_box]
    if any(cell.lo >= cell.hi for cell in state):
        raise InvalidInput("INITIAL_BOX_NOT_POSITIVE_WIDTH")
    if state[3].lo <= 0:
        raise InvalidInput("INITIAL_BODY_SPEED_NOT_STRICTLY_FORWARD")
    hold = q(task.get("hold_s"))
    if hold != 2:
        raise InvalidInput("HOLD_DURATION_MISMATCH")
    if q(task.get("required_progress_m")) != Fraction(7, 20):
        raise InvalidInput("TASK_THRESHOLD_MISMATCH")
    obstacle = task.get("obstacle", {})
    if obstacle.get("kind") != "static_circle":
        raise InvalidInput("UNSUPPORTED_OBSTACLE")
    if len(obstacle.get("center_m", [])) != 2 or q(obstacle.get("inflated_radius_m")) <= 0:
        raise InvalidInput("INVALID_OBSTACLE_GEOMETRY")
    actions = protocol.get("actions")
    expected = [
        ("W2_G2_DEV_001_ZERO", "zero", ["0", "0"]),
        ("W2_G2_DEV_001_NOMINAL", "nominal", ["1/2", "1/2"]),
        ("W2_G2_DEV_001_ALTERNATIVE", "alternative", ["1", "1"]),
    ]
    if not isinstance(actions, list) or len(actions) != 3:
        raise InvalidInput("ACTION_COUNT_MISMATCH")
    for item, want in zip(actions, expected):
        if (item.get("id"), item.get("role"), item.get("voltage")) != want:
            raise InvalidInput("ACTION_SET_MISMATCH")
        if any(abs(q(v)) > q(constants["V_max"]) for v in item["voltage"]):
            raise InvalidInput("VOLTAGE_LIMIT_EXCEEDED")
    return state, labels, actions, hold


def build_augmented_matrix(labels: dict[str, I], voltage: tuple[Fraction, Fraction]) -> list[list[I]]:
    """Build the signed 7x7 affine matrix directly from MASTER §§7–11."""
    zero, one = I.point(0), I.point(1)
    m = iz = rw = b = vs = cu = cr = one
    rho_l, rho_r = labels["rho_L"], labels["rho_R"]
    c_l, c_r = labels["C_L"], labels["C_R"]
    lam_l, lam_r = labels["lambda_L"], labels["lambda_R"]
    r_l, r_r = labels["R_L"], labels["R_R"]
    b_l, b_r = labels["B_L"], labels["B_R"]
    k_l, k_r = labels["k_L"], labels["k_R"]
    alpha_l, alpha_r = c_l / vs, c_r / vs
    a = [[zero for _ in range(7)] for _ in range(7)]

    # Body translation: m*u_dot=F_L+F_R-c_u*u.
    a[0][0] = -(cu / m) - (alpha_l + alpha_r) / m
    a[0][1] = (b * (alpha_l - alpha_r)) / m
    a[0][2] = (rw * alpha_l) / m
    a[0][3] = (rw * alpha_r) / m

    # Body yaw: I_z*r_dot=b*(F_R-F_L)-c_r*r.
    a[1][0] = (b * (alpha_l - alpha_r)) / iz
    a[1][1] = -(cr / iz) - (b * b * (alpha_l + alpha_r)) / iz
    a[1][2] = -(b * rw * alpha_l) / iz
    a[1][3] = (b * rw * alpha_r) / iz

    # Wheel dynamics use 1/J_j=rho_j; contact force enters with -R_w*F_j.
    a[2][0] = rho_l * rw * alpha_l
    a[2][1] = -(rho_l * rw * alpha_l * b)
    a[2][2] = -(rho_l * b_l) - rho_l * rw * rw * alpha_l
    a[2][4] = rho_l * k_l

    a[3][0] = rho_r * rw * alpha_r
    a[3][1] = rho_r * rw * alpha_r * b
    a[3][3] = -(rho_r * b_r) - rho_r * rw * rw * alpha_r
    a[3][5] = rho_r * k_r

    # Winding equations: L_j*i_dot=V_j-R_j*i_j-k_j*omega_j.
    a[4][2] = -(k_l / lam_l)
    a[4][4] = -(r_l / lam_l)
    a[4][6] = I.point(voltage[0]) / lam_l
    a[5][3] = -(k_r / lam_r)
    a[5][5] = -(r_r / lam_r)
    a[5][6] = I.point(voltage[1]) / lam_r
    # Final coordinate is the affine constant 1; its derivative is exactly zero.
    a[6][6] = zero
    return a


def _matvec(matrix: list[list[I]], vector: list[I]) -> list[I]:
    out: list[I] = []
    for row in matrix:
        total = I.point(0)
        for aij, vj in zip(row, vector):
            total = total + aij * vj
        out.append(total)
    return out


def _matrix_norm_inf(matrix: list[list[I]]) -> Fraction:
    return max(sum((entry.abs_upper() for entry in row), Fraction(0)) for row in matrix)


def _vector_norm_inf(vector: list[I]) -> Fraction:
    return max((entry.abs_upper() for entry in vector), default=Fraction(0))


def exp_range(
    matrix: list[list[I]], vector: list[I], h: Fraction, degree: int, *, partial: bool,
) -> tuple[list[I], dict[str, str]]:
    """Enclose exp(A*tau)y for tau in [0,h] (partial) or tau=h (endpoint)."""
    qnorm = _matrix_norm_inf(matrix) * h
    if qnorm < 0 or qnorm / (degree + 2) >= 1:
        raise ArithmeticLimit("EXPONENTIAL_TAIL_RATIO_NOT_CONTRACTIVE")
    if qnorm == 0:
        tail = Fraction(0)
    else:
        tail = (qnorm ** (degree + 1)) / math.factorial(degree + 1)
        tail /= (1 - qnorm / (degree + 2))
    radius = tail * _vector_norm_inf(vector)
    current = vector
    result = [I.point(0) for _ in vector]
    h_power = Fraction(1)
    for order in range(degree + 1):
        if partial and order > 0:
            time_power = I(Fraction(0), h_power)
        else:
            time_power = I.point(h_power)
        divisor = math.factorial(order)
        for idx, value in enumerate(current):
            result[idx] = result[idx] + value * time_power / divisor
        current = _matvec(matrix, current)
        h_power *= h
    for idx in range(len(result) - 1):
        result[idx] = result[idx] + I(-radius, radius)
    # The final augmented coordinate has zero derivative and is exactly constant.
    diagnostics = {
        "q_norm_upper": qs(qnorm),
        "tail_norm_upper": qs(tail),
        "remainder_inf_upper": qs(radius),
        "degree": str(degree),
        "time_mode": "partial_[0,h]" if partial else "endpoint_h",
    }
    return result, diagnostics


def _position_gap(interval: I, obstacle: Fraction) -> Fraction:
    if obstacle < interval.lo:
        return interval.lo - obstacle
    if obstacle > interval.hi:
        return obstacle - interval.hi
    return Fraction(0)


def _sin_outer(theta: I) -> I:
    extent = theta.abs_upper()
    return I(-extent, extent)


def _cos_lower(theta: I) -> Fraction:
    extent = theta.abs_upper()
    # cos(x) >= 1-x^2/2 globally; outward exact rational lower bound.
    return 1 - extent * extent / 2


def _certificate_status(slabs: list[dict[str, Any]], branch_ok: bool) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if not branch_ok:
        reasons.append("CLIP_INTERIOR_NOT_ESTABLISHED_ON_EVERY_SLAB")
    if any(q(s["collision_margin_lower"]) < 0 for s in slabs):
        reasons.append("COLLISION_MARGIN_NEGATIVE_ON_A_SLAB")
    if any(q(s["contact_margin_lower"]) < 0 for s in slabs):
        reasons.append("CONTACT_MARGIN_NEGATIVE_ON_A_SLAB")
    return not reasons, reasons


def evaluate(protocol: dict[str, Any], profile: dict[str, Any], action: dict[str, Any], protocol_sha: str, profile_sha: str) -> dict[str, Any]:
    state, labels, _, hold = parse_protocol(protocol)
    voltage = (q(action["voltage"][0]), q(action["voltage"][1]))
    obstacle_raw = protocol["task"]["obstacle"]
    ox, oy = (q(v) for v in obstacle_raw["center_m"])
    rs = q(obstacle_raw["inflated_radius_m"])
    threshold = q(protocol["task"]["required_progress_m"])
    slabs_n = int(profile["time_slabs"])
    degree = int(profile["matrix_taylor_degree"])
    sqrt_bits = int(profile["sqrt_bisections"])
    if slabs_n <= 0 or hold * int(1) / slabs_n <= 0:
        raise InvalidInput("INVALID_TIME_PARTITION")
    h = hold / slabs_n
    if q(profile["slab_duration_s"]) != h:
        raise InvalidInput("PROFILE_HOLD_PARTITION_MISMATCH")
    matrix = build_augmented_matrix(labels, voltage)
    label_image_hash = canonical_sha256({"order": LABEL_ORDER, "bounds": ["9999/10000", "10001/10000"], "maps": protocol["model"]["parameter_maps"]})
    # z starts from the exact same initial box for every hidden label; pose is carried separately.
    z_start = state[3:9] + [I.point(1)]
    theta_start, px_start, py_start = state[2], state[0], state[1]
    progress = I.point(0)
    slab_records: list[dict[str, Any]] = []
    branch_ok = True
    for slab_index in range(slabs_n):
        t0 = slab_index * h
        t1 = (slab_index + 1) * h
        z_partial, part_diag = exp_range(matrix, z_start, h, degree, partial=True)
        z_endpoint, end_diag = exp_range(matrix, z_start, h, degree, partial=False)
        z_ranges = z_partial[:6]
        u_rng, r_rng, w_l_rng, w_r_rng, i_l_rng, i_r_rng = z_ranges
        # Fixed synthetic R_w=b=v_s=1. These are the true normalized slips.
        slip_l = w_l_rng - u_rng + r_rng
        slip_r = w_r_rng - u_rng - r_rng
        beta_l, beta_r = slip_l.abs_upper(), slip_r.abs_upper()
        slab_branch = beta_l < 1 and beta_r < 1
        branch_ok = branch_ok and slab_branch
        branch_slack_l, branch_slack_r = 1 - beta_l, 1 - beta_r
        reserve_l = q(protocol["model"]["fixed_label_bounds"][0]) * sqrt_lower(max(Fraction(0), 1 - beta_l * beta_l), sqrt_bits) if beta_l <= 1 else Fraction(0)
        reserve_r = q(protocol["model"]["fixed_label_bounds"][0]) * sqrt_lower(max(Fraction(0), 1 - beta_r * beta_r), sqrt_bits) if beta_r <= 1 else Fraction(0)
        demand = u_rng.abs_upper() * r_rng.abs_upper()
        contact_margin = reserve_l + reserve_r - demand

        theta_rng = theta_start + I(Fraction(0), h) * r_rng
        cos_rng = I(_cos_lower(theta_rng), Fraction(1))
        sin_rng = _sin_outer(theta_rng)
        xdot_rng = u_rng * cos_rng
        ydot_rng = u_rng * sin_rng
        p_x_slab = px_start + I(Fraction(0), h) * xdot_rng
        p_y_slab = py_start + I(Fraction(0), h) * ydot_rng
        p_x_end = px_start + I.point(h) * xdot_rng
        p_y_end = py_start + I.point(h) * ydot_rng
        theta_end = theta_start + I.point(h) * r_rng

        dx_gap = _position_gap(p_x_slab, ox)
        dy_gap = _position_gap(p_y_slab, oy)
        distance_sq_lower = dx_gap * dx_gap + dy_gap * dy_gap
        distance_lower = sqrt_lower(distance_sq_lower, sqrt_bits)
        collision_margin = distance_lower - rs
        progress_increment = I.point(h) * xdot_rng
        progress = progress + progress_increment

        slab_records.append({
            "index": slab_index,
            "start_s": qs(t0),
            "end_s": qs(t1),
            "duration_s": qs(h),
            "label_image_sha256": label_image_hash,
            "matrix_augmented": [[entry.to_json() for entry in row] for row in matrix],
            "internal_state_range": {name: z_ranges[idx].to_json() for idx, name in enumerate(INTERNAL_ORDER)},
            "internal_endpoint_range": {name: z_endpoint[idx].to_json() for idx, name in enumerate(INTERNAL_ORDER)},
            "slip_normalized_range": {"L": slip_l.to_json(), "R": slip_r.to_json()},
            "clip_interior": {"proved_strict": slab_branch, "beta_upper": [qs(beta_l), qs(beta_r)], "slack_lower": [qs(branch_slack_l), qs(branch_slack_r)]},
            "contact": {"reserve_lower_N": qs(reserve_l + reserve_r), "reserve_wheel_lower_N": [qs(reserve_l), qs(reserve_r)], "demand_upper_N": qs(demand), "margin_lower_N": qs(contact_margin)},
            "heading_range_rad": theta_rng.to_json(),
            "position_range_m": {"p_x": p_x_slab.to_json(), "p_y": p_y_slab.to_json()},
            "position_endpoint_m": {"p_x": p_x_end.to_json(), "p_y": p_y_end.to_json()},
            "collision": {"coordinate_gaps_lower_m": [qs(dx_gap), qs(dy_gap)], "distance_squared_lower_m2": qs(distance_sq_lower), "distance_lower_m": qs(distance_lower), "radius_m": qs(rs), "margin_lower_m": qs(collision_margin)},
            "progress_increment_range_m": progress_increment.to_json(),
            "partial_taylor": part_diag,
            "endpoint_taylor": end_diag,
        })
        z_start = z_endpoint
        theta_start, px_start, py_start = theta_end, p_x_end, p_y_end

    safety_ok, reasons = _certificate_status(slab_records, branch_ok)
    task_eligible = safety_ok and progress.lo >= threshold
    if safety_ok and progress.lo < threshold:
        reasons.append("PROGRESS_LOWER_BELOW_TASK_THRESHOLD")
    return {
        "schema": "G2_W2_VOF_ROW_v2",
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": protocol_sha,
        "profile_id": profile["profile_id"],
        "profile_sha256": profile_sha,
        "action_id": action["id"],
        "action_role": action["role"],
        "held_voltage_V": [qs(voltage[0]), qs(voltage[1])],
        "parameter_label_order": LABEL_ORDER,
        "parameter_label_bounds": ["9999/10000", "10001/10000"],
        "parameter_image_sha256": label_image_hash,
        "hold_s": qs(hold),
        "time_coverage": {"slab_count": slabs_n, "covered_start_s": "0/1", "covered_end_s": qs(hold), "contiguous": True, "fixed_label_carried": True, "held_voltage_constant": True},
        "safety_status": "CERTIFIED" if safety_ok else "UNKNOWN",
        "task_eligible": task_eligible,
        "reason_codes": reasons,
        "collision_margin_lower_min_m": qs(min(q(s["collision"]["margin_lower_m"]) for s in slab_records)),
        "contact_margin_lower_min_N": qs(min(q(s["contact"]["margin_lower_N"]) for s in slab_records)),
        "progress_enclosure_m": progress.to_json(),
        "required_progress_m": qs(threshold),
        "slabs": slab_records,
        "arithmetic": {},
    }


def evaluate_bound_row(binding: dict[str, Any], action_id: str) -> dict[str, Any]:
    protocol_path = ROOT / binding["protocol_path"]
    profile_path = ROOT / binding["profile_path"]
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    configure_integer_string_limit(int(profile["python_int_string_digit_cap"]), int(profile["rational_bit_cap"]))
    if sha256_file(protocol_path) != binding["protocol_sha256"] or sha256_file(profile_path) != binding["profile_sha256"]:
        raise InvalidInput("FROZEN_INPUT_HASH_MISMATCH")
    for relpath, expected in binding["source_files"].items():
        if sha256_file(ROOT / relpath) != expected:
            raise InvalidInput(f"SOURCE_HASH_MISMATCH:{relpath}")
    budget = Budget(int(profile["interval_operation_cap"]), int(profile["rational_bit_cap"]))
    activate(budget)
    try:
        matches = [action for action in protocol["actions"] if action["id"] == action_id]
        if len(matches) != 1:
            raise InvalidInput("ACTION_ID_NOT_UNIQUE_OR_UNKNOWN")
        record = evaluate(protocol, profile, matches[0], binding["protocol_sha256"], binding["profile_sha256"])
        record["arithmetic"] = {"interval_operations": budget.operations, "max_rational_bits": budget.max_observed_bits, "operation_cap": budget.max_operations, "bit_cap": budget.max_bits}
        record["binding_sha256"] = sha256_file(ROOT / binding["binding_path"])
        return record
    finally:
        activate(None)
