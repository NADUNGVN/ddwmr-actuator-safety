"""Non-query analytic fixtures for W2 G2 arithmetic/model conventions."""
from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

from .producer import ROOT, build_augmented_matrix, exp_range, parse_protocol
from .rational_interval import I, q, sqrt_lower


def run() -> list[dict[str, str]]:
    passed: list[dict[str, str]] = []
    protocol_path = ROOT / "research/autonomous_w2/g2/task_protocol_v1.json"
    profile_path = ROOT / "validation/autonomous_w2/g2/profile_v1.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    profile = json.loads(profile_path.read_text(encoding="utf-8"))

    x = I(F(-1, 3), F(2, 5))
    y = I(F(1, 4), F(1, 2))
    prod = x * y
    assert prod.lo <= F(-1, 6) and prod.hi >= F(1, 5)
    passed.append({"fixture": "rational_interval_four_corner_product", "status": "PASS"})

    root = sqrt_lower(F(2), 48)
    assert root * root <= 2 < (root + F(1, 2**48)) ** 2
    passed.append({"fixture": "directed_sqrt_lower_and_bisection_width", "status": "PASS"})

    state, labels, actions, duration = parse_protocol(protocol)
    assert duration == 2 and len(state) == 9 and len(labels) == 12 and len(actions) == 3
    passed.append({"fixture": "positive_width_nine_state_and_fixed_label_image", "status": "PASS"})

    matrix = build_augmented_matrix(labels, (F(1), F(1)))
    assert matrix[0][0].lo <= -3 <= matrix[0][0].hi
    assert matrix[0][2].lo <= 1 <= matrix[0][2].hi
    assert matrix[0][3].lo <= 1 <= matrix[0][3].hi
    assert matrix[2][0] == I(F(9999, 10000) ** 2, F(10001, 10000) ** 2)
    assert matrix[2][1].hi < 0 and matrix[2][4].lo > 0
    assert matrix[4][2].hi < 0 and matrix[4][2].lo <= -1 <= matrix[4][2].hi
    # Voltage coefficient is 1/lambda_L; lambda is fixed but uncertain.
    # The interval must be positive and contain the nominal value 1.
    assert matrix[4][6].lo > 0 and matrix[4][6].lo <= 1 <= matrix[4][6].hi
    assert matrix[5][6].lo > 0 and matrix[5][6].lo <= 1 <= matrix[5][6].hi
    passed.append({"fixture": "master_force_reaction_back_emf_and_voltage_signs", "status": "PASS"})

    # Exact diagonal fixture: y1'= -y1 and y2'=0. For tau in [0,1/2],
    # exp(-tau) lies between its alternating Taylor bracket at 1/2 and 1.
    toy = [[I.point(-1), I.point(0)], [I.point(0), I.point(0)]]
    enclosure, _ = exp_range(toy, [I.point(1), I.point(1)], F(1, 2), 20, partial=True)
    alt_lower = sum(((-F(1, 2)) ** k / __import__("math").factorial(k) for k in range(1, 22, 2)), F(0))
    alt_lower += sum(((-F(1, 2)) ** k / __import__("math").factorial(k) for k in range(0, 22, 2)), F(0))
    # The full Taylor polynomial plus the validated geometric tail must cover
    # the exact exponential; the partial interval also contains tau=0.
    assert enclosure[0].lo <= alt_lower and enclosure[0].hi >= 1
    assert enclosure[1] == I.point(1)
    passed.append({"fixture": "partial_slab_signed_matrix_flow_and_tail", "status": "PASS"})

    # Branch checks: strict interior passes, exact corner and corner-crossing do not.
    assert I(F(-1, 2), F(3, 4)).abs_upper() < 1
    assert not I(F(-1), F(1)).abs_upper() < 1
    assert not I(F(9, 10), F(101, 100)).abs_upper() < 1
    passed.append({"fixture": "clip_corner_and_crossing_fail_closed", "status": "PASS"})
    return passed


def main() -> int:
    results = run()
    print(json.dumps({"schema": "G2_W2_NONQUERY_FIXTURES_v1", "count": len(results), "results": results}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
