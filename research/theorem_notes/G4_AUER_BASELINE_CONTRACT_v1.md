# Auer-style piecewise derivative baseline contract for G4

**Version:** v1, preflight draft, 2026-09-30.  
**Status:** isolated clip derivative layer implemented; full ODE enclosure contract remains **UNVERIFIED** pending solver build, full-time inclusion implementation and independent review.  
**Scope:** comparison preparation for the authorized synthetic `G2-COMP-clip` family only. No G2/G3/G4 gate is promoted.

## 1. Source identity and adaptation boundary

The method candidate is Auer, Kiel & Rauh (2013), *A Verified Method for Solving Piecewise Smooth Initial Value Problems*, DOI `10.2478/amcs-2013-0055`, §§4.1–4.2. The article introduces piecewise interval evaluation (31), generalized derivatives (33), discontinuity corrections (35)/(41), and a VALENCIA-IVP functional tube (42) with residual iteration (43). The pinned VALENCIA-IVP 0.92_2e source is an older smooth core and does not contain the 2013 piecewise derivative extension. It has not been represented as the complete method.

This contract adopts the paper’s branch construction only for the continuous two-corner clip law used by this synthetic benchmark. The scalar functions are exactly `clip(q,-1,1)`. There is no smoothing, clipping dead-zone, parameter switching, or jump correction. Since the function has zero jump at both thresholds, the jump terms in (35)/(41) reduce to zero and are not divided by a distance that may contain zero.

## 2. Derivative and composition contract

For `I=[a,b]`, define the generalized derivative enclosure

\[
D(I)=\begin{cases}
\{0\}, & b<-1\text{ or }a>1,\\
\{1\}, & -1<a\le b<1,\\
[0,1], & \text{otherwise.}
\end{cases}
\]

The strict tests matter: `I=[-2,-1]`, `I=[1,2]`, `{−1}`, `{1}`, any interval crossing either threshold, and an interval crossing both thresholds all receive `[0,1]`. `D(I)` contains every ordinary derivative in the branches that meet I and both one-sided slopes at each corner. For all `x,y∈I`,

\[
\operatorname{clip}(x)-\operatorname{clip}(y)\in D(I)(x-y).
\]

For a smooth scalar composition `q(x)` on a convex box X, the clip chain derivative enclosure is `D(q(X))·∇q(X)`. With multiple coordinates the componentwise interval-Jacobian product encloses the difference: along the line segment from `x₀` to `x`, the scalar composition is piecewise C¹ and Lipschitz; split the segment at its finitely many clip crossings, apply the ordinary mean-value theorem on each subsegment, and sum the signed subsegment increments. Each local slope is in `D(q(X))`, and the sum remains in the interval Jacobian product. For vector RHS, apply the scalar argument to each output row; each row may use a different mean-value selection.

The code path is `validation/baselines/auer2013/piecewise.py` (`clip_derivative_interval`, `DualInterval.clip`) and `rhs.py` (chain through affine slip, fixed rational parameter maps, products and quotients). It intentionally shares the project's `validation.g2.rational.Interval` and `Budget`, and the `validation.g2.model` positivity and parameter-image checker. It is not an independent arithmetic engine.

## 3. DDWMR state and fixed-label representation

Use physical state order

\[
x=(p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R)
\]

plus exactly twelve constant labels in the benchmark order: `rho_L,C_L,lambda_L,R_L,B_L,k_L,rho_R,C_R,lambda_R,R_R,B_R,k_R`. The augmented system has 21 coordinates. Label equations are exactly `dot(xi)=0`. For each label vector, the same rational map is evaluated throughout the hold; use the existing checked image `J_j=1/rho_j`, `L_j=lambda_j`, and other parameter assignments. Do not independently re-box `J` and `rho` or resample labels over time.

The rational parameter map is admissible only where all declared denominators exclude zero and every required positive coefficient has a checked strictly positive lower bound. The existing `build_model` verifies the label cover, rational-function identities for the gear witness, and positivity/nonnegativity of the mapped coefficients. If a denominator interval includes zero, reject the cell before a trajectory claim. The implementation does not claim that interval products retain all parameter correlation; any later Cartesian relaxation must be disclosed as an outer enclosure.

For a fixed common voltage V, the formal RHS is

\[
\dot p_x=u\cos\theta,\quad\dot p_y=u\sin\theta,\quad\dot\theta=r,
\]
\[
\sigma_L=R_w\omega_L-u+br,\quad\sigma_R=R_w\omega_R-u-br,\quad
F_j=C_j\operatorname{clip}(\sigma_j/v_s),
\]
\[
m\dot u=F_L+F_R-c_u u,\quad
I_z\dot r=b(F_R-F_L)-c_r r,
\]
\[
J_j\dot\omega_j=k_ji_j-B_j\omega_j-R_wF_j,\quad
L_j\dot i_j=V_j-R_ji_j-k_j\omega_j.
\]

The implemented adapter includes those nine equations and appends the twelve zero derivatives. The symbolic labels are bookkeeping coordinates, not new measured physical states. The exact clip is preserved. The contact-domain square root is not differentiated by the ODE validator.

## 4. Required validated integration contract (not yet implemented)

