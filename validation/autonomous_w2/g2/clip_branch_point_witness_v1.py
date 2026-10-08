"""Exact-rational point witness for the clip-interior branch on the W2 task."""
from __future__ import annotations

import json
from fractions import Fraction as F
from math import factorial
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/validation/autonomous_w2/g2/clip_branch_point_witness_v1.json"
N = 30
SLABS = 16
H = F(2, SLABS)
STATE0 = [F(3, 10), F(1, 4), F(0), F(1)]


Interval = tuple[F, F]


def add(x: Interval, y: Interval) -> Interval:
    return x[0] + y[0], x[1] + y[1]


def scale(c: F, x: Interval) -> Interval:
    lo, hi = c * x[0], c * x[1]
    return min(lo, hi), max(lo, hi)


def matvec(a: list[list[F]], x: list[Interval]) -> list[Interval]:
    result = []
    for row in a:
        value = (F(0), F(0))
        for coefficient, cell in zip(row, x):
            value = add(value, scale(coefficient, cell))
        result.append(value)
    return result


def norm_upper(x: Iterable[Interval]) -> F:
    return max(max(abs(lo), abs(hi)) for lo, hi in x)


def taylor(a: list[list[F]], initial: list[Interval], *, partial: bool) -> tuple[list[Interval], F]:
    norm = max(sum(abs(c) for c in row) for row in a)
    q = norm * H
    if q / (N + 2) >= 1:
        raise ValueError("TAYLOR_TAIL_RATIO_NOT_CONTRACTIVE")
    tail = q ** (N + 1) / factorial(N + 1) / (1 - q / (N + 2))
    radius = tail * norm_upper(initial)
    power = initial
    total = [(F(0), F(0)) for _ in initial]
    for degree in range(N + 1):
        if partial:
            time_factor = (F(0), H**degree)
        else:
            time_factor = (H**degree, H**degree)
        term = []
        for lo, hi in power:
            candidates = (lo * time_factor[0], lo * time_factor[1], hi * time_factor[0], hi * time_factor[1])
            term.append((min(candidates) / factorial(degree), max(candidates) / factorial(degree)))
        total = [add(x, y) for x, y in zip(total, term)]
        power = matvec(a, power)
    widened = [(lo - radius, hi + radius) for lo, hi in total]
    return widened, tail


def run() -> dict[str, object]:
    if OUT.exists():
        raise FileExistsError("CLIP_BRANCH_POINT_WITNESS_ALREADY_EXISTS")
    action_voltages = {"ZERO": F(0), "NOMINAL": F(1, 2), "ALTERNATIVE": F(1)}
    action_results = {}
    for name, voltage in action_voltages.items():
        a = [
            [F(-3), F(2), F(0), F(0)],
            [F(1), F(-2), F(1), F(0)],
            [F(0), F(-1), F(-1), voltage],
            [F(0), F(0), F(0), F(0)],
        ]
        state = [(v, v) for v in STATE0]
        slab_rows = []
        for index in range(SLABS):
            partial, partial_tail = taylor(a, state, partial=True)
            endpoint, endpoint_tail = taylor(a, state, partial=False)
            slip = partial[1][0] - partial[0][1], partial[1][1] - partial[0][0]
            beta = max(abs(slip[0]), abs(slip[1]))
            slab_rows.append({
                "index": index,
                "start_s": str(index * H),
                "end_s": str((index + 1) * H),
                "slip_L_outer": [str(slip[0]), str(slip[1])],
                "absolute_slip_upper": str(beta),
                "strict_clip_interior_proved": beta < 1,
                "partial_tail_inf_upper": str(partial_tail),
                "endpoint_tail_inf_upper": str(endpoint_tail),
            })
            state = endpoint
        action_results[name] = {
            "voltage_V": [str(voltage), str(voltage)],
            "all_slabs_strictly_inside_clip": all(row["strict_clip_interior_proved"] for row in slab_rows),
            "maximum_slab_absolute_slip_upper": max(F(row["absolute_slip_upper"]) for row in slab_rows).__str__(),
            "slabs": slab_rows,
        }
    if not all(value["all_slabs_strictly_inside_clip"] for value in action_results.values()):
        raise AssertionError("POINT_CLIP_INTERIOR_NOT_PROVED")
    report = {
        "schema": "G2_W2_CLIP_BRANCH_POINT_WITNESS_v1",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "classification": "exact-rational nonquery analytic fixture; one allowed point in the frozen positive-width task/domain",
        "point": {
            "state_order": ["p_x", "p_y", "theta", "u", "r", "omega_L", "omega_R", "i_L", "i_R"],
            "state": ["0", "0", "0", "3/10", "0", "1/4", "1/4", "0", "0"],
            "fixed_parameter_labels": {name: "1" for name in ["rho_L", "rho_R", "C_L", "C_R", "lambda_L", "lambda_R", "R_L", "R_R", "B_L", "B_R", "k_L", "k_R"]},
            "hold_s": "2/1",
        },
        "method": {
            "symmetric_reduced_affine_state": ["u", "omega", "i", "1"],
            "matrix_rule": "y'=[[ -3, 2, 0, 0 ],[1,-2,1,0],[0,-1,-1,V],[0,0,0,0]] y while |omega-u|<1",
            "exact_arithmetic": "fractions.Fraction only; every state cell is an exact rational interval",
            "partition": {"slab_count": SLABS, "slab_duration_s": str(H), "contiguous_coverage_s": ["0/1", "2/1"]},
            "taylor_degree": N,
            "tail_bound": "q^(N+1)/(N+1)!/(1-q/(N+2))*||y_start||_inf, q=||A||_inf*h; symmetric outward interval added on each slab",
            "fixed_labels_and_voltage": "one point label vector and one voltage per full hold; carried unchanged",
        },
        "actions": action_results,
        "native_attempts_added": 0,
        "held_out_rows": 0,
        "legacy_800_row_study": "NOT_RUN",
        "interpretation": "This proves the center point remains on the affine clip-interior branch for all three actions. It does not prove the whole state/parameter cell, contact, collision or task eligibility. The full-cell v4 clip failure is therefore a domain-enclosure overestimate at least for this allowed point; it is not a trajectory counterexample.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
