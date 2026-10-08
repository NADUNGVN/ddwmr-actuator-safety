"""Read-only byte/hash audit for a frozen project source-closure manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit(root: Path, manifest_path: Path) -> dict[str, Any]:
    project = root.resolve(strict=True)
    manifest = manifest_path.resolve(strict=True)
    try:
        manifest.relative_to(project)
    except ValueError as exc:
        raise ValueError("manifest path escapes project root") from exc
    raw = manifest.read_bytes()
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("manifest is not valid UTF-8 JSON") from exc
    dependencies = payload.get("dependencies") if isinstance(payload, dict) else None
    if not isinstance(dependencies, list):
        raise ValueError("manifest has no dependencies array")

    counts: Counter[str] = Counter()
    issues: list[dict[str, Any]] = []
    for index, row in enumerate(dependencies):
        if not isinstance(row, dict):
            issues.append({"index": index, "reason": "DEPENDENCY_ROW_NOT_OBJECT"})
            continue
        relative = row.get("path")
        expected_size = row.get("size_bytes")
        expected_hash = row.get("sha256")
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
            issues.append({"index": index, "path": relative, "reason": "INVALID_RELATIVE_PATH"})
            continue
        if not isinstance(expected_size, int) or isinstance(expected_size, bool) or expected_size < 0:
            issues.append({"index": index, "path": relative, "reason": "INVALID_SIZE_BINDING"})
            continue
        if not isinstance(expected_hash, str) or len(expected_hash) != 64:
            issues.append({"index": index, "path": relative, "reason": "INVALID_SHA256_BINDING"})
            continue
        counts[relative] += 1
        candidate = (project / Path(relative)).resolve()
        try:
            candidate.relative_to(project)
        except ValueError:
            issues.append({"index": index, "path": relative, "reason": "PATH_ESCAPES_PROJECT"})
            continue
        if not candidate.is_file():
            issues.append({"index": index, "path": relative, "reason": "MISSING_FILE"})
            continue
        actual_size = candidate.stat().st_size
        actual_hash = _sha256(candidate)
        if actual_size != expected_size or actual_hash.lower() != expected_hash.lower():
            issues.append({
                "index": index,
                "path": relative,
                "reason": "SIZE_OR_HASH_MISMATCH",
                "expected_size_bytes": expected_size,
                "actual_size_bytes": actual_size,
                "expected_sha256": expected_hash,
                "actual_sha256": actual_hash,
            })
    duplicates = sorted(path for path, count in counts.items() if count > 1)
    for relative in duplicates:
        issues.append({"path": relative, "reason": "DUPLICATE_DEPENDENCY_PATH", "count": counts[relative]})
    return {
        "schema": "ddwmr-g4-w2-source-closure-audit-v1",
        "manifest_path": manifest.relative_to(project).as_posix(),
        "manifest_sha256": hashlib.sha256(raw).hexdigest(),
        "candidate_status": payload.get("candidate_status"),
        "declared_dependency_count": len(dependencies),
        "unique_dependency_path_count": len(counts),
        "verified_count": max(0, len(dependencies) - sum(1 for item in issues if item.get("reason") != "DUPLICATE_DEPENDENCY_PATH")),
        "issue_count": len(issues),
        "issues": issues,
        "result": "PASS" if not issues else "MISMATCHES_FOUND",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="project root")
    parser.add_argument("--manifest", type=Path, required=True, help="relative or absolute manifest inside root")
    args = parser.parse_args()
    try:
        result = audit(args.root, args.root / args.manifest if not args.manifest.is_absolute() else args.manifest)
    except (OSError, ValueError) as exc:
        print(json.dumps({"result": "AUDIT_ERROR", "detail": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["result"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
