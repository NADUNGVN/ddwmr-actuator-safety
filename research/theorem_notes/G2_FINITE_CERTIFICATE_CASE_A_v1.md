# G2 Case A: a finite rational one-hold certificate

2026-09-29. **ACCEPTED FINITE HAND CASE ONLY. G2 UNVERIFIED; overall HOLD.** GPT accepted A.1--A.23 at commit `d2cd85407bb5ba4b4360836c49aa8a9c7ec83f28`; see [the user-relayed review record](../../docs/reviews/GPT_G2_R2_d2cd854_ACCEPT_RECORD.md). Equations are unchanged. Acceptance does not establish practical usefulness or pass G2.

Governing formulation: MASTER v2.1. This is a deliberately synthetic mathematical instance of the accepted reduced model, not identified robot data. It instantiates [G2.1--G2.29](G2_ENCLOSURE_CANDIDATE_v1.md) without changing their assumptions. It supplies a hand proof with finitely many rational bounds, not an implemented interval solver. No trajectory samples, numerical integration or floating-point `expm` are used as evidence.

## 1. Data, units and quantifiers

Use reference units 1 s, 1 m, 1 kg, 1 A and their derived SI units. Normalize each coordinate by its own reference unit: u by 1 m/s, r and wheel rates by 1 rad/s, currents by 1 A, positions by 1 m, angle by 1 rad. Normalize time by 1 s. All norms and matrix row sums below act on these dimensionless coordinates. Rad is dimensionless in the equations. Parameter values in this table are numerical values in the stated units, not equalities between physical dimensions.

| Parameters | Numerical value | Unit |
|---|---:|---|
| m | 1 | kg |
| I_z, J_L, J_R | 1 | kg m^2 |
| R_w, b | 1 | m |
| v_s | 1 | m/s |
| c_u | 1 | kg/s |
| c_r, B_L, B_R | 1 | kg m^2/s |
| L_L, L_R | 1 | H |
| R_L, R_R | 1 | ohm |
| k_L, k_R | 1 | N m/A, equivalently V s/rad under ideal matched conversion |
| C_L, C_R | independently in [1,11/10] | N |
| V_max | 1 | V |

J, B, k are reflected wheel-side quantities. One purely algebraic ideal-gear realization on each side is ratio n_g=10, motor constant 1/10, wheel inertia/damping 1/10, and motor inertia/damping 9/1000 in their respective units. Then k=n_g k_motor=1 and J=J_w+n_g^2 J_motor=1, B=B_w+n_g^2 B_motor=1. This witnesses the adopted convention only; it does not identify a physical drivetrain or platform.

Select the known function

\[
\phi(q)=\max(-1,\min(q,1)),\qquad L_\phi=1. \tag{A.1}
\]

Clipping onto an interval is nonexpansive: case separation at -1 and 1 gives |phi(a)-phi(b)|<=|a-b|. It is bounded by 1, zero at zero, and q phi(q)>0 for every q!=0. Its extra oddness and monotonicity are properties of this example, not added MASTER assumptions. No derivative at the two corners is used.

Theta is exactly the rational box [1,11/10]^2 for (C_L,C_R), times the listed singleton values for all other parameters. The optional gear realization is fixed, not independently uncertain. Use **one parameter cell** covering this entire box, width 1/10 in each uncertain coordinate, and **one time slab** [0,T], where

\[
T=\frac1{10},\quad V=(\tfrac12,-\tfrac12),\quad
z_*=(\tfrac14,\tfrac18,\tfrac18,\tfrac38,0,0),\quad
(p_*,\theta_*)=((0,0),0). \tag{A.2}
\]

The common voltage satisfies the box limit. Each hidden C is fixed for the entire execution; no voltage selection uses it. Initial slip is zero on both sides. Initial forward and yaw speeds are nonzero. The obstacle and exclusion radius are

\[
p_o=(\tfrac35,0),\qquad R_s=\tfrac12. \tag{A.3}
\]

All ensuing bounds hold for **every** (C_L,C_R) in the full box and **every** t in [0,T]. Bounds on different coefficients relax dependence outward; they do not assert physical parameter switching. Use predictor depth n=1, with radius refinement ell=0 or 1, and the finite-cell fallback on the identical data.

## 2. Exact predictor primitives and residual

