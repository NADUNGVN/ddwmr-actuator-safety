# G3 candidate — zero-terminal-voltage energy backup seed

**Status:** candidate theorem note for independent review; not an accepted G3 result, not a gate change, not implementation authorization.  
**Repository state used:** `main` after `a1bf1541c5c2f6f008d2fa91182c7b0f22c82566`.  
**Authoritative model:** `research_context/MASTER_RESEARCH_CONTEXT_v2.md` (v2.1).  
**Project status remains:** `HOLD`; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.

## 1. Purpose

The immediate paper-gate question is whether the adopted nine-state voltage-driven DDWMR has a **specific, non-oracle, moving robust recursive seed** before any large G3 kernel/predecessor implementation is attempted.

This note derives one candidate based on the exact electromechanical power identity under the admissible held input

\[
V_B=(0,0).
\]

`V=0` is used exactly as MASTER defines it: a closed zero-terminal-voltage RL boundary condition. It is **not** interpreted as open-circuit coasting, a mechanical brake or a wheel-lock mode.

The core observation is that, for the adopted force/sign conventions, contact dissipation enters the stored-energy derivative as `-F_j sigma_j <= 0`. This can support a robust low-energy backup region without requiring equal left/right capacities or a monotone braking-force assumption.

The generic ideas “backup set”, “Lyapunov sublevel set” and “recursive safety” are prior art. Any eventual contribution must therefore be tied to the exact voltage/contact construction, its fixed-hidden-parameter quantifiers, the simultaneous collision/contact proof, and a matched-baseline decision advantage.

---

## 2. Plant quantities used

Let

\[
z=(u,r,\omega_L,\omega_R,i_L,i_R).
\]

For a fixed hidden parameter realization `vartheta`, define the stored internal energy

\[
E_{\vartheta}(z)
=
\frac12 m u^2
+\frac12 I_z r^2
+\sum_{j\in\{L,R\}}
\left(
\frac12 J_j\omega_j^2
+\frac12 L_j i_j^2
\right).
\]

The adopted dynamics are

\[
m\dot u=F_L+F_R-c_u u,
\]

\[
I_z\dot r=b(F_R-F_L)-c_r r,
\]

\[
J_j\dot\omega_j=k_j i_j-B_j\omega_j-R_wF_j,
\]

\[
L_j\dot i_j=V_j-R_ji_j-k_j\omega_j,
\]

with

\[
F_j=C_j\phi(\sigma_j/v_s),
\qquad
\sigma_L=R_w\omega_L-u+br,
\qquad
\sigma_R=R_w\omega_R-u-br.
\]

MASTER assumes `C_j>0`, `v_s>0`, `phi(0)=0` and strict sign preservation

\[
s\phi(s)>0\quad(s\neq0).
\]

Therefore

\[
F_j\sigma_j
=C_j\phi(\sigma_j/v_s)\sigma_j\ge0.
\]

---

## 3. Exact energy identity under a held voltage

Differentiate `E_vartheta` and substitute the plant equations. The motor torque/back-EMF terms cancel pairwise. The body/wheel contact-power sum is

\[
F_L(u-br)+F_R(u+br)-R_wF_L\omega_L-R_wF_R\omega_R
=-F_L\sigma_L-F_R\sigma_R.
\]

Hence

\[
\boxed{
\dot E_{\vartheta}
=
\sum_j i_jV_j
-c_u u^2-c_r r^2
-\sum_j B_j\omega_j^2
-\sum_j R_j i_j^2
-\sum_j F_j\sigma_j.
}
\]

For the backup input `V_B=(0,0)`,

\[
\boxed{
\dot E_{\vartheta}
\le
-c_u u^2-c_r r^2
-\sum_j B_j\omega_j^2
-\sum_j R_j i_j^2.
}
\]

This result does **not** assume that longitudinal contact force always opposes body speed. It uses only the declared slip-force power sign `F_j sigma_j >= 0`.

---

## 4. Theorem-local damping condition

