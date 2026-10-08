# Codex review — G2 decision-domain R4 integrity candidate

**Date:** 2026-10-03  
**Handoff:** `docs/reviews/LUNA_TO_CODEX_G2_DECISION_DOMAIN_R4_INTEGRITY_CORRECTIONS_FULL_HANDOFF.md`  
**Authority:** MASTER v2.1 and `AGENTS.md`. Branch `main`, HEAD `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`; shared uncommitted tree preserved.

## Decision

**ACCEPT the R4 correction as a non-query source/fixture preflight. NO-GO to freeze or execute a G2 study query yet.** R4 closes the specific R3 defect in which arbitrary outcome flags could reach the selector, and corrects the byte-addressed input ledger. It has no sealed query runner or authorization receipt. The 800-row study remains **800/800 `NOT_RUN`**; G2 remains UNVERIFIED and overall HOLD remains.

## Finding 1 — exact candidate relation and source integrity

**Evidence.** I inspected the R4 adapter, worker, selector, proposal and handoff, then ran the source-inspected read-only R4 `--check-only` path. It returned `PASS_READ_ONLY`, with 57 source/input hashes verified, config raw SHA-256 `50cb4387eb436af4da903483299fc1b338820a86083ec35fd1bccfef2d5389db`, manifest raw SHA-256 `2036404e02c32da25eb94cee803da6be4723bc67b6e23d80189d5a0e1ea0113b`, and closure raw SHA-256 `b267d0963b2e8e7d51ba5dbe852f27d0b25a417be1b85b9ae1e1c4c4aee29fcc`. Direct JSON comparison found all 800 R4 row objects exactly equal to R3 v6, with every result null and status `NOT_RUN`. The proposal's corrected raw SHA-256 is `a302c144a919a1e4501afe973593bf479e8e93f7e66064e5375c6f96d97cbabf`.

**Consequence.** R4 changes result integrity plumbing while preserving the declared scientific query universe and native R3 v6 query context. This is source/input consistency evidence, not a query outcome.

**Status:** VALID for the exact unfrozen candidate bytes.

## Finding 2 — proof-enforced counting path

**Evidence.** `offline_study_r4.aggregate_candidate_result_bytes` reloads the candidate context, checks provenance and stream hashes, parses exact physical JSONL bytes, aligns rows to the 800 IDs, binds each row through the unchanged R3 adapter, calls native R3 `replay_record`, then creates and replays the R2 endpoint record. Only the resulting internal `VerifiedRow` values enter `decision_selector_r4._aggregate_verified_rows`; caller-provided eligibility/replay/lower-bound fields are rejected. The selector parses rationals defensively. Its zero-`UNKNOWN` coverage condition requires replayed proof or a checker-classified integrity-valid resource abstention; a nonzero certificate requires replayed `CERTIFIED` safety. The handoff's adversarial fixtures exercise forged success, rejected zero `UNKNOWN`, malformed rationals and fixed denominators without calling `run_query`.

**Consequence.** The public raw-byte-to-counter path no longer has the R3 arbitrary-dictionary acceptance defect. The private Python token is a code-path guard, not a cryptographic authorization mechanism; the source-bound raw-byte entry point and replay are the actual evidence boundary.

**Status:** ACCEPT in source/fixture scope. No 800-row task numerator exists.

## Finding 3 — ledger and bundle scope

**Evidence.** `_split_physical_lines` retains exact bytes, index, input byte offset and length, including blank/malformed/orphan/duplicate lines. `_verify_lossless_input_ledger` reconstructs the stream and reparses lines. The output writer stages four files and publishes by directory rename with an exact-hash completion marker; it refuses an existing destination. The reported overwrite and injected-partial-write fixtures passed in temporary space.

`verify_result_bundle` checks byte hashes, offsets, ledger consistency and completion status. It does **not** independently replay R3/R2 proofs from the published result bundle. Also, `write_result_bundle_once` accepts a result dictionary with the expected schema/status/800 rows; its own boundary does not establish that the dictionary came from `aggregate_candidate_result_bytes`.

**Consequence.** The bundle verifier establishes serialization/provenance consistency for a correctly produced aggregate. A future study artifact still needs a sealed runner that invokes the replay-enforcing entry point and an independent post-publication proof/count audit. A self-consistent `COMMIT.json` is not proof of scientific validity.

**Status:** VALID write-once integrity component; **remaining execution/audit obligation** before real results.

## Finding 4 — real-run and one-query boundary

**Evidence.** R4 v1 deliberately has no `sealed_study_runner_source`; the proposed one-query runner path does not exist. The R4 study provenance route rejects an unclosed runner. The versioned proposal selects index 0, `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1`, only for a later plumbing check and labels it outside the 800-row study. The full-study receipt currently requires `run_query_invocations=800`; when a future runner is designed, clarify how pre-call failures are represented while retaining all 800 attempted rows in denominators. The current 15-second evaluator check is cooperative.

**Consequence.** A proposal and checked preflight code are ready, but no source-bound execution path is ready to invoke a task query. A single query, even if later certified, cannot establish voltage-selection usefulness.

**Status:** **NO-GO to freeze/query.** Prepare and review a versioned one-query runner, receipt and independent published-output auditor first. No extra permission request is inferred from this preflight review; execution scope will be decided on the completed bytes under the user's existing validation mandate.

## Final disposition

R4 repairs the identified R3 aggregation, coverage and input-ledger faults in non-query scope. The next direct assignment is `docs/CODEX_TO_LUNA_G2_DECISION_DOMAIN_R5_ONE_QUERY_RUNNER_PREPARATION.md`. Preserve **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED**. No G3, controller, hardware work, commit or push.
