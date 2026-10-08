**Session: DDWMR | LUNA-G2-SCOPE**

# G2 R23 — correlated action-gap scaling research

**Date:** 2026-10-06  
**Disposition:** Complete synthetic derivation; merits a narrowly scoped prospective paired evaluator study. This is not practical task validation, a certificate implementation, or a G2 promotion.

## 1. Finding

For the frozen synthetic family, R22's separate scalar progress tubes certify \(J_+^- > J_0^+\) only at \(\eta=10^{-6}\). Their outward radius is proportional to the common state/parameter half-width, and their intervals first overlap at \(10^{-5}\). The scalar comparison's domain and Lipschitz assumptions still hold at every requested width through \(10^{-2}\); the loss is enclosure conservatism, not a counterexample or an assumption failure.

A paired comparison that subtracts trajectories with the **same initial state and same execution-fixed parameter labels** preserves the voltage-to-current-to-wheel-to-slip-to-force coupling. A clip-branch bootstrap proves both trajectories stay unsaturated throughout the hold. The paired comparison then proves, uniformly for every \(\eta\) in the frozen grid and every matched realization,

\[
\Delta J=J_{(1,1)}-J_{(0,0)}>\frac{1}{25{,}000}\ {\rm m}=40\ \mu{\rm m}.
\]

This proves per-realization action ordering in this synthetic model. It does not prove one common task threshold across the whole cell: the paired inequality compares matched realizations, while a common threshold requires a lower bound for the positive action exceeding the upper bound for the baseline over potentially different realizations.

Independent whole-hold bounds also establish, for both actions and every grid point, collision clearance \(>0.097\) m and formal contact margin \(c>1.9\) in the declared synthetic model units. Neither these margins nor the action gap have physical-platform provenance.

## 2. Frozen scope and source basis

The study uses exactly the R23 family, declared before deriving the results:

- \(X_0(\eta)=[-\eta,\eta]^9\), in MASTER v2.1 state order \([p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R]\).
- \(\Theta_{\rm lab}(\eta)=[1-\eta,1+\eta]^{12}\), with label order \((\rho_L,C_L,\lambda_L,R_L,B_L,k_L,\rho_R,C_R,\lambda_R,R_R,B_R,k_R)\), and \(\eta\in\{10^{-6},10^{-5},10^{-4},10^{-3},10^{-2}\}\).
- The twelve labels are independently ranged in the stated product set, selected once per execution, and held fixed through the hold. In each paired comparison, the same \(x_0\) and the same complete label vector generate both trajectories.
- \(m=I_z=R_w=b=v_s=c_u=c_r=1\), \(J_j=1/\rho_j\), and \(L_j=\lambda_j\). The labels \(C_j,R_j,B_j,k_j\) are used directly. A direct-drive realization consistent with MASTER §10 is \(n_j=1,\ J_{{wheel},j}=1/2,\ J_{{motor},j}=1/\rho_j-1/2>0,\ B_{{wheel},j}=0,\ B_{{motor},j}=B_j,\ k_j^m=k_j\).
- \(\phi(z)=\operatorname{clip}(z,-1,1)\), \(T=1/4\), common obstacle center \((1/5,1/20)\), radius \(3/50\), and held voltages \(V_+=(1,1)\), \(V_0=(0,0)\).
- The displacement is \(J=p_x(T)-p_x(0)=\int_0^T u\cos\theta\,dt\). No task threshold is declared.

The source equations are MASTER v2.1 §§5–12. I read AGENTS.md, all four canonical research_context files, R23, the R22 handoff, and the R22 Codex review. The R22 review accepted the nominal trajectory and scalar-tube calculations in their stated scope. I did not use archived R3/R17 outcomes to choose or alter the R23 grid.

Every parameter lies in \([0.99,1.01]\) on the complete grid; in particular \(\lambda_j\ge0.99\) and the direct-drive motor inertia witness stays positive. The derived statements below are for this one synthetic family, not a general assumption about MASTER's admissible \(\phi\).

