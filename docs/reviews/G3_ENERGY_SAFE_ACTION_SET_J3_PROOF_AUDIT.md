# G3 J3 independent proof audit — energy/contact safe-action set

**Reviewed artifact:** `research/theorem_notes/G3_ENERGY_SAFE_ACTION_SET_v1.md`  
**Dependency:** energy backup seed and J1 audit.  
**Review mode:** independent analytic rederivation; no numerical execution.  
**Disposition:** `SAFE_ACTION_PROOF_SURVIVES`  
**Gate effect:** none; project remains HOLD.

## 1. Finding

The closed-form nonzero safe-action theorem is algebraically sound under the same restricted assumptions as the capacity-only energy backup seed.

For any sampled state in the terminal seed, every voltage satisfying the proposed weighted-`l1` energy/clearance budget is sufficient to guarantee:

1. continuous collision safety over the hold;
2. continuous algebraic contact admissibility for every independent hidden capacity realization; and
3. endpoint return to the terminal seed.

The action set always contains zero and contains nonzero voltages at strict-interior states.

This is a valid recursive-safety candidate, but task usefulness and novelty advantage are still unproved.

---

## 2. Forced energy comparison

From the exact power identity,

\[
\dot E\le-\lambda E+\sum_j|V_j||i_j|.
\]

Since

\[
|i_j|\le\sqrt{2E/L_j},
\]

define

\[
\nu(V)=\sum_j|V_j|\sqrt{2/L_j}.
\]

Then

\[
\dot E\le-\lambda E+\nu(V)\sqrt E.
\]

For `y=sqrt(E)>0`,

\[
\dot y\le-\frac\lambda2y+\frac{\nu(V)}2.
\]

The scalar comparison solution is

\[
\bar y(t)=q_ty_0+(1-q_t)y_V,
\quad
q_t=e^{-\lambda t/2},
\quad
y_V=\nu(V)/\lambda.
\]

This derivation is correct. At `E=0`, the comparison inequality can be understood through the scalar differential inequality / Dini derivative rather than ordinary differentiation of `sqrt(E)`.

**Status:** VALID.

---

## 3. Contact preservation

If

\[
\max\{y_0,y_V\}\le\sqrt{e_c},
\]

then the convex-combination form of `bar y(t)` gives

\[
y(t)\le\sqrt{e_c}
\]

for the whole hold.

The already audited low-energy contact theorem therefore applies for every hidden `C_L,C_R` realization.

The action condition

\[
\nu(V)\le\lambda\sqrt{e_c}
\]

is sufficient together with the state condition `E_0<=e_c`.

**Status:** VALID.

---

## 4. Path-length integral

Let

\[
a=\sqrt{2/m},
\qquad
q=e^{-\lambda T/2}.
\]

Since `|u|<=a y`,

\[
\Delta p_T
\le a\int_0^T\bar y(t)dt.
\]

Direct integration gives

\[
\int_0^T\bar y(t)dt
=
\frac2\lambda(1-q)y_0
+\left(T-\frac2\lambda(1-q)\right)y_V.
\]

The coefficient of `y_V` is nonnegative because

\[
1-e^{-x}\le x
\]

with `x=lambda T/2`.

**Status:** VALID.

---

## 5. Endpoint-return simplification

The terminal backup set requires at the endpoint

\[
d_T\ge\Gamma_0 y_T,
\qquad
\Gamma_0=2a/\lambda.
\]

A sufficient initial condition is

\[
d_0\ge a\int_0^T\bar y(t)dt+\Gamma_0\bar y(T).
\]

Substitution yields

\[
\begin{aligned}
& a\frac2\lambda(1-q)y_0
+a\left(T-\frac2\lambda(1-q)\right)y_V \\
&\quad+\frac{2a}{\lambda}\left(qy_0+(1-q)y_V\right).
\end{aligned}
\]

The `y_0` terms reduce to

\[
\frac{2a}{\lambda}y_0=\Gamma_0y_0,
\]

and the `y_V` terms reduce exactly to

\[
aTy_V.
\]

Therefore

\[
\boxed{
d_0\ge\Gamma_0y_0+aTy_V}
\]

is correct.

This condition also implies continuous collision safety during the hold: the total possible path length over `[0,T]` is no larger than `d_0-Gamma_0 bar y(T)`, hence no prefix path can consume all positive obstacle clearance.

