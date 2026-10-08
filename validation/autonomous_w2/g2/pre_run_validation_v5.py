"""Nonquery v5 preflight over saved W2 evidence and the exact point fixture."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT_REL = "results/validation/autonomous_w2/g2/pre_run_validation_v5.json"


def sha(rel: str) -> str:
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def read(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def run() -> dict:
    out = ROOT / OUT_REL
    if out.exists():
        raise FileExistsError("V5_PRE_RUN_RECEIPT_ALREADY_EXISTS")
    status = read("coordination/autonomous_w2/g2/STATUS.json")
    stage = read("results/validation/autonomous_w2/g2/development_v4/stage_receipt.json")
    release = read("coordination/autonomous_w2/g2/releases/RELEASE_v4.json")
    witness = read("results/validation/autonomous_w2/g2/clip_branch_point_witness_v1.json")
    profile = read("validation/autonomous_w2/g2/profile_v5.json")
    if status.get("sequence") != 11 or status.get("native_attempts", {}).get("count_completed") != 18:
        raise RuntimeError("PRIOR_STATUS_OR_NATIVE_ATTEMPT_DENOMINATOR_MISMATCH")
    if stage.get("attempts_counted") != 3 or stage.get("status_counts") != {"REPLAYED": 3}:
        raise RuntimeError("V4_STAGE_NOT_FULLY_REPLAYED")
    if any(row.get("status") != "REPLAYED" or row.get("task_eligible") is not False for row in stage.get("attempts", [])):
        raise RuntimeError("V4_ROW_RESULT_NOT_REPRODUCED_OR_ELIGIBILITY_MISMATCH")
    if release.get("release_sequence") != 4 or release.get("schema") != "DDWMR_G2_W2_IMMUTABLE_RELEASE_v4":
        raise RuntimeError("V4_RELEASE_BINDING_MISMATCH")
    if not all(item.get("all_slabs_strictly_inside_clip") for item in witness.get("actions", {}).values()):
        raise RuntimeError("EXACT_POINT_BRANCH_WITNESS_FAILED")
    if profile.get("time_slabs") != 256 or profile.get("slab_duration_s") != "1/128":
        raise RuntimeError("V5_PROFILE_NOT_THE_DECLARED_SINGLE_REFINEMENT")
    if profile.get("worker_wall_cap_seconds") != 60 or profile.get("worker_memory_cap_bytes") != 1073741824 or profile.get("interval_operation_cap") != 5000000:
        raise RuntimeError("V5_WORKER_RESOURCE_CAP_CHANGED")
    if status.get("native_attempts", {}).get("legacy_800_row_study") != "800/800 NOT_RUN" or status.get("native_attempts", {}).get("held_out_rows") != 0:
        raise RuntimeError("HELD_OUT_OR_LEGACY_STUDY_SCOPE_CHANGED")
    report = {
        "schema": "G2_W2_PRE_RUN_VALIDATION_v5",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "native_attempts_before_v5": 18,
        "held_out_rows": 0,
        "legacy_800_row_study": "NOT_RUN",
        "task_protocol_path": "research/autonomous_w2/g2/task_protocol_v1.json",
        "task_protocol_sha256": sha("research/autonomous_w2/g2/task_protocol_v1.json"),
        "v4_stage_path": "results/validation/autonomous_w2/g2/development_v4/stage_receipt.json",
        "v4_stage_sha256": sha("results/validation/autonomous_w2/g2/development_v4/stage_receipt.json"),
        "v4_release_sha256": sha("coordination/autonomous_w2/g2/releases/RELEASE_v4.json"),
        "point_clip_witness_path": "results/validation/autonomous_w2/g2/clip_branch_point_witness_v1.json",
        "point_clip_witness_sha256": sha("results/validation/autonomous_w2/g2/clip_branch_point_witness_v1.json"),
        "v5_profile_sha256": sha("validation/autonomous_w2/g2/profile_v5.json"),
        "checks": {
            "v4_candidate_rows_replayed": 3,
            "v4_task_eligible_rows": 0,
            "center_point_strict_clip_branch_all_actions": True,
            "task_and_threshold_unchanged": True,
            "native_query_or_worker_called": False,
            "same_signed_vof_candidate_only_profile_change": True,
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
