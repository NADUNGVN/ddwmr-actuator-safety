"""One-shot, resource-bounded W2 G2 v6 development stage; no retries."""
from __future__ import annotations
import argparse, base64, hashlib, json, os, subprocess, sys, time, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .windows_job_supervisor import result_to_json, run_bounded_process

ROOT=Path(__file__).resolve().parents[3]
PLAN_REL="research/autonomous_w2/g2/development_plan_centered_v6.json"
FREEZE_REL="results/validation/autonomous_w2/g2/development_centered_v6/freeze_receipt_v6.json"
RUNNER_REL="validation/autonomous_w2/g2/run_stage_centered_v6.py"
STATUS_REL="coordination/autonomous_w2/g2/STATUS.json"

def sha(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path:Path)->Any: return json.loads(path.read_text(encoding="utf-8"))
def dump(path:Path,value:Any,exclusive:bool=False)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    mode="xb" if exclusive else "wb"
    with path.open(mode) as f:
        f.write(json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True).encode()+b"\n")
        f.flush(); os.fsync(f.fileno())
def now()->str: return datetime.now(timezone.utc).isoformat()

def bounded(command:list[str],profile:dict[str,Any])->dict[str,Any]:
    env=os.environ.copy(); env["PYTHONHASHSEED"]="0"; env["PYTHONUTF8"]="1"
    try:
        result=run_bounded_process(command,cwd=ROOT,wall_seconds=int(profile["worker_wall_cap_seconds"]),
          cpu_seconds=int(profile["worker_wall_cap_seconds"]),memory_bytes=int(profile["worker_memory_cap_bytes"]),
          max_processes=int(profile["worker_process_cap"]),stdout_limit_bytes=int(profile["stdout_cap_bytes"]),
          stderr_limit_bytes=int(profile["stderr_cap_bytes"]),environment=env)
        return {"launch_error":None,"job":result_to_json(result)}
    except BaseException as exc:
        return {"launch_error":f"{type(exc).__name__}:{exc}","job":None}

def persist_process(folder:Path,name:str,evidence:dict[str,Any])->bytes:
    dump(folder/f"{name}.job.json",evidence,exclusive=True)
    job=evidence.get("job") or {}; out=job.get("stdout") or {}; err=job.get("stderr") or {}
    out_bytes=base64.b64decode(out.get("prefix_base64","")); err_bytes=base64.b64decode(err.get("prefix_base64",""))
    (folder/f"{name}.stdout.bin").write_bytes(out_bytes); (folder/f"{name}.stderr.bin").write_bytes(err_bytes)
    return out_bytes

