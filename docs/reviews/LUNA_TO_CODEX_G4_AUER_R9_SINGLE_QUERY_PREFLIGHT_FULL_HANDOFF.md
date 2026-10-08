Session: DDWMR | LUNA-G4-AUER

# G4 Auer R9 single-query matched preflight — full handoff

**Date:** 2026-10-03  
**Repository:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Assignment:** `docs/CODEX_TO_LUNA_G4_AUER_R9_SINGLE_QUERY_PREFLIGHT.md` (SHA-256 `fc697e9cf58d85b4ae66cb10fec09230ff602df271ae7b349f7a08b5d1360b8c`)  
**Authorization review:** `docs/reviews/CODEX_G4_AUER_R9_PROFILE_PIN_CORRECTION_REVIEW.md` (SHA-256 `9ec6684653e16752bcf2652a8503a6e8f51e9f96acb99c81f36b7a99fab31e83`)  
**Research disposition:** HOLD; G1 restricted reduced-model PASS; G2/G3/G4 and physical correspondence remain UNVERIFIED.

## Summary

The fresh R9 lock passed. I invoked the R3 guard once and the Auer guard once, for the single authorized first ID. Both workers produced complete proof and common-record artifacts, both delivered `CERTIFIED`, and both separate proof-to-common audits passed. The Auer audit exercised and passed the live RHS/Jacobian worker-vector equality check.

- **Attempted IDs:** 1 — `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`
- **Arms invoked:** R3 once; Auer once
- **Complete matched pairs:** 1
- **Progress:** **1/1,944 preflight only**; the **1,944-row batch remains 0/1,944 and unauthorized**
- **Retries, substituted IDs, query 2, batch rows:** 0

This is one successful paired sample. It does not establish method superiority, G4 completion, a novelty claim, physical correspondence, or gate promotion.

## Finding 1 — Fresh exact-byte lock passed before either arm

**Evidence.** The pre-run checker recomputed the candidate manifest, sidecar, closure and every closure dependency. It also reran the active-profile checker, independently reconstructed both static inputs, and verified the preserved predecessor ledger before either worker was called.

| Lock item | Expected / declared identity | Fresh result |
|---|---|---|
| R9 candidate manifest `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v9.json` | `db0df35c634b91df0e498819d1480ee18c694608b2b68538a0580044132c74d8` | Match |
| R9 source closure `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R9.json` | `7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533` | Match; **316/316** dependencies match exact bytes |
| Manifest sidecar | File SHA-256 `c335e0daf4bcae5a6c9a9698bc92d5e32c052191b64634280581e1b3f4d5e1dc` | Match; content names the exact candidate manifest hash |
| Active path/hash assertions | 4 profiles, 8 path/hash pairs | **8/8 PASS**; 0 mismatches, duplicates, missing files, malformed hashes, closure mismatches or manifest mismatches |
| R3 semantic specification digest | `84b444d0be6e18c946697c3b95662ffd0f30dd228ae7ca5e742cee47d446c850` | PASS against development manifest and semantic ledger |
| Runtime | `C:\msys64\ucrt64\bin\python.exe`; SHA-256 `b5c33df60c2a8421dcf8117a67e848436b5d395c71ec1c0dfd96bad10f441d7f` | Match |
| Process limiter | `validation/baselines/auer2013/process_limiter.py`; SHA-256 `a8d6edf16f092f15334ad94e715af3d9a3db5319c82b0488d5ddb1da50bc0a82` | Match |
| Ordered universe | 1,944 unique IDs; LF-joined SHA-256 `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac` | Match; first ID is the authorized ID above |
| Static Auer input | SHA-256 `b59dc0f4bd05bf277384387115e7138d6df6450c187d2eefd38cae577a474e94` | Reconstructed under R9 and matched |
| Static R3 input | SHA-256 `da25e1e32521792d576a6614f8f6ae6f595ba7aead7d15343aea51817504baf6` | Reconstructed under R9 and matched the first inventory row |
| Historical R7/R8 preservation ledger | 294 path/hash entries | **294/294** still match |
| Final R9 post-build pin report | SHA-256 `f3a36fb4cf0ce841a8a7b83baad06f5c8043578cd831381b3b88fd39010cf367` | PASS and bound to the locked candidate and closure |

The immutable manifest still records `query_1_authorized=false` and `batch_start_authorized=false`. The separate R9 Codex review authorizes this exact query only; neither the manifest nor the candidate profile was edited. The pre-run authorization receipt records this scope and the exact candidate/closure identities.

**Consequence.** Both guards started from the reviewed R9 bytes. There was no source-lock stop and no need to rebuild or repair a candidate pin.

**Status:** **PASS — authorization lock complete before worker invocation.**

