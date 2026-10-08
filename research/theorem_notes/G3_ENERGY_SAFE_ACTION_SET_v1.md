# G3 candidate — energy/contact certified nonzero safe-action set

**Dependency:** `research/theorem_notes/G3_ZERO_VOLTAGE_ENERGY_BACKUP_SEED_v1.md` and its J1 proof audit.  
**Scope:** capacity-only positive-width hidden uncertainty specialization, known energy/damping weights, explicit positive damping lower bounds.  
**Status:** analytic candidate; no gate change; no numerical execution.

## 1. Purpose

The zero-terminal-voltage energy seed is recursively safe but, by itself, is only a terminal/backup object. This note derives a **nonzero voltage safe-action relation** inside that seed.

The goal is not to claim optimality. The goal is to obtain a closed-form, state-dependent action set such that every voltage in the set:

1. is applied as one common ZOH terminal voltage for the full hold;
2. is valid for every independent fixed hidden capacity realization;
3. preserves collision and algebraic contact admissibility continuously over the hold; and
4. returns the endpoint to the zero-voltage energy backup seed.

This converts the terminal seed into a minimal recursive safety filter with nonzero actions available in its strict interior.

---

## 2. Recalled quantities

Use the capacity-only hidden-uncertainty specialization of the seed theorem, so the stored energy weights are known:

\[
E(z)=\frac12mu^2+\frac12I_zr^2+
\sum_j\left(\frac12J_j\omega_j^2+\frac12L_ji_j^2\right).
\]

Let

\[
y=\sqrt E,
\qquad
a=\sqrt{\frac2m},
\qquad
\Gamma_0=\frac{2a}{\lambda}.
\]

Let `e_c` be any accepted robust contact-safe energy threshold from the seed theorem.

The terminal set is

\[
K_E=\{x:E(z)\le e_c,\ d(p)\ge\Gamma_0\sqrt{E(z)}\},
\]

where

\[
d(p)=\|p-p_o\|-R_s.
\]

---

## 3. Energy comparison under a nonzero held voltage

The exact power identity is

\[
\dot E
=\sum_ji_jV_j
-c_uu^2-c_rr^2
-\sum_jB_j\omega_j^2
-\sum_jR_ji_j^2
-\sum_jF_j\sigma_j.
\]

Using the same decay constant `lambda` as the zero-voltage seed,

\[
\dot E\le-\lambda E+\sum_j|V_j||i_j|.
\]

Since

\[
\frac12L_ji_j^2\le E,
\]

\[
|i_j|\le\sqrt{\frac{2E}{L_j}}.
\]

For a held voltage `V`, define

\[
\nu(V)=\sum_{j\in\{L,R\}}|V_j|\sqrt{\frac2{L_j}},
\]

and

\[
y_V(V)=\frac{\nu(V)}{\lambda}.
\]

For `y>0`,

\[
\dot y
=\frac{\dot E}{2\sqrt E}
\le-\frac\lambda2y+\frac{\nu(V)}2.
\]

Thus for `t in [0,T]`,

\[
\boxed{
y(t)\le\bar y(t)
=q_t y_0+(1-q_t)y_V,
\qquad
q_t=e^{-\lambda t/2}.
}
\]

The result extends to `y_0=0` by scalar comparison/continuity.

---

## 4. Contact-preserving input-energy condition

If

\[
\boxed{
\max\{y_0,y_V(V)\}\le\sqrt{e_c},
}
\]

then

\[
y(t)\le\sqrt{e_c}\quad\forall t\in[0,T].
\]

The robust low-energy contact theorem therefore gives

\[
x_\vartheta(t)\in D_c(\vartheta)
\]

for every hidden independent capacity realization and every `t` in the hold.

A convenient voltage-only sufficient restriction is

\[
\boxed{
\nu(V)\le\lambda\sqrt{e_c}.
}
\]

---

## 5. Collision path-length and endpoint-return bound

Let

\[
q=e^{-\lambda T/2}.
\]

Since

\[
|u(t)|\le a\,y(t),
\]

we obtain

\[
\int_0^T|u(t)|dt
\le a\int_0^T\bar y(t)dt.
\]

The scalar integral is

\[
\int_0^T\bar y(t)dt
\le
\frac2\lambda(1-q)y_0
+\left(T-\frac2\lambda(1-q)\right)y_V.
\]

The endpoint energy bound is

\[
y(T)\le qy_0+(1-q)y_V.
\]

A sufficient condition for continuous collision safety during the current hold **and** endpoint membership in the zero-voltage terminal set is

\[
d(p_0)
\ge
 a\int_0^T\bar y(t)dt
+\Gamma_0\bar y(T).
\]

Using

\[
\Gamma_0=\frac{2a}{\lambda},
\]

the terms simplify exactly to

\[
\boxed{
 d(p_0)
\ge
\Gamma_0 y_0+aT y_V(V).
}
\]

Thus a nonzero held voltage has a closed-form sufficient **clearance tax**

\[
\boxed{
\Delta d_V(V)=aT\frac{\nu(V)}{\lambda}.
}
\]

Equivalently,

\[
\Delta d_V(V)
=
\frac{2T}{\lambda}
\sum_j\frac{|V_j|}{\sqrt{mL_j}}.
\]

This tax is conservative because it treats every unit of path length as potentially directed toward the obstacle and discards beneficial voltage/current sign information.

---

## 6. Closed-form certified action set

For a sampled state `x in K_E`, define residual energy-clearance slack

\[
s_E(x)=d(p)-\Gamma_0\sqrt{E(z)}\ge0.
\]

Define the candidate action set

