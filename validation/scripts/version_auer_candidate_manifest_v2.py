"""Create a v2 preparation manifest from the frozen v1 1,944-ID universe.

This changes only the proposed profile metadata. It never evaluates queries or
joins R3 outcomes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "results/validation/g4/auer2013/auer_matched_candidate_manifest_v1.json"
R2 = ROOT / "results/validation/g2/r2/development_manifest_r2_v1.json"
DEFAULT_OUTPUT = ROOT / "results/validation/g4/auer2013/auer_matched_candidate_manifest_v2.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    source = json.loads(INPUT.read_text(encoding="utf-8"))
    r2 = json.loads(R2.read_text(encoding="utf-8"))
    ids = [item.get("query_id") for item in source.get("queries", [])]
    original = r2.get("original_query_ids")
    if len(ids) != 1944 or ids != original or len(set(ids)) != 1944:
        raise SystemExit("v1 Auer manifest does not exactly match the frozen 1,944 R2 IDs")
    if any(item.get("status") != "NOT_RUN" for item in source["queries"]):
        raise SystemExit("v1 candidate manifest contains a non-NOT_RUN status")
    if source.get("execution", {}).get("comparison_run") is not False:
        raise SystemExit("v1 source manifest indicates an evaluation was run")

    payload: dict[str, Any] = json.loads(json.dumps(source))
    payload["schema"] = "ddwmr-g4-auer-candidate-manifest-v2"
    payload["status"] = "PREPARATION_ONLY_PROFILE_DRAFT_NOT_EVALUATED_NOT_LOCKED"
    payload["candidate_profile_id"] = "AUER_WSL_CANDIDATE_V2_UNAPPROVED"
    payload["candidate_settings_pending_independent_review"].update({
        "max_steps_per_query": 1000,
        "max_step_width_seconds": {"num": "1", "den": "1000"},
        "step_width_interpretation": (
            "Maximum accepted step width, not a fixed integration grid. The 1000-step cap permits at most 10x "
            "refinement of the 0.1 s maximum hold relative to 0.001 s, subject to inclusion and work caps; "
            "exhaustion remains UNKNOWN. This is proposed, not evidence of convergence."
        ),
        "IEEE754_backend_target": (
            "WSL2 Ubuntu 24.04 x86-64, GCC 13.3, PROFIL/BIAS 2.0.8 x86-64 Linux profile. Local build and finite "
            "checks pass, but the documented glibc/libm sin/cos error bound and compatibility with historical "
            "PROFIL/BIAS 2.0.2/2.0.4 remain unresolved; NOT APPROVED for certificates."
        ),
        "status": "PROPOSED_SETTINGS_ONLY_NOT_FROZEN_FOR_EXECUTION",
    })
    payload["execution"].update({
        "comparison_run": False,
        "auer_status_all_queries": "NOT_RUN",
        "r3_status_joined": False,
        "scope": "Preparation metadata only; no matched query or ODE enclosure was evaluated.",
    })
    payload["source_manifest_v1_sha256"] = sha256(INPUT)
    payload["r2_ids_preserved_exactly"] = True

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "output": str(args.output),
        "query_count": len(payload["queries"]),
        "all_not_run": True,
        "comparison_run": False,
        "max_steps_per_query": payload["candidate_settings_pending_independent_review"]["max_steps_per_query"],
        "manifest_sha256": sha256(args.output),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
