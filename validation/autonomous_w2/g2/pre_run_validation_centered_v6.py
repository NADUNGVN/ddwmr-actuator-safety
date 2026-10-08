"""Static/protocol/resource pre-run gate; does not evaluate any protocol action."""
from __future__ import annotations
import hashlib,json,platform,subprocess,sys
from fractions import Fraction as F
from datetime import datetime,timezone
from pathlib import Path
from validation.autonomous_w2.g2 import checker_centered_v6 as checker
from validation.autonomous_w2.g2 import producer_centered_v6 as producer
from validation.autonomous_w2.g2.rational_interval_v3 import I,configure_fixed_grid,configure_integer_string_limit

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/"results/validation/autonomous_w2/g2/pre_run_validation_centered_v6_v3.json"
SOURCES=["validation/autonomous_w2/g2/producer_centered_v6.py","validation/autonomous_w2/g2/checker_centered_v6.py",
 "validation/autonomous_w2/g2/run_stage_centered_v6.py","validation/autonomous_w2/g2/freeze_development_centered_v6.py",
 "validation/autonomous_w2/g2/publish_release_centered_v6.py","validation/autonomous_w2/g2/centered_v6_nonquery_fixtures.py",
 "validation/autonomous_w2/g2/pre_run_validation_centered_v6.py"]

def sha(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def main()->dict[str,object]:
    p=json.loads((ROOT/"research/autonomous_w2/g2/task_protocol_v1.json").read_text(encoding="utf-8"))
    prof=json.loads((ROOT/"validation/autonomous_w2/g2/profile_centered_v6.json").read_text(encoding="utf-8"))
    fixture=json.loads((ROOT/"results/validation/autonomous_w2/g2/centered_v6_nonquery_fixtures_v1.json").read_text(encoding="utf-8"))
    screen=json.loads((ROOT/"results/validation/autonomous_w2/g2/centered_error_tube_preflight_v2.json").read_text(encoding="utf-8"))
    status=json.loads((ROOT/"coordination/autonomous_w2/g2/STATUS.json").read_text(encoding="utf-8"))
    branch=subprocess.run(["git","branch","--show-current"],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()
    head=subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()
    configure_integer_string_limit(5000,16384); configure_fixed_grid(96,16384,20)
    synthetic=[[I.point(0) for _ in range(7)] for _ in range(6)]; synthetic_center=[[I.point(0) for _ in range(7)] for _ in range(6)]
    for i in range(6): synthetic[i][i]=I.point(-2); synthetic_center[i][i]=I.point(-2)
    synthetic[0][0]=I(F(-11,10),F(-9,10)); synthetic_center[0][0]=I.point(-1)
    synthetic[1][1]=I.point(F(3,2)); synthetic_center[1][1]=I.point(F(7,5))
    synthetic[2][6]=I.point(F(1,4)); synthetic[3][3]=I.point(F(7,5)); synthetic_center[3][3]=I.point(F(7,5)); synthetic_center[3][6]=I.point(F(2,5))
    producer_bounds=producer._parameter_bounds(synthetic,synthetic_center)
    checker_bounds=checker._matrix_bounds(synthetic,synthetic_center)
    producer_center=producer._center_matrix((F(1,2),F(1,2)))
    checker_center=checker._center_matrix(F(1,2))
    helper_parity=producer_bounds==checker_bounds and producer_center==checker_center
    checks={
      "task_protocol_frozen_development_only":p.get("protocol_state")=="FROZEN_FOR_DEVELOPMENT_NOT_CONFIRMATION",
      "task_has_three_ordered_actions":[a.get("id") for a in p.get("actions",[]) ]==["W2_G2_DEV_001_ZERO","W2_G2_DEV_001_NOMINAL","W2_G2_DEV_001_ALTERNATIVE"],
      "task_domain_positive_width":F(p["model"]["fixed_label_bounds"][0])>0 and F(p["model"]["fixed_label_bounds"][0])<F(p["model"]["fixed_label_bounds"][1]) and all(F(cell[0])<F(cell[1]) for cell in p["task"]["initial_box"]),
      "profile_full_hold_partition":prof.get("center_time_slabs")==256 and prof.get("center_slab_duration_s")=="1/128",
      "profile_worker_caps":prof.get("worker_wall_cap_seconds")==60 and prof.get("worker_memory_cap_bytes")==1073741824 and prof.get("worker_process_cap")==1,
      "profile_phase_cap":prof.get("phase_wall_cap_seconds")==7200,
      "nonquery_fixtures_pass":fixture.get("status")=="PASS" and fixture.get("native_attempts_added")==0 and fixture.get("actual_protocol_action_rows_evaluated")==0,
      "independent_feasibility_screen_supports_distinction":screen.get("prospective_task_rule_possible") is True and screen.get("all_actions_center_safe_clip_contact") is True,
      "producer_checker_synthetic_matrix_parity":helper_parity,
      "native_budget_exactly_three_remaining":status.get("native_attempts",{}).get("count_completed")==21 and status.get("native_attempts",{}).get("remaining_attempts")==3,
      "correct_branch_and_head":branch=="main" and head=="94c60f627a2ce1a8d52101050bdc0ce9d2e59afe",
      "compute_lock_available":not (ROOT/"coordination/autonomous_w2/COMPUTE.lock").exists(),
    }
    compile_ok=True; compile_errors=[]
    for rel in SOURCES:
        try: compile((ROOT/rel).read_text(encoding="utf-8-sig"),rel,"exec")
        except BaseException as exc: compile_ok=False; compile_errors.append(f"{rel}:{type(exc).__name__}:{exc}")
    checks["source_compile"] = compile_ok
    report={"schema":"G2_W2_CENTERED_V6_PRE_RUN_VALIDATION_v1","session":"DDWMR | LUNA-G2-SCOPE",
      "status":"PASS" if all(checks.values()) else "FAIL","checked_utc":datetime.now(timezone.utc).isoformat(),
      "checks":checks,"compile_errors":compile_errors,"source_sha256":{rel:sha(ROOT/rel) for rel in SOURCES},
      "repository":{"branch":branch,"head":head},"python":sys.version,"platform":platform.platform(),
      "native_attempts_before_stage":21,"remaining_native_attempts":3,"attempts_run_by_preflight":0,
      "held_out_rows":0,"legacy_800_row_study":"800/800 NOT_RUN",
      "limitation":"This pre-run gate and the prior exact feasibility screen are not a full-hold row certificate; the frozen worker/checker stage is still required."}
    if OUT.exists(): raise FileExistsError("PRE_RUN_OUTPUT_ALREADY_EXISTS")
    OUT.write_text(json.dumps(report,sort_keys=True,indent=2,ensure_ascii=True)+"\n",encoding="utf-8")
    return report

if __name__=="__main__": print(json.dumps(main(),sort_keys=True,indent=2))
