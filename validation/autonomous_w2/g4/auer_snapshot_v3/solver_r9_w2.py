"""Versioned matched-query residual/Picard producer candidate, R9.

The implementation reconstructs the Auer 2013 functional tube and residual
iteration with exact rational intervals.  The benchmark model is evaluated by
the existing exact-rational DDWMR RHS/Jacobian preflight.  This is a disclosed
method reconstruction, not a VALENCIA software reproduction.
"""

from __future__ import annotations

import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from validation.autonomous_w2.g4.auer_snapshot_v3.piecewise import clip_derivative_interval, clip_interval
from validation.autonomous_w2.g4.auer_snapshot_v3.rhs import augmented_rhs
from validation.g2.rational import Budget, Interval, InvalidInput, ResourceLimit, qobj


METHOD_ID = "AUER2013_PIECEWISE_RESIDUAL_RECONSTRUCTION_DDWMR_R4"
PROOF_SCHEMA = "ddwmr-g4-auer-native-residual-proof-v1"
PHYSICAL_ORDER = ("p_x", "p_y", "theta", "u", "r", "omega_L", "omega_R", "i_L", "i_R")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def interval_vector_json(values: list[Interval] | tuple[Interval, ...]) -> list[Any]:
    return [item.to_json() for item in values]


def vector_add(a: list[Interval], b: list[Interval]) -> list[Interval]:
    if len(a) != len(b):
        raise InvalidInput("interval vector size mismatch")
    return [x + y for x, y in zip(a, b)]


def interval_subset(inner: Interval, outer: Interval) -> bool:
    inner._same(outer)
    return outer.lo <= inner.lo and inner.hi <= outer.hi


def vector_subset(inner: list[Interval], outer: list[Interval]) -> bool:
    return len(inner) == len(outer) and all(interval_subset(x, y) for x, y in zip(inner, outer))


def integrated_remainder(initial_error: list[Interval], derivative: list[Interval], h: Fraction, budget: Budget) -> list[Interval]:
    if len(initial_error) != len(derivative) or h <= 0:
        raise InvalidInput("invalid residual integral dimensions or step width")
    time_range = Interval(Fraction(0), h, budget)
    return [r0 + time_range * dr for r0, dr in zip(initial_error, derivative)]


def endpoint_remainder(initial_error: list[Interval], derivative: list[Interval], h: Fraction, budget: Budget) -> list[Interval]:
    if len(initial_error) != len(derivative):
        raise InvalidInput("invalid endpoint residual dimensions")
    time_point = Interval.point(h, budget)
    return [r0 + time_point * dr for r0, dr in zip(initial_error, derivative)]


def validate_matched_input_schema(case: dict[str, Any]) -> None:
    """Check the matched-case version guard without starting proof computation."""
    if not isinstance(case, dict) or case.get("schema") != "ddwmr-g4-auer-matched-query-input-v3-r9":
        raise InvalidInput("unsupported versioned matched-query input schema")


def _seed_record(
    *, case_kind: str, case_id: str, input_path: Path, input_sha256: str,
    method_sha256: str, backend_sha256: str, profile_sha256: str,
    snapshot_sha256: str, solver_sha256: str, checker_sha256: str,
    resource_profile_path: str,
) -> dict[str, Any]:
    return {
        "schema": PROOF_SCHEMA,
        "method_id": METHOD_ID,
        "case_kind": case_kind,
        "case_id": case_id,
        "binding": {
            "input_path": input_path.as_posix(),
            "input_sha256": input_sha256,
            "method_contract_path": "docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md",
            "method_contract_sha256": method_sha256,
            "arithmetic_backend_manifest_path": "validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v2.json",
            "arithmetic_backend_manifest_sha256": backend_sha256,
            "resource_profile_path": resource_profile_path,
            "resource_profile_sha256": profile_sha256,
            "source_snapshot_manifest_sha256": snapshot_sha256,
            "solver_source_sha256": solver_sha256,
            "checker_source_sha256": checker_sha256,
            "arithmetic_dependency": "shared validation.g2 exact Fraction/Interval/Budget and Taylor sin/cos; separately disclosed and not an independent arithmetic library",
        },
        "step_records": [],
        "rejected_step_attempts": [],
        "status": "IN_PROGRESS",
    }


