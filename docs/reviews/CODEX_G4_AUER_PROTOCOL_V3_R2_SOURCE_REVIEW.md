# Codex source review — G4 Auer matched protocol v3 R2

**Date:** 2026-10-01  
**Input:** `LUNA_TO_CODEX_G4_AUER_PROTOCOL_V3_R2_CORRECTIONS_FULL_HANDOFF.md`, protocol v3 R2, candidate freeze manifest v3, source closure, profiles, schema, workers, guard, and retained probe records.  
**Disposition:** **PARTIAL / CORRECTIONS REQUIRED.** The listed identities and source-aligned mathematical route are credible. The candidate is **not a complete source closure or final freeze**. Query 1 and the 1,944-query matched batch remain unauthorized.  
**Research state:** **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED; matched batch 0/1,944.**

This is a source and artifact-identity review. I did not invoke either matched query worker, run the batch, rerun the old proof fixtures, or claim an end-to-end resource measurement.

## 1. Source-aligned route and query identity

**Finding.** R2 removes the earlier algorithm/source contradiction. The versioned Auer solver differs from the accepted `residual_ivp.py` in its module description and guards for schema, query ID, horizon, and voltage. The residual/Picard step-producing body is unchanged. The two prospective workers call the existing Auer replay or R3 evaluator/checker and the shared common-tube predicates.

**Evidence.** The source diff changes only the input checks near `solve_ddwmr_case`, leaving the remaining-horizon, native-inclusion-failure bisection policy in place. `matched_worker_common_v3_r2.py` reconstructs an Auer row and compares its semantic input hash with the existing candidate manifest. R3 `make_query` binds the prospective profile, benchmark, R3 development-manifest digest, query ID and specification-bundle digest into its native input hash; `replay_record` checks those fields for a successful native record. I independently compared the Auer manifest to the frozen R2 list: 1,944 IDs, 1,944 unique, exactly the same order, all `NOT_RUN`. Regenerating the benchmark's 6 × 12 × 3 × 9 IDs gave the same order and LF-joined SHA-256 `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`.

**Consequence.** The previous 0.01-second-base-slab and common-predicate-refinement mismatch is resolved at source level. This is not a successful matched query or a proof that every prospective query will finish.

**Status.** **VALID source alignment and declared ID identity, within static review.**

**Required action.** Keep the R2 step policy and preserve all old R4/R5 and R3 v5 evidence. Do not count the historical R3 v5 fixture as an equal-resource matched observation.

## 2. The 49 checked hashes are valid, but the source closure is incomplete

**Finding.** The inventory omits a proof-relevant transitive Python dependency.

**Evidence.** I independently recomputed all 49 `dependencies[].sha256` values in `G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R2.json`: **49/49 match**. The closure file's SHA-256 is `f63707d34118fe78fbf8e0e3ce73be9329bb6824ef3523e1375a91d11abc3bea`; candidate manifest v3 is `579b2ff675cbfff733bf539e8bb22bad5ce817b434807b8fa71417de5ff324bc`. Eleven direct manifest-to-file profile/schema/worker/solver/closure bindings checked also match. However, `validation/g2/model.py:9` imports `validation/g2/polynomial.py`, which is absent from the 49 dependencies. The missing file's current SHA-256 is `48e3ff7dcce8353cb9d58b31f6986e12fcaaaf320cd06896f95e0813740b66a4`. Both arms use `build_model` through their RHS or common-tube path, so this is within the prospective proof computation, not an unused historical file.

**Consequence.** “Every listed hash matches” is true; “complete proof-critical source closure” is false. The current clean-copy/freeze claim could miss a changed model polynomial parser or rational-function implementation.

**Status.** **BLOCKER for final source freeze.**

**Required action.** Add `polynomial.py`, audit the transitive local import graph of both workers, and issue a newly versioned closure and manifest. Rebind any profile/probe references whose hashes depend on the changed closure. Rerun the memory probes on that exact revised source identity; they remain memory probes, not matched queries. A clean copied-package hash audit remains required. Keep the stated v10/v11 snapshot-member limitation.

## 3. The outer guard can erase a completed native proof status

**Finding.** The guard's timeout/memory branches override `native_status` to `RESOURCE_LIMIT` and `common_status` to `NOT_EVALUATED` unconditionally. This disagrees with protocol §6's instruction to retain an already established native proof when a later stage stops.

**Evidence.** `run_matched_worker_guard_v3_r2.py:165-174` rewrites both fields even when it has loaded a worker result containing a proof path/hash, native `PROOF_COMPLETE` or `CERTIFIED`, replay result, and perhaps a common UNKNOWN. If a worker is killed after serializing its proof but before writing its final result, `:143-148` creates a fallback with null proof metadata; the existing proof file is not inspected or recorded. The workers normally write their result only after producer, proof serialization, native replay and common work (`auer_matched_query_worker_v3_r2.py:478-484`; `r3_matched_query_worker_v3_r2.py:288-295`). Thus the no-result window is real.

**Consequence.** The final outcome should be `RESOURCE_LIMIT` after an outer stop, but the record must distinguish that outcome from the native proof stage already reached. The current code can destroy that distinction and omit an extant proof artifact. A fallback also writes a 64-zero `method_input_sha256`, which is a placeholder rather than a binding to the query input.

