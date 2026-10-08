# Codex review — G2 R20 degree-zero witness and R17 pair feasibility

**Date:** 2026-10-06  
**Reviewed handoff:** `LUNA_TO_CODEX_G2_R20_STRUCTURED_FEASIBILITY_WITNESS_FULL_HANDOFF.md`  
**Disposition:** **ACCEPT the limited degree-zero failure. BLOCK the selected R17 pair as a strong task-selection challenge, subject to adversarial review of the exact counterexample below.** No gate promotion or new execution GO follows.

I read `AGENTS.md`, all four canonical `research_context` files, the R20 handoff and source, the unchanged R17 manifest/records, the task-progress identity in `validation/g2/endpoint_checker_r2.py`, and the pair truth table in `validation/g2/r11_stage_binding.py`. The R20 prototype SHA-256 matches the handoff (`c4a86d61b3d22c303413a9c5635697175b8150bc60ef39e576c356c69ce3370e`). I ran only its read-only saved-input calculation and obtained the displayed `L`, defect, radii and margins. This uses the prototype's own arithmetic, so it is reproduction rather than independent checker replay. No native query, worker, stage or study row was run.

## A. Finding

R20's degree-zero comparison path is mathematically conservative and loses collision separation because a scalar nine-state error radius expands the initial position interval across the obstacle center. This stops **that representation**, not all higher-order or componentwise enclosures.

There is a stronger, separate issue with the selected R17 pair. A nominal parameter/state realization **inside the exact full query cell** has true forward progress strictly below the frozen `1/20` threshold for **both** held voltages `(0,0)` and `(1,1)`. A sound all-cell task-progress lower bound therefore cannot meet the threshold for either action. The R17 pair cannot produce its predeclared strong `CERTIFIED_TASK_ELIGIBLE` positive-action outcome, regardless of enclosure refinement. This is a blocker for the **selected pair and task rule**, not for G2 as a whole.

## B. Evidence

### R20 limited result

The reproduced prototype gives the uniform state-Lipschitz bound `L=38/5`; constant-path defects `rho=411/500` for row 62 and `337/300` for row 74. Its full-slab scalar radii are `676171473429/1099511627776` on row 62 slab 0 and `257702452777/1099511627776` already on row 74 slab 0. Both exceed the coordinate offsets needed to make the expanded initial pose box contain `(1/5,1/20)`. Accordingly, every R20 collision distance lower bound is zero and every collision margin lower bound is `-3/50`. Row 74 slab 0 has positive contact margin, but no full-hold conjunction or task threshold passes. The rational exponential tail and outward radius rounding are explicit; the source does not differentiate the clip or contact square root.

The degree-zero path `P(xi,t)=x0(xi)` retains the same initial variables and parameter labels conceptually, but its single uniform defect and scalar error radius discard much of their useful dependence. Its failure does not assess a time-varying predictor, a componentwise error vector or a joint-margin range evaluator.

### Exact task-feasibility counterexample for the frozen pair

Use the point

\[
p_x=p_y=\theta=r=\omega_L=\omega_R=i_L=i_R=0,
\qquad u=\frac15,
\]

with **all twelve parameter labels equal to 1**. The R17 manifest includes this state and label point: `u` has lower endpoint `1/5`; all zero coordinates lie in their declared intervals; every label interval contains 1. The fixed maps then give `m=I_z=R_w=b=v_s=c_u=c_r=J_j=B_j=L_j=R_j=k_j=C_j=1`. The selected law is `clip`; `T=1/4`; the progress threshold is `1/20`. The endpoint identity is

\[
J=p_x(T)-p_x(0)=\int_0^{1/4}u(t)\cos\theta(t)\,dt.
\]

For either matched voltage, symmetry and uniqueness preserve `r=theta=0`, equal wheel rates and equal currents. Write their common wheel rate/current as `w,i` and set `d=u-w`.

**Positive voltage `(1,1)`.** On the region `u>0`, `w,i>=0`, `d>0`, the relations `w<=u<=1/5` imply `0<d<=1/5<1`, so the clip is exactly `clip(w-u)=-d`. The reduced equations are

