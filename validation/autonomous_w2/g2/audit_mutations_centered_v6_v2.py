"""Bounded post-run mutations of saved v6 records only; no producer/query is called."""
from __future__ import annotations
import base64,hashlib,json,os,sys,uuid
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
from typing import Any,Callable

from .windows_job_supervisor import result_to_json,run_bounded_process

ROOT=Path(__file__).resolve().parents[3]
STAGE_REL="results/validation/autonomous_w2/g2/development_centered_v6"
OUT_REL=f"{STAGE_REL}/mutation_audit_v2/mutation_audit_report.json"
LOCK_REL="coordination/autonomous_w2/COMPUTE.lock"

def sha(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path:Path)->Any: return json.loads(path.read_text(encoding="utf-8"))
def dump(path:Path,value:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("xb") as f: f.write(json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True).encode()+b"\n"); f.flush(); os.fsync(f.fileno())
def now()->str: return datetime.now(timezone.utc).isoformat()

def main()->dict[str,Any]:
    out=ROOT/OUT_REL
    if out.exists(): raise FileExistsError("MUTATION_AUDIT_ALREADY_EXISTS_NO_RETRY")
    plan=load(ROOT/"research/autonomous_w2/g2/development_plan_centered_v6.json")
    profile=load(ROOT/"validation/autonomous_w2/g2/profile_centered_v6.json")
    stage=load(ROOT/f"{STAGE_REL}/stage_receipt.json")
    if stage.get("attempts_counted")!=3 or stage.get("cumulative_native_attempts")!=24 or stage.get("status_counts")!={"REPLAYED":3}:
        raise ValueError("V6_STAGE_NOT_COMPLETE_WITH_THREE_REPLAYED_ROWS")
    lock_path=ROOT/LOCK_REL; token=uuid.uuid4().hex
    dump(lock_path,{"session":"DDWMR | LUNA-G2-SCOPE","pid":os.getpid(),"started_utc":now(),"task":"saved-record adversarial replay mutations; no native queries","token":token})
    audit_root=out.parent; audit_root.mkdir(parents=True,exist_ok=False)
    cases=[]
    try:
        for attempt in stage["attempts"]:
            if attempt["action_id"]!="W2_G2_DEV_001_ALTERNATIVE": continue
            row_rel=f"{STAGE_REL}/attempt_{int(attempt['attempt']):02d}_{attempt['action_id']}/row.json"
            real_row=load(ROOT/row_rel)
            original_binding=load(ROOT/attempt["binding_path"])
            action_id=attempt["action_id"]
            mutations:list[tuple[str,str,Callable[[dict[str,Any],dict[str,Any],Path],None]]]=[]
            def source_change(binding:dict[str,Any],record:dict[str,Any],case_dir:Path)->None:
                probe_rel=(case_dir/"probe_source.txt").relative_to(ROOT).as_posix()
                probe=ROOT/probe_rel; probe.write_text("source-before\n",encoding="utf-8")
                binding["source_files"][probe_rel]=sha(probe)
                probe.write_text("source-after\n",encoding="utf-8")
            def input_change(binding:dict[str,Any],record:dict[str,Any],case_dir:Path)->None:
                protocol=load(ROOT/plan["protocol_path"]); protocol["task"]["required_progress_m"]="351/1000"
                mutated=case_dir/"protocol_mutated.json"; dump(mutated,protocol)
                binding["protocol_path"]=mutated.relative_to(ROOT).as_posix()
            def omit_slab(binding:dict[str,Any],record:dict[str,Any],case_dir:Path)->None: record["slabs"]=record["slabs"][:-1]
            def reset_label(binding:dict[str,Any],record:dict[str,Any],case_dir:Path)->None: record["slabs"][128]["center_label_sha256"]="0"*64
            def weaken_inequality(binding:dict[str,Any],record:dict[str,Any],case_dir:Path)->None: record["contact_margin_lower_N"]=str(F(record["contact_margin_lower_N"])+1)
            mutations=[("changed_source","SOURCE_CLOSURE_HASH",source_change),("changed_protocol","FROZEN_PROTOCOL_OR_PROFILE_HASH",input_change),
              ("omitted_last_slab","RECOMPUTED_FIELDS_MISMATCH",omit_slab),("changed_center_label","RECOMPUTED_FIELDS_MISMATCH",reset_label),
              ("inflated_contact_margin","RECOMPUTED_FIELDS_MISMATCH",weaken_inequality)]
            for name,expected_reject,mutate in mutations:
                case_dir=audit_root/name; case_dir.mkdir(parents=True,exist_ok=False)
                binding=json.loads(json.dumps(original_binding)); record=json.loads(json.dumps(real_row))
                binding_rel=(case_dir/"binding.json").relative_to(ROOT).as_posix()
                record_rel=(case_dir/"record.json").relative_to(ROOT).as_posix()
                binding["binding_path"]=binding_rel
                mutate(binding,record,case_dir)
                dump(ROOT/binding_rel,binding)
                record["binding_sha256"]=sha(ROOT/binding_rel)
                dump(ROOT/record_rel,record)
                command=[sys.executable,"-m","validation.autonomous_w2.g2.checker_centered_v6","--binding",binding_rel,"--record",record_rel]
                env=os.environ.copy(); env["PYTHONHASHSEED"]="0"; env["PYTHONUTF8"]="1"
                proc=run_bounded_process(command,cwd=ROOT,wall_seconds=60,cpu_seconds=60,memory_bytes=1073741824,max_processes=1,
                  stdout_limit_bytes=8388608,stderr_limit_bytes=1048576,environment=env)
                ev=result_to_json(proc); dump(case_dir/"checker.job.json",ev)
                job=ev; stdout=base64.b64decode(((job.get("stdout") or {}).get("prefix_base64","")))
                stderr=base64.b64decode(((job.get("stderr") or {}).get("prefix_base64","")))
                (case_dir/"checker.stdout.bin").write_bytes(stdout); (case_dir/"checker.stderr.bin").write_bytes(stderr)
                try: parsed=json.loads(stdout.decode("utf-8").strip())
                except BaseException: parsed={}
                rejection=str(parsed.get("rejection",""))
                rejected=(parsed.get("replayed") is False and expected_reject in rejection and job.get("status")=="NONZERO_EXIT")
                case={"name":name,"binding_path":binding_rel,"binding_sha256":sha(ROOT/binding_rel),"record_path":record_rel,
                  "record_sha256":sha(ROOT/record_rel),"expected_rejection_class":expected_reject,"actual_rejection":rejection,
                  "job_status":job.get("status"),"returncode":job.get("returncode"),
                  "elapsed_seconds_display_only":job.get("elapsed_seconds_display_only"),
                  "peak_memory_bytes":(job.get("job") or {}).get("peak_memory_bytes"),"rejected":rejected}
                dump(case_dir/"case_receipt.json",case); cases.append(case)
        all_rejected=len(cases)==5 and all(x["rejected"] for x in cases)
        report={"schema":"G2_W2_CENTERED_V6_MUTATION_AUDIT_v2","session":"DDWMR | LUNA-G2-SCOPE",
          "status":"PASS" if all_rejected else "FAIL","completed_utc":now(),"release_path":"coordination/autonomous_w2/g2/releases/RELEASE_v6.json",
          "release_sha256":sha(ROOT/"coordination/autonomous_w2/g2/releases/RELEASE_v6.json"),"base_action_id":action_id,
          "base_record_path":row_rel,"base_record_sha256":sha(ROOT/row_rel),"mutation_count":len(cases),"cases":cases,
          "all_required_mutations_rejected":all_rejected,"native_attempts_added":0,"held_out_rows":0,"legacy_800_row_study":"NOT_RUN",
          "limits_per_checker_replay":{"wall_seconds":60,"memory_bytes":1073741824,"processes":1},
          "shared_checker_and_interval_arithmetic_disclosed":True}
        dump(out,report)
        return report
    finally:
        try:
            if load(lock_path).get("token")==token: lock_path.unlink()
        except FileNotFoundError: pass

if __name__=="__main__": print(json.dumps(main(),sort_keys=True,indent=2))
