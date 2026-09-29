#!/usr/bin/env python3
"""Regenerate pilot counts, strata, margins, widths, costs, and ledgers."""

from __future__ import annotations

import hashlib
import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

from validation.g2.evaluator import ROOT
from validation.g2.rational import parse_q, qtext


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_values(values: list[Fraction]):
    if not values:
        return None
    ordered = sorted(values)
    return {
        "count": len(values),
        "min": qtext(ordered[0]),
        "median_lower": qtext(ordered[(len(ordered) - 1) // 2]),
        "max": qtext(ordered[-1]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", default="results/validation/g2/dev_pilot_records_v1.jsonl")
    parser.add_argument("--summary", default=None)
    parser.add_argument("--unknown-ledger", default=None)
    parser.add_argument("--failure-ledger", default=None)
    args = parser.parse_args()
    base = ROOT / "results/validation/g2"
    records_path = ROOT / args.records
    records = [json.loads(line) for line in records_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    manifest = load(base / "development_manifest_v1.json")
    benchmark = load(ROOT / "validation/configs/benchmark_v1.json")
    states = {x["id"]: x for x in benchmark["state_cells"]}
    scenes = {x["id"]: x for x in benchmark["scenes"]}
    counts = Counter(record["status"] for record in records)
    strata = {key: defaultdict(Counter) for key in ("speed", "yaw", "clearance", "horizon")}
    action_groups: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    collision_margins, contact_margins, widths, radii, total_widths = [], [], [], [], []
    runtimes, operations, max_bits = [], [], []
    unknown_ledger, failure_ledger = [], []
    for record in records:
        state = states[record["state_cell_id"]]
        scene = scenes[record["scene_id"]]
        speed, yaw = record["state_cell_id"].split("_")[1:]
        clearance = f"{scene['clearance']['num']}/{scene['clearance']['den']}"
        action_groups[(record["state_cell_id"], record["scene_id"], record["horizon_id"])].append(record)
        for name, value in (("speed", speed), ("yaw", yaw), ("clearance", clearance), ("horizon", record["horizon_id"])):
            strata[name][value][record["status"]] += 1
        if "collision_margin_lower" in record:
            collision_margins.extend(parse_q(x) for x in record["collision_margin_lower"])
            contact_margins.append(parse_q(record["contact_margin_lower"]))
            widths.extend(parse_q(x) for x in record["center_width_internal_physical"])
            radii.extend(parse_q(x) for x in record["error_radius_internal_physical"])
            total_widths.extend(parse_q(x) for x in record["total_width_internal_physical"])
        if "elapsed_seconds_display_only" in record:
            runtimes.append(record["elapsed_seconds_display_only"])
        if "rational_operations" in record.get("work", {}):
            operations.append(record["work"]["rational_operations"])
            max_bits.append(record["work"].get("max_rational_bits", 0))
        if record["status"] == "UNKNOWN":
            unknown_ledger.append({key: record[key] for key in (
                "query_id", "status", "reason_codes", "reason", "collision_margin_lower",
                "contact_margin_lower", "work", "elapsed_seconds_display_only",
            ) if key in record})
        if record["status"] in {"INVALID_INPUT", "EXECUTION_FAILURE"}:
            failure_ledger.append({key: record[key] for key in (
                "query_id", "status", "reason_codes", "reason", "work", "elapsed_seconds_display_only",
            ) if key in record})

    group_certified = sum(any(r["status"] == "CERTIFIED" for r in group) for group in action_groups.values())
    all_unknown_groups = sum(all(r["status"] == "UNKNOWN" for r in group) for group in action_groups.values())
    strata_summary = {}
    for name, values in strata.items():
        strata_summary[name] = {
            key: {"counts": dict(sorted(count.items())), "queries": sum(count.values())}
            for key, count in sorted(values.items())
        }
    report = {
        "schema": "ddwmr-g2-development-pilot-summary-v1",
        "disposition": "DEVELOPMENT_PILOT_ONLY; NOT_LOCKED; NO_G2_G4_PROMOTION",
        "method": "one-hold finite-cell whole-hold interval-hull fallback, predictor depth n=1",
        "profile_id": "DEV_FALLBACK_N1_PILOT_V1",
        "original_grid_denominator_per_method_profile": manifest["original_query_count_per_method_profile"],
        "selected_pilot_denominator": manifest["selected_query_count"],
        "not_run_original_query_count": manifest["not_run_query_count"],
        "status_counts_on_pilot": dict(sorted(counts.items())),
        "pilot_certified_fraction": f"{counts['CERTIFIED']}/{len(records)}",
        "original_grid_certified_fraction_not_estimable": "No full-grid run; report pilot only and retain 1944 denominator.",
        "state_scene_horizon_groups": len(action_groups),
        "groups_with_at_least_one_certified_action": group_certified,
        "all_nine_actions_unknown_groups": all_unknown_groups,
        "action_vectors": {
            "|".join(key): [r["status"] for r in sorted(group, key=lambda r: next(i for i, a in enumerate(benchmark["actions"]) if a["id"] == r["action_id"]))]
            for key, group in sorted(action_groups.items())
        },
        "strata": strata_summary,
        "lower_margin_bounds": {
            "collision_m": summarize_values(collision_margins),
            "contact_N": summarize_values(contact_margins),
        },
        "widths_and_radii": {
            "predictor_center_internal_component_widths_physical": summarize_values(widths),
            "internal_error_radius_physical": summarize_values(radii),
            "total_internal_enclosure_component_widths_physical": summarize_values(total_widths),
        },
        "work": {
            "rational_operations_per_completed_query": summarize_values([Fraction(x) for x in operations]),
            "max_rational_bits_seen": max(max_bits, default=0),
            "elapsed_seconds_display_only": {
                "count": len(runtimes), "min": min(runtimes) if runtimes else None,
                "median": sorted(runtimes)[(len(runtimes) - 1) // 2] if runtimes else None,
                "max": max(runtimes) if runtimes else None,
                "sum": round(sum(runtimes), 6) if runtimes else None,
            },
            "elapsed_time_is_not_a_safety_predicate": True,
        },
        "unknown_ledger_path": "results/validation/g2/dev_pilot_unknown_ledger_v1.jsonl",
        "failure_ledger_path": "results/validation/g2/dev_pilot_failure_ledger_v1.jsonl",
        "limitations": [
            "Only 216 preselected queries were evaluated; 1728 original IDs remain NOT_RUN.",
            "Synthetic order-one parameter family only; no physical provenance.",
            "One whole-hold predictor hull; no-op time-panel refinement, no parameter/state splitting or refined-kernel comparator.",
            "No external validated-reachability baseline and no predeclared coverage threshold.",
            "CERTIFIED is implementation evidence pending independent scientific review; UNKNOWN does not imply unsafe.",
        ],
    }
    summary_path = ROOT / args.summary if args.summary else (base / "dev_pilot_summary_v1.json" if args.records.endswith("dev_pilot_records_v1.jsonl") else records_path.with_name(records_path.stem + "_summary.json"))
    unknown_path = ROOT / args.unknown_ledger if args.unknown_ledger else (base / "dev_pilot_unknown_ledger_v1.jsonl" if args.records.endswith("dev_pilot_records_v1.jsonl") else records_path.with_name(records_path.stem + "_unknown_ledger.jsonl"))
    failure_path = ROOT / args.failure_ledger if args.failure_ledger else (base / "dev_pilot_failure_ledger_v1.jsonl" if args.records.endswith("dev_pilot_records_v1.jsonl") else records_path.with_name(records_path.stem + "_failure_ledger.jsonl"))
    report["records_path"] = str(records_path.relative_to(ROOT))
    report["unknown_ledger_path"] = str(unknown_path.relative_to(ROOT))
    report["failure_ledger_path"] = str(failure_path.relative_to(ROOT))
    summary_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    unknown_path.write_text(
        "".join(json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n" for x in unknown_ledger), encoding="utf-8"
    )
    failure_path.write_text(
        "".join(json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n" for x in failure_ledger), encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in report.items() if k not in {"action_vectors", "strata", "lower_margin_bounds", "widths_and_radii", "limitations"}}, sort_keys=True))


if __name__ == "__main__":
    main()
