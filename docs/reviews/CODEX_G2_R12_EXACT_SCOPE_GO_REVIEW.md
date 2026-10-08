# Codex review — G2 R12 exact two-row offline validation

Disposition: GO

<!-- G2_R12_EXACT_SCOPE_GO_V1
decision_id: CODEX_G2_R12_TWO_OFFLINE_ROWS_20261004
decision_artifact_path: research/benchmarks/G2_R12_CODEX_SCOPE_DECISION_v1.json
review_id: CODEX_G2_R12_EXACT_SCOPE_GO_REVIEW_20261004
execution_authority: GO
stage_id: G2_R12_WHOLE_HOLD_PICARD_STAGE_CANDIDATE_V1
manifest_path: research/benchmarks/G2_R12_WHOLE_HOLD_PICARD_STAGE_CANDIDATE_v1.json
manifest_sha256_raw: f0094dda957ba8e165fda21982fadee20bd2c5839ed309b1b377acc17764337f
source_closure_path: research/benchmarks/G2_R12_WHOLE_HOLD_PICARD_SOURCE_CLOSURE_v1.json
source_closure_sha256_raw: adbde039053db9438e989f9d74987421aad3f5f46db4ee88af7d9d5c41c98d62
runner_path: validation/g2/r12_stage_runner.py
runner_sha256_raw: a9f8582625b8ee0364d634a672dfae87e29d74cf3dd9f7b6481b024f830555e4
picard_checker_path: validation/g2/whole_hold_picard_checker_r11.py
picard_checker_sha256_raw: 2a794e8f46c4b029331a2548dccd1948b78d3f5d5d7a96efa118d9353ba56f7e
receipt_checker_path: validation/g2/r12_execution_checker.py
receipt_checker_sha256_raw: f4e6b2aa753802cf8649037b3a2b83d47f2d458eaf248dfdad18942e8a77e15f
ordered_r5_source_indices: 12,24
ordered_query_ids: S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_L0_R0,S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lp1_Rp1
ordered_query_sha256_raw: d5648569b11c576c8cc0ecb07c5096c21b06fe3a5e849358f254770649465471,105a0710185446312933ec8c92922acd1db0f3af0e999d67207ccd70534b4808
ordered_input_payload_semantic_sha256: 422afd0448a184f4f67262c6338593c871739b41fb677e8ab1d6b566d18b93ac,70301bc5df76aab2dfdb8bef5135592fbf0063af6799b0f0eb119f4873b2cf9a
-->

**Date:** 2026-10-04  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G2_R12_EXACT_SCOPE_GO_BINDING_CORRECTIONS_FULL_HANDOFF.md`  
**Decision artifact:** [Exact two-row decision](research/benchmarks/G2_R12_CODEX_SCOPE_DECISION_v1.json); [repository navigation link](../../research/benchmarks/G2_R12_CODEX_SCOPE_DECISION_v1.json).  

I read `AGENTS.md`, all four canonical `research_context` files, the R11 review and R12 assignment, the R12 handoff/contract, manifest, closure, runner, Picard checker, independent receipt checker, source binder, schema and stored fixture declarations. This was source/artifact review; I did not run a real row, native query or fixture suite.

## Finding 1 — source identity and rows

**Evidence.** Independent hashes match the exact source values in the marker. All 202/202 R12 closure path/hash entries match live bytes, and the 186 inherited R11 records are unchanged by path. The closure sidecar matches the raw closure hash. The manifest binds development-overlap R5 indices 12 and 24 in that order, their exact query/input hashes, the unchanged 36-pair table and its sole preparation trigger. The R12 results directory was absent at review time. R5 remains 800/800 `NOT_RUN`; the earlier two R6 observations remain consumed.

**Consequence.** The decision has exactly two previously selected offline inputs. It grants no R5 study or R6 rerun.

**Status:** VALID source and row identity.

**Required action:** Preserve R3/R5/R6/R10/R11 artifacts and use only the two named R12 rows in order.

## Finding 2 — decision binding and one-shot replay

**Evidence.** Both the production runner and independent public auditor check the fixed machine-decision path, exact candidate/source hashes, ordered rows, review Markdown raw hash, unique marker and explicit disposition. They reject an unrelated review, a contradictory execution disposition, changed decision bytes or mismatched scope. The runner copies the decision before a row intent, rechecks the live decision and review before each intent, writes each intent once and refuses to retry an intent without a terminal. The auditor inventories partial artifacts and independently replays completed records. The handoff reports 18 synthetic non-query gate/crash fixtures, including the prior R10 review cited with a forged legacy acceptance field, and all expected outcomes passed. I inspected the source and fixture coverage but did not rerun those fixtures.

**Consequence.** The R11 self-reported review field no longer grants authority. A valid `UNKNOWN` is an abstention; resource, invalid or interrupted outcomes stop the two-row sequence. The stage may end with zero, one or two completed rows, and only a checked complete pair can be interpreted under the predeclared table.

**Status:** ACCEPT the exact-scope source/contract candidate for two offline row evaluations; live certificates and usefulness remain unverified.

**Required action:** Use at most two offline Picard row calls, with a declared 60-second hard worker timeout, zero native-query calls and no retry. Afterward, run the public read-only audit, preserve every partial artifact, and report complete source/record/receipt hashes and the two outcome classes. Do not reinterpret `UNKNOWN` as unsafe or task failure.

## Finding 3 — scientific limits

**Evidence.** No R12 real row has been evaluated. The conditional whole-hold Picard argument applies to the stipulated reduced model under the interval-RHS and positive-denominator assumptions reviewed earlier. A positive two-safe-action result would only meet the predeclared trigger to **prepare** a broader protocol.

**Consequence.** This decision authorizes two development-overlap offline evaluations only. It does not establish voltage necessity, physical safety, practical usefulness, G2 PASS, or authority to execute the 800-row study.

**Status:** **HOLD** overall; G1 restricted reduced-model PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.

**Required action:** Return one detailed result handoff for Codex review. Keep the larger study unrun.
