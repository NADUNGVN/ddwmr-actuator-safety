# Research review gates - adopted formulation v2.1

Read the canonical MASTER_RESEARCH_CONTEXT_v2.md, DECISION_LOG and LITERATURE_MATRIX before reasoning. **Overall HOLD; no gate has passed.** This tracker accompanies the adopted v2.1 formulation. Formulation adoption is not gate acceptance.

| Gate | Status | Evidence required | Evidence present |
|---|---|---|---|
| G1 Plant consistency | NEEDS REVISION | Independent review of actual reduced capacity model and scientific scope; units, signs, energy, geometry, reactions, uncertainty, information and driver conventions | F01–F12 audit, archived GPT handoffs and Codex responses; conditional algebraic/model identities, no accepted G1 |
| G2 Certified enclosure | UNVERIFIED | Joint outer enclosure for every execution-fixed parameter, one held voltage, all times and coupled motor/wheel/body/contact dynamics | Corrected target only; no enclosure constructed |
| G3 Recursive subset | UNVERIFIED | Useful K_T, admissible observation-based voltage selection, full-hold contact/collision safety and robust endpoint return | Sufficient predecessor specification only; no useful set or policy proof |
| G4 Novelty | UNVERIFIED | Primary-source equation/theorem/computation comparison under reduced capacity and fixed-parameter scope | Preliminary matrix; no novelty closure |

## G1 — review the actual revised text

- [ ] Accept or revise the reduced ideal planar scientific scope and title. Formal safety of this model is not validated physical robot safety.
- [ ] Check exact axle-COM geometry, exact lateral constraint, signs, units and electromechanical energy identity.
- [ ] Check F_j=C_j phi and the matching envelope F_j²+Y_j²<=C_j², reaction selection including zero lateral capacity, and the parameter-specific validity set.
- [ ] Confirm C_j has force units and is an execution-fixed reduced-model parameter; no literal mu_j or N_j remains in the formal parameter vector or force equations.
- [ ] Review the known fixed phi assumptions; neither oddness nor monotonicity is silently used in the core. Any auxiliary pure-spin assumption must be local to that analysis.
- [ ] Review compact joint parameter bounds and correlations, exact sampled-state information and ideal drive/gear conventions.
- [ ] Check rest/equilibrium, mirror covariance, matched-side straight motion and wheel-zero statements under their actual assumptions.
- [ ] Identify the function/parameter data needed for later quantitative work without inventing physical provenance.

Physical transfer remains UNVERIFIED. Before a claim about actual hardware, establish a platform/support/contact mapping or sound model-error enclosure on an explicit operating domain. A calibrated capacity envelope alone does not establish the exact force law or prove trajectory inclusion. This physical correspondence is not silently resolved by renaming mu_j N_j. G1 for the restricted theoretical scope still needs explicit independent acceptance; no pass is recorded here.

Braking, finite stopping distance and persistent-lock backup claims require separate compatible voltage-policy proofs. They cannot be silently used to support G3. Their absence is not by itself a failure to define a reduced ODE.

## G2/G3 after G1 resolution

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

Use Finding / Evidence / Consequence / Status / Required action. Stop affected branches on contradiction. G1 scope/assumptions must be resolved before G2/G3 construction. No controller/simulator/experiment implementation before all G1–G4 pass and reviewed GO is recorded in MASTER and DECISION_LOG. Adoption of a formulation revision is not a gate pass.
