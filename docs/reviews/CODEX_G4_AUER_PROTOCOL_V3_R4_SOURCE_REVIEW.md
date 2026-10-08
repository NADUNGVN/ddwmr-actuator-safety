# Codex review — G4 Auer protocol v3 R4 source candidate

**Date:** 2026-10-02  
**Input:** `LUNA_TO_CODEX_G4_AUER_PROTOCOL_V3_R4_SOURCE_BLOCKERS_FULL_HANDOFF.md`, protocol v3 R4, candidate manifest v5, source closure, worker/solver/guard/validator, and stored non-query evidence.  
**Disposition:** **Four R3 source-contract blockers corrected; PARTIAL for final freeze.** The prospective artifact validator still lacks proof-to-common composition binding.  
**Research state:** **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED; matched batch 0/1,944.**

I read `AGENTS.md` and the four canonical `research_context` files. This review inspected source and existing artifacts only. I did not invoke a matched worker, run query 1, rerun the 64-MiB probes, produce or replay a new trajectory proof, or start the batch. The shared tree was not committed or pushed.

## 1. R3 source-contract corrections

**Finding.** The four deterministic mismatches identified in the R3 review are corrected in the R4 source candidate.

**Evidence.** The helper emits `ddwmr-g4-auer-matched-query-input-v3-r4` (`matched_worker_common_v3_r4.py:333`), and the versioned solver checks the same value before matched-case processing (`residual_ivp_g4_matched_v3_r4.py:74-77,471`). The solver seed takes `resource_profile_path` as an explicit argument (`:80-100,499-507`); the worker supplies `validation/configs/auer_g4_matched_profile_v3_r4.json` and uses the same path in its expected proof binding (`auer_matched_query_worker_v3_r4.py:65-83,340-378`). Native replay still compares the complete proof binding with `expected_binding` (`replay_ivp.py:576-577`).

The Auer worker assigns `common_adapter_source_sha256` and no longer emits the undeclared `shared_common_source_sha256` (`auer_matched_query_worker_v3_r4.py:346-355`). The R4 result schema requires the former and retains root `additionalProperties: false`. The artifact validator reads `proof.binding.input_sha256`, compares the full reconstructed binding, and compares `query_action_binding` with the frozen query (`validate_matched_result_v3_r4.py:128-184,190-208,273-287`). The versioned solver diff changes metadata/input-contract code; its residual/Picard step body is unchanged from the R3 copy.

**Consequence.** The exact R3 schema, profile-path, result-key, and proof-digest-location blockers no longer prevent the R4 Auer path at source level. This is not evidence that a prospective query completes or that the full artifact checker accepts a real produced proof.

**Status.** **VALID for these four static corrections.**

**Required action.** Preserve these bindings and strict native replay in any next version.

## 2. Candidate identity, closure, and non-query evidence

**Finding.** The stated package identities and zero-query status are internally consistent. The probe-path cycle was removed from the guard profile.

**Evidence.** I independently recomputed manifest v5 SHA-256 `735a36130916f4cbbc28924b3f937cd2a5acb70e4e78d28af5d46b5b959d66f4`, source-closure SHA-256 `33ec3437d55136117e9c322ce588458aa484060702e7fb46c579ccb47447762b`, and all **53/53** listed dependency hashes. The import audit lists 19 reachable local modules and 53 edges; all 19 module paths and hashes occur in the closure, and it reports no unresolved local imports. I did not independently rerun its AST traversal. Another **23/23** selected manifest/index references to protocol, schema, profiles, workers, validator, fixture reports, probe records, and stdout have matching exact-byte hashes.

The Auer candidate manifest has **1,944 unique ordered IDs**, all `NOT_RUN`; the LF-joined digest is `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`. Manifest v5 records `matched_query_evaluations=0`, `comparison_run=false`, and `query_1_authorized=false`. The guard profile has no old or R4 probe-output paths. Its pinned Python executable exists at the declared hash. The fresh probe index and both stored 64-MiB records have the declared hashes and report allocation failure under an installed process-commit cap. The stored fixture report exercises source contracts and in-memory schema shapes only. The clean-copy report records 53 copied dependencies, 25 compiled files, and 19 imported modules; I verified its hash, not its temporary execution independently.

