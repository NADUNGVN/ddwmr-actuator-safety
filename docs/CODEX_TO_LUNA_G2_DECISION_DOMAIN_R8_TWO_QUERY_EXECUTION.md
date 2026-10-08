# Assignment — DDWMR | LUNA-G2-SCOPE — exact R6 pilot

Read `AGENTS.md`, all four canonical `research_context` files, `docs/reviews/CODEX_G2_DECISION_DOMAIN_R7_STAGE_IMPLEMENTATION_REVIEW.md`, the R6 protocol and `research/benchmarks/G2_DECISION_DOMAIN_R6_STAGE_EXECUTION_RECEIPT_v1.json`.

The receipt authorizes **one run of the fixed two-row R6 development stage only**: first R5 index 12, voltage `(0,0)`; then index 24, voltage `(+1,+1)`. Check the source closure, receipt, pinned runtime, exact query hashes and empty canonical stage namespace before launch. Use only `validation/scripts/run_g2_decision_domain_r6_stage.py` with the pinned Python runtime. Ordinary replayable `UNKNOWN` does not prevent the second predeclared row. A hard failure, malformed record, resource stop or consumed intent ends the stage without retry or replacement. Do not run the 800-row study or any other native query.

Run the read-only auditor after publication. If publication is incomplete, preserve the stage and report the incomplete state without repairing or retrying it. Write a full Markdown handoff under `docs/reviews/` with two-row results, R3/R2 replay, endpoint progress, trigger evaluation, resource records, hashes, intent accounting and the unchanged 800-row study manifest. Treat this pair as development overlap, never independent confirmation. No G2 gate claim follows from it. Do not commit or push; preserve the shared tree.

Reply to the user in only three short lines; keep all details in the handoff:

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE/BLOCKED and pilot attempts out of 2; study remains 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
