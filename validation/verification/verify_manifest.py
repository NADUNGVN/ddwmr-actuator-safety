#!/usr/bin/env python3
"""Verify frozen benchmark IDs, selection rule, and pre-evaluation hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def main() -> None:
    benchmark_path = "validation/configs/benchmark_v1.json"
    pilot_path = "validation/configs/dev_pilot_v1.json"
    generator_path = "validation/scripts/generate_manifest.py"
    manifest_path = "results/validation/g2/development_manifest_v1.json"
    manifest = load(manifest_path)
    bench = load(benchmark_path)
    pilot = load(pilot_path)

    states = [x["id"] for x in bench["state_cells"]]
    scenes = [x["id"] for x in bench["scenes"]]
    horizons = [x["id"] for x in bench["horizons"]]
    actions = [x["id"] for x in bench["actions"]]
    ids = [f"{s}__{c}__{t}__{a}" for s in states for c in scenes for t in horizons for a in actions]
    selected = [
        f"{s}__{c}__{t}__{a}"
        for s in pilot["selected_state_cells"]
        for c in pilot["selected_scenes"]
        for t in pilot["selected_horizons"]
        for a in pilot["selected_actions"]
    ]
    selected_set = set(selected)
    checks = {
        "benchmark_dimensions": (len(states), len(scenes), len(horizons), len(actions)) == (6, 12, 3, 9),
        "all_original_ids_unique": len(ids) == len(set(ids)) == 1944,
        "selected_ids_unique": len(selected) == len(selected_set) == 216,
        "selected_subset_of_original": selected_set <= set(ids),
        "not_run_exact_complement": set(manifest["not_run_query_ids"]) == set(ids) - selected_set,
        "manifest_original_ids_exact": manifest["original_query_ids"] == ids,
        "manifest_selected_ids_exact": manifest["selected_query_ids"] == selected,
        "both_speed_groups": {"state_low_neg", "state_high_neg"} <= set(pilot["selected_state_cells"]),
        "both_yaw_signs": {"state_low_neg", "state_low_pos", "state_high_neg", "state_high_pos"} == set(pilot["selected_state_cells"]),
        "all_actions_and_horizons": pilot["selected_actions"] == actions and pilot["selected_horizons"] == horizons,
        "two_clearances": len({x["clearance"]["num"] + "/" + x["clearance"]["den"] for x in bench["scenes"] if x["id"] in pilot["selected_scenes"]}) == 2,
        "benchmark_hash_matches": manifest["benchmark_config_sha256"] == digest(benchmark_path),
        "pilot_hash_matches": manifest["pilot_config_sha256"] == digest(pilot_path),
    }
    sums_path = ROOT / "results/validation/g2/SHA256SUMS_PRE_EVAL.txt"
    sums = sums_path.read_text(encoding="utf-8").splitlines()
    expected = {
        "validation/configs/benchmark_v1.json": digest(benchmark_path),
        "validation/configs/dev_pilot_v1.json": digest(pilot_path),
        "validation/scripts/generate_manifest.py": digest(generator_path),
        manifest_path: digest(manifest_path),
    }
    checks["pre_eval_hash_ledger_matches"] = all(
        any(line == f"{value}  {path}" for line in sums) for path, value in expected.items()
    )
    checks["not_marked_locked"] = manifest["status"].endswith("NOT_LOCKED")
    output = {"checks": checks, "all_pass": all(checks.values()), "selected": len(selected), "not_run": len(ids) - len(selected)}
    print(json.dumps(output, sort_keys=True))
    if not output["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
