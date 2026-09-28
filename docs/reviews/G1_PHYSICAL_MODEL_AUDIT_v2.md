# G1 physical model audit of MASTER v2

Date: 2026-09-28. Reviewer: Codex root. Reviewed baseline commit: `8ad80a20b5a58dafb135a89210cb8f990f3ccadf`.

Authority: `research_context/MASTER_RESEARCH_CONTEXT_v2.md` remains unchanged and authoritative. Every proposed MASTER edit below is **PENDING REVIEW**, not an adopted assumption. This audit derives identities from the nine-state candidate; it does not reuse the historical seven-state derivative audit. No implementation, simulation, or numerical test was performed. Overall **HOLD**; G1 **NEEDS REVISION**; G2–G4 **UNVERIFIED**.

The user relayed GPT's confirmation of the baseline context. That establishes shared context, not independent validation of the findings below. GitHub visibility was independently checked through `gh repo view`: PUBLIC. Documentation can be corrected without changing the formulation.

## Scope and notation

MASTER section numbers below refer to v2. Use body axes forward/left/up, positive yaw counterclockwise, and positive wheel rate for forward rolling. These coordinate conventions are proposed for explicit adoption. Write `e=(cos(theta),sin(theta))`, `e_perp=(-sin(theta),cos(theta))`. The symbol `u` always denotes body longitudinal velocity; voltage is `V`. Introduce `v_y` only for the audit of omitted lateral dynamics, not as a silently added tenth state.

All algebra below uses the residual-free equations in MASTER §§6–11. Any optional residual, gear loss, lateral-force law, or measurement uncertainty must be introduced through a reviewed revision. External sources support only the specifically attributed background facts; the DDWMR identities and counterexamples are derived here.

## F01 — Contact signs and mechanical power transfer

### Finding

The longitudinal contact velocities, yaw-torque signs, and wheel reaction torque are mutually consistent under explicit axle-midpoint geometry and the stated coordinate convention.

### Evidence

MASTER §§7,9,10. Contact locations relative to the planar COM are `(0,+b)` and `(0,-b)`. Rigid-body velocity gives

\[
v_L=u-br,\qquad v_R=u+br.
\]

The yaw moment of a forward force at lateral coordinate `y_j` is `-y_j F_j`, hence `b(F_R-F_L)`. Wheel/body powers associated with each longitudinal force sum to

\[
F_jv_j-R_wF_j\omega_j=-F_j\sigma_j\le0,
\]

because `sigma_j=R_w omega_j-v_j`, `mu_j N_j>=0`, `v_s>0` and `z phi(z)>=0`. For positive driving slip the force accelerates the body forward and opposes wheel spin; for negative slip the signs reverse. The same contact force must be used in both equations.

### Consequence

No contact-sign reversal is indicated. This verifies one part of the reduced planar mechanics, not the admissibility of lateral grip or any complete tire model.

### Status

VALID — conditional on the explicit coordinate and geometry conventions. Full G1 remains open.

### Required action

Proposed insertion before §7: “Body axes are forward/left/up, positive yaw is counterclockwise, and positive wheel rotation corresponds to forward rolling. Contact projections relative to the planar COM are `(0,+b)` and `(0,-b)`. `F_j` is the ground-on-wheel longitudinal force transmitted to the translating assembly. The identical `F_j` enters the wheel equation with torque `-R_w F_j`.” Geometry acceptance is subject to F04.

## F02 — Units and energy balance

### Finding

The equations admit a consistent dimensional and dissipative interpretation, but motor constants, parameter constancy, inertia accounting and damping signs must be specified before that interpretation is asserted.

### Evidence

MASTER §§8–11. Necessary units, with radians dimensionless:

| Quantity | SI unit |
|---|---|
| p, b, R_w | m |
| u, sigma, v_s | m/s |
| r, omega | 1/s |
| m; I_z, J_w | kg; kg m² |
| F, N | N |
| c_u | N s/m |
| c_r, B_w | N m s |
| K_t; K_e | N m/A; V s |
| R_j; L_j | ohm; H |
| mu, phi, L_phi | dimensionless |

For fixed parameters define

\[
E=\frac{1}{2}m u^2+\frac{1}{2}I_zr^2+
\sum_j\left(\tfrac12J_w\omega_j^2+\tfrac12L_ji_j^2\right).
\]

