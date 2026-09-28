# GPT → CODEX HANDOFF — Independent Review of Proposal R2 at commit 12edd1b

**Purpose:** Complete handoff of GPT's independent review of Codex proposal R2 at commit `12edd1b`, preserving all equation-level checks, accept/modify/reject decisions, mandatory edits before adoption, remaining blockers, and gate status without relying on chat history.

**Repository:** `NADUNGVN/ddwmr-actuator-safety`  
**Reviewed commit:** `12edd1b6e93cef58870924b1d8bdb627000ccca7`  
**Commit message:** `Revise pending v2.1 to effective contact capacities and minimal phi assumptions`

**Current authoritative formulation:** `research_context/MASTER_RESEARCH_CONTEXT_v2.md`  
**Authority status:** MASTER v2 remains authoritative. Proposal v2.1 R2 is not yet adopted.  
**Overall project status:** **HOLD**  
**Implementation status:** No controller/simulator/experiment implementation is authorized.  
**Gate status:** G1 NEEDS REVISION; G2/G3/G4 UNVERIFIED.

---

# 0. OPERATING INSTRUCTIONS FOR CODEX

Treat this document as **GPT's independent review evidence**, not as an amendment to MASTER.

Do not:

- infer GO from reviewer agreement;
- treat model agreement as proof;
- silently change assumptions;
- apply the current pending patch byte-for-byte as final adoption without finalizing proposal metadata;
- begin G2/G3 implementation or controller coding.

Before changing authoritative context:

1. read current MASTER v2;
2. read:
   - `docs/reviews/CODEX_RESPONSE_TO_REVIEW_094f3c8_R2.md`
   - `docs/proposals/v2_1/MASTER_v2_1_PREVIEW.md`
   - `docs/proposals/v2_1/MASTER_v2_1_PENDING.patch`
3. apply the mandatory edits in this handoff;
4. prepare an **adoption-finalization patch**;
5. return that exact final text for review before authoritative application;
6. preserve overall **HOLD** and all open gates.

Use for each substantive issue:

**Finding / Evidence / Consequence / Status / Required action**

---

# 1. REVIEWED MATERIAL

GPT independently reviewed commit `12edd1b`, especially:

- `docs/reviews/CODEX_RESPONSE_TO_REVIEW_094f3c8_R2.md`
- `docs/proposals/v2_1/MASTER_v2_1_PREVIEW.md`
- `docs/proposals/v2_1/MASTER_v2_1_PENDING.patch`
- `research_context/MASTER_RESEARCH_CONTEXT_v2.md`
- `research_context/DECISION_LOG.md`
- `research_context/LITERATURE_MATRIX.md`
- `research_context/REVIEW_GATE.md`

The authoritative four research-context files remain unchanged at this point.

---

# 2. OVERALL REVIEW DECISION

GPT's disposition of proposal R2 is:

\[
\boxed{
\text{ACCEPT R2 FORMULATION WITH MINOR MANDATORY EDITS BEFORE ADOPTION}
}
\]

The three mandatory edits are:

1. replace the phrase **“unknown fixed physical parameter vector”** with **“unknown fixed model-parameter vector”**;
2. move the explicit historical finite-height diagnostic
   \[
   b(N_L-N_R)+Hmur=0
   \]
   out of the future authoritative MASTER and keep it in review/decision history;
3. if/when adopting, replace all proposal metadata such as
   - `pending adoption`,
   - `candidate`,
   - `proposal R2`,
   - “enter the actual adoption date”

   with final adopted-version wording and actual decision/date.

After those edits, GPT considers the **reduced \(C_j\)-based nine-state formal plant internally coherent enough to become the next candidate MASTER formulation**.

This is **not**:

- a G1 pass;
- physical validation;
- a G2/G3 result;
- a G4 novelty result;
- implementation authorization.

---

# 3. CURRENT PROPOSED R2 PLANT

## 3.1 State

\[
x=
[p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R]^\top.
\]

## 3.2 Input

\[
V=[V_L,V_R]^\top.
\]

## 3.3 Geometry

The planar COM projection coincides exactly with the drive-axle midpoint.

Contact locations:

\[
(0,+b),
\qquad
(0,-b).
\]

Body axes:

- \(x\): forward;
- \(y\): left;
- \(z\): up.

Positive yaw is counterclockwise.

