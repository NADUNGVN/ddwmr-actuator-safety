# Codex to Luna — protocol-v3 R2 corrections before GPT review

**Date:** 2026-10-01  
**Package:** `G4_AUER_MATCHED_PROTOCOL_V3_R2_CORRECTIONS`  
**Authority:** MASTER v2.1; read `AGENTS.md` and the four `research_context/` files first.  
**Starting review:** `docs/reviews/CODEX_G4_AUER_PROTOCOL_V3_PREPARATION_REVIEW.md`.  
**Boundary:** no 1,944-query matched batch, no G3/controller/hardware work, no gate promotion, no commit/push in this package.

## Required corrections

1. **Resolve algorithm-to-source mismatch.** Protocol candidate v3 specifies 0.01 s base slabs, depth-five refinement and bisection after common-predicate UNKNOWN, while frozen `residual_ivp.py::solve_ddwmr_case` starts with the remaining horizon and bisects only failed native inclusion. Choose and justify one path before final freeze:
   - prefer a versioned protocol policy that faithfully describes the existing accepted residual core, with common checking after the proof-complete full hold, if this still serves the matched scientific question; or
   - implement the proposed richer policy in new versioned producer/runner/replay source, preserve frozen R4/R5 source/artifacts, and provide a new independent proof-critical source review target.
   State exactly which path was chosen. Do not present a proposed policy as already implemented.

2. **Fix UNKNOWN and rollback semantics.** A native proof-complete slab with `UNKNOWN_ON_SUPPLIED_TUBE` remains a valid IVP enclosure. Define how optional refinement retains or replaces that parent proof, how a right child starts from the complete left endpoint, how all closed slabs cover `[0,T]`, and the final status if the predicate remains UNKNOWN at a depth limit. Never map that case to `INCLUSION_NOT_ESTABLISHED` or `RESOURCE_LIMIT` unless the actual failed premise warrants that status.

3. **Materialize paired resource contracts.** Specify and version the Auer and R3 matched profiles, common predicate profile, and complete-pipeline external 120 s / 1 GiB guard or a reviewed alternative. Identify measured stage boundaries, serial execution order and total wall/commit-memory accounting. Explain how the proposed shared exact-rational operation cap is charged through producer, native replay, adapter and common predicate for each method; if it cannot be implemented consistently, retain equal external caps and report method-native operations separately. Resolve the proposed common 24 square-root bisections versus R4's historical 128 without modifying R4/R5 evidence.

4. **Make source closure reviewable.** Auer `r4_worker.py` is hardcoded to the single frozen R4 input/profile. R3's historical runner also is not a prospective paired worker. Version any new per-query runner and proof binding, state whether the accepted producer/replay math is unchanged, and produce a candidate manifest that hashes every active source/profile/output-schema dependency. Keep historical snapshot-member limitations explicit. Preserve the existing 1,944 IDs and all old records exactly.

5. **Keep the R3 parity correction.** Reuse the already published v5 R3-to-common fixture. Do not duplicate it without a named deficiency. Its historical resource profile does not populate the primary equal-resource results.

## Deliverables

- A **new versioned protocol candidate**, leaving `G4_AUER_MATCHED_PROTOCOL_v3.md` untouched as the reviewed R1 candidate.
- A matching **new candidate freeze manifest** and materialized profiles/source where applicable. Do not label the candidate as finally frozen.
- A complete Markdown handoff at `docs/reviews/LUNA_TO_CODEX_G4_AUER_PROTOCOL_V3_R2_CORRECTIONS_FULL_HANDOFF.md`, with exact hashes and Finding / Evidence / Consequence / Status / Required action.
- A short GPT review request that points to the corrected version and requires GPT to return a downloadable `.md` file. The request must ask GPT to evaluate protocol/source alignment, status semantics, existing R3 parity, resource fairness and manifest closure. It must say that batch execution is still 0/1,944 and not authorized.

Stop and report a blocker if satisfying the protocol requires an unreviewed change to MASTER, the query universe, a frozen R4/R5 proof, or proof-critical mathematics. Do not run any matched batch query or infer G4 novelty from the preparation work.
