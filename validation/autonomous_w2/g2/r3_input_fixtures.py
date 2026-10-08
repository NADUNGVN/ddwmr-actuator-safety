"""Non-query schema/model checks for the frozen custom R3 comparator inputs."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from validation.g2.model import build_model
from validation.g2.rational import Budget, parse_q


ROOT = Path(__file__).resolve().parents[3]


def verify() -> dict[str, object]:
    protocol = json.loads((ROOT / "research/autonomous_w2/g2/r3_baseline_input_v1.json").read_text(encoding="utf-8"))
    benchmark = json.loads((ROOT / protocol["benchmark_path"]).read_text(encoding="utf-8"))
    profile = json.loads((ROOT / "research/autonomous_w2/g2/r3_baseline_profile_v1.json").read_text(encoding="utf-8"))
    budget = Budget(profile["max_rational_bits"], profile["max_rational_operations"])
    model = build_model(benchmark, budget)
    assert protocol["state_cell"]["coordinates"] == ["p_x", "p_y", "theta", "u", "r", "omega_L", "omega_R", "i_L", "i_R"]
    assert len(protocol["state_cell"]["box"]) == 9
    assert all(Fraction(int(pair[0]["num"]), int(pair[0]["den"])) < Fraction(int(pair[1]["num"]), int(pair[1]["den"])) for pair in protocol["state_cell"]["box"])
    assert len(model.parameter_label_order) == 12
    assert all(item.lo > 0 for name, item in model.parameter_label_box.items())
    assert all(item.lo < item.hi for item in model.parameter_label_box.values())
    assert len(protocol["query_actions"]) == 3
    expected = [("W2_G2_DEV_001_ZERO", Fraction(0)), ("W2_G2_DEV_001_NOMINAL", Fraction(1, 2)), ("W2_G2_DEV_001_ALTERNATIVE", Fraction(1))]
    for row, (action_id, voltage) in zip(protocol["query_actions"], expected):
        assert row["action"]["id"] == action_id
        assert [parse_q(value, budget) for value in row["action"]["V"]] == [voltage, voltage]
    assert parse_q(protocol["horizon"]["T"], budget) == 2
    assert parse_q(protocol["task_progress_threshold"], budget) == Fraction(7, 20)
    return {
        "schema": "G2_W2_R3_INPUT_NONQUERY_FIXTURES_v1",
        "status": "PASS",
        "fixture_count": 6,
        "positive_width_initial_coordinates": 9,
        "positive_width_fixed_labels": len(model.parameter_label_order),
        "action_count": 3,
        "model_build_operations": budget.operations,
        "run_query_calls": 0,
        "legacy_800_row_study": "NOT_RUN",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True, indent=2))
