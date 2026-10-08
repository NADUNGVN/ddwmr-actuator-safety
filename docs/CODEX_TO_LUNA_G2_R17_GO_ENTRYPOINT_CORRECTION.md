# Assignment — DDWMR | LUNA-G2-SCOPE — R17 GO entrypoint correction

Read `AGENTS.md`, all four canonical `research_context` files, the R16 handoff and `docs/reviews/CODEX_G2_R16_FULL_STAGE_RECEIPT_PARITY_REVIEW.md`. Prepare a **NO-GO correction candidate**. Do not run a real row, worker, native query, R5 study or retry; do not commit or push.

The fixed pair remains R5 indices **62 then 74**. R16 has 0/2 real rows; R5 remains 800/800 `NOT_RUN`. Preserve all R5/R6/R10–R16 source/result/intent bytes and the consumed development indices 0, 12 and 24.

1. Repair the production entrypoint contradiction: `load_r16_candidate()` currently rejects the GO file and stage directory that `run_stage()` and `audit_stage()` require. Separate the unstarted NO-GO preflight from source binding and authorized read-only replay. Keep exact GO hash/scope checks, write-once stage creation and no-retry behavior.
2. Add isolated, **non-query** entrypoint fixtures that exercise the actual candidate-loader → GO-validation → stage-audit path with a synthetic exact-scope decision and stage, and prove a missing or NO-GO decision refuses before stage creation. Do not place an executable GO or fixture intent at the canonical paths. The positive entrypoint fixture must fail on unchanged R16 and pass only after this correction. Keep R16 receipt-parity and R11 mathematical-replay boundaries explicit; no stubbed record is a safety certificate.
3. Inspect the production branch for other deterministic errors that the R16 synthetic receipt fixture bypassed. Record the exact outcome of every fixture, re-pin all changed executable/fixture/schema bytes in a new manifest and closure, and give a full Markdown handoff for Codex review. No real execution authority is conferred by this assignment.

Reply to the user in exactly three short chat lines:

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE or BLOCKED; R17 0/2 real rows; R5 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
