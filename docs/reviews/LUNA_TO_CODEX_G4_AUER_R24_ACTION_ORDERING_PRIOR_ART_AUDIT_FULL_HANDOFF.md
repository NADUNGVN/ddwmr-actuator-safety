# G4 Auer R24 — action-ordering prior-art audit

Session: DDWMR | LUNA-G4-AUER

**Date:** 2026-10-06  
**Disposition:** The R23 voltage-to-current-to-slip-to-force cone is **not a direct corollary of the inspected monotone-control or incremental-positivity theorem under its stated hypotheses**. Its first-exit/cone-invariance proof uses a generic invariance principle, while its facet inequalities, bounds and terminal-heading correction are specific to the R23 synthetic DDWMR equations. Validated differential-reachability methods can represent and potentially certify the paired output, but do not imply its positive sign or the numerical \(1/25{,}000\) m margin.  
**Contribution disposition:** The R23 result remains valid in the accepted synthetic scope, but the present source comparison and R24 common-threshold result leave **no useful task-level analytic novelty claim** for this frozen family. Stop this synthetic action-ordering novelty branch. No theorem is claimed novel, and the R19/R20 Auer pilot is not used to choose a workload or resource criterion.  
**Gate state:** **HOLD; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.** The Auer batch remains paused.

## 1. Scope, required context and execution record

I read the project AGENTS.md, all four canonical research_context files (MASTER_RESEARCH_CONTEXT_v2.md, DECISION_LOG.md, LITERATURE_MATRIX.md, REVIEW_GATE.md), MASTER v2.1 §§20–23 and 28–31, the G2 R23 and R24 handoffs and Codex reviews, the G4 R23 paired-method handoff and its Codex review, and G4_MATCHED_PRIOR_ART_COMPARISON_v1.md. I treated the literature matrix and prior-art comparison as leads, not as a completed systematic review.

This audit examines at most five primary full-text sources. Four are the closest validated-IVP/reachability sources already documented in the G4 comparison; the fifth is a targeted primary monotone-control source. Full-text status and precise scope are recorded below. No source search was expanded beyond these five.

This was read-only source and equation analysis. **Zero** Auer/R3/G2 native queries, workers, stages, retries, or batch entries were run or created. No solver, code, manifest, or resource rule was created. Existing R19/R20 and R23/R24 artifacts remain unchanged. No MASTER or canonical context file was modified. No commit or push occurred.

## 2. Exact R23/R24 statement and assumptions

### 2.1 Frozen synthetic family

The R23/R24 statement is not a general assumption of MASTER v2.1. It fixes the following synthetic family:

- The nine-state order is \(x=(p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R)\), and the initial cell is \(X_0(\eta)=[-\eta,\eta]^9\), with \(\eta\in\{10^{-6},10^{-5},10^{-4},10^{-3},10^{-2}\}\).
- Each wheel has six execution-fixed labels \((\rho_j,C_j,\lambda_j,R_j,B_j,k_j)\), independently ranging in \([1-\eta,1+\eta]\); the complete twelve-label vector is shared by both compared trajectories and is constant for the entire hold. The synthetic mapping is \(m=I_z=R_w=b=v_s=c_u=c_r=1\), \(J_j=1/\rho_j\), and \(L_j=\lambda_j\).
- The known traction shape is \(\phi(z)=\operatorname{clip}(z,-1,1)\). This is a case choice; MASTER does not assume that every admissible \(\phi\) is monotone or linear.
- The two held actions are \(V_+=(1,1)\) and \(V_0=(0,0)\), with \(T=1/4\). Both begin from the exact same \(\xi\in X_0(\eta)\) and use the same fixed label vector \(\vartheta\).
- The reported output is \(J_a=p_{x,a}(T)-p_{x,a}(0)=\int_0^T u_a\cos\theta_a\,dt\), and \(\Delta J=J_+-J_0\). There is no owner-declared task threshold.
- The synthetic full-hold checks use obstacle center \((1/5,1/20)\), radius \(3/50\), and the reduced model's formal contact margin. These do not establish a physical tire/support model.

R24 accepts the matched statement

\[
\forall \xi\in X_0(\eta),\ \forall\vartheta\in\Theta_{\rm lab}(\eta):
\qquad \Delta J(\xi,\vartheta)\ge
\frac{841159}{20480000000}\ {\rm m}>
\frac{1}{25000}\ {\rm m}.
\]

The R23/R24 whole-hold bounds are collision clearance \(>0.097\) m and formal contact margin \(>1.9\) N for both actions and every realization in the specified family. Strict lower inequalities for the difference states hold for \(t>0\); the trajectories coincide at \(t=0\).

