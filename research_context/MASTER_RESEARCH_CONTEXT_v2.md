# MASTER RESEARCH CONTEXT v2
## Actuator- and Contact-Aware Inter-Sample Safety for Differential-Drive Robots

**Status:** HOLD — theoretical formulation under review  
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

The research is no longer framed as:

> “Apply sampled-data HOCBF to a DDWMR.”

The current scientific question is:

> **When can collision safety commanded by a digital controller actually be realized by a voltage-limited differential-drive robot whose motor, wheel, body, and wheel-ground contact dynamics prevent instantaneous execution of the commanded motion?**

The research focuses on the distinction between:

\[
\text{mathematical safety command}
\]

and

\[
\text{physically realizable collision safety}.
\]

---

# 2. CURRENT WORKING TITLE

Current candidate:

**Actuator- and Contact-Aware Inter-Sample Collision Safety for Differential-Drive Robots under Voltage Limits and Uncertain Longitudinal Traction**

This title is not permanently frozen.

Do not put HOCBF in the title unless HOCBF eventually becomes an essential original contribution.

---

# 3. CURRENT DECISION

## HOLD

The research problem remains active.

The following are **not frozen**:

- safety controller;
- HOCBF formulation;
- reachable-tube algorithm;
- recursively safe set construction;
- final title;
- novelty claim.

The following is the current **candidate theoretical plant**:

\[
\boxed{
x=
[p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R]^\top
}
\]

with voltage inputs

\[
\boxed{
V=[V_L,V_R]^\top.
}
\]

---

# 4. WHY THE PREVIOUS 7-STATE MODEL WAS NOT SELECTED

Previous candidate:

\[
[p_x,p_y,\theta,\omega_L,\omega_R,i_L,i_R].
\]

With a kinematic effectiveness relation such as

\[
v=\kappa R_w\omega,
\]

wheel lock gives

\[
\omega=0
\Rightarrow
v=0.
\]

This cannot represent continued body motion after wheel lock.

Therefore the 7-state model is valid only for a restricted rolling/transmission uncertainty regime.

It is insufficient if the scientific question concerns physical braking authority or longitudinal skidding during emergency safety action.

The new model therefore introduces explicit body longitudinal velocity and yaw rate.

---

# 5. CANDIDATE 9-STATE PLANT

## 5.1 State

\[
x=
[p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R]^\top.
\]

where:

- \(p_x,p_y\): body COM position;
- \(\theta\): yaw angle;
- \(u\): body longitudinal velocity;
- \(r\): body yaw rate;
- \(\omega_L,\omega_R\): wheel angular velocities;
- \(i_L,i_R\): motor currents.

---

# 6. BODY KINEMATICS

Assume no lateral body velocity in the theoretical core:

\[
\dot p_x=u\cos\theta,
\]

\[
\dot p_y=u\sin\theta,
\]

\[
\dot\theta=r.
\]

This is a deliberate modeling restriction.

The core theory does **not** cover arbitrary lateral skidding.

---

# 7. WHEEL-CONTACT KINEMATICS

Let \(b\) be half-track width.

Longitudinal ground velocities at the left and right contact locations:

\[
v_L=u-br,
\]

\[
v_R=u+br.
\]

Define longitudinal slip velocities:

\[
\sigma_L
=
R_w\omega_L-(u-br),
\]

\[
\sigma_R
=
R_w\omega_R-(u+br).
\]

This formulation permits:

\[
\omega_L=\omega_R=0,
\qquad
u>0,
\]

so the body may continue moving after the wheels lock.

---

# 8. LONGITUDINAL CONTACT FORCE MODEL

Candidate generic traction law:

\[
F_j
=
\mu_j N_j
\phi
\left(
\frac{\sigma_j}{v_s}
\right),
\qquad
j\in\{L,R\}.
\]

Assume:

\[
\mu_j
\in
[\underline\mu_j,\bar\mu_j].
\]

