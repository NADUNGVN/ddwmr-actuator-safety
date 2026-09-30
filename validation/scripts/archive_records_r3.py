"""Losslessly gzip a completed R3 JSONL result after replay verification."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import platform
import tempfile
import zlib
from pathlib import Path

from validation.g2.hashing import canonical_json_bytes
from validation.g2.provenance import current_revision


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = Path("results/validation/g2/r3/conditional_full_grid_records_r3_v1.jsonl")
DEFAULT_ARCHIVE = Path("results/validation/g2/r3/conditional_full_grid_records_r3_v1.jsonl.gz")
DEFAULT_METADATA = Path("results/validation/g2/r3/conditional_full_grid_run_metadata_r3_v1.json")
DEFAULT_MANIFEST = Path("results/validation/g2/r3/conditional_full_grid_archive_manifest_r3_v1.json")


def semantic_jsonl_digest_and_count(path: Path, *, copy_to=None) -> tuple[str, int, str, int]:
    semantic_digest = hashlib.sha256()
    raw_digest = hashlib.sha256()
    record_count = 0
    byte_count = 0
    with path.open("rb") as stream:
        for raw_line in stream:
            raw_digest.update(raw_line)
            byte_count += len(raw_line)
            if copy_to is not None:
                copy_to.write(raw_line)
            line = raw_line[:-1] if raw_line.endswith(b"\n") else raw_line
            if line.endswith(b"\r"):
                line = line[:-1]
            if not line.strip():
                continue
            record = json.loads(line.decode("utf-8"))
            semantic_digest.update(canonical_json_bytes(record) + b"\n")
            record_count += 1
    return semantic_digest.hexdigest(), record_count, raw_digest.hexdigest(), byte_count


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--remove-source-after-verification", action="store_true")
    args = parser.parse_args()

    source = ROOT / args.source
    archive = ROOT / args.archive
    metadata_path = ROOT / args.metadata
    manifest_path = ROOT / args.manifest
    for path in (source, metadata_path):
        if not path.is_file():
            raise SystemExit(f"required R3 input missing: {path}")
    if archive.exists() or manifest_path.exists():
        raise SystemExit("refusing to overwrite R3 archive or archive manifest")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("phase_id") != "R3_CONDITIONAL_REMAINING_1728":
        raise SystemExit("source metadata is not the frozen R3 conditional full-grid phase")
    if metadata.get("output_path") != args.source.as_posix():
        raise SystemExit("metadata output path does not match the source JSONL")

    archive.parent.mkdir(parents=True, exist_ok=True)
    semantic_sha256, record_count, source_raw_sha256, source_bytes = semantic_jsonl_digest_and_count(source)
    if record_count != metadata.get("selected_queries"):
        raise SystemExit(f"JSONL record count {record_count} does not match run metadata")
    if semantic_sha256 != metadata.get("records_semantic_sha256"):
        raise SystemExit("source semantic hash does not match producer run metadata")

    temporary_path = None
    archive_created = False
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=archive.parent, prefix=archive.name + ".", suffix=".tmp", delete=False
        ) as raw_output:
            temporary_path = Path(raw_output.name)
            with gzip.GzipFile(
                filename="", mode="wb", fileobj=raw_output, compresslevel=9, mtime=0
            ) as compressed:
                copied_semantic, copied_count, copied_raw_sha256, copied_bytes = semantic_jsonl_digest_and_count(
                    source, copy_to=compressed
                )
        if (copied_semantic, copied_count, copied_raw_sha256, copied_bytes) != (
            semantic_sha256, record_count, source_raw_sha256, source_bytes
        ):
            raise SystemExit("source JSONL changed while the archive was being written")

        archive_bytes = temporary_path.stat().st_size
        archive_sha256 = file_sha256(temporary_path)
        expanded_digest = hashlib.sha256()
        expanded_bytes = 0
        with gzip.open(temporary_path, "rb") as expanded:
            for chunk in iter(lambda: expanded.read(1024 * 1024), b""):
                expanded_digest.update(chunk)
                expanded_bytes += len(chunk)
        if expanded_digest.hexdigest() != source_raw_sha256 or expanded_bytes != source_bytes:
            raise SystemExit("gzip round-trip bytes do not match the original JSONL")

        temporary_path.replace(archive)
        archive_created = True
        manifest = {
            "schema": "ddwmr-g2-r3-compressed-record-archive-v1",
            "phase_id": metadata["phase_id"],
            "logical_source_path": args.source.as_posix(),
            "archive_path": args.archive.as_posix(),
            "record_count": record_count,
            "source_semantic_sha256": semantic_sha256,
            "source_raw_bytes_sha256": source_raw_sha256,
            "source_bytes": source_bytes,
            "archive_raw_bytes_sha256": archive_sha256,
            "archive_bytes": archive_bytes,
            "compression": {
                "format": "gzip",
                "level": 9,
                "mtime_header": 0,
                "stored_filename": "",
                "python_version": platform.python_version(),
                "zlib_version": zlib.ZLIB_VERSION,
                "round_trip_raw_sha256_match": True,
            },
            "producer_records_semantic_sha256": metadata["records_semantic_sha256"],
            "archive_tool_revision": current_revision(),
            "archive_tool_path": "validation/scripts/archive_records_r3.py",
        }
        manifest_temporary = manifest_path.with_name(manifest_path.name + ".tmp")
        if manifest_temporary.exists():
            raise SystemExit(f"refusing to overwrite temporary manifest: {manifest_temporary}")
        manifest_temporary.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
        )
        manifest_temporary.replace(manifest_path)
        if args.remove_source_after_verification:
            source.unlink()
    except Exception:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
        if archive_created and archive.exists() and not manifest_path.exists():
            archive.unlink()
        raise

    print(json.dumps({
        "archive": str(archive),
        "archive_bytes": archive_bytes,
        "manifest": str(manifest_path),
        "record_count": record_count,
        "round_trip_raw_sha256_match": True,
        "source_removed": args.remove_source_after_verification,
        "source_semantic_sha256": semantic_sha256,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
