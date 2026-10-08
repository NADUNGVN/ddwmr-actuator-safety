# Assignment — DDWMR | LUNA-G2-SCOPE — R23 action-gap scaling research

Read `AGENTS.md`, all four canonical `research_context` files, MASTER v2.1 §§5–12, and the R22 handoff and Codex review. This is a **synthetic method-stress study** that needs no owner task form. It must not be described as practical task validation.

## Scientific question

How quickly does the R22 robust voltage distinction disappear as the initial-state and fixed-parameter cells widen, and can a sound **paired-action** enclosure retain the shared-state/shared-parameter dependence that the two separate scalar tubes discard?

## Frozen exploratory family

Use R22's clip law, parameter maps, obstacle, `T=1/4`, and held actions `V_+=(1,1)` and `V_0=(0,0)`. Before deriving outcomes, declare the symmetric cells `X_0(eta)=[-eta,eta]^9` and `Theta_lab(eta)=[1-eta,1+eta]^12` for the complete fixed grid `eta in {10^-6,10^-5,10^-4,10^-3,10^-2}`. Preserve `J_j=1/rho_j` and one unchanged hidden parameter label vector per trajectory. Both actions start from the **same** state and parameter realization in each paired comparison. Do not inspect archived R3/R17 outcomes to select a grid point.

## Required work

1. Derive the exact width limit of **R22's existing scalar comparison** for `J_+^- > J_0^+`, accounting for the domain and outward constants that remain valid as `eta` changes. Give a proof or an explicit point where its assumptions fail; do not merely extrapolate the `eta=10^-6` numeric result.
2. Derive a sound comparison for `Delta J(x_0,vartheta)=J_+(x_0,vartheta)-J_0(x_0,vartheta)` using shared initial state and execution-fixed labels. Preserve the voltage-to-current-to-wheel-to-slip-to-force chain. If the clip's linear branch or monotonicity is used, prove that the entire considered paired tubes remain in that branch and identify this as an R23 case-specific property of `clip`, not a MASTER-wide assumption.
3. For every grid width, report separately: (a) whether both actions have proven whole-hold collision and contact margins; (b) the two **separate** progress intervals and whether `J_+^- > J_0^+`; and (c) any paired lower bound on `Delta J`. A positive paired bound means action ordering for each matched realization; it does **not** by itself give one common task threshold across the whole cell.
4. Show the first width where each proof loses separation, and identify whether the obstruction is a true counterexample, a domain failure, or conservatism of the chosen enclosure. Quantify the effect of initial-state versus parameter width where the derivation permits it. Avoid extrapolating a failed sufficient bound into actual task failure.
5. Conclude whether this structure-preserving direction merits a prospective certified evaluator. If the paired bound cannot be made sound, stop at the exact failed inequality and report it. Do not spend the handoff on protocol/runner preparation.

This family is exploratory and synthetic. There is no owner-declared `delta_task`, physical-platform mapping, or claim of practical usefulness. Keep the R17 consumed rows and R22 evidence unchanged. Run **zero native queries, workers, stages, retries, 800-row study entries, and G4 comparisons**. Exact symbolic/rational arithmetic used solely to check a derivation is allowed; provide any script and its inputs as exploratory source, not a certificate producer. Do not commit or push. Preserve **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED**. G4 remains paused.

Write a complete Markdown handoff in `docs/reviews/`. Reply in exactly three short lines:

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE or BLOCKED; zero new native rows; R5 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