\[
\dot u=-u-2d,\qquad
\dot w=i+u-2w,\qquad
\dot i=1-i-w,\qquad
\dot d=-4d-i.
\]

The region is maintained through `T`: `w=0` has `dot w=u+i>0`; `i=0` has `dot i=1-w>=4/5>0`; `u=w+d>0`. Within the region, `dot u<0` gives `u<=1/5`, and `dot i<=1` gives `i(t)<=t`. Variation of constants then yields, for `0<=t<=1/4`,

\[
d(t)=\frac15e^{-4t}-\int_0^t e^{-4(t-s)}i(s)\,ds
\ge \frac15e^{-4t}-\frac{t^2}{2}
> \frac1{15}-\frac1{32}=\frac{17}{480}>0,
\]

using `e<3`. Thus `d` cannot be the first exit either, closing the bootstrap. In particular `dot u=-u-2d<=-17/240`, whence

\[
J=\int_0^{1/4}u(t)\,dt
\le \frac1{20}-\frac{17}{7680}
=\frac{367}{7680}<\frac1{20}.
\]

This is an explicit rational upper witness for one admissible realization. Along it, `r=0` and `0<d<1`, so the formal contact reserve is positive. Also `0<=p_x(t)<1/20`, `p_y=0`; its distance to the declared obstacle center is larger than the `3/50` radius. This chosen trajectory is formally safe/contact-admissible but misses the locked task threshold.

**Zero voltage `(0,0)`.** At the same state/label point, MASTER §11 gives

\[
\dot E=-u^2-\sum_j\bigl(w_j^2+i_j^2+F_j\sigma_j\bigr)\le0,
\]

because the known clip law is sign-preserving. Initially `E(0)=1/50` and `dot E(0)=-3/25<0`. Hence `E(t)<1/50` for every `t>0`; in particular `|u(t)|<1/5`. Symmetry keeps `theta=0`, so

\[
J=\int_0^{1/4}u(t)\,dt
\le\int_0^{1/4}|u(t)|\,dt<\frac1{20}.
\]

This second witness also remains formally contact-admissible: `r=0`, and the energy bound gives `|u|,|w|<1/5` for positive time, hence `|w-u|<2/5<1`. Its displacement magnitude is below `1/20`, so it remains outside the stated obstacle. These trajectory facts concern the single declared realization, not robust safety of the whole input cell.

The manifest's strong pair rule requires positive voltage `CERTIFIED_TASK_ELIGIBLE` and zero voltage `CERTIFIED_TASK_NOT_ELIGIBLE`. Since the true positive-voltage progress fails for one admissible state/label point, **no sound all-cell evaluator can produce the strong positive outcome on this unchanged query**. The zero-voltage witness confirms that neither action meets the threshold uniformly. The saved R17 `VALID_UNKNOWN` statuses and receipt remain untouched; this is a separate analytic feasibility result.

## C. Consequence

Further enclosure tuning on indices 62/74 may teach numerical behavior, but it cannot establish the locked strong task-selection distinction. The next G2 decision challenge needs a prospectively declared state/parameter/scene/horizon/task combination with a mathematically plausible all-cell task-eligible action before any new solver or matched-query execution. This does not authorize changing the consumed threshold or reusing those IDs as fresh evidence. G4 remains paused.

## D. Status

**VALID** for R20's limited degree-zero arithmetic and stopping decision. **BLOCKER** for the selected R17 pair as a strong task-selection challenge, conditional on independent adversarial audit of the new exact counterexample. **UNVERIFIED** for higher-order/componentwise enclosure usefulness, a general G2 evaluator, G4 novelty and physical-platform correspondence. G1 stays PASS only in the restricted reduced-model scope; G2/G3/G4 remain UNVERIFIED; overall **HOLD**.

## E. Required action

Adversarially check the counterexample against the exact manifest and MASTER equations, including its symmetry, bootstrap, energy and task identity. If it holds, retire this consumed pair as a task-selection target and design a **new prospective challenge with pre-execution task-feasibility screening**. If any step fails, identify the exact failing inequality before further enclosure work. Do not run a new row, retry, stage or 800-row study from this review.
