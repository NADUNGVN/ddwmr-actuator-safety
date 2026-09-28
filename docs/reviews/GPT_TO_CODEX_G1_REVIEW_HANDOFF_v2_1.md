# GPT -> Codex G1 Independent Review Handoff v2.1

**Project:** DDWMR Actuator- and Contact-Aware Safety  
**Repository:** `NADUNGVN/ddwmr-actuator-safety`  
**Branch:** `main`  
**Codex G1 audit commit reviewed:** `5424c2b86837b95eece87726da7c2d7fdea0a7e2`  
**Codex audit file:** `docs/reviews/G1_PHYSICAL_MODEL_AUDIT_v2.md`  
**Authoritative research source:** `research_context/MASTER_RESEARCH_CONTEXT_v2.md`  
**Project state:** **HOLD**  
**Purpose of this document:** Independent GPT equation-level review of F01-F12 and a minimal, internally consistent revision proposal for the next MASTER. This document does **not** itself amend MASTER, pass G1, authorize GO, or authorize implementation.

---

## 0. Instructions to Codex

Read this handoff together with the repository files at the commit being reviewed:

1. `research_context/MASTER_RESEARCH_CONTEXT_v2.md`
2. `research_context/DECISION_LOG.md`
3. `research_context/LITERATURE_MATRIX.md`
4. `research_context/REVIEW_GATE.md`
5. `docs/reviews/G1_PHYSICAL_MODEL_AUDIT_v2.md`
6. `AGENTS.md`

MASTER remains authoritative until a reviewed new version is explicitly adopted. The proposals below are review recommendations only.

Do not:

- treat agreement between GPT and Codex as proof;
- silently edit assumptions;
- transfer the historical 7-state relative-degree result to the 9-state plant;
- infer recursive safety from instantaneous feasibility;
- claim exact viability from a sufficient certificate;
- conclude GO;
- implement controller/simulator/experiments.

For the next Codex response, check the derivations below, identify any errors/over-strong assumptions, and propose an explicit diff for the next MASTER + DECISION_LOG + REVIEW_GATE. If a proposed repair creates a new physical or mathematical obligation, state it.

---

# 1. Context reconstruction

## 1.1 Current scientific question

The project is **not** framed as “apply sampled-data HOCBF to DDWMR.”

The current question is:

> When can collision safety commanded by a digital controller actually be realized by a voltage-limited differential-drive robot whose motor, wheel, body, and wheel-ground contact dynamics prevent instantaneous execution of the commanded motion?

The intended distinction is:

$$
\text{mathematical safety command}
\quad\neq\quad
\text{physically realizable collision safety}.
$$

## 1.2 Current candidate 9-state plant

$$
x=
[p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R]^\top.
$$

Physical input:

$$
V=[V_L,V_R]^\top,\qquad |V_j|\le V_{\max}.
$$

Body kinematics currently written as

$$
\dot p_x=u\cos\theta,
\qquad
\dot p_y=u\sin\theta,
\qquad
\dot\theta=r.
$$

Wheel-contact longitudinal velocities:

$$
v_L=u-br,
\qquad
v_R=u+br.
$$

Slip velocities:

$$
\sigma_L=R_w\omega_L-(u-br),
\qquad
\sigma_R=R_w\omega_R-(u+br).
$$

Candidate longitudinal contact law:

$$
F_j=\mu_jN_j\phi(\sigma_j/v_s).
$$

Body dynamics:

$$
m\dot u=F_L+F_R-c_u u,
$$

$$
I_z\dot r=b(F_R-F_L)-c_r r.
$$

Wheel dynamics:

$$
J_w\dot\omega_j=K_t i_j-B_w\omega_j-R_wF_j.
$$

Electrical dynamics:

$$
L_j\dot i_j=V_j-R_ji_j-K_{e,j}\omega_j.
$$

The physical chain is intended to be

$$
V\rightarrow i\rightarrow\omega\rightarrow\sigma\rightarrow F
\rightarrow(u,r)\rightarrow(p,\theta).
$$

## 1.3 Current safety objects

Geometric collision-safe set for a static circular obstacle:

$$
\mathcal S=\{x:h(p)\ge0\},
\qquad
h(p)=\|p-p_o\|^2-R_s^2.
$$

The project distinguishes:

- instantaneous certificate-feasible set $\mathcal F_{\mathrm{inst}}$;
- one-hold safe set $\mathcal F_T(\mathcal S)$;
- sampled-state recursively safe certified subset $K_T$;
- exact robust viability kernel.

Robust quantifier order is intended to be