**Required action:** Keep the candidate, closure, sidecar, profiles and all R7/R8 evidence immutable.

## Finding 2 — One paired query completed under the frozen method guards

**Evidence.** The protocol’s serial order for the first (even-indexed) row is R3 then Auer. Each guard was called exactly once. Both Job Objects were installed, each worker was created suspended and assigned before resume, and neither timed out or hit memory limits.

| Arm | Native / replay / common / final status | Proof bytes and cap | Worker time / peak process commit | Input SHA-256 |
|---|---|---:|---:|---|
| R3 | `CERTIFIED` / `PASS` / `PASS_ON_SUPPLIED_TUBE` / `CERTIFIED` | 120,765 / 4,194,304 bytes | 0.563 s / 49,225,728 bytes | `da25e1e32521792d576a6614f8f6ae6f595ba7aead7d15343aea51817504baf6` |
| Auer | `PROOF_COMPLETE` / `PASS` / `PASS_ON_SUPPLIED_TUBE` / `CERTIFIED` | 225,167 / 536,870,912 bytes | 0.516 s / 49,025,024 bytes | `b59dc0f4bd05bf277384387115e7138d6df6450c187d2eefd38cae577a474e94` |

Both method guards used the frozen **120-second / 1,073,741,824-byte** per-arm limit; both reported `guard_status=PASS`, artifact validation `PASS`, worker exit code 0, and batch evaluations 0. Parent finalization, result-write and post-write validation timings are recorded separately in each guard receipt (R3: 0.156 / 0.000 / 0.078 s; Auer: 0.156 / 0.000 / 0.079 s).

The R9 Auer RHS/Jacobian work vector is complete: **producer 4, native replay 4, combined 8, cap 100,000**. Its other recorded work values are 1 accepted step, 1 Picard iteration and 0 rejected attempts. R3 records 29,601 producer rational operations, 29,550 native-replay rational operations, 1,251 common-conversion operations and 6,039 common-predicate/common-record operations; its work vector records 29,601 rational operations, 29,601 operation attempts, 10,435 maximum rational bits and 1 time slab.

Worker stage times (seconds) were:

| Stage | R3 | Auer |
|---|---:|---:|
| Canonical input load/validation | 0.079 | 0.063 |
| Native producer | 0.109 | 0.140 |
| Native proof serialization | 0.000 | 0.016 |
| Native replay | 0.093 | 0.109 |
| Common conversion | 0.125 | 0.000 |
| Common predicate and record replay | 0.032 | 0.015 |
| Common-record serialization | 0.000 | 0.000 |
| Worker pre-final-write time | 0.469 | 0.391 |

**Consequence.** This first ID produced a complete matched pair with both common predicates passing on their supplied tubes. The point is an execution and artifact-integrity result for this ID only.

**Status:** **PASS — 1 complete matched pair; no partial worker artifact or resource-limit stop.**

**Required action:** Review the raw results and proof bindings through the receipts and hash ledger before considering any separate batch-start request.

## Finding 3 — Independent proof-to-common composition audits passed

**Evidence.** Each separate R9 audit reopened the delivered result, proof, common record and worker guard receipt. It reconstructed the frozen query, replayed the native proof, derived common segments from the proof, recomputed the common predicate, and confirmed that the stored common record and delivered margin vectors matched the recomputation. Each audit was separately guarded at 120 seconds / 1 GiB and ran with no producer/IVP call, matched-query evaluation or batch evaluation.

| Audit | Status | Separate audit wall / peak memory | Additional evidence |
|---|---|---:|---|
| R3 | `PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED` | 0.546 s / 52,764,672 bytes | 1 segment; R3 conversion 1,251 operations; common stage 2,415 / 2,000,000 operations |
| Auer | `PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED` | 0.484 s / 51,396,608 bytes | 1 segment; common stage 2,415 / 1,917,002 available operations; separate replay confirms producer 4 + replay 4 = combined 8, cap 100,000 |

Both audits recorded `native_replay_status=PASS`, `common_predicate_status=PASS_ON_SUPPLIED_TUBE`, exact proof-derived/stored segment equality, and complete stored/recomputed common-record equality. Audit time and memory above are separate from method-worker performance.

The live worker-vector equality branch **was exercised**. The guarded Auer live audit calls `verify_live_result`, which passes `live=True` into `audit_artifact_bundle`; that branch compares the delivered worker’s producer, replay, combined and cap fields against independent producer-seeded replay counts. The audit passed with worker and audit values equal at **4 / 4 / 8 / 100,000**. This equality is not inferred from the archived fixture.

**Consequence.** The live R9 proof-to-common delivery path and its Auer work-vector equality check both passed for this first query. The audits emitted no standalone certificate and do not establish a general method comparison.

**Status:** **PASS — both independent composition audits complete.**