MASTER allows nonnegative mechanical damping. The candidate below requires a restricted quantitative parameter domain with strictly positive uniform lower bounds

\[
\underline c_u>0,
\quad
\underline c_r>0,
\quad
\underline B_L>0,
\quad
\underline B_R>0,
\quad
\underline R_L>0,
\quad
\underline R_R>0.
\]

`R_j` already has a positive lower bound in MASTER; positivity of the mechanical damping terms is an additional theorem-local restriction on the chosen `Theta`, not a claim that MASTER globally requires it.

Let the corresponding upper inertia/inductance bounds be finite and define

\[
\lambda
=
\min\left\{
\frac{2\underline c_u}{\overline m},
\frac{2\underline c_r}{\overline I_z},
\frac{2\underline B_L}{\overline J_L},
\frac{2\underline B_R}{\overline J_R},
\frac{2\underline R_L}{\overline L_L},
\frac{2\underline R_R}{\overline L_R}
\right\}>0.
\]

Then, for every fixed hidden realization,

\[
\boxed{
\dot E_{\vartheta}\le-\lambda E_{\vartheta}
}
\]

and therefore

\[
E_{\vartheta}(t)\le e^{-\lambda t}E_{\vartheta}(0).
\]

This is a sufficient bound. Contact dissipation is discarded from `lambda`, so uncertainty in `C_L,C_R` does not weaken this decay estimate.

---

## 5. Capacity-only hidden-uncertainty specialization

The cleanest first G3 target is the scientifically central uncertainty class where the hidden positive-width labels are `C_L,C_R` (independent intervals are allowed), while the coefficients appearing in `E` and `lambda` are known fixed data.

This remains a positive-width hidden-parameter problem and preserves the important independent-side contact uncertainty. It does **not** impose `C_L=C_R` and does not use straight-line symmetry.

In this specialization, write simply

\[
E(z)=E_{\vartheta}(z),
\]

because the energy weights are known and do not depend on the hidden capacities.

From the energy bound,

\[
|u(t)|
\le
\sqrt{\frac{2E(0)}{m}}e^{-\lambda t/2}.
\]

Thus the total future translation length under `V_B=0` is bounded by

\[
\int_0^\infty |u(t)|\,dt
\le
\Gamma_0\sqrt{E(0)},
\qquad
\Gamma_0=\frac{2}{\lambda}\sqrt{\frac{2}{m}}.
\]

This is a path-length bound, not a claim that body speed is monotonically decreasing and not a claim that any particular contact force is a mechanical brake.

---

## 6. Robust low-energy contact-admissibility threshold

Collision safety alone is insufficient. The backup trajectory must remain in every true parameter-specific contact domain.

For a uniform energy level `E <= e`,

\[
|u|\le\sqrt{\frac{2e}{\underline m}},
\qquad
|r|\le\sqrt{\frac{2e}{\underline I_z}},
\qquad
|\omega_j|\le\sqrt{\frac{2e}{\underline J_j}}.
\]

Hence

\[
|\sigma_j|\le s_j\sqrt e,
\]

where a valid uniform coefficient is

\[
s_j
=\sqrt2\left(
\frac{\overline R_w}{\sqrt{\underline J_j}}
+\frac{1}{\sqrt{\underline m}}
+\frac{\overline b}{\sqrt{\underline I_z}}
\right).
\]

Because `phi(0)=0` and `phi` is globally Lipschitz,

\[
|\phi(\sigma_j/v_s)|
\le
\alpha_j\sqrt e,
\qquad
\alpha_j=\frac{L_\phi s_j}{\underline v_s}.
\]

Choose `e_c>0` so that

\[
\alpha_j^2 e_c<1,
\qquad j=L,R,
\]

and

\[
\boxed{
\underline C_L\sqrt{1-\alpha_L^2e_c}
+
\underline C_R\sqrt{1-\alpha_R^2e_c}
-
\frac{2\overline m}{\sqrt{\underline m\,\underline I_z}}e_c
\ge0.
}
\]

