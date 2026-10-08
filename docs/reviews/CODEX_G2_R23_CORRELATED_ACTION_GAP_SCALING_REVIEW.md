# Codex review — G2 R23 correlated action-gap scaling

**Date:** 2026-10-06  
**Reviewed handoff:** `LUNA_TO_CODEX_G2_R23_CORRELATED_ACTION_GAP_SCALING_RESEARCH_FULL_HANDOFF.md`  
**Handoff SHA-256:** `c59c2eabc3a551f3f8ddb67f202066d651c341aba90111bcfbebccda69a9d402`  
**Disposition:** **VALID** for the synthetic paired-action lower bound and whole-hold formal margins; **NEEDS REVISION** for the interpretation of wide-cell scalar overlap. At two grid widths there is a true counterexample to a **common task threshold**, even though matched action ordering stays positive. No gate promotion or new query GO.

I read `AGENTS.md`, the canonical research context, the R23 assignment and handoff, R22 review, and MASTER v2.1 §§5–12. I independently checked the slip and paired-difference equations, the first-exit inequalities, and the exact fractions. This was read-only mathematical review. I ran no native row, worker, stage, retry, study, or G4 comparison.

## A. Finding 1 — R23 paired bound is sound in its synthetic scope

**Evidence.** Direct subtraction of MASTER's body/yaw equations gives `A_j'=2C_j S_j-A_j` for `A_L=delta u-delta r`, `A_R=delta u+delta r`. Differentiating the slip definitions gives, on the R23-proven linear clip branch,

\[
S_j'=\rho_jk_jI_j-[\rho_jB_j+(\rho_j+2)C_j]S_j
 +(1-\rho_jB_j)A_j,
\quad
I_j'=\frac{1-R_jI_j-k_j(S_j+A_j)}{\lambda_j}.
\]

The unit voltage difference appears only in `I_j'`, as required by MASTER. The all-action bootstrap first bounds `I+W` below `0.71`; at either slip boundary `sigma_j=+1` or `-1`, the derivative points inward. Thus `|sigma_j|<1`, and the sharper comparison gives `|sigma_j|<0.2` on the whole hold. The argument uses the specific clip law and does not assert a general monotone MASTER traction law.

For the paired system, the trial cone `A,S,I>=0`, `H=I-A/20>=0` closes: all lower faces point inward, while `I<=100t/99`, `S<0.5175t²`, and `A<0.41t³` avoid its upper faces through `T=1/4`. The lower estimates `I>=0.69t`, `S>0.11t²`, and `A>0.054t³` are valid for `t>0` (at `t=0` the strict inequalities are equalities). The heading correction is outward, and independent exact-rational recomputation gives

\[
\Delta J\ge
\frac{2349}{51200000}-\frac{98441}{20480000000}
=\frac{841159}{20480000000}
>\frac1{25000}\;\mathrm m.
\]

This holds for each matched initial state and fixed label vector in every declared `eta` cell. R23's separate safety bootstrap gives full-hold clearance greater than `0.097 m` and formal contact margin greater than `1.9` for both actions throughout the same grid. The rational exponential cap, `I+W` cap, and reported margins also check. These statements concern only the synthetic model and specified `clip` law.

**Status:** **VALID with the `t>0` strictness correction.** It proves matched-realization action ordering, not an independently declared task threshold.

## B. Finding 2 — Scalar-tube width limit is correct

**Evidence.** R22's outward scalar cap gives `Ebar=49 eta` on all five declared grid widths; the a-priori `[-5,5]^9` domain still holds at `eta=10^-2`. Its separate progress intervals have gap

\[
J_+^- -J_0^+=\frac{685}{4718592}-\frac{147}{4}\eta.
\]

The exact cutoff is `eta<685/173408256`, about `3.9502e-6`, so the first grid width with overlapping **computed** intervals is `10^-5`. The printed rational cutoff and paired lower-bound subtraction were independently recomputed.

**Status:** **VALID for these sufficient scalar bounds.** Overlap does not decide whether a common task threshold actually exists.

## C. Finding 3 — True common-threshold blocker at wider cells

**Evidence.** Take the admissible all-one parameter label vector and two different initial states in the same `X_0(eta)`: all coordinates zero except `u_0=+eta` for the **zero-voltage** trajectory, and all coordinates zero except `u_0=-eta` for the **positive-voltage** trajectory. Both trajectories are symmetric, so `r=theta=0`. R23's whole-cell slip proof puts both on the linear clip branch. Let `G=J_{(1,1)}` from exact rest, with `G<=1/3072` by R22. Let `H` be the zero-voltage displacement produced by unit positive initial body speed on this linear symmetric system. Linearity gives

\[
J_{0,+\eta}=\eta H,
\qquad
J_{+,-\eta}=G-\eta H.
\]

For the zero-voltage trajectory starting at `u=eta`, MASTER's energy identity gives `|u|,|w|<=eta` throughout the hold. Its slip magnitude is at most `2eta<1`. In the linear branch, `u'=-3u+2w`, `w'=u-2w+i`, `i'=-i-w`. A first-exit argument proves `w>=0`: while `w>=0`, `u>=eta e^{-3t}>eta/3` because `e^{3/4}<3`; also `i=-int_0^t e^{-(t-s)}w(s)ds>=-eta t>=-eta/4`. At any putative first crossing of `w=0`, `w'=u+i>eta/12>0`, a contradiction. Therefore

\[
H\ge\int_0^{1/4}e^{-3t}dt
=\frac{1-e^{-3/4}}3>\frac16,
\]

where `e^{3/4}>1+3/4+(3/4)^2/2>2`. At `eta>=10^-3`,

\[
J_{0,+\eta}-J_{+,-\eta}
=2\eta H-G
>\frac{\eta}{3}-\frac1{3072}
\ge\frac1{3000}-\frac1{3072}
=\frac1{128000}>0.
\]

Thus, for `eta=10^-3` and `10^-2`, a baseline trajectory in the cell progresses farther than a positive-action trajectory from **another** admissible initial state. No single `delta_task` can satisfy `sup J_0 < delta_task <= inf J_+` on either whole cell. These witness trajectories retain the R23 full-hold collision/contact bounds. This does not contradict `J_+(x_0,vartheta)>J_0(x_0,vartheta)` for each **matched** realization.

**Status:** **BLOCKER for a common-threshold task-selection claim at `eta>=10^-3` in the declared grid.** The truth at `eta=10^-5` and `10^-4` remains **UNVERIFIED**; only the separate scalar proof fails there.

## D. Consequence and required action

R23 should qualify §1 and §6: the scalar interval overlap at `10^-5` is an inconclusive sufficient-bound result; it cannot be classified as *only* enclosure conservatism across the entire grid. At `10^-3` and `10^-2`, the common-threshold separation is actually false, while the matched paired ordering still holds. Also state the lower `S,A` inequalities as strict only for `t>0`.

The paired bound is a useful **synthetic dependence-preservation result** and may merit a narrowly scoped evaluator prototype for action ordering. Before treating it as decision-relevant task selection, distinguish its quantifier (`forall matched realization, Delta J>0`) from a common threshold (`sup J_0<delta<=inf J_+`). Request an independent audit of the wide-cell counterexample and a corrected R23 handoff before committing to a paired-evaluator build or wider study. Do not run a new query, retry, stage, or 800-row study from this review.

Overall **HOLD**; **G1 PASS only for restricted reduced-model consistency**; **G2/G3/G4 and physical-platform correspondence UNVERIFIED**. R5 stays `800/800 NOT_RUN`; G4 remains paused.
