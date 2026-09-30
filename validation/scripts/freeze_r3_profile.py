"""Create the immutable R3 profile and conditional continuation list."""

from __future__ import annotations

import json
from pathlib import Path

from validation.g2.evaluator import DISTANCE_METHOD_R3, R3_METHOD_ID, ROOT
from validation.g2.hashing import semantic_json_file_sha256, semantic_json_sha256
from validation.g2.provenance import current_revision, specification_ledger


PILOT_R2 = Path("validation/configs/dev_pilot_r2_v1.json")
MANIFEST_R2 = Path("results/validation/g2/r2/development_manifest_r2_v1.json")
R3_PILOT = Path("validation/configs/dev_pilot_r3_v1.json")
R3_FULL_GRID = Path("results/validation/g2/r3/full_grid_continuation_manifest_r3_v1.json")
R3_SPEC_LEDGER = Path("results/validation/g2/r3/specification_content_ledger_r3_v1.json")

SPECIFICATION_PATHS = [
    "AGENTS.md",
    "research_context/MASTER_RESEARCH_CONTEXT_v2.md",
    "research_context/DECISION_LOG.md",
    "research_context/LITERATURE_MATRIX.md",
    "research_context/REVIEW_GATE.md",
    "docs/LUNA_VALIDATION_HANDOFF_v1.md",
    "docs/CODEX_TO_LUNA_G2_VALIDATION_R3.md",
    "research/theorem_notes/G2_FINITE_EVALUATOR_SPEC_v1.md",
    "research/benchmarks/G2_USEFULNESS_BENCHMARK_SPEC_v1.md",
    "docs/LUNA_G2_DISTANCE_ADDENDUM_R3_v1.md",
]


def load(path: Path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write_new(path: Path, value: dict) -> None:
    output = ROOT / path
    if output.exists():
        raise SystemExit(f"refusing to overwrite frozen R3 input: {path}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    revision = current_revision()
    old_pilot = load(PILOT_R2)
    old_manifest = load(MANIFEST_R2)
    ledger = specification_ledger(revision, SPECIFICATION_PATHS)

    pilot = json.loads(json.dumps(old_pilot))
    pilot["schema"] = "ddwmr-g2-development-pilot-r3-v1"
    pilot["status"] = "FROZEN_R3_DEVELOPMENT_PILOT_NOT_LOCKED"
    pilot["hash_protocol_id"] = "ddwmr-semantic-json-sha256-v2"
    profile = pilot["profile"]
    profile["id"] = "DEV_FALLBACK_N1_PILOT_R3_DYADIC_P24_BITS16384_V1"
    profile["distance_method_id"] = DISTANCE_METHOD_R3
    profile["distance_rounding_precision_bits"] = 24
    profile["specification_bundle_sha256"] = ledger["specification_bundle_sha256"]
    profile["reason_for_cap"] = (
        "One predeclared R3 development profile using the unchanged R2 16384-bit, 1000000-operation, "
        "15-second/query caps and unchanged Taylor, predictor, state, parameter, time, voltage and physics settings. "
        "The only numerical-method change is fixed p=24 exact directed dyadic coordinate-gap enclosure before "
        "squaring. This is one bounded diagnostic, not cap/precision tuning or a locked comparison."
    )
    profile["distance_rounding_contract"] = "exact_floor_ceil_integer_shift_division; all primitives charged to Budget"

    original_ids = old_manifest["original_query_ids"]
    selected_ids = old_manifest["selected_query_ids"]
    remaining_ids = old_manifest["not_run_query_ids"]
    if len(original_ids) != 1944 or len(selected_ids) != 216 or len(remaining_ids) != 1728:
        raise SystemExit("R2 original grid or frozen selection counts do not match the R3 contract")
    if set(selected_ids) & set(remaining_ids) or set(selected_ids) | set(remaining_ids) != set(original_ids):
        raise SystemExit("R2 pilot and remaining IDs do not exactly partition the original query universe")

    full_grid = {
        "schema": "ddwmr-g2-r3-conditional-full-grid-manifest-v1",
        "status": "FROZEN_CONDITIONAL_CONTINUATION_NOT_STARTED",
        "method_id": R3_METHOD_ID,
        "distance_method_id": DISTANCE_METHOD_R3,
        "profile_id": profile["id"],
        "profile_semantic_sha256": semantic_json_sha256(profile),
        "specification_bundle_sha256": ledger["specification_bundle_sha256"],
        "original_query_count_per_method_profile": 1944,
        "conditional_query_count": len(remaining_ids),
        "selected_query_ids": remaining_ids,
        "rule_frozen_before_pilot": (
            "Run each of the 1728 remaining original IDs exactly once only if all 216 pilot outcomes are "
            "non-resource-limited and valid, every completed proof replays, and all input/spec/source provenance "
            "checks pass. Otherwise do not run this manifest. No cap or precision change is allowed."
        ),
        "source_pilot_manifest": MANIFEST_R2.as_posix(),
        "source_pilot_manifest_semantic_sha256": semantic_json_file_sha256(ROOT / MANIFEST_R2),
        "selection_unchanged_from_r2_not_run_ids": True,
    }

    write_new(R3_SPEC_LEDGER, ledger)
    write_new(R3_PILOT, pilot)
    write_new(R3_FULL_GRID, full_grid)
    print(json.dumps({
        "schema": "ddwmr-g2-r3-prepilot-profile-freeze-v1",
        "generated_from_commit": revision,
        "profile_id": profile["id"],
        "method_id": R3_METHOD_ID,
        "distance_method_id": DISTANCE_METHOD_R3,
        "precision_bits": 24,
        "selected_pilot_queries": len(selected_ids),
        "conditional_remaining_queries": len(remaining_ids),
        "specification_bundle_sha256": ledger["specification_bundle_sha256"],
        "pilot_config_semantic_sha256": semantic_json_file_sha256(ROOT / R3_PILOT),
        "full_grid_manifest_semantic_sha256": semantic_json_file_sha256(ROOT / R3_FULL_GRID),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
