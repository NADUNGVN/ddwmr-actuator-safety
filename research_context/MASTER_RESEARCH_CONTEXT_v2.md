# MASTER RESEARCH CONTEXT v2.1
## Inter-Sample Safety of a Reduced Voltage-Driven DDWMR with Uncertain Tangential Contact Capacity

**Status:** HOLD — theoretical formulation under review  
**Version scope:** Adopted research formulation v2.1; the canonical filename remains `MASTER_RESEARCH_CONTEXT_v2.md` for stable links. Adoption provenance is recorded in DECISION_LOG. Formulation adoption is not G1 acceptance or implementation authorization.

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

The motivating question is the gap between kinematic safety commands and finite actuator/contact authority. The first formal research question is: when can continuous collision safety be certified within a reduced electromechanical/contact DDWMR model that explicitly represents finite voltage-driven actuator dynamics and bounded modeled tangential contact authority?

The theoretical scope is a nine-state ideal planar constrained-contact DDWMR, with fixed unknown model parameters and per-wheel effective tangential capacities C_j, a known longitudinal traction shape, and an ideal four-quadrant terminal-voltage source. The aim is continuous collision safety **and preservation of algebraic contact admissibility** under fixed-period voltage ZOH.

The ideal contact model is not a validated constitutive tire law. G1 has accepted internal consistency for this restricted reduced-model scope; any transfer to an actual platform additionally requires support/load/contact and actuation justification or a certified model-error extension. Replacing literal normal loads with capacities does not establish that physical correspondence. Formal safety of the ideal plant alone does not establish complete hardware feasibility.

---

# 2. CURRENT WORKING TITLE

Scope-aligned working title:

**Inter-Sample Collision Safety for a Reduced Differential-Drive Robot Model under Voltage Limits and Uncertain Tangential Contact Capacity**

The title remains provisional. It denotes safety of a reduced model, not validated physical tire/support mechanics. Retaining or strengthening a physical robot claim requires separate evidence. HOCBF is optional/baseline and should not enter the title unless it becomes an essential original contribution.

---

# 3. CURRENT DECISION

**HOLD.** Version v2.1 is the adopted formulation for continuing research review. G1 PASS - restricted reduced-model scope; physical-platform correspondence UNVERIFIED; G2/G3/G4 UNVERIFIED; overall HOLD. Implementation remains unauthorized.

Current authorized phase (2026-09-29): G2 research only, following the user's "thực hiện" in response to the proposal to open G2. This authorizes analytic enclosure construction and review artifacts, not G2 acceptance. G3 construction and controller/simulator/experiment implementation remain unauthorized. The working candidate is `research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md`; it is supporting research under review and does not change this formulation or prove a gate pass.

Review evidence update (2026-09-29): the user relayed GPT's independent acceptance of Case A equations A.1--A.23 at commit `d2cd85407bb5ba4b4360836c49aa8a9c7ec83f28`. One finite rational synthetic one-hold certificate now exists; the earlier absence of any instantiated finite certificate is superseded. Evidence: `docs/reviews/GPT_G2_R2_d2cd854_ACCEPT_RECORD.md`. This accepts that exact hand case only, not a general certified evaluator, practical usefulness, physical correspondence, novelty or G2 PASS. The subsequent Case B addressed the synthetic actuator-parameter challenge; its accepted scope and the current next target are recorded below. Hidden parameters remain fixed; no model amendment or implementation authorization follows.

The formulation has nine physical dynamic states and two voltage inputs. Algebraic lateral reactions and fixed-parameter labels do not add physical dynamic states. The title is accepted as scope-aligned for G1 and remains provisional; no useful reachable enclosure, recursive safe subset or novelty result is established.

