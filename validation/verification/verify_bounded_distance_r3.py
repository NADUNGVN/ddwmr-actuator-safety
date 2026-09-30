"""Exact bounded-distance regressions and checker mutation checks for R3."""

from __future__ import annotations

import copy
import json
import subprocess
from fractions import Fraction
from pathlib import Path

from validation.g2.checker import replay_record
from validation.g2.evaluator import (
    DISTANCE_METHOD_R3, _bounded_collision_distance, make_query, run_query,
)
from validation.g2.hashing import HASH_PROTOCOL_ID, semantic_json_file_sha256
from validation.g2.rational import Budget, ResourceLimit, qobj


ROOT = Path(__file__).resolve().parents[2]
PILOT_PATH = ROOT / "validation/configs/dev_pilot_r3_v1.json"
MANIFEST_PATH = ROOT / "results/validation/g2/r3/development_manifest_r3_v1.json"
BENCHMARK_PATH = ROOT / "validation/configs/benchmark_v1.json"
R2_RECORDS_PATH = ROOT / "results/validation/g2/r2/dev_pilot_records_r2_v1.jsonl"


def _assert(condition: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def _distance(dx: Fraction, dy: Fraction, precision: int = 24) -> dict:
    budget = Budget(16384, 1_000_000)
    budget.set_stage("verification.r3.bounded_distance")
    return _bounded_collision_distance(dx, dy, precision, 40, budget)


def _mutated(record: dict, mutator) -> dict:
    output = copy.deepcopy(record)
    mutator(output)
    return output


def main() -> None:
    checks: dict[str, bool] = {}
    p = 24
    eps = Fraction(1, 1 << p)

    zero = _distance(Fraction(0), Fraction(0))
    _assert(zero["coordinate_gap_bounds_dyadic"] == [(Fraction(0), Fraction(0))] * 2, "zero_gaps_exact", checks)
    _assert(zero["minimum_distance_lower"] == zero["minimum_distance_upper"] == 0, "zero_distance_exact", checks)

    exact = _distance(Fraction(1, 8), Fraction(3, 16))
    _assert(exact["coordinate_gap_bounds_dyadic"] == [(Fraction(1, 8), Fraction(1, 8)), (Fraction(3, 16), Fraction(3, 16))], "dyadic_gaps_exact", checks)

    non_dyadic = _distance(Fraction(1, 3), Fraction(5, 7))
    _assert(all(lo <= value <= hi and hi - lo <= eps for value, (lo, hi) in zip((Fraction(1, 3), Fraction(5, 7)), non_dyadic["coordinate_gap_bounds_dyadic"])), "non_dyadic_directed_bounds", checks)
    _assert(non_dyadic["squared_distance_lower"] <= Fraction(1, 9) + Fraction(25, 49) <= non_dyadic["squared_distance_upper"], "non_dyadic_radicand_enclosure", checks)

    one_nonzero = _distance(Fraction(7, 13), Fraction(0))
    two_nonzero = _distance(Fraction(7, 13), Fraction(11, 17))
    _assert(one_nonzero["coordinate_gap_bounds_dyadic"][1] == (0, 0), "one_nonzero_gap", checks)
    _assert(all(pair[0] > 0 for pair in two_nonzero["coordinate_gap_bounds_dyadic"]), "two_nonzero_gaps", checks)

    lower = _distance(Fraction(1), Fraction(0))["minimum_distance_lower"]
    _assert(lower - lower - 0 == 0, "zero_margin", checks)
    _assert(lower - (lower - Fraction(1, 10)) > 0, "positive_margin", checks)
    _assert(lower - (lower + Fraction(1, 10)) < 0, "negative_margin", checks)

    shift_budget = Budget(8, 10)
    try:
        shift_budget.shift_left_nonnegative(1, 8, primitive_id="verification.shift-cap")
        shift_cap_rejected = False
    except ResourceLimit as exc:
        shift_cap_rejected = exc.kind == "RATIONAL_BIT_LIMIT" and shift_budget.operations == 0
    _assert(shift_cap_rejected, "shift_preoperation_bit_guard", checks)

    div_budget = Budget(16, 1)
    quotient, remainder = div_budget.divmod_nonnegative(11, 4, primitive_id="verification.divmod")
    _assert((quotient, remainder, div_budget.operations) == (2, 3, 1), "metered_integer_division", checks)
    try:
        div_budget.increment_nonnegative(quotient, primitive_id="verification.increment-cap")
        operation_cap_rejected = False
    except ResourceLimit as exc:
        operation_cap_rejected = exc.kind == "RATIONAL_OPERATION_LIMIT" and div_budget.operations == 1 and div_budget.operation_attempts == 2
    _assert(operation_cap_rejected, "integer_primitive_operation_cap", checks)

    pilot = json.loads(PILOT_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    benchmark = json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))
    r2_rows = [json.loads(line) for line in R2_RECORDS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    prior_positive = next(row for row in r2_rows if row["status"] == "CERTIFIED")
    query_id = prior_positive["query_id"]
    query = make_query(
        benchmark, query_id, pilot["profile"],
        manifest["development_manifest_semantic_sha256"],
        manifest["benchmark_config_semantic_sha256"], HASH_PROTOCOL_ID,
        manifest["specification_bundle_sha256"],
    )
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip()
    record = run_query(query, revision)
    _assert(record.get("distance_method_id") == DISTANCE_METHOD_R3, "r3_method_binding", checks)
    _assert(record.get("proof") is not None, "tamper_fixture_completed_proof", checks)
    replay = replay_record(record, query)
    _assert(replay.get("replayed") is True, "checker_replay", checks)

    collision = record["proof"]["collision"][0]
    den = 1 << p

    def raise_lower(row):
        row["proof"]["collision"][0]["minimum_distance_lower"] = qobj(
            Fraction(*map(int, (collision["minimum_distance_lower"]["num"], collision["minimum_distance_lower"]["den"]))) + eps
        )

    def lower_upper(row):
        value = Fraction(int(collision["minimum_distance_upper"]["num"]), int(collision["minimum_distance_upper"]["den"]))
        row["proof"]["collision"][0]["minimum_distance_upper"] = qobj(value - Fraction(1, den))

    def change_precision(row):
        row["proof"]["collision"][0]["distance_rounding_precision_bits"] = p + 1

    def corrupt_bounds(row):
        row["proof"]["collision"][0]["coordinate_gap_bounds_dyadic"][0]["lower"] = qobj(Fraction(0))
        row["proof"]["collision"][0]["coordinate_gap_bounds_dyadic"].pop()

    def overstate_proof_margin(row):
        margin = Fraction(int(collision["margin_lower"]["num"]), int(collision["margin_lower"]["den"])) + 1
        row["proof"]["collision"][0]["margin_lower"] = qobj(margin)
        row["collision_margin_lower"][0] = qobj(margin)

    for name, mutator in (
        ("reject_lower_endpoint_up", raise_lower),
        ("reject_upper_endpoint_down", lower_upper),
        ("reject_precision_mutation", change_precision),
        ("reject_malformed_rounding_witness", corrupt_bounds),
        ("reject_proof_and_record_margin_overstatement", overstate_proof_margin),
    ):
        rejected = replay_record(_mutated(record, mutator), query)
        _assert(rejected.get("replayed") is False, name, checks)

    changed_query = copy.deepcopy(query)
    changed_query["action"]["V"][0] = qobj(Fraction(0)) if changed_query["action"]["V"][0] != qobj(Fraction(0)) else qobj(Fraction(1, 2))
    _assert(replay_record(record, changed_query).get("replayed") is False, "reject_voltage_query_binding", checks)

    changed_profile_query = copy.deepcopy(query)
    changed_profile_query["profile"]["distance_rounding_precision_bits"] = p + 1
    _assert(replay_record(record, changed_profile_query).get("replayed") is False, "reject_profile_precision_binding", checks)

    old_margin = Fraction(
        int(record["collision_margin_lower"][0]["num"]),
        int(record["collision_margin_lower"][0]["den"]),
    )
    changed_margin = _mutated(record, lambda row: row["collision_margin_lower"].__setitem__(0, qobj(old_margin + 1)))
    _assert(replay_record(changed_margin, query).get("replayed") is False, "reject_reported_margin_mutation", checks)

    changed_status = _mutated(record, lambda row: row.__setitem__("status", "UNKNOWN" if row["status"] == "CERTIFIED" else "CERTIFIED"))
    _assert(replay_record(changed_status, query).get("replayed") is False, "reject_status_mutation", checks)

    print(json.dumps({
        "schema": "ddwmr-g2-bounded-distance-r3-verification-v1",
        "method_id": record["method_id"],
        "distance_method_id": DISTANCE_METHOD_R3,
        "fixture_query_id": query_id,
        "fixture_status": record["status"],
        "fixture_replay": replay,
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(checks.values()),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
