# Assignment — DDWMR | LUNA-G4-AUER — R19 successful-arm binding correction

Read `AGENTS.md`, all four canonical `research_context` files, the R18 handoff and `docs/reviews/CODEX_G4_AUER_R18_STAGE_STOP_REPLAY_REVIEW.md`. Prepare a **NO-GO source candidate**. Do not run a real query, producer, live audit, matched stage, retry or full batch; do not commit or push.

R18 Stage 1 is 0/10. Preserve all R9–R18 source/result/GO/stop bytes, the four historical consumed IDs, and the exact 1,940-ID continuation order. The proposed first stage remains its first ten IDs.

1. Fix `batch_stage_runner_v3_r18.py::_write_method()` calling the undefined `_bound_result_references` on a `PASS` worker arm. Bind the helper explicitly and keep its bounded proof/common-file checks. Inspect the adjacent successful method and audit branches for other unbound symbols or deterministic runner/checker mismatches.
2. Add an isolated **non-query** fixture that actually reaches the production `_write_method()` successful guard/result branch with synthetic, source-labeled evidence. It must fail against unchanged R18 at the unbound-name point and show that the corrected branch reaches independent result validation without a `NameError`. Do not use a real producer or make a synthetic result appear to be a validated numerical proof. Retain the full stopped-stage replay, overflow/incomplete-capture and hashed NO-GO review refusal fixtures.
3. Produce a fresh R19 manifest, closure, schedule, protocol, sidecars and detailed Markdown handoff. Pin every changed executable/fixture byte, preserve the 525 inherited R17 dependency records and R18 lineage, and report 0 new queries, 0/10 new Stage 1 attempts and NO-GO pending separate Codex review. No executable GO or canonical batch directory may be created.

Reply to the user in exactly three short chat lines:

`Session: DDWMR | LUNA-G4-AUER`  
`Status: <DONE or BLOCKED; zero new queries; R19 first stage 0/10>`  
`Handoff: <absolute Markdown path>`