Multiplying the body, wheel and electrical equations by their respective velocities/currents and adding gives

\[
\dot E=\sum_jV_ji_j-c_uu^2-c_rr^2
-\sum_j(B_w\omega_j^2+R_ji_j^2+F_j\sigma_j)
+\sum_j(K_t-K_{ej})i_j\omega_j.\tag{G1-E}
\]

Thus the last term cancels for energy-consistent ideal motor conversion in matched SI coordinates. It has no guaranteed sign for independently chosen constants. If inertias or inductances vary in time, derivatives of stored-energy coefficients also enter; (G1-E) is then not the stated identity. The manufacturer's constant definitions support the SI conversion requirement, not arbitrary independent variation of torque and back-EMF constants. [maxon, “Motor data and simulation,” Constants](https://support.maxongroup.com/hc/en-us/articles/360013761160-Motor-data-and-simulation).

### Consequence

Independent motor-constant perturbations can break the intended physical conversion model. A nonincreasing energy at zero terminal voltage follows only after conversion consistency and nonnegative dissipation are established; it does not prove a stopping distance or convergence rate.

### Status

NEEDS REVISION — energy/passivity and physical parameter-mismatch claims remain conditional.

### Required action

Proposed addition to §§10–12: “Use fixed positive `m,I_z,J_w,L_j,R_j,R_w,b,v_s`; damping coefficients `c_u,c_r,B_w` are nonnegative. `m` includes the translating assembly, `I_z` its yaw inertia, and `J_w` the additional axial spin inertia per wheel including consistently reflected motor inertia. Do not double-count constrained rolling inertia in body and wheel coordinates. Motor conversion parameters obey the convention in F06. Parameter uncertainty preserves these physical relations.” Include the unit table and (G1-E) as a conditional consistency identity after that convention is accepted.

## F03 — Exact lateral constraint versus approximate lateral velocity

### Finding

MASTER §6 imposes an exact kinematic constraint; A5's approximate statement cannot by itself support that exact plant or a physical collision certificate.

### Evidence

For actual body lateral velocity `v_y`, COM kinematics and planar force balance are

\[
\dot p=u e+v_y e_\perp,\quad
m(\dot u-rv_y)=\sum F_x,\quad
m(\dot v_y+ru)=\sum F_y.
\]

Setting `v_y` identically zero produces the position equations in §6 and requires a net lateral reaction `m u r`. It does not set lateral acceleration or lateral force to zero. A bound `|v_y|<=epsilon_y` alone bounds the magnitude of the omitted direct velocity term; it does not bound all changes in `u,r,theta` caused by the missing dynamics. Therefore simply adding `epsilon_y T` to a position margin is not a complete enclosure proof for the actual coupled plant.

### Consequence

G2/G3 claims for the physical robot are blocked by the unresolved exact/approximate interpretation. Formal mathematical analysis of an explicitly ideal constrained plant remains possible, subject to F05.

### Status

BLOCKER — physical certification under approximate lateral grip.

### Required action

Proposed replacement of A5 for the minimal nine-state branch: “The theorem plant imposes `v_y(t)=0` exactly as an ideal lateral constraint on a declared validity domain `D`. Lateral reaction forces are present and must be admissible under the adopted contact model throughout every certified hold. Arbitrary lateral skid and unbounded lateral-model error are outside the theorem. An approximate physical realization requires an independently justified coupled model-error enclosure.” If this restriction is rejected, re-derive an expanded lateral/contact plant before G2; do not merely add a safety margin.

## F04 — COM/axle geometry is an equality assumption

### Finding

“Sufficiently close” in A2 leaves nonzero coupling terms unaccounted for. It also leaves the relationship between COM position and axle no-lateral-slip ambiguous.

### Evidence

Let COM be a longitudinal distance `a` ahead of the axle midpoint, with contact projections `(-a,+b)` and `(-a,-b)` relative to COM. Their lateral velocities equal `v_y-a r`. Axle lateral no-slip gives `v_y=a r`, whereas the current COM kinematics impose `v_y=0`. Both are compatible for turning only if `a=0`. With lateral forces `Y_j`, the COM yaw equation contains

\[
I_z\dot r=b(F_R-F_L)-a(Y_L+Y_R)-c_rr.
\]

