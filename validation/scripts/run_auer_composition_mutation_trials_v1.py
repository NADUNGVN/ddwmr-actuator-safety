"""Create hash-bound stored-artifact trials and run the frozen R5 verifier."""
from __future__ import annotations
import argparse, copy, hashlib, json, os, subprocess, sys
from pathlib import Path

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
PROJECT = Path(__file__).resolve().parents[2]
if str(PROJECT) not in sys.path: sys.path.insert(0, str(PROJECT))
from validation.baselines.auer2013.process_limiter import _run_guarded
from validation.baselines.auer2013.replay_ivp import canonical_sha256

PROFILE_REL = Path("validation/configs/auer_r5_composition_replay_profile_v1.json")
VERIFIER_REL = Path("validation/scripts/verify_auer_composition_replay_v1.py")
PROOF_NAME = "r4_ddwmr_single_query_native_v2.json"
EVIDENCE_NAME = "r4_ddwmr_single_query_evidence_v2.json"
OUTPUT_MANIFEST_NAME = "r4_output_artifact_manifest_v1.json"
DEFAULT_COMMON = Path("inputs/r4_common_check_v2.json")
DEFAULT_COMPOSITION = Path("inputs/r4_composition_v1.json")

def sha_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path: Path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes((json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+"\n").encode("utf-8"))

def canonical_file(path: Path, value) -> str:
    write_json(path,value); return sha_file(path)

def set_field_proof_digest(envelope):
    envelope["proof_sha256"] = canonical_sha256(envelope["proof"])

