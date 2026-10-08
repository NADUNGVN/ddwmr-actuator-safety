"""Pre-run checks for the frozen-grid v3 arithmetic correction; no native rows."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
OUT_REL = "results/validation/autonomous_w2/g2/pre_run_validation_v3.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, Any]:
    output = ROOT / OUT_REL
    if output.exists():
        raise FileExistsError("V3_PRE_RUN_VALIDATION_RECEIPT_ALREADY_EXISTS")
    v1 = json.loads((ROOT / "results/validation/autonomous_w2/g2/development_v1/stage_receipt.json").read_text(encoding="utf-8"))
    v2 = json.loads((ROOT / "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json").read_text(encoding="utf-8"))
    legacy = json.loads((ROOT / "research/autonomous_w2/g2/development_plan_v2.json").read_text(encoding="utf-8"))
    if v1.get("attempts_counted") != 6 or v2.get("attempts_counted") != 6 or v1.get("held_out_rows") != 0 or v2.get("held_out_rows") != 0:
        raise RuntimeError("PRIOR_DEVELOPMENT_COUNTS_OR_HELD_OUT_SCOPE_MISMATCH")
    if v1.get("legacy_800_row_study") != "NOT_RUN" or v2.get("legacy_800_row_study") != "NOT_RUN" or legacy.get("legacy_800_row_study") != "NOT_RUN":
        raise RuntimeError("LEGACY_800_ROW_SCOPE_CHANGED")
    if sum(v1.get("status_counts", {}).values()) != 6 or sum(v2.get("status_counts", {}).values()) != 6:
        raise RuntimeError("PRESERVED_STAGE_DENOMINATOR_MISMATCH")
    fixtures_path = ROOT / "results/validation/autonomous_w2/g2/fixtures/fixed_grid_arithmetic_v3.json"
    fixtures = json.loads(fixtures_path.read_text(encoding="utf-8"))
    if fixtures.get("all_checks_pass") is not True:
        raise RuntimeError("FIXED_GRID_ARITHMETIC_FIXTURE_FAILED")
    if fixtures.get("source_sha256", {}).get("validation/autonomous_w2/g2/rational_interval_v3.py") != sha(ROOT / "validation/autonomous_w2/g2/rational_interval_v3.py"):
        raise RuntimeError("FIXED_GRID_ARITHMETIC_FIXTURE_SOURCE_HASH_MISMATCH")
    report = {
        "schema": "G2_W2_PRE_RUN_VALIDATION_v3",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "native_attempts_before_v3": 12,
        "v3_planned_attempts_before_freeze": 0,
        "held_out_rows": 0,
        "legacy_800_row_study": "NOT_RUN",
        "prior_stages": {
            "development_v1": {"path": "results/validation/autonomous_w2/g2/development_v1/stage_receipt.json", "sha256": sha(ROOT / "results/validation/autonomous_w2/g2/development_v1/stage_receipt.json"), "attempts": 6, "status_counts": v1["status_counts"]},
            "development_v2": {"path": "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json", "sha256": sha(ROOT / "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json"), "attempts": 6, "status_counts": v2["status_counts"]},
        },
        "checks": {"outward_fixed_grid_arithmetic": {"path": "results/validation/autonomous_w2/g2/fixtures/fixed_grid_arithmetic_v3.json", "sha256": sha(fixtures_path), "fixture": fixtures}, "legacy_800_row_manifest_preserved": True, "no_query_or_worker_called": True},
    }
    output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