Positive wheel rate corresponds to forward rolling.

## 3.4 Exact body kinematics

\[
\dot p_x=u\cos\theta,
\]

\[
\dot p_y=u\sin\theta,
\]

\[
\dot\theta=r.
\]

The theorem plant imposes:

\[
\boxed{
v_y\equiv0
}
\]

exactly.

This is an ideal constrained planar model.

It does not model arbitrary lateral skid.

---

# 4. CONTACT KINEMATICS

Left and right longitudinal contact velocities:

\[
v_L=u-br,
\]

\[
v_R=u+br.
\]

Slip velocities:

\[
\sigma_L=R_w\omega_L-v_L,
\]

\[
\sigma_R=R_w\omega_R-v_R.
\]

---

# 5. EFFECTIVE TANGENTIAL CAPACITY FORMULATION

This is the central accepted R2 correction.

The formal core no longer uses literal physical normal loads \(N_j\) or friction coefficients \(\mu_j\).

Instead define:

\[
\boxed{
C_j>0
}
\]

as an effective per-wheel tangential contact-force capacity of the reduced model.

Units:

\[
[C_j]=\mathrm N.
\]

Bounds:

\[
0<
\underline C_j
\le
C_j
\le
\overline C_j
<
\infty.
\]

The longitudinal contact force is:

\[
\boxed{
F_j
=
C_j
\phi(\sigma_j/v_s).
}
\]

The combined tangential-force envelope is:

\[
\boxed{
F_j^2+Y_j^2
\le
C_j^2.
}
\]

This is an **ideal reduced force-budget model**.

It is not yet a validated tire constitutive law.

---

# 6. WHY \(C_j\) IS ACCEPTED

## Finding

The \(C_j\) substitution is mathematically coherent and removes the previous fixed-normal-load overclaim.

## Evidence

The formal force law has correct units:

\[
F_j
=
C_j\phi(\sigma_j/v_s),
\]

where \(\phi\) is dimensionless.

The contact dissipation satisfies:

\[
F_j\sigma_j
=
C_jv_s z_j\phi(z_j),
\qquad
z_j=\sigma_j/v_s.
\]

Since:

\[
z\phi(z)>0
\quad
(z\neq0),
\]

contact dissipation has the intended sign.

No \(\mu_j\) or \(N_j\) remains in the formal parameter vector.

## Consequence

The formal core no longer pretends that wheel normal-load distribution, roll/pitch balance, and support mechanics are solved.

## Status

**VALID**

## Required action

Keep \(C_j\) as the formal reduced-model parameter.

Do not revert to literal \(\mu_jN_j\) unless a support/load/contact model is explicitly added.

---

# 7. PHYSICAL INTERPRETATION OF \(C_j\)

The proposed MASTER should state clearly:

> \(C_j\) is an effective tangential contact-force capacity of the reduced planar model. It is not asserted to equal the instantaneous physical friction-normal-load product of a real wheel contact.

A relation such as:

\[
C_j\approx\mu_jN_j
\]

may be used only after separate justification.

Possible future evidence could include:

- a support/load model;
- experimentally justified operating envelope;
- parameter identification;
- validated model-error enclosure.

The following implication is **not** allowed:

\[
\text{“real force capacity is bounded”}
\Rightarrow
\text{“real trajectory is enclosed by the fixed-}C_j\text{ model”}.
\]

---

# 8. WHY CAPACITY BOUNDS DO NOT AUTOMATICALLY GIVE TRAJECTORY BOUNDS

## Finding

R2 correctly adds this caveat.

## Evidence

Changing capacity changes force:

\[
\Delta F_j
=
\Delta C_j
\phi(\sigma_j/v_s).
\]

Therefore:

\[
\Delta\dot u
=
\frac{\Delta F_j}{m},
\]

\[
\Delta\dot\omega_j
=
-
\frac{R_w}{J_j}
\Delta F_j,
\]

and yaw acceleration also changes.

Hence there is no generic monotonic ordering:

\[
C_j^{(1)}
\le
C_j^{(2)}
\]

that implies one trajectory safely outer-bounds the other.

Likewise, the envelope:

\[
F_j^2+Y_j^2
\le
C_j^2
\]

does not by itself prove the exact equality law:

\[
F_j=C_j\phi(\sigma_j/v_s)
\]

for a real robot.

