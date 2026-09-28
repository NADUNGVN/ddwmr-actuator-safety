# GPT → CODEX HANDOFF — Independent Review of Proposed MASTER v2.1

**Purpose:** Complete handoff of GPT's independent review of Codex commit `094f3c8`, preserving all equation-level findings, patch decisions, scope corrections, and gate status without relying on chat history.

**Repository:** `NADUNGVN/ddwmr-actuator-safety`  
**Reviewed commit:** `094f3c8`  
**Current authoritative formulation:** `research_context/MASTER_RESEARCH_CONTEXT_v2.md`  
**Authority status:** MASTER v2 remains authoritative. All v2.1 files are proposals only.  
**Overall project status:** **HOLD**  
**Implementation status:** No controller/simulator/experiment implementation is authorized.  
**Gate status:** G1 NEEDS REVISION; G2/G3/G4 UNVERIFIED.

---

# 0. CODEX OPERATING INSTRUCTION FOR THIS HANDOFF

Treat this document as GPT's independent review evidence, **not** as an amendment to MASTER.

Do not silently edit assumptions. Do not infer GO from reviewer agreement. Do not treat model agreement as proof.

Before changing MASTER:

1. compare this handoff against the current authoritative MASTER;
2. compare it against:
   - `docs/reviews/CODEX_RESPONSE_TO_GPT_G1_v2_1.md`
   - `docs/proposals/v2_1/MASTER_v2_1_PREVIEW.md`
   - `docs/proposals/v2_1/MASTER_v2_1_PENDING.patch`
3. resolve every **MODIFY** or **REJECT** decision explicitly;
4. if proposing a new MASTER revision, preserve version traceability in `DECISION_LOG.md`;
5. keep overall status **HOLD**.

Use, for each substantive response:

**Finding / Evidence / Consequence / Status / Required action**

---

# 1. REVIEWED MATERIAL

GPT independently reviewed commit `094f3c8`, especially:

- `docs/reviews/CODEX_RESPONSE_TO_GPT_G1_v2_1.md`
- `docs/proposals/v2_1/MASTER_v2_1_PREVIEW.md`
- `docs/proposals/v2_1/MASTER_v2_1_PENDING.patch`
- `research_context/MASTER_RESEARCH_CONTEXT_v2.md`
- `research_context/DECISION_LOG.md`
- `research_context/REVIEW_GATE.md`

The current MASTER v2 remains the single source of truth.

---

# 2. CURRENT SCIENTIFIC CORE BEFORE ANY v2.1 ADOPTION

The active candidate remains a voltage-driven nine-state DDWMR:

\[
x=[p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R]^\top.
\]

Input:

\[
V=[V_L,V_R]^\top.
\]

The intended physical chain is:

\[
V\rightarrow i\rightarrow\omega\rightarrow\sigma\rightarrow F\rightarrow(u,r)\rightarrow(p,\theta).
\]

The current research question is no longer “apply sampled-data HOCBF to a DDWMR.” The core question is the gap between a mathematical safety command and what can be executed through finite voltage, electromechanical dynamics, and contact limitations.

However, after this review GPT recommends **narrowing the wording of physical claims**. The proposed reduced model should not be advertised as already proving safety of a real robot with fully validated tire/support mechanics.

HOCBF remains optional/baseline only.

Candidate theoretical methodology remains:

\[
\text{plant-structured robust reachable set/tube + sampled predecessor}.
\]

No reachable enclosure or recursive set has yet been constructed.

---

# 3. SUMMARY OF GPT DECISIONS ON B1–B6

| Item | GPT decision | Short reason |
|---|---|---|
| B1 Algebraic lateral reactions | **ACCEPT** | Valid closure of an ideal constrained planar model; no tenth dynamic state required. |
| B2 Typed state/parameter contact domain | **ACCEPT** | Corrects a real type/quantifier error; preserves fixed hidden parameter realization. |
| B3 Fixed normal loads | **MODIFY SUBSTANTIALLY** | Literal fixed \(N_L,N_R\) are not generally defensible as real wheel normal loads for a finite-height robot without support/load-transfer modeling. Replace with effective tangential contact capacities \(C_j\). |
| B4 Minimal \(\phi\) assumptions | **MODIFY** | Global monotonicity unnecessary; oddness should not be mandatory in the core unless needed for auxiliary symmetry. |
| B5 Mirror symmetry | **ACCEPT** | Correct: symmetry requires transformation of the entire side-dependent problem, not merely a symmetric friction interval. |
| B6 Fixed uncertainty over execution | **ACCEPT WITH SCOPE MODIFICATION** | Coherent first problem, but strictly narrower than time-varying traction uncertainty. |

