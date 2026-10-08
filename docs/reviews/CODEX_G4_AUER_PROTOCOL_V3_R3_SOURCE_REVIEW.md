# Codex review — G4 Auer protocol v3 R3 source-corrections candidate

**Date:** 2026-10-02  
**Input:** `LUNA_TO_CODEX_G4_AUER_PROTOCOL_V3_R3_SOURCE_CORRECTIONS_FULL_HANDOFF.md`, protocol v3 R3, candidate manifest v4, 53-file closure, import audit, workers, guard, validator, and probe records.  
**Disposition:** **PARTIAL; BLOCKED for final freeze.** The R2 source-closure, resource-status, and timing corrections have substantial static evidence, but three deterministic Auer contracts disagree.  
**Research state:** **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED; matched batch 0/1,944.**

This review inspected source and existing non-query artifacts. It did not execute a matched query, rerun the probes, or grant batch authorization. The synthetic control-flow probe is not a mathematical proof.

## 1. Auer input schema prevents the matched solver from starting

**Finding.** The R3 query helper emits a schema that the byte-identical R2 solver copy rejects.

**Evidence.** `validation/g4/matched_worker_common_v3_r3.py:327` creates `case["schema"] = "ddwmr-g4-auer-matched-query-input-v3-r3"`. The matched solver `validation/baselines/auer2013/residual_ivp_g4_matched_v3_r3.py:449-450` requires `"ddwmr-g4-auer-matched-query-input-v3-r2"` and raises `InvalidInput` otherwise. `auer_matched_query_worker_v3_r3.py` passes this R3 case directly to that solver. The v3 R3 solver file is indeed byte-identical to the v3 R2 copy, which explains the stale guard but does not make the R3 input acceptable.

**Consequence.** Every correctly constructed R3 Auer query reaches `INVALID_INPUT` before a native proof can be produced. The clean-copy import check and synthetic control-flow probe do not exercise this call. A hash-correct package is not an executable matched Auer arm.

**Status.** **BLOCKER.**

**Required action.** Version the matched solver input guard or the case contract so they agree, preserving the accepted residual/Picard equations. Bind the exact case schema in source, protocol, closure, manifest, worker and replay review. Keep the earlier solver copy unchanged.

## 2. Auer proof profile binding fails native replay

**Finding.** The matched solver seeds a historical profile path into its proof, while the prospective worker requires the R3 matched profile path.

**Evidence.** `_seed_record` in `residual_ivp_g4_matched_v3_r3.py:91-92` writes `binding.resource_profile_path = "validation/baselines/auer2013/small_case_resource_profile_v2.json"` with the prospective profile hash. The worker builds `expected_binding.resource_profile_path = "validation/configs/auer_g4_matched_profile_v3_r3.json"` at `auer_matched_query_worker_v3_r3.py:326-327`. `replay_native_proof` in `replay_ivp.py:576-577` rejects any `proof.binding != expected_binding` before verifying the trajectory. These paths are unequal for every prospective Auer proof.

**Consequence.** Even after fixing Finding 1, a proof-complete Auer producer cannot pass the worker's native replay. This is a proof metadata contract problem; it does not show the residual/Picard mathematics is invalid.

The same hard-coded profile path was present in the R2 solver copy. My earlier R2 source review accepted the step-policy alignment but missed this producer/replay binding mismatch; that earlier assessment does **not** establish a runnable R2 Auer query path.

**Status.** **BLOCKER.**

**Required action.** Make the versioned producer record the actual matched profile path and hash, and preserve strict replay comparison. Review the complete binding object, not only the one path, before reissuing source hashes.

## 3. Auer result contains a field forbidden by its schema

**Finding.** The Auer worker adds an undeclared top-level field to every post-input result.

**Evidence.** `auer_matched_query_worker_v3_r3.py:344` assigns `result["shared_common_source_sha256"]`. The result schema has `additionalProperties: false` at its root and contains `common_adapter_source_sha256` but no `shared_common_source_sha256` property. The validator's `_check_schema` rejects an unexpected top-level field. The outer guard invokes this validator on any worker result before delivering it.

**Consequence.** Once the Auer worker gets past input validation, its result is rejected as an artifact-validation error, including structured resource and invalid-input outcomes. Removing the duplicate assignment or versioning the schema is required; the common-source hash is already carried in `common_adapter_source_sha256` and the full source map.

**Status.** **BLOCKER for matched-result acceptance.**

**Required action.** Align the Auer result keys and schema, then inspect every emitted status branch against the same schema and cross-field validator. A synthetic result fixture cannot substitute for the actual worker-produced shape.

## 4. Closure, retained evidence, and resource corrections

