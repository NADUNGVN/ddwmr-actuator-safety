"""Analytic fixtures for outward dyadic rational interval operations; no task rows."""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from .rational_interval_v3 import Budget, I, activate, configure_fixed_grid, q, sqrt_lower


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/validation/autonomous_w2/g2/fixtures/fixed_grid_arithmetic_v3.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contains(interval: I, value: Fraction) -> bool:
    return interval.lo <= value <= interval.hi


def run() -> dict[str, Any]:
    if OUT.exists():
        raise FileExistsError("FIXED_GRID_FIXTURE_OUTPUT_ALREADY_EXISTS")
    configure_fixed_grid(96, 16384, 20)
    budget = Budget(100000, 16384)
    activate(budget)
    try:
        thirds = I.point(Fraction(1, 3))
        a = I(Fraction(-1, 3), Fraction(2, 7))
        b = I(Fraction(1, 5), Fraction(4, 3))
        summed = a + b
        product = a * b
        reciprocal = I(Fraction(1, 3), Fraction(2, 3)).reciprocal()
        root = sqrt_lower(Fraction(2, 3), 48)
        checks = {
            "rational_input_enclosed_after_quantization": contains(thirds, Fraction(1, 3)),
            "non_dyadic_point_expands_exactly_one_grid_cell": thirds.width() == Fraction(1, 1 << 96),
            "lower_and_upper_endpoints_are_on_declared_grid": all(
                (x * (1 << 96)).denominator == 1
                for interval in (thirds, a, b, summed, product, reciprocal)
                for x in (interval.lo, interval.hi)
            ),
            "addition_contains_exact_endpoint_extrema": summed.lo <= Fraction(-1, 3) + Fraction(1, 5)
            and summed.hi >= Fraction(2, 7) + Fraction(4, 3),
            "multiplication_contains_all_four_exact_corner_products": all(
                contains(product, x * y)
                for x in (Fraction(-1, 3), Fraction(2, 7))
                for y in (Fraction(1, 5), Fraction(4, 3))
            ),
            "reciprocal_contains_exact_positive_endpoint_images": contains(reciprocal, Fraction(3, 2))
            and contains(reciprocal, Fraction(3, 1)),
            "sqrt_result_is_a_valid_lower_witness": root * root <= Fraction(2, 3),
        }
        try:
            I(Fraction(-1), Fraction(1)).reciprocal()
            checks["zero_crossing_reciprocal_rejected"] = False
        except ZeroDivisionError as exc:
            checks["zero_crossing_reciprocal_rejected"] = str(exc) == "INTERVAL_DIVISOR_CONTAINS_ZERO"
    finally:
        activate(None)
    result = {
        "schema": "G2_W2_FIXED_GRID_ARITHMETIC_FIXTURES_v3",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "fixture_kind": "analytic rational containment; no benchmark input or task protocol imported",
        "grid_bits": 96,
        "grid_denominator": str(1 << 96),
        "rational_bit_cap": 16384,
        "tail_bit_precheck": {"degree": 20, "upper_bound_bits": (96 + 8) * 22 + 8 * 22},
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "budget": {"operations": budget.operations, "max_observed_bits": budget.max_observed_bits, "rounded_endpoint_count": budget.rounded_endpoint_count, "rounding_events": budget.rounding_events},
        "source_sha256": {
            "validation/autonomous_w2/g2/rational_interval_v3.py": sha(ROOT / "validation/autonomous_w2/g2/rational_interval_v3.py"),
            "validation/autonomous_w2/g2/fixed_grid_arithmetic_fixtures_v3.py": sha(Path(__file__)),
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    if not result["all_checks_pass"]:
        raise AssertionError("FIXED_GRID_ARITHMETIC_FIXTURE_FAILED")
    return result


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
