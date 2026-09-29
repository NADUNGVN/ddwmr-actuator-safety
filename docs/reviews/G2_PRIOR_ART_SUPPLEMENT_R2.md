# G2 R2: targeted prior-art supplement

2026-09-29. Research evidence supplement to the unchanged canonical LITERATURE_MATRIX and [v1 audit](G2_PRIOR_ART_AND_BLOCKERS_v1.md). No G4 closure; unknown is not No. Primary-source access below is scoped to the stated passages, not a claim of exhaustive full-paper review. No source establishes novelty of Case A.

## Additional primary-source comparison

| ID / source | Access and inspected location | Relevant established result | Comparison with G2 and outstanding work |
|---|---|---|---|
| R2-01 Lin and Stadtherr, *Validated Solutions of Initial Value Problems for Parametric ODEs*, accepted author manuscript revised October 2006 | [Author manuscript](https://academicweb.nd.edu/~markst/lin-stadtherr-vspode-apnum.pdf), full text accessible; Section 2, Eq. (1); Sections 4.1--4.2, Eqs. (18)--(23) | Time-invariant interval parameters; Picard/existence enclosure over a complete step, followed by Taylor-model tightening. Stated differentiability requirements exclude branches/abs/min/max in the function representation. | Fixed parameters and a finite full-time enclosure are already addressed. Our Lipschitz proof differs in assumptions, but Case A stays inside the linear part of clip: its nonsmooth global definition alone does not establish an advantage. A fair applicable-method comparison remains unperformed. |
| R2-02 Collins et al., *Rigorous Function Calculi in Ariadne*, arXiv:2306.17541v2 | [Primary full text](https://arxiv.org/html/2306.17541v2), Section 6.2 | Parameterized flow phi(x,t,a); bound refinement B'=D+[0,h]conv(f(B)); validated Picard composition/integration and Taylor flow models. | A finite predictor with an enclosure is established methodology. G2 separates a linear actuator block before bounding residuals; neither that decomposition nor our use of only Lipschitz contact automatically establishes originality. Applicable flow-model representation and computational comparison remain open. |
| R2-03 Houska, Villanueva and Chachuat, *Stable Set-Valued Integration of Nonlinear Dynamic Systems Using Affine Set-Parameterizations*, SIAM J. Numer. Anal. 53(5), 2015, 2307--2328 | [Author-hosted paper](https://faculty.sist.shanghaitech.edu.cn/faculty/boris/paper/stableSetIntegrator.pdf), full text accessible; Section 3 assumptions A1--A3, Eqs. (3.1)--(3.4), Theorem 3.1, Corollary 3.2 | Predict a parametric reachable set, then validate a step using a remainder condition. The theorem encloses every intermediate time; the corollary gives an interval sufficient check. The displayed assumptions require smooth/factorable data. | This is a direct threat to generic predictor-validation novelty. G2 has a different residual bound but has not shown a useful advantage over this construction. Case A does not discriminate between them. |
| R2-04 Althoff, Stursberg and Buss, *Reachability Analysis of Nonlinear Systems with Uncertain Parameters using Conservative Linearization*, CDC 2008 | [Author archive](https://archive.air.in.tum.de/2018/Main/Publications/Althoff2008c.pdf), accessible PDF; Section II Eq. (1), Section III and Fig. 1 inspected; later retrieval intermittent | The declared parameters can vary with time within bounds; nonlinear flow is enclosed through local linearization plus a bounded error input, with set splitting. Full intervals and endpoints are distinguished. | A switching-parameter outer relaxation differs from our fixed-parameter fibers, but uncertainty-aware nonlinear enclosures are prior art. Later theorem/remainder details and the cost of retaining fixed dependence still require direct comparison; no claim that this paper already has the entire DDWMR problem. |
| R2-05 Zivanovic Gonzalez et al., *Higher Order Method for Differential Inclusions*, arXiv:2001.11330 | [Primary manuscript](https://arxiv.org/pdf/2001.11330), full text accessible; Eq. (28), Theorems 8--9 and their local-error assumptions inspected | Finite-parameter approximations of uncertain inputs and rigorous local error estimates; the inspected theorems require C^2 vector fields and moment conditions, with different second/third-order conclusions. | Time-varying input approximation is not the fixed hidden-capacity semantics of MASTER. Nevertheless analytical predictor-error certification is established. Comparing applicable assumptions and any fixed-parameter embedding remains necessary. This is not a complete audit of every result in the paper. |
| R2-06 Althoff, *Reachability Analysis of Nonlinear Systems using Conservative Polynomialization and Non-Convex Sets*, 2013 author paper | [Institutional PDF](https://mediatum.ub.tum.de/doc/1283922/39133.pdf), [author archive](https://archive.air.in.tum.de/Main/Publications/Althoff2013a.pdf). Retrieval returned metadata/first extraction; repeated section retrieval timed out. **PARTIAL** | Identified as the close conservative-polynomialization/differential-inclusion family. Section 3.1 is a retrieval target, not a completed equation audit in this supplement. | Keep as an active threat. Do not infer absence of voltage/contact applicability or certified time coverage from incomplete access. Exact abstraction and remainder comparison remain UNVERIFIED. |

The equations paraphrased above are source-local descriptions; they are not amendments to MASTER.

## Coverage of the ten families requested by GPT

| Requested family | Evidence location | Remaining limitation |
|---|---|---|
| 1. Uncertain-parameter conservative linearization | R2-04, Eq. (1) and algorithm structure | Later error theorem and fixed-versus-varying parameter effect need deeper comparison |
| 2. Verified Taylor-model ODE integration | R2-01, Eqs. (18)--(23) | No same-data computation |
| 3. Rigorous Picard/Taylor flow integration | R2-02, Section 6.2 | No applicable-tool arithmetic/cost audit |
| 4. Taylor-model nonlinear flowpipes | R2-02; Flow* lead in v1 audit | Flow* full theorem access remains incomplete |
| 5. Parametric continuous-time enclosures | R2-01, Section 4; R2-03, Theorem 3.1 | No superiority result |
| 6. Predictor-validation set-valued integration | R2-03, Theorem 3.1 and Corollary 3.2 | Strong direct overlap; no same-data comparison |
| 7. Polynomial differential inclusions | R2-06; R2-05 is adjacent, not a substitute | R2-06 equation audit incomplete |
| 8. Componentwise contraction/growth bounds | Arcak/Maidens evidence in v1 audit | Generic branch remains blocked |
| 9. Interval reachability toolchains | TIRA evidence in v1 audit | Numerical soundness/configuration comparison open |
| 10. Validated hybrid flowpipes | Flow* evidence in v1 audit; R2-02 Section 6.3 is a follow-up target | No completed hybrid-method theorem comparison here |

Coverage of a family is not exhaustive coverage of that literature. This supplement records five additional targeted mathematical inspections plus one partial lead; it does not silently upgrade the 27-row canonical matrix or its access statuses.

## Finding

Generic growth, parameter augmentation, Picard iteration, predictor-validation and flowpipe certification cannot support a standalone novelty claim. The new hand certificate does not change that conclusion.

## Evidence

The preceding primary passages establish the closest mechanisms independently of a DDWMR substitution. Case A uses a parameter box, a finite predictor, an error enclosure and a set-containment safety test. Those ingredients alone provide no equation-level distinction with demonstrated value.

## Consequence

The generic novelty branch remains stopped. A narrower research hypothesis is a useful coupled voltage/contact certificate with proven or measured conservatism/cost benefits on defensible data. That hypothesis remains unverified; the hand example does not establish it.

## Status

**BLOCKER** for generic-method originality; overall G4 **UNVERIFIED**. G2 analytical review may continue.

## Required action

Finish the incomplete primary passages and compare admissible constructions at matched data, assumptions and accuracy after appropriate authorization. A later implementation cannot be justified merely by renaming existing enclosure machinery. Do not change the model to evade the cited overlaps.
