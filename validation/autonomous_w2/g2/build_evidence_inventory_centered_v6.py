"""Inventory/hash all v6 source, binding, run and mutation evidence files."""
from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/"results/validation/autonomous_w2/g2/development_centered_v6/evidence_inventory_v1.json"
ROOT_FILES=[
 "AGENTS.md","docs/DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2.md","docs/CODEX_TO_LUNA_G2_AUTONOMOUS_COMPLETION_W2.md",
 "research_context/MASTER_RESEARCH_CONTEXT_v2.md","research_context/DECISION_LOG.md","research_context/LITERATURE_MATRIX.md","research_context/REVIEW_GATE.md",
 "research/autonomous_w2/g2/task_protocol_v1.json","research/autonomous_w2/g2/HYPOTHESIS_CENTERED_RESIDUAL_TUBE_v1.md",
 "research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v6.md","research/autonomous_w2/g2/development_plan_centered_v6.json",
 "research/autonomous_w2/g2/bindings_centered_v6/attempt_01.json","research/autonomous_w2/g2/bindings_centered_v6/attempt_02.json","research/autonomous_w2/g2/bindings_centered_v6/attempt_03.json",
 "validation/autonomous_w2/g2/profile_centered_v6.json","validation/autonomous_w2/g2/producer_centered_v6.py","validation/autonomous_w2/g2/checker_centered_v6.py",
 "validation/autonomous_w2/g2/centered_v6_nonquery_fixtures.py","validation/autonomous_w2/g2/pre_run_validation_centered_v6.py",
 "validation/autonomous_w2/g2/freeze_development_centered_v6.py","validation/autonomous_w2/g2/run_stage_centered_v6.py",
 "validation/autonomous_w2/g2/publish_release_centered_v6.py","validation/autonomous_w2/g2/audit_mutations_centered_v6.py",
 "validation/autonomous_w2/g2/audit_mutations_centered_v6_v2.py","validation/autonomous_w2/g2/build_evidence_inventory_centered_v6.py",
 "validation/autonomous_w2/g2/producer_v4.py","validation/autonomous_w2/g2/rational_interval_v3.py","validation/autonomous_w2/g2/windows_job_supervisor.py",
 "results/validation/autonomous_w2/g2/centered_error_tube_preflight_v2.json","results/validation/autonomous_w2/g2/centered_v6_nonquery_fixtures_v1.json",
 "results/validation/autonomous_w2/g2/pre_run_validation_centered_v6.json","results/validation/autonomous_w2/g2/pre_run_validation_centered_v6_v2.json",
 "results/validation/autonomous_w2/g2/pre_run_validation_centered_v6_v3.json",
 "results/validation/autonomous_w2/g2/development_centered_v6/freeze_receipt_v6.json",
 "results/validation/autonomous_w2/g2/development_centered_v6/stage_receipt.json",
 "coordination/autonomous_w2/g2/releases/RELEASE_v5.json","coordination/autonomous_w2/g2/releases/RELEASE_v6.json",
 "coordination/autonomous_w2/g2/releases/RELEASE_v6.json.sha256","coordination/autonomous_w2/g2/AUDIT_REQUEST_TO_G4_v6.md",
 "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_14.json","coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_15.json",
 "coordination/autonomous_w2/g4/STATUS.json","coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v1.json",
]

def entry(rel:str)->dict[str,object]:
 p=ROOT/rel
 if not p.is_file(): raise FileNotFoundError(rel)
 b=p.read_bytes(); return {"path":rel,"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def main()->dict[str,object]:
 if OUT.exists(): raise FileExistsError("EVIDENCE_INVENTORY_EXISTS")
 files={rel for rel in ROOT_FILES}
 run_root=ROOT/"results/validation/autonomous_w2/g2/development_centered_v6"
 files.update(p.relative_to(ROOT).as_posix() for p in run_root.rglob("*") if p.is_file())
 entries=[entry(x) for x in sorted(files) if x!=OUT.relative_to(ROOT).as_posix()]
 report={"schema":"G2_W2_CENTERED_V6_EVIDENCE_INVENTORY_v1","session":"DDWMR | LUNA-G2-SCOPE",
  "created_utc":datetime.now(timezone.utc).isoformat(),"release_path":"coordination/autonomous_w2/g2/releases/RELEASE_v6.json",
  "release_sha256":hashlib.sha256((ROOT/"coordination/autonomous_w2/g2/releases/RELEASE_v6.json").read_bytes()).hexdigest(),
  "evidence_root":"results/validation/autonomous_w2/g2/development_centered_v6","file_count":len(entries),
  "files":entries,"excluded_self":True,"native_attempts_added":0,"held_out_rows":0,"legacy_800_row_study":"NOT_RUN"}
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(report,sort_keys=True,indent=2,ensure_ascii=True)+"\n",encoding="utf-8")
 return {"inventory_path":OUT.relative_to(ROOT).as_posix(),"sha256":hashlib.sha256(OUT.read_bytes()).hexdigest(),"file_count":len(entries)}
if __name__=="__main__": print(json.dumps(main(),sort_keys=True,indent=2))
