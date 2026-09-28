# Luna G2 supporting audit v1

2026-09-29. Requested execution/research agent: **gpt-6-luna, reasoning max**. Read-only adversarial audit; no code or canonical edits delegated. Root records the returned findings below. This is supporting review evidence, not mathematical evidence by model agreement and not G2 acceptance.

## Reviewed construction

[G2 enclosure candidate](../../research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md), with the adopted v2.1 MASTER and four context files governing interpretation.

### Finding

Luna's returned core audit found the fixed-parameter Dini comparison, pose lift, algebraic contact bounds, and finite predictor generalization consistent with the declared assumptions. No extra differentiability, oddness or monotonicity assumption was needed in those checks.

### Evidence

The audit independently wrote the force-error split through the predictor, the componentwise Dini inequality with A^# + |D|Q, and the contact lower-budget/upper-demand comparison. It also checked the exact-kernel refinement using H<=exp(A^# t)|D| and the comparison-radius integral identity. Soundness starts from the established Dini bound; the supersolution inequality alone is not used as an unsupported comparison to the unknown error.

### Consequence

The submitted proof order is retained. The n=0 body-center limitation is explicitly reported; finite n>=1 predictors carry voltage into body motion. The candidate stays parameter-labeled with a single common held voltage. Contact-margin square roots are evaluated algebraically rather than differentiated.

### Status

**Preliminary supporting audit; G2 UNVERIFIED.** No useful numerical regime, computational implementation, original contribution or hardware correspondence is established.

### Required action

Submit the equations and proof to the user's independent GPT review. Verify finite arithmetic and usefulness separately after the current proof review and applicable authorization. Preserve the following reservations from Luna:

- Every matrix, predictor, radius and force bound must use the same parameter realization within its fiber; coefficient/parameter boxes are labeled outer relaxations.
- Explicit convolution notation alone is not finite certified computation. Matrix exponentials, phi, quadrature, pose/trigonometric evaluation and complete time/parameter ranges need validated bounds.
- MASTER specifies a Lipschitz function class but no selected numerical realization; do not invent one.
- Frozen-force body centers are voltage-independent, even though their error bounds can depend on voltage.
- No G3, stopping, hardware safety or novelty result follows from this enclosure.

## Supplemental audit of Sections 7–8

Luna completed the additional checks before publication:

- The finite-cell recurrence is a sound outer comparison when one candidate voltage is used across every time slab and parameter cell. The fallback d_ab=2 C_upper can be too loose for a useful certificate.
- The local predictor-difference, residual and error orders in G2.26 are consistent for each fixed finite n. They do not bound total uncertainty width over Theta or establish practical usefulness.
- The sparsity argument in G2.27 supports the stated upper response orders: current O(t), wheel rate O(t^2), body u/r O(t^3), heading/position O(t^4). It gives no lower avoidance authority or relative-degree theorem.
- Luna requested an explicit submultiplicative-norm qualification for the matrix-exponential remainder. Root added a compatible induced matrix norm after fixed coordinate scaling in Section 7.

All these checks remain supporting evidence. No evaluated phi/Theta, certified numerical arithmetic, practical hold range or positive margins have been demonstrated. The exact submitted equations remain subject to the full GPT review request; G2 remains UNVERIFIED.
