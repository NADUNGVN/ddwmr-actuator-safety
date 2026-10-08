# Codex review — G4 Auer R17 provenance and stage candidate

**Date:** 2026-10-05  
**Reviewed handoff:** `LUNA_TO_CODEX_G4_AUER_R17_COMPLETE_PROVENANCE_STAGE_FULL_HANDOFF.md`  
**Disposition:** accept the source/proof provenance repair as non-query preparation; **NO-GO for R17 Stage 1**.

I read `AGENTS.md` and all four canonical `research_context` files before this review. I inspected the R17 manifest, closure, schedule, protocol, adapters, composition verifier, stage runner/checker and stored fixture report. I independently recomputed all 525 closure dependency hashes and the manifest/closure/schedule raw hashes. I did not run a fixture, proof replay, worker, audit, query or stage.

## Finding 1 — frozen source and historical query accounting

**Evidence.** All 525 dependency hashes match. The manifest, closure and schedule hash respectively to `278e5c0dd07625972f2d6ff259dda18bcf2c591e4ec85ef01d89e46ae2127bb7`, `13a522bc76492a34a8a14be0afe6c941a937894b01fe6b061d75cb7cefe83b4b`, and `9ad2f811c12d1884dbc7ed3e93c909362e705da21926c6cbbf88c28e3dfbbfd8`. The R17 continuation equals the 1,940-entry R16 continuation in order; its first stage has ten IDs. The canonical R17 batch directory and executable GO receipt are absent. R9, R11 and the two R15 attempts remain separate consumed strata.

**Consequence.** The candidate preserves the 1,944 denominator and does not retry or pool a historical attempt. It contains no new matched benchmark result.

**Status:** **VALID** source/accounting preparation; stage **NOT_RUN**.

**Required action.** Preserve all historical source, result, stop and GO bytes; retain 1,940 never-attempted IDs.

## Finding 2 — the R16 provenance mismatch is addressed at source/fixture level

**Evidence.** Both R17 adapters emit the five direct per-segment proof/snapshot/closure path-and-hash fields. The independent composition verifier reconstructs them from opened proof/source files and compares each segment. `source_identity` distinguishes R9 numerical-baseline source from the executing R17 worker/adapter/checker closure. The stored non-query report references byte-identical archived R15 proofs, native replay, positive R3 and Auer common paths, and twenty field-deletion/alteration rejections. Its fixture scope explicitly excludes producers, live guards and stages.

**Consequence.** The specific missing Auer path fields and misidentified adapter hash found in R16 are repaired in this candidate. The stored report is interface evidence, not a new Auer-vs-R3 comparison or an executed-stage proof.

**Status:** **VALID** narrowly for source/proof interface preparation; live-stage behavior **UNVERIFIED**.

**Required action.** Keep the R9 baseline and R17 execution identities separate in all subsequent records.

## Finding 3 — the full stage checker cannot replay declared class-3 partial stops

**Evidence.** `validation/g4/batch_stage_runner_v3_r17.py` catches a method exception, writes `STOPPED_CLASS3` when an invocation intent exists, and records partial-intent paths. But `validation/g4/check_matched_batch_v3_r17.py` rejects any such method with `method_terminal is None` in `validate_stage_artifacts`; it also requires both a worker guard and a result and calls final result validation before classifying a failed terminal. Thus an intentional stop after a durable intent but before a terminal, or a failed guard with no valid result, cannot be replayed as a valid stopped stage. The fixture calls the pure `validate_stop_accounting` helper only; it does not exercise `validate_stage_artifacts` on a stopped on-disk stage.

**Consequence.** The stage can consume an ID and produce a stopped receipt that its own independent checker rejects. Fail-closed execution is preferable to a false certificate, but the declared stop/partial-intent evidence contract is incomplete. This is relevant because the earlier R15 stage stopped on a class-3 path.

**Status:** **BLOCKER** for an exact-stage GO.

**Required action.** Version the checker/runner contract so a well-formed stopped stage is independently verifiable without accepting failed mathematical output. Include isolated, non-query on-disk fixtures for missing method terminal, failed guard/result, failed audit, and a fully completed pair; exercise the full stage-artifact checker rather than only the pure count helper. Keep all intents consumed and all later IDs unattempted.

## Finding 4 — GO and launcher resource checks need tighter binding

**Evidence.** `validate_go_receipt` checks a review file's prefix and raw hash, but does not verify that the review actually contains an exact-scope GO decision. A matching receipt could therefore reference a hashed NO-GO review file. The runner's method and audit launchers use `subprocess.run(..., stdout=subprocess.PIPE, stderr=subprocess.STDOUT)` and retain the entire launcher output before writing it. The 1 GiB/120-second policy applies to the guarded method/audit child, not to an explicit cap on the runner's captured output. The stage checker also parses result/guard/report JSON through unbounded `read_text()`.

**Consequence.** The receipt does not by itself establish the intended Codex decision, and malformed or excessive launcher/artifact output can exceed the reviewable resource envelope. No actual excessive output is claimed.

**Status:** **NEEDS REVISION** before execution.

**Required action.** Require an explicit exact-scope GO marker/decision bound to the reviewed manifest, closure, schedule and ten IDs. Bound launcher output capture and checker file reads before parsing, recording overflow or incomplete capture as a stopped class-3 outcome. Preserve one-shot/no-retry semantics.

## Gate disposition

**HOLD.** G1 remains PASS only for the restricted reduced model. G2/G3/G4 and physical-platform correspondence remain UNVERIFIED. R17 Stage 1, later stages, the full 1,944-query comparison, G3, and operational/hardware work are not authorized by this review.
