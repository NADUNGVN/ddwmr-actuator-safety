> HISTORICAL / SUPERSEDED BY MASTER v2 (2026-09-28). Read [MASTER_RESEARCH_CONTEXT_v2.md](../../research_context/MASTER_RESEARCH_CONTEXT_v2.md), DECISION_LOG, LITERATURE_MATRIX and REVIEW_GATE first. This note records earlier analysis, not the current nine-state plant or an implementation authorization. Seven-state results must not be transferred to the current plant without a new derivation.

# Independent mathematical review — preliminary

Date: 2026-09-28. Status: formulation freeze **HOLD**. These are analytic checks, not simulation results or claims of novelty.

## 1. A collision-free position set is not invariant for arbitrary actuator states

Let `q=p-p_o`, `e=(cos(theta),sin(theta))`, `rho=q^T e`, and body forward speed `v`. For the no-lateral-slip kinematics, `h=||q||^2-R_s^2` gives `hdot=2 rho v`. At a boundary state with `h=0` and `rho v<0`, this derivative is strictly negative and independent of instantaneous motor voltage. For a continuous velocity trajectory, sufficiently short positive times violate `h>=0`, whatever bounded voltage is selected. Thus Theorem A cannot assert invariance of all `{h>=0}` in the full electromechanical state space.

An HOCBF implication starts from an appropriate intersection of lower-order barrier sets. A recursively invariant certified subset requires a separate construction. Being outside that sufficient subset does not prove inevitable collision.

## 2. Exact local relative-degree calculation for a conditional seven-state model

Assume frozen longitudinal transmission factors, `v=a^T w`, `Omega=b^T w`, `wdot=F(w,i)`, and `L idot=u-Ri-K_e w`. Let `eta=q^T e_perp`. The kinematic identities are

`rhodot=v+eta Omega`, `etadot=-rho Omega`.

Consequently,

`hdot = 2 rho v`,

`hddot = 2v^2 + 2 eta Omega v + 2 rho vdot`,

`h''' = 6v vdot - 2rho Omega^2 v + 2eta Omegadot v + 4eta Omega vdot + 2rho vddot`.

Here `vdot=a^T F`, `Omegadot=b^T F`, and

`vddot=a^T[F_w F + F_i L^-1(u-Ri-K_e w)]`.

Hence `L_g h = L_g L_f h = 0`, and

`L_g L_f^2 h = 2 rho a^T F_i L^-1`.

The barrier has relative degree three on an open domain where this row is nonzero. If `rho=0`, the row vanishes. This is a real configuration: the heading is tangent to an obstacle-centered circle. A scalar barrier row normally has rank one, not rank two; rank loss here means rank one to zero. A nonzero higher derivative at an isolated singular point is not a uniform relative-degree-four neighborhood.

The same radial geometry can cause degeneracy even at a kinematic input level; motor order alone is not novel. A restricted domain must be explicitly reported and kept invariant if used for a theorem. Silently avoiding tangent states is unacceptable.

## 3. Slip assumptions change the mathematics and the physical claim

If `a=a(s(t))`, then `vdot=adot^T w+a^T F`, and `vddot=addot^T w+2adot^T F+a^T dF/dt`. Thus a magnitude bound on slip gives neither the first nor second derivative bound needed by this calculation. An inter-sample proof that differentiates `h'''` may demand a third slip derivative, beyond the assumptions needed just to define it. Unfiltered random resampling and Brownian paths do not satisfy classical smooth-slip assumptions automatically.

For a discontinuous slip transmission model, one must address jumps in `psi1,psi2`; concatenating smooth-interval HOCBF proofs without jump conditions is invalid. An alternative is a differential inclusion/reachable-tube proof that uses measurable bounded disturbances without differentiating them. That is a candidate reformulation requiring explicit acceptance, not a reason to silently change the implementation.

A wheel-speed-to-body-speed slip relation with an independently imposed motor load equation is a phenomenological model until ground-contact consistency is established. A traction model may need body velocity/yaw states and tire forces in addition to wheel speeds/current, so relative degree must be re-derived. A force-slip law depending on wheel speed can generically introduce another stage between voltage and position. Neither a universal seven-state plant nor degree three should be frozen now.

