# Codex review — G4 Auer R23 paired-method overlap audit

**Date:** 2026-10-06  
**Reviewed handoff:** `LUNA_TO_CODEX_G4_AUER_R23_PAIRED_METHOD_OVERLAP_AUDIT_FULL_HANDOFF.md`  
**Handoff SHA-256:** `2b66197d85980f8f38eeedf965bcac9789625a8e4c96255549fc8e401a9a9b5e`  
**Disposition:** **ACCEPT the method-level overlap finding.** Generic paired validated enclosure is blocked as a standalone novelty claim. A finite generic-method certificate of R23's `1/25,000 m` action gap, a DDWMR-specific computational advantage, and G4 remain **UNVERIFIED**. No execution GO.

I read `AGENTS.md`, the four canonical `research_context` files, the R23/R24 G2 reviews and R25 source-domain review, the G4 R21/R22 pilot reviews, and this handoff. I independently checked the augmented-IVP construction against MASTER v2.1 and the retained Auer 2013 PDF. Its SHA-256 is `d6310c8fd32280addda3f50e3367f9923940641d39de0e70a0932869a2d0ead2`. I also inspected the primary Arcak–Maidens and TIRA full-text sections cited below. Houska's locators are supported by the existing primary-source audit; I did not rerun a Houska computation. No query, worker, stage, batch, or proof-producing solver was run for this review.

## A. Finding — the paired initial-set construction is exact as a mathematical IVP

For each R23 product cell, let `xi` be the one shared nine-state initial value and `vartheta` the one shared twelve-label, execution-fixed parameter vector. Set `y_a=x_a-xi`, for `a in {+,0}`. The augmented system is

\[
\dot y_a=f(\xi+y_a,V_a;\vartheta),\qquad
\dot\xi=0,\qquad \dot\vartheta=0,
\quad
(y_+(0),y_0(0),\xi(0),\vartheta(0))
\in\{0\}^{18}\times X_0(\eta)\times\Theta_{\rm lab}(\eta).
\]

Its dimension is `9+9+9+12=39`. Every initial point in this ordinary interval box maps to exactly one R23 matched pair; neither the initial state nor the fixed label is independently selected for the two actions. Since the initial positions coincide, `Delta J=y_{+,p_x}(T)-y_{0,p_x}(T)`. An optional output accumulator would make the system 40-dimensional. The R23 full-hold collision and contact predicates must be evaluated on **both** `x_a=xi+y_a` trajectories for every time in `[0,T]`.

**Evidence.** This is direct substitution into MASTER §§5–11 and R23's declared `X_0=[-eta,eta]^9`, twelve-label product set, two held voltages, and `T=1/4`. The source label map has positive `rho,lambda` throughout the grid, so its divisions are defined. R24 accepts the matched synthetic gap `Delta J>1/25,000 m` and both formal full-hold margins, with strict time-dependent lower inequalities only for `t>0`.

**Consequence.** A naive box on `(x_+(0),x_0(0))` would admit unmatched initial states. The shared-latent construction avoids that modeling error. It does **not** guarantee that a computed interval tube retains useful correlation between `y_+` and `y_0`: componentwise wrapping, endpoint subtraction, or an interval accumulator can still produce an inconclusive bound. For a correlated non-product parameter set, its exact set or an exact latent parameterization must replace the product box; a hull is an explicitly disclosed relaxation.

**Status:** **VALID mathematical construction; numerical tightness UNVERIFIED.**

## B. Finding — primary methods cover the construction at the level claimed

**Auer, Kiel and Rauh (2013).** The retained full paper, printed pp. 740–743, §4.1 Eq. (26), permits an autonomous IVP with interval initial values and a scalar expression graph, Eqs. (27)–(33), including one-input piecewise operations. The R23 `clip` is such an operation. Its branch slopes are `0,1,0`; Eq. (33) encloses both adjacent slopes at a corner. Because the clip values agree at each corner, the discontinuity-gap treatment of Eqs. (35)–(41) is not needed. Section 4.2 Eq. (42) describes a functional tube around an approximate trajectory, with residual/Picard construction in Eq. (43). The 39-dimensional system uses one shared frozen `xi` and `vartheta`, elementary functions, and a continuous RHS, so it fits this **method formulation**. Auer's paper does not present a paired DDWMR run or prove that a particular implementation closes an inclusion or resolves a `40 micrometre` output gap under finite resources. Its §5 mechanical example is a different system.

