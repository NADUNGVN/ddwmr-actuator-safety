"""Run exactly one isolated v5 saved-proof mutation audit trial."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

from . import checker_v4 as checker

ROOT = Path(__file__).resolve().parents[3]
TRIALS = (
    "untouched_baseline",
    "changed_source",
    "changed_protocol_input",
    "omitted_final_slab",
    "reset_fixed_label_hash",
    "altered_contact_inequality",
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_tree(base: Path, binding: dict[str, Any], binding_bytes: bytes, row: dict[str, Any]) -> tuple[Path, Path]:
    files = set(binding["source_files"])
    files.update((binding["protocol_path"], binding["profile_path"], binding["binding_path"]))
    for rel in sorted(files):
        source = ROOT / rel
        target = base / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(binding_bytes if rel == binding["binding_path"] else source.read_bytes())
    row_path = base / "mutation_input" / "row.json"
    write_json(row_path, row)
    return base / binding["binding_path"], row_path


def mutate_trial(label: str, tree_root: Path, protocol_path: Path, row_path: Path, binding: dict[str, Any]) -> str | None:
    if label == "untouched_baseline":
        return None
    if label == "changed_source":
        candidates = [p for p in binding["source_files"] if p.startswith("validation/autonomous_w2/g2/")]
        if not candidates:
            raise ValueError("NO_G2_SCIENTIFIC_SOURCE_IN_CLOSURE")
        rel = sorted(candidates)[0]
        source = tree_root / rel
        source.write_bytes(source.read_bytes() + b"\n# isolated mutation trial\n")
        return rel
    if label == "changed_protocol_input":
        protocol = read_json(protocol_path)
        protocol["task"]["required_progress_m"] = "71/200"
        write_json(protocol_path, protocol)
        return binding["protocol_path"]
    row = read_json(row_path)
    if label == "omitted_final_slab":
        row["slabs"].pop()
    elif label == "reset_fixed_label_hash":
        row["slabs"][1]["label_image_sha256"] = "0" * 64
    elif label == "altered_contact_inequality":
        row["slabs"][0]["contact"]["margin_lower_N"] = "999/1"
    else:
        raise ValueError("UNKNOWN_MUTATION_TRIAL")
    write_json(row_path, row)
    return None


def run_one(label: str, binding_path: Path, record_path: Path, scratch_root: Path) -> dict[str, Any]:
    if label not in TRIALS:
        raise ValueError("UNKNOWN_MUTATION_TRIAL")
    binding_bytes = binding_path.read_bytes()
    binding = json.loads(binding_bytes.decode("utf-8"))
    row = read_json(record_path)
    for rel, expected in binding["source_files"].items():
        if sha(ROOT / rel) != expected:
            raise RuntimeError(f"SOURCE_HASH_CHANGED_BEFORE_MUTATION_AUDIT:{rel}")
    if sha(ROOT / binding["protocol_path"]) != binding["protocol_sha256"] or sha(ROOT / binding["profile_path"]) != binding["profile_sha256"]:
        raise RuntimeError("FROZEN_INPUT_CHANGED_BEFORE_MUTATION_AUDIT")

    scratch_root.mkdir(parents=True, exist_ok=False)
    try:
        with tempfile.TemporaryDirectory(prefix=f"{label}-", dir=scratch_root) as temp:
            tree_root = Path(temp)
            trial_binding, trial_row = prepare_tree(tree_root, binding, binding_bytes, copy.deepcopy(row))
            protocol_path = tree_root / binding["protocol_path"]
            mutated_path = mutate_trial(label, tree_root, protocol_path, trial_row, binding)
            original_root = checker.ROOT
            checker.ROOT = tree_root
            try:
                try:
                    audited = checker.audit(trial_binding, trial_row)
                except BaseException as exc:
                    if label == "untouched_baseline":
                        return {"trial": label, "status": "FAILED", "rejection": f"{type(exc).__name__}:{exc}"}
                    return {
                        "trial": label,
                        "status": "REJECTED_AS_REQUIRED",
                        "rejection": f"{type(exc).__name__}:{exc}",
                        "mutated_path": mutated_path,
                    }
                if label != "untouched_baseline":
                    return {"trial": label, "status": "FAILED_MUTATION_ACCEPTED", "mutated_path": mutated_path}
                return {"trial": label, "status": "PASS", "replayed": audited.get("replayed") is True}
            finally:
                checker.ROOT = original_root
    finally:
        shutil.rmtree(scratch_root, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trial", required=True, choices=TRIALS)
    parser.add_argument("--binding", required=True)
    parser.add_argument("--record", required=True)
    parser.add_argument("--scratch-root", required=True)
    args = parser.parse_args()

    def rooted(value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else ROOT / path

    result = run_one(args.trial, rooted(args.binding), rooted(args.record), rooted(args.scratch_root))
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] in ("PASS", "REJECTED_AS_REQUIRED") else 3


if __name__ == "__main__":
    raise SystemExit(main())