def row_attempt(item:dict[str,Any],binding_path:Path,profile:dict[str,Any],out_root:Path,deadline:float)->dict[str,Any]:
    folder=out_root/f"attempt_{int(item['attempt']):02d}_{item['action_id']}"
    folder.mkdir(parents=True,exist_ok=False)
    intent={"schema":"G2_W2_V6_ATTEMPT_INTENT_v1","attempt":item["attempt"],"native_attempt_ordinal":item["native_attempt_ordinal"],
      "action_id":item["action_id"],"binding_path":item["binding_path"],"binding_sha256":sha(binding_path),
      "started_utc":now(),"no_retry":True,"counted_as_native_configuration_attempt":True}
    dump(folder/"attempt_intent.json",intent,exclusive=True)
    result={**intent,"status":"STARTED","worker":None,"checker":None}
    if time.monotonic()>=deadline:
        result["status"]="PHASE_WALL_LIMIT_BEFORE_WORKER"; dump(folder/"attempt_receipt.json",result,exclusive=True); return result
    binding_rel=binding_path.relative_to(ROOT).as_posix()
    cmd=[sys.executable,"-m","validation.autonomous_w2.g2.producer_centered_v6","--binding",binding_rel,"--action-id",item["action_id"]]
    ev=bounded(cmd,profile); stdout=persist_process(folder,"worker",ev); job=ev.get("job") or {}
    row=None; parse_error=None
    try:
        row=json.loads(stdout.decode("utf-8").strip())
        if not isinstance(row,dict): raise TypeError("WORKER_OUTPUT_NOT_OBJECT")
        dump(folder/"row.json",row,exclusive=True)
    except BaseException as exc: parse_error=f"{type(exc).__name__}:{exc}"
    record_ok=(job.get("status")=="COMPLETED" and job.get("returncode")==0 and isinstance(row,dict) and row.get("schema")=="G2_W2_CENTERED_RESIDUAL_ROW_v6")
    result["worker"]={"status":job.get("status") or "LAUNCH_FAILURE","launch_error":ev.get("launch_error"),
      "returncode":job.get("returncode"),"stdout_sha256":hashlib.sha256(stdout).hexdigest(),"stdout_bytes":len(stdout),
      "parsed":isinstance(row,dict),"schema":row.get("schema") if isinstance(row,dict) else None,
      "failure_reason":row.get("reason_code") if isinstance(row,dict) else parse_error,
      "peak_memory_bytes":(job.get("job") or {}).get("peak_memory_bytes"),
      "elapsed_seconds_display_only":job.get("elapsed_seconds_display_only")}
    if not record_ok:
        result["status"]="WORKER_FAILURE_OR_RESOURCE_UNKNOWN"; result["worker_parse_error"]=parse_error
        dump(folder/"attempt_receipt.json",result,exclusive=True); return result
    if time.monotonic()>=deadline:
        result["status"]="PHASE_WALL_LIMIT_BEFORE_CHECKER"; dump(folder/"attempt_receipt.json",result,exclusive=True); return result
    record_rel=(folder/"row.json").relative_to(ROOT).as_posix()
    check_cmd=[sys.executable,"-m","validation.autonomous_w2.g2.checker_centered_v6","--binding",binding_rel,"--record",record_rel]
    cev=bounded(check_cmd,profile); cstdout=persist_process(folder,"checker",cev); cjob=cev.get("job") or {}
    replay=None; cparse=None
    try:
        replay=json.loads(cstdout.decode("utf-8").strip())
        if not isinstance(replay,dict): raise TypeError("CHECKER_OUTPUT_NOT_OBJECT")
        dump(folder/"replay.json",replay,exclusive=True)
    except BaseException as exc: cparse=f"{type(exc).__name__}:{exc}"
    replay_ok=cjob.get("status")=="COMPLETED" and cjob.get("returncode")==0 and isinstance(replay,dict) and replay.get("replayed") is True
    result["checker"]={"status":cjob.get("status") or "LAUNCH_FAILURE","launch_error":cev.get("launch_error"),
      "returncode":cjob.get("returncode"),"stdout_sha256":hashlib.sha256(cstdout).hexdigest(),"stdout_bytes":len(cstdout),
      "replayed":replay.get("replayed") if isinstance(replay,dict) else False,
      "rejection":replay.get("rejection") if isinstance(replay,dict) else cparse,
      "peak_memory_bytes":(cjob.get("job") or {}).get("peak_memory_bytes"),
      "elapsed_seconds_display_only":cjob.get("elapsed_seconds_display_only")}
    result["row_sha256"]=sha(folder/"row.json"); result["replay_sha256"]=sha(folder/"replay.json") if (folder/"replay.json").exists() else None
    if replay_ok:
        result.update({"status":"REPLAYED","safety_status":row["safety_status"],"task_eligible":row["task_eligible"],
          "progress_enclosure_m":row["progress_enclosure_m"],"clip_beta_upper":row["clip_beta_upper_full_domain"],
          "contact_margin_lower_N":row["contact_margin_lower_N"],"collision_margin_lower_m":row["collision_margin_lower_m"],
          "internal_error_radius_full_hold":row["internal_error_radius_full_hold"],"reason_codes":row["reason_codes"],
          "interval_operations":row["arithmetic"]["interval_operations"],"max_rational_bits":row["arithmetic"]["max_rational_bits"]})
    else: result["status"]="REPLAY_OR_RESOURCE_FAILURE"
    dump(folder/"attempt_receipt.json",result,exclusive=True)
    return result

