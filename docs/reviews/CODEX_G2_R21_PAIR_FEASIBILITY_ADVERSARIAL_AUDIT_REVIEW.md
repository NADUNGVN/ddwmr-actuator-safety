# Codex review — G2 R21 pair-feasibility adversarial audit

**Date:** 2026-10-06  
**Reviewed handoff:** `LUNA_TO_CODEX_G2_R21_PAIR_FEASIBILITY_ADVERSARIAL_AUDIT_FULL_HANDOFF.md`  
**Disposition:** **ACCEPT** the exact R17 counterexample and its limited consequence. **BLOCK** indices 62/74 as the locked strong task-selection challenge. No new execution GO or gate promotion.

I read `AGENTS.md`, the four canonical `research_context` files, the R21 assignment and handoff, the R20 review, MASTER v2.1 §§5–11, the exact R17 manifest, and the saved R17 records. This was a read-only mathematical and artifact review. I ran no native query, worker, stage, retry, or study row and did not alter archived records.

## Finding 1 — Exact witness belongs to both locked cells

**Evidence.** The R17 manifest has SHA-256 `a4913d3d0282de6a5d1a16c4c88e3c402a91f1c3dee2df1ea99afd44a71c6bb9`. Its ordered rows bind R5 indices 62 and 74 to the same state cell, twelve-label parameter cell, obstacle, horizon `T=1/4`, and task threshold `1/20 m`; only the held voltages differ: `(0,0)` and `(1,1)`. The state `x_0=(0,0,0,1/5,0,0,0,0,0)` lies in the displayed state box. Every label interval contains `1`, so setting all twelve labels to `1` gives the stipulated fixed model parameters equal to `1`. The two saved record hashes match R21: `316434ab6eacb7e221eca4feb1062001a8b576b450b725bbc1246d5e744f5cf3` and `fbb23303ff218e3ddf56453ccea7ca41a70d40f0ff1e85335341eff7e5651421`. Their raw status is `UNKNOWN`; the earlier independent replay classified each as `VALID_UNKNOWN`.

**Status:** **VALID.** The witness is a single allowed initial state and one execution-fixed parameter realization, sufficient to refute a proposed *uniform* task lower bound.

## Finding 2 — The task counterexample is mathematically sound

**Evidence.** MASTER's symmetric equations preserve `r=theta=0` and equal wheel/current states. For `V=(1,1)` and `d=u-w>0`, the clip stays linear because `0<d<=u<=1/5<1`. Direct substitution into MASTER §§8–11 gives

\[
\dot u=-u-2d,\quad \dot w=i+u-2w,\quad
\dot i=1-i-w,\quad \dot d=-4d-i.
\]

The first-exit argument is closed: the `w=0` and `i=0` boundaries point inward, `u=w+d>0`, and `i(t)<=t`. Variation of constants, `e^{-1}>1/3`, and `t<=1/4` yield

\[
d(t)\ge \tfrac15e^{-4t}-\tfrac{t^2}{2}
>\tfrac1{15}-\tfrac1{32}=\tfrac{17}{480}>0.
\]

Hence `u'<=-17/240` and the exact kinematic identity gives

\[
J_{(1,1)}=\int_0^{1/4}u(t)\,dt
\le \tfrac1{20}-\tfrac{17}{7680}
=\tfrac{367}{7680}<\tfrac1{20}.
\]

For `V=(0,0)`, MASTER's energy identity has `E(0)=1/50`, `E'(0)=-3/25`, and `E'<=0` because the clip is sign-preserving. Consequently `E(t)<1/50` for every `t>0`, so `|u(t)|<1/5` and `J_{(0,0)}<1/20`. The same symmetric trajectories have zero yaw and lateral demand. Their slips stay strictly inside the clip limit and each has positive formal contact reserve. Their horizontal distance from the obstacle center exceeds its `3/50` radius throughout the hold. These last statements concern the **single witness trajectory under each action**, not safety of either entire query cell.

**Status:** **VALID.** Both true trajectories miss the locked task threshold; neither is shown unsafe.

## Finding 3 — Exact scope of the blocker

**Consequence.** `CERTIFIED_TASK_ELIGIBLE` for the positive action requires a checked full-hold safety proof and an all-cell progress lower bound at least `1/20 m`. One admissible positive-action trajectory has true progress below that value. Thus no sound evaluator can achieve the locked positive-arm outcome for unchanged R17 indices 62/74. Refining its enclosure cannot repair this task infeasibility. The archived `VALID_UNKNOWN` outcomes remain valid and unchanged. The defined `CERTIFIED_TASK_NOT_ELIGIBLE` label is only a sufficient-certificate outcome; failure of its lower bound alone would not prove actual task failure.

**Status:** **BLOCKER for this consumed pair's strong task-selection claim.** It is not a G2 impossibility result, an unsafety finding, or a statement about a different voltage pair or task.

## Finding 4 — Prospective rest screen

**Evidence.** R21's separate nominal rest calculation is internally consistent. For the single rest point with labels `1`, positive voltage gives `q=w-u` and `u'=2q-u`, `q'=i-4q`, `i'=1-i-u-q`. Its nonnegative bootstrap yields `i<=t`, `q<=t^2/2`, `u<=t^3/3`, then `i'>=137/192` through `T=1/4`. The resulting rational bounds are

\[
\frac{685}{4718592}\le J_{(1,1)}\le\frac1{3072},
\qquad J_{(0,0)}=0.
\]

**Consequence.** This screens only a synthetic nominal point. It supplies neither a positive-width all-cell result nor a task threshold chosen independently of the computed progress. In particular it cannot replace the R17 threshold or establish practical voltage-selection usefulness.

**Status:** **VALID as a nominal analytic screen; usefulness UNVERIFIED.**

## Required action and project status

Retire the **consumed** R17 indices 62/74 only as a strong task-selection target. Preserve their records. The next G2 research step is a prospective, non-executing analytic screen on one shared positive-width state/parameter cell: derive full-hold safety/contact and progress bounds for two held actions and expose any mathematical threshold gap before creating IDs or running a solver. A task threshold with practical meaning must be specified independently of those bounds; without task/platform inputs, label this work synthetic and exploratory. G4 remains paused.

Overall **HOLD**; **G1 PASS only for the restricted reduced model**; **G2/G3/G4 and physical-platform correspondence UNVERIFIED**. R5 remains **800/800 `NOT_RUN`**. No G3, controller, hardware, or new G2/G4 execution is authorized by this review.