**Status:** VALID.

---

## 6. Weighted-voltage clearance tax

Because

\[
y_V=\frac1\lambda\sum_j|V_j|\sqrt{2/L_j},
\]

the extra clearance budget is

\[
\Delta d_V
=aTy_V
=\frac{2T}{\lambda}\sum_j\frac{|V_j|}{\sqrt{mL_j}}.
\]

Units are consistent:

- `V/sqrt(L)` has units compatible with `sqrt(power/time)` under the energy comparison;
- after multiplication by the defined coefficients the final `Delta d_V` has length units.

For the manuscript, a full dimensional derivation should be included or checked symbolically from SI base units to avoid relying on informal unit cancellation.

**Status:** VALID FORMULA; manuscript unit table recommended.

---

## 7. Safe-action set

For

\[
s_E(x)=d(p)-\Gamma_0\sqrt E,
\]

the proposed set

\[
\mathcal A_E(x)=\{V\in\mathcal U:
\nu(V)\le\lambda\sqrt{e_c},
\ aT\nu(V)/\lambda\le s_E(x)\}
\]

is a sufficient action set.

It is the intersection of the voltage box and a weighted `l1` ball. `V=0` is always included for any `x in K_E`. If `s_E(x)>0`, the set contains a nonzero neighborhood of zero.

For every selected action in the set, the same voltage is applied to every hidden capacity realization. The policy therefore respects the MASTER information structure.

**Status:** VALID.

---

## 8. Recursive implication

For every

\[
x_k\in K_E
\]

and every

\[
V_k\in\mathcal A_E(x_k),
\]

the previous sections prove full-hold safety/contact and

\[
x_\vartheta(T;x_k,V_k)\in K_E
\]

for all hidden capacity labels.

Thus

\[
K_E\subseteq\operatorname{Pre}_T^c(K_E).
\]

A repeated policy that selects any `V_k in A_E(x_k)` therefore satisfies the sampled recursive-safety induction.

**Status:** VALID CANDIDATE G3 PROPERTY.

---

## 9. What this does and does not resolve

### Resolved at candidate-proof level

- a moving state-only recursive set exists under the restricted capacity-only uncertainty class;
- a non-oracle common action exists at every state in the set;
- nonzero actions exist in the strict interior;
- continuous collision and contact safety are included, not just endpoint safety.

### Still unresolved

- whether the set has meaningful task-scale extent under defensible parameters;
- whether task-progressing voltages are available on a predeclared domain;
- whether a plant-structured one-hold refinement materially expands the action set;
- whether the exact construction is sufficiently novel for the target journal;
- broader hidden parameter uncertainty;
- physical-platform correspondence.

Therefore the result is not yet a G3 PASS and not a paper-ready contribution.

---

## 10. Main conservatism and next scientific discriminator

The action theorem uses

\[
\sum_j|V_j||i_j|
\]

and path length

\[
\int|u|dt,
\]

so it throws away:

- voltage/current sign;
- obstacle direction;
- turning direction;
- state/parameter correlation inside the hold;
- possible contact dissipation beyond the minimum used in `lambda`.

This gives a natural, predeclared baseline.

The next DDWMR-specific method should be judged by whether it can safely certify actions outside `A_E(x)` by recovering one or more of those discarded correlations while returning to the same `K_E` terminal seed.

This is a stronger and cleaner scientific test than comparing raw enclosure widths.

---

## 11. J3 proof disposition

**Finding:** the nonzero weighted-`l1` safe-action relation is a correct sufficient recursive-safety construction under the seed assumptions.

**Evidence:** independent derivation verifies the forced energy comparison, contact condition, path integral, exact terminal-buffer simplification and robust quantifier order.

**Consequence:** the project has progressed from a zero-action terminal seed to a closed-form recursive set-valued voltage policy with nonzero actions. The remaining journal question is useful scale and structural advantage over this conservative baseline / other prior art.

**Status:** `SAFE_ACTION_PROOF_SURVIVES`.

**Required action:** freeze a prospective usefulness/comparison protocol before any numerical execution. The protocol must measure decision-relevant safe-action expansion on moving states and include a matched generic prior-art baseline.

**Gate statuses remain unchanged:** `HOLD`; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.
