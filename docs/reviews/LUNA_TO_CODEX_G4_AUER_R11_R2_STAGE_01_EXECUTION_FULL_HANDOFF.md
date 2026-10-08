Session: DDWMR | LUNA-G4-AUER

# G4 Auer R11 R2 Stage 1 execution handoff

**Date:** 2026-10-03  
**Assignment:** docs/CODEX_TO_LUNA_G4_AUER_R11_R2_STAGE_01_EXECUTION.md  
**Authorization:** GO for stage_01 only, exactly 11 ordered IDs  
**Stage result:** STOPPED_AFTER_FIRST_NONVALID_PAIR after the first ID  
**Batch progress:** 1/1,944; the R9 preflight remains a separate carry-in  
**Research disposition:** HOLD; G4 remains UNVERIFIED

## Executive result

The exact authorized Stage 1 runner was invoked once. It attempted the first scheduled ID with R3 followed by Auer and ran one read-only composition audit for each method. The pair was nonvalid/inconclusive, so the runner stopped as required. The other ten Stage 1 IDs were not run. Stages 2–7 were not launched. No retry, ID substitution, commit, or push occurred.

The terminal stage receipt records one attempted ID, two arm intents, two audit intents, zero complete valid matched pairs, one nonvalid pair, ten remaining Stage 1 rows, zero retries, no unresolved query IDs, and no stage exception. The runner command emitted that terminal receipt and the execution tool surfaced a nonzero exit status (1). This was the protocol stop after a nonvalid pair: the stored stage state is explicit, stage_exception is null, and the attempts are fully represented in the preserved records.

The post-run summary was derived successfully from the stored records and has all 1,944 universe rows. It marks the attempted row ineligible for comparison. It also detects a stricter integrity problem in Auer’s stored common record: the result points to the exact common-record bytes, but that JSON lacks query_id and method_input_sha256. The summary therefore rejects Auer’s terminal arm receipt and counts its invocation as indeterminate for verified accounting. Preserve this discrepancy for Codex review; do not reinterpret it as a valid Auer comparison result.

## Authorization and source locks

Before launch, the canonical context and assignment materials were read: AGENTS.md, all four research_context files, this assignment, the R11 R2 protocol, the Stage 1 Codex review, the GO receipt, the frozen schedule, and the R11 R2 source lock.

The receipt was GO for stage_01 only, with the canonical output root, exact Stage 1 digest/count, R3-then-Auer order, one invocation per method and ID, one read-only composition audit per method and ID, no retry/substitution, and unchanged resource limits. Live identities matched:

| Item | SHA-256 |
|---|---|
| Stage authorization receipt | f275808e0b0a44c3a7b4c24496385d5178f82b22da837bbf65887df860e35a31 |
| Reviewed Stage 1 Codex review | 7659edc894324b6c138083c07057fa0a4bcee0acca3f19a455e1be335bfa4d6c |
| R11 R2 candidate manifest | 193dbead525d1a1c2fae00920a2ff385e7281a6a28aae00e69d72ea7778d106d |
| R11 R2 source closure | dbe23888fac40caf518009dd96f888e1da45eace388d9ace8cffe906074cbf7b |
| Frozen R10 stage schedule | 212b6a09526379188acad46aa05070626b5248a76bc64047d18dd47f9c136e9c |
| Stage 1 ordered-ID digest | 80383e5344268b6a7f402579615d9dbe076fd38c30b9a0bd8741951cc359c8f2 |
| Pinned Python executable | b5c33df60c2a8421dcf8117a67e848436b5d395c71ec1c0dfd96bad10f441d7f |

The prelaunch runner source-lock-only check returned PASS_SOURCE_LOCK_ONLY: 376 R11 dependencies and 316 R9 dependencies checked, eight active profile pins checked, 21 preflight artifacts checked, zero workers invoked, and zero producer/IVP invocations. The Stage 1 output directory was absent before launch. The post-run summary derivation revalidated the source and authorization bindings.

## Exact Stage 1 execution

Command:

    C:/msys64/ucrt64/bin/python.exe -m validation.g4.batch_stage_runner_v3_r11_r2 --project-root . --stage-id stage_01 --authorization-receipt results/validation/g4/auer2013/protocol_v3_r11_batch/authorizations/stage_01.json --output-root results/validation/g4/auer2013/protocol_v3_r11_batch

Stage window: 2026-10-03 16:05:14.958965 UTC through 2026-10-03 16:05:27.999427 UTC. Recorded stage elapsed wall time: 13.047 seconds.

Only attempted ID:

1. state_low_mid__scene_d020_l+000__T_050__V_m1_0

The ten remaining Stage 1 IDs are unrun:

