"""Run bounded replay mutations against one saved W2 proof row."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any, Callable

from . import checker_v4 as checker


ROOT = Path(__file__).resolve().parents[3]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def prepare_tree(base: Path, binding: dict[str, Any], binding_bytes: bytes, row: dict[str, Any]) -> tuple[Path, Path]:
    files = set(binding["source_files"])
    files.add(binding["protocol_path"])
    files.add(binding["profile_path"])
    files.add(binding["binding_path"])
    for rel in files:
        source = ROOT / rel
        target = base / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if rel == binding["binding_path"]:
            target.write_bytes(binding_bytes)
        else:
            shutil.copyfile(source, target)
    row_path = base / "mutation_input" / "row.json"
    write_json(row_path, row)
    return base / binding["binding_path"], row_path


def reject_trial(
    label: str,
    scratch_root: Path,
    binding: dict[str, Any],
    binding_bytes: bytes,
    row: dict[str, Any],
    mutate: Callable[[Path, Path, Path], None],
) -> dict[str, Any]:
    trial_root = scratch_root / label
    trial_root.mkdir(parents=True, exist_ok=False)
    binding_path, row_path = prepare_tree(trial_root, binding, binding_bytes, copy.deepcopy(row))
    protocol_path = trial_root / binding["protocol_path"]
    mutate(trial_root, protocol_path, row_path)
    original_root = checker.ROOT
    checker.ROOT = trial_root
    try:
        try:
            checker.audit(binding_path, row_path)
        except BaseException as exc:
            return {"trial": label, "status": "REJECTED_AS_REQUIRED", "rejection": f"{type(exc).__name__}:{exc}"}
        return {"trial": label, "status": "FAILED_MUTATION_ACCEPTED"}
    finally:
        checker.ROOT = original_root


def no_change(_root: Path, _protocol: Path, _record: Path) -> None:
    return


def mutate_source(root: Path, _protocol: Path, _record: Path) -> None:
    source = root / "validation/autonomous_w2/g2/producer_v2.py"
    source.write_bytes(source.read_bytes() + b"\n# mutation trial\n")


def mutate_input(_root: Path, protocol_path: Path, _record: Path) -> None:
    protocol = read_json(protocol_path)
    protocol["task"]["required_progress_m"] = "71/200"
    write_json(protocol_path, protocol)


def omit_slab(_root: Path, _protocol: Path, record_path: Path) -> None:
    record = read_json(record_path)
    record["slabs"].pop()
    write_json(record_path, record)


def reset_label(_root: Path, _protocol: Path, record_path: Path) -> None:
    record = read_json(record_path)
    record["slabs"][1]["label_image_sha256"] = "0" * 64
    write_json(record_path, record)


def alter_inequality(_root: Path, _protocol: Path, record_path: Path) -> None:
    record = read_json(record_path)
    record["slabs"][0]["contact"]["margin_lower_N"] = "999/1"
    write_json(record_path, record)


def run(binding_path: Path, row_path: Path, report_path: Path) -> dict[str, Any]:
    binding_bytes = binding_path.read_bytes()
    binding = json.loads(binding_bytes.decode("utf-8"))
    row = read_json(row_path)
    for rel, expected in binding["source_files"].items():
        if sha(ROOT / rel) != expected:
            raise RuntimeError(f"SOURCE_HASH_CHANGED_BEFORE_MUTATION_AUDIT:{rel}")
    if sha(ROOT / binding["protocol_path"]) != binding["protocol_sha256"] or sha(ROOT / binding["profile_path"]) != binding["profile_sha256"]:
        raise RuntimeError("FROZEN_INPUT_CHANGED_BEFORE_MUTATION_AUDIT")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(prefix="g2-w2-mutations-", dir=report_path.parent) as temp:
        scratch = Path(temp)
        baseline_binding, baseline_row = prepare_tree(scratch / "baseline", binding, binding_bytes, row)
        original_root = checker.ROOT
        checker.ROOT = scratch / "baseline"
        try:
            baseline = checker.audit(baseline_binding, baseline_row)
        finally:
            checker.ROOT = original_root
        results.append({"trial": "untouched_baseline", "status": "PASS" if baseline.get("replayed") else "FAILED", "replayed": baseline.get("replayed")})
        results.append(reject_trial("changed_source", scratch, binding, binding_bytes, row, mutate_source))
        results.append(reject_trial("changed_protocol_input", scratch, binding, binding_bytes, row, mutate_input))
        results.append(reject_trial("omitted_final_slab", scratch, binding, binding_bytes, row, omit_slab))
        results.append(reject_trial("reset_fixed_label_hash", scratch, binding, binding_bytes, row, reset_label))
        results.append(reject_trial("altered_contact_inequality", scratch, binding, binding_bytes, row, alter_inequality))
    summary = {
        "schema": "G2_W2_ADVERSARIAL_REPLAY_MUTATIONS_v4",
        "binding_path": binding["binding_path"],
        "binding_sha256": hashlib.sha256(binding_bytes).hexdigest(),
        "record_path": row_path.resolve().relative_to(ROOT).as_posix(),
        "record_sha256": sha(row_path),
        "trial_count": len(results),
        "all_required_mutations_rejected": all(item["status"] in ("PASS", "REJECTED_AS_REQUIRED") for item in results),
        "results": results,
    }
    write_json(report_path, summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding", required=True)
    parser.add_argument("--record", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    def rooted(value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else ROOT / path

    binding = rooted(args.binding)
    record = rooted(args.record)
    report = rooted(args.report)
    summary = run(binding, record, report)
    print(json.dumps(summary, sort_keys=True, indent=2))
    return 0 if summary["all_required_mutations_rejected"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