---

# 4. B1 — ALGEBRAIC LATERAL REACTIONS

## Finding

Codex's B1 argument is mathematically correct. An exact \(v_y=0\) reduced plant can be closed using algebraic lateral constraint reactions without adding a tenth dynamic state.

## Evidence

Under the exact lateral constraint,

\[
Y_L+Y_R=mur.
\]

Suppose each side has available lateral capacity

\[
|Y_j|\le a_j.
\]

Then

\[
Y_L+Y_R=mur
\]

has a feasible solution iff

\[
|mur|\le a_L+a_R.
\]

For \(A=a_L+a_R>0\), the selection

\[
Y_j=\frac{mur\,a_j}{A}
\]

satisfies the force balance and \(|Y_j|\le a_j\). At \(A=0\), feasibility forces \(mur=0\), and \(Y_L=Y_R=0\) is admissible.

At the adopted contact locations \((0,\pm b)\), lateral reactions contribute zero yaw moment because their longitudinal lever arm is zero. Under \(v_y=0\), their mechanical power is zero:

\[
P_Y=Y_jv_{y,j}=0.
\]

Therefore the nine-state ODE does not need to depend on the individual allocation.

## Consequence

The ideal constrained planar model can be internally closed mathematically. This proves only existence of admissible algebraic reactions within a stipulated force budget. It does **not** prove a real tire constitutive law, maximum-dissipation Coulomb sliding behavior, real normal-load distribution, or real platform support balance.

## Status

**VALID**

## Required action

Keep the algebraic reaction structure, subject to the B3 correction below.

---

# 5. B2 — CORRECT STATE/PARAMETER TYPING AND ROBUST QUANTIFIERS

## Finding

Codex's B2 correction is fully valid and should be retained. The earlier object mixed state-space and state-parameter-space quantities.

## Evidence

For fixed unknown parameter realization \(\vartheta\),

\[
D_c(\vartheta)=\{x:c(x,\vartheta)\ge0\}.
\]

Define the joint set:

\[
\mathscr D_c=\{(x,\vartheta):\vartheta\in\Theta,\ x\in D_c(\vartheta)\}.
\]

Then

\[
\mathscr S_c=(\mathcal S\times\Theta)\cap\mathscr D_c.
\]

For the same held voltage \(V\), robust one-hold safety/contact admissibility requires:

\[
\exists V\in\mathcal U\quad\forall\vartheta\in\Theta\quad\forall t\in[0,T]:
\]

\[
(x_\vartheta(t;x_k,V),\vartheta)\in\mathscr S_c.
\]

An existential hidden-parameter projection such as

\[
\exists\vartheta:\ x\in D_c(\vartheta)
\]

is not a robust safety condition.

A conservative state-only set may be defined as

\[
\mathcal S_{\rm rob}=\mathcal S\cap\bigcap_{\vartheta\in\Theta}D_c(\vartheta).
\]

For joint reachability,

\[
\mathscr R(t;x,V)=\{(x_\vartheta(t;x,V),\vartheta):\vartheta\in\Theta\}.
\]

A joint enclosure should satisfy

\[
\mathscr R([0,T];x,V)\subseteq\widehat{\mathscr R}([0,T];x,V).
\]

A state-only enclosure may instead use

\[
\widehat{\mathcal R}_x([0,T])\times\Theta\subseteq\mathscr S_c,
\]

but this is more conservative and must not be called equivalent.

## Consequence

The robust quantifier order is correctly preserved:

\[
\exists V_k\quad\forall\vartheta\in\Theta.
\]

The same hidden fixed parameter realization must persist over the trajectory.

## Status

**VALID**

## Required action

Accept the typed joint objects and quantifier correction. Keep clear that state-only robust intersections are sufficient/conservative abstractions, not exact fixed-parameter viability objects.

---

# 6. B3 — FIXED NORMAL LOADS: KEY MODIFICATION

## Finding

Codex correctly identifies the physical problem with fixed wheel normal loads. GPT recommends a stronger and cleaner theoretical repair:

> **Do not use literal fixed \(N_L,N_R\) as physical normal loads in the theorem core.**

Instead introduce a reduced-model tangential contact-force capacity parameter:

\[
\boxed{C_j>0.}
\]

## Evidence

Consider two physical contacts at

\[
(0,\pm b,-H)
\]