$$
\exists V_k\in\mathcal U\quad\forall\delta(\cdot)\in\Delta,
$$

with the **same held voltage** valid for all admissible hidden uncertainty trajectories during the hold.

## 1.4 Current candidate theoretical strategy

HOCBF is **optional/baseline only**.

Candidate core:

$$
\text{plant-structured robust reachable tube / predecessor reasoning}.
$$

No reachable enclosure $\widehat{\mathcal R}$ or useful nonempty $K_T$ has yet been constructed.

## 1.5 Gate state

- G1 Plant consistency: **NEEDS REVISION**
- G2 Certified reachable enclosure: **UNVERIFIED**
- G3 Recursive safe subset: **UNVERIFIED**
- G4 Novelty audit: **UNVERIFIED**

Overall remains **HOLD**.

---

# 2. Independent review of F01-F12

Each item below uses the project contract:

**Finding / Evidence / Consequence / Status / Required action**

---

## F01 — Contact signs and mechanical power transfer

### Finding

The Codex derivation is correct under the proposed body-frame convention and axle-midpoint geometry. No longitudinal contact-sign reversal is needed.

### Evidence

Take body axes forward/left/up, positive yaw counterclockwise, and contact coordinates

$$
r_L=(0,+b),\qquad r_R=(0,-b).
$$

Rigid-body contact longitudinal velocities are

$$
v_L=u-br,
\qquad
v_R=u+br.
$$

A forward force $F_j e_x$ produces moments

$$
\tau_{z,L}=-bF_L,
\qquad
\tau_{z,R}=+bF_R,
$$

hence

$$
I_z\dot r=b(F_R-F_L)-c_rr.
$$

With

$$
\sigma_j=R_w\omega_j-v_j,
$$

contact contribution to body-plus-wheel mechanical power is

$$
F_jv_j-R_wF_j\omega_j
=-F_j\sigma_j.
$$

For

$$
F_j=\mu_jN_j\phi(\sigma_j/v_s),
$$

with $\mu_jN_j\ge0$ and $z\phi(z)\ge0$,

$$
-F_j\sigma_j\le0.
$$

### Consequence

The longitudinal contact signs, yaw moment sign, and wheel reaction-torque sign are mutually consistent. This does **not** establish physical admissibility of lateral reactions or validate a complete tire model.

### Status

**VALID**, conditional on explicit coordinate conventions and the geometry decision in F04.

### Required action

Add to the next MASTER:

- explicit body-axis/sign conventions;
- $p$ as the adopted reference point;
- contact locations $(0,\pm b)$;
- definition of $F_j$ as ground-on-wheel longitudinal force transmitted to the body;
- the same $F_j$ entering wheel dynamics with torque $-R_wF_j$.

---

## F02 — Units and electromechanical energy consistency

### Finding

The energy identity in the Codex audit is correct. The current model must not allow arbitrary independent torque and back-EMF constants if it intends an ideal energy-consistent DC conversion.

### Evidence

For fixed parameters, define

$$
E=\frac12mu^2+\frac12I_zr^2+
\sum_{j=L,R}
\left(
\frac12J_j\omega_j^2+
\frac12L_ji_j^2
\right).
$$

Using the current equations gives

$$
\dot E=
\sum_jV_ji_j
-c_uu^2-c_rr^2
-\sum_j
\left(
B_j\omega_j^2+R_ji_j^2+F_j\sigma_j
\right)
+\sum_j(K_{t,j}-K_{e,j})i_j\omega_j.
$$

Thus ideal SI electromechanical conversion is power-consistent if, after any ideal gear transformation,

$$
K_{t,j}=K_{e,j}=:k_j.
$$

### Consequence

Without this physical relation, zero-input passivity and energy-based bounds are not established. Independent uncertainty in $K_t$ and $K_e$ is physically unsafe unless a different conversion/loss model is introduced.

### Status

**NEEDS REVISION**.

### Required action

For the minimal theorem plant, use one effective wheel-side conversion parameter per side:

$$
J_j\dot\omega_j=k_ji_j-B_j\omega_j-R_wF_j,
$$

$$
L_j\dot i_j=V_j-R_ji_j-k_j\omega_j.
$$

State:

- $m,I_z,J_j,L_j,R_j,R_w,b,v_s>0$;
- $c_u,c_r,B_j\ge0$;
- physical parameter uncertainty preserves electromechanical correlations;
- no double-counting of reflected motor/wheel inertia.

---

## F03 — Exact lateral constraint versus approximate lateral grip

### Finding

Codex is correct. The current 9-state plant imposes an **exact** lateral kinematic constraint, while the current textual statement $v_{body,y}\approx0$ is only approximate. These cannot support the same theorem without an additional coupled error model.

