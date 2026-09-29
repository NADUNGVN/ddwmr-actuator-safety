# G2 finite evaluator specification v1

**Status (2026-09-29): DRAFT for root/GPT audit. G2 UNVERIFIED; G3/G4 UNVERIFIED; overall HOLD.** Workflow W1 authorizes scoped validation implementation through `../../docs/LUNA_VALIDATION_HANDOFF_v1.md`. This document specifies a computational subclass and a one-hold sufficient evaluator; its equations remain a draft requiring audit, not an accepted theorem or physical-platform claim. The code permission comes from the user decision in MASTER, not this specification.

## 1. Claim boundary

For one exact held voltage and an effective finite input described below, the evaluator must halt. `CERTIFIED` implies that every initial state in the queried rational cell, every fixed hidden-parameter label in the represented parameter set, and every time in the entire hold satisfy the static-obstacle and ideal-contact conditions of MASTER §§14–16. `UNKNOWN` makes no safety or unsafety claim. `INVALID_INPUT` means the input failed the declared computational contract. No endpoint-only result is a continuous-safety certificate.

A cell of initial states is an offline verification family: the theorem quantifies over every member of that cell under the one listed voltage. It does not model state-estimation error or change MASTER's exact sampled-state assumption. At deployment-scale queries the cell may be a singleton. The center/predictor remains indexed by the same initial state and parameter label; no midpoint initialization is allowed. Error radii start at zero relative to that same pair.

## 2. Effective input class: `G2-COMP-clip`

This is a deliberately narrower computability class inside the adopted reduced model, not a new physical assumption.

1. **Plant and law.** Use the nine-state MASTER v2.1 equations, fixed period `T>0`, exact ZOH input `V`, and the known selected law
   `phi(q)=clip(q,-1,1)`, `L_phi=1`. Clip is globally bounded, globally 1-Lipschitz and strictly sign-preserving. No contact derivative is required. Its explicit min/max representation supplies interval evaluation; this does not assume monotonicity or oddness for the broader MASTER law class. Other laws may enter a future effective class only with their own finite evaluator contract.
2. **Rational state cells.** Each initial cell `X` is a nonempty closed rational box in the nine state coordinates. All endpoints are exact rationals. Positive widths are permitted and used by the benchmark; a singleton is permitted. The same input `V in [-Vmax,Vmax]^2` is one rational vector for the whole cell and every hidden label.
3. **Fixed parameter labels.** A parameter cell is the image of a rational label box `xi in [a,b]` under a finite vector of rational functions `theta_i(xi)=p_i(xi)/q_i(xi)`. A finite union of these mapped cells defines `Theta_COMP`. Labels and their correlations are retained as one fixed `xi` along the whole hold; no resampling or parameter switching occurs. This admits identity and correlated maps such as reciprocal actuator parameters. Every denominator and every parameter required positive has a rational positivity witness. One allowed witness is a positive lower bound verified from exact Bernstein coefficients on the rational label box. Cells must also certify all required nonnegative/positive parameter bounds and declared gear/conversion relations.
4. **Coverage of a broader `Theta`.** The theorem directly covers `Theta_COMP`. A claim for another declared compact `Theta` is permitted only with a checked finite witness that `Theta` is contained in `Theta_COMP`; there is no membership or optimization oracle for arbitrary compact sets. Outer-cover relaxation is sound when inclusion and denominator validity are proved and its extra conservatism is reported.
5. **Scene and query.** `T`, `Vmax`, the query voltage, circular-obstacle centers/radii, and all fixed data are rational. A query carries a finite obstacle list and one parameter/state cell. Endpoint targets are optional rational boxes. Pose uses the full MASTER footprint radius `R_s`; no estimation margin is implicit.
6. **Finite resource profile.** The query supplies finite limits fixed before the run: predictor depth (`n>=1`), Taylor-series terms, parameter-cell split depth/count, initial-state split depth/count, time subdivisions/integration panels, square-root bisections, rational bit length, and rational-operation count. No tolerance-driven unbounded loop is allowed. Exceeding any limit on an otherwise valid input returns `UNKNOWN`.

All rational arithmetic below is exact. An implementation using binary floating-point must replace it with directed outward rounding and verify rounding-error inclusion. This specification does not assert such an implementation exists.

