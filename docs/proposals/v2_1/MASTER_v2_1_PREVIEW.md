> PENDING PROPOSAL - NOT AUTHORITATIVE. This preview is generated from the pending patch; its declared v2.1 is not adopted. The authoritative MASTER remains v2. Do not use this draft for derivation or implementation before reviewed acceptance.

# MASTER RESEARCH CONTEXT v2.1
## Actuator- and Contact-Aware Inter-Sample Safety for Differential-Drive Robots

**Status:** HOLD — theoretical formulation under review  
**Version scope:** Declared v2.1; the canonical filename remains `MASTER_RESEARCH_CONTEXT_v2.md` for stable links. Adoption records belong in DECISION_LOG. A draft preview outside research_context has no authority.

**Authority:** This file is the current single source of truth. If any previous chat, handoff, note, or model output conflicts with this document, this document takes precedence unless explicitly superseded by a later version.

---

# 0. OPERATING INSTRUCTIONS FOR CODEX

Do not treat agreement between language models as mathematical evidence.

Do not freeze a controller or implementation before the theoretical gates listed in this document are satisfied.

Do not silently repair assumptions.

If an equation, physical assumption, certificate, or novelty claim fails, report the failure explicitly.

Separate:

1. physical plant validity;
2. mathematical certificate validity;
3. recursive safety;
4. implementation;
5. empirical evidence;
6. novelty relative to literature.

Do not conflate them.

The next execution model/Luna may implement artifacts and code only after the research formulation passes the stated gate.

---

# 1. CURRENT RESEARCH QUESTION

The motivating physical question remains: when can digitally commanded collision safety be realized through voltage-limited motor, wheel, body and contact dynamics?

The first proposed theorem scope is narrower: a nine-state ideal planar constrained-contact DDWMR, with fixed unknown physical parameters, a known longitudinal traction shape, and an ideal four-quadrant terminal-voltage source. The aim is continuous collision safety **and preservation of algebraic contact admissibility** under fixed-period voltage ZOH.

The ideal contact model is not a validated constitutive tire law. Transfer to an actual platform requires explicit support/load/contact and actuation justification or a certified model-error extension. This physical correspondence remains an open G1 obligation. Formal safety of the ideal plant alone does not establish complete hardware feasibility.

---

# 2. CURRENT WORKING TITLE

Current candidate:

**Actuator- and Contact-Aware Inter-Sample Collision Safety for Differential-Drive Robots under Voltage Limits and Uncertain Longitudinal Traction**

This title is not permanently frozen.

Do not put HOCBF in the title unless HOCBF eventually becomes an essential original contribution.

---

# 3. CURRENT DECISION

**HOLD.** Proposed v2.1 assumptions define a candidate revised core, not a passed plant or implementation freeze. G1 NEEDS REVISION; G2/G3/G4 UNVERIFIED.

The candidate has nine physical dynamic states and two voltage inputs. Algebraic lateral reactions and fixed-parameter labels do not add physical dynamic states. The title, useful reachable enclosure, recursive safe subset and novelty remain unaccepted.

The v2.1 change from time-varying traction to parameters fixed for the entire execution is a deliberate scope narrowing. Earlier time-varying uncertainty targets are superseded for this core, not solved by it.

# 4. WHY THE PREVIOUS 7-STATE MODEL WAS NOT SELECTED

The seven-state pose/wheel/current model with an algebraic rolling-effectiveness relation cannot represent a body moving when its wheels have zero angular speed. The current candidate retains independent body longitudinal velocity and yaw rate.

Zero wheel speed with nonzero body speed is an admissible state, generally transient. The nine-state ODE does not introduce a separate sustained-lock mode or an automatic mechanical brake. Special trajectories may maintain zero wheel speed only if the existing torque and electrical equations permit it.

# 5. CANDIDATE 9-STATE PLANT AND COORDINATES

\[
x=[p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R]^\top,
\qquad V=[V_L,V_R]^\top.
\]

Body axes are forward/left/up; yaw is positive counterclockwise; positive wheel rate corresponds to forward rolling. `u` is body longitudinal speed, not voltage. `theta` is yaw; `vartheta` below is an unknown fixed physical parameter vector.

