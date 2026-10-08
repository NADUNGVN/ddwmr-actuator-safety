# Codex review — G2 R14 source-bound two-row candidate

**Date:** 2026-10-05  
**Reviewed handoff:** `LUNA_TO_CODEX_G2_R14_SOURCE_BOUND_TWO_ROW_CANDIDATE_FULL_HANDOFF.md`  
**Disposition:** source and selection evidence accepted in its preparation scope; **NO-GO for either real row**.

I read `AGENTS.md` and all four canonical `research_context` files before this review. I inspected the R14 manifest, source closure, runner, worker, source binder, checker, fixture report, and the previous R13 review. I independently recomputed all 143 listed source hashes and the R14 manifest/closure raw hashes. I did not run a fixture, worker, query, or stage.

## Finding 1 — source identity and the predeclared pair

**Evidence.** All 143 source-closure entries match their current raw SHA-256 values. The manifest and closure hash to `5d6cd57cbb494c42ab4b2428af9ff6863fc9dc782cd461042dc35e6f01ef5b93` and `642323e50f9e9d610c99e4e5a8cd5139e35b6e73a2bd33a141131c4052008f46`. The manifest contains R5 indices 62 then 74, with query IDs `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_L0_R0` and `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_Lp1_Rp1`. The source binder explicitly preserves previously consumed indices 0, 12 and 24 and fails rather than substituting another pair. The R14 stage directory and GO decision file are absent.

**Consequence.** This is a source-bound, predeclared development pair. It supplies no executed decision or population-level usefulness evidence.

**Status:** **VALID** preparation; execution **NOT_RUN**.

**Required action.** Preserve the candidate and consumed-intent ledger. Keep the R5 study at 800/800 `NOT_RUN`.

## Finding 2 — deterministic runner failure after the first row

**Evidence.** `validation/g2/r14_stage_runner.py` line 309 evaluates `row_result["outcome"] in STOP_OUTCOMES`, but the module neither defines nor imports `STOP_OUTCOMES`. The set exists in `validation/g2/r14_execution_checker.py` line 31. Python compilation and the six stored non-query fixture groups do not resolve this name at runtime. The fixture report records zero worker calls and does not exercise the two-row loop.

**Consequence.** If the first worker returns a row result, the runner raises `NameError` before writing `receipt.json` or considering the second row. The first intent would be consumed without the intended stage receipt. This is an execution blocker, irrespective of the first row's mathematical outcome.

**Status:** **BLOCKER** for R14 execution.

**Required action.** In a new versioned source candidate, bind one shared definition of the stop outcomes and exercise both the continue-after-valid-result and stop-after-resource/invalid-result branches without a real query. Pin the changed runner and fixture bytes in a new manifest/closure. Do not run indices 62 or 74 under the current R14 candidate.

## Finding 3 — limits of the current fixture and checker evidence

**Evidence.** The worker entry point is pinned, uses the R10 producer and is launched with Python `-I -S`; the source-only import audit covers the local import closure. The R14 checker uses file-type and size gates before bounded reads, hashes source and stage files in chunks, and contains R11 record replay logic. The stored fixture report covers source selection, import closure, truth-table uniqueness, bounded JSON parsing, inventory rejection, and missing-GO refusal. It contains no real record, terminal, or paired outcome.

**Consequence.** These facts support interface preparation and fail-closed intent, but not a successful executed stage or a replayed certificate. The runner failure in Finding 2 prevents an exact-scope GO now.

**Status:** **VALID** limited preparation; real-stage behavior **UNVERIFIED**.

**Required action.** Add a non-query control-flow check that reaches the actual loop and receipt path. After a corrected candidate is independently reviewed, any execution decision must separately pin exact source hashes, indices 62/74, resource caps, no retry, and zero R5 study rows.

## Gate disposition

**HOLD.** G1 remains PASS only for the restricted reduced model. G2/G3/G4 and physical-platform correspondence remain UNVERIFIED. No R14 row, R5 study, G3 construction, operational controller, or hardware work is authorized by this review.
