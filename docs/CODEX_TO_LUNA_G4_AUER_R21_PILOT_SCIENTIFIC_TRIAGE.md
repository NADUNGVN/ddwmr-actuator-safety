# Assignment — DDWMR | LUNA-G4-AUER — R21 scientific triage of the preserved pilot

Read `AGENTS.md`, the four canonical `research_context` files, `docs/reviews/LUNA_TO_CODEX_G4_AUER_R19_STAGE_01_EXECUTION_FULL_HANDOFF.md`, `docs/reviews/LUNA_TO_CODEX_G4_AUER_R20_PATH_BINDING_FULL_HANDOFF.md`, and `docs/reviews/CODEX_G4_AUER_R20_PATH_BINDING_REVIEW.md` first.

R20 is accepted only as a **retrospective read-only replay** of the ten preserved R19 Stage 1 pairs. The original R19 checker exited 2; R20 exited 0. The fixed universe is 1,944 IDs; four historical IDs and the ten R19 IDs are consumed, leaving 1,930 never attempted. This assignment grants **no new execution authority**.

1. Analyze the ten preserved matched pairs directly from their saved machine-readable artifacts. For every pair, report R3 and Auer native/common/final outcomes, the exact `UNKNOWN` reasons, collision/contact margins when present, proof bytes, and measured worker and composition-audit wall time and memory. Define each cost measure and keep worker time distinct from later offline audit time. Retain exact query IDs and hashes; do not treat ten deliberately selected IDs as independent statistical samples.
2. Explain the descriptive pilot result: R3 certified 6/10, Auer certified 9/10, with three Auer-certified/R3-unknown pairs and no reverse pair in this stage. Identify which R3 bounds caused those `UNKNOWN` outputs and whether the difference follows from shared assumptions and the declared common predicate. `UNKNOWN` is inconclusive, never unsafe. Do not tune either method or change a threshold after seeing these outcomes.
3. Give a scientific stop/go recommendation for a **future prospective** comparison. State what question additional IDs would answer, which result could support a DDWMR-specific contribution, and what result would strengthen the existing novelty/usefulness blocker. If continuation is justified, specify the minimum prospective runner/checker/source-closure and Windows reparse/junction guard work required before a separate exact-scope GO. This document must not itself authorize a stage or the full batch.
4. Store the analysis script if one is used, its exact input artifact references, and a full Markdown handoff in `docs/reviews/`. Preserve all R19/R20 bytes. Run no query, producer, worker, composition audit, stage or batch; do not retry or substitute an ID; do not commit or push.

Reply to the user in exactly three short chat lines:

`Session: DDWMR | LUNA-G4-AUER`  
`Status: <DONE or BLOCKED; zero new queries; R19 10 consumed; 1,930 never attempted>`  
`Handoff: <absolute Markdown path>`