## Consequence

Physical transfer requires either:

\[
\text{actual trajectories}
\subseteq
\text{modeled family},
\]

or a certified discrepancy enclosure.

## Status

**VALID**

## Required action

Retain this caveat in the next MASTER.

---

# 9. MINIMAL CORE ASSUMPTIONS ON \(\phi\)

The proposed R2 core assumptions are accepted.

Use one known fixed function:

\[
\phi:\mathbb R\to[-1,1]
\]

satisfying:

\[
\phi(0)=0,
\]

\[
z\phi(z)>0
\quad
(z\neq0),
\]

\[
|\phi(z)|\le1,
\]

and global Lipschitz continuity:

\[
|\phi(z_1)-\phi(z_2)|
\le
L_\phi|z_1-z_2|.
\]

Do **not** assume globally:

- oddness;
- monotonicity;
- differentiability;
- a uniform positive traction floor.

---

# 10. ODDNESS STATUS

Oddness:

\[
\phi(-z)=-\phi(z)
\]

is **not** a core plant assumption.

It may be added only for auxiliary analyses requiring antisymmetry, such as:

- pure spin;
- reversal symmetry;
- matched-side antisymmetric contact-force arguments.

The general plant must not use oddness silently.

---

# 11. ALGEBRAIC LATERAL REACTIONS

Exact lateral constraint requires:

\[
Y_L+Y_R=mur.
\]

Combined capacity:

\[
F_j^2+Y_j^2
\le
C_j^2.
\]

Available lateral capacity:

\[
a_j
=
\sqrt{
C_j^2-F_j^2
}.
\]

Equivalently:

\[
a_j
=
C_j
\sqrt{
1-\phi^2(\sigma_j/v_s)
}.
\]

Define:

\[
A=a_L+a_R.
\]

Contact-force allocation exists iff:

\[
\boxed{
|mur|
\le
A.
}
\]

For \(A>0\), one admissible selection is:

\[
Y_j
=
\frac{mur\,a_j}{A}.
\]

At \(A=0\), admissibility requires:

\[
mur=0,
\]

and:

\[
Y_L=Y_R=0.
\]

The individual reaction allocation does not enter the nine-state ODE.

---

# 12. CONTACT VALIDITY DOMAIN

For fixed model parameter realization \(\vartheta\), define:

\[
\boxed{
D_c(\vartheta)
=
\left\{
x:
|mur|
\le
\sum_{j=L,R}
\sqrt{
C_j^2-F_j(x,\vartheta)^2
}
\right\}.
}
\]

This is a **parameter-specific validity domain** for the ideal constrained model.

Leaving this domain means:

> the selected reduced contact model is no longer valid.

It does **not** mean:

- the real robot necessarily crashes;
- the robot automatically switches to a skid model;
- state projection is allowed;
- contact validity is recovered by clipping.

---

# 13. BODY DYNAMICS

\[
m\dot u
=
F_L+F_R-c_uu,
\]

\[
I_z\dot r
=
b(F_R-F_L)-c_rr.
\]

No additive residual/disturbance is active in the first core.

Residuals cannot be used to hide missing support/contact mechanics.

---

# 14. WHEEL DYNAMICS

\[
\boxed{
J_j\dot\omega_j
=
k_ji_j
-
B_j\omega_j
-
R_wF_j.
}
\]

---

# 15. ELECTRICAL DYNAMICS

\[
\boxed{
L_j\dot i_j
=
V_j
-
R_ji_j
-
k_j\omega_j.
}
\]

The same wheel-side effective conversion constant \(k_j\) is used for:

- torque/current conversion;
- back-EMF/wheel-speed conversion.

This preserves ideal electromechanical power consistency.

---

# 16. GEAR/SHAFT CONVENTION

For ideal fixed reduction:

\[
n_j
=
\frac{\omega_{m,j}}{\omega_j}.
\]

Use effective wheel-side quantities:

\[
k_j
=
n_jk_j^m,
\]

\[
J_j
=
J_{wheel,j}
+
n_j^2J_{motor,j},
\]

\[
B_j
=
B_{wheel,j}
+
n_j^2B_{motor,j}.
\]

The core assumes an ideal rigid, bidirectionally backdrivable reduction.

Excluded unless explicitly modeled:

- backlash;
- compliance;
- nonlinear gearbox loss;
- non-backdrivability;
- undeclared drivetrain friction.

---

# 17. ENERGY CONSISTENCY

Define:

\[
E
=
\frac12mu^2
+
\frac12I_zr^2
+
\sum_j
\left(
\frac12J_j\omega_j^2
+
\frac12L_ji_j^2
\right).
\]

Then:

\[
\boxed{
\dot E
=
\sum_jV_ji_j
-
c_uu^2
-
c_rr^2
-
\sum_j
\left(
B_j\omega_j^2
+
R_ji_j^2
+
F_j\sigma_j
\right).
}
\]

The ideal lateral reactions do no work.

At:

\[
V=0,
\]

total energy is nonincreasing under the stated assumptions.

This does **not** imply:

- monotonic body speed;
- guaranteed stop;
- finite stopping time;
- finite stopping distance;
- safe emergency braking policy.

---

# 18. VOLTAGE SOURCE MODEL

The theorem input is actual terminal voltage:

\[
|V_j|
\le
V_{\max}.
\]

Input is held by ZOH:

\[
V(t)=V_k,
\qquad
t\in[kT,(k+1)T).
\]

The source is an ideal four-quadrant terminal-voltage source.

Allowed:

- positive current;
- negative current;
- regenerated electrical power;
- source/sink behavior.

Not modeled:

- current limits;
- thermal protection;
- bus clipping;
- PWM ripple;
- open-circuit switching;
- driver delay.

At:

\[
V=0,
\]

the model represents a closed zero-terminal-voltage RL condition, not open-circuit coast.

---

# 19. FIXED MODEL-PARAMETER SEMANTICS

**Mandatory terminology edit:**

Do not call \(\vartheta\) an “unknown fixed physical parameter vector.”

Use:

> **unknown fixed model-parameter vector**

or:

> **unknown fixed plant/model parameter vector**.

Recommended:

\[
\vartheta
=
(
m,I_z,R_w,b,v_s,
c_u,c_r,
J_L,J_R,
B_L,B_R,
L_L,L_R,
R_L,R_R,
k_L,k_R,
C_L,C_R
)
\in\Theta.
\]

Requirements:

- \(\Theta\) nonempty;
- compact;
- positive lower bounds for positive physical/model quantities;
- damping nonnegative;
- model correlations preserved;
- \(\vartheta\) fixed for the complete execution.

Analytical augmentation:

\[
\dot\vartheta=0
\]

is allowed.

This does not make \(\vartheta\) measured.

---

# 20. UNCERTAINTY CLASSES — DO NOT CONFUSE

The R2 core uses:

\[
\boxed{
\vartheta(t)\equiv\vartheta_0
}
\]

for the whole execution.

This does **not** cover:

### Time-varying capacity

\[
C_j(t)
\in
[\underline C_j,\overline C_j].
\]

### Hold-wise changing capacity

\[
C_j(t)=C_{j,k}
\quad
t\in[kT,(k+1)T).
\]

### Spatially varying terrain

\[
C_j=C_j(p).
\]

These are future extensions.

A switching differential inclusion may outer-bound some of them, but it is not the exact fixed-parameter plant.

---

# 21. CONTROLLER INFORMATION

The first theorem assumes exact knowledge of:

\[
x(kT)
=
[p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R]^\top.
\]

Assume zero:

- sensing delay;
- computation delay;
- actuation delay.

The controller knows:

\[
\Theta,
\]

not the true:

\[
\vartheta.
\]

The controller does not observe or select:

\[
Y_L,Y_R.
\]

Estimated-state safety is future work.

---

# 22. COLLISION SAFE SET

For one static circular obstacle:

\[
h(p)
=
\|p-p_o\|^2
-
R_s^2.
\]

Define:

\[
\mathcal S
=
\{x:h(p)\ge0\}.
\]

The entire \(\mathcal S\) is not claimed invariant.

---

# 23. CORRECT JOINT CONTACT SETS

Define:

\[
\mathscr D_c
=
\{
(x,\vartheta):
\vartheta\in\Theta,
\;
x\in D_c(\vartheta)
\}.
\]

Then:

\[
\boxed{
\mathscr S_c
=
(\mathcal S\times\Theta)
\cap
\mathscr D_c.
}
\]

Define conservative state-only robust admissibility:

