# Luna independent arithmetic audit — G2 Case A R2

2026-09-29. Reviewer: `/root/luna_g2_audit`, requested Luna max role. Scope: read-only review of the incoming GPT handoff, canonical context, the proposed arithmetic, and then the actual file [G2_FINITE_CERTIFICATE_CASE_A_v1.md](../../research/theorem_notes/G2_FINITE_CERTIFICATE_CASE_A_v1.md). No implementation, numerical solver or experiment was run by the reviewer. No gate promotion.

The final file review below supersedes an earlier suggestion to describe M through its induced norm. The submitted proof instead uses positive-semigroup comparison, explicitly confirmed as valid in the final review. Coordinate scaling and ideal-gear labeling are present in the reviewed file.

## Final reviewer response (verbatim)

**Finding:** The certificate’s arithmetic checks out for the stated synthetic model. In particular, (A.10) is valid: Metzler positivity and \(M\mathbf1\le q\mathbf1\) imply \(0\le e^{Mt}\mathbf1\le e^{qt}\mathbf1\), which bounds the induced infinity norm because \(e^{Mt}\) is nonnegative. It does not rely on treating signed row sums as a matrix norm.

The data table includes the MASTER parameters and defines a fixed rational capacity box, common voltage, and full time slab. The \(n=1\) residual coefficient, global and refined radii, fallback radius, pose budgets, and positive collision/contact margins all check out. The finite primitive ledger covers the bounds used; the gear realization is consistently labeled ideal gear, and the coordinate scaling is explicit.

**Status:** VALID as a read-only arithmetic audit of Case A. No file changes made. This does not change the overall gate: **G2 remains UNVERIFIED**.

## Root disposition

### Finding

No arithmetic defect was identified by this independent read-only review.

### Evidence

The reviewer separately checked the residual coefficient, the rational exponential estimate, all three radius constructions and the safety/contact margins, then read the final case file. The proof chain A.1--A.23 is the primary evidence; reviewer agreement alone is not a proof.

### Consequence

The case is ready for the user's independent GPT equation-level review. It remains a synthetic one-hold example.

### Status

**VALID** as an internal arithmetic audit only. Independent GPT acceptance of Case A and general G2 usefulness remain **UNVERIFIED**.

### Required action

Follow [GPT_G2_REVIEW_REQUEST_R2.md](../GPT_G2_REVIEW_REQUEST_R2.md); preserve HOLD, the implementation boundary and all canonical statuses.