relative to a finite-height COM. Under no roll acceleration and no extra roll moment,

\[
b(N_L-N_R)+H(Y_L+Y_R)=0.
\]

The ideal lateral constraint requires

\[
Y_L+Y_R=mur.
\]

Hence

\[
\boxed{b(N_L-N_R)+Hm ur=0.}
\]

If \(N_L=N_R\), then in that diagnostic model \(ur=0\). Thus equal fixed physical wheel normal loads are incompatible with generic turning for a finite-height two-contact rigid platform unless another support or moment contribution exists.

Similarly, longitudinal contact forces create pitch moments proportional to

\[
H(F_L+F_R).
\]

A caster, suspension, distributed support, body contact, or support moments can change these balances, but none is modeled in the nine-state core.

Therefore

\[
N_j=\text{fixed real wheel normal force}
\]

is not generically justified by the current reduced plant.

## Consequence

The current v2.1 preview is honest in calling physical correspondence open, but the notation \(\mu_jN_j\) still unnecessarily suggests a solved physical normal-load problem. The theorem only needs a bound on admissible tangential contact force.

## Recommended replacement

Define an effective per-wheel contact-force capacity:

\[
\boxed{C_j>0.}
\]

Use

\[
\boxed{F_j=C_j\phi(\sigma_j/v_s).}
\]

Adopt the combined tangential force envelope

\[
\boxed{F_j^2+Y_j^2\le C_j^2.}
\]

Then available lateral capacity is

\[
a_j=\sqrt{C_j^2-F_j^2}=C_j\sqrt{1-\phi^2(\sigma_j/v_s)}.
\]

Contact validity becomes

\[
\boxed{|mur|\le a_L+a_R.}
\]

Define

\[
C_j\in[\underline C_j,\overline C_j],
\]

fixed for the complete execution in the first theoretical core.

## Physical interpretation

MASTER should explicitly state:

> \(C_j\) is an effective per-wheel tangential contact-force capacity of the reduced planar model. It is not asserted to equal an instantaneous physical friction-normal-load product on a real platform. A relation such as \(C_j\approx\mu_jN_j\) requires separate support/load/contact justification or calibration on a declared operating envelope.

This avoids treating a 2-D reduced theorem as if it has solved 3-D load transfer.

## Status

**NEEDS REVISION**

## Patch decision

**MODIFY SUBSTANTIALLY**

Do not adopt the current fixed-\(N_j\) formulation unchanged.

## Required action

Replace \(\mu_j,N_j\) by \(C_j\) throughout the formal theoretical core: longitudinal force law, lateral force budget, parameter vector, \(D_c(\vartheta)\), \(\mathscr D_c\), \(\mathscr S_c\), robust predecessor, reachability targets, symmetry discussion, and novelty scope.

If the project later insists on actual \(\mu_jN_j\) physics, add a genuine support/load model or a separately justified mapping.

---

# 7. B4 — MINIMAL ASSUMPTIONS ON \(\phi\)

## Finding

Codex is correct that global monotonicity is unnecessary. GPT further recommends that oddness **not** be a mandatory core assumption unless a theorem uses it.

## Evidence

Energy dissipation requires only

\[
z\phi(z)\ge0.
\]

Well-posedness requires \(\phi\) globally Lipschitz. Combined force admissibility requires

\[
|\phi(z)|\le1.
\]

To exclude the degenerate v2 law \(\phi(z)\equiv0\), use

\[
\boxed{z\phi(z)>0\quad(z\neq0).}
\]

Global monotonicity is unnecessary for these arguments. Oddness

\[
\phi(-z)=-\phi(z)
\]

is only required for particular antisymmetric auxiliary subproblems, e.g. pure spin with matched left/right data.

## Recommended core assumption

Use one **known fixed** function \(\phi\) satisfying

\[
\phi(0)=0,
\]

\[
z\phi(z)>0\quad(z\neq0),
\]

\[
|\phi(z)|\le1,
\]

and

\[
|\phi(z_1)-\phi(z_2)|\le L_\phi|z_1-z_2|.
\]

Do not require global monotonicity, differentiability, oddness, or a uniform positive traction floor in the core.

## Consequence

This keeps the theoretical plant minimal. It does **not** prove minimum braking force, finite stopping time, finite stopping distance, or existence of a voltage policy that reaches a required negative-slip region.

## Status

**NEEDS REVISION**

## Patch decision

**MODIFY**

## Required action

