Session: DDWMR | LUNA-G4-AUER

# G4 Auer R23 — paired-method overlap audit

**Date:** 2026-10-06  
**Disposition:** **BLOCK** a standalone novelty claim for generic paired validated enclosure. Auer 2013 and other recorded validated-reachability methods can express the R23 shared-state/shared-parameter paired IVP under the R23 synthetic assumptions. Whether those methods produce a sufficiently tight numerical certificate for the stated $1/25{,}000$ m output bound is **UNVERIFIED**. The exact R23 cone proof remains a valid synthetic, model-specific derivation; it does not establish a DDWMR-specific computational advantage.  
**Gate state:** HOLD; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED. The Auer batch remains paused.

## 1. Scope and execution record

I read the R23 assignment, AGENTS.md, the four canonical research_context files, MASTER v2.1 §§20–23 and 28–31, the G2 R23 and R24 handoffs and reviews, the R24 R23-wording erratum, the preserved G4 Auer R4/R5 and R21/R22 reviews, the Auer method contract, and the retained Auer 2013 primary text. I also checked the recorded primary-source locators for Arcak–Maidens, TIRA, and Houska–Villanueva–Chachuat.

This was a source and method comparison only. **No query, worker, stage, retry, batch entry, solver, manifest, or evidence artifact was created or changed.** Preserved R19/R20 and G2 evidence remains untouched. No commit or push was made.

## 2. The exact paired problem R23 proves

Let $x=(p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R)$ and let $f(x,V;\vartheta)$ be the MASTER v2.1 voltage-driven RHS. For one common initial state $\xi$ and one execution-fixed parameter vector $\vartheta$, R23 compares

$$
\dot x_+=f(x_+,V_+;\vartheta),\qquad
\dot x_0=f(x_0,V_0;\vartheta),\qquad
\dot\vartheta=0,
$$
$$
x_+(0)=x_0(0)=\xi\in X_0(\eta),\quad
\vartheta(0)\in\Theta_{\rm lab}(\eta),\quad
V_+=(1,1),\quad V_0=(0,0),\quad T=1/4.
$$

The same single $\vartheta$ coordinate feeds both vector fields; it is not copied and independently ranged. The same $\xi$ initializes both trajectories. The R23 family has $X_0(\eta)=[-\eta,\eta]^9$, twelve labels in the order $(\rho_L,C_L,\lambda_L,R_L,B_L,k_L,\rho_R,C_R,\lambda_R,R_R,B_R,k_R)$, independently ranging in $[1-\eta,1+\eta]^{12}$, and $\eta\in\{10^{-6},10^{-5},10^{-4},10^{-3},10^{-2}\}$. In the synthetic parameterization $m=I_z=R_w=b=v_s=c_u=c_r=1$, $J_j=1/\rho_j$, and $L_j=\lambda_j$; the traction law is $\phi(z)=\operatorname{clip}(z,-1,1)$. These are R23 case choices, not general MASTER assumptions.

For action $a\in\{+,0\}$, define

$$
J_a=p_{x,a}(T)-p_{x,a}(0)
    =\int_0^T u_a(t)\cos\theta_a(t)\,dt,
\qquad \Delta J=J_+-J_0.
$$

Because the initial states are identical, $\Delta J=p_{x,+}(T)-p_{x,0}(T)$. Equivalently, a solver can append an accumulator $q(0)=0$, $\dot q=u_+\cos\theta_+-u_0\cos\theta_0$, and return $q(T)=\Delta J$.

The full-hold predicates apply to **both** trajectories and every shared realization:

$$
h_a(t)=\|p_a(t)-(1/5,1/20)\|_2^2-(3/50)^2\ge0,
$$
$$
c_a(t,\vartheta)=\sum_{j\in\{L,R\}} C_j
\sqrt{1-\phi(\sigma_{j,a}(t)/v_s)^2}
-|m u_a(t)r_a(t)|\ge0,
\quad \sigma_L=R_w\omega_L-u+br,\quad
\sigma_R=R_w\omega_R-u-br,
$$

for every $t\in[0,T]$, $a\in\{+,0\}$. In the R23 synthetic constants the contact term is $\sum_j C_j\sqrt{1-\operatorname{clip}(\sigma_{j,a},-1,1)^2}-|u_ar_a|$.