### Evidence

General planar COM kinematics/dynamics are

$$
\dot p=ue+v_ye_\perp,
$$

$$
m(\dot u-rv_y)=\sum F_x,
$$

$$
m(\dot v_y+ru)=\sum F_y.
$$

The current plant uses

$$
\dot p=ue,
$$

which is equivalent to imposing

$$
v_y\equiv0.
$$

Then the required net lateral reaction is

$$
\sum F_y=mur.
$$

A bound $|v_y|\le\varepsilon_y$ alone does not bound all effects of omitted lateral dynamics on $u,r,\theta$, so a simple positional margin is not a sound replacement.

### Consequence

Physical certification under merely approximate lateral grip is not justified by the current plant. Formal certification of an explicitly ideal constrained plant remains possible if contact validity is closed in F05.

### Status

**BLOCKER** for the current wording; repairable without adding a tenth state if the theorem plant is explicitly idealized.

### Required action

For the minimal branch, replace A5 by:

> The theorem plant imposes $v_y(t)\equiv0$ exactly as an ideal nonholonomic lateral constraint on a declared contact-validity domain. Arbitrary lateral skid is outside the theorem. Approximate physical realization requires a separately derived coupled model-error enclosure.

---

## F04 — COM/axle geometry

### Finding

Codex is correct. “COM sufficiently close to the axle midpoint” is not precise enough for the current equations. The current equations require the planar COM projection to coincide with the axle midpoint if exact axle lateral no-slip is used while $v_y=0$.

### Evidence

Let the COM be a longitudinal distance $a$ ahead of the drive-axle midpoint. Wheel-contact coordinates relative to COM become

$$
(-a,+b),\qquad(-a,-b).
$$

Their lateral velocity is

$$
v_y-ar.
$$

Axle lateral no-slip requires

$$
v_y=ar.
$$

The current plant simultaneously imposes

$$
v_y=0.
$$

For generic turning $r\neq0$, both conditions imply

$$
a=0.
$$

With nonzero $a$, lateral reactions also enter yaw dynamics:

$$
I_z\dot r=b(F_R-F_L)-a(Y_L+Y_R)-c_rr.
$$

### Consequence

The current 9-state equations are specifically an axle-midpoint-COM idealization. They do not certify an unspecified nonzero COM offset.

### Status

**BLOCKER** for unspecified COM geometry; straightforwardly repairable.

### Required action

Set, for the theoretical core,

$$
\text{planar COM projection} = \text{drive-axle midpoint}.
$$

Define $p$ at that point and use $R_s$ as a footprint-enclosing safety radius about this reference.

---

## F05 — Lateral reaction and combined friction capacity

### Finding

The main Codex objection is correct: the present longitudinal model alone does not guarantee that curved motion is contact-feasible. However, the statement can be repaired **without** adding dynamic lateral tire states if the project explicitly adopts an ideal set-valued lateral constraint-reaction model.

The algebraic condition derived by Codex is a correct **force-allocation feasibility condition** under an assumed combined-force envelope. It is not, by itself, a constitutive tire law.

### Evidence

With exact $v_y=0$ and COM at the axle midpoint, lateral balance requires

$$
Y_L+Y_R=mur.
$$

Suppose the theorem explicitly adopts the ideal combined tangential-force admissibility set

$$
F_j^2+Y_j^2\le(\mu_jN_j)^2.
$$

For fixed $F_j,\mu_j,N_j$, define

$$
a_j=\sqrt{(\mu_jN_j)^2-F_j^2}.
$$

Then

$$
Y_j\in[-a_j,a_j].
$$

There exists at least one pair $(Y_L,Y_R)$ satisfying both contact budgets and

$$
Y_L+Y_R=mur
$$

if and only if

$$
\boxed{|mur|\le a_L+a_R.}
$$

If

$$
F_j=\mu_jN_j\phi(\sigma_j/v_s),
$$

then

$$
a_j=\mu_jN_j\sqrt{1-\phi^2(\sigma_j/v_s)}.
$$

This proves existence of admissible algebraic constraint reactions inside the **assumed** envelope. It does not prove that a real isotropic Coulomb sliding point contact generates that reaction, nor does it identify a unique $Y_j$.

Therefore define a contact-validity set

$$
D_{contact}
=\left\{
(x,\vartheta):
\exists Y_L,Y_R\text{ such that }
Y_L+Y_R=mur,
\;F_j^2+Y_j^2\le(\mu_jN_j)^2
\right\}.
$$

