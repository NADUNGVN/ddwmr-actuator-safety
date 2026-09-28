# Pending MASTER v2.1 review package

**NOT ADOPTED. Overall HOLD.** Current authority remains `research_context/MASTER_RESEARCH_CONTEXT_v2.md` declaring v2. No authoritative context file was edited to produce this package.

## Read in this order

1. The four current authoritative context files, as required by AGENTS.md.
2. [User-supplied GPT review](../../reviews/GPT_TO_CODEX_G1_REVIEW_HANDOFF_v2_1.md), archived verbatim.
3. [Codex response](../../reviews/CODEX_RESPONSE_TO_GPT_G1_v2_1.md), including the F01–F12 verdicts and B1–B6 corrections.
4. [Complete MASTER preview](MASTER_v2_1_PREVIEW.md), a non-authoritative candidate.
5. [Exact pending unified diff](MASTER_v2_1_PENDING.patch), including MASTER, DECISION_LOG, REVIEW_GATE and limited matrix screening updates.

[REPLACEMENTS.md](REPLACEMENTS.md) contains the exact replacement section blocks used to prepare the MASTER preview. [BASELINE_SHA256.json](BASELINE_SHA256.json) records byte hashes of the four unchanged authoritative files at preparation. Base commit: `5424c2b86837b95eece87726da7c2d7fdea0a7e2`. Pending proposal publications do not change this baseline.

## Changes requiring explicit review

- Option 1: exact ideal lateral constraint with algebraic reaction budgets; no added physical state.
- Parameter slices `D_c(vartheta)` and joint state/parameter sets, rather than intersecting incompatible spaces or projecting onto a favorable parameter.
- Known prescribed normal loads as an ideal planar assumption with a still-open physical support/load obligation.
- One known fixed strictly sign-preserving odd Lipschitz traction shape; global monotonicity is deferred unless a proof requires it.
- Fixed unknown parameters for the entire execution, a narrowing from time-varying traction uncertainty.
- Power-consistent wheel-side motors, exact sampled state, zero delay, and an ideal four-quadrant terminal-voltage source.
- Qualified wheel-zero and symmetry statements; no unsupported braking backup.

No new tube, recursive-set theorem, controller, simulator or experiment is included. The proposed definitions specify what future proofs would have to establish.

## Acceptance procedure

Do not apply the patch automatically. The handoff explicitly requires proposals to remain pending until user/reviewer acceptance. This requirement is from `GPT_TO_CODEX_G1_REVIEW_HANDOFF_v2_1.md`, §§0 and 6, not an external permission policy.

Ask the reviewer to accept/modify/reject B1–B6 and the exact patch, especially the finite-height normal-load issue and the intended physical claim. Once explicit adoption is relayed, re-check the baseline, apply only the accepted edits, complete the actual dated decision record and update AGENTS/README version references together. An adopted v2.1 would still be HOLD; it is not G1 acceptance or implementation authorization.

The pending diff can be syntax/context-checked with `git apply --check` without applying it. The reviewed preview is a working proposal, not a second source of truth. Any baseline change requires refreshing the diff and hash manifest before adoption.

## Copyable next message to GPT

```text
Read the latest published main commit, the current four context files,
docs/reviews/CODEX_RESPONSE_TO_GPT_G1_v2_1.md, and
docs/proposals/v2_1/MASTER_v2_1_PREVIEW.md plus its pending patch.

MASTER v2 remains authoritative. All v2.1 changes are pending.

Review B1–B6 at equation level:
1. algebraic reaction selection and nine-state closure;
2. parameter-dependent contact slices and joint tube quantifiers;
3. finite-height roll/pitch balance versus prescribed normal loads;
4. which phi assumptions are actually needed;
5. complete symmetry conditions;
6. narrowing to globally fixed parameter uncertainty.

For each: Finding / Evidence / Consequence / Status / Required action.
Explicitly accept, modify or reject the proposed text. Identify remaining
physical scope obligations. Do not conclude GO, implement, or treat model
agreement as proof. Return any corrections through the user.
```