## 3. R22 separate scalar comparison and width limit

Let \(E(t)\) be the maximum-norm difference between a trajectory and the nominal center trajectory for the **same action**. R22's accepted bounds on \(D=[-5,5]^9\) are state Lipschitz constant \(9\) and fixed-state parameter forcing at most \(30\eta\). The wheel equation is written as
\[
\dot\omega_j=\rho_j(k_ji_j-B_j\omega_j-F_j),
\]
so the declared \(J_j=1/\rho_j\) dependence is included.

For separate state and label half-widths \(\eta_x,\eta_\theta\), the same Grönwall calculation gives
\[
E(t)\le \eta_x e^{9t}+\frac{30\eta_\theta}{9}(e^{9t}-1).
\]
Since \(e^{9/4}<12\), equal widths \(\eta_x=\eta_\theta=\eta\) give
\[
E(t)<\frac{146}{3}\eta<49\eta=:\bar E(\eta).
\]

These hypotheses remain valid over the requested grid. The R22 a-priori domain comparison is
\[
\|x(t)\|_\infty\le(\eta+\tfrac12)e^{8t}-\tfrac12
<4+9\eta\le4.09<5,\quad 0\le t\le\tfrac14,
\]
using \(e^2<9\). The label bounds remain \(\rho,C,\lambda,R,B,k\in[0.99,1.01]\). Thus the width loss below is not caused by leaving the proved domain.

At the center, the symmetric positive-action path has \(q=\omega-u\) and
\[
\dot u=2q-u,\qquad \dot q=i-4q,\qquad \dot i=1-i-u-q.
\]
The R22 rational center comparison gives
\[
\frac{685}{4{,}718{,}592}\le J_{+,*}\le\frac1{3{,}072},\qquad J_{0,*}=0.
\]
The separate tubes therefore yield
\[
J_0\in[-49\eta/4,\;49\eta/4],
\]
\[
J_+\in[685/4{,}718{,}592-49\eta/2,\;1/3{,}072+49\eta/2].
\]
The outward-cap separation condition is exactly
\[
J_+^- -J_0^+
=\frac{685}{4{,}718{,}592}-\frac{147}{4}\eta>0
\quad\Longleftrightarrow\quad
\eta<\frac{685}{173{,}408{,}256}
\approx3.95021561\times10^{-6}.
\]
Only \(10^{-6}\) from the requested grid satisfies it. Equality gives touching bounds, not strict separation. The uncapped \((146/3)\eta\) estimate would relax this sufficient width slightly; the threshold above is the exact limit for the outward \(49\eta\) comparison used in R22.

The error budget also distinguishes the two sources of width. Before the outward rounding, the terminal state radius is bounded by \(12\eta_x+(110/3)\eta_\theta\). In the scalar progress-gap erosion, the initial-state contribution is at most \(9\eta_x\), and the parameter-width contribution is at most \((55/2)\eta_\theta\). With equal widths, the parameter term is about \(3.06\) times the initial-state term. The \(49\eta\) outward cap gives the slightly more conservative total erosion \(147\eta/4\).

## 4. Clip-branch and whole-hold safety bootstrap

The following independent bootstrap both proves the clip branch needed by the paired comparison and restores safety/contact bounds when the coarse scalar tube is too wide.

Let \(I(t)=\max_j|i_j(t)|\), \(W(t)=\max_j|\omega_j(t)|\), and \(Z=I+W\). Before assuming any unsaturated behavior, \(|F_j|\le C_j\le1.01\). The electrical and wheel equations give
\[
D^+I\le\frac{1+1.01Z}{0.99},\qquad
D^+W\le1.0201(Z+1),
\]
hence \(D^+Z\le2.031+2.041Z\), with \(Z(0)\le2\eta\le0.02\). On \(T=1/4\), \(e^{2.041T}<e^{0.511}<1.67\), so the comparison solution gives
\[
Z(t)\le0.02e^{2.041t}+\frac{2.031}{2.041}(e^{2.041t}-1)<0.704<0.71.
\]
The exponential cap follows from the explicit rational Taylor bound
\[
e^{0.511}\le1+0.511+\frac{0.511^2}{2}+\frac{0.511^3}{6}
+\frac{0.511^4}{24(1-0.511/5)}<1.67,
\]
where every ratio after the degree-four term is at most \(0.511/5\).