For the two-contact idealization, this is equivalent pointwise to the boxed inequality above whenever $|F_j|\le\mu_jN_j$.

### Consequence

Under MASTER v2, F05 is a true blocker because no lateral reaction model or validity domain is defined.

But a full lateral tire-dynamics expansion is **not mathematically mandatory** for the minimal theoretical core. A defensible restricted model can instead be:

- exact nonholonomic lateral constraint;
- algebraic lateral reaction variables;
- explicit combined-force admissibility envelope;
- safety certificate required to preserve both collision safety and contact validity.

This remains an ideal constrained-contact approximation, not a complete tire model or arbitrary-skid theorem.

### Status

**BLOCKER** under MASTER v2.

Codex is **correct** that the allocation inequality alone does not validate a real tire law. Codex would be **too strong** only if interpreted as requiring a separate dynamic lateral constitutive law for any mathematically valid theorem.

### Required action

Minimal proposed repair:

1. introduce algebraic reactions $Y_L,Y_R$ (not new dynamic states);
2. impose
   $$
   Y_L+Y_R=mur;
   $$
3. adopt an explicit combined-force envelope;
4. freeze $N_L,N_R>0$ as fixed known drive-wheel normal loads in the first core theorem;
5. define $D_{contact}$;
6. require every later G2/G3 hold certificate to establish
   $$
   x(t)\in\mathcal S\cap D_{contact}
   \qquad\forall t\in[kT,(k+1)T];
   $$
7. explicitly exclude arbitrary lateral skid/full tire physics.

If Codex finds this ideal reaction model physically or mathematically inadequate for the intended claims, that disagreement must be resolved before revising MASTER; do not silently introduce lateral states.

---

## F06 — Motor/gear convention

### Finding

Codex is correct: the plant requires one consistent shaft convention. An unspecified gearbox changes torque, back EMF, reflected inertia, and braking authority.

### Evidence

For an ideal rigid reduction

$$
n=\omega_m/\omega_w>0,
$$

wheel-side effective quantities satisfy

$$
k_j^w=nk_j^m,
$$

$$
J_j^w=J_{wheel}+n^2J_m,
$$

$$
B_j^w=B_{wheel}+n^2B_m.
$$

Using wheel speed as $\omega_j$, the energy-consistent equations become

$$
J_j^w\dot\omega_j=k_j^w i_j-B_j^w\omega_j-R_wF_j,
$$

$$
L_j\dot i_j=V_j-R_ji_j-k_j^w\omega_j.
$$

### Consequence

Catalog motor-side and wheel-side constants cannot be mixed. Independent torque/back-EMF uncertainty is not automatically physically admissible.

### Status

**NEEDS REVISION**.

### Required action

For the minimal core, absorb a specified ideal rigid, bidirectionally backdrivable gearbox into wheel-side $k_j,J_j,B_j$. Electrical variables remain winding-terminal quantities. Transmission losses not represented by declared damping are outside scope.

---

## F07 — Braking-authority counterexample

### Finding

The Codex counterexample is correct and exposes a real logical flaw: $\underline\mu>0$ does **not** imply any positive braking-force lower bound under the current broad class of $\phi$.

### Evidence

The current assumptions permit

$$
\phi(z)\equiv0.
$$

This satisfies

$$
\phi(0)=0,
\quad z\phi(z)\ge0,
\quad |\phi(z)|\le1,
$$

and global Lipschitz continuity.

Then

$$
F_L=F_R=0.
$$

If $c_u=0$,

$$
\dot u=0
$$

for all voltage commands, so a positive inward body velocity can persist indefinitely despite $\underline\mu>0$.

If $c_u>0$,

$$
u(t)=u_0e^{-c_ut/m},
$$

but this slowing comes from modeled drag rather than actuator/contact braking.

Therefore

$$
\underline\mu>0
\not\Rightarrow
|F_{brake}|\ge F_{min}>0.
$$

Even adding a negative-slip force lower bound does not prove that bounded voltage can create and maintain the required negative slip.

### Consequence

Any theorem relying on guaranteed stopping distance, emergency motor braking, or a braking-based recursive backup is invalid under the current traction class.

### Status

**BLOCKER** for braking-authority claims.

### Required action

For the minimal next MASTER, prefer a **known fixed traction-shape function** rather than an adversarial $\phi$-family. Recommended structural assumptions:

$$
\phi(0)=0,
$$

$$
z\phi(z)>0\quad(z\neq0),
$$

$$
\phi(-z)=-\phi(z),
$$

$$
|\phi(z)|\le1,
$$

with global Lipschitz continuity and monotonicity.

A function such as $\tanh$ satisfies this type of structure.

