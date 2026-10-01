# Codex review — G4 Auer R5 stored-artifact composition replay

**Date:** 2026-10-01  
**Branch / HEAD:** `luna/g2-validation-v1` / `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_R5_COMPOSITION_REPLAY_FULL_HANDOFF.md`  
**Frozen R5 source:** `results/validation/g4/auer2013/r5_composition_replay_v1/source_snapshot_v11`  
**Snapshot manifest SHA-256:** `d6ed85d98f630889912e30baaf00314ac4069c4dc846525c639832c64ff959eb`  
**R5 artifact registry SHA-256:** `48196f1f3ebb5cf9787c68bc98f6ad88a0678ebd92683014fe877d015f18dd44`

MASTER v2.1 remains authoritative. This is a read-only source, ledger, and artifact-integrity review. I did not rerun the IVP producer, native proof checker, R5 verifier, mutation runner, or matched batch. No commit, push, gate edit, or MASTER edit was made.

## Disposition

**ACCEPT R5 for the frozen single R4 DDWMR composition.** The stored-artifact verifier closes the specific R4 audit gap: it checks the proof from disk, derives the common tube and predicate again, and compares the complete saved common and composition records to independently reconstructed expectations. The 17 recorded file-based mutations were rejected in their declared layers. This is a reproducible one-case artifact replay, with disclosed shared arithmetic; it is not a general Auer baseline result.

The two pre-freeze snapshot-assembly failures have an explicit **provenance gap**: their transient source bytes and raw stdout were not saved. The gap concerns setup attempts before the v11 freeze, not a proof or predicate execution. It must remain visible and must not be retroactively described as a complete attempt ledger.

**Research status:** **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical-platform correspondence UNVERIFIED.** Matched batch: **0/1,944**.

## 1. Artifact and source integrity

**Finding.** The reported final files are intact under their stated manifests.

**Evidence.** I recomputed sizes and SHA-256 hashes for **88/88** R5 registry artifacts, **726/726** v11 source-snapshot members, **720/720** v10 members, and **34/34** R4 output-manifest artifacts; all matched. The v11 manifest and R5 registry hashes equal the handoff values. The R5 ledger hash is `fb319214ea01503108427e4e0925b6cac14d26ffa05a532d50f0052ced5eb4fb`. The v11 pre/post integrity reports record PASS. The v11 snapshot includes eight listed Python `.pyc` files inherited from v10; I compared their marshalled code objects with freshly compiled corresponding source under the frozen Python 3.12 runtime, and all eight matched. This static comparison did not run the IVP or verifier.

**Consequence.** The final R5 run can be tied to stable code, input and output bytes. The integrity result does not fill missing logs for the earlier setup failures.

**Status:** VALID for final artifact integrity.

**Required action:** Preserve v10/v11 and R4/R5 manifests as immutable evidence. Retain the declared pre-freeze provenance gap.

## 2. Stored proof to common predicate

**Finding.** The R5 verifier rebuilds the expected common result from the replayed native proof, rather than comparing a stored dictionary against itself.

**Evidence.** `verify_auer_composition_replay_v1.py` verifies the v11 and v10 snapshot members, all 34 R4 output artifacts, the selected input/benchmark/profile/method/backend hashes, runtime identity and proof bindings. It parses the stored native proof and calls `replay_native_proof` using the frozen case, 21-coordinate model and source/profile binding. Only after replay succeeds does it form each `TubeSegment` from the proof's accepted full-time hull and separate endpoints. It supplies all twelve original fixed-label intervals, sets `NATIVE_TOTAL_HULL` with expansion count zero, and calls `check_tube_segments` on the full `[0,1/50]` hold. It then compares the entire recomputed common record with the saved common record, constructs a new expected composition from the replayed proof and recomputed common result, and compares every stored composition field. The pristine report records native replay PASS, one segment, common `PASS_ON_SUPPLIED_TUBE`, composition PASS, 39,081 native-replay and 2,415 common-predicate rational operations. Its exact positive margins match the R4 evidence.