### 2.2 Difference equations and the cone used

For each wheel \(j\), set

\[
A_j=\delta u\mp\delta r,\qquad
S_j=\delta\sigma_j,\qquad
I_j=\delta i_j,
\]

using minus for the left side and plus for the right. On the separately proved unsaturated branch, \(\delta F_j=C_jS_j\), and direct subtraction of MASTER's equations gives

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

All three start at zero. The final equation contains the unit action difference \(V_{+,j}-V_{0,j}=1\). The parameters are not reselected or switched between trajectories. The separate all-action bootstrap bounds \(Z=\max_j|i_j|+\max_j|\omega_j|<0.71\), first proves \(|\sigma_j|<1\), then applies the linear-branch slip equation to obtain \(|\sigma_j|<0.2\) for both actions, both wheels, every label and the full hold. This is the domain justification for using \(\delta F_j=C_jS_j\).

R23 uses the trial box

\[
0\le I_j\le0.32,\quad 0\le S_j\le0.11,\quad
0\le A_j\le0.07,\quad H_j:=I_j-A_j/20\ge0.
\]

On this box the lower faces point inward. At \(S_j=0\), for example,
\[
\dot S_j\ge (0.9801/20-0.0201)A_j\ge0.
\]
At \(H_j=0\), the R23 bounds give \(\dot H_j>0.78\). Upper-face estimates prove the solution cannot leave the trial box before \(T\). Subsequent comparison bounds are

\[
I_j(t)\ge0.69t,\qquad S_j(t)>0.11t^2,\qquad
A_j(t)>0.054t^3\quad(t>0),
\]

with corresponding upper bounds \(I_j\le(100/99)t\), \(S_j\le(3/5)t^2\), \(A_j\le(41/100)t^3\). The proof propagates the imposed voltage difference through current, relative wheel/body slip, clipped longitudinal force, and longitudinal body speed.

### 2.3 The output step is separate from state-cone positivity

The left/right bounds imply \(\delta u=(A_L+A_R)/2>0\), but do not order the heading: \(\delta r=(A_R-A_L)/2\) can have either sign. Thus the terminal displacement is not obtained merely by applying an increasing state-output map to the cone.

R23 instead writes

\[
\Delta J=\int_0^T[
\delta u\cos\theta_+
+u_0(\cos\theta_+-\cos\theta_0)]\,dt.
\]

It separately bounds \(|\delta\theta(t)|\le0.41t^4/4\), \(|u_0|,|\theta_0|,|\theta_+|\le0.49\), and \(\cos\theta_+>0.87\). The positive longitudinal term then dominates the absolute heading correction, yielding the exact rational lower bound above. This local output argument is essential: global monotonicity of cosine is false, and a generic state-order theorem does not supply this estimate.

### 2.4 R24 threshold correction

Matched ranking is strictly weaker than one common threshold separating all baseline outputs from all positive-action outputs:

\[
\forall(\xi,\vartheta):J_+(\xi,\vartheta)>J_0(\xi,\vartheta)
\quad\not\Rightarrow\quad
\sup_{\xi,\vartheta}J_0<
\inf_{\xi,\vartheta}J_+.
\]

R24 establishes the common-threshold separation at \(\eta=10^{-6}\), leaves it unresolved at \(10^{-5}\) and \(10^{-4}\), and refutes it at \(10^{-3}\) and \(10^{-2}\) using admissible cross-state witnesses. The matched \(\Delta J\) bound remains valid at those widths. It must not be described as task selection, task success, or a common threshold guarantee.

## 3. Primary-source comparison — five full-text sources

