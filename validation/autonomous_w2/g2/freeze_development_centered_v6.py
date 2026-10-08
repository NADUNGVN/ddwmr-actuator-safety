"""Freeze v6 code, task, resource profile, three ordered actions and source pins."""
from __future__ import annotations
import hashlib, json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[3]
PLAN_REL="research/autonomous_w2/g2/development_plan_centered_v6.json"
PROTOCOL_REL="research/autonomous_w2/g2/task_protocol_v1.json"
PROFILE_REL="validation/autonomous_w2/g2/profile_centered_v6.json"
RUNNER_REL="validation/autonomous_w2/g2/run_stage_centered_v6.py"
BINDING_DIR_REL="research/autonomous_w2/g2/bindings_centered_v6"
RESULT_REL="results/validation/autonomous_w2/g2/development_centered_v6"
FREEZE_REL=f"{RESULT_REL}/freeze_receipt_v6.json"
ACTION_IDS=["W2_G2_DEV_001_ZERO","W2_G2_DEV_001_NOMINAL","W2_G2_DEV_001_ALTERNATIVE"]
SOURCE_PATHS=[
 "AGENTS.md","docs/DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2.md","docs/CODEX_TO_LUNA_G2_AUTONOMOUS_COMPLETION_W2.md",
 "research_context/MASTER_RESEARCH_CONTEXT_v2.md","research_context/DECISION_LOG.md","research_context/LITERATURE_MATRIX.md","research_context/REVIEW_GATE.md",
 "research/autonomous_w2/g2/HYPOTHESIS_CENTERED_RESIDUAL_TUBE_v1.md","research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v6.md",
 PROTOCOL_REL,PROFILE_REL,
 "results/validation/autonomous_w2/g2/centered_error_tube_preflight_v2.json",
 "results/validation/autonomous_w2/g2/centered_v6_nonquery_fixtures_v1.json",
 "results/validation/autonomous_w2/g2/pre_run_validation_centered_v6.json",
 "results/validation/autonomous_w2/g2/pre_run_validation_centered_v6_v2.json",
 "results/validation/autonomous_w2/g2/pre_run_validation_centered_v6_v3.json",
 "validation/autonomous_w2/g2/__init__.py","validation/autonomous_w2/g2/producer_v4.py","validation/autonomous_w2/g2/rational_interval_v3.py",
 "validation/autonomous_w2/g2/windows_job_supervisor.py","validation/autonomous_w2/g2/producer_centered_v6.py",
 "validation/autonomous_w2/g2/checker_centered_v6.py","validation/autonomous_w2/g2/centered_v6_nonquery_fixtures.py",
 "validation/autonomous_w2/g2/pre_run_validation_centered_v6.py","validation/autonomous_w2/g2/freeze_development_centered_v6.py","validation/autonomous_w2/g2/run_stage_centered_v6.py",
 "validation/autonomous_w2/g2/publish_release_centered_v6.py",
 "results/validation/autonomous_w2/g2/pre_run_validation_centered_v6.json",
 "coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_14.json",
 "results/validation/autonomous_w2/g2/development_v5/stage_receipt.json",
 "results/validation/autonomous_w2/g2/development_v5/freeze_receipt_v5.json",
 "coordination/autonomous_w2/g2/releases/RELEASE_v5.json",
]

