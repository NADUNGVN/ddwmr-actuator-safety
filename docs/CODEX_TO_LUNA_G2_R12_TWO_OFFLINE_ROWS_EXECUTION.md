# Assignment — DDWMR | LUNA-G2-SCOPE — one R12 two-row offline execution

Read `AGENTS.md`, all four canonical `research_context` files, the R12 handoff/contract and `docs/reviews/CODEX_G2_R12_EXACT_SCOPE_GO_REVIEW.md` first. The exact machine decision is `research/benchmarks/G2_R12_CODEX_SCOPE_DECISION_v1.json` (raw SHA-256 `2c4d16c8d529c55222f49cc0c76cf66c9020b35ee527c1e2c2cfa7bb7d0c8bd5`). The review raw SHA-256 is `37bcabaf2e3d333f7bb8a1483d594279f33d098979514ae8c0be14fecdfc3519`. Both the production runner and public receipt checker accepted the decision binding in Codex's read-only review; no row was run.

Execute this assignment **once**, while the G4 stage is idle. Preserve all existing R3/R5/R6/R10/R11/R12 candidate source and result bytes. Do not commit, push, clean, run a native R6 query or start the 800-row R5 study.

1. Confirm the exact decision/review/source hashes and that `results/validation/g2/decision_domain_r12_whole_hold_picard_v1/` is absent. On any mismatch or pre-existing intent/result namespace, stop and report it; do not repair or retry in place.
2. Run the source-bound R12 stage only once, using `python -B validation/scripts/run_g2_r12_picard_stage.py --root . --authorization research/benchmarks/G2_R12_CODEX_SCOPE_DECISION_v1.json --stage-dir results/validation/g2/decision_domain_r12_whole_hold_picard_v1`. It is limited to offline R5 indices 12 then 24, at most two row calls, a 60-second hard timeout per worker, zero native-query calls and no retry. Save exact command, exit status, raw stdout/stderr and start/end times. A valid `UNKNOWN` is a completed abstention and may allow row 24; resource, invalid, timeout or interrupted outcomes stop the pair.
3. Run the **public read-only** `validation.g2.r12_execution_checker.audit_stage` on the canonical stage directory after the invocation, including if the process exits with a stop or error. Preserve and hash every file in the stage inventory. Report both producer and independent replay statuses, safety margins/progress only where a certificate actually exists, the bound truth-table outcome, and any partial intent or orphan artifact. Do not infer unsafety or task failure from `UNKNOWN`.
4. Do not start a broader study even if the sole strong paired trigger occurs. Return one detailed Markdown handoff for Codex review. If the stage stops or its receipt fails replay, report the exact evidence and leave the namespace untouched; no second invocation.

Reply in exactly three short chat lines:

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE or BLOCKED; R12 attempted x/2; R5 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