Such a positive `e_c` always exists under the stated bounds because the left-hand side is continuous and equals `underline C_L+underline C_R>0` at `e=0`.

For any fixed realization with `E_vartheta<=e_c`, the MASTER contact margin satisfies

\[
c(x,\vartheta)
= a_L+a_R-|mur|\ge0.
\]

Therefore the whole energy sublevel `E_vartheta<=e_c` lies inside the true parameter-specific contact domain. No derivative of the square-root contact margin is used.

---

## 7. Candidate capacity-robust backup set

For one static circular obstacle define clearance

\[
d(p)=\|p-p_o\|-R_s.
\]

Consider

\[
\boxed{
K_E
=
\left\{x:
E(z)\le e_c,
\quad
d(p)\ge\Gamma_0\sqrt{E(z)}
\right\}.
}
\]

### Proposition 1 — continuous backup invariance for capacity-only hidden uncertainty

Under the assumptions above, the common held action

\[
V_B=(0,0)
\]

keeps every trajectory starting in `K_E` collision-safe and contact-admissible for all time and for every fixed independent capacity realization

\[
(C_L,C_R)\in[\underline C_L,\overline C_L]\times[\underline C_R,\overline C_R].
\]

Moreover `K_E` is forward invariant under the backup action.

### Proof sketch

The contact statement follows from `E(t)<=E(0)<=e_c` and Section 6.

For collision clearance,

\[
\dot d
=\frac{(p-p_o)^\top}{\|p-p_o\|}\,u
\begin{bmatrix}\cos\theta\\\sin\theta\end{bmatrix}
\ge-|u|.
\]

Also, where `E>0`,

\[
\frac{d}{dt}\sqrt E
=\frac{\dot E}{2\sqrt E}
\le-\frac\lambda2\sqrt E.
\]

Therefore for

\[
b_E(x)=d(p)-\Gamma_0\sqrt E,
\]

\[
\dot b_E
\ge
-\sqrt{\frac{2E}{m}}
+\Gamma_0\frac\lambda2\sqrt E
=0.
\]

The `E=0` point is handled by continuity. Thus `b_E>=0` is preserved. Since `E<=e_c` is also preserved, `K_E` is invariant.

### Quantifiers

The policy is non-oracle:

\[
\forall x\in K_E,
\quad
\exists V_B=(0,0),
\quad
\forall(C_L,C_R),
\quad
\forall t\ge0:
\ x(t)\in\mathcal S\cap D_c(C_L,C_R).
\]

Consequently, for every sampling period `T>0`,

\[
K_E\subseteq\operatorname{Pre}_T^c(K_E).
\]

No parameter is reset between holds.

---

## 8. Nontrivial moving extent

`K_E` is not merely the rest equilibrium.

At any position with strict geometric clearance `d(p)>0`, sufficiently small but nonzero internal states satisfy

\[
0<E(z)<\min\left\{e_c,\left(\frac{d(p)}{\Gamma_0}\right)^2\right\}.
\]

In particular, states with `u != 0` exist in the interior of the certified region. Therefore the set has positive extent beyond rest states.

This does **not** yet prove mission/task usefulness. The backup action dissipates energy and tends toward rest. For a journal contribution this set should be treated as a certified recursive **terminal/backup seed** that enables a larger action-selecting safe set, not as the full operating policy by itself.

---

## 9. Extension to hidden uncertainty in the energy weights

If `m,I_z,J_j,L_j` are also hidden, the physical energy depends on the unknown fixed realization. Define the state-only upper energy

\[
E^+(z)=
\frac12\overline m u^2
+\frac12\overline I_z r^2
+\sum_j\left(
\frac12\overline J_j\omega_j^2
+\frac12\overline L_j i_j^2
\right).
\]

For every hidden realization,

\[
E_{\vartheta}(z)\le E^+(z)\le\rho E_{\vartheta}(z),
\]

where