A positivity witness must be finite and checked, not an assertion from the caller. For the Bernstein option, supply rational coefficients and finite degrees on the affinely normalized label box; expand the supplied polynomial representation and verify coefficient equality exactly against the declared polynomial. Its range lies within the minimum and maximum Bernstein coefficients, providing the claimed sign bound. Direct rational interval evaluation is another sufficient witness when its range has the required sign. For a rational expression, check denominator positivity before division. A declared gear witness supplies rational component maps; verify their required signs and the gear identities by clearing the already validated nonzero denominators and checking polynomial coefficients. These checks may reject a representation whose underlying plant is nevertheless valid; `INVALID_INPUT` refers only to this effective contract. Resource exhaustion while checking a well-formed witness is `UNKNOWN`, not proof of an invalid physical model.

## 3. Finite enclosure recipe

Use the six-state block `z=(u,r,omega_L,omega_R,i_L,i_R)` and the MASTER/candidate decomposition `zdot=A(theta)z+B(theta)V+D(theta)F(z,theta)`, `F_j=C_j clip((S(theta)z)_j/v_s)`. Matrix entries are enclosed on each mapped parameter-label cell with rational interval arithmetic; all required divisors have positivity witnesses.

### 3.1 Matrix exponential and integral primitives

Choose a positive rational diagonal scaling matrix `P_s` and write `z=P_s*z_tilde`. In scaled coordinates use `A_tilde=P_s^(-1) A P_s`, `B_tilde=P_s^(-1) B`, `D_tilde=P_s^(-1) D`, and `S_tilde=S P_s`. Compute exponential, matrix-norm, predictor, and comparison bounds in these coordinates (with `Q_F_tilde=diag(C_j L_phi/v_s)*|S_tilde|`). Before pose/contact checks, restore every internal-state range and radius by multiplication by `P_s`, componentwise. If `eta_tilde` is the scaled error radius, the physical radius is `eta_z=P_s*eta_tilde`. The exponential enclosure may be kept scaled throughout; if a physical-coordinate exponential is needed, map it by `P_s*exp(A_tilde*tau)*P_s^(-1)`. The identity scaling is allowed.

For any interval matrix `K` enclosing `A_tilde(theta)*tau` over a complete parameter/time cell, compute `Q >= sup ||A_tilde(theta)*tau||_infinity` rationally. Enclose `exp(A_tilde*tau)` by the interval polynomial `sum_{k=0}^N K^k/k!` plus a symmetric entrywise remainder of radius

`R_N = 3^ceil(Q) * Q^(N+1)/(N+1)!`.

This follows from the exponential series tail `e^Q Q^(N+1)/(N+1)!` and `e^Q < 3^ceil(Q)` for `Q>0`; the zero case has zero tail. Choose `N` from the finite resource profile. If the resulting interval is too wide, return `UNKNOWN`; do not substitute an ordinary floating-point `expm`.

For a continuous integrand whose complete range on a fixed panel `[a,b]` of length `h=b-a` is enclosed by interval `G`, use `integral_a^b g(s)ds in h*G` (componentwise interval product). For a variable partial upper limit `t in [a,b]`, use the sound but coarser inclusion `[0,h]*G`. Every integrand value on the whole panel must first be enclosed; this is interval range integration, not a hidden quadrature oracle. Dependency can make it wide, and no convergence or usefulness claim follows merely from subdivision. A tighter midpoint rule is allowed only with a certified uniform derivative bound `M1` and explicit remainder `M1*h^2/4`; it is not assumed here. Polynomial pieces may instead be integrated exactly with rational antiderivatives. Time subdivisions cover closed slabs whose union is `[0,T]`; slab boundaries do not reset voltage, state, or parameter labels.

For a nonnegative rational endpoint `a`, select the square-root enclosure deterministically by `B_sqrt` bisections, where `B_sqrt` is the finite profile limit. Start with `[lo,hi]=[0,max(1,a)]`, so `lo^2<=a<=hi^2`. Repeat exactly `B_sqrt` times: set `mid=(lo+hi)/2`; if `mid^2<=a`, replace `lo` by `mid`, otherwise replace `hi` by `mid`. Return `[lo,hi]`; both endpoints are nonnegative rationals and exact squaring verifies `lo^2<=a<=hi^2`. For `a=0`, return `[0,0]` directly. For an interval radicand `[l,u]`, require `0<=l<=u`, apply this procedure to `l` and `u`, and use the lower endpoint for `sqrt_lower(l)` and upper endpoint for `sqrt_upper(u)`. If a preceding outward calculation cannot prove `l>=0`, return `UNKNOWN`. For sine/cosine, use rational Taylor polynomials on the complete angle interval and Lagrange remainder `|theta|^(N+1)/(N+1)!` (all derivatives have magnitude at most one); insufficient series budget gives `UNKNOWN`.