Remove global monotonicity from any proposed core. Move oddness from the base assumptions to an auxiliary symmetry assumption unless the project deliberately selects a specific odd calibrated law such as `tanh`.

---

# 8. B5 — MIRROR SYMMETRY

## Finding

Codex's correction is correct. An exchange-symmetric uncertainty interval alone does not make the full problem mirror symmetric.

## Evidence

Let \(P\) denote reflection plus left/right exchange. The dynamical covariance statement is

\[
P x(t;x_0,V,\vartheta)=x(t;Px_0,PV,P\vartheta)
\]

when all side-dependent data are transformed consistently.

To make this a symmetry of the **same** robust problem, require

\[
P\Theta=\Theta.
\]

Also require the relevant known side parameters, initial set, admissible action set, and policy to transform compatibly.

Independent side uncertainty does not imply each trajectory is symmetric. At \(r=0\), with equal slip,

\[
\dot r=\frac{b}{I_z}(F_R-F_L).
\]

If \(C_L\neq C_R\) for the realized hidden parameters, then generally \(F_R-F_L\neq0\), so \(r=0\) is not robustly invariant.

## Consequence

Symmetry may be used only as a diagnostic, an auxiliary matched-side problem, or a computational reduction after proving complete problem invariance. It cannot justify the main robust straight-line reduction.

## Status

**VALID**

## Patch decision

**ACCEPT**, after replacing friction/load products by \(C_j\).

## Required action

Keep independent side capacities in the general core. State exact symmetry assumptions only in the corresponding auxiliary section.

---

# 9. B6 — FIXED UNCERTAINTY OVER THE COMPLETE EXECUTION

## Finding

The fixed-parameter scope is mathematically coherent and suitable as a first problem. It is strictly narrower than the original time-varying traction problem.

## Evidence

These three classes are different:

### Arbitrary measurable variation

\[
C_j(t)\in[\underline C_j,\overline C_j].
\]

### Hold-wise constant variation

\[
C_j(t)=C_{j,k}\quad t\in[kT,(k+1)T).
\]

### Execution-fixed hidden parameter

\[
C_j(t)\equiv C_j\quad\forall t.
\]

The proposed v2.1 uses the third. One can preserve this analytically by augmenting

\[
\dot\vartheta=0.
\]

A pointwise differential inclusion that permits parameter switching is only an outer relaxation. A state-only predecessor that checks every \(\vartheta\in\Theta\) at every sample is safe but conservative relative to a history-dependent policy that may learn fixed parameters.

## Consequence

The paper must **not** claim robustness to arbitrary changing terrain or arbitrary time-varying friction if v2.1 adopts fixed hidden parameters. G4 must compare against prior art under the correct fixed-parameter scope.

## Status

**VALID AS A SCOPE CHOICE**

## Patch decision

**ACCEPT WITH SCOPE MODIFICATION**

## Required action

Write explicitly:

> The first theoretical core treats contact and plant parameters as unknown but fixed over the entire execution.

Treat time-varying/spatially varying traction as a future extension, not as solved uncertainty.

---

# 10. PATCH-LEVEL ACCEPT / MODIFY / REJECT TABLE