The planar COM projection coincides exactly with the drive-axle midpoint. `p` denotes this reference point. The contact projections relative to it are `(0,+b)` and `(0,-b)`. This is an ideal geometry equality, not “sufficiently close.” Nonzero offsets require revised equations or an explicitly justified error model.

`m` includes the translating assembly; `I_z` is its effective yaw inertia; `J_j` describes additional axial spin inertia of the wheel and consistently reflected rotor. Do not add no-slip-reflected translational inertia while also modeling body velocity and wheel rotation independently.

# 6. EXACT THEOREM KINEMATICS

\[
\dot p_x=u\cos\theta,\quad \dot p_y=u\sin\theta,\quad\dot\theta=r.
\]

The theorem imposes `v_y=0` exactly as an ideal lateral constraint. Approximate lateral grip is not an exact theorem assumption. Arbitrary lateral skid, lateral estimation error and finite COM-offset effects are excluded unless explicitly bounded in a coupled extension. A positional error margin alone does not bound the omitted coupling to body/yaw dynamics.

# 7. CONTACT KINEMATICS AND FORCE CONVENTIONS

\[
v_L=u-br,\quad v_R=u+br,
\]
\[
\sigma_L=R_w\omega_L-v_L,\quad\sigma_R=R_w\omega_R-v_R.
\]

`F_j` is the ground-on-wheel longitudinal contact force contributing to assembly translation. The identical force enters axial wheel dynamics with reaction torque `-R_w F_j`. Its yaw contribution is `b(F_R-F_L)`. The total contact contribution to body/wheel power is `-sum_j F_j sigma_j`.

# 8. LONGITUDINAL LAW AND IDEAL ALGEBRAIC LATERAL REACTIONS

## 8.1 Longitudinal law

\[
F_j(x,\vartheta)=\mu_j N_j\phi(\sigma_j/v_s),\qquad j=L,R.
\]

`N_L,N_R>0` are known fixed coefficients of the ideal planar model. Their correspondence to actual normal loads is governed by A3 below. Unknown `mu_j` belong to positive bounded intervals and remain constant for the entire trajectory.

The core uses one known fixed function phi satisfying

\[
\phi(0)=0,\quad z\phi(z)>0\ (z\ne0),\quad
|\phi(z)|\le1,\quad |\phi(z_1)-\phi(z_2)|\le L_\phi|z_1-z_2|.
\]

Additionally, `phi(-z)=-phi(z)` is adopted explicitly as a reversal-symmetry idealization. Oddness is not needed for the energy/enclosure definitions themselves. Global monotonicity and differentiability are not assumed. Any later theorem requiring them must say so. `tanh` is one eligible example, not a calibrated tire law or an implicitly mandatory realization.

Strict sign preservation excludes the v2 counterexample `phi=0` but does not guarantee finite stopping distance, a uniform braking force, or a voltage-admissible braking policy.

## 8.2 Algebraic lateral reaction model

The ideal constraint supplies algebraic reactions `Y_L,Y_R` satisfying

\[
Y_L+Y_R=mur,\qquad F_j^2+Y_j^2\le(\mu_jN_j)^2.
\]

This combined-force envelope uses the same coefficient as the longitudinal law by explicit modeling choice. It is an ideal constrained-force admissibility model, not isotropic Coulomb sliding or complete tire physics. No additional planar lateral forces or contact yaw moments are included. At the adopted projected geometry, the reactions add no yaw moment and do zero power under the exact lateral constraint. They do not enter the nine-state ODE and are not controller decision inputs.

For a fixed parameter realization let

\[
a_j(x,\vartheta)=\mu_jN_j\sqrt{1-\phi(\sigma_j/v_s)^2},
\quad A=a_L+a_R,
\]
\[
c(x,\vartheta)=A-|m u r|,\qquad
D_c(\vartheta)=\{x:c(x,\vartheta)\ge0\}.
\]

The lateral force allocation exists exactly when `c>=0`, under this stipulated envelope. One selection is `Y_j=(mur)a_j/A` for `A>0`, and `Y_j=0` if `A=0`, where admissibility requires `mur=0`. This selection establishes algebraic consistency, not physical validation or invariance of `D_c`.

All certified holds must preserve the relevant parameter-dependent domain. Outside it, this constrained contact model is invalid; do not project states back, assume an unmodeled skid mode, or extend the physical safety claim there. The square-root expression need not be Lipschitz at saturation; no later derivative/Lipschitz bound for this margin may be assumed without proof. The original algebraic inequalities remain an equivalent representation.

