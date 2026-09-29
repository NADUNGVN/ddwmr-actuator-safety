#!/usr/bin/env python3
"""Write the R2 semantic-JSON artifact ledger; leave all v1 raw ledgers unchanged."""

from __future__ import annotations

import json
from pathlib import Path

from validation.g2.evaluator import ROOT
from validation.g2.hashing import HASH_PROTOCOL_ID, semantic_json_file_sha256, semantic_jsonl_file_sha256


JSON_PATHS = [
    "validation/configs/benchmark_v1.json",
    "validation/configs/dev_pilot_r2_v1.json",
    "validation/configs/g2_proof_pipeline_fixture_r2_v1.json",
    "results/validation/g2/r2/development_manifest_r2_v1.json",
    "results/validation/g2/r2/SHA256SUMS_PRE_EVAL_R2.json",
    "results/validation/g2/r2/radius_series_regression_r2_v1.json",
    "results/validation/g2/r2/hash_protocol_check_r2_v1.json",
    "results/validation/g2/r2/proof_fixture_metadata_r2_v1.json",
    "results/validation/g2/r2/proof_fixture_check_r2_v1.json",
    "results/validation/g2/r2/dev_pilot_run_metadata_r2_v1.json",
    "results/validation/g2/r2/dev_pilot_record_check_r2_v1.json",
    "results/validation/g2/r2/dev_pilot_summary_r2_v1.json",
    "results/validation/g2/r2/pilot_positive_tamper_check_r2_v1.json",
]
JSONL_PATHS = [
    "results/validation/g2/r2/proof_fixture_records_r2_v1.jsonl",
    "results/validation/g2/r2/dev_pilot_records_r2_v1.jsonl",
    "results/validation/g2/r2/dev_pilot_unknown_ledger_r2_v1.jsonl",
    "results/validation/g2/r2/dev_pilot_failure_ledger_r2_v1.jsonl",
]


def main() -> None:
    missing = [name for name in JSON_PATHS + JSONL_PATHS if not (ROOT / name).is_file()]
    if missing:
        raise SystemExit("missing R2 artifacts: " + ", ".join(missing))
    rows = []
    for name in JSON_PATHS:
        rows.append({"path": name, "format": "semantic-json", "sha256": semantic_json_file_sha256(ROOT / name)})
    for name in JSONL_PATHS:
        rows.append({"path": name, "format": "semantic-jsonl", "sha256": semantic_jsonl_file_sha256(ROOT / name)})
    ledger = {
        "schema": "ddwmr-g2-results-semantic-hashes-r2-v1",
        "hash_protocol_id": HASH_PROTOCOL_ID,
        "semantics": "JSON is parsed then canonicalized as sorted-key compact UTF-8 JSON; JSONL records are canonicalized in order with LF delimiters.",
        "artifacts": rows,
    }
    output = ROOT / "results/validation/g2/r2/SHA256SUMS_RESULTS_R2.json"
    if output.exists():
        raise SystemExit(f"refusing to overwrite R2 result hash ledger: {output}")
    output.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"hash_protocol_id": HASH_PROTOCOL_ID, "artifact_count": len(rows), "ledger": str(output)}, sort_keys=True))


if __name__ == "__main__":
    main()