\[
\rho=
\max\left\{
\frac{\overline m}{\underline m},
\frac{\overline I_z}{\underline I_z},
\frac{\overline J_L}{\underline J_L},
\frac{\overline J_R}{\underline J_R},
\frac{\overline L_L}{\underline L_L},
\frac{\overline L_R}{\underline L_R}
\right\}\ge1.
\]

Let

\[
q=e^{-\lambda T/2}.
\]

Then one hold under `V_B=0` gives

\[
E^+(z(T))\le\rho q^2 E^+(z(0)).
\]

A state-only endpoint-return proof that **rechecks the full original parameter set** requires

\[
\boxed{\sqrt\rho\,q<1.}
\]

Equivalently,

\[
T>\frac{\log\rho}{\lambda}.
\]

This condition is not a physical parameter-reset statement. It is the conservatism price of using a single state-only energy envelope after forgetting which fixed realization generated the endpoint.

Define

\[
\Gamma_T
=
\frac{2}{\lambda}\sqrt{\frac{2}{\underline m}}
\frac{1-q}{1-\sqrt\rho\,q}.
\]

Because `rho>=1`, `Gamma_T` is at least the full-tail coefficient `2/lambda*sqrt(2/underline m)` whenever the condition above holds.

A sufficient state-only sampled seed is then

\[
\boxed{
K_{E,T}^+
=
\{x:\ E^+(z)\le e_c,\ d(p)\ge\Gamma_T\sqrt{E^+(z)}\}.
}
\]

For every `x in K_{E,T}^+`, every hidden fixed realization, and the common action `V=0`, continuous collision/contact safety holds over `[0,T]` and

\[
x_{\vartheta}(T;x,0)\in K_{E,T}^+.
\]

The endpoint proof uses

\[
\int_0^T |u(t)|dt
\le
\frac{2}{\lambda}\sqrt{\frac{2E^+(0)}{\underline m}}(1-q)
\]

and

\[
\sqrt{E^+(T)}\le\sqrt\rho q\sqrt{E^+(0)}.
\]

The chosen `Gamma_T` makes the clearance consumed during the hold plus the reinitialized robust endpoint buffer no larger than the initial buffer.

### Interpretation

This exposes a concrete distinction between:

1. fixed-parameter physical execution; and
2. MASTER's conservative state-only predecessor that rechecks all of `Theta` at every sample.

When only capacities are hidden, `rho=1` and the artificial relabeling penalty disappears. When energy weights are hidden, `rho>1` produces an explicit state-only recursion penalty.

This may be scientifically useful even if the eventual paper retains the simpler capacity-only theorem, because it quantifies a source of conservatism that is otherwise only described qualitatively in MASTER.

---

## 10. Relation to prior art and novelty boundary

The following are **not** available novelty claims:

- backup control barrier functions / backup sets;
- Lyapunov sublevel backup regions;
- braking-aware safety constraints;
- robust backup tubes under uncertain dynamics;
- adaptive backup CBFs for parametric uncertainty;
- recursive invariant-set logic.

Direct threats include:

1. Chen, Jankovic, Santillo, Ames, *Backup Control Barrier Functions: Formulation and Comparative Study*, CDC 2021, DOI `10.1109/CDC45484.2021.9683111`.
2. van Wijk, Coogan, Molnar, Majji, Hobbs, *Disturbance-Robust Backup Control Barrier Functions: Safety Under Uncertain Dynamics*, IEEE L-CSS 2024, DOI `10.1109/LCSYS.2024.3514998`.
3. Gacsi, Kiss, Molnar, *Braking within Barriers: Constructive Safety-Critical Control for Input-Constrained Vehicles via the Backup Set Method*, arXiv `2510.15797` (2025): systematic backup-set/controller synthesis via feedback linearization and continuous-time Lyapunov equations, including split-friction vehicle braking.
4. Das, van Wijk, Molnar, Ames, Burdick, *Robust Adaptive Backup Control Barrier Functions*, arXiv `2607.20842` (2026): backup safety with parametric uncertainty and certified parameter-estimation bounds.
5. Energy-based CBF literature for robotic systems/manipulators, including kinetic-energy safe sets and damping-based safety control.