Further review evidence (2026-09-29): GPT accepted Case B B.1--B.25 at commit `1da2166949ad12a0741c876c3a0daf8a5d957ddf`, including parameter-dependent actuator matrices, preserved correlations, formal-model saturation exit and the strictly limited refined-CERTIFIED/coarse-UNKNOWN comparison of three locked evaluations. Record: `docs/reviews/GPT_G2_R3_1da2166_ACCEPT_RECORD.md`. Multiple synthetic finite hand cases now exist; general evaluation, practical usefulness, voltage-selection value, tractability and novelty remain unverified. G2 is not promoted.

Current challenge artifact: `research/theorem_notes/G2_VOLTAGE_SELECTION_CASE_C_v1.md`, submitted for independent review, compares two forward voltage levels plus zero under the same state, synthetic matched-side parameter family, shared error envelope and locked full-hold evaluation. Its claim concerns certificate outputs only. It does not establish unsafe alternatives, voltage necessity, n=1 necessity or practical usefulness. Exact matched sides are restrictions of this auxiliary case, not amended MASTER assumptions.

The v2.1 change from time-varying traction to parameters fixed for the entire execution is a deliberate scope narrowing. Earlier time-varying uncertainty targets are superseded for this core, not solved by it.

# 4. WHY THE PREVIOUS 7-STATE MODEL WAS NOT SELECTED

The seven-state pose/wheel/current model with an algebraic rolling-effectiveness relation cannot represent a body moving when its wheels have zero angular speed. The adopted formulation retains independent body longitudinal velocity and yaw rate.

Zero wheel speed with nonzero body speed is an admissible state, generally transient. The nine-state ODE does not introduce a separate sustained-lock mode or an automatic mechanical brake. Special trajectories may maintain zero wheel speed only if the existing torque and electrical equations permit it.

# 5. NINE-STATE PLANT AND COORDINATES

\[
x=[p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R]^\top,
\qquad V=[V_L,V_R]^\top.
\]

Body axes are forward/left/up; yaw is positive counterclockwise; positive wheel rate corresponds to forward rolling. `u` is body longitudinal speed, not voltage. `theta` is yaw; `vartheta` below is an unknown fixed model-parameter vector.

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
F_j(x,\vartheta)=C_j\phi(\sigma_j/v_s),\qquad j=L,R.
\]

Each C_j is an effective tangential contact-force capacity of the reduced planar model, measured in newtons:

\[
0<\underline C_j\le C_j\le\overline C_j<\infty.
\]

The capacities are unknown but fixed for the complete execution. They are not asserted to equal instantaneous physical friction-normal-load products. No mu_j or N_j is a parameter of the formal core. A physical mapping requires the separate evidence specified in A3.

The core uses one known fixed function phi satisfying

\[
\phi(0)=0,\quad z\phi(z)>0\ (z\ne0),\quad
|\phi(z)|\le1,\quad |\phi(z_1)-\phi(z_2)|\le L_\phi|z_1-z_2|.
\]

Global oddness, monotonicity and differentiability are not assumed. Any later theorem requiring them must state the additional assumption. Oddness is reserved for auxiliary reversal/pure-spin symmetry in §26. `tanh` is one eligible example, not a calibrated tire law or an implicitly mandatory realization. One selected phi is fixed and known; the controller does not face an arbitrarily switching unknown function family.

Strict sign preservation excludes the v2 counterexample `phi=0` but does not guarantee finite stopping distance, a uniform braking force, or a voltage-admissible braking policy.

## 8.2 Algebraic lateral reaction model

The ideal constraint supplies algebraic reactions `Y_L,Y_R` satisfying

\[
Y_L+Y_R=mur,\qquad F_j^2+Y_j^2\le C_j^2.
\]

The same capacity scales the longitudinal force law and limits the combined tangential force by explicit modeling choice. This is an ideal constrained-force admissibility model, not isotropic Coulomb sliding or complete tire physics. No additional planar lateral forces or contact yaw moments are included. At the adopted projected geometry, the reactions add no yaw moment and do zero power under the exact lateral constraint. They do not enter the nine-state ODE and are not controller decision inputs.

For a fixed parameter realization let

