# Codex review — G4 Auer protocol v3 R6

**Date:** 2026-10-02  
**Review lane:** `LUNA-G4-AUER`  
**Input:** `LUNA_TO_CODEX_G4_AUER_PROTOCOL_V3_R6_COMPOSITION_BLOCKER_FULL_HANDOFF.md`  
**Disposition:** **PARTIAL.** Archived-proof composition evidence is accepted in its stated scope; the prospective R3 worker has a deterministic profile-key blocker. No matched query is authorized by this review.  
**Research state:** **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.**

I read `AGENTS.md` and the four canonical `research_context/` files. This was a read-only source and stored-artifact review. I did not invoke either matched worker, rerun the fixture, run query 1, or start the 1,944-query batch. I did not commit or push. The other shared-tree session, `LUNA-G2-SCOPE`, owns a separate G2 scope audit.

## 1. Identity and archived evidence

**Finding.** The R6 candidate and the selected non-query evidence have the stated byte identities.

**Evidence.** I recomputed manifest v6 SHA-256 `f722ac6f2df39cc1f2fdbae8ea3df7b1684c91659efb708aeba01fb5b436fa65`, source-closure SHA-256 `56de9b89ed0d6bc0d4b46e88163b37e3254e61c4dbf2f95a306fcc8b83205c72`, and every **92/92** listed dependency digest. The import-audit artifact reports 23 reachable local modules, 69 directed edges and zero unresolved local imports; I checked its recorded counts but did not rerun its AST traversal. The selected fixture report hashes to `41572aee0145f8ba696ad8d5139c92701bd47ab66d40c1a68fd0b4b31aff0c0c`; its separate guard hashes to `1e02a54ee709e362081f0a3b828d430d261e6e48e36060830a0403efd8025569` and binds that report and the R6 closure. The stored report records both archived-proof compositions as passing and **13/13** digest-recomputed mutation trials rejected with the expected named premise error. The guard reports zero producer, matched-worker and batch invocations.

Manifest v6 records 1,944 ordered IDs with digest `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`, all `NOT_RUN`, `matched_query_evaluations=0`, `comparison_run=false`, `query_1_authorized=false`, and `batch_start_authorized=false`. The fixture uses one archived R4 Auer proof and one archived R3 record; it does not exercise prospective worker completion.

**Consequence.** These artifacts support the exact archived-fixture claim. They provide no measured one-query worker outcome or matched comparison.

**Status.** **VALID for checked identities and archived non-query scope.**

**Required action.** Preserve the R6 candidate, fixture and predecessors byte-for-byte when preparing a correction.

## 2. Proof-to-common logic and the `work` comparison

**Finding.** The R6 verifier supplies the missing proof-to-common checks for the two archived cases. The apparent extra input parse before its common check is not, by itself, an arithmetic-operation mismatch.

**Evidence.** `verify_matched_composition_v3_r6.py:427-525` opens the bound proof and common record, replays the native proof, reconstructs Auer or R3 segments, compares every serialized segment and frozen common input, recomputes `check_tube_segments`, then checks final status and both delivered margin vectors. The R3 worker reparses its adapter segment under the common-stage `Budget` (`r3_matched_query_worker_v3_r6.py:177-203`); the verifier mirrors this at `verify_matched_composition_v3_r6.py:313-341,466-499`. The in-worker common-record replay deliberately compares predicate fields while validating stored `work` separately (`replay_common_check_record_v3_r6.py:49-101`). The offline verifier instead reconstructs the original check path and compares the complete record at `verify_matched_composition_v3_r6.py:501-508`. Its `_expected_inputs` pass parses rationals before the check, but `parse_q`/`Interval.from_json` use `Budget.check_input`, which explicitly does not count arithmetic operations (`rational.py:79-89,298-327,353-356`). Both archived records passed the complete comparison.

**Consequence.** I do not find a `work`-counter blocker from this extra input parse in the currently reviewed path. This is a source-path and archived-fixture conclusion, not a prospective worker observation or a general claim for future modified code.

