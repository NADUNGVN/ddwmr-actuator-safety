# GPT → CODEX G2 REVIEW HANDOFF — commit 7390942f

**Repository:** `NADUNGVN/ddwmr-actuator-safety`  
**Branch:** `main`  
**Reviewed commit:** `7390942f49e4e1b303fb37a2c060edcfa0036d5c`

**Review scope:** independent G2 audit of the current analytic enclosure candidate under authoritative MASTER v2.1.  
**Overall project status:** **HOLD**.  
**Gate status before this review:** G1 PASS — restricted reduced-model scope; G2/G3/G4 UNVERIFIED.  
**Physical-platform correspondence:** UNVERIFIED.  
**Implementation:** NOT AUTHORIZED.  
**G3 construction:** NOT AUTHORIZED.

This document is a complete handoff of GPT's independent G2 review. It is review evidence only. It does not amend MASTER or pass G2 by itself.

---

# 0. OPERATING INSTRUCTIONS FOR CODEX

Read this handoff together with the canonical repository state at commit:

`7390942f49e4e1b303fb37a2c060edcfa0036d5c`

Treat the following as authoritative until formally changed:

- `AGENTS.md`
- `research_context/MASTER_RESEARCH_CONTEXT_v2.md`
- `research_context/DECISION_LOG.md`
- `research_context/LITERATURE_MATRIX.md`
- `research_context/REVIEW_GATE.md`

Also use:

- `docs/GPT_G2_REVIEW_REQUEST_v1.md`
- `research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md`
- `docs/reviews/G2_PRIOR_ART_AND_BLOCKERS_v1.md`
- `docs/reviews/LUNA_G2_AUDIT_v1.md`

Do not treat Luna/GPT agreement as proof.

Do not silently change the plant or \(\phi\)-assumption class.

Do not start G3.

Do not implement controller/simulator/experiments.

Do not infer GO.

Use:

**Finding / Evidence / Consequence / Status / Required action**

for each substantive response.

---

# 1. AUTHORITATIVE CONTEXT AT REVIEWED COMMIT

## G1

G1 is already accepted for the restricted reduced-model scope:

\[
\boxed{
\text{G1 PASS — restricted reduced-model scope}
}
\]

Physical-platform correspondence remains:

\[
\boxed{
\text{UNVERIFIED}
}
\]

The accepted theoretical plant is the nine-state reduced ideal planar DDWMR:

\[
x=
[p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R]^\top.
\]

Input:

\[
V=[V_L,V_R]^\top.
\]

Exact lateral constraint:

\[
v_y=0.
\]

Longitudinal contact force:

\[
F_j=C_j\phi(\sigma_j/v_s).
\]

Effective tangential capacities:

\[
0<\underline C_j\le C_j\le\overline C_j.
\]

Combined tangential envelope:

\[
F_j^2+Y_j^2\le C_j^2.
\]

The hidden model parameter realization:

\[
\vartheta\in\Theta
\]

is fixed for the entire execution.

The controller knows \(x(kT)\) exactly at samples and knows \(\Theta\), but does not know the true \(\vartheta\).

The robust input quantifier remains:

\[
\exists V_k
\quad
\forall\vartheta\in\Theta.
\]

---

# 2. CURRENT G2 CANDIDATE

The G2 candidate introduces internal state

\[
z=
(u,r,\omega_L,\omega_R,i_L,i_R)^\top
\]

and writes

\[
\dot z
=
Az+BV+DF(z),
\]

where

\[
F_j(z)
=
C_j\phi((Sz)_j/v_s).
\]

The proposed construction contains:

1. exact six-state decomposition;
2. finite Picard-like predictors \(z^n\);
3. residual bounds \(d_n\);
4. componentwise Dini comparison radius \(E_{n,0}\);
5. optional signed impulse-response refinement \(E_{n,\ell}\);
6. pose lifting;
7. parameter-labeled joint tubes;
8. sufficient collision/contact checks;
9. a finite-cell certified-evaluation contract;
10. local asymptotic order analysis;
11. voltage-to-position causal upper-order diagnostics.

Generic comparison/reachability machinery is explicitly **not** claimed as novelty.

---

# 3. G2-01 — DECOMPOSITION \(A,B,D,S\)

## Finding

Equations (G2.1)–(G2.3) reproduce the authoritative nine-state plant correctly after extracting the six internal states

\[
z=
(u,r,\omega_L,\omega_R,i_L,i_R)^\top.
\]

## Evidence

From MASTER:

\[
m\dot u
=
F_L+F_R-c_uu,
\]

\[
I_z\dot r
=
b(F_R-F_L)-c_rr.
\]

Therefore the first two rows of \(A,D\) are:

\[
A_{11}=-c_u/m,
\qquad
A_{22}=-c_r/I_z,
\]

and force mapping:

\[
D_{u,:}
=
(1/m,\;1/m),
\]

\[
D_{r,:}
=
(-b/I_z,\;b/I_z).
\]

Wheel equations:

\[
J_L\dot\omega_L
=
k_Li_L-B_L\omega_L-R_wF_L,
\]

\[
J_R\dot\omega_R
=
k_Ri_R-B_R\omega_R-R_wF_R.
\]

Hence:

\[
D_{\omega_L,:}
=
(-R_w/J_L,\;0),
\]

\[
D_{\omega_R,:}
=
(0,\;-R_w/J_R).
\]