Therefore the candidate contribution, if any, must be narrower:

> a closed-form robust backup seed for the **voltage-driven electromechanical/contact DDWMR** derived from the exact power identity, with independent fixed hidden contact capacities, simultaneous continuous collision and algebraic-contact admissibility, and a quantified state-only rechecking penalty for broader fixed parameter uncertainty.

Even that is only a **plausible contribution hypothesis** until an equation-level novelty audit verifies that the exact construction is absent from the closest sources.

---

## 11. Paper-value test

This seed alone is insufficient for the target journal paper because the backup policy is always `V=0` and asymptotically dissipative. It provides a strong terminal/backup object, not useful task execution by itself.

The journal-grade next construction should use `K_E` or `K_{E,T}^+` as a terminal set and define a larger one-hold recoverability/action set

\[
K_{\mathrm{rec}}
=
\left\{x:
\exists V\in\mathcal U\ \forall\vartheta\in\Theta:
\begin{array}{l}
x_\vartheta(t;x,V)\in\mathcal S\cap D_c(\vartheta),\ \forall t\in[0,T],\\
x_\vartheta(T;x,V)\in K_E
\end{array}
\right\}.
\]

A useful safety filter can then select task-compatible nonzero voltages while retaining `V=0` as a certified terminal backup once the state is inside the seed.

The substantive paper discriminator should be predeclared as:

- same plant, same `Theta`, same voltage/action grid or optimization domain, same collision/contact predicate;
- generic validated-reachability / generic backup baseline versus the plant-structured energy-seed construction;
- at least one moving state/action where the proposed construction changes the certified safe-action decision or enlarges certified recoverability for a structural reason;
- no resource-cap, arithmetic-precision or unmatched-assumption explanation accepted as the contribution.

---

## 12. Immediate proof obligations before implementation

### Finding

The candidate supplies a concrete moving recursive seed under explicit damping restrictions and independent positive-width capacity uncertainty.

### Evidence

Sections 3–8 derive the energy identity, exponential decay, robust contact threshold and collision-clearance invariant using one common `V=(0,0)` action for every hidden capacity realization.

### Consequence

The previous feasibility blocker “no moving robust seed is known” is no longer empty: there is now a specific candidate theorem worth adversarial review. It does **not** yet establish G3 or novelty.

### Status

`CANDIDATE — NEEDS INDEPENDENT PROOF AUDIT`.

### Required action

Before any controller/kernel implementation:

1. independently rederive the exact energy identity and all signs;
2. verify that the intended quantitative `Theta` has the required strictly positive mechanical damping lower bounds, or weaken the theorem without silently adding them;
3. audit the `e_c` contact threshold against the original algebraic inequalities and units;
4. audit the nonsmooth points `E=0` and obstacle-distance differentiability boundary;
5. compare the exact theorem against Gacsi–Kiss–Molnar 2025, robust backup CBF 2024/2026, and energy-based CBF literature at equation/theorem level;
6. only after 1–5 pass, build a recoverability/action construction from moving states into this seed and predeclare a matched baseline criterion.

No numerical batch is authorized by this note.

---

## 13. Paper Gate interpretation

If this candidate survives independent proof and novelty review, the paper architecture becomes materially clearer:

1. exact voltage/contact DDWMR power structure;
2. closed-form capacity-robust terminal backup seed;
3. sampled state-only robust extension for broader fixed labels;
4. certified one-hold recoverability/action selection into the seed;
5. full-hold collision/contact theorem;
6. matched prior-art decision/coverage comparison;
7. reproducible journal evidence.

If the seed fails because the required damping restriction cannot be justified, or if the exact construction is already covered by prior art with no DDWMR-specific scientific separation, stop this branch before implementation and return to hypothesis revision.

**Gate statuses remain unchanged.**
