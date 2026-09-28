# Project operating contract

## Mandatory context read
- Every session, before research reasoning, derivation or code, read all four files in `research_context/`: `MASTER_RESEARCH_CONTEXT_v2.md`, `DECISION_LOG.md`, `LITERATURE_MATRIX.md`, `REVIEW_GATE.md`.
- MASTER is authoritative current research state; user instructions take precedence. Previous chat, handoff v1, and `docs/`/`research/` notes are historical where they conflict with MASTER.
- Adopted formulation v2.1: nine states `[p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R]`; u is body speed and V is voltage. Reduced ideal constrained-contact model with execution-fixed hidden model parameters, effective capacities C_j, exact sampled state and ideal four-quadrant fixed-period voltage ZOH. HOCBF is optional/baseline. Physical tire/support correspondence is unverified. Do not transfer the historical seven-state derivative audit to this plant.
- G1 PASS - restricted reduced-model scope, through the separate independent review of authoritative v2.1. Physical-platform correspondence remains UNVERIFIED. G2/G3 construction requires explicit user authorization of the next research phase.
- No implementation before G1–G4 pass and reviewed GO is recorded in MASTER and DECISION_LOG. Preparing context/review documents does not open the gate.
- On contradiction, blocker or literature overlap, stop the affected branch and report it explicitly; never repair assumptions silently.
- Substantive formulation changes belong in MASTER with a version increment and dated DECISION_LOG entry; update matrix/gates as needed. Mark old claims as superseded.
- The user relays messages between Codex and GPT. Do not use browser/computer automation to read or send GPT research exchanges.

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
- User explicitly requests **gpt-6-luna, reasoning max** as execution agent. Luna may draft phase-1 research artifacts now. All later implementation code is delegated to Luna after the research gate.
- No autonomous additional agent delegation beyond this requested division.
- Independent verification of outputs remains necessary. Model agreement is not evidence.

## Outputs
- Research documents may be written in English; decision summaries should be in Vietnamese.
- Each mathematical claim must state assumptions and whether it is derived, conjectured, or externally established.
- Keep future implementation and results directories free of fabricated outputs.