The body block of A is diag(-1,-1). On each ordered pair (omega_j,i_j), the motor block and its exponential are

\[
A_m=\begin{pmatrix}-1&1\\-1&-1\end{pmatrix},\qquad
e^{A_m t}=e^{-t}\begin{pmatrix}\cos t&\sin t\\-\sin t&\cos t\end{pmatrix}. \tag{A.4}
\]

F(z_*)=0. Writing w_j for the initial wheel rate (1/8 or 3/8), the n=0 predictor is

\[
u^0=\tfrac14e^{-t},\quad r^0=\tfrac18e^{-t},\quad
\omega_j^0=w_je^{-t}\cos t+V_j\int_0^te^{-s}\sin s\,ds,
\quad i_j^0=-w_je^{-t}\sin t+V_j\int_0^te^{-s}\cos s\,ds. \tag{A.5}
\]

The analytic inequalities e^{-t}<=1, |sin t|<=t and |1-cos t|<=t^2/2 for t>=0 imply

\[
|\sigma_j^0(t)|
\le\frac{w_j+|V_j|}{2}t^2\le\frac7{16}t^2,
\qquad |F_j(z^0(t))|\le a t^2,\quad a=\frac{77}{160}. \tag{A.6}
\]

Here the rolling initial condition cancels the w_j e^{-t} term in slip. This bound uses |phi(q)|<=|q|, which holds globally for (A.1); it does not presume the actual trajectory is unsaturated.

Let Delta z=z^1-z^0. Its exact integral is e^{A dot}*D F(z^0). Each body row has two force kernels with absolute value e^{-t}<=1, each wheel has one kernel bounded by 1, and each current has one kernel bounded by t. Hence

\[
|\Delta u|,|\Delta r|\le\frac{2a}{3}t^3,\quad
|\Delta\omega_j|\le\frac a3t^3,\quad
|\Delta i_j|\le\frac a{12}t^4. \tag{A.7}
\]

The last integral uses int_0^t (t-s)s^2 ds=t^4/12. Each slip row contains one u, one r, and one wheel component. Therefore the residual in G2.8 satisfies

\[
|S\Delta z|_j\le\frac{5a}{3}t^3,\qquad
d_{1,j}(t)\le c_d t^3,\quad c_d=\frac{11}{10}\frac{5a}{3}=\frac{847}{960}. \tag{A.8}
\]

The minimum with 2C in G2.8 can only reduce d_1. In particular all full-slab predictor bounds below are rational:

\[
|u^1|\le\frac14+\frac{2a}{3}T^3<\frac{251}{1000}=:U,
\quad |r^1|\le\frac18+\frac{2a}{3}T^3<\frac{126}{1000}=:R,
\quad |(Sz^1)_j|\le\frac7{16}T^2+\frac{5a}{3}T^3<\frac{13}{2500}. \tag{A.9}
\]

No nonlinear solution oracle or nested numerical quadrature is hidden here: (A.5) is explicit, and (A.6--9) bound its force and the next finite convolution on the complete domain.

## 3. Global comparison: a rational exponential bound

For M=A^#+|D|Q, the two body row sums are -1+3(C_L+C_R)<=28/5, the wheel row sums are 3C_j<=33/10, and current row sums are 0. M is Metzler. Positivity and M 1<=q 1 with q=28/5 imply

\[
0\le e^{Mt}{\bf1}\le e^{qt}{\bf1},\qquad
\|e^{Mt}\|_\infty\le e^{qt}. \tag{A.10}
\]

This is a positive-system comparison, not a claim that ||M||_infinity equals its signed row sum.

For x=14/25=qT, the Taylor terms starting at degree 2 have successive ratios at most x/3. Thus

\[
e^{qT}\le1+x+\frac{x^2}{2(1-x/3)}
=\frac{2673}{1525}<\frac95. \tag{A.11}
\]

Since || |D| d_1(s)||_infinity<=2 c_d s^3, G2.9 gives

\[
\|E_{1,0}(t)\|_\infty
\le\frac95\,2c_d\int_0^t s^3ds
=\alpha t^4,\quad \alpha=\frac9{10}c_d=\frac{2541}{3200}.
\quad \alpha T^4<\varepsilon_G:=\frac1{12500}. \tag{A.12}
\]

This is uniform on the slab; the polynomial upper envelope is increasing.