# 9. BODY DYNAMICS

\[
m\dot u=F_L+F_R-c_u u,\qquad
I_z\dot r=b(F_R-F_L)-c_r r.
\]

No additive disturbance or residual is active in this first core. Adding one requires an explicit versioned uncertainty-model change. Residuals cannot silently replace missing lateral/support physics.

# 10. WHEEL DYNAMICS AND SHAFT CONVENTION

\[
J_j\dot\omega_j=k_ji_j-B_j\omega_j-R_wF_j.
\]

Use effective wheel-side parameters for an ideal DC conversion with a specified ideal rigid bidirectionally backdrivable reduction `n_j=omega_motor/omega_wheel>0`; direct drive is `n_j=1`. In matched SI units,

\[
k_j=n_j k_j^m,\qquad J_j=J_{wheel,j}+n_j^2J_{motor,j},
\qquad B_j=B_{wheel,j}+n_j^2B_{motor,j}.
\]

The mechanical torque/current constant and electrical back-EMF/wheel-speed constant are the same effective `k_j`. Winding voltage/current/resistance/inductance retain their electrical meaning. Undeclared transmission loss, backlash, compliance and non-backdrivability are outside this ideal core.

# 11. ELECTRICAL DYNAMICS AND VOLTAGE SOURCE

\[
L_j\dot i_j=V_j-R_ji_j-k_j\omega_j,\qquad
\mathcal U=[-V_{max},V_{max}]^2.
\]

The source is an ideal bidirectional four-quadrant terminal-voltage drive. Both current signs and the necessary source/sink or dissipation of electrical power are permitted. `V=0` means the closed zero-terminal-voltage RL boundary condition; it is not open-circuit coast or a mechanical brake.

No current limiter, bus clipping, thermal protection, PWM ripple, open-circuit switching or driver delay modifies this theorem input. Any physical deployment requires justified operating limits or an explicitly revised plant/enclosure. Voltage-limited actuator dynamics do not imply complete hardware-driver feasibility.

For fixed parameters the energy

\[
E=\tfrac12 m u^2+\tfrac12 I_zr^2+
\sum_j(\tfrac12J_j\omega_j^2+\tfrac12L_ji_j^2)
\]

satisfies the algebraic consistency identity

\[
\dot E=\sum_jV_ji_j-c_uu^2-c_rr^2
-\sum_j(B_j\omega_j^2+R_ji_j^2+F_j\sigma_j).
\]

The ideal lateral reactions do no work. Thus `V=0` yields nonincreasing total energy, but not necessarily monotone body speed, a stopping rate or a safe emergency policy.

# 12. PHYSICAL ASSUMPTIONS AND FIXED UNCERTAINTY

## A1 — Ideal planar reduction

Roll, pitch and vertical dynamics are absent. This is a stipulated reduced model, not a proof that omitted force/moment balances are satisfied by a real robot.

## A2 — Exact planar geometry

The planar COM projection equals the axle midpoint exactly; use the sign and inertia conventions in §§5–7,10.

## A3 — Prescribed normal loads and open physical correspondence

`N_L,N_R>0` are known fixed coefficients of this ideal first core. This choice is not derived from a suspension/caster/roll/pitch model. It does not assert that any finite-height robot maintains these values during arbitrary motion. Actual vertical and moment balances, support reactions and the validity of neglecting load transfer require separate justification on a declared operating domain. No hidden ideal support moment, zero COM height or extra stabilizing contact is presumed.

In the diagnostic case of only two contacts `(0,±b,-H)`, finite COM height H, and no additional roll moment, zero roll acceleration requires `b(N_L-N_R)+Hmur=0`. Fixed equal loads would force `ur=0` in that diagnostic model. Actual supports can change this relation and must be identified. G1 physical correspondence remains open until this obligation is resolved or the scientific claim is explicitly limited and accepted. The ideal planar result alone cannot be advertised as validated tire/platform contact safety.

## A4 — Longitudinal slip and zero wheel speed

Longitudinal slip and transient `omega_j=0` with nonzero body speed are admitted. No independent wheel-lock mode is modeled or assumed available. Special ODE trajectories may maintain zero speed when torque balance and admissible held voltage allow it; this is not a guaranteed backup policy. No mechanical brake is silently added.