The regularizing function \(\phi\) satisfies:

\[
\phi(0)=0,
\]

\[
z\phi(z)\ge0,
\]

\[
|\phi(z)|\le1,
\]

and is Lipschitz:

\[
|\phi(z_1)-\phi(z_2)|
\le
L_\phi|z_1-z_2|.
\]

A numerical realization may use, for example,

\[
\phi(z)=\tanh z,
\]

but the theorem should not depend specifically on `tanh` unless mathematically necessary.

This is a **regularized longitudinal traction model**.

Do not call it a complete tire model.

---

# 9. BODY DYNAMICS

Candidate longitudinal rigid-body dynamics:

\[
m\dot u
=
F_L+F_R-c_u u,
\]

\[
I_z\dot r
=
b(F_R-F_L)-c_r r.
\]

Optional bounded residuals may later be added:

\[
m\dot u
=
F_L+F_R-c_u u+d_u,
\]

\[
I_z\dot r
=
b(F_R-F_L)-c_r r+d_r.
\]

If used:

\[
|d_u|\le\bar d_u,
\qquad
|d_r|\le\bar d_r.
\]

These residuals are not a substitute for missing contact physics.

---

# 10. WHEEL DYNAMICS

Contact force reaction must appear in wheel dynamics:

\[
J_w\dot\omega_L
=
K_t i_L
-
B_w\omega_L
-
R_wF_L,
\]

\[
J_w\dot\omega_R
=
K_t i_R
-
B_w\omega_R
-
R_wF_R.
\]

This closes the wheel/contact/body interaction.

---

# 11. MOTOR ELECTRICAL DYNAMICS

\[
L_L\dot i_L
=
V_L-R_Li_L-K_{eL}\omega_L,
\]

\[
L_R\dot i_R
=
V_R-R_Ri_R-K_{eR}\omega_R.
\]

Voltage constraints:

\[
|V_L|\le V_{\max},
\]

\[
|V_R|\le V_{\max}.
\]

Therefore the physical actuation chain is

\[
\boxed{
V
\rightarrow i
\rightarrow \omega
\rightarrow \sigma
\rightarrow F
\rightarrow (u,r)
\rightarrow (p,\theta).
}
\]

---

# 12. PHYSICAL ASSUMPTIONS

The theoretical core currently assumes:

### A1 — Planar motion

No roll/pitch dynamics.

### A2 — COM geometry

COM is sufficiently close to the axle midpoint for the selected rigid-body model.

If this is relaxed, coupling terms must be re-derived.

### A3 — Normal force

\(N_L,N_R\) are known or belong to explicit bounded sets.

No dynamic load transfer in the core model.

### A4 — Longitudinal slip

Longitudinal slip and wheel lock may occur.

### A5 — Lateral grip

The body remains in an operating regime where

\[
v_{\text{body},y}\approx0.
\]

The theory does not claim safety under arbitrary lateral skidding.

### A6 — Contact law

The regularized traction relation is an engineering model, not full contact/tire physics.

### A7 — Minimum traction authority

A positive lower traction bound is required:

\[
\underline\mu_j>0.
\]

If

\[
\underline\mu_j=0,
\]

a worst-case robust braking guarantee may become impossible.

### A8 — Digital actuation

Voltage is zero-order held:

\[
V(t)=V_k,
\qquad
t\in[kT,(k+1)T).
\]

---

# 13. CONTROLLER INFORMATION ASSUMPTIONS

At sampling instant \(kT\), the controller may use estimates or measurements of:

\[
p_x,p_y,\theta,
\]

\[
u,r,
\]

\[
\omega_L,\omega_R,
\]

\[
i_L,i_R.
\]

Possible sensors:

- localization for pose;
- IMU/body velocity estimator;
- wheel encoders;
- motor current sensing.

The theoretical core does not initially include an observer.

The controller is assumed to know bounds such as:

\[
\mu_j\in[\underline\mu_j,\bar\mu_j].
\]

