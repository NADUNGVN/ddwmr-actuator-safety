"""Materialize a source-faithful R3 comparator on the prospectively frozen W2 task."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
TASK_REL = "research/autonomous_w2/g2/task_protocol_v1.json"
LEGACY_BENCHMARK_REL = "validation/configs/benchmark_v1.json"
BENCHMARK_REL = "research/autonomous_w2/g2/r3_baseline_benchmark_v1.json"
INPUT_REL = "research/autonomous_w2/g2/r3_baseline_input_v1.json"
PROFILE_REL = "research/autonomous_w2/g2/r3_baseline_profile_v1.json"
LOW = {"num": "9999", "den": "10000"}
HIGH = {"num": "10001", "den": "10000"}


def qobj(value: str) -> dict[str, str]:
    from fractions import Fraction

    exact = Fraction(value)
    return {"num": str(exact.numerator), "den": str(exact.denominator)}


def dump_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True).encode("utf-8") + b"\n")


def write_or_verify(path: Path, value: Any) -> None:
    if path.exists():
        if json.loads(path.read_text(encoding="utf-8")) != value:
            raise ValueError(f"PREPARED_R3_INPUT_DIFFERS_FROM_DECLARATION:{path.relative_to(ROOT)}")
        return
    dump_new(path, value)


def prepare() -> dict[str, Any]:
    paths = [ROOT / BENCHMARK_REL, ROOT / INPUT_REL, ROOT / PROFILE_REL]
    exists = [path.exists() for path in paths]
    if any(exists) and not all(exists):
        raise FileExistsError("R3_BASELINE_W2_INPUT_SET_IS_PARTIAL")
    task_path = ROOT / TASK_REL
    task = json.loads(task_path.read_text(encoding="utf-8"))
    legacy = json.loads((ROOT / LEGACY_BENCHMARK_REL).read_text(encoding="utf-8"))
    label_order = task["model"]["fixed_label_order"]
    labels = {name: [LOW, HIGH] for name in label_order}
    benchmark = {
        "V_max": legacy["V_max"],
        "fixed_parameters": legacy["fixed_parameters"],
        "gear_witness": legacy["gear_witness"],
        "parameter_labels": [{"name": name, "range": [LOW, HIGH]} for name in label_order],
        "parameter_cell": {"id": "W2_G2_POSITIVE_WIDTH_FIXED_LABEL_IMAGE_V1", "labels": labels},
        "coordinate_scaling": legacy["coordinate_scaling"],
        "law": legacy["law"],
    }
    write_or_verify(ROOT / BENCHMARK_REL, benchmark)
    state_box = [[qobj(pair[0]), qobj(pair[1])] for pair in task["task"]["initial_box"]]
    state_cell = {
        "id": "W2_G2_DEV_001_MOVING_STATE_BOX",
        "coordinates": task["task"]["initial_box_state_order"],
        "box": state_box,
    }
    obstacle = task["task"]["obstacle"]
    scene = {
        "id": "W2_G2_DEV_001_STATIC_CIRCLE",
        "p_o": [qobj(value) for value in obstacle["center_m"]],
        "R_s": qobj(obstacle["inflated_radius_m"]),
    }
    horizon = {"id": "W2_G2_DEV_001_T_2S", "T": qobj(task["task"]["hold_s"])}
    query_actions = []
    for item in task["actions"]:
        action = {"id": item["id"], "V": [qobj(v) for v in item["voltage"]]}
        query_id = "__".join([state_cell["id"], scene["id"], horizon["id"], action["id"]])
        query_actions.append({"action": action, "query_id": query_id})
    r3_input = {
        "schema": "G2_W2_R3_COMPARATOR_INPUT_v1",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "task_protocol_path": TASK_REL,
        "legacy_source_benchmark_path": LEGACY_BENCHMARK_REL,
        "benchmark_path": BENCHMARK_REL,
        "state_cell": state_cell,
        "scene": scene,
        "horizon": horizon,
        "task_progress_threshold": qobj(task["task"]["required_progress_m"]),
        "source_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip(),
        "query_actions": query_actions,
        "scope": "same W2 initial state, fixed-label bounds, circle, two-second common held-voltage actions, and progress threshold; legacy R3 full-hold comparison/one panel; development only",
    }
    # Preserve R3's published pilot approximation orders while rebinding to the W2 common top-level cap.
    old_profile = json.loads((ROOT / "validation/configs/dev_pilot_r3_v1.json").read_text(encoding="utf-8"))["profile"]
    profile = {
        "id": "G2_W2_R3_BASELINE_PILOT_ORDER_V1",
        "exp_taylor_degree": old_profile["exp_taylor_degree"],
        "trig_taylor_degree": old_profile["trig_taylor_degree"],
        "comparison_series_order": old_profile["comparison_series_order"],
        "sqrt_bisections": old_profile["sqrt_bisections"],
        "max_rational_bits": 16384,
        "max_rational_operations": 5000000,
        "wall_seconds_per_query": {"num": "60", "den": "1"},
        "predictor_depth": 1,
        "parameter_split_depth": 0,
        "parameter_leaf_limit": 1,
        "initial_state_split_depth": 0,
        "initial_state_leaf_limit": 1,
        "time_slab_count": 1,
        "integration_panels": 1,
        "distance_method_id": old_profile["distance_method_id"],
        "distance_rounding_precision_bits": old_profile["distance_rounding_precision_bits"],
        "distance_rounding_contract": old_profile["distance_rounding_contract"],
        "resource_diagnostic_schema": old_profile["resource_diagnostic_schema"],
        "hash_protocol_id": "ddwmr-semantic-json-sha256-v2",
        "specification_bundle_sha256": "93e7cea7c78d48a1843c111937bf6cbf1436e001dbe5f46b8b42887b16806772",
        "outer_worker_wall_cap_seconds": 60,
        "outer_worker_memory_cap_bytes": 1073741824,
        "reason_for_cap": "Reuses the prior R3 pilot numerical orders (exp=16, trig=18, comparison=16, sqrt=24, one whole-hold panel) and pins the W2 common outer 60 s / 1 GiB envelope. The operation cap is 5,000,000 and bit cap 16,384; any resource UNKNOWN is retained.",
    }
    write_or_verify(ROOT / INPUT_REL, r3_input)
    write_or_verify(ROOT / PROFILE_REL, profile)
    return {
        "schema": "G2_W2_R3_COMPARATOR_PREPARATION_v1",
        "benchmark_path": BENCHMARK_REL,
        "input_path": INPUT_REL,
        "profile_path": PROFILE_REL,
        "action_count": len(query_actions),
        "same_domain_and_task": True,
        "held_out_rows": 0,
        "legacy_800_row_study": "NOT_RUN",
    }


if __name__ == "__main__":
    print(json.dumps(prepare(), sort_keys=True, indent=2))