### 3.2 Predictor range and internal error

In this subsection only, suppress tildes: `A,B,D,S,X_z,z,P_k,Q_F,M,N,eta` denote their consistently scaled-coordinate versions from §3.1, with initial box `X_z=P_s^(-1)*X_z_physical`. Restore `P_s*P_n` and `P_s*eta` before §3.3; its matrices and velocity/rate quantities are physical again. This convention prevents applying a scaled radius to an unscaled slip row.

For `P_-1` equal to the interval hull of the initial internal-state box, construct finitely many predictor range enclosures. Given `P_(k-1)`, enclose the complete integrand

`G_k = exp(A*tau) [B V + D F(P_(k-1),theta)]`, `tau in [0,T]`,

by interval operations, then set

`P_k = exp(A*[0,T]) X_z + [0,T]*G_k`.

This encloses the candidate finite Picard predictor `z^k(t;x0,theta,V)` for every `t in [0,T]`, `x0 in X`, and label in the cell. It uses the exact clip interval extension and the exponential/integral rules above; it does not evaluate the unknown nonlinear trajectory. Correlations may be relaxed in interval hulls only outward. Predictor ranges are families indexed by the original `(x0,xi)` even if the arithmetic hull discards dependence.

Use `n>=1`. Bound the paired predictor increment `|z^n-z^(n-1)|` by the interval difference of their complete ranges; this is conservative and includes every same-`(x0,xi,t)` difference. With `Q_F=diag(C_j L_phi/v_s)|S|`, form a rational force residual bound

`dbar_j = min( (Qbar_F * delta_z)_j, 2*Cbar_j )`,

where `delta_z` is the componentwise upper absolute difference, `Qbar_F` is a rational componentwise nonnegative upper bound on every `Q_F(theta)` in the cell, and `Cbar_j` is an upper capacity bound. No coefficient is evaluated only at a favorable parameter label.

For the comparison step compute a rational componentwise upper bound `Mbar` on `M(theta)=A#(theta)+|D(theta)|Q_F(theta)`, where `A#` retains the diagonal and takes absolute off-diagonal entries. Set `N=max(0,Mbar)` entrywise and `Dbar >= |D|`; then `N>=M(theta)` and `N>=0` on the full cell. The comparison radius solves the nonnegative majorant `eta_dot=N eta + Dbar*dbar`, `eta(0)=0`. Enclose it by the finite positive series

`eta(T) = sum_{k>=0} N^k T^(k+1)/(k+1)! * Dbar*dbar`.

Keep terms through the configured order and add a rational upper tail: with `Q=||N||_infinity*T`, `q=||Dbar*dbar||_infinity`, the omitted norm is at most `T*q*3^ceil(Q)*Q^(K+1)/(K+2)!`. Since `N` and the forcing are nonnegative, the resulting outward vector bounds every `eta(t)` for `0<=t<=T`. No matrix inverse is used. Failure of a tail/margin check returns `UNKNOWN`.

### 3.3 Full-hold pose, collision, and contact checks

Let `eta_z` be the full-hold physical internal radius, `U` an upper bound on physical `|u^n|`, and `R` an upper bound on physical `|r^n|`, all over the complete initial/parameter/time cell. Lift the predictor family by

`E_theta = T*eta_r`, `E_p = T*[eta_u + U*min(T*eta_r,2)]`.

Explicitly enclose the heading predictor range and position predictor range as

`Theta^n = X_theta + [0,T]*P_(n,r)`,

`P^n = X_p + [0,T]*(P_(n,u) * (cos(Theta^n), sin(Theta^n)))`,

where `P_(n,u)` and `P_(n,r)` are the restored physical component ranges of `P_n`; all products and trigonometric ranges are outward interval operations. The Taylor sine/cosine rule above applies to the complete `Theta^n`. The exact positions lie within distance `E_p` of their same-label/same-initial-state predictor centers, and all such centers lie in `P^n`.

For each static circle `(p_o,R_s)`, compute a rational lower bound on distance from its center to the complete position box `P^n` by coordinatewise box-to-point gaps and the square-root recipe. A collision pass requires `dist_lower(p_o,P^n)-R_s-E_p >= 0` for every obstacle. This check covers every point in the full hold, not just slab endpoints.

For contact, use the candidate sufficient bound

`beta_j = min(1, bphi_j + (L_phi/v_s_low) (Sbar_abs eta_z)_j)`.