In particular, `v=(1-s)r*w` with a bounded transmission factor forces `v=0` when `w=0`. It cannot describe a locked wheel while the chassis continues sliding under braking. A proof for bounded longitudinal transmission loss must not be advertised as a proof for arbitrary braking skid. This distinction matters directly to any stopping-authority claim. Extending a conventional drive-slip ratio through wheel speed zero without an explicit definition can also introduce a singular model.

Inductance mismatch makes `g` uncertain. Use `g(X,Delta)` or state precisely which input-channel parameters are known. Reducing electrical dynamics by `L=0` changes the derivative order and needs a uniform safety error bound, including initial current transients, if the full plant is the claimed target.

## 4. Four different safety/feasibility objects

1. **Instantaneous certificate feasibility:** a common voltage satisfies all robust HOCBF inequalities at the current state (and lower-order initial conditions, if claiming safety implications).
2. **One-hold safety:** one constant admissible voltage keeps all possible physical trajectories collision-free over the next hold.
3. **Recursive certified invariance:** a certified subset admits a safe hold whose every endpoint returns to that subset, for all admissible uncertainty trajectories.
4. **Robust viability:** existence of a causal admissible policy for all future times under the defined information pattern and disturbances. It is relative to a model and execution class, not a property of `h` alone.

These objects are not interchangeable. An instantaneous sufficient certificate can be infeasible while safe controls exist. A one-hold-safe state need not admit a safe successor action. With partial state/slip observation, use an uncertainty or information set rather than an unrealistically known true state.

If a construction proves `flow([0,T]) subset C` and `flow(T) in S`, it establishes all-time collision safety and invariance of `S` at update instants. It does not by itself establish continuous-time invariance of `S`. Either use that more limited wording or augment the state with the hold clock/held input and construct the corresponding invariant tube.

For any robust action, the order is `exists u in U, for all admissible uncertainties`; selecting a separate optimal `u` for each unknown slip realization gives the controller information it does not have.

## 5. What voltage-box algebra actually proves

For a **known single** affine constraint `c+a_u^T u>=0` with `|u_j|<=Vmax`, feasibility is exactly

`c+Vmax ||a_u||_1>=0`.

If `a_u=0`, feasibility depends only on `c`. Otherwise a minimal nonnegative box half-width is `max(0,-c/||a_u||_1)` when the coefficients are independent of `Vmax`. This support-function identity is elementary, not a new theorem about DDWMR viability.

For multiple inequalities, individual feasibility is insufficient: `u_L>=1` and `u_L<=-1` each meet a box with `Vmax>=1`, but have no common solution. With uncertainty, `min_delta max_u` cannot replace `max_u min_delta`. Coefficients and sampling margins may depend on `Vmax`; an explicit formula cannot ignore that dependence. Robust nonlinear input-dependent margins also need not preserve a standard QP.

## 6. Physical monotonicity must be qualified

Increasing a voltage box preserves old admissible actions, so an exact existential safe set cannot shrink with more voltage authority. A conservative bound computed over all possible voltages can nevertheless get worse. Sampling-period monotonicity is straightforward for one-hold path safety (shorter prefixes of a safe hold are safe), but recursive sampled policies and terminal constraints need care; arbitrary periodic grids are not necessarily nested. Speed/distance monotonicity is plausible in a specified one-dimensional braking reduction, not established for all headings, currents, and turning states.

Stopping distance depends on initial current as well as speed when electrical dynamics are retained. A stopping certificate in a straight symmetric subsystem is sufficient for that maneuver; failure of straight braking is not impossibility of avoidance by turning.

## 7. Research acceptance conditions

- Choose and justify the plant/contact closure and controller observations.
- Resolve singularity without hiding excluded physical states.
- Declare a disturbance function class and derive uniform hold bounds on a reachable domain.
- Construct a nonempty invariant/backup subset; do not assume persistent QP feasibility as the main contribution.
- Compare equations/theorems with the closest existing work, including generic methods applied fairly to the same actuator plant.
- Define false certification as a model/execution mismatch. It is not a counterexample to an existing theorem whose hypotheses the real plant violates.
- Compare conservatism at comparable tracking progress and available information; stopping forever can improve collision statistics without a methodological contribution.

The working problem title can remain provisional. The subtitle promising HOCBF and input-feasibility guarantees should remain uncommitted until these conditions are met. Q1 ambition is a target, not a numerical result established by this review.