It does not need to measure \(F_L,F_R\) directly.

---

# 14. COLLISION SAFE SET

For one static circular obstacle centered at \(p_o\):

\[
h(p)
=
\|p-p_o\|^2-R_s^2.
\]

Define:

\[
\boxed{
\mathcal S
=
\{x:h(p)\ge0\}.
}
\]

The entire set \(\mathcal S\) is **not expected to be invariant**.

For example, at the boundary with sufficiently large inward velocity, finite voltage cannot instantaneously prevent collision.

Therefore no theorem should claim:

> the whole geometric collision-free set is forward invariant.

---

# 15. IMPORTANT SET DEFINITIONS

These concepts must remain distinct.

## 15.1 Instantaneous certificate-feasible set

For a chosen certificate \(\Phi\):

\[
\mathcal F_{\mathrm{inst}}
=
\left\{
x:
\exists V\in\mathcal U
\;
\forall\delta\in\Delta:
\Phi(x,V,\delta)\ge0
\right\}.
\]

This means only that an admissible input satisfying the selected certificate exists **at the current instant**.

It is not automatically recursively feasible.

It is not automatically invariant.

It is not the viability kernel.

---

## 15.2 One-hold safe set

For a held voltage over period \(T\), define the robust reachable set

\[
\mathcal R(\tau;x,V).
\]

Then

\[
\boxed{
\mathcal F_T(\mathcal S)
=
\left\{
x\in\mathcal S:
\exists V\in\mathcal U,\;
\mathcal R([0,T];x,V)
\subseteq
\mathcal S
\right\}.
}
\]

This says there exists one held input preserving safety for one hold.

It does not guarantee feasibility at the next sample.

---

## 15.3 Sampled-state recursively safe subset

Define robust predecessor:

\[
\operatorname{Pre}_T(A)
=
\left\{
x\in\mathcal S:
\exists V\in\mathcal U:
\begin{array}{l}
\mathcal R([0,T];x,V)\subseteq\mathcal S,\\
\mathcal R(T;x,V)\subseteq A
\end{array}
\right\}.
\]

A certified sampled-state recursively safe set \(K_T\) should satisfy:

\[
\boxed{
K_T
\subseteq
\operatorname{Pre}_T(K_T).
}
\]

This yields:

\[
x(kT)\in K_T
\]

at sample instants and

\[
x(t)\in\mathcal S
\]

continuously between samples.

Do **not** call \(K_T\) continuously invariant unless the state is augmented with held input/clock and the corresponding theorem is proven.

---

## 15.4 Exact viability kernel

The exact robust viability object is conceptually:

\[
\operatorname{Viab}_{\Pi_T}(\mathcal S)
=
\left\{
x\in\mathcal S:
\exists\pi\in\Pi_T
\;
\forall\delta(\cdot):
x^{\pi,\delta}(t)\in\mathcal S,\;
\forall t\ge0
\right\}.
\]

A computed \(K_T\) is expected to be a **certified inner approximation**.

Do not claim:

\[
K_T=\operatorname{Viab}_{\Pi_T}(\mathcal S)
\]

without proof.

---

# 16. ROBUST QUANTIFIER ORDER

For a held digital input, the intended robust condition is:

\[
\boxed{
\exists V_k\in\mathcal U
\quad
\forall \delta(\cdot)\in\Delta.
}
\]

The same voltage must work for every admissible uncertainty trajectory during that hold.

Do not accidentally use:

\[
\forall \delta\;\exists V.
\]

Those are different problems.

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

# 20. CURRENT CANDIDATE THEORETICAL STRATEGY

Use robust reachable-set / reachable-tube reasoning.

Under held voltage:

\[
\dot x(t)
\in
\mathcal F(x(t),V_k),
\qquad
t\in[kT,(k+1)T).
\]

Construct an outer enclosure:

\[
\boxed{
\mathcal R(t;x_k,V_k)
\subseteq
\widehat{\mathcal R}(t;x_k,V_k).
}
\]

