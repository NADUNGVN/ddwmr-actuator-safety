# G3 J1 independent proof audit — zero-voltage energy backup seed

**Reviewed artifact:** `research/theorem_notes/G3_ZERO_VOLTAGE_ENERGY_BACKUP_SEED_v1.md`  
**Review mode:** analytic/adversarial derivation only; no solver, simulator, controller or numerical batch executed.  
**Disposition:** `SEED_PROOF_SURVIVES_WITH_REVISIONS`  
**Gate effect:** none. Overall `HOLD`; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.

## 1. Executive result

The core capacity-only theorem candidate survives independent rederivation:

- the exact stored-energy identity has the stated signs;
- under `V=(0,0)` and explicit strictly positive damping lower bounds, stored internal energy decays exponentially;
- the collision buffer `d(p) >= Gamma_0 sqrt(E)` is forward invariant under the zero-terminal-voltage backup;
- a sufficiently small energy sublevel lies uniformly inside every parameter-specific algebraic contact domain for independent positive-width `C_L,C_R` intervals;
- the resulting set contains moving states of positive extent and uses one common non-oracle voltage for all hidden capacities.

The broader state-only extension with hidden energy weights is also mathematically plausible and its `rho` reset penalty is correctly motivated, but the note should be revised to make several proof boundaries explicit before it is treated as a theorem candidate for paper use.

The surviving result is a **terminal/backup seed**, not yet a useful G3 action policy and not yet a novelty result.

---

## 2. Audit of the exact power identity

### Finding

The energy derivative in the candidate is correct for the adopted nine-state ODE and force conventions.

### Evidence

Use

\[
E_\vartheta=
\frac12mu^2+\frac12I_zr^2+
\sum_j\left(\frac12J_j\omega_j^2+\frac12L_ji_j^2\right).
\]

Then

\[
\dot E_\vartheta
=u(F_L+F_R-c_u u)
+r(b(F_R-F_L)-c_r r)
\]

\[
+\sum_j\omega_j(k_ji_j-B_j\omega_j-R_wF_j)
+\sum_ji_j(V_j-R_ji_j-k_j\omega_j).
\]

The motor conversion terms cancel exactly:

\[
\omega_jk_ji_j-i_jk_j\omega_j=0.
\]

For the contact terms,

\[
u(F_L+F_R)+br(F_R-F_L)
=F_L(u-br)+F_R(u+br)
=F_Lv_L+F_Rv_R.
\]

Therefore

\[
F_jv_j-R_wF_j\omega_j
=-F_j(R_w\omega_j-v_j)
=-F_j\sigma_j.
\]

Hence

\[
\boxed{
\dot E_\vartheta
=\sum_ji_jV_j-c_uu^2-c_rr^2
-\sum_jB_j\omega_j^2-\sum_jR_ji_j^2
-\sum_jF_j\sigma_j.
}
\]

Because

\[
F_j\sigma_j=C_j\phi(\sigma_j/v_s)\sigma_j\ge0
\]

under the MASTER sign-preserving traction law, contact is dissipative in this stored-energy balance.

### Consequence

The candidate does not need a separate assumption that `F_j` opposes body speed, and it does not interpret `V=0` as a mechanical brake.

### Status

`VALID`.

### Required action

None for the sign identity. Preserve the exact conventions in any later manuscript proof.

---

## 3. Exponential decay under zero terminal voltage

### Finding

The stated exponential bound is valid only on a theorem-local parameter domain with strictly positive lower bounds for every quadratic dissipative channel used to dominate the stored energy.

### Evidence

For `V=0`,

\[
\dot E_\vartheta
\le-c_uu^2-c_rr^2-\sum_jB_j\omega_j^2-\sum_jR_ji_j^2.
\]

If

\[
\underline c_u,\underline c_r,\underline B_L,\underline B_R,
\underline R_L,\underline R_R>0,
\]

then the candidate

\[
\lambda=\min\left\{
2\underline c_u/\bar m,
2\underline c_r/\bar I_z,
2\underline B_L/\bar J_L,
2\underline B_R/\bar J_R,
2\underline R_L/\bar L_L,
2\underline R_R/\bar L_R
\right\}
\]

satisfies

\[
\dot E_\vartheta\le-\lambda E_\vartheta.
\]

MASTER itself permits nonnegative mechanical damping rather than globally requiring strictly positive `c_u,c_r,B_j`. Therefore the theorem cannot be claimed over all MASTER-admissible parameter sets without this local restriction.

### Consequence

This is the main scientific assumption risk of the seed. If realistic/declared quantitative work cannot justify these positive lower bounds, the current closed-form exponential proof does not apply as written.

### Status

`VALID WITH EXPLICIT RESTRICTION`.

### Required action

Before promotion, either:

1. declare a scientifically justified quantitative `Theta_seed` with the required positive lower bounds; or
2. derive a weaker decay/LaSalle/integral estimate that does not require positivity in every mechanical damping channel.

