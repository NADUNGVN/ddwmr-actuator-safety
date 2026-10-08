"""Non-query regression fixture for bounded exact-rational serialization and R3 hashes."""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from .r3_baseline_checker_v2 import build_query as build_r3_replay_query
from .r3_baseline_worker_v2 import build_query as build_r3_worker_query
from .rational_interval_v2 import ArithmeticLimit, Budget, activate, configure_integer_string_limit, qs


ROOT = Path(__file__).resolve().parents[3]
PROFILE_PATH = ROOT / "validation/autonomous_w2/g2/profile_v2.json"
PRIOR_BINDING_PATH = ROOT / "research/autonomous_w2/g2/bindings_v1/attempt_04.json"


def run() -> dict[str, Any]:
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    configure_integer_string_limit(profile["python_int_string_digit_cap"], profile["rational_bit_cap"])
    checks: list[dict[str, Any]] = []

    wide = Fraction(1, 10**4401)
    budget = Budget(100, profile["rational_bit_cap"])
    activate(budget)
    try:
        encoded = qs(wide)
    finally:
        activate(None)
    decoded = Fraction(encoded)
    assert decoded == wide
    assert len(encoded.split("/")[1]) > 4300
    checks.append({"check": "above_default_4300_digit_round_trip", "status": "PASS", "decimal_digits": len(encoded.split("/")[1]), "rational_operations": budget.operations, "max_rational_bits": budget.max_observed_bits})

    oversized = Fraction(1, 1 << profile["rational_bit_cap"])
    limit_budget = Budget(100, profile["rational_bit_cap"])
    activate(limit_budget)
    rejected = False
    try:
        qs(oversized)
    except ArithmeticLimit as exc:
        rejected = str(exc) == "RATIONAL_BIT_CAP"
    finally:
        activate(None)
    assert rejected
    checks.append({"check": "excess_rational_bit_width_fails_closed", "status": "PASS", "max_rational_bits": limit_budget.max_observed_bits})

    prior = json.loads(PRIOR_BINDING_PATH.read_text(encoding="utf-8"))
    worker_query = build_r3_worker_query(prior, prior["action_id"])
    replay_query = build_r3_replay_query(prior, prior["action_id"])
    benchmark = json.loads((ROOT / prior["r3_benchmark_path"]).read_text(encoding="utf-8"))
    raw_hash = hashlib.sha256((ROOT / prior["r3_benchmark_path"]).read_bytes()).hexdigest()
    assert worker_query["benchmark_sha256"] == replay_query["benchmark_sha256"]
    assert worker_query["benchmark_sha256"] != raw_hash
    checks.append({"check": "r3_worker_and_replay_bind_semantic_benchmark_hash", "status": "PASS", "semantic_sha256": worker_query["benchmark_sha256"], "raw_file_sha256": raw_hash, "benchmark_keys": sorted(benchmark)})

    return {"schema": "G2_W2_V2_NONQUERY_FIXTURES_v1", "query_or_run_query_calls": 0, "check_count": len(checks), "checks": checks, "status": "PASS"}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
