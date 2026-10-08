# Assignment — DDWMR | LUNA-G2-SCOPE — R17 exact two-row execution

Read `AGENTS.md`, all four canonical `research_context` files, the R17 handoff and `docs/reviews/CODEX_G2_R17_GO_ENTRYPOINT_CORRECTION_REVIEW.md` first. The exact GO decision is `research/benchmarks/G2_R17_CODEX_SCOPE_DECISION_v1.json`; its SHA-256 at issue is `314dcce10a10db9c862b99694e5b1cda6e72bcae27fdabaeefa17f105a6af30f`. The independent R17 GO validator accepted indices **62 then 74**. This authorizes one R17 stage only; the R5 800-row study remains unauthorized.

1. Before the run, verify the raw hashes of the review, GO, R17 manifest and source closure, the exact selected query IDs and hashes, CPython 3.12, and absence of `results/validation/g2/decision_domain_r17_go_entrypoint_correction_stage_v1`. Preserve the GO and source bytes. `validation/scripts/audit_g2_r17_candidate.py` is a **NO-GO unstarted audit** and is expected to refuse after the GO file exists; use the source loader and exact GO validator for this check.
2. Run `validation/scripts/run_g2_r17_picard_stage.py` **once** on the shared repository, with CPython 3.12. The stage invokes at most two source-bound offline R10 workers, in order 62 then 74. It may start 74 only if the fixed stop rule permits it after 62. Never retry an intent, substitute an index, run an R3 native query or start the 800-row study.
3. Avoid overlapping this live run with G4 R19 Stage 1 on the same laptop; complete one stage before starting the other so resource and timing records remain interpretable. This does not delay independent read-only review work.
4. After the run, independently call `validation.g2.r17_execution_checker.audit_stage()` in read-only mode and retain its exact output. Preserve stage authorization, all intent/terminal/record/diagnostic/receipt bytes and raw top-level stdout/stderr. If an exception leaves partial evidence, do not repair or rerun the consumed stage; report the exact exception, current artifact inventory and attempted/unattempted rows.
5. Return a detailed Markdown handoff with a hash ledger, worker/capture statuses, R11 replay outcomes, any certified collision/contact margins, the exact paired truth-table result, remaining R5 denominator, and limitations. A valid `UNKNOWN` is inconclusive; a synthetic fixture is not a certificate. No G2 PASS or physical claim follows from this run. Do not commit or push; do not edit G4 artifacts.

Reply to the user in exactly three short chat lines:

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE or BLOCKED; R17 attempted X/2; R5 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