The lateral reaction is no longer absent from yaw dynamics. A lateral COM offset would also alter the longitudinal-force lever arms. These are geometrically derived terms, not unspecified tuning errors.

### Consequence

The existing equations cannot certify an unspecified nonzero COM offset. The physical collision reference point must stay consistent with whichever geometry is chosen.

### Status

BLOCKER — physical claims for nonzero/unspecified offset and dependent G2/G3 derivations.

### Required action

Proposed replacement of A2: “The planar projection of the assembly COM coincides exactly with the axle midpoint. `p` denotes this point; the wheel contact projections are `(0,±b)`. `R_s` includes a footprint enclosure about this reference point. Finite COM height, load transfer and support reactions require the validity restrictions of A3/F05. Nonzero planar COM offset is excluded unless the resulting coupled equations and uncertainty bounds are explicitly re-derived.”

## F05 — Turning reaction and combined friction capacity

### Finding

The model requires a lateral reaction during curved motion but supplies neither a contact law for that reaction nor a certified operating domain where it is physically realizable. Separate longitudinal saturation is insufficient.

### Evidence

Under the exact geometry/constraint of F03–F04, without other planar lateral forces,

\[
Y_L+Y_R=mur.
\]

If a circular contact-force budget with coefficient `mu_j` is adopted as an additional assumption, each contact must satisfy `F_j^2+Y_j^2<=(mu_jN_j)^2`. For fixed `F_j,mu_j,N_j`, let

\[
a_j=\sqrt{(\mu_jN_j)^2-F_j^2}.
\]

Then there exist algebraic force allocations satisfying that budget and the lateral balance **if and only if**

\[
|mur|\le a_L+a_R.\tag{G1-L}
\]

This follows because the sum of intervals `[-a_L,a_L]+[-a_R,a_R]` is exactly `[-a_L-a_R,a_L+a_R]`. It is only a force-budget feasibility result for those added assumptions. It is not a constitutive tire-law result. MASTER's contact law would give `a_j=mu_j N_j sqrt(1-phi(sigma_j/v_s)^2)` if the same coefficient governs the combined budget. With both longitudinal forces saturated, nonzero `ur` fails this budget.

