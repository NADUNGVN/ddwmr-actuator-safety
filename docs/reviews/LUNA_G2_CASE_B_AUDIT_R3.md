# Luna independent read-only audit — Case B

2026-09-29. Reviewer: `/root/luna_g2_audit`, requested Luna max role. Scope: canonical context, accepted Case A, proposed Case B arithmetic, and the final file [G2_CHALLENGE_CASE_B_v1.md](../../research/theorem_notes/G2_CHALLENGE_CASE_B_v1.md). No solver, simulation, implementation or file edit was requested or performed by the reviewer.

## Final reviewer response (verbatim)

**Finding:** I found no material error in Case B’s constants or proof. The reciprocal parameter image, ideal gear witness, positive comparison matrix, and saturation exit argument are consistent.

**Evidence:** The gear witness gives \(J_j=L_j=1/\rho_j\) with positive motor inertia throughout \([1,11/10]\). The bounds \(d_1\le16t^2\), \(q=28/5\), and the global, refined, and fallback radii check arithmetically. In B.15, \(N\ge M\) entrywise, including the current rows whose actual diagonal is \(-\rho_j\); its maximum row sum is \(28/5\). The B.23 upper bound follows from the stated exponential, cosine, and force-integral bounds. B.22 keeps left slip above 1 through \(t=0.01\), while B.24 places it between \(4/5\) and \(49/50\) at \(T=0.05\). Thus continuity establishes an exit from saturation during the hold.

**Consequence:** The reported contact and collision margins support only the stated finite case and the three locked scalar-ball evaluations. The obstacle is tuned, and the UNKNOWN evaluations do not imply unsafety or failure of other enclosures.

**Status:** This audit found no blocking defect in Case B; G2 remains **UNVERIFIED / HOLD**.

**Required action:** No correction is required for the audited claims. Keep the stated limits on the separation claim and the gate status.

## Root clarification and disposition

The review's shorthand about the gear witness must not be interpreted as a gear law for inductance. B.1 **assigns** L_j=1/rho_j as electrical data; the gear witness independently verifies reflected J_j=1/rho_j, B_j=1 and k_j=1. Their numerical correlation is a stipulated synthetic parameter family. The proof file already makes this distinction; no physical gear-induced inductance relation is claimed.

### Finding

The read-only arithmetic audit found no blocking defect. Case B remains a new candidate awaiting GPT review.

### Evidence

Primary evidence is the explicit derivation B.1--B.25, including the signed parameter-dependent kernels, matrix majorant and rational full-cell inequalities. Reviewer agreement alone is not proof.

### Consequence

Submit this case for independent equation review. No conclusion about online usefulness, alternative voltage decisions or originality follows from the internal check.

### Status

**UNVERIFIED** pending independent GPT review; G2 remains UNVERIFIED and overall HOLD.

### Required action

Follow [the R3 request](../GPT_G2_REVIEW_REQUEST_R3.md), retain the limited sufficient-evaluation comparison, and preserve all implementation boundaries.