R23's matched proof, accepted in R24's exact synthetic scope, establishes

$$
\forall(\xi,\vartheta)\in X_0(\eta)\times\Theta_{\rm lab}(\eta):
\quad \Delta J(\xi,\vartheta)>1/25{,}000\;\mathrm m,
$$

and full-hold collision clearance $>0.097$ m and contact margin $>1.9$ N for both branches. It uses the shared labels and shared initial state in its difference equations. R24 also corrected the strict inequalities to hold for $t>0$, with equality at $t=0$.

### Matched ranking is not a common threshold

The bound above means that the positive-voltage branch ranks above the zero-voltage branch for each **matched** realization. It does not imply a single $\delta$ with

$$
\sup_{\xi,\vartheta}J_0(\xi,\vartheta)<\delta\le
\inf_{\xi,\vartheta}J_+(\xi,\vartheta),
$$

where the supremum and infimum can be attained at different initial states or labels. The accepted R24 audit finds this common-threshold condition established for the synthetic $\eta=10^{-6}$ cell, unresolved at $10^{-5}$ and $10^{-4}$, and false by an admissible cross-state witness at $10^{-3}$ and $10^{-2}$. The owner has not supplied a task threshold. Do not present the matched ranking bound as a threshold-based action guarantee.

## 3. An exact generic construction for the shared initial set

A rectangular interval state box over duplicated $x_+$ and $x_0$ coordinates would allow the two initial states to vary independently. That is an outer relaxation and does **not** preserve R23's matched quantifier. The diagonal initial set can instead be represented exactly with one shared frozen initial-state label $\xi$ and two zero-initialized deviations:

$$
y_+=x_+-\xi,\qquad y_0=x_0-\xi,
$$
$$
\dot y_+=f(\xi+y_+,V_+;\vartheta),\qquad
\dot y_0=f(\xi+y_0,V_0;\vartheta),\qquad
\dot\xi=0,\qquad\dot\vartheta=0,
$$
$$
y_+(0)=y_0(0)=0,\qquad
\xi(0)\in X_0(\eta),\qquad
\vartheta(0)\in\Theta_{\rm lab}(\eta).
$$

For the R23 product boxes, the augmented initial set is the ordinary interval box

$$
\{0\}^9\times\{0\}^9\times X_0(\eta)\times\Theta_{\rm lab}(\eta),
$$

and has dimension 39. It preserves the common initial state and fixed parameter exactly because each appears once and is reused in both RHS blocks. The output is $\Delta J=(y_+)_{p_x}(T)-(y_0)_{p_x}(T)$; an accumulator makes the output a state coordinate if desired. For a non-product correlated parameter set, the exact set or an exact latent parameterization must be retained; replacing it with its interval hull can lose correlation and must be reported as an outer relaxation.

Collision and contact are checked on $x_a=\xi+y_a$ for both branches over the complete validated time interval. The IVP method supplies a tube; the collision/contact predicates and the paired output are continuous functions to evaluate over that tube. A negative sufficient margin or an unclosed inclusion is UNKNOWN, not evidence that the real trajectory collides or violates contact.

## 4. Primary-source comparison