## A5 — Exact lateral constraint with bounded algebraic reactions

`v_y=0` exactly, with reactions and domain from §8. Arbitrary lateral skid and an approximate real-tire interpretation are outside the theorem. Every certified trajectory must stay contact-admissible for its true parameter realization, not merely at sample times.

## A6 — Known traction shape

Use the known fixed regularized law in §8. It is not an adversarial time-varying phi-family or a full tire model. Numerical physical validation requires identifying the selected function and its scale.

## A7 — Positive coefficients are not a braking guarantee

Positive friction/load bounds and strict sign-preserving phi do not imply a realizable minimum braking force. A stopping result requires a voltage-admissible policy, a proven reachable braking-slip regime, and explicit remaining-travel/low-speed analysis. No such result is currently established.

## A8 — Digital actuation

`V(t)=V_k` for `t in [kT,(k+1)T)`, with known fixed `T>0` and zero execution delay. Source conditions are those of §11.

## A9 — Uncertainty semantics

Let

\[
\vartheta=(m,I_z,R_w,b,v_s,c_u,c_r,J_L,J_R,B_L,B_R,
L_L,L_R,R_L,R_R,k_L,k_R,\mu_L,\mu_R)\in\Theta.
\]

`Theta` is a declared nonempty compact joint set. Every component is constant for the entire execution, including across successive holds. Known parameters are singleton components; uncertainty in every component is not required. Mass, inertias, inductances, resistances, radii, half-track, regularization speed, conversion constants and friction coefficients have positive lower bounds. Damping is nonnegative. Physical gear/conversion correlations must be preserved. Fixed known `N_L,N_R`, phi, `V_max` and T are not hidden decision variables.

Left/right friction may vary independently within their specified fixed intervals. Intervals need not be equal. Exchange symmetry is a separate optional condition on all known side data and the whole joint parameter set, not a default implication of independence.

This core excludes spatially/time-varying friction, parameter changes between holds, and additive disturbances. A differential inclusion allowing parameter switching is an outer relaxation, not the exact fixed-parameter plant. Preserve state/parameter dependence in reachability where possible. Parameters may be analytically appended with `dot vartheta=0`; this is not additional measured state or physical dynamics.

With these assumptions, fixed held voltage gives a locally Lipschitz vector field. The internal states have at most linear growth plus bounded contact forcing, and pose integrates body velocities. Solutions of the formal ODE exist uniquely on finite horizons. Such existence does not prove contact-domain preservation or physical correspondence; those obligations remain separate.

# 13. CONTROLLER INFORMATION

The theoretical core assumes exact knowledge of all nine states at each sample, zero sensing/computation/actuation delay, and only the known parameter set Theta for hidden quantities. The controller does not observe the true vartheta or select an action after learning it from an oracle. It need not measure contact forces or choose algebraic reaction allocations.

State estimates require a certified uncertainty set and one voltage valid for every compatible state. Delay requires an evolution enclosure during the delay. Neither extension is claimed here.

# 14. COLLISION AND CONTACT SETS

For a static circular obstacle,

\[
h(p)=\|p-p_o\|^2-R_s^2,\qquad\mathcal S=\{x:h(p)\ge0\}.
\]

`R_s` encloses obstacle radius and the complete robot footprint about the selected reference point, with any declared fixed clearance. State estimation error is not implicitly covered by this radius.

Keep the spaces distinct:

\[
\mathscr D_c=\{(x,\vartheta):\vartheta\in\Theta,\ x\in D_c(\vartheta)\},
\qquad \mathscr S_c=(\mathcal S\times\Theta)\cap\mathscr D_c,
\]
\[
\mathcal S_{rob}=\mathcal S\cap\bigcap_{\vartheta\in\Theta}D_c(\vartheta).
\]

The first two are joint state/parameter sets; `S_rob` is a state set. `x in S intersect mathscr D_c` is ill-typed. An existential projection onto favorable hidden parameters is not robust safety. These sets encode the stipulated planar contact constraints, not the unresolved real-platform support validation in A3. The whole geometric set S is not claimed invariant.

# 15. DISTINCT SAFETY OBJECTS