Electrical equations:

\[
L_j\dot i_j
=
V_j-R_ji_j-k_j\omega_j
\]

give the displayed \(A,B\).

Slip:

\[
\sigma_L
=
-u+br+R_w\omega_L,
\]

\[
\sigma_R
=
-u-br+R_w\omega_R.
\]

Thus the displayed matrix

\[
S
=
\begin{pmatrix}
-1&b&R_w&0&0&0\\
-1&-b&0&R_w&0&0
\end{pmatrix}
\]

is correct.

Signs remain consistent with G1.

## Consequence

No decomposition correction is required.

## Status

**VALID**

## Required action

Retain (G2.1)–(G2.3).

---

# 4. G2-02 — GLOBAL FORCE INCREMENT BOUND

## Finding

(G2.4)–(G2.5) are valid under only the adopted global Lipschitz assumption on \(\phi\).

## Evidence

For each side:

\[
|F_j(z)-F_j(w)|
=
C_j
\left|
\phi((Sz)_j/v_s)
-
\phi((Sw)_j/v_s)
\right|.
\]

Using global Lipschitz continuity:

\[
|F_j(z)-F_j(w)|
\le
\frac{C_jL_\phi}{v_s}
|(S(z-w))_j|.
\]

Define:

\[
\Lambda
=
\operatorname{diag}
\left(
C_LL_\phi/v_s,
C_RL_\phi/v_s
\right),
\]

and

\[
Q=\Lambda|S|.
\]

Then:

\[
|F(z)-F(w)|
\le
\Lambda|S(z-w)|
\le
Q|z-w|.
\]

No derivative of \(\phi\) is used.

No oddness is used.

No monotonicity is used.

## Consequence

The G2 nonlinear comparison is compatible with G1 assumptions.

## Status

**VALID**

## Required action

No change.

---

# 5. G2-03 — FINITE PREDICTOR AND \(n=0\)

The candidate defines:

\[
z^{-1}(t)=z_0
\]

and for \(n\ge0\):

\[
z^n(t)
=
e^{At}z_0
+
\int_0^t
e^{A(t-s)}
\left[
BV+DF(z^{n-1}(s))
\right]ds.
\]

Equivalent differential form:

\[
\dot z^n
=
Az^n+BV+DF(z^{n-1}).
\]

## Finding

The finite iteration is mathematically valid for every finite \(n\ge0\).

However, one sentence in Section 2 should be weakened.

## Evidence

For \(n=0\):

\[
\dot z^0
=
Az^0+BV+DF(z_0).
\]

Because the first two rows of \(B\) vanish and the first two rows of \(A\) do not receive wheel/current states,

\[
u^0,r^0
\]

are independent of \(V\).

The current states in \(z^0\) depend on \(V\), and the wheel states may therefore depend on \(V\).

Thus

\[
F(z^0)
\]

may become voltage-dependent.

However, with the adopted \(\phi\)-class, one may not assert that a changed slip **must** produce a changed force, because \(\phi\) is not assumed injective or monotone.

Therefore:

\[
n=1
\]

is the first predictor depth at which the body-center predictor **can** depend on voltage through the contact law.

It is not guaranteed to have nonzero directional voltage sensitivity.

## Consequence

The mathematical predictor construction is sound.

Only the interpretation sentence is slightly too strong.

## Status

**NEEDS REVISION** for wording only.

The predictor equations are **VALID**.

## Required action

Replace wording equivalent to:

> the wheel/current response in \(z^0\) changes \(F(z^0)\)

with:

> the wheel/current response in \(z^0\) makes \(F(z^0)\), and hence the \(n=1\) body center, potentially voltage-dependent.

Do not add monotonicity or injectivity to \(\phi\).

---

# 6. G2-04 — RESIDUAL BOUND \(d_n\)

The candidate defines:

\[
d_{n,j}(t)
=
\min
\left\{
(\Lambda|S(z^n-z^{n-1})|)_j,
2C_j
\right\}.
\]

## Finding

The residual bound is sound for all finite \(n\ge0\).

## Evidence

Lipschitz force difference:

\[
|F(z^n)-F(z^{n-1})|
\le
\Lambda|S(z^n-z^{n-1})|.
\]

Amplitude bound:

\[
|F_j(z)|\le C_j.
\]

Therefore:

\[
|F_j(z^n)-F_j(z^{n-1})|
\le
2C_j.
\]

The exact residual is bounded by both quantities, hence by their minimum.

No force derivative is required.

## Consequence

The predictor defect can be bounded without strengthening the contact law.

## Status

**VALID**

## Required action

No change.

---

# 7. G2-05 — DINI COMPARISON / LEMMA 1

