**Session: DDWMR | LUNA-G2-SCOPE**

# G2 R24 — paired-bound and common-threshold adversarial audit

**Date:** 2026-10-06  
**Disposition:** R23 matched-realization ordering bound is valid in its synthetic scope, with one endpoint wording correction. The common-threshold claim is established at \(\eta=10^{-6}\), unresolved by the available bounds at \(10^{-5}\) and \(10^{-4}\), and false at \(10^{-3}\) and \(10^{-2}\) by an admissible cross-state witness.

## 1. Audit result by width

| \(\eta\) | Matched ordering \(J_+(x_0,\vartheta)>J_0(x_0,\vartheta)\) | One common threshold \(\sup J_0<\delta\le\inf J_+\) |
|---:|---|---|
| \(10^{-6}\) | **VALID:** R23 proves \(\Delta J>1/25{,}000\) m for every matched state/label pair. | **ESTABLISHED, synthetic:** R22's separate intervals are disjoint; e.g. \(49/4{,}000{,}000<\delta\le8{,}896{,}789/73{,}728{,}000{,}000\) m. No owner task threshold is specified. |
| \(10^{-5}\) | **VALID:** same R23 paired lower bound. | **UNVERIFIED:** separate scalar intervals overlap, which is inconclusive; the reviewed cross-state witness lower bound does not establish reversal at this width. |
| \(10^{-4}\) | **VALID:** same R23 paired lower bound. | **UNVERIFIED:** scalar overlap remains inconclusive; the reviewed witness lower bound does not establish reversal at this width. |
| \(10^{-3}\) | **VALID:** same R23 paired lower bound. | **IMPOSSIBLE:** the admissible baseline value from \(u_0=+\eta\) is strictly greater than the positive-action value from \(u_0=-\eta\), so \(\sup J_0>\inf J_+\). |
| \(10^{-2}\) | **VALID:** same R23 paired lower bound. | **IMPOSSIBLE:** the same cross-state reversal is strict and larger. |

The two propositions have different quantifiers. R23 compares actions at the **same** \(x_0,\vartheta\). A common threshold compares the baseline supremum and positive-action infimum over potentially **different** realizations.

## 2. Independent audit of R23's paired result

### 2.1 Slip dynamics, clip branch, and safety/contact