def verify_r4_final(workspace: Path, profile: dict):
    base=workspace/"results/validation/g4/auer2013"
    manifest_path=base/OUTPUT_MANIFEST_NAME
    expected=profile["frozen_sha256"]["r4_output_artifact_manifest"]
    if sha_file(manifest_path)!=expected: raise RuntimeError("R4 output manifest changed before final audit")
    manifest=read_json(manifest_path)
    count=0
    for item in manifest["artifacts"]:
        p=(base/item["path"]).resolve()
        if base.resolve() not in p.parents: raise RuntimeError("R4 manifest path escaped artifact root")
        if not p.is_file() or p.stat().st_size!=item["bytes"] or sha_file(p)!=item["sha256"]:
            raise RuntimeError(f"R4 final artifact mismatch: {item['path']}")
        count+=1
    v10=base/"source_snapshot_v10"
    v10_manifest_path=v10/"snapshot_manifest.json"
    if sha_file(v10_manifest_path)!=profile["frozen_sha256"]["r4_source_snapshot_v10_manifest"]:
        raise RuntimeError("v10 manifest changed during R5")
    v10_manifest=read_json(v10_manifest_path)
    for item in v10_manifest["members"]:
        p=(v10/item["snapshot_relative_path"]).resolve()
        if v10.resolve() not in p.parents or not p.is_file() or p.stat().st_size!=item["bytes"] or sha_file(p)!=item["sha256"]:
            raise RuntimeError(f"v10 final member mismatch: {item['snapshot_relative_path']}")
    original_proof=base/PROOF_NAME
    original_evidence=base/EVIDENCE_NAME
    return {
        "status":"PASS",
        "r4_output_artifact_count":count,
        "v10_snapshot_member_count":len(v10_manifest["members"]),
        "r4_output_manifest_sha256":sha_file(manifest_path),
        "v10_manifest_sha256":sha_file(v10_manifest_path),
        "r4_native_proof_sha256_after":sha_file(original_proof),
        "r4_evidence_sha256_after":sha_file(original_evidence),
        "matched_query_evaluations":manifest["matched_query_evaluations"],
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace-root",type=Path,required=True)
    p.add_argument("--r5-artifact-root",type=Path,required=True)
    p.add_argument("--r5-snapshot",type=Path,required=True)
    p.add_argument("--r5-snapshot-manifest-sha256",required=True)
    p.add_argument("--trial-only",action="store_true")
    a=p.parse_args()
    workspace=a.workspace_root.resolve()
    root=a.r5_artifact_root.resolve()
    snapshot=a.r5_snapshot.resolve()
    project=snapshot/"project"
    profile_path=project/PROFILE_REL
    verifier=project/VERIFIER_REL
    profile=read_json(profile_path)
    manifest_path=snapshot/"snapshot_manifest.json"
    if sha_file(manifest_path)!=a.r5_snapshot_manifest_sha256:
        raise RuntimeError("R5 snapshot manifest hash mismatch")
    frozen_manifest=read_json(manifest_path)
    frozen_members={item["snapshot_relative_path"]:item for item in frozen_manifest["members"]}
    for rel,path in (("project/"+PROFILE_REL.as_posix(),profile_path),
                     ("project/"+VERIFIER_REL.as_posix(),verifier),
                     ("project/validation/scripts/run_auer_composition_mutation_trials_v1.py",Path(__file__).resolve())):
        if rel not in frozen_members or sha_file(path)!=frozen_members[rel]["sha256"]:
            raise RuntimeError(f"R5 snapshot member hash mismatch: {rel}")
    r4=workspace/"results/validation/g4/auer2013"
    v10_manifest=read_json(r4/"source_snapshot_v10/snapshot_manifest.json")
    v10_member={item["snapshot_relative_path"]:item for item in v10_manifest["members"]}.get(
        "project/validation/baselines/auer2013/process_limiter.py")
    limiter_active=PROJECT/"validation/baselines/auer2013/process_limiter.py"
    limiter_frozen=project/"validation/baselines/auer2013/process_limiter.py"
    if not v10_member or sha_file(limiter_active)!=v10_member["sha256"] or sha_file(limiter_frozen)!=v10_member["sha256"]:
        raise RuntimeError("R5 process guard source differs from frozen v10 launcher")
    trial_root=root/"trials"
    trial_root.mkdir(parents=True,exist_ok=True)
    evidence_path=r4/EVIDENCE_NAME
    original_proof_path=r4/PROOF_NAME
    common_default=root/DEFAULT_COMMON
    composition_default=root/DEFAULT_COMPOSITION
    inputs={
        "native_proof":read_json(original_proof_path),
        "common_record":read_json(common_default),
        "composition":read_json(composition_default),
    }
    originals={
        "native_proof":sha_file(original_proof_path),
        "common_record":sha_file(common_default),
        "composition":sha_file(composition_default),
    }
    proof_trials=[]
    def proof_edit(label, edit):
        item=copy.deepcopy(inputs["native_proof"])
        edit(item)
        set_field_proof_digest(item)
        proof_trials.append((label,"native_proof",item,"native_proof_failure"))
    proof_edit("total_hull",lambda x:x["proof"]["step_records"][0]["full_time_total_hull_augmented"][0][0].__setitem__("num","999"))
    proof_edit("residual_iterate",lambda x:x["proof"]["step_records"][0]["residual_iterations"][0]["new_residual_derivative"][0][0].__setitem__("num","999"))
    proof_edit("endpoint",lambda x:x["proof"]["global_endpoint"][0][0].__setitem__("num","999"))
    proof_digest=copy.deepcopy(inputs["native_proof"])
    proof_digest["proof_sha256"]="0"*64
    proof_trials.append(("proof_digest","native_proof",proof_digest,"native_proof_failure"))
    proof_edit("action",lambda x:x["proof"]["query_action_binding"]["held_voltage"][0].__setitem__("num","-2"))

    common_trials=[]
    def common_edit(label, edit):
        item=copy.deepcopy(inputs["common_record"]); edit(item)
        common_trials.append((label,"common_record",item,"common_predicate_mismatch"))
    common_edit("segment_hull",lambda x:x["segments"][0]["state_hull"][0][0].__setitem__("num","999"))
    common_edit("endpoint",lambda x:x["segments"][0]["endpoint_end"]["state_hull"][0][0].__setitem__("num","999"))
    common_edit("radius_mode",lambda x:x["segments"][0].__setitem__("radius_expansion_mode","CENTER_PLUS_RESIDUAL_ONCE"))
    common_edit("radius_count",lambda x:x["segments"][0].__setitem__("radius_expansion_count",1))
    common_edit("exact_margin",lambda x:x["segment_checks"][0]["contact"]["margin_lower"].__setitem__("num","0"))
    common_edit("segment_hash",lambda x:x.__setitem__("segments_sha256","0"*64))

    composition_trials=[]
    def composition_edit(label,edit):
        item=copy.deepcopy(inputs["composition"]); edit(item)
        composition_trials.append((label,"composition",item,"composition_mismatch"))
    composition_edit("proof_digest",lambda x:x.__setitem__("native_proof_sha256","0"*64))
    composition_edit("common_check_digest",lambda x:x.__setitem__("common_check_sha256","0"*64))
    composition_edit("segment_digest",lambda x:x.__setitem__("segments_sha256","0"*64))
    composition_edit("query_id",lambda x:x.__setitem__("query_id","tampered-query"))
    composition_edit("held_action",lambda x:x["held_voltage"][0].__setitem__("num","0"))
    composition_edit("source_snapshot_digest",lambda x:x.__setitem__("source_snapshot_manifest_sha256","0"*64))
    trials=proof_trials+common_trials+composition_trials
    if len(proof_trials)!=5 or len(common_trials)!=6 or len(composition_trials)!=6:
        raise RuntimeError("trial matrix does not contain the frozen 5+6+6 mutations")

    verifier_sha=sha_file(verifier)
    commands=[]
    def execute(name, expected_reason=None, changed=None):
        trial_dir=trial_root/name
        trial_dir.mkdir(parents=True,exist_ok=False)
        proof_path=original_proof_path
        common_path=common_default
        composition_path=composition_default
        if changed:
            label,kind,value,_=changed
            filename=f"{kind}.json"
            copy_path=trial_dir/filename
            trial_input_sha=canonical_file(copy_path,value)
            if kind=="native_proof": proof_path=copy_path
            elif kind=="common_record": common_path=copy_path
            elif kind=="composition": composition_path=copy_path
            changed_record={
                "artifact_kind":kind,"mutation":label,
                "original_input_sha256":originals[kind],
                "trial_input_sha256":trial_input_sha,
                "trial_input_path":str(copy_path.resolve()),
            }
        else:
            trial_input_sha=None
            changed_record=None
        report_path=(root/"pristine_replay_report.json") if name=="pristine_replay" else trial_dir/"verifier_report.json"
        stdout_path=(root/"pristine_replay_stdout.log") if name=="pristine_replay" else trial_dir/"verifier_stdout.log"
        guard_path=(root/"pristine_replay_resource_guard.json") if name=="pristine_replay" else trial_dir/"resource_guard.json"
        args=[
            str(sys.executable),str(verifier),
            "--workspace-root",str(workspace),
            "--project-root",str(project),
            "--r5-snapshot",str(snapshot),
            "--r5-snapshot-manifest-sha256",a.r5_snapshot_manifest_sha256,
            "--r5-profile",str(profile_path),
            "--r5-artifact-root",str(root),
            "--v10-snapshot",str(r4/"source_snapshot_v10"),
            "--r4-output-root",str(r4),
            "--r4-output-manifest",str(r4/OUTPUT_MANIFEST_NAME),
            "--case-input",str(project/profile["project_paths"]["selected_case_input"]),
            "--benchmark",str(project/profile["project_paths"]["benchmark"]),
            "--resource-profile",str(project/profile["project_paths"]["r4_resource_profile"]),
            "--method-contract",str(project/profile["project_paths"]["method_contract"]),
            "--backend-manifest",str(project/profile["project_paths"]["arithmetic_backend_manifest"]),
            "--native-proof",str(proof_path),
            "--r4-evidence",str(evidence_path),
            "--common-record",str(common_path),
            "--composition",str(composition_path),
            "--report",str(report_path),
        ]
        if changed:
            args += ["--trial-mode","--trial-root",str(trial_root)]
        guard=_run_guarded(command=args,project=project,
                           memory_limit_mib=int(profile["resource_limits"]["memory_limit_mib_per_replay"]),
                           timeout_seconds=int(profile["resource_limits"]["wall_time_seconds_per_replay"]),
                           stdout_path=stdout_path)
        guard_record={**guard,"guard_runner_source_sha256":sha_file(project/"validation/baselines/auer2013/process_limiter.py")}
        write_json(guard_path,guard_record)
        report=None
        if report_path.is_file():
            try: report=read_json(report_path)
            except Exception: report=None
        if report is None:
            report={
                "schema":"ddwmr-g4-auer-composition-replay-report-v1",
                "status":"REJECTED","reason":"resource_limit",
                "detail":"verifier did not complete and emit a replay report under the installed process guard",
                "certificate_emitted":False,"matched_query_evaluations":0,
            }
            write_json(report_path,report)
        expected_status="PASS" if expected_reason is None else "REJECTED"
        outcome_ok=(report.get("status")==expected_status and
                    (expected_reason is None or report.get("reason")==expected_reason) and
                    guard["status"]=="PROCESS_EXITED" and
                    guard.get("worker_exit_code")== (0 if expected_reason is None else {"native_proof_failure":11,"common_predicate_mismatch":12,"composition_mismatch":13}[expected_reason]))
        stdout_sha=sha_file(stdout_path) if stdout_path.is_file() else None
        result={
            "trial_id":name,
            "mutation":changed_record,
            "expected_reason":expected_reason,
            "actual_reason":report.get("reason"),
            "verifier_status":report.get("status"),
            "verifier_detail":report.get("detail"),
            "verifier_report_path":str(report_path.resolve()),
            "verifier_report_sha256":sha_file(report_path),
            "verifier_stdout_path":str(stdout_path.resolve()),
            "verifier_stdout_sha256":stdout_sha,
            "resource_guard_path":str(guard_path.resolve()),
            "resource_guard_sha256":sha_file(guard_path),
            "resource_guard_status":guard["status"],
            "resource_record":guard_record,
            "outcome_pass":outcome_ok,
            "frozen_verifier_sha256":verifier_sha,
            "command":args,
        }
        if name=="pristine_replay": write_json(root/"pristine_replay_trial_record.json",result)
        return result

    results=[]
    if not a.trial_only:
        results.append(execute("pristine_replay"))
    for label,kind,value,reason in trials:
        trial_name=f"{kind.split('_')[0]}_{label}"
        results.append(execute(trial_name,reason,(label,kind,value,reason)))
    final=verify_r4_final(workspace,profile)
    write_json(root/"final_r4_integrity_check.json",final)
    ledger={
        "schema":"ddwmr-g4-auer-r5-trial-ledger-v1",
        "r5_snapshot_manifest_sha256":a.r5_snapshot_manifest_sha256,
        "r5_profile_sha256":sha_file(profile_path),
        "frozen_verifier_sha256":verifier_sha,
        "mutation_counts":{"native_proof":len(proof_trials),"common_record":len(common_trials),"composition":len(composition_trials)},
        "pristine_replay":next((x for x in results if x["trial_id"]=="pristine_replay"),None),
        "trials":results,
        "final_r4_integrity_check":final,
        "matched_query_evaluations":0,
        "all_expected_outcomes_pass":all(x["outcome_pass"] for x in results) and final["status"]=="PASS",
    }
    write_json(root/"trial_ledger_v1.json",ledger)
    print(json.dumps({"pristine":ledger["pristine_replay"]["verifier_status"] if ledger["pristine_replay"] else "NOT_RUN",
                      "trials":len(trials),"all_expected_outcomes_pass":ledger["all_expected_outcomes_pass"],
                      "ledger":str((root/"trial_ledger_v1.json").resolve())},sort_keys=True))
    return 0 if ledger["all_expected_outcomes_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
