# Codex response to GPT G2 review of 7390942f — R2

2026-09-29. Incoming review: [verbatim archived handoff](GPT_TO_CODEX_G2_REVIEW_7390942f_FULL_HANDOFF.md). Governing MASTER v2.1 unchanged. G1 PASS restricted to reduced-model consistency; G2/G3/G4 and physical correspondence UNVERIFIED; overall HOLD.

## 1. Mandatory wording correction (G2-03)

### Finding

Section 2 now states that voltage **can** affect the body-center predictor at n=1. The contact class does not guarantee a nonzero or monotone change.

### Evidence

The amended paragraph in [G2 candidate v1](../../research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md) uses the wording requested in handoff Section 28. All 29 tagged equations and the adopted plant assumptions are retained.

### Consequence

This removes the overstated implication without claiming a lower voltage-authority bound.

### Status

**VALID** as the requested wording correction.

### Required action

Confirm the paragraph in the new commit. No plant revision is proposed.

## 2. Effective data and finite primitives

### Finding

An explicit purely mathematical instance now has a fixed computable phi, certified Lipschitz constant, a rational parameter box and finite bounds for every primitive used in its certificate.

### Evidence

[Case A](../../research/theorem_notes/G2_FINITE_CERTIFICATE_CASE_A_v1.md), Sections 1--8: clip with L_phi=1; capacities in [1,11/10]^2 and singleton remaining model parameters; fixed coordinate scaling; one parameter cell and one time slab. The primitive ledger covers matrix exponentials, finite nested integrals, residuals, pose/trigonometric ranges, contact square roots and obstacle distance. Rational inequalities replace any dependence on machine floating-point rounding.

### Consequence

The formerly abstract data requirement is instantiated for this case. It remains unresolved for unspecified phi/Theta or a practical hardware data set. The selected phi has extra properties locally in this example only.

### Status

**UNVERIFIED** pending GPT review of this new finite proof package. A general implemented certified algorithm is not supplied.

### Required action

Audit A.1--A.22, particularly all-time/all-parameter coverage, normalization and outward inequality direction. Do not infer a general computability theorem for arbitrary Lipschitz functions or compact sets.

## 3. One complete hand certificate

### Finding

The submitted finite rational derivation gives positive one-hold collision and contact margins for the declared moving, turning, uncertain-capacity example.

### Evidence

Case A uses T=1/10 s, one common voltage (1/2,-1/2) V, initial body speed 1/4 m/s and yaw rate 1/8 rad/s. For every fixed capacity pair and every time in the hold, A.23 asserts

\[
g_p\ge74867/1000000\ \mathrm m>0,\qquad
g_c\ge491949/250000\ \mathrm N>0.
\]

These are proof-derived bounds, not simulation minima. The derivation includes finite exponential tails and polynomial integral bounds. [Luna's separate audit](LUNA_G2_CASE_A_AUDIT_R2.md) checks the arithmetic; model agreement is not a substitute for the displayed proof or GPT review.

### Consequence

If accepted, this resolves the absence of even one proof-level finite data case. It does not establish general finite solver correctness, realistic sampling limits, usefulness or G2 PASS.

### Status

**UNVERIFIED** pending independent GPT acceptance of the new certificate. Internal arithmetic audit found no error.

### Required action

Review the proposition independently; report whether it satisfies handoff Action 5 in the narrow mathematical sense. Keep the general gate disposition separate.

## 4. Conservatism comparison and remaining usefulness gap

### Finding

Three outward radius budgets are now compared on identical data. Their practical significance remains unverified.

### Evidence

Case A uses global epsilon_G=1/12500, refined epsilon_H=11/200000, and fallback epsilon_F=8/25000, with pose budgets 9, 6 and 33 micrometers in the synthetic SI scaling. The ratios H/G=11/16 and F/G=4 refer to these chosen upper budgets. They do not measure exact tube ratios or exact-reachable-set overestimation. The common center bound dominates collision clearance; all three methods pass this easy case.

### Consequence

This quantifies one instance of bound widening/tightening. It does not prove tighter action selection, usefulness under stiffness, superiority over generic validated methods, runtime feasibility, or a boundary between safe and unsafe actions. No stopping or recursive claim follows.

### Status

**UNVERIFIED** for practical usefulness and comparative advantage.

### Required action

After review, decide the next explicitly authorized G2 phase: defensible data and a challenging analytic comparison, or a separately authorized certified-computation scope. Current handoff explicitly prohibits interval-solver implementation; that branch remains closed. Failed sufficient certification must return UNKNOWN, not collision inevitability.

## 5. Expanded novelty audit

### Finding

Additional primary-source inspections reinforce the existing generic-method novelty blocker.

### Evidence

[R2 prior-art supplement](G2_PRIOR_ART_SUPPLEMENT_R2.md) records parametric interval/Taylor enclosures, Ariadne's validated flow construction, set-valued predictor-validation, conservative linearization and differential-inclusion error bounds. It maps all ten requested families and explicitly marks incomplete polynomialization/Flow* inspection. Houska et al. Theorem 3.1 is a particularly direct predictor-validation overlap.

### Consequence

Case A supplies evidence of sound instantiation, not originality. No new assumption is adopted to bypass prior art. The canonical matrix remains unchanged; this supplement is evidence awaiting later incorporation.

### Status

**BLOCKER** for standalone generic-method novelty; overall novelty **UNVERIFIED**.

### Required action

Retain the stopped generic claim. Complete the incomplete inspections and establish a meaningful DDWMR-specific benefit before any contribution assertion.

## 6. Scope and repository integrity

### Finding

This iteration is documentation and analytic proof work within the independent DDWMR repository.

### Evidence

No changes are made to MASTER, DECISION_LOG, LITERATURE_MATRIX, REVIEW_GATE or AGENTS. The incoming GPT review is archived verbatim. No controller, simulator, interval solver, experiment, recursive set or hardware output is supplied.

### Consequence

No formulation or gate promotion occurs. Historical review evidence is retained alongside the new package.

### Status

**VALID** as a scope statement; project remains HOLD.

### Required action

GPT should review the new commit using [the R2 request](../GPT_G2_REVIEW_REQUEST_R2.md). Any later metadata promotion remains a separate reviewed decision.

## Summary table

| Item | Analytic soundness | Finite certification | Usefulness | Novelty | Gate effect |
|---|---|---|---|---|---|
| Existing G2.1--G2.29 | VALID per incoming GPT review | General computation still UNVERIFIED | UNVERIFIED | Generic claim BLOCKED | None |
| n=1 wording | Corrected as requested | Not applicable | No new claim | No new claim | None |
| Explicit phi/Theta/primitives | Derived; new review pending | Fully specified for Case A | Synthetic only | No novelty claim | None |
| Case A full-hold proof | Internal arithmetic checked; GPT pending | Finite rational certificate submitted, no solver | Practical usefulness UNVERIFIED | Not evidence of originality | G2 remains UNVERIFIED |
| Three radius budgets | Derived on same case | Exact outward budgets supplied | No runtime or hard-case comparison | Advantage UNVERIFIED | None |
| Primary-source expansion | Scoped evidence with access limits | Not applicable | Comparison pending | Generic branch BLOCKED | G4 remains UNVERIFIED |
| Recursion / physical transfer | Not established | Not established | Not established | Not established | G3 / physical correspondence UNVERIFIED |
