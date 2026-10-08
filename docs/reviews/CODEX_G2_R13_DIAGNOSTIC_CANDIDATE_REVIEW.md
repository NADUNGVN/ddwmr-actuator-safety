# Codex review — G2 R13 worker diagnostic candidate

**Date:** 2026-10-04  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G2_R13_WORKER_FAILURE_POSTMORTEM_AND_DIAGNOSTIC_CANDIDATE_FULL_HANDOFF.md`  
**Disposition:** accept the R12 postmortem and R13 synthetic diagnostic transport in their stated scopes; **NO-GO for any real row**.

I read `AGENTS.md`, the four canonical `research_context` files, the handoff, R13 capture/runner/checker source, contract, schemas, manifest and stored fixture report. I independently checked all 18 source-input and 12 audit-evidence path/size/SHA-256 entries in the R13 closure, plus the manifest, closure and final fixture-report hashes. I did not rerun fixtures, workers, queries or checkers.

## Finding 1 — R12 diagnosis has the right limit

**Evidence.** The R12 runner captures child stdout/stderr in `subprocess.PIPE`, returns only `WORKER_FAILED` and exit code 1 after a nonzero exit, and deletes its temporary worker directory. The retained outer stderr is empty and is not child stderr. No R12 `record.json` exists. The R13 handoff preserves the exact four-file R12 stage inventory and reports zero new real rows. R5 remains 800/800 `NOT_RUN`.

**Consequence.** The diagnostic-loss defect is established. The exact exception behind R12 row 00's exit code 1 remains **UNVERIFIED**. The R12 intent is consumed; R12 row 01 has no R12 attempt, while its R5 index 24 was already used in the earlier R6 diagnostic stage.

**Status:** **VALID** postmortem; row-level cause **UNVERIFIED**.

**Required action.** Preserve R12 and R6 bytes. Never retry indices 0, 12 or 24 as fresh development observations under this line of work.

## Finding 2 — R13 captures bounded diagnostic prefixes in synthetic fixtures

**Evidence.** The new capture source drains two pipes concurrently in 4,096-byte chunks, stores at most 65,536 bytes per stream using exclusive files, and records observed/captured byte counts, hashes, overflow, exit/timeout and capture-completeness fields. The runner writes an intent before process creation and a terminal afterward; the checker independently reads the stored prefixes and recomputes their raw hashes. It rejects missing, extra, symlinked and mismatched artifacts in its declared fixture namespace. The stored fixture report claims 13/13 expected groups passed in temporary synthetic directories, including nonzero exit, timeout, overflow, partial intent and tampering. Its raw hash matches the source closure. The runner has no production-row CLI or source-bound real-row GO path.

**Consequence.** R13 provides credible fixture-level evidence for preserving diagnostics on the failure path that R12 lost. A hash over drained bytes after the retained prefix is a producer diagnostic: the independent checker can recompute the stored-prefix hash, but cannot reconstruct discarded tail bytes. The 13-group report is stored evidence that I inspected and hashed, not a suite I reran.

**Status:** **VALID for synthetic interface preparation**; real-row integration **UNVERIFIED**.

**Required action.** Keep R13 fixture-only and its manifest `NOT_AUTHORIZED`. Do not promote this transport to a DDWMR certificate or infer the R12 exception from the synthetic cases.

## Finding 3 — production resource and source binding remain open

**Evidence.** `r13_execution_checker._inventory` currently calls `read_bytes()` on every inventoried file before a size gate. A tampered large artifact could make the read-only checker itself consume unbounded memory. `r13_worker_diagnostics._terminate` terminates the direct child on Windows; `CREATE_NEW_PROCESS_GROUP` alone is not a proof of descendant-process containment. The fixture runner binds an arbitrary fixture argv hash, and its terminal deliberately carries no producer record. It is not connected to the exact R5 manifest, R10 Picard record replay, authorization marker, or a real two-row stage. No prospective pair was selected.

**Consequence.** These gaps do not invalidate the declared synthetic fixture result, but they block a production GO. A future real-row checker must cap its own reads and replay the mathematical record, not only the diagnostic transport. A future worker launch must either constrain the bound worker to a single process or enforce a process-tree resource boundary.

**Status:** **NEEDS REVISION** before any real-row execution.

**Required action.** Prepare a new versioned source-bound candidate with bounded checker inventory/hash reading, exact worker/process containment semantics, real record persistence and independent Picard replay. Predeclare a fresh pair from never-attempted R5 IDs and lock its hashes before obtaining a separate exact-scope review. This review grants no GO.

## Gate disposition

**HOLD**. G1 remains PASS for the restricted reduced model; G2/G3/G4 and physical-platform correspondence remain UNVERIFIED. No G3 or operational implementation follows.