Let `x_vartheta(t;x,V)` be the formal ODE trajectory from x under a common held voltage V and fixed vartheta. A successful certificate must prevent leaving the parameter-specific contact domain.

## 15.1 Instantaneous certificate feasibility

For a chosen certificate Phi,

\[
\mathcal F_{inst}=\{x\in\mathcal S_{rob}:\exists V\in\mathcal U\ \forall\vartheta\in\Theta:
\Phi(x,V,\vartheta)\ge0\}.
\]

This definition provides no one-hold, recursive or exact viability guarantee on its own.

## 15.2 Joint reachable pairs and one-hold safety

\[
\mathscr R(t;x,V)=\{(x_\vartheta(t;x,V),\vartheta):\vartheta\in\Theta\},
\quad\mathscr R([0,T];x,V)=\bigcup_{t\in[0,T]}\mathscr R(t;x,V).
\]
\[
\mathcal F_T^c=\{x\in\mathcal S_{rob}:\exists V\in\mathcal U:
\mathscr R([0,T];x,V)\subseteq\mathscr S_c\}.
\]

This is one-hold safety/contact admissibility, not recursive feasibility.

## 15.3 State-only robust predecessor

For a state set `A subset S_rob`, define

\[
\operatorname{Pre}_T^c(A)=\left\{x\in\mathcal S_{rob}:\exists V\in\mathcal U\ \forall\vartheta\in\Theta:
\begin{array}{l}
x_\vartheta(t;x,V)\in\mathcal S\cap D_c(\vartheta),\quad\forall t\in[0,T],\\
x_\vartheta(T;x,V)\in A
\end{array}\right\}.
\]

The candidate recursive target is `K_T subset S_rob` with `K_T subset Pre_T^c(K_T)`. At each sample an admissible voltage must be selected using only the allowed information. This target rechecks the full parameter set at each endpoint, so it can be conservative relative to parameter-learning policies; it does not permit the true parameter to change along the physical trajectory. No useful K_T or policy has been constructed.

Only sampled-state membership in K_T and continuous membership in the collision/contact sets are intended. Do not call K_T continuously invariant without a corresponding held-input/clock theorem.

## 15.4 Exact fixed-parameter viability object

With Pi_T denoting nonanticipative sampled policies based on the allowed observed history, define conceptually

\[
\mathcal V_T^c=\{x\in\mathcal S_{rob}:\exists\pi\in\Pi_T\ \forall\vartheta\in\Theta\ \forall t\ge0:
x^{\pi,\vartheta}(t)\in\mathcal S\cap D_c(\vartheta)\}.
\]

A constructed K_T is only a certified inner approximation when the necessary policy and recursion result have been proved. It is not asserted equal to this object, to a switching-parameter viability set, or to the physical robot's full viability kernel. Failure of a sufficient certificate does not prove unavoidable collision.

# 16. ROBUST QUANTIFIERS AND REACTION VARIABLES

The held input must satisfy

\[
\exists V_k\in\mathcal U\quad\forall\vartheta\in\Theta\quad\forall t\in[0,T]
\]

for the appropriate collision/contact and endpoint conditions. Algebraic reactions may depend on the realized state/parameter because they are constraint forces, not voltages commanded by the controller. Their existence does not change the voltage quantifier to `forall vartheta exists V`. A single fixed true vartheta generates the entire executed trajectory.

For a joint outer enclosure require `mathscr Rhat([0,T]) subset mathscr S_c`. A state-only outer tube may instead satisfy `Rhat_x([0,T]) × Theta subset mathscr S_c`; this is sufficient but discards state/parameter correlations. The latter stronger condition must not be presented as equivalent to the exact joint one.

---

# 17. PREVIOUS HOCBF RELATIVE-DEGREE BLOCKER

For the previous 7-state electromechanical model, let

\[
h=q^\top q-R_s^2,
\]

\[
\rho=q^\top e,
\qquad
\eta=q^\top e_\perp,
\]

\[
v=a^\top w,
\qquad
r=b^\top w.
\]

Then:

\[
\dot h=2\rho v,
\]

\[
\ddot h
=
2v^2+2\eta rv+2\rho\dot v,
\]

\[
h^{(3)}
=
6v\dot v
-2\rho r^2v
+2\eta\dot r\,v
+4\eta r\dot v
+2\rho\ddot v.
\]

