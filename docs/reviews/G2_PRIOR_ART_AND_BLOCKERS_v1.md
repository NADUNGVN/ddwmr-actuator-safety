# G2 preliminary overlap audit and blockers

2026-09-29. Supports [G2 candidate v1](../../research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md). This is targeted primary-source screening, not completion of G4. No absence-of-prior-art claim is made.

## Primary evidence inspected

| Source | Directly inspected location | Established overlap | Limit of this inspection |
|---|---|---|---|
| Arcak and Maidens, *Simulation-based reachability analysis for nonlinear systems using componentwise contraction properties*, 2017 author manuscript | [Author manuscript](https://arxiv.org/pdf/1709.06661), §2 Proposition 1, Corollary 1, §3 Algorithm 1 and Example 1 | Componentwise matrix-exponential growth bounds; constant uncertain parameters as zero-dynamics coordinates; parameter grouping to reduce overestimation | The displayed proposition assumes a continuously differentiable vector field; the draft here uses a direct Lipschitz/Dini proof. That distinction alone does not establish novelty. No exhaustive follow-up literature audit |
| Meyer, Devonport and Arcak, *TIRA: Toolbox for Interval Reachability Analysis*, 2019 author manuscript | [Author manuscript](https://arxiv.org/pdf/1902.05204), §3.1 Assumption 3, Eq. (4), Proposition 4 and remarks | Interval enclosures with a contraction/growth matrix, exponential propagation and integrated uncertainty forcing; generalized growth-bound functions | A tool/method survey plus stated results, not a proof that every numerical solver invocation is certified. Full numerical comparison with the present candidate remains open |
| Chen, Abraham and Sankaranarayanan, Flow*: An Analyzer for Non-Linear Hybrid Systems, CAV 2013 | [Author publication page](https://home.cs.colorado.edu/~srirams/papers/cav2013-flowstar.html), abstract; author PDF first-page extraction available through search | Guaranteed Taylor-model flowpipe approximation is established prior work | Direct PDF open returned an internal retrieval error. No full theorem audit or smoothness comparison was completed; do not label this as full-text verification |

## Finding A — generic growth-bound novelty

### Finding

The linear comparison radius and fixed-parameter labeling in the G2 draft overlap established reachability techniques. Writing them for a DDWMR is not enough to claim a new method.

### Evidence

The first two inspected sources explicitly exhibit the relevant matrix-exponential/componentwise machinery. The first also treats constant unknown parameters. The draft's proof rederives a safe sufficient bound using the adopted Lipschitz contact law; it is not evidence of priority.

### Consequence

Separate G2 soundness from G4 originality. Any future contribution must demonstrate an additional useful construction or a nontrivial physical-authority result and survive direct comparison.

### Status

**BLOCKER for a standalone novelty claim based on generic comparison or parameter augmentation.** G2 soundness research may continue under the authorized scope.

### Required action

Retain this overlap as an active threat. Compare the completed construction and its cost/conservatism against the closest applicable alternatives before claiming novelty. No numerical baseline implementation is authorized now.

## Finding B — frozen-force predictor misses directional voltage effect

### Finding

At predictor depth n=0, body-center u and r are independent of the held voltage. Calling that center an actuator-aware avoidance construction would overstate what was built.

### Evidence

G2.2 has no current/wheel-to-body coupling in A; the body is driven through D F. Freezing F at F(z_0) removes voltage from that center's body equations. This is an algebraic limitation, not an empirical result.

### Consequence

The n=0 predictor remains a bounding initializer. The candidate direction uses n>=1 with rigorous residual error; no plant assumption is changed.

### Status

**NEEDS REVISION for use of n=0 alone as a useful safety-filter model; addressed in the submitted candidate by finite integral iterations.** Usefulness remains UNVERIFIED.

### Required action

Reviewer should check that n>=1 really propagates voltage through the contact law and that the radius does not erase the useful effect. No universal performance assertion is permitted.

## Finding C — analytic enclosure versus finite certificate

### Finding

The abstract MASTER supplies no selected evaluable phi, numerical parameter set, certified arithmetic, or declared practical hold range. Those are required to demonstrate a useful finite certificate.

### Evidence

The fiber union ranges over a compact set and continuous time; existence of these objects is not an algorithm for evaluating them. Full-hold verification requires interval/time-domain bounds, including integral and rounding errors.

### Consequence

An analytic inclusion proof can be reviewed now. Quantitative certification and G2 usefulness remain open. Do not silently substitute tanh or fabricate hardware values.

### Status

**UNVERIFIED for finite certified computation and practical usefulness.** An unspecified effective representation blocks a numerical instantiation, not the parameterized analytic proof.

### Required action

After proof review, explicitly select a mathematical example or obtain platform-grounded data with provenance. Declare which it is. Implement only after the existing implementation gate is changed or passed; no implied exception here.

## Finding D — interval losses and motor stiffness

### Finding

Metzler majorization loses signed motor feedback; scalar contact and ur product bounds lose correlations. These losses may dominate practical conservatism.

### Evidence

The draft exposes both transformations and provides an optional exact impulse-response refinement, with a monotone upper-bound proof. It provides no numerical tightness or runtime evidence.

### Consequence

Neither G1 power consistency nor stable motor dynamics ensures the comparison radius stays useful. Failed certification is inconclusive about physical safety.

### Status

**UNVERIFIED.** No evidence yet supports a claim that practical sampling periods are certified.

### Required action

Audit growth and dependence loss on defensible parameters later. If useful intervals collapse, stop the affected method branch; do not mask it with favorable simulation choices.

## Scope retained

The candidate is one-hold theory for the restricted ideal plant. It establishes no stopping policy, recursive set, QP feasibility, exact viability, real-platform safety, or Q1 readiness. G2/G3/G4 remain UNVERIFIED and the overall project remains HOLD.
