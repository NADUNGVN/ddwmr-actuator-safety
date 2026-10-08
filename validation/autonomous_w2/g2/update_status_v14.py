from __future__ import annotations
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
coord=ROOT/'coordination/autonomous_w2/g2'
status_path=coord/'STATUS.json'
old=json.loads(status_path.read_text(encoding='utf-8'))
if old.get('sequence') != 13:
    raise RuntimeError('EXPECTED_STATUS_SEQUENCE_13')
if old.get('head') != '94c60f627a2ce1a8d52101050bdc0ce9d2e59afe':
    raise RuntimeError('HEAD_CHANGED')
archive=coord/'STATUS_W2_SEQUENCE_14.json'
if archive.exists():
    raise FileExistsError('SEQUENCE_14_ARCHIVE_EXISTS')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
new_paths=[
'coordination/autonomous_w2/g2/AUDIT_REQUEST_TO_G4_v5_UPDATED.md',
'results/validation/autonomous_w2/g2/development_v5/attempt_03_W2_G2_DEV_001_ALTERNATIVE/mutation_audit_process/mutation_audit_receipt.json',
'results/validation/autonomous_w2/g2/development_v5/attempt_03_W2_G2_DEV_001_ALTERNATIVE/mutation_audit_split_v1/mutation_audit_report.json',
'validation/autonomous_w2/g2/mutation_trial_v5.py',
'validation/autonomous_w2/g2/run_mutation_audit_v5_split.py',
'validation/autonomous_w2/g2/analyze_v5_saved_evidence.py',
'results/validation/autonomous_w2/g2/v5_saved_evidence_summary_v1.json',
'validation/autonomous_w2/g2/centered_error_tube_screen_v1.py',
'results/validation/autonomous_w2/g2/centered_error_tube_preflight_v1.json',
'results/validation/autonomous_w2/g2/centered_error_tube_preflight_v2.json',
'validation/autonomous_w2/g2/update_status_v14.py',
]
for rel in new_paths:
    p=ROOT/rel
    if not p.is_file():
        raise FileNotFoundError(rel)
    old.setdefault('artifacts',{})[rel]=sha(p)
peer_status_path=ROOT/'coordination/autonomous_w2/g4/STATUS.json'
peer_audit_path=ROOT/'coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v1.json'
peer=json.loads(peer_status_path.read_text(encoding='utf-8'))
audit=json.loads(peer_audit_path.read_text(encoding='utf-8'))
old['sequence']=14
old['utc']=datetime.now(timezone.utc).isoformat()
old['phase']='ACTIVE'
old['objective']='Finish exact v5 release audit exchange, complete a sound centered-matrix residual candidate preflight, and use the remaining bounded development attempts only on a frozen viable release.'
old['next_action']='G4 release-scoped audit of v5 is requested in AUDIT_REQUEST_TO_G4_v5_UPDATED.md. Independently finalize the centered residual proof, checker/fixtures, and source-bound v6 preflight; do not consume the last 3 native attempts before its release and deterministic resource checks are frozen.'
old['peer_status_observed']={
    'sequence':peer.get('sequence'),
    'phase':peer.get('phase'),
    'status_path':'coordination/autonomous_w2/g4/STATUS.json',
    'status_sha256':sha(peer_status_path),
    'release_audit_path':'coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v1.json',
    'release_audit_sha256':sha(peer_audit_path),
    'release_audit_decision':audit.get('decision'),
    'release_consumed':peer.get('peer_release_consumed'),
    'observed_utc':datetime.now(timezone.utc).isoformat(),
}
old['blocker']=None
old['native_attempts'].update({'count_completed':21,'remaining_attempts':3,'held_out_rows':0,'legacy_800_row_study':'800/800 NOT_RUN'})
old['working_tree_note']='Shared tree retained. G2 writes remain inside G2-owned W2 prefixes. G4 status/release files were read only.'
raw=(json.dumps(old,sort_keys=True,indent=2)+'\n').encode('utf-8')
archive.write_bytes(raw)
with tempfile.NamedTemporaryFile('wb',delete=False,dir=coord,prefix='STATUS.tmp.') as f:
    f.write(raw); f.flush(); os.fsync(f.fileno()); temp=Path(f.name)
os.replace(temp,status_path)
print(json.dumps({'sequence':old['sequence'],'status_sha256':sha(status_path),'archive_sha256':sha(archive),'peer_sequence':peer.get('sequence'),'peer_decision':audit.get('decision'),'artifacts_added':len(new_paths)},sort_keys=True))