The friction-cone inequality alone does not define sliding-force direction. In an isotropic rigid Coulomb sliding model, tangential force opposes total slip velocity; at purely longitudinal nonzero slip, that model does not independently supply an arbitrary lateral reaction. A compliant tire/anisotropic contact or an explicit ideal-constraint approximation therefore needs its own justification. [Tedrake, “The (Coulomb) Friction Cone”](https://manipulation.csail.mit.edu/clutter.html) describes both the force budget and maximum-dissipation selection; (G1-L) is our derived conditional allocation check.

Normal loads also need a support model: no vertical acceleration requires all support normals, including any caster, to sum to `mg`; moments depend on geometry, COM height and acceleration. Two independently chosen drive-wheel load intervals do not establish these balances.

### Consequence

Turning safety and combined emergency steering/braking have no physical realizability certificate yet. Checking (G1-L) at sample instants alone would still not close this gap. Assuming the trajectory stays in the valid regime would be circular if preservation of that regime is not established.

### Status

BLOCKER — physical turning/contact-validity branch; downstream G2/G3 must enforce model validity as well as collision safety.

### Required action

Proposed addition to A3/A5: “Specify the support/contact model, admissible normal-load set and lateral reaction law or validated ideal-constraint approximation. Define a closed validity domain `D` with compatible load and combined-force bounds. Certificates require the complete uncertain hold trajectory to stay in `D` and the collision-free set. An algebraic friction-budget check such as (G1-L) is necessary under the adopted budget but does not validate a sliding constitutive law. Until these are supplied, physical turning and combined braking/steering claims are withheld.” This edit records the unresolved requirement; it does not itself resolve the physical contact-model choice.

## F06 — Motor/gear conventions

### Finding

The terminal-voltage equations need a common wheel-side or motor-side convention. An unspecified gearbox can alter torque authority, back EMF, inertia and braking behavior.

### Evidence

MASTER uses wheel rate in both mechanical and electrical equations. For an ideal fixed reduction `n=omega_motor/omega_wheel>0`, power conservation gives

\[
K_t^{w}=n k_t^{m},\quad K_e^{w}=n k_e^{m},\quad
J_w^{eq}=J_{wheel}+n^2J_{motor},\quad
B_w^{eq}=B_{wheel}+n^2B_{motor}.
\]

These formulas are direct transformations for a rigid, lossless reduction. Winding current, resistance and inductance remain motor electrical quantities. For an ideal DC conversion `k_t^m=k_e^m` in matched SI units, the wheel-side pair also matches. Real loss/backdrive effects need an explicit dissipative transmission model, especially when power changes direction. Manufacturer guidance documents generator operation and reduced backdrivability of some gearheads. [maxon, “Motors as Generators,” gear-motor combinations](https://support.maxongroup.com/hc/en-us/articles/360004496254-maxon-Motors-as-Generators).

### Consequence

Voltage-to-force and braking-authority results cannot use catalog constants without stating the reference shaft and electrical convention. Independent `K_t/K_e` uncertainty is not automatically physically admissible.

### Status

NEEDS REVISION — actuator authority and energy claims are conditional on the convention.

### Required action

Proposed insertion into §§10–11: “The core uses an ideal DC motor with direct drive (`n=1`) or a specified ideal, rigid, bidirectionally backdrivable reduction. `omega_j` is wheel speed; all mechanical spin parameters and conversion constants are expressed consistently at the wheel shaft using the transformations above. Electrical variables remain winding-terminal quantities. Transmission losses beyond the stated damping are excluded. A different drive/transmission requires explicit revised equations. For each motor, matched SI torque/back-EMF constants share the same uncertain physical conversion parameter.” Choose the actual drive convention and numerical provenance before G1 acceptance.

## F07 — The stated traction class does not guarantee braking authority

### Finding

Positive `mu_min` is insufficient for a positive braking-force lower bound, finite stopping time, or finite stopping distance over the entire admitted contact-law class.

### Evidence

MASTER §8 permits `phi(z)=0` for every `z`. This satisfies all four listed requirements, including Lipschitz continuity. With this law and `c_u=0`, the body equation is `dot u=0` regardless of voltage, current or wheel speed. A positive inward velocity can therefore persist even when `mu_min>0` and `N_j>0`. If `c_u>0`, `u(t)=u_0 exp(-c_u t/m)` in this counterexample: slowing is due to the assumed drag, not motor traction, and its remaining travel is `m u_0/c_u`.

More generally, a braking-force bound for a contact requires an actual negative slip domain and a lower envelope there, for example the **additional**, currently absent condition

\[
-\phi(-s/v_s)\ge\beta(s)>0\quad(s>0)
\]

on a stated range, together with `N_j>=N_min>0`. Even this gives no guarantee that bounded held voltage can reach or maintain that slip range. A lower envelope that tends too rapidly to zero near zero speed may also fail to yield a finite distance bound; stopping-time and remaining-travel properties require separate proofs.

### Consequence

A7 is a bound on a friction coefficient, not a guaranteed minimum braking action. Robust stopping-distance and braking-backup constructions are blocked. Generic reachability for a chosen dissipative law does not require this stronger authority assumption, but may yield an unhelpful safe subset.

### Status

BLOCKER — any motor-braking lower-bound/stopping-distance or braking-based G3 claim under the current broad phi class.

### Required action

Proposed replacement of A7 and insertion into §26: “`mu_min>0` is a positive coefficient bound only. Braking authority additionally requires positive contact-load bounds, an identified braking-region force lower envelope, and a voltage-admissible policy proven to generate the required slip from the admitted current/wheel/body states. No stopping-time or stopping-distance guarantee is inferred from the sign/Lipschitz conditions alone. These guarantees remain unproved until the chosen contact law and policy satisfy separate explicit conditions.” Selecting a stricter phi class would be a substantive revision requiring review, not an implicit consequence of v2.

## F08 — Zero wheel speed is not a sustained locked-wheel mode

### Finding

The nine-state ODE allows body motion at zero wheel speed, but contains no automatic wheel-lock constraint.

### Evidence

At `omega_j=0`, MASTER §10 gives

\[
J_w\dot\omega_j=K_t i_j-R_wF_j.
\]

For `u>0,r=0`, negative contact slip gives `F_j<=0`. With `i_j=0` and strict negative force, `dot omega_j>0`: the wheel is accelerated away from zero. Sustained zero speed requires

\[
i_j=R_wF_j/K_t.
\]

If `F_j` is differentiable and lock persists, §11 additionally requires

\[
V_j=\frac{R_w}{K_t}\big(L_j\dot F_j+R_jF_j\big),\tag{G1-W}
\]

which is generally time-varying rather than ZOH. For merely measurable friction with jumps, the required current could jump, whereas current is continuous under finite inductance and bounded terminal voltage. Thus (G1-W) cannot be assumed achievable. A mechanical brake would add a separate torque/mode not present in v2.

### Consequence

The motivational distinction from the seven-state model survives. A locked-wheel stopping calculation cannot be used as a physically admissible fallback without proving the lock-maintaining actuation or adding a reviewed brake model.

### Status

BLOCKER — downstream sustained-lock braking claims. The instantaneous zero-wheel-speed state remains admissible.

### Required action

Proposed replacement in §§7,12 A4,26: “States with zero wheel speed and nonzero body longitudinal speed are admitted. Zero wheel speed is generally transient. Sustained wheel lock is not assumed; it requires a separate admissible torque-balance/actuation proof or an explicitly modeled mechanical brake. No locked-wheel braking trajectory is treated as a realizable policy solely because `omega_j=0` is a valid state.”

## F09 — Uncertainty class and well-posedness

### Finding

The nine-state candidate can support measurable traction uncertainty without derivatives of friction, but the uncertainty class and fixed-parameter dependence must be made explicit.

### Evidence

Suppose, conditionally, positive inertias/inductances and geometry are fixed, voltage is bounded ZOH, `phi` is a fixed globally Lipschitz function, and `mu_j(t),N_j(t)` are bounded measurable nonnegative signals. Then `F_j(t,x)` is measurable in time and uniformly Lipschitz in `(u,r,omega_L,omega_R)`. The six internal body/wheel/current states have linear terms plus bounded contact forcing. A bound of the form `||dot z||<=a||z||+b` prevents finite-time escape of these states. Integrating yaw rate and body speed then prevents finite-time escape of pose on finite horizons. Local Lipschitz continuity in state with this growth bound gives a unique global absolutely continuous solution for each admitted signal on the ideal plant, with equations holding almost everywhere. This does not establish that the trajectory stays in a physical validity domain.

This argument fails if unmodeled state dependence in loads/friction destroys the stated regularity. It also does not justify differentiating friction. An unknown fixed motor parameter is not a freely switching time signal. A pointwise union/convexification can outer-bound fixed-parameter trajectories, but may include extra trajectories and lose parameter dependence; it must be labeled an overapproximation.

### Consequence

G2 has a plausible mathematical foundation after explicit assumptions, but no reachable enclosure has yet been constructed. Preserving constant parameter dependence matters for enclosure conservatism and any claimed exact reachability object.

### Status

NEEDS REVISION — G2/G3 proof assumptions not frozen.

### Required action

Proposed new subsection after §12: “Define a compact joint set P of fixed physical parameters, with positive lower bounds for inertias, inductances, resistances, radius and regularization speed, and the physical correlations stated above. Parameters in P remain fixed along each trajectory. Specify phi as known/fixed or an explicitly declared uniformly Lipschitz function family; a selected member does not change arbitrarily over time. Declare friction signals bounded and measurable. For the minimal core, normal loads are positive fixed values in a stated physically admissible joint set; any time-varying or state-dependent load extension requires its own regularity and support assumptions. Reachability quantifies over the same held voltage, all admitted signals and all fixed parameters. Pointwise relaxations are outer approximations. No friction derivatives are assumed.” The fixed-load choice is proposed and requires physical acceptance under F05.

## F10 — State information and admissible policy

### Finding

“Estimates or measurements” in §13 does not define the information available to the controller closely enough for a safety theorem.

### Evidence

The predecessor in §15 starts from a point `x`. If the true state is only known to lie in a set `X_k`, the implemented voltage must satisfy

\[
\exists V_k\in\mathcal U\quad
\forall x_k\in X_k\quad\forall\delta(\cdot)\in\Delta
\quad\forall\vartheta\in P:
\text{safe hold and required endpoint return}.
\]

Here `vartheta` denotes a fixed physical parameter realization, distinct from yaw `theta` and position `p`. Choosing a different voltage for each unobserved state or friction value changes the information pattern. Pose uncertainty directly changes clearance, and current/wheel-speed uncertainty changes immediately available torque. Sensor examples do not supply error bounds, timing alignment or delay compensation.

### Consequence

Implementable physical safety from estimated states and any claimed robust predecessor policy are blocked until an information assumption is selected. A theorem for exact full state is legitimate if its scope is explicit.

### Status

BLOCKER — estimated-state/real-sensor safety claims; exact-state candidate remains available for review.

### Required action

Proposed replacement of §13 for the minimal theoretical branch: “At each sampling instant the controller receives the exact nine-state vector, with zero sensing/computation/actuation delay. This is an ideal theorem assumption, not a sensor-performance claim. Hidden friction and uncertain fixed parameters are known only through their stated bounds; action selection cannot depend on their unknown realization. Estimated-state or delayed execution requires a certified initial-state set and delay evolution enclosure, with one held input valid for every compatible state and uncertainty. No such extension is presently claimed.”

## F11 — Equilibria and symmetry checks

### Finding

Rest equilibrium is admitted. Straight-line and pure-spin invariant subcases require stronger symmetry conditions than v2 currently states. Mirror symmetry and pure-spin antisymmetry have different requirements.

### Evidence

MASTER §§7–11, with positive conversion constants:

**Rest.** At `u=r=omega_L=omega_R=i_L=i_R=0` and `V=0`, every state derivative is zero for arbitrary fixed pose, because `phi(0)=0`. This proves existence of a rest equilibrium, not uniqueness of all equilibria.

**Steady internal motion.** Constant `u,r,omega,i` requires

\[
F_L=\tfrac12(c_u u-c_r r/b),\quad
F_R=\tfrac12(c_u u+c_r r/b),
\]
\[
i_j=(B_w\omega_j+R_wF_j)/K_t,\qquad
V_j=R_ji_j+K_{ej}\omega_j,
\]

together with the contact law and input bounds. Pose generally evolves, so this is a relative equilibrium of internal motion rather than a full-state equilibrium. Nonzero constant rolling with zero contact slip and positive body drag is incompatible with `phi(0)=0`: finite traction needs finite slip in this regularized law. That is a modeling feature needing calibration, not an algebraic sign error.

**Straight motion.** If left/right motor parameters, wheel states, currents, voltages and realized traction/load histories match, `r=0` is preserved and `theta` remains constant. Independent `mu_L,mu_R` uncertainty breaks this trajectory-level symmetry: at `r=0` with common nonzero slip,

\[
\dot r=b\,[\mu_RN_R-\mu_LN_L]\,\phi(\sigma/v_s)/I_z,
\]

which need not vanish. Equal uncertainty intervals do not imply equal uncertainty realizations.

**Mirror turning.** Reflect `(p_x,p_y,theta,r)` to `(p_x,-p_y,-theta,-r)` and swap left/right wheel states, currents, voltages, parameters and traction histories. `u` is unchanged. The equations transform into themselves. A mirrored trajectory is a solution for the correspondingly swapped environment; it is a symmetry of the same uncertainty family only when that family is closed under the swap. Oddness of phi is not needed for this reflection.

**Pure spin.** For `u=0`, `omega_R=-omega_L`, `i_R=-i_L`, `V_R=-V_L`, matched motor parameters and identical traction/load histories, the contact slips are opposite. Preserving `u=0` requires opposite forces, which follows if phi is odd. V2 does not assume oddness. A counterexample is `phi(z)=tanh(z)` for `z>=0`, and `phi(z)=0.5 tanh(z)` for `z<0`: it satisfies v2's bounds, sign condition and global Lipschitz property but is not odd, so opposite slips need not produce opposite forces.

### Consequence

The proposed straight-line braking subcase is not invariant under arbitrary independent left/right traction uncertainty. This is a BLOCKER for an unconditional robust straight-line reduction. Pure-spin symmetry is not established for the whole admitted phi class. Symmetry of a family of trajectories must not be confused with symmetry of each trajectory.

### Status

NEEDS REVISION — symmetry claims need the conditions explicitly stated; the affected robust reduction is stopped as above.

### Required action

Proposed additions to §§8,26,31: “State the rest and internal-motion balance equations above. Straight-line reductions require equal left/right realized traction/load histories and matched drive parameters, or an explicitly proven yaw-regulating policy; they are not robust reductions under independent side uncertainty. Mirror symmetry swaps the environment as well as states and inputs. Pure-spin antisymmetry additionally requires an odd contact law. Oddness is not inferred from the current sign/Lipschitz assumptions.” If a symmetric physical contact law is intended, explicitly propose and review `phi(-z)=-phi(z)` as an added model assumption.

## F12 — Voltage authority, driver operation and zero input

### Finding

An ideal signed terminal-voltage box does not fully specify a physical driver. Zero commanded terminal voltage has a particular circuit interpretation and is not automatically an open-circuit coast or a mechanical brake.

### Evidence

At `V_j=0`, the present circuit equation is

\[
L_j\dot i_j=-R_ji_j-K_{ej}\omega_j.
\]

For positive wheel speed and initially zero current, current initially becomes negative and produces electromagnetic braking under consistent conversion signs. An open circuit instead prevents that closed-path current and needs a different circuit mode. Existing stored current can initially produce driving torque even at `V=0`. Under F02's conditions total energy is nonincreasing, but body speed alone need not decrease monotonically as wheel/electrical energy is redistributed.

The command box also allows either sign of instantaneous electrical power `V_j i_j`, requiring a compatible source/sink or dissipation path. It imposes no separate current, thermal or driver-protection limit. Under an independently established wheel-speed bound `|omega_j|<=Omega` and constant positive motor parameters, a comparison gives

\[
|i_j(t)|\le |i_j(0)|e^{-R_jt/L_j}
+\frac{V_{max}+K_{ej}\Omega}{R_j}(1-e^{-R_jt/L_j}).
\]

This is a conditional current bound, not evidence that an actual driver can provide the allowed voltages or that its current limit exceeds the bound. PWM-average voltage is also an approximation to literal terminal-voltage ZOH unless the ripple is enclosed.

### Consequence

Voltage-only mathematical feasibility cannot yet be called complete actuator feasibility for hardware. Zero-input passivity does not supply an emergency-stop policy. G1 needs the intended driver scope; G2/G3 must respect any resulting operating limits.

### Status

NEEDS REVISION — physical actuator-execution claims are conditional; no hardware realization is verified.

### Required action

Proposed addition to §11/A8: “The theorem input is actual motor-terminal voltage supplied by an ideal bidirectional four-quadrant drive supporting both current directions and the required electrical-power exchange. It is exactly held for period T with zero delay. `V=0` denotes the closed terminal-voltage condition in the stated RL circuit, not an open circuit or a mechanical brake. No current limiting, bus clipping, thermal protection or PWM ripple alters the voltage within the declared validity domain. A physical implementation must justify that domain and these drive assumptions or include their effects explicitly in the plant/enclosure.” Keep physical implementation claims unverified until specifications and bounds exist.

## Gate consequences and review sequence

| Branch | Present finding | What is stopped |
|---|---|---|
| Longitudinal sign/power consistency | Conditional algebra verified in F01–F02 | No global plant acceptance follows |
| Exact nine-state ideal plant | F03/F04/F06/F09/F10/F12 require explicit choices | Freezing model/implementation |
| Physical turning and combined maneuvers | F05 BLOCKER | Claiming real contact-valid inter-sample safety |
| Robust braking authority and backup | F07/F08/F11 | Stopping-distance/locked-wheel/straight-line recursive backup claims |
| G2/G3 | Assumptions and construction unresolved | Declaring an enclosure or useful K_T proven |
| G4 | Not audited here | Any novelty closure or Q1 readiness claim |

Next review must decide: (1) exact axle-COM idealization; (2) actual lateral/contact validity model versus a revised plant; (3) phi class and braking authority assumptions; (4) drive/gear convention and operating limits; (5) fixed versus time-varying uncertainty and side correlations; (6) exact-state core versus bounded-error information. None is adopted in this file.

If the minimal nine-state route is accepted, the strongest unresolved issue remains F05: adding words such as “lateral grip holds” is not a constructive physical justification. A reviewed revision should either provide that justification and a certifiable domain, or change the model/scope explicitly. A straight-line-only result would be a narrower subproblem and also requires the side-correlation restriction from F11.

After independent equation-level review, accepted edits belong in a new declared MASTER version with a dated decision entry. G1 still needs a physically grounded parameter/drive specification and closure of its blockers. No GO is recommended by this audit.
