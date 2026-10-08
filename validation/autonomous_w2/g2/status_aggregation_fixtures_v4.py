"""Nonquery regression fixtures for v4's nested collision/contact status keys."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .producer_v4 import _certificate_status


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/validation/autonomous_w2/g2/fixtures/status_aggregation_v4.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slab(collision: str = "1/10", contact: str = "1/5") -> dict[str, Any]:
    return {"collision": {"margin_lower_m": collision}, "contact": {"margin_lower_N": contact}}


def run() -> dict[str, Any]:
    if OUT.exists():
        raise FileExistsError("V4_STATUS_FIXTURE_ALREADY_EXISTS")
    cases = {
        "nonnegative_two_slab_certificate": _certificate_status([slab(), slab("0/1", "0/1")], True) == (True, []),
        "negative_collision_keeps_unknown_reason": _certificate_status([slab("-1/100")], True) == (False, ["COLLISION_MARGIN_NEGATIVE_ON_A_SLAB"]),
        "negative_contact_keeps_unknown_reason": _certificate_status([slab("1/10", "-1/100")], True) == (False, ["CONTACT_MARGIN_NEGATIVE_ON_A_SLAB"]),
        "failed_clip_branch_keeps_unknown_reason": _certificate_status([slab()], False) == (False, ["CLIP_INTERIOR_NOT_ESTABLISHED_ON_EVERY_SLAB"]),
        "all_three_failed_predicates_are_reported": _certificate_status([slab("-1/10", "-1/20")], False) == (False, ["CLIP_INTERIOR_NOT_ESTABLISHED_ON_EVERY_SLAB", "COLLISION_MARGIN_NEGATIVE_ON_A_SLAB", "CONTACT_MARGIN_NEGATIVE_ON_A_SLAB"]),
    }
    result = {
        "schema": "G2_W2_STATUS_AGGREGATION_FIXTURES_v4",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "fixture_kind": "direct rational predicate aggregation; no task protocol or benchmark rows",
        "cases": cases,
        "all_cases_pass": all(cases.values()),
        "source_sha256": {
            "validation/autonomous_w2/g2/producer_v4.py": sha(ROOT / "validation/autonomous_w2/g2/producer_v4.py"),
            "validation/autonomous_w2/g2/checker_v4.py": sha(ROOT / "validation/autonomous_w2/g2/checker_v4.py"),
            "validation/autonomous_w2/g2/status_aggregation_fixtures_v4.py": sha(Path(__file__)),
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    if not result["all_cases_pass"]:
        raise AssertionError("STATUS_AGGREGATION_FIXTURE_FAILED")
    return result


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