| Method and inspected primary locator | Expressing the R23 paired IVP | Clip, labels, predicates, and output | Scope/access limit |
|---|---|---|---|
| **Auer, Kiel & Rauh (2013),** “A Verified Method for Solving Piecewise Smooth Initial Value Problems,” *International Journal of Applied Mathematics and Computer Science* 23(4), 731–747, DOI 10.2478/amcs-2013-0055. §4.1, Eq. (26), Eqs. (27)–(33), Properties 1–2; discontinuity treatment Eqs. (35)–(41); §4.2, Eqs. (42)–(43), pp. 740–743 printed. | The article's autonomous IVP with uncertain initial interval, Eq. (26), can take the 39-dimensional transformed system above. Its frozen $\xi,\vartheta$ coordinates have zero derivative. Eq. (42) gives a functional tube around an approximate solution, and Eq. (43) gives the residual/Picard iteration used to enclose it. A terminal difference or an appended $q$ state gives $\Delta J$. | The scalar-expression representation in Eqs. (27)–(33) and generalized derivative enclosure handles piecewise-smooth RHS branches. For clip, its interval derivative is $\{0\}$ on saturated intervals, $\{1\}$ strictly inside $(-1,1)$, and $[0,1]$ at or across either corner. The R23 clip is continuous at both corners, so its value jump is zero; the discontinuity correction in Eqs. (35)–(41) is unnecessary. R23's own bootstrap further proves $\lvert\sigma_j\rvert<0.2$ on both trajectories, so the realized R23 family stays in the smooth unsaturated branch and the contact square root stays away from saturation. The contact predicate can then be interval-evaluated without differentiating its margin. The method's tube can be passed to interval evaluations of $h_a,c_a$ and the $\Delta J$ output. | Complete local PDF and extracted text were inspected; PDF SHA-256 D6310C8FD32280ADDDA3F50E3367F9923940641D39DE0E70A0932869A2D0EAD2. The article's §5 example is friction/hysteresis, not the nine-state DDWMR, and supplies no DDWMR contact or $\Delta J$ certificate. This is method-level expressibility, not evidence that an Auer implementation certifies the R23 bound. The local R4/R5 solver and replay are a documented single-action 21-coordinate reconstruction, not the original VALENCIA binary; the 39-dimensional paired extension described here has not been implemented. |
| **Arcak & Maidens (2017 author manuscript),** “Simulation-based reachability analysis for nonlinear systems using componentwise contraction properties,” §2 Proposition 1, Eqs. (3)–(4); Corollary 1, Eqs. (6)–(8); §3 Algorithm 1 and Example 1, Eq. (13). | Proposition 1 bounds the componentwise separation of trajectories by $e^{Ct}$ on a justified domain. Corollary 1 turns a coarse full-horizon reachable-set enclosure and an admissible growth matrix into a reachable-set overapproximation. Example 1, Eq. (13), represents a constant uncertain parameter with zero dynamics. Apply it to the same transformed pair state with one shared $\xi,\vartheta$; known held voltages are fixed RHS constants. | Its displayed theorem assumes a vector field continuous in time and $C^1$ in state. The R23 all-action branch proof supplies a route to a convex comparison domain strictly inside $\lvert\sigma_j\rvert<1$, where the selected clip RHS is smooth; the Jacobian/growth bound and a coarse domain still must be established for the augmented pair. Eq. (4) is a trajectory-separation bound for all $t$; use the augmented output or derive bounds for $\Delta J$, and evaluate $h_a,c_a$ over a full-time enclosure. | Full arXiv HTML was accessible and the stated sections were inspected. The source does not provide a DDWMR implementation or an R23 paired computation. Its reference flow and growth bound must be computed/validated for a proof-producing comparison; its example is not evidence of matched R23 performance. |
| **Meyer, Devonport & Arcak (2019),** “TIRA: Toolbox for Interval Reachability Analysis,” HSCC ’19, DOI 10.1145/3302504.3311808, §3.1 Assumption 3, Eq. (4), Proposition 4 and remarks. | Eq. (4) propagates an initial half-width and an uncertainty forcing with a matrix exponential. Proposition 4 gives an endpoint reachable-set enclosure. The paired state and constant $\xi,\vartheta$ can be placed in the same augmented state; the source's general-system remarks allow a user-provided growth bound when its additive-input special case does not fit directly. | Assumption 3 bounds a componentwise Jacobian growth matrix on an invariant set. As with Arcak–Maidens, use the R23 unsaturated invariant domain to meet the smoothness requirement. Proposition 4 is an endpoint statement; continuous-time collision/contact requires applying a sound bound across time or using validated subinterval tubes, not checking only $t=T$. $\Delta J$ can be a terminal augmented coordinate. | Full arXiv HTML was retrieved and §3.1 read in this pass; it explicitly describes TIRA as a toolbox of interval overapproximations. The cited proposition does not implement the paired DDWMR or certify its margins. TIRA's abstract also cautions that interval reachability prioritizes simplicity/scalability over approximation accuracy. |
| **Houska, Villanueva & Chachuat (2015),** “Stable Set-Valued Integration of Nonlinear Dynamic Systems Using Affine Set-Parameterizations,” *SIAM Journal on Numerical Analysis* 53(5), 2307–2328. §3, Assumptions A1–A3, Eqs. (3.1)–(3.4), Theorem 3.1 and Corollary 3.2. | The predictor-validation construction propagates a parameterized reachable set and validates a complete time segment with a remainder condition. The common $\xi,\vartheta$ can be shared set-parameters in the transformed pair system. | The displayed assumptions require smooth/factorable data. R23's proof that all trajectories remain on the linear clip branch allows an equivalent smooth RHS on its validated invariant domain; a sound predictor and remainder must stay within that domain. The theorem's validated segment supports full-time predicates; an output coordinate or terminal difference represents $\Delta J$. | Full author-hosted paper was available in the prior primary-source audit; the exact locators and smoothness limit are retained in G4_MATCHED_PRIOR_ART_COMPARISON_v1.md and G2_PRIOR_ART_SUPPLEMENT_R2.md. No adapted Houska computation or R23 performance comparison is in the record. |