| Primary source and locator | Full-text access and assumptions relevant here | Input order, sign structure, fixed labels and output | Does it give the R23 conclusion? |
|---|---|---|---|
| **Angeli & Sontag, “Monotone Control Systems,” IEEE TAC 48(10), 1684–1698 (2003), DOI 10.1109/TAC.2003.817920.** Author manuscript arXiv:math/0206133v1; §2 Theorem 1, §3.1 Proposition 3.3 and Corollary 3.4, §8 Proposition 8.3. | Complete author-manuscript PDF was retrieved and text inspected. Theorem 1 requires state and input orders induced by positive cones and a tangent-cone condition for every ordered state/input pair. In the cooperative orthant case, Proposition 3.3 assumes continuously differentiable dynamics and order-convex domains; its equivalent Jacobian test requires nonnegative off-diagonal state partials and nonnegative input partials. Proposition 8.3 identifies cooperativity with incremental positivity under the stated regularity/domain conditions. | This is the closest direct theory for action ordering. A held voltage pair can be ordered componentwise, and the fixed \(\vartheta\) can be treated as a shared frozen coordinate; equal labels do not themselves establish monotonicity. The R23 transformed difference Jacobian below is not Metzler in the natural cone coordinates. Also, \(\Delta J\) is not a monotone output of the cone alone because heading may have either sign and cosine needs a separate local bound. | **No direct implication under the displayed hypotheses.** The general tangent-cone/invariance proof style is established, but the theorem's order-preserving-flow hypotheses and output step are not supplied by R23's box-face checks. R23 must prove its signed bounds and output correction specifically. |
| **Auer, Kiel & Rauh, “A Verified Method for Solving Piecewise Smooth Initial Value Problems,” IJAMCS 23(4), 731–747 (2013), DOI 10.2478/amcs-2013-0055.** §4.1 Eq. (26), Eqs. (27)–(33); §4.2 Eqs. (42)–(43). | Complete retained paper/text is available locally; the prior G4 review records source SHA-256 d6310c8fd32280addda3f50e3367f9923940641d39de0e70a0932869a2d0ead2. This is a verified-IVP method for stated piecewise-smooth models, with derivative/slope enclosures and a residual/Picard tube. | It assumes neither ordered actions nor cooperative signs. The R23 clip is a continuous piecewise-affine expression with branch slopes 0/1; \(\xi,\vartheta\) can be shared frozen state coordinates in a paired augmented IVP, and a terminal output accumulator can represent \(\Delta J\). | **It can represent and potentially certify the numerical paired predicate, not derive its sign analytically.** A successful validated computation would prove its enclosed result for the encoded problem; the paper does not guarantee a \(1/25{,}000\) m lower bound or a finite-resource closure for this pair. |
| **Arcak & Maidens, “Simulation-based Reachability Analysis for Nonlinear Systems Using Componentwise Contraction Properties,” arXiv:1709.06661v1 (2017 author manuscript), §2 Proposition 1 Eqs. (3)–(4), Corollary 1 Eqs. (6)–(8), and parameter-augmentation example.** | Complete arXiv PDF was retrieved. Proposition 1 assumes a componentwise matrix growth bound over the relevant state/time domain. Corollary 1 also requires a coarse full-time reachable-set overapproximation \(D\) where that bound is valid. The paper explicitly treats constant uncertain parameters as frozen state variables. Its displayed smooth Jacobian assumptions do not hold at clip corners. | There is no input-order or Metzler requirement; it bounds distances between trajectories. Shared parameter labels and paired trajectories can be encoded in one augmented state. R23's strict slip-branch proof offers a possible smooth specialization, but a comparison implementation would still need a validated invariant domain and validated reference. An output accumulator can make the difference a terminal coordinate. | **Only after nontrivial plant-specific domain/reference construction, and only as an enclosure.** The result does not say \(\Delta J>0\); a computed output enclosure would have to exclude zero and clear the exact target itself. No such paired numerical computation is in evidence. |
| **Meyer, Devonport & Arcak, “TIRA: Toolbox for Interval Reachability Analysis,” arXiv:1902.05204 (2019 author manuscript), §3.1 Assumption 3, Eq. (4), Proposition 4 and the general-dynamics remarks.** | Complete primary PDF was retrieved. The displayed componentwise growth-matrix method assumes a supplied invariant state domain \(X\) and a matrix bounding the state Jacobian there; Proposition 4 gives an endpoint reachable-set overapproximation. The paper describes alternative methods and generalizations; it does not establish that an unchanged toolbox command accepts this 39-state pair. | No ordered voltage or cooperative state pattern is required for the growth-bound enclosure. Constant labels can be represented in the augmented state. The displayed endpoint result is not by itself a full-hold safety/contact proof; a full-time method or sound subinterval cover is needed. A terminal difference can be added as a coordinate. | **Only as a reachability overapproximation, after supplying the required bounds/domain.** It may certify a positive output if tight enough; it does not entail that result or prove the action-order theorem symbolically. |
| **Houska, Villanueva & Chachuat, “Stable Set-Valued Integration of Nonlinear Dynamic Systems Using Affine Set-Parameterizations,” SIAM J. Numer. Anal. 53(5), 2307–2328 (2015), §3 Assumptions A1–A3, Eqs. (3.1)–(3.4), Theorem 3.1 and Corollary 3.2.** | Complete author-hosted paper and these locators are recorded in the existing G4 primary-source comparison; that audit was reused here. Its predictor-validation theorem requires the displayed smooth/factorable model and a verified remainder/inclusion over a time segment. | It does not rely on input ordering or cooperativity. The paired initial state and fixed parameters can be shared set parameters in the augmented system. A proven strict clip branch can support a smooth branch model, but a predictor and remainder must be certified on that domain. Its validated segment can support full-time predicates; an accumulator or terminal difference represents the output. | **Only after a nontrivial smooth-domain transformation and actual predictor/remainder proof.** It can validate an enclosure, not infer the R23 sign or bound from a generic monotonicity premise. No R23 paired run is recorded. |

