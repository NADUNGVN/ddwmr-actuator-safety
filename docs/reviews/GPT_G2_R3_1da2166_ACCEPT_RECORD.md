# GPT G2 R3 disposition record — Case B accepted

Recorded 2026-09-29 from the user's complete 30-section pasted GPT review. Repository `NADUNGVN/ddwmr-actuator-safety`, branch `main`, reviewed commit `1da2166949ad12a0741c876c3a0daf8a5d957ddf`.

This is a structured record, **not a verbatim transcript**. The original review was supplied in conversation; no browser interaction with GPT was used.

## Accepted findings

| Incoming sections | Inspected content | Disposition |
|---|---|---|
| 1--4 | B.1--B.5 correlated label image, gear witness, common voltage, initial contact status, parameterized motor kernels and frozen-force predictor | VALID |
| 5--9 | B.6--B.10 uniform predictor/slip/residual bounds and center ranges | VALID |
| 10--12 | B.11--B.14 positive semigroup, rational exponential, global/refined radius coefficients | VALID |
| 13--14 | B.15--B.16 explicit entrywise N>=M, including -rho current diagonals, full-slab fallback | VALID |
| 15--16 | B.17--B.19 pose budgets and deliberately engineered three-evaluation separation | VALID, strictly limited to the locked evaluations |
| 17--18 | B.20--B.21 right-wheel reserve, zero credited left reserve and contact margin | VALID |
| 19--21 | B.22--B.24 true formal trajectory initially saturated through 10 ms and unsaturated at 50 ms; global proof is noncircular | VALID |
| 22 | B.25 continuous one-hold safety for all fixed labels and a common voltage | VALID / ACCEPT |
| 23--24 | Multiple finite synthetic cases now exist; general evaluator and practical usefulness remain open | Scoped progress only |
| 25--26 | Generic originality blocked; comparison does not establish general method superiority or voltage necessity | BLOCKER / limitations retained |
| 27--30 | Next priority is decision-relevant voltage selection; no G2 promotion | G2 UNVERIFIED; HOLD |

## Accepted scope

Case B B.1--B.25 is accepted as a finite synthetic hand certificate. For the exact declared data the refined evaluation has collision lower margin 8/10^6 m and contact lower margin 885209/10^6 N throughout [0,1/20] for every fixed label in [1,11/10]^4.

The formal left slip stays above 1 through 10 ms and lies between 4/5 and 49/50 at 50 ms. The correlated parameter image is preserved. N dominates M entrywise; an all-upper-corner shortcut must not replace the explicit proof because current diagonals are -rho.

Permitted separation: on this tuned instance, using the same center-ball rule, the locked one-refinement scalar evaluation is CERTIFIED while the two specified coarser scalar evaluations return UNKNOWN. This says nothing about actual unsafety, the exact global tube, all implementations, other pose enclosures, necessity of n=1 or of the chosen voltage, or practical superiority.

## Finding

GPT independently accepts Case B including saturation exit and the strictly limited certificate separation.

## Evidence

The user-relayed review checks every group B.1--B.25 and explicitly constructs the parameter-dependent M to verify B.15. Reviewed equations remain accessible in the cited commit and [Case B](../../research/theorem_notes/G2_CHALLENGE_CASE_B_v1.md).

## Consequence

Multiple explicit finite synthetic certificates exist, including actuator-parameter dependence and saturation crossing. A useful general evaluator, practical data, tractability and meaningful voltage-selection value remain unverified.

## Status

**Case B ACCEPT only. G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED; HOLD.** Generic-method novelty BLOCKED. No implementation, experiments, G3 or GO.

## Required action

Prioritize a finite analytic voltage-selection challenge: same initial state, parameter set and locked evaluation, one admissible held voltage CERTIFIED and another UNKNOWN, with the distinction traced through voltage/current/wheel/slip/force/body dynamics. UNKNOWN is not unsafety. Continue the separate matched-assumption generic-method comparison for G4. No plant amendment or implementation authorization follows.