**Status.** **VALID for the stated archived composition; prospective path UNVERIFIED.**

**Required action.** Keep the distinction between original common-record construction and later serialized-record replay explicit. Include a prospective end-to-end check after the source blocker below is corrected and separately authorized.

## 3. Deterministic prospective R3 worker blocker

**Finding.** The R3 worker reads a required top-level profile key that its R6 profile does not contain.

**Evidence.** `r3_matched_query_worker_v3_r6.py:333-345` executes `int(profile["max_serialized_proof_bytes"])` for every producer-returned record when writing the native proof. `validation/configs/r3_g4_matched_profile_v3_r6.json` has no `max_serialized_proof_bytes` key. A static enumeration of literal top-level `profile[...]` accesses found this as the sole missing key in the R3 worker; the Auer worker's corresponding keys are present. The `try` around the R3 write catches `OutputSizeLimitError` and `MemoryError`, not `KeyError`. The archived R3 fixture creates its fixture proof and result files directly (`protocol_v3_r6_composition_fixture.py:603-635` and the fixture delivery helper); it does not call `r3_matched_query_worker_v3_r6.run_one`.

**Consequence.** Once the R3 native producer returns a record, the prospective R3 worker will raise `KeyError` at proof serialization instead of issuing the declared complete/size-limited artifact. A recovered checkpoint may classify the run as an implementation failure, but this does not make the intended R3 matched-query path executable. The archived fixture cannot detect this failure. R6 cannot be the final matched-protocol freeze and query 1 should not start from this candidate.

**Status.** **BLOCKER for prospective R3 execution and final freeze.**

**Required action.** In a new versioned candidate, declare a finite R3 serialized-proof byte cap before any query execution, justify it against the existing external resource contract, use that exact cap in worker and validation metadata, and add a non-query static/profile-contract check that reaches this lookup. Do not silently alter R6 or relabel the archived R3 record as a new-profile output. Rebuild source closure, manifest, profile/input hashes and affected non-query evidence.

## 4. Auer combined RHS resource premise

**Finding.** The read-only Auer verifier does not currently mirror the prospective worker's combined producer-plus-native-replay RHS/Jacobian evaluation cap.

**Evidence.** The Auer profile declares `max_rhs_jacobian_evaluations_per_ivp=100000` with combined producer/native-replay scope. The worker seeds `rhs_eval_counter` from `proof.work.rhs_jacobian_evaluations` and passes it to `replay_native_proof` (`auer_matched_query_worker_v3_r6.py:489-519`). The offline verifier calls `replay_native_proof` without that counter (`verify_matched_composition_v3_r6.py:255-275`), so `replay_ivp.py:560-567` starts its audit counter at zero. The verifier later accounts for producer and replay *rational operations* at `:453-463`, but has no analogous combined RHS-count check. The archived fixture is far below the 100,000-evaluation cap and does not stress this difference.

**Consequence.** This does not invalidate the archived trajectory replay or its common predicate. It does mean an offline `PASS` alone does not establish the same combined RHS resource premise as the prospective Auer worker. The separate audit process may have its own resources, but the report must not imply that it has independently checked every method-worker cap unless this counter is reconciled.

**Status.** **OPEN resource-accounting contract gap; blocker for a fully audited matched resource claim.**

**Required action.** Mirror or explicitly verify the worker's combined RHS counter in the next verifier version, using the frozen profile and complete-proof work record. Distinguish this method cap from the separate post-worker audit's 120-second/1-GiB guard. Add a non-query boundary fixture for the count and its rejection behavior.

## Disposition and session boundary

R6 makes meaningful progress on the archived proof-to-common composition gap, but the missing R3 profile key is a direct prospective execution blocker. The Auer combined RHS cap also needs a precise audit contract before final matched-resource claims. The next correction belongs to **`LUNA-G4-AUER`**. **`LUNA-G2-SCOPE`** continues its separate G2 proof/usefulness audit and must not edit the G4 frozen source or manifest. No query 1, batch, G3 construction, gate promotion, physical-safety claim, commit or push follows from this review.
