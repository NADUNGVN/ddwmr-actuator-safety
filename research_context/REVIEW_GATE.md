# Research review gates - adopted formulation v2.1

Read the canonical MASTER_RESEARCH_CONTEXT_v2.md, DECISION_LOG and LITERATURE_MATRIX before reasoning. **Overall HOLD; G1 PASS - restricted reduced-model scope; G2/G3/G4 UNVERIFIED.** This tracker accompanies the adopted v2.1 formulation. Formulation adoption is not gate acceptance.

| Gate | Status | Evidence required | Evidence present |
|---|---|---|---|
| G1 Plant consistency | PASS - restricted reduced-model scope | Internal consistency of adopted reduced ideal model only | Independent G1 review of commit `8341014eac52ea66fe38559d6e1baee92e8f9b96`: G1-01 through G1-12 VALID; see `../docs/reviews/GPT_TO_CODEX_G1_REVIEW_8341014e_PASS.md`. Physical-platform correspondence UNVERIFIED |
| G2 Certified enclosure | UNVERIFIED | Joint outer enclosure for every execution-fixed parameter, one held voltage, all times and coupled motor/wheel/body/contact dynamics | Analytic framework reviewed; synthetic hand Cases A/B/C accepted at `d2cd854` / `1da2166` / `c9ff32d`. See `../docs/reviews/GPT_G2_R3_1da2166_ACCEPT_RECORD.md`. General evaluator, practical usefulness, voltage-selection value and tractability remain unverified; Case C accepted only as a narrow synthetic certificate-output example |
| G3 Recursive subset | UNVERIFIED | Useful K_T, admissible observation-based voltage selection, full-hold contact/collision safety and robust endpoint return | Sufficient predecessor specification only; no useful set or policy proof |
| G4 Novelty | UNVERIFIED | Primary-source equation/theorem/computation comparison under reduced capacity and fixed-parameter scope | Preliminary matrix; no novelty closure |

## G1 - accepted internal consistency of the restricted reduced model

- [x] Accept or revise the reduced ideal planar scientific scope and title. Formal safety of this model is not validated physical robot safety.
- [x] Check exact axle-COM geometry, exact lateral constraint, signs, units and electromechanical energy identity.
- [x] Check F_j=C_j phi and the matching envelope F_j²+Y_j²<=C_j², reaction selection including zero lateral capacity, and the parameter-specific validity set.
- [x] Confirm C_j has force units and is an execution-fixed reduced-model parameter; no literal mu_j or N_j remains in the formal parameter vector or force equations.
- [x] Review the known fixed phi assumptions; neither oddness nor monotonicity is silently used in the core. Any auxiliary pure-spin assumption must be local to that analysis.
- [x] Review compact joint parameter bounds and correlations, exact sampled-state information and ideal drive/gear conventions.
- [x] Check rest/equilibrium, mirror covariance, matched-side straight motion and wheel-zero statements under their actual assumptions.

Remaining quantitative/physical-validation obligation (not a failed G1 consistency check):

- [ ] Identify the function/parameter data needed for later quantitative work without inventing physical provenance.

Physical transfer remains UNVERIFIED. Before a claim about actual hardware, establish a platform/support/contact mapping or sound model-error enclosure on an explicit operating domain. A calibrated capacity envelope alone does not establish the exact force law or prove trajectory inclusion. This physical correspondence is not silently resolved by renaming mu_j N_j. G1 PASS applies only to internal consistency of the restricted theoretical scope. Physical-platform correspondence: **UNVERIFIED**.

Braking, finite stopping distance and persistent-lock backup claims require separate compatible voltage-policy proofs. They cannot be silently used to support G3. Their absence is not by itself a failure to define a reduced ODE.

## G2 research authorized; G3 requires separate authorization

2026-09-29, workflow W1: user authorized G2 analytic research and scoped G2/G4 validation code, with the user mediating Luna execution. This does not accept G2 or authorize G3/operational implementation. GPT accepted finite rational Cases A/B/C in their recorded synthetic scopes; multiple hand certificates now exist. General certified evaluation, practical usefulness and runtime remain UNVERIFIED. Assignment: `../docs/LUNA_VALIDATION_HANDOFF_v1.md`.

- [x] One explicit finite hand case with evaluable phi, effective Theta, full-time primitive bounds and positive collision/contact margins: Case A only.
- [x] One synthetic challenge with parameter-dependent actuator matrices, correlated fixed labels, saturation exit and strictly scoped certificate outputs: Case B only.
- [ ] Establish decision-relevant voltage-selection value: same state/parameters/locked evaluation, trace the action distinction through actuator/contact dynamics. Case C C.1--C.16 passed independent equation review and demonstrates a same-rule voltage-dependent certificate-output distinction. This usefulness item remains unchecked: exact rest, an already-safe zero action, engineered clearance and no task/tracking tradeoff do not establish a useful operating domain.
- [ ] Establish practical parameter relevance, useful conservatism and eventually tractability; Cases A/B do not establish these.

- [ ] Preserve joint state/parameter dependence or quantify the conservatism of a sound relaxation.
- [ ] Use one voltage for all hidden parameters, constant along each entire execution; do not reset or existentially select favorable parameters.
- [ ] Prove full-hold collision and contact-domain preservation with actuator/contact coupling intact.
- [ ] Do not assume differentiability or Lipschitz continuity of the square-root contact margin at saturation.
- [ ] Construct a useful recursive subset with robust endpoint return and non-oracle input selection. Rest states alone do not establish usefulness.
- [ ] Keep sampled K_T membership, continuous model safety, state-only conservative recursion and history-dependent fixed-parameter viability distinct.

## G4 under the narrowed scope

- [ ] Compare fixed unknown tangential capacity, time-varying friction, full tire/support/load dynamics and reduced nonholonomic constrained models separately.
- [ ] Audit voltage-level models, robust joint state/parameter reachability, inter-sample safety and recursive filtering at equation/theorem level.
- [ ] Record source-access limitations; unknown is not No. Preserve existing novelty threats until checked.
- [ ] Identify an actual useful construction beyond plant substitution, parameter renaming or generic enclosure/predecessor logic.

## Review and implementation gate

Use Finding / Evidence / Consequence / Status / Required action. Stop affected branches on contradiction. G1 is resolved for the restricted model. User authorization W1 permits scoped G2/G4 validation coding; current W2 (2026-10-07) lets the two owner-started Luna max sessions own the complete verification packages, coordinate through repository files, correct routine defects, cross-audit and run covered bounded offline validation without a new Codex GO per iteration. Follow `../docs/DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2.md` and its two session assignments. Prior per-iteration permission waits are superseded, not mathematical blockers. Draft specifications must be audited; benchmark locks and unsupported refinements remain explicit. Codex does not autonomously delegate. G3 and operational controller/closed-loop/hardware work remain outside the assignments. All gate statuses remain unchanged; final independent scientific review is still required for gate promotion.