def solve_analytic_fixture(
    fixture: dict[str, Any], *, input_path: Path, input_sha256: str,
    method_sha256: str, backend_sha256: str, profile: dict[str, Any], profile_sha256: str,
    snapshot_sha256: str, solver_sha256: str, checker_sha256: str, budget: Budget,
) -> dict[str, Any]:
    """Prove the prescribed branch crossing using one closed residual slab."""
    if fixture.get("schema") != "ddwmr-g4-auer-analytic-branch-crossing-fixture-v1":
        raise InvalidInput("unsupported analytic fixture schema")
    if fixture.get("rhs_id") != "x_prime_1_y_prime_clip_x_minus1_plus1":
        raise InvalidInput("unsupported analytic fixture RHS")
    t0 = Fraction(0)
    t1 = Fraction(
        int(fixture["time_interval"]["end"]["num"]),
        int(fixture["time_interval"]["end"]["den"]),
    )
    h = t1 - t0
    initial = [Interval.from_json(row, budget) for row in fixture["initial_state"]]
    xmid = budget.div(budget.add(initial[0].lo, initial[0].hi), Fraction(2))
    ymid = budget.div(budget.add(initial[1].lo, initial[1].hi), Fraction(2))
    switch = budget.add(Fraction(1), -xmid)

    # Exact non-verified approximate path: x_app=xmid+t and y_app is its
    # exact integral of clip(x_app). It is C1 and crosses +1 at `switch`.
    app_end_x = budget.add(xmid, h)
    app_end_y = budget.add(h, -budget.div(budget.pow(switch, 2), Fraction(2)))
    app_range = [
        Interval(xmid, app_end_x, budget),
        Interval(ymid, app_end_y, budget),
    ]
    initial_error = [
        Interval(budget.add(initial[0].lo, -xmid), budget.add(initial[0].hi, -xmid), budget),
        Interval(budget.add(initial[1].lo, -ymid), budget.add(initial[1].hi, -ymid), budget),
    ]
    # Rdot^0 is the frozen rough seed; the first residual evaluation must
    # contract into it before a tube is accepted.
    previous = [
        Interval.point(Fraction(0), budget),
        Interval(Fraction(-1), Fraction(1), budget),
    ]
    previous_derivative = interval_vector_json(previous)
    old_remainder = integrated_remainder(initial_error, previous, h, budget)
    rough_domain = vector_add(app_range, old_remainder)
    clip_input = rough_domain[0]
    clip_value = clip_interval(clip_input)
    clip_derivative = clip_derivative_interval(clip_input)

    # On this fixture, f(x_app(t))-x_app_dot(t)=0 exactly.  The generalized
    # Jacobian route encloses clip(x_app+R)-clip(x_app) in Dclip(X) * R_x.
    app_rhs = [Interval.point(Fraction(1), budget), clip_interval(app_range[0])]
    app_derivative = [Interval.point(Fraction(1), budget), clip_interval(app_range[0])]
    residual_base = [Interval.point(Fraction(0), budget), Interval.point(Fraction(0), budget)]
    jacobian = [
        [Interval.point(Fraction(0), budget), Interval.point(Fraction(0), budget)],
        [clip_derivative, Interval.point(Fraction(0), budget)],
    ]
    correction = [
        Interval.point(Fraction(0), budget),
        jacobian[1][0] * old_remainder[0] + jacobian[1][1] * old_remainder[1],
    ]
    new_derivative = vector_add(residual_base, correction)
    derivative_inclusion = vector_subset(new_derivative, previous)
    new_remainder = integrated_remainder(initial_error, new_derivative, h, budget)
    remainder_inclusion = vector_subset(new_remainder, old_remainder)
    accepted = derivative_inclusion and remainder_inclusion

    end_remainder = endpoint_remainder(initial_error, new_derivative, h, budget)
    endpoint = [
        Interval.point(app_end_x, budget) + end_remainder[0],
        Interval.point(app_end_y, budget) + end_remainder[1],
    ]
    full_tube = vector_add(app_range, new_remainder)
    switch_interval = [
        Fraction(1) - initial[0].hi,
        Fraction(1) - initial[0].lo,
    ]
    step = {
        "step_index": 0,
        "time_closed": {"start": qobj(t0), "end": qobj(t1)},
        "state_order": ["x", "y"],
        "approximate_path": {
            "kind": "EXACT_RATIONAL_PIECEWISE_C1",
            "x": {"formula": "xmid+t", "xmid": qobj(xmid)},
            "y": {
                "formula": "xmid*t+t^2/2 for t<=1-xmid; t-(1-xmid)^2/2 for t>=1-xmid",
                "xmid": qobj(xmid),
                "switch_time": qobj(switch),
                "y0": qobj(ymid),
            },
            "derivative_range": interval_vector_json(app_derivative),
            "full_time_range": interval_vector_json(app_range),
        },
        "initial_enclosure": interval_vector_json(initial),
        "initial_error": interval_vector_json(initial_error),
        "rough_domain": interval_vector_json(rough_domain),
        "residual_iterations": [{
            "iteration": 1,
            "previous_residual_derivative": previous_derivative,
            "old_full_time_remainder": interval_vector_json(old_remainder),
            "clip_input_interval": clip_input.to_json(),
            "clip_value_interval": clip_value.to_json(),
            "clip_generalized_derivative": clip_derivative.to_json(),
            "active_switches": [
                {"switch": qobj(Fraction(-1)), "intersects": clip_input.lo <= -1 <= clip_input.hi},
                {"switch": qobj(Fraction(1)), "intersects": clip_input.lo <= 1 <= clip_input.hi},
            ],
            "switch_time_interval_from_initial_box": [qobj(item) for item in switch_interval],
            "rhs_on_approximate_path": interval_vector_json(app_rhs),
            "approximate_path_derivative": interval_vector_json(app_derivative),
            "residual_base": interval_vector_json(residual_base),
            "interval_jacobian": [[item.to_json() for item in row] for row in jacobian],
            "jacobian_times_old_remainder": interval_vector_json(correction),
            "new_residual_derivative": interval_vector_json(new_derivative),
            "derivative_inclusion_componentwise": derivative_inclusion,
            "new_full_time_remainder": interval_vector_json(new_remainder),
            "remainder_inclusion_componentwise": remainder_inclusion,
            "accepted": accepted,
        }],
        "inclusion": {
            "criterion": "Rdot_next([0,h]) subset Rdot_current([0,h]) and the integrated residual tube maps into the previous compact convex rough tube",
            "derivative_subset_pass": derivative_inclusion,
            "integrated_tube_subset_pass": remainder_inclusion,
            "compact_convex_rough_domain": True,
            "closed_time_coverage": True,
            "status": "PASS" if accepted else "NOT_ESTABLISHED",
        },
        "full_time_total_hull": interval_vector_json(full_tube),
        "endpoint_start": interval_vector_json(initial),
        "endpoint_end": interval_vector_json(endpoint),
        "exact_reference_containment": {
            "full_time_reference": fixture["exact_full_time_reference"],
            "endpoint_reference": fixture["exact_endpoint_reference"],
            "switch_time_reference": fixture["analytic_switch_time"],
        },
        "work": {"picard_iterations": 1, "clip_branch_splits": 0, "rhs_jacobian_evaluations": 0},
    }
    proof = _seed_record(
        case_kind="ANALYTIC_CLIP_BRANCH_CROSSING", case_id=fixture["fixture_id"],
        input_path=input_path, input_sha256=input_sha256,
        method_sha256=method_sha256, backend_sha256=backend_sha256,
        profile_sha256=profile_sha256, snapshot_sha256=snapshot_sha256,
        solver_sha256=solver_sha256, checker_sha256=checker_sha256,
        resource_profile_path="validation/baselines/auer2013/small_case_resource_profile_v2.json",
    )
    proof["time_horizon"] = {"start": qobj(t0), "end": qobj(t1)}
    proof["initial_state"] = interval_vector_json(initial)
    proof["step_records"].append(step)
    proof["global_full_time_hull"] = interval_vector_json(full_tube)
    proof["global_endpoint"] = interval_vector_json(endpoint)
    proof["exact_reference_containment_pass"] = _reference_containment(fixture, full_tube, endpoint, budget)
    proof["status"] = "PROOF_COMPLETE" if accepted and proof["exact_reference_containment_pass"] else "UNKNOWN"
    return proof