- state_low_pos__scene_d020_l+200__T_100__V_m1_p1
- state_high_neg__scene_d050_l-200__T_020__V_0_m1
- state_high_mid__scene_d050_l+000__T_050__V_0_0
- state_high_pos__scene_d050_l+200__T_100__V_0_p1
- state_low_neg__scene_d100_l-200__T_020__V_p1_m1
- state_low_mid__scene_d100_l+000__T_050__V_p1_0
- state_low_pos__scene_d100_l+200__T_100__V_p1_p1
- state_high_neg__scene_d200_l-200__T_020__V_m1_m1
- state_high_mid__scene_d200_l+000__T_050__V_m1_0
- state_high_pos__scene_d200_l+200__T_100__V_m1_p1

The authorized stage digest covers all eleven scheduled IDs; the attempted ID was the first in that order. Stages 2–7 have no output directories.

## Method and composition-audit results

| Evidence | R3 | Auer |
|---|---|---|
| Attempt | Invocation intent and terminal receipt present; attempt 1 | Invocation intent and terminal receipt present; attempt 1 |
| Raw final status | UNKNOWN | PROOF_COMPLETE_COMMON_UNKNOWN |
| Common predicate | NOT_EVALUATED | UNKNOWN_ON_SUPPLIED_TUBE |
| Native status / replay | UNKNOWN / NOT_RUN | PROOF_COMPLETE / PASS |
| Worker guard and artifact validation | PASS / PASS | PASS / PASS in raw terminal receipt |
| Composition audit | ARTIFACT_REJECTED; report missing | PASS, report status PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| Relevant raw diagnostic | DELIVERY_ARTIFACT_BINDING_MISMATCH: common_record_path is missing | Summary verifier rejects arm receipt: common record is not bound to the stored result |

R3’s result reports termination reason COLLISION_SUFFICIENT_MARGIN_NEGATIVE, but its final status is UNKNOWN. Under the protocol, UNKNOWN is inconclusive; it is not a finding of unsafe behavior or unavoidable collision. The R3 audit log records zero producer/IVP invocations and zero matched-query evaluations.

Auer’s raw result reports native proof completion and replay PASS, while its common predicate remains UNKNOWN. Its audit receipt/report say PASS and record zero producer/IVP invocations. However, Auer’s result.common.json has the exact raw SHA-256 named by result.json, but the common JSON has no query_id or method_input_sha256 fields. The R11 summary verifier requires those fields to bind the common record to the scheduled ID and method input, so it rejected Auer’s arm receipt. The summary records Auer’s invocation as indeterminate, not as confirmed or not-run.

The stage runner’s raw terminal receipt records terminal arm and audit states for both methods. The independently derived summary is the stricter evidence boundary: confirmed worker invocations are R3=1 and Auer=0, with one Auer invocation indeterminate. Arm intent counts are one per method; audit intent counts are one per method. Do not promote the raw Auer PASS fields past the summary’s failed binding check.

The runner stopped for the first pair on these recorded reasons:

- R3 composition audit did not PASS.
- R3 final status was UNKNOWN and common status was NOT_EVALUATED.
- Auer final status was PROOF_COMPLETE_COMMON_UNKNOWN and common status was UNKNOWN_ON_SUPPLIED_TUBE.

## Read-only summary and fixed-denominator accounting

The read-only summary builder validated the preserved receipt/artifact stream and created:

    results/validation/g4/auer2013/protocol_v3_r11_batch/derived_batch_summary.json

Builder result: PASS_SUMMARY_DERIVED; 1,944 unique rows; batch progress 1/1,944.

| Count | Value |
|---|---:|
| Fixed universe denominator | 1,944 |
| Separate R9 preflight carry-in | 1 |
| Batch-eligible rows | 1,943 |
| Attempted batch IDs | 1 |
| Complete valid matched pairs | 0 |
| Incomplete pairs | 1 |
| Valid common-predicate pairs | 0 |
| Audit-rejected pairs | 1 |
| Unrun batch rows | 1,942 |
| Retries | 0 |
| ID substitutions | 0 |
| Comparison-eligible rows | 0 |

The attempted row is AUDIT_REJECTED / INCOMPLETE_PAIR and comparison_eligible=false. UNKNOWN_is_inconclusive is true. The carry-in remains a separate stratum and is not pooled with this attempted row. No comparison, novelty, or gate claim follows from Stage 1.

## Resource evidence

The receipts keep method-worker, launcher/setup, and independent audit resources separate. The frozen per-worker cap was 120 seconds and 1 GiB process commit; the R11 outer method wrapper was 150 seconds. Each audit had a separate 120-second / 1-GiB process limit and 630-second R11 audit-wrapper timeout. Setup memory was not measured.

