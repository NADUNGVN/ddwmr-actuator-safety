# Codex review — G2 R22 prospective task-feasibility screen

**Date:** 2026-10-06  
**Reviewed handoff:** `LUNA_TO_CODEX_G2_R22_PROSPECTIVE_TASK_FEASIBILITY_SCREEN_FULL_HANDOFF.md`  
**Handoff SHA-256:** `65795fd584ce1e6ea2ddc2c4251ae0549a922187080e2fc8386f0a2b92497b41`  
**Disposition:** **ACCEPT** the narrowly scoped synthetic full-cell analytic separation. Practical task relevance, general G2 usefulness, and physical correspondence remain **UNVERIFIED**.

I read `AGENTS.md`, the four canonical `research_context` files, the R22 assignment and handoff, and the R21 review. I checked the inequalities against MASTER v2.1 §§5–12 and recomputed the displayed rational endpoint, collision, and contact arithmetic independently. I ran no native row, worker, stage, retry, study, or G4 comparison and changed no archived evidence.

## A. Finding

R22 gives a sound analytic screen for **one declared synthetic cell**: `X_0=[-10^-6,10^-6]^9`, twelve execution-fixed parameter labels in `[1-10^-6,1+10^-6]^12` with `J_j=1/rho_j`, clip traction, `T=1/4`, and common scene. Both `V_+=(1,1)` and `V_0=(0,0)` have positive whole-hold collision and formal contact margins. Their rigorously bounded terminal progress intervals are disjoint.

## B. Evidence

**Plant and nominal center.** The declared parameter map and direct-drive witness satisfy MASTER's wheel-side conventions; positive inertia and damping are retained. At the all-one/rest center, left-right symmetry is an invariant special case. MASTER's equations give `u'=2q-u`, `q'=i-4q`, and `i'=1-i-u-q` for `q=w-u` under `(1,1)`. The bootstrap `i<=t`, `q<=t²/2`, `u<=t³/3` closes on `[0,1/4]`, where the clip stays unsaturated. The stated nominal bounds `685/4718592 <= J_{+,*} <= 1/3072` and `J_{0,*}=0` follow.

**Whole-cell comparison.** From `|phi|<=1`, the component equations imply `D^+||x||_infty <= 8||x||_infty+4`; the claimed `[-5,5]^9` domain follows from `e²<9`. On that domain, pose, body, wheel, and current state row bounds are respectively at most `6`, less than `9`, less than `7`, and less than `3`. The overall Lipschitz constant `9` is valid. At fixed state, varying all labels by at most `eta` changes each force by at most `eta`, each body/yaw row by at most `2eta`, each wheel row by less than `23eta`, and each current row by less than `23eta`. Thus `30eta` is a valid common parameter forcing bound. This includes the correlated `J=1/rho` map. Comparing each fixed-parameter trajectory with its same-action nominal trajectory gives `E(t)<(146/3)eta<49/10^6` for all `t<=1/4`. This is an outer perturbation bound; it does not permit parameter switching along a true trajectory.

**Exact rational spot-check.** With `Ebar=49/10^6`, the progress calculations reduce to

\[
J_+^- = \frac{685}{4718592}-\frac{49}{2000000}
=\frac{8896789}{73728000000},\qquad
J_0^+=\frac{49}{4000000},
\]

\[
J_+^- -J_0^+=\frac{7993621}{73728000000}>0.
\]

The stated positive-action upper bound is `16801/48000000`. The conservative whole-hold collision clearance for `(1,1)` is `7/50-1/3072-1/1000 = 53251/384000>0`; the baseline clearance is greater than `139/1000`. The slip bound `1/32+3Ebar<1/16` keeps every perturbed wheel on the clip's linear branch. Direct square-root reserve inequalities give `c>297/160-1/100=1477/800>0` for either action. No derivative of the contact margin is invoked.

## C. Consequence

There exists a **mathematically possible** threshold interval

\[
\frac{49}{4000000}<\delta_{task}\le
\frac{8896789}{73728000000}\quad\text{m}
\]

for this synthetic cell. Because it comes from uniform lower/upper trajectory bounds, the interval shows a true robust progress separation within the stipulated reduced model. It is **not** an independently specified task: no `delta_task` was declared, each state/label coordinate has width only `2e-6`, the guaranteed gap is about `0.108 mm`, and the numerical plant/scene data have no physical provenance. The action pair starts near an exact rest equilibrium, with zero voltage as the baseline. No general evaluator, runtime benefit, physical robot guarantee, novelty, or practical safety-filter advantage follows.

The handoff declares the candidate before presenting its bounds, but it has no external preregistration or independent task specification. Treat it as exploratory evidence; do not create fresh query IDs or tune a threshold inside the observed interval as confirmatory validation.

## D. Status

- **VALID:** one synthetic positive-width full-cell, full-hold analytic action separation with positive formal collision/contact margins.
- **UNVERIFIED:** meaningful operating-domain width, independently defined task threshold, practical voltage-selection value, general G2 computation, physical-platform correspondence, and G4 novelty.
- **UNCHANGED:** R17 indices 62/74 remain consumed and retired only as a strong task-selection challenge. R5 remains `800/800 NOT_RUN`; G4 stays paused.

Overall **HOLD**; **G1 PASS only for restricted reduced-model consistency**; **G2/G3/G4 UNVERIFIED**. No new execution GO or G3/operational authorization follows.

## E. Required action

The project owner should specify the intended task's direction, minimum displacement, time limit, voltage limits, initial-state/parameter ranges, and obstacle geometry **independently of this interval**. For physical transfer, identify platform and contact/support evidence or a certified model-error envelope. Until such inputs exist, further micro-cell construction should not be presented as practical-usefulness progress. A separate, explicitly labeled synthetic-method study could still investigate scaling, but would not close this task/domain gap.
