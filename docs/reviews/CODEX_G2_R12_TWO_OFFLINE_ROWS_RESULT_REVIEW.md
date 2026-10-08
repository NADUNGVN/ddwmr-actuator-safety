# Codex review — G2 R12 stopped two-row execution

**Date:** 2026-10-04  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G2_R12_TWO_OFFLINE_ROWS_EXECUTION_FULL_HANDOFF.md`  
**Disposition:** accept the stopped-stage accounting; **BLOCK** interpretation as a completed offline row or paired study. No repeat execution is authorized by this review.

I read `AGENTS.md`, the four canonical `research_context` files, the handoff, the R12 runner/worker/checker source, and the stored stage artifacts. I independently checked the raw SHA-256 of the stage receipt, row intent and terminal, and the captured runner stdout/metadata against the handoff. I did not invoke a row worker, query runner, fixture suite, or stage checker.

## Finding 1 — the stage is a valid record of an invalid worker attempt

**Evidence.** The single authorized R12 runner invocation wrote `row_00/intent.json` for R5 index 12, then a terminal with `outcome=INVALID_OR_INTERRUPTED`, `termination_reason=WORKER_FAILED`, `worker_exit_code=1`, `producer_status=NOT_COMPLETED`, and `checker_status=NOT_RUN`. There is no `record.json`. The independent public auditor's stored result is `receipt_valid=true`, `status=STOPPED_INVALID`, one consumed row intent, and zero native-query calls. The exact receipt, intent and terminal raw hashes match the handoff. Row 01, R5 index 24, has no intent or result. R5 remains 800/800 `NOT_RUN`.

**Consequence.** There is no Picard certificate, safety margin, progress result, or valid `UNKNOWN` from this attempt. The predeclared paired truth table returns `INCOMPLETE_NO_TRIGGER`; no broader study is authorized. The consumed row 00 cannot be retried or relabeled as unattempted.

**Status:** **VALID** stopped-stage accounting; **BLOCKER** for the R12 paired result.

**Required action.** Keep the stage and capture files byte-for-byte intact. Do not run row 01 in R12, rerun row 00, or start the 800-row study under the R12 GO.

## Finding 2 — the worker exception is not recoverable from retained diagnostics

**Evidence.** `validation/g2/r12_stage_runner.py` invokes the worker with `stdout=subprocess.PIPE` and `stderr=subprocess.PIPE`, but `_worker_invoker` returns only a termination label and exit code on failure. The temporary output directory is then removed. The captured top-level runner stderr is empty; it is not the worker's stderr. `validation/scripts/run_g2_r12_picard_row_worker.py` can exit 1 on an uncaught exception before writing its record. The retained R12 artifacts contain no worker diagnostic stream or exception text.

**Consequence.** `WORKER_FAILED` is established, but its underlying cause is **UNVERIFIED**. The elapsed time and exit code do not justify attributing it to a specific Picard, binding, resource, or operating-system defect. The prospective runner needs bounded, durable worker diagnostics before another real row is considered.

**Status:** **NEEDS REVISION** for diagnostic completeness; root cause **UNVERIFIED**.

**Required action.** Prepare a new, source-locked prospective runner/checker contract that persists bounded write-once worker stdout/stderr and binds their byte counts and hashes in the terminal, including failure and timeout paths. Audit the R12 worker path statically and report any provable cause separately from hypotheses. Use only non-query development fixtures for interface checks. Before any new real evaluation, predeclare fresh, never-attempted paired inputs and obtain a new exact-scope review; do not substitute R5 index 24 as a post hoc complete pair.

## Gate disposition

**HOLD**. G1 remains PASS for the restricted reduced model. G2/G3/G4 and physical-platform correspondence remain UNVERIFIED. The prior R12 GO was consumed by this stopped attempt; this review grants no execution authority.
