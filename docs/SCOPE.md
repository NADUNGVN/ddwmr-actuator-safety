> HISTORICAL / SUPERSEDED BY MASTER v2 (2026-09-28). Read [MASTER_RESEARCH_CONTEXT_v2.md](../research_context/MASTER_RESEARCH_CONTEXT_v2.md), DECISION_LOG, LITERATURE_MATRIX and REVIEW_GATE first. This note records earlier analysis, not the current nine-state plant or an implementation authorization. Seven-state results must not be transferred to the current plant without a new derivation. The earlier promise of a 27-paper matrix was not delivered by Luna; the current register has 24 evidence-tiered entries.

# Research scope and Phase 1 decision

**Project:** Thầy Viễn — actuator-level inter-sample collision safety for differential-drive mobile robots (DDWMRs)  
**Research cutoff:** 2026-09-28  
**Status:** preliminary research audit; formulation freeze **HOLD**; implementation not authorized.

## Intended research question

For a differential-drive robot actuated by motor voltage and sampled under zero-order hold, determine when collision avoidance is physically achievable in the presence of finite voltage authority and wheel-ground uncertainty. The object of interest is the full continuous trajectory, not only the controller's sampled states.

The proposed intersection remains worth investigating:

> voltage-level electromechanical DDWMR dynamics + bounded actuation + wheel-ground uncertainty + digital sample-and-hold + continuous-time collision safety + a useful actuator-feasibility or viability characterization.

This is a screening target, not a verified novelty claim. Strong nearby results already exist for robust sampled-data HOCBFs, sample-aware unicycle safety, segment-safe MPC, CBF-QP obstacle avoidance on DDWMRs, and DDWMR actuator lag/saturation. Equation-level comparison with the closest paywalled or otherwise unavailable papers remains open.

## Included in this phase

1. Evidence-tiered screening of 27 close or foundational works, with primary links, plant/input details, implementation dimensions, access status, and available equation/theorem locators.
2. Conditional electromechanical plant candidates, separating an ideal no-slip constrained mechanics model from a phenomenological frozen-slip kinematic extension and from contact-force mechanics.
3. An exact relative-degree derivation for the conditional frozen-slip seven-state model, including singular configurations.
4. Candidate theorem definitions that distinguish instantaneous QP feasibility, one-hold safety, recursive sample invariance, and robust viability.
5. A gated execution brief for later work. Deliverable 6, the implementation specification, is deliberately deferred until deliverables 1–5 are reviewed and accepted.

## Excluded until the gate is passed

- Controller implementation, simulator design, experiment plans that imply an accepted model, test code, MATLAB optimization, and results generation.
- Any novelty claim that no prior work covers the full intersection, any “first” claim, and any Q1-readiness score.
- Dynamic obstacles as theory, multi-robot coordination, learning-based control, and algorithm additions unrelated to the central physical-realizability question.

## Phase 1 decision

The current formulation is **not frozen** for five concrete reasons:

1. **Physical slip closure is undecided.** A scalar wheel-speed transmission factor is not a general tire-slip/skid model. A contact-force model adds body-velocity states and changes the plant and relative-degree calculation.
2. **The all-collision-free-state claim is too broad.** With actuator states, position-only set `h>=0` includes states already moving inward at the boundary; bounded voltage cannot undo a negative initial `hdot` instantaneously. A theorem needs a proper augmented initial set or backup/viability certificate.
3. **The relative degree is local, not global.** In the seven-state reduced model the voltage coefficient vanishes for obstacle-tangent configurations (`rho=0`), among other possible model-specific degeneracies.
4. **A slip amplitude bound is inadequate for differentiated HOCBF/sample-margin calculations.** Time-varying slip needs regularity bounds; measurable bounded slip instead calls for a nonsmooth/reachable-tube treatment.
5. **Instantaneous feasibility is not recursive feasibility or physical impossibility.** A robust common-input QP at the present sample does not prove safety over the hold or existence of a safe policy for all future time.

The research reviewers' independent mathematical notes are in `docs/reviews/ROOT_MATH_REVIEW.md` and `docs/reviews/PHYSICAL_AUTHORITY_PROBE.md`. They are complementary evidence, not theorem proofs.

## Provisional working title

**Actuator-Level Inter-Sample Safety Control of Differential-Drive Mobile Robots under Voltage Saturation and Wheel-Slip Uncertainty**

The title may remain as a working label. “Robust Sampled-Data HOCBF” and “Input-Feasibility Guarantees” remain uncommitted subtitle claims until the gap and proof are established. The term “wheel slip” must be narrowed to a stated model class or replaced by physically closed tire/contact uncertainty.

## Acceptance gate

Root/GPT reviewers must review the novelty audit, plant specification, derivative audit, and candidate theorem architecture. The gate passes only after the reviewers choose the plant/contact closure, observation pattern, disturbance class, treatment of relative-degree singularities, and the safety object to prove. Only after written acceptance may Luna prepare the deliverable-6 implementation specification.
