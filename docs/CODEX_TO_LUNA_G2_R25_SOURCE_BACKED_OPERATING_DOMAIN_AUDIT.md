# Assignment — DDWMR | LUNA-G2-SCOPE — R25 source-backed operating-domain audit

Read `AGENTS.md`, all four canonical `research_context` files, MASTER v2.1 §§5–12 and 20–23, and `docs/reviews/CODEX_G2_R24_PAIRED_BOUND_AND_THRESHOLD_AUDIT_REVIEW.md`. This task needs no owner form and runs no native query.

## Research question

Is there a defensible **published or manufacturer-documented** DDWMR task and parameter envelope that could replace the arbitrary scale of the R22–R24 synthetic screens without silently changing MASTER's voltage/contact model? Find at most two candidate platforms/tasks and give a source-backed readiness decision. If none is sufficiently documented, report the exact missing evidence.

## Required work

1. Search primary manufacturer datasheets, platform manuals, and peer-reviewed full text. For each candidate, record source URL/DOI, access status, exact page/table/equation locator, units, and whether a value is measured, specified, inferred, or unknown. Do not fill unknowns by convenient defaults.
2. Build a provenance matrix for: mass, yaw inertia, wheel radius/track, wheel/motor inertia and damping, motor winding resistance/inductance, matched torque/back-EMF constant, terminal-voltage limit and driver semantics, sample/hold period, initial-state uncertainty, obstacle/footprint clearance, selected longitudinal traction shape/scale, and per-wheel effective tangential capacities. Record correlations and whether parameters can be treated as fixed over a hold or execution.
3. Identify at least one independently specified task metric if a source provides one: direction, required displacement or clearance, and deadline. Keep it separate from R22–R24's computed progress interval. Do not invent a threshold to make a certificate pass.
4. Compare each source model to MASTER's exact lateral constraint and algebraic contact domain. A friction coefficient, normal-load estimate, or empirical traction curve is **not** automatically MASTER's fixed `C_j` and exact force law. State what physical correspondence or model-error evidence would still be required.
5. Conclude for each candidate: (a) usable as a **synthetic/theoretical parameter stress benchmark with attributed scales**, (b) promising physical-correspondence candidate needing named measurements, or (c) unsuitable under current MASTER assumptions. Recommend one next G2 experiment or derivation only if its task and domain are prospectively specified; otherwise state the blocker.

Do not inspect saved R3/R17 query outcomes to choose favorable data. Do not modify the plant, fabricate measurements, build a controller, create a new query manifest, run a native row/worker/stage/retry/800-row study, or perform hardware work. Preserve R17–R24 and G4 artifacts. This is a research-source audit, not an implementation task. Do not commit or push. Keep **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED**.

Write one complete Markdown handoff under `docs/reviews/`. Reply in exactly three short lines:

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE or BLOCKED; zero new native rows; R5 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
