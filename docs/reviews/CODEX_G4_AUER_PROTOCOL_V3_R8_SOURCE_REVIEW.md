# Codex review — G4 Auer matched protocol v3 R8

**Date:** 2026-10-03  
**Lane:** `LUNA-G4-AUER`  
**Input:** `LUNA_TO_CODEX_G4_AUER_PROTOCOL_V3_R8_RHS_ACCOUNTING_FULL_HANDOFF.md`  
**Repository:** `main` at `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`; shared working tree not cleaned or committed.  
**Authority:** MASTER v2.1. **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.**

## Decision

**ACCEPT the focused R8 correction of the R7 successful Auer RHS/Jacobian replay accounting defect.** The archived-proof and source-contract evidence is valid in its stated non-query scope. **GO for exactly one guarded matched preflight query, the first ID in the frozen order, after an exact-byte pre-run lock check. NO-GO for the 1,944-query batch.** This review supersedes the candidate's pre-review `query_1_authorized=false` only for that single preflight run; the candidate manifest itself must remain byte-identical, with a separate run authorization/receipt referring to this review.

I inspected the R8 handoff, R7 blocker review, corrected verifier and worker paths, result validator, archived fixture report, guard/manifest, source closure and import audit. I made read-only hash and source checks and one in-memory call to the count validator. I did not invoke a producer, matched worker, query 1 or batch; no proof or query-level result was generated.

## 1. Successful replay accounting

**Finding.** The R7 wrong-dictionary-level defect is repaired in the inspected R8 source.

**Evidence.** `verify_matched_composition_v3_r8.py` reads `rhs_jacobian_replay_evaluations` and `rhs_jacobian_combined_count` from the successful replay object's **top level**. `_validated_auer_rhs_replay_counts` requires exact nonnegative integer types, `combined=producer+replay`, equality with the seeded mutable counter, and `combined<=100000`. `_replay_auer_envelope` seeds that counter from the complete proof's producer work field, then stores the validated 4-field work vector. `audit_artifact_bundle(..., live=True)` compares the reconstructed vector with the worker vector. The result validator independently requires exact integer fields and reconciles the same complete-proof counts with the frozen profile. My in-memory source call returned 4/4/8 under cap 100,000 and rejected missing, Boolean and wrong-sum fields as `NATIVE_PROOF_RHS_ACCOUNTING_INVALID`.

**Consequence.** A successful archived replay with positive replay work no longer becomes the false 4/0/4 report observed in R7. The live branch has a coherent comparison target.

**Status.** **VALID focused source correction.** Prospective live worker-vector equality remains unexercised.

**Required action.** Keep this source byte-identical for the preflight. Review the first live result's producer/replay/combined/cap vector against the independent composition report; if no complete Auer proof is produced, report that the successful live equality branch remains untested.

## 2. Archived fixture and resource boundaries

**Finding.** The recorded R8 fixture covers the intended positive-replay case and selected boundary failures without representing a matched query.

**Evidence.** The fixture report's archived Auer case records producer 4, replay 4, combined 8, cap 100,000, and five malformed/tampered successful-count rejections. Its full suite reports 13/13 mutation rejections and zero producer calls, matched workers or new trajectory proofs. The at-cap boundary is rejected before another RHS evaluation. The R3 profile/worker/validator retain the 4,194,304-byte serialized-proof cap and `RESOURCE_LIMIT` over-cap classification. The fixture explicitly states `live_worker_vector_equality_exercised=false`. The two 64-MiB probe records are allocation-failure checks, not query-pipeline time or memory measurements.

**Consequence.** The old blocker is addressed as a source and stored-proof contract. Query-level resources and live composition still need direct observation.

**Status.** **VALID within archived-proof/probe scope; live preflight UNVERIFIED.**

**Required action.** Keep fixture, offline audit and worker measurements separate. Do not infer prospective proof size or matched performance from the archived records or probes.

## 3. Candidate identity and query universe

**Finding.** The R8 candidate is internally hash-bound and still unexecuted.

**Evidence.** I recomputed SHA-256 of the R8 closure (`37fde1b2ba705fe9e44eba101989035643aeb1c9fd0e4dc84d1eff288b2ca276`), candidate manifest (`263305153edd39b60110e1a275956391dd19da4ba2ee339c6cf53c4d31c3bb86`), verifier (`84b87b82c15a06057a0044ace329c79f2ffee51a3ada29e06ab4dd1ab3142a54`), fixture report (`4e684f6ad482faefb1f0dc5467003b7314ec3f299e2fa2e0428092acdbf66203`), guard, fixture source and probe index; all match the handoff. All **214/214** dependency hashes in the closure match present files. The ordered 1,944-ID SHA-256 is `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`, independently recomputed from the original ID list joined by LF without a trailing LF. The manifest states 1,944/1,944 `NOT_RUN`, 0 matched evaluations, and `comparison_run=false`.

**Consequence.** R8 has a reviewable exact-byte pre-run identity. It is not a final matched comparison or a novelty result.

**Status.** **VALID identity check for the current tree; G4 still UNVERIFIED.**

**Required action.** Before preflight, recheck every closure dependency and input/profile hash. Preserve the candidate and predecessor artifacts unchanged; write new run evidence under a separate versioned output directory.

## 4. One-query boundary and remaining G4 work

**Finding.** The next informative experiment is one predeclared, guard-bound matched query, with both arms and complete audit. The batch requires a later decision.

**Evidence.** The current R8 fixture never invokes the live worker-vector equality branch. The candidate's first ordered ID is `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`. The frozen method-worker resource policy is 120 seconds and 1 GiB per arm; Auer has the 100,000 combined producer/replay RHS cap and R3 the 4-MiB serialized-proof cap. A separate read-only composition audit has its own guard and is not method runtime. The candidate manifest remains a pre-run snapshot with 0/1,944 rows and must not be rewritten to imply execution or authorization retroactively.

**Consequence.** A single preflight can test the actual worker, artifact validation, source binding, replay, common predicate and live vector composition path. One query cannot establish matched-method superiority, overall runtime, or novelty. If it stops or returns incomplete proof, retain that result and report the unexercised paths.

**Status.** **GO for one exact-ID guarded preflight after lock verification; batch NO-GO.**

**Required action.** `LUNA-G4-AUER` should execute only the first ordered query under unchanged R8 sources/profiles with both method arms, guard receipts, native proof/status artifacts, independent common replay and exact hash ledger. No cap increase, substitution of an easier ID, or silent rerun. Report raw outcome and whether live 4-field equality was exercised. Submit a full Markdown handoff for review before any further query or batch.

## Final disposition

The R7 RHS-accounting blocker is **closed in source and archived-fixture scope**. R8 is authorized for one controlled preflight query only; **0/1,944 matched queries have run at this review point**. The 1,944-query batch, G4 originality claim, G3, implementation and physical transfer remain unapproved. Overall **HOLD** is unchanged.

**Vietnamese forwarding summary:** R8 đã sửa đúng lỗi đếm 4/0/4 của R7; nguồn và fixture lưu trữ cho 4/4/8 đạt trong phạm vi phi-query. Tôi cho phép `LUNA-G4-AUER` khóa hash rồi chạy đúng query đầu tiên với cả hai phương pháp và replay, dừng để gửi handoff. Chưa chạy batch; G4 vẫn UNVERIFIED.
