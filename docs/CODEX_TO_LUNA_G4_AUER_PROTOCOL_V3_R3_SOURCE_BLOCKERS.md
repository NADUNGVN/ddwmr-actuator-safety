# Codex to Luna — resolve v3 R3 Auer source-contract blockers

**Date:** 2026-10-02  
**Review:** `docs/reviews/CODEX_G4_AUER_PROTOCOL_V3_R3_SOURCE_REVIEW.md`  
**Authority:** MASTER v2.1 and `AGENTS.md`; read all four canonical `research_context/` files.  
**Boundary:** Preserve every earlier candidate and R3 v5/R4/R5 artifact. Keep the shared tree uncommitted and unpushed. Do not run query 1 or the 1,944-query matched batch. No gate change or G3 work.

The v4 manifest is not ready for GPT freeze review. Its 53 listed hashes match, but static source inspection found four deterministic Auer blockers:

1. `matched_worker_common_v3_r3.py` emits input schema `...v3-r3`; the byte-identical matched solver requires `...v3-r2`, so it raises `InvalidInput` before producing a proof.
2. The matched solver writes the historical `small_case_resource_profile_v2.json` path into `proof.binding`; the worker's native replay expects `auer_g4_matched_profile_v3_r3.json`, so a proof-complete record fails binding comparison.
3. The Auer worker emits `shared_common_source_sha256`, which the root result schema forbids through `additionalProperties: false`.
4. The artifact validator looks for `proof.input_sha256`, while the producer stores that digest at `proof.binding.input_sha256`; it rejects a complete Auer proof.

## Required correction

- Issue **new versioned** solver/helper/worker/validator/protocol/schema/profile/closure/manifest files as needed. Keep the accepted residual/Picard equations and historical R4/R5 sources unchanged. Version changes to input guards and proof binding explicitly; do not describe a changed solver file as byte-identical.
- Align the case schema, full proof binding (including matched profile path/hash), Auer emitted result keys, and validator's input-digest location. Keep strict native replay and artifact validation.
- Make one non-query contract fixture from the actual source shapes: construct the case through the helper, confirm its schema is accepted by the versioned solver guard; inspect the producer's seeded proof binding against the worker's `expected_binding`; validate a structurally faithful Auer result/proof shape without claiming a trajectory proof. Include the rejection cases that exposed these four defects. The synthetic control-flow probe alone missed them.
- Recheck all worker result branches against the result schema, especially structured `RESOURCE_LIMIT`, `INVALID_INPUT`, proof-complete/common-UNKNOWN, and `CERTIFIED`. Do not promote fabricated proof content to mathematical evidence.
- Version the guard profile so it no longer embeds stale probe paths. Let the downstream manifest bind the profile/closure and fresh probe-index hashes; avoid a profile→probe-index→closure→profile hash cycle. Reissue closure and fresh memory-probe evidence for the corrected source identity.

Return a complete Markdown handoff under `docs/reviews/` with exact hashes, source diff, four defect dispositions, static contract evidence, source-closure and 1,944-ID checks, and explicit limits of non-query probes. The matched batch must remain **0/1,944**, with all rows `NOT_RUN`, `comparison_run=false`, and `query_1_authorized=false`. Do not send the present v4 candidate to GPT as a freeze-ready package.