**Required action:** Preserve the audit reports and guard sidecars as separate, read-only evidence; do not add their wall or memory figures to either worker measurement.

## Finding 4 — Hash ledger and run accounting are complete

**Evidence.** The matched-query receipt records one attempted ID, one R3 arm, one Auer arm, one complete matched pair, zero retries and zero batch rows. `artifact_hash_ledger.json` contains exact-byte SHA-256 and byte length for every one of the 21 new lock, arm, audit, receipt and log artifacts. The adjacent `.sha256` sidecar binds the final Markdown handoff and the hash ledger.

Key artifact identities:

| Artifact | SHA-256 |
|---|---|
| Preflight authorization/lock receipt | `5409881c62366bb8227b2d6bbfecb364ad41a90f18a70b1ce369608a3edd5d7d` |
| Preflight lock ledger (includes 316 dependency and 294 preservation path/hash outcomes) | `20ad4b852f072bdf66366fec8b88f92f48416992245cbaea944c4950242f8124` |
| Matched-query receipt | `962d2cf1b2c9647716a0c0a81c54c96ca8e256ad94f69c81c44230b823815656` |
| Lossless artifact hash ledger (21 files) | `f3d4733400bd6348ef56a5212f3d29ffee974a97787fe1111fe1859d2e9533c9` |
| R3 native proof | `382abe9fdbf2e246a3df3a24859231bc9b45341f40fff6434b3e07057bbd2544` |
| R3 worker result | `0d70da5e927f137d2fd6f9a0abdb97426bc4970376a380a1adf7ed97bdaaacdd` |
| R3 common record | `6585a7cc3f71fd66ec0fdaf025f210d79b93c696ee14afb877e0427969df3269` |
| R3 composition audit | `1ed7a016bf4ae211e2eda866eaadabbf490cb307055846383cd638645a27dbd8` |
| Auer native proof | `55d9ab3f55a96506661c86b198649bb412da6c45cd2c7b341dc752b37e3c857c` |
| Auer worker result | `1804843a5b7c36d247b66a04be773c84e3cbad47f926324586173fa69b95f05b` |
| Auer common record | `060eb761fb2a2f661b18b76d4c1f5572f74ab875da75775fff6e83d85882ce0b` |
| Auer composition audit | `65c0ec380dfdbe36a9d6891d9a83c38ea413765450e76c0b29690cb01ff3d1a6` |

The full 21-file path/hash/size list is in `results/validation/g4/auer2013/protocol_v3_r9_single_query_preflight_v1/artifact_hash_ledger.json`. All proof and common artifacts are complete; no partial proof/common artifact, timeout, memory stop, malformed proof, or audit failure was produced. Both method stdout logs are empty (0 bytes). No candidate or predecessor file was edited. No commit or push was made.

**Consequence.** The execution can be independently replayed from a complete, hash-bound output set. R9’s candidate still records its pre-review `query_1_authorized=false`; only the separate one-query review receipt records that the exact authorization was consumed.

**Status:** **PASS — output ledger and matched-query accounting reconcile.**

**Required action:** Use the adjacent `.sha256` sidecar to verify this handoff and the lossless ledger before forwarding the package.

## Final disposition and recommendation

**Finding.** The exact first ID completed as a certified matched pair, the locked R9 source set remained valid, and both separate composition audits passed.

**Evidence.** One ID was attempted; R3 and Auer were each invoked once; one complete matched pair was produced; all worker, proof, common-record and audit artifacts passed their validators and exact-byte hash checks.

**Consequence.** The first R9 preflight supports a review decision on whether to consider the larger experiment. One sample cannot support a comparative performance claim or a G4 pass.

**Status:** **GO to Codex review of this single-query result. NO-GO for executing the batch under this assignment. HOLD remains unchanged; G4 remains UNVERIFIED.**

**Required action:** A later **separate batch-start review is warranted for Codex consideration** because the first paired preflight completed successfully. The 1,944-query batch remains unauthorized and unrun until that separate review makes an explicit decision. No second query, G2/G3 work, controller, hardware experiment, or gate promotion follows from this handoff.

### Tóm tắt chuyển giao

Đã khóa đúng candidate R9 và chạy duy nhất query đầu tiên với R3 rồi Auer, mỗi nhánh đúng một lần. Cả hai trả `CERTIFIED`, common predicate và audit độc lập đều PASS; vector RHS/Jacobian của Auer khớp 4/4/8 dưới cap 100.000. Có **1 cặp preflight hoàn chỉnh trên 1.944 ID**; batch vẫn **0/1.944**, chưa được phép chạy. Các receipt, proof, result, common record và audit đã được ghi hash; G4 vẫn UNVERIFIED và trạng thái nghiên cứu vẫn HOLD.