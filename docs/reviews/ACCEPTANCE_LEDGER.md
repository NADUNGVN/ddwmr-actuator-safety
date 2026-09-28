> HISTORICAL / SUPERSEDED BY MASTER v2 (2026-09-28). Read [MASTER_RESEARCH_CONTEXT_v2.md](../../research_context/MASTER_RESEARCH_CONTEXT_v2.md), DECISION_LOG, LITERATURE_MATRIX and REVIEW_GATE first. This note records earlier analysis, not the current nine-state plant or an implementation authorization. Seven-state results must not be transferred to the current plant without a new derivation.

# Research review acceptance ledger

Date: 2026-09-28. This ledger records what can be accepted now and what still needs evidence. Acceptance of a conditional calculation is not acceptance of the final plant or permission to implement it.

| Item | Review disposition | Remaining evidence |
|---|---|---|
| Workspace isolation | Accepted operationally | Writes confined to new repository; sibling quadrotor Git status rechecked and matches initial listing; no bytewise sibling audit claimed |
| Scientific question | Retain | Physical significance must survive justified actuator/contact parameter ranges |
| Seven-state plant | Conditional candidate only | Contact/load consistency, COM/reference point, motor/gear conventions, driver capabilities, state observations |
| Local third-order voltage coefficient | Algebra accepted for fixed coefficients/disturbances | `2 rho a^T F_i L^-1`; vanishes at tangency; cannot serve as a global degree-three certificate |
| General slip claim | Rejected as presently formulated | Bounded gain cannot represent locked-wheel chassis skid; select and justify uncertainty class |
| Whole collision-free set invariant | Rejected | Use an appropriate augmented initial/certified set; inward boundary states provide counterexample |
| Instantaneous box feasibility identity | Accepted only for a single known affine inequality | Does not characterize joint robust feasibility, recursive feasibility, or physical inevitability |
| Generic reachable-tube induction | Valid conditional route | Must construct a sound tube and useful nonempty endpoint-return set; not itself novel |
| GPT feedback | Reviewed with corrections | Three root corrections accepted in follow-up; model agreement remains non-evidence |
| Literature novelty | Open | Closest full-text theorem comparisons and structured-method advantage still missing |
| Implementation and experiments | HOLD | Deliverables 1–5 acceptance and concrete formulation freeze required by handoff |

## What a sufficient next research result would contain

1. A single mathematical plant with all units and reference frames fixed, including the exact wheel-ground regime covered. Parameter values, if supplied later, must have sources or be clearly labelled hypothetical.
2. An uncertainty class compatible with the proof: fixed parameters, smooth signals with derivative bounds, or measurable bounded disturbances with an appropriate inclusion/flow interpretation.
3. A constructive action/set certificate that handles the admitted domain, including singular states if those states are claimed. Assuming that an admissible input always exists does not discharge the main feasibility question.
4. A complete comparison with at least the closest generic method on the same physical model. A theorem application to a different plant is not automatically a new theorem.
5. A clear statement of which results are exact, sufficient, restricted to straight braking, restricted to one obstacle, or numerical evidence only.

No numeric quality score is assigned before this evidence exists. This ledger is a review of the initial package, not a proof that all future assumptions can be satisfied.
