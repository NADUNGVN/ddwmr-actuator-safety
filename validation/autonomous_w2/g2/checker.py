"""Independent W2 G2 replay; imports no producer/model/margin helpers."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

from .rational_interval import ArithmeticLimit, Budget, I, activate, q, qs, sqrt_lower


ROOT = Path(__file__).resolve().parents[3]
STATE_ORDER = ["p_x", "p_y", "theta", "u", "r", "omega_L", "omega_R", "i_L", "i_R"]
LABEL_ORDER = ["rho_L", "rho_R", "C_L", "C_R", "lambda_L", "lambda_R", "R_L", "R_R", "B_L", "B_R", "k_L", "k_R"]
INTERNAL_ORDER = ["u", "r", "omega_L", "omega_R", "i_L", "i_R"]


class ReplayReject(RuntimeError):
    pass


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csha(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _read_and_validate(protocol: dict[str, Any]) -> tuple[list[I], dict[str, I], list[dict[str, Any]], Fraction]:
    model = protocol.get("model", {})
    if protocol.get("protocol_id") != "G2_W2_VOF_TASK_V1" or protocol.get("protocol_state") != "FROZEN_FOR_DEVELOPMENT_NOT_CONFIRMATION":
        raise ReplayReject("FROZEN_PROTOCOL_ID_OR_STATE")
    if model.get("phi") != "clip(s,-1,1)" or model.get("lipschitz_constant") != "1" or model.get("fixed_label_order") != LABEL_ORDER:
        raise ReplayReject("SUPPORTED_CLIP_OR_LABEL_CONTRACT")
    const = model.get("fixed_constants", {})
    if set(const) != {"m", "I_z", "R_w", "b", "v_s", "c_u", "c_r", "V_max"} or any(q(v) != 1 for v in const.values()):
        raise ReplayReject("FIXED_MODEL_CONSTANTS")
    if model.get("fixed_label_bounds") != ["9999/10000", "10001/10000"]:
        raise ReplayReject("LABEL_BOUND_PIN")
    lo, hi = map(q, model["fixed_label_bounds"])
    if not (0 < lo < hi):
        raise ReplayReject("LABEL_DOMAIN_POSITIVITY_OR_WIDTH")
    labels = {name: I(lo, hi) for name in LABEL_ORDER}
    if any(item.lo <= 0 or item.lo >= item.hi for item in labels.values()):
        raise ReplayReject("PARAMETER_IMAGE_INVALID")
    rho_max = labels["rho_L"].hi
    if 1 / rho_max <= Fraction(1, 10):
        raise ReplayReject("GEAR_WITNESS_POSITIVITY")
    if model.get("parameter_maps") != {"J_j": "1/rho_j", "L_j": "lambda_j"}:
        raise ReplayReject("RATIONAL_PARAMETER_IMAGE")

    task = protocol.get("task", {})
    if task.get("initial_box_state_order") != STATE_ORDER:
        raise ReplayReject("STATE_COORDINATE_ORDER")
    raw = task.get("initial_box")
    if not isinstance(raw, list) or len(raw) != 9:
        raise ReplayReject("INITIAL_STATE_DIMENSION")
    state = [I(q(e[0]), q(e[1])) for e in raw]
    if any(x.lo >= x.hi for x in state) or state[3].lo <= 0:
        raise ReplayReject("INITIAL_STATE_DOMAIN")
    duration = q(task.get("hold_s"))
    if duration != 2 or q(task.get("required_progress_m")) != Fraction(7, 20):
        raise ReplayReject("HOLD_OR_TASK_THRESHOLD")
    obs = task.get("obstacle", {})
    if obs.get("kind") != "static_circle" or len(obs.get("center_m", [])) != 2 or q(obs.get("inflated_radius_m")) <= 0:
        raise ReplayReject("STATIC_FOOTPRINT_CIRCLE")
    actions = protocol.get("actions", [])
    expected = [
        {"id": "W2_G2_DEV_001_ZERO", "role": "zero", "voltage": ["0", "0"]},
        {"id": "W2_G2_DEV_001_NOMINAL", "role": "nominal", "voltage": ["1/2", "1/2"]},
        {"id": "W2_G2_DEV_001_ALTERNATIVE", "role": "alternative", "voltage": ["1", "1"]},
    ]
    if actions != expected:
        raise ReplayReject("THREE_ACTION_ORDER_OR_VOLTAGE_SEMANTICS")
    if any(abs(q(v)) > 1 for action in actions for v in action["voltage"]):
        raise ReplayReject("VOLTAGE_CAP")
    return state, labels, actions, duration


def _assemble(labels: dict[str, I], v: tuple[Fraction, Fraction]) -> list[list[I]]:
    z, one = I.point(0), I.point(1)
    rho0, rho1 = labels["rho_L"], labels["rho_R"]
    cap0, cap1 = labels["C_L"], labels["C_R"]
    ind0, ind1 = labels["lambda_L"], labels["lambda_R"]
    res0, res1 = labels["R_L"], labels["R_R"]
    damp0, damp1 = labels["B_L"], labels["B_R"]
    motor0, motor1 = labels["k_L"], labels["k_R"]
    g0, g1 = cap0, cap1  # v_s=1
    m = iz = rw = b = cu = cr = one
    a = [[z for _ in range(7)] for _ in range(7)]
    # Re-derive from F_L=C_L*(omega_L-u+r), F_R=C_R*(omega_R-u-r).
    a[0][0] = -cu / m - (g0 + g1) / m
    a[0][1] = b * (g0 - g1) / m
    a[0][2] = rw * g0 / m
    a[0][3] = rw * g1 / m
    a[1][0] = b * (g0 - g1) / iz
    a[1][1] = -cr / iz - b * b * (g0 + g1) / iz
    a[1][2] = -b * rw * g0 / iz
    a[1][3] = b * rw * g1 / iz
    a[2][0] = rho0 * rw * g0
    a[2][1] = -rho0 * rw * g0 * b
    a[2][2] = -rho0 * damp0 - rho0 * rw * rw * g0
    a[2][4] = rho0 * motor0
    a[3][0] = rho1 * rw * g1
    a[3][1] = rho1 * rw * g1 * b
    a[3][3] = -rho1 * damp1 - rho1 * rw * rw * g1
    a[3][5] = rho1 * motor1
    a[4][2] = -motor0 / ind0
    a[4][4] = -res0 / ind0
    a[4][6] = I.point(v[0]) / ind0
    a[5][3] = -motor1 / ind1
    a[5][5] = -res1 / ind1
    a[5][6] = I.point(v[1]) / ind1
    return a


def _mv(a: list[list[I]], v: list[I]) -> list[I]:
    out = []
    for row in a:
        acc = I.point(0)
        for lhs, rhs in zip(row, v):
            acc = acc + lhs * rhs
        out.append(acc)
    return out


def _ninf(a: list[list[I]]) -> Fraction:
    return max(sum((x.abs_upper() for x in row), Fraction(0)) for row in a)


def _vinf(v: list[I]) -> Fraction:
    return max(x.abs_upper() for x in v)


def _flow(a: list[list[I]], initial: list[I], h: Fraction, degree: int, range_over_time: bool) -> tuple[list[I], dict[str, str]]:
    qbound = _ninf(a) * h
    if qbound / (degree + 2) >= 1:
        raise ArithmeticLimit("REPLAY_TAYLOR_TAIL_RATIO")
    tail = Fraction(0) if qbound == 0 else (qbound ** (degree + 1) / math.factorial(degree + 1)) / (1 - qbound / (degree + 2))
    remainder = tail * _vinf(initial)
    power = Fraction(1)
    vector = initial
    total = [I.point(0) for _ in initial]
    for k in range(degree + 1):
        tau_power = I(Fraction(0), power) if range_over_time and k else I.point(power)
        fact = math.factorial(k)
        for j in range(len(total)):
            total[j] = total[j] + vector[j] * tau_power / fact
        vector = _mv(a, vector)
        power *= h
    for j in range(len(total) - 1):
        total[j] = total[j] + I(-remainder, remainder)
    return total, {"q_norm_upper": qs(qbound), "tail_norm_upper": qs(tail), "remainder_inf_upper": qs(remainder), "degree": str(degree), "time_mode": "partial_[0,h]" if range_over_time else "endpoint_h"}


def _gap(x: I, c: Fraction) -> Fraction:
    if c < x.lo:
        return x.lo - c
    if c > x.hi:
        return c - x.hi
    return Fraction(0)


def _reconstruct(protocol: dict[str, Any], profile: dict[str, Any], action: dict[str, Any], protocol_sha: str, profile_sha: str) -> dict[str, Any]:
    state, labels, actions, T = _read_and_validate(protocol)
    if action not in actions:
        raise ReplayReject("ACTION_NOT_FROM_FROZEN_PROTOCOL")
    v = (q(action["voltage"][0]), q(action["voltage"][1]))
    obstacle = protocol["task"]["obstacle"]
    ox, oy = map(q, obstacle["center_m"])
    radius = q(obstacle["inflated_radius_m"])
    required = q(protocol["task"]["required_progress_m"])
    slab_count = int(profile["time_slabs"])
    degree = int(profile["matrix_taylor_degree"])
    roots = int(profile["sqrt_bisections"])
    h = T / slab_count
    if q(profile["slab_duration_s"]) != h:
        raise ReplayReject("PROFILE_SLAB_COUNT_DURATION")
    a = _assemble(labels, v)
    parameter_hash = csha({"order": LABEL_ORDER, "bounds": ["9999/10000", "10001/10000"], "maps": protocol["model"]["parameter_maps"]})
    y0 = state[3:9] + [I.point(1)]
    theta0, px0, py0 = state[2], state[0], state[1]
    j_total = I.point(0)
    slabs: list[dict[str, Any]] = []
    all_clip = True
    for index in range(slab_count):
        begin, end = index * h, (index + 1) * h
        flow, flow_proof = _flow(a, y0, h, degree, True)
        endpoint, endpoint_proof = _flow(a, y0, h, degree, False)
        ur, rr, wl, wr, il, ir = flow[:6]
        s_l = wl - ur + rr
        s_r = wr - ur - rr
        b_l, b_r = s_l.abs_upper(), s_r.abs_upper()
        inside = b_l < 1 and b_r < 1
        all_clip = all_clip and inside
        slack_l, slack_r = 1 - b_l, 1 - b_r
        cmin = q(protocol["model"]["fixed_label_bounds"][0])
        reserve_l = cmin * sqrt_lower(max(Fraction(0), 1 - b_l * b_l), roots) if b_l <= 1 else Fraction(0)
        reserve_r = cmin * sqrt_lower(max(Fraction(0), 1 - b_r * b_r), roots) if b_r <= 1 else Fraction(0)
        demand = ur.abs_upper() * rr.abs_upper()
        contact_margin = reserve_l + reserve_r - demand

        theta_rng = theta0 + I(Fraction(0), h) * rr
        theta_abs = theta_rng.abs_upper()
        cosine = I(1 - theta_abs * theta_abs / 2, Fraction(1))
        sine = I(-theta_abs, theta_abs)
        xd = ur * cosine
        yd = ur * sine
        px_range = px0 + I(Fraction(0), h) * xd
        py_range = py0 + I(Fraction(0), h) * yd
        px_end = px0 + I.point(h) * xd
        py_end = py0 + I.point(h) * yd
        theta_end = theta0 + I.point(h) * rr

        gx, gy = _gap(px_range, ox), _gap(py_range, oy)
        d2 = gx * gx + gy * gy
        distance = sqrt_lower(d2, roots)
        collision_margin = distance - radius
        dJ = I.point(h) * xd
        j_total = j_total + dJ
        slabs.append({
            "index": index,
            "start_s": qs(begin),
            "end_s": qs(end),
            "duration_s": qs(h),
            "label_image_sha256": parameter_hash,
            "matrix_augmented": [[cell.to_json() for cell in row] for row in a],
            "internal_state_range": {name: flow[k].to_json() for k, name in enumerate(INTERNAL_ORDER)},
            "internal_endpoint_range": {name: endpoint[k].to_json() for k, name in enumerate(INTERNAL_ORDER)},
            "slip_normalized_range": {"L": s_l.to_json(), "R": s_r.to_json()},
            "clip_interior": {"proved_strict": inside, "beta_upper": [qs(b_l), qs(b_r)], "slack_lower": [qs(slack_l), qs(slack_r)]},
            "contact": {"reserve_lower_N": qs(reserve_l + reserve_r), "reserve_wheel_lower_N": [qs(reserve_l), qs(reserve_r)], "demand_upper_N": qs(demand), "margin_lower_N": qs(contact_margin)},
            "heading_range_rad": theta_rng.to_json(),
            "position_range_m": {"p_x": px_range.to_json(), "p_y": py_range.to_json()},
            "position_endpoint_m": {"p_x": px_end.to_json(), "p_y": py_end.to_json()},
            "collision": {"coordinate_gaps_lower_m": [qs(gx), qs(gy)], "distance_squared_lower_m2": qs(d2), "distance_lower_m": qs(distance), "radius_m": qs(radius), "margin_lower_m": qs(collision_margin)},
            "progress_increment_range_m": dJ.to_json(),
            "partial_taylor": flow_proof,
            "endpoint_taylor": endpoint_proof,
        })
        y0, theta0, px0, py0 = endpoint, theta_end, px_end, py_end

    reasons: list[str] = []
    if not all_clip:
        reasons.append("CLIP_INTERIOR_NOT_ESTABLISHED_ON_EVERY_SLAB")
    if any(q(s["collision"]["margin_lower_m"]) < 0 for s in slabs):
        reasons.append("COLLISION_MARGIN_NEGATIVE_ON_A_SLAB")
    if any(q(s["contact"]["margin_lower_N"]) < 0 for s in slabs):
        reasons.append("CONTACT_MARGIN_NEGATIVE_ON_A_SLAB")
    safe = not reasons
    eligible = safe and j_total.lo >= required
    if safe and j_total.lo < required:
        reasons.append("PROGRESS_LOWER_BELOW_TASK_THRESHOLD")
    return {
        "schema": "G2_W2_VOF_ROW_v1",
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": protocol_sha,
        "profile_id": profile["profile_id"],
        "profile_sha256": profile_sha,
        "action_id": action["id"],
        "action_role": action["role"],
        "held_voltage_V": [qs(v[0]), qs(v[1])],
        "parameter_label_order": LABEL_ORDER,
        "parameter_label_bounds": ["9999/10000", "10001/10000"],
        "parameter_image_sha256": parameter_hash,
        "hold_s": qs(T),
        "time_coverage": {"slab_count": slab_count, "covered_start_s": "0/1", "covered_end_s": qs(T), "contiguous": True, "fixed_label_carried": True, "held_voltage_constant": True},
        "safety_status": "CERTIFIED" if safe else "UNKNOWN",
        "task_eligible": eligible,
        "reason_codes": reasons,
        "collision_margin_lower_min_m": qs(min(q(s["collision"]["margin_lower_m"]) for s in slabs)),
        "contact_margin_lower_min_N": qs(min(q(s["contact"]["margin_lower_N"]) for s in slabs)),
        "progress_enclosure_m": j_total.to_json(),
        "required_progress_m": qs(required),
        "slabs": slabs,
    }


def audit(binding_path: Path, record_path: Path) -> dict[str, Any]:
    binding = json.loads(binding_path.read_text(encoding="utf-8"))
    protocol_path = ROOT / binding["protocol_path"]
    profile_path = ROOT / binding["profile_path"]
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    if sha(protocol_path) != binding["protocol_sha256"] or sha(profile_path) != binding["profile_sha256"]:
        raise ReplayReject("FROZEN_PROTOCOL_OR_PROFILE_HASH")
    for relpath, expected in binding["source_files"].items():
        if sha(ROOT / relpath) != expected:
            raise ReplayReject(f"SOURCE_CLOSURE_HASH:{relpath}")
    record = json.loads(record_path.read_text(encoding="utf-8"))
    if record.get("binding_sha256") != sha(binding_path):
        raise ReplayReject("BINDING_HASH_MISMATCH")
    action_matches = [a for a in protocol.get("actions", []) if a.get("id") == record.get("action_id")]
    if len(action_matches) != 1:
        raise ReplayReject("RECORDED_ACTION_NOT_IN_PROTOCOL")
    budget = Budget(int(profile["interval_operation_cap"]), int(profile["rational_bit_cap"]))
    activate(budget)
    try:
        expected = _reconstruct(protocol, profile, action_matches[0], binding["protocol_sha256"], binding["profile_sha256"])
    finally:
        activate(None)
    if record.get("parameter_label_order") != LABEL_ORDER or record.get("held_voltage_V") != expected["held_voltage_V"]:
        raise ReplayReject("FIXED_LABEL_OR_VOLTAGE_SEMANTICS")
    proof_keys = [
        "schema", "protocol_id", "protocol_sha256", "profile_id", "profile_sha256", "action_id", "action_role",
        "held_voltage_V", "parameter_label_order", "parameter_label_bounds", "parameter_image_sha256", "hold_s",
        "time_coverage", "safety_status", "task_eligible", "reason_codes", "collision_margin_lower_min_m",
        "contact_margin_lower_min_N", "progress_enclosure_m", "required_progress_m", "slabs",
    ]
    mismatches = [key for key in proof_keys if record.get(key) != expected.get(key)]
    if mismatches:
        raise ReplayReject("RECOMPUTED_PROOF_FIELDS_MISMATCH:" + ",".join(mismatches))
    slabs = record.get("slabs")
    if not isinstance(slabs, list) or len(slabs) != int(profile["time_slabs"]):
        raise ReplayReject("INCOMPLETE_SLAB_COVERAGE")
    prev = Fraction(0)
    for i, slab in enumerate(slabs):
        if q(slab["start_s"]) != prev or q(slab["end_s"]) <= prev or slab["index"] != i:
            raise ReplayReject("SLAB_GAP_OVERLAP_OR_REORDER")
        if slab["label_image_sha256"] != expected["parameter_image_sha256"]:
            raise ReplayReject("ILLEGAL_LABEL_RESET")
        prev = q(slab["end_s"])
    if prev != q(protocol["task"]["hold_s"]):
        raise ReplayReject("TIME_COVERAGE_DOES_NOT_REACH_HOLD_END")
    return {
        "schema": "G2_W2_REPLAY_AUDIT_v1",
        "replayed": True,
        "recomputed_safety_status": expected["safety_status"],
        "recomputed_task_eligible": expected["task_eligible"],
        "proof_fields_recomputed": len(proof_keys),
        "slabs_recomputed": len(slabs),
        "fixed_label_chaining_recomputed": True,
        "held_voltage_constant_recomputed": True,
        "recomputed_progress_enclosure_m": expected["progress_enclosure_m"],
        "recomputed_min_collision_margin_m": expected["collision_margin_lower_min_m"],
        "recomputed_min_contact_margin_N": expected["contact_margin_lower_min_N"],
        "replay_arithmetic": {"interval_operations": budget.operations, "max_rational_bits": budget.max_observed_bits},
        "shared_trust": ["Python fractions.Fraction", "rational_interval.I/Budget/sqrt_lower"],
        "independent_recomputation": ["protocol semantics", "parameter-to-matrix mapping", "signed 7x7 flow", "Taylor remainder", "slab carry", "pose/contact/collision/progress inequalities", "status aggregation"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding", required=True)
    parser.add_argument("--record", required=True)
    args = parser.parse_args()
    binding_path = Path(args.binding)
    record_path = Path(args.record)
    if not binding_path.is_absolute():
        binding_path = Path.cwd() / binding_path
    if not record_path.is_absolute():
        record_path = Path.cwd() / record_path
    try:
        result = audit(binding_path, record_path)
    except BaseException as exc:
        result = {"schema": "G2_W2_REPLAY_AUDIT_v1", "replayed": False, "rejection": f"{type(exc).__name__}:{exc}"}
        sys.stdout.write(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
        return 3
    sys.stdout.write(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