## 4. One exact-kernel refinement

For H(t)=|e^{At}D|, body row sums are bounded by 2, wheel row sums by 1, and current row sums by t. Each row of Q sums to at most 33/10. Substitution of (A.8),(A.12) into G2.12 with ell=0 gives

\[
E_{1,1,u}(t),E_{1,1,r}(t)
\le\frac{c_d}{2}t^4+\frac{33\alpha}{25}t^5, \tag{A.13}
\]

\[
E_{1,1,\omega_j}(t)\le\frac{c_d}{4}t^4+\frac{33\alpha}{50}t^5,
\qquad E_{1,1,i_j}(t)\le\frac{c_d}{20}t^5+\frac{11\alpha}{100}t^6. \tag{A.14}
\]

For example, int_0^t (t-s)s^3 ds=t^5/20 and int_0^t (t-s)s^4 ds=t^6/30. All coefficients are nonnegative, so substitution t=T bounds the whole slab. Every component is less than

\[
\varepsilon_H:=\frac{11}{200000}. \tag{A.15}
\]

The kernel is exact before the explicit inequalities above. These scalar bounds do not evaluate the exact refined radius or recover all signed correlations.

## 5. Finite-cell fallback on the same cell

Choose M_bar=M evaluated at C_L=C_R=11/10 (entrywise nondecreasing dependence). D_bar=|D|. Replace negative diagonal entries of M_bar by zero to get N. Body diagonals are positive and wheel diagonals nonnegative; only the current diagonals change. The row sums of N are at most 28/5 (current row sum becomes 1). Thus ||e^{Nt}||_infinity<=e^{qt}.

Choose the full-slab residual d_bar=c_d T^3 (1,1)^top. G2.28 with eta(0)=0 gives a nondecreasing comparison solution and

\[
\|\eta(T)\|_\infty
\le2c_d T^3\int_0^T e^{qs}ds
\le\frac{18}{5}c_d T^4
<\varepsilon_F:=\frac8{25000}. \tag{A.16}
\]

Consequently epsilon_F bounds the global comparison radius, hence the true predictor error, at every time in the one slab. The factor from replacing s^3 by T^3 is an explicit source of widening. No inverse of N is needed.

## 6. Full-time pose and collision evaluation

For any of the three uniform radii epsilon, G2.15 or G2.29 gives

\[
E_\theta\le T\varepsilon,\qquad
E_p\le T[\varepsilon+U T\varepsilon]
=\frac{10251}{100000}\varepsilon. \tag{A.17}
\]

The min with 2 can safely be upper-bounded by T epsilon. For the predictor, |theta^1|<=TR and ||p^1||_2<=TU=251/10000, since ||(cos theta,sin theta)||_2=1 exactly. This supplies a full reference-position ball without sampling the heading or computing transcendental values. Reverse triangle inequality yields

\[
g_p\ge\frac35-\frac{251}{10000}-\frac12-P, \tag{A.18}
\]

where P is a rational outward pose-radius budget in the table below.

| Radius construction | Uniform internal radius budget | Pose-radius budget P (m) | Certified lower g_p (m) |
|---|---:|---:|---:|
| Global, n=1, ell=0 | 1/12500 | 9/1000000 | 74891/1000000 |
| Impulse refinement, n=1, ell=1 | 11/200000 | 6/1000000 | 74894/1000000 |
| Finite fallback, n=1, one cell/slab | 8/25000 | 33/1000000 | 74867/1000000 |

These are absolute errors relative to each parameter's own center. They are not diameters of the union over parameter-dependent centers. A common full position enclosure is the ball of radius TU+P, centered at p_*. It deliberately drops the center dependence outward.

## 7. Full-time contact evaluation

Because v_s=L_phi=1 and |S| has row sums 3, G2.19 and (A.9) imply

\[
\beta_j\le\frac{13}{2500}+3\varepsilon.
\tag{A.19}
\]

The resulting bounds are 68/12500 (global), 1073/200000 (refined), and 77/12500 (fallback). All are below 1/100. For each wheel,

\[
\sqrt{1-\beta_j^2}\ge\sqrt{\frac{9999}{10000}}
\ge\frac{9999}{10000}, \tag{A.20}
\]

