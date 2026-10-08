"""Independent stdlib Fraction audit of the released G2 v6 bound equations.

This script imports no G2 producer, checker, or interval library. It rederives
the parameter-matrix bounds and center Taylor ranges from the frozen protocol,
then checks saved proof fields by exact rational inequalities.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
RELEASE_SHA256 = "789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55"
PROTOCOL_REL = "research/autonomous_w2/g2/task_protocol_v1.json"
PROFILE_REL = "validation/autonomous_w2/g2/profile_centered_v6.json"
ROWS = (
    (
        "zero",
        "results/validation/autonomous_w2/g2/development_centered_v6/attempt_01_W2_G2_DEV_001_ZERO/row.json",
    ),
    (
        "nominal",
        "results/validation/autonomous_w2/g2/development_centered_v6/attempt_02_W2_G2_DEV_001_NOMINAL/row.json",
    ),
    (
        "alternative",
        "results/validation/autonomous_w2/g2/development_centered_v6/attempt_03_W2_G2_DEV_001_ALTERNATIVE/row.json",
    ),
)
GRID_BITS = 96


def root_file(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError(f"PATH_ESCAPES_REPO:{relative}")
    return path


def load(relative: str) -> Any:
    return json.loads(root_file(relative).read_text(encoding="utf-8"))


def q(value: Any) -> F:
    return F(str(value))


def floor_grid(value: F, bits: int) -> F:
    scale = 1 << bits
    return F((value.numerator * scale) // value.denominator, scale)


def ceil_grid(value: F, bits: int) -> F:
    scale = 1 << bits
    return F(-((-value.numerator * scale) // value.denominator), scale)


@dataclass(frozen=True)
class I:
    lo: F
    hi: F

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError("REVERSED_INTERVAL")
        scale = 1 << GRID_BITS
        low_numerator = self.lo.numerator * scale
        high_numerator = self.hi.numerator * scale
        rounded_lo = F(low_numerator // self.lo.denominator, scale)
        rounded_hi = F(-((-high_numerator) // self.hi.denominator), scale)
        object.__setattr__(self, "lo", rounded_lo)
        object.__setattr__(self, "hi", rounded_hi)

    @staticmethod
    def point(value: F) -> "I":
        return I(value, value)

    def __add__(self, other: "I") -> "I":
        return I(self.lo + other.lo, self.hi + other.hi)

    def __neg__(self) -> "I":
        return I(-self.hi, -self.lo)

    def __sub__(self, other: "I") -> "I":
        return self + (-other)

    def __mul__(self, other: "I") -> "I":
        values = (self.lo * other.lo, self.lo * other.hi, self.hi * other.lo, self.hi * other.hi)
        return I(min(values), max(values))

    def __truediv__(self, value: int | F) -> "I":
        value = F(value)
        if value == 0:
            raise ZeroDivisionError
        return self * I.point(1 / value)

    def divided_by(self, other: "I") -> "I":
        if other.lo <= 0 <= other.hi:
            raise ZeroDivisionError("INTERVAL_DIVISOR_CONTAINS_ZERO")
        reciprocal = I(min(1 / other.lo, 1 / other.hi), max(1 / other.lo, 1 / other.hi))
        return self * reciprocal

    def abs_upper(self) -> F:
        return max(abs(self.lo), abs(self.hi))


def interval_matrix(labels: dict[str, I], voltage: tuple[F, F]) -> list[list[I]]:
    z, o = I.point(F(0)), I.point(F(1))
    rl, rr = labels["rho_L"], labels["rho_R"]
    cl, cr = labels["C_L"], labels["C_R"]
    ll, lr = labels["lambda_L"], labels["lambda_R"]
    r_l, r_r = labels["R_L"], labels["R_R"]
    b_l, b_r = labels["B_L"], labels["B_R"]
    k_l, k_r = labels["k_L"], labels["k_R"]
    a = [[z for _ in range(7)] for _ in range(7)]
    a[0][0] = -o - cl - cr
    a[0][1] = cl - cr
    a[0][2], a[0][3] = cl, cr
    a[1][0] = cl - cr
    a[1][1] = -o - cl - cr
    a[1][2], a[1][3] = -cl, cr
    a[2][0], a[2][1] = rl * cl, -(rl * cl)
    a[2][2], a[2][4] = -(rl * b_l) - (rl * cl), rl * k_l
    a[3][0], a[3][1] = rr * cr, rr * cr
    a[3][3], a[3][5] = -(rr * b_r) - (rr * cr), rr * k_r
    a[4][2], a[4][4] = -(k_l.divided_by(ll)), -(r_l.divided_by(ll))
    a[4][6] = I.point(voltage[0]).divided_by(ll)
    a[5][3], a[5][5] = -(k_r.divided_by(lr)), -(r_r.divided_by(lr))
    a[5][6] = I.point(voltage[1]).divided_by(lr)
    return a


def matrix_bounds(matrix: list[list[I]], center: list[list[I]]) -> tuple[F, F, F]:
    delta = F(0)
    mu_parameter = F(0)
    mu_center_augmented = F(0)
    for i in range(6):
        row_delta = F(0)
        row_mu = matrix[i][i].hi
        row_mu_center = center[i][i].hi
        for j in range(7):
            c = center[i][j]
            p = matrix[i][j]
            row_delta += max(abs(p.lo - c.hi), abs(p.hi - c.lo))
            if j != i:
                row_mu_center += c.abs_upper()
                if j < 6:
                    row_mu += p.abs_upper()
        delta = max(delta, row_delta)
        mu_parameter = max(mu_parameter, row_mu)
        mu_center_augmented = max(mu_center_augmented, row_mu_center)
    return delta, mu_parameter, max(F(0), mu_center_augmented)


def center_matrix(voltage: F) -> list[list[I]]:
    z, o = I.point(F(0)), I.point(F(1))
    return [
        [-I.point(F(3)), I.point(F(2)), z, z, z],
        [o, -I.point(F(2)), o, z, z],
        [z, -o, -o, z, I.point(voltage)],
        [o, z, z, z, z],
        [z, z, z, z, z],
    ]


def norm_vector(values: list[I]) -> F:
    return max(cell.abs_upper() for cell in values)


def norm_matrix(values: list[list[I]]) -> F:
    return max(sum((cell.abs_upper() for cell in row), F(0)) for row in values)


def matvec(matrix: list[list[I]], vector: list[I]) -> list[I]:
    result: list[I] = []
    for row in matrix:
        value = I.point(F(0))
        for coefficient, cell in zip(row, vector):
            value = value + coefficient * cell
        result.append(value)
    return result


def flow(
    matrix: list[list[I]], initial: list[I], h: F, degree: int, partial: bool, bits: int
) -> list[I]:
    qnorm = norm_matrix(matrix) * h
    if qnorm / (degree + 2) >= 1:
        raise ValueError("TAYLOR_REMAINDER_RATIO")
    tail = F(0) if qnorm == 0 else (
        qnorm ** (degree + 1) / math.factorial(degree + 1)
    ) / (1 - qnorm / (degree + 2))
    radius = ceil_grid(tail * norm_vector(initial), bits)
    total = [I.point(F(0)) for _ in initial]
    current = initial
    hpow = F(1)
    for n in range(degree + 1):
        time_cell = I(F(0), hpow) if partial and n > 0 else I.point(hpow)
        total = [acc + value * time_cell / math.factorial(n) for acc, value in zip(total, current)]
        current = matvec(matrix, current)
        hpow *= h
    remainder = I(-radius, radius)
    return [total[i] + remainder if i < len(total) - 1 else total[i] for i in range(len(total))]


def contains(saved: list[str], computed: I) -> bool:
    lo, hi = map(q, saved)
    return lo <= computed.lo and hi >= computed.hi


def main() -> int:
    release = load("coordination/autonomous_w2/g2/releases/RELEASE_v6.json")
    release_path = root_file("coordination/autonomous_w2/g2/releases/RELEASE_v6.json")
    release_hash = hashlib.sha256(release_path.read_bytes()).hexdigest()
    if release_hash != RELEASE_SHA256:
        raise ValueError("RELEASE_HASH_MISMATCH")
    protocol, profile = load(PROTOCOL_REL), load(PROFILE_REL)
    lo, hi = map(q, protocol["model"]["fixed_label_bounds"])
    labels = {name: I(lo, hi) for name in protocol["model"]["fixed_label_order"]}
    center_labels = {name: I.point(F(1)) for name in protocol["model"]["fixed_label_order"]}
    bits, degree = int(profile["interval_fractional_bits"]), int(profile["matrix_taylor_degree"])
    hold, slabs = q(protocol["task"]["hold_s"]), int(profile["center_time_slabs"])
    h = hold / slabs
    expected_rows: list[dict[str, Any]] = []

    for case_name, row_rel in ROWS:
        row = load(row_rel)
        action = next(item for item in protocol["actions"] if item["id"] == row["action_id"])
        voltage = tuple(map(q, action["voltage"]))
        matrix = interval_matrix(labels, voltage)
        center_full = interval_matrix(center_labels, voltage)
        delta, mu_param, mu_aug = matrix_bounds(matrix, center_full)
        mu = max(F(0), mu_param, mu_aug)
        if q(row["matrix_residual_norm_inf_upper"]) < delta:
            raise ValueError(f"{case_name}:MATRIX_RESIDUAL_UNDERBOUND")
        if q(row["internal_log_norm_upper"]) < mu_param or q(row["center_augmented_log_norm_upper"]) < mu_aug:
            raise ValueError(f"{case_name}:LOG_NORM_UNDERBOUND")
        if q(row["common_log_norm_upper"]) < mu:
            raise ValueError(f"{case_name}:COMMON_LOG_NORM_UNDERBOUND")

        initial = [I(q(pair[0]), q(pair[1])) for pair in protocol["task"]["initial_box"]]
        reference = list(map(q, ("3/10", "0", "1/4", "1/4", "0", "0")))
        e0 = max(max(abs(initial[3 + i].lo - reference[i]), abs(initial[3 + i].hi - reference[i])) for i in range(6))
        if q(row["initial_internal_reference_radius"]) < e0:
            raise ValueError(f"{case_name}:INITIAL_RADIUS_UNDERBOUND")
        x = mu * hold
        exp_series = sum((x**n / math.factorial(n) for n in range(degree + 1)), F(0))
        exp_tail = F(0) if x == 0 else (
            x ** (degree + 1) / math.factorial(degree + 1)
        ) / (1 - x / (degree + 2))
        exp_upper = ceil_grid(exp_series + exp_tail, bits)
        if q(row["exp_growth_upper"]) < exp_upper:
            raise ValueError(f"{case_name}:EXPONENTIAL_UNDERBOUND")
        radius_min = q(row["exp_growth_upper"]) * (
            q(row["initial_internal_reference_radius"]) + hold * q(row["matrix_residual_norm_inf_upper"])
        )
        if q(row["internal_error_radius_full_hold"]) < ceil_grid(radius_min, bits):
            raise ValueError(f"{case_name}:RESIDUAL_RADIUS_UNDERBOUND")

        center = [I.point(F(3, 10)), I.point(F(1, 4)), I.point(F(0)), I.point(F(0)), I.point(F(1))]
        a0 = center_matrix(voltage[0])
        beta_center, u_center = F(0), F(0)
        px_lo = px_hi = F(0)
        slab_checks = 0
        for index, saved_slab in enumerate(row["slabs"]):
            partial = flow(a0, center, h, degree, True, bits)
            endpoint = flow(a0, center, h, degree, False, bits)
            slip = partial[1] - partial[0]
            checks = (
                ("partial_u_mps", partial[0]),
                ("partial_wheel_rate_radps", partial[1]),
                ("partial_current_A", partial[2]),
                ("partial_p_x_m", partial[3]),
                ("partial_slip_LR", slip),
            )
            if any(not contains(saved_slab[key], value) for key, value in checks):
                raise ValueError(f"{case_name}:CENTER_PARTIAL_RANGE_NOT_CONTAINED:{index}")
            beta_center = max(beta_center, slip.abs_upper())
            u_center = max(u_center, partial[0].abs_upper())
            px_lo, px_hi = min(px_lo, partial[3].lo), max(px_hi, partial[3].hi)
            center = endpoint
            slab_checks += 1
        if slab_checks != 256 or len(row["slabs"]) != 256:
            raise ValueError(f"{case_name}:SLAB_COUNT")
        if not contains(row["center_progress_enclosure_m"], center[3]):
            raise ValueError(f"{case_name}:CENTER_ENDPOINT_NOT_CONTAINED")
        saved_px = list(map(q, row["center_p_x_full_time_range_m"]))
        if saved_px[0] > px_lo or saved_px[1] < px_hi:
            raise ValueError(f"{case_name}:CENTER_POSITION_RANGE_UNDERBOUND")
        if q(row["center_slip_abs_upper"]) < beta_center or q(row["center_u_abs_upper"]) < u_center:
            raise ValueError(f"{case_name}:CENTER_SLIP_OR_SPEED_UNDERBOUND")

        radius = q(row["internal_error_radius_full_hold"])
        beta = q(row["clip_beta_upper_full_domain"])
        if beta < ceil_grid(q(row["center_slip_abs_upper"]) + 3 * radius, bits) or beta >= 1:
            raise ValueError(f"{case_name}:FIRST_EXIT_OR_CLIP_BOUND")
        if not row["clip_strict_interior_proved"]:
            raise ValueError(f"{case_name}:CLIP_FLAG")

        task = protocol["task"]
        pose = [I(q(pair[0]), q(pair[1])) for pair in task["initial_box"][:3]]
        theta0 = max(abs(pose[2].lo), abs(pose[2].hi))
        px0 = max(abs(pose[0].lo), abs(pose[0].hi))
        py0 = max(abs(pose[1].lo), abs(pose[1].hi))
        theta_h = ceil_grid(theta0 + hold * radius, bits)
        if q(row["theta_abs_upper_full_hold"]) < theta_h:
            raise ValueError(f"{case_name}:HEADING_UNDERBOUND")
        ej_min = ceil_grid(hold * radius + hold * q(row["center_u_abs_upper"]) * theta_h**2 / 2, bits)
        if q(row["progress_error_radius_m"]) < ej_min:
            raise ValueError(f"{case_name}:PROGRESS_ERROR_UNDERBOUND")
        if q(row["position_error_x_upper_m"]) < px0 + q(row["progress_error_radius_m"]):
            raise ValueError(f"{case_name}:POSITION_X_ERROR_UNDERBOUND")
        epy_min = py0 + hold * (q(row["center_u_abs_upper"]) + radius) * theta_h
        if q(row["position_error_y_upper_m"]) < ceil_grid(epy_min, bits):
            raise ValueError(f"{case_name}:POSITION_Y_ERROR_UNDERBOUND")

        threshold = q(task["required_progress_m"])
        center_j = [q(v) for v in row["center_progress_enclosure_m"]]
        progress = [q(v) for v in row["progress_enclosure_m"]]
        if progress[0] > floor_grid(center_j[0] - q(row["progress_error_radius_m"]), bits):
            raise ValueError(f"{case_name}:PROGRESS_LOWER_NOT_OUTWARD")
        if progress[1] < ceil_grid(center_j[1] + q(row["progress_error_radius_m"]), bits):
            raise ValueError(f"{case_name}:PROGRESS_UPPER_NOT_OUTWARD")

        cmin = min(q(protocol["model"]["fixed_label_bounds"][0]), q(protocol["model"]["fixed_label_bounds"][0]))
        reserve = q(row["contact_reserve_per_wheel_lower_N"])
        if reserve > cmin * (1 - beta**2):
            raise ValueError(f"{case_name}:CONTACT_RESERVE_NOT_LOWER")
        demand = q(row["contact_demand_upper_N"])
        if demand < (q(row["center_u_abs_upper"]) + radius) * radius:
            raise ValueError(f"{case_name}:CONTACT_DEMAND_NOT_UPPER")
        contact = q(row["contact_margin_lower_N"])
        if contact > 2 * reserve - demand or contact < 0:
            raise ValueError(f"{case_name}:CONTACT_MARGIN")

        obsx, obsy = map(q, task["obstacle"]["center_m"])
        xgap = F(0) if saved_px[0] <= obsx <= saved_px[1] else min(abs(obsx - saved_px[0]), abs(obsx - saved_px[1]))
        distance = q(row["center_distance_lower_m"])
        if distance < 0 or distance**2 > xgap**2 + obsy**2:
            raise ValueError(f"{case_name}:CENTER_DISTANCE_NOT_LOWER")
        collision = q(row["collision_margin_lower_m"])
        if collision > distance - q(row["position_error_l1_upper_m"]) - q(task["obstacle"]["inflated_radius_m"]):
            raise ValueError(f"{case_name}:COLLISION_MARGIN_NOT_LOWER")
        if collision <= 0:
            raise ValueError(f"{case_name}:COLLISION_NOT_STRICT")

        eligible = contact >= 0 and collision > 0 and progress[0] >= threshold
        if bool(row["task_eligible"]) != eligible:
            raise ValueError(f"{case_name}:TASK_CLASSIFICATION")
        expected_rows.append(
            {
                "case": case_name,
                "matrix_delta_exact_le_saved": True,
                "log_norms_exact_le_saved": True,
                "exponential_and_residual_bounds": True,
                "center_partial_slabs_independently_rederived": slab_checks,
                "center_position_range_contains_rederived_path": True,
                "clip_first_exit_bound": str(beta),
                "contact_margin_lower_N": str(contact),
                "collision_margin_lower_m": str(collision),
                "progress_enclosure_m": [str(v) for v in progress],
                "task_eligible": eligible,
            }
        )

    result = {
        "schema": "G4_W2_G2_V6_INDEPENDENT_EXACT_BOUND_AUDIT_v1",
        "release_sha256": RELEASE_SHA256,
        "arithmetic": "stdlib fractions.Fraction; independent interval/Taylor implementation; no G2 imports",
        "rows": expected_rows,
        "all_pass": True,
    }
    out = root_file("results/validation/autonomous_w2/g4/exact_bound_audit_v1.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
