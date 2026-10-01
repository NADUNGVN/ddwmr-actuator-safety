"""Re-hash every v9 frozen source member without modifying the snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    snapshot = args.snapshot.resolve()
    manifest_path = snapshot / "snapshot_manifest.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
    sidecar_hash = (snapshot / "snapshot_manifest.sha256").read_text(encoding="ascii").split()[0]
    manifest = json.loads(manifest_bytes)
    mismatches = []
    checked = 0
    for item in manifest["members"]:
        path = snapshot / item["snapshot_relative_path"]
        if not path.is_file():
            mismatches.append({"path": item["snapshot_relative_path"], "reason": "missing"})
            continue
        checked += 1
        actual_size = path.stat().st_size
        actual_hash = sha256(path)
        if actual_size != item["bytes"] or actual_hash != item["sha256"]:
            mismatches.append({
                "path": item["snapshot_relative_path"],
                "expected_bytes": item["bytes"], "actual_bytes": actual_size,
                "expected_sha256": item["sha256"], "actual_sha256": actual_hash,
            })
    report = {
        "schema": "ddwmr-g4-auer-source-integrity-v9-v1",
        "checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "snapshot_path": str(snapshot),
        "manifest_sha256": manifest_hash,
        "sidecar_sha256": sidecar_hash,
        "manifest_sidecar_match": manifest_hash == sidecar_hash,
        "expected_member_count": len(manifest["members"]),
        "checked_member_count": checked,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "status": "PASS" if manifest_hash == sidecar_hash and len(mismatches) == 0 and checked == len(manifest["members"]) else "FAIL",
    }
    destination = args.output.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": report["status"], "members": checked, "manifest_sha256": manifest_hash, "output": str(destination)}, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