The verifier uses `replay_ivp.py` and `common_tube.py`; it shares the existing G2 rational/Taylor arithmetic. `certificate_emitted=false` remains explicit, and `ode_tube_proof_replayed=false` remains the **common layer's** flag; native proof replay is reported separately as PASS.

**Consequence.** The R4 same-worker composition now also has a separately executable, stored-artifact replay for this one frozen query. It does not independently validate the shared arithmetic library or establish physical safety.

**Status:** VALID for the restricted stored composition.

**Required action:** Keep the native, common, and composition verdicts distinct in later summaries.

## 3. Mutation evidence

**Finding.** The 17 mutation outcomes test actual stored-artifact copies and reach the verifier's respective proof, predicate, or composition checks.

**Evidence.** The runner writes five changed native-proof copies, six common-record copies, and six composition copies under separate trial directories. Each child command, changed-input hash, verifier report, raw stdout, guard record and expected/actual exit status is in `trial_ledger_v1.json`. All **5/5** native mutations returned `native_proof_failure` (exit 11), **6/6** common mutations returned `common_predicate_mismatch` (exit 12), and **6/6** composition mutations returned `composition_mismatch` (exit 13). The trial details name the first differing proof field or JSON path. Unlike R4's in-memory inequality trials, the R5 verifier derives the expected common/composition values from the saved proof and frozen inputs before comparing a mutated copy.

**Consequence.** The stated classes of tampering are detected by the actual stored-artifact verifier. These finite trials do not prove the verifier complete against every possible corruption.

**Status:** VALID for the declared 17 cases.

**Required action:** Do not call the mutation set an exhaustive formal verification of verifier code.

## 4. Freeze sequence, failed setup, and resources

**Finding.** The final replay was run after source freeze and under a process guard; two earlier snapshot-assembly attempts are incompletely evidenced.

**Evidence.** The v11 creator refuses to overwrite a snapshot and refuses a preexisting R5 replay/trial output before freeze. It copied all v10 manifest-listed members, included six new R5 files, and wrote a 726-member v11 manifest. The pre/post integrity reports and all 18 guarded child records are retained. The pristine child reports process-memory cap installed before resume, exit 0, about 1.172 seconds and peak 19,726,336 bytes; the handoff reports a maximum 20,291,584 bytes across the 18 children, versus a 1,024 MiB cap and 120-second deadline. The two prior attempts in `pre_freeze_setup_attempts_v1.json` report `v10 snapshot file set mismatch` before target creation and before verifier execution. Their transient creator-source hashes and original stdout were not retained, so their exact source provenance cannot be reconstructed independently.

**Consequence.** The missing transient setup records do not contradict the verified final v11 replay, but they limit any claim that *every* development attempt has full raw provenance. Runtime evidence applies to one replay plus mutations, not 1,944 comparable IVPs.

**Status:** VALID final freeze/run evidence; PARTIAL historical provenance for two setup checks.

**Required action:** Keep the failed-attempt disclosure unchanged. Do not infer full-grid throughput from the one-case replay.

## Next scientific review

R5 removes the stored-composition replay gap identified in the R4 Codex review. Before any matched-batch run, obtain an independent source-level scientific review of the Auer 2013 / Rauh–Auer 2011 equation-to-code mapping, the interval mean-value and Picard inclusion argument, exact arithmetic dependency, selected-query correspondence, common-predicate composition, and fairness of the frozen G4 matched protocol. The reviewer must receive the actual source, native proof and records; an inaccessible local path or summary is insufficient. A source-backed review bundle and request should require a returned Markdown handoff file.

Even if that review accepts the single case, G4 remains UNVERIFIED until a matched-assumption comparison is completed and interpreted without turning UNKNOWN into failure or claiming generic validated integration as novel. No G3 construction or physical-platform claim follows from R5.