**Arcak and Maidens (2017).** In the accessible [author full text](https://arxiv.org/html/1709.06661v1), §2 Proposition 1 Eqs. (3)–(4) gives a componentwise trajectory-separation bound, and Corollary 1 Eqs. (6)–(8) uses a coarse domain and growth matrix. Example 1 gives a zero-dynamics parameter augmentation. Its displayed `C^1` state assumption is not globally satisfied by `clip`. R23's independent proof that both true actions have `|sigma_j|<0.2` offers a smooth local specialization; a valid augmented comparison domain, growth matrix, and validated reference still have to be constructed. The corollary's displayed endpoint enclosure alone is not a full-hold contact/collision certificate.

**TIRA, Meyer, Devonport and Arcak (2019).** In the accessible [primary full text](https://arxiv.org/html/1902.05204), §3.1 Assumption 3 and Eq. (4) bound growth on an invariant domain; Proposition 4 gives an endpoint enclosure. The remarks discuss general nonadditive systems through a suitable supplied growth bound. This supports representability of the transformed pair, conditional on the same smooth-domain and bound obligations. It neither supplies an R23 paired computation nor automatically verifies predicates over every intermediate time. The paper distinguishes methods available in the toolbox from further generalized growth constructions; this review makes no claim that an off-the-shelf TIRA command handles this 39-dimensional input unchanged.

The earlier primary-source audit of Houska, Villanueva and Chachuat (2015), §3 assumptions A1–A3, Eqs. (3.1)–(3.4), Theorem 3.1 and Corollary 3.2, is corroborating overlap for smooth predictor-validation. Applying it here requires a sound smooth branch/domain and an actual validated remainder. The Auer construction alone suffices for the generic expressibility conclusion.

**Consequence.** The handoff correctly separates *expressing the paired problem and its output predicate* from *obtaining a positive finite certificate for that predicate*. A full-time tube can be interval-evaluated for collision and contact only if its computed range and the square-root domain are enclosed soundly; R23's strict true-trajectory slip proof does not by itself guarantee a generic numerical tube remains inside that branch. Failure to close an inclusion or obtain a positive margin means `UNKNOWN`.

**Status:** **VALID method-level overlap; finite paired performance UNVERIFIED.**

## C. Finding — contribution and pilot limits

R23's direct voltage-to-current-to-slip-to-force difference cone is an accepted **synthetic plant-specific analytical result**. The general idea of two action-conditioned IVPs with shared initial/parameter coordinates and a terminal output difference is not a new validated-reachability architecture. The R19/R20 selected ten-pair Auer pilot concerns **single-action safety queries**, not `Delta J`: Auer certified 9/10 and R3 6/10 in that selected set. Its proof sizes and costs cannot establish paired-method superiority or representative coverage.

The matched statement `forall (xi,vartheta): J_+(xi,vartheta)>J_0(xi,vartheta)` does not supply a single task threshold separating `sup J_0` from `inf J_+`. R24 establishes a common threshold only at `eta=10^-6`, leaves `10^-5` and `10^-4` unresolved, and gives a cross-state counterexample at `10^-3` and `10^-2`. R25 finds no complete MASTER-compatible operating task/domain in **the two sources it inspected**; it is not an exhaustive platform finding.

**Consequence.** Any DDWMR/contact-specific advantage needs an independently declared task and domain, a prospective matched method comparison on exactly the same paired quantifiers and full-hold predicates, proof replay, and predeclared coverage/resource criteria. Its cost must include the branch/domain proof and reference validation where a baseline requires them. The preserved ten pairs remain development evidence, not a population sample or fresh evaluation set.

**Status:** **BLOCKED** for generic paired-enclosure novelty as a standalone claim. **UNVERIFIED** for a DDWMR-specific computational advantage, practical task value, plant-specific originality, physical transfer, and G4 overall.

## D. Required action and gate disposition

Keep the Auer batch paused. Do not launch a paired evaluator or another synthetic threshold variant merely because the mathematical augmentation is possible. G2 needs a task threshold and operating domain specified independently of R22–R24 results; G4 needs a reviewed, prospective matched workload only after a concrete plant-specific effect and its falsification criterion are defined. No new query or batch GO follows from this audit.

**HOLD; G1 PASS only for restricted reduced-model consistency; G2/G3/G4 and physical-platform correspondence UNVERIFIED.** G2 R5 remains `800/800 NOT_RUN`. No G3, operational controller, hardware claim, commit, or push follows.
