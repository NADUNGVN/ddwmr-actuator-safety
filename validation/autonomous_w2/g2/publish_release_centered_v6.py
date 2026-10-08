"""Publish immutable v6 candidate and file-based G4 audit request/status."""
from __future__ import annotations
import hashlib,json,os,tempfile
from datetime import datetime,timezone
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[3]
RELEASE_REL="coordination/autonomous_w2/g2/releases/RELEASE_v6.json"
REQUEST_REL="coordination/autonomous_w2/g2/AUDIT_REQUEST_TO_G4_v6.md"
STATUS_REL="coordination/autonomous_w2/g2/STATUS.json"

def sha(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path:Path)->Any: return json.loads(path.read_text(encoding="utf-8"))
def dump_exclusive(path:Path,value:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("xb") as f: f.write(json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True).encode()+b"\n"); f.flush(); os.fsync(f.fileno())
def atomic_json(path:Path,value:Any)->None:
    raw=json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True).encode()+b"\n"
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=path.name+".",suffix=".tmp",dir=path.parent)
    try:
        with os.fdopen(fd,"wb") as f: f.write(raw); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    except BaseException:
        try: os.unlink(tmp)
        except FileNotFoundError: pass
        raise
def now()->str: return datetime.now(timezone.utc).isoformat()

