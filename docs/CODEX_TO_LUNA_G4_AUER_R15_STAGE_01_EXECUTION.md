# Assignment — DDWMR | LUNA-G4-AUER — one exact R15 matched stage

Read `AGENTS.md`, all four canonical `research_context` files, the R15 handoff/protocol and `docs/reviews/CODEX_G4_AUER_R15_EXACT_STAGE_GO_REVIEW.md` first. The review grants one ten-ID stage only. The exact machine decision is `docs/reviews/CODEX_G4_AUER_R15_EXACT_STAGE_GO_DECISION.json` (raw SHA-256 `0e7553a3f1134c00286bb0b7cc87807e429aadcee2090dd4f863e626681e9f97`). The canonical executable receipt is `results/validation/g4/auer2013/protocol_v3_r15_batch/authorizations/r15_continuation_01.json` (raw SHA-256 `017f36d5bca13daf08f19a7193c6e19d592cba344157e57e9f059b2d6119a017`). Codex's read-only exact-scope validator accepted the binding; no stage query was run.

Execute only **after the G2 R12 two-row run has finished or stopped**, so the two sessions do not compete for the same laptop's time and memory. Preserve all R9/R11/R12/R13/R14/R15 candidate and historical result bytes. Do not commit, push, clean, retry a historical ID or advance to a second stage.

1. Confirm the exact review/decision/receipt/source hashes, the same ten ordered IDs and that `stage_01` is absent. The GO receipt already exists in the `authorizations` directory. The pre-authorization `--verify-only` command expects that directory to be absent and is therefore not the launch precheck now; use the source-bound GO validator/read-only checks. Stop on any mismatch or pre-existing stage namespace.
2. Invoke `python -B -m validation.g4.batch_stage_runner_v3_r15 --project-root . --stage-id r15_continuation_01 --authorization-receipt results/validation/g4/auer2013/protocol_v3_r15_batch/authorizations/r15_continuation_01.json` **once**. Record command, exit code, raw stdout/stderr and start/end times. The runner may call R3 and then Auer once per scheduled ID under the pinned resource caps. It must halt on a class-3 stop; do not retry or replace an ID.
3. Replay the actual stage with the independent read-only R15 checker and composition audit receipts. Write the fixed-denominator summary outside the canonical batch root, for example under `results/validation/g4/auer2013/protocol_v3_r15_candidate/`, so the batch-root layout remains exact. Keep R9 preflight and R11 consumed observations separate; count the ten R15 IDs against the fixed 1,944-ID universe. Inspect the stage terminal's method/audit invocation counters: the read-only checker CLI's own `query_workers_invoked: 0` reports that the checker launched no workers, not that the stage launched none.
4. Report each matched pair's terminal class, native proof and common/audit replay status, resource/stop reason, all output hashes and any unresolved intent. If replay rejects or the stage stops, preserve raw bytes and report the blocker; do not restart. No later stage, full batch, novelty conclusion or gate promotion is authorized.

Return one detailed Markdown handoff for Codex review. Reply in exactly three short chat lines:

`Session: DDWMR | LUNA-G4-AUER`  
`Status: <DONE or BLOCKED; R15 attempted x/10; no later stage>`  
`Handoff: <absolute Markdown path>`
