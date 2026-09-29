#!/usr/bin/env python3
"""Write exact SHA-256 hashes for the frozen pilot and generated evidence."""

from __future__ import annotations

import hashlib
from pathlib import Path

from validation.g2.evaluator import ROOT


PATHS = [
    "validation/configs/benchmark_v1.json",
    "validation/configs/dev_pilot_v1.json",
    "validation/scripts/generate_manifest.py",
    "results/validation/g2/development_manifest_v1.json",
    "results/validation/g2/SHA256SUMS_PRE_EVAL.txt",
    "results/validation/g2/dev_pilot_run_metadata_v1.json",
    "results/validation/g2/dev_pilot_records_v1.jsonl",
    "results/validation/g2/dev_pilot_record_check_v1.json",
    "results/validation/g2/dev_pilot_summary_v1.json",
    "results/validation/g2/dev_pilot_unknown_ledger_v1.jsonl",
    "results/validation/g2/dev_pilot_failure_ledger_v1.jsonl",
    "results/validation/g2/dev_pilot_records_v1_replay2_run_metadata.json",
    "results/validation/g2/dev_pilot_records_v1_replay2.jsonl",
    "results/validation/g2/dev_pilot_records_v1_replay2_record_check.json",
    "results/validation/g2/dev_pilot_records_v1_replay2_summary.json",
    "results/validation/g2/dev_pilot_records_v1_replay2_unknown_ledger.jsonl",
    "results/validation/g2/dev_pilot_records_v1_replay2_failure_ledger.jsonl",
]


def main() -> None:
    rows = []
    missing = []
    for relative in PATHS:
        path = ROOT / relative
        if not path.exists():
            missing.append(relative)
        else:
            rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {relative}")
    if missing:
        raise SystemExit("missing required result artifacts: " + ", ".join(missing))
    output = ROOT / "results/validation/g2/SHA256SUMS_RESULTS.txt"
    output.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print("\n".join(rows))


if __name__ == "__main__":
    main()