The enclosure must cover every admissible uncertainty trajectory under the **same** held voltage \(V_k\).

---

# 21. CORE TECHNICAL PROBLEM

The generic implication

\[
\widehat{\mathcal R}([0,T];x,V)
\subseteq\mathcal S
\]

implies one-hold safety.

That logic is generic and **not novelty**.

Similarly:

\[
K_T\subseteq\operatorname{Pre}_T(K_T)
\]

implies sampled recursive safety through induction.

That induction is generic and **not novelty**.

Potential novelty must lie in a plant-specific construction such as:

\[
\boxed{
\widehat{\mathcal R}_{\mathrm{DDWMR}}
}
\]

and/or:

\[
\boxed{
K_T^{\mathrm{actuator/contact}}
}
\]

that is:

- certified;
- computationally tractable;
- sufficiently nonconservative;
- explicitly dependent on voltage authority/contact uncertainty.

---

# 22. TARGET THEOREM 1 — REACHABLE ENCLOSURE

Under stated assumptions, derive a computable enclosure satisfying:

\[
\boxed{
\mathcal R([0,T];x_k,V_k)
\subseteq
\widehat{\mathcal R}([0,T];x_k,V_k)
}
\]

uniformly over:

\[
\mu_j(\cdot)\in
[\underline\mu_j,\bar\mu_j].
\]

The mathematical contribution should exploit the structure:

\[
V
\rightarrow i
\rightarrow\omega
\rightarrow F
\rightarrow(u,r)
\rightarrow p.
\]

A generic global Lipschitz ball will likely be too conservative and is not automatically a contribution.

---

# 23. TARGET THEOREM 2 — ONE-HOLD COLLISION SAFETY

If:

\[
\widehat{\mathcal R}([0,T];x_k,V_k)
\subseteq\mathcal S,
\]

then:

\[
h(p(t))\ge0
\]

for all:

\[
t\in[kT,(k+1)T].
\]

The implication itself is elementary.

Do not claim novelty for it.

---

# 24. TARGET THEOREM 3 — SAMPLED RECURSIVE SAFETY

Seek a nonempty \(K_T\subset\mathcal S\) satisfying:

\[
K_T
\subseteq
\operatorname{Pre}_T(K_T).
\]

If at every sample the controller selects an admissible voltage satisfying the robust predecessor condition, then:

\[
x(kT)\in K_T
\quad\forall k,
\]

and:

\[
x(t)\in\mathcal S
\quad
\forall t\ge0.
\]

Again, the induction is generic.

The difficult contribution is constructing a useful nonempty \(K_T\).

---

# 25. POSSIBLE PLANT-STRUCTURED TUBE STRATEGY

Partition:

\[
z_a=
[\omega_L,\omega_R,i_L,i_R]^\top.
\]

If the electromechanical part can be bounded using a linear or structured nonlinear subsystem:

\[
\dot z_a
=
A z_a+B V+d_a,
\]

then exploit:

\[
z_a(t)
=
e^{At}z_a(0)
+
\int_0^t
e^{A(t-\tau)}
B V\,d\tau
+
\text{uncertainty}.
\]

Then propagate bounds through contact dynamics to obtain:

\[
u(t)\in\mathcal U_b(t),
\]

\[
r(t)\in\mathcal R_b(t),
\]

\[
\theta(t)\in\Theta_b(t),
\]

\[
p(t)\in\mathcal P_b(t).
\]

A useful geometric condition could have the form:

\[
\|\hat p(t)-p_o\|
-
R_s
-
\varepsilon_p(t)
\ge0
\]

for every:

\[
t\in[0,T].
\]

The continuous interval minimum must be certified.

Do not substitute dense numerical simulation for a proof.

---

# 26. PHYSICAL BRAKING SUBCASE

The new model permits a straight-line braking subcase:

\[
r=0.
\]