For the declared \(b=R_w=v_s=1\), differentiating the exact left and right slip definitions and substituting MASTER's body, yaw, and wheel equations gives, for either side,
\[
\dot\sigma_j=\rho_j k_ji_j+(1-\rho_jB_j)\omega_j-\sigma_j-(\rho_j+2)C_j\operatorname{clip}(\sigma_j).
\]
At \(\sigma_j=1\), its derivative is at most
\[
1.0201(0.71)+0.0201(0.71)-1-(2.99)(0.99)<0;
\]
at \(\sigma_j=-1\), its derivative is strictly positive by the symmetric lower estimate. Initially \(|\sigma_j|\le3\eta\le0.03\). Therefore a first-exit argument proves \(|\sigma_j(t)|<1\) for both actions, both wheels, every declared initial state/label vector, and the complete hold. This is a case-specific consequence of the declared saturating clip; MASTER does not generally assume its traction shape is monotone or linear.

Inside this now-proven branch, the slip equation is linear with damping
\[
d_j=1+(\rho_j+2)C_j\ge1+(2.99)(0.99)=3.9601,
\]
and its non-slip input has magnitude at most \((1.0201+0.0201)(0.71)<0.74\). Since \(0.74/3.9601<0.2\) and the initial slip is at most \(0.03\), scalar comparison yields \(|\sigma_j(t)|<0.2\).

Consequently \(|F_j|<1.01(0.2)=0.202\). From \(\dot u=F_L+F_R-u\) and \(\dot r=F_R-F_L-r\), with \(|u(0)|,|r(0)|\le0.01\),
\[
|u(t)|,\ |r(t)|
\le(0.01+0.404)e^t-0.404
\le0.414(1.29)-0.404<0.131.
\]
Here \(e^{1/4}<1.29\). It follows that \(|p_x(t)|\le0.01+0.131/4=0.04275\). The obstacle's horizontal separation is at least \(0.2-0.04275=0.15725\); subtracting its radius gives whole-hold clearance \(>0.09725\) m (reported conservatively as \(>0.097\) m).

For formal contact, each reserve satisfies
\[
a_j=C_j\sqrt{1-\sigma_j^2}>0.99(0.97)=0.9603
\]
because \(\sqrt{1-0.2^2}>0.97\). Thus \(a_L+a_R>1.9206\), while \(|m u r|<0.131^2=0.017161\). The stipulated contact margin is therefore
\[
c=a_L+a_R-|m u r|>1.903439>1.9
\]
throughout the hold. This evaluates the square root directly inside the strictly unsaturated branch; no derivative bound at saturation is used.

## 5. Shared-realization paired-action bound

Fix any one \(x_0\in X_0(\eta)\) and one fixed \(\vartheta\in\Theta_{\rm lab}(\eta)\); compare the two trajectories from exactly those same values. Put \(\delta z=z_+-z_0\) and define
\[
A_L=\delta u-\delta r,\quad A_R=\delta u+\delta r,\quad
S_j=\delta\sigma_j,\quad I_j=\delta i_j.
\]
Then \(\delta u=(A_L+A_R)/2\) and \(\delta\omega_j=S_j+A_j\). The branch proof above makes \(\delta F_j=C_jS_j\) valid over the entire paired tube. Subtraction of the two actions' MASTER equations gives, separately for each wheel,
\[
\dot A_j=2C_jS_j-A_j,
\]
\[
\dot S_j=\rho_jk_jI_j-
[\rho_jB_j+(\rho_j+2)C_j]S_j+(1-\rho_jB_j)A_j,
\]
\[
\dot I_j=\frac{1-R_jI_j-k_j(S_j+A_j)}{\lambda_j}.
\]
The last equation includes the unit voltage difference \(V_{+,j}-V_{0,j}=1\). All three differences start at zero. No parameter is reselected or switched in time; the same fixed label occurs in both subtracted vector fields. Left/right parameter labels may differ from one another, and the bounds below hold for either side independently.

