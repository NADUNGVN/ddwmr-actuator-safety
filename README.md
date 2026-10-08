# DDWMR actuator- and contact-aware safety research

Independent research repository for Thầy Viễn. **HOLD - G1 PASS for restricted reduced-model scope; G2/G3/G4 UNVERIFIED.**

**Current research question (2026-10-08): [Independent G3 feasibility and prior-art assignment](docs/G3_FEASIBILITY_RESEARCH_ASSIGNMENT.md).** Determine whether a useful recursive safe set and an observable voltage policy offer a defensible next contribution. The required output is a self-contained Markdown report. This stage evaluates the direction before G3 implementation.

**Latest completed work: [W2 final scientific disposition](docs/reviews/autonomous_w2/CODEX_W2_FINAL_DISPOSITION_2026_10_08.md).** The finite synthetic development record is accepted; the contribution verdict is `NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE`. G2/G3/G4 remain UNVERIFIED. The W2 [G2 audit](docs/reviews/autonomous_w2/g2/LUNA_TO_CODEX_G2_W2_V6_FINAL_FROZEN_RESULT_AUDIT_FULL_HANDOFF_v1.md) and [G4 resource attribution](docs/reviews/autonomous_w2/g4/LUNA_TO_CODEX_G4_W2_V6_FINAL_RESOURCE_ATTRIBUTION_FULL_HANDOFF_v1.md) contain the evidence and limitations.

[Publication index and scope](docs/RESEARCH_PUBLICATION_2026_10_08.md) identify the source, result and provenance files included for independent review. The public snapshot does not promote a gate.

[Cập nhật tiến độ ngày 2026-09-29](docs/PROGRESS_SUMMARY_2026-09-29.md): Cases A/B accepted; Case C accepted by GPT in narrow synthetic scope, with practical usefulness still unverified. This summary does not change MASTER or the research gates.

## Start every session here

Read these before reasoning, derivation or code:

1. [MASTER_RESEARCH_CONTEXT_v2.md](research_context/MASTER_RESEARCH_CONTEXT_v2.md) — authoritative declared v2.1; canonical filename retained for stable links. Original v2 import is preserved in history.
2. [DECISION_LOG.md](research_context/DECISION_LOG.md) — decisions and superseded assumptions.
3. [LITERATURE_MATRIX.md](research_context/LITERATURE_MATRIX.md) — source evidence and unresolved overlaps.
4. [REVIEW_GATE.md](research_context/REVIEW_GATE.md) — G1–G4 status and evidence required.

Adopted formulation v2.1: nine-state reduced ideal planar DDWMR, motor-voltage inputs, execution-fixed hidden model parameters and effective tangential capacities C_j, exact lateral constraint with algebraic reactions, exact sampled state and ideal four-quadrant voltage ZOH. Joint state/parameter tubes and predecessor reasoning remain under investigation. HOCBF is optional/baseline. Formulation adoption does not pass G1, validate a physical platform or authorize implementation.

## Session instruction

> Read `AGENTS.md` and all four `research_context/` files before reasoning. Treat MASTER as authoritative. For the new independent research stage follow `docs/G3_FEASIBILITY_RESEARCH_ASSIGNMENT.md`. W2 governs the completed G2/G4 verification packages; W1 is historical. Report contradictions, blockers or overlap explicitly; do not repair assumptions silently.

## GPT review handoff

The current external research entry point is [G3_FEASIBILITY_RESEARCH_ASSIGNMENT.md](docs/G3_FEASIBILITY_RESEARCH_ASSIGNMENT.md). Report the exact reviewed Git commit and return `docs/reviews/G3_FEASIBILITY_PRIOR_ART_RESEARCH_FULL_HANDOFF.md` as an actual Markdown file. [GPT_REVIEW_REQUEST.md](docs/GPT_REVIEW_REQUEST.md) is the historical formulation-review route. The GitHub repository is public, verified again on 2026-10-08. Publishing this repository does not change the research HOLD.

The [GPT R2 review](docs/reviews/GPT_TO_CODEX_REVIEW_12edd1b_R2_FULL_HANDOFF.md) and [finalization response](docs/reviews/CODEX_FINALIZATION_RESPONSE_12edd1b.md) record the reviewed formulation. The [R2 proposal](docs/proposals/v2_1/README.md) and [finalization package](docs/proposals/v2_1_finalization/README.md) are archived review artifacts, not alternate authoritative masters. Adoption provenance belongs in DECISION_LOG and the dated adoption commit.