This is a targeted comparison of five sources, not an exhaustive search of mobile-robot or contact-control literature. “Not established by these sources” is not a claim that no plant-specific prior theorem exists.

## 4. Equation-level test of the strongest action-order source

Angeli–Sontag is the strongest inspected source for the question “does larger voltage force a larger ordered output?” To test its cooperative orthant criterion, transform each R23 three-state difference subsystem using the actual cone coordinate

\[
H=I-A/20,\qquad q=(A,S,H),\qquad I=H+A/20.
\]

The equations become

\[
\dot A=-A+2CS,
\]
\[
\dot S=(\rho k/20+1-\rho B)A-
[\rho B+(\rho+2)C]S+\rho k H,
\]
\[
\dot H=\frac1\lambda+
\left(\frac1{20}-\frac{R}{20\lambda}-\frac{k}{\lambda}\right)A
-\left(\frac{k}{\lambda}+\frac{C}{10}\right)S
-\frac{R}{\lambda}H.
\]

On the R23 label interval, the \(A\to S\), \(S\to A\), and \(H\to S\) off-diagonal coefficients are positive. In contrast, both \(A\to H\) and \(S\to H\) coefficients are strictly negative. Thus the Jacobian in the R23 positive coordinates is not Metzler. A diagonal sign change cannot make every off-diagonal sign nonnegative: the positive \(A\leftrightarrow S\) and \(H\to S\) links require the three coordinates to have the same sign, while the negative \(A\to H\) link requires \(A\) and \(H\) to have opposite signs. This rules out the standard orthant cooperative test in these coordinates; it does **not** rule out every conceivable non-orthant or state-dependent order.

R23 does not need a globally order-preserving flow. It proves only forward invariance of a compact, trial-box-restricted cone for the one trajectory launched at the cone vertex under the fixed positive voltage-difference forcing. In particular, the affine \(1/\lambda\) term makes \(\dot H>0.78\) on the reachable part of the face \(H=0\), even though the derivatives of \(\dot H\) with respect to \(A\) and \(S\) are negative. The specific upper bounds keep the trajectory on that favorable face segment. This is a valid first-exit/Nagumo-style invariance argument, not the full pairwise order-preservation theorem of a cooperative system.

After cone invariance, the lower estimates on \(I,S,A\) are obtained from bounded parameter coefficients and scalar variation-of-constants inequalities. Then the output proof uses a separate local bound on \(\cos\theta\) and the heading-difference error. The source theorem does not supply those chain coefficients, the \(t^3\) lower response, or the final rational \(40\)-micrometre gap.

### Generic and plant-specific pieces

- **Generic:** augmenting two action-conditioned trajectories with shared frozen initial/parameter labels; testing a candidate cone by inward-pointing boundary conditions; first-exit/Nagumo invariance; integrating scalar differential inequalities; appending an output accumulator; and enclosing full-time predicates with a validated tube.
- **DDWMR/model-specific:** the chosen variables \(A,S,I\), the extra facet \(H=I-A/20\), the finite box on which each face inequality holds, coefficient margins derived from the motor/wheel/slip/body equations, the proof that both trajectories stay on the linear clip branch, the \(\cos\theta\) correction, and the stated synthetic obstacle/contact margins.
- **Not shown:** an order-preserving theorem for the full nine-state voltage-driven plant; a general monotone output map for \(J\); a theorem valid for arbitrary MASTER traction shapes; physical tire/support correspondence; or a finite-resource computational advantage.

## 5. Surviving question and disposition

The equation-level comparison does **not** show that the R23 analytic calculation is merely an application of a standard cooperative-system theorem. The natural transformed difference system fails that theorem's Metzler test, and the terminal displacement needs a separate heading estimate. The accepted rational result therefore remains a genuine *model-specific synthetic lemma*.

However, no useful distinct **research contribution** remains for the frozen R23 family on the evidence now available:

1. Its order statement compares matched realizations only. R24 refutes a common task threshold at the two wider cells and does not resolve it at the intermediate cells.
2. The narrow cell where a common threshold is established has no task threshold or operating-domain provenance from an external use specification.
3. The assumptions fix an engineered clip law, parameter labels and geometry. MASTER v2.1 does not establish that they represent a physical platform or constitutive tire/contact law.
4. The five-source audit distinguishes the proof mechanism from the plant inequalities, but does not close the dedicated DDWMR/contact prior-art search. Exact-case derivation alone is not evidence of originality or practical value.

