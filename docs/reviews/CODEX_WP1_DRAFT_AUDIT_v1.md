# Root audit — WP1 drafts

2026-09-29. **Internal analytic review; not independent GPT acceptance; HOLD.** No evaluator was implemented or run. This note concerns the new fallback specification and benchmark proposal, not a new audit of every A/B/C equation.

## W1-01 — finite positive-series tails

**Finding.** The proposed matrix-exponential and forced-comparison tail formulas are sound conservative norm bounds after consistent coordinate scaling.

**Evidence.** For Q>=0, the exponential remainder is bounded by exp(Q) Q^(N+1)/(N+1)!. For Q>0, exp(Q)<3^ceil(Q); Q=0 is handled exactly. For the comparison integral truncated through k=K, write k=K+1+j. Since (K+2+j)! >= (K+2)! j!, its omitted norm is bounded by T q exp(Q) Q^(K+1)/(K+2)!, where q bounds the forcing norm. A symmetric entrywise exponential error or a positive componentwise comparison tail follows from the infinity-norm bound.

**Consequence.** Neither primitive needs a floating exponential or inverse matrix. These estimates may be very wide; the proof supplies no efficiency claim.

**Status.** Analytic check passed for these formulas; implementation and practical widths unverified.

**Required action.** Preserve the order convention, Q=0 handling and state scaling in any later implementation. Do not use physical mixed-unit row sums without that scaling.

## W1-02 — requested primitive clarifications

**Finding.** The first Luna draft left three details insufficiently explicit: the sign and selection of square-root bounds, the construction of the pose-center range, and the mapping between scaled and physical error coordinates.

**Evidence.** A putative upper root with only s^2>=u is insufficient if s is negative. An instruction to enclose P^n does not itself give a finite pose recipe. Applying matrix norms after scaling requires restoring physical velocity/yaw-rate units before pose and contact tests.

**Consequence.** These are specification obligations, not changes to MASTER. Root requested bounded nonnegative root bisection, explicit interval pose formulas and the diagonal similarity/input/output transforms.

**Status.** Targeted revisions inspected and incorporated. Root additionally made the scaled-coordinate convention, componentwise Q/S coefficient bounds, finite clip extension and finite witness checks explicit. These are computational-subclass clarifications; MASTER is unchanged.

**Required action.** Independently review the revised evaluator paragraphs. Nonnegative bisection preserves lo^2<=a<=hi^2; the explicit pose ranges follow by interval integration from the same initial-state family. This internal check is not GPT acceptance of the full evaluator or its usefulness.

## W1-03 — conservative full-hold predictor

**Finding.** Whole-hold interval hulls can soundly enclose the finite predictors, but the draft does not supply general finite evaluation of the sharper fiber/global radius or exact-kernel refinement.

**Evidence.** If P_(k-1) encloses the previous predictor for all s in [0,T], interval evaluation of exp(A tau)[BV+DF(P_(k-1))] for tau in [0,T] encloses every integrand for 0<=s<=t<=T. Multiplication by [0,T] therefore encloses the variable-upper-limit integral. Subtracting two such hulls bounds the paired increment but discards its common initial-state and parameter dependence. Repeating the same complete-hold hull on smaller slabs is not a proof of tighter localization.

**Consequence.** The fallback can be reviewed for soundness. It cannot be presented as completion of all proposed comparison variants or as evidence that subdivision restores useful accuracy. Fixed-panel integral hG and partial-panel [0,h]G should be distinguished; the latter deliberately retains zero and need not converge to a signed integral under subdivision.

**Status.** **UNVERIFIED for usefulness; NEEDS ADDITIONAL SPECIFICATION for general global/refined comparison variants.**

**Required action.** Keep these gaps explicit in the benchmark. Review a localized predictor/radius recipe before locking comparison configurations that rely on it. No new hand case closes this algorithmic gap.

## W1-04 — benchmark data and scope

**Finding.** The proposed benchmark moves beyond exact-rest, matched-side, engineered-micrometer cases, but is synthetic and not locked.

**Evidence.** Six nonzero-width nine-state cells include two positive speed ranges and both turning signs. Twelve independent actuator/contact labels are fixed over the hold. The gear witness has positive rotor inertia since 1/rho>=10/11>1/10. Twelve scenes, three durations and nine voltages produce 1944 original state-action queries. These data were declared without running an evaluator.

**Consequence.** This supplies a concrete reviewable domain and denominator. It gives no coverage, voltage-selection usefulness, physical parameter provenance or runtime result. Work settings, acceptance criteria and external baseline applicability remain open.

**Status.** **DRAFT; NOT LOCKED; no quantitative result.**

**Required action.** Resolve the declared pre-lock gaps in one consolidated review. Preserve all original query denominators and UNKNOWN outcomes. Never count refined leaves as independent samples.

## W1-05 — readiness

**Finding.** The package is suitable for a consolidated scientific review, not yet a full validation-implementation work order.

**Evidence.** A conservative finite-evaluator draft, explicit benchmark proposal and primary-source comparison are present. General refined/global evaluation, a matched external baseline, resource settings and usefulness acceptance criteria are not all closed. The proposed validation-only policy remains unapplied pending the user's decision.

**Consequence.** There is no G2 PASS, no scoped WP2 launch and no G3 or operational GO. A reviewer may accept a narrower fallback specification while requiring revisions to the broader comparison package.

**Status.** **HOLD; G2/G3/G4 UNVERIFIED.**

**Required action.** Use `../GPT_WP1_CONSOLIDATED_REVIEW_REQUEST.md` to obtain all dispositions and exact edits in one returned Markdown file.