\[
\boxed{
\mathcal S_{\rm rob}
=
\mathcal S
\cap
\bigcap_{\vartheta\in\Theta}
D_c(\vartheta).
}
\]

Do not write:

\[
x\in\mathcal S\cap\mathscr D_c
\]

because the objects occupy different spaces.

Do not project existentially over favorable hidden parameters.

---

# 24. JOINT REACHABLE PAIRS

For fixed hidden parameter \(\vartheta\), denote:

\[
x_\vartheta(t;x,V).
\]

Define:

\[
\boxed{
\mathscr R(t;x,V)
=
\{
(x_\vartheta(t;x,V),\vartheta):
\vartheta\in\Theta
\}.
}
\]

Full-hold reachable pairs:

\[
\mathscr R([0,T];x,V)
=
\bigcup_{t\in[0,T]}
\mathscr R(t;x,V).
\]

---

# 25. ONE-HOLD SAFETY / CONTACT ADMISSIBILITY

Define:

\[
\boxed{
\mathcal F_T^c
=
\left\{
x\in\mathcal S_{\rm rob}:
\exists V\in\mathcal U,
\;
\mathscr R([0,T];x,V)
\subseteq
\mathscr S_c
\right\}.
}
\]

Equivalent quantifier interpretation:

\[
\exists V
\quad
\forall\vartheta\in\Theta
\quad
\forall t\in[0,T]:
\]

\[
x_\vartheta(t;x,V)
\in
\mathcal S
\cap
D_c(\vartheta).
\]

This is only one-hold safety.

It is not recursive feasibility.

---

# 26. ROBUST PREDECESSOR

For:

\[
A\subseteq\mathcal S_{\rm rob},
\]

define:

\[
\boxed{
\operatorname{Pre}_T^c(A)
=
\left\{
x\in\mathcal S_{\rm rob}:
\exists V\in\mathcal U
\;
\forall\vartheta\in\Theta:
\begin{array}{l}
x_\vartheta(t;x,V)
\in
\mathcal S\cap D_c(\vartheta),
\quad
\forall t\in[0,T],
\\[1mm]
x_\vartheta(T;x,V)
\in
A
\end{array}
\right\}.
}
\]

Candidate recursive safe set:

\[
\boxed{
K_T
\subseteq
\operatorname{Pre}_T^c(K_T).
}
\]

This is a sufficient recursive target.

It may be conservative.

It is not exact history-dependent viability.

---

# 27. SAMPLE-TIME VS CONTINUOUS-TIME CLAIMS

If a future theorem proves the predecessor recursion, then intended claims are:

\[
x(kT)\in K_T
\quad
\forall k,
\]

and:

\[
x(t)
\in
\mathcal S
\cap
D_c(\vartheta)
\quad
\forall t\ge0.
\]

Do **not** say:

\[
K_T
\]

is continuously invariant unless the hybrid state including held input/clock is treated explicitly.

---

# 28. JOINT TUBE VS STATE-ONLY TUBE

Preferred:

\[
\mathscr R
\subseteq
\widehat{\mathscr R}
\]

with state/parameter correlation preserved.

A stronger state-only sufficient condition is:

\[
\widehat{\mathcal R}_x
\times
\Theta
\subseteq
\mathscr S_c.
\]

This discards correlation.

It is not equivalent to the exact joint condition.

---

# 29. WHEEL ZERO VS SUSTAINED LOCK

The model admits:

\[
\omega_j=0,
\qquad
u\neq0.
\]

This may occur transiently.

Sustained:

\[
\omega_j(t)\equiv0
\]

requires:

\[
k_ji_j
=
R_wF_j.
\]

If \(F_j\) is differentiable:

\[
V_j(t)
=
\frac{R_w}{k_j}
\left(
L_j\dot F_j
+
R_jF_j
\right).
\]

A ZOH input can maintain zero wheel speed only for special admissible trajectories.

Therefore:

- no automatic wheel-lock mode;
- no mechanical brake;
- no guaranteed locked-wheel backup policy.

---

# 30. BRAKING CLAIM STATUS

Strict sign preservation:

\[
z\phi(z)>0
\]

does not establish a stopping theorem.

A stopping result still requires proving:

1. a voltage-admissible braking policy;
2. that negative braking slip is reachable;
3. that the required slip region is maintained;
4. contact validity is preserved;
5. low-speed behavior;
6. finite remaining travel.

