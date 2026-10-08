# Project operating contract

## Mandatory context read
- Every session, before research reasoning, derivation or code, read all four files in `research_context/`: `MASTER_RESEARCH_CONTEXT_v2.md`, `DECISION_LOG.md`, `LITERATURE_MATRIX.md`, `REVIEW_GATE.md`.
- MASTER is authoritative current research state; user instructions take precedence. Previous chat, handoff v1, and `docs/`/`research/` notes are historical where they conflict with MASTER.
- Adopted formulation v2.1: nine states `[p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R]`; u is body speed and V is voltage. Reduced ideal constrained-contact model with execution-fixed hidden model parameters, effective capacities C_j, exact sampled state and ideal four-quadrant fixed-period voltage ZOH. HOCBF is optional/baseline. Physical tire/support correspondence is unverified. Do not transfer the historical seven-state derivative audit to this plant.
- G1 PASS - restricted reduced-model scope, through the separate independent review of authoritative v2.1. Physical-platform correspondence and G2/G3/G4 remain UNVERIFIED. G2 analytic work and scoped validation code for G2/G4 are authorized under MASTER sections 3/32 and `docs/LUNA_VALIDATION_HANDOFF_v1.md`. Overall HOLD is a research disposition, not a blanket prohibition of authorized validation work.
- Current workflow W2 (2026-10-07): the owner authorized the two existing Luna max sessions to own G2/G4 verification autonomously without routine Codex review/GO waits. Follow `docs/DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2.md` and the session's W2 assignment. It supersedes per-iteration Codex permission requirements within the same scope; mathematical soundness, immutable evidence and final independent gate review remain required.
- The user explicitly superseded the blanket pre-gate code prohibition on 2026-09-29. Luna may implement validation arithmetic, one-hold enclosure evaluation, certificate checking, baseline adapters and reproducible offline benchmark tooling under the current handoff. Operational controller/safety-filter integration, G3 construction, closed-loop or hardware experiments are not part of this assignment. Do not require another policy approval for the authorized scope. Draft specifications still require a soundness audit; authorization is not proof acceptance.
- On contradiction, blocker or literature overlap, stop the affected branch and report it explicitly; never repair assumptions silently.
- Substantive formulation changes belong in MASTER with a version increment and dated DECISION_LOG entry; update matrix/gates as needed. Mark old claims as superseded.
- The user starts the existing Luna sessions and relays final reports to Codex/GPT. Under W2 the two Luna sessions coordinate directly through owned files/releases in the shared repository; the user need not relay routine corrections. Do not use browser/computer automation or tool messages to other people. Codex prepares assignments and reviews consolidated evidence; do not spawn, resume or message execution subagents to bypass the user's launch.

## Isolation
- Work only within `D:/Research/Teacher_Vien/projects/ddwmr-actuator-safety`.
- This is a new independent Git repository. Do not edit the workspace README, templates, sibling projects, their Git indexes, global software settings, or MATLAB search paths.
- Existing sibling changes belong to their owners. Do not clean, restore, commit, or copy their unpublished research.

## Research gates
- The governing research gates are G1–G4 in MASTER v2.1 (canonical filename retained). The old deliverables 1–5 are historical organization, not a competing acceptance rule.
- Preserve motor voltage as the physical input. Explicitly distinguish amplitude-bounded slip, differentiable slip, parameter uncertainty, and ground-contact mechanics.
- Never equate instantaneous QP feasibility with recursive feasibility, viability, or physical impossibility of avoidance.
- Report relative-degree singularities and hidden assumptions; do not silently exclude them.
- Treat citations in the user handoff as leads until independently verified. Unknown is not No. Absence of evidence is not a novelty claim.
- Use primary sources for literature claims. Record full-text access status, equation/theorem location, and uncertainty.
- No claim of first, Q1 readiness, successful tests, or proven theorem without evidence.

## Roles
- Root agent and the user's GPT research conversation act as critical research reviewers.
- User requests **Luna max** for `DDWMR | LUNA-G2-SCOPE` and `DDWMR | LUNA-G4-AUER`. Current assignments: `docs/CODEX_TO_LUNA_G2_AUTONOMOUS_COMPLETION_W2.md` and `docs/CODEX_TO_LUNA_G4_AUTONOMOUS_COMPLETION_W2.md`. W1 handoff is historical implementation context; W2 governs autonomy, ownership and bounded validation execution.
- No autonomous agent delegation. The user starts Luna; Codex does not run the implementation in its place.
- Independent verification of outputs remains necessary. Model agreement is not evidence.

## Outputs
- Research documents may be written in English; decision summaries should be in Vietnamese.
- Each mathematical claim must state assumptions and whether it is derived, conjectured, or externally established.
- Keep future implementation and results directories free of fabricated outputs.
- Luna chat handoffs contain exactly three short lines: `Session`, `Status`, `Handoff`. Detailed evidence belongs in the required Markdown report. A prepared preflight alone does not complete a W2 verification package.
