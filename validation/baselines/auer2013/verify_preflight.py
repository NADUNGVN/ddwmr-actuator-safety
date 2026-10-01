"""Targeted checks for the clip derivative layer and scalar reference case."""

from __future__ import annotations

import argparse
import copy
import json
import platform
import sys
import time
from fractions import Fraction as F
from pathlib import Path

from validation.g2.rational import Budget, Interval, InvalidInput

from .piecewise import (
    DualInterval,
    clip_derivative_interval,
    clip_mean_value_record,
    contains,
    verify_clip_mean_value_record,
)
from .reference_eq34 import reproduce
from .rhs import augmented_rhs


ROOT = Path(__file__).resolve().parents[3]


def require(name: str, condition: bool, detail: str) -> dict:
    if not condition:
        raise AssertionError(f"{name}: {detail}")
    return {"name": name, "pass": True, "detail": detail}


def expect_exception(name: str, expected: type[BaseException], function) -> dict:
    try:
        function()
    except expected as exc:
        return {"name": name, "pass": True, "detail": f"{type(exc).__name__}: {exc}"}
    raise AssertionError(f"{name}: expected {expected.__name__}")


def interval_pair(value: Interval) -> tuple[F, F]:
    return value.lo, value.hi


def main() -> None:
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", default="validation/configs/benchmark_v1.json")
    parser.add_argument("--output", default="results/validation/g4/auer2013/clip_preflight_checks_v1.json")
    parser.add_argument("--reference-output", default="results/validation/g4/auer2013/reference_eq34_reproduction_v1.json")
    args = parser.parse_args()
    benchmark_path, output_path, reference_path = (ROOT / args.benchmark, ROOT / args.output, ROOT / args.reference_output)
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    checks: list[dict] = []
    budget = Budget(16384, 1000000)

    cases = [
        ("strict_negative_saturation", F(-3), F(-2), F(0), F(0)),
        ("strict_linear_branch", F(-1, 2), F(1, 2), F(1), F(1)),
        ("touch_negative_threshold", F(-2), F(-1), F(0), F(1)),
        ("touch_positive_threshold", F(1), F(2), F(0), F(1)),
        ("cross_negative_threshold", F(-2), F(0), F(0), F(1)),
        ("cross_positive_threshold", F(0), F(2), F(0), F(1)),
        ("cross_both_thresholds", F(-2), F(2), F(0), F(1)),
        ("point_at_negative_threshold", F(-1), F(-1), F(0), F(1)),
        ("point_at_positive_threshold", F(1), F(1), F(0), F(1)),
    ]
    branch_results = []
    for name, lo, hi, d_lo, d_hi in cases:
        domain = Interval(lo, hi, budget)
        got = clip_derivative_interval(domain)
        branch_results.append({"name": name, "domain": domain.to_json(), "derivative": got.to_json()})
        checks.append(require(name, interval_pair(got) == (d_lo, d_hi), f"D({domain}) = [{d_lo},{d_hi}]"))

    # Exact finite secant stress grid across both corners and saturated branches.
    secant_count = 0
    secant_domains = [Interval(F(-3), F(3), budget), Interval(F(-2), F(-1), budget),
                      Interval(F(-1), F(1), budget), Interval(F(1), F(2), budget)]
    grid = [F(n, 2) for n in range(-6, 7)]
    for domain in secant_domains:
        points = [x for x in grid if domain.lo <= x <= domain.hi]
        for a in points:
            for b in points:
                record = clip_mean_value_record(domain, a, b)
                if not verify_clip_mean_value_record(record, budget):
                    raise AssertionError(f"exact clip secant inclusion failed on {domain}, a={a}, b={b}")
                secant_count += 1
    checks.append(require(
        "exact rational clip secants",
        secant_count == 212,
        f"{secant_count} ordered rational point pairs checked against D(I)*(a-b)",
    ))

    # The univariate secant inclusion composes through an affine multivariate
    # input: the independent interval Jacobian dot the full coordinate delta
    # contains the function difference for each enumerated pair.
    x1 = Interval(F(-1), F(1), budget)
    x2 = Interval(F(-1), F(1), budget)
    label = Interval(F(0), F(1), budget)
    affine_q = Interval(F(-4), F(4), budget)  # 2*x1 - 3*x2 + label
    slope = clip_derivative_interval(affine_q)
    jac = [slope.scale(F(2)), slope.scale(F(-3)), slope]
    triples = [
        ((F(-1), F(-1), F(0)), (F(1), F(1), F(1))),
        ((F(1), F(-1, 2), F(1, 2)), (F(-1), F(1), F(0))),
        ((F(0), F(0), F(0)), (F(1, 1), F(-1, 1), F(1, 1))),
        ((F(-1, 2), F(1, 2), F(1, 4)), (F(1, 2), F(-1, 2), F(3, 4))),
    ]
    multivariate_ok = True
    for left, right in triples:
        if not (x1.lo <= left[0] <= x1.hi and x2.lo <= left[1] <= x2.hi and label.lo <= left[2] <= label.hi):
            continue
        if not (x1.lo <= right[0] <= x1.hi and x2.lo <= right[1] <= x2.hi and label.lo <= right[2] <= label.hi):
            continue
        q_left = 2 * left[0] - 3 * left[1] + left[2]
        q_right = 2 * right[0] - 3 * right[1] + right[2]
        diff = F(max(-1, min(1, q_left)) - max(-1, min(1, q_right)))
        total = Interval.point(F(0), budget)
        for derivative, delta in zip(jac, (a - b for a, b in zip(left, right))):
            total = total + derivative * Interval.point(delta, budget)
        if not total.lo <= diff <= total.hi:
            multivariate_ok = False
    checks.append(require(
        "multivariate affine mean-value inclusion",
        multivariate_ok,
        "independent interval chain-rule row encloses exact clip differences for all declared state/label pairs",
    ))

    # Shared outward arithmetic is exact rational interval arithmetic here.
    a = Interval(F(1, 3), F(2, 3), budget)
    b = Interval(F(3, 5), F(5, 7), budget)
    product = a * b
    checks.append(require(
        "outward rational interval arithmetic",
        interval_pair(product) == (F(1, 5), F(10, 21)),
        "endpoint products are exact rational bounds; no floating rounding is involved in this layer",
    ))

    state_box = next(row["box"] for row in benchmark["state_cells"] if row["id"] == "state_low_neg")
    rhs, rhs_info = augmented_rhs(benchmark, state_box, [
        {"num": "0", "den": "1"}, {"num": "0", "den": "1"},
    ], Budget(16384, 1000000))
    checks.append(require(
        "21-coordinate fixed-label augmentation",
        len(rhs) == 21 and rhs_info["augmented_dimension"] == 21
        and rhs_info["label_derivatives_identically_zero"]
        and all(item.value.lo == item.value.hi == 0 for item in rhs[9:]),
        "nine physical RHS entries plus twelve exact dot(label)=0 coordinates; positivity witnesses checked",
    ))

    bad_rho = copy.deepcopy(benchmark)
    bad_rho["parameter_cell"]["labels"]["rho_L"] = [
        {"num": "-1", "den": "1"}, {"num": "1", "den": "1"},
    ]
    for row in bad_rho["parameter_labels"]:
        if row["name"] == "rho_L":
            row["range"] = bad_rho["parameter_cell"]["labels"]["rho_L"]
    checks.append(expect_exception(
        "positive-denominator/domain rejection",
        InvalidInput,
        lambda: augmented_rhs(bad_rho, state_box, [{"num": "0", "den": "1"}] * 2, Budget(16384, 100000)),
    ))
    checks.append(expect_exception(
        "malformed physical state rejection",
        InvalidInput,
        lambda: augmented_rhs(benchmark, state_box[:-1], [{"num": "0", "den": "1"}] * 2, Budget(16384, 100000)),
    ))
    checks.append(expect_exception(
        "reversed interval rejection",
        InvalidInput,
        lambda: Interval(F(1), F(0), budget),
    ))

    tamper_budget = Budget(4096, 100000)
    valid_record = clip_mean_value_record(Interval(F(-2), F(2), tamper_budget), F(-3, 2), F(1, 2))
    checks.append(require(
        "clip lemma record round-trip",
        verify_clip_mean_value_record(valid_record, Budget(4096, 100000)),
        "the small lemma checker recomputes the exact derivative product and difference",
    ))
    tampered_record = copy.deepcopy(valid_record)
    tampered_record["mean_value_product"] = [
        {"num": "0", "den": "1"}, {"num": "0", "den": "1"},
    ]
    checks.append(require(
        "tampered lemma evidence rejected",
        not verify_clip_mean_value_record(tampered_record, Budget(4096, 100000)),
        "changing a claimed enclosure without changing its derivation is detected",
    ))

    ref_budget = Budget(4096, 100000)
    reference = reproduce(ref_budget)
    actual = Interval.from_json(reference["actual_range_closure"], ref_budget)
    naive = Interval.from_json(reference["smooth_rule_mean_value_enclosure"], ref_budget)
    corrected = Interval.from_json(reference["auer_eq35_mean_value_enclosure"], ref_budget)
    checks.append(require(
        "published Eq. (34) failure reproduced",
        interval_pair(actual) == (F(-1), F(6))
        and interval_pair(naive) == (F(-3, 2), F(9, 2))
        and not reference["smooth_rule_contains_actual_range"],
        "exact output closure [-1,6] is not contained in the paper's naive [-3/2,9/2] mean-value enclosure",
    ))
    checks.append(require(
        "published Eq. (35) correction reproduced",
        interval_pair(Interval.from_json(reference["auer_eq35_derivative_enclosure"], ref_budget)) == (F(1), F(6))
        and contains(corrected, actual)
        and reference["auer_eq35_contains_actual_range"],
        "jump-corrected derivative and resulting mean-value enclosure contain the exact range",
    ))

    report = {
        "schema": "auer2013-targeted-preflight-checks-v1",
        "status": "PASS_FOR_CLIP_EXTENSION_AND_SCALAR_REFERENCE_ONLY",
        "full_valencia_ivp_baseline": "NOT_BUILT_OR_VALIDATED",
        "comparison_queries_run": 0,
        "checks": checks,
        "check_count": len(checks),
        "all_checks_pass": all(row["pass"] for row in checks),
        "branch_cases": branch_results,
        "exact_secant_pairs": secant_count,
        "shared_backend": "validation.g2.rational exact Fraction intervals and Budget",
        "runtime_environment": {
            "python": sys.version,
            "executable": sys.executable,
            "platform": platform.platform(),
        },
        "elapsed_seconds_display_only": round(time.monotonic() - started, 6),
        "limitations": [
            "The local checks do not validate Picard inclusion, full-time ODE tubes, or endpoint propagation.",
            "The local checks do not establish source-faithful VALENCIA-IVP behavior.",
            "No 1,944-query comparison was run.",
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    reference_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    reference_path.write_text(json.dumps(reference, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"output": str(output_path), "reference_output": str(reference_path),
                      "check_count": len(checks), "all_checks_pass": report["all_checks_pass"],
                      "comparison_queries_run": 0}, sort_keys=True))
    if not report["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
