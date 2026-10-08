# Codex to Luna — correct protocol-v3 R2 source candidate

**Date:** 2026-10-01  
**Review:** `docs/reviews/CODEX_G4_AUER_PROTOCOL_V3_R2_SOURCE_REVIEW.md`  
**Authority:** MASTER v2.1 and `AGENTS.md`. Read the four canonical `research_context/` files before work.  
**Boundary:** Keep the shared working tree uncommitted and unpushed. Preserve R1/R2 candidates and all historical R3 v5, R4 and R5 evidence. Do not run a matched query or the 1,944-query batch. No G3, controller, hardware or gate promotion.

## Correct these source and evidence gaps

1. **Complete the source closure.** `validation/g2/model.py` imports `validation/g2/polynomial.py`, yet the latter is absent from the 49-item closure. Audit all transitive local imports of both prospective workers, add every proof-relevant dependency with exact-byte hash, and issue a new versioned closure and freeze-manifest candidate. Rebind profile/schema/worker/probe references as needed. Do not mutate the existing v3 R2 candidate or historical evidence. Recheck a clean copied package and state the still-unavailable v10/v11 snapshot-member audit plainly.

2. **Keep native proof evidence across late resource stops.** The current outer guard overwrites `native_status` and `common_status` on timeout/memory limit. Add durable stage checkpoints or another reviewable bounded mechanism. The final status may be `RESOURCE_LIMIT`, while an already established native `PROOF_COMPLETE`/`CERTIFIED` state, raw status, proof digest/path, replay status and common UNKNOWN remain separate. If only a partial/unverified proof file exists, record its byte identity without asserting proof completion. Replace the fallback's all-zero input digest with the real query binding or an explicit unavailable value in a revised schema.

3. **Classify proof-size exhaustion correctly.** `write_json` currently raises `CandidateInputError` when a proof exceeds its declared size cap. Distinguish proof-size `RESOURCE_LIMIT` from invalid input, handle it in both workers, and retain producer status/work in a structured result. Specify the classification of an outer process-memory stop during JSON construction.

4. **Repair timing and result finalization.** Both workers write the result twice; the measured `final_result_serialization` covers the first write, not the delivered worker file. Specify a non-self-referential stage-timing method and a single clear final write or sidecar timing record. Keep the parent's outer wall through worker exit/output flush as the primary equal-resource measurement. Update workers, guard, protocol, schema and manifest consistently.

5. **Make result acceptance independently checkable.** JSON Schema's free-form `status_rule` does not enforce `CERTIFIED` iff native proof/replay and common predicate pass. Provide a validator or explicit replay/check path that checks output schema, query/source/profile hashes, proof-file and common-record digests, and cross-field status implications. It must reject mutation or corruption without converting it to a mathematical UNKNOWN. Correct stale candidate metadata, including `PROBES_PENDING` after fresh probes.

## Evidence to return

- A complete full handoff at `docs/reviews/LUNA_TO_CODEX_G4_AUER_PROTOCOL_V3_R3_SOURCE_CORRECTIONS_FULL_HANDOFF.md`, with Finding / Evidence / Consequence / Status / Required action.
- Exact hashes, old-to-new source diff, transitive-import inventory, new closure/manifest/profile/schema paths and clean-copy verification result.
- Targeted non-query evidence for timeout/memory/proof-size/partial-proof status retention and finalization timing. Rerun the 64-MiB probes for the newly hash-bound workers/closure; keep them explicitly separate from matched queries.
- Reconfirm 1,944 identical ordered IDs, all `NOT_RUN`, `comparison_run=false`, `query_1_authorized=false`, and **0/1,944** matched evaluations.
- A short GPT review request that asks for an independent source/proof/resource disposition in a downloadable `.md` file. Do not present the new candidate as finally frozen or ask GPT to infer G4 novelty from this preparation.

If any correction requires changing MASTER, the frozen query universe or historical R4/R5 proof mathematics/evidence, stop the affected branch and report the contradiction instead of editing those artifacts.