No stopping-distance theorem is currently established.

---

# 31. STRAIGHT-LINE AUXILIARY SUBPROBLEM

The general independent-side uncertain problem does **not** preserve:

\[
r=0.
\]

At equal slip:

\[
\dot r
=
\frac{b}{I_z}
(C_R-C_L)
\phi(\sigma/v_s).
\]

Therefore a straight-line reduction requires matched realized data, including:

\[
C_L=C_R,
\]

matched motor/wheel parameters,

symmetric states,

symmetric voltages,

and:

\[
r(0)=0.
\]

This is an auxiliary subproblem only.

It cannot prove the general robust theorem.

---

# 32. MIRROR SYMMETRY

Let \(P\) denote reflection plus left/right exchange.

Covariance:

\[
P
x(t;x_0,V,\vartheta)
=
x(t;Px_0,PV,P\vartheta)
\]

requires all side-dependent data to transform consistently.

Symmetry of the **same** robust problem requires:

\[
P\Theta=\Theta,
\]

plus compatible:

- known side data;
- initial sets;
- input sets;
- policy;
- obstacle/domain geometry.

A fixed off-axis obstacle need not be reflection invariant.

---

# 33. HOCBF STATUS

HOCBF remains:

- optional;
- baseline;
- local regular-domain comparison;
- literature bridge.

Do not restore HOCBF as the core method.

Do not transfer the old seven-state relative-degree result to the nine-state plant.

---

# 34. RESEARCH QUESTION / TITLE SCOPE

The R2 title is accepted in principle:

> **Inter-Sample Collision Safety for a Reduced Differential-Drive Robot Model under Voltage Limits and Uncertain Tangential Contact Capacity**

The formal research question should remain phrased in terms of the reduced model.

Recommended scope language:

> When can continuous collision safety be certified within a reduced electromechanical/contact DDWMR model that explicitly represents finite voltage-driven actuator dynamics and bounded modeled tangential contact authority?

Avoid unqualified phrases such as:

> physically realizable collision safety of a DDWMR

until model correspondence to a real platform is separately demonstrated.

---

# 35. PHYSICAL CORRESPONDENCE REMAINS UNVERIFIED

A theorem for the reduced plant does not prove safety of an actual robot.

A real-platform claim needs at least one of:

\[
\text{actual trajectories}
\subseteq
\text{modeled parameter family},
\]

or:

\[
\text{actual trajectory}
\in
\text{model trajectory}
\oplus
\text{certified discrepancy bound}.
\]

Evidence may require:

- selected \(\phi\);
- identified \(C_j\) range;
- motor constants;
- drivetrain parameters;
- support/contact operating envelope;
- driver limits;
- model discrepancy characterization.

---

# 36. MANDATORY EDIT 1 — TERMINOLOGY

Current proposal says approximately:

> `vartheta below is an unknown fixed physical parameter vector`.

Change to:

> `vartheta below is an unknown fixed model-parameter vector`.

Reason:

\(C_j\) is explicitly a reduced-model effective capacity and is not yet established as a physical instantaneous quantity.

Status:

**MANDATORY BEFORE ADOPTION**

---

# 37. MANDATORY EDIT 2 — MOVE HISTORICAL NORMAL-LOAD DIAGNOSTIC OUT OF MASTER

The R2 MASTER preview currently includes the historical equation:

\[
b(N_L-N_R)+Hmur=0.
\]

The equation is correct as the diagnostic argument that motivated abandoning literal fixed \(N_j\).

However, \(N_j\) and \(H\) no longer belong to the formal core.

Keeping this detailed equation inside the new authoritative MASTER may cause future agents to reintroduce rejected normal-load variables.

Recommended action:

Move the derivation to:

- `docs/reviews/G1_PHYSICAL_MODEL_AUDIT_v2.md`, and/or
- `DECISION_LOG.md`.

In MASTER A3 retain only:

> Literal wheel normal loads and friction coefficients are not formal core parameters. Mapping the effective capacities to physical support/contact quantities requires independent justification.

Status:

**MANDATORY EDITORIAL CLEANUP BEFORE ADOPTION**

---

# 38. MANDATORY EDIT 3 — FINALIZE PROPOSAL METADATA ON ADOPTION

The current pending patch intentionally contains proposal-only wording such as:

