"""Capture non-query regression evidence for the versioned W2 G2 repair."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .integer_serialization_fixture_v2 import run as run_v2_fixtures
from .r3_input_fixtures import verify as verify_r3_inputs


ROOT = Path(__file__).resolve().parents[3]
OUT_REL = "results/validation/autonomous_w2/g2/pre_run_validation_v2.json"
V1_STAGE_REL = "results/validation/autonomous_w2/g2/development_v1/stage_receipt.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, Any]:
    output = ROOT / OUT_REL
    if output.exists():
        raise FileExistsError("V2_PRE_RUN_VALIDATION_RECEIPT_ALREADY_EXISTS")
    prior = json.loads((ROOT / V1_STAGE_REL).read_text(encoding="utf-8"))
    if prior.get("attempts_counted") != 6 or prior.get("held_out_rows") != 0 or prior.get("legacy_800_row_study") != "NOT_RUN":
        raise RuntimeError("PRESERVED_V1_FAILURE_COUNT_OR_SCOPE_MISMATCH")
    fixtures = run_v2_fixtures()
    if fixtures.get("status") != "PASS" or fixtures.get("query_or_run_query_calls") != 0:
        raise RuntimeError("V2_NONQUERY_FIXTURE_FAILED")
    r3 = verify_r3_inputs()
    if r3.get("status") != "PASS" or r3.get("run_query_calls") != 0:
        raise RuntimeError("R3_INPUT_NONQUERY_FIXTURES_FAILED")
    report = {
        "schema": "G2_W2_PRE_RUN_VALIDATION_v2",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "native_attempts_before_receipt": 6,
        "native_attempts_in_v2_plan": 0,
        "held_out_rows": 0,
        "legacy_800_row_study": "NOT_RUN",
        "v1_failure_stage": {"path": V1_STAGE_REL, "sha256": sha(ROOT / V1_STAGE_REL), "attempts_counted": 6, "status_counts": prior["status_counts"]},
        "checks": {
            "integer_serialization_and_semantic_hash_fixtures": fixtures,
            "r3_input_nonquery_fixtures": r3,
            "existing_job_supervisor_fixture": {
                "path": "results/validation/autonomous_w2/g2/job_supervisor_fixture_v1.json",
                "sha256": sha(ROOT / "results/validation/autonomous_w2/g2/job_supervisor_fixture_v1.json"),
                "status": json.loads((ROOT / "results/validation/autonomous_w2/g2/job_supervisor_fixture_v1.json").read_text(encoding="utf-8"))["status"],
            },
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as stream:
        stream.write(json.dumps(report, sort_keys=True, indent=2, ensure_ascii=True).encode("utf-8") + b"\n")
        stream.flush()
    return report


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
