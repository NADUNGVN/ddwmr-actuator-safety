"""Atomically publish final W2 G2 sequence 16 after the frozen v6 stage."""
from __future__ import annotations
import hashlib,json,os,tempfile
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
STATUS=ROOT/"coordination/autonomous_w2/g2/STATUS.json"
SNAPSHOT=ROOT/"coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_16.json"
HANDOFF=ROOT/"docs/reviews/autonomous_w2/g2/LUNA_TO_CODEX_G2_AUTONOMOUS_W2_FULL_HANDOFF.md"
INVENTORY=ROOT/"results/validation/autonomous_w2/g2/development_centered_v6/evidence_inventory_v1.json"
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p:Path):return json.loads(p.read_text(encoding="utf-8"))
def atomic(path:Path,value)->None:
 raw=json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True).encode()+b"\n"; fd,tmp=tempfile.mkstemp(prefix=path.name+".",suffix=".tmp",dir=path.parent)
 try:
  with os.fdopen(fd,"wb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
  os.replace(tmp,path)
 except BaseException:
  try:os.unlink(tmp)
  except FileNotFoundError:pass
  raise
def main():
 current=load(STATUS)
 if current.get("sequence")!=15:raise ValueError("EXPECTED_STATUS_SEQUENCE_15")
 inv=load(INVENTORY); artifacts={item["path"]:item["sha256"] for item in inv["files"]}
 artifacts[INVENTORY.relative_to(ROOT).as_posix()]=sha(INVENTORY)
 artifacts[HANDOFF.relative_to(ROOT).as_posix()]=sha(HANDOFF)
 own=Path(__file__).resolve(); artifacts[own.relative_to(ROOT).as_posix()]=sha(own)
 stage_rel="results/validation/autonomous_w2/g2/development_centered_v6/stage_receipt.json"
 mutation_rel="results/validation/autonomous_w2/g2/development_centered_v6/mutation_audit_v2/mutation_audit_report.json"
 if load(ROOT/stage_rel).get("status_counts")!={"REPLAYED":3}:raise ValueError("V6_STAGE_NOT_THREE_REPLAYED")
 if load(ROOT/mutation_rel).get("all_required_mutations_rejected") is not True:raise ValueError("V6_MUTATION_AUDIT_NOT_PASS")
 peer_status_rel="coordination/autonomous_w2/g4/STATUS.json";peer_audit_rel="coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v1.json"
 peer_status=load(ROOT/peer_status_rel);peer_audit=load(ROOT/peer_audit_rel)
 new={**current,"sequence":16,"utc":datetime.now(timezone.utc).isoformat(),"phase":"AWAITING_PEER_INPUT",
  "objective":"Complete G2 W2 synthetic one-hold enclosure package, preserve all 24 bounded attempts, and obtain a release-bound independent G4 decision.",
  "artifacts":artifacts,"blocker":"G4 has not yet issued a decision bound to G2 release SHA-256 789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55; the prior G4 audit state refers to its earlier peer observation and is not a v6 rejection.",
  "native_attempts":{"G2_limit":24,"count_completed":24,"remaining_attempts":0,"held_out_rows":0,
    "v1_attempts":6,"v2_attempts":6,"v3_attempts":3,"v4_attempts":3,"v5_attempts":3,"v6_attempts":3,
    "legacy_800_row_study":"800/800 NOT_RUN","g4_confirmation_rows_run_by_g2":0},
  "release":{"path":"coordination/autonomous_w2/g2/releases/RELEASE_v6.json","sha256":"789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55","state":"FROZEN_FOR_G4_AUDIT_AND_BOUNDED_DEVELOPMENT"},
  "previous_release":{"path":"coordination/autonomous_w2/g2/releases/RELEASE_v5.json","sha256":"1fa1a1e14f311a49fdf6f92b79ecdb362a69004317ee5a512be3bfa0efe8776e"},
  "stage_result":{"path":stage_rel,"sha256":sha(ROOT/stage_rel),"attempts_counted":3,"status_counts":{"REPLAYED":3},
    "safety_certified_rows":3,"task_eligible_rows":1,"task_ineligible_by_upper_rows":2,"all_required_mutations_rejected":True,
    "mutation_audit_path":mutation_rel,"mutation_audit_sha256":sha(ROOT/mutation_rel)},
  "peer_status_observed":{"status_path":peer_status_rel,"status_sha256":sha(ROOT/peer_status_rel),"sequence":peer_status.get("sequence"),
    "phase":peer_status.get("phase"),"audit_path":peer_audit_rel,"audit_sha256":sha(ROOT/peer_audit_rel),
    "decision":peer_audit.get("decision"),"peer_release_manifest_sha256":peer_audit.get("peer_release_manifest_sha256"),
    "release_consumed":peer_audit.get("release_consumed"),"observed_utc":datetime.now(timezone.utc).isoformat()},
  "next_action":"Consume G4's direct release-bound decision for v6. If accepted, G4 owns frozen matched confirmation; if defective, correct/version the source and request a new cycle before any additional native G2 attempt.",
  "scientific_disposition":"One synthetic task group shows alternative-only certificate eligibility; final G2/G4 disposition remains pending independent audit.",
  "gate_statuses":{"overall":"HOLD","G1":"PASS_RESTRICTED_REDUCED_MODEL_SCOPE","G2":"UNVERIFIED","G3":"UNVERIFIED","G4":"UNVERIFIED","physical_platform_correspondence":"UNVERIFIED"},
  "working_tree_note":"Shared tree retained; all G2 writes remained in G2-owned W2 prefixes; G4 files were read-only; no branch switch, commit or push."}
 if SNAPSHOT.exists():raise FileExistsError("STATUS_SEQUENCE_16_ALREADY_EXISTS")
 SNAPSHOT.write_text(json.dumps(new,sort_keys=True,indent=2,ensure_ascii=True)+"\n",encoding="utf-8")
 atomic(STATUS,new)
 return {"status_path":STATUS.relative_to(ROOT).as_posix(),"snapshot_path":SNAPSHOT.relative_to(ROOT).as_posix(),
   "sequence":16,"phase":"AWAITING_PEER_INPUT","native_attempts":24,"remaining":0,"status_sha256":sha(STATUS),"snapshot_sha256":sha(SNAPSHOT),"artifact_count":len(artifacts)}
if __name__=="__main__":print(json.dumps(main(),sort_keys=True,indent=2))
