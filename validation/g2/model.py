"""Interval parameter maps and the v2.1 six-state matrix decomposition."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from .polynomial import RationalFunction, parse_expression, rational_functions_equal
from .rational import Budget, Interval, InvalidInput, parse_q


PARAMETER_NAMES = [
    "m", "I_z", "R_w", "b", "v_s", "c_u", "c_r",
    "J_L", "J_R", "B_L", "B_R", "L_L", "L_R", "R_L", "R_R",
    "k_L", "k_R", "C_L", "C_R",
]
POSITIVE_PARAMETERS = {
    "m", "I_z", "R_w", "b", "v_s", "J_L", "J_R", "L_L", "L_R",
    "R_L", "R_R", "k_L", "k_R", "C_L", "C_R",
}
NONNEGATIVE_PARAMETERS = {"c_u", "c_r", "B_L", "B_R"}


@dataclass
class ModelIntervals:
    parameters: dict[str, Interval]
    A: list[list[Interval]]
    B: list[list[Interval]]
    D: list[list[Interval]]
    S: list[list[Interval]]
    QF: list[list[Interval]]
    scales: list[Fraction]
    parameter_label_order: list[str]
    parameter_label_box: dict[str, Interval]


def _positive_constant(value: Fraction, budget: Budget) -> Interval:
    if value <= 0:
        raise InvalidInput("coordinate scaling entries must be positive")
    return Interval.point(value, budget)


def _mat_zero(rows: int, cols: int, budget: Budget) -> list[list[Interval]]:
    return [[Interval.point(Fraction(0), budget) for _ in range(cols)] for _ in range(rows)]


def _mul(a: Interval, b: Interval) -> Interval:
    return a * b


def _div(a: Interval, b: Interval) -> Interval:
    return a / b


def _abs(value: Interval) -> Interval:
    if value.lo >= 0:
        return value
    if value.hi <= 0:
        return -value
    return Interval(Fraction(0), value.abs_upper(), value.budget)


def _scale_matrix(A: list[list[Interval]], left: list[Fraction], right: list[Fraction]) -> list[list[Interval]]:
    out = []
    for i, row in enumerate(A):
        out_row = []
        for j, value in enumerate(row):
            factor = value.budget.div(right[j], left[i])
            out_row.append(value.scale(factor))
        out.append(out_row)
    return out


def _checked_parameter_images(raw: dict[str, Any], budget: Budget) -> tuple[dict[str, Interval], list[str], dict[str, Interval]]:
    labels = raw.get("parameter_labels")
    cell = raw.get("parameter_cell")
    maps = raw.get("fixed_parameters")
    if not isinstance(labels, list) or not isinstance(cell, dict) or not isinstance(maps, dict):
        raise InvalidInput("missing parameter-label or parameter-map declarations")
    if any(not isinstance(item, dict) or set(item) != {"name", "range"} or not isinstance(item.get("name"), str) for item in labels):
        raise InvalidInput("each parameter-label declaration needs a string name and a rational range")
    label_order = [item["name"] for item in labels]
    if len(label_order) != len(labels) or len(set(label_order)) != len(label_order):
        raise InvalidInput("parameter labels must have unique names")
    label_box_raw = cell.get("labels")
    if not isinstance(label_box_raw, dict) or set(label_box_raw) != set(label_order):
        raise InvalidInput("parameter cell does not cover exactly the declared labels")
    label_box = {name: Interval.from_json(label_box_raw[name], budget) for name in label_order}
    if any(label_box[name].lo != Interval.from_json(item["range"], budget).lo or label_box[name].hi != Interval.from_json(item["range"], budget).hi
           for name in label_order for item in labels if item["name"] == name):
        raise InvalidInput("parameter cell bounds differ from the declared full label domain")
    variables = [label_box[name] for name in label_order]

    if set(maps) != set(PARAMETER_NAMES):
        missing = sorted(set(PARAMETER_NAMES) - set(maps))
        extra = sorted(set(maps) - set(PARAMETER_NAMES))
        raise InvalidInput(f"parameter map mismatch; missing={missing}, extra={extra}")
    functions: dict[str, RationalFunction] = {}
    values: dict[str, Interval] = {}
    for name in PARAMETER_NAMES:
        functions[name] = parse_expression(maps[name], label_order, label_box, budget)
        values[name] = functions[name].evaluate(variables)
        if name in POSITIVE_PARAMETERS and values[name].lo <= 0:
            raise InvalidInput(f"parameter {name} lacks a positive lower-bound witness")
        if name in NONNEGATIVE_PARAMETERS and values[name].lo < 0:
            raise InvalidInput(f"parameter {name} lacks a nonnegative lower-bound witness")

    _check_gear_witness(raw.get("gear_witness"), functions, label_order, label_box, budget)
    return values, label_order, label_box


def _check_gear_witness(
    raw: Any,
    functions: dict[str, RationalFunction],
    label_order: list[str],
    label_box: dict[str, Interval],
    budget: Budget,
) -> None:
    if not isinstance(raw, dict) or set(raw) != {"L", "R"}:
        raise InvalidInput("ideal gear witness must be supplied for both sides")
    vars_box = [label_box[name] for name in label_order]
    dim = len(label_order)
    for side in ("L", "R"):
        item = raw[side]
        required = {"n", "k_motor", "J_wheel", "J_motor", "B_wheel", "B_motor"}
        if not isinstance(item, dict) or set(item) != required:
            raise InvalidInput(f"incomplete ideal gear witness on side {side}")
        witness = {name: parse_expression(item[name], label_order, label_box, budget) for name in required}
        bounds = {name: witness[name].evaluate(vars_box) for name in required}
        for name in ("n", "k_motor", "J_wheel", "J_motor"):
            if bounds[name].lo <= 0:
                raise InvalidInput(f"gear witness {side}.{name} must be strictly positive")
        for name in ("B_wheel", "B_motor"):
            if bounds[name].lo < 0:
                raise InvalidInput(f"gear witness {side}.{name} must be nonnegative")
        n = witness["n"]
        n2 = n * n
        checks = [
            (functions[f"k_{side}"], n * witness["k_motor"], "k=n*k_motor"),
            (functions[f"J_{side}"], witness["J_wheel"] + n2 * witness["J_motor"], "J=J_wheel+n^2*J_motor"),
            (functions[f"B_{side}"], witness["B_wheel"] + n2 * witness["B_motor"], "B=B_wheel+n^2*B_motor"),
        ]
        for actual, expected, relation in checks:
            if not rational_functions_equal(actual, expected):
                raise InvalidInput(f"gear witness failed exact {relation} identity on side {side}")


def build_model(raw: dict[str, Any], budget: Budget) -> ModelIntervals:
    p, label_order, label_box = _checked_parameter_images(raw, budget)
    scaling_raw = raw.get("coordinate_scaling", [
        {"num": "1", "den": "1"} for _ in range(6)
    ])
    if not isinstance(scaling_raw, list) or len(scaling_raw) != 6:
        raise InvalidInput("coordinate_scaling must contain six positive rationals")
    scales = [parse_q(value, budget) for value in scaling_raw]
    for value in scales:
        if value <= 0:
            raise InvalidInput("coordinate scaling entries must be positive")

    zero = lambda: Interval.point(Fraction(0), budget)
    one = lambda: Interval.point(Fraction(1), budget)
    A = _mat_zero(6, 6, budget)
    B = _mat_zero(6, 2, budget)
    D = _mat_zero(6, 2, budget)
    S = _mat_zero(2, 6, budget)
    A[0][0] = -_div(p["c_u"], p["m"])
    A[1][1] = -_div(p["c_r"], p["I_z"])
    A[2][2] = -_div(p["B_L"], p["J_L"])
    A[2][4] = _div(p["k_L"], p["J_L"])
    A[3][3] = -_div(p["B_R"], p["J_R"])
    A[3][5] = _div(p["k_R"], p["J_R"])
    A[4][2] = -_div(p["k_L"], p["L_L"])
    A[4][4] = -_div(p["R_L"], p["L_L"])
    A[5][3] = -_div(p["k_R"], p["L_R"])
    A[5][5] = -_div(p["R_R"], p["L_R"])
    B[4][0] = one() / p["L_L"]
    B[5][1] = one() / p["L_R"]

    D[0][0] = one() / p["m"]
    D[0][1] = one() / p["m"]
    D[1][0] = -p["b"] / p["I_z"]
    D[1][1] = p["b"] / p["I_z"]
    D[2][0] = -p["R_w"] / p["J_L"]
    D[3][1] = -p["R_w"] / p["J_R"]
    S[0][0] = Interval.point(Fraction(-1), budget)
    S[0][1] = p["b"]
    S[0][2] = p["R_w"]
    S[1][0] = Interval.point(Fraction(-1), budget)
    S[1][1] = -p["b"]
    S[1][3] = p["R_w"]

    scale_intervals = [_positive_constant(value, budget) for value in scales]
    inverse_scales = [Interval.point(budget.div(Fraction(1), value), budget) for value in scales]
    A_tilde = _scale_matrix(A, scales, scales)
    B_tilde = _scale_matrix(B, scales, [Fraction(1), Fraction(1)])
    D_tilde = _scale_matrix(D, scales, [Fraction(1), Fraction(1)])
    S_tilde = [[S[i][j] * scale_intervals[j] for j in range(6)] for i in range(2)]

    law = raw.get("law")
    if not isinstance(law, dict) or law.get("name") != "clip":
        raise InvalidInput("only the explicitly represented clip law is supported")
    L_phi = parse_q(law.get("L_phi"), budget)
    if L_phi != 1:
        raise InvalidInput("clip profile requires certified L_phi=1")
    QF = _mat_zero(2, 6, budget)
    for side_index, side in enumerate(("L", "R")):
        coefficient = p[f"C_{side}"] / p["v_s"]
        for j in range(6):
            QF[side_index][j] = _abs(S_tilde[side_index][j]) * coefficient

    return ModelIntervals(p, A_tilde, B_tilde, D_tilde, S_tilde, QF, scales, label_order, label_box)


def physical_internal_box(scaled: list[Interval], scales: list[Fraction]) -> list[Interval]:
    return [item.scale(scale) for item, scale in zip(scaled, scales)]


def physical_radius(scaled: list[Fraction], scales: list[Fraction], budget: Budget) -> list[Fraction]:
    return [budget.mul(radius, scale) for radius, scale in zip(scaled, scales)]
