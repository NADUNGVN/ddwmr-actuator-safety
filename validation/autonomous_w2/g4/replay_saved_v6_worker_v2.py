"""Read-only, resource-bounded replay of one already saved G2 v6 row."""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from validation.autonomous_w2.g4.matched_v6_common_v2 import (
    PROJECT, configure_integer_string_limit, initial_state_from_task, scene_from_task,
    score_serialize_replay_progress, sha256_file, strict_json, summarize_common, write_json,
)
from validation.autonomous_w2.g4.v6_snapshot_v2.checker_centered_v6 import audit as replay_v6_row
from validation.autonomous_w2.g4.v6_w2_adapter_v2 import convert_v6_row_to_segments
from validation.g2.rational import Budget


def run(binding_path: Path, comparison_id: str, row_path: Path, output_dir: Path) -> int:
    binding_path, row_path, output_dir = binding_path.resolve(), row_path.resolve(), output_dir.resolve()
    if not row_path.is_file():
        raise ValueError("SAVED_G2_ROW_MISSING")
    row_hash = sha256_file(row_path)
    native_replay = replay_v6_row(binding_path, row_path)
    if not native_replay.get("replayed"):
        raise ValueError(f"SAVED_G2_NATIVE_REPLAY_FAILED:{native_replay}")
    row = strict_json(row_path)
    core_binding = strict_json(binding_path)
    root = Path(__file__).resolve().parents[3]
    task_path = root / "research/autonomous_w2/g2/task_protocol_v1.json"
    task = strict_json(task_path)
    candidate = root / "research/autonomous_w2/g4/matched_v6_task_development_v2"
    protocol = strict_json(candidate / "protocol_v2.json")
    profile = strict_json(candidate / "g2_profile_centered_v6.json")
    benchmark = strict_json(candidate / "benchmark_v2.json")
    common_profile = strict_json(candidate / "common_profile_v2.json")
    action = next(item for item in protocol["actions"] if item["comparison_id"] == comparison_id)
    adapter_binding = dict(core_binding)
    adapter_binding.update({
        "comparison_id": comparison_id,
        "peer_action_id": action["peer_action_id"],
        "peer_release_sha256": protocol["peer_release"]["sha256"],
        "physical_input_sha256": action["physical_input_sha256"],
        "native_row_sha256": row_hash,
        "peer_saved_row_sha256": row_hash,
    })
    common_budget = Budget(
        max_bits=int(common_profile["max_rational_bits"]),
        max_operations=int(common_profile["max_rational_operations_per_common_stage"]),
        wall_seconds=Fraction(int(common_profile["wall_seconds"])),
    )
    configure_integer_string_limit(int(common_profile["max_integer_string_digits"]))
    segments, adapter_work = convert_v6_row_to_segments(
        row, task, protocol, adapter_binding, profile, benchmark, common_budget,
    )
    common_record, common_replay, progress, common_files = score_serialize_replay_progress(
        segments, benchmark, scene_from_task(task), Fraction(task["task"]["hold_s"]),
        initial_state_from_task(task, common_budget), sqrt_bisections=int(common_profile["sqrt_bisections"]),
        budget=common_budget, common_record_path=output_dir / "common_record.json",
        progress_path=output_dir / "progress.json",
        max_record_bytes=int(common_profile["max_common_record_bytes"]),
        max_progress_bytes=int(common_profile["max_progress_record_bytes"]),
    )
    if not common_replay.get("replayed"):
        raise ValueError(f"SAVED_G2_COMMON_REPLAY_FAILED:{common_replay}")
    bounds = [Fraction(int(item["num"]), int(item["den"])) for item in progress["progress_enclosure_m"]]
    result = {
        "schema": "ddwmr-g4-w2-saved-v6-readonly-replay-v2",
        "comparison_id": comparison_id,
        "saved_row_path": row_path.relative_to(root).as_posix(),
        "saved_row_sha256": row_hash,
        "saved_binding_path": binding_path.relative_to(root).as_posix(),
        "saved_binding_sha256": sha256_file(binding_path),
        "native_replay": native_replay,
        "native_replay_status": "PASS",
        "common_record_path": (output_dir / "common_record.json").relative_to(root).as_posix(),
        "common_progress_path": (output_dir / "progress.json").relative_to(root).as_posix(),
        "common_summary": summarize_common(common_record),
        "common_replay": common_replay,
        "common_replay_status": "PASS",
        "common_progress": progress,
        "progress_lower_meets_threshold": bounds[0] >= Fraction(7, 20),
        "task_eligible": common_record.get("predicate_status") == "PASS_ON_SUPPLIED_TUBE" and bounds[0] >= Fraction(7, 20),
        "adapter_work": adapter_work,
        "common_files": common_files,
        "fresh_native_calls": 0,
        "read_only_saved_row_replay": True,
    }
    write_json(output_dir / "saved_replay_result.json", result, max_bytes=1_048_576)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding", required=True)
    parser.add_argument("--comparison-id", required=True)
    parser.add_argument("--row", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    return run(Path(args.binding), args.comparison_id, Path(args.row), Path(args.output_dir))


if __name__ == "__main__":
    raise SystemExit(main())
