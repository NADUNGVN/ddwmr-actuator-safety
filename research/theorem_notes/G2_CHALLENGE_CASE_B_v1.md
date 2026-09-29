# G2 Case B: uncertain actuator blocks and a declared certificate separation

2026-09-29. **DERIVED CANDIDATE; INDEPENDENT GPT REVIEW PENDING. G2 UNVERIFIED; HOLD.**

This synthetic mathematical challenge follows [accepted Case A](G2_FINITE_CERTIFICATE_CASE_A_v1.md) and [GPT's R2 disposition](../../docs/reviews/GPT_G2_R2_d2cd854_ACCEPT_RECORD.md). It uses the unchanged MASTER v2.1 and the reviewed G2.1--G2.29 framework. It supplies a hand proof, no numerical solver or experiment.

Three aims: (i) genuinely parameter-dependent A, B and D; (ii) contact saturation followed by exit from saturation during a hold; (iii) a positive refined sufficient test versus UNKNOWN for two explicitly declared coarser evaluations. This is not a voltage-necessity, physical-usefulness or originality claim.

## 1. Exact synthetic data and correlated parameter representation

Use Case A's fixed SI reference units and coordinate normalization. Set m=I_z=R_w=b=v_s=c_u=c_r=1 in their respective units. Set B_j=R_j=k_j=1, V_max=1, and the same known clip function phi(q)=max(-1,min(q,1)), L_phi=1.

Let the independent parameter labels be

\[
\xi=(\rho_L,\rho_R,C_L,C_R)\in[1,11/10]^4,
\qquad J_j=L_j=1/\rho_j. \tag{B.1}
\]

The equalities are between normalized numerical values; J has inertia units and L has inductance units. Theta is the **image** of this closed rational box under the displayed reciprocal map and the other singleton assignments, not an independent box over J and L. Use one label cell of width 1/10 in all four coordinates. Each xi is unknown and fixed for the full execution. The artificial J/L correlation is part of this synthetic benchmark, not an identified hardware relation.

A consistent ideal-gear witness for each member is n_g=10, k_motor=1/10, J_wheel=1/10, J_motor=(1/rho_j-1/10)/100>0, B_wheel=1/10, B_motor=9/1000. Thus reflected J=1/rho_j, B=k=1. No gear/conversion correlation is dropped.

Choose one common voltage, one time slab and measured initial state:

\[
T=1/20,\quad V=(1/2,-1/2),\quad
z_*=(1/4,1/8,5/4,3/8,0,0),\quad p_*=(0,0),\quad\theta_*=0.
\tag{B.2}
\]

Initial slips are sigma_L*=9/8 and sigma_R*=0. Therefore F_*=(C_L,0). The left force starts saturated, while the right wheel retains lateral reserve. Initial contact demand is 1/32<1, so the initial state is contact-admissible for the entire parameter set.

Each ordered (omega_j,i_j) motor block is now

\[
A_{m,j}=\rho_j\begin{pmatrix}-1&1\\-1&-1\end{pmatrix},\qquad
e^{A_{m,j}t}=e^{-\rho_jt}
\begin{pmatrix}\cos(\rho_jt)&\sin(\rho_jt)\\-\sin(\rho_jt)&\cos(\rho_jt)\end{pmatrix}.
\tag{B.3}
\]

B's current entries are rho_j and D's wheel reaction entries are -rho_j; their body entries and S remain those of Case A. Hence A, B and D are parameter-dependent. No nominal matrix substitutes for the whole family. The special scaled blocks make this hand calculation tractable; arbitrary independent electrical/mechanical uncertainty and stiffness are not covered by this case.

## 2. Frozen-force predictor on the full label/time cell

Write w_L=5/4, w_R=3/8, f_L=C_L, f_R=0. The exact n=0 body predictor is

\[
u^0=\tfrac14e^{-t}+C_L(1-e^{-t}),\qquad
r^0=\tfrac18e^{-t}-C_L(1-e^{-t}). \tag{B.4}
\]

Define I_c,j(t)=int_0^t rho_j e^{-rho_j s} cos(rho_j s) ds and I_s,j(t)=int_0^t rho_j e^{-rho_j s} sin(rho_j s) ds. The motor predictor is

\[
\omega_j^0=w_je^{-\rho_jt}\cos(\rho_jt)-f_j I_{c,j}(t)+V_j I_{s,j}(t),
\quad i_j^0=-w_je^{-\rho_jt}\sin(\rho_jt)+f_j I_{s,j}(t)+V_j I_{c,j}(t).
\tag{B.5}
\]

Signs of the force/current response follow from the negative wheel reaction and the negative back-EMF entry, not independent force inputs.

For all t in [0,T], elementary trigonometric/exponential inequalities give

\[
|u^0-u_*|\le\tfrac{17}{20}t,\quad
|r^0-r_*|\le\tfrac{49}{40}t,\quad
|\omega_j^0-w_j|\le\tfrac{517}{200}t+\tfrac{847}{800}t^2.
\tag{B.6}
\]

For the last bound, |e^{-rho t}cos(rho t)-1|<=rho t+(rho t)^2/2, |I_c|<=rho t and |I_s|<=rho^2 t^2/2. Insert rho<=11/10, w<=5/4, f<=11/10 and |V|=1/2. This yields the displayed coefficients.

Each row of S involves body u, r and its wheel, hence

\[
|(S(z^0-z_*))_j|\le\tfrac{233}{50}t+\tfrac{847}{800}t^2\le5t,
\qquad |F_j(z^0)-F_{*,j}|\le\tfrac{11}{2}t.
\tag{B.7}
\]

The first coefficient at t=T is 233/50+847/16000<5. This uses the global Lipschitz bound, valid across the saturation corner; no differentiation of clip is used.

## 3. n=1 predictor differences, residual and center ranges

Delta z=z^1-z^0 is the convolution of e^{At}D with F(z^0)-F_*. The body kernel row sum is at most 2; a wheel force kernel is at most rho<=11/10; its current kernel is at most rho^2 t<=121t/100. Thus

\[
|\Delta u|,|\Delta r|\le\tfrac{11}{2}t^2,\quad
|\Delta\omega_j|\le\tfrac{121}{40}t^2,\quad
|\Delta i_j|\le\tfrac{1331}{1200}t^3.
\tag{B.8}
\]

Consequently,

\[
|S\Delta z|_j\le\tfrac{561}{40}t^2,\qquad
d_{1,j}\le\tfrac{6171}{400}t^2\le16t^2.
\tag{B.9}
\]

The amplitude minimum in G2.8 only decreases this bound. From B.6 and B.8,

\[
|u^1|\le\tfrac14+\tfrac{17}{20}T+\tfrac{11}{2}T^2
=\tfrac{49}{160}<U:=\tfrac{307}{1000},
\quad |r^1|\le\tfrac18+\tfrac{49}{40}T+\tfrac{11}{2}T^2
=\tfrac15<R:=\tfrac{201}{1000}.
\tag{B.10}
\]

All inequalities apply throughout the label cell and time slab, not only at vertices or endpoints.

## 4. Three certified internal error budgets

### 4.1 Global comparison

The signed row sums of M are at most -1+3(C_L+C_R)<=28/5 for body rows, 3rho_j C_j<=363/100 for wheel rows, and 0 for current rows. M is Metzler. With q=28/5, positive comparison gives ||e^{Mt}||_infinity<=e^{qt}. The rational exponential tail is

\[
e^{qT}=e^{7/25}\le1+\tfrac7{25}+
\frac{(7/25)^2}{2(1-7/75)}
=\tfrac{4499}{3400}<\tfrac43.
\tag{B.11}
\]

The largest row sum of |D| is still 2. Therefore

\[
\|E_{1,0}(t)\|_\infty\le\tfrac43\,32\int_0^t s^2ds
=\alpha t^3,\quad\alpha=\tfrac{128}{9},\quad
\alpha T^3<\varepsilon_G:=\tfrac9{5000}.
\tag{B.12}
\]

### 4.2 One exact-kernel refinement

Each row of Q sums to at most 33/10. H=|e^{At}D| has body row sums <=2, wheel sums <=11/10, and current sums <=121t/100. Inserting B.9 and B.12 into G2.12 gives

\[
E_{1,1,u},E_{1,1,r}\le\tfrac{32}{3}t^3+\tfrac{33\alpha}{20}t^4,
\quad E_{1,1,\omega_j}\le\tfrac{88}{15}t^3+\tfrac{363\alpha}{400}t^4,
\quad E_{1,1,i_j}\le\tfrac{121}{75}t^4+\tfrac{3993\alpha}{20000}t^5.
\tag{B.13}
\]

These use exact monomial integrals, including int_0^t (t-s)s^2 ds=t^4/12 and int_0^t (t-s)s^3 ds=t^5/20. Every polynomial increases on the slab. At T the body bound is exactly 37/25000; wheel/current bounds are smaller. Hence

\[
\|E_{1,1}(t)\|_\infty\le\tfrac{37}{25000}<
\varepsilon_H:=\tfrac3{2000}. \tag{B.14}
\]

### 4.3 Explicit finite-cell fallback

The signed current diagonal -rho_j is not entrywise increasing with rho_j. Therefore **do not** claim that evaluating all of M at the upper parameter corner gives an entrywise upper matrix.

Instead define the following nonnegative majorant directly, ordered (u,r,omega_L,omega_R,i_L,i_R):

\[
N=\begin{pmatrix}
6/5&11/5&11/10&11/10&0&0\\
11/5&6/5&11/10&11/10&0&0\\
121/100&121/100&11/100&0&11/10&0\\
121/100&121/100&0&11/100&0&11/10\\
0&0&11/10&0&0&0\\
0&0&0&11/10&0&0
\end{pmatrix}. \tag{B.15}
\]

For every fixed label N>=M entrywise. In particular rho_j(C_j-1)<=11/100, and current diagonals are bounded by zero. N 1<=q 1. Let D_bar have the body absolute entries of D, wheel entries 11/10 and zero current rows; D_bar>=|D|. With d_bar=16T^2(1,1)^top, the G2.28 comparison is nondecreasing and

\[
\|\eta(T)\|_\infty\le32T^2\int_0^T e^{qs}ds
\le\tfrac{128}{3}T^3<\varepsilon_F:=\tfrac{27}{5000}.
\tag{B.16}
\]

This bounds the full slab. The coefficient matrix N is an explicit outer comparison, not a switching realization of the physical family.

## 5. Locked evaluation rules and obstacle choice

For each of the three budgets epsilon use exactly the same scalar pose-lift evaluation and center ball:

\[
E_\theta\le T\varepsilon,\qquad
E_p\le T(1+UT)\varepsilon=\tfrac{20307}{400000}\varepsilon,
\qquad \|p^1(t)\|_2\le TU=\tfrac{307}{20000}.
\tag{B.17}
\]

Choose outward rational pose budgets P_G=92/10^6, P_H=77/10^6, P_F=275/10^6. Their unrounded upper expressions are respectively 0.0000913815, 0.00007615125 and 0.0002741445 (terminating decimals exactly denote rationals).

For this analytic discrimination example, deliberately place the obstacle using these budgets:

\[
R_s=\tfrac12,\quad p_o=(\tfrac{103087}{200000},0),\quad
\|p_o\|-R_s-TU=\tfrac{85}{10^6}.
\tag{B.18}
\]

This obstacle was engineered to fall between the refined and coarse bound thresholds. It is not a natural obstacle-placement distribution or an empirical benchmark. The finite collision evaluation is the explicitly declared sufficient test

\[
L_p(P):=\|p_o\|-R_s-TU-P=\tfrac{85}{10^6}-P.
\tag{B.19}
\]

| Declared evaluation | Internal budget | Pose budget | Evaluated lower bound L_p | Collision-test output |
|---|---:|---:|---:|---|
| Global scalar-ball evaluation | 9/5000 | 92/10^6 | -7/10^6 | UNKNOWN |
| One-refinement scalar-ball evaluation | 3/2000 | 77/10^6 | +8/10^6 | CERTIFIED |
| One-cell fallback scalar-ball evaluation | 27/5000 | 275/10^6 | -190/10^6 | UNKNOWN |

Only the positive lower bound implies safety. A negative lower bound does not prove g_p itself is negative, nor that the exact global tube fails containment. Tighter pose/center evaluation, more cells or different predictor depth could change the other outputs. This is a separation of the three **locked sufficient evaluations**, not all algorithms based on global comparison, nor an intrinsic impossibility result. It is not caused solely by decimal rounding: the three unrounded pose upper expressions also straddle 85/10^6.

## 6. Certified contact reserve despite one saturated wheel

For the right wheel, initially zero slip, B.7--B.9 and any of the three error budgets give

\[
\beta_R\le5T+\tfrac{561}{40}T^2+3\varepsilon_F
=\tfrac{24101}{80000}<\tfrac{31}{100},\qquad \beta_L\le1.
\tag{B.20}
\]

We count **zero** guaranteed left lateral reserve. Since C_R>=1, the right reserve alone is at least 19/20: (19/20)^2=361/400<=1-(31/100)^2=9039/10000. Meanwhile

\[
|u^1|+E_u\le U+\varepsilon_F<313/1000,\quad
|r^1|+E_r\le R+\varepsilon_F<207/1000,
\quad g_c\ge\tfrac{19}{20}-\tfrac{313\cdot207}{10^6}
=\tfrac{885209}{10^6}>0.
\tag{B.21}
\]

These are all-time/all-label bounds. No square-root derivative or reaction allocation chosen by the voltage controller is used. The remaining margin is still large; this case does not stress the contact-domain boundary tightly.

## 7. Genuine saturation exit: proof, not assumed regime

For any true formal ODE trajectory in the certified family, the fallback error and B.7--B.9 imply

\[
|\sigma_L(t)-9/8|\le5t+\tfrac{561}{40}t^2+3\varepsilon_F.
\tag{B.22}
\]

At t=1/100 the right-hand side is 0.0676025<1/8; it increases with t. Therefore sigma_L(t)>1 throughout [0,1/100], so the left force is exactly C_L there.

To prove exit by T, write sigma_L^0=omega_L^0-u^0+r^0 from B.4--B.5. For a=rho_j s<=11/200, both 1-a and 1-a^2/2 are positive, and

e^{-a}cos(a)>=(1-a)(1-a^2/2)>=1-a-a^2/2.

It follows that I_c,L(T)>=T-121T^2/200-1331T^3/6000>0. Also 1-e^{-T}>=T-T^2/2, e^{-rho T}<=1-rho T+(rho T)^2/2, e^{-T}>=1-T and |I_s,L(T)|<=121T^2/200. With C_L>=1 these yield

\[
\sigma_L^0(T)\le\tfrac98-\tfrac{33}{8}T+\tfrac{2131}{800}T^2+\tfrac{1331}{6000}T^3.
\tag{B.23}
\]

For example, the quadratic coefficient is (5/4)(121/200)+121/200+1+121/400=2131/800; the negative linear terms sum to -5/4+1/8-1-2=-33/8. The force-integral lower bound is positive, justifying use of C_L>=1 with a negative sign.

Adding |S(z^1-z^0)| and the true-state error at T gives

\[
\sigma_L(T)\le\tfrac98-\tfrac{33}{8}T+
\left(\tfrac{2131}{800}+\tfrac{561}{40}\right)T^2+
\tfrac{1331}{6000}T^3+3\varepsilon_F<\tfrac{49}{50}<1.
\tag{B.24}
\]

Equation B.22 also gives sigma_L(T)>=9/8-24101/80000>4/5. Thus every fixed realization starts on the saturated branch for at least 10 ms and is strictly in the positive unsaturated branch by 50 ms. Continuity ensures a crossing. No switching physical model or capacity reset is introduced; the same globally Lipschitz clip law governs the entire trajectory. The enclosure was derived globally before proving this regime information, avoiding circularity.

## 8. Candidate proposition and finite primitives

**Proposition B (submitted for review).** Under B.1--B.2 and B.18, the n=1, ell=1 enclosure with the declared full-slab evaluation satisfies, for every execution-fixed xi in [1,11/10]^4,

\[
\forall t\in[0,1/20]:\quad g_p(t,\xi)\ge8/10^6>0,
\quad g_c(t,\xi)\ge885209/10^6>0.
\tag{B.25}
\]

**Proof.** Use the parameter-indexed G2 inclusion separately for every fixed xi, B.12--B.16 for its error, B.17--B.19 for collision, and B.20--B.21 for contact. The common V is independent of xi. Therefore G2-A/B imply continuous one-hold safety of the stipulated model. B.22--B.24 establish the additional saturation-exit assertion. The two negative outputs in the table are only failures of the locked sufficient evaluations. QED, pending independent GPT review.

| Finite primitive | Explicit enclosure used |
|---|---|
| Theta and positive denominators | Rational image of one box; rho>=1 and J=L=1/rho preserve the declared correlation |
| Parameter-dependent matrix exponential | Exact B.3 for each fixed rho; scalar inequalities on the entire cell/slab |
| Predictor integrals/clip | B.4--B.7; global Lipschitz bound and exact polynomial integrals; no mode derivative |
| Global/refined error | B.8--B.14; positive semigroup and finite geometric Taylor-tail bound |
| Cell comparison | Explicit N and D_bar domination, monotone forced system, B.15--B.16 |
| Pose/heading | G2.15, unit-heading norm, B.17; no heading samples |
| Contact square root | Direct rational squaring in B.20--B.21; left reserve may vanish |
| Collision distance | Reverse triangle inequality from one common center ball, B.19 |
| Saturation-exit proof | B.22--B.24 with uniform analytic remainders, not regime-dependent numerical integration |

There are two finite predictor levels (0 and 1), one optional kernel refinement, one parameter-label cell, one verification slab and finitely many explicit rational inequalities. This describes the operations in this hand proof, not general input complexity or online runtime. No implemented evaluator, solver, controller or experiment is part of this result.

## 9. Interpretation and unresolved research

Progress beyond Case A: matrices A/B/D vary with hidden parameters; the parameter image has an explicit preserved correlation; true trajectories cross a contact saturation corner; and the locked refined sufficient evaluation certifies where the other two declared evaluations return UNKNOWN.

Limitations: the actuator family is specially scaled and nonstiff; the obstacle is deliberately tuned; the contact margin remains generous; motor constants/resistances/damping are still singletons. The comparison isolates radius evaluation, not voltage selection: it does not show that V=0 fails or n=1 beats n=0. It establishes neither physical relevance nor intrinsic superiority over generic validated methods. A generic solver with an appropriate representation may do as well or better; no matched-method comparison was performed.

Thus practical usefulness, decision-relevant **voltage** dependence, general finite certification, runtime, physical correspondence and novelty remain UNVERIFIED. The generic-method novelty branch remains BLOCKED. No G2 PASS, G3 construction or GO follows. Case B does not amend MASTER or extend its uncertainty model.