With

\[
\dot w=F(w,i),
\]

\[
L\dot i=V-Ri-K_ew,
\]

the voltage coefficient in \(h^{(3)}\) is

\[
2\rho a^\top F_iL^{-1}.
\]

Therefore it vanishes at:

\[
\rho=0.
\]

This prevents claiming a uniform relative degree 3 over the entire domain.

At \(\rho=0\), the input may reappear in the fourth derivative along the held-input flow.

However:

> this does not establish a regular relative-degree-four structure because the lower-order input coefficient does not vanish identically in a neighborhood.

Therefore the correct conclusion is:

\[
\boxed{
\text{state-dependent / singular relative-degree structure}.
}
\]

Do not state “relative degree becomes globally 4 at the singularity.”

---

# 18. PREVIOUS SLIP/HOCBF BLOCKER

If:

\[
v=a(s(t))^\top w,
\]

then:

\[
\dot v
=
a^\top\dot w
+
\dot a^\top w.
\]

Higher barrier derivatives require bounds on derivatives of \(s\).

Therefore:

\[
s(t)\in[\underline s,\bar s]
\]

alone is insufficient for a classical high-order derivative-based robust HOCBF derivation.

This was one reason HOCBF was removed as a mandatory core method.

---

# 19. STATUS OF HOCBF

HOCBF is an **optional candidate tool**, not frozen.

Potential roles:

1. baseline;
2. local regular-domain controller;
3. comparison to reachable-set safety;
4. literature bridge.

Do not build the novelty claim around:

> sampled-data HOCBF for DDWMR.

That landscape is already populated.

---

# 20. CANDIDATE THEORETICAL STRATEGY

The revised core is a fixed-parameter uncertain ODE `dot x=f(x,V;vartheta)`. Seek a plant-structured joint reachable enclosure with constant parameter labels. An analytical augmentation `dot vartheta=0` preserves this dependence. A switching-parameter differential inclusion is only an explicitly labeled outer relaxation.

No G2/G3 construction begins until the revised G1 assumptions and scope are explicitly resolved and adopted. The following are specification targets, not newly proved theorems.

# 21. WHAT MUST CARRY THE CONTRIBUTION

An outer enclosure contained in the safe/contact domain implies safety; a suitable predecessor recursion implies repeated safe holds. Those logical implications are generic and not novelty. Candidate novelty requires a certified, tractable and useful plant-specific enclosure or recursive-set construction that depends meaningfully on voltage and contact parameters. None exists yet.

# 22. TARGET 1 — JOINT REACHABLE ENCLOSURE

Seek a computable enclosure

\[
\mathscr R([0,T];x_k,V_k)\subseteq\widehat{\mathscr R}([0,T];x_k,V_k)
\]

for every fixed parameter realization in Theta under the same held V_k. It must preserve dependence or quantify conservatism from any relaxation. A pointwise simulated trajectory and a generic global Lipschitz ball alone do not establish a useful new construction.

# 23. TARGET 2 — COLLISION SAFETY AND IDEAL CONTACT ADMISSIBILITY

The required certificate is

\[
\widehat{\mathscr R}([0,T];x_k,V_k)\subseteq\mathscr S_c.
\]

For a proven enclosure, this gives `h(p(t))>=0` and `x(t) in D_c(vartheta)` for the true fixed parameter throughout the hold. It does not establish real-platform contact validity beyond the model assumptions. No inference is made from checking sampling endpoints alone.

# 24. TARGET 3 — USEFUL SAMPLED RECURSIVE SUBSET

Construct a useful `K_T subset S_rob` satisfying `K_T subset Pre_T^c(K_T)`, with admissible action selection under exact-state/hidden-parameter information. Assuming repeated feasibility does not solve this construction problem. Rest states alone may be nonempty but do not establish practical usefulness. The generic induction is not novelty, and no exact-viability equality is claimed.

# 25. STRUCTURED ENCLOSURE CANDIDATE

The wheel/current subsystem can be written schematically as

\[
\dot z_a=A(\vartheta)z_a+B(\vartheta)V+d_a(x,\vartheta),
\quad z_a=[\omega_L,\omega_R,i_L,i_R]^\top.
\]

