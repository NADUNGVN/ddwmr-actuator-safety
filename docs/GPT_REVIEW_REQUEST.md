# GPT research review request

This is a review instruction, not a replacement for MASTER. The user relays the review between GPT and Codex. Current status: **HOLD**.

## Access and revision

Repository: https://github.com/NADUNGVN/ddwmr-actuator-safety

The repository is private. Review only content actually accessible through authorized repository access or files attached by the user. A repository URL alone does not establish access. If access fails, request the four files below; do not infer their contents from earlier chats. State the branch and commit reviewed when available, or explicitly state that the review uses attached files without a verified commit.

## First message — establish current context

Read in this order, in full:

1. `research_context/MASTER_RESEARCH_CONTEXT_v2.md`
2. `research_context/DECISION_LOG.md`
3. `research_context/LITERATURE_MATRIX.md`
4. `research_context/REVIEW_GATE.md`

Treat MASTER as authoritative current formulation. Read `AGENTS.md` for the project operating contract. Earlier `docs/` and `research/` files marked historical are superseded wherever they conflict with MASTER. Do not use the seven-state relative-degree derivation as a result for the current nine-state plant.

First return a concise reconstruction of the nine-state model, voltage input, uncertainty, safety objects, robust quantifier order, and current G1–G4 status. Identify any contradictory instructions explicitly. No controller, simulator, experiment, or implementation specification before G1–G4 pass and a reviewed GO is recorded.

## Second message — G1 physical model audit

Review MASTER §§5–13 and the open questions in REVIEW_GATE. Check at equation level:

- Contact-force signs, reaction torques, units, dissipation, wheel/body energy consistency, and motor/gear conventions.
- Whether exact zero lateral velocity and axle-midpoint COM are needed; distinguish exact assumptions from approximate engineering statements.
- Lateral reaction forces during turning and compatibility with the available friction budget.
- Whether positive lower friction coefficient and the stated properties of phi provide the braking authority later claims would require; do not silently add monotonicity or a force lower bound.
- Passing through zero wheel speed versus sustained wheel lock, including required torque balance and physical driver/braking assumptions.
- Uncertainty trajectories, fixed parameter dependence, positive parameter bounds, state-information accuracy, and solution well-posedness.
- Straight-line symmetry, equilibria and zero-input behavior; state any extra conditions each check needs.

For each finding use:

**Finding / Evidence (file and section or equation) / Consequence / Status (VALID, NEEDS REVISION, BLOCKER, UNVERIFIED) / Required action.**

Stop claims dependent on unresolved physical assumptions. Propose exact edits for a possible next MASTER version, with reasons and tradeoffs; do not silently replace the accepted source. End with the unresolved decisions that require the user's review. A G1 pass alone does not authorize implementation.

## Later messages — G2, G3 and G4

After the affected G1 assumptions are resolved and logged:

1. **G2:** Audit a specific computable reachable enclosure, its proof of inclusion for every time in a hold, shared held voltage, coupled contact dynamics, and all admissible uncertainty trajectories. A simulated trajectory or global Lipschitz placeholder is insufficient evidence of a useful new construction.
2. **G3:** Audit a constructive, useful, nonempty K_T with K_T contained in Pre_T(K_T). Distinguish one-hold feasibility, sampled recursive safety, continuous collision safety, and exact viability. Certificate failure does not prove collision unavoidable.
3. **G4:** Audit primary full texts at equation/theorem level, including relevant contact/friction, robust reachability and recursive safety-filter work. Use LITERATURE_MATRIX as a preliminary evidence register. Its unknown cells do not prove absence of prior work. Record source version, theorem/equation locator, access limitations, overlap, and the exact new result needed.

Return separate gate verdicts and evidence, not an aggregate novelty score. Generic enclosure-to-safety and predecessor induction implications are not research novelty. Model agreement is not proof.

## Returning the review to Codex

The user pastes GPT's findings back into this project session. Codex checks the evidence and proposes corresponding MASTER/version, DECISION_LOG, matrix and gate changes. Keep HOLD until G1–G4 have explicit reviewed acceptance. Luna implementation follows only after that gate.
