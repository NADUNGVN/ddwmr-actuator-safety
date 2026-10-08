Session: DDWMR | LUNA-G2-SCOPE

# W2 G2 v6 proof-to-code map

**State:** implementation candidate for release-scoped G4 audit. The equations below are derived under the declared synthetic protocol and the reduced MASTER v2.1 model; independent audit is still required. No native row is represented by the fixtures in this package.

## Supported plant and task

The supported trajectory has nine states `(p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R)`, the known law `phi(s)=clip(s,-1,1)`, constants `m=I_z=R_w=b=v_s=c_u=c_r=V_max=1`, and one fixed label vector in `[0.9999,1.0001]^12`, ordered as in the frozen protocol. The initial state is anywhere in the positive-width protocol box. For one query the selected voltage is fixed for all `T=2 s`; allowed pairs are `(0,0)`, `(1/2,1/2)`, `(1,1)`. The same fixed label is used in all 256 slabs. Task: full-hold static-circle clearance and algebraic contact admissibility, plus displacement `p_x(T)-p_x(0) >= 7/20 m`.

This does not establish a physical tire/support model, a recursive safe set, closed-loop safety, or general asymmetric-voltage coverage.

## Center and residual enclosure

For the all-one label vector and initial point `(0,0,0,3/10,0,1/4,1/4,0,0)`, symmetry is invariant for equal left/right held voltage. On the clip-affine branch the reduced center equations are

`u_c'=-3u_c+2w_c`, `w_c'=u_c-2w_c+i_c`, `i_c'=-w_c-i_c+V`, `p_xc'=u_c`.

The center path is enclosed on each complete partial slab `[kh,(k+1)h]`, `h=1/128`, with an order-20 Taylor polynomial and a symmetric induced-infinity-norm tail. The endpoint interval is passed to the next slab. `producer_centered_v6._center_matrix`, `_flow` (through `producer_v4.exp_range`) and its per-slab state hashes implement this path; checker `_center_matrix`, `_flow`, and endpoint-chain checks independently reconstruct it.

Let `z=(u,r,omega_L,omega_R,i_L,i_R)`, `y=(z,1)`, and `z'=A(theta,V) y` whenever both slips are inside the clip-affine region. `A_0(V)` is the exact matrix at the all-one center label. The interval label image induces

`delta_A >= sup_theta ||A(theta,V)-A_0(V)||_infinity`,

`mu_p >= sup_theta mu_inf(A(theta,V)[:6,:6])`,

`mu_0 >= mu_inf(A_0(V))` for the augmented center matrix,

where `mu_inf(M)=max_i(M_ii + sum_{j != i}|M_ij|)`. The implementation bounds each diagonal above and each off-diagonal absolute value above using exact rational interval endpoints; the residual includes the affine input column. Set `mu=max(0,mu_p,mu_0)`.

With `e=z-z_c`, the same-label difference satisfies `e'=A(theta,V)[:6,:6]e + (A(theta,V)-A_0(V))y_c`. The logarithmic-norm comparison and `||y_c(0)||_infinity=1` give, for each fixed label and every `t in [0,T]`,

`||e(t)||_infinity <= exp(mu*t) (e0+t*delta_A)`,

with `e0=1/10000`. Thus `E=ceil_grid(exp(mu*T)*(e0+T*delta_A))` is a uniform full-hold error radius. This comparison takes a supremum over labels; it does not allow a true label to vary between slabs. `producer_centered_v6._parameter_bounds`, `_exp_scalar_upper`, and `_compute` implement the bound. `checker_centered_v6._matrix_bounds`, `_exp_upper`, and `_reconstruct` recompute it without importing the producer.

## Clip branch and contact

For each wheel, normalized slip is `sigma_L=omega_L-u+r` and `sigma_R=omega_R-u-r`. The center slip bound `beta_c` comes from the complete partial-slab center path. Each slip differs from the center by at most `3E`, so `beta=beta_c+3E`. If `beta<1`, a first-exit argument proves every true trajectory remains in the affine clip branch through the full hold: up to a first hit, the residual estimate applies, but it implies strict distance from the hit set. If this strict condition fails, v6 returns UNKNOWN and does not use the affine formula.

For beta below one, `a_j=C_j*sqrt(1-sigma_j^2)`. Since `sqrt(q)>=q` for `q in [0,1]`, each reserve is at least `C_min*(1-beta^2)`, with `C_min=9999/10000`. Center yaw rate is zero, hence `|m*u*r| <= (U_c+E)E`, where `U_c` is the complete center-speed absolute upper bound. The lower contact margin is `2*C_min*(1-beta^2) - (U_c+E)E`. A nonnegative margin proves `a_L+a_R >= |mur|`, exactly the stipulated algebraic lateral-reaction feasibility condition. No derivative of the square-root reserve is taken. Producer fields: `clip_beta_upper_full_domain`, `contact_reserve_per_wheel_lower_N`, `contact_demand_upper_N`, and `contact_margin_lower_N`; the checker recomputes each.

## Pose, collision, and task progress

Let `theta_H=theta_0+T*E`. Then for every time, `|theta-theta_c|<=T*E`. Because `|1-cos(theta)|<=theta^2/2` and `|sin(theta)|<=|theta|`,

`E_J=T*E + T*U_c*theta_H^2/2`,

`E_px=p_x0_abs+E_J`, `E_py=p_y0_abs+T*(U_c+E)*theta_H`.

The reference has `p_yc=0`. Its entire `p_x` path is enclosed in `[P_min,P_max]` by all contiguous partial slabs, with no monotonicity assumption. For obstacle center `(o_x,o_y)`, the distance from the reference path to the obstacle center is bounded below by the distance from `(o_x,o_y)` to `[P_min,P_max] x {0}`. Subtracting `E_px+E_py` (an upper bound on Euclidean deviation) and the inflated radius yields a conservative full-hold collision-margin lower bound; it must be strictly positive.

The task displacement enclosure is `[p_xc(T)-E_J, p_xc(T)+E_J]`. `progress_lower >= 7/20` together with replayed contact and collision predicates is the only eligibility rule. An upper endpoint below `7/20` proves that action is uniformly task-ineligible on this declared domain. UNKNOWN alone does not.

## Arithmetic, replay, and trust

All endpoints are exact `Fraction` values rounded outward to a 96-bit dyadic grid. The order-20 Taylor remainder uses `q^(N+1)/(N+1)!/(1-q/(N+2))`; profile validation fixes 256 slabs, 1/128 s, precision, bit/operation caps and process caps before evaluation. Full-hold proof fields are serialized as reduced rational strings. The checker independently rebuilds the parameter matrix, center path, residual, contact, collision, progress and every output field; it also checks ordered contiguous slab coverage, endpoint chaining, fixed center labels, fixed voltage and binding/source hashes.

Shared trust dependencies are Python `fractions.Fraction`, `rational_interval_v3.I/Budget`, JSON parsing, the Windows Job Object supervisor for resource enforcement, and the correctness of the MASTER v2.1 reduced equations and clip law. The checker does not import the producer or its matrix constructor. The finite path is not independently audited until G4 records a decision bound to the release manifest hash.
