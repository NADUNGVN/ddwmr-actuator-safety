# Assignment — DDWMR | LUNA-G2-SCOPE — R15 runner control-flow correction

Read `AGENTS.md`, all four canonical `research_context` files, the R14 handoff, and `docs/reviews/CODEX_G2_R14_SOURCE_BOUND_TWO_ROW_CANDIDATE_REVIEW.md` first. This is a **NO-GO correction assignment**. No real row, native query, 800-row study, retry, commit or push is authorized.

Current state: the R14 candidate has 0/2 real rows; the R5 study has 800/800 `NOT_RUN`. R5 indices 0, 12 and 24 are consumed development observations. The next pair remains the predeclared never-attempted indices **62 then 74**, with the exact query IDs and hashes in the R14 handoff. Do not select replacements or reinterpret an `UNKNOWN` result as unsafe.

1. Fix the deterministic `STOP_OUTCOMES` missing-name error in `r14_stage_runner.py` through a single source-bound definition. Audit the entire path from first row return through branch decision, second-row gating, receipt writing, and independent receipt replay for similar unresolved names or source-contract mismatches. Keep the existing R10 producer/R11 checker mathematics and the R12 truth table unchanged.
2. Add **non-query** control-flow evidence that reaches the actual stage-loop decision for: a valid first row that continues to row two; a resource/invalid first row that stops; and a complete two-row pair that creates a receipt and recomputes the paired decision. Use synthetic records or injected row outcomes in an isolated fixture namespace. Do not call the real R10 worker, create a canonical stage intent, or disguise a stub as native proof replay. Ensure the fixture would have rejected the current R14 missing-name defect.
3. Preserve bounded diagnostic capture, bounded checker reads, exact worker import closure, source-bound query payloads, one-shot intent and no-retry rules. Keep timeout, overflow, capture-incomplete, invalid and mathematical `UNKNOWN` outcomes distinct. If another actual execution blocker is found, report it rather than opening a real row.
4. Prepare a fresh **versioned R15 source candidate**, manifest, source closure, inert NO-GO template and hash sidecars. Bind the fixed pair, current source bytes and exact future GO path. Preserve every R5/R6/R10–R14 source/result/intent byte. The old R14 candidate remains a failed historical candidate and receives no GO.
5. Return one detailed Markdown handoff with the new hashes, what changed, fixture scope, consumed-ID ledger and explicit `0/2 real rows; 800/800 study NOT_RUN`. Do not issue an executable GO receipt or call `run_query()`.

Reply to the user in exactly three short chat lines:

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE or BLOCKED; R15 0/2 real rows; R5 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
