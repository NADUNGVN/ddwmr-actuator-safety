"""21-coordinate augmented DDWMR right-hand side with Auer clip derivatives.

This evaluator is a local mathematical preflight for the derivative extension.
It uses the shared exact-rational interval and parameter-map code. It is not an
ODE integrator, and its output is not a validated trajectory tube.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

from validation.g2.interval import interval_cosine, interval_sine
from validation.g2.model import build_model
from validation.g2.rational import Budget, Interval, InvalidInput, parse_q

from .piecewise import DualInterval


PHYSICAL_STATES = ("p_x", "p_y", "theta", "u", "r", "omega_L", "omega_R", "i_L", "i_R")


def _param_dual(raw: Any, labels: dict[str, DualInterval], dimension: int, budget: Budget) -> DualInterval:
    if not isinstance(raw, dict):
        raise InvalidInput("parameter expressions must be objects")
    if set(raw) == {"const"}:
        q = parse_q(raw["const"], budget)
        return DualInterval.constant(Interval.point(q, budget), dimension)
    if set(raw) == {"var"}:
        name = raw["var"]
        if not isinstance(name, str) or name not in labels:
            raise InvalidInput("parameter expression refers to an undeclared label")
        return labels[name]
    if set(raw) != {"op", "args"} or raw.get("op") not in {"add", "sub", "mul", "div"}:
        raise InvalidInput("unsupported rational parameter expression")
    args = raw["args"]
    if not isinstance(args, list) or len(args) != 2:
        raise InvalidInput("binary parameter expression must have two operands")
    a = _param_dual(args[0], labels, dimension, budget)
    b = _param_dual(args[1], labels, dimension, budget)
    return {"add": lambda: a + b, "sub": lambda: a - b,
            "mul": lambda: a * b, "div": lambda: a / b}[raw["op"]]()


def _dual_sin(value: DualInterval, degree: int) -> DualInterval:
    derivative = interval_cosine(value.value, degree)
    return DualInterval(interval_sine(value.value, degree), tuple(derivative * item for item in value.gradient))


def _dual_cos(value: DualInterval, degree: int) -> DualInterval:
    derivative = -interval_sine(value.value, degree)
    return DualInterval(interval_cosine(value.value, degree), tuple(derivative * item for item in value.gradient))


def augmented_rhs(
    benchmark: dict[str, Any], state_box: list[Any], voltage: list[Any], budget: Budget,
    trig_degree: int = 18,
) -> tuple[list[DualInterval], dict[str, Any]]:
    """Evaluate f and interval Jacobian over nine states plus twelve fixed labels.

    The parameter coordinates are included in the differentiation domain so
    a future mean-value implementation can retain the same fixed labels. Their
    ODE components are exactly zero; this function never switches them in time.
    """
    model = build_model(benchmark, budget)  # validates the rational image and positivity witnesses
    if not isinstance(state_box, list) or len(state_box) != 9:
        raise InvalidInput("the Auer baseline adapter requires exactly nine physical state intervals")
    if not isinstance(voltage, list) or len(voltage) != 2:
        raise InvalidInput("held voltage must have two rational components")
    if trig_degree < 1:
        raise InvalidInput("trigonometric Taylor degree must be positive")

    states_i = [Interval.from_json(pair, budget) for pair in state_box]
    n_state, labels_order = len(states_i), model.parameter_label_order
    n_total = n_state + len(labels_order)
    labels: dict[str, DualInterval] = {}
    for index, name in enumerate(labels_order):
        labels[name] = DualInterval.variable(model.parameter_label_box[name], n_total, n_state + index)
    state = [DualInterval.variable(value, n_total, index) for index, value in enumerate(states_i)]
    param_raw = benchmark["fixed_parameters"]
    params = {name: _param_dual(expr, labels, n_total, budget) for name, expr in param_raw.items()}
    V = [parse_q(value, budget) for value in voltage]
    V_max = parse_q(benchmark["V_max"], budget)
    if any(abs(value) > V_max for value in V):
        raise InvalidInput("held voltage lies outside the declared voltage box")
    held = [DualInterval.constant(Interval.point(value, budget), n_total) for value in V]

    px, py, theta, u, r, omega_l, omega_r, current_l, current_r = state
    sin_theta, cos_theta = _dual_sin(theta, trig_degree), _dual_cos(theta, trig_degree)
    slip_l = params["R_w"] * omega_l - (u - params["b"] * r)
    slip_r = params["R_w"] * omega_r - (u + params["b"] * r)
    force_l = params["C_L"] * (slip_l / params["v_s"]).clip()
    force_r = params["C_R"] * (slip_r / params["v_s"]).clip()

    rhs = [
        u * cos_theta,
        u * sin_theta,
        r,
        (force_l + force_r - params["c_u"] * u) / params["m"],
        (params["b"] * (force_r - force_l) - params["c_r"] * r) / params["I_z"],
        (params["k_L"] * current_l - params["B_L"] * omega_l - params["R_w"] * force_l) / params["J_L"],
        (params["k_R"] * current_r - params["B_R"] * omega_r - params["R_w"] * force_r) / params["J_R"],
        (held[0] - params["R_L"] * current_l - params["k_L"] * omega_l) / params["L_L"],
        (held[1] - params["R_R"] * current_r - params["k_R"] * omega_r) / params["L_R"],
    ]
    zero = Interval.point(Fraction(0), budget)
    rhs.extend(DualInterval.constant(zero, n_total) for _ in labels_order)
    if len(rhs) != 21 or any(item.dimension != 21 for item in rhs):
        raise RuntimeError("augmented RHS construction did not produce 21 coordinates")

    diagnostics = {
        "physical_state_coordinates": list(PHYSICAL_STATES),
        "label_order": labels_order,
        "augmented_dimension": n_total,
        "label_derivatives_identically_zero": all(
            item.value.lo == item.value.hi == 0
            and all(part.lo == part.hi == 0 for part in item.gradient)
            for item in rhs[n_state:]
        ),
        "parameter_image_positive_witnesses_checked": True,
        "formal_ode_only_contact_domain_not_checked_here": True,
        "trigonometric_backend": "shared validation.g2.interval Taylor enclosure with rational remainder",
        "arithmetic_backend": "shared exact rational Interval/Budget; no floating-point rounding",
    }
    return rhs, diagnostics