**Consequence.** The candidate is reproducibly identified and the old profile-to-probe path ambiguity is corrected. The probes establish their declared memory-probe scope only; they do not measure the 120-second/1-GiB query pipeline. The fixture supplies no native proof, full validator pass, or matched observation.

**Status.** **VALID for checked identities and declared non-query scope; prospective query pipeline UNVERIFIED.**

**Required action.** Keep all rows `NOT_RUN`; retain the previous candidates and R3/R4/R5 evidence. Preserve the stated limitation on external member-by-member audit of the v10/v11 snapshot trees.

## 3. New final-freeze blocker: proof-to-common artifact composition

**Finding.** The R4 worker derives Auer common segments from a replayed native proof in its honest execution path, but the persistent artifact validator does not establish that the stored common record came from that proof or even from the frozen query scene. This remains a deterministic checker-contract gap for a proof-backed matched result.

**Evidence.** The worker calls native replay before `_make_segments`; `_make_segments` copies `full_time_total_hull_augmented` and endpoints from each proof step and embeds native proof digests in segment provenance (`auer_matched_query_worker_v3_r4.py:121-151,503-594`). By contrast, `validate_result_object` checks the common file hash/size, predicate status, segment count, segment self-digest, and the record's Boolean `full_closed_hold_covered` (`validate_matched_result_v3_r4.py:341-369`). It does **not** compare `common_record.inputs` with the reconstructed benchmark, scene, horizon, and initial state. It does **not** compare common segments and their provenance with the proof's step hulls/endpoints or proof/file digests, call `replay_common_check_record`, or compare the result's margin vectors with `segment_checks`. The native proof is checked separately at `:303-319`; the two verified files are not joined by an enforced predicate. The same result validator serves both arms.

The R4 non-query fixture calls `_check_schema` on invented `CERTIFIED` and common-UNKNOWN shapes with placeholder paths/sizes; its own report explicitly says those shapes did not pass full artifact validation or native replay. The archived R5 composition verifier is hard-bound to the earlier selected R4 case and v10/v11 snapshots (`verify_auer_composition_replay_v1.py`, including `EXPECTED_QUERY`); it is not a per-query verifier for this prospective v3 R4 worker output.

**Consequence.** A common record's self-consistency and file digest do not by themselves prove that its tube and scene are the ones certified by the native proof for this query. The source control flow supports linkage for an unaltered worker run, but a later independent reader cannot accept the persisted proof-to-common composition on the current validator alone. No actual matched result has been produced, so this is a source-level gap, not a claim that a particular certificate is false.

**Status.** **BLOCKER for final freeze and proof-backed matched-result acceptance.**

**Required action.** Add a versioned, read-only per-query composition check for both arms. Reconstruct the frozen input; compare the common record's benchmark/scene/horizon/initial-state binding and its exact segments, endpoints, radius mode, label image and provenance against the validated native proof and method adapter. Recompute or independently replay the common predicate and compare the stored margins/status; reject mutations of the common file or result even when their hashes are recomputed. Keep any offline audit time distinct from the declared per-method 120-second guard measurement. Bind changed source in a new closure/manifest and provide non-query mutation fixtures. Preserve archived R5 artifacts unchanged.

## Disposition and next boundary

R4 **resolves the four R3 Auer wiring blockers and stale probe-path issue**, but candidate v5 is **not a final freeze**. The proof-to-common composition check above is still required. A source/proof review and a separately authorized one-query guard-boundary inspection must precede any batch-start decision. The matched batch remains **0/1,944**; query 1, the 1,944-query batch, G3 construction, and any gate promotion remain outside this review.
