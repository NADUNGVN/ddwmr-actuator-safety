# G2 candidate v1: voltage-dependent joint enclosure for one hold

2026-09-29. **DERIVED CANDIDATE FOR INDEPENDENT REVIEW; G2 UNVERIFIED.** Governing formulation: canonical MASTER v2.1; G1 PASS for restricted reduced-model consistency. User authorized G2 research after commit `4ee3c82c1c944119ad2b9923bfd830a1b6480503`. No G3 construction, numerical implementation or gate acceptance is contained here.

## 0. Deliverable and limits

This note supplies an explicit six-state electromechanical/contact decomposition, finite exponential-Picard predictors, comparison error bounds, pose lifting, and sufficient collision/contact checks on the complete hold. Proofs are given for exact mathematical objects. A finite evaluation contract is specified separately below; the original v1 package supplied no concrete certified arithmetic case or useful numerical operating range.

R2 review supplement (2026-09-29): [Case A](G2_FINITE_CERTIFICATE_CASE_A_v1.md) now submits one synthetic finite rational certificate for independent review. It does not establish a general implemented solver or practical usefulness. [GPT's review of v1](../../docs/reviews/GPT_TO_CODEX_G2_REVIEW_7390942f_FULL_HANDOFF.md) accepted analytic soundness subject to the Section 2 wording correction applied here. G2 remains UNVERIFIED; all tagged equations below are unchanged.

The comparison and integral-iteration machinery is established methodology, not a novelty claim. See [the primary-source overlap audit](../../docs/reviews/G2_PRIOR_ART_AND_BLOCKERS_v1.md). The branch claiming novelty from a generic growth bound, fixed-parameter augmentation, or tube inclusion alone is **BLOCKED**. Applicability and usefulness of this particular construction remain review questions.

No assumption is added to the plant. In particular, phi remains known, bounded, globally Lipschitz and strictly sign preserving, without mandatory differentiability, oddness or monotonicity. A computable representation of phi and Theta is an outstanding data requirement for finite numerical evaluation, not an assumed theorem about every Lipschitz function or compact set.

## 1. Fixed-parameter decomposition

For one hold, shift its start to time zero. Fix the measured initial state x_0, the same voltage V in U for every hidden parameter, and T>0. All objects below are indexed by one execution-fixed parameter realization vartheta in Theta; suppress that index only within a fiber. No center or certificate allows the controller to choose V after seeing vartheta.

Let

\[
z=(u,r,\omega_L,\omega_R,i_L,i_R)^\top,\qquad
\dot z=Az+BV+DF(z),\qquad F_j(z)=C_j\phi((Sz)_j/v_s). \tag{G2.1}
\]

The matrices are

\[
A=\begin{pmatrix}
-c_u/m&0&0&0&0&0\\
0&-c_r/I_z&0&0&0&0\\
0&0&-B_L/J_L&0&k_L/J_L&0\\
0&0&0&-B_R/J_R&0&k_R/J_R\\
0&0&-k_L/L_L&0&-R_L/L_L&0\\
0&0&0&-k_R/L_R&0&-R_R/L_R
\end{pmatrix},\quad
B=\begin{pmatrix}0&0\\0&0\\0&0\\0&0\\1/L_L&0\\0&1/L_R\end{pmatrix}, \tag{G2.2}
\]

\[
D=\begin{pmatrix}1/m&1/m\\-b/I_z&b/I_z\\-R_w/J_L&0\\0&-R_w/J_R\\0&0\\0&0\end{pmatrix},\quad
S=\begin{pmatrix}-1&b&R_w&0&0&0\\-1&-b&0&R_w&0&0\end{pmatrix}. \tag{G2.3}
\]

Thus Sz is slip velocity, not a slip ratio. B is an input matrix, whereas B_j denotes wheel damping. D maps forces to state derivatives; its negative wheel reaction entries are retained in every predictor. All occurrences of A,B,D,S,C,v_s in a fiber use the same vartheta, including gear correlations.

Absolute values and inequalities between vectors/matrices are componentwise unless a norm is written. Define

\[
\Lambda=\operatorname{diag}(C_L L_\phi/v_s,C_R L_\phi/v_s),\qquad
Q=\Lambda |S|\in\mathbb R_{\ge0}^{2\times6}. \tag{G2.4}
\]

The global incremental bound is

\[
|F(z)-F(w)|\le \Lambda|S(z-w)|\le Q|z-w|. \tag{G2.5}
\]

No Jacobian of phi is used. Each row of Q times a state difference has force units. Matrix entries have coordinate-dependent units; numerical matrix norms below require a declared fixed diagonal state scaling first, not addition of incompatible physical units.

## 2. Predictors: why freezing force alone is insufficient

Set z^{-1}(t)=z_0 and, for any finite n>=0, define

\[
z^n(t)=e^{At}z_0+\int_0^t e^{A(t-s)}[BV+DF(z^{n-1}(s))]ds. \tag{G2.6}
\]

These are explicit finite nested integrals, not calls to the unknown nonlinear solution. All iterates start at z_0. They satisfy

\[
\dot z^n=Az^n+BV+DF(z^{n-1}). \tag{G2.7}
\]

For n=0 the force is frozen at its initial value. Its u and r center components are independent of V, since the first two rows of A are decoupled and the first two rows of B vanish. A safety filter using only that center can miss directional benefit from changing voltage and reflect voltage mainly through uncertainty inflation. **Do not present the n=0 center as an adequate voltage-aware avoidance construction.**

Use n>=1 as the research candidate: the voltage-dependent current/wheel components can make the slip entering F(z^0) voltage-dependent, so n=1 is the first predictor depth at which the body-center predictor can depend on voltage through the contact law. The adopted phi class does not guarantee a nonzero or monotone force change. More iterations may be needed for a useful certificate. This is mathematical quadrature/iteration, not a change in ZOH input. V is constant through every integral.

Define the computable-in-principle residual bound

\[
d_{n,j}(t)=\min\{(\Lambda |S(z^n(t)-z^{n-1}(t))|)_j,\ 2C_j\}. \tag{G2.8}
\]

Then |F(z^n)-F(z^{n-1})|<=d_n. The exact absolute residual may instead be used when its evaluation is certified. No time derivatives of contact force or phi are required.

## 3. Lemma 1: global comparison radius

Let A^# retain A's diagonal and replace its off-diagonal entries by their absolute values. Put

\[
M=A^\#+|D|Q,\qquad
E_{n,0}(t)=\int_0^t e^{M(t-s)}|D|d_n(s)ds. \tag{G2.9}
\]

M is Metzler, so E_{n,0}>=0. For every fixed vartheta, common V and all t in [0,T],

\[
|z_\vartheta(t)-z^n_\vartheta(t)|\le E_{n,0,\vartheta}(t). \tag{G2.10}
\]

**Proof.** Let epsilon=z-z^n. Subtract (G2.7) from (G2.1) and insert F(z^n):

\[
\dot\epsilon=A\epsilon+D[F(z)-F(z^n)]+D[F(z^n)-F(z^{n-1})].
\]

For each component, the upper right Dini derivative of its absolute value obeys

\[
D^+|\epsilon|\le A^\#|\epsilon|+|D|Q|\epsilon|+|D|d_n
=M|\epsilon|+|D|d_n.
\]

At zero components the same bound follows by the absolute value of the component derivative. The linear Metzler comparison system with initial value zero yields (G2.10). Global Lipschitz contact bounds justify the estimate without assuming the unknown trajectory stays in a guessed local box. Finite-horizon existence of the formal ODE is already part of the accepted model. QED.

**Restriction.** This is an enclosure of the formal ODE. Continuing its formula outside D_c is a mathematical bounding device only; no skid mode or physical continuation is claimed. Section 6 separately verifies full-hold contact admissibility. The argument therefore does not assume the property it is meant to check.

## 4. Lemma 2: optional exact impulse-response refinement

The signed motor block in A includes back-EMF cancellation. Taking absolute off-diagonal entries can lose damping and make (G2.9) very loose. It is not valid to assume M is stable because the physical motor block is stable.

To recover some cancellation before taking absolute values, define

\[
H(t)=|e^{At}D|,\quad K(t)=H(t)Q,\quad
a_n(t)=\int_0^t H(t-s)d_n(s)ds. \tag{G2.11}
\]

Starting from E_{n,0}, for finite ell>=0 set

\[
E_{n,\ell+1}(t)=a_n(t)+\int_0^t K(t-s)E_{n,\ell}(s)ds. \tag{G2.12}
\]

Every refinement is sound and nonincreasing:

\[
|z-z^n|\le E_{n,\ell+1}\le E_{n,\ell},\qquad \ell\ge0. \tag{G2.13}
\]

**Proof.** Variation of constants for epsilon and (G2.5) give |epsilon|<=a_n+K*|epsilon|. K has nonnegative entries, so substituting any sound upper radius preserves soundness. The standard entrywise bound |e^{At}|<=e^{A^#t} implies H(t)<=e^{A^#t}|D|. Equation (G2.9) also solves

\[
E_{n,0}=e^{A^\#\cdot}*|D|(d_n+QE_{n,0}).
\]

Hence E_{n,1}<=E_{n,0}; order preservation of convolution gives the remaining inequalities by induction. This argument needs neither infinite iteration nor convergence to define a finite candidate. QED.

This refinement is still a generic Volterra/comparison technique. It does not restore all force/state correlations or prove a runtime advantage. Numerical rounding must not invalidate the inequalities; a looser validated upper radius is acceptable.

## 5. Theorem candidate G2-A: pose lifting and joint enclosure

Choose finite n>=1 and ell>=0; write E=E_{n,ell}. Define the reference pose by integration, using an unwrapped angle on this hold:

\[
\theta^n(t)=\theta_0+\int_0^t r^n(s)ds,\quad
p^n(t)=p_0+\int_0^t u^n(s)e(\theta^n(s))ds,
\quad e(\theta)=(\cos\theta,\sin\theta)^\top. \tag{G2.14}
\]

Define

\[
E_\theta(t)=\int_0^t E_r(s)ds,\qquad
E_p(t)=\int_0^t[E_u(s)+|u^n(s)|\min\{E_\theta(s),2\}]ds. \tag{G2.15}
\]

The fiber tube consists of states satisfying

\[
|z-z^n_\vartheta(t)|\le E_\vartheta(t),\quad
|\theta-\theta^n_\vartheta(t)|\le E_{\theta,\vartheta}(t),\quad
\|p-p^n_\vartheta(t)\|_2\le E_{p,\vartheta}(t). \tag{G2.16}
\]

Retain the joint graph structure by defining

\[
\widehat{\mathscr R}_n^\ell(t)=
\bigcup_{\vartheta\in\Theta}
\{(x,\vartheta):x\text{ satisfies (G2.16) for that same }\vartheta\}. \tag{G2.17}
\]

Then the exact reachable pairs from MASTER satisfy

\[
\mathscr R(t;x_0,V)\subseteq\widehat{\mathscr R}_n^\ell(t),\qquad
\mathscr R([0,T];x_0,V)\subseteq\bigcup_{t\in[0,T]}\widehat{\mathscr R}_n^\ell(t). \tag{G2.18}
\]

**Proof.** Lemmas 1–2 give internal-state inclusion for each fixed parameter. Integrating r-r^n gives E_theta. The unit-heading identity yields

\[
\|e(\theta)-e(\theta^n)\|_2
\le\min\{|\theta-\theta^n|,2\}.
\]

Split the translational velocity difference as (u-u^n)e(theta)+u^n[e(theta)-e(theta^n)]. The triangle inequality and integration yield E_p. Take the union over fixed parameters, never replacing their labels or changing voltage, and then over time. QED.

Parameter-dependent centers are mathematical families indexed by known uncertainty bounds. They are not measurements of hidden parameters. Enumerating a favorable member is not a robust certificate. A Cartesian overapproximation may be used later only with an explicit inclusion and acknowledged loss of dependence.

## 6. Theorem candidate G2-B: sufficient continuous collision/contact checks

For every parameter fiber and time, define

\[
\beta_j(t,\vartheta)=\min\left\{1,
\left|\phi((Sz^n(t))_j/v_s)\right|
+(L_\phi/v_s)(|S|E(t))_j\right\}. \tag{G2.19}
\]

For all internal states in the box (G2.16), |phi((Sz)_j/v_s)|<=beta_j. Therefore

\[
\underline A(t,\vartheta)=\sum_j C_j\sqrt{1-\beta_j(t,\vartheta)^2},\quad
\overline Y(t,\vartheta)=m(|u^n(t)|+E_u(t))(|r^n(t)|+E_r(t)) \tag{G2.20}
\]

are respectively a lower bound on available lateral capacity and an upper bound on |mur|. For one circular obstacle set

\[
g_p(t,\vartheta)=\|p^n(t)-p_o\|_2-R_s-E_p(t),\quad
g_c(t,\vartheta)=\underline A(t,\vartheta)-\overline Y(t,\vartheta). \tag{G2.21}
\]

If one common V in U satisfies

\[
\forall\vartheta\in\Theta\ \forall t\in[0,T]:\quad g_p(t,\vartheta)\ge0,\quad g_c(t,\vartheta)\ge0, \tag{G2.22}
\]

the tube is contained in mathscr S_c throughout the hold. Consequently the true restricted-model trajectory has h>=0 and belongs to D_c(vartheta) continuously. For finitely many static obstacles, require the position inequality for each obstacle.

**Proof.** The reverse triangle inequality implies ||p-p_o||>=R_s for every tube position. Monotonicity of sqrt(1-b^2) on b in [0,1] and (G2.19) imply A(z,vartheta)>=underline A. Also |mur|<=overline Y, so the exact algebraic contact condition is satisfied for every tube state with the same label. Invoke G2-A. QED.

No derivative of the square-root margin is taken. If beta_j=1, that wheel contributes zero certified lateral reserve. If both are one, the certificate requires overline Y=0. Failure is inconclusive; it neither proves actual contact loss nor unavoidable collision. The interval product can be especially conservative near ur=0 when box correlations are lost.

This is a sufficient one-hold certificate only. It imposes no robust endpoint return, constructs no K_T, and proves no repeated feasibility. Its selection over V need not be affine or convex; no QP architecture follows from this theorem.

## 7. Finite evaluation contract: no sampling masquerading as certification

Theorems G2-A/B are analytic statements. Their universal checks do not become an executable certificate by evaluating finitely many ordinary trajectories. A finite certified evaluation needs:

1. A finite outer cover of the declared Theta preserving positive denominators, with each parameter cell labeled and carried unchanged throughout the hold. Correlations should remain constraints; using a box hull is a named outer relaxation, not an exact representation.
2. Validated point/interval evaluation of the selected known phi and a certified upper bound for L_phi. Given such a point evaluator, the Lipschitz inequality supplies a convergent interval extension on a scalar interval. The currently abstract phi class by itself does not specify an evaluator.
3. Certified matrix exponentials, integrals and their parameter/time ranges, including rounding and quadrature remainders. Exact formulas in this note do not certify a floating-point `expm` or adaptive quadrature call.
4. Full coverage by time slabs I_a of [0,T]. Slab widths are verification subdivisions, **not** controller sampling periods. They never change V or reset vartheta.

For each slab I_a and parameter cell Theta_b obtain outward bounds on all expressions used in (G2.14–21). One sufficient finite check is

\[
\operatorname{dist}(P^n_{ab},p_o)-R_s-\overline E_{p,ab}\ge0, \tag{G2.23}
\]

where P^n_ab contains every reference position for (t,vartheta) in that cell, and

\[
\sum_j\underline C_{j,b}\sqrt{1-\overline\beta_{j,ab}^{\,2}}
-\overline m_b U_{ab}R_{ab}\ge0. \tag{G2.24}
\]

Here beta upper bounds are clipped to [0,1]; U_ab and R_ab bound |u^n|+E_u and |r^n|+E_r respectively. The distance must have a rigorous lower bound; for an axis-aligned position box it is computed coordinatewise. Use lower-rounded square roots in (G2.24). Products of extrema deliberately relax dependence within a cell and can only give a sufficient condition. Retain every cell in the union, including boundary cells. Sound but wide cells may give UNKNOWN.

An elementary route to certified exponentials exists without inverses: after fixed coordinate scaling, choose a compatible induced (hence submultiplicative) matrix norm, truncate the exponential series and use, for q>=||At||,

\[
\left\|e^{At}-\sum_{k=0}^N(At)^k/k!\right\|
\le e^q q^{N+1}/(N+1)!. \tag{G2.25}
\]

This bounds a range when q covers the whole parameter/time cell; interval arithmetic on the polynomial handles parameter dependence conservatively. It may be inefficient for stiff motors. Integrals similarly require enclosures of their integrands on complete subintervals and outward interval sums, or certified higher-order quadrature. Nonsmooth absolute values/minimum do not prevent interval bounds. Integrals with variable upper limit can be rewritten t times an integral over [0,1] before range evaluation.

Because predictor depth n and radius-refinement depth ell are finite, no nonlinear unknown-solution oracle occurs in these expressions. The generic compact set Theta still needs an effective outer-cover representation. Convergent interval evaluations, finite covers, and sufficiently strict positive margins can support a terminating verification; no unconditional termination at equality boundaries, no practical complexity bound and no usable T have been established. Arbitrary splitting does not remove the intrinsic radius conservatism.

### 7.1 Explicit conservative finite-cell radius assembly

The following fallback makes the radius part of that contract concrete; it uses ell=0. For each fixed parameter cell choose entrywise bounds M_b>=M(vartheta) and D_b>=|D(vartheta)| for every member. M_b must be Metzler. Set N_b equal to M_b with any negative diagonal entries replaced by zero, so N_b is entrywise nonnegative. On slab I_a=[t_a,t_(a+1)], obtain d_ab>=d_n(t,vartheta) uniformly. Using d_ab=2(C_L_upper,C_R_upper)^T is always a safe but loose fallback. Set q_ab=D_b d_ab and eta_0b=0. Recursively compute

\[
\eta_{a+1,b}=e^{N_b h_a}\eta_{ab}
+\int_0^{h_a}e^{N_b s}q_{ab}ds,\qquad h_a=t_{a+1}-t_a. \tag{G2.28}
\]

By positive comparison, every fiber error radius E_n,0 is bounded by the corresponding piecewise comparison solution; because N_b and q_ab are nonnegative, its value throughout I_a is no larger than eta_(a+1,b). Thus eta_(a+1,b) is a full-slab internal error bound, not just an endpoint estimate. No physical parameter changes at slab boundaries; this comparison system is a named outer relaxation.

Let U^n_ab uniformly bound |u^n| on the cell. Accumulate nonnegative pose radii from zero:

\[
\eta^\theta_{a+1,b}=\eta^\theta_{ab}+h_a\eta_{a+1,b,r},\qquad
\eta^p_{a+1,b}=\eta^p_{ab}
+h_a[\eta_{a+1,b,u}+U^n_{ab}\min\{\eta^\theta_{a+1,b},2\}]. \tag{G2.29}
\]

These final values upper-bound the angle and position errors throughout I_a. Evaluate (G2.23–24) with these radii and certified center/slip ranges. Every matrix/integral evaluation in (G2.28) still needs outward errors; its integral can use the series sum of N_b^k h_a^(k+1)/(k+1)! applied to q_ab with a norm-tail bound, avoiding an inverse even when N_b is singular.

This is an explicit finite sufficient certificate given the input representations and certified predictor ranges. It may be too conservative, particularly after discarding diagonal damping. It makes no claim that parameter/time subdivision alone recovers the tighter fiber radius, and it is not the proposed contribution by itself. Failure returns UNKNOWN. A tighter validated evaluation of the fiber formulas or Lemma 2 can replace it after its own inclusion is established.

## 8. Local-order and voltage-authority diagnostics

For fixed finite n and compact admissible parameter/input sets, as t tends to zero:

\[
z^0-z_0=O(t),\quad z^n-z^{n-1}=O(t^{n+1}),\quad
d_n=O(t^{n+1}),\quad E_{n,0}=O(t^{n+2}). \tag{G2.26}
\]

**Derivation.** Bounded coefficients and bounded contact forces give the first estimate. Subtract successive versions of (G2.6); Lipschitz F and bounded e^{At} supply one additional time integral at each iteration. Equations (G2.8–9) supply the other estimates. Constants depend on the initial state, finite horizon, scaling and parameter bounds. Refinements are no larger than E_n,0. Therefore E_theta=O(t^{n+3}) and E_p=O(t^{n+3}) for bounded u^n. These are local error orders, not tight uncertainty-width orders over Theta and not practical sampling limits.

An independent causal check compares two constant voltages V,W for the **same** initial state and parameter. With the same M,

\[
|z_V(t)-z_W(t)|\le\int_0^t e^{M(t-s)}|B||V-W|ds. \tag{G2.27}
\]

**Derivation.** Repeat the Dini comparison, replacing the predictor residual with the additive difference B(V-W). In the nonnegative off-diagonal graph of M, voltage enters currents; wheels are reached after one edge; u and r after two edges. Q has zero current columns. The power series for the integral thus yields current response O(t), wheel response O(t^2), body velocity/yaw-rate response O(t^3), heading response O(t^4), and position response O(t^4), using pose lifting with bounded body velocity. These are upper orders only; coefficients can vanish. They require no derivative of phi and establish no uniform HOCBF relative degree.

This explains why an immediate kinematic steering command cannot be assumed realizable. It does not prove a minimum available avoidance displacement, stopping authority, or feasibility boundary. Larger V_max enlarges the admissible action set, but radius inflation and optimized certified sets need not exhibit any claimed strict monotonic improvement without proof. No universal monotonic T_safe versus speed/capacity/distance claim is made.

## 9. Review disposition and exact open obligations

| Item | Current disposition |
|---|---|
| A,B,D,S decomposition | Explicit derivation; independent verification requested |
| Dini comparison and finite kernel refinement | Proof supplied; review pending; generic machinery |
| Fixed parameter joint enclosure | Explicit candidate; no parameter switching or voltage oracle |
| Collision/contact over full hold | Sufficient analytic checks supplied; no recursive claim |
| Finite arithmetic/representation | Contract specified; not implemented or validated |
| Useful T, parameter cells, runtime, conservatism | UNVERIFIED; no physical parameter set supplied |
| Novelty of generic comparison/Picard/parameter augmentation | Not claimed; branch BLOCKED as a standalone contribution |
| G2 gate | UNVERIFIED; this note does not pass it |
| G3, physical correspondence, implementation | Not authorized here / unverified as applicable |

The independent reviewer should check every equation and quantify whether any claim requires a stronger phi class or unavailable data. If the error radius is unusable on defensible motor/contact scales, stop the usefulness branch and reformulate the enclosure; do not select fictitious favorable parameters. Before a novelty claim, compare to existing growth-bound, parameter-dependent reachability, residual-certified integration and fixed-input safety methods at theorem/computation level.