def _reference_containment(
    fixture: dict[str, Any], full_tube: list[Interval], endpoint: list[Interval], budget: Budget,
) -> bool:
    full_reference = [Interval.from_json(row, budget) for row in fixture["exact_full_time_reference"]]
    endpoint_reference = [Interval.from_json(row, budget) for row in fixture["exact_endpoint_reference"]]
    return vector_subset(full_reference, full_tube) and vector_subset(endpoint_reference, endpoint)


def _bench_with_labels(benchmark: dict[str, Any], labels: dict[str, Interval]) -> dict[str, Any]:
    updated = copy.deepcopy(benchmark)
    names = [item["name"] for item in updated["parameter_labels"]]
    if set(names) != set(labels):
        raise InvalidInput("label image does not match the benchmark's complete declaration")
    for item in updated["parameter_labels"]:
        item["range"] = labels[item["name"]].to_json()
    updated["parameter_cell"]["labels"] = {name: labels[name].to_json() for name in names}
    return updated


def _call_rhs(
    benchmark: dict[str, Any], state: list[Interval], labels: dict[str, Interval], voltage: list[Any],
    budget: Budget, trig_degree: int,
) -> tuple[list[Interval], list[list[Interval]]]:
    parameterized = _bench_with_labels(benchmark, labels)
    values, _diagnostics = augmented_rhs(
        parameterized, interval_vector_json(state[:9]), voltage, budget, trig_degree=trig_degree,
    )
    rhs_values = [item.value for item in values]
    jacobian = [list(item.gradient) for item in values]
    return rhs_values, jacobian


