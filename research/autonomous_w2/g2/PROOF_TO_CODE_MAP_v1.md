Session: DDWMR | LUNA-G2-SCOPE

# W2 G2 candidate v1 — proof and implementation map

**State:** candidate proof for bounded development, not a gate acceptance or confirmation lock. The task and threshold were frozen in `HYPOTHESIS_AND_TASK_PREIMPLEMENTATION_v1.md` before this implementation. All quantities below are exact rationals unless explicitly described as a displayed decimal.

## Claim and quantifiers

For each fixed action (V=(V_L,V_R)) in the frozen three-action set, let (X_0) be the entire rational initial box in state order `[p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R]`, and let (artheta) range over the entire twelve-coordinate fixed-label image. If all 16 slab enclosures satisfy the resource, strict clip-interior, full-slab contact and collision inequalities below, the replayed result encloses the trajectory for every (x_0\in X_0), every one fixed (artheta\in\Theta), and that one constant (V) on the complete hold ([0,2]). `CERTIFIED` means the stated full-hold collision and contact inequalities hold for this synthetic model/domain. `UNKNOWN` means the sufficient enclosure did not establish them. It does not assert a physical failure.

The model is MASTER v2.1 with known `phi(s)=clip(s,-1,1)`, fixed constants (m=I_z=R_w=b=v_s=c_u=c_r=1), and execution-fixed labels

\[
\rho_j,C_j,\lambda_j,R_j,B_j,k_j\in[9999/10000,10001/10000],\quad
J_j=1/\rho_j,\quad L_j=\lambda_j.
\]

All interval widths, including each of the nine initial-state coordinates, are positive. The parameter image is rational and compact; every denominator ρ, λ, (m), (I_z), (v_s) is bounded strictly above zero. The optional gear witness has (n=10), (k_m=k/10), (J_w=1/10), (J_m=(1/\rho-1/10)/100>0), (B_w=0), and (B_m=B/100); it is an algebraic realizability witness only, not platform provenance.

## Signed affine branch

Write (z=(u,r,\omega_L,\omega_R,i_L,i_R)). If both normalized slips stay strictly inside ((-1,1)), then the clip law is the identity on the full trajectory and, for each fixed label and held voltage,

\[
\dot z=A(\vartheta)z+b(\vartheta,V),\qquad
\dot y=\mathcal A(\vartheta,V)y,\quad y=(z,1).
\]

With (F_L=C_L(\omega_L-u+r)), (F_R=C_R(\omega_R-u-r)), the nonzero coefficient structure is:

\[
\begin{aligned}
\dot u&=-(1+C_L+C_R)u+(C_L-C_R)r+C_L\omega_L+C_R\omega_R,\\
\dot r&=(C_L-C_R)u-(1+C_L+C_R)r-C_L\omega_L+C_R\omega_R,\\
\dot\omega_L&=\rho_L(C_Lu-C_Lr-(B_L+C_L)\omega_L+k_Li_L),\\
\dot\omega_R&=\rho_R(C_Ru+C_Rr-(B_R+C_R)\omega_R+k_Ri_R),\\
\dot i_j&=-(k_j/\lambda_j)\omega_j-(R_j/\lambda_j)i_j+V_j/\lambda_j.
\end{aligned}
\]

This keeps signed off-diagonal coupling through body speed/yaw, wheel speed, winding current, back-EMF and the one constant voltage. It replaces the R3 route that bounds force defects and propagates them with a nonnegative comparison matrix by a direct interval matrix flow on the clip-interior subclass. It is not a tighter bound by theorem alone; only replayed output can establish an effect on this task.

## Per-slab enclosure and termination

Partition ([0,2]) into 16 contiguous slabs of (h=1/8). Let Τ be the single full label image. On slab (k), the input interval (Y_k) contains the previous endpoint enclosure; the same Τ and (V) are used again. Interval matrix products outer-bound every fixed (\mathcal A(\vartheta,V)^nY_k). For each (0\le\tau\le h), retain the rational Taylor polynomial

\[
P_{20}(\tau)Y_k=\sum_{n=0}^{20}\frac{\tau^n}{n!}\,\mathcal A^nY_k
\]

and add a symmetric remainder to each nonconstant coordinate. With (q=h\sup_{\vartheta\in\Theta}\|\mathcal A(\vartheta,V)\|_\infty), (M=\sup_{y\in Y_k}\|y\|_\infty), and (q/22<1),

\[
\left\|\sum_{n=21}^{\infty}\frac{\tau^n}{n!}\mathcal A^ny\right\|_\infty
\le M\frac{q^{21}}{21!}\frac{1}{1-q/22}.
\]

The tail follows by bounding the ratio of successive absolute terms by (q/22) after degree 21. For a partial-slab range, use τᴿⁿ ∈ [0,hⁿ] for each (n>0); for an endpoint, use exactly (h^n). Thus the partial enclosure covers every time in a slab and the separate endpoint encloses (z(t_{k+1})). The last augmented coordinate remains exactly one. If an operation/bit/wall/memory/output cap is hit, no finite enclosure is reported.

At every slab, compute

\[
s_L=\omega_L-u+r,\qquad s_R=\omega_R-u-r.
\]