def run_stage(plan_path:Path)->dict[str,Any]:
    plan_path=plan_path.resolve(); plan_rel=plan_path.relative_to(ROOT).as_posix(); plan=load(plan_path)
    if plan.get("schema")!="G2_W2_CENTERED_V6_DEVELOPMENT_PLAN_v1" or plan.get("plan_path")!=plan_rel or plan.get("plan_state")!="FROZEN_BEFORE_NATIVE_ATTEMPTS":
        raise ValueError("PLAN_SCHEMA_PATH_OR_STATE")
    freeze_path=ROOT/FREEZE_REL; freeze=load(freeze_path)
    if freeze.get("plan_sha256")!=sha(plan_path): raise ValueError("FREEZE_RECEIPT_PLAN_HASH")
    if sha(ROOT/RUNNER_REL)!=plan.get("runner_sha256"): raise ValueError("RUNNER_HASH_MISMATCH")
    if sha(ROOT/plan["protocol_path"])!=plan["protocol_sha256"] or sha(ROOT/plan["profile_path"])!=plan["profile_sha256"]:
        raise ValueError("FROZEN_PROTOCOL_OR_PROFILE_HASH_MISMATCH")
    for rel,want in plan["source_files"].items():
        if sha(ROOT/rel)!=want: raise ValueError(f"SOURCE_CLOSURE_HASH_MISMATCH:{rel}")
    protocol=load(ROOT/plan["protocol_path"]); expected_actions={a["id"]:a for a in protocol.get("actions",[])}
    if [x.get("action_id") for x in plan["ordered_attempts"]]!=["W2_G2_DEV_001_ZERO","W2_G2_DEV_001_NOMINAL","W2_G2_DEV_001_ALTERNATIVE"]:
        raise ValueError("FROZEN_ACTION_ORDER_MISMATCH")
    for item in plan["ordered_attempts"]:
        bpath=ROOT/item["binding_path"]; binding=load(bpath)
        if freeze["binding_sha256"].get(item["binding_path"])!=sha(bpath): raise ValueError("FREEZE_BINDING_HASH_MISMATCH")
        expected={"binding_path":item["binding_path"],"action_id":item["action_id"],"action":expected_actions.get(item["action_id"]),
          "attempt":item["attempt"],"native_attempt_ordinal":item["native_attempt_ordinal"],"protocol_sha256":plan["protocol_sha256"],
          "profile_sha256":plan["profile_sha256"],"source_files":plan["source_files"],"result_root":plan["result_root"]}
        if any(binding.get(k)!=v for k,v in expected.items()): raise ValueError("FROZEN_BINDING_CONTENT_MISMATCH")
    if plan.get("prior_native_attempts")!=21 or plan.get("planned_attempt_count")!=3 or plan.get("prior_native_attempts",0)+3>24:
        raise ValueError("NATIVE_ATTEMPT_BUDGET")
    status=load(ROOT/STATUS_REL)
    if status.get("native_attempts",{}).get("count_completed")!=21 or status.get("native_attempts",{}).get("remaining_attempts")!=3:
        raise ValueError("CURRENT_G2_STATUS_ATTEMPT_COUNT_MISMATCH")
    profile=load(ROOT/plan["profile_path"]); lock_path=ROOT/plan["compute_lock_path"]; token=uuid.uuid4().hex
    lock={"session":"DDWMR | LUNA-G2-SCOPE","pid":os.getpid(),"started_utc":now(),"plan_path":plan_rel,"plan_sha256":sha(plan_path),"token":token}
    dump(lock_path,lock,exclusive=True)
    started=time.monotonic(); deadline=started+int(profile["phase_wall_cap_seconds"]); results=[]
    stage_root=ROOT/plan["result_root"]
    try:
        stage_root.mkdir(parents=True,exist_ok=True)
        if (stage_root/"stage_receipt.json").exists() or any(p.is_dir() and p.name.startswith("attempt_") for p in stage_root.iterdir()):
            raise FileExistsError("V6_STAGE_OR_ATTEMPT_OUTPUT_ALREADY_EXISTS_NO_RETRY")
        for item in plan["ordered_attempts"]:
            bpath=ROOT/item["binding_path"]
            try: row=row_attempt(item,bpath,profile,stage_root,deadline)
            except BaseException as exc:
                row={"attempt":item["attempt"],"native_attempt_ordinal":item["native_attempt_ordinal"],"action_id":item["action_id"],
                  "binding_path":item["binding_path"],"status":"STAGE_OR_PRELAUNCH_FAILURE","error":f"{type(exc).__name__}:{exc}",
                  "counted_as_native_configuration_attempt":True,"ended_utc":now()}
                results.append(row); break
            results.append(row)
            if row.get("status") not in ("REPLAYED",): break
        counts={}
        for row in results: counts[row["status"]]=counts.get(row["status"],0)+1
        finished=now()
        stage={"schema":"G2_W2_CENTERED_V6_DEVELOPMENT_STAGE_RECEIPT_v1","session":"DDWMR | LUNA-G2-SCOPE",
          "plan_path":plan_rel,"plan_sha256":sha(plan_path),"freeze_receipt_sha256":sha(freeze_path),
          "protocol_sha256":plan["protocol_sha256"],"profile_sha256":plan["profile_sha256"],"source_files":plan["source_files"],
          "stage_started_utc":lock["started_utc"],"stage_ended_utc":finished,"attempts_counted":len(results),
          "prior_native_attempts":21,"cumulative_native_attempts":21+len(results),"planned_attempts":3,"status_counts":counts,
          "attempts":results,"phase_wall_cap_seconds":profile["phase_wall_cap_seconds"],
          "phase_elapsed_seconds_display_only":round(time.monotonic()-started,6),"no_retries":True,
          "held_out_rows":0,"legacy_800_row_study":"NOT_RUN"}
        dump(stage_root/"stage_receipt.json",stage,exclusive=True)
        return stage
    finally:
        try:
            if load(lock_path).get("token")==token: lock_path.unlink()
        except FileNotFoundError: pass

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--plan",default=PLAN_REL); args=ap.parse_args()
    p=Path(args.plan); p=p if p.is_absolute() else ROOT/p
    try:
        out=run_stage(p); print(json.dumps(out,sort_keys=True,indent=2)); return 0
    except BaseException as exc:
        print(json.dumps({"schema":"G2_W2_CENTERED_V6_STAGE_FAILURE_v1","reason":f"{type(exc).__name__}:{exc}","native_attempts_may_have_started":False},sort_keys=True)); return 2

if __name__=="__main__": raise SystemExit(main())
