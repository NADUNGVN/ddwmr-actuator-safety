# DDWMR actuator- and contact-aware safety research

Independent research repository for Thầy Viễn. **HOLD - G1 PASS for restricted reduced-model scope; G2/G3/G4 UNVERIFIED.**

## Start every session here

Read these before reasoning, derivation or code:

1. [MASTER_RESEARCH_CONTEXT_v2.md](research_context/MASTER_RESEARCH_CONTEXT_v2.md) — authoritative declared v2.1; canonical filename retained for stable links. Original v2 import is preserved in history.
2. [DECISION_LOG.md](research_context/DECISION_LOG.md) — decisions and superseded assumptions.
3. [LITERATURE_MATRIX.md](research_context/LITERATURE_MATRIX.md) — source evidence and unresolved overlaps.
4. [REVIEW_GATE.md](research_context/REVIEW_GATE.md) — G1–G4 status and evidence required.

Adopted formulation v2.1: nine-state reduced ideal planar DDWMR, motor-voltage inputs, execution-fixed hidden model parameters and effective tangential capacities C_j, exact lateral constraint with algebraic reactions, exact sampled state and ideal four-quadrant voltage ZOH. Joint state/parameter tubes and predecessor reasoning remain under investigation. HOCBF is optional/baseline. Formulation adoption does not pass G1, validate a physical platform or authorize implementation.

## Session instruction

> Read `research_context/MASTER_RESEARCH_CONTEXT_v2.md`, `DECISION_LOG.md`, `LITERATURE_MATRIX.md`, and `REVIEW_GATE.md` before reasoning. Treat MASTER as authoritative current state. Do not implement before G1–G4 pass. If you find a contradiction, blocker, or literature overlap, stop the affected branch and report it explicitly rather than repairing assumptions silently.

## GPT review handoff

Use [GPT_REVIEW_REQUEST.md](docs/GPT_REVIEW_REQUEST.md) to review the current context, then G1, then the remaining gates in separate exchanges. The GitHub repository is public as verified on 2026-09-28. If repository access fails, attach the four context files. Report the reviewed commit when available. Publishing this repository does not change the research HOLD.

The [GPT R2 review](docs/reviews/GPT_TO_CODEX_REVIEW_12edd1b_R2_FULL_HANDOFF.md) and [finalization response](docs/reviews/CODEX_FINALIZATION_RESPONSE_12edd1b.md) record the reviewed formulation. The [R2 proposal](docs/proposals/v2_1/README.md) and [finalization package](docs/proposals/v2_1_finalization/README.md) are archived review artifacts, not alternate authoritative masters. Adoption provenance belongs in DECISION_LOG and the dated adoption commit.

G1 PASS - restricted reduced-model scope, per [independent G1 review](docs/reviews/GPT_TO_CODEX_G1_REVIEW_8341014e_PASS.md). Physical-platform correspondence UNVERIFIED; G2/G3/G4 UNVERIFIED. The user authorized G2 analytic research on 2026-09-29; G3 construction remains unauthorized; no controller/simulator/experiment implementation before all gates pass and reviewed GO is recorded.

## Current G2 research package

- [Analytic enclosure candidate](research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md): proof draft, full-hold collision/contact checks and finite-evaluation obligations.
- [Prior-art overlap and blockers](docs/reviews/G2_PRIOR_ART_AND_BLOCKERS_v1.md).
- [Independent GPT review request](docs/GPT_G2_REVIEW_REQUEST_v1.md).

G2 is UNVERIFIED. These are research artifacts, not an accepted theorem, implementation freeze or new authoritative formulation.

## Supporting history

Earlier `docs/` and `research/` notes retain the initial seven-state audit and alternative model discussions. Their historical labels prevent them from overriding MASTER. Derive the nine-state results afresh.

[Workspace audit](docs/WORKSPACE_AUDIT.md) records the isolation boundary. The [earlier Luna supertask](docs/LUNA_SUPER_TASK.md) is historical and must be aligned to adopted v2.1 and the research gates before execution. Luna previously stopped at a usage limit; no controller, simulator or experimental results were produced.

## Collaboration and isolation

The user relays messages between Codex and GPT; no browser/computer automation for that exchange. Luna max is the requested execution model after research acceptance. All writes remain inside this project; sibling studies, templates, shared workspace files and global settings are outside the write boundary.
