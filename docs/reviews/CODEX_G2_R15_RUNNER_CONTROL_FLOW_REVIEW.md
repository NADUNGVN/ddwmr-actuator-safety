# Codex review — G2 R15 runner control-flow candidate

**Date:** 2026-10-05  
**Reviewed handoff:** `LUNA_TO_CODEX_G2_R15_RUNNER_CONTROL_FLOW_CORRECTION_FULL_HANDOFF.md`  
**Disposition:** accept the R14 name-error and summary-transport corrections as source/non-query preparation; **NO-GO for both real rows**.

I read `AGENTS.md`, all four canonical `research_context` files, the R15 handoff, manifest, source closure, runner, checker, worker and stored fixture report. I independently recomputed all 167 R15 source-input hashes; all 143 inherited R14 tuples are unchanged. I did not run fixtures, the R10 worker, native queries, or a stage.

## Finding 1 — source and execution ledger

**Evidence.** The R15 manifest, closure and fixture report raw SHA-256 values match the handoff: `01e35cf5763caa486b3741f78e9dee658d73f9d5cba81f651f310227ee332ed8`, `6b7b178652fb6c17ebc518a571db105ba58b49e15f3351171bdf66d7b240b9c0`, and `1071bd5dbb1a53d3fad9224f97f02ceda249c1aedc62bbc22869c1a9b9f667d0`. The selected R5 indices remain 62 then 74. The canonical R15 stage and GO file are absent. The fixture reports zero worker and native-query calls.

**Consequence.** R15 is a distinct source candidate with no real row result. The R5 study remains 800/800 `NOT_RUN`; previously consumed development indices 0, 12 and 24 remain consumed.

**Status:** **VALID** source/accounting preparation.

**Required action.** Preserve the existing source, result and intent bytes. Do not promote a synthetic receipt to a mathematical record.

## Finding 2 — R14 name error is corrected, with limited fixture evidence

**Evidence.** `r15_stage_contract.py` defines `must_stop_after`; the R15 runner and checker import it. The production `run_stage()` calls `_execute_row_loop()`, which uses the bound stop rule. The stored non-query fixture reports continue/stop outcomes for injected rows and reproduces the old R14 `NameError`. R15 also makes the checker recompute whether bounded worker stdout contains a matching summary; a mismatched summary becomes `WORKER_FAILED` and `INVALID_OR_INTERRUPTED`.

**Consequence.** The specific R14 name error and the newly identified summary-status mismatch are addressed at source and synthetic control-flow level. These checks do not exercise a real producer record or the complete on-disk stage audit.

**Status:** **VALID** limited correction; real-stage behavior **UNVERIFIED**.

**Required action.** Retain the common stop rule and bounded diagnostic/status distinctions in the next candidate.

## Finding 3 — runner receipt and independent checker receipt cannot match

**Evidence.** `r15_stage_runner.py::_run_row` returns a row summary without `checker_safety_certified`, `checker_task_eligible`, `termination_reason`, `diagnostic_overflow`, or `capture_status`. Its `_build_receipt` stores that summary directly in `receipt["rows"]`. In contrast, `r15_execution_checker.py::_audit_row` returns those five additional fields. `audit_stage` feeds its longer rows into `_receipt` and compares the entire rebuilt object with the stored runner receipt (`receipt != expected_receipt`, line 689). The fixture only replays a separate synthetic receipt shape through `replay_fixture_receipt`; it does not compare the production `_build_receipt` output against `audit_stage` for an on-disk row.

**Consequence.** For any completed R15 row with a terminal, the runner and checker construct different receipt objects, even if the worker and R11 mathematical replay are valid. The runner's post-run audit therefore rejects its own receipt. A real attempt would consume an intent without producing an accepted stage result.

**Status:** **BLOCKER** for an exact-scope R15 GO.

**Required action.** Version a corrected source candidate. Define the exact production row receipt fields once as a contract, then have the runner record them and the checker independently derive and compare each field. Add an isolated non-query **full-stage receipt parity** fixture that reaches the real `_build_receipt`/`audit_stage` comparison for one valid row, a stopped row, and a complete pair; it must fail against the current R15 code. Do not call the real worker or create a canonical intent. Re-pin all changed source/fixture bytes and review the new candidate before execution.

## Gate disposition

**HOLD.** G1 remains PASS only for the restricted reduced model. G2/G3/G4 and physical-platform correspondence remain UNVERIFIED. No R15 row, R5 study, G3, operational controller or hardware work is authorized by this review.
