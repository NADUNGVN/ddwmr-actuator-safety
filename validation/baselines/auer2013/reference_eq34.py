"""Exact reproduction of the scalar reference illustration in Auer et al. §4.1."""

from __future__ import annotations

from fractions import Fraction

from validation.g2.rational import Budget, Interval


def reproduce(budget: Budget) -> dict:
    # Paper Eq. (34): f(x)=x for x<0, and f(x)=2x+2 for x>0.
    X = Interval(Fraction(-1), Fraction(2), budget)
    x0 = Fraction(-1, 2)
    f_x0 = Fraction(-1, 2)
    actual_range_closure = Interval(Fraction(-1), Fraction(6), budget)

    # The continuous-function derivative rule (Eq. (33)) gives [1,2].
    smooth_derivative_hull = Interval(Fraction(1), Fraction(2), budget)
    displacement = X - Interval.point(x0, budget)
    naive_mva = Interval.point(f_x0, budget) + smooth_derivative_hull * displacement

    # Eq. (35), x0 on the left of c0=0, with the jump g=2.  The crossing
    # portion uses g/([0,2]-x0) + hull({1},{2}), then hulls this with the
    # left-branch derivative {1}.
    right_part = Interval(Fraction(0), Fraction(2), budget)
    gap = Fraction(2)
    right_displacement = right_part - Interval.point(x0, budget)
    jump_quotient = Interval.point(gap, budget) / right_displacement
    branch_derivative_hull = Interval(Fraction(1), Fraction(2), budget)
    corrected_derivative = Interval(
        min(Fraction(1), (jump_quotient + branch_derivative_hull).lo),
        max(Fraction(1), (jump_quotient + branch_derivative_hull).hi),
        budget,
    )
    corrected_mva = Interval.point(f_x0, budget) + corrected_derivative * displacement

    return {
        "schema": "auer2013-reference-eq34-reproduction-v1",
        "reference": "Auer, Kiel & Rauh (2013), §4.1, Eqs. (34)-(35), p. 741",
        "function_branches": {"left": "x", "right": "2*x+2", "switch": "0"},
        "domain": X.to_json(),
        "reference_point": {"num": str(x0.numerator), "den": str(x0.denominator)},
        "actual_range_closure": actual_range_closure.to_json(),
        "smooth_rule_derivative": smooth_derivative_hull.to_json(),
        "smooth_rule_mean_value_enclosure": naive_mva.to_json(),
        "smooth_rule_contains_actual_range": (
            naive_mva.lo <= actual_range_closure.lo and actual_range_closure.hi <= naive_mva.hi
        ),
        "jump": {"num": "2", "den": "1"},
        "jump_quotient_interval": jump_quotient.to_json(),
        "auer_eq35_derivative_enclosure": corrected_derivative.to_json(),
        "auer_eq35_mean_value_enclosure": corrected_mva.to_json(),
        "auer_eq35_contains_actual_range": (
            corrected_mva.lo <= actual_range_closure.lo and actual_range_closure.hi <= corrected_mva.hi
        ),
        "exact_paper_reported_failure": "[-3/2,9/2] does not contain the function range [-1,6]",
        "scope_note": "This is the paper's scalar formula illustration, not its §5 friction/hysteresis simulation or a DDWMR trajectory.",
    }