Primary contact uncertainty should enter through fixed unknown $\mu_L,\mu_R$, not arbitrary switching of $\phi$.

Even after this change, do **not** claim a finite stopping-distance bound until a voltage-admissible braking policy is separately proved to generate/maintain sufficient braking slip.

---

## F08 — Zero wheel speed versus sustained wheel lock under ZOH

### Finding

Codex is correct. The 9-state ODE permits the state $\omega_j=0,u\neq0$, but this is not automatically a sustained wheel-lock mode.

### Evidence

At

$$
\omega_j=0,
$$

wheel dynamics give

$$
J_j\dot\omega_j=k_ji_j-R_wF_j.
$$

Sustained lock requires

$$
\dot\omega_j=0,
$$

hence

$$
i_j(t)=\frac{R_w}{k_j}F_j(t).
$$

If $F_j$ is differentiable and lock persists,

$$
\dot i_j=\frac{R_w}{k_j}\dot F_j.
$$

Since $\omega_j=0$,

$$
L_j\dot i_j=V_j-R_ji_j,
$$

so the terminal voltage required to maintain lock is

$$
\boxed{
V_j(t)=\frac{R_w}{k_j}
\left(L_j\dot F_j(t)+R_jF_j(t)\right).
}
$$

A ZOH command imposes

$$
V_j(t)=V_{j,k}
$$

over the entire hold. Therefore sustained lock can occur only on special trajectories for which the required expression is constant and admissible. For merely measurable traction changes, lock current requirements may change discontinuously while finite-inductance current remains continuous.

### Consequence

The motivation for retaining body velocity $u$ is valid: the model can represent passage through zero wheel speed while the body still moves. However, locked-wheel braking cannot be assumed as an available safety policy.

### Status

**BLOCKER** for sustained-lock braking claims.  
**VALID** for transient $\omega_j=0,u\neq0$.

### Required action

Replace any statement “wheel lock may occur” that suggests a persistent mode with:

> Zero wheel speed with nonzero body velocity is an admissible transient state. Sustained wheel lock is outside the core model unless an explicit admissible lock torque/mode is later added and proved.

Do not add a mechanical brake merely to save the current argument unless the project intentionally changes plant class.

---

## F09 — Uncertainty semantics and well-posedness

### Finding

The Codex well-posedness argument is substantially correct, but the proposed arbitrary measurable traction variation is broader than needed and can make G2 unnecessarily conservative. The minimal core should distinguish **unknown fixed physical parameters** from time-varying disturbances.

### Evidence

With a fixed known globally Lipschitz $\phi$, bounded input, positive inertias/inductances, and bounded contact coefficients, the vector field is measurable in time and Lipschitz in state under standard Caratheodory assumptions. Contact forces remain bounded because $|\phi|\le1$.

The internal body/wheel/electrical states have at most linear growth plus bounded contact forcing, so finite-time escape can be ruled out under fixed positive coefficients.

However, a physical parameter such as $\mu_j$ that is unknown but fixed along one trajectory is not equivalent to a freely switching signal $\mu_j(t)$. Replacing fixed uncertainty with a pointwise interval differential inclusion is a valid outer relaxation only if labeled as such.

### Consequence

G2 can begin from a mathematically well-posed uncertain ODE after the uncertainty class is frozen. Failing to preserve fixed-parameter dependence can dramatically enlarge the tube and make $K_T$ useless.

### Status

**NEEDS REVISION**.

### Required action

For the first core theorem, define a compact fixed parameter vector

$$
\vartheta\in\Theta
$$

that remains constant along each trajectory. Include uncertain motor/mechanical parameters and independently uncertain left/right traction coefficients as appropriate.

For the minimal branch:

- use fixed known $N_L,N_R>0$;
- use one fixed known $\phi$;
- do not introduce arbitrary time switching of $\mu_j$ yet;
- preserve fixed-parameter dependence in reachability when possible;
- if a pointwise interval/convex relaxation is later used, label it explicitly as an outer approximation.

---

## F10 — Controller information pattern

### Finding

Codex is correct. “Measurements or estimates” is not a complete information pattern for a safety theorem.

### Evidence

With exact state, the robust action requirement has the form

$$
\exists V_k\in\mathcal U
\quad\forall\vartheta\in\Theta
\quad\text{safe hold / endpoint return}.
$$

If instead the controller only knows

$$
x_k\in X_k,
$$

the correct condition is

$$
\exists V_k\in\mathcal U
\quad\forall x_k\in X_k
\quad\forall\vartheta\in\Theta
\quad\text{safe hold / endpoint return}.
$$