| Measurement | R3 | Auer |
|---|---:|---:|
| Worker wall seconds in raw receipt | 0.281 | 0.485 |
| Worker peak process commit bytes in raw receipt | 49,254,400 | 48,967,680 |
| Separate launcher/setup wall seconds | 1.531 | 1.672 |
| Audit wall seconds | 0.250 | 0.469 |
| Audit peak process memory bytes | 51,339,264 | 51,257,344 |

R3’s worker values and both audit measurements are present in the derived summary. Auer’s worker measurement is preserved in its raw receipt, but its arm record is not promoted to confirmed invocation in the derived summary because of the common-record binding rejection. These measurements do not imply a matched comparison or method advantage.

## Key artifact hashes

All paths below are project-relative to projects/ddwmr-actuator-safety. Hashes are exact-byte SHA-256 values observed after the stage stopped.

| Artifact | SHA-256 |
|---|---|
| Stage intent | 90c3abf1400326b800f69bc72091f6ba2eea213ea79c039d94bc1145e33c5f50 |
| Stage terminal receipt | 67fcf72dcf5eebe32ef093311aa1f8bf5b8b640ab7a079251487d2672f5dde64 |
| Derived 1,944-row summary | 6e3b073e0abe077536529b61e9278d5f7b257e3b470d4206fe3b61ef32a83f32 |
| R3 invocation intent | 6b645e611a419cd7486b83f6b8a1065376ecf8c27014b1ac817e45be8c4e44f8 |
| R3 terminal receipt | 029037666d425abe7dfe09ceded6ebc2f00965a42a01fbe409980aafc70346c6 |
| R3 result.json | 0b30beefce92517f3f292f87098b211c0d61d3a3f023edc0ad5626e48f1509dd |
| R3 proof.json | 434530122f8833681edcd9057f2df75eeb066a70c92fa84a3f1b93eaab237852 |
| R3 worker.guard.json | b252fe04e89571d1ab1a1fa0ec4a2707991388b1818444f3b236eab6c09cb3b6 |
| R3 audit intent | 71722ddacf4aeb4b1b2c0ef9c5910434608f36bc14be8e4eff5a6e5239dcf363 |
| R3 audit receipt | d8d12d468d77a892909427d4b892193e62b63c6fe063c3bef8ad6325b179f845 |
| R3 audit guard | 8e3bd25041313433da5c92d6a27da44dcd4972bc006cf38bfa7a673f1c1f60b3 |
| R3 audit stdout log | 29a157fe14e1a9b9309c7591d1f296c7b40e9e5f25c08660620935d66e955d55 |
| Auer invocation intent | 1e95c59728ab793ea7330b4b493236d959c9ab1db47fc575ee357409b539c0bb |
| Auer terminal receipt | 61752b92214c86f7ffa6b36f0ecd609076de4a1817391b0c78a226572eecd673 |
| Auer result.json | 6e3ecf19fecfae1ca8bfa2dfd539f5c2d4e8f5bd79d7f1851d09607c6952f598 |
| Auer proof.json | 7cdc2537c9060adb7d3fbf67f2ecf0deb1f8480f2d50eca554ea428bd7049010 |
| Auer result.common.json | 23b9c80c49f26a5021d3c78589d8ba8cc3834aad99f016dbb672e0d614ee2659 |
| Auer worker.guard.json | 8b8d618b9cd494579d37a03efbd5c5a650a92b5fd3abcb6d76ea1f16105a3e96 |
| Auer audit intent | 3b098d6c927620731e19fba7add217b30d9102ee2d8b8c3619e7f07da3733838 |
| Auer audit receipt | b82b317b268f3e4b8c00da5b22798bbfc6a3f76e67886e769c56b372ad0db67c |
| Auer composition report | 155500c61f83181d7867538c7b0f74a18075e0f5348e231ac6beaaf81b4f1268 |
| Auer audit guard | 18a57b3f29a5de33c9862e8559c0db84041bbab67edc05ef6549dbb440152ce6 |
| Auer audit stdout log | 0c53b86230f7075bec9b30a83e4526de85c4338c1e81f9a505656886d1d94cb3 |

The R3 composition report is absent; its audit receipt explicitly records a missing report and ARTIFACT_REJECTED. The stage output root contains only the authorization directory, stage_01, and the derived summary. No stage_02 through stage_07 directory exists.

## Review boundary and required follow-up

This is an execution handoff, not acceptance of the R11 R2 implementation or evidence. Codex should review the failed R3 common-record delivery and the Auer common-record metadata binding against the source contract. Preserve the current raw records and summary. Do not retry this consumed Stage 1 intent, rerun either method/audit, or launch a later stage without a new explicit authorization. G4, method comparison, novelty, and physical-platform correspondence remain UNVERIFIED.