Its contact forcing is coupled to the body and the same parameter realization. Matrix-exponential propagation may be useful, but no independent-box decomposition is sound or sufficiently tight merely by assertion. Propagate coupling to body velocities, heading and position, and certify both collision clearance and the parameter-dependent contact budget over the entire hold. Any derivative bound for the square-root contact margin requires separate regularity analysis. No tube algorithm is frozen.

# 26. AUXILIARY SYMMETRIC BRAKING SUBPROBLEM

A straight-line reduction is auxiliary only. It requires equal realized traction/load products (a sufficient restriction is `mu_L=mu_R`, `N_L=N_R`), matched motor/wheel parameters, symmetric wheel/current states and applied voltages, and initial `r=0`. Independent side uncertainty in the general model does not preserve that subspace.

Transient zero wheel rate does not supply a sustained locked-wheel policy. A braking result requires explicit actuator feasibility and a proof of the required slip history, including the near-zero-speed regime. A symmetric stopping bound cannot serve as the general independent-side-uncertainty recursive backup without an additional proof.

Mirror reflection exchanges side data, states and inputs. Symmetry of the same reachable problem additionally requires invariant known side data, an exchange-closed joint parameter set, and compatible initial/input sets or policy. Odd phi enables pure-spin antisymmetry only under the matched-side conditions. None of these symmetries is presumed for all realizations.

# 27. PROHIBITED CLAIMS

Do not claim:

- a seven-state relative-degree result for the nine-state plant;
- uniform global relative degree three, or a regular global degree-four structure at an isolated singularity;
- invariance of the entire geometric set S;
- instantaneous feasibility implies recursive safety;
- certificate infeasibility proves physically unavoidable collision;
- K_T equals exact viability;
- a state-only existential projection of the parameter-dependent contact domain is robustly safe;
- fixed-parameter safety covers changing terrain or time-varying friction;
- positive friction or strict-sign phi guarantees stopping distance;
- zero wheel rate supplies a persistent lock mode;
- algebraic force allocation validates a real tire law, normal-load balance, or full lateral-skid safety;
- an auxiliary symmetric model proves the general independent-side-uncertainty result;
- voltage feasibility is complete hardware-driver feasibility;
- unbounded state-estimation or timing error is covered;
- dense numerical simulation proves inter-sample safety;
- generic reachability/predecessor logic is novelty;
- moving-obstacle, multi-robot or variable-sampling theory;
- “first” or Q1 readiness without evidence and G4 review.

---

# 28. CURRENT NOVELTY BOUNDARY

Existing literature already contains combinations of:

- CBF/HOCBF;
- sampled-data CBF;
- robust sampled-data HOCBF;
- variable sampling;
- arbitrary/variable relative degree;
- zero-order CBF;
- segment/inter-sample safety;
- WMR obstacle avoidance;
- wheel-slip control;
- actuator saturation;
- contact-aware mobile-robot control;
- tube MPC.

Therefore novelty, if validated, must be narrower:

> **A tractable actuator- and contact-aware inter-sample safety certificate for a voltage-driven differential-drive robot that explicitly accounts for electromechanical dynamics, longitudinal traction uncertainty, and sampled recursive safety.**

This remains a hypothesis, not a verified claim.

---

# 29. LITERATURE THREATS THAT MUST REMAIN IN THE MATRIX

At minimum preserve the previously identified papers covering:

- Control Barrier Function Based Quadratic Programs for Safety Critical Systems;
- High-Order Control Barrier Functions;
- feasibility of CBF constraints under bounded control;
- Safety of Sampled-Data Systems with CBFs;
- robust sampled-data HOCBF;
- robust sampled-data robotic CBF/HOCBF;
- linear MPC + CBF for differential-drive robots;
- WMR CBF safety filters;
- WMR slip/traction control;
- actuator saturation;
- DDWMR actuator lag and sampled/event-based control;
- zero-order CBF;
- variable-sampling robust sampled-data HOCBF;
- segment-safe CBF;
- arbitrary/variable relative-degree discrete CBF;
- incorrect relative-degree CBF safety filters;
- contact-aware/friction-limited ground robot control.

The exact paper metadata should live in `LITERATURE_MATRIX.md`, not be duplicated throughout code.

---

# 30. REQUIRED LITERATURE MATRIX COLUMNS

For every close paper, record:

| Field | Meaning |
|---|---|
| Citation | full citation |
| DOI | primary identifier |
| Plant | robot/system |
| Input level | velocity / torque / voltage |
| Electrical dynamics | yes/no |
| Wheel rotational dynamics | yes/no |
| Body inertia | yes/no |
| Contact force | yes/no |
| Longitudinal slip | yes/no |
| Lateral slip | yes/no |
| Input saturation | yes/no |
| Sampling/ZOH | yes/no |
| Inter-sample guarantee | yes/no |
| Reachability/tube | yes/no |
| Recursive feasibility | yes/no |
| Viability claim | yes/no |
| CBF/HOCBF | yes/no |
| Hardware | yes/no |
| Exact contribution | concise |
| Overlap risk | concise |
| Full text verified | yes/no |

No novelty statement should be made without checking this matrix.

---

# 31. RESEARCH GATES

All gates remain open. A proposed/adopted revision is not a gate pass.

## G1 — Plant consistency and explicit physical scope

Review the complete nine-state ideal plant, force signs, power balance, geometry, algebraic reaction existence, fixed-parameter semantics, exact-state assumptions and driver boundary condition. Distinguish this mathematical consistency from physical platform correspondence. The support/load/contact justification in A3 remains unresolved; an accepted restricted scientific claim or justified physical extension is required before G1 acceptance. Provide parameter/function/drive provenance before quantitative physical claims. Diagnostic equilibria/symmetries and wheel-zero behavior must be checked under their actual assumptions.

## G2 — Certified enclosure

Construct an enclosure of all joint state/parameter trajectories for the entire hold and use the correctly typed collision/contact target. Preserve or explicitly relax parameter dependence. Dense numerical integration is not proof.

## G3 — Useful recursive subset

Construct a useful nonempty sampled-state K_T with the stated robust predecessor property and admissible non-oracle action selection. Do not present isolated rest states or assumed repeated feasibility as a practically useful construction.

## G4 — Novelty

Compare fixed-parameter constrained-contact models, force-admissible safety, robust reachability and recursive filtering at equation/theorem/computation level. Distinguish time-varying uncertainty, ideal normal loads and full tire physics. Existing matrix entries remain evidence-limited; unknown is not No. No first claim is accepted.

# 32. IMPLEMENTATION GATE

Overall **HOLD**. No controller, simulator, experiment or implementation code before explicit G1–G4 acceptance and a recorded `GO — implementation freeze of reviewed formulation` in MASTER and DECISION_LOG. Context documents and review proposals are permitted. No “exploratory implementation” exception is implied. A future G1 pass alone does not authorize implementation.

---

# 33. CODEX RESPONSE CONTRACT

For every research-review iteration, Codex should respond using:

## A. Finding

State the mathematical or physical result.

## B. Evidence

Show derivation/equation/source.

## C. Consequence

Explain what it changes in the research formulation.

## D. Status

Choose one:

- VALID;
- NEEDS REVISION;
- BLOCKER;
- UNVERIFIED.

## E. Required action

State exactly what needs to be derived, changed, or checked next.

Do not replace derivation with confidence language.

---

# 34. VERSION CONTROL RULE

Whenever a substantive decision changes:

1. update this master file;
2. increment version;
3. add a dated entry to `DECISION_LOG.md`;
4. update literature matrix if novelty changed;
5. mark old claims as superseded rather than silently deleting their history.

Example:

```text
v2.1
Decision: HOCBF removed as mandatory core.
Reason: nonuniform relative degree + slip differentiability issue.
Consequence: reachable-tube/predecessor formulation promoted to candidate core.
Status: HOLD.
```

---

# 35. CURRENT SUMMARY

Candidate: nine-state voltage-driven DDWMR with exact axle-COM geometry, exact ideal lateral constraint and algebraic force-budget admissibility. Known fixed traction shape; fixed unknown physical parameters for the whole execution; known fixed prescribed normal loads; ideal four-quadrant voltage ZOH; exact sampled state.

Target: continuous collision safety and preservation of the parameter-specific ideal contact domain, with a useful sampled recursive subset. Method candidate: structured joint state/parameter reachability. HOCBF remains optional/baseline.

Physical support/load/contact correspondence and all gate acceptances remain open. No enclosure, useful K_T, braking policy or novelty result has been established. **HOLD.**

---