MASTER gives \(\sigma_L=\omega_L-u+r\), \(\sigma_R=\omega_R-u-r\), \(u'=F_L+F_R-u\), \(r'=F_R-F_L-r\), and \(\omega'_j=\rho_j(k_ji_j-B_j\omega_j-F_j)\) for R23's unit constants. Differentiating each slip definition gives the same side equation:
\[
\dot\sigma_j=\rho_jk_ji_j+(1-\rho_jB_j)\omega_j-\sigma_j-(\rho_j+2)F_j.
\]
With \(F_j=C_j\operatorname{clip}(\sigma_j)\), this matches R23's displayed formula. The signs of the \(F_j\), yaw, and wheel-reaction terms are consistent with MASTER §§7–10.

For both applied actions, \(|V_j|\le1\). Before assuming the clip branch, set \(Z=\max_j|i_j|+\max_j|\omega_j|\). The MASTER electrical/wheel equations and \(C,\rho,R,B,k\le1.01,\lambda\ge0.99\) give
\[
D^+Z\le2.031+2.041Z,\quad Z(0)\le0.02,
\]
hence \(Z<0.704<0.71\) for \(t\le1/4\). Also \(|1-\rho B|\le0.0201\), \(\rho k\le1.0201\), and \(1+(\rho+2)C\ge1+(2.99)(0.99)=3.9601\). At \(\sigma=+1\), the slip derivative is at most
\[
(1.0201+0.0201)(0.71)-3.9601<0;
\]
at \(\sigma=-1\), it is at least the negative of the input bound plus \(3.9601\), hence is positive. Since initially \(|\sigma_j|\le3\eta\le0.03\), the first-exit proof keeps both trajectories strictly inside \(|\sigma_j|<1\). This depends on the R23-specific saturating clip and the declared parameter box; it is not a MASTER-wide monotonicity assumption.

Inside the branch, the damping lower bound is \(3.9601\) and the non-slip input is less than \(0.74\). Thus \(|\sigma_j|<\max(0.03,0.74/3.9601)<0.2\). Then \(|F_j|<0.202\), and the body/yaw comparison gives
\[
|u(t)|,\ |r(t)|\le(0.01+0.404)e^{1/4}-0.404<0.131.
\]
Therefore \(|p_x(t)|\le0.01+0.131/4=0.04275\), so the obstacle's horizontal separation is at least \(0.2-0.04275=0.15725\) m and collision clearance exceeds \(0.09725\) m. For contact, \(a_j=C_j\sqrt{1-\sigma_j^2}>0.99(0.97)=0.9603\), while \(|mur|<0.131^2\); hence \(c>1.9206-0.017161=1.903439>1.9\). These uniform bounds apply to both actions at all five widths and also cover the two witness trajectories below. No contact-margin derivative at saturation is used.

### 2.2 Paired difference equations and cone

For a fixed shared \(x_0,\vartheta\), let \(\delta z=z_+-z_0\),
\[
A_L=\delta u-\delta r,\quad A_R=\delta u+\delta r,\quad
S_j=\delta\sigma_j,\quad I_j=\delta i_j.
\]
Because both trajectories are inside the clip's linear branch, \(\delta F_j=C_jS_j\). Direct subtraction of MASTER's equations, retaining the same fixed labels, gives
\[
A'_j=2C_jS_j-A_j,\qquad
S'_j=\rho_jk_jI_j-[\rho_jB_j+(\rho_j+2)C_j]S_j+(1-\rho_jB_j)A_j,
\]
\[
I'_j=\frac{1-R_jI_j-k_j(S_j+A_j)}{\lambda_j}.
\]
The action difference is the unit forcing in the last equation. All differences start at zero. No label switching, relabeling, or independent-parameter substitution is present.

The R23 cone \(A_j,S_j,I_j\ge0,\ H_j:=I_j-A_j/20\ge0\) closes on its trial box \(I\le0.32,S\le0.11,A\le0.07\). At \(A=0\), \(A'=2CS\ge0\). At \(S=0\), using \(I\ge A/20\) and \(\rho k\ge0.9801,\ 1-\rho B\ge-0.0201\),
\[
S'\ge(0.9801/20-0.0201)A\ge0.
\]
At \(I=0\), \(I'=[1-k(S+A)]/\lambda>0\). At \(H=0\), \(I=A/20\); the trial box gives \(I'>0.80\), \(A'/20<0.012\), hence \(H'>0.78\). The initial cone vertex enters with \(I'(0)=1/\lambda>0\).

Within that cone, \(I\le100t/99\le25/99\). On the trial box, \(A\le2.02(0.11)t=0.2222t\), then
\[
S'\le\left(1.0201\frac{100}{99}+0.0199(0.2222)\right)t<1.035t,
\]
so \(S<0.5175t^2\). These integral bounds prevent any upper-face exit and sharpen to \(S\le(3/5)t^2,\ A\le(41/100)t^3\).

Using those upper bounds,
\[
1-RI-k(S+A)>0.70,\quad I'>0.69,\quad I(t)>0.69t\quad(t>0).
\]
Since \(\rho k\ge0.9801\), \(\rho B+(\rho+2)C<4.061\), \(1-\rho B\ge-0.0201\), and \(A\le0.41t^3\le(0.41/16)t\),
\[
S'\ge0.67t-4.061S.
\]
For \(0\le s\le t\le1/4\), \(e^{-4.061(t-s)}>1/3\); variation of constants yields \(S(t)>0.11t^2\) for \(t>0\). Then \(A'=2CS-A\), \(C\ge0.99\), and \(e^{-(t-s)}\ge3/4\) yield \(A(t)>0.054t^3\) for \(t>0\). At \(t=0\), these lower bounds equal zero and must not be written as strict inequalities.

### 2.3 Heading correction and rational gap

Since the initial state is shared, \(\delta\theta(0)=0\), and
\[
\delta r=(A_R-A_L)/2,\qquad |\delta r|\le0.41t^3,\qquad
|\delta\theta|\le0.41t^4/4.
\]
R22's per-action tube gives \(|u_0|,|\theta_0|,|\theta_+|\le49\eta\le0.49\). Thus \(\cos\theta_+>0.87\) and \(|\cos\theta_+-\cos\theta_0|\le0.49|\delta\theta|\). Substituting in the exact MASTER displacement integral gives a positive contribution of at least
\[
0.87(0.054)\int_0^{1/4}t^3dt=\frac{2349}{51{,}200{,}000}
\]
and an absolute heading subtraction at most
\[
(0.49)^2(0.41)\int_0^{1/4}\frac{t^4}{4}dt
=\frac{98{,}441}{20{,}480{,}000{,}000}.
\]
Their difference is exactly \(841{,}159/20{,}480{,}000{,}000>1/25{,}000\). The lower inequalities for \(I,S,A\) are strict for \(t>0\); their integrals give the stated strict positive \(\Delta J\). I found no false inequality in the paired proof. Its limits are the declared synthetic family, the matched-realization quantifier, and the selected clip law.

## 3. Cross-state witness refutes a common threshold at two widths

Choose all twelve labels equal to \(1\). In the baseline trajectory set all initial coordinates to zero except \(u(0)=+\eta\); in the positive-action trajectory use a different admissible initial state with only \(u(0)=-\eta\). Both belong to \(X_0(\eta)\), have \(r=\theta=0\), equal left/right wheels and currents, and start at the same position. The two states are deliberately **not matched**.

In the unsaturated symmetric branch, writing \(w=\omega_L=\omega_R\) and \(i=i_L=i_R\), MASTER directly reduces to
\[
u'=-3u+2w,\qquad w'=u-2w+i,\qquad i'=v-i-w,
\]
where \(v=0\) or \(1\) is the common held voltage. The R23 whole-cell branch proof covers both witness trajectories. At exact rest with \(v=1\), the center comparison has \(0\le i\le t,\ 0\le q=w-u\le t^2/2,\ 0\le u\le t^3/3\) through \(T=1/4\); hence
\[
G=\int_0^{1/4}u(t)\,dt\le\frac{T^4}{12}=\frac1{3072}.
\]
Let \(H\) be the displacement response per unit initial body speed of the resulting homogeneous linear system.

For the actual zero-voltage trajectory with initial speed \(+\eta\), MASTER's energy identity gives
\[
\mathcal E=\tfrac12u^2+w^2+i^2\le\tfrac12\eta^2,\qquad
\dot{\mathcal E}=-u^2-2w^2-2i^2-2\operatorname{clip}(w-u)(w-u)\le0,
\]
so \(|u|,|w|,|i|\le\eta\) and \(|w-u|\le2\eta<1\). This proves its linear-branch assumption directly for both requested widths; dividing the trajectory by \(\eta\) defines the unit-response coefficient \(H\) without assuming a physical unit-speed trajectory lies in the clip branch.

To prove \(H>1/6\), first note that \(w'(0)=\eta>0\). While \(w\ge0\), \(u'\ge-3u\), so \(u(t)\ge\eta e^{-3t}>\eta/3\) on \([0,1/4]\). Also
\[
i(t)=-\int_0^t e^{-(t-s)}w(s)\,ds\ge-\eta t\ge-\eta/4,
\]
using \(0\le w\le\eta\). At any putative first return of \(w\) to zero,
\[
w'=u+i>\eta/3-\eta/4=\eta/12>0,
\]
contradicting a crossing into negative values. Thus \(w\ge0\) throughout, and
\[
H\ge\int_0^{1/4}e^{-3t}dt
=\frac{1-e^{-3/4}}3>\frac16.
\]
The final inequality follows from \(e^{3/4}>1+3/4+(3/4)^2/2>2\).

Linearity on the proven clip branch and superposition now give the exact displacement identities
\[
J_{0,+\eta}=\eta H,\qquad J_{+,-\eta}=G-\eta H.
\]
Consequently
\[
J_{0,+\eta}-J_{+,-\eta}=2\eta H-G>
\frac{\eta}{3}-\frac1{3072}.
\]
At \(\eta=10^{-3}\), this is strictly greater than
\[
\frac1{3000}-\frac1{3072}=\frac1{128{,}000}>0,
\]
confirming the review's claim. At \(\eta=10^{-2}\), it is strictly greater than
\[
\frac1{300}-\frac1{3072}=\frac{77}{25{,}600}>0.
\]
Since a baseline value from one state exceeds a positive-action value from another state, \(\sup J_0\ge J_{0,+\eta}>J_{+,-\eta}\ge\inf J_+\). No \(\delta\) can satisfy \(\sup J_0<\delta\le\inf J_+\) at either width. This does not contradict R23's matched action-ordering result.

Both witnesses remain collision/contact-admissible: they lie in the declared state and parameter cells, and the uniform whole-cell margins audited in §2.1 apply. They have clearance \(>0.097\) m and contact margin \(c>1.9\) throughout the hold.

## 4. R23 wording erratum

Keep the R23 numerical paired bound, safety/contact bounds, scalar formulas, and artifacts unchanged. Clarify its interpretation as follows:

1. State \(I_j(t)>0.69t,\ S_j(t)>0.11t^2,\ A_j(t)>0.054t^3\) for \(t>0\); at \(t=0\) both sides are zero.
2. The separate scalar intervals overlap at \(10^{-5}\) and \(10^{-4}\), which is inconclusive about actual common-threshold separation. Do not infer a counterexample or actual task failure from those overlaps.
3. The paired result proves matched action ranking only. A separate admissible cross-state witness makes a common threshold impossible at \(10^{-3}\) and \(10^{-2}\). This impossibility comes from the witness, not from scalar-interval overlap.

## 5. Recommendation and status

A prospective paired evaluator should first target **matched action ranking** and report its quantifier explicitly. Task selection should be a separate predicate supplied independently of the computed action gap; acceptance then requires a direct proof such as \(\sup J_0<\delta_{\rm task}\le\inf J_+\). Do not derive a task threshold after seeing the bound or treat per-realization ordering as a common-threshold guarantee.

Overall status remains **HOLD**; **G1 restricted PASS**; **G2/G3/G4 and physical correspondence UNVERIFIED**; **G4 paused**. No formulation or gate changes follow from this audit.

## 6. Execution ledger

- Native queries: **0**; workers, stages, retries: **0**.
- R5 800-row study: **800/800 NOT_RUN**; G4 comparisons: **0**.
- New manifest or query IDs: **none**; no certificate producer created.
- R17–R23 evidence and files: **unchanged**. This handoff is the only R24 file created.
- No commit or push.
