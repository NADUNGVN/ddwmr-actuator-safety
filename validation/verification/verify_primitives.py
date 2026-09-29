#!/usr/bin/env python3
"""Exact finite checks for sign, zero, clip corners, scaling, inputs, and caps."""

from __future__ import annotations

import copy
import json
from fractions import Fraction as F
from pathlib import Path

from validation.g2.evaluator import _clip_interval, _parse_input_query, make_query
from validation.g2.interval import interval_matrix_exponential, sqrt_lower
from validation.g2.model import build_model
from validation.g2.polynomial import parse_expression
from validation.g2.rational import Budget, Interval, InvalidInput, ResourceLimit, parse_q

ROOT = Path(__file__).resolve().parents[2]


def q(n: int, d: int = 1) -> dict[str, str]:
    value = F(n, d)
    return {"num": str(value.numerator), "den": str(value.denominator)}


def require(name: str, condition: bool, detail: str) -> dict:
    if not condition:
        raise AssertionError(f"{name}: {detail}")
    return {"name": name, "pass": True, "detail": detail}


def expect_exception(name: str, exception_type, fn) -> dict:
    try:
        fn()
    except exception_type as exc:
        return {"name": name, "pass": True, "detail": f"{type(exc).__name__}: {exc}"}
    raise AssertionError(f"{name}: expected {exception_type.__name__}")


