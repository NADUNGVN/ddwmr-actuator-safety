"""Prepare the Auer candidate manifest without evaluating a single query."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK = Path("validation/configs/benchmark_v1.json")
R2_MANIFEST = Path("results/validation/g2/r2/development_manifest_r2_v1.json")
DEFAULT_OUTPUT = Path("results/validation/g4/auer2013/auer_matched_candidate_manifest_v1.json")


def raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic_sha256(value) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=DEFAULT_OUTPUT.as_posix())
    args = parser.parse_args()
    benchmark_path, r2_path = ROOT / BENCHMARK, ROOT / R2_MANIFEST
    benchmark, r2 = json.loads(benchmark_path.read_text(encoding="utf-8")), json.loads(r2_path.read_text(encoding="utf-8"))
    generated = [
        f"{state['id']}__{scene['id']}__{horizon['id']}__{action['id']}"
        for state in benchmark["state_cells"]
        for scene in benchmark["scenes"]
        for horizon in benchmark["horizons"]
        for action in benchmark["actions"]
    ]
    original = r2["original_query_ids"]
    if len(generated) != 1944 or len(set(generated)) != 1944:
        raise SystemExit("the benchmark configuration did not generate 1,944 unique IDs")
    if original != generated or r2.get("original_query_count_per_method_profile") != 1944:
        raise SystemExit("the candidate IDs do not exactly match the frozen R2 original universe")

    state_by_id = {item["id"]: item for item in benchmark["state_cells"]}
    scene_by_id = {item["id"]: item for item in benchmark["scenes"]}
    horizon_by_id = {item["id"]: item for item in benchmark["horizons"]}
    action_by_id = {item["id"]: item for item in benchmark["actions"]}
    parameter_cell = benchmark["parameter_cell"]
    queries = []
    for query_id in original:
        state_id, scene_id, horizon_id, action_id = query_id.split("__")
        payload = {
            "query_id": query_id,
            "state_cell": state_by_id[state_id],
            "scene": scene_by_id[scene_id],
            "horizon": horizon_by_id[horizon_id],
            "action": action_by_id[action_id],
            "parameter_cell": parameter_cell,
        }
        queries.append({
            "query_id": query_id,
            "input_sha256": semantic_sha256(payload),
            "status": "NOT_RUN",
        })

    payload = {
        "schema": "ddwmr-g4-auer-candidate-manifest-v1",
        "status": "PREPARATION_ONLY_NOT_EVALUATED_NOT_LOCKED",
        "method_id": "AUER_2013_VALENCIA_IVP_PIECEWISE_MEAN_VALUE_CANDIDATE",
        "base_git_revision": "aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46",
        "benchmark_config_path": BENCHMARK.as_posix(),
        "benchmark_config_sha256": raw_sha256(benchmark_path),
        "r2_original_manifest_path": R2_MANIFEST.as_posix(),
        "r2_original_manifest_sha256": raw_sha256(r2_path),
        "original_query_count_per_method_profile": 1944,
        "original_query_ids_sha256_lf": hashlib.sha256("\n".join(original).encode("utf-8")).hexdigest(),
        "ids_exactly_match_r2_original_universe": True,
        "queries": queries,
        "execution": {
            "comparison_run": False,
            "auer_status_all_queries": "NOT_RUN",
            "r3_status_joined": False,
            "scope": "The IDs and inputs are enumerated only; no ODE, enclosure, checker, or safety query was evaluated.",
        },
        "candidate_settings_pending_independent_review": {
            "step_size_seconds": {"num": "1", "den": "1000"},
            "step_size_basis": "The §5 article reference reports step size 0.001 s; transfer to this new model requires method audit.",
            "IEEE754_backend_target": "binary64 directed-rounding PROFIL/BIAS, if the pinned dependencies can be lawfully obtained and built",
            "compiler_flags_target": ["-O2", "-frounding-math", "-fno-fast-math", "-ffp-contract=off"],
            "max_steps_per_query": 100,
            "max_piecewise_range_splits_per_component_step": 10,
            "max_reinitialization_attempts_per_step": 5,
            "max_function_plus_jacobian_evaluations_per_query": 1000000,
            "wall_seconds_per_query": 15,
            "peak_memory_bytes_per_query": 536870912,
            "failure_semantics": "Any failed inclusion, exhausted iteration/split/work cap, unsupported input, arithmetic exception, or timeout is UNKNOWN or a separately reported implementation failure; never CERTIFIED.",
            "status": "PROPOSED_SETTINGS_ONLY_NOT_FROZEN_FOR_EXECUTION",
        },
    }
    output_path = ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "output": str(output_path),
        "query_count": len(queries),
        "ids_exactly_match_r2": True,
        "query_ids_sha256_lf": payload["original_query_ids_sha256_lf"],
        "comparison_run": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()

