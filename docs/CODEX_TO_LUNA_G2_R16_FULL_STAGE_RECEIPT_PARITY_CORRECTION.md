# Assignment — DDWMR | LUNA-G2-SCOPE — R16 full-stage receipt parity

Read `AGENTS.md`, all four canonical `research_context` files, the R15 handoff, and `docs/reviews/CODEX_G2_R15_RUNNER_CONTROL_FLOW_REVIEW.md` first. Prepare a **NO-GO correction candidate**. No real row, native query, R5 study, retry, commit or push is authorized.

The fixed development pair remains R5 indices **62 then 74** (`V_L0_R0` then `V_Lp1_Rp1` in `S_LOW_NEG__D_OFFSET_LEFT__T_250MS`). R15 is 0/2 real rows; R5 is 800/800 `NOT_RUN`. Indices 0, 12 and 24 remain consumed. Do not substitute a pair or interpret `UNKNOWN` as unsafe.

1. Correct the deterministic row-shape mismatch: the R15 runner omits five fields that its independent checker adds before exact receipt comparison. Establish an explicit exact row-receipt schema and make the runner's stored row and the checker's **independently recomputed** row match on every declared field. Keep R10 producer/R11 proof replay, the R12 paired truth table, and the R15 stop/summary rules unchanged.
2. Add isolated **non-query, on-disk full-stage fixtures** that reach the production receipt comparison through the actual runner/checker receipt functions for: a valid first row that permits the second; a resource/invalid first row that stops; and a completed two-row pair. Include a regression that rejects the unchanged R15 row shapes. Stubbed mathematical records must be labeled synthetic; do not call the R10 worker or place fixture intents under the canonical stage path.
3. Check the entire path for any other deterministic runner/checker field or status mismatch, including terminal hashes, transport summary, no-record and partial-intent cases. Keep file reads and diagnostic capture bounded, preserve partial evidence, and never retry a consumed intent.
4. Produce a fresh versioned R16 manifest, source closure, NO-GO template, sidecars and detailed Markdown handoff. Pin all changed executable and fixture bytes, preserve every R5/R6/R10–R15 source/result/intent byte, and show the exact selected IDs and hash ledger. Do not create an executable Codex GO or canonical R16 stage directory.
5. Report separately what the fixture proves and what remains unverified. A corrected candidate will receive a separate Codex review before any exact-scope GO; no 800-row study is authorized.

Reply to the user in exactly three short chat lines:

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE or BLOCKED; R16 0/2 real rows; R5 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