**Finding.** The R2 omitted local import is now listed, and the new candidate's declared byte identities are internally consistent. This does not resolve Findings 1–3.

**Evidence.** I recomputed all 53 listed source-closure dependency hashes: **53/53 match**. The closure SHA-256 is `4e19ddf5f4fdfa28bc47bcd12baf96f82ee1682021f74b28dc375a9098400bf8`; candidate manifest v4 is `9a5994399a5296af1671369c7e08b79a96193d0d0037d10fa522fbf48b7146ca`. The import audit lists 18 reachable local modules and 47 directed edges, including `validation/g2/polynomial.py`; each listed reachable module appears in the closure and the audit reports no unresolved local import. The retained clean-copy report records 53/53 copied hash matches and import/compile checks, not a native proof computation. The manifest records zero matched evaluations, `comparison_run=false`, `query_1_authorized=false`, and 1,944 unchanged `NOT_RUN` rows.

The checkpoint, distinct proof-size exception, partial-artifact byte identity, and non-self-referential worker/parent timing fields address the R2 review's source-level concerns. The stored synthetic control-flow report says those branches passed its own probe. Two fresh 64-MiB probe records are bound to the current closure and report installed Job Object limits and failed 256-MiB allocations. Those probes do not exercise the 120-second/1-GiB proof pipeline. I did not independently rerun them or replay native mathematical proof under the R3 candidate.

**Consequence.** Source identity and memory-probe setup are materially improved. The R3 Auer arm still cannot produce an accepted prospective result, so final freeze and meaningful paired evaluation remain blocked.

**Status.** **VALID for checked hashes and declared probe scope; query pipeline UNVERIFIED.**

**Required action.** Preserve all old R3 v5/R4/R5 proof records and the v10/v11 external snapshot-member audit limitation. Reissue a new versioned closure and manifest after correcting Findings 1–3. Keep resource probes distinct from scientific query results.

## 5. Guard-profile probe binding remains split

**Finding.** The preserved v3 R3 guard profile points to earlier probe files, while candidate v4 selects fresh closure-bound probes through a separate index.

**Evidence.** `g4_equal_resource_guard_v3_r3.json` embeds paths under `protocol_v3_r3_guard_probes/`. `protocol_v3_r3_source_corrections_probes/probe_refresh_index.json` says those older records bind closure `6f83fae5…`, while the fresh records bind `4e19ddf5…`. The handoff discloses the split; the candidate manifest hashes the fresh index. The guard launcher itself reads the profile for runtime/caps, not probe evidence.

**Consequence.** The v4 manifest identifies which probes are intended, but the execution profile is not self-contained evidence of the final source identity. A later reader of the profile alone could select stale probe records.

**Status.** **NEEDS REVISION before final freeze.**

**Required action.** In the next versioned guard profile, remove the stale embedded probe paths and state that the downstream freeze manifest selects probe evidence. Let that manifest bind the profile/closure hashes and a fresh probe-index hash. Do not embed a closure-bound probe-index hash into a profile that is itself hashed by the closure; that would create a hash cycle. Do not rewrite the preserved v3 R3 profile. The revised closure will require fresh probe binding again.

## 6. Auer artifact validator reads the input digest from the wrong proof location

**Finding.** The validator rejects any otherwise complete Auer proof because it looks for a top-level `input_sha256` that the producer never writes.

**Evidence.** `_seed_record` in `residual_ivp_g4_matched_v3_r3.py:84-96` places the digest in `proof["binding"]["input_sha256"]`. The DDWMR producer adds `proof["query_id"]` and `proof["query_action_binding"]` but no top-level `proof["input_sha256"]`. `_proof_record_sha` in `validate_matched_result_v3_r3.py` compares `envelope["proof"].get("input_sha256")` with the result's bound method-input digest. That left side is `None` for a normal Auer proof, so the validator raises `Auer proof input binding mismatch` before accepting the artifact.

**Consequence.** Fixing the solver input schema, replay profile path, and result schema still would not make a complete Auer result pass artifact validation. The source hash and query/action binding must be checked at their actual proof locations.

**Status.** **BLOCKER.**

**Required action.** Make the validator read `proof.binding.input_sha256` and check the whole expected Auer binding plus `query_action_binding` against the reconstructed frozen query. Retain exact-byte and embedded proof digests; do not weaken native replay to accommodate this mismatch.

## Disposition

The v4 manifest is a **review candidate only**. Findings 1–3 and 6 are deterministic source-contract blockers for the Auer arm; they are not judgments about the underlying Auer IVP theorem. Correct them in new versioned files, preserve previous candidates and historical evidence, and return a new handoff for source review. An authorized one-query end-to-end guard inspection and separate batch-start review are still future steps. **No query 1, no batch, no gate promotion.**
