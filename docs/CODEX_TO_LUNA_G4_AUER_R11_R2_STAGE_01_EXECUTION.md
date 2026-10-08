# Assignment — DDWMR | LUNA-G4-AUER — R11 R2 Stage 1

Read `AGENTS.md`, all four canonical `research_context` files, `docs/reviews/CODEX_G4_AUER_R11_R2_STAGE_01_REVIEW.md`, the R11 R2 protocol and the exact stage authorization receipt at `results/validation/g4/auer2013/protocol_v3_r11_batch/authorizations/stage_01.json`.

The receipt authorizes **only `stage_01`**, eleven ordered IDs, R3 then Auer once per ID, one read-only composition audit per method, fixed caps and no retries/substitutions. Check source pins and the receipt before launch. Use the pinned Python runtime. Run `validation.g4.batch_stage_runner_v3_r11_r2` with `--stage-id stage_01`, the exact canonical authorization path and the canonical `results/validation/g4/auer2013/protocol_v3_r11_batch` output root. Do not launch Stage 2–7. Stop at the first nonvalid pair under the frozen protocol. Do not rerun a consumed intent or the R9 preflight.

After the stage stops or completes, run the read-only receipt/summary verification on the preserved records and write a full Markdown handoff under `docs/reviews/`. Record exact attempted IDs, R3/Auer statuses, proof and audit replay, resource evidence, any interruption, file hashes and the fixed 1,944-ID denominator. Keep `UNKNOWN` inconclusive. Report any code/source/hash mismatch before a query, with zero attempts. No comparison or gate claim follows from this stage alone. Do not commit or push; preserve the shared tree.

Reply to the user in only three short lines; keep all details in the handoff:

`Session: DDWMR | LUNA-G4-AUER`  
`Status: <DONE/BLOCKED and attempted Stage 1 IDs; no later stage run>`  
`Handoff: <absolute Markdown path>`
