> HISTORICAL / SUPERSEDED BY MASTER v2 (2026-09-28). Read [MASTER_RESEARCH_CONTEXT_v2.md](../research_context/MASTER_RESEARCH_CONTEXT_v2.md), DECISION_LOG, LITERATURE_MATRIX and REVIEW_GATE first. This note records earlier analysis, not the current nine-state plant or an implementation authorization. Seven-state results must not be transferred to the current plant without a new derivation.

# Luna max — gated research and execution super task

## Status and role

Requested executor: **gpt-6-luna, reasoning max**. Root and the user's GPT conversation review research claims and results. User authorization covers independent project setup, research audit, and this delegation. It does not waive the handoff requirement to accept deliverables 1–5 before implementation.

On 2026-09-28, the Luna agent stopped with an explicit **usage-limit error**. It delivered README, scope, plant alternatives, and the conditional derivative audit. It did not deliver the promised literature matrix, theorem architecture, or this supertask. Root completed the preliminary review/bibliographic register and task contract. Do not attribute those files to completed Luna work.

Resume from these files, not from a new controller design. No controller/simulation code exists. No tests or experiments have run.

## Boundary

Work only in `D:/Research/Teacher_Vien/projects/ddwmr-actuator-safety`. Read `AGENTS.md`, `docs/WORKSPACE_AUDIT.md`, `docs/RESEARCH_DECISION.md`, and `docs/reviews/ACCEPTANCE_LEDGER.md`. Do not edit sibling projects, templates, workspace README, global software settings or MATLAB paths. Do not reuse their unpublished results.

## Phase 1: close the research formulation

1. **Novelty audit.** Upgrade the 24-entry preliminary register into a source-verified 20–30-paper comparison. Unknown is not No. Obtain lawful full-text/author versions of the closest threats, record exact equations/theorems, and compare assumption-by-assumption. Include Lin, Xiong, Xiao feasibility, ZOCBF, SACBF, Brunke, and relevant DDWMR safety. Additional leads are not verified publications just because GPT or the handoff names them.
2. **Plant.** Select one physically defensible plant and operating regime. Resolve rolling effectiveness versus chassis skid, COM/axle reference, coupled inertia, gearbox conventions, available braking, current observation, and parameter sources. Keep voltage as input. Do not call an imposed algebraic transmission factor a general tire/traction model.
3. **Derivatives.** Verify every Lie derivative for that chosen plant. The present degree-three calculation is conditional on constant transmission parameters and constant mechanical uncertainties/load terms. Report singular domains; never patch an input coefficient with an epsilon to manufacture a proof.
4. **Theorem architecture.** Establish a sound continuous-hold enclosure or barrier margin. For indefinite safety, construct a useful nonempty sampled-state set with safe holds and robust endpoint return. An assumed invariant set or assumed persistent feasibility is not the requested constructive contribution.
5. **Feasibility/authority.** Distinguish certificate infeasibility from unavoidable collision. Investigate the symmetric straight-motion probe as a restricted sufficient maneuver. Preserve initial current, voltage, inertia and inductance effects. Do not extrapolate braking failure to impossibility of turning avoidance.

Deliver reviewed mathematical files, an assumption ledger, equation identifiers, proof obligations, source evidence, and a concrete GO/HOLD recommendation. A reviewer disagreement is resolved with derivation/source evidence, not majority agreement between models.

## Gate F: formulation acceptance

Required: written reviewed formulation defining plant, disturbance class, observations, safe initial set, singularity treatment, proof scope and novelty. Follow the user's handoff: only after deliverables 1–5 are accepted may deliverable 6 be produced. Current gate: **HOLD**. The reachable-tube alternative is a candidate, not an approved replacement for HOCBF.

## Phase 2: implementation specification, after Gate F

Produce the module/function/test specification only now. Trace each module and numerical approximation to equation identifiers and bounds in the accepted formulation. Include one configuration/seed system, units, solver tolerances, controller hold timing, simulation integration timing, estimation assumptions, infeasibility behavior and result provenance. Review that specification before using it to create the implementation.

## Phase 3: Luna implementation, after specification acceptance

Luna owns the plant, nominal tracker, safety filter, uncertainty generator, optimizer, simulation, metrics and experiment code. Preserve the accepted equations. Every discrepancy requiring a mathematical change returns to the reviewers before implementation is modified around it.

Use the handoff's independent `src/`, `experiments/`, `tests/`, `results/` and `paper/` organization when implementation begins. Choose MATLAB/tooling from the accepted specification and available environment; no global setup changes. Check units, actuator/input bounds, derivative consistency, hold semantics and numerical convergence. Never treat an integration time step as the sampling period.

## Phase 4: evidence and review

Baselines: B0 tracker; B1 actuator-unaware kinematic filter; B2 closest faithful sampled-data method applied to the same actuator plant where its assumptions allow; B3 accepted proposed method; B4 optional continuous-time actuator-aware comparison. State every adaptation and provide comparable information, limits and tuning budgets.

Preserve all 13 validation categories from the handoff: nominal tracking, one obstacle, multiple obstacles, near-boundary states, voltage saturation, deterministic slip, time-varying/random slip, parameter mismatch, sampling sweep, combined adverse case, Monte Carlo, theorem-bound checks and ablation. Scenarios outside theorem assumptions must be labelled stress tests, not formal validation of a guarantee.

Report position/heading RMSE, continuous-trajectory minimum barrier and clearance with numerical error treatment, collision/violation counts, peak/RMS voltage, saturation rate, mean/max solve time, QP infeasibility count, empirical safe fraction, prediction mismatch and certified-versus-observed boundary differences. Seeds and raw failures are retained. A fine numerical grid is not a proof of inter-sample safety.

The false-certification experiment must compare the simplified prediction and actual actuator plant under a disclosed command-realization map. Baseline failure under violated assumptions is not a refutation of the baseline's theorem. Measure task progress and conservatism so stopping indefinitely cannot count as an unqualified improvement.

## Phase 5: manuscript readiness

Root/GPT review the model, proofs, literature differentiation, experiment fairness and reproducibility artifacts. Q1 ambition and handoff quality scores are review targets, not generated evidence. Do not publish, submit, invent hardware validation, or declare the study complete without the corresponding actual work.

## Stop conditions

Report and return to research review for: unresolved singularities, hidden slip smoothness, unrealistic load/traction bounds, unavailable controller quantities, nontrivial infeasibility inside a claimed certified set, uselessly conservative sampling limits, an unproved endpoint-return condition, or contribution reduced to an existing theorem with a substituted plant. Do not continue to controller code merely because a simulation can be made to run.
