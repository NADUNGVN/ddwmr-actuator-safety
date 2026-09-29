# Luna independent read-only audit — Case C

2026-09-29. Reviewer `/root/luna_g2_audit`, requested Luna max role. Scope: canonical context, the accepted Case B and the actual file [G2_VOLTAGE_SELECTION_CASE_C_v1.md](../../research/theorem_notes/G2_VOLTAGE_SELECTION_CASE_C_v1.md). Read-only analytic audit; no code, solver, simulation or edits requested or performed by the reviewer.

## Final reviewer response (verbatim)

**Finding:** Case C’s arithmetic and certificate argument check out for the declared matched-side synthetic family. I found no blocking error.

**Evidence:** The force bound \(F(z^0)\le(1331/2000)t^2\) gives \(|\Delta i_j|\le(161051/2400000)t^4\). The slip residual coefficient is \(453871/600000<4/5\), yielding the stated shared error bound \(\|E_{1,0}\|_\infty\le(18/25)t^4\). The generic pose lift is \((18/125)t^5+(8/1125)t^9\le(3/20)t^5\) over the slab. The collision margins calculate to \(13/2{,}000{,}000\) for zero voltage, \(67/18{,}000{,}000\) for \(a=1/4\), and \(-83/18{,}000{,}000\) for \(a=1\). The contact bounds also hold with the stated generic error box.

**Consequence:** This supports a narrow, same-rule certificate-output distinction between two forward voltage levels. The larger action’s UNKNOWN result does not establish collision or unsafety. The exact matched-side restriction, engineered clearance, already-safe zero action, and lack of a tracking objective limit the example’s decision relevance.

**Status:** Valid within the stated synthetic case; G2 remains **UNVERIFIED / HOLD**.

**Required action:** Preserve those scope limits and the distinction between UNKNOWN and unsafe. No correction is required to the audited equations.

## Root disposition

### Finding

The independent internal audit identifies no blocking defect. Case C still awaits GPT's equation-level review.

### Evidence

The primary evidence is the full-cell derivation C.1--C.16. Reviewer agreement alone is not proof and does not alter the general research gate.

### Consequence

The package can be submitted for external review with its existing restrictions. There is no practical superiority or originality claim.

### Status

**UNVERIFIED** pending independent GPT review of Case C. G2 UNVERIFIED; overall HOLD.

### Required action

Follow [the R4 request](../GPT_G2_REVIEW_REQUEST_R4.md), retaining the same-state, same-rule output claim and all limits on implementation and G3.