Pose uncertainty changes obstacle clearance directly; current and wheel-speed uncertainty change immediately available actuator authority.

### Consequence

Estimated-state physical safety is currently unformulated. Exact-state theory is still legitimate if scoped honestly.

### Status

**BLOCKER** for estimator/sensor claims; not a blocker for an ideal exact-state theorem.

### Required action

For the minimal theorem branch, assume:

- exact nine-state knowledge at sampling instants;
- zero sensing/computation/actuation delay;
- hidden uncertain parameters known only through $\Theta$.

No observer/estimator claim should appear in the core theorem.

---

## F11 — Equilibria, symmetry, and independent left/right uncertainty

### Finding

Codex is correct. The key distinction is between:

1. invariance of an individual straight/symmetric trajectory; and
2. symmetry of the **family of uncertain trajectories** under left/right exchange.

Equal uncertainty intervals do not imply equal realized left/right friction.

### Evidence

### Rest equilibrium

At

$$
u=r=\omega_L=\omega_R=i_L=i_R=0,
\qquad V_L=V_R=0,
$$

we have

$$
\sigma_L=\sigma_R=0,
\qquad F_L=F_R=0,
$$

so all internal derivatives vanish. Arbitrary fixed pose is therefore a rest equilibrium family.

### Straight-line invariance

At $r=0$, equal left/right states and voltages do not preserve $r=0$ under independent traction coefficients. If

$$
\sigma_L=\sigma_R=\sigma,
$$

then

$$
F_R-F_L=
(\mu_RN_R-\mu_LN_L)\phi(\sigma/v_s),
$$

and

$$
\dot r=
\frac{b}{I_z}
(\mu_RN_R-\mu_LN_L)
\phi(\sigma/v_s),
$$

which need not vanish.

Thus

$$
r=0
$$

is not robustly invariant under independently realized left/right uncertainty.

### Mirror symmetry of the uncertainty family

If the joint uncertainty set is closed under left/right exchange, e.g.

$$
(\mu_L,\mu_R)\in[\underline\mu,\bar\mu]^2,
$$

then reflecting

$$
(p_y,\theta,r)\mapsto(-p_y,-\theta,-r)
$$

and swapping left/right states, parameters, and inputs maps an admissible trajectory to another admissible trajectory. Therefore the **reachable family/set** can be mirror symmetric even though an individual realization does not remain straight.

### Pure spin

For opposite slips to generate opposite forces under matched left/right loads/coefficients, one needs

$$
\phi(-z)=-\phi(z).
$$

Current MASTER v2 does not require oddness. The Codex nonodd counterexample is valid.

### Consequence

The current straight-line braking subsection cannot be used as an unconditional robust reduction of the main independent-side-uncertainty problem.

However, exchange symmetry of the uncertainty set may later be exploitable when constructing reachable sets.

### Status

**NEEDS REVISION**.

### Required action

For the minimal MASTER revision:

- retain independent left/right traction uncertainty if scientifically intended;
- choose a joint set closed under left/right exchange;
- do **not** claim robust straight-line invariance for the general model;
- relabel straight-line braking as an **auxiliary symmetric subproblem** requiring explicitly
  $$
  \mu_L=\mu_R,
  \quad N_L=N_R,
  $$
  matched drive parameters and symmetric states/inputs;
- if F07 adopts odd $\phi$, pure-spin antisymmetry becomes available only under corresponding matched-side assumptions.

The auxiliary straight-line result must not be used as proof of the general independent-uncertainty theorem.

---

## F12 — Terminal-voltage authority, driver mode, and zero command

### Finding

Codex is correct. A signed voltage box becomes a precise theorem input only after the electrical boundary condition/driver mode is explicitly idealized.

### Evidence

At

$$
V_j=0,
$$

the current model gives

$$
L_j\dot i_j=-R_ji_j-k_j\omega_j.
$$

For

$$
\omega_j>0,
\qquad i_j(0)=0,
$$

initially

$$
\dot i_j<0,
$$

so electromagnetic torque becomes braking. This corresponds to a closed zero-terminal-voltage electrical path capable of accepting/generating current, not an open circuit.

Also $V_ji_j$ may be negative, so the ideal source/drive must be able to accept regenerated power or dissipate it.

A conditional current bound such as

$$
|i_j(t)|
\le
|i_j(0)|e^{-R_jt/L_j}
+
\frac{V_{max}+k_j\Omega}{R_j}
(1-e^{-R_jt/L_j})
$$

requires an independently established wheel-speed bound $|\omega_j|\le\Omega$; it does not prove real driver current capability.