**Status.** **BLOCKER for protocol/status fidelity and final freeze.**

**Required action.** Introduce durable stage checkpoints or an equivalent bounded recovery record. Preserve the worker's established native status, raw status, proof path and digests, replay status, and common status when present; set final/guard status to the actual outer resource stop. For a proof file without a validated stage checkpoint, retain its byte identity as a partial artifact but do not assert proof completeness or replay PASS. Bind fallback input to the real query or use an explicit unavailable value allowed by a revised schema. The guard must not silently turn a late resource stop into a native inclusion failure or erase proof-complete/common-UNKNOWN evidence.

## 4. A declared proof-size stop is reported as an implementation failure

**Finding.** Both workers have a proof-size cap, but exceeding it takes the input-error exception path instead of producing a structured `RESOURCE_LIMIT` record.

**Evidence.** `matched_worker_common_v3_r2.py:52-56` raises `CandidateInputError` when serialized bytes exceed `maximum_bytes`. The Auer and R3 workers call this function at proof serialization (`:380` and `:233` respectively) without a local size-limit handler. Their `main()` catches `CandidateInputError` and exits with a text message; if no result file exists, the outer guard's fallback records `IMPLEMENTATION_FAILURE`. Both method profiles and protocol §3 explicitly classify the proof-size cap as a resource stop.

**Consequence.** Resource-limit counts can be understated and implementation-failure counts overstated, particularly for large prospective proofs. A completed producer's native status and work can also be lost.

**Status.** **BLOCKER for matched-result taxonomy.**

**Required action.** Use a distinct size-limit exception/status, catch it at proof serialization in both workers, and emit a bounded structured result retaining producer status/work and a proof-size-stage `RESOURCE_LIMIT`. Preserve `INVALID_INPUT` for genuinely invalid input. Specify how an external memory stop during JSON construction is recorded; the 1-GiB guard remains authoritative for that case.

## 5. Final-result stage timing does not measure the final result write

**Finding.** The worker's `final_result_serialization` value measures its first result write, while the delivered worker result is rewritten a second time, and then rewritten by the parent guard.

**Evidence.** Auer `:478-484` and R3 `:288-295` write result JSON, set `final_result_serialization` to the duration of that write, update `total_wall_seconds`, and write it again. The second write is not measured by that stage field. The guard later replaces `total_wall_seconds` with a parent measurement obtained after `_run_guarded` returns, then rewrites the result (`run_matched_worker_guard_v3_r2.py:164,179`). `_run_guarded` does include worker exit and stdout flush, so the parent outer-wall value has a clear useful boundary. The self-referential worker stage value does not have the claimed “final result serialization” boundary.

**Consequence.** Equal external 120-second and 1-GiB caps are specified and both worker modules passed separate 64-MiB probe commands, but the per-stage timing fields are not yet comparable observations of the declared final artifact. The probes do not exercise the 120-second/1-GiB proof pipeline.

**Status.** **CORRECTION REQUIRED before timing-based matched reporting.**

**Required action.** Define a non-self-referential timing scheme with one clear final worker write and a separately recorded parent finalization duration, or put the measured write duration in a separate sidecar. Update both workers, the guard, schema and protocol together. When a single query is separately authorized, inspect actual worker/guard clocks, installed 1-GiB cap and `PeakProcessMemoryUsed` before freezing batch execution.

## 6. Artifact checks and remaining validation boundary

**Finding.** The candidate's listed probe records and manifest state are internally consistent, within the stated probe scope. Result-level status invariants are described in prose but are not enforced by the JSON Schema alone.

**Evidence.** Both stored probe JSON hashes and stdout hashes match manifest v3. Each record reports an installed 64-MiB process limit, suspended assignment before resume, a failed 256-MiB allocation with `MemoryError`, and `probe_enforcement_verified=true`. Manifest `batch_state` is 0 evaluations, `comparison_run=false`, `query_1_authorized=false`, and zero query-worker invocations. The result schema's `status_rule` is a nonstandard annotation; the guard uses `strict_json` but does not validate the loaded result against the schema or check its cross-field proof/common/final-status implication.

**Consequence.** The probes support memory-enforcement setup for the two probe commands only. Independently replayable native/common evidence must still accompany any later certified result; schema parsing by itself is not scientific proof verification.

**Status.** **VALID probe identity and candidate batch state; prospective artifact validation UNVERIFIED.**

**Required action.** Add a final artifact validator or equivalent explicit guard checks for schema, source/query/proof/common-record digests and the `CERTIFIED` implication. Keep a resource-stop record if a partial artifact cannot be replayed. Correct stale metadata such as the guard profile's `PROBES_PENDING` status after reissuing the candidate.

## Disposition and next handoff

The R2 correction resolves the earlier Auer step-policy mismatch and retains the narrow R3 v5 parity evidence. **Do not freeze this package yet.** Findings 2–4 block source completeness and outcome semantics; Finding 5 blocks truthful stage-timing claims. Implement the corrections in new versioned candidate files, preserve the R1/R2 candidates and all R3/R4/R5 evidence, then return a new full handoff with hashes and source diff. Request independent GPT review only of that concrete corrected candidate. The matched batch remains **0/1,944**; no gate changes.
