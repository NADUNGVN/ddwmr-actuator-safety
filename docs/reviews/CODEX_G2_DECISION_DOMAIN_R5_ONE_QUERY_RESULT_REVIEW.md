# Codex review — G2 R5 one-query preflight result

**Date:** 2026-10-03  
**Session reviewed:** `DDWMR | LUNA-G2-SCOPE`  
**Handoff:** `docs/reviews/LUNA_TO_CODEX_G2_DECISION_DOMAIN_R5_ONE_QUERY_PREFLIGHT_FULL_HANDOFF.md`  
**Authority:** MASTER v2.1 and `AGENTS.md`.

## Decision

**Retain the one attempted query and its replayable UNKNOWN bundle as diagnostic evidence. Reject the active receipt as a verbatim authorization transcript. NO-GO to retry, repair the receipt in place, or count this as a study row.** The handoff reports an explicit user one-call instruction, but I have not independently authenticated the original conversation event from the repository. The 800-row decision study remains **800/800 `NOT_RUN`**. G2 remains UNVERIFIED.

## Finding 1 — exact-text provenance defect

**Evidence.** The handoff quotes a one-call user instruction for `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1`. UTF-8 SHA-256 of that *handoff quotation* is `13e209f5a3f0de042998618b4703b9fc379b40a3b6ab8f5041dddbae20ade1b6`. The original conversation event is not a repository artifact independently available to this review. The active write-once receipt at `research/benchmarks/G2_DECISION_DOMAIN_R5_ONE_QUERY_FREEZE_AUTHORIZATION_RECEIPT_v1.json` contains ASCII `?` in place of Vietnamese diacritics. Its recorded hash `4e5e84ad4357445ad9fb622fa2ae0301bde88e43d18d8a2de86772a4b1871a2f` correctly hashes that damaged string, not the handoff quotation. I recomputed both hashes and confirmed the strings differ. The receipt's raw hash is `5672096c8c3c636dd51bef77f109bc7496cb410dfb82b49a00aa776ae51d62d0`.

**Consequence.** The stored receipt is self-consistent but does not satisfy the assignment's verbatim user-message binding. The one-call authorization was consumed; changing this receipt would erase the record of what the runner actually accepted.

**Status:** BLOCKED for exact-text receipt provenance; the handoff reports one authorized call, but this review cannot authenticate the original message from the repository. No evidence of a second call appears in the bundle.

**Required action:** Keep the original receipt unchanged. Attach a separate, clearly labeled provenance erratum citing the exact user message and both hashes if later reporting needs the discrepancy; do not present the erratum as a repaired original receipt. Diagnose the text-encoding step without running another query.

## Finding 2 — bundle integrity and scientific outcome

**Evidence.** I recomputed the raw SHA-256 of the nine payload members listed in `results/validation/g2/decision_domain_r5_one_query_v1/COMMIT.json`; all nine match. The safety record and endpoint record hashes match the handoff (`aa12f85b94b41d2f267be985ae93e8fc3abe73c97936add4504f7072bd072c23` and `b81b408e7d446dc3af1eb69b757418a872d425d985cd076caeb2adf1d5cb58d6`). The stored independent auditor reports `PASS_READ_ONLY_PROOF_REPLAY`, one native call attempt, R3 and R2 replay, and no study-row change. I did not rerun the producer or proof checkers. The safety result is `UNKNOWN` with negative collision and contact sufficient-margin bounds; the R2 endpoint status is `PROGRESS_BOUND_ONLY_SAFETY_UNKNOWN` and `task_eligible=false`.

**Consequence.** This is a traceable inconclusive diagnostic for the exact preflight query. Negative sufficient bounds do not prove collision or contact failure. The replay report does not cure the authorization-text defect.

**Status:** Artifact hashes VALID; stored replay PASS as reported; safety and progress UNVERIFIED for this query.

**Required action:** Preserve the bundle. Label it `one-query preflight, UNKNOWN, provenance caveat` in any synthesis.

## Finding 3 — study isolation and next G2 work

**Evidence.** The R5 candidate manifest has exactly 800 records, all `NOT_RUN`, with `task_rows_not_run=800`, `query_status=NOT_RUN` and `evaluated=false`. The one-query bundle says `study_result=false` and `study_row_attempt_count=0`. The R3 timing limit was cooperative rather than a hard outer timeout.

**Consequence.** This preflight does not demonstrate decision-relevant voltage usefulness, task progress, a general G2 certificate, or runtime feasibility under a hard cap. A further real query would need a fresh separately reviewed one-shot path and authorization; the consumed receipt cannot be reused.

**Status:** 800/800 study rows NOT_RUN; G2 UNVERIFIED.

**Required action:** Prepare a read-only provenance erratum and encoding diagnosis, then a separately versioned next-query plan that treats this UNKNOWN as a diagnostic. No G2 study run is authorized by this review.

## Final disposition

**One call consumed; bundle retained; verbatim receipt provenance rejected; no retry.** Preserve **HOLD; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED**. The next assignment is `docs/CODEX_TO_LUNA_G2_DECISION_DOMAIN_R6_PROVENANCE_AND_NEXT_QUERY_PLAN.md`.