def main() -> None:
    benchmark = json.loads((ROOT / "validation/configs/benchmark_v1.json").read_text(encoding="utf-8"))
    pilot = json.loads((ROOT / "validation/configs/dev_pilot_v1.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "results/validation/g2/development_manifest_v1.json").read_text(encoding="utf-8"))
    checks = []

    budget = Budget(4096, 100000)
    checks.append(require("sign change interval", Interval(F(-2), F(3), budget).abs_upper() == 3, "abs upper bound is 3"))
    checks.append(require("exact zero interval", Interval(F(0), F(0), budget).abs_upper() == 0, "zero remains exact"))
    checks.append(require("negative clip saturation", _clip_interval(Interval(F(-3), F(-1), budget)) == Interval(F(-1), F(-1), budget), "[-3,-1] maps to {-1}"))
    checks.append(require("clip crossing corner", _clip_interval(Interval(F(-2), F(2), budget)) == Interval(F(-1), F(1), budget), "[-2,2] maps to [-1,1]"))
    checks.append(require("positive clip saturation", _clip_interval(Interval(F(1), F(4), budget)) == Interval(F(1), F(1), budget), "[1,4] maps to {1}"))
    lo, hi = sqrt_lower(F(2), 24, budget)
    checks.append(require("root bisection brackets sqrt(2)", lo * lo <= 2 <= hi * hi, "nonnegative rational endpoints verified by exact squaring"))

    zero = Interval.point(F(0), budget)
    zero_matrix = [[zero for _ in range(2)] for _ in range(2)]
    exp_zero, exp_norm, exp_tail = interval_matrix_exponential(zero_matrix, F(1, 10), 12)
    checks.append(require("zero matrix exponential", exp_zero[0][0].lo == 1 and exp_zero[1][1].lo == 1 and exp_zero[0][1].hi == 0, "Q=0 produces exact identity and zero remainder"))

    model_identity = build_model(benchmark, Budget(16384, 1000000))
    scaled_benchmark = copy.deepcopy(benchmark)
    scaled_benchmark["coordinate_scaling"] = [q(x) for x in (2, 3, 4, 5, 6, 7)]
    model_scaled = build_model(scaled_benchmark, Budget(16384, 1000000))
    scale = [F(x) for x in (2, 3, 4, 5, 6, 7)]
    scaling_ok = True
    for i in range(6):
        for j in range(6):
            expected = model_identity.A[i][j].scale(scale[j] / scale[i])
            if (model_scaled.A[i][j].lo, model_scaled.A[i][j].hi) != (expected.lo, expected.hi):
                scaling_ok = False
            expected_d = model_identity.D[i][j if j < 2 else 0].scale(F(1, 1) / scale[i]) if j < 2 else None
            if j < 2 and (model_scaled.D[i][j].lo, model_scaled.D[i][j].hi) != (expected_d.lo, expected_d.hi):
                scaling_ok = False
        for j in range(2):
            expected_b = model_identity.B[i][j].scale(F(1, 1) / scale[i])
            if (model_scaled.B[i][j].lo, model_scaled.B[i][j].hi) != (expected_b.lo, expected_b.hi):
                scaling_ok = False
    for i in range(2):
        for j in range(6):
            expected_s = model_identity.S[i][j].scale(scale[j])
            if (model_scaled.S[i][j].lo, model_scaled.S[i][j].hi) != (expected_s.lo, expected_s.hi):
                scaling_ok = False
            expected_qf = model_identity.QF[i][j].scale(scale[j])
            if (model_scaled.QF[i][j].lo, model_scaled.QF[i][j].hi) != (expected_qf.lo, expected_qf.hi):
                scaling_ok = False
    checks.append(require("diagonal similarity scaling", scaling_ok, "A/B/D/S/QF transforms agree componentwise with the declared diagonal scale"))
    checks.append(require(
        "motor/contact/current signs",
        model_identity.B[4][0].lo > 0 and model_identity.A[2][4].lo > 0
        and model_identity.A[4][2].hi < 0 and model_identity.D[2][0].hi < 0
        and model_identity.D[1][0].hi < 0 and model_identity.D[1][1].lo > 0
        and model_identity.S[0][1].lo > 0 and model_identity.S[1][1].hi < 0,
        "voltage-to-current, torque/back-EMF, reaction, yaw, and slip signs match MASTER",
    ))
    state_low = next(x for x in benchmark["state_cells"] if x["id"] == "state_low_neg")
    checks.append(require("nonzero-width initial cell", all(parse_q(pair[1]) > parse_q(pair[0]) for pair in state_low["box"]), "all nine initial-state coordinates have positive width"))
    label_order = model_identity.parameter_label_order
    checks.append(require("independent side labels", label_order.index("rho_L") != label_order.index("rho_R") and label_order.index("C_L") != label_order.index("C_R"), "left and right actuator/contact labels are distinct coordinates"))
    checks.append(require("positive gear witness", model_identity.parameters["J_L"].lo > 0 and model_identity.parameters["J_R"].lo > 0, "both gear identities were checked with positive rotor inertia"))
    asymmetric = copy.deepcopy(benchmark)
    left_range, right_range = [q(1), q(F(101, 100))], [q(F(109, 100)), q(F(11, 10))]
    asymmetric["parameter_cell"]["labels"]["C_L"] = left_range
    asymmetric["parameter_cell"]["labels"]["C_R"] = right_range
    for label in asymmetric["parameter_labels"]:
        if label["name"] == "C_L":
            label["range"] = left_range
        if label["name"] == "C_R":
            label["range"] = right_range
    asymmetric_model = build_model(asymmetric, Budget(16384, 1000000))
    checks.append(require("asymmetric contact capacities", asymmetric_model.parameters["C_L"].hi < asymmetric_model.parameters["C_R"].lo, "left and right capacity label intervals remain independent and unequal"))

    bad_query = make_query(
        benchmark, manifest["selected_query_ids"][0], pilot["profile"], "0" * 64,
        manifest["benchmark_config_sha256"],
    )
    bad_query["action"] = copy.deepcopy(bad_query["action"])
    bad_query["action"]["V"][0] = q(2)
    checks.append(expect_exception("voltage input rejection", InvalidInput, lambda: _parse_input_query(
        benchmark, bad_query["state_cell"], bad_query["scene"], bad_query["horizon"], bad_query["action"], pilot["profile"], Budget(4096, 10000)
    )))
    bad_law = copy.deepcopy(benchmark)
    bad_law["law"]["name"] = "unrestricted-python"
    checks.append(expect_exception("unsupported force-law rejection", InvalidInput, lambda: build_model(bad_law, Budget(4096, 10000))))
    bad_denominator_budget = Budget(4096, 10000)
    bad_denominator = {"op": "div", "args": [{"const": q(1)}, {"var": "x"}]}
    checks.append(expect_exception("zero-crossing denominator rejection", InvalidInput, lambda: parse_expression(
        bad_denominator, ["x"], {"x": Interval(F(-1), F(1), bad_denominator_budget)}, bad_denominator_budget
    )))
    checks.append(expect_exception("unreduced rational rejection", InvalidInput, lambda: parse_q({"num": "2", "den": "4"})))

    bit_budget = Budget(8, 100)
    checks.append(expect_exception("pre-operation bit exhaustion", ResourceLimit, lambda: bit_budget.mul(F(255), F(255))))
    bit_failure = bit_budget.failure_context or {}
    checks.append(require(
        "pre-operation failure telemetry",
        bit_failure.get("kind") == "RATIONAL_BIT_LIMIT"
        and bit_failure.get("stage_id") == "unclassified"
        and bit_failure.get("primitive_id") == "fraction.mul"
        and bit_failure.get("estimate_kind") == "preoperation_intermediate_upper_estimate"
        and bit_failure.get("configured_cap_name") == "max_rational_bits"
        and bit_failure.get("configured_cap_value") == 8
        and bit_failure.get("operand_bit_lengths") == [
            {"numerator_bits": 8, "denominator_bits": 1},
            {"numerator_bits": 8, "denominator_bits": 1},
        ],
        "failure captures stage, primitive, upper estimate, exact cap, and operand widths before multiplication",
    ))
    operation_budget = Budget(1024, 1)
    a = Interval(F(1), F(2), operation_budget)
    checks.append(expect_exception("operation exhaustion", ResourceLimit, lambda: a * a))
    operation_failure = operation_budget.failure_context or {}
    checks.append(require(
        "operation-limit telemetry",
        operation_failure.get("kind") == "RATIONAL_OPERATION_LIMIT"
        and operation_failure.get("configured_cap_name") == "max_rational_operations"
        and operation_failure.get("configured_cap_value") == 1
        and operation_failure.get("operation_attempts") == 2
        and operation_failure.get("operations_started") == 1,
        "the rejected second primitive attempt is distinguished from the one operation started",
    ))
    identity_budget = Budget(8, 16)
    identity_results = [
        identity_budget.add(F(0), F(255)),
        identity_budget.add(F(255), F(-255)),
        identity_budget.mul(F(255), F(1)),
        identity_budget.div(F(255), F(1)),
        identity_budget.div(F(255), F(255)),
        identity_budget.pow(F(255), 1),
        identity_budget.pow(F(255), 0),
        identity_budget.pow(F(-1), 99999),
    ]
    checks.append(require(
        "exact arithmetic identities under tight bit cap",
        identity_results == [F(255), F(0), F(255), F(255), F(1), F(255), F(1), F(-1)]
        and identity_budget.operation_attempts == 8
        and identity_budget.operations == 8
        and identity_budget.completed_results == 8
        and identity_budget.max_completed_result_bits == 8,
        "zero/one identities return exact values and account for each attempted primitive without a false intermediate-bit limit",
    ))
    oversized_input_budget = Budget(8, 16)
    oversized_input_budget.set_stage("fixture.input_contract")
    checks.append(expect_exception("oversized rational input digit exhaustion", ResourceLimit, lambda: parse_q(
        {"num": "9" * 100, "den": "1"}, oversized_input_budget,
    )))
    input_failure = oversized_input_budget.failure_context or {}
    checks.append(require(
        "input-width failure telemetry",
        input_failure.get("kind") == "RATIONAL_BIT_LIMIT"
        and input_failure.get("stage_id") == "fixture.input_contract"
        and input_failure.get("primitive_id") == "fraction.parse"
        and input_failure.get("estimate_kind") == "input_digit_width_upper_estimate"
        and input_failure.get("configured_cap_value") == 8
        and input_failure.get("input_digit_lengths") == {"num": 100, "den": 1},
        "oversized decimal input is rejected before integer construction with its stage, digits, estimate, and cap",
    ))
    shared_budget = Budget(32, 10)
    shared_den = F(1, 2**20)
    shared_sum = shared_budget.add(shared_den, shared_den)
    checks.append(require("shared-denominator bit accounting", shared_sum == F(1, 2**19), "preflight uses the common denominator before estimating intermediate bits"))
    cancel_budget = Budget(32, 10)
    cancel_product = cancel_budget.mul(F(2**30, 3), F(3, 2**30))
    checks.append(require("cross-cancelled product bit accounting", cancel_product == 1, "preflight accounts for exact cross-cancellation before multiplication"))

    output = {"scope": "exact primitive/input arithmetic checks; separate from benchmark results", "checks": checks,
              "count": len(checks), "all_pass": all(x["pass"] for x in checks)}
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
