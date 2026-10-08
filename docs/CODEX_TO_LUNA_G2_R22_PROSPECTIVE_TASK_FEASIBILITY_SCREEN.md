# Assignment — DDWMR | LUNA-G2-SCOPE — R22 prospective task-feasibility screen

Read `AGENTS.md`, all four canonical `research_context` files, MASTER v2.1 §§5–12, `docs/reviews/CODEX_G2_R21_PAIR_FEASIBILITY_ADVERSARIAL_AUDIT_REVIEW.md`, and the R21 handoff before research reasoning. The R17 indices 62/74 are retired as a strong task-selection target; preserve their records. This assignment is for a **new synthetic analytic screen**, not a query or a gate claim.

## Scientific question

Can two admissible held voltages, applied to the **same positive-width initial-state cell and the same joint execution-fixed parameter set**, have a provable separation in full-hold forward progress while both stay collision-safe and contact-admissible in the formal MASTER model?

Build an exploratory candidate around a declared operating point, with nonzero widths in the relevant body, wheel, current, and parameter coordinates. State the cell, parameter correlations, clip law, scene, horizon, and two actions explicitly before reporting any computed bounds. The R21 exact-rest point may guide the mathematics, but a singleton rest point is not the target. If you revise the candidate, retain the earlier candidate and reason for revision in an exploratory ledger. Do not inspect archived query outcomes to select it.

## Required analysis

1. Derive the coupled state evolution or rigorous differential inequalities directly from MASTER. Preserve the same hidden parameter value throughout each trajectory. Prove bounds over every initial state and parameter in the proposed joint cell, for every time in the whole hold. Handle contact-law saturation without assuming an unproved derivative.
2. For each action, give certified symbolic/rational bounds on terminal progress `J=p_x(T)-p_x(0)`, full-hold collision clearance, and full-hold contact margin. State assumptions and outward rounding. If a bound cannot be proved, report the precise obstruction; do not substitute a nominal trace or a solver `UNKNOWN` status.
3. Report whether the interval `J_baseline^+ < delta_task <= J_positive^-` is mathematically nonempty. This is a *possible threshold interval*, not a task specification. Do not choose `delta_task` from this interval and then claim decision relevance. If the interval is empty, determine whether that follows from true dynamics or only from conservative bounds.
4. Record the cell widths, progress-gap size, clearance/contact slack, and which actuator-to-slip-to-force dependency creates any action difference. Explain why the example is or is not more informative than the exact-rest screen. Flag all synthetic normalizations and missing physical provenance.
5. Recommend a single next decision: refine the analytic screen, request owner task/domain inputs, or stop this synthetic branch. Do not create a new manifest or IDs unless a separately declared task threshold and review authorize that step.

## Execution boundary

This is read-only/derivation work. Run **zero** native rows, workers, stages, retries, G4 comparisons, or 800-row study queries. You may use exact symbolic or rational arithmetic solely to check your derivation; retain the derivation and any script as exploratory source, not a certificate producer. Do not alter R17–R21/G4 evidence, commit, or push. G4 remains paused. Preserve **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED**.

Write a complete Markdown handoff under `docs/reviews/`. Reply to the user in exactly three short lines:

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE or BLOCKED; zero new native rows; R5 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