If the computed partial-slab range gives βⱼ = max |sⱼ| < 1 for both sides, it proves strict interior for the candidate linear solution throughout that slab. By induction, starting from (X_0), assume the true state is in (Y_k); the interval matrix Taylor bound contains its affine solution. A first-exit argument then applies: any first clip-boundary time would belong to the partial-slab enclosure, contradicting the strict β < 1 bound. Hence the MASTER clip trajectory equals the affine trajectory on the slab and lies in the enclosure; the endpoint is a valid next input enclosure. If strict interior fails, the candidate returns `UNKNOWN` and makes no claim about the nonlinear branch.

The outer interval matrix image may decorrelate parameters between polynomial terms and slabs. This only enlarges enclosures: every actual trajectory uses one matrix selected from the same full image on every slab. The label-image hash is therefore unchanged through the slab record. It is not a label resampling or a probabilistic model.

## Pose, contact, collision and task outputs

For each slab, with its full (u,r) range and the carried initial heading interval Θₖ,

\[
\Theta_k=\Theta_k^0+[0,h]R_k,\quad
\cos\Theta_k\subseteq[1-M_k^2/2,1],\quad
\sin\Theta_k\subseteq[-M_k,M_k],\quad M_k=\sup_{\theta\in\Theta_k}|\theta|.
\]

These are global inequalities and do not assume monotone sine/cosine. Then (u_k\cos\Theta_k) and (u_k\sin\Theta_k), multiplied by ([0,h]), enclose all partial-slab position changes and, multiplied by (h), enclose endpoint changes. Position and heading endpoints are chained slab-to-slab. The inflated obstacle radius is the task's entire stipulated circle radius.

The interval circle-box distance lower bound is the Euclidean norm of the coordinate gaps from the full-slab position box to the circle center. It is rounded downward; subtracting the fixed inflated radius yields the slab collision-margin lower bound. A negative or zero lower bound does not certify strict separation.

For contact, βⱼ≤ 1 implies

\[
\sqrt{C_j^2-F_j^2}=C_j\sqrt{1-s_j^2}
\ge C_{\min}\sqrt{1-\beta_j^2},\qquad
C_{\min}=9999/10000.
\]

The square root is computed by exact rational bisection and only its lower endpoint is used; no derivative at saturation is taken. The reserve lower bound is compared against the outward upper bound for the centripetal demand. For \(m=1\),

\[
|m u r|\le \sup|u|\sup|r|.
\]

A contact margin lower bound is the sum of the two reserve lower bounds minus this demand upper bound. A nonnegative value on every full slab is sufficient for the stipulated contact predicate.

For task progress, each slab bounds the integral increment by

\[
\Delta p_{x,k}=\int_{t_k}^{t_{k+1}}u(t)\cos\theta(t)\,dt
\in h\,\big(U_k\,[1-M_k^2/2,1]\big).
\]

Summing interval increments gives a lower bound on (p_x(2)-p_x(0)); initial (p_x) cancels. `task_eligible` requires replayed safety plus a lower bound at least (7/20) m. A positive alternative result with zero/nominal below that threshold is a certificate-level selector distinction; an `UNKNOWN` comparator is never interpreted as physically incapable or unsafe.

## Equation-to-code map and replay duties

| Obligation | Producer implementation | Independent replay |
|---|---|---|
| protocol, state/label widths, action voltage and fixed-label order | `producer.py::parse_protocol` | `checker.py::_read_and_validate` |
| signed motor/body/slip matrix and affine constant coordinate | `producer.py::build_augmented_matrix` | separately reconstructed in `checker.py::_assemble` |
| partial and endpoint Taylor terms and norm tail | `producer.py::exp_range` | separately implemented as `checker.py::_flow` |
| clip interior and first-exit obligation | `producer.py::evaluate` | `checker.py::_reconstruct` recomputes every slab |
| pose, circle distance, contact reserve and progress | `producer.py::evaluate` | independent inequalities in `checker.py::_reconstruct` |
| source, protocol, profile, record, fixed voltage, labels, slab count/order/chaining | `producer.py::evaluate_bound_row`; `run_stage.py` | `checker.py::audit` |
| resource stop and output integrity | `windows_job_supervisor.py`; `run_stage.py` | saved job/stdout/stderr/replay receipts; not inferred from a row status |

Producer and replay do not import each other's model/margin functions. They share `rational_interval.I`, `Budget`, `sqrt_lower`, Python `Fraction`, the task/protocol, and the recorded source/hash trust root. Thus the replay is structurally independent for model, Taylor loop and predicates, but it is not an independent arithmetic implementation.

## Expected applicability and limitations

This may help only where the full reachable normalized slips are strictly inside the identity branch and signed matrix propagation is materially tighter than a comparison-radius bound. It may fail at either clip corner, with broad labels or initial boxes, from dependency growth in the interval matrix powers, through pose/collision geometry, the contact reserve, or the task integral. It does not cover arbitrary known φ laws, time-varying labels, control switching within a hold, moving obstacles, tire/support mechanics, G3 recursive safety, physical-DDWMR measurements, or unmodeled hardware.

Generic validated Taylor propagation, interval matrix exponentials, parameter augmentation and Picard inclusion are established tools. This package tests a narrow DDWMR-specific signed affine effect; no novelty claim is made absent the G4 primary-source audit. Scientific outcome depends on actual per-action full-domain replay and G4's overlap analysis.