def _count_rhs_call(counters: dict[str, int], profile: dict[str, Any]) -> None:
    counters["rhs_jacobian_evaluations"] += 1
    if counters["rhs_jacobian_evaluations"] > int(profile["max_rhs_jacobian_evaluations_per_ivp"]):
        raise ResourceLimit("RHS_JACOBIAN_EVALUATION_LIMIT", "frozen RHS/Jacobian evaluation cap exceeded")


def _ddwmr_trial_step(
    *, step_index: int, t0: Fraction, h: Fraction, state_start: list[Interval],
    labels_start: dict[str, Interval], benchmark: dict[str, Any], voltage: list[Any],
    profile: dict[str, Any], budget: Budget, counters: dict[str, int],
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    trig = int(profile["transcendental_profile"]["sine_taylor_degree"])
    dimension = 9 + len(labels_start)
    if dimension != 21:
        raise InvalidInput("DDWMR augmented system must have 21 state and fixed-label coordinates")
    names = [item["name"] for item in benchmark["parameter_labels"]]
    label_vector = [labels_start[name] for name in names]
    start_augmented = state_start + label_vector
    center = [budget.div(budget.add(item.lo, item.hi), Fraction(2)) for item in start_augmented]
    point_labels = {name: Interval.point(center[9 + i], budget) for i, name in enumerate(names)}
    full_labels = {name: labels_start[name] for name in names}
    point_state = [Interval.point(item, budget) for item in center[:9]]

    _count_rhs_call(counters, profile)
    rhs_center, _jac_center = _call_rhs(benchmark, point_state, point_labels, voltage, budget, trig)
    path_slope = [
        budget.div(budget.add(rhs_center[i].lo, rhs_center[i].hi), Fraction(2))
        for i in range(9)
    ] + [Fraction(0)] * 12
    t_range = Interval(Fraction(0), h, budget)
    app_range = [
        Interval.point(center[i], budget) + t_range.scale(path_slope[i])
        for i in range(9)
    ] + [Interval.point(center[i], budget) for i in range(9, 21)]
    initial_error = [
        Interval(budget.add(item.lo, -center[i]), budget.add(item.hi, -center[i]), budget)
        for i, item in enumerate(start_augmented)
    ]

    _count_rhs_call(counters, profile)
    rhs_start, _jac_start = _call_rhs(benchmark, state_start, full_labels, voltage, budget, trig)
    seed: list[Interval] = []
    for i in range(9):
        left = budget.add(rhs_start[i].lo, -path_slope[i])
        right = budget.add(rhs_start[i].hi, -path_slope[i])
        radius = budget.add(max(abs(left), abs(right)), Fraction(1))
        seed.append(Interval(-radius, radius, budget))
    seed.extend(Interval.point(Fraction(0), budget) for _ in range(12))

    _count_rhs_call(counters, profile)
    app_rhs, _app_jac = _call_rhs(benchmark, app_range, point_labels, voltage, budget, trig)
    residual_iterations = []
    derivative_old = seed
    accepted_derivative: list[Interval] | None = None
    accepted_remainder: list[Interval] | None = None
    max_iterations = int(profile["max_picard_iterations_per_step"])
    for iteration in range(1, max_iterations + 1):
        old_remainder = integrated_remainder(initial_error, derivative_old, h, budget)
        rough_domain = vector_add(app_range, old_remainder)
        rough_labels = {name: rough_domain[9 + i] for i, name in enumerate(names)}
        _count_rhs_call(counters, profile)
        rhs_rough, jacobian = _call_rhs(benchmark, rough_domain, rough_labels, voltage, budget, trig)
        if len(jacobian) != dimension or any(len(row) != dimension for row in jacobian):
            raise InvalidInput("RHS Jacobian is not the complete 21 by 21 augmented Jacobian")
        base = [app_rhs[i] - Interval.point(path_slope[i], budget) for i in range(9)]
        base.extend(Interval.point(Fraction(0), budget) for _ in range(12))
        correction = []
        for row in jacobian:
            total = Interval.point(Fraction(0), budget)
            for coefficient, error in zip(row, old_remainder):
                total = total + coefficient * error
            correction.append(total)
        derivative_new = vector_add(base, correction)
        derivative_inclusion = vector_subset(derivative_new, derivative_old)
        remainder_new = integrated_remainder(initial_error, derivative_new, h, budget)
        remainder_inclusion = vector_subset(remainder_new, old_remainder)
        accepted = derivative_inclusion and remainder_inclusion
        residual_iterations.append({
            "iteration": iteration,
            "previous_residual_derivative": interval_vector_json(derivative_old),
            "old_full_time_remainder": interval_vector_json(old_remainder),
            "rough_domain": interval_vector_json(rough_domain),
            "rhs_on_approximate_path": interval_vector_json(app_rhs),
            "approximate_path_derivative": interval_vector_json(
                [Interval.point(item, budget) for item in path_slope]
            ),
            "residual_base": interval_vector_json(base),
            "interval_rhs_on_rough_domain": interval_vector_json(rhs_rough),
            "interval_jacobian": [[item.to_json() for item in row] for row in jacobian],
            "jacobian_times_old_remainder": interval_vector_json(correction),
            "new_residual_derivative": interval_vector_json(derivative_new),
            "derivative_inclusion_componentwise": derivative_inclusion,
            "new_full_time_remainder": interval_vector_json(remainder_new),
            "remainder_inclusion_componentwise": remainder_inclusion,
            "accepted": accepted,
        })
        counters["picard_iterations"] += 1
        if accepted:
            accepted_derivative = derivative_new
            accepted_remainder = remainder_new
            break
        derivative_old = derivative_new

    attempt = {
        "step_index": step_index,
        "time_closed": {"start": qobj(t0), "end": qobj(t0 + h)},
        "step_width": qobj(h),
        "initial_enclosure_augmented": interval_vector_json(start_augmented),
        "approximate_path": {
            "kind": "LINEAR_RATIONAL_CENTER_SLOPE",
            "center": [qobj(item) for item in center],
            "slope": [qobj(item) for item in path_slope],
            "full_time_range": interval_vector_json(app_range),
        },
        "initial_error": interval_vector_json(initial_error),
        "residual_seed": interval_vector_json(seed),
        "residual_iterations": residual_iterations,
    }
    if accepted_derivative is None or accepted_remainder is None:
        return None, {
            "reason": "PICARD_DERIVATIVE_INCLUSION_NOT_ESTABLISHED",
            "attempt": attempt,
            "picard_iteration_limit": max_iterations,
        }

    end_error = endpoint_remainder(initial_error, accepted_derivative, h, budget)
    app_end = [Interval.point(center[i] + h * path_slope[i], budget) for i in range(21)]
    endpoint_end = vector_add(app_end, end_error)
    endpoint_start = start_augmented
    full_tube = vector_add(app_range, accepted_remainder)
    accepted_step = {
        **attempt,
        "rough_domain": residual_iterations[-1]["rough_domain"],
        "residual_derivative_accepted": interval_vector_json(accepted_derivative),
        "integrated_remainder_accepted": interval_vector_json(accepted_remainder),
        "inclusion": {
            "criterion": "componentwise residual-derivative inclusion and induced integrated-tube inclusion on a compact convex box",
            "derivative_subset_pass": residual_iterations[-1]["derivative_inclusion_componentwise"],
            "integrated_tube_subset_pass": residual_iterations[-1]["remainder_inclusion_componentwise"],
            "compact_convex_rough_domain": True,
            "closed_time_coverage": True,
            "status": "PASS",
        },
        "full_time_total_hull_augmented": interval_vector_json(full_tube),
        "endpoint_start_augmented": interval_vector_json(endpoint_start),
        "endpoint_end_augmented": interval_vector_json(endpoint_end),
        "work": {
            "picard_iterations": len(residual_iterations),
            "clip_branch_splits": 0,
            "rhs_jacobian_evaluations": counters["rhs_jacobian_evaluations"],
        },
    }
    return accepted_step, {"reason": "ACCEPTED"}


def _query_action_binding(case: dict[str, Any], current_labels: dict[str, Interval]) -> dict[str, Any]:
    return {
        "candidate_manifest_v2_input_sha256": case["candidate_manifest_v2_input_sha256"],
        "benchmark_sha256": case["benchmark_sha256"],
        "state_order": case["state_order"],
        "initial_state": case["initial_state"],
        "fixed_labels": {name: current_labels[name].to_json() for name in current_labels},
        "held_voltage": case["held_voltage"],
        "horizon": case["horizon"],
        "scene": case["scene"],
    }


def solve_ddwmr_case(
    case: dict[str, Any], benchmark: dict[str, Any], *, input_path: Path, input_sha256: str,
    method_sha256: str, backend_sha256: str, profile: dict[str, Any], profile_sha256: str,
    snapshot_sha256: str, solver_sha256: str, checker_sha256: str,
    resource_profile_path: str, budget: Budget,
) -> dict[str, Any]:
    """Apply the unchanged residual path to one manifest-bound matched query."""
    validate_matched_input_schema(case)
    if case.get("state_order") != list(PHYSICAL_ORDER) or not isinstance(case.get("query_id"), str):
        raise InvalidInput("DDWMR input has an invalid state order or query identity")
    if case.get("benchmark_sha256") != sha256_file(Path(case["benchmark_path"])):
        raise InvalidInput("benchmark bytes do not match the frozen selected input")
    names = [item["name"] for item in benchmark["parameter_labels"]]
    if set(names) != set(case["fixed_labels"]):
        raise InvalidInput("selected query does not bind every benchmark label")
    current_labels = {
        name: Interval.from_json(case["fixed_labels"][name], budget) for name in names
    }
    benchmark_labels = {
        item["name"]: Interval.from_json(item["range"], budget) for item in benchmark["parameter_labels"]
    }
    if any(current_labels[name].lo != benchmark_labels[name].lo or current_labels[name].hi != benchmark_labels[name].hi for name in names):
        raise InvalidInput("selected query label image differs from the benchmark's complete declared image")
    initial_state = [Interval.from_json(row, budget) for row in case["initial_state"]]
    horizon = Fraction(int(case["horizon"]["num"]), int(case["horizon"]["den"]))
    voltage = case["held_voltage"]
    declared_horizons = {
        Fraction(int(item["T"]["num"]), int(item["T"]["den"]))
        for item in benchmark.get("horizons", [])
    }
    vmax = Fraction(int(benchmark["V_max"]["num"]), int(benchmark["V_max"]["den"]))
    voltage_values = [Fraction(int(item["num"]), int(item["den"])) for item in voltage]
    if horizon not in declared_horizons or len(voltage_values) != 2 or any(abs(value) > vmax for value in voltage_values):
        raise InvalidInput("matched-query horizon or held voltage is outside the declared benchmark grid")

    proof = _seed_record(
        case_kind="DDWMR_SINGLE_QUERY", case_id=case["query_id"], input_path=input_path,
        input_sha256=input_sha256, method_sha256=method_sha256, backend_sha256=backend_sha256,
        profile_sha256=profile_sha256, snapshot_sha256=snapshot_sha256,
        solver_sha256=solver_sha256, checker_sha256=checker_sha256,
        resource_profile_path=resource_profile_path,
    )
    proof["query_id"] = case["query_id"]
    proof["query_action_binding"] = _query_action_binding(case, current_labels)
    proof["time_horizon"] = {"start": qobj(Fraction(0)), "end": qobj(horizon)}
    proof["initial_state"] = interval_vector_json(initial_state)

    counters = {"picard_iterations": 0, "rhs_jacobian_evaluations": 0, "clip_branch_splits": 0}
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    current_state = initial_state
    current_time = Fraction(0)
    max_steps = int(profile["max_accepted_steps"])
    max_rejected = int(profile["max_rejected_step_attempts"])
    max_halvings = int(profile["max_step_halvings_per_attempt"])
    while current_time < horizon and len(accepted) < max_steps:
        step_width = horizon - current_time
        halvings = 0
        while True:
            try:
                step, outcome = _ddwmr_trial_step(
                    step_index=len(accepted), t0=current_time, h=step_width,
                    state_start=current_state, labels_start=current_labels,
                    benchmark=benchmark, voltage=voltage, profile=profile, budget=budget, counters=counters,
                )
            except ResourceLimit as exc:
                proof["status"] = "RESOURCE_LIMIT"
                proof["termination"] = {"kind": exc.kind, "detail": exc.detail, "failure_context": budget.failure_context}
                proof["rejected_step_attempts"] = rejected + [{
                    "step_index": len(accepted), "attempt_index": len(rejected),
                    "time_closed": {"start": qobj(current_time), "end": qobj(current_time + step_width)},
                    "step_width": qobj(step_width), "reason": exc.kind, "detail": exc.detail,
                    "partial_work_counters": dict(counters),
                }]
                proof["step_records"] = accepted
                proof["work"] = {**counters, "accepted_steps": len(accepted),
                                  "rejected_step_attempts": len(rejected) + 1,
                                  "rational_operations": budget.operations,
                                  "max_observed_rational_bits": budget.max_seen_bits}
                return proof
            if step is not None:
                accepted.append(step)
                endpoint_augmented = [Interval.from_json(raw, budget) for raw in step["endpoint_end_augmented"]]
                next_labels = {name: endpoint_augmented[9 + i] for i, name in enumerate(names)}
                if any(next_labels[name].lo != current_labels[name].lo or next_labels[name].hi != current_labels[name].hi for name in names):
                    raise RuntimeError("zero-derivative fixed labels changed at an accepted step boundary")
                current_labels = next_labels
                current_state = endpoint_augmented[:9]
                current_time += step_width
                break
            rejected.append({"step_index": len(accepted), "attempt_index": len(rejected), **outcome})
            if len(rejected) > max_rejected:
                proof["status"] = "RESOURCE_LIMIT"
                proof["termination"] = {"reason": "REJECTED_STEP_ATTEMPT_LIMIT", "max_rejected_step_attempts": max_rejected}
                proof["rejected_step_attempts"] = rejected
                proof["step_records"] = accepted
                proof["work"] = {**counters, "accepted_steps": len(accepted), "rejected_step_attempts": len(rejected)}
                return proof
            if halvings >= max_halvings:
                proof["status"] = "UNKNOWN"
                proof["termination"] = {"reason": "PICARD_INCLUSION_FAILURE_AFTER_FROZEN_HALVINGS", "max_step_halvings": max_halvings}
                proof["rejected_step_attempts"] = rejected
                proof["step_records"] = accepted
                proof["work"] = {**counters, "accepted_steps": len(accepted), "rejected_step_attempts": len(rejected)}
                return proof
            step_width = budget.div(step_width, Fraction(2))
            halvings += 1
            if step_width <= 0:
                raise RuntimeError("rational time bisection underflowed")
        if len(rejected) > max_rejected:
            break

    if current_time != horizon:
        proof["status"] = "RESOURCE_LIMIT" if len(accepted) >= max_steps else "IMPLEMENTATION_FAILURE"
        proof["termination"] = {"reason": "ACCEPTED_STEP_LIMIT_OR_TIME_COVERAGE_FAILURE"}
        proof["rejected_step_attempts"] = rejected
        proof["step_records"] = accepted
        proof["work"] = {**counters, "accepted_steps": len(accepted), "rejected_step_attempts": len(rejected)}
        return proof

    physical_tubes = [[Interval.from_json(row, budget) for row in step["full_time_total_hull_augmented"][:9]] for step in accepted]
    physical_ends = [[Interval.from_json(row, budget) for row in step["endpoint_end_augmented"][:9]] for step in accepted]
    proof["step_records"] = accepted
    proof["rejected_step_attempts"] = rejected
    proof["global_full_time_hulls"] = [interval_vector_json(row) for row in physical_tubes]
    proof["global_endpoint"] = interval_vector_json(physical_ends[-1])
    proof["work"] = {
        **counters,
        "accepted_steps": len(accepted),
        "rejected_step_attempts": len(rejected),
        "max_rational_bits": budget.max_bits,
        "rational_operations": budget.operations,
        "rational_operation_attempts": budget.operation_attempts,
        "max_observed_rational_bits": budget.max_seen_bits,
    }
    proof["status"] = "PROOF_COMPLETE"
    return proof
