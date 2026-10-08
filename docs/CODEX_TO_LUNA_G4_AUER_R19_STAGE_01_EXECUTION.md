# Assignment — DDWMR | LUNA-G4-AUER — exact R19 Stage 1 execution

Read `AGENTS.md`, all four canonical `research_context` files, the R19 full handoff, and `docs/reviews/CODEX_G4_AUER_R19_STAGE_01_REVIEW.md` first. The exact-scope GO receipt is `results/validation/g4/auer2013/protocol_v3_r19_candidate/authorizations/r19_continuation_01.json`. Its SHA-256 at issue is `1ef1e7acbbb4376117737e0b1d601dbb7dd20185ac70a772b41418b23048fa51`. The independent R19 GO validator accepted it for `r19_continuation_01` and exactly ten ordered IDs. This is Stage 1 evidence acquisition only; G4 and project HOLD do not change.

1. Before execution, read and verify the review/receipt hashes, the pinned candidate and source closure, the exact ten-ID order, the pinned runtime and the absence of the canonical R19 batch output directory. Do not change the review, receipt or source bytes. The `--verify-only` command is an **unstarted NO-GO preflight** and is expected to refuse once the valid GO receipt exists; use the exact GO validator instead.
2. Run the one-shot `validation.g4.batch_stage_runner_v3_r19` entrypoint for `--execute-stage r19_continuation_01` with `--authorization results/validation/g4/auer2013/protocol_v3_r19_candidate/authorizations/r19_continuation_01.json`. Use the pinned CPython runtime at `C:/msys64/ucrt64/bin/python.exe`. Do not launch any other stage, batch, retry or replacement ID. A failed/partial intent consumes its ID; stop at the first class-3 outcome.
3. Independently replay the produced R19 stage with `validation.g4.check_matched_batch_v3_r19` in stage-verification mode using the same authorization receipt. Preserve all raw stdout/stderr, intents, terminals, proof/result/common files, audit records and checker outputs. If the runner or checker fails, preserve the partial namespace and report the exact error without retrying.
4. Return a detailed Markdown handoff with the fixed 1,944 denominator, four historical consumed IDs separately, R19 attempted/completed/unattempted IDs, native and common outcomes per matched pair, composition replay, hashes, resource/timing records, and all stop reasons. Do not interpret `UNKNOWN` as unsafe or count synthetic fixtures as matched data. Do not commit or push; do not touch the independent G2 session's files.

Reply to the user in exactly three short chat lines:

`Session: DDWMR | LUNA-G4-AUER`  
`Status: <DONE or BLOCKED; R19 attempted X/10; no later stage>`  
`Handoff: <absolute Markdown path>`
