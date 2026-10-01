"""Verify every file in frozen Auer source snapshot v11."""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

PREVIOUS_V10_SHA256 = "29ca0f22791ccc740ef377b232522dee88bbaf00367213bfc45cc07925c5bcd5"
SCHEMA = "ddwmr-g4-auer-local-source-snapshot-v11"

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--snapshot",type=Path,required=True)
    p.add_argument("--expected-manifest-sha256",required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    root=a.snapshot.resolve()
    manifest_path=root/"snapshot_manifest.json"
    sidecar=root/"snapshot_manifest.sha256"
    mismatches=[]
    manifest_sha=sha(manifest_path) if manifest_path.is_file() else None
    if manifest_sha!=a.expected_manifest_sha256.lower():
        mismatches.append({"path":"snapshot_manifest.json","reason":"manifest_hash_mismatch","actual":manifest_sha})
    if not sidecar.is_file() or sidecar.read_text(encoding="ascii").split()[0]!=manifest_sha:
        mismatches.append({"path":"snapshot_manifest.sha256","reason":"sidecar_mismatch"})
    manifest=json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
    if manifest.get("schema")!=SCHEMA: mismatches.append({"path":"snapshot_manifest.json","reason":"schema_mismatch"})
    if manifest.get("previous_snapshot_manifest_sha256")!=PREVIOUS_V10_SHA256:
        mismatches.append({"path":"snapshot_manifest.json","reason":"previous_v10_binding_mismatch"})
    members={item["snapshot_relative_path"]:item for item in manifest.get("members",[])}
    if len(members)!=manifest.get("member_count"):
        mismatches.append({"path":"snapshot_manifest.json","reason":"member_count_mismatch"})
    actual={f.relative_to(root).as_posix() for f in root.rglob("*")
            if f.is_file() and f.name not in {"snapshot_manifest.json","snapshot_manifest.sha256"}}
    extras=actual-set(members)
    unlisted_noncache={rel for rel in extras if "__pycache__" not in Path(rel).parts and Path(rel).suffix!=".pyc"}
    if set(members)-actual or unlisted_noncache:
        mismatches.append({"path":"snapshot","reason":"member_set_mismatch",
                           "missing":sorted(set(members)-actual),"extra_noncache":sorted(unlisted_noncache)})
    checked=0
    for rel,item in members.items():
        path=root/rel
        if not path.is_file():
            mismatches.append({"path":rel,"reason":"missing"}); continue
        checked+=1
        actual_hash=sha(path); actual_bytes=path.stat().st_size
        if actual_hash!=item.get("sha256") or actual_bytes!=item.get("bytes"):
            mismatches.append({"path":rel,"reason":"member_hash_or_size_mismatch",
                               "expected_sha256":item.get("sha256"),"actual_sha256":actual_hash,
                               "expected_bytes":item.get("bytes"),"actual_bytes":actual_bytes})
    report={
        "schema":"ddwmr-g4-auer-source-integrity-v11-v1",
        "checked_utc":datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "snapshot_path":str(root),"manifest_sha256":manifest_sha,
        "expected_member_count":len(members),"checked_member_count":checked,
        "mismatch_count":len(mismatches),"mismatches":mismatches,
        "status":"PASS" if not mismatches and checked==len(members) else "FAIL",
    }
    out=a.output.resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps({"status":report["status"],"members":checked,"manifest_sha256":manifest_sha,"output":str(out)},sort_keys=True))
    return 0 if report["status"]=="PASS" else 1

if __name__=="__main__": raise SystemExit(main())
