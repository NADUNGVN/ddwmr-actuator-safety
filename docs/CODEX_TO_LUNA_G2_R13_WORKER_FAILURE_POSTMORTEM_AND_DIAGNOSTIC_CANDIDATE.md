# Assignment — DDWMR | LUNA-G2-SCOPE — R13 worker-failure postmortem

Read `AGENTS.md`, all four canonical `research_context` files, the R12 execution handoff, and `docs/reviews/CODEX_G2_R12_TWO_OFFLINE_ROWS_RESULT_REVIEW.md` first. This is a **prospective diagnostic and contract-correction assignment**, not execution authority.

1. Preserve the entire R12 stopped namespace, its external captures, all R3/R5/R6/R10/R11/R12 source and results, and all G4 files byte-for-byte. The R12 row-00 intent was consumed. Do not rerun it, invoke row 01 under R12, call native `run_query`, or start any R5 study row. Do not commit or push.
2. Perform a source-only postmortem of `run_g2_r12_picard_row_worker.py`, `r12_stage_runner.py`, the source-bound query loader and `time_slab_picard_r10.py`. Distinguish a proven deterministic defect from a hypothesis. The current artifacts show exit code 1 but omit worker stderr; do not invent the exception.
3. Prepare a **new versioned** runner/terminal/independent-checker candidate that durably captures bounded raw worker stdout and stderr on success, nonzero exit, timeout and interruption. Bind actual byte counts, caps and raw SHA-256 to write-once terminal evidence. Define an explicit overflow outcome and avoid unbounded in-memory `subprocess.PIPE` accumulation. Make the public read-only checker reject missing, extra or mismatched diagnostic artifacts and preserve partial intent accounting.
4. Prepare non-query interface evidence for worker failure and timeout paths. Any illustrative synthetic input must be labeled a fixture, never a real R5 result. If a prospective paired study is designed, select **two never-attempted R5 inputs by a declared deterministic rule before seeing their outputs**, in a fresh manifest/namespace. R5 index 24 alone cannot complete the consumed R12 pair. Do not run a prospective real row or issue a GO receipt; Codex will review a frozen candidate first.
5. Return one Markdown handoff with exact source/artifact hashes, the identified or unresolved root cause, diagnostic-capture contract, independent-checker behavior, preserved consumed-ID ledger and proposed next decision point. Keep G2 UNVERIFIED and overall HOLD.

Reply in exactly three short chat lines:

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE or BLOCKED; zero new real rows; R5 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
