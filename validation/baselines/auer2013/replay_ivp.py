"""Independent replay checker for R4 native residual/Picard proof records.

This module does not import the proof producer. It reconstructs the clip law,
the 21-coordinate RHS/Jacobian, every residual iteration, the integrated tube,
and every endpoint from the frozen inputs. It intentionally shares only the
project's exact-rational interval primitives and Taylor transcendental bounds.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from validation.g2.interval import interval_cosine, interval_sine
from validation.g2.rational import Budget, Interval, InvalidInput, ResourceLimit, parse_q, qobj


PROOF_SCHEMA = "ddwmr-g4-auer-native-residual-proof-v1"
METHOD_ID = "AUER2013_PIECEWISE_RESIDUAL_RECONSTRUCTION_DDWMR_R4"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _interval(raw: Any, budget: Budget) -> Interval:
    return Interval.from_json(raw, budget)


def _vector(raw: Any, budget: Budget) -> list[Interval]:
    if not isinstance(raw, list):
        raise InvalidInput("expected serialized interval vector")
    return [_interval(item, budget) for item in raw]


def _vec_json(values: list[Interval]) -> list[Any]:
    return [item.to_json() for item in values]


def _sum_vectors(a: list[Interval], b: list[Interval]) -> list[Interval]:
    if len(a) != len(b):
        raise InvalidInput("interval vector dimensions differ")
    return [x + y for x, y in zip(a, b)]


def _subset(a: Interval, b: Interval) -> bool:
    a._same(b)
    return b.lo <= a.lo and a.hi <= b.hi


def _vector_subset(a: list[Interval], b: list[Interval]) -> bool:
    return len(a) == len(b) and all(_subset(x, y) for x, y in zip(a, b))


def _same_serialized(actual: Any, expected: Any, where: str) -> None:
    if actual != expected:
        raise InvalidInput(f"replayed field differs: {where}")


def _integral_error(r0: list[Interval], d: list[Interval], h: Fraction, budget: Budget) -> list[Interval]:
    if len(r0) != len(d) or h <= 0:
        raise InvalidInput("invalid residual integral dimensions or width")
    time_range = Interval(Fraction(0), h, budget)
    return [x + time_range * y for x, y in zip(r0, d)]


def _endpoint_error(r0: list[Interval], d: list[Interval], h: Fraction, budget: Budget) -> list[Interval]:
    time = Interval.point(h, budget)
    return [x + time * y for x, y in zip(r0, d)]


def _clip_range(value: Interval) -> Interval:
    return Interval(max(Fraction(-1), min(Fraction(1), value.lo)),
                    max(Fraction(-1), min(Fraction(1), value.hi)), value.budget)


def _clip_generalized_derivative(value: Interval) -> Interval:
    if value.hi < -1 or value.lo > 1:
        return Interval.point(Fraction(0), value.budget)
    if value.lo > -1 and value.hi < 1:
        return Interval.point(Fraction(1), value.budget)
    return Interval(Fraction(0), Fraction(1), value.budget)


@dataclass(frozen=True)
class _AD:
    value: Interval
    gradient: tuple[Interval, ...]

    def _coerce(self, other: Any) -> "_AD":
        if isinstance(other, _AD):
            if other.value.budget is not self.value.budget or len(other.gradient) != len(self.gradient):
                raise InvalidInput("independent checker AD shape/budget mismatch")
            return other
        value = other if isinstance(other, Interval) else Interval.point(Fraction(other), self.value.budget)
        if value.budget is not self.value.budget:
            raise InvalidInput("independent checker interval budget mismatch")
        zero = Interval.point(Fraction(0), self.value.budget)
        return _AD(value, (zero,) * len(self.gradient))

    @classmethod
    def variable(cls, value: Interval, dimension: int, index: int) -> "_AD":
        zero = Interval.point(Fraction(0), value.budget)
        one = Interval.point(Fraction(1), value.budget)
        grad = [zero for _ in range(dimension)]
        grad[index] = one
        return cls(value, tuple(grad))

    @classmethod
    def constant(cls, value: Interval, dimension: int) -> "_AD":
        zero = Interval.point(Fraction(0), value.budget)
        return cls(value, (zero,) * dimension)

    def __add__(self, other: Any) -> "_AD":
        rhs = self._coerce(other)
        return _AD(self.value + rhs.value, tuple(a + b for a, b in zip(self.gradient, rhs.gradient)))

    def __radd__(self, other: Any) -> "_AD":
        return self + other

    def __neg__(self) -> "_AD":
        return _AD(-self.value, tuple(-item for item in self.gradient))

    def __sub__(self, other: Any) -> "_AD":
        return self + (-self._coerce(other))

    def __rsub__(self, other: Any) -> "_AD":
        return self._coerce(other) - self

    def __mul__(self, other: Any) -> "_AD":
        rhs = self._coerce(other)
        return _AD(self.value * rhs.value, tuple(
            a * rhs.value + self.value * b for a, b in zip(self.gradient, rhs.gradient)
        ))

    def __rmul__(self, other: Any) -> "_AD":
        return self * other

    def reciprocal(self) -> "_AD":
        inverse = self.value.reciprocal()
        factor = -(inverse * inverse)
        return _AD(inverse, tuple(factor * item for item in self.gradient))

    def __truediv__(self, other: Any) -> "_AD":
        return self * self._coerce(other).reciprocal()

    def __rtruediv__(self, other: Any) -> "_AD":
        return self._coerce(other) * self.reciprocal()

    def clip(self) -> "_AD":
        slope = _clip_generalized_derivative(self.value)
        return _AD(_clip_range(self.value), tuple(slope * part for part in self.gradient))

    def sin(self, degree: int) -> "_AD":
        derivative = interval_cosine(self.value, degree)
        return _AD(interval_sine(self.value, degree), tuple(derivative * part for part in self.gradient))

    def cos(self, degree: int) -> "_AD":
        derivative = -interval_sine(self.value, degree)
        return _AD(interval_cosine(self.value, degree), tuple(derivative * part for part in self.gradient))


def _parameter_ad(raw: Any, labels: dict[str, _AD], dimension: int, budget: Budget) -> _AD:
    if not isinstance(raw, dict):
        raise InvalidInput("invalid fixed parameter expression")
    if set(raw) == {"const"}:
        return _AD.constant(Interval.point(parse_q(raw["const"], budget), budget), dimension)
    if set(raw) == {"var"}:
        name = raw["var"]
        if not isinstance(name, str) or name not in labels:
            raise InvalidInput("parameter expression refers to an undeclared fixed label")
        return labels[name]
    if set(raw) != {"op", "args"} or raw.get("op") not in {"add", "sub", "mul", "div"}:
        raise InvalidInput("unsupported rational parameter expression")
    args = raw["args"]
    if not isinstance(args, list) or len(args) != 2:
        raise InvalidInput("fixed parameter expression must be binary")
    a = _parameter_ad(args[0], labels, dimension, budget)
    b = _parameter_ad(args[1], labels, dimension, budget)
    if raw["op"] == "add":
        return a + b
    if raw["op"] == "sub":
        return a - b
    if raw["op"] == "mul":
        return a * b
    return a / b


def _independent_rhs(
    benchmark: dict[str, Any], physical_state: list[Interval], label_box: dict[str, Interval],
    voltage: list[Any], budget: Budget, trig_degree: int, rhs_eval_counter: dict[str, int] | None = None,
) -> tuple[list[Interval], list[list[Interval]]]:
    """Re-evaluate the model and AD locally, without importing the producer RHS."""
    if rhs_eval_counter is not None:
        limit = rhs_eval_counter.get("limit")
        if limit is not None and rhs_eval_counter.get("count", 0) >= limit:
            raise ResourceLimit(
                "RHS_JACOBIAN_EVALUATION_LIMIT",
                f"combined RHS/Jacobian evaluation cap {limit} reached before checker evaluation",
            )
        rhs_eval_counter["count"] = rhs_eval_counter.get("count", 0) + 1
    if len(physical_state) != 9:
        raise InvalidInput("checker expects nine DDWMR state coordinates")
    names = [item["name"] for item in benchmark.get("parameter_labels", [])]
    if len(names) != 12 or set(names) != set(label_box):
        raise InvalidInput("checker requires exactly the complete twelve-label image")
    dim = 21
    state = [_AD.variable(value, dim, i) for i, value in enumerate(physical_state)]
    labels = {
        name: _AD.variable(label_box[name], dim, 9 + i) for i, name in enumerate(names)
    }
    params = {
        name: _parameter_ad(expr, labels, dim, budget)
        for name, expr in benchmark["fixed_parameters"].items()
    }
    positive = {"m", "I_z", "R_w", "b", "v_s", "J_L", "J_R", "L_L", "L_R", "R_L", "R_R", "k_L", "k_R", "C_L", "C_R"}
    nonnegative = {"c_u", "c_r", "B_L", "B_R"}
    if any(params[name].value.lo <= 0 for name in positive):
        raise InvalidInput("checker found a nonpositive parameter image")
    if any(params[name].value.lo < 0 for name in nonnegative):
        raise InvalidInput("checker found a negative damping image")
    V = [parse_q(value, budget) for value in voltage]
    Vmax = parse_q(benchmark["V_max"], budget)
    if len(V) != 2 or any(abs(value) > Vmax for value in V):
        raise InvalidInput("checker rejected the held voltage")
    held = [_AD.constant(Interval.point(value, budget), dim) for value in V]
    px, py, theta, u, r, omega_l, omega_r, current_l, current_r = state
    sin_theta, cos_theta = theta.sin(trig_degree), theta.cos(trig_degree)
    slip_l = params["R_w"] * omega_l - u + params["b"] * r
    slip_r = params["R_w"] * omega_r - u - params["b"] * r
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
    rhs.extend(_AD.constant(zero, dim) for _ in names)
    return [item.value for item in rhs], [list(item.gradient) for item in rhs]


def _expected_binding(
    *, input_path: str, input_sha256: str, method_sha256: str, backend_sha256: str,
    profile_sha256: str, snapshot_sha256: str, solver_sha256: str, checker_sha256: str,
) -> dict[str, Any]:
    return {
        "input_path": input_path,
        "input_sha256": input_sha256,
        "method_contract_path": "docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md",
        "method_contract_sha256": method_sha256,
        "arithmetic_backend_manifest_path": "validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v2.json",
        "arithmetic_backend_manifest_sha256": backend_sha256,
        "resource_profile_path": "validation/baselines/auer2013/small_case_resource_profile_v2.json",
        "resource_profile_sha256": profile_sha256,
        "source_snapshot_manifest_sha256": snapshot_sha256,
        "solver_source_sha256": solver_sha256,
        "checker_source_sha256": checker_sha256,
        "arithmetic_dependency": "shared validation.g2 exact Fraction/Interval/Budget and Taylor sin/cos; separately disclosed and not an independent arithmetic library",
    }


def _verify_analytic(
    proof: dict[str, Any], fixture: dict[str, Any], budget: Budget,
) -> None:
    if proof.get("case_id") != fixture.get("fixture_id") or proof.get("case_kind") != "ANALYTIC_CLIP_BRANCH_CROSSING":
        raise InvalidInput("analytic proof is bound to a different fixture")
    t_end = Fraction(int(fixture["time_interval"]["end"]["num"]), int(fixture["time_interval"]["end"]["den"]))
    start_raw = fixture["initial_state"]
    start = [_interval(row, budget) for row in start_raw]
    midpoint_x = budget.div(budget.add(start[0].lo, start[0].hi), Fraction(2))
    midpoint_y = budget.div(budget.add(start[1].lo, start[1].hi), Fraction(2))
    crossing = budget.add(Fraction(1), -midpoint_x)
    app_end_x = budget.add(midpoint_x, t_end)
    app_end_y = budget.add(t_end, -budget.div(budget.pow(crossing, 2), Fraction(2)))
    app = [Interval(midpoint_x, app_end_x, budget), Interval(midpoint_y, app_end_y, budget)]
    error0 = [
        Interval(budget.add(start[0].lo, -midpoint_x), budget.add(start[0].hi, -midpoint_x), budget),
        Interval(budget.add(start[1].lo, -midpoint_y), budget.add(start[1].hi, -midpoint_y), budget),
    ]
    d0 = [Interval.point(Fraction(0), budget), Interval(Fraction(-1), Fraction(1), budget)]
    r0 = _integral_error(error0, d0, t_end, budget)
    rough = _sum_vectors(app, r0)
    c_value = _clip_range(rough[0])
    c_derivative = _clip_generalized_derivative(rough[0])
    app_rhs = [Interval.point(Fraction(1), budget), _clip_range(app[0])]
    app_dot = [Interval.point(Fraction(1), budget), _clip_range(app[0])]
    zero = Interval.point(Fraction(0), budget)
    jac = [[zero, zero], [c_derivative, zero]]
    correction = [zero, jac[1][0] * r0[0] + jac[1][1] * r0[1]]
    d1 = correction
    d_in = _vector_subset(d1, d0)
    r1 = _integral_error(error0, d1, t_end, budget)
    r_in = _vector_subset(r1, r0)
    end_error = _endpoint_error(error0, d1, t_end, budget)
    endpoint = [Interval.point(app_end_x, budget) + end_error[0], Interval.point(app_end_y, budget) + end_error[1]]
    tube = _sum_vectors(app, r1)
    switch_interval = [Fraction(1) - start[0].hi, Fraction(1) - start[0].lo]
    expected_iteration = {
        "iteration": 1,
        "previous_residual_derivative": _vec_json(d0),
        "old_full_time_remainder": _vec_json(r0),
        "clip_input_interval": rough[0].to_json(),
        "clip_value_interval": c_value.to_json(),
        "clip_generalized_derivative": c_derivative.to_json(),
        "active_switches": [
            {"switch": qobj(Fraction(-1)), "intersects": rough[0].lo <= -1 <= rough[0].hi},
            {"switch": qobj(Fraction(1)), "intersects": rough[0].lo <= 1 <= rough[0].hi},
        ],
        "switch_time_interval_from_initial_box": [qobj(item) for item in switch_interval],
        "rhs_on_approximate_path": _vec_json(app_rhs),
        "approximate_path_derivative": _vec_json(app_dot),
        "residual_base": _vec_json([zero, zero]),
        "interval_jacobian": [[item.to_json() for item in row] for row in jac],
        "jacobian_times_old_remainder": _vec_json(correction),
        "new_residual_derivative": _vec_json(d1),
        "derivative_inclusion_componentwise": d_in,
        "new_full_time_remainder": _vec_json(r1),
        "remainder_inclusion_componentwise": r_in,
        "accepted": d_in and r_in,
    }
    expected_step = {
        "step_index": 0,
        "time_closed": {"start": qobj(Fraction(0)), "end": qobj(t_end)},
        "state_order": ["x", "y"],
        "approximate_path": {
            "kind": "EXACT_RATIONAL_PIECEWISE_C1",
            "x": {"formula": "xmid+t", "xmid": qobj(midpoint_x)},
            "y": {
                "formula": "xmid*t+t^2/2 for t<=1-xmid; t-(1-xmid)^2/2 for t>=1-xmid",
                "xmid": qobj(midpoint_x), "switch_time": qobj(crossing), "y0": qobj(midpoint_y),
            },
            "derivative_range": _vec_json(app_dot),
            "full_time_range": _vec_json(app),
        },
        "initial_enclosure": _vec_json(start),
        "initial_error": _vec_json(error0),
        "rough_domain": _vec_json(rough),
        "residual_iterations": [expected_iteration],
        "inclusion": {
            "criterion": "Rdot_next([0,h]) subset Rdot_current([0,h]) and the integrated residual tube maps into the previous compact convex rough tube",
            "derivative_subset_pass": d_in,
            "integrated_tube_subset_pass": r_in,
            "compact_convex_rough_domain": True,
            "closed_time_coverage": True,
            "status": "PASS" if d_in and r_in else "NOT_ESTABLISHED",
        },
        "full_time_total_hull": _vec_json(tube),
        "endpoint_start": _vec_json(start),
        "endpoint_end": _vec_json(endpoint),
        "exact_reference_containment": {
            "full_time_reference": fixture["exact_full_time_reference"],
            "endpoint_reference": fixture["exact_endpoint_reference"],
            "switch_time_reference": fixture["analytic_switch_time"],
        },
        "work": {"picard_iterations": 1, "clip_branch_splits": 0, "rhs_jacobian_evaluations": 0},
    }
    _same_serialized(proof.get("time_horizon"), {"start": qobj(Fraction(0)), "end": qobj(t_end)}, "analytic horizon")
    _same_serialized(proof.get("initial_state"), _vec_json(start), "analytic initial state")
    _same_serialized(proof.get("step_records"), [expected_step], "analytic residual proof step")
    _same_serialized(proof.get("global_full_time_hull"), _vec_json(tube), "analytic global tube")
    _same_serialized(proof.get("global_endpoint"), _vec_json(endpoint), "analytic endpoint")
    references = [_interval(row, budget) for row in fixture["exact_full_time_reference"]]
    end_refs = [_interval(row, budget) for row in fixture["exact_endpoint_reference"]]
    if not _vector_subset(references, tube) or not _vector_subset(end_refs, endpoint):
        raise InvalidInput("analytic exact-reference containment does not replay")
    if proof.get("exact_reference_containment_pass") is not True or proof.get("status") != "PROOF_COMPLETE":
        raise InvalidInput("analytic proof is not complete or reference containment is false")


def _verify_ddwmr(
    proof: dict[str, Any], case: dict[str, Any], benchmark: dict[str, Any], profile: dict[str, Any], budget: Budget,
    rhs_eval_counter: dict[str, int],
) -> int:
    if proof.get("case_kind") != "DDWMR_SINGLE_QUERY" or proof.get("query_id") != case.get("query_id"):
        raise InvalidInput("native DDWMR proof is bound to a different query")
    names = [item["name"] for item in benchmark["parameter_labels"]]
    labels0 = {name: _interval(case["fixed_labels"][name], budget) for name in names}
    initial = [_interval(row, budget) for row in case["initial_state"]]
    horizon = parse_q(case["horizon"], budget)
    _same_serialized(proof.get("query_action_binding"), {
        "candidate_manifest_v2_input_sha256": case["candidate_manifest_v2_input_sha256"],
        "benchmark_sha256": case["benchmark_sha256"],
        "state_order": case["state_order"],
        "initial_state": case["initial_state"],
        "fixed_labels": {name: labels0[name].to_json() for name in names},
        "held_voltage": case["held_voltage"],
        "horizon": case["horizon"],
        "scene": case["scene"],
    }, "DDWMR query/action binding")
    _same_serialized(proof.get("initial_state"), _vec_json(initial), "DDWMR initial state")
    _same_serialized(proof.get("time_horizon"), {"start": qobj(Fraction(0)), "end": qobj(horizon)}, "DDWMR horizon")

    steps = proof.get("step_records")
    if not isinstance(steps, list) or not steps:
        raise InvalidInput("DDWMR proof has no accepted residual steps")
    current_time = Fraction(0)
    current_state = initial
    current_labels = dict(labels0)
    total_rhs_evals = 0
    total_picard_iterations = 0
    trig_degree = int(profile["transcendental_profile"]["sine_taylor_degree"])
    for step_index, step in enumerate(steps):
        t_start = parse_q(step["time_closed"]["start"], budget)
        t_end = parse_q(step["time_closed"]["end"], budget)
        h = t_end - t_start
        if t_start != current_time or h <= 0:
            raise InvalidInput("DDWMR closed step slabs have a gap, overlap, or nonpositive width")
        start_aug = current_state + [current_labels[name] for name in names]
        _same_serialized(step.get("initial_enclosure_augmented"), _vec_json(start_aug), f"step {step_index} initial enclosure")
        center = [budget.div(budget.add(item.lo, item.hi), Fraction(2)) for item in start_aug]
        point_labels = {name: Interval.point(center[9 + i], budget) for i, name in enumerate(names)}
        point_state = [Interval.point(item, budget) for item in center[:9]]
        rhs_center, _ = _independent_rhs(benchmark, point_state, point_labels, case["held_voltage"], budget, trig_degree, rhs_eval_counter)
        slope = [budget.div(budget.add(rhs_center[i].lo, rhs_center[i].hi), Fraction(2)) for i in range(9)] + [Fraction(0)] * 12
        time_range = Interval(Fraction(0), h, budget)
        app_range = [Interval.point(center[i], budget) + time_range.scale(slope[i]) for i in range(9)]
        app_range.extend(Interval.point(center[i], budget) for i in range(9, 21))
        r_init = [
            Interval(budget.add(item.lo, -center[i]), budget.add(item.hi, -center[i]), budget)
            for i, item in enumerate(start_aug)
        ]
        rhs_start, _ = _independent_rhs(benchmark, current_state, current_labels, case["held_voltage"], budget, trig_degree, rhs_eval_counter)
        seed = []
        for i in range(9):
            left = budget.add(rhs_start[i].lo, -slope[i])
            right = budget.add(rhs_start[i].hi, -slope[i])
            radius = budget.add(max(abs(left), abs(right)), Fraction(1))
            seed.append(Interval(-radius, radius, budget))
        seed.extend(Interval.point(Fraction(0), budget) for _ in names)
        _same_serialized(step.get("approximate_path"), {
            "kind": "LINEAR_RATIONAL_CENTER_SLOPE",
            "center": [qobj(item) for item in center],
            "slope": [qobj(item) for item in slope],
            "full_time_range": _vec_json(app_range),
        }, f"step {step_index} approximate path")
        _same_serialized(step.get("initial_error"), _vec_json(r_init), f"step {step_index} initial error")
        _same_serialized(step.get("residual_seed"), _vec_json(seed), f"step {step_index} residual seed")

        app_rhs, _ = _independent_rhs(benchmark, app_range[:9], point_labels, case["held_voltage"], budget, trig_degree, rhs_eval_counter)
        total_rhs_evals += 3
        base = [app_rhs[i] - Interval.point(slope[i], budget) for i in range(9)]
        base.extend(Interval.point(Fraction(0), budget) for _ in names)
        derivative_old = seed
        iteration_records = step.get("residual_iterations")
        if not isinstance(iteration_records, list) or not iteration_records:
            raise InvalidInput("DDWMR step omits residual derivative iterations")
        accepted = False
        accepted_d = accepted_r = None
        for iteration_index, recorded in enumerate(iteration_records, start=1):
            total_picard_iterations += 1
            old_r = _integral_error(r_init, derivative_old, h, budget)
            rough = _sum_vectors(app_range, old_r)
            rough_labels = {name: rough[9 + i] for i, name in enumerate(names)}
            rhs_rough, jacobian = _independent_rhs(
                benchmark, rough[:9], rough_labels, case["held_voltage"], budget, trig_degree, rhs_eval_counter,
            )
            total_rhs_evals += 1
            correction = []
            for row in jacobian:
                value = Interval.point(Fraction(0), budget)
                for coefficient, error in zip(row, old_r):
                    value = value + coefficient * error
                correction.append(value)
            derivative_new = _sum_vectors(base, correction)
            derivative_subset = _vector_subset(derivative_new, derivative_old)
            remainder_new = _integral_error(r_init, derivative_new, h, budget)
            remainder_subset = _vector_subset(remainder_new, old_r)
            is_accepted = derivative_subset and remainder_subset
            expected_iter = {
                "iteration": iteration_index,
                "previous_residual_derivative": _vec_json(derivative_old),
                "old_full_time_remainder": _vec_json(old_r),
                "rough_domain": _vec_json(rough),
                "rhs_on_approximate_path": _vec_json(app_rhs),
                "approximate_path_derivative": _vec_json([Interval.point(item, budget) for item in slope]),
                "residual_base": _vec_json(base),
                "interval_rhs_on_rough_domain": _vec_json(rhs_rough),
                "interval_jacobian": [[item.to_json() for item in row] for row in jacobian],
                "jacobian_times_old_remainder": _vec_json(correction),
                "new_residual_derivative": _vec_json(derivative_new),
                "derivative_inclusion_componentwise": derivative_subset,
                "new_full_time_remainder": _vec_json(remainder_new),
                "remainder_inclusion_componentwise": remainder_subset,
                "accepted": is_accepted,
            }
            _same_serialized(recorded, expected_iter, f"step {step_index} Picard iteration {iteration_index}")
            if is_accepted:
                if iteration_index != len(iteration_records):
                    raise InvalidInput("DDWMR proof continues after an accepted Picard inclusion")
                accepted = True
                accepted_d, accepted_r = derivative_new, remainder_new
                break
            derivative_old = derivative_new
        if not accepted or accepted_d is None or accepted_r is None:
            raise InvalidInput("DDWMR accepted step lacks a verified Picard inclusion")
        _same_serialized(step.get("rough_domain"), iteration_records[-1]["rough_domain"], f"step {step_index} final rough domain")
        _same_serialized(step.get("residual_derivative_accepted"), _vec_json(accepted_d), f"step {step_index} accepted derivative")
        _same_serialized(step.get("integrated_remainder_accepted"), _vec_json(accepted_r), f"step {step_index} integrated remainder")
        endpoint_err = _endpoint_error(r_init, accepted_d, h, budget)
        app_end = [Interval.point(center[i] + h * slope[i], budget) for i in range(21)]
        endpoint_end = _sum_vectors(app_end, endpoint_err)
        full_tube = _sum_vectors(app_range, accepted_r)
        expected_inclusion = {
            "criterion": "componentwise residual-derivative inclusion and induced integrated-tube inclusion on a compact convex box",
            "derivative_subset_pass": True,
            "integrated_tube_subset_pass": True,
            "compact_convex_rough_domain": True,
            "closed_time_coverage": True,
            "status": "PASS",
        }
        _same_serialized(step.get("inclusion"), expected_inclusion, f"step {step_index} inclusion record")
        _same_serialized(step.get("full_time_total_hull_augmented"), _vec_json(full_tube), f"step {step_index} full-time tube")
        _same_serialized(step.get("endpoint_start_augmented"), _vec_json(start_aug), f"step {step_index} endpoint start")
        _same_serialized(step.get("endpoint_end_augmented"), _vec_json(endpoint_end), f"step {step_index} endpoint end")
        if any(endpoint_end[9 + i].lo != labels0[name].lo or endpoint_end[9 + i].hi != labels0[name].hi for i, name in enumerate(names)):
            raise InvalidInput("fixed parameter labels changed during the held-input execution")
        current_state = endpoint_end[:9]
        current_labels = {name: endpoint_end[9 + i] for i, name in enumerate(names)}
        current_time = t_end
    if current_time != horizon:
        raise InvalidInput("DDWMR proof does not cover the full closed hold")
    final = _vec_json(current_state)
    _same_serialized(proof.get("global_endpoint"), final, "DDWMR global endpoint")
    hulls = [step["full_time_total_hull_augmented"][:9] for step in steps]
    _same_serialized(proof.get("global_full_time_hulls"), hulls, "DDWMR global full-time hulls")
    if proof.get("status") != "PROOF_COMPLETE":
        raise InvalidInput("DDWMR native record does not claim a complete proof")
    if rhs_eval_counter["count"] > int(profile["max_rhs_jacobian_evaluations_per_ivp"]):
        raise InvalidInput("independent replay exceeded the frozen RHS/Jacobian evaluation cap")
    return rhs_eval_counter["count"]


def replay_native_proof(
    envelope: dict[str, Any], *, case: dict[str, Any], benchmark: dict[str, Any] | None,
    profile: dict[str, Any], fixture: dict[str, Any] | None,
    expected_binding: dict[str, Any], budget: Budget,
    rhs_eval_counter: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Replay an outer proof envelope and reject all changed proof premises."""
    if rhs_eval_counter is None:
        rhs_eval_counter = {
            "count": 0,
            "limit": int(profile["max_rhs_jacobian_evaluations_per_ivp"]),
        }
    elif "limit" not in rhs_eval_counter:
        rhs_eval_counter["limit"] = int(profile["max_rhs_jacobian_evaluations_per_ivp"])
    rhs_before = rhs_eval_counter.get("count", 0)
    if not isinstance(envelope, dict) or set(envelope) != {"proof", "proof_sha256"}:
        return {"replayed": False, "reason": "invalid_native_envelope"}
    proof = envelope["proof"]
    if not isinstance(proof, dict) or proof.get("schema") != PROOF_SCHEMA or proof.get("method_id") != METHOD_ID:
        return {"replayed": False, "reason": "invalid_native_schema_or_method"}
    if envelope.get("proof_sha256") != canonical_sha256(proof):
        return {"replayed": False, "reason": "native_proof_digest_mismatch"}
    try:
        if proof.get("binding") != expected_binding:
            raise InvalidInput("native source/profile/input binding does not match frozen artifacts")
        rhs_evaluations = 0
        if proof.get("case_kind") == "ANALYTIC_CLIP_BRANCH_CROSSING":
            if fixture is None:
                raise InvalidInput("analytic fixture input is unavailable")
            _verify_analytic(proof, fixture, budget)
        elif proof.get("case_kind") == "DDWMR_SINGLE_QUERY":
            if benchmark is None:
                raise InvalidInput("DDWMR benchmark is unavailable")
            rhs_evaluations = _verify_ddwmr(proof, case, benchmark, profile, budget, rhs_eval_counter)
        else:
            raise InvalidInput("unsupported native proof case kind")
    except ResourceLimit as exc:
        return {
            "replayed": False,
            "reason": "resource_limit",
            "termination": {"kind": exc.kind, "detail": exc.detail},
            "work": {
                "rational_operations": budget.operations,
                "rational_operation_attempts": budget.operation_attempts,
                "max_observed_rational_bits": budget.max_seen_bits,
                "rhs_jacobian_replay_evaluations": rhs_eval_counter.get("count", 0) - rhs_before,
                "rhs_jacobian_combined_count": rhs_eval_counter.get("count", 0),
            },
            "rational_budget_failure_context": budget.failure_context,
        }
    except (InvalidInput, KeyError, TypeError, ValueError, ZeroDivisionError, IndexError) as exc:
        return {
            "replayed": False,
            "reason": "proof_premise_mismatch",
            "detail": str(exc),
            "work": {
                "rational_operations": budget.operations,
                "rational_operation_attempts": budget.operation_attempts,
                "max_observed_rational_bits": budget.max_seen_bits,
                "rhs_jacobian_replay_evaluations": rhs_eval_counter.get("count", 0) - rhs_before,
                "rhs_jacobian_combined_count": rhs_eval_counter.get("count", 0),
            },
            "rational_budget_failure_context": budget.failure_context,
        }
    return {
        "replayed": True,
        "native_status": proof["status"],
        "proof_sha256": envelope["proof_sha256"],
        "steps_replayed": len(proof["step_records"]),
        "rhs_jacobian_replay_evaluations": rhs_eval_counter.get("count", 0) - rhs_before,
        "rhs_jacobian_combined_count": rhs_eval_counter.get("count", 0),
        "work": {
            "rational_operations": budget.operations,
            "rational_operation_attempts": budget.operation_attempts,
            "max_observed_rational_bits": budget.max_seen_bits,
        },
        "shared_exact_arithmetic_source": "validation.g2.rational and validation.g2.interval",
        "rhs_jacobian_replay": "independent local interval AD implementation; producer RHS source not imported",
    }
