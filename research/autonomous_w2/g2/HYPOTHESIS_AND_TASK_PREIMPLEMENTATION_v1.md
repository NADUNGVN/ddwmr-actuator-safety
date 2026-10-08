Session: DDWMR | LUNA-G2-SCOPE

# W2 G2 — preimplementation hypothesis and task

**Version:** 1.0. **Declared:** 2026-10-07 UTC, before candidate implementation or query evaluation. **State:** frozen for development; not a confirmation lock. This is a synthetic design assumption, not a physical parameter or platform claim.

## 1. Candidate hypothesis

For the declared `phi(s)=clip(s,-1,1)` subclass, a whole-hold proof can be tighter than the R3 interval Picard plus positive comparison-radius path when the complete reachable tube stays strictly inside both clip corners. On that branch the six internal states

\[
z=(u,r,\omega_L,\omega_R,i_L,i_R)
\]

satisfy an affine linear ODE for each fixed parameter label:

\[
\dot z=A(\vartheta)z+B(\vartheta)V.
\]

The candidate uses **time-local variation of constants** on contiguous slabs,

\[
y(t_k+\tau)=\exp(\mathcal A(\vartheta,V)\tau)y(t_k),\quad
y=(z,1),\quad 0\le\tau\le h_k,
\]

with the signed wheel/current/body/slip coefficients of the full DDWMR matrix preserved in the matrix series. A rational Taylor sum and a rational series-tail bound enclose every partial-slab state and endpoint. One common fixed label cell and held voltage are reused on every slab; the interval image is an outward relaxation of the same fixed-label trajectories and is never reset to a favorable label. Pose, contact, collision and progress are checked on every full slab. This branch-specific inclusion avoids the R3 global absolute-value comparison radius only when its clip-interior premise is itself proved over the complete hold.

The inclusion is conditional on: (i) exact rational interval enclosure of the parameter-to-matrix map; (ii) strict full-hold slip inclusion in `(-1,1)` for both wheels, established by a first-exit argument against the same computed linear enclosure; (iii) validated matrix Taylor truncation and tail on every partial slab; (iv) contiguous endpoint carry with no state/label reset; and (v) outward full-slab pose, circle-distance, contact-reserve and progress bounds. At a clip corner, branch uncertainty, wide parameter cell, failed carry or arithmetic cap, the path must return `UNKNOWN`. It does not differentiate `clip` or the square-root reserve. This is not a theorem for arbitrary MASTER `phi`, arbitrary `Theta`, or physical tire/contact dynamics.

**Plant-specific effect to test:** in the interior branch, the finite interval matrix powers preserve the signed path from terminal voltage through winding current, wheel torque/back-EMF, slip force, body acceleration and the output integral. R3 bounds force defects and then passes them through a nonnegative comparison matrix, which drops off-diagonal signs. The candidate may therefore retain a decision-relevant input effect on a declared domain. Exact matrix exponentiation/Taylor validation, parameter augmentation and IVP inclusion are established generic tools; no novelty is claimed before G4's audit.

## 2. Task rule declared independently of certificate margins

Task assumption: a short one-hold forward approach command requests at least **0.35 m of world-`+x` displacement in 2.0 s**, equivalent to a mean forward displacement rate of 0.175 m/s. This is the formal task requirement; it is not inferred from an R22–R24 action-gap calculation, a tube radius, a collision margin or an observed certificate result. It is not a sourced hardware requirement.

The task is one complete nine-state initial box, one static circular obstacle whose radius includes the stipulated footprint, and three fixed symmetric terminal-voltage actions:

| Role | Held terminal voltage |
|---|---|
| zero | `(0,0) V` |
| nominal | `(1/2,1/2) V` |
| alternative | `(1,1) V` |

The nominal-preserving selector admits an action only when the same full-hold certificate proves collision clearance, parameter-specific contact admissibility and `J^- >= 7/20 m`, where

\[
J=p_x(T)-p_x(0)=\int_0^T u(t)\cos\theta(t)\,dt.
\]

