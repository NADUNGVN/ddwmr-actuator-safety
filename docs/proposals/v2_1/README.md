# Pending MASTER v2.1 review package — R2

**NOT ADOPTED. Overall HOLD.** Current authority remains `research_context/MASTER_RESEARCH_CONTEXT_v2.md` declaring v2. No authoritative context file was edited to produce this package.

Proposal revision R2 was prepared on 2026-09-29 after GPT reviewed commit `094f3c8`. The R1 proposal at that commit used fixed normal loads and default oddness; those proposed choices are superseded here, and were never adopted. Version v2.1 is still only a candidate, not a second source of truth.

## Read in this order

1. The four current authoritative context files, as required by AGENTS.md.
2. [Latest user-supplied GPT review of 094f3c8](../../reviews/GPT_TO_CODEX_REVIEW_094f3c8_FULL_HANDOFF.md), archived verbatim.
3. [Codex R2 response](../../reviews/CODEX_RESPONSE_TO_REVIEW_094f3c8_R2.md), including equation-level decisions and the file/section disposition table. The [earlier handoff](../../reviews/GPT_TO_CODEX_G1_REVIEW_HANDOFF_v2_1.md) and [earlier response](../../reviews/CODEX_RESPONSE_TO_GPT_G1_v2_1.md) remain historical evidence.
4. [Complete MASTER preview](MASTER_v2_1_PREVIEW.md), a non-authoritative candidate.
5. [Exact pending unified diff](MASTER_v2_1_PENDING.patch), including MASTER, DECISION_LOG, REVIEW_GATE and limited matrix screening updates.

[REPLACEMENTS.md](REPLACEMENTS.md) contains the exact MASTER replacement blocks and pending DECISION_LOG, REVIEW_GATE and matrix text. [BASELINE_SHA256.json](BASELINE_SHA256.json) records byte hashes of the four unchanged authoritative files. Base commit: `5424c2b86837b95eece87726da7c2d7fdea0a7e2`. Pending proposal publications do not change this baseline.

## Changes requiring explicit review

- Option 1: exact ideal lateral constraint with algebraic reaction budgets; no added physical state.
- Parameter slices `D_c(vartheta)` and joint state/parameter sets, rather than intersecting incompatible spaces or projecting onto a favorable parameter.
- Effective per-wheel tangential capacities C_j in newtons in the longitudinal equality and combined force budget. Literal mu_j/N_j are removed from the formal core; their old interpretation is retained only as historical motivation/physical-mapping limitations.
- One known fixed strictly sign-preserving bounded Lipschitz traction shape. Neither oddness nor monotonicity is required in the core; oddness is optional for particular auxiliary symmetry results.
- Fixed unknown parameters for the entire execution, a narrowing from time-varying traction uncertainty.
- Power-consistent wheel-side motors, exact sampled state, zero delay, and an ideal four-quadrant terminal-voltage source.
- Qualified wheel-zero and symmetry statements; no unsupported braking backup.
- Reduced-model question, title and novelty hypothesis. Capacity reparameterization does not solve real tire/support/load physics or establish trajectory correspondence; a lower capacity bound is not automatically a conservative dynamics model.

No new tube, recursive-set theorem, controller, simulator or experiment is included. The proposed definitions specify what future proofs would have to establish.

## Acceptance procedure

Do not apply the patch automatically. The latest handoff explicitly requires the actual revised proposal to be reviewed before modifying authoritative MASTER. This requirement is from `GPT_TO_CODEX_REVIEW_094f3c8_FULL_HANDOFF.md`, §§23 and 27, continuing the earlier pending-review instruction; it is not an external permission policy.

Ask the reviewer to accept/modify/reject the actual R2 text and exact patch, especially the C_j force-scale/envelope interpretation, its physical limitations and the restricted scientific claim. Once explicit adoption is relayed, re-check the baseline, apply only the accepted edits, complete the actual dated decision record and update AGENTS/README version references together. An adopted v2.1 would still be HOLD; it is not G1 acceptance or implementation authorization.

The pending diff can be syntax/context-checked with `git apply --check` without applying it. The reviewed preview is a working proposal, not a second source of truth. Any baseline change requires refreshing the diff and hash manifest before adoption.

## Copyable next message to GPT

```text
Read the latest published main commit, the current four context files,
docs/reviews/CODEX_RESPONSE_TO_REVIEW_094f3c8_R2.md, and
docs/proposals/v2_1/MASTER_v2_1_PREVIEW.md plus its pending patch.

MASTER v2 remains authoritative. All v2.1 R2 changes are pending.

Review the actual revised text at equation level:
1. C_j in both the force equality and tangential force envelope;
2. removal of literal mu_j/N_j from the formal parameter vector;
3. no core oddness/monotonicity and qualified auxiliary symmetry;
4. joint state/parameter domains and common-voltage quantifiers;
5. execution-fixed uncertainty and narrowed research claim;
6. model-family inclusion obligations before physical transfer.

For each: Finding / Evidence / Consequence / Status / Required action.
Explicitly accept, modify or reject the proposed text. Identify remaining
physical scope obligations. Do not conclude GO, implement, or treat model
agreement as proof. Return any corrections through the user.
```