def publish()->dict[str,Any]:
    if (ROOT/RELEASE_REL).exists() or (ROOT/REQUEST_REL).exists(): raise FileExistsError("V6_RELEASE_OR_REQUEST_ALREADY_EXISTS")
    plan_rel="research/autonomous_w2/g2/development_plan_centered_v6.json"; plan=load(ROOT/plan_rel)
    freeze_rel="results/validation/autonomous_w2/g2/development_centered_v6/freeze_receipt_v6.json"; freeze=load(ROOT/freeze_rel)
    if freeze.get("plan_sha256")!=sha(ROOT/plan_rel) or plan.get("plan_state")!="FROZEN_BEFORE_NATIVE_ATTEMPTS": raise ValueError("PLAN_OR_FREEZE_RECEIPT_MISMATCH")
    for rel,want in plan["source_files"].items():
        if sha(ROOT/rel)!=want: raise ValueError(f"SOURCE_CLOSURE_MISMATCH:{rel}")
    peer_status_rel="coordination/autonomous_w2/g4/STATUS.json"; peer_audit_rel="coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v1.json"
    peer_status=load(ROOT/peer_status_rel); peer_audit=load(ROOT/peer_audit_rel)
    protocol=load(ROOT/plan["protocol_path"]); profile=load(ROOT/plan["profile_path"])
    code_map_rel="research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v6.md"; hypothesis_rel="research/autonomous_w2/g2/HYPOTHESIS_CENTERED_RESIDUAL_TUBE_v1.md"
    preflight_rel="results/validation/autonomous_w2/g2/centered_error_tube_preflight_v2.json"
    preflight=load(ROOT/preflight_rel)
    release={"schema":"DDWMR_G2_W2_IMMUTABLE_RELEASE_v6","release_id":"G2_W2_VOF_TASK_V1_CENTERED_RESIDUAL_V6",
      "release_sequence":6,"session":"DDWMR | LUNA-G2-SCOPE","workflow":"DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2",
      "published_utc":now(),"release_state":"FROZEN_FOR_G4_AUDIT_AND_BOUNDED_DEVELOPMENT",
      "repository":{"branch":plan["repository_branch"],"head":plan["repository_head"]},
      "claim_scope":{"type":"one-hold robust enclosure candidate, synthetic development domain only",
        "quantifiers":"for every initial state in the complete protocol box, every fixed label vector in the complete positive-width Cartesian image, and every t in [0,2 s], for each separately held common voltage action",
        "predicates":["clip-affine branch by first-exit proof","algebraic lateral-reaction/contact admissibility on full hold","static-circle full-hold collision clearance","endpoint p_x(T)-p_x(0) lower bound"],
        "not_claimed":["physical tire/support correspondence","recursive/closed-loop safety","universal usefulness or novelty","G2 gate PASS"]},
      "supported_model":{"formulation":protocol["model"]["formulation"],"traction_law":protocol["model"]["phi"],
        "fixed_constants":protocol["model"]["fixed_constants"],"parameter_order":protocol["model"]["fixed_label_order"],
        "parameter_bounds":protocol["model"]["fixed_label_bounds"],"parameter_maps":protocol["model"]["parameter_maps"],
        "label_semantics":protocol["model"]["label_semantics"],"initial_box_state_order":protocol["task"]["initial_box_state_order"],
        "initial_box":protocol["task"]["initial_box"]},
      "task":{"protocol_path":plan["protocol_path"],"protocol_sha256":plan["protocol_sha256"],"hold_s":protocol["task"]["hold_s"],
        "progress_metric":protocol["task"]["progress_metric"],"required_progress_m":protocol["task"]["required_progress_m"],
        "threshold_declared_before_evaluator_outputs":True,"obstacle":protocol["task"]["obstacle"],"actions":protocol["actions"],
        "selection_rule":protocol["selection_rule"],"task_rationale":protocol["task"]["independent_task_rationale"]},
      "proof":{"hypothesis_path":hypothesis_rel,"hypothesis_sha256":sha(ROOT/hypothesis_rel),"proof_to_code_map_path":code_map_rel,
        "proof_to_code_map_sha256":sha(ROOT/code_map_rel),"centered_residual_statement":"||e(t)||_inf <= exp(mu*t)*(e0+t*delta_A), E=ceil(exp(mu*T)*(e0+T*delta_A))",
        "full_hold_slabs":256,"slab_duration_s":"1/128","fixed_labels_across_slabs":True,"same_voltage_across_hold":True,
        "checker_recomputes_all_claim_fields":True},
      "arithmetic_resource_profile":{"path":plan["profile_path"],"sha256":plan["profile_sha256"],"settings":profile},
      "implementation":{"producer":"validation.autonomous_w2.g2.producer_centered_v6","checker":"validation.autonomous_w2.g2.checker_centered_v6",
        "stage_runner":plan["runner_path"],"stage_runner_sha256":plan["runner_sha256"],"independent_replay_command":"python -m validation.autonomous_w2.g2.checker_centered_v6 --binding <binding.json> --record <row.json>",
        "development_command":"python -m validation.autonomous_w2.g2.run_stage_centered_v6 --plan research/autonomous_w2/g2/development_plan_centered_v6.json",
        "artifact_schemas":["G2_W2_CENTERED_RESIDUAL_ROW_v6","G2_W2_CENTERED_RESIDUAL_REPLAY_v6","G2_W2_CENTERED_V6_DEVELOPMENT_STAGE_RECEIPT_v1"]},
      "source_closure":{"count":plan["source_count"],"sha256_by_path":plan["source_files"],"freeze_receipt_path":freeze_rel,
        "freeze_receipt_sha256":sha(ROOT/freeze_rel),"plan_path":plan_rel,"plan_sha256":sha(ROOT/plan_rel),
        "binding_paths":[x["binding_path"] for x in plan["ordered_attempts"]],"binding_sha256":freeze["binding_sha256"]},
      "preimplementation_screen":{"path":preflight_rel,"sha256":sha(ROOT/preflight_rel),"classification":preflight.get("classification"),
        "native_attempts_added":preflight.get("native_attempts_added"),"all_actions_center_safe_clip_contact":preflight.get("all_actions_center_safe_clip_contact"),
        "task_distinction_possible":preflight.get("prospective_task_rule_possible"),"not_a_certificate":True},
      "development_budget":{"limit":24,"prior_attempts":21,"frozen_attempts":3,"ordinals":[22,23,24],
        "ordered_actions":[x["action_id"] for x in plan["ordered_attempts"]],"attempts_run_at_release":0,"retries":0,
        "held_out_rows":0,"g4_confirmation_rows_run_by_g2":0,"old_800_row_study":"800/800 NOT_RUN"},
      "peer_state_at_release":{"status_path":peer_status_rel,"status_sha256":sha(ROOT/peer_status_rel),"sequence":peer_status.get("sequence"),
        "phase":peer_status.get("phase"),"audit_state_path":peer_audit_rel,"audit_state_sha256":sha(ROOT/peer_audit_rel),
        "decision":peer_audit.get("decision"),"release_consumed":peer_audit.get("peer_release_manifest_sha256")},
      "previous_release":{"path":"coordination/autonomous_w2/g2/releases/RELEASE_v5.json","sha256":plan["previous_release_sha256"]}}
    dump_exclusive(ROOT/RELEASE_REL,release); release_sha=sha(ROOT/RELEASE_REL)
    (ROOT/(RELEASE_REL+".sha256")).write_text(release_sha+"  RELEASE_v6.json\n",encoding="ascii")
    request=(f"Session: DDWMR | LUNA-G2-SCOPE\n\n# G2 W2 v6 release audit request\n\n"
      f"Please independently audit immutable release `{RELEASE_REL}` (SHA-256 `{release_sha}`) under W2 and bind your decision to this exact hash in the G4-owned coordination prefix.\n\n"
      "Audit the quantifiers and first-exit argument, residual/logarithmic-norm bounds, center-slab and endpoint chaining, clip/contact/collision/progress derivations, producer/checker independence, exact arithmetic/resource pins, artifact/source closure, and the task's prospective usefulness rule.\n\n"
      "This is a candidate for scoped development, not a request to pass G2. The three final G2 development attempts have not run at release time; held-out rows remain 0 and the legacy 800-row study remains NOT_RUN.\n\n"
      "Please state `ACCEPT_FOR_SCOPED_VALIDATION` or the exact mathematical/code defects and publish the audit result only in your G4-owned files. The G2 request and release are read-only to G4.\n")
    (ROOT/REQUEST_REL).parent.mkdir(parents=True,exist_ok=True); (ROOT/REQUEST_REL).write_text(request,encoding="utf-8")
    paths=[RELEASE_REL,RELEASE_REL+".sha256",REQUEST_REL,plan_rel,freeze_rel,plan["profile_path"],plan["runner_path"],
      "validation/autonomous_w2/g2/producer_centered_v6.py","validation/autonomous_w2/g2/checker_centered_v6.py",code_map_rel,hypothesis_rel,
      "validation/autonomous_w2/g2/centered_v6_nonquery_fixtures.py","results/validation/autonomous_w2/g2/centered_v6_nonquery_fixtures_v1.json",preflight_rel]
    paths.extend(["results/validation/autonomous_w2/g2/pre_run_validation_centered_v6.json",
      "results/validation/autonomous_w2/g2/pre_run_validation_centered_v6_v2.json",
      "results/validation/autonomous_w2/g2/pre_run_validation_centered_v6_v3.json"])
    artifacts={p:sha(ROOT/p) for p in paths}
    status=load(ROOT/STATUS_REL)
    if status.get("sequence")!=14: raise ValueError("STATUS_SEQUENCE_MUST_BE_14_BEFORE_V6_PUBLISH")
    new={**status,"sequence":15,"utc":now(),"phase":"PUBLISHED","objective":"Release the centered residual v6 runnable candidate for direct G4 audit, then use only the three remaining bounded development actions.",
      "artifacts":artifacts,"blocker":None,"native_attempts":{"G2_limit":24,"count_completed":21,"remaining_attempts":3,
        "planned_frozen_attempts":3,"held_out_rows":0,"legacy_800_row_study":"800/800 NOT_RUN",
        "v1_attempts":6,"v2_attempts":6,"v3_attempts":3,"v4_attempts":3,"v5_attempts":3},
      "release":{"path":RELEASE_REL,"sha256":release_sha,"state":release["release_state"]},
      "previous_release":{"path":"coordination/autonomous_w2/g2/releases/RELEASE_v5.json","sha256":plan["previous_release_sha256"]},
      "stage_result":{"path":None,"status":"NOT_RUN_AT_RELEASE","all_candidate_rows_replayed":False,"task_eligible_rows":None},
      "peer_status_observed":{"status_path":peer_status_rel,"status_sha256":sha(ROOT/peer_status_rel),"sequence":peer_status.get("sequence"),
        "phase":peer_status.get("phase"),"audit_path":peer_audit_rel,"audit_sha256":sha(ROOT/peer_audit_rel),
        "decision":peer_audit.get("decision"),"release_consumed":peer_audit.get("peer_release_manifest_sha256"),"observed_utc":now()},
      "next_action":"Read the G4-owned release decision directly. Complete G2's one-shot frozen 3-row development stage with no retry, then replay saved proof and run mutation audits.",
      "working_tree_note":"Shared tree retained; G2 writes confined to G2-owned W2 prefixes; G4 files read only; no branch switch, commit or push."}
    dump_exclusive(ROOT/"coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_15.json",new)
    atomic_json(ROOT/STATUS_REL,new)
    return {"release_path":RELEASE_REL,"release_sha256":release_sha,"request_path":REQUEST_REL,"status_sequence":15,"status_phase":"PUBLISHED","artifact_count":len(artifacts)}

if __name__=="__main__": print(json.dumps(publish(),sort_keys=True,indent=2))