- `Pending adoption entry`;
- `proposal R2`;
- `declared v2.1 candidate`;
- `This note takes effect only with explicit adoption`;
- `Enter the actual adoption date...`.

This is correct for a review patch.

It is not correct as final authoritative text.

If adoption is approved, create a finalization patch that:

1. records the actual adoption date;
2. replaces pending/candidate wording with adopted v2.1 wording;
3. preserves links to prior review evidence;
4. leaves gate statuses unchanged unless separately reviewed.

Do **not** apply the current pending patch literally as the final authoritative commit.

Status:

**MANDATORY BEFORE AUTHORITATIVE APPLICATION**

---

# 39. R2 ACCEPT / MODIFY / REJECT TABLE

| R2 item | GPT decision | Reason |
|---|---|---|
| \(F_j=C_j\phi(\sigma_j/v_s)\) | **ACCEPT** | Correct reduced force law. |
| \(F_j^2+Y_j^2\le C_j^2\) | **ACCEPT** | Valid ideal tangential budget. |
| Remove active \(\mu_j,N_j\) from formal core | **ACCEPT** | Fixes unresolved normal-load overclaim. |
| \(C_j\) as effective model capacity | **ACCEPT** | Proper reduced-model interpretation. |
| \(C_j\) as proven physical \(\mu N\) | **REJECT** | No support/load/contact proof. |
| Core strict-sign \(\phi\) | **ACCEPT** | Excludes degenerate zero-force law. |
| Core Lipschitz \(\phi\) | **ACCEPT** | Supports ODE well-posedness. |
| Core global monotonicity | **REJECT / unnecessary** | Not used. |
| Core global oddness | **REJECT** | Auxiliary only. |
| Auxiliary oddness | **ACCEPT** | Valid local symmetry assumption. |
| Execution-fixed hidden parameters | **ACCEPT** | Coherent narrowed uncertainty class. |
| Time-varying traction claim | **REJECT for v2.1 core** | Not covered. |
| Typed joint state/parameter sets | **ACCEPT** | Correct quantifier/type structure. |
| State-only robust set | **ACCEPT as conservative** | Sound sufficient abstraction. |
| State-only predecessor | **ACCEPT as sufficient target** | Not exact viability. |
| Reduced-model title/question | **ACCEPT WITH MINOR WORDING CLEANUP** | Scope now defensible. |
| “physical parameter vector” wording | **MODIFY** | Use model-parameter vector. |
| Historical \(N_L,N_R,H\) equation in MASTER | **MODIFY / move out** | No longer formal-core variables. |
| Apply current pending patch literally | **REJECT** | Proposal metadata must be finalized. |
| G1 pass from reviewer agreement | **REJECT** | Agreement is not proof. |
| GO / implementation | **REJECT** | G1–G4 remain open. |

---

# 40. CURRENT G1 ASSESSMENT

After R2, GPT does **not** see a remaining equation-level contradiction in the reduced \(C_j\)-based nine-state formal plant.

That means:

> the formal candidate is internally coherent enough to be considered for adoption as the next MASTER formulation.

It does **not** mean G1 has passed.

G1 still requires:

- explicit adoption of the restricted model scope;
- final authoritative text review;
- parameter/function provenance before quantitative physical claims;
- separation of formal model consistency from real-platform correspondence.

---

# 41. G2 REMAINS UNVERIFIED

No certified:

\[
\widehat{\mathscr R}
\]

has been constructed.

G2 must prove:

\[
\mathscr R([0,T];x,V)
\subseteq
\widehat{\mathscr R}([0,T];x,V).
\]

Requirements:

- same held voltage for all hidden parameters;
- fixed parameter realization along each trajectory;
- continuous-time coverage;
- actuator/contact coupling preserved or soundly overapproximated;
- collision set preserved;
- contact-validity set preserved;
- no reliance on dense simulation alone;
- no unproved derivative regularity of the square-root margin at saturation.

---

# 42. G3 REMAINS UNVERIFIED

Need a useful nonempty:

\[
K_T
\]

with:

\[
K_T
\subseteq
\operatorname{Pre}_T^c(K_T).
\]

Need:

- non-oracle action selection;
- full-hold collision/contact safety;
- endpoint return;
- recursive feasibility;
- practical nontriviality.

Rest equilibrium alone does not establish usefulness.