| Proposed change | Decision | Reason |
|---|---|---|
| Exact axle-midpoint COM geometry | **ACCEPT** | Required by current kinematics/yaw dynamics. |
| Exact \(v_y=0\) theorem constraint | **ACCEPT** | Current equations are an exact constraint model, not an approximation. |
| Algebraic lateral reactions | **ACCEPT** | Valid closure of reduced constrained model. |
| Combined tangential force validity domain | **ACCEPT**, after capacity reformulation | Valid as ideal contact admissibility, not real tire law. |
| Fixed physical \(N_L,N_R\) in formal core | **REJECT IN PRESENT FORM** | Not generically compatible with finite-height roll/pitch/load balance. |
| Replace \(\mu_jN_j\) by effective \(C_j\) | **REQUIRED MODIFICATION** | Separates planar capacity from unresolved support mechanics. |
| Single wheel-side electromechanical conversion constant \(k_j\) | **ACCEPT** | Preserves ideal power conversion. |
| Ideal rigid backdrivable gear reduction | **ACCEPT** | Valid theorem idealization if clearly stated. |
| Ideal four-quadrant terminal-voltage source | **ACCEPT AS IDEALIZATION** | Needed to interpret signed terminal voltage consistently. |
| Exact sampled state | **ACCEPT AS IDEALIZATION** | Makes information pattern unambiguous. |
| Zero sensing/computation/actuation delay | **ACCEPT AS IDEALIZATION** | Required for first theorem. |
| Known fixed \(\phi\) | **ACCEPT** | Removes adversarial function-family ambiguity. |
| Strict sign preservation | **ACCEPT** | Removes degenerate \(\phi=0\) case. |
| Global monotonicity | **REJECT / unnecessary** | Not used by model-consistency arguments. |
| Global oddness as core assumption | **MODIFY** | Needed only for auxiliary reversal/pure-spin symmetry. |
| Fixed unknown parameters for complete execution | **ACCEPT** | Coherent narrowed problem. |
| Arbitrary time-varying friction claim | **REJECT for v2.1 core** | Not covered by fixed-parameter formulation. |
| Joint state/parameter reachable sets | **ACCEPT** | Correct quantifier/type structure. |
| \(\mathcal S_{\rm rob}\) state intersection | **ACCEPT AS CONSERVATIVE** | Sound sufficient state-only abstraction. |
| State-only robust predecessor | **ACCEPT AS SUFFICIENT TARGET** | Conservative but valid. |
| Sustained wheel lock as automatic mode | **REJECT** | Not supplied by ODE. |
| Transient \(\omega=0,u\neq0\) | **ACCEPT** | Valid state of nine-state model. |
| Straight-line braking as general robust reduction | **REJECT** | Broken by independent side uncertainty. |
| Straight-line matched-side auxiliary problem | **ACCEPT** | Valid with explicit symmetry assumptions. |
| HOCBF as mandatory method | **REJECT** | Remains optional/baseline only. |
| G1 pass merely because patch is coherent | **REJECT** | Physical scope and model adoption still require review. |
| GO / implementation authorization | **REJECT** | G1–G4 remain open. |

---

# 11. RECOMMENDED MINIMAL MASTER v2.1 FORMAL MODEL

## State

\[
\boxed{x=[p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R]^\top.}
\]

## Input

\[
\boxed{V=[V_L,V_R]^\top.}
\]

## Geometry

The planar COM projection equals the drive axle midpoint exactly. Contacts are \((0,+b)\) and \((0,-b)\). Body axes are forward/left/up. Positive yaw is counterclockwise. Positive wheel rate means forward rolling.

## Body kinematics

\[
\dot p_x=u\cos\theta,
\]

\[
\dot p_y=u\sin\theta,
\]

\[
\dot\theta=r.
\]

Exact theorem constraint:

\[
v_y\equiv0.
\]

## Contact longitudinal velocities

\[
v_L=u-br,
\]

\[
v_R=u+br.
\]

Slip velocity:

\[
\sigma_j=R_w\omega_j-v_j.
\]

## Longitudinal contact force

\[
\boxed{F_j=C_j\phi(\sigma_j/v_s).}
\]

with

\[
C_j\in[\underline C_j,\overline C_j],
\]

fixed but hidden over the entire execution.

## Contact-shape assumptions

One known fixed \(\phi\):

\[
\phi(0)=0,
\]

\[
z\phi(z)>0\quad(z\neq0),
\]

\[
|\phi(z)|\le1,
\]

\[
|\phi(z_1)-\phi(z_2)|\le L_\phi|z_1-z_2|.
\]

No default global monotonicity. No default oddness. No derivative assumption.

## Algebraic lateral reactions

\[
Y_L+Y_R=mur.
\]

Ideal tangential force budget:

\[
\boxed{F_j^2+Y_j^2\le C_j^2.}
\]

Available lateral capacity:

\[
a_j(x,\vartheta)=\sqrt{C_j^2-F_j^2}.
\]

Contact validity:

\[
\boxed{|mur|\le a_L+a_R.}
\]

Define

\[
D_c(\vartheta)=\left\{x:|mur|\le a_L(x,\vartheta)+a_R(x,\vartheta)\right\}.
\]

## Body dynamics

\[
m\dot u=F_L+F_R-c_uu,
\]

\[
I_z\dot r=b(F_R-F_L)-c_rr.
\]

No additive residual in the first core.

## Wheel dynamics

\[
J_j\dot\omega_j=k_ji_j-B_j\omega_j-R_wF_j.
\]

## Electrical dynamics

\[
L_j\dot i_j=V_j-R_ji_j-k_j\omega_j.
\]

## Voltage box

\[
|V_j|\le V_{\max}.
\]

## Digital execution

\[
V(t)=V_k,\qquad t\in[kT,(k+1)T).
\]

## Ideal source