Do not silently promote the local restriction into MASTER.

---

## 4. Collision-buffer invariance

### Finding

For known energy weights (in particular the capacity-only hidden uncertainty specialization),

\[
K_E=\{E\le e_c,\ d(p)\ge\Gamma_0\sqrt E\}
\]

with

\[
\Gamma_0=\frac{2}{\lambda}\sqrt{\frac2m}
\]

is collision-buffer invariant under the backup input.

### Evidence

For a circular obstacle,

\[
d(p)=\|p-p_o\|-R_s.
\]

On `d>=0`, the obstacle-center distance is at least `R_s`; for the intended inflated obstacle `R_s>0`, so `d` is differentiable on the certified set. Moreover

\[
\dot d
=\hat n^T u[\cos\theta,\sin\theta]^T\ge-|u|.
\]

The energy bound gives

\[
|u|\le\sqrt{2E/m}
\]

and

\[
\frac d{dt}\sqrt E\le-\frac\lambda2\sqrt E
\]

for `E>0`. Thus

\[
\frac d{dt}(d-\Gamma_0\sqrt E)
\ge
-\sqrt{2E/m}+\Gamma_0\frac\lambda2\sqrt E=0.
\]

At `E=0`, every weighted internal coordinate is zero; continuity closes the boundary case.

An equivalent integral proof is

\[
\int_0^\infty|u(t)|dt
\le\Gamma_0\sqrt{E(0)},
\]

which avoids relying on differentiability of `sqrt(E)` at zero.

### Consequence

The theorem controls total path length, not only radial closing speed. It therefore remains sufficient even if the robot turns under unequal hidden capacities.

### Status

`VALID`.

### Required action

Use the integral proof as the primary manuscript proof; it handles the zero-energy corner more cleanly.

---

## 5. Uniform contact-admissibility sublevel

### Finding

The proposed existence of a positive contact-safe energy threshold `e_c` is valid.

### Evidence

For `E_\vartheta<=e`, the coordinate bounds imply

\[
|\sigma_j|\le s_j\sqrt e.
\]

The global Lipschitz property and `phi(0)=0` imply

\[
|\phi(\sigma_j/v_s)|\le\alpha_j\sqrt e.
\]

For `alpha_j^2e<1`,

\[
a_j=C_j\sqrt{1-\phi^2}\ge
\underline C_j\sqrt{1-\alpha_j^2e}.
\]

Also

\[
|mur|\le
\bar m\sqrt{2e/\underline m}\sqrt{2e/\underline I_z}
=
\frac{2\bar m}{\sqrt{\underline m\underline I_z}}e.
\]

Therefore the displayed lower bound for the contact margin is valid. At `e=0` it equals

\[
\underline C_L+\underline C_R>0.
\]

By continuity, a sufficiently small positive `e_c` satisfying both the square-root-domain conditions and nonnegative contact lower bound exists.

This proof uses the original algebraic contact margin and does not differentiate its square root.

### Consequence

Independent unequal `C_L,C_R` are allowed. Straight-line symmetry is not needed.

### Status

`VALID`.

### Required action

In a paper, define `e_c` as any positive value satisfying the inequalities, or define the supremal certified threshold only if its computation is separately justified. Do not imply optimality.

---

## 6. Nontrivial moving extent and robust quantifiers

### Finding

The candidate seed is nontrivial in the G3 sense of containing moving states of positive extent, and the voltage quantifier is correct.

### Evidence

At any state position with strict clearance `d>0`, continuity of the quadratic energy gives a neighborhood of internal states with

\[
0<E<\min\{e_c,(d/\Gamma_0)^2\}.
\]

This neighborhood includes points with `u != 0` and/or other nonzero internal coordinates.

The action is fixed:

\[
V_B=(0,0),
\]

so the robust quantifier is exactly

\[
\forall x\in K_E\ \exists V_B\ \forall(C_L,C_R)\ \forall t\ge0.
\]

There is no `forall theta exists V` oracle reversal.

### Consequence

The earlier feasibility statement “no moving robust seed is known” is superseded at candidate-proof level for the restricted capacity-only uncertainty class, subject to the damping assumption and independent review acceptance.

### Status

`VALID CANDIDATE RESULT`.

### Required action

Do not call it “useful G3” yet. Mission usefulness requires a larger recoverability/action set with nonzero task-compatible voltages.

---

## 7. Circularity / contact-domain continuation check

### Finding

The proof is not fatally circular, but the continuation argument should be explicit.

### Evidence

The reduced ODE equations can be algebraically evaluated beyond the contact-validity domain, but physical/model claims are only meaningful while `c>=0`. Starting with `E<=e_c`, the energy identity plus the low-energy coordinate bounds imply `c>=0` for any interval on which the formal solution exists. A standard first-exit contradiction therefore prevents a first exit from the contact domain while the energy bound holds.

### Consequence

The proof should not casually say “energy decay holds globally, therefore contact holds”; it should state that local ODE existence plus the derived lower bound rules out the first contact-domain exit.