A source-faithful baseline certificate must provide, for every starting state/label in the specified box and one common fixed V, a validated tube over every closed step `[t_k,t_{k+1}]` and an endpoint enclosure at T. Following (42)–(43), the conceptual object is `x*(t)∈x̃(t)+R(t)` with a validated error residual. Each step must:

1. construct a rough compact box containing the proposed approximate path plus the complete error range;
2. prove all rational denominators stay away from zero on that full box and the entire parameter image satisfies its positivity contract;
3. evaluate the state RHS and interval Jacobian on that box with outward arithmetic, including `D(I)` at every clip branch and a proved multivariate mean-value inclusion;
4. enclose the residual differential/integral operator on a compact convex set and verify the inclusion/fixed-point condition used by the solver;
5. propagate the complete time-slab range and the endpoint through the same enclosure; a collection of validated endpoints without between-step tubes is insufficient;
6. retain the same twelve labels and V through every subdivision and step; subdivision refines proof work only;
7. check contact admissibility as a full-time predicate on each resulting state/parameter tube using the common outward checker. The formal ODE may be bounded outside the contact domain for analysis, but no physical theorem claim is allowed there.

The core residual mechanism is specified in Rauh & Auer (2011), §2, Algorithm 1, Eqs. (3)–(6), pp. 371–372. Given a nonvalidated approximation `x_app`, set

\[
r(R^{(k)},t)=-\dot x_{app}(t)+f(x_{app}(t)+R^{(k)}(t),t),\qquad
\dot R^{(k+1)}(t)\supseteq r(R^{(k)},t).
\]

The iteration has a verified residual enclosure only after `Rdot^(k+1)(t) ⊆ Rdot^k(t)` is checked on the complete time segment and all state/parameter ranges. The paper then encloses the error by integrating an outward range, including the direct bound `R^(k+1)(0)+t·r(R^k)([0,t],[0,t])`. The Auer 2013 derivative extension supplies the generalized Jacobian needed to tighten this residual evaluation at a piecewise-smooth branch. The definition of the derivative enclosure does not replace the residual inclusion test or fixed-point argument.

The article’s fixed-point discussion depends on compact convex tube domains and an inclusion property. A finite number of Picard iterations, a small interval, local Lipschitz continuity by itself, or a floating trajectory does not establish inclusion. A proposed step size must be validated by the actual inclusion condition; no arbitrary contraction claim is made for a finite hold. Inability to prove inclusion means `UNKNOWN`.

Termination/resource semantics for a future finite implementation: cap time steps, Picard iterations, branch splits, RHS/Jacobian calls, memory and wall time before a run. If a step needs subdivision, count it against the predeclared cap while preserving the same V and labels. Unsupported equations, invalid dimensions or invalid rational data are `INVALID_INPUT`; a valid query that exhausts a cap, fails an inclusion check or times out is `UNKNOWN` (with reason); crashes and inconsistent interval intersections are separately reported implementation failures. None may produce `CERTIFIED`. Successful output must contain every tube segment, the endpoint, parameter enclosure, proof status and resource counters.

The local derivative preflight uses exact `Fraction` intervals and therefore has no machine rounding. This does not replace the legacy solver’s binary directed-rounding backend. A future VALENCIA port/build needs a tested directed-rounding PROFIL/BIAS configuration and audited compiler/runtime arithmetic semantics. No fast-math or unverified rounding-mode behavior is acceptable.

## 5. Contact and collision checker contract

After integration review, map the method’s 21-coordinate tube to the common representation: a physical 9-state range plus the unchanged 12 label ranges for every closed time segment. The adapter may hull multiple time pieces but cannot omit segment boundaries or widen only endpoints. The common checker evaluates the full-time collision and contact sufficient predicates for each complete segment and all fixed labels. Collision includes the pose tube/radius. Contact retains the current exact algebraic capacity predicate and does not differentiate its square root at saturation. Any checker-side dependency loss is reported.

R3 native certificates and results remain historical. If a reviewed common checker changes representation tightness, the R3 result is a separate `R3_COMMON_CHECK` series; never overwrite the native R3 producer/checker records.

## 6. Development evidence and explicit gaps

The targeted exact-rational check report covers both corners, intervals crossing either or both thresholds, 212 ordered secant pairs, a multivariate affine mean-value inclusion, the 21-coordinate fixed-label shape, invalid parameter-domain rejection, exact interval arithmetic and rejection of a tampered scalar-lemma record. The scalar reference harness reproduces Auer et al. §4.1, Eqs. (34)–(35): exact function-range closure `[-1,6]`, the paper’s naive mean-value result `[-3/2,9/2]` that misses 6, and a jump-corrected derivative enclosure `[1,6]` whose mean-value enclosure contains the whole reference range.

These results check only the implemented algebraic specialization and scalar illustration. They do not check an ODE Picard inclusion, full-time DDWMR tube, exact article §5 friction/hysteresis simulation, collision/contact checker, or independent review. Table 2’s printed static-friction interval has reversed endpoints `[0.15,0.03] N`; no authoritative correction or exact numeric enclosure table was found. Do not silently change it or infer plot pixels as exact output data.