The primary-source record also includes Lin–Stadtherr, *Validated Solutions of Initial Value Problems for Parametric ODEs*, §2 Eq. (1), §§4.1–4.2 Eqs. (18)–(23). It covers time-invariant interval parameters and complete-step Picard/Taylor enclosures, but its displayed differentiability assumptions exclude piecewise branches as written. R23's proved strict unsaturated domain is a possible smooth specialization; no same-data computation is recorded. Flow* is only partially accessed in the matrix and is not used here as a theorem-level comparator.

## Primary-source links

- Auer, Kiel & Rauh 2013: [retained PDF](../../research/third_party/auer2013/auer-kiel-rauh-2013.pdf) and [extracted text](../../research/third_party/auer2013/auer-kiel-rauh-2013.txt).
- Arcak & Maidens: [arXiv full text](https://arxiv.org/html/1709.06661v1).
- Meyer, Devonport & Arcak, TIRA: [arXiv full text](https://arxiv.org/html/1902.05204).
- Houska, Villanueva & Chachuat: [author-hosted paper](https://faculty.sist.shanghaitech.edu.cn/faculty/boris/paper/stableSetIntegrator.pdf).
- Lin & Stadtherr: [author manuscript](https://academicweb.nd.edu/~markst/lin-stadtherr-vspode-apnum.pdf).
- R23/R24 derivations and accepted corrections: [G2 R23 handoff](LUNA_TO_CODEX_G2_R23_CORRELATED_ACTION_GAP_SCALING_RESEARCH_FULL_HANDOFF.md), [R23 review](CODEX_G2_R23_CORRELATED_ACTION_GAP_SCALING_REVIEW.md), [G2 R24 handoff](LUNA_TO_CODEX_G2_R24_PAIRED_BOUND_AND_THRESHOLD_ADVERSARIAL_AUDIT_FULL_HANDOFF.md), and [R24 review](CODEX_G2_R24_PAIRED_BOUND_AND_THRESHOLD_AUDIT_REVIEW.md).


### Source-level answer

**Yes, an established validated-IVP construction can express the same paired problem under the R23 synthetic assumptions.** The exact latent-state formulation prevents independent initial-state or parameter copies; Auer handles a continuous piecewise-smooth clip directly, while the $C^1$ growth-bound methods can use R23's strict unsaturated branch if their invariant comparison domain is actually established. Any of these methods can enclose the output by appending $q$ or subtracting paired endpoint positions, then apply the same full-hold collision/contact predicate to both branches.

That is a theoretical expressibility result. It does **not** prove that a particular implementation, resource profile, finite step schedule, interval representation, or independent checker obtains an output lower bound exceeding $1/25{,}000$ m on every R23 cell. Auer's Eqs. (42)–(43) support verified tubes when their inclusion checks close; the source does not guarantee a desired tightness on arbitrary dimension/cells. The Arcak/TIRA growth matrices and the Houska predictor remainder likewise require concrete, validated bounds. No such paired numerical comparison was run.

## 5. Disposition of the contribution claims

### Generic paired-enclosure novelty — BLOCKED

Appending two action-conditioned copies of a plant to one IVP, sharing initial-state and fixed-parameter coordinates, then bounding an output difference is a generic construction. Auer's interval IVP and residual tube, Arcak–Maidens' trajectory-separation bounds, and TIRA's growth-bound reachability already supply relevant machinery. A paired state is a formulation of the comparison, not by itself a new validated-reachability method. Do not claim first, generic novelty, or superiority from the augmentation or the $\Delta J$ output alone.

### R23 plant-specific analytic result — VALID, synthetic and narrow

R23's direct difference equations and positivity cone trace the held voltage difference through current, slip, contact force, body progress, and heading correction. R24 accepts the bound $\Delta J>1/25{,}000$ m and the stated formal whole-hold margins for this synthetic clip family. This is a model-specific analytical certificate/result, not an implemented general paired evaluator. Its novelty relative to a dedicated plant-specific analytical literature search remains **UNVERIFIED**.

### DDWMR/contact-specific computational contribution — UNVERIFIED

A plausible remaining hypothesis is that an enclosure exploiting voltage–actuator–slip–contact–pose dependencies yields a useful, proof-checkable output and collision/contact tube with lower conservatism or binding cost than applicable generic methods on a declared DDWMR domain. R23 does not establish it: it is a hand derivation on a tuned synthetic family, does not define an owner task threshold, and has no paired Auer/TIRA/Arcak/Houska run. It also does not establish physical tire/support correspondence, a recursive safe set, or G2/G3.

R24's threshold distinction constrains the potential decision claim: a common threshold is only established on the narrowest synthetic cell, unresolved on two cells, and refuted on the two widest cells. Matched action ranking remains true across the grid. Do not collapse those statements into one threshold claim.

## 6. Why the preserved Auer pilot is not the missing comparison

The R19/R20 ten-pair pilot evaluates individual state/action queries with two methods and a common safety/contact predicate. It is not a paired-action computation of $\Delta J$, and its ten IDs were deliberately selected, not a representative sample. Codex's R21/R22 reviews accept only descriptive pilot accounting: Auer certified 9/10 and R3 6/10; the pairs were not a prospective population sample. The much smaller R3 proof files and its lower measured peak memory do not establish an advantage for R23's paired output or a deployment benefit. The four R3 UNKNOWN cases did not enter the common predicate. Preserve the pilot's scope and checker-history qualifications; do not use its proof sizes, costs, or selected cases as representative performance evidence for this method question.

## 7. Evidence required before an advantage claim

Any future computation intended to support a DDWMR-specific advantage needs a prospective, reviewed comparison with:

1. **The same frozen problem:** identical nine-state equations, clip law, $X_0$, complete fixed $\Theta$ and correlations, common initial-state semantics, $V_+,V_0$, hold interval, obstacle/footprint, and contact domain. Use the shared latent $\xi,\vartheta$ pair exactly or identify each sound relaxation.
2. **The same outputs and quantifiers:** both full-hold predicates $h_a(t)\ge0,c_a(t,\vartheta)\ge0$; $\Delta J$ lower/upper bounds; and separate reporting of matched ranking versus any predeclared common task-threshold rule. A threshold must come from the task specification before inspecting results.
3. **Comparable validated work:** proof-producing enclosures with full-time coverage, equivalent outward arithmetic obligations, replayable checkers, and consistent CERTIFIED/UNKNOWN/invalid-input semantics. If a method needs a validated reference trajectory or smooth invariant-domain proof, include that work.
4. **Predeclared resource/cost accounting:** same host and external caps, with wall time, peak memory, method work counters, subdivisions/steps, proof and audit cost, and termination reason. Compare both certified coverage and enclosure quality under a common work cap; do not infer equal work from similar step counts.
5. **Outcome-independent cases and review:** choose cells before seeing outputs; keep UNKNOWN and failures in the denominator; separate development IDs from a locked evaluation; independently review source bindings and proof replay. Fix the target coverage/cost criterion from a declared use need before execution.

No such prospective comparison or GO follows from this read-only audit. The selected R19 ten-pair pilot cannot supply its workload, threshold, or cost criterion after the fact.

## 8. Final status

- **Generic paired validated-enclosure novelty:** **BLOCKED** as a standalone claim by direct method overlap.
- **R23 matched ranking and formal synthetic margins:** **VALID** in the R24-accepted synthetic scope.
- **A generic method's ability to produce the same numeric $1/25{,}000$ m certificate in finite resources:** **UNVERIFIED**; expressibility does not establish tightness or runtime.
- **DDWMR/contact-specific computational advantage, practical task value, and physical correspondence:** **UNVERIFIED**.
- **Gates:** HOLD; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.
- **Execution:** zero new queries/workers/stages/retries; Auer batch remains paused and unchanged; R19/R20 and G2 R23/R24 evidence unchanged; no code or manifest created; no commit or push.
