"""Versioned line-ending-independent semantic hashes for JSON evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


HASH_PROTOCOL_ID = "ddwmr-semantic-json-sha256-v2"


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False,
    ).encode("utf-8")


def semantic_json_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def semantic_json_file_sha256(path: Path) -> str:
    return semantic_json_sha256(json.loads(path.read_text(encoding="utf-8")))


def parse_jsonl_records(payload: bytes) -> list[Any]:
    """Parse physical LF/CRLF-delimited JSONL records without splitting Unicode content."""
    try:
        decoded = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("JSONL artifact must be UTF-8") from exc
    lines = (line[:-1] if line.endswith("\r") else line for line in decoded.split("\n"))
    return [json.loads(line) for line in lines if line.strip()]


def semantic_jsonl_sha256_bytes(payload: bytes) -> str:
    """Hash parsed JSONL records in order, ignoring CRLF/LF and final newline."""
    records = parse_jsonl_records(payload)
    normalized = b"".join(canonical_json_bytes(record) + b"\n" for record in records)
    return hashlib.sha256(normalized).hexdigest()


def semantic_jsonl_file_sha256(path: Path) -> str:
    return semantic_jsonl_sha256_bytes(path.read_bytes())


def verify_line_ending_invariance(value: Any) -> dict[str, Any]:
    canonical = canonical_json_bytes(value)
    lf_json = canonical + b"\n"
    crlf_json = canonical.replace(b"\n", b"\r\n") + b"\r\n"
    json_lf = semantic_json_sha256(json.loads(lf_json.decode("utf-8")))
    json_crlf = semantic_json_sha256(json.loads(crlf_json.decode("utf-8")))
    jsonl_rows = [{"record": value}, {"record_count": 2}, {"unicode_separator": "left\u2028right"}]
    lf_jsonl = b"".join(canonical_json_bytes(row) + b"\n" for row in jsonl_rows)
    crlf_jsonl = lf_jsonl.replace(b"\n", b"\r\n")
    return {
        "protocol_id": HASH_PROTOCOL_ID,
        "json_lf_semantic_sha256": json_lf,
        "json_crlf_semantic_sha256": json_crlf,
        "json_semantic_hashes_match": json_lf == json_crlf,
        "jsonl_lf_semantic_sha256": semantic_jsonl_sha256_bytes(lf_jsonl),
        "jsonl_crlf_semantic_sha256": semantic_jsonl_sha256_bytes(crlf_jsonl),
        "jsonl_semantic_hashes_match": semantic_jsonl_sha256_bytes(lf_jsonl) == semantic_jsonl_sha256_bytes(crlf_jsonl),
        "raw_json_lf_crlf_hashes_differ": hashlib.sha256(lf_json).digest() != hashlib.sha256(crlf_json).digest(),
    }