### 5.1 Positivity cone and upper bounds

For each side let \(H_j=I_j-A_j/20\). On the trial box
\[
0\le I_j\le0.32,\quad 0\le S_j\le0.11,\quad 0\le A_j\le0.07,\quad H_j\ge0,
\]
the lower-face derivatives point inward:

- At \(A_j=0\), \(\dot A_j=2C_jS_j\ge0\).
- At \(S_j=0\), \(\dot S_j=\rho_jk_jI_j+(1-\rho_jB_j)A_j\ge(0.9801/20-0.0201)A_j\ge0\), using \(I_j\ge A_j/20\).
- At \(I_j=0\), \(\dot I_j=[1-k_j(S_j+A_j)]/\lambda_j>0\).
- At \(H_j=0\), \(I_j=A_j/20\). The box gives
  \[
  \dot I_j\ge\frac{1-1.01(0.0035+0.18)}{1.01}>0.80,\qquad
  \dot A_j/20\le\frac{2.02(0.11)}{20}<0.012,
  \]
  so \(\dot H_j>0.78\).

The initial point is the cone vertex; \(\dot I_j(0)=1/\lambda_j>0\). These inequalities give the cone invariance by a first-exit argument.

Within the cone, \(\dot I_j\le1/\lambda_j\le100/99\), hence \(I_j(t)\le100t/99\le25/99<0.32\). Under the trial box, \(\dot A_j\le2.02(0.11)\), so \(A_j(t)\le0.2222t\le0.05555<0.07\). Also
\[
\dot S_j\le1.0201 I_j+0.0199A_j
\le\left(1.0201\frac{100}{99}+0.0199(0.2222)\right)t
<1.035t,
\]
so \(S_j(t)<0.5175t^2\le0.03235<0.11\). Thus no upper face of the trial box can be the first exit. These estimates sharpen to
\[
I_j(t)\le\frac{100}{99}t,\qquad S_j(t)\le\frac35t^2,\qquad
A_j(t)\le\frac{41}{100}t^3.
\]
For the last two, substitute the strict \(S_j<0.5175t^2\) bound into \(\dot A_j\le2.02S_j\) and integrate.

### 5.2 Positive lower bound through the full force chain

Using these upper bounds,
\[
1-R_jI_j-k_j(S_j+A_j)>0.70,
\]
so \(\dot I_j>0.69\) and \(I_j(t)\ge0.69t\). With
\[
\rho_jk_j\ge0.9801,\quad
\rho_jB_j+(\rho_j+2)C_j<4.061,\quad
1-\rho_jB_j\ge-0.0201,
\]
and \(A_j\le0.41t^3\le(0.41/16)t\) on \([0,1/4]\), it follows that
\[
\dot S_j\ge0.67t-4.061S_j.
\]
The kernel is uniformly \(e^{-4.061(t-s)}>1/3\) for \(0\le s\le t\le1/4\). One rational check is
\[
e^{1.01525}=e\,e^{0.01525}
<\frac{11}{4}\frac{1}{1-0.01525}
=\frac{11000}{3939}<3,
\]
where \(e<11/4\) and \(e^x\le(1-x)^{-1}\) for \(0\le x<1\). Variation of constants gives
\[
S_j(t)>\frac{0.67}{6}t^2>0.11t^2.
\]
Then \(\dot A_j=2C_jS_j-A_j\), \(C_j\ge0.99\), and \(e^{-(t-s)}\ge1-(t-s)\ge3/4\) give
\[
A_j(t)\ge1.98(0.11)\int_0^t e^{-(t-s)}s^2\,ds
\ge0.05445t^3>0.054t^3.
\]
This traces the comparison through voltage \(\to\) current \(I_j\) \(\to\) wheel/body relative speed \(S_j\) \(\to\) clipped force difference \(C_jS_j\) \(\to\) longitudinal body response \(A_j\).