Define \(A^\#\) by preserving the diagonal of \(A\) and replacing off-diagonal entries by absolute values.

Define:

\[
M
=
A^\#+|D|Q.
\]

Then:

\[
E_{n,0}(t)
=
\int_0^t
e^{M(t-s)}
|D|d_n(s)\,ds.
\]

The claimed bound is:

\[
|z(t)-z^n(t)|
\le
E_{n,0}(t).
\]

## Finding

The proof is analytically sound under merely Lipschitz \(\phi\).

## Evidence

Let:

\[
\epsilon=z-z^n.
\]

Subtract exact and predictor equations:

\[
\dot\epsilon
=
A\epsilon
+
D[F(z)-F(z^n)]
+
D[F(z^n)-F(z^{n-1})].
\]

Componentwise Dini derivative:

\[
D^+|\epsilon|
\le
A^\#|\epsilon|
+
|D|Q|\epsilon|
+
|D|d_n.
\]

Hence:

\[
D^+|\epsilon|
\le
M|\epsilon|
+
|D|d_n.
\]

\(M\) is Metzler.

The positive comparison system with zero initial error yields:

\[
|\epsilon(t)|
\le
\int_0^t
e^{M(t-s)}
|D|d_n(s)\,ds.
\]

At zero error components, the Dini derivative is bounded by absolute component derivative, so no differentiability of absolute value at zero is needed.

## Consequence

The main global analytic error enclosure is correct.

## Status

**VALID**

## Required action

No change.

---

# 8. G2-06 — EXACT IMPULSE-RESPONSE REFINEMENT

The candidate defines:

\[
H(t)=|e^{At}D|,
\]

\[
K(t)=H(t)Q,
\]

\[
a_n(t)
=
\int_0^t
H(t-s)d_n(s)\,ds.
\]

Then:

\[
E_{n,\ell+1}(t)
=
a_n(t)
+
\int_0^t
K(t-s)E_{n,\ell}(s)\,ds.
\]

Claim:

\[
|z-z^n|
\le
E_{n,\ell+1}
\le
E_{n,\ell}.
\]

## Finding

The refinement is sound and monotone nonincreasing.

The convolution order and units are consistent.

## Evidence

Variation of constants gives:

\[
|\epsilon|
\le
a_n+K*|\epsilon|.
\]

Thus any sound radius \(E\ge|\epsilon|\) produces another sound radius:

\[
a_n+K*E.
\]

The standard componentwise exponential bound gives:

\[
|e^{At}|
\le
e^{A^\#t}.
\]

Hence:

\[
H(t)
\le
e^{A^\#t}|D|.
\]

The global comparison solution also satisfies the integral identity:

\[
E_{n,0}
=
e^{A^\#\cdot}*|D|
\left(
d_n+QE_{n,0}
\right).
\]

Therefore:

\[
E_{n,1}
=
a_n+K*E_{n,0}
\le
E_{n,0}.
\]

Because \(K\ge0\), induction gives:

\[
E_{n,\ell+1}
\le
E_{n,\ell}.
\]

Dimensionally, after time convolution, \(H*d_n\) and \(K*E\) both have state units.

## Consequence

Lemma 2 is a valid tightening.

It is generic Volterra/comparison machinery, not an established novelty contribution.

## Status

**VALID**

## Required action

No analytic change.

Any numerical implementation must preserve outward bounds.

---

# 9. G2-07 — POSE LIFTING

Reference heading and position:

\[
\theta^n(t)
=
\theta_0+\int_0^t r^n(s)\,ds,
\]

\[
p^n(t)
=
p_0+\int_0^t
u^n(s)e(\theta^n(s))\,ds.
\]

Pose radii:

\[
E_\theta(t)
=
\int_0^tE_r(s)\,ds,
\]

\[
E_p(t)
=
\int_0^t
\left[
E_u(s)
+
|u^n(s)|
\min\{E_\theta(s),2\}
\right]ds.
\]

## Finding

The lifting is sound.

## Evidence

Heading difference:

\[
|\theta-\theta^n|
\le
E_\theta.
\]

Unit-vector identity:

\[
\|e(\theta)-e(\theta^n)\|_2
\le
\min\{|\theta-\theta^n|,2\}.
\]

Velocity error split:

\[
u e(\theta)
-
u^ne(\theta^n)
=
(u-u^n)e(\theta)
+
u^n
\left[
e(\theta)-e(\theta^n)
\right].
\]

Therefore:

\[
\|
u e(\theta)
-
u^ne(\theta^n)
\|
\le
E_u
+
|u^n|
\min\{E_\theta,2\}.
\]

Integrating yields \(E_p\).

## Consequence

The six-state internal tube lifts correctly to pose.

## Status

**VALID**

## Required action

No change.

---

# 10. G2-08 — JOINT PARAMETER-LABELED TUBE

The candidate defines:

\[
\widehat{\mathscr R}_n^\ell(t)
=
\bigcup_{\vartheta\in\Theta}
\{
(x,\vartheta):
x\text{ lies in the fiber tube for that same }\vartheta
\}.
\]

## Finding

This preserves fixed-parameter state/parameter dependence.

## Evidence

For every fiber:

- \(A,B,D,S,C_j,v_s\) use the same \(\vartheta\);
- the same \(\vartheta\) persists across the entire hold;
- the same candidate voltage \(V\) is used for all fibers.

No favorable fiber is selected by the controller.

## Consequence

The analytic construction does not silently replace:

\[
\exists V\forall\vartheta
\]

with:

\[
\forall\vartheta\exists V.
\]

## Status

**VALID**

## Required action

Any later Cartesian or coefficient-box relaxation must be explicitly labeled as an outer approximation.

---

# 11. G2-09 — COLLISION CERTIFICATE

Define:

\[
g_p(t,\vartheta)
=
\|p^n(t)-p_o\|_2
-
R_s
-
E_p(t).
\]

## Finding

The condition

\[
g_p\ge0
\]

is a sound sufficient collision-clearance certificate for the full position tube.

## Evidence

For any tube state:

\[
\|p-p_o\|
\ge
\|p^n-p_o\|
-
\|p-p^n\|.
\]

Since:

\[
\|p-p^n\|
\le
E_p,
\]

then:

\[
g_p\ge0
\]

implies:

\[
\|p-p_o\|
\ge
R_s.
\]

## Consequence

Collision safety follows for all states inside the certified tube.

## Status

**VALID**

## Required action

No change.

---

# 12. G2-10 — CONTACT-DOMAIN CERTIFICATE

Define:

\[
\beta_j
=
\min
\left\{
1,\,
|\phi((Sz^n)_j/v_s)|
+
(L_\phi/v_s)(|S|E)_j
\right\}.
\]

Then:

\[
\underline A
=
\sum_j
C_j\sqrt{1-\beta_j^2},
\]

\[
\overline Y
=
m
(|u^n|+E_u)
(|r^n|+E_r).
\]

Define:

\[
g_c
=
\underline A-\overline Y.
\]

## Finding

The contact-domain certificate is sound.

## Evidence

For every internal tube state:

\[
|(Sz)_j-(Sz^n)_j|
\le
(|S|E)_j.
\]

Therefore:

\[
|\phi((Sz)_j/v_s)|
\le
\beta_j.
\]

Actual lateral reserve:

\[
C_j
\sqrt{
1-\phi((Sz)_j/v_s)^2
}
\]

is therefore lower bounded by:

\[
C_j
\sqrt{
1-\beta_j^2
}.
\]

Also:

\[
|u|
\le
|u^n|+E_u,
\]

\[
|r|
\le
|r^n|+E_r.
\]

Thus:

\[
|mur|
\le
\overline Y.
\]

Hence:

\[
g_c\ge0
\]

implies:

\[
\sum_j
C_j\sqrt{1-\phi_j^2}
\ge
|mur|,
\]

which is exactly the algebraic contact-validity condition.

## Consequence

The candidate proves a sufficient full-hold contact-validity condition for the restricted model.

## Status

**VALID**

## Required action

No change.

---

# 13. G2-11 — \(\beta_j=1\), ZERO RESERVE, AND SATURATION EDGE CASE

## Finding

The edge case is handled correctly.

## Evidence

If:

\[
\beta_j=1,
\]

then:

\[
C_j\sqrt{1-\beta_j^2}=0.
\]

If both sides have:

\[
\beta_L=\beta_R=1,
\]

then:

\[
\underline A=0.
\]

For:

\[
g_c\ge0,
\]

we require:

\[
\overline Y=0.
\]

Because:

\[
m>0,
\]

this implies:

\[
(|u^n|+E_u)
(|r^n|+E_r)
=
0.
\]

Thus either every tube \(u\) is zero or every tube \(r\) is zero, guaranteeing:

\[
ur=0
\]

throughout the tube.

No derivative of:

\[
\sqrt{1-\beta^2}
\]

is taken.

## Consequence

No hidden regularity assumption appears at the force-budget boundary.

## Status

**VALID**

## Required action

No change.

---

# 14. G2-12 — NONCIRCULAR CONTACT-DOMAIN LOGIC

## Finding

The enclosure proof does not assume contact-domain invariance in order to prove it.

## Evidence

The formal ODE:

\[
\dot z
=
Az+BV+DF(z)
\]

remains mathematically defined outside:

\[
D_c(\vartheta).
\]

The global Lipschitz contact-force law therefore permits construction of the comparison tube over the entire hold without first assuming:

\[
x(t)\in D_c(\vartheta).
\]

Only afterward does the candidate check:

\[
g_c(t,\vartheta)\ge0.
\]

## Consequence

The logic is noncircular.

Continuation outside \(D_c\) is only a mathematical comparison device.

No physical skid continuation is claimed.

## Status

**VALID**

## Required action

Retain the existing restriction statement.

---

# 15. G2-13 — FINITE-CELL COMPARISON FALLBACK

For a parameter cell \(\Theta_b\), the candidate defines:

\[
M_b\ge M(\vartheta)
\]

entrywise.

Replace negative diagonals by zero to form nonnegative:

\[
N_b.
\]

Let:

\[
d_{ab}
\ge
d_n(t,\vartheta)
\]

uniformly over slab \(I_a\) and cell \(\Theta_b\).

Set:

\[
q_{ab}=D_bd_{ab}.
\]

Recurrence:

\[
\eta_{a+1,b}
=
e^{N_bh_a}\eta_{ab}
+
\int_0^{h_a}
e^{N_bs}q_{ab}\,ds.
\]

## Finding

This fallback is analytically sound.

## Evidence

For all \(\vartheta\in\Theta_b\):

\[
N_b\ge M(\vartheta)
\]

entrywise.

The comparison forcing:

\[
q_{ab}
\]

dominates the true radius forcing over the entire slab.

The positive comparison solution therefore dominates every fiber error.

Because:

\[
N_b\ge0,
\qquad
q_{ab}\ge0,
\qquad
\eta\ge0,
\]

we have:

\[
\dot\eta
=
N_b\eta+q_{ab}
\ge0.
\]

Therefore the slab endpoint:

\[
\eta_{a+1,b}
\]

is also an upper bound for all intermediate times in that slab.

No physical parameter is changed at slab boundaries; only the comparison overapproximation changes.

## Consequence

(G2.28) is a genuine full-slab sufficient comparison, not endpoint sampling.

It can be extremely loose.

## Status

**VALID analytically**

## Required action

Retain it only as a conservative fallback.

Do not advertise it as the preferred or useful enclosure without quantitative evidence.

---

# 16. G2-14 — FINITE-CELL POSE RADIUS

The candidate defines:

\[
\eta^\theta_{a+1,b}
=
\eta^\theta_{ab}
+
h_a\eta_{a+1,b,r},
\]

\[
\eta^p_{a+1,b}
=
\eta^p_{ab}
+
h_a
\left[
\eta_{a+1,b,u}
+
U^n_{ab}
\min\{\eta^\theta_{a+1,b},2\}
\right].
\]

## Finding

These formulas are sound slab-wide upper bounds.

## Evidence

Within slab \(I_a\):

\[
E_r(t)
\le
\eta_{a+1,b,r}.
\]

Hence:

\[
E_\theta(t)
\le
\eta^\theta_{ab}
+
h_a\eta_{a+1,b,r}.
\]

Similarly:

\[
E_u(t)
\le
\eta_{a+1,b,u}
\]

and:

\[
|u^n(t)|
\le
U^n_{ab}.
\]

Substitute into the position-error integrand and integrate over width \(h_a\).

## Consequence

The angle/position fallback is also full-slab, not endpoint-only.

## Status

**VALID analytically**

## Required action

No analytic change.

---

# 17. G2-15 — MATRIX EXPONENTIAL TAIL BOUND

The candidate uses:

\[
\left\|
e^{At}
-
\sum_{k=0}^{N}
\frac{(At)^k}{k!}
\right\|
\le
e^q
\frac{q^{N+1}}{(N+1)!},
\]

with:

\[
q\ge\|At\|.
\]

## Finding

This is a valid conservative bound under the explicitly stated compatible submultiplicative norm.

## Evidence

By submultiplicativity:

\[
\left\|
\sum_{k=N+1}^{\infty}
\frac{(At)^k}{k!}
\right\|
\le
\sum_{k=N+1}^{\infty}
\frac{\|At\|^k}{k!}
\le
\sum_{k=N+1}^{\infty}
\frac{q^k}{k!}.
\]

The exponential tail satisfies:

\[
\sum_{k=N+1}^{\infty}
\frac{q^k}{k!}
\le
e^q
\frac{q^{N+1}}{(N+1)!}.
\]

The candidate correctly requires fixed state-coordinate scaling before numerical norms are interpreted.

## Consequence

There is a mathematically valid finite route to enclosing exponentials without matrix inversion.

This says nothing about efficiency for stiff motor dynamics.

## Status

**VALID**

## Required action

Keep the scaling qualification explicit.

---

# 18. G2-16 — ANALYTIC INCLUSION VS FINITE CERTIFIED COMPUTATION

## Finding

The candidate currently provides:

\[
\boxed{
\text{a sound analytic construction}
}
\]

and:

\[
\boxed{
\text{a conditional finite-certification specification}
}
\]

but not yet:

\[
\boxed{
\text{an instantiated certified computation}.
}
\]

## Evidence

The authoritative context still lacks:

- a selected machine-evaluable \(\phi\);
- a certified numerical \(L_\phi\) for that selected representation;
- an effective finite representation of generic compact \(\Theta\);
- explicit parameter cells;
- validated center/predictor ranges;
- outward-rounded matrix exponential evaluations;
- certified nested integral bounds;
- validated pose/trigonometric bounds;
- any actual evaluated positive \(g_p\) margin;
- any actual evaluated positive \(g_c\) margin.

The candidate correctly acknowledges these omissions.

Therefore:

\[
\forall t,\forall\vartheta
\]

has not yet been reduced to a completed finite arithmetic certificate for a concrete declared mathematical data set.

## Consequence

The G2 gate cannot pass merely because the finite-evaluation contract is logically coherent.

A "constructed computable enclosure" requires a genuine finite certified realization or an equivalently complete theorem-level finite algorithm with every primitive enclosure defined.

## Status

\[
\boxed{
\textbf{UNVERIFIED for actual finite certified computation}
}
\]

## Required action

Before G2 acceptance, provide an explicit mathematical instance with:

1. selected \(\phi\);
2. certified \(L_\phi\);
3. effective \(\Theta\) representation;
4. finite cells;
5. outward interval/exact arithmetic primitives;
6. full-time predictor/radius ranges;
7. certified safety/contact margins.

Ordinary floating-point trajectory sampling does not satisfy this requirement.

---

# 19. G2-17 — LOCAL PREDICTOR ERROR ORDERS

The candidate claims, for fixed finite \(n\):

\[
z^0-z_0=O(t),
\]

\[
z^n-z^{n-1}=O(t^{n+1}),
\]

\[
d_n=O(t^{n+1}),
\]

\[
E_{n,0}=O(t^{n+2}).
\]

## Finding

These local orders are correct.

## Evidence

The first finite predictor departs from the initial state linearly:

\[
z^0-z_0=O(t).
\]

Successive predictor differences satisfy:

\[
z^n-z^{n-1}
=
\int_0^t
e^{A(t-s)}D
\left[
F(z^{n-1})
-
F(z^{n-2})
\right]ds.
\]

Lipschitz \(F\) adds one order through integration.

Thus recursively:

\[
z^n-z^{n-1}
=
O(t^{n+1}).
\]

Then:

\[
d_n
=
O(t^{n+1}),
\]

and one additional integration in (G2.9) gives:

\[
E_{n,0}
=
O(t^{n+2}).
\]

Consequently:

\[
E_\theta
=
O(t^{n+3}),
\]

\[
E_p
=
O(t^{n+3})
\]

for locally bounded \(u^n\).

## Consequence

The asymptotic predictor/error-order statement is valid.

It does not give practical sampling limits or uncertainty-width order over \(\Theta\).

## Status

**VALID**

## Required action

No change.

---

# 20. G2-18 — UPPER VOLTAGE-TO-POSITION RESPONSE ORDER

For two constant voltages \(V,W\) and the same \((x_0,\vartheta)\):

\[
|z_V-z_W|
\le
\int_0^t
e^{M(t-s)}
|B||V-W|\,ds.
\]

The candidate states:

- current response \(O(t)\);
- wheel response \(O(t^2)\);
- body \(u,r\) response \(O(t^3)\);
- heading response \(O(t^4)\);
- position response \(O(t^4)\).

## Finding

The stated **upper orders** are sound.

## Evidence

Dependency path:

\[
V
\rightarrow
i
\]

directly through \(B\).

Then:

\[
i
\rightarrow
\omega
\]

through wheel-current coupling in \(A^\#\).

Then:

\[
\omega
\rightarrow
F
\rightarrow
(u,r)
\]

through the \(|D|Q\) comparison structure.

Because \(Q\) has zero current columns, no shorter comparison path exists from \(V\) to body velocity.

Hence the integral/power-series expansion yields:

\[
\Delta i=O(t),
\]

\[
\Delta\omega=O(t^2),
\]

\[
\Delta u,\Delta r=O(t^3).
\]

Then:

\[
\Delta\theta=O(t^4),
\]

and:

\[
\Delta p=O(t^4).
\]

The leading coefficient may vanish.

## Consequence

This is a causal upper-order diagnostic only.

It is **not**:

- a lower voltage-authority guarantee;
- a relative-degree theorem;
- proof that avoidance displacement scales nontrivially as \(t^4\);
- proof of stopping authority.

## Status

**VALID**

## Required action

Keep the current caveats.

Also apply the G2-03 wording correction so the candidate does not imply guaranteed force change at \(n=1\).

---

# 21. PRACTICAL USEFULNESS — GLOBAL COMPARISON RADIUS

## Finding

Practical usefulness is currently unverified.

## Evidence

Several safe relaxations can compound:

### 1. Signed motor coupling is lost

The physical motor subsystem has stabilizing signed back-EMF coupling.

Replacing off-diagonal entries by absolute values in:

\[
A^\#
\]

removes cancellation.

### 2. Contact/state dependence is relaxed

\[
|D|Q|\epsilon|
\]

drops signs and correlations.

### 3. Fallback drops negative damping

The fallback replaces negative diagonal entries by zero to create:

\[
N_b\ge0.
\]

This is especially conservative.

### 4. Contact-demand product loses correlation

\[
m
(|u^n|+E_u)
(|r^n|+E_r)
\]

is a box product and can be large even when actual \(ur\) remains small because of correlation.

### 5. Parameter cells may lose fixed-parameter dependence

Any box hull or coefficient-wise bound introduces further dependency loss.

## Consequence

A mathematically correct radius can still be too wide to certify:

\[
g_p>0
\]

or:

\[
g_c>0
\]

for any useful hold time.

No current result proves otherwise.

## Status

\[
\boxed{
\textbf{UNVERIFIED}
}
\]

## Required action

Do not pass G2 from proof coherence alone.

In a later authorized quantitative G2 phase, report:

- certified tube widths;
- certified collision margins;
- certified contact margins;
- hold time \(T\);
- parameter-cell widths;
- refinement depth \(n,\ell\);
- runtime/complexity evidence;
- failure/UNKNOWN regions.

If useful margins collapse on defensible data, stop this enclosure branch rather than hiding conservatism.

---

# 22. PRACTICAL USEFULNESS — IMPULSE-RESPONSE REFINEMENT

## Finding

Lemma 2 is guaranteed no worse than Lemma 1, but usefulness is still unverified.

## Evidence

Analytically:

\[
E_{n,\ell+1}
\le
E_{n,\ell}.
\]

This proves monotone tightening.

It does not prove that the resulting radius is sufficiently narrow to certify nontrivial holds.

It also does not preserve every nonlinear state/parameter dependency.

## Consequence

The exact-kernel refinement is a plausible tightening mechanism, not yet a demonstrated useful method.

## Status

**UNVERIFIED for usefulness**

## Required action

Later compare:

\[
E_{n,0}
\]

against:

\[
E_{n,\ell}
\]

on a declared certified parameter set.

Do not claim practical advantage before such evidence exists.

---

# 23. NOVELTY — GENERIC GROWTH-BOUND MACHINERY

## Finding

Novelty based solely on the following is blocked:

- componentwise growth matrices;
- matrix-exponential comparison;
- constant-parameter augmentation;
- interval parameter cells;
- generic outer-tube inclusion.

## Evidence

Existing reachability literature already contains closely related machinery, including:

- Arcak & Maidens: componentwise contraction/growth bounds and constant uncertain parameters;
- TIRA / Meyer et al.: growth-bound interval reachability and integrated uncertainty forcing;
- nonlinear reachable-set methods with uncertain parameters;
- validated continuous-time enclosures for parametric nonlinear ODEs.

## Consequence

The paper contribution cannot be:

> augment fixed parameters and propagate a componentwise exponential radius.

## Status

\[
\boxed{
\textbf{BLOCKED for standalone novelty}
}
\]

## Required action

Treat this machinery as infrastructure only.

---

# 24. NOVELTY — FINITE PICARD / PREDICTOR-VALIDATION

## Finding

A generic novelty claim based on:

\[
\text{finite Picard predictor}
+
\text{validated residual tube}
\]

is also high risk and currently unsupported.

## Evidence

Validated ODE integration and nonlinear flowpipe literature already includes:

- rigorous interval ODE integration;
- Taylor-model integration;
- Picard-based rigorous flow enclosures;
- predictor-validation schemes;
- validated nonlinear flowpipes;
- parametric nonlinear ODE enclosures.

Thus generic predictor-plus-validation structure is established territory.

## Consequence

The contribution, if one exists, must depend materially on the DDWMR/contact/safety structure.

## Status

\[
\boxed{
\textbf{BLOCKED for generic-method novelty}
}
\]

## Required action

Do not claim generic Picard/residual certification as original.

---

# 25. ADDITIONAL CLOSE PRIOR-ART FAMILIES TO AUDIT

The current targeted matrix should be expanded before G4.

At minimum compare against the following methodological families at equation/theorem level:

1. nonlinear reachability with uncertain parameters and conservative linearization;
2. verified Taylor-model ODE integration;
3. rigorous Picard/Taylor flow integration;
4. Taylor-model nonlinear flowpipes;
5. continuous-time enclosures for parametric nonlinear ODEs;
6. predictor-validation set-valued integration;
7. polynomial-difference-inclusion reachability;
8. componentwise contraction/growth-bound reachability;
9. interval reachability toolchains such as TIRA;
10. validated nonlinear hybrid flowpipe methods such as Flow*.

The contribution hypothesis, if retained, should be narrower, for example:

> a DDWMR-specific certified one-hold collision/contact test exploiting the exact voltage → current → wheel → slip → force → body structure and algebraic contact reserve, with demonstrably useful conservatism versus generic validated reachability.

This is only a hypothesis.

No novelty is established yet.

---

# 26. FOUR SEPARATE G2 DISPOSITIONS

| Dimension | Disposition | Rationale |
|---|---|---|
| **Analytic soundness** | **VALID with one minor wording revision** | G2.1–G2.29 are analytically sound under MASTER assumptions. Section 2 must say voltage can make \(F(z^0)\) voltage-dependent, not that it necessarily changes it. |
| **Finite certified computation** | **UNVERIFIED** | Sound finite-certification contract exists, but no complete instantiated certified arithmetic/data case exists. |
| **Practical usefulness** | **UNVERIFIED** | No certified nontrivial \(T\), positive safety/contact margin, runtime, or conservatism result exists. |
| **Novelty** | **BLOCKED for generic machinery; overall UNVERIFIED** | Growth bounds, fixed-parameter augmentation, validated Picard/predictor methods and flowpipe machinery are established prior art. |

---

# 27. EXPLICIT G2 GATE DISPOSITION

\[
\boxed{
\textbf{G2 REMAINS UNVERIFIED}
}
\]

The analytic proof branch should **not** be abandoned.

GPT finds no equation-level defect requiring rejection of:

- G2-A;
- G2-B;
- Lemma 1;
- Lemma 2;
- the pose lift;
- the joint parameter union;
- the full-hold collision/contact logic;
- the finite-cell fallback.

However, G2 must not pass yet because the gate requires more than symbolic proof structure.

The unresolved requirements are:

1. actual finite certified evaluation;
2. effective \(\phi\) and \(\Theta\) representation;
3. outward numerical/interval primitives;
4. positive certified safety/contact margins;
5. practical nonconservatism;
6. runtime/complexity evidence;
7. non-generic contribution evidence.

---

# 28. ONE MANDATORY TEXTUAL CORRECTION

In `G2_ENCLOSURE_CANDIDATE_v1.md`, Section 2 currently states in substance that the wheel/current response in \(z^0\) **changes** \(F(z^0)\).

This is too strong under the adopted \(\phi\)-class.

Replace with wording equivalent to:

> For \(n=0\), the body-center components \(u^0,r^0\) are independent of \(V\). The voltage-dependent current/wheel components can make the slip entering \(F(z^0)\) voltage-dependent, so \(n=1\) is the first predictor depth at which the body-center predictor can depend on voltage through the contact law. The adopted \(\phi\)-class does not guarantee a nonzero or monotone force change.

This is a wording correction only.

No plant assumption changes.

---

# 29. WHAT IS ALREADY STRONG ENOUGH TO RETAIN

The following analytic content should be retained:

- exact \(A,B,D,S\) decomposition;
- global Lipschitz force bound;
- finite predictor family;
- residual \(d_n\);
- Dini comparison radius;
- signed impulse-response refinement;
- parameter-labeled fiber union;
- pose lifting;
- robust collision check;
- robust algebraic contact check;
- \(\beta=1\) edge handling;
- noncircular ODE/contact logic;
- finite-cell fallback;
- full-slab pose-radius fallback;
- local predictor/error order derivation;
- causal voltage-response upper-order derivation.

No stronger \(\phi\) assumptions are needed for these results.

---

# 30. WHAT MUST NOT BE CLAIMED YET

Do not claim:

- G2 PASS;
- a completed certified numerical algorithm;
- useful certified hold time;
- practical runtime;
- practical tightness;
- a physical robot safety guarantee;
- hardware validation;
- guaranteed stopping;
- minimum avoidance authority;
- lower voltage-to-position response;
- relative degree from the \(O(t^4)\) diagnostic;
- exact viability;
- recursive safety;
- G3;
- generic growth-bound novelty;
- generic Picard/residual novelty;
- parameter augmentation novelty;
- tube inclusion novelty;
- “first”;
- Q1 readiness;
- GO.

---

# 31. REQUIRED NEXT G2-ONLY ACTIONS

The next G2 iteration should remain analytic/certification-focused.

## Action 1 — revise Section 2 wording

Apply the correction in Section 28.

## Action 2 — choose an explicit mathematical \(\phi\)

Not necessarily hardware-calibrated yet.

But it must be:

- fixed;
- computable;
- consistent with MASTER assumptions;
- accompanied by a certified \(L_\phi\).

Clearly label whether the example is:

- purely mathematical; or
- physically identified.

Do not blur the distinction.

## Action 3 — give an effective \(\Theta\) representation

Specify a finite/algorithmically coverable joint set preserving relevant correlations.

Do not use a favorable fabricated hardware set.

## Action 4 — make every finite primitive certified

Define outward evaluation for:

- matrix exponentials;
- nested predictor integrals;
- \(d_n\);
- \(\phi\);
- pose integrals;
- trigonometric ranges;
- contact square roots;
- distance-to-obstacle lower bounds;
- parameter/time slab ranges.

## Action 5 — demonstrate one complete finite certificate

For one declared mathematical data case, produce a proof-level finite evaluation showing:

\[
g_p(t,\vartheta)\ge0
\]

and:

\[
g_c(t,\vartheta)\ge0
\]

for all:

\[
t\in[0,T],
\qquad
\vartheta\in\Theta.
\]

Ordinary samples do not count.

## Action 6 — quantify conservatism

Compare:

- global comparison;
- exact impulse refinement;
- finite-cell fallback;

on the same certified problem.

## Action 7 — keep novelty separate

Expand primary-source comparison before any originality claim.

No G4 closure is implied.

---

# 32. G3 / IMPLEMENTATION BOUNDARY

Do not construct:

\[
K_T
\]

in this review phase.

Do not design the recursive controller.

Do not implement:

- safety filter;
- simulator;
- interval solver;
- experiments;
- hardware test;
- controller code.

Current user authorization covers G2 analytic research only.

---

# 33. CANONICAL STATUS TO PRESERVE

After this review, unless the user separately authorizes a metadata update, keep:

\[
\boxed{
\text{G1 PASS — restricted reduced-model scope}
}
\]

\[
\boxed{
\text{G2 UNVERIFIED}
}
\]

\[
\boxed{
\text{G3 UNVERIFIED}
}
\]

\[
\boxed{
\text{G4 UNVERIFIED}
}
\]

\[
\boxed{
\text{Physical-platform correspondence UNVERIFIED}
}
\]

and:

\[
\boxed{
\textbf{HOLD}
}
\]

No GO.

No implementation authorization.

---

# 34. REQUIRED CODEX RESPONSE FORMAT

For the next response, use:

## Finding

State the exact result.

## Evidence

Give the equation-level derivation or certified-evaluation argument.

## Consequence

State what changes or remains blocked.

## Status

Choose one:

- VALID;
- NEEDS REVISION;
- BLOCKER;
- UNVERIFIED.

## Required action

State the exact next step.

Also include a summary table with:

| Item | Analytic soundness | Finite certification | Usefulness | Novelty | Gate effect |
|---|---|---|---|---|---|

---

# 35. BOTTOM LINE

The G2 candidate at commit:

`7390942f49e4e1b303fb37a2c060edcfa0036d5c`

is analytically strong.

The central equations and proofs are sound under the adopted MASTER v2.1 assumptions.

The only identified analytic/text issue is local:

\[
\boxed{
\text{voltage can make }F(z^0)\text{ voltage-dependent}
}
\]

rather than:

\[
\boxed{
\text{voltage necessarily changes }F(z^0).
}
\]

The decisive distinction is:

\[
\boxed{
\text{analytic enclosure}
\neq
\text{finite certified computation}
}
\]

and:

\[
\boxed{
\text{finite certified computation}
\neq
\text{practical usefulness}
}
\]

and:

\[
\boxed{
\text{analytic usefulness}
\neq
\text{novelty}.
}
\]

Therefore:

\[
\boxed{
\textbf{Analytic soundness: VALID with one minor wording revision}
}
\]

\[
\boxed{
\textbf{Finite certified computation: UNVERIFIED}
}
\]

\[
\boxed{
\textbf{Practical usefulness: UNVERIFIED}
}
\]

\[
\boxed{
\textbf{Generic-method novelty: BLOCKED}
}
\]

\[
\boxed{
\textbf{Overall G2: UNVERIFIED}
}
\]

and the project remains:

\[
\boxed{
\textbf{HOLD}
}
\]

with no G3 construction, no GO, and no implementation authorization.
