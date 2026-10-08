Session: DDWMR | LUNA-G2-SCOPE

# W2 G2 v6 preimplementation hypothesis — centered affine residual tube

**State:** frozen mathematical hypothesis before producer/checker implementation. It reuses the already locked synthetic task `G2_W2_VOF_TASK_V1`; no state, parameter, obstacle, voltage, duration, threshold, or criterion is changed. It is a candidate only until independent replay and the release audit.

## Supported subclass and quantifiers

Use MASTER v2.1's nine-state plant with the fixed known law `phi(s)=clip(s,-1,1)`, the fixed parameter image `[9999/10000,10001/10000]^12`, and the existing positive-width moving state box. For one fixed label vector `vartheta` and one common held voltage `V` from `(0,0)`, `(1/2,1/2)`, `(1,1)`, the claim concerns every initial state in that complete box and every `t in [0,T]`, `T=2 s`. Labels and voltage are constant along each trajectory. No physical-platform, recursive-safety, or hardware claim is included.

The reference is the allowed symmetric initial point

`x_c(0)=(p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R)=(0,0,0,3/10,0,1/4,1/4,0,0)`

with all twelve labels equal to one. Symmetry and uniqueness keep `r_c=theta_c=p_yc=0` and equal wheel/current states. On a clip-interior branch its reduced reference equations are

`u_c'=-3u_c+2w_c`, `w_c'=u_c-2w_c+i_c`, `i_c'=-w_c-i_c+V`, and `p_xc'=u_c`.

The point path is enclosed on contiguous partial slabs by exact/outward Taylor arithmetic. A strict bound `|w_c-u_c|<1` on every slab proves the reference uses the affine branch.

## Parameter-aware full-hold error bound

Write the six internal dynamics with an affine coordinate as `y' = A(vartheta,V)y`, `y=(z,1)`, `z=(u,r,omega_L,omega_R,i_L,i_R)`. Let `A0(V)` be the exact all-one parameter matrix and `Delta(vartheta,V)=A(vartheta,V)-A0(V)`. The interval parameter image gives an outward matrix residual

`delta_A >= sup_vartheta ||Delta(vartheta,V)||_infinity`.

Let `mu` outward-bound both (i) the infinity logarithmic norm of every six-state homogeneous matrix `A_theta[:6,:6]` and (ii) the infinity logarithmic norm of the augmented reference matrix `A0`. For `e=z_theta-z_c`, the exact difference equation is

`e' = A_theta,6 e + Delta_6,7 y_c`.

The logarithmic-norm differential inequality and `||y_c(0)||_infinity=1` imply, for every fixed label and all `t in [0,T]`,

`||e(t)||_infinity <= exp(mu*t) (e0 + t*delta_A)`,

where `e0=1/10000` is the exact maximum internal-coordinate distance from the reference point to the entire initial box. The implementation outward-encloses `exp(mu*T)` and rounds the resulting uniform radius `E` upward. This is a single continuous-time perturbation proof; it does not reset labels or carry a favorable label between slabs. Taking suprema in this error inequality is a comparison relaxation, not a model that permits time-varying true parameters.

For normalized slips `sigma_L=omega_L-u+r` and `sigma_R=omega_R-u-r`, the reference slip bound `beta_c` yields `|sigma_j|<=beta_c+3E`. If this is strictly less than one, a first-exit argument proves the complete true tube remains on the clip-affine branch; a trajectory could not first reach a clip corner while still lying in a tube whose slip bound is below one.

## Contact, pose, collision, endpoint task

On the proved branch, use the direct reserve inequality, without differentiating a square root:

`C_j*sqrt(1-sigma_j^2) >= C_min*(1-beta^2)`, for `beta=beta_c+3E<1`, because `sqrt(q)>=q` on `[0,1]` and `C_j>=C_min=9999/10000`.

The center has `r_c=0`, so `|m*u*r| <= (u_c_abs_upper+E)*E`. The sum of both wheel reserve lower bounds minus this demand is the contact-margin lower bound. A nonnegative lower bound certifies the algebraic contact domain on every time slab.

Let `theta_H=1/100000 + T*E`. Since `|r-r_c|<=E`, this bounds the full-hold heading. With a certified center speed upper bound `U_c`, directed endpoint and time-integrated pose deviations are

`E_J = T*E + T*U_c*theta_H^2/2`,

`E_px = 1/100000 + E_J`, and

`E_py = 1/100000 + T*(U_c+E)*theta_H`.

The center `p_xc(t)` is enclosed on every partial slab in a full-hold range `[P_min,P_max]`; monotonicity is not assumed. Its distance to the static center `(1/2,1/10)` is bounded using the closest horizontal gap from `[P_min,P_max]` to `1/2` and vertical gap `1/10`. The complete pose tube lies within Manhattan radius `E_px+E_py` of the reference path, which is an upper bound on Euclidean displacement. Collision is certified only if the directed center-distance lower bound minus `E_px+E_py` exceeds `3/50`.

The endpoint task enclosure is `[J_c^- - E_J, J_c^+ + E_J]`, where `[J_c^-,J_c^+]` is the independently Taylor-enclosed reference displacement. Task eligibility requires replayed collision/contact proof and lower progress at least the already frozen `7/20 m` threshold. An upper endpoint bound below `7/20 m` establishes a uniform task counterexample for that action; an UNKNOWN or a lower bound below threshold alone does not establish failure.

## Prospective feasibility screen and stop conditions

The exact/outward nonquery screen in `validation/autonomous_w2/g2/centered_error_tube_screen_v1.py` with its corrected full-time center-position tube is `results/validation/autonomous_w2/g2/centered_error_tube_preflight_v2.json`. It gives `delta_A=0.00100005`, `mu=1.00100001`, and `E=0.015548824` on all three actions. Rounded task enclosures are zero `[0.177596,0.240385] m`, nominal `[0.270772,0.333561] m`, and alternative `[0.363949,0.426737] m`. The corrected alternative collision lower margin is `0.033311 m`; contact lower margins exceed `1.63 N`; all clip bounds are below `0.422`. These are a feasibility screen, not query certificates. The earlier preflight v1 report used an unjustified monotone-center-path shortcut; v2 replaces it with the complete center `p_x` tube and exact minimum distance to that path. Preserve v1 as a failed diagnostic.

This method is rejected before native execution if the independent checker, arithmetic/resource guard, complete center-slab coverage, first-exit slip proof, endpoint task bound, or any action's required task distinction does not reproduce. No resource limit, task threshold, obstacle, or input is widened after observing candidate outputs. The method is generic centered validated-flow/comparison machinery; no novelty claim is made before G4's audit.