### Consequence

Voltage feasibility is not complete hardware feasibility. Zero voltage does not mean coast/open circuit, and energy dissipation/passivity does not automatically provide an emergency-stop policy.

### Status

**NEEDS REVISION**.

### Required action

For the theoretical core, explicitly assume an ideal bidirectional four-quadrant terminal-voltage source:

$$
|V_j|\le V_{max},
\qquad
V(t)=V_k\text{ under fixed-period ZOH}.
$$

State that:

- $V=0$ means the closed zero-terminal-voltage RL boundary condition;
- both current directions and regenerative power flow are allowed;
- no current limiter, bus clipping, PWM ripple, thermal protection, open-circuit mode, or driver delay is included in the theorem plant.

Use the phrase **voltage-limited actuator dynamics**, not complete hardware-driver feasibility.

---

# 3. Minimal internally consistent revision set for the next MASTER

These are recommendations, not adopted assumptions.

## M1 — Freeze coordinates and geometry

Adopt exact conventions:

- body axes forward/left/up;
- positive yaw CCW;
- positive wheel rate = forward rolling;
- planar COM projection coincides with drive-axle midpoint;
- $p$ is this reference point;
- contact positions are $(0,\pm b)$.

## M2 — Exact lateral theorem constraint

Replace approximate lateral wording with

$$
v_y(t)\equiv0.
$$

State explicitly that arbitrary lateral skid is outside theorem scope.

## M3 — Algebraic lateral reactions and contact-validity domain

Introduce algebraic reactions $Y_L,Y_R$, not dynamic states:

$$
Y_L+Y_R=mur.
$$

Adopt, for the idealized theorem contact model,

$$
F_j^2+Y_j^2\le(\mu_jN_j)^2.
$$

Use fixed known $N_L,N_R>0$ in the first core theorem.

Define

$$
D_{contact}
=\{(x,\vartheta):\exists Y_L,Y_R\text{ satisfying lateral balance and contact budgets}\}.
$$

Future certified holds must establish

$$
x(t)\in\mathcal S\cap D_{contact}
\quad\forall t\text{ in the hold}.
$$

Do not call this a full tire model.

## M4 — Power-consistent motor model

Use effective wheel-side parameters:

$$
J_j\dot\omega_j=k_ji_j-B_j\omega_j-R_wF_j,
$$

$$
L_j\dot i_j=V_j-R_ji_j-k_j\omega_j.
$$

Any ideal rigid gearbox is absorbed into $k_j,J_j,B_j$.

## M5 — Known fixed traction-shape function

Use one known fixed $\phi$ satisfying at least:

$$
\phi(0)=0,
$$

$$
z\phi(z)>0\quad(z\ne0),
$$

$$
\phi(-z)=-\phi(z),
$$

$$
|\phi(z)|\le1,
$$

plus global Lipschitz continuity and monotonicity.

Do not infer finite stopping distance from these properties alone.

## M6 — Remove sustained-wheel-lock claims

Permit transient

$$
\omega_j=0,
\qquad u\neq0.
$$

State that sustained wheel lock is outside the core model unless a separate actuation/brake mode is later introduced and proved.

## M7 — Freeze uncertainty semantics

Use a compact **fixed unknown parameter vector**

$$
\vartheta\in\Theta
$$

that remains constant along each trajectory.

Keep independent left/right traction uncertainty if desired, with an exchange-symmetric set such as

$$
(\mu_L,\mu_R)\in[\underline\mu,\bar\mu]^2.
$$

Do not silently replace fixed uncertainty with arbitrary switching signals.

## M8 — Exact-state core theorem

Assume exact knowledge of the nine-state vector at each sample and zero sensing/computation/actuation delay.

State estimation/error/delay is a later extension.

## M9 — Ideal four-quadrant terminal-voltage source

Assume

$$
|V_j|\le V_{max},
\qquad
V(t)=V_k
$$

over each hold.

Allow both current directions and regenerative power. Exclude current limiting, bus clipping, PWM ripple, thermal protection, and open-circuit switching from the theorem plant.

## M10 — Straight-line braking becomes auxiliary only

Do not use the straight-line subcase as a robust reduction of the main model.

Any straight-line analysis must explicitly assume matched/symmetric realized parameters and loads. It may be useful as a diagnostic/corollary, but cannot establish the general independent-side-uncertainty result.

---

# 4. Claims that remain prohibited after this review

Unless later proven, the project must not claim:

- the whole geometric collision-free set $\mathcal S$ is invariant;
- instantaneous certificate/QP feasibility implies recursive feasibility;
- certificate infeasibility means collision is physically unavoidable;
- $K_T$ equals the exact viability kernel;
- the historical 7-state relative-degree result applies to the current 9-state plant;
- bounded friction coefficient alone implies braking authority;
- positive $\underline\mu$ implies finite stopping distance;
- $\omega=0$ means sustained wheel lock;
- the 9-state model covers arbitrary lateral skid/full tire physics;
- the combined-force allocation check is a validated real tire constitutive law;
- an auxiliary symmetric straight-line model proves the general independent-side-uncertainty case;
- voltage feasibility equals complete hardware feasibility;
- dense numerical integration proves inter-sample safety;
- generic reachable-set inclusion or predecessor induction is research novelty;
- any “first” claim before G4 full-text novelty closure.

---

# 5. Consequences for G2 and G3

Do not start G2/G3 theorem derivations until the next MASTER explicitly resolves the G1 assumptions above.

When G2 eventually begins, the certified object must cover **both** collision safety and contact validity:

$$
\widehat{\mathcal R}([0,T];x_k,V_k)
\subseteq
\mathcal S\cap D_{contact}
$$

or an equivalent rigorously defined condition.

The same held voltage $V_k$ must work for all admissible fixed parameter realizations in $\Theta$.

If computational reachability uses a relaxed differential inclusion that permits parameter switching, this is an outer approximation and its conservatism must be acknowledged.

For G3, any certified set $K_T$ must remain distinct from exact viability. A sufficient recursion target remains conceptually:

$$
K_T\subseteq\operatorname{Pre}_T(K_T),
$$

but the induction itself is generic and not novelty.

---

# 6. What Codex should do next

Do **not** conclude G1 pass immediately from this handoff.

Instead:

1. Re-check each F01-F12 derivation above against the repository equations.
2. Explicitly agree/disagree with the proposed F05 resolution using algebraic lateral reactions and $D_{contact}$.
3. Check whether M5 (known fixed odd monotone $\phi$) is the smallest acceptable repair or unnecessarily restrictive.
4. Check the physical consistency of fixing $N_L,N_R$ while allowing turning under the ideal constrained model.
5. Check whether the fixed independent $(\mu_L,\mu_R)$ uncertainty semantics are compatible with the intended contact-validity domain and future reachability computation.
6. Produce a proposed patch for:
   - `MASTER_RESEARCH_CONTEXT_v2.md` -> next declared version;
   - `DECISION_LOG.md`;
   - `REVIEW_GATE.md`;
   - `LITERATURE_MATRIX.md` only if the formulation change materially changes G4 screening fields.
7. Keep all edits proposed/pending until user/reviewer acceptance.
8. Keep project status **HOLD**.
9. Do not create controller/simulator/experiment code.

For every disagreement or newly discovered issue, respond using:

**Finding / Evidence / Consequence / Status / Required action.**

---

# 7. Expected Codex response structure

## A. Review of GPT F01-F12

For each F01-F12:

- ACCEPT / MODIFY / REJECT the GPT reasoning;
- show the equation-level reason;
- identify whether it changes the proposed MASTER revision.

## B. F05 decision

Choose explicitly between:

1. ideal nonholonomic constraint + algebraic admissible lateral reactions + $D_{contact}$; or
2. expanded lateral/contact dynamic plant.

Do not choose by convenience only; state theorem implications and physical scope.

## C. Minimal MASTER revision

Return exact replacement/addition text and equations, not only prose summaries.

## D. Remaining G1 blockers

List what would still prevent G1 acceptance after the revision.

## E. Gate status

Remain HOLD unless all G1 issues are actually closed and reviewed. Even a future G1 pass does not authorize implementation because G2-G4 remain open.

---

# 8. Review bottom line

The Codex G1 audit is strong and most F01-F12 findings are correct. The principal independent-review adjustment is F05:

> The force-allocation inequality does not constitute a real tire constitutive law, but a separate dynamic lateral tire model is not necessarily required if the theorem deliberately adopts an ideal nonholonomic lateral constraint with algebraic reaction forces and an explicit combined-force validity domain.

The most important confirmed blockers are:

- approximate-versus-exact lateral constraint ambiguity;
- unspecified COM/axle geometry;
- missing lateral/contact validity domain;
- unconstrained electromechanical parameter conventions;
- overly broad traction-law class that provides no braking authority;
- unsupported sustained-wheel-lock interpretation;
- unresolved uncertainty semantics and state-information pattern;
- misuse of straight-line symmetry under independent left/right uncertainty;
- underspecified electrical drive boundary condition.

Recommended project state remains **HOLD**. No controller or implementation is authorized by this review.