Even if:

\[
\omega_L=\omega_R=0,
\]

the body may retain:

\[
u>0.
\]

Then contact forces may produce:

\[
m\dot u<0.
\]

A possible secondary theoretical result is a conservative robust stopping-distance expression:

\[
d_{\mathrm{stop}}^{\mathrm{rob}}
=
d_{\mathrm{stop}}^{\mathrm{rob}}
(x,T,V_{\max},\underline\mu,\ldots).
\]

Potential sufficient safety condition:

\[
d_{\mathrm{obs}}
>
d_{\mathrm{hold}}
+
d_{\mathrm{stop}}^{\mathrm{rob}}
+
d_{\mathrm{margin}}.
\]

This is not yet derived.

Do not claim it before proof.

---

# 27. CLAIMS THAT ARE CURRENTLY PROHIBITED

Do not claim:

- uniform relative degree 3;
- global relative degree 4 at tangent configurations;
- the whole geometric safe set is invariant;
- instantaneous QP feasibility implies recursive safety;
- QP infeasibility means collision is physically unavoidable;
- \(K_T\) equals the exact viability kernel;
- bounded slip amplitude is sufficient for arbitrary HOCBF derivatives;
- the 7-state model captures locked-wheel body sliding;
- the 9-state model is full tire/contact physics;
- full lateral skid robustness;
- moving-obstacle theory;
- multi-robot safety;
- variable-sampling novelty;
- generic reachability induction as a contribution;
- “first” without systematic verification.

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

# 31. NEXT RESEARCH GATE

Remain HOLD until the following four outputs exist.

## Gate G1 — Plant consistency

Provide a closed, dimensionally consistent 9-state model.

Verify:

- units;
- signs;
- wheel reaction forces;
- equilibrium behavior;
- straight-line symmetry;
- turning symmetry;
- locked-wheel behavior;
- zero-input behavior.

---

## Gate G2 — Certified reachable enclosure

Construct:

\[
\widehat{\mathcal R}
\]

or an equivalent certified state/position tube.

Must show mathematically:

\[
\mathcal R
\subseteq
\widehat{\mathcal R}.
\]

Numerical simulation alone does not pass this gate.

---

## Gate G3 — Nontrivial recursive safe subset

Construct a nonempty:

\[
K_T
\]

or another rigorously defined certified sampled-state set satisfying a recursive predecessor property.

If the set is empty or practically meaningless, report this rather than tuning around it.

---

## Gate G4 — Novelty audit

Update the close-paper matrix after the plant and theorem form are known.

The novelty question must be asked at the level of:

- system model;
- uncertainty model;
- safety object;
- theorem;
- computation.

Not merely keywords.

---

# 32. GO CONDITION

Only after G1–G4 are satisfied may the project switch from:

**HOLD**

to:

**GO — implementation freeze v2**

At that point Luna/execution model may implement:

- plant;
- validated integrator;
- reachable-tube algorithm;
- certified safety filter/policy;
- baselines;
- experiment harness;
- Monte Carlo;
- plots/tables.

Until then, implementation should remain exploratory only.

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

# 35. CURRENT BOTTOM LINE

Current candidate plant:

\[
\boxed{
[p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R].
}
\]

Current candidate uncertainty:

\[
\boxed{
\text{bounded uncertain longitudinal traction}.
}
\]

Current digital control structure:

\[
\boxed{
V(t)=V_k
\text{ under fixed-period ZOH}.
}
\]

Current safety objective:

\[
\boxed{
\text{continuous collision avoidance between samples}.
}
\]

Current long-horizon object:

\[
\boxed{
\text{sampled-state recursively safe certified subset}.
}
\]

Current candidate methodology:

\[
\boxed{
\text{plant-structured robust reachable tube / predecessor}.
}
\]

HOCBF:

\[
\boxed{
\text{candidate/baseline only}.
}
\]

Project status:

\[
\boxed{\text{HOLD}}.
\]