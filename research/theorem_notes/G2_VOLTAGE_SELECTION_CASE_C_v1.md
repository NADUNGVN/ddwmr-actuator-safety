# G2 Case C: two forward voltage levels under one locked certificate

2026-09-29. **DERIVED CANDIDATE FOR GPT REVIEW. G2 UNVERIFIED; HOLD.**

This is a minimal synthetic response to [GPT's next-priority request](../../docs/reviews/GPT_G2_R3_1da2166_ACCEPT_RECORD.md). It compares held voltages using the same state, parameter family, obstacle, predictor depth, error budget and full-slab evaluation rule. It is an auxiliary symmetric example within MASTER v2.1, not a new plant assumption or a general actuator-authority theorem. No solver or simulation is used.

## 1. Matched-side family, initial state and candidate actions

Use the fixed SI reference units and coordinate normalization of Case A. Set m=I_z=R_w=b=v_s=c_u=c_r=1 and B_L=B_R=R_L=R_R=k_L=k_R=1 in their respective units. Select the same fixed clip function with L_phi=1.

The hidden execution-fixed labels and parameter image are

\[
(\rho,C)\in[1,11/10]^2,\quad
\rho_L=\rho_R=\rho,\quad C_L=C_R=C,\quad
J_L=J_R=L_L=L_R=1/\rho. \tag{C.1}
\]

J and L equality refers to normalized values with different physical units. This two-label family enforces equal realized side parameters. It is **not** a claim that independent left/right uncertainty preserves straight motion. The ideal gear witness is the Case B witness with common rho on both sides: n_g=10, k_motor=1/10, J_wheel=1/10, J_motor=(1/rho-1/10)/100, B_wheel=1/10, B_motor=9/1000. L=1/rho is separately stipulated electrical data. All inertias and denominators are positive.

Use one label cell, one hold/slab, exact rest and three declared voltage candidates:

\[
T=1/10,\quad p_*=(0,0),\quad\theta_*=0,\quad z_*=0,\quad
V_a=(a,a),\qquad a\in\{0,1/4,1\},\quad V_{\max}=1.
\tag{C.2}
\]

Each candidate is held unchanged for the entire interval and common to all hidden labels. The two nonzero candidates both command forward voltage; they have the same initial state and obstacle. Zero is included to expose the easy rest alternative, not concealed as an unfavorable comparator.

For a fixed label, uniqueness and exchange symmetry imply equal left/right wheel and current states and r=theta=0 for the true formal ODE and every finite predictor. Indeed at equal wheel states and r=0, slips and forces coincide and dot r=0. This argument uses the **exact matched family C.1**. No global assumption of odd phi is needed for this equal-side symmetry. We retain the full six-state generic error box and generic pose lift below, without assuming every box state is symmetric.

## 2. Voltage passes through the finite predictor

The motor block is the parameterized damped rotation B.3. With the same I_s,rho and I_c,rho integrals as B.5, F(z_*)=0 yields

\[
u^0=r^0=0,\quad
\omega_j^0=a I_s(t),\quad i_j^0=a I_c(t),\qquad
I_s(t)=\int_0^t\rho e^{-\rho s}\sin(\rho s)ds,quad
I_c(t)=\int_0^t\rho e^{-\rho s}\cos(\rho s)ds.
\tag{C.3}
\]

For 0<=s<=T and 1<=rho<=11/10, rho s<=11/100. The elementary remainder bounds give e^{-rho s}>=89/100 and sin(rho s)>=rho s(1-(rho s)^2/6)>=(99/100)rho s. Their product is at least (4/5)rho s. Using rho>=1 for a lower bound and rho<=11/10 for an upper bound,

\[
\frac25t^2\le I_s(t)\le\frac{121}{200}t^2,
\qquad 0\le\omega_j^0\le\frac{121}{200}T^2<1.
\tag{C.4}
\]

Consequently phi(sigma_j^0)=sigma_j^0=a I_s exactly, so F_j(z^0)=a C I_s. This branch fact is proved for the explicit predictor, not assumed for the unknown true trajectory.

The n=1 body and pose centers are therefore

\[
u^1=a U(t),\quad r^1=0,\quad\theta^1=0,\quad
p^1=(a P(t),0),\quad
U(t)=2C\int_0^t e^{-(t-s)}I_s(s)ds,\quad P(t)=\int_0^t U(s)ds.
\tag{C.5}
\]

Since e^{-(t-s)}>=9/10 on the hold, C.4 and C<=11/10 imply

\[
\frac6{25}t^3\le U(t)\le\frac{1331}{3000}t^3<\frac49t^3,
\qquad \frac3{50}t^4\le P(t)\le\frac19t^4.
\tag{C.6}
\]

The final strict inequality for U is understood at t>0; all functions vanish at t=0. These explicit lower bounds are specific to this selected law/data, not transferred to the abstract MASTER phi class. They show a nonzero voltage effect through V -> current -> wheel speed -> slip -> force -> u -> p in this case.

For the same parameter label and t>0, the two nonzero predictor positions differ by (3/4)P(t)>0. The common uncertainty label must be retained in this comparison; no favorable parameter is selected for either action.

## 3. One shared residual/error construction for every action

Let Delta z=z^1-z^0. The force entering its convolution is F(z^0), bounded by (1331/2000)s^2 for every a in the candidate list. Signed kernel bounds from B.3 give

\[
|\Delta u|\le\frac{1331}{3000}t^3,\quad\Delta r=0,\quad
|\Delta\omega_j|\le\frac{14641}{60000}t^3,\quad
|\Delta i_j|\le\frac{161051}{2400000}t^4.
\tag{C.7}
\]

These follow from force-to-wheel kernel <=rho and force-to-current kernel <=rho^2(t-s). The exact zero Delta r is used only in this predictor residual calculation. Thus

\[
|S\Delta z|_j\le\frac{41261}{60000}t^3,\qquad
d_{1,j}\le\frac{453871}{600000}t^3\le\frac45t^3.
\tag{C.8}
\]

The full six-state Metzler comparison M still has signed row sums <=q=28/5 (body: -1+6C; wheel: 3rho C; current: zero). Positivity gives ||e^{Mt}||_infinity<=e^{qt}. The accepted rational tail bound A.11 gives e^{qT}<=2673/1525<9/5. With || |D| ||_infinity=2,

\[
\|E_{1,0}(t)\|_\infty
\le\frac95\frac85\int_0^t s^3ds
=\frac{18}{25}t^4=:e_z(t).
\tag{C.9}
\]

Use this **same** outward envelope for all three actions, including zero. No action is assigned a different refinement level, error tolerance or rounding convention. The zero action's exact error is zero; keeping the common bound makes the comparison rule identical.

## 4. Full generic pose tube

Although the exact trajectories and centers are straight, we use G2.15 for the full error box, so possible yaw error in that box is included. Equations C.6 and C.9 yield

\[
E_\theta(t)\le\frac{18}{125}t^5,\qquad
E_p(t)\le\int_0^t\left[\frac{18}{25}s^4+
\frac49s^3\frac{18}{125}s^5\right]ds
=\frac{18}{125}t^5+\frac8{1125}t^9
\le\frac3{20}t^5.
\tag{C.10}
\]

For the last inequality, (8/1125)T^4<3/20-18/125=3/500; the t=0 equality is harmless. The full-slab common position radius is

\[
\bar E_p=\frac3{20}T^5=\frac3{2000000}\ \mathrm m.
\tag{C.11}
\]

No yaw samples or planar trajectory samples establish this estimate. The heading norm inequality and exact monomial integrals suffice.

## 5. One locked directional-center evaluation and one obstacle

Place a circular exclusion disk ahead of the initial center:

\[
R_s=\frac12,\qquad d=\frac1{125000},\qquad
p_o=(R_s+d,0).
\tag{C.12}
\]

The initial geometric clearance is 8 micrometers in the synthetic SI scale. This is deliberately selected near the finite bounds to expose action discrimination; it is not physically plausible measurement tolerance or hardware evidence.

For each candidate a, use **the same rule**: enclose all center positions over the entire cell/slab by

\[
\mathcal P_a=[0,aT^4/9]\times\{0\},\qquad
L_p(a)=\operatorname{dist}(\mathcal P_a,p_o)-R_s-\bar E_p
=d-aT^4/9-\bar E_p.
\tag{C.13}
\]

C.6 proves this directional segment enclosure for every fixed label and time. All segments lie strictly to the left of p_o, so the distance expression is exact for the **outer center set**. It is not a sampled-center approximation or the exact attainable-center set. The same shared E_p bounds the error around each center.

| Candidate held voltage | Center upper bound aT^4/9 (m) | Common pose radius (m) | Evaluated full-hold collision lower bound | Output |
|---|---:|---:|---:|---|
| (0,0) | 0 | 3/2000000 | 13/2000000 | CERTIFIED |
| (1/4,1/4) | 1/360000 | 3/2000000 | 67/18000000 | CERTIFIED |
| (1,1) | 1/90000 | 3/2000000 | -83/18000000 | UNKNOWN |

The two nonzero candidates share all error budgets; their output distinction comes from the voltage-dependent center bound. The zero action also certifies; this example does not require forward motion or solve a tracking tradeoff. UNKNOWN for (1,1) is only the outcome of C.13. It proves neither actual collision nor failure of a tighter evaluation or another enclosure.

## 6. Contact certificate for the entire generic tube

From C.3--C.8, for all candidates,

\[
|\sigma_j^1(t)|\le\frac{121}{200}t^2+\frac{41261}{60000}t^3,
\qquad
\beta_j(t)\le\frac{121}{200}T^2+
\frac{41261}{60000}T^3+3e_z(T)<\frac7{1000}<\frac1{100}.
\tag{C.14}
\]

Here row sums of |S| equal three; the full error box is used even though the true yaw rate is zero. With C>=1, the two-wheel reserve is at least 9999/5000 N, by the same direct square-root rational bound as A.20. Also

\[
|u^1|+E_u\le\frac49T^3+e_z(T)<\frac3{5000},\quad
|r^1|+E_r\le e_z(T)<\frac1{10000},\quad
g_c\ge\frac{9999}{5000}-\frac3{50000000}>
\frac{1999}{1000}>0.
\tag{C.15}
\]

Thus the contact test succeeds for every candidate on the same full tube. Collision, not contact-budget loss, determines the distinct outputs in C.13. The true trajectories remain in the unsaturated contact region for this example; unlike Case B, no saturation crossing is claimed here.

## 7. Candidate proposition and exact interpretation

**Proposition C (submitted for review).** For C.1--C.2 and C.12, the finite evaluation C.13 with shared error envelope C.9--C.11 and contact check C.15 certifies V=(1/4,1/4) and V=(0,0) for all fixed labels and all t in [0,1/10]. In particular, the nonzero smaller action has

\[
g_p\ge\frac{67}{18000000}\ \mathrm m>0,\qquad
g_c\ge\frac{1999}{1000}\ \mathrm N>0.
\tag{C.16}
\]

The **same locked evaluation** returns UNKNOWN for V=(1,1). The certified/UNKNOWN distinction is tied to the voltage-dependent n=1 center, not different radius assignments.

**Proof.** C.3--C.8 bound explicit finite predictor integrals on the full parameter/time cell. C.9 is the reviewed G2 comparison inclusion. C.10--C.15 give full-hold center/radius and contact containment for each common input. Apply G2-A/B to the positive outputs. The negative computed lower bound for the larger action is merely inconclusive. QED, pending independent review.

For these locked envelopes, L_p(a)=d-aT^4/9-bar E_p is an explicit affine diagnostic of candidate amplitude. This is not a physical feasibility boundary or a controller: the action list is declared for a single hold and no recursive policy is built.

## 8. Finite primitive and evidence ledger

| Operation | Finite certified realization in this case |
|---|---|
| Parameter family | One rational two-label box mapped to correlated matched-side values, positive reciprocal denominators |
| Symmetry | Uniqueness and exact equal-side equations; only auxiliary C.1 has this restriction |
| Motor exponential and integrals | Exact damped rotation; global scalar inequalities C.3--C.4 on rho t<=11/100 |
| Contact-law evaluation | Predictor slip bound proves its clip value; true-state inclusion uses the global Lipschitz law |
| Predictor/residual | Exact finite convolution bounds and monomial integrals C.5--C.8 |
| Comparison exponential | Metzler semigroup plus already accepted rational Taylor-tail bound A.11 |
| Pose and distance | Generic G2 pose lift; exact distance from declared center segment; same full-slab radius for every candidate |
| Square-root reserve | Rational lower bound checked by squaring, no derivative |

No ordinary trajectory sampling, certified solver implementation, runtime measurement or experiment was used. There are three declared actions, two predictor levels, one label cell and one slab; that counts this hand instance, not the complexity of a general evaluator.

## 9. Research value and unresolved obligations

This example directly supplies a voltage-dependent **certificate-output** distinction under a single locked evaluation, if accepted. It also derives a nonzero predictor center response for this specific synthetic family. These are narrower claims than general actuator authority or practical usefulness.

Limitations are substantial: exact rest, exact matched sides, specially correlated nonstiff motor data, unsaturated contact, generous contact slack, engineered micrometer obstacle clearance, zero voltage already safe, no nominal tracking objective, no proof that n=1 outperforms a properly validated n=0 construction, no matched generic-method comparison and no runtime evidence. None of Case B's saturation-crossing or independent-side labels is implicitly imported into Case C. The two cases test different mechanisms.

A more persuasive research operating domain still requires moving/turning states, defensible numerical data, useful robust margins, practical voltage decisions, and comparison to applicable existing validated reachability under matched assumptions. The generic-method novelty branch remains BLOCKED. No practical or G2/G4 conclusion follows from this deliberately minimal decision example, and no G3, physical-transfer, implementation or GO claim is made.
