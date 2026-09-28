# Research review gates — v2

Read MASTER, DECISION_LOG and LITERATURE_MATRIX first. **Overall HOLD. No gate has passed.** This tracker is subordinate to MASTER.

| Gate | Status | Evidence required | Evidence present |
|---|---|---|---|
| G1 Plant consistency | NEEDS REVISION | Closed nine-state model; units, signs, reaction forces, equilibria, straight/turning symmetry, wheel lock, zero input | [Root G1 audit](../docs/reviews/G1_PHYSICAL_MODEL_AUDIT_v2.md): conditional sign/energy identities, counterexamples and 12 findings; physical blockers and proposed MASTER edits await independent review |
| G2 Certified enclosure | UNVERIFIED | Constructed computable tube covering every admitted trajectory under the same held voltage for the full interval | Strategy in §§20–25 only; no enclosure proof |
| G3 Recursive safe subset | UNVERIFIED | Useful nonempty K_T with safe hold and robust endpoint return; observations and action selection specified | Definitions/target in §§15,24 only |
| G4 Novelty | UNVERIFIED | Source-backed model/uncertainty/safety-object/theorem/computation comparison | Preliminary register; closest full texts and contact/friction/tube coverage incomplete |

## G1 questions requiring explicit resolution

The 2026-09-28 root audit is review evidence, not acceptance. Affected branches explicitly stopped include approximate lateral-grip certification, unspecified COM offset, physical turning/contact validity, generic braking authority, sustained wheel lock, estimated-state safety, and an unconditional robust straight-line reduction under independent side uncertainty. MASTER v2 is unchanged; none of the proposed repairs is adopted.

- [ ] Equations impose zero lateral velocity, while A5 says approximately zero. Choose exact idealized constraint or quantified residual; do not treat approximation as exact certification.
- [ ] A2 says COM is “sufficiently close” to axle midpoint. Specify exact geometry for the theorem or bound omitted coupling.
- [ ] Justify lateral reaction during turning and the operating domain where lateral grip and longitudinal traction coexist; independent longitudinal force bounds do not validate combined friction capacity.
- [ ] Specify direct-drive or wheel-equivalent K_t, K_e, J_w with consistent gearing, reflected inertia, units and energy balance.
- [ ] Define positive parameter bounds, voltage-driver/braking assumptions and the time regularity of traction/normal loads. Do not infer monotonicity or differentiability from phi's Lipschitz/sign conditions.
- [ ] Distinguish passing through omega=0 from sustained wheel lock. Holding a wheel at zero needs torque balance or an explicit brake constraint; the ODE alone does not supply one.
- [ ] Specify exact state knowledge or bounded estimation errors. “Measurements or estimates” without bounds leaves the theorem's information pattern unresolved.
- [ ] Check all required equilibria/symmetry/zero-input cases for the nine-state model. No physical numerical parameter set has been identified yet.

These are reviewer questions from reading v2, not silently adopted changes to its equations. Stop dependent claims until resolved and logged.

## G2/G3 proof checks

- [ ] Establish well-posedness and operating-domain bounds without assuming the safety conclusion.
- [ ] Preserve wheel/body/contact coupling in subsystem enclosures, or prove that any decoupled bounds are sound and assess conservatism.
- [ ] Certify every time in a hold, not only integration points.
- [ ] Use one voltage for all hidden uncertainties and preserve fixed-parameter dependence across time.
- [ ] Construct a useful K_T; assuming persistent feasible inputs does not solve the feasibility problem.
- [ ] Prove sample-invariance of K_T and continuous safety in S separately. Do not claim exact viability or unavoidable collision from sufficient-certificate failure.

## G4 evidence checks

- [ ] Compare closest full-text results: bounded-input feasibility, Lin, Xiong, ZOCBF, SACBF, nonuniform-relative-degree safety and relevant reachability/tube methods.
- [ ] Add primary-source contact-aware/friction-limited ground-robot and tube-control works; these categories are currently open.
- [ ] Record exact equation/theorem locators and inspected scope. Unknown is not No; a DOI/title is not a theorem audit.
- [ ] Identify a mathematical/computational result beyond substituting the nine-state plant into an existing generic method.

## Implementation wording

The user's current instruction is **no implementation before G1–G4 pass**. MASTER §32 also says implementation should remain “exploratory only.” Do not interpret that phrase as authorization to bypass the user's stricter gate. Context management and theoretical review may proceed; controller/simulator/experiment implementation remains HOLD. MASTER was imported verbatim rather than silently editing this ambiguity.

## Review response and GO

Use MASTER §33: **Finding → Evidence → Consequence → Status (VALID / NEEDS REVISION / BLOCKER / UNVERIFIED) → Required action.** Stop the affected branch on contradiction, blocker or overlap; unaffected documentation work may continue.

Record `GO — implementation freeze v2` only after G1–G4 each have explicit evidence and reviewed acceptance, updated in MASTER and DECISION_LOG. A plan, numerical success or model agreement cannot replace proof or novelty verification.
