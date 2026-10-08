# Codex review — G4 Auer R11 R2 Stage 1 result

**Date:** 2026-10-03  
**Decision:** ACCEPT the recorded Stage 1 stop and fixed-denominator accounting; BLOCK R11 continuation and scientific comparison. No new query authorization.  
**Source:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_R11_R2_STAGE_01_EXECUTION_FULL_HANDOFF.md` and the preserved Stage 1 artifacts.

## 1. Execution identity and stop

**Finding.** The first scheduled Stage 1 ID was attempted once, in the authorized R3-then-Auer order, followed by one audit intent per arm. The runner stopped after that nonvalid pair. The other ten Stage 1 IDs and Stages 2–7 were not run.

**Evidence.** I read `AGENTS.md`, all four canonical `research_context` files, the R11 R2 protocol, the Stage 1 GO review and authorization, the handoff, runner/summary source and stored records. Independent SHA-256 checks matched the authorization, candidate manifest, source closure, schedule, reviewed GO document, stage terminal receipt, derived summary, both result files, Auer common record and both audit receipts. The four arm/audit artifact maps list 20 present files; their recorded byte counts and hashes match. They also list the absent R3 common record and absent R3 composition report as absent. The stage receipt says `STOPPED_AFTER_FIRST_NONVALID_PAIR`, one attempted ID, zero retries, zero substitutions, ten Stage 1 rows remaining and `stage_exception=null`. Only the first ID has an output directory; no `stage_02`–`stage_07` directory exists.

**Consequence.** The process exit status 1 is consistent with the recorded protocol stop, rather than evidence of an unrecorded stage exception. This is an execution/accounting acceptance, not a certificate or method comparison.

**Status:** VALID for the recorded, source-bound stop. The review did not independently rerun either native proof or a query.

**Required action:** Preserve every consumed intent, result, guard, audit record, receipt and summary byte-for-byte. Do not retry this ID.

## 2. Scientific result of the attempted pair

**Finding.** Neither arm produced a positive common collision/contact certificate on this ID. `UNKNOWN` is inconclusive.

**Evidence.** R3's stored result is `UNKNOWN`, with `COLLISION_SUFFICIENT_MARGIN_NEGATIVE`, `common_status=NOT_EVALUATED`, and no common record. Its audit was `ARTIFACT_REJECTED` with `DELIVERY_ARTIFACT_BINDING_MISMATCH: common_record_path is missing`; the R9 composition verifier requires a complete native proof and common record before proof-to-common replay. Auer's raw result is `PROOF_COMPLETE_COMMON_UNKNOWN`; its stored native replay and composition audit report say PASS, while the recomputed common predicate is `UNKNOWN_ON_SUPPLIED_TUBE`. The audit report binds the scheduled query and Auer input hash and records zero new producer/IVP calls. These are stored replay reports, not a new independent replay by this review.

**Consequence.** R3's negative *sufficient bound* does not establish collision or unsafety. Auer's completed IVP proof does not imply a passing common safety predicate. The pair has zero positive common-predicate results and cannot support a performance or safety superiority claim.

**Status:** VALID interpretation of the preserved records; no matched scientific result accepted.

**Required action:** Keep `UNKNOWN`, audit rejection and proof completion as separate fields in future reporting.

## 3. R11/R9 common-record contract defect

**Finding.** The R11 summary rejects the Auer terminal arm because R11 demands direct `query_id` and `method_input_sha256` fields in `result.common.json`. The R9 common-record producer does not put those fields in that record. This is a producer/consumer contract mismatch, not evidence that the stored Auer common bytes were changed.

**Evidence.** `validation/g4/batch_stage_runner_v3_r11_r2.py`, lines 1078–1086, requires both fields in every existing common record. `validation/g4/common_tube.py`, lines 486–518, builds the common record with frozen-input hashes, segments, checks and predicate status, but no direct query ID or method-input hash; the Auer worker writes exactly that record at `validation/g4/auer_matched_query_worker_v3_r9.py`, lines 599–620. The stored Auer common record has neither field. Its SHA-256 `23b9c80c49f26a5021d3c78589d8ba8cc3834aad99f016dbb672e0d614ee2659` matches `result.json` and the arm receipt. The R9 composition verifier independently reconstructs the frozen query, checks the result's query/input binding, checks the common-file hash and bytes, compares proof-derived segments and frozen inputs, and recomputes the complete common record (`validation/g4/verify_matched_composition_v3_r9.py`, lines 500–630). Its stored audit report says PASS. The derived R11 summary correctly follows its stricter source rule and marks Auer's terminal receipt rejected, invocation indeterminate for *verified R11 accounting*, and the pair incomplete.

**Consequence.** Do not describe Auer as not invoked: an intent, worker guard, raw result, proof, common record, terminal receipt and audit are present. Do not promote it to a verified R11 pair either. The earlier Codex Stage 1 source review overlooked this direct-field assumption; this review corrects that finding. A versioned consumer correction must validate the existing R9 schema and its actual cross-artifact bindings without weakening positive-artifact or tamper rejection.

**Status:** BLOCKER for R11 summary acceptance of this Auer arm.

**Required action:** Investigate and prepare a versioned, read-only contract correction. Do not edit historical R9/R11 records to insert missing fields.

## 4. Batch design blocker independent of the contract defect

**Finding.** Correcting the Auer metadata check would still leave this pair nonvalid under R11's frozen stop rule. R11 cannot proceed to Stage 2 from the preserved Stage 1 state.

**Evidence.** `pair_disposition` in `batch_stage_runner_v3_r11_r2.py`, lines 749–765, requires both arms `CERTIFIED`, both common predicates `PASS_ON_SUPPLIED_TUBE`, and both audits PASS. R3 and Auer fail those scientific conditions regardless of the direct-field issue. The protocol's section 4 stops at the first `UNKNOWN` or otherwise nonvalid pair. `_verify_prior_stage_complete`, lines 1653–1744, requires all eleven Stage 1 rows and a `STAGE_COMPLETE` receipt before a later stage. The immutable receipt instead records one attempted row and `STOPPED_AFTER_FIRST_NONVALID_PAIR`.

**Consequence.** The frozen R11 path is ended at 1/1,944 attempted universe IDs. Treating all `UNKNOWN` outcomes as stage-stopping also prevents this protocol from measuring certification yield over the prespecified 1,944-ID universe. A new prospective protocol must distinguish an authenticated inconclusive method outcome from an integrity failure, retain the fixed denominator and all observed strata, and make any continuation rule explicit before another query.

**Status:** BLOCKER for R11 Stage 2–7 and the intended full matched batch.

**Required action:** Prepare a versioned continuation proposal; do not resume Stage 1, reuse its authorization, or silently skip its consumed ID.

## 5. Fixed-denominator disposition

The stored summary has 1,944 unique rows: one separate R9 preflight carry-in, one attempted R11 batch ID, and 1,942 unrun batch IDs. It reports zero comparison-eligible pairs, zero retries, and zero ID substitutions. Its `Auer=0 confirmed, 1 indeterminate` count is a consequence of the R11 contract rejection, not a claim of zero physical worker executions. The first Stage 1 ID and the R9 preflight are already observed strata for any later design. A later version cannot truthfully call the remaining study wholly prospective.

**Final disposition:** ACCEPT the stop and preserved evidence in this narrow sense; **NO-GO for further R11 queries, Stage 2–7, matched-method conclusions or gate promotion**. Overall status stays **HOLD; G1 PASS for restricted reduced-model scope; G2/G3/G4 and physical-platform correspondence UNVERIFIED**. Generic-method novelty remains blocked by prior art; this Stage 1 result changes no novelty disposition.
