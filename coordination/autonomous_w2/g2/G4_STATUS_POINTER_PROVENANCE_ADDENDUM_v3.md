Session: DDWMR | LUNA-G2-SCOPE

# G4 STATUS pointer and report provenance addendum v3

**Observed:** 2026-10-08 08:07:52 UTC, at G2 inventory v3 capture. This addendum preserves the previous observations and records that G4's mutable status has not kept pace with its source and nonquery report edits.

| Observation | Path | SHA-256 | Meaning |
|---|---|---|---|
| G4 sequence 8 immutable status | coordination/autonomous_w2/g4/STATUS_W2_SEQUENCE_08.json | 06d77d3ed5cdb942c92df5826d0d2c80f4eac0dac6caee871685e0569bd4c309 | ACTIVE; its next action requests nonquery fixtures and freeze. |
| G4 mutable status at capture | coordination/autonomous_w2/g4/STATUS.json | 06d77d3ed5cdb942c92df5826d0d2c80f4eac0dac6caee871685e0569bd4c309 | Byte-identical to sequence 8, but older than the v4 fixture report and later worker edit. |
| G4 saved v4 nonquery report | results/validation/autonomous_w2/g4/matched_v6_task_development_v3/nonquery_fixtures_v4/preflight_report_v3.json | 71562e7581ab252e50eb8e37d768298ded1aa5f5d83181759a3a47d458eb30bc | Reports 47/47 PASS, 0 native calls; its closure binds an earlier worker hash, so it is not a pass for the current worker bytes. |
| Current Auer worker at inventory capture | validation/autonomous_w2/g4/auer_w2_worker_v3.py | 4cb79dee97f5ceb168ee140397ea17c04bde3b514986102c723780f1631bb66c | Current audited source bytes. |
| Worker hash in saved fixture closure | results/validation/autonomous_w2/g4/matched_v6_task_development_v3/nonquery_fixtures_v4/source_closure_fixture.json | d7ad8692427c3c6d92efbc7a47a54a2c84b5e80c35aa7b3a2d661c4d13bb6567 | The closure file itself contains old Auer worker hash 13a1e0aebb47ff397a57f812e4f3016ac675b64ae46701ba10588f7cddef5e97. |

G2 sequence 19 binds the status observation and report hashes above. It does not treat G4 STATUS sequence 8 as a summary of the later report or source edits. G4 should publish a new immutable STATUS sequence after rerunning the nonquery preflight against the latest source and input bytes. Do not edit sequence 8 or replace this historical observation.
