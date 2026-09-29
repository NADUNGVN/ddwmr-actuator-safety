#!/usr/bin/env python3
"""Deterministically generate the synthetic benchmark and frozen dev pilot."""

from __future__ import annotations

import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIGS = ROOT / "validation" / "configs"
RESULTS = ROOT / "results" / "validation" / "g2"


def q(value: str | Fraction | int) -> dict[str, str]:
    value = Fraction(value)
    return {"num": str(value.numerator), "den": str(value.denominator)}


def interval(lo: str | Fraction | int, hi: str | Fraction | int) -> list[dict[str, str]]:
    return [q(lo), q(hi)]


def expr_var(name: str) -> dict[str, str]:
    return {"var": name}


def expr_const(value: str | Fraction | int) -> dict[str, dict[str, str]]:
    return {"const": q(value)}


def expr(op: str, *args: dict) -> dict:
    return {"op": op, "args": list(args)}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def make_benchmark() -> dict:
    labels = [
        ("rho_L", Fraction(1), Fraction(11, 10)),
        ("C_L", Fraction(1), Fraction(11, 10)),
        ("lambda_L", Fraction(9, 10), Fraction(11, 10)),
        ("R_L", Fraction(9, 10), Fraction(11, 10)),
        ("B_L", Fraction(9, 10), Fraction(11, 10)),
        ("k_L", Fraction(9, 10), Fraction(11, 10)),
        ("rho_R", Fraction(1), Fraction(11, 10)),
        ("C_R", Fraction(1), Fraction(11, 10)),
        ("lambda_R", Fraction(9, 10), Fraction(11, 10)),
        ("R_R", Fraction(9, 10), Fraction(11, 10)),
        ("B_R", Fraction(9, 10), Fraction(11, 10)),
        ("k_R", Fraction(9, 10), Fraction(11, 10)),
    ]
    label_box = {name: interval(lo, hi) for name, lo, hi in labels}
    params = {
        "m": expr_const(1), "I_z": expr_const(1), "R_w": expr_const(1),
        "b": expr_const(1), "v_s": expr_const(1), "c_u": expr_const(1),
        "c_r": expr_const(1),
    }
    for side in ("L", "R"):
        params[f"J_{side}"] = expr("div", expr_const(1), expr_var(f"rho_{side}"))
        params[f"L_{side}"] = expr_var(f"lambda_{side}")
        params[f"R_{side}"] = expr_var(f"R_{side}")
        params[f"B_{side}"] = expr_var(f"B_{side}")
        params[f"k_{side}"] = expr_var(f"k_{side}")
        params[f"C_{side}"] = expr_var(f"C_{side}")
    gear = {}
    for side in ("L", "R"):
        gear[side] = {
            "n": q(10), "k_motor": expr("div", expr_var(f"k_{side}"), expr_const(10)),
            "J_wheel": q(Fraction(1, 10)),
            "J_motor": expr("div", expr("sub", expr("div", expr_const(1), expr_var(f"rho_{side}")), expr_const(Fraction(1, 10))), expr_const(100)),
            "B_wheel": q(0),
            "B_motor": expr("div", expr_var(f"B_{side}"), expr_const(100)),
        }

    states = []
    speeds = [("low", Fraction(1, 5), Fraction(3, 10)), ("high", Fraction(3, 5), Fraction(7, 10))]
    yaws = [("neg", Fraction(-1, 5), Fraction(-1, 10)), ("mid", Fraction(-1, 20), Fraction(1, 20)), ("pos", Fraction(1, 10), Fraction(1, 5))]
    for speed_name, ulo, uhi in speeds:
        uc = (ulo + uhi) / 2
        for yaw_name, rlo, rhi in yaws:
            rc = (rlo + rhi) / 2
            sid = f"state_{speed_name}_{yaw_name}"
            states.append({
                "id": sid,
                "coordinates": ["p_x", "p_y", "theta", "u", "r", "omega_L", "omega_R", "i_L", "i_R"],
                "box": [
                    interval(Fraction(-1, 100), Fraction(1, 100)),
                    interval(Fraction(-1, 100), Fraction(1, 100)),
                    interval(Fraction(-1, 20), Fraction(1, 20)),
                    interval(ulo, uhi),
                    interval(rlo, rhi),
                    interval(uc - rc - Fraction(1, 10), uc - rc + Fraction(1, 10)),
                    interval(uc + rc - Fraction(1, 10), uc + rc + Fraction(1, 10)),
                    interval(Fraction(-1, 10), Fraction(1, 10)),
                    interval(Fraction(-1, 10), Fraction(1, 10)),
                ],
            })

    scenes = []
    for clearance in (Fraction(1, 50), Fraction(1, 20), Fraction(1, 10), Fraction(1, 5)):
        for lateral in (Fraction(-1, 5), Fraction(0), Fraction(1, 5)):
            cid = f"d{int(clearance * 1000):03d}_l{int(lateral * 1000):+04d}"
            scenes.append({
                "id": f"scene_{cid}",
                "p_o": [q(Fraction(1, 2) + clearance), q(lateral)],
                "R_s": q(Fraction(1, 2)),
                "clearance": q(clearance),
                "lateral_offset": q(lateral),
            })

    actions = []
    for left in (Fraction(-1), Fraction(0), Fraction(1)):
        for right in (Fraction(-1), Fraction(0), Fraction(1)):
            def code(v: Fraction) -> str:
                return "m1" if v < 0 else ("0" if v == 0 else "p1")
            actions.append({"id": f"V_{code(left)}_{code(right)}", "V": [q(left), q(right)]})

    return {
        "schema": "ddwmr-g2-benchmark-v1",
        "status": "SYNTHETIC_DRAFT_INPUT; NOT_A_LOCKED_SCIENTIFIC_COMPARISON",
        "source_spec": "research/benchmarks/G2_USEFULNESS_BENCHMARK_SPEC_v1.md",
        "plant_scope": "MASTER v2.1 nine-state reduced ideal planar DDWMR; G2-COMP-clip subset",
        "units": {"position": "m", "angle": "rad", "time": "s", "voltage": "V", "force": "N", "reference_coordinate_scales": [q(1)] * 6},
        "law": {"name": "clip", "L_phi": q(1)},
        "V_max": q(1),
        "fixed_parameters": params,
        "parameter_labels": [{"name": n, "range": interval(lo, hi)} for n, lo, hi in labels],
        "gear_witness": gear,
        "state_cells": states,
        "scenes": scenes,
        "horizons": [
            {"id": "T_020", "T": q(Fraction(1, 50))},
            {"id": "T_050", "T": q(Fraction(1, 20))},
            {"id": "T_100", "T": q(Fraction(1, 10))},
        ],
        "actions": actions,
        "parameter_cell": {"id": "theta_full_12d", "labels": label_box},
        "coordinate_scaling": [q(1)] * 6,
        "counts": {"state_cells": 6, "scenes": 12, "horizons": 3, "actions": 9, "queries": 1944},
    }