where the last lower bound is certified by squaring the nonnegative rational and comparing it with the radicand. Since C_j>=1, the total reserve is at least 9999/5000. For all methods,

\[
|u^1|+E_u\le U+\varepsilon_F<\frac{63}{250},\quad
|r^1|+E_r\le R+\varepsilon_F<\frac{127}{1000}.
\tag{A.21}
\]

With m=1, the demand is at most 8001/250000. Therefore

\[
g_c\ge\frac{9999}{5000}-\frac{8001}{250000}
=\frac{491949}{250000}>0. \tag{A.22}
\]

This common coarse lower bound is in N; it does not assert equal actual margins across methods. The square root is bounded directly, with no differentiation near its boundary.

## 8. Finite primitive ledger and conclusion

| Primitive | Complete bounding rule used here |
|---|---|
| Rational arithmetic | Exact integer fractions; any stated strict comparison follows by cross-multiplication of positive denominators. No machine rounding is part of the proof. |
| phi and L_phi | Exact clip at rational endpoints; nonexpansiveness and |phi(q)|<=|q| from (A.1). |
| Parameter/time cover | One closed rational capacity box and one closed time interval; every displayed inequality holds throughout their product. |
| e^{At} | Exact damped rotation/body exponentials (A.4--5); scalar inequalities (A.6). |
| e^{Mt}, e^{Nt} | Positive comparison (A.10), rational series-tail bound (A.11). |
| Nested predictor and residual | (A.5--9), polynomial integrals; all forces bounded before integration. |
| Refined kernel integrals | (A.13--14), kernels bounded by 1 or t; exact integrals of monomials. |
| Trigonometric/pose range | |sin t|<=t, |1-cos t|<=t^2/2, |cos t|<=1 and exact unit-heading norm. Pose errors use G2.15. |
| Square root | Nonnegative rational lower bound verified by squaring (A.20). |
| Obstacle distance | Reverse triangle inequality from a reference-position ball (A.18). |

**Proposition (Case A, independently accepted).** For the exact data in Section 1, the single admissible voltage V=(1/2,-1/2), applied continuously over [0,1/10], has for all execution-fixed capacity pairs in Theta a tube satisfying

\[
\forall\vartheta\in\Theta\ \forall t\in[0,1/10]:\qquad
g_p(t,\vartheta)\ge\frac{74867}{1000000}>0,\qquad
g_c(t,\vartheta)\ge\frac{491949}{250000}>0. \tag{A.23}
\]

**Proof.** Equations (A.6--16) instantiate the already reviewed global/refined/fallback inclusions. Equations (A.17--22) bound all required quantities on the full parameter/time cell. Apply G2-A/B, using the same parameter label in each fiber. The worst listed collision bound and common contact bound give (A.23). Thus the formal reduced-model trajectory remains collision-free and contact-admissible for this hold. QED. The arithmetic chain was independently accepted in the review cited above.

## 9. What the comparison measures and leaves open

The declared internal **upper budgets** have H/G=11/16 and F/G=4. This compares the explicit outward bounds used in this proof, not actual tube-radius ratios and not measured overestimation relative to the exact reachable set. The generic analytical inequality E_1,1<=E_1,0 is separate. The position-clearance bounds differ by only micrometers in this synthetic scaling because the common coarse center ball dominates.

This is a nonzero-speed, nonzero-yaw, nonzero-voltage, uncertain-capacity example; it is intentionally easy. Large contact reserve, broad obstacle clearance, simple motor coefficients and locally unsaturated phi make it unsuitable as evidence of practical superiority. The proof does not establish that a zero-voltage or n=0 alternative fails; safe action necessity is unproved. It also does not compare against a generic validated solver.

Time T=1/10 s is an accepted certified mathematical example horizon. It is **not** a useful physical sampling limit. All uncertainty is in two capacities; stiff motor parameter uncertainty is absent. In particular, A.9 and A.19 imply every certified normalized slip is below one in magnitude, so this entire example remains on the linear branch of clip. There is no runtime measurement, implemented arithmetic library, general finite solver, operational UNKNOWN map, stopping/turning guarantee, state-estimation error model, hardware correspondence, recursive subset or novelty closure.

G1 retains its restricted PASS. G2/G3/G4 remain UNVERIFIED, physical correspondence UNVERIFIED, overall HOLD. Case A does not change canonical metadata or authorize implementation.
