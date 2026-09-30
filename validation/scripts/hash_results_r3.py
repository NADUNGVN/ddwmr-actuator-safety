"""Write non-overwriting R3 pilot or final result hash ledgers."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path

from validation.g2.evaluator import ROOT
from validation.g2.hashing import HASH_PROTOCOL_ID, canonical_json_bytes, semantic_json_file_sha256
from validation.g2.provenance import current_revision


PILOT_FILES = [
    "validation/configs/benchmark_v1.json",
    "validation/configs/dev_pilot_r3_v1.json",
    "results/validation/g2/r3/full_grid_continuation_manifest_r3_v1.json",
    "results/validation/g2/r3/specification_content_ledger_r3_v1.json",
    "results/validation/g2/r3/development_manifest_r3_v1.json",
    "results/validation/g2/r3/SHA256SUMS_PRE_EVAL_R3.json",
    "results/validation/g2/r3/dev_pilot_records_r3_v1.jsonl",
    "results/validation/g2/r3/dev_pilot_run_metadata_r3_v1.json",
    "results/validation/g2/r3/dev_pilot_record_check_r3_v1.json",
    "results/validation/g2/r3/dev_pilot_summary_r3_v1.json",
    "results/validation/g2/r3/r2_to_r3_query_transitions_r3_v1.jsonl",
    "results/validation/g2/r3/action_group_summary_r3_v1.json",
    "results/validation/g2/r3/r2_compatibility_record_check_r3_v1.json",
]
FULL_FILES = PILOT_FILES + [
    "results/validation/g2/r3/SHA256SUMS_PILOT_R3.json",
    "results/validation/g2/r3/conditional_full_grid_records_r3_v1.jsonl.gz",
    "results/validation/g2/r3/conditional_full_grid_archive_manifest_r3_v1.json",
    "results/validation/g2/r3/conditional_full_grid_run_metadata_r3_v1.json",
    "results/validation/g2/r3/full_grid_record_check_r3_v1.json",
    "results/validation/g2/r3/full_grid_summary_r3_v1.json",
    "results/validation/g2/r3/r2_to_r3_full_grid_transitions_r3_v1.jsonl",
    "results/validation/g2/r3/full_grid_action_group_summary_r3_v1.json",
]


def semantic_jsonl_sha256_stream(stream) -> str:
    """Hash canonical JSONL one record at a time, including gzip streams."""
    digest = hashlib.sha256()
    for raw_line in stream:
        line = raw_line[:-1] if raw_line.endswith(b"\n") else raw_line
        if line.endswith(b"\r"):
            line = line[:-1]
        if not line.strip():
            continue
        record = json.loads(line.decode("utf-8"))
        digest.update(canonical_json_bytes(record) + b"\n")
    return digest.hexdigest()


def raw_file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("pilot", "full-grid"), default="pilot")
    args = parser.parse_args()
    files = PILOT_FILES if args.phase == "pilot" else FULL_FILES
    ledger_path = ROOT / ("results/validation/g2/r3/SHA256SUMS_PILOT_R3.json" if args.phase == "pilot" else "results/validation/g2/r3/SHA256SUMS_RESULTS_R3.json")
    if ledger_path.exists():
        raise SystemExit(f"refusing to overwrite R3 hash ledger: {ledger_path}")
    hashes = {}
    for relative in files:
        path = ROOT / relative
        if not path.is_file():
            raise SystemExit(f"required R3 artifact missing: {relative}")
        if path.name.endswith(".jsonl.gz"):
            with gzip.open(path, "rb") as stream:
                semantic = semantic_jsonl_sha256_stream(stream)
        elif path.suffix == ".jsonl":
            with path.open("rb") as stream:
                semantic = semantic_jsonl_sha256_stream(stream)
        else:
            semantic = semantic_json_file_sha256(path)
        hashes[relative] = {
            "semantic_sha256": semantic,
            "raw_bytes_sha256": raw_file_sha256(path),
            "bytes": path.stat().st_size,
        }
    ledger = {
        "schema": "ddwmr-g2-r3-pilot-result-hashes-v1" if args.phase == "pilot" else "ddwmr-g2-r3-final-result-hashes-v1",
        "phase": args.phase,
        "hash_protocol_id": HASH_PROTOCOL_ID,
        "source_revision_when_ledger_created": current_revision(),
        "hash_semantics": "JSON/JSONL semantic SHA-256 uses sorted-key compact UTF-8 JSON with LF record delimiters; raw_bytes_sha256 records exact stored bytes.",
        "files": hashes,
    }
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"ledger": str(ledger_path), "file_count": len(hashes), "phase": args.phase}, sort_keys=True))


if __name__ == "__main__":
    main()
