"""Freeze R5 verifier, profile and protocol as source snapshot v11."""
from __future__ import annotations
import hashlib, json, shutil, subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"results/validation/g4/auer2013"
PREVIOUS=BASE/"source_snapshot_v10"
SNAPSHOT=BASE/"r5_composition_replay_v1/source_snapshot_v11"
EXPECTED_BRANCH="luna/g2-validation-v1"
EXPECTED_HEAD="aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46"
EXPECTED_V10_SHA="29ca0f22791ccc740ef377b232522dee88bbaf00367213bfc45cc07925c5bcd5"
EXPECTED_R4_OUTPUT_SHA="6a8d5501972cbb1351cb9ea09500427cb37f8b30c37673ee9e573e156ab6b1a7"
NEW_MEMBERS=[
    "validation/configs/auer_r5_composition_replay_profile_v1.json",
    "validation/baselines/auer2013/R5_COMPOSITION_REPLAY_PROTOCOL_v1.md",
    "validation/scripts/verify_auer_composition_replay_v1.py",
    "validation/scripts/run_auer_composition_mutation_trials_v1.py",
    "validation/scripts/verify_auer_source_snapshot_v11.py",
    "validation/scripts/create_auer_source_snapshot_v11.py",
]

def sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()

def check_manifest(root:Path, expected_sha:str):
    mf=root/"snapshot_manifest.json"; side=root/"snapshot_manifest.sha256"
    raw=mf.read_bytes(); actual=hashlib.sha256(raw).hexdigest()
    if actual!=expected_sha or side.read_text(encoding="ascii").split()[0]!=actual:
        raise SystemExit("v10 snapshot manifest/sidecar binding mismatch")
    manifest=json.loads(raw)
    members={i["snapshot_relative_path"]:i for i in manifest["members"]}
    actual_files={p.relative_to(root).as_posix() for p in root.rglob("*")
                  if p.is_file() and p.name not in {"snapshot_manifest.json","snapshot_manifest.sha256"}}
    extras=actual_files-set(members)
    unlisted_noncache={rel for rel in extras if "__pycache__" not in Path(rel).parts and Path(rel).suffix!=".pyc"}
    if set(members)-actual_files or unlisted_noncache or len(members)!=manifest["member_count"]:
        raise SystemExit("v10 snapshot file set mismatch")
    for rel,item in members.items():
        p=root/rel
        if not p.is_file() or p.stat().st_size!=item["bytes"] or sha(p)!=item["sha256"]:
            raise SystemExit(f"v10 snapshot member mismatch: {rel}")
    return manifest,members