### 5.3 Heading correction and terminal progress

Because the initial state is shared, \(\delta\theta(0)=0\). Also
\[
\delta r=(A_R-A_L)/2,\qquad
|\delta r(t)|\le0.41t^3,\qquad
|\delta\theta(t)|\le0.41t^4/4.
\]
The R22 per-action scalar tube gives \(|u_0|,|\theta_0|,|\theta_+|\le49\eta\le0.49\). Thus \(\cos\theta_+\ge1-\theta_+^2/2>0.87\), and \(|\cos\theta_+-\cos\theta_0|\le0.49|\delta\theta|\). Using the exact displacement integral,
\[
\Delta J=\int_0^T\left[\delta u\cos\theta_+
+u_0(\cos\theta_+-\cos\theta_0)\right]dt.
\]
The first term is bounded below by
\[
0.87(0.054)\int_0^{1/4}t^3dt
=\frac{2349}{51{,}200{,}000}\ {\rm m}.
\]
The absolute heading-error subtraction is bounded above by
\[
(0.49)^2(0.41)\int_0^{1/4}\frac{t^4}{4}dt
=\frac{98{,}441}{20{,}480{,}000{,}000}\ {\rm m}.
\]
Their rational difference is
\[
\Delta J\ge\frac{841{,}159}{20{,}480{,}000{,}000}\ {\rm m}
>\frac1{25{,}000}\ {\rm m}>0.
\]
The same lower bound holds at each of the five grid points; its constants use only the outer label box \([0.99,1.01]^{12}\), not a selected width or archived outcome.

## 6. Width-by-width findings

The intervals below use R22's outward \(49\eta\) scalar tube. Decimal endpoints are rounded for display; the exact defining formulas are in §3.

| \(\eta\) | Separate \(J_0\) interval | Separate \(J_+\) interval | \(J_+^- - J_0^+\) | Separate tubes disjoint? | Whole-hold collision and contact for both actions? | Matched paired bound |
|---:|---:|---:|---:|:---:|:---:|:---:|
| \(10^{-6}\) | \([-1.2250\cdot10^{-5},\,1.2250\cdot10^{-5}]\) | \([1.2067042\cdot10^{-4},\,3.5002083\cdot10^{-4}]\) | \(+1.0842042\cdot10^{-4}\) | Yes | Yes: clearance \(>0.097\) m; \(c>1.9\) | \(\Delta J>1/25{,}000\) m |
| \(10^{-5}\) | \([-1.2250\cdot10^{-4},\,1.2250\cdot10^{-4}]\) | \([-9.9829576\cdot10^{-5},\,5.7052083\cdot10^{-4}]\) | \(-2.2232958\cdot10^{-4}\) | No | Yes: clearance \(>0.097\) m; \(c>1.9\) | \(\Delta J>1/25{,}000\) m |
| \(10^{-4}\) | \([-1.2250\cdot10^{-3},\,1.2250\cdot10^{-3}]\) | \([-2.3048296\cdot10^{-3},\,2.7755208\cdot10^{-3}]\) | \(-3.5298296\cdot10^{-3}\) | No | Yes: clearance \(>0.097\) m; \(c>1.9\) | \(\Delta J>1/25{,}000\) m |
| \(10^{-3}\) | \([-1.2250\cdot10^{-2},\,1.2250\cdot10^{-2}]\) | \([-2.4354830\cdot10^{-2},\,2.4825521\cdot10^{-2}]\) | \(-3.6604830\cdot10^{-2}\) | No | Yes: clearance \(>0.097\) m; \(c>1.9\) | \(\Delta J>1/25{,}000\) m |
| \(10^{-2}\) | \([-1.2250\cdot10^{-1},\,1.2250\cdot10^{-1}]\) | \([-2.4485483\cdot10^{-1},\,2.4532552\cdot10^{-1}]\) | \(-3.6735483\cdot10^{-1}\) | No | Yes: clearance \(>0.097\) m; \(c>1.9\) | \(\Delta J>1/25{,}000\) m |

