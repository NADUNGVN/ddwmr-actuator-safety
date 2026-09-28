# Proposed G1 status synchronization

Prepared 2026-09-29. **NOT APPLIED.** Canonical formulation remains v2.1 with its previously recorded gate metadata until this status update is accepted and applied.

## Finding

The [independent GPT G1 review](../../reviews/GPT_TO_CODEX_G1_REVIEW_8341014e_PASS.md) reports **G1 PASS - restricted reduced-model scope** for authoritative commit `8341014eac52ea66fe38559d6e1baee92e8f9b96`. Physical-platform correspondence remains UNVERIFIED. Overall HOLD; G2/G3/G4 UNVERIFIED; implementation unauthorized.

## Evidence

The incoming review records twelve VALID checks and an explicit restricted G1 disposition in section 14. Sections 15 and 18 condition canonical status recording on user acceptance. The archived incoming file matches the supplied source, SHA-256 `d428301b9ba0a8118484ca7d13bf992b85794aade7e6a66d5392583f98266b49`.

## Consequence

The [exact pending metadata diff](G1_STATUS_PENDING.patch) synchronizes five canonical files. It preserves the existing formulation version, plant equations, assumptions, physical limitations and all G2/G3/G4 statuses. LITERATURE_MATRIX is unchanged because no literature evidence or formulation changes.

The seven completed G1 checklist items refer to the restricted consistency review. The outstanding quantitative parameter/function provenance item remains unchecked and is explicitly separated from formal consistency acceptance. Historical decision-log entries retain their original statuses.

## Status

VALID as a prepared status proposal. **User acceptance/application is pending.** This package does not independently create a canonical G1 pass or authorize the next research phase.

The patch passes `git apply --check`; all 43 displayed MASTER equation blocks are preserved. The six baseline hashes include the unchanged literature matrix. These are document checks, not simulation or implementation tests.

## Exact targets

| Canonical file | Proposed target |
|---|---|
| `research_context/MASTER_RESEARCH_CONTEXT_v2.md` | [MASTER target](MASTER_RESEARCH_CONTEXT_v2_TARGET.md) |
| `research_context/REVIEW_GATE.md` | [Gate target](REVIEW_GATE_TARGET.md) |
| `research_context/DECISION_LOG.md` | [Log target](DECISION_LOG_TARGET.md) |
| `AGENTS.md` | [Agent contract target](AGENTS_TARGET.md) |
| `README.md` | [Repository entry target](README_TARGET.md) |

Target files contain future canonical wording to make the proposed patch reviewable. They have no authority from their placement here; their relative links refer to the intended canonical location.

## Required action

Accept or revise this restricted G1 disposition and the metadata patch. The user may relay this exact package for independent text review if desired. Before application, recheck [baseline hashes](BASELINE_SHA256.json), apply only this status diff, and add one actual dated provenance record under the new G1 decision entry identifying the authorizing user message and reviewed evidence. No acceptance date is invented in this proposal. Verify the resulting text matches the targets plus that event record; retain HOLD.

No substantive formulation edit is proposed, so declared formulation version remains v2.1. A subsequent G2/G3 research phase requires explicit user authorization; acceptance of G1 status does not provide it. Controller/simulator/experiment implementation remains prohibited until all required gates and reviewed GO.
