#!/usr/bin/env python3
"""Independent coefficient regressions for evaluator and checker comparison radii."""

from __future__ import annotations

import json
import math
import subprocess
import argparse
from fractions import Fraction as F

from validation.g2.checker import _replay_radius
from validation.g2.evaluator import ROOT, _radius_series
from validation.g2.rational import Budget


def direct_partial(N: list[list[F]], forcing: list[F], T: F, order: int) -> list[F]:
    """Build terms independently as T**(k+1)/(k+1)! times N**k q."""
    vector = forcing[:]
    result = [F(0)] * len(forcing)
    for k in range(order + 1):
        coefficient = T ** (k + 1) / math.factorial(k + 1)
        for i in range(len(result)):
            result[i] += coefficient * vector[i]
        vector = [sum((N[i][j] * vector[j] for j in range(len(vector))), F(0)) for i in range(len(vector))]
    return result


def require(name: str, condition: bool, detail: str) -> dict[str, object]:
    if not condition:
        raise AssertionError(f"{name}: {detail}")
    return {"name": name, "pass": True, "detail": detail}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true", help="run checks without writing the frozen evidence file")
    args = parser.parse_args()
    T = F(1, 10)
    N = [[F(1) if i == j == 0 else F(0) for j in range(6)] for i in range(6)]
    D_abs = [[F(1) if i == 0 and j == 0 else F(0) for j in range(2)] for i in range(6)]
    force = [F(1), F(0)]
    expected_forcing = [F(1), F(0), F(0), F(0), F(0), F(0)]
    checks = []
    details = []

    for order in (0, 1, 2, 16):
        expected = direct_partial(N, expected_forcing, T, order)
        evaluator_total, evaluator_q, evaluator_Q, evaluator_tail = _radius_series(
            N, D_abs, force, T, order, Budget(32768, 100000),
        )
        checker_total, checker_q, checker_Q, checker_tail = _replay_radius(
            N, D_abs, force, T, order, Budget(32768, 100000),
        )
        checks.append(require(
            f"evaluator factorial coefficients K={order}",
            [x - evaluator_tail for x in evaluator_total] == expected,
            "computed partial sum equals direct powers/factorials",
        ))
        checks.append(require(
            f"checker factorial coefficients K={order}",
            [x - checker_tail for x in checker_total] == expected,
            "replayed partial sum equals independently constructed powers/factorials",
        ))
        checks.append(require(
            f"evaluator/checker radius agreement K={order}",
            (evaluator_total, evaluator_q, evaluator_Q, evaluator_tail)
            == (checker_total, checker_q, checker_Q, checker_tail),
            "separate implementations agree on complete radius and tail",
        ))
        details.append({
            "order": order,
            "partial_component_0": f"{expected[0].numerator}/{expected[0].denominator}",
            "tail": f"{evaluator_tail.numerator}/{evaluator_tail.denominator}",
            "total_component_0": f"{evaluator_total[0].numerator}/{evaluator_total[0].denominator}",
        })

    checks.append(require(
        "locked K=1 regression values",
        details[1]["partial_component_0"] == "21/200"
        and details[1]["tail"] == "1/2000"
        and details[1]["total_component_0"] == "211/2000",
        "expected partial 21/200, tail 1/2000, total upper 211/2000",
    ))

    zero_N = [[F(0) for _ in range(6)] for _ in range(6)]
    zero_order_total, _, zero_Q, zero_tail = _radius_series(
        zero_N, D_abs, force, T, 16, Budget(4096, 10000),
    )
    checks.append(require(
        "zero comparison norm", zero_Q == 0 and zero_tail == 0 and zero_order_total == [T, F(0), F(0), F(0), F(0), F(0)],
        "N=0 yields exact first forcing integral and zero tail",
    ))
    zero_force_total, _, zero_force_Q, zero_force_tail = _radius_series(
        N, D_abs, [F(0), F(0)], T, 16, Budget(4096, 10000),
    )
    checks.append(require(
        "zero comparison forcing", zero_force_Q == F(1, 10) and zero_force_tail == 0 and not any(zero_force_total),
        "q=0 produces an exact zero radius even when N is nonzero",
    ))

    output = {
        "schema": "ddwmr-g2-radius-series-regression-r2-v1",
        "source_revision": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip(),
        "all_pass": all(item["pass"] for item in checks),
        "check_count": len(checks),
        "checks": checks,
        "fixture": {"N00": "1", "q0": "1", "T": "1/10", "orders": [0, 1, 2, 16]},
        "exact_values": details,
        "scope": "coefficient/tail implementation regression; not a plant trajectory or general proof",
    }
    output_path = ROOT / "results/validation/g2/r2/radius_series_regression_r2_v1.json"
    if not args.check_only:
        if output_path.exists():
            raise SystemExit(f"refusing to overwrite regression evidence: {output_path}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