def sha(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(path:Path,value:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("xb") as f: f.write(json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True).encode()+b"\n"); f.flush(); os.fsync(f.fileno())
def now()->str: return datetime.now(timezone.utc).isoformat()

def freeze()->dict[str,Any]:
    plan_path=ROOT/PLAN_REL; bind_dir=ROOT/BINDING_DIR_REL; freeze_path=ROOT/FREEZE_REL; result_root=ROOT/RESULT_REL
    if plan_path.exists() or bind_dir.exists() or freeze_path.exists() or result_root.exists(): raise FileExistsError("V6_PLAN_BINDING_OR_RESULT_PATH_ALREADY_EXISTS")
    status=json.loads((ROOT/"coordination/autonomous_w2/g2/STATUS.json").read_text(encoding="utf-8"))
    if status.get("sequence")!=14 or status.get("native_attempts",{}).get("count_completed")!=21 or status.get("native_attempts",{}).get("remaining_attempts")!=3:
        raise ValueError("G2_STATUS_MUST_BE_SEQUENCE_14_WITH_21_USED_AND_3_REMAINING")
    fixture=json.loads((ROOT/"results/validation/autonomous_w2/g2/centered_v6_nonquery_fixtures_v1.json").read_text(encoding="utf-8"))
    if fixture.get("status")!="PASS" or fixture.get("native_attempts_added")!=0 or fixture.get("actual_protocol_action_rows_evaluated")!=0:
        raise ValueError("CENTERED_V6_NONQUERY_FIXTURES_NOT_PASS_OR_CONTAIN_TASK_EVALUATION")
    pre_run=json.loads((ROOT/"results/validation/autonomous_w2/g2/pre_run_validation_centered_v6_v3.json").read_text(encoding="utf-8"))
    if pre_run.get("status")!="PASS" or pre_run.get("attempts_run_by_preflight")!=0: raise ValueError("V6_PRE_RUN_VALIDATION_NOT_PASS_OR_EVALUATED_TASK")
    profile=json.loads((ROOT/PROFILE_REL).read_text(encoding="utf-8")); protocol=json.loads((ROOT/PROTOCOL_REL).read_text(encoding="utf-8"))
    profile_expected={"profile_id":"G2_W2_CENTERED_RESIDUAL_TUBE_V6_256_SLABS","center_time_slabs":256,"center_slab_duration_s":"1/128",
      "matrix_taylor_degree":20,"interval_fractional_bits":96,"rational_bit_cap":16384,"python_int_string_digit_cap":5000,
      "sqrt_bisections":48,"interval_operation_cap":5000000,"worker_wall_cap_seconds":60,"worker_memory_cap_bytes":1073741824,
      "worker_process_cap":1,"stdout_cap_bytes":8388608,"stderr_cap_bytes":1048576,"phase_wall_cap_seconds":7200}
    if any(profile.get(k)!=v for k,v in profile_expected.items()): raise ValueError("PROFILE_DOES_NOT_MATCH_FROZEN_CAPS")
    if protocol.get("protocol_id")!="G2_W2_VOF_TASK_V1" or len(protocol.get("actions",[]))!=3 or [a.get("id") for a in protocol["actions"]]!=ACTION_IDS:
        raise ValueError("PROTOCOL_ORDER_OR_ACTION_SET")
    branch=subprocess.run(["git","branch","--show-current"],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()
    head=subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()
    if branch!="main" or head!="94c60f627a2ce1a8d52101050bdc0ce9d2e59afe": raise ValueError("BRANCH_OR_HEAD_CHANGED_FROM_W2_BASELINE")
    source_files={rel:sha(ROOT/rel) for rel in sorted(set(SOURCE_PATHS))}
    protocol_sha=sha(ROOT/PROTOCOL_REL); profile_sha=sha(ROOT/PROFILE_REL); runner_sha=sha(ROOT/RUNNER_REL)
    prior_release="coordination/autonomous_w2/g2/releases/RELEASE_v5.json"
    prior_stage="results/validation/autonomous_w2/g2/development_v5/stage_receipt.json"
    peer_status_path=ROOT/"coordination/autonomous_w2/g4/STATUS.json"
    peer_audit_path=ROOT/"coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v1.json"
    peer={"status_path":peer_status_path.relative_to(ROOT).as_posix(),"status_sha256":sha(peer_status_path),
      "sequence":json.loads(peer_status_path.read_text(encoding="utf-8")).get("sequence"),
      "phase":json.loads(peer_status_path.read_text(encoding="utf-8")).get("phase"),
      "audit_path":peer_audit_path.relative_to(ROOT).as_posix(),"audit_sha256":sha(peer_audit_path),
      "decision":json.loads(peer_audit_path.read_text(encoding="utf-8")).get("decision"),"release_consumed":json.loads(peer_audit_path.read_text(encoding="utf-8")).get("peer_release_manifest_sha256")}
    attempts=[]; action_map={a["id"]:a for a in protocol["actions"]}
    for ix,action_id in enumerate(ACTION_IDS,1):
        bpath=f"{BINDING_DIR_REL}/attempt_{ix:02d}.json"
        binding={"schema":"G2_W2_CENTERED_V6_ROW_BINDING_v1","session":"DDWMR | LUNA-G2-SCOPE","attempt":ix,
          "native_attempt_ordinal":21+ix,"method":"centered_residual_v6","action_id":action_id,"action":action_map[action_id],
          "plan_id":"G2_W2_CENTERED_V6_DEVELOPMENT_PLAN","plan_path":PLAN_REL,"binding_path":bpath,
          "protocol_path":PROTOCOL_REL,"protocol_sha256":protocol_sha,"profile_path":PROFILE_REL,"profile_sha256":profile_sha,
          "runner_path":RUNNER_REL,"runner_sha256":runner_sha,"source_files":source_files,"result_root":RESULT_REL,
          "attempt_kind":"counted native development evaluation; not held-out confirmation","attempt_order":"zero, nominal, alternative; one worker launch; no retry",
          "prior_native_attempts":21,"legacy_800_row_study":"NOT_RUN","held_out_rows":0}
        dump(ROOT/bpath,binding); attempts.append({"attempt":ix,"native_attempt_ordinal":21+ix,"action_id":action_id,
          "binding_path":bpath,"binding_sha256":sha(ROOT/bpath),"action":action_map[action_id]})
    plan={"schema":"G2_W2_CENTERED_V6_DEVELOPMENT_PLAN_v1","plan_id":"G2_W2_CENTERED_V6_DEVELOPMENT_PLAN","plan_path":PLAN_REL,
      "session":"DDWMR | LUNA-G2-SCOPE","repository_branch":branch,"repository_head":head,"plan_state":"FROZEN_BEFORE_NATIVE_ATTEMPTS",
      "frozen_utc":now(),"protocol_id":protocol["protocol_id"],"protocol_path":PROTOCOL_REL,"protocol_sha256":protocol_sha,
      "profile_path":PROFILE_REL,"profile_sha256":profile_sha,"runner_path":RUNNER_REL,"runner_sha256":runner_sha,
      "freeze_script_path":"validation/autonomous_w2/g2/freeze_development_centered_v6.py","freeze_script_sha256":sha(ROOT/"validation/autonomous_w2/g2/freeze_development_centered_v6.py"),
      "source_files":source_files,"source_count":len(source_files),"result_root":RESULT_REL,"binding_directory":BINDING_DIR_REL,
      "compute_lock_path":"coordination/autonomous_w2/COMPUTE.lock","attempt_limit":24,"prior_native_attempts":21,
      "planned_attempt_count":3,"cumulative_native_attempts_after_all":24,"ordered_attempts":attempts,
      "retry_policy":"exactly one producer launch per ordered action; stop on integrity, worker, resource or replay failure; no retries",
      "development_inputs_are_consumed":True,"held_out_rows":0,"g4_confirmation_rows_run_by_g2":0,
      "legacy_800_row_study":"800/800 NOT_RUN","previous_release_path":prior_release,"previous_release_sha256":sha(ROOT/prior_release),
      "previous_stage_path":prior_stage,"previous_stage_sha256":sha(ROOT/prior_stage),"peer_state_observed":peer,
      "independent_feasibility_screen_path":"results/validation/autonomous_w2/g2/centered_error_tube_preflight_v2.json",
      "independent_feasibility_screen_sha256":sha(ROOT/"results/validation/autonomous_w2/g2/centered_error_tube_preflight_v2.json"),
      "direct_R3_same_input_attempts":"NOT_PLANNED_WITHIN_REMAINING_THREE; G4 owns matched confirmation",
      "environment":{"python":sys.version,"platform":sys.platform}}
    dump(plan_path,plan)
    receipt={"schema":"G2_W2_CENTERED_V6_FREEZE_RECEIPT_v1","plan_path":PLAN_REL,"plan_sha256":sha(plan_path),
      "frozen_utc":plan["frozen_utc"],"source_count":len(source_files),"source_files":source_files,
      "attempt_count_frozen":3,"prior_native_attempts":21,"cumulative_cap":24,
      "binding_paths":[x["binding_path"] for x in attempts],"binding_sha256":{x["binding_path"]:x["binding_sha256"] for x in attempts},
      "no_attempt_executed_by_freeze":True,"peer_state_observed":peer}
    dump(freeze_path,receipt)
    return receipt

if __name__=="__main__": print(json.dumps(freeze(),sort_keys=True,indent=2))