It keeps the nominal action if eligible, else may select the alternative; the two simple comparators try only zero or only nominal. `UNKNOWN` means the sufficient test did not establish eligibility, never that an action is unsafe or physically unable to complete the task. A claimed decision advantage requires the alternative to replay as eligible while a comparator lacks an eligible action, with the result identified as a certificate-level task decision. An actual task-failure claim for a comparator would separately require a sound uniform upper bound below `7/20 m`.

## 3. Exact prospective development domain

All values are closed exact rationals in MASTER's state order `[p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R]`.

| State coordinate | Initial interval | Unit |
|---|---:|---|
| `p_x,p_y` | `[-1/100000, 1/100000]` | m |
| `theta` | `[-1/100000, 1/100000]` | rad |
| `u` | `[3/10, 3001/10000]` | m/s |
| `r` | `[0, 1/100000]` | rad/s |
| `omega_L,omega_R` | `[2499/10000, 1/4]` | rad/s |
| `i_L,i_R` | `[-1/100000, 1/100000]` | A |

Every state coordinate has positive width. The moving `u,r` intervals are a narrow development subcell of the existing R3 `S_HIGH_POS` synthetic family; wheel/current/pose intervals are narrowed subsets of its common state cell. Each of twelve execution-fixed labels `(rho_L,rho_R,C_L,C_R,lambda_L,lambda_R,R_L,R_R,B_L,B_R,k_L,k_R)` independently ranges over `[9999/10000,10001/10000]`. Thus every parameter interval has positive width. Maps are `J_j=1/rho_j`, `L_j=lambda_j`; fixed synthetic constants are `m=I_z=R_w=b=v_s=c_u=c_r=1`; the known law is `clip`; `V_max=1 V`. An ideal gear-consistency witness may use `n=10`, `k_m=k/10`, `J_w=1/10`, `J_m=(1/rho-1/10)/100`, `B_w=0`, `B_m=B/100`; it identifies no real component.

The static circle center is `(1/2,1/10) m` and the complete inflated radius is `R_s=3/50 m`. Hold duration is exactly `T=2 s`. The collision/contact predicates are the MASTER v2.1 full-hold predicates; contact reserve is evaluated directly and no square-root derivative is used. The complete task is one group with three rows, `W2_G2_DEV_001_ZERO`, `W2_G2_DEV_001_NOMINAL`, and `W2_G2_DEV_001_ALTERNATIVE`.

The domain is intentionally synthetic. The R3 `S_HIGH_POS` label is only provenance for a moving-state development subcell; the horizon, circle, voltage triple, narrowed state image, task requirement and W2 source are new. The W1/R5 800-row candidate remains 800/800 `NOT_RUN`.

## 4. Prospective criteria and limitations

For each of the three actions, report full-hold collision/contact status, lower safety margins, complete-slab internal/pose widths, branch slack to both clip corners, endpoint progress enclosure, execution/resource counts, and exact reason codes. The candidate task passes only if the alternative is `CERTIFIED` and its independently replayed lower progress is at least `7/20`; comparator eligibility is evaluated by the same checker and threshold. No threshold, obstacle, voltage or parameter interval will be moved in response to an outcome. The three rows are development evidence; G4 owns any fresh matched confirmation workload and its unused identities.

Potential failure modes were predeclared: (a) a strict clip-interior branch cannot be proved; (b) interval matrix powers widen over the 2 s hold; (c) endpoint/slab carry or pose range loses clearance; (d) the alternative fails progress; (e) the interval box is too small to support any usefulness claim; and (f) G4 determines that the method is generic prior-art application. Any such result is reported without retuning the frozen task.

No native query, solver, worker or evaluator was run before this document and the machine-readable task record were written. Analytic feasibility screening follows this preimplementation declaration. Any later development configuration must first bind the exact protocol, source closure and resource profile by hash. G4 confirmation outcomes will not be inspected in advance.
