"""Independently recompute the saved G2 v6 pose-error and collision bounds.

Uses only stdlib Fraction. This closes the pose-error composition audit that
was not explicit in exact_bound_audit_v1; it reads only the three saved rows.
"""
from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
RELEASE_SHA256 = "789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55"
PROTOCOL_REL = "research/autonomous_w2/g2/task_protocol_v1.json"
ROWS = (
    ("zero", "results/validation/autonomous_w2/g2/development_centered_v6/attempt_01_W2_G2_DEV_001_ZERO/row.json"),
    ("nominal", "results/validation/autonomous_w2/g2/development_centered_v6/attempt_02_W2_G2_DEV_001_NOMINAL/row.json"),
    ("alternative", "results/validation/autonomous_w2/g2/development_centered_v6/attempt_03_W2_G2_DEV_001_ALTERNATIVE/row.json"),
)
BITS = 96


def root_file(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError(f"PATH_ESCAPES_REPO:{relative}")
    return path


def q(value: Any) -> F:
    return F(str(value))


def floor_grid(value: F) -> F:
    scale = 1 << BITS
    return F((value.numerator * scale) // value.denominator, scale)


def ceil_grid(value: F) -> F:
    scale = 1 << BITS
    return F(-((-value.numerator * scale) // value.denominator), scale)


def main() -> int:
    protocol = json.loads(root_file(PROTOCOL_REL).read_text(encoding="utf-8"))
    hold = q(protocol["task"]["hold_s"])
    initial = protocol["task"]["initial_box"]
    px0 = max(abs(q(initial[0][0])), abs(q(initial[0][1])))
    py0 = max(abs(q(initial[1][0])), abs(q(initial[1][1])))
    theta0 = max(abs(q(initial[2][0])), abs(q(initial[2][1])))
    obsx, obsy = map(q, protocol["task"]["obstacle"]["center_m"])
    obs_radius = q(protocol["task"]["obstacle"]["inflated_radius_m"])
    outputs = []
    for case_name, row_rel in ROWS:
        row = json.loads(root_file(row_rel).read_text(encoding="utf-8"))
        if len(row.get("slabs", [])) != 256:
            raise ValueError(f"{case_name}:SLAB_COUNT")
        e = q(row["internal_error_radius_full_hold"])
        u_center = q(row["center_u_abs_upper"])
        theta_saved = q(row["theta_abs_upper_full_hold"])
        progress_error = q(row["progress_error_radius_m"])
        px_error = q(row["position_error_x_upper_m"])
        py_error = q(row["position_error_y_upper_m"])
        l1_error = q(row["position_error_l1_upper_m"])

        theta_min = ceil_grid(theta0 + hold * e)
        progress_error_min = ceil_grid(hold * e + hold * u_center * theta_saved**2 / 2)
        px_error_min = ceil_grid(px0 + progress_error)
        py_error_min = ceil_grid(py0 + hold * (u_center + e) * theta_saved)
        l1_error_min = ceil_grid(px_error + py_error)
        if theta_saved < theta_min:
            raise ValueError(f"{case_name}:THETA_H_UNDERBOUND")
        if progress_error < progress_error_min:
            raise ValueError(f"{case_name}:PROGRESS_ERROR_UNDERBOUND")
        if px_error < px_error_min:
            raise ValueError(f"{case_name}:POSITION_X_ERROR_UNDERBOUND")
        if py_error < py_error_min:
            raise ValueError(f"{case_name}:POSITION_Y_ERROR_UNDERBOUND")
        if l1_error < l1_error_min:
            raise ValueError(f"{case_name}:POSITION_L1_ERROR_UNDERBOUND")

        px_range = list(map(q, row["center_p_x_full_time_range_m"]))
        if len(px_range) != 2 or px_range[0] > px_range[1]:
            raise ValueError(f"{case_name}:INVALID_CENTER_X_RANGE")
        xgap = F(0) if px_range[0] <= obsx <= px_range[1] else min(abs(obsx - px_range[0]), abs(obsx - px_range[1]))
        geometric_square = xgap**2 + obsy**2
        distance = q(row["center_distance_lower_m"])
        if distance < 0 or distance**2 > geometric_square:
            raise ValueError(f"{case_name}:CENTER_DISTANCE_NOT_LOWER")
        collision_min = floor_grid(distance - l1_error - obs_radius)
        collision_saved = q(row["collision_margin_lower_m"])
        if collision_saved > collision_min or collision_saved <= 0:
            raise ValueError(f"{case_name}:COLLISION_MARGIN_INVALID")

        outputs.append({
            "case": case_name,
            "theta_h_saved_ge_recomputed": True,
            "progress_error_saved_ge_recomputed": True,
            "position_x_error_saved_ge_recomputed": True,
            "position_y_error_saved_ge_recomputed": True,
            "position_l1_ge_position_x_plus_y": True,
            "center_distance_is_nonnegative_geometric_lower_bound": True,
            "collision_margin_saved_le_recomputed_lower_bound": True,
            "theta_h_min": str(theta_min),
            "progress_error_min_m": str(progress_error_min),
            "position_x_error_min_m": str(px_error_min),
            "position_y_error_min_m": str(py_error_min),
            "position_l1_error_min_m": str(l1_error_min),
            "collision_margin_recomputed_floor_m": str(collision_min),
            "collision_margin_saved_m": str(collision_saved),
        })
    result = {
        "schema": "G4_W2_G2_V6_INDEPENDENT_POSE_COLLISION_AUDIT_v1",
        "release_sha256": RELEASE_SHA256,
        "arithmetic": "stdlib fractions.Fraction with explicit 96-bit outward grid; no G2 imports",
        "rows": outputs,
        "all_pass": len(outputs) == 3,
        "native_attempts_added": 0,
        "producer_invocations": 0,
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["all_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
