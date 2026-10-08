Session: DDWMR | LUNA-G2-SCOPE

# W2 G2 analytic task feasibility screen

**Protocol bound:** `G2_W2_VOF_TASK_V1`, before any full-cell evaluator attempt. **Screen type:** exact-rational point calculation for the affine clip-interior candidate only. It is not a safety certificate, a positive-width result, or a query row.

## Point and equations

The point is inside the frozen initial/parameter domain: `p=theta=r=i_L=i_R=0`, `u=3/10`, `omega_L=omega_R=1/4`, and all twelve labels equal 1. Its initial slips are both `-1/20`. Under the symmetric affine branch `|omega-u|<1`, let `w=omega_L=omega_R` and `i=i_L=i_R`. MASTER's body, wheel and current equations reduce to

\[
\dot u=-3u+2w,\qquad \dot w=u-2w+i,\qquad
\dot i=V-i-w,
\]

with a common constant wheel voltage `V` in `{0, 1/2, 1}`. The output is `J=integral_0^2 u(t) dt` because `theta=r=0` on this equal-side point. This is a rational affine IVP and the finite series uses no floating arithmetic.

For the augmented vector `y=(u,w,i,1)`, `y'=A_V y`. The script sums

\[
J_N=\sum_{n=0}^{N}(A_V^n y_0)_u\frac{T^{n+1}}{(n+1)!},\quad N=100,
\]

and encloses the omitted tail by

\[
|J-J_N|\le \frac{Tq^{N+1}}{(N+2)!}\frac{\|y_0\|_\infty}{1-q/(N+3)},\quad
q=\|A_V\|_\infty T=10.
\]

The exact common tail is less than `10^-60 m`. The executable is `validation/autonomous_w2/g2/analytic_task_screen.py`.

| Held action | Rational Taylor enclosure, shown to 36 decimal places | Relation to locked `7/20 m` |
|---|---:|---|
| zero `(0,0)` | `[0.208990264713054504467242247303735458 ± 10^-60] m` | Below at this point |
| nominal `(1/2,1/2)` | `[0.302166497282866554929071730875957080 ± 10^-60] m` | Below at this point |
| alternative `(1,1)` | `[0.395342729852678605390901214448178702 ± 10^-60] m` | Above at this point |

## Finding and limits

The locked threshold admits a plausible action distinction on a moving initial point with fixed nonzero wheel speed and a positive-width parameter family surrounding it. The task threshold was declared as a 0.175 m/s average-progress requirement before these values were calculated; it was not set from these bounds or from R22–R24. This screen does not show that the full state/parameter box is task-eligible, that clip remains on its affine branch for the full hold, or that any action is safe. The candidate producer must establish the clip interior, collision, contact and progress inequalities for every state, every fixed label and every full-hold slab. A failed full-cell proof returns `UNKNOWN`; the task and threshold remain fixed.

The physical scales, 35 cm command, two-second duration and circle are stipulated synthetic choices. The only inherited provenance is that the positive moving speed is anchored in the prior R3 `S_HIGH_POS` synthetic family. This is not a physical-DDWMR or CommonRoad operating-domain claim.
