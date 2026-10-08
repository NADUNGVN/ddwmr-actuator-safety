# Assignment — DDWMR | LUNA-G4-AUER — R24 action-ordering prior-art audit

Read `AGENTS.md`, all four canonical `research_context` files, MASTER v2.1 §§20–23 and 28–31, the R23/R24 G2 handoffs and Codex reviews, and `docs/reviews/CODEX_G4_AUER_R23_PAIRED_METHOD_OVERLAP_AUDIT_REVIEW.md` before research reasoning. The Auer batch remains paused.

## Research question

R23's **generic paired-IVP/enclosure construction** is blocked as a standalone novelty claim. Is its more specific voltage-to-current-to-slip-to-force positivity-cone/action-ordering argument already an instance of established monotone-system, incremental comparison, positive-system, or differential-reachability theory under matched assumptions? What genuinely DDWMR/contact-specific theorem question, if any, survives that comparison?

## Required work

1. Extract the exact R23/R24 synthetic assumptions and the paired variables/inequalities used for `Delta J>1/25,000 m`. Distinguish the R23 analytic cone result from the generic 39-dimensional IVP representation. Record the R24 common-threshold counterexample and do not transform matched ranking into a task guarantee.
2. Search at most **five** closest primary full-text sources, starting with existing `LITERATURE_MATRIX.md` and `G4_MATCHED_PRIOR_ART_COMPARISON_v1.md` leads, then targeted monotone/incremental/positive-system sources as needed. For each, record full-text access, theorem/equation locator, assumptions on input ordering, cooperativity/sign pattern, fixed parameters and output monotonicity, and whether it yields R23's result directly, only after a nontrivial plant-specific transformation, or not at all. Unknown is not No.
3. Test the R23 cone against the strongest applicable source at equation level: identify its state transform, Metzler/cooperative or other order structure, domain restriction to the unsaturated clip branch, and heading/position output step. State precisely which step is generic and which step would require a new DDWMR-specific proof. Do not claim novelty merely because a source lacks a robot example.
4. Give one falsifiable contribution hypothesis **only if** it survives the source comparison; specify the assumptions, output, and what an existing theorem would or would not already imply. If no useful distinct theorem remains, say so and recommend stopping this analytic novelty branch. Do not select a new Auer workload or resource criterion from the preserved pilot.

## Execution boundary

This is read-only literature and equation analysis. Run **zero** Auer/R3/G2 native queries, workers, stages, retries, or batch entries. Do not implement a paired solver, modify preserved pilot artifacts, revise MASTER, start G3/hardware work, commit, or push. Keep **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED**.

Write one complete Markdown handoff under `docs/reviews/`. Reply in exactly three short lines:

`Session: DDWMR | LUNA-G4-AUER`  
`Status: <DONE or BLOCKED; zero new queries; Auer batch unchanged>`  
`Handoff: <absolute Markdown path>`