Four-quadrant terminal-voltage source. Signed current is permitted. Regenerated electrical power may be absorbed/dissipated by the ideal source. No current limit, bus clipping, PWM ripple, thermal protection, open-circuit mode, or delay is part of the theorem core.

---

# 12. PARAMETER SEMANTICS

Let

\[
\vartheta=(m,I_z,R_w,b,v_s,c_u,c_r,J_L,J_R,B_L,B_R,L_L,L_R,R_L,R_R,k_L,k_R,C_L,C_R)\in\Theta.
\]

Requirements:

- \(\Theta\) is nonempty and compact;
- all inertias, inductances, resistances, radii, lengths, regularization speed, conversion constants and capacities have positive lower bounds;
- damping is nonnegative;
- physical correlations are preserved;
- \(\vartheta\) is fixed along the entire execution;
- controller knows \(\Theta\), not the true \(\vartheta\);
- analytical augmentation \(\dot\vartheta=0\) is allowed;
- parameter switching is not the exact plant.

Known parameters may be represented by singleton components.

---

# 13. CONTROLLER INFORMATION

First theorem assumption:

\[
x_k=x(kT)
\]

is known exactly.

Zero sensing delay, computation delay, and actuation delay.

Controller does not observe hidden \(\vartheta\). Controller does not choose \(Y_j\). Controller does not require contact-force measurements.

Estimated-state safety is a future extension.

---

# 14. SAFE / CONTACT SETS

Collision barrier:

\[
h(p)=\|p-p_o\|^2-R_s^2.
\]

Collision-safe set:

\[
\mathcal S=\{x:h(p)\ge0\}.
\]

Joint contact domain:

\[
\mathscr D_c=\{(x,\vartheta):\vartheta\in\Theta,\ x\in D_c(\vartheta)\}.
\]

Joint collision/contact domain:

\[
\boxed{\mathscr S_c=(\mathcal S\times\Theta)\cap\mathscr D_c.}
\]

Conservative state-only robust set:

\[
\mathcal S_{\rm rob}=\mathcal S\cap\bigcap_{\vartheta\in\Theta}D_c(\vartheta).
\]

Do not use \(x\in\mathcal S\cap\mathscr D_c\) because the spaces do not match. Do not existentially project hidden parameters.

---

# 15. ONE-HOLD SAFETY OBJECT

For fixed hidden parameter \(\vartheta\), trajectory:

\[
x_\vartheta(t;x,V).
\]

Joint reachable pairs:

\[
\mathscr R(t;x,V)=\{(x_\vartheta(t;x,V),\vartheta):\vartheta\in\Theta\}.
\]

One-hold safety/contact admissibility requires

\[
\exists V\in\mathcal U
\]

such that

\[
\mathscr R([0,T];x,V)\subseteq\mathscr S_c.
\]

Equivalent quantified form:

\[
\exists V\quad\forall\vartheta\in\Theta\quad\forall t\in[0,T]:
\]

\[
x_\vartheta(t;x,V)\in\mathcal S\cap D_c(\vartheta).
\]

This is not recursive feasibility.

---

# 16. ROBUST PREDECESSOR

For \(A\subseteq\mathcal S_{\rm rob}\), define

\[
\operatorname{Pre}_T^c(A)=\left\{x:\exists V\in\mathcal U\;\forall\vartheta\in\Theta:\begin{array}{l}
x_\vartheta(t;x,V)\in\mathcal S\cap D_c(\vartheta),\ \forall t\in[0,T],\\[1mm]
x_\vartheta(T;x,V)\in A
\end{array}\right\}.
\]

Candidate recursive set:

\[
\boxed{K_T\subseteq\operatorname{Pre}_T^c(K_T).}
\]

This implies only after proof and admissible repeated input selection: sampled-state membership in \(K_T\) and continuous collision/contact admissibility.

It does not establish exact viability equality, continuous-time invariance of \(K_T\), or physical inevitability of collision when the certificate fails.

---

# 17. HOCBF STATUS

HOCBF remains optional candidate, baseline, local regular-domain comparison, or literature bridge.

Do not restore sampled-data HOCBF for DDWMR as the primary novelty statement.

The old seven-state relative-degree derivation remains historical and cannot be transferred as a result for the nine-state plant.

---

# 18. WHEEL-ZERO / LOCK STATUS

The model admits

\[
\omega_j=0,\qquad u\neq0.
\]

This may occur transiently.

Sustained wheel lock requires torque balance

\[
k_ji_j=R_wF_j
\]

