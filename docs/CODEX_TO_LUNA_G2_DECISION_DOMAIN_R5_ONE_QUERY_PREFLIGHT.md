Session: DDWMR | LUNA-G2-SCOPE

# Codex → LUNA-G2-SCOPE — exact R5 one-query preflight

Read `AGENTS.md`, all four canonical `research_context/` files, `docs/reviews/CODEX_G2_DECISION_DOMAIN_R5_ONE_QUERY_RUNNER_REVIEW.md`, the R5 handoff and receipt template first. Work only in `D:/Research/Teacher_Vien/projects/ddwmr-actuator-safety`. Preserve the shared dirty tree, R2/R3/R4/R5 candidate bytes, archived R3 records and G4/Auer artifacts. Do not switch branches, clean, commit or push.

## Authorization boundary

Codex accepted the exact runner in `CODEX_G2_DECISION_DOMAIN_R5_ONE_QUERY_RUNNER_REVIEW.md`, raw SHA-256 `867a967c157040627a897ecb5c9889a3d0dfde7a2f34af4ae0e13620a1c073c9`, decision code `ACCEPT_R5_ONE_QUERY_RUNNER`. This assignment does **not** fill the runner's `user_authorization` receipt field. **Wait for a separate user-forwarded instruction that explicitly names** `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1` **and limits the native call to one.** Preserve that instruction verbatim, its UTF-8 SHA-256 and a truthful message/event reference. Never manufacture an authorization string from the template or this assignment. If the separate instruction is absent, stop at `NOT_RUN` and report the missing precondition.

The only eligible preflight is manifest index `0`, query ID `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1`. It is **outside** the 800-row decision-domain study. No second native call, alternate row, batch, G3, controller or hardware work is authorized.

## Before the native call

1. Recompute exact bytes for R5 config `8e2816468bf682290a91535857f2c3f9ad4ff2ba8be99ec5c77acc0ca19a6e19`, manifest `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b`, closure `53a923a0be15bd9be977040b996dc2104a763a061e2bad9ef848241a530a55e9`, sealed CLI `4a5885528a5c9aebab76ad38b3278a66e75cb44e5b90f6f5fc52fbd41b1fe66a` and accepted review hash above. Require all 74 closure entries and all nested R4/R3 bindings to match. Require canonical query hash `3668b9fb3bf30e11b8b177508f8b519855e8d4e96e33d7352335cbaea838db17` and native input-payload hash `dde72762c6a6feb8932d0d617c11cefbe271ecaba288bc6d282d8be19bcbb0a5`. The R5 handoff's config hash is a 63-character transcription error; use the actual 64-character hash above, also found in the config sidecar and template.
2. While the active authorization receipt is still absent, run the read-only R5 `--check-only` path and record its result. Confirm the one-query attempt marker, checkpoint and final output directory do not exist. If any exact-byte check fails, stop before creating the receipt or invoking the evaluator. Do not repair reviewed candidate bytes.
3. Only after receiving the separate exact user instruction, create the active receipt at the R5 template's declared runtime path as a new write-once file. Fill it from the verified template, accepted review hash and the **verbatim** user instruction. The receipt must authorize `ONE_QUERY_ONLY`, index 0 and maximum native calls 1. Record its raw SHA-256. Use the runner's read-only preparation path to confirm all preconditions without invoking `run_query`. Once the active receipt exists, the candidate builder's pre-authorization `--check-only` command is expected to reject it; do not interpret that expected state check as a reason to rewrite the candidate.

## One execution and audit

4. Invoke `python -B -m validation.scripts.run_g2_decision_domain_r5_one_query` **once**, with no arguments and no injected runner. Preserve the exact stdout, exit status, attempt marker and native-call checkpoint. If the marker is created, the one-call cap is consumed even if the call raises, times out cooperatively, output staging fails, or no final bundle appears. Do not retry or choose another output location.
5. If a final bundle is published, invoke the independent read-only R5 bundle auditor against that exact path. Record its full diagnostic and every bundle member's raw hash. If the auditor rejects, keep the raw bundle and rejection; do not recast it as a certificate. Keep `UNKNOWN`, resource and execution-failure outcomes distinct and inconclusive. The evaluator's 15-second timing is cooperative, not a hard outer deadline.
6. Report separately: user instruction/receipt binding, selected row and query hashes, whether a native call was **attempted**, whether it **returned**, raw safety status, R3 proof replay, R2 endpoint replay, auditor status, attempt/checkpoint/final-bundle status, elapsed time and source hashes. Keep the full 800-row study at **800/800 `NOT_RUN`** regardless of this one preflight. No task-usefulness, physical or gate claim follows from one row.

Write `docs/reviews/LUNA_TO_CODEX_G2_DECISION_DOMAIN_R5_ONE_QUERY_PREFLIGHT_FULL_HANDOFF.md` with Finding / Evidence / Consequence / Status / Required action. If the separate user instruction never arrives, report `STOP_NOT_RUN` and no native call. Do not commit or push.

**Reply to the user in only three short lines; put details in the handoff:**

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE or BLOCKED; one sentence; native call count; study 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