def query_id(state: str, scene: str, horizon: str, action: str) -> str:
    return f"{state}__{scene}__{horizon}__{action}"


def main() -> None:
    benchmark = make_benchmark()
    benchmark_path = CONFIGS / "benchmark_v1.json"
    dump(benchmark_path, benchmark)

    selected_states = ["state_low_neg", "state_low_pos", "state_high_neg", "state_high_pos"]
    selected_scenes = ["scene_d050_l+000", "scene_d200_l+200"]
    all_state = [x["id"] for x in benchmark["state_cells"]]
    all_scenes = [x["id"] for x in benchmark["scenes"]]
    all_horizons = [x["id"] for x in benchmark["horizons"]]
    all_actions = [x["id"] for x in benchmark["actions"]]
    original = [query_id(s, c, t, v) for s in all_state for c in all_scenes for t in all_horizons for v in all_actions]
    selected = [query_id(s, c, t, v) for s in selected_states for c in selected_scenes for t in all_horizons for v in all_actions]
    selected_set = set(selected)
    not_run = [qid for qid in original if qid not in selected_set]

    profile = {
        "id": "DEV_FALLBACK_N1_PILOT_V1",
        "predictor_depth": 1,
        "exp_taylor_degree": 16,
        "trig_taylor_degree": 18,
        "comparison_series_order": 16,
        "parameter_split_depth": 0,
        "parameter_leaf_limit": 1,
        "initial_state_split_depth": 0,
        "initial_state_leaf_limit": 1,
        "time_slab_count": 1,
        "integration_panels": 1,
        "sqrt_bisections": 24,
        "max_rational_bits": 8192,
        "max_rational_operations": 1000000,
        "wall_seconds_per_query": q(15),
        "selection_rule": "Fixed before any evaluator output: all nine benchmark actions for the four speed-yaw corner cells (low/high speed crossed with negative/positive yaw), two predeclared scenes (d=1/20,l=0 and d=1/5,l=1/5), and all three horizons. No outcome-based replacement, obstacle movement, or action omission.",
        "reason_for_cap": "A bounded, affordable 216-query development pilot using one full-hold interval hull per initial/parameter cell. It deliberately avoids subdivision/refinement so all UNKNOWN outcomes remain visible; time-panel repetition would be a no-op for this global hull. This is not a formal matched-comparison configuration.",
    }
    pilot_path = CONFIGS / "dev_pilot_v1.json"
    dump(pilot_path, {
        "schema": "ddwmr-g2-development-pilot-v1",
        "status": "FROZEN_DEVELOPMENT_ONLY_NOT_LOCKED",
        "benchmark_config": "validation/configs/benchmark_v1.json",
        "selected_state_cells": selected_states,
        "selected_scenes": selected_scenes,
        "selected_horizons": all_horizons,
        "selected_actions": all_actions,
        "profile": profile,
        "original_grid_count": len(original),
        "pilot_query_count": len(selected),
        "selection_rule": profile["selection_rule"],
        "reason_for_cap": profile["reason_for_cap"],
    })

    manifest_path = RESULTS / "development_manifest_v1.json"
    if manifest_path.exists():
        prior = json.loads(manifest_path.read_text(encoding="utf-8"))
        revision = prior.get("source_base_commit")
    else:
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True
        ).stdout.strip()
    if not isinstance(revision, str) or len(revision) != 40:
        raise SystemExit("manifest source_base_commit is missing or malformed")
    manifest = {
        "schema": "ddwmr-g2-development-manifest-v1",
        "status": "IMMUTABLE_DEVELOPMENT_INPUTS_FROZEN_BEFORE_EVALUATION; NOT_LOCKED",
        "source_base_commit": revision,
        "benchmark_spec": benchmark["source_spec"],
        "benchmark_config_sha256": sha256(benchmark_path),
        "pilot_config_sha256": sha256(pilot_path),
        "profile": profile,
        "original_query_count_per_method_profile": len(original),
        "selected_query_count": len(selected),
        "not_run_query_count": len(not_run),
        "original_query_ids": original,
        "selected_query_ids": selected,
        "not_run_query_ids": not_run,
        "aggregation": "An original state-scene-horizon-action query is CERTIFIED only if every state/parameter leaf, obstacle and all-time check passes. No leaf-level denominator. Every unselected original ID is NOT_RUN.",
        "disposition": "Development pilot only; no predeclared minimum coverage threshold, no held-out claim, no external baseline, no G2/G4 promotion.",
    }
    dump(manifest_path, manifest)
    sums = RESULTS / "SHA256SUMS_PRE_EVAL.txt"
    sum_lines = [
        f"{sha256(benchmark_path)}  validation/configs/benchmark_v1.json",
        f"{sha256(pilot_path)}  validation/configs/dev_pilot_v1.json",
        f"{sha256(Path(__file__))}  validation/scripts/generate_manifest.py",
        f"{sha256(manifest_path)}  results/validation/g2/development_manifest_v1.json",
    ]
    sums.write_text("\n".join(sum_lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "source_base_commit": revision,
        "original": len(original), "selected": len(selected), "not_run": len(not_run),
        "benchmark_sha256": sha256(benchmark_path), "pilot_sha256": sha256(pilot_path),
        "manifest_sha256": sha256(manifest_path), "selection_matches_expected": len(selected) == 216,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