and compatible electrical dynamics. Under differentiability,

\[
V_j(t)=\frac{R_w}{k_j}\left(L_j\dot F_j+R_jF_j\right).
\]

A ZOH voltage can maintain lock only for special trajectories satisfying this expression with a constant admissible voltage over the hold.

Therefore there is no automatic wheel-lock mode, no mechanical brake, and no guaranteed locked-wheel emergency policy.

---

# 19. BRAKING AUTHORITY STATUS

Even after strict sign preservation of \(\phi\), no stopping guarantee exists automatically.

A stopping theorem still requires proving:

1. a voltage-admissible policy;
2. that the policy generates the necessary negative slip;
3. that the slip stays in a region with enough braking force;
4. low-speed behavior;
5. remaining travel;
6. consistency with the contact-validity domain.

Do not claim \(\underline C_j>0\) alone implies finite stopping distance.

Straight-line braking remains an auxiliary matched-side subproblem only.

---

# 20. SYMMETRY STATUS

General independent side uncertainty does not preserve \(r=0\). At equal slip,

\[
\dot r=\frac{b}{I_z}(F_R-F_L).
\]

Matched straight-line reduction requires explicit side equality conditions.

Mirror covariance

\[
P x(t;x_0,V,\vartheta)=x(t;Px_0,PV,P\vartheta)
\]

holds only with consistent transformation of all side-dependent data.

Symmetry of the same robust problem requires \(P\Theta=\Theta\) plus compatible initial/action sets or policy.

Pure-spin antisymmetry requires an odd \(\phi\) in that auxiliary analysis. Oddness is not a mandatory global core assumption.

---

# 21. PHYSICAL CLAIM BOUNDARY

This is a key conclusion.

The revised model should be described as:

> **a reduced ideal planar constrained-contact DDWMR with voltage-driven electromechanical dynamics and bounded per-wheel tangential contact capacity.**

It should **not** be advertised as already proving full physical tire behavior, real 3-D normal-load balance, load transfer, roll/pitch stability, arbitrary lateral skid safety, validated hardware-driver feasibility, or arbitrary changing-terrain traction safety.

Suggested research-question wording:

> **When can continuous collision safety be certified for a voltage-driven differential-drive robot within a reduced electromechanical/contact model that explicitly represents finite actuator dynamics and bounded tangential contact authority?**

Motivation may still state:

> The objective is to study the gap between kinematic safety commands and finite actuator/contact authority.

But correspondence to a specific physical robot requires platform/support model justification, an experimentally justified operating domain, or a certified model-error extension.

---

# 22. CLAIMS THAT REMAIN PROHIBITED

Do not claim:

- uniform relative degree 3 for the nine-state plant;
- regular degree 4 at the previous singularity;
- entire geometric safe set invariant;
- instantaneous feasibility implies recursive safety;
- certificate failure proves unavoidable collision;
- \(K_T\) equals exact viability;
- old seven-state HOCBF derivative results apply to current plant;
- time-varying traction robustness under a fixed-parameter theorem;
- \(C_j\) is a proven instantaneous physical \(\mu_jN_j\);
- algebraic reaction feasibility validates a tire law;
- full lateral-skid safety;
- fixed contact capacities validate roll/pitch/load-transfer physics;
- positive capacity implies stopping distance;
- zero wheel speed gives persistent lock;
- straight-line auxiliary result proves the independent-side general case;
- voltage feasibility equals complete hardware feasibility;
- generic tube inclusion logic is novelty;
- generic predecessor induction is novelty;
- moving-obstacle or multi-robot theorem;
- variable-sampling novelty;
- “first” without full G4 audit;
- Q1 readiness based on model agreement.

---

# 23. G1 STATUS AFTER THIS REVIEW

GPT does **not** recommend passing G1 yet.

The following can be accepted as coherent modeling choices:

- exact axle-midpoint COM geometry;
- exact \(v_y=0\);
- ideal algebraic reactions;
- wheel-side power-consistent electromechanical model;
- exact sampled state;
- ideal four-quadrant voltage source;
- fixed hidden parameter vector;
- typed joint state/parameter contact domain.

However, before adopting v2.1:

1. replace literal physical \(N_j,\mu_j\) with effective \(C_j\) in the formal core;
2. remove unnecessary global monotonicity;
3. remove default global oddness unless explicitly desired;
4. rewrite physical claims to match the reduced-model scope;
5. ensure all definitions and G4 scope use fixed hidden parameters, not time-varying terrain.

