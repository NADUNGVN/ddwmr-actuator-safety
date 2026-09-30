"""Git-blob provenance helpers for the versioned R3 validation path."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path
from typing import Iterable

from .hashing import semantic_json_sha256


ROOT = Path(__file__).resolve().parents[2]


def git_blob_commitment(revision: str, relative_path: str) -> dict[str, str]:
    path = Path(relative_path).as_posix()
    object_id = subprocess.run(
        ["git", "rev-parse", f"{revision}:{path}"], cwd=ROOT,
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    blob = subprocess.run(
        ["git", "cat-file", "blob", object_id], cwd=ROOT,
        check=True, capture_output=True,
    ).stdout
    return {
        "source_revision": revision,
        "repository_relative_path": path,
        "git_blob_object_id": object_id,
        "sha256_git_blob_bytes": hashlib.sha256(blob).hexdigest(),
    }


def source_commitments(revision: str, paths: Iterable[str]) -> list[dict[str, str]]:
    return [git_blob_commitment(revision, path) for path in paths]


def specification_ledger(revision: str, paths: Iterable[str]) -> dict:
    body = {
        "schema": "ddwmr-g2-r3-specification-content-ledger-v1",
        "hash_protocol": "sha256 of immutable Git blob bytes; source revision and repository path are explicit",
        "sources": source_commitments(revision, paths),
    }
    return {**body, "specification_bundle_sha256": semantic_json_sha256(body)}


def verify_commitment(entry: dict) -> bool:
    try:
        return git_blob_commitment(
            entry["source_revision"], entry["repository_relative_path"],
        ) == entry
    except (KeyError, subprocess.CalledProcessError, OSError):
        return False


def worktree_status(paths: Iterable[str] | None = None) -> list[str]:
    command = ["git", "status", "--porcelain=v1"]
    if paths is not None:
        command.extend(["--", *[Path(path).as_posix() for path in paths]])
    raw = subprocess.run(command, cwd=ROOT, check=True, capture_output=True).stdout
    return [line.decode("utf-8", errors="replace") for line in raw.splitlines() if line]


def current_revision() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
