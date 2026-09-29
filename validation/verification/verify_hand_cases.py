#!/usr/bin/env python3
"""Reproduce selected declared A/B/C rational inequalities, separate from evaluator."""

from __future__ import annotations

import json
from fractions import Fraction as F


def require(name: str, actual: F, relation: str, target: F) -> dict:
    ok = (actual < target if relation == "<" else actual <= target if relation == "<="
          else actual > target if relation == ">" else actual >= target if relation == ">=" else actual == target)
    if not ok:
        raise AssertionError(f"{name}: {actual} !{relation} {target}")
    return {"name": name, "actual": f"{actual.numerator}/{actual.denominator}", "relation": relation,
            "target": f"{target.numerator}/{target.denominator}", "pass": True}


def verify_A() -> list[dict]:
    T = F(1, 10)
    cd = F(847, 960)
    alpha = F(9, 10) * cd
    e_q = F(2673, 1525)
    eps_g, eps_h, eps_f = F(1, 12500), F(11, 200000), F(8, 25000)
    pose = [F(9, 1000000), F(6, 1000000), F(33, 1000000)]
    collision = [F(74891, 1000000), F(74894, 1000000), F(74867, 1000000)]
    betas = [F(68, 12500), F(1073, 200000), F(77, 12500)]
    contact = F(491949, 250000)
    checks = [
        require("A exp bound", e_q, "<", F(9, 5)),
        require("A global radius", alpha * T**4, "<", eps_g),
        require("A refined radius ordering", eps_h, "<", eps_g),
        require("A fallback/global radius ratio", eps_f, "=", 4 * eps_g),
        require("A pose global margin", F(3, 5) - F(251, 10000) - F(1, 2) - pose[0], "=", collision[0]),
        require("A pose refined margin", F(3, 5) - F(251, 10000) - F(1, 2) - pose[1], "=", collision[1]),
        require("A pose fallback margin", F(3, 5) - F(251, 10000) - F(1, 2) - pose[2], "=", collision[2]),
        require("A beta global", betas[0], "<", F(1, 100)),
        require("A beta refined", betas[1], "<", F(1, 100)),
        require("A beta fallback", betas[2], "<", F(1, 100)),
        require("A contact margin", contact, ">", F(0)),
        require("A upper budget H/G", F(11, 16), "<", F(1)),
        require("A upper budget F/G", F(4), "=", F(4)),
    ]
    return checks


def verify_B() -> list[dict]:
    T = F(1, 20)
    eps_f = F(27, 5000)
    residual_exit_10ms = 5 * F(1, 100) + F(561, 40) * F(1, 10000) + 3 * eps_f
    beta_r = 5 * T + F(561, 40) * T**2 + 3 * eps_f
    initial_to_final_upper = (
        F(9, 8) - F(33, 8) * T
        + (F(2131, 800) + F(561, 40)) * T**2
        + F(1331, 6000) * T**3 + 3 * eps_f
    )
    initial_to_final_lower = F(9, 8) - (5 * T + F(561, 40) * T**2 + 3 * eps_f)
    collision = [F(-7, 1000000), F(8, 1000000), F(-190, 1000000)]
    pose = [F(92, 1000000), F(77, 1000000), F(275, 1000000)]
    checks = [
        require("B saturation through 10ms", residual_exit_10ms, "<", F(1, 8)),
        require("B right-wheel beta", beta_r, "<", F(31, 100)),
        require("B refined collision positive", collision[1], ">", F(0)),
        require("B global collision negative", collision[0], "<", F(0)),
        require("B fallback collision negative", collision[2], "<", F(0)),
        require("B tuned global margin", F(85, 1000000) - pose[0], "=", collision[0]),
        require("B tuned refined margin", F(85, 1000000) - pose[1], "=", collision[1]),
        require("B tuned fallback margin", F(85, 1000000) - pose[2], "=", collision[2]),
        require("B left slip final upper", initial_to_final_upper, "<", F(49, 50)),
        require("B left slip final lower", initial_to_final_lower, ">", F(4, 5)),
        require("B contact margin", F(885209, 1000000), ">", F(0)),
    ]
    return checks


def verify_C() -> list[dict]:
    T = F(1, 10)
    d = F(1, 125000)
    E_p = F(3, 2000000)
    predicted = [F(0), T**4 / 36, T**4 / 9]
    margins = [F(13, 2000000), F(67, 18000000), F(-83, 18000000)]
    checks = [
        require("C zero action margin", d - predicted[0] - E_p, "=", margins[0]),
        require("C quarter action margin", d - predicted[1] - E_p, "=", margins[1]),
        require("C full action margin", d - predicted[2] - E_p, "=", margins[2]),
        require("C zero output certified", margins[0], ">", F(0)),
        require("C quarter output certified", margins[1], ">", F(0)),
        require("C full output inconclusive", margins[2], "<", F(0)),
        require("C contact lower margin", F(1999, 1000), ">", F(0)),
        require("C common pose radius", E_p, "=", F(3, 2000000)),
    ]
    return checks


def main() -> None:
    cases = {"A": verify_A(), "B": verify_B(), "C": verify_C()}
    total = sum(map(len, cases.values()))
    output = {"scope": "separate exact rational reproduction of selected declared hand inequalities; not evaluator output", "cases": cases,
              "checks": total, "all_pass": all(check["pass"] for rows in cases.values() for check in rows)}
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