After those changes, perform another G1 review of the **actual revised MASTER text**.

Even then G2 remains UNVERIFIED, G3 remains UNVERIFIED, G4 remains UNVERIFIED, and overall remains HOLD.

---

# 24. G2 REQUIREMENTS AFTER ANY v2.1 ADOPTION

Do not start from a state-only generic box without checking correlation loss.

G2 must construct an actual enclosure

\[
\widehat{\mathscr R}
\]

satisfying

\[
\mathscr R([0,T];x,V)\subseteq\widehat{\mathscr R}([0,T];x,V).
\]

It must:

- use one held voltage;
- preserve fixed parameter dependence or explicitly overapproximate it;
- include motor/current/wheel/body coupling;
- certify the full continuous hold;
- certify collision safety;
- certify contact-domain validity;
- avoid assuming the safety result to prove the validity domain;
- quantify conservatism if state/parameter dependence is relaxed.

A generic Lipschitz ball alone is not automatically a meaningful contribution.

---

# 25. G3 REQUIREMENTS

Need a constructive, nontrivial

\[
K_T
\]

with

\[
K_T\subseteq\operatorname{Pre}_T^c(K_T).
\]

Need admissible input-selection, no oracle access to true hidden parameters, full-hold collision/contact safety, endpoint return, and nontrivial practical usefulness.

Rest equilibrium alone is not sufficient evidence of a useful recursive safe set.

Failure of the chosen certificate does not prove unavoidable collision.

---

# 26. G4 REQUIREMENTS UNDER THE NARROWED SCOPE

Literature comparison must now explicitly distinguish:

- fixed unknown contact capacity;
- time-varying friction;
- full tire/contact dynamics;
- reduced nonholonomic constrained models;
- sampled-data inter-sample safety;
- robust joint state/parameter reachability;
- recursive safe filtering;
- actuator-voltage-level models.

Update the literature matrix after the plant/theorem target is adopted.

Do not claim absence of prior work from unverified matrix cells.

---

# 27. EXACT NEXT REQUEST TO CODEX

Codex should now:

1. revise the pending v2.1 proposal rather than apply it unchanged;
2. replace \(\mu_j,N_j\) with effective \(C_j\) in the formal core;
3. retain the fixed-normal-load discussion only as historical/rejected reasoning or as an explanation of why \(C_j\) is introduced;
4. remove unnecessary global monotonicity;
5. move oddness to the auxiliary symmetry subsection unless deliberately retained with a stated reason;
6. rewrite the physical-scope language to make the reduced-model limitation explicit;
7. update:
   - MASTER preview;
   - pending patch;
   - DECISION_LOG pending entry;
   - REVIEW_GATE candidate text;
   - LITERATURE_MATRIX scope note;
8. preserve all gate statuses as open;
9. return the revised proposal for independent review before modifying the authoritative MASTER.

Do not implement code. Do not conclude GO.

---

# 28. REQUIRED CODEX RESPONSE FORMAT

For each major proposed change, respond using:

## Finding

What was changed or retained.

## Evidence

Equation-level justification.

## Consequence

Effect on plant/theorem/scope.

## Status

Choose:

- VALID
- NEEDS REVISION
- BLOCKER
- UNVERIFIED

## Required action

Exact next action.

Also include a final table:

| Proposal item | Codex decision | Exact file/section changed | Remaining obligation |
|---|---|---|---|

---

# 29. BOTTOM LINE

GPT's review accepts most of the formal structure in Codex's proposed v2.1, especially algebraic lateral reactions, typed joint state/parameter sets, fixed hidden parameter semantics, and explicit ideal actuation/information assumptions.

The major required correction is:

\[
\boxed{\mu_jN_j\longrightarrow C_j}
\]

for the theoretical core.

This prevents the reduced 2-D model from silently implying a resolved 3-D normal-load/support problem.

Recommended formal contact model:

\[
\boxed{F_j=C_j\phi(\sigma_j/v_s)}
\]

and

\[
\boxed{F_j^2+Y_j^2\le C_j^2.}
\]

Then

\[
\boxed{D_c(\vartheta)=\left\{x:|mur|\le\sum_{j=L,R}\sqrt{C_j^2-F_j^2}\right\}.}
\]

The resulting theory remains an **ideal reduced constrained-contact model**, not a validated full tire/platform model.

Project status remains:

\[
\boxed{\text{HOLD}}.
\]

No G1 pass. No G2/G3/G4 pass. No implementation authorization.