\[
a_j(x,\vartheta)=\sqrt{C_j^2-F_j(x,\vartheta)^2}
=C_j\sqrt{1-\phi(\sigma_j/v_s)^2},
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

## A3 — Effective capacities and reduced-model scope

C_j is an effective per-wheel tangential contact-force capacity in newtons. Literal normal forces N_j and friction coefficients mu_j are not formal core parameters. Mapping the effective capacities to physical support/contact quantities requires independent justification on a declared operating envelope. Calibration agreement alone does not provide a certified model-error bound. C_j fixed for the execution is not a theorem about physical normal-load constancy or load-transfer dynamics.

The capacity is both a force-law scale and an envelope radius. A lower bound on actual available force cannot simply be substituted as an exact C_j trajectory model: different capacities change body acceleration and wheel reaction, and no monotone ordering of collision safety is assumed. To transfer a theorem, establish that each actual trajectory lies in the modeled fixed-parameter family or in a sound model-error enclosure, and that the modeled constraint reactions are physically admissible. Renaming the parameter is not a proof of either fact and is not itself novelty. Physical correspondence remains unverified; the separate G1 acceptance covers internal consistency of the restricted reduced model only.

## A4 — Longitudinal slip and zero wheel speed

Longitudinal slip and transient `omega_j=0` with nonzero body speed are admitted. No independent wheel-lock mode is modeled or assumed available. Special ODE trajectories may maintain zero speed when torque balance and admissible held voltage allow it; this is not a guaranteed backup policy. No mechanical brake is silently added.

## A5 — Exact lateral constraint with bounded algebraic reactions

`v_y=0` exactly, with reactions and domain from §8. Arbitrary lateral skid and an approximate real-tire interpretation are outside the theorem. Every certified trajectory must stay contact-admissible for its true parameter realization, not merely at sample times.

## A6 — Known traction shape

Use the known fixed regularized law in §8. It is not an adversarial time-varying phi-family or a full tire model. Numerical physical validation requires identifying the selected function and its scale.

## A7 — Positive coefficients are not a braking guarantee

Positive capacity bounds and strict sign-preserving phi do not imply a realizable minimum braking force. A stopping result requires a voltage-admissible policy, a proven reachable braking-slip regime, preservation of the contact-validity domain, and explicit remaining-travel/low-speed analysis. No such result is currently established.

## A8 — Digital actuation

`V(t)=V_k` for `t in [kT,(k+1)T)`, with known fixed `T>0` and zero execution delay. Source conditions are those of §11.

## A9 — Uncertainty semantics

Let

\[
\vartheta=(m,I_z,R_w,b,v_s,c_u,c_r,J_L,J_R,B_L,B_R,
L_L,L_R,R_L,R_R,k_L,k_R,C_L,C_R)\in\Theta.
\]

`Theta` is a declared nonempty compact joint set. Every component is constant for the entire execution, including across successive holds. Known parameters are singleton components; uncertainty in every component is not required. Mass, inertias, inductances, resistances, radii, half-track, regularization speed, conversion constants and capacities have positive lower bounds. Damping is nonnegative. Physical gear/conversion correlations must be preserved. Fixed known phi, `V_max` and T are not hidden decision variables. C_j, F_j, Y_j and a_j have force units; phi is dimensionless.

Left/right capacities may have independently selected fixed realizations within their specified intervals. Intervals need not be equal. Exchange symmetry is a separate optional condition on all known side data and the whole joint parameter set, not a default implication of independence.

This core excludes time-varying capacities, spatially/time-varying traction, parameter changes between holds, and additive disturbances. A differential inclusion allowing parameter switching is an outer relaxation, not the exact fixed-parameter plant. Preserve state/parameter dependence in reachability where possible. Parameters may be analytically appended with `dot vartheta=0`; this is not additional measured state or physical dynamics.

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

The unproved recursive target is `K_T subset S_rob` with `K_T subset Pre_T^c(K_T)`. At each sample an admissible voltage must be selected using only the allowed information. This target rechecks the full parameter set at each endpoint, so it can be conservative relative to parameter-learning policies; it does not permit the true parameter to change along the physical trajectory. No useful K_T or policy has been constructed.

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

HOCBF is an **optional tool under investigation**, not frozen.

Potential roles:

1. baseline;
2. local regular-domain controller;
3. comparison to reachable-set safety;
4. literature bridge.

Do not build the novelty claim around:

> sampled-data HOCBF for DDWMR.

That landscape is already populated.

---

# 20. THEORETICAL STRATEGY UNDER INVESTIGATION

The adopted core is a fixed-parameter uncertain ODE `dot x=f(x,V;vartheta)`. Seek a plant-structured joint reachable enclosure with constant parameter labels. An analytical augmentation `dot vartheta=0` preserves this dependence. A switching-parameter differential inclusion is only an explicitly labeled outer relaxation.

G1 has passed for the restricted reduced-model scope. G2 analytic research is authorized as recorded in section 3 and DECISION_LOG; G3 construction still requires separate explicit user authorization. The following are specification targets, not newly proved theorems.

# 21. WHAT MUST CARRY THE CONTRIBUTION

An outer enclosure contained in the safe/contact domain implies safety; a suitable predecessor recursion implies repeated safe holds. Those logical implications are generic and not novelty. Any novelty claim requires a certified, tractable and useful plant-specific enclosure or recursive-set construction that depends meaningfully on voltage and contact parameters. The G2 analytic framework and finite synthetic Cases A/B have passed independent equation review. A general useful computational construction and originality remain unverified; accepting these cases does not establish either.

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

# 25. STRUCTURED ENCLOSURE DIRECTION

The wheel/current subsystem can be written schematically as

\[
\dot z_a=A(\vartheta)z_a+B(\vartheta)V+d_a(x,\vartheta),
\quad z_a=[\omega_L,\omega_R,i_L,i_R]^\top.
\]

Its contact forcing is coupled to the body and the same parameter realization. Matrix-exponential propagation may be useful, but no independent-box decomposition is sound or sufficiently tight merely by assertion. Propagate coupling to body velocities, heading and position, and certify both collision clearance and the parameter-dependent contact budget over the entire hold. Any derivative bound for the square-root contact margin requires separate regularity analysis. No tube algorithm is frozen.

# 26. AUXILIARY SYMMETRIC BRAKING SUBPROBLEM

A straight-line reduction is auxiliary only. It requires equal realized capacities `C_L=C_R`, matched motor/wheel parameters, the same known phi and scale, symmetric wheel/current states and applied voltages, and initial `r=0`. Independent side uncertainty in the general model does not preserve that subspace. At equal nonzero slip, `dot r=(b/I_z)(C_R-C_L)phi(sigma/v_s)` generally does not vanish.

Transient zero wheel rate does not supply a sustained locked-wheel policy. A braking result requires explicit actuator feasibility and a proof of the required slip history, including the near-zero-speed regime. A symmetric stopping bound cannot serve as the general independent-side-uncertainty recursive backup without an additional proof.

Mirror reflection exchanges side data, states and inputs. Symmetry of the same reachable problem additionally requires invariant known side data, an exchange-closed joint parameter set, and compatible initial/input sets or policy; comparison of obstacle-constrained problems also transforms the obstacle/domain. Odd phi is an additional assumption only for auxiliary pure-spin/reversal antisymmetry under the corresponding matched-side conditions. It is not a core assumption. None of these symmetries is presumed for all realizations.

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
- positive capacity or strict-sign phi guarantees stopping distance;
- C_j is a proven instantaneous physical friction-normal-load product, or a conservative capacity substitution automatically encloses actual trajectories;
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

The literature register already identifies CBF/HOCBF, bounded-input feasibility, sampled-data and inter-sample safety, robot obstacle avoidance, robust reachability, constrained contact and tube-control threats. Their detailed coverage must be verified, not inferred from titles or unknown cells.

The narrowed contribution hypothesis is a tractable, certified and useful construction for inter-sample collision/contact admissibility in the reduced voltage-driven electromechanical DDWMR with execution-fixed unknown effective tangential capacities and sampled recursive safety. Joint parameter dependence and actuator/contact coupling must yield more than substituting a plant into generic reachability or predecessor logic.

Changing notation from mu_j N_j to C_j and removing unused phi assumptions are formulation corrections, not novelty. This model does not establish arbitrary changing-terrain safety, physical tire behavior or support/load transfer. The title and contribution remain provisional; no first claim is accepted.

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

G1 PASS - restricted reduced-model scope; physical-platform correspondence UNVERIFIED; G2/G3/G4 UNVERIFIED; overall HOLD. Formulation adoption and the subsequent G1 review are distinct decisions.

## G1 — Plant consistency and explicit physical scope

G1 PASS - restricted reduced-model scope. Independent review of authoritative commit `8341014eac52ea66fe38559d6e1baee92e8f9b96` is recorded in `docs/reviews/GPT_TO_CODEX_G1_REVIEW_8341014e_PASS.md`, checks G1-01 through G1-12. Acceptance covers internal consistency of geometry, force signs, units, energy, algebraic contact admissibility, ODE regularity, fixed uncertainty, information/driver conventions, and qualified equilibrium/symmetry/wheel-zero statements. Physical-platform correspondence in A3 remains UNVERIFIED; provide model-family inclusion or a certified model-error extension before hardware safety claims. No plant equations or assumptions are changed by this status update.

## G2 — Certified enclosure

Construct an enclosure of all joint state/parameter trajectories for the entire hold and use the correctly typed collision/contact target. Preserve or explicitly relax parameter dependence. Dense numerical integration is not proof.

## G3 — Useful recursive subset

Construct a useful nonempty sampled-state K_T with the stated robust predecessor property and admissible non-oracle action selection. Do not present isolated rest states or assumed repeated feasibility as a practically useful construction.

## G4 — Novelty

Compare fixed unknown contact capacities, voltage-level actuator models, reduced nonholonomic constrained models, force-admissible inter-sample safety, joint state/parameter reachability and recursive filtering at equation/theorem/computation level. Distinguish time-varying friction and full tire/support/load dynamics. Renaming mu_j N_j as C_j is not a mathematical contribution. Existing matrix entries remain evidence-limited; unknown is not No. No first claim is accepted.

# 32. IMPLEMENTATION GATE

Overall **HOLD**. No controller, simulator, experiment or implementation code before explicit G1–G4 acceptance and a recorded `GO — implementation freeze of reviewed formulation` in MASTER and DECISION_LOG. Context documents and review proposals are permitted. No “exploratory implementation” exception is implied. The restricted G1 pass itself authorizes no subsequent work. The separate user authorization in section 3 opens G2 analytic research only; G3 and implementation remain unauthorized.

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


---

# 35. CURRENT SUMMARY

Adopted formulation: reduced ideal planar nine-state voltage-driven DDWMR with exact axle-COM geometry, exact lateral constraint and algebraic tangential force-budget admissibility. Unknown fixed per-wheel capacities C_L,C_R and model parameters for the whole execution; one known fixed strictly sign-preserving bounded Lipschitz phi, without default oddness or monotonicity; ideal four-quadrant voltage ZOH; exact sampled state. No literal normal-load parameter is in the formal core.

Target: continuous collision safety and preservation of the parameter-specific ideal contact domain, with a useful sampled recursive subset. Method under investigation: structured joint state/parameter reachability. HOCBF remains optional/baseline.

G1 PASS - restricted reduced-model scope, on the independent review of authoritative v2.1. Physical tire/platform/support/load correspondence remains UNVERIFIED. G2/G3/G4 remain UNVERIFIED. An analytic G2 enclosure candidate with proofs is under independent review; no accepted enclosure, useful K_T, braking policy or novelty result is established. **HOLD.** G2 research only is authorized; G3 construction and implementation remain unauthorized.

---