\[
\boxed{
\mathcal A_E(x)=\left\{V\in[-V_{max},V_{max}]^2:
\begin{array}{l}
\nu(V)\le\lambda\sqrt{e_c},\\[1mm]
 aT\,\nu(V)/\lambda\le s_E(x)
\end{array}
\right\}.
}
\]

Equivalently,

\[
\boxed{
\nu(V)
\le
\lambda\min\left\{
\sqrt{e_c},
\frac{s_E(x)}{aT}
\right\}.
}
\]

Because

\[
\nu(V)=\sum_j|V_j|\sqrt{2/L_j},
\]

this is the intersection of the physical voltage box with a state-dependent weighted `l1` ball.

---

## 7. Candidate theorem — robust one-hold safe action and endpoint return

### Theorem

Assume the accepted conditions of the capacity-only energy backup seed, including the explicit positive damping restriction and a valid contact-safe threshold `e_c`.

For any sampled state

\[
x_k\in K_E
\]

and any held voltage

\[
V_k\in\mathcal A_E(x_k),
\]

for every independent fixed hidden capacity realization

\[
(C_L,C_R)\in
[\underline C_L,\overline C_L]
\times
[\underline C_R,\overline C_R],
\]

the corresponding formal trajectory satisfies

\[
x_\vartheta(t;x_k,V_k)
\in\mathcal S\cap D_c(\vartheta)
\quad\forall t\in[0,T],
\]

and

\[
x_\vartheta(T;x_k,V_k)\in K_E.
\]

Therefore

\[
\boxed{
K_E\subseteq\operatorname{Pre}_T^c(K_E)
}
\]

with a certified **set-valued non-oracle policy** `A_E(x)`.

### Quantifier order

\[
\forall x_k\in K_E,
\quad
\forall V_k\in\mathcal A_E(x_k),
\quad
\forall\vartheta\in\Theta_C,
\quad
\forall t\in[0,T].
\]

In particular, a policy may choose any element of `A_E(x_k)` using only the sampled state and known model bounds.

---

## 8. Nonzero actions exist in the strict interior

At any state with

\[
s_E(x)>0,
\]

the right-hand side of the weighted-`l1` action inequality is positive. Therefore `A_E(x)` contains a neighborhood of `V=0` intersected with the voltage box, including nonzero voltages.

Thus the recursive set is not restricted to an always-zero action: nonzero held terminal voltages are certified in the strict interior.

This still does not imply positive task progress. Because the bound uses `|V_j|`, it does not distinguish forward, reverse or turning action directions. Task usefulness must be established separately on a declared moving domain.

---

## 9. Minimal safety-filter interpretation

Given a task/nominal voltage `V_nom(x)`, a minimal certified filter can conceptually solve

\[
\min_{V\in\mathcal A_E(x)}\|V-V_{nom}(x)\|^2.
\]

The safety proof belongs to the set `A_E`; the projection/QP itself is generic and is not a novelty claim.

Because `A_E` is a voltage box intersected with a weighted `l1` ball, online action selection is computationally elementary once state energy and clearance are known.

No operational controller implementation is authorized by this theorem note.

---

## 10. Scientific limitations

1. **Conservative direction loss.** The bound taxes absolute path length and absolute voltage magnitude. It cannot reward actions that turn or accelerate away from an obstacle.
2. **Capacity-only uncertainty.** The clean closed-form theorem assumes energy weights/damping are known while `C_L,C_R` remain hidden positive-width labels. Broader hidden coefficients require an additional robust state-only construction.
3. **Positive damping.** The exponential comparison requires explicit strictly positive lower bounds.
4. **Static circular obstacle.** The displayed clearance formula is for the current MASTER obstacle model.
5. **No task guarantee.** Nonzero safe voltage availability is not equivalent to mission progress.
6. **No novelty pass.** Weighted energy action budgets and safety-filter projections are generic ideas; only the exact plant/contact construction is a candidate contribution.

---

## 11. Decision-relevant next test

This theorem creates a predeclared analytic baseline for action availability.

A next plant-structured refinement is scientifically worthwhile only if it can exploit sign/direction/correlation discarded by `A_E` and certify a voltage outside this weighted-`l1` set while still proving the same full-hold collision/contact and endpoint-return conditions.

This suggests a clean contribution test:

> On a predeclared moving-state domain, can a correlation-preserving DDWMR one-hold enclosure certify task-compatible voltages that the closed-form energy safe-action set rejects, while preserving endpoint return to `K_E`?

If yes, the energy theorem provides the robust recursive backbone and the structured enclosure supplies useful action expansion. If no meaningful expansion exists, the journal contribution becomes weaker.

---

## 12. Status

### Finding

A state-dependent nonzero safe-action set can be derived in closed form from the candidate energy seed.

### Evidence

The forced energy comparison, contact threshold, path-length integral and terminal-buffer algebra yield the exact sufficient clearance condition

\[
d(p_0)\ge\Gamma_0\sqrt{E_0}+aT\nu(V)/\lambda.
\]

### Consequence

The candidate recursive set now supports nonzero voltage actions in its strict interior, making it more than an always-zero terminal policy. Task usefulness and comparative advantage remain open.

### Status

`J3_ANALYTIC_CANDIDATE — NEEDS INDEPENDENT PROOF AND NOVELTY REVIEW`.

### Required action

Independently audit this derivation, then freeze a moving-state/action usefulness criterion comparing:

1. this closed-form energy action set;
2. a generic matched backup/reachability baseline; and
3. any correlation-preserving DDWMR structured one-hold refinement.

Do not run a numerical campaign before the comparison protocol is frozen.

**All project gate statuses remain unchanged.**