def main():
    if SNAPSHOT.exists(): raise SystemExit(f"refusing to overwrite snapshot: {SNAPSHOT}")
    if subprocess.run(["git","branch","--show-current"],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()!=EXPECTED_BRANCH:
        raise SystemExit("unexpected Git branch")
    if subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()!=EXPECTED_HEAD:
        raise SystemExit("unexpected Git HEAD")
    v10,previous_members=check_manifest(PREVIOUS,EXPECTED_V10_SHA)
    if len(previous_members)!=720: raise SystemExit("unexpected v10 member count")
    profile_path=ROOT/"validation/configs/auer_r5_composition_replay_profile_v1.json"
    profile=json.loads(profile_path.read_text(encoding="utf-8"))
    if profile.get("status")!="FROZEN_BEFORE_FIRST_R5_REPLAY": raise SystemExit("R5 profile is not frozen")
    r5=BASE/"r5_composition_replay_v1"
    if not (r5/"inputs/r4_common_check_v2.json").is_file() or not (r5/"inputs/r4_composition_v1.json").is_file():
        raise SystemExit("extracted R4 common/composition inputs are missing")
    if (r5/"trials").exists() or (r5/"pristine_replay_report.json").exists():
        raise SystemExit("an R5 verifier replay/trial exists before source freeze")
    output_manifest_path=BASE/"r4_output_artifact_manifest_v1.json"
    if sha(output_manifest_path)!=EXPECTED_R4_OUTPUT_SHA: raise SystemExit("R4 output manifest hash changed")
    output_manifest=json.loads(output_manifest_path.read_text(encoding="utf-8"))
    for item in output_manifest["artifacts"]:
        path=BASE/item["path"]
        if not path.is_file() or path.stat().st_size!=item["bytes"] or sha(path)!=item["sha256"]:
            raise SystemExit(f"R4 output changed before R5 freeze: {item['path']}")
    evidence=json.loads((BASE/"r4_ddwmr_single_query_evidence_v2.json").read_text(encoding="utf-8"))
    common=json.loads((r5/"inputs/r4_common_check_v2.json").read_text(encoding="utf-8"))
    composition=json.loads((r5/"inputs/r4_composition_v1.json").read_text(encoding="utf-8"))
    if common!=evidence["common_predicate_check"] or composition!=evidence["typed_proof_to_common_composition"]:
        raise SystemExit("extracted R5 inputs differ from their R4 evidence members")
    fixed_files={
        "r4_source_snapshot_v10_manifest":PREVIOUS/"snapshot_manifest.json",
        "r4_output_artifact_manifest":output_manifest_path,
        "selected_case_input":ROOT/profile["project_paths"]["selected_case_input"],
        "benchmark":ROOT/profile["project_paths"]["benchmark"],
        "r4_resource_profile":ROOT/profile["project_paths"]["r4_resource_profile"],
        "method_contract":ROOT/profile["project_paths"]["method_contract"],
        "arithmetic_backend_manifest":ROOT/profile["project_paths"]["arithmetic_backend_manifest"],
        "r4_native_proof_file":BASE/"r4_ddwmr_single_query_native_v2.json",
        "r4_evidence":BASE/"r4_ddwmr_single_query_evidence_v2.json",
        "r5_common_record_copy":r5/"inputs/r4_common_check_v2.json",
        "r5_composition_copy":r5/"inputs/r4_composition_v1.json",
    }
    for name,path in fixed_files.items():
        if sha(path)!=profile["frozen_sha256"][name]:
            raise SystemExit(f"profile frozen hash mismatch before v11: {name}")

    SNAPSHOT.mkdir(parents=True)
    for folder in ("project","environment","runs"):
        shutil.copytree(PREVIOUS/folder,SNAPSHOT/folder)
    v10_listed=set(previous_members)
    for copied in SNAPSHOT.rglob("*"):
        if not copied.is_file() or copied.name in {"snapshot_manifest.json","snapshot_manifest.sha256"}:
            continue
        rel=copied.relative_to(SNAPSHOT).as_posix()
        if rel not in v10_listed and ("__pycache__" in copied.parts or copied.suffix==".pyc"):
            copied.unlink()
    for relative in NEW_MEMBERS:
        source=ROOT/relative
        if not source.is_file(): raise SystemExit(f"R5 frozen member missing: {relative}")
        target=SNAPSHOT/"project"/relative
        if target.exists(): raise SystemExit(f"R5 source path already exists in v10: {relative}")
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)

    branch=subprocess.run(["git","branch","--show-current"],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()
    revision=subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()
    status=subprocess.run(["git","status","--short"],cwd=ROOT,check=True,capture_output=True,text=True).stdout.splitlines()
    members=[]
    for path in sorted(p for p in SNAPSHOT.rglob("*") if p.is_file()):
        if path.name in {"snapshot_manifest.json","snapshot_manifest.sha256"}: continue
        members.append({"snapshot_relative_path":path.relative_to(SNAPSHOT).as_posix(),
                        "bytes":path.stat().st_size,"sha256":sha(path)})
    manifest={
        "schema":"ddwmr-g4-auer-local-source-snapshot-v11",
        "status":"R5_COMPOSITION_REPLAY_SOURCE_FROZEN_BEFORE_FIRST_REPLAY",
        "created_utc":datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_git_revision":revision,"branch":branch,
        "worktree_status_at_snapshot":status,"source_tree_clean":not bool(status),
        "previous_snapshot_manifest_sha256":EXPECTED_V10_SHA,
        "previous_snapshot_member_count_verified":len(previous_members),
        "pre_snapshot_r5_verifier_replays":0,
        "pre_snapshot_r5_mutation_trials":0,
        "matched_query_evaluations":0,
        "member_count":len(members),"members":members,
        "manifest_hash_semantics":"SHA-256 over exact UTF-8 bytes of this indented sorted-key JSON plus one LF; manifest and sidecar are excluded.",
    }
    raw=(json.dumps(manifest,indent=2,sort_keys=True,ensure_ascii=False)+"\n").encode("utf-8")
    (SNAPSHOT/"snapshot_manifest.json").write_bytes(raw)
    digest=hashlib.sha256(raw).hexdigest()
    (SNAPSHOT/"snapshot_manifest.sha256").write_text(f"{digest}  snapshot_manifest.json\n",encoding="ascii",newline="\n")
    print(json.dumps({"snapshot":str(SNAPSHOT.resolve()),"manifest_sha256":digest,"member_count":len(members),
                      "previous_v10_manifest_sha256":EXPECTED_V10_SHA,
                      "pre_snapshot_r5_replays":0,"pre_snapshot_mutation_trials":0},sort_keys=True))
    return 0

if __name__=="__main__": raise SystemExit(main())