**Recommendation: stop this synthetic analytic-novelty branch.** Preserve the accepted R23/R24 calculation as a narrow synthetic result or method-validation example, with matched ranking clearly separated from common-threshold claims. Do not extend it through more hand-tuned threshold cells, use the selected Auer pilot as a comparison workload, or promote the proof to a task or hardware claim. No new falsifiable contribution hypothesis is proposed because the current result lacks a declared use domain in which that hypothesis would matter.

## 6. Findings, consequences and status

### Finding 1 — Direct monotone-system implication does not apply

**Evidence:** In \(q=(A,S,H)\), the R23 Jacobian is not Metzler, has a sign-inconsistent cycle for diagonal orthant changes, and the \(\Delta J\) output is not monotone in this cone without R23's heading estimate.  
**Consequence:** Do not describe the action-order proof as a direct corollary of Angeli–Sontag, a standard positive linear system, or incremental positivity.  
**Status:** **NOT DIRECTLY IMPLIED** by the inspected monotone-control theorem.

### Finding 2 — The proof skeleton is established mathematics

**Evidence:** Cone forward-invariance/first-exit reasoning and scalar comparison are generic; the inspected validated-reachability papers also provide machinery to encode the shared fixed labels and bound the paired output.  
**Consequence:** The proof style and paired-IVP architecture are not standalone novelty. The case-specific facet and output calculations are still the substance of R23's narrow lemma.  
**Status:** **GENERIC METHOD OVERLAP; finite generic-method tightness UNVERIFIED.**

### Finding 3 — No useful contribution claim survives for this frozen synthetic branch

**Evidence:** Matched \(\Delta J>1/25{,}000\) m is accepted, but common-threshold separation fails at \(\eta=10^{-3},10^{-2}\), is unresolved at \(10^{-5},10^{-4}\), and is established only at \(\eta=10^{-6}\); no owner threshold or physical operating domain is declared.  
**Consequence:** Stop the synthetic analytic-novelty branch and retain R23 as a scoped lemma. G4 remains open and unverified; the limited source comparison does not justify an absence-of-prior-art claim.  
**Status:** **STOP THIS BRANCH; G4 UNVERIFIED.**

## 7. Execution ledger

- Auer/R3/G2 native queries: **0**.
- Workers, stages, retries, or new batch entries: **0**.
- Auer batch: **paused and unchanged**.
- R19/R20, R23/R24 and their review evidence: **unchanged**.
- Solver, code, manifest, resource criterion, or new workload: **none**.
- MASTER/canonical research context: **unchanged**.
- Commit/push: **none**.
- Project disposition: **HOLD; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.**

## Primary-source links

- Angeli & Sontag, DOI [10.1109/TAC.2003.817920](https://doi.org/10.1109/TAC.2003.817920); author manuscript [arXiv:math/0206133](https://arxiv.org/pdf/math/0206133).
- Auer, Kiel & Rauh, DOI [10.2478/amcs-2013-0055](https://doi.org/10.2478/amcs-2013-0055); retained local full text: research/third_party/auer2013/auer-kiel-rauh-2013.pdf.
- Arcak & Maidens, author manuscript [arXiv:1709.06661](https://arxiv.org/pdf/1709.06661).
- Meyer, Devonport & Arcak, author manuscript [arXiv:1902.05204](https://arxiv.org/pdf/1902.05204).
- Houska, Villanueva & Chachuat, [author-hosted full paper](https://faculty.sist.shanghaitech.edu.cn/faculty/boris/paper/stableSetIntegrator.pdf).
- Existing equation/review records: [G4 R23 paired-method handoff](LUNA_TO_CODEX_G4_AUER_R23_PAIRED_METHOD_OVERLAP_AUDIT_FULL_HANDOFF.md), [G4 R23 Codex review](CODEX_G4_AUER_R23_PAIRED_METHOD_OVERLAP_AUDIT_REVIEW.md), [G2 R23 handoff](LUNA_TO_CODEX_G2_R23_CORRELATED_ACTION_GAP_SCALING_RESEARCH_FULL_HANDOFF.md), [G2 R24 handoff](LUNA_TO_CODEX_G2_R24_PAIRED_BOUND_AND_THRESHOLD_ADVERSARIAL_AUDIT_FULL_HANDOFF.md), and [G2 R24 Codex review](CODEX_G2_R24_PAIRED_BOUND_AND_THRESHOLD_AUDIT_REVIEW.md).