The first proof to lose its conclusion is the **separate scalar progress-interval separation** at \(10^{-5}\). Its assumptions and domain do not fail. The paired comparison, the clip-branch bootstrap, and the independent full-hold collision/contact bounds lose no conclusion on this grid. There is no counterexample in this analysis. Overlapping separate intervals at wider cells mean only that these independent scalar tubes discard too much shared-state/shared-parameter dependence; they do not show task failure or reversed action ordering.

## 7. Decision and limits

**Recommendation: yes, pursue a prospective certified paired-evaluator prototype as a synthetic method study.** Here the independent scalar tubes lose action separation immediately beyond the narrowest grid point, while a matched paired bound remains positive over the entire \(10^{-6}\)–\(10^{-2}\) grid and the full-hold safety/contact checks remain closed. That is evidence that preserving the paired dependence is a worthwhile evaluator direction for this model family.

The result is limited to one held-action pair, one clip law, one synthetic parameter map, one obstacle, one hold, and one symmetric family of product cells. It does not establish:

- a common \(\delta_{\rm task}\) separating all baseline trajectories from all positive-action trajectories;
- a useful or owner-declared task, practical operating-domain widths, physical parameter provenance, or real-platform correspondence;
- a general evaluator's completeness, runtime, conservatism, or advantage over other certified methods;
- G2, G3, or G4 acceptance, novelty, or practical safety-filter value.

The model equations, physical correspondence, and task relevance remain in their prior states. Overall status stays **HOLD**; **G1 restricted PASS**; **G2/G3/G4 and physical correspondence UNVERIFIED**; **G4 paused**.

## 8. Execution and artifact ledger

- Native queries: **0**; workers/stages/retries: **0**.
- R5 800-row study: **800/800 NOT_RUN**.
- New query IDs/manifests: **none**; G4 comparisons: **0**.
- R17 consumed rows and R22 evidence: **unchanged**; G4 files/evidence: **untouched**.
- This handoff is the only file created for R23. No source or manifest was edited; no branch switch, commit, or push occurred.
- No saved certificate or query result was produced. The derivation and exact arithmetic below are exploratory research only.

### Exploratory exact-arithmetic check

The following inline Python Fraction snippet checks the displayed scalar interval endpoints, scalar gap, and final rational paired-bound subtraction. Its inputs are the frozen grid and constants shown in this report. It is not a model evaluator or certificate producer.

~~~python
from fractions import Fraction as F

etas = [F(1, 10**6), F(1, 10**5), F(1, 10**4),
        F(1, 10**3), F(1, 100)]
j_plus_center_lo = F(685, 4718592)
j_plus_center_hi = F(1, 3072)

for eta in etas:
    j0 = (-F(49, 4) * eta, F(49, 4) * eta)
    jp = (j_plus_center_lo - F(49, 2) * eta,
          j_plus_center_hi + F(49, 2) * eta)
    print(float(eta), tuple(map(float, j0)), tuple(map(float, jp)),
          float(jp[0] - j0[1]))

paired_progress = F(2349, 51200000)
heading_error = F(98441, 20480000000)
paired_gap = paired_progress - heading_error
assert paired_gap == F(841159, 20480000000)
assert paired_gap > F(1, 25000)
~~~