G1 PASS - restricted reduced-model scope, per [independent G1 review](docs/reviews/GPT_TO_CODEX_G1_REVIEW_8341014e_PASS.md). Physical-platform correspondence UNVERIFIED; G2/G3/G4 UNVERIFIED. The W2 validation work is governed by its recorded scope; the independent research assignment does not open G3 implementation.

## Current G2 research package

**Completed execution workflow:** [Autonomous G2/G4 verification W2](docs/DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2.md), followed by the [final disposition](docs/reviews/autonomous_w2/CODEX_W2_FINAL_DISPOSITION_2026_10_08.md). The earlier [Luna validation assignment](docs/LUNA_VALIDATION_HANDOFF_v1.md), [WP1 GPT request](docs/GPT_WP1_CONSOLIDATED_REVIEW_REQUEST.md) and [consolidated review](docs/reviews/GPT_TO_CODEX_DDWMR_CONSOLIDATED_REVIEW_FULL_HANDOFF.md) remain historical context. Read dated final dispositions before older candidate claims.

- [Analytic enclosure candidate](research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md): proof draft, full-hold collision/contact checks and finite-evaluation obligations.
- [Prior-art overlap and blockers](docs/reviews/G2_PRIOR_ART_AND_BLOCKERS_v1.md).
- [GPT review of v1](docs/reviews/GPT_TO_CODEX_G2_REVIEW_7390942f_FULL_HANDOFF.md): analytic equations accepted with a wording correction; G2 remains UNVERIFIED.
- [Finite rational Case A](research/theorem_notes/G2_FINITE_CERTIFICATE_CASE_A_v1.md): accepted by GPT at `d2cd854` for the exact synthetic hand case; [acceptance record](docs/reviews/GPT_G2_R2_d2cd854_ACCEPT_RECORD.md). No general solver or practical validation.
- [R2 response](docs/reviews/CODEX_RESPONSE_TO_G2_REVIEW_7390942f_R2.md) and [additional prior art](docs/reviews/G2_PRIOR_ART_SUPPLEMENT_R2.md).
- [Case B](research/theorem_notes/G2_CHALLENGE_CASE_B_v1.md): uncertain actuator blocks, saturation exit and strictly limited comparison of three sufficient evaluations, accepted at `1da2166`; [review record](docs/reviews/GPT_G2_R3_1da2166_ACCEPT_RECORD.md).
- [Case C voltage-selection challenge](research/theorem_notes/G2_VOLTAGE_SELECTION_CASE_C_v1.md): same state/family and shared error envelope for two forward voltage levels plus zero; accepted by GPT at `c9ff32d` as a synthetic certificate-output example only; practical usefulness remains UNVERIFIED.
- Earlier GPT requests [R4](docs/GPT_G2_REVIEW_REQUEST_R4.md), [R3](docs/GPT_G2_REVIEW_REQUEST_R3.md), [R2](docs/GPT_G2_REVIEW_REQUEST_R2.md) and [v1](docs/GPT_G2_REVIEW_REQUEST_v1.md) remain historical.

G2 is UNVERIFIED. These are research artifacts, not an accepted theorem, implementation freeze or new authoritative formulation.

## Supporting history

Earlier `docs/` and `research/` notes retain the initial seven-state audit and alternative model discussions. Their historical labels prevent them from overriding MASTER. Derive the nine-state results afresh.

[Workspace audit](docs/WORKSPACE_AUDIT.md) records the isolation boundary. The [earlier Luna supertask](docs/LUNA_SUPER_TASK.md) is historical and must be aligned to adopted v2.1 and the research gates before execution. Luna previously stopped at a usage limit; no controller, simulator or experimental results were produced.

## Collaboration and isolation

The user starts the research sessions. Under W2 the two Luna owners coordinate through repository files and publish consolidated handoffs; Codex reviews the evidence. The new independent reviewer produces the assigned research report. All writes remain inside this project; sibling studies, templates, shared workspace files and global settings are outside the write boundary.