### Status

`NEEDS EXPLICIT PROOF TEXT`, not a blocker.

### Required action

Add a first-exit/continuation paragraph in the next theorem revision.

---

## 8. Broader hidden-energy-weight extension

### Finding

The candidate's state-only rechecking penalty

\[
\sqrt\rho e^{-\lambda T/2}<1
\]

is a valid sufficient condition for the proposed `E^+` reset construction, not a necessary condition for state-only G3 feasibility.

### Evidence

Define `E^+` with upper coefficient bounds. For any true realization,

\[
E_\vartheta(z)\le E^+(z)\le\rho E_\vartheta(z).
\]

Along the true trajectory,

\[
E_\vartheta(T)\le q^2E_\vartheta(0),
\qquad q=e^{-\lambda T/2}.
\]

Thus

\[
E^+(T)\le\rho q^2E^+(0),
\]

so

\[
\sqrt{E^+(T)}\le\sqrt\rho q\sqrt{E^+(0)}.
\]

The within-hold path-length bound is

\[
\Delta p_T\le
A(1-q)\sqrt{E^+(0)},
\qquad
A=\frac2\lambda\sqrt{2/\underline m}.
\]

To preserve a state-only buffer `d>=Gamma_T sqrt(E^+)`, it is sufficient that

\[
Gamma_T\ge A(1-q)+Gamma_T\sqrt\rho q,
\]

which gives the candidate formula when the denominator is positive.

The `rho` term arises because MASTER's state-only endpoint set must be robust to the full parameter set again; it is not a claim that the physical parameter changes at the sample.

### Consequence

This may be an interpretable contribution component: it quantifies the price of state-only rechecking versus fixed-parameter execution. But it is only one sufficient bounding construction and may be conservative.

### Status

`VALID SUFFICIENT EXTENSION`.

### Required action

Revise wording to emphasize:

- sufficient, not necessary;
- failure of `sqrt(rho) q < 1` does not prove no robust seed exists;
- alternative common Lyapunov functions or parameter-dependent/state-information constructions may avoid this penalty.

---

## 9. Most important limitation: terminal safety is not journal usefulness

### Finding

Even if every proof above is accepted, the candidate by itself does not meet the project Paper Gate.

### Evidence

The only guaranteed policy in the seed is `V=0`, and the proof is dissipative. It establishes a safe terminal region with moving states, but not useful repeated task progress or meaningful voltage selection.

### Consequence

The next mathematical object must be a recoverability/action set that reaches this seed under a task-compatible voltage while retaining the same robust full-hold collision/contact quantifiers.

### Status

`OPEN — REQUIRED FOR USEFUL_G3`.

### Required action

Construct and prove a one-step or finite-step set

\[
K_{rec}=\{x:\exists V\ \forall\vartheta,
\ x_\vartheta([0,T])\subseteq\mathscr S_c,
\ x_\vartheta(T)\in K_E\}
\]

and demonstrate nonzero admissible task actions on a declared moving domain.

---

## 10. Novelty status

### Finding

No novelty pass follows from the proof audit.

### Evidence

Backup sets, Lyapunov/energy terminal sets, robust backup CBFs, adaptive backup methods and constructive braking safety are established research areas. The candidate's potentially distinctive content is narrower: voltage-level DDWMR power cancellation, independent fixed hidden contact capacities, simultaneous algebraic contact/collision certificate and explicit state-only fixed-parameter reset penalty.

### Consequence

An equation-level J2 audit is mandatory before claiming contribution.

### Status

`UNVERIFIED`.

### Required action

Compare exact theorem assumptions and conclusions against the closest primary sources before implementation investment.

---

## 11. Required revisions to candidate note

The next revision should:

1. make the theorem-local positive mechanical damping assumption visually prominent;
2. use an integral collision proof as the primary proof;
3. add a first-exit argument for contact-domain preservation;
4. distinguish the capacity-only theorem from the broader hidden-weight sufficient extension;
5. label `sqrt(rho)q<1` as sufficient only;
6. state explicitly that `e_c` is a conservative existence threshold, not optimal;
7. avoid any novelty wording until J2 closes;
8. retain all gate statuses unchanged.

---

## 12. Final J1 disposition

**Finding:** a concrete moving robust terminal seed exists as a defensible candidate under explicit local damping and uncertainty restrictions.

**Evidence:** independent rederivation validates the power identity, energy decay, collision buffer, low-energy contact threshold, robust quantifiers and positive moving extent.

**Consequence:** the project now has a specific theorem object worth J2 novelty audit and subsequent recoverability construction; brute-force nine-dimensional kernel work remains premature.

**Status:** `SEED_PROOF_SURVIVES_WITH_REVISIONS`.

**Required action:** revise the seed theorem note as above, then perform J2 equation-level novelty audit. No numerical batch or operational controller implementation is authorized by this review.

**Gate statuses unchanged:** `HOLD`; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.
