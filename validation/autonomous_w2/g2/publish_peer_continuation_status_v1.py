"""Atomically publish G2 W2 STATUS sequence 17 for v6 peer-audit support."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STATUS = ROOT / "coordination/autonomous_w2/g2/STATUS.json"
SNAPSHOT = ROOT / "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_17.json"
EXPECTED_STATUS_SHA = "43c1e9235b5fb470e930a8e1195894adacb9a6341c0fc33b5b0a3dd38441a1a7"
RELEASE = ROOT / "coordination/autonomous_w2/g2/releases/RELEASE_v6.json"
STAGE = ROOT / "results/validation/autonomous_w2/g2/development_centered_v6/stage_receipt.json"
INVENTORY = ROOT / "results/validation/autonomous_w2/g2/development_centered_v6/evidence_inventory_v1.json"
PEER_STATUS = ROOT / "coordination/autonomous_w2/g4/STATUS.json"
PEER_AUDIT = ROOT / "coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write(path: Path, payload: bytes) -> None:
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise


def main() -> dict:
    if SNAPSHOT.exists():
        raise FileExistsError("STATUS_SEQUENCE_17_ALREADY_EXISTS")
    if sha(STATUS) != EXPECTED_STATUS_SHA:
        raise ValueError("EXPECTED_G2_STATUS_SEQUENCE_16_BYTES")
    current = load(STATUS)
    if current.get("sequence") != 16 or current.get("release", {}).get("sha256") != "789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55":
        raise ValueError("EXPECTED_G2_STATUS_SEQUENCE_16_V6")
    if sha(RELEASE) != "789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55":
        raise ValueError("V6_RELEASE_HASH_MISMATCH")
    stage = load(STAGE)
    if sha(STAGE) != "9b906c008af8ff51f92bb55d4f1fe072f9a4ebdc48f4caf64c29feec58f0aa36":
        raise ValueError("V6_STAGE_HASH_MISMATCH")
    if stage.get("cumulative_native_attempts") != 24 or stage.get("attempts_counted") != 3:
        raise ValueError("V6_ATTEMPT_ACCOUNTING_MISMATCH")
    peer_status = load(PEER_STATUS)
    peer_audit = load(PEER_AUDIT)
    if peer_status.get("sequence") != 3 or peer_audit.get("decision") != "NOT_ISSUED_NO_IMMUTABLE_G2_RELEASE":
        raise ValueError("UNEXPECTED_G4_PEER_STATE")
    if peer_audit.get("peer_release_manifest_sha256") is not None:
        raise ValueError("G4_ALREADY_BINDS_A_RELEASE; DO_NOT_PUBLISH_STALE_STATE")

    new = dict(current)
    artifacts = dict(current.get("artifacts", {}))
    owned = (
        "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_16.json",
        "coordination/autonomous_w2/g2/G4_PEER_RESPONSE_TO_V6_AUDIT_v1.md",
        "docs/reviews/autonomous_w2/g2/LUNA_TO_CODEX_G2_AUTONOMOUS_W2_FULL_HANDOFF_v2.md",
        "results/validation/autonomous_w2/g2/peer_replay_v6_v1.json",
        "validation/autonomous_w2/g2/replay_saved_centered_v6_peer_v1.py",
        "validation/autonomous_w2/g2/publish_peer_continuation_status_v1.py",
    )
    for rel in owned:
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        artifacts[rel] = sha(path)

    now = datetime.now(timezone.utc).isoformat()
    new.update(
        {
            "sequence": 17,
            "utc": now,
            "phase": "AWAITING_PEER_INPUT",
            "artifacts": artifacts,
            "previous_status": {
                "path": "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_16.json",
                "sha256": sha(ROOT / "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_16.json"),
            },
            "peer_status_observed": {
                "status_path": "coordination/autonomous_w2/g4/STATUS.json",
                "status_sha256": sha(PEER_STATUS),
                "sequence": peer_status["sequence"],
                "phase": peer_status.get("phase"),
                "audit_path": "coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v1.json",
                "audit_sha256": sha(PEER_AUDIT),
                "decision": peer_audit["decision"],
                "peer_release_manifest_sha256": peer_audit.get("peer_release_manifest_sha256"),
                "release_consumed": peer_audit.get("release_consumed"),
                "interpretation": "Historical no-release observation predates G2 v6 and is not a mathematical rejection.",
                "observed_utc": now,
            },
            "peer_release_consumed": None,
            "peer_response": {
                "path": "coordination/autonomous_w2/g2/G4_PEER_RESPONSE_TO_V6_AUDIT_v1.md",
                "sha256": sha(ROOT / "coordination/autonomous_w2/g2/G4_PEER_RESPONSE_TO_V6_AUDIT_v1.md"),
                "release_sha256": "789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55",
            },
            "saved_record_replay": {
                "path": "results/validation/autonomous_w2/g2/peer_replay_v6_v1.json",
                "sha256": sha(ROOT / "results/validation/autonomous_w2/g2/peer_replay_v6_v1.json"),
                "replayed_rows": 3,
                "proof_fields_per_row": 46,
                "center_slabs_per_row": 256,
                "evidence_inventory_entries_verified": 139,
                "native_rows_added": 0,
            },
            "blocker": "No G4 decision bound to G2 v6 is available; observed G4 sequence 3 predates v6 and is historical, not a rejection.",
            "next_action": "Consume a new G4 decision bound to v6 SHA-256 789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55. G2 native allowance is exhausted; preserve zero held-out rows and legacy 800/800 NOT_RUN.",
            "scientific_disposition": "Saved v6 evidence replays: all three reduced safety predicates certify; only the alternative meets the frozen synthetic progress requirement. Proof soundness, matched advantage, novelty, external task provenance, physical correspondence and final gate status remain unverified.",
            "native_attempts": {
                **current["native_attempts"],
                "count_completed": 24,
                "remaining_attempts": 0,
                "held_out_rows": 0,
                "legacy_800_row_study": "800/800 NOT_RUN",
                "g4_confirmation_rows_run_by_g2": 0,
            },
        }
    )

    report_rel = "docs/reviews/autonomous_w2/g2/LUNA_TO_CODEX_G2_AUTONOMOUS_W2_FULL_HANDOFF_v2.md"
    response_rel = "coordination/autonomous_w2/g2/G4_PEER_RESPONSE_TO_V6_AUDIT_v1.md"
    replay_rel = "results/validation/autonomous_w2/g2/peer_replay_v6_v1.json"
    new["handoff"] = {"path": report_rel, "sha256": sha(ROOT / report_rel)}
    new["phase"] = "AWAITING_PEER_INPUT"
    snapshot_bytes = (json.dumps(new, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    atomic_write(SNAPSHOT, snapshot_bytes)
    atomic_write(STATUS, snapshot_bytes)
    return {
        "sequence": 17,
        "phase": new["phase"],
        "status_path": STATUS.relative_to(ROOT).as_posix(),
        "status_sha256": sha(STATUS),
        "snapshot_path": SNAPSHOT.relative_to(ROOT).as_posix(),
        "snapshot_sha256": sha(SNAPSHOT),
        "handoff_path": report_rel,
        "handoff_sha256": new["handoff"]["sha256"],
        "peer_response_path": response_rel,
        "peer_response_sha256": sha(ROOT / response_rel),
        "replay_path": replay_rel,
        "replay_sha256": sha(ROOT / replay_rel),
    }


if __name__ == "__main__":
    print(json.dumps(main(), sort_keys=True, indent=2))
