> HISTORICAL / SUPERSEDED BY MASTER v2 (2026-09-28). Read [MASTER_RESEARCH_CONTEXT_v2.md](../../research_context/MASTER_RESEARCH_CONTEXT_v2.md), DECISION_LOG, LITERATURE_MATRIX and REVIEW_GATE first. This note records earlier analysis, not the current nine-state plant or an implementation authorization. Seven-state results must not be transferred to the current plant without a new derivation.

# A tractable authority probe before general controller design

Status: proposed analytic subproblem, not an accepted full-robot theorem or an implementation specification.

## Purpose and restrictions

Use a symmetric, straight-line approach to one circular obstacle as a controlled subproblem. Fix the heading through the obstacle center, equal motor/wheel states and parameters, equal voltages, constant equal longitudinal transmission factor `kappa>0`, and no lateral slip. Let `r` be wheel radius and `J_eff` the mechanically justified effective inertia for this symmetric mode. Then body speed is `v=kappa*r*w`.

This is an invariant symmetry restriction only if the selected plant preserves it. Unequal disturbances invalidate that reduction. Failure of this maneuver cannot establish failure of all possible turning maneuvers of the planar robot.

## Exact electrical/mechanical hold response

For the linear symmetric subsystem, write `z=[w,i]^T`,

`zdot=A z+B V`,

`A=[-b_m/J_eff, K_t/J_eff; -K_e/L, -R/L]`, `B=[0,1/L]^T`.

Use wheel-equivalent motor constants, or explicitly include gearbox factors. These equations assume the effective load/friction model is valid over the maneuver.

For constant voltage, `z(t)=exp(A t)z0+Integral_0^t exp(A(t-s)) B V ds`.

Signed forward displacement from the initial position is

`D(t;z0,V)=kappa*r*[1,0] Integral_0^t z(s) ds`.

Let initial obstacle clearance along this ray be `d0=||p0-po||-R_s>0`. The sufficient one-hold safety condition is

`sup_(0<=t<=T) D(t;z0,V) <= d0`.

It explicitly retains initial current, inductance, voltage limit, mechanical inertia, and hold length. Endpoint displacement alone is insufficient when velocity changes sign. A certified maximum must include interior stationary points, parameter uncertainty, and numerical enclosure if later evaluated computationally.

The short-time expansion is

`D(t)=kappa*r*[w0*t + (-b_m*w0+K_t*i0)*t^2/(2J_eff) + ([1,0]A^2 z0 + K_t*V/(J_eff*L))*t^3/6] + O(t^4)`.

This demonstrates a concrete physical effect: voltage first affects displacement at order `t^3` in this reduced full-current plant, while initial current already affects order `t^2`. Two states with identical position, heading, wheel speeds, voltage bound, and sampling period can therefore have different avoidance authority because their currents differ. A universal boundary based only on speed and obstacle distance omits relevant state.

## Candidate backup certificate

Under positive physical constants and a stable `A`, a fixed admissible reverse voltage can be investigated as a simple backup maneuver. A bound on `sup_(t>=0)D(t;z0,V_backup)` would give a sufficient forward-excursion clearance for that backup, assuming the rearward ray has no obstacles and the symmetry/plant assumptions remain valid. A robust version needs a uniform bound over all allowed parameters/slip and the same voltage action for those realizations.

This is a constructive sufficient inner certificate. It is not the optimal stopping distance or exact viability boundary. In particular, motor dynamics are not automatically order-preserving in voltage because back EMF couples speed and current with a negative coefficient. Claiming maximum negative voltage is globally optimal requires proof.

## Decision value

This subproblem should establish whether retaining electrical dynamics creates a materially different, interpretable authority boundary in the relevant parameter range. It also provides a mathematically controlled future false-certification example. If its only effect is negligible at all realistic sample periods, the manuscript must explain why a full-current model matters, or rigorously reduce it and reassess novelty.
