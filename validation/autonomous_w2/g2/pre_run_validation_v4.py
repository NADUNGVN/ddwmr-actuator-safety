"""V4 source-correction preflight using saved receipts and analytic fixtures only."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
OUT_REL = "results/validation/autonomous_w2/g2/pre_run_validation_v4.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, Any]:
    output = ROOT / OUT_REL
    if output.exists():
        raise FileExistsError("V4_PRE_RUN_RECEIPT_ALREADY_EXISTS")
    v1 = json.loads((ROOT / "results/validation/autonomous_w2/g2/development_v1/stage_receipt.json").read_text(encoding="utf-8"))
    v2 = json.loads((ROOT / "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json").read_text(encoding="utf-8"))
    v3 = json.loads((ROOT / "results/validation/autonomous_w2/g2/development_v3/stage_receipt.json").read_text(encoding="utf-8"))
    if [v1.get("attempts_counted"), v2.get("attempts_counted"), v3.get("attempts_counted")] != [6, 6, 3]:
        raise RuntimeError("PRESERVED_PRIOR_ATTEMPT_DENOMINATOR_MISMATCH")
    if any(item.get("held_out_rows") != 0 or item.get("legacy_800_row_study") != "NOT_RUN" for item in (v1, v2, v3)):
        raise RuntimeError("HELD_OUT_OR_LEGACY_STUDY_SCOPE_CHANGED")
    if v3.get("status_counts") != {"EXECUTION_FAILURE": 3}:
        raise RuntimeError("V3_FAILURE_STAGE_STATUS_MISMATCH")
    fixture_path = ROOT / "results/validation/autonomous_w2/g2/fixtures/status_aggregation_v4.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    if fixture.get("all_cases_pass") is not True:
        raise RuntimeError("V4_STATUS_AGGREGATION_FIXTURE_FAILED")
    for rel, expected in fixture.get("source_sha256", {}).items():
        if sha(ROOT / rel) != expected:
            raise RuntimeError(f"V4_FIXTURE_SOURCE_HASH_MISMATCH:{rel}")
    report = {
        "schema": "G2_W2_PRE_RUN_VALIDATION_v4",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "native_attempts_before_v4": 15,
        "held_out_rows": 0,
        "legacy_800_row_study": "NOT_RUN",
        "prior_stages": {
            name: {"path": rel, "sha256": sha(ROOT / rel), "attempts": stage.get("attempts_counted"), "status_counts": stage.get("status_counts")}
            for name, rel, stage in (
                ("v1", "results/validation/autonomous_w2/g2/development_v1/stage_receipt.json", v1),
                ("v2", "results/validation/autonomous_w2/g2/development_v2/stage_receipt.json", v2),
                ("v3", "results/validation/autonomous_w2/g2/development_v3/stage_receipt.json", v3),
            )
        },
        "checks": {"nested_margin_status_aggregation": {"path": "results/validation/autonomous_w2/g2/fixtures/status_aggregation_v4.json", "sha256": sha(fixture_path), "fixture": fixture}, "no_native_query_or_worker_called": True},
    }
    output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