Here `bphi_j` is the rational upper absolute endpoint from interval evaluation of `clip((S P_n)_j/v_s)` on the restored physical predictor range and full parameter cell; `Sbar_abs` bounds every physical `|S(theta)|` componentwise. Thus no supremum oracle occurs. The finite clip extension is `[clip(a),clip(b)]` for an input interval `[a,b]`, using exact rational min/max. This uses the known clip representation, not a monotonicity assumption on every law admitted by MASTER.

Compute `A_lower = sum_j C_lower,j * sqrt_lower(1-beta_j^2)`, and `Y_upper = m_upper*(U+eta_u)*(R+eta_r)`. Contact passes only if `A_lower-Y_upper >= 0` on every label/state cell and every full time slab. This checks the algebraic contact domain without differentiating its square root. If a wheel has `beta_j=1`, it contributes zero lower reserve.

`CERTIFIED` requires both full-hold checks for every cell. An optional endpoint target is a separate additional predicate. A coarse endpoint enclosure may reuse the complete hold enclosure: the endpoint internal state lies in `P_n` expanded by `eta_z`, heading in `Theta^n` expanded by `E_theta`, and position in `P^n` expanded by `E_p`. Prove this product enclosure is contained in the target box. Endpoint inclusion never substitutes for collision/contact checks over `[0,T]`, and does not establish recursive feasibility or G3.

## 4. Soundness and finite-termination statement

**Sufficient evaluator theorem (specification target).** For every valid `G2-COMP-clip` query, the bounded algorithm halts with `CERTIFIED` or `UNKNOWN`. If it returns `CERTIFIED`, then for every `x0 in X`, every fixed `xi` represented by the parameter cell (hence its single fixed `theta(xi)`), and every `t in [0,T]`, the MASTER reduced-model trajectory under the one common rational voltage `V` satisfies `h_l(p(t))>=0` for every listed obstacle and belongs to `D_c(theta(xi))`. If the optional endpoint predicate is requested and certified, `x(T)` also lies in its target box. `UNKNOWN` is inconclusive. No theorem is asserted for malformed inputs or for arbitrary non-effective compact parameter sets/functions.

**Soundness argument.** The interval exp/integral rules enclose each finite predictor range; Lipschitz force increments give the residual bound; the Metzler comparison theorem with `N>=M` and `Dbar*dbar` encloses the exact internal-state error for each same initial/parameter label. Pose lifting encloses heading and position over the complete hold. The reverse triangle inequality proves obstacle clearance; the clip Lipschitz bound and rational square-root lower bounds prove available contact reserve dominates the `|m u r|` demand. Thus the exact trajectory remains in the collision/contact set at all times. The quantifier order is `for each X-cell: one V; for all fixed labels; for all t`; it is never `for each label choose V`.

**Termination.** All loops are bounded by finite input limits: finite cells, predictor depth, time/parameter subdivisions, Taylor orders, and rational-operation budget. There is no iteration until convergence or positive tolerance. Exhaustion, a wide enclosure, or an unproved nonnegative radicand produces `UNKNOWN`. `INVALID_INPUT` is reserved for malformed dimensions/rationals, empty cells, failed positivity/correlation/voltage witnesses, unsupported law/scene encoding, or a requested parameter cover with no checked inclusion. A valid input can therefore never run indefinitely.

## 5. Separate acceptance obligations and open items

- **Soundness:** mandatory before interpreting any certificate; independently audit the interval integration, parameter map/positivity checker, comparison matrix domination, and full-slab pose/contact equations.
- **Finite termination:** established by bounded loops only once an implementation fixes its resource profile; termination is not a complexity or runtime guarantee.
- **Useful coverage:** not implied by soundness or termination. An always-`UNKNOWN` evaluator satisfies neither usefulness nor G2 closure. It is measured only by the predeclared benchmark spec.
- **OPEN:** this interval-hull predictor may be very conservative; no useful coverage, runtime, solver implementation, or physical parameter provenance is claimed. The midpoint-rule option remains conditional on a separately checked derivative bound. Exact-kernel refinement is not required by this fallback and is not claimed closed for the general input class.
- **OPEN:** externally supplied covers of a more general MASTER `Theta` need an independently checkable inclusion witness. The arbitrary compact-set and arbitrary Lipschitz-function cases in MASTER are outside `G2-COMP-clip` unless given effective representations.

Cases A/B are accepted finite synthetic hand certificates; Case C is limited to its reviewed certificate-output scope. None supplies a general evaluator result or usefulness evidence. Preserve **G2/G3/G4 UNVERIFIED; HOLD**.

