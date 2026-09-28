# DDWMR actuator- and contact-aware safety research

Independent research repository for Thầy Viễn. **HOLD — G1–G4 have not passed.**

## Start every session here

Read these before reasoning, derivation or code:

1. [MASTER_RESEARCH_CONTEXT_v2.md](research_context/MASTER_RESEARCH_CONTEXT_v2.md) — authoritative current formulation, imported verbatim from the user-supplied file.
2. [DECISION_LOG.md](research_context/DECISION_LOG.md) — decisions and superseded assumptions.
3. [LITERATURE_MATRIX.md](research_context/LITERATURE_MATRIX.md) — source evidence and unresolved overlaps.
4. [REVIEW_GATE.md](research_context/REVIEW_GATE.md) — G1–G4 status and evidence required.

Current candidate: nine states (pose, body longitudinal velocity/yaw rate, wheel speeds, motor currents), motor-voltage inputs, uncertain longitudinal traction, fixed-period ZOH, and structured reachable tubes/predecessor. HOCBF is optional/baseline. The plant and method are not frozen.

## Session instruction

> Read `research_context/MASTER_RESEARCH_CONTEXT_v2.md`, `DECISION_LOG.md`, `LITERATURE_MATRIX.md`, and `REVIEW_GATE.md` before reasoning. Treat MASTER as authoritative current state. Do not implement before G1–G4 pass. If you find a contradiction, blocker, or literature overlap, stop the affected branch and report it explicitly rather than repairing assumptions silently.

## GPT review handoff

Use [GPT_REVIEW_REQUEST.md](docs/GPT_REVIEW_REQUEST.md) to review the current context, then G1, then the remaining gates in separate exchanges. The GitHub repository is public as verified on 2026-09-28. If repository access fails, attach the four context files. Report the reviewed commit when available. Publishing this repository does not change the research HOLD.

Latest review: [G1 physical model audit of MASTER v2](docs/reviews/G1_PHYSICAL_MODEL_AUDIT_v2.md), with twelve equation-level findings and proposed edits pending independent review. MASTER has not been changed or accepted as a frozen plant.

Follow-up: [GPT handoff and pending v2.1 R2 review package](docs/proposals/v2_1/README.md), revised after GPT's review of commit `094f3c8`. R2 proposes effective tangential capacities C_j and optional auxiliary oddness, with an explicitly reduced-model claim. It includes Codex's equation-level response, a complete proposed MASTER preview and an unapplied diff. All four current context files remain unchanged; v2.1 is not adopted.

## Supporting history

Earlier `docs/` and `research/` notes retain the initial seven-state audit and alternative model discussions. Their historical labels prevent them from overriding MASTER. Derive the nine-state results afresh.

[Workspace audit](docs/WORKSPACE_AUDIT.md) records the isolation boundary. The [earlier Luna supertask](docs/LUNA_SUPER_TASK.md) is historical and must be aligned to v2 before execution. Luna previously stopped at a usage limit; no controller, simulator or experimental results were produced.

## Collaboration and isolation

The user relays messages between Codex and GPT; no browser/computer automation for that exchange. Luna max is the requested execution model after research acceptance. All writes remain inside this project; sibling studies, templates, shared workspace files and global settings are outside the write boundary.
