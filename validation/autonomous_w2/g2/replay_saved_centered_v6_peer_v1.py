"""Recompute the three frozen G2 v6 records for peer-review support only.

This script never launches a producer, worker, native query, or stage. It reads
the immutable v6 release inputs and refuses to overwrite its output artifact.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from .checker_centered_v6 import audit

ROOT = Path(__file__).resolve().parents[3]
RELEASE = ROOT / "coordination/autonomous_w2/g2/releases/RELEASE_v6.json"
INVENTORY = ROOT / "results/validation/autonomous_w2/g2/development_centered_v6/evidence_inventory_v1.json"
STAGE = ROOT / "results/validation/autonomous_w2/g2/development_centered_v6/stage_receipt.json"
OUTPUT = ROOT / "results/validation/autonomous_w2/g2/peer_replay_v6_v1.json"
EXPECTED_RELEASE_SHA = "789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55"
ROWS = (
    (
        "W2_G2_DEV_001_ZERO",
        "research/autonomous_w2/g2/bindings_centered_v6/attempt_01.json",
        "results/validation/autonomous_w2/g2/development_centered_v6/attempt_01_W2_G2_DEV_001_ZERO/row.json",
    ),
    (
        "W2_G2_DEV_001_NOMINAL",
        "research/autonomous_w2/g2/bindings_centered_v6/attempt_02.json",
        "results/validation/autonomous_w2/g2/development_centered_v6/attempt_02_W2_G2_DEV_001_NOMINAL/row.json",
    ),
    (
        "W2_G2_DEV_001_ALTERNATIVE",
        "research/autonomous_w2/g2/bindings_centered_v6/attempt_03.json",
        "results/validation/autonomous_w2/g2/development_centered_v6/attempt_03_W2_G2_DEV_001_ALTERNATIVE/row.json",
    ),
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> dict:
    if OUTPUT.exists():
        raise FileExistsError(f"REFUSE_OVERWRITE:{OUTPUT.relative_to(ROOT).as_posix()}")
    if sha(RELEASE) != EXPECTED_RELEASE_SHA:
        raise ValueError("V6_RELEASE_HASH_MISMATCH")

    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    verified = 0
    for item in inventory["files"]:
        path = ROOT / item["path"]
        if not path.is_file() or path.stat().st_size != item["bytes"] or sha(path) != item["sha256"]:
            raise ValueError(f"EVIDENCE_INVENTORY_MISMATCH:{item['path']}")
        verified += 1

    stage = json.loads(STAGE.read_text(encoding="utf-8"))
    if sha(STAGE) != "9b906c008af8ff51f92bb55d4f1fe072f9a4ebdc48f4caf64c29feec58f0aa36":
        raise ValueError("V6_STAGE_RECEIPT_HASH_MISMATCH")
    if stage.get("attempts_counted") != 3 or stage.get("cumulative_native_attempts") != 24:
        raise ValueError("V6_STAGE_ACCOUNTING_MISMATCH")

    checker_path = ROOT / "validation/autonomous_w2/g2/checker_centered_v6.py"
    results = []
    for action_id, binding_rel, record_rel in ROWS:
        binding = ROOT / binding_rel
        record = ROOT / record_rel
        binding_doc = json.loads(binding.read_text(encoding="utf-8"))
        stored_record = json.loads(record.read_text(encoding="utf-8"))
        if stored_record.get("action_id") != action_id:
            raise ValueError(f"ACTION_ID_MISMATCH:{action_id}")
        attempt = next((a for a in stage["attempts"] if a["action_id"] == action_id), None)
        if attempt is None or attempt["binding_sha256"] != sha(binding) or attempt["row_sha256"] != sha(record):
            raise ValueError(f"STAGE_BINDING_MISMATCH:{action_id}")
        result = audit(binding, record)
        if result.get("replayed") is not True:
            raise ValueError(f"REPLAY_FAILED:{action_id}")
        results.append(
            {
                "action_id": action_id,
                "binding_path": binding_rel,
                "binding_sha256": sha(binding),
                "record_path": record_rel,
                "record_sha256": sha(record),
                "checker_path": checker_path.relative_to(ROOT).as_posix(),
                "checker_sha256": sha(checker_path),
                **result,
            }
        )

    artifact = {
        "schema": "G2_W2_V6_SAVED_RECORD_PEER_REPLAY_v1",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "purpose": "Read-only full checker replay of saved development records for the G4 v6 audit.",
        "native_queries_or_producer_rows_added": 0,
        "legacy_800_row_study": "800/800 NOT_RUN",
        "release_path": RELEASE.relative_to(ROOT).as_posix(),
        "release_sha256": sha(RELEASE),
        "stage_receipt_path": STAGE.relative_to(ROOT).as_posix(),
        "stage_receipt_sha256": sha(STAGE),
        "evidence_inventory_path": INVENTORY.relative_to(ROOT).as_posix(),
        "evidence_inventory_sha256": sha(INVENTORY),
        "evidence_inventory_entries_verified": verified,
        "replays": results,
        "shared_trust_limits": [
            "Python fractions.Fraction",
            "validation.autonomous_w2.g2.rational_interval_v3.I/Budget and outward 96-bit arithmetic",
            "replay reconstructs all stored fields independently of the producer module but shares the interval arithmetic backend",
        ],
        "completed_utc": datetime.now(timezone.utc).isoformat(),
    }
    raw = (json.dumps(artifact, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    with OUTPUT.open("xb") as stream:
        stream.write(raw)
        stream.flush()
    return {
        "output_path": OUTPUT.relative_to(ROOT).as_posix(),
        "output_sha256": sha(OUTPUT),
        "replays": len(results),
        "verified_inventory_entries": verified,
        "native_rows_added": 0,
    }


if __name__ == "__main__":
    print(json.dumps(main(), sort_keys=True, indent=2))
