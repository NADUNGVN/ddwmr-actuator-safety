# Codex review — G4 Auer R18 stage-stop replay candidate

**Date:** 2026-10-05  
**Reviewed handoff:** `LUNA_TO_CODEX_G4_AUER_R18_STAGE_STOP_REPLAY_AND_GO_CORRECTION_FULL_HANDOFF.md`  
**Disposition:** accept the narrow source and non-query preparation; **NO-GO for R18 Stage 1**.

I read `AGENTS.md` and the four canonical `research_context` files earlier in this review, then inspected the R17 review, R18 handoff, manifest, closure, schedule, runner, checker and fixture source. Independent hash comparison found 549/549 closure inputs matching; the 525 R17 inherited dependency records are unchanged. The R18 manifest, closure and schedule raw hashes match the handoff (`22e95160333fcd0551b3ce83ecbaea3c91a2fb32cb988383c0ef02812b6f54bc`, `3b40c3feb3c2f2d5c44735e456a4176c606ffb4235f8f416bdf5dc2a83ed0bae`, `4051f7503d692395197481c673701930217286fd301953ffb026c338e76a0f48`). I did not run a fixture, producer, composition audit, query or stage. I did not modify source, create a GO, commit or push.

## Finding 1 — R17 source blockers are addressed at the declared non-query level

The R18 checker has on-disk branches for partial method/audit intents and failed guard, result or audit arms. It derives attempted IDs from durable method intents, checks the ordered prefix and suffix, and requires stopped stages to carry no safety conclusion. Its GO parser requires an explicit exact-scope `GO` block in the bounded hashed review file. The runner caps captured launcher stdout; the checker bounds its JSON reads and referenced-file hashes. The stored nine-case fixture report exercises these branches with synthetic stage records. The copied R3 and Auer positive proofs belong to different historical IDs and establish interface replay only.

**Status:** **VALID as source/non-query preparation only**. The full matched Stage 1 is still 0/10; the 1,944-query comparison has not run.

## Finding 2 — an unbound name stops every successful method arm

In `validation/g4/batch_stage_runner_v3_r18.py`, `_write_method()` calls `_bound_result_references(value, lock["project"])` at line 242 when the worker guard and artifact status are both `PASS`. That name is neither defined nor imported in the runner. It is defined only in `validation/g4/check_matched_batch_v3_r18.py` (line 937), where it is used by the checker. The runner catches the resulting `NameError` (lines 241–248) and writes `CLASS3_INDEPENDENT_RESULT_CHECK_FAILED` to the method terminal. A valid, successful worker arm would therefore be mislabeled class 3, after which Stage 1 stops and consumes an intent instead of producing an accepted matched pair. The nine stored non-query cases do not exercise this production runner branch; bytecode compilation cannot detect this name error.

**Status:** **BLOCKER for R18 Stage 1 GO**. Issuing a GO now risks consuming the first scheduled ID for a deterministic runner error, independently of the numerical method.

**Required action:** version a new candidate and bind the reference-check helper explicitly (or move it into a separately pinned shared module). Add a non-query production-path fixture that reaches the `PASS` guard/result branch in `_write_method()` without launching either real producer, fails against unchanged R18, and demonstrates that valid synthetic inputs reach the independent result validator instead of a `NameError`. Retain the stopped-stage and NO-GO refusal fixtures. Re-pin changed executable and fixture bytes, then request a separate Codex review before any Stage 1 run.

## Scope and gate disposition

The four historical consumed IDs remain separate; R18 proposes the same first ten of the 1,940 never-attempted continuation IDs. The canonical R18 output and executable receipt are absent. The runner and checker process-tree/memory enforcement limits disclosed in the handoff remain limitations; they do not explain or cure the deterministic name error.

**HOLD.** G1 remains PASS only for the restricted reduced model. G2/G3/G4 and physical-platform correspondence remain UNVERIFIED. This review authorizes no R18 query, retry, later stage, full batch, G3 or hardware work. `UNKNOWN` remains inconclusive, not unsafe.