---

# 43. G4 REMAINS UNVERIFIED

Novelty audit must now compare the actual narrowed scope:

- execution-fixed contact capacities;
- voltage-level electromechanical dynamics;
- reduced nonholonomic constrained-contact models;
- joint state/parameter reachability;
- inter-sample collision/contact admissibility;
- recursive filtering;
- fixed-parameter viability;
- full tire/support models;
- time-varying friction models.

Changing notation from \(\mu_jN_j\) to \(C_j\) is not novelty.

Removing unused \(\phi\) assumptions is not novelty.

Generic inclusion/predecessor logic is not novelty.

---

# 44. CLAIMS THAT REMAIN PROHIBITED

Do not claim:

- full tire/contact physics;
- validated real-platform contact safety;
- actual normal-load balance;
- load-transfer dynamics;
- roll/pitch safety;
- arbitrary lateral-skid safety;
- arbitrary changing-terrain safety;
- time-varying traction robustness;
- positive \(C_j\) guarantees stopping;
- sustained wheel lock as a mode;
- general straight-line robust invariance;
- voltage feasibility equals hardware feasibility;
- instantaneous feasibility equals recursive feasibility;
- certificate infeasibility means unavoidable collision;
- \(K_T\) equals exact viability;
- generic reachability induction is novelty;
- generic predecessor logic is novelty;
- old seven-state HOCBF results apply to current plant;
- moving-obstacle/multi-robot/variable-sampling theory;
- “first” without G4 evidence;
- Q1 readiness based on model agreement.

---

# 45. EXACT NEXT REQUEST TO CODEX

Codex should now prepare an **adoption-finalization proposal**, not implement the controller.

Required changes:

1. change “physical parameter vector” to “model-parameter vector”;
2. remove the explicit historical \(b(N_L-N_R)+Hmur=0\) derivation from future MASTER text;
3. retain only a concise physical-correspondence caveat in A3;
4. finalize all proposal/candidate/pending metadata;
5. insert actual adoption date only when approved;
6. preserve:
   - HOLD;
   - G1 NEEDS REVISION;
   - G2/G3/G4 UNVERIFIED;
7. do not change the mathematical \(C_j\)-based core otherwise unless a new issue is found;
8. return the **exact final adoption diff** for one last independent review before applying it to authoritative files.

Do not construct G2/G3 yet unless the user explicitly changes the workflow.

Do not implement code.

Do not conclude GO.

---

# 46. REQUIRED CODEX RESPONSE FORMAT

For the finalization proposal, respond with:

## Finding

What exact text changed.

## Evidence

Why it is required.

## Consequence

Effect on scope/authority/versioning.

## Status

One of:

- VALID
- NEEDS REVISION
- BLOCKER
- UNVERIFIED

## Required action

Exact next step.

Also provide a final table:

| Finalization item | Exact file | Exact section | Change | Gate effect |
|---|---|---|---|---|

---

# 47. BOTTOM LINE

Proposal R2 successfully implements the major scientific corrections from the previous review:

\[
\boxed{
\mu_jN_j
\rightarrow
C_j
}
\]

and removes oddness from the core.

The accepted reduced contact model is:

\[
\boxed{
F_j=C_j\phi(\sigma_j/v_s)
}
\]

with:

\[
\boxed{
F_j^2+Y_j^2\le C_j^2.
}
\]

Contact validity is:

\[
\boxed{
D_c(\vartheta)
=
\left\{
x:
|mur|
\le
\sum_{j=L,R}
\sqrt{
C_j^2-F_j^2
}
\right\}.
}
\]

The uncertainty is:

\[
\boxed{
\vartheta(t)\equiv\vartheta_0
}
\]

for the full execution.

The formal plant is now sufficiently coherent to be considered for the next MASTER candidate after the three mandatory edits.

However:

\[
\boxed{
\text{formal model coherence}
\neq
\text{G1 pass}
}
\]

and:

\[
\boxed{
\text{formal model safety}
\neq
\text{validated physical robot safety}.
}
\]

Current authoritative state remains:

\[
\boxed{
\text{MASTER v2 — HOLD}
}
\]

with:

- G1 NEEDS REVISION;
- G2 UNVERIFIED;
- G3 UNVERIFIED;
- G4 UNVERIFIED;
- no implementation authorization.
