#!/usr/bin/env python3
"""Check semantic JSON hashes across LF/CRLF without changing Git settings."""

from __future__ import annotations

import hashlib
import argparse
import json
import subprocess
from pathlib import Path

from validation.g2.evaluator import ROOT
from validation.g2.hashing import (
    HASH_PROTOCOL_ID, semantic_json_file_sha256, semantic_jsonl_sha256_bytes,
    verify_line_ending_invariance,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true", help="run checks without writing frozen evidence")
    args = parser.parse_args()
    bench_path = ROOT / "validation/configs/benchmark_v1.json"
    pilot_path = ROOT / "validation/configs/dev_pilot_v1.json"
    manifest_path = ROOT / "results/validation/g2/development_manifest_v1.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    line_ending = verify_line_ending_invariance({"fraction": {"num": "1", "den": "20"}, "label": "r2"})
    cases = []
    for path, legacy_expected in (
        (bench_path, manifest["benchmark_config_sha256"]),
        (pilot_path, manifest["pilot_config_sha256"]),
    ):
        blob = subprocess.run(
            ["git", "show", f"HEAD:{path.relative_to(ROOT).as_posix()}"],
            cwd=ROOT, check=True, capture_output=True,
        ).stdout
        working_raw = path.read_bytes()
        semantic = semantic_json_file_sha256(path)
        cases.append({
            "path": path.relative_to(ROOT).as_posix(),
            "legacy_manifest_raw_sha256_matches_working_copy": hashlib.sha256(working_raw).hexdigest() == legacy_expected,
            "legacy_git_blob_raw_sha256_differs": hashlib.sha256(blob).hexdigest() != legacy_expected,
            "semantic_sha256": semantic,
            "lf_crlf_semantic_hashes_match": line_ending["json_semantic_hashes_match"],
        })
    jsonl_lf = b'{"x":1}\n{"y":2}\n'
    jsonl_crlf = b'{"x":1}\r\n{"y":2}\r\n'
    jsonl_check = semantic_jsonl_sha256_bytes(jsonl_lf) == semantic_jsonl_sha256_bytes(jsonl_crlf)
    checks = {
        "protocol_id": HASH_PROTOCOL_ID,
        "synthetic_json_lf_crlf_match": line_ending["json_semantic_hashes_match"],
        "synthetic_jsonl_lf_crlf_match": line_ending["jsonl_semantic_hashes_match"] and jsonl_check,
        "raw_json_hashes_differ_on_line_endings": line_ending["raw_json_lf_crlf_hashes_differ"],
        "legacy_files_and_git_blobs_demonstrate_prior_mismatch": all(
            row["legacy_manifest_raw_sha256_matches_working_copy"] and row["legacy_git_blob_raw_sha256_differs"]
            for row in cases
        ),
    }
    output = {
        "schema": "ddwmr-g2-hash-protocol-verification-r2-v1",
        "source_revision": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip(),
        "all_pass": all(checks[key] for key in (
            "synthetic_json_lf_crlf_match", "synthetic_jsonl_lf_crlf_match",
            "raw_json_hashes_differ_on_line_endings", "legacy_files_and_git_blobs_demonstrate_prior_mismatch",
        )),
        "checks": checks,
        "legacy_checkout_evidence": cases,
        "scope": "semantic hash protocol check; v1 files and ledgers remain untouched",
    }
    output_path = ROOT / "results/validation/g2/r2/hash_protocol_check_r2_v1.json"
    if not args.check_only:
        if output_path.exists():
            raise SystemExit(f"refusing to overwrite hash protocol evidence: {output_path}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(output, sort_keys=True))
    if not output["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
