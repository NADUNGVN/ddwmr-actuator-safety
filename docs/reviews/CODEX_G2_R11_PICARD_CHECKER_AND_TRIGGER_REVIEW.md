# Codex review — G2 R11 Picard checker, trigger and one-shot stage

**Date:** 2026-10-04  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G2_R11_PICARD_CHECKER_AND_TRIGGER_CORRECTIONS_FULL_HANDOFF.md`  
**Disposition:** Accept the clip-interval correction and the predeclared two-action truth table in their limited source/contract scope. **NO-GO for the two real R11 offline row evaluations:** the authorization gate does not verify that its cited Codex review actually grants this exact stage.

I read `AGENTS.md`, all four canonical `research_context` files, the R10 review and R11 assignment, the R11 handoff/contract, manifest, closure, checker, binder, runner, independent receipt checker and authorization templates. This was a read-only source/artifact review. I did not run a fixture, offline Picard row, native query or R5 study.

## Finding 1 — source identity and execution state

**Evidence.** Independent raw SHA-256 checks match the R11 manifest `9ed8c4709c7b398702d73877bfe32c58ca7097777bab08ee7b67e3055cb8708a`, closure `6b4f1e144a7e9384e9c13f8e7edd8c67be41b97b3283f59de793886e32ae6f1e`, Picard checker `2a794e8f46c4b029331a2548dccd1948b78d3f5d5d7a96efa118d9353ba56f7e`, receipt checker `d613a3375d7c4c9de97392587195b09226c2d510da63ee8e81586acb350fe3a0`, and runner `3980452e08ac5453acff7d2fc446dee6dd6db181788e5cfd91bf00dc35476b5f`. All 186/186 closure source path/hash entries match live files; the closure sidecar matches the raw hash. The R11 result directory is absent. The handoff reports 17 synthetic Picard groups and nine synthetic stage-protocol fixtures; those suites were not rerun in this review.

**Consequence.** R11 is a prepared source-bound candidate, not a new safety or usefulness result. R5 remains 800/800 NOT_RUN; the two earlier R6 observations remain consumed and separate.

**Status:** VALID identity and stated non-execution scope.

**Required action:** Preserve the R3/R5/R6/R10 data and source bytes. Do not count synthetic fixtures as real-row certificates.

## Finding 2 — interval clip and decision rule

**Evidence.** `whole_hold_picard_checker_r11.py:58-63` computes the exact monotone image of `[a,b]` by clamping **both** endpoints, including intervals wholly above `+1` or below `-1`. The corrected function is used by the RHS at line 80 and contact reserve at line 195. The handoff's four full-record saturation cases are synthetic and all replay as `UNKNOWN`; they exercise producer/checker agreement without asserting safety. `r11_stage_binding.py:67-118` reconstructs all 36 ordered outcome pairs and accepts exactly one broader-study **preparation** trigger: positive action `CERTIFIED_TASK_ELIGIBLE` and nominal action `CERTIFIED_TASK_NOT_ELIGIBLE`. Positive-certified versus nominal `VALID_UNKNOWN` is explicitly inconclusive. The manifest contains this same table with one true trigger.

**Consequence.** The two mathematical/protocol defects identified in the R10 review are corrected. The conditional whole-hold Picard theorem remains conditional on sound interval RHS, positive denominators, fixed parameter labels and the reduced model. The truth table prevents an `UNKNOWN` result from being read as unsafe or task failure.

**Status:** VALID correction and predeclared rule in their declared scope; real-row usefulness UNVERIFIED.

**Required action:** Keep the rule locked before evaluating either real row. A later strong trigger may justify preparing a broader protocol only; it does not authorize that study or establish physical voltage necessity.

## Finding 3 — GO authorization can cite an unrelated or NO-GO review

**Evidence.** The production runner's `_validate_authorization` in `r11_stage_runner.py:165-193` checks `independent_codex_review.result == "ACCEPT"`, a nonempty review ID, a path inside the repository and a raw hash matching the cited file. It does **not** read that file for an exact R11 GO decision, candidate hashes, row IDs or a contradictory NO-GO disposition. The independent receipt checker repeats the same limited check in `r11_execution_checker.py:111-157`. The JSON schema defines only the self-reported `result`, `review_id`, `review_path` and `review_sha256_raw`. For example, a future GO-shaped authorization could cite the hash of the existing R10 review, which explicitly says NO-GO for the real rows, while setting its own `result` field to `ACCEPT`; these validators would not detect that contradiction if their other fields matched. The ninth stage fixture checks hash mutation, not review meaning or exact decision scope.

**Consequence.** The current template is inert and no real authorization exists, but the production gate does not enforce its promised independent exact-scope Codex decision. A later self-described GO object could start the two offline rows with an unrelated or NO-GO review link. This is an execution-authority defect, not a Picard proof defect.

**Status:** **BLOCKER** for two-row execution authorization.

**Required action:** In a versioned R12 candidate, require a separate machine-readable exact-scope review decision linked to review Markdown and bind the exact manifest, closure, checker, runner, receipt checker, ordered indices 12/24 and query/input hashes. Reject unrelated reviews and explicit NO-GO text with negative synthetic fixtures. Keep all checked-in decision/authorization templates non-executable; do not evaluate either row while correcting the gate.

## Final disposition

No R11 real-row result, 800-row study, voltage-usefulness conclusion or G2 PASS follows. No row execution GO is issued. Preserve **HOLD; G1 restricted reduced-model PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED**. The next G2 assignment is `docs/CODEX_TO_LUNA_G2_R12_EXACT_SCOPE_GO_BINDING_CORRECTIONS.md`.
