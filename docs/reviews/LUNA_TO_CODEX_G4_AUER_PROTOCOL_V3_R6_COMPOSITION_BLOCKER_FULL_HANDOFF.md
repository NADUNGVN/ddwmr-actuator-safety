# Luna to Codex — G4 Auer protocol v3 R6 composition-blocker handoff

**Date:** 2026-10-02  
**Input handoff:** `docs/CODEX_TO_LUNA_G4_AUER_PROTOCOL_V3_R4_COMPOSITION_BLOCKER.md`  
**Disposition:** R6 review candidate prepared; no matched query is authorized.  
**Research state:** HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence remain UNVERIFIED.

## 1. Executive summary

R6 adds a read-only, disk-backed, per-query proof-to-common composition verifier for both Auer and R3. It reconstructs the frozen query and input hash; loads the delivered result, native proof, common record, and worker guard receipt; replays the native proof; reconstructs common segments from that proof; checks frozen common inputs; recomputes the common predicate; and compares the delivered result's collision/contact margin vectors.

R6 also repairs R3 common-stage budget ownership. Adapter output is serialized and reparsed under the common-stage `Budget`, so that parse work is charged to the existing common-stage operation cap. Common-record replay compares predicate fields exactly and validates stored work counters separately, because replay parses the serialized inputs again and therefore has different work counts.

The final archived-proof fixture passed for both methods, and all 13 digest-recomputed mutations were rejected with their expected premise errors. Current-source Auer common-stage and 64-MiB memory-enforcement probes passed. Source closure and manifest rebuilds are stable. No query worker, query 1, or batch was run; the batch remains 0/1,944.

## 2. Candidate identity and exact-byte hashes

| Artifact | SHA-256 |
|---|---|
| `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R6.md` | `005b39ab1f01b9185a6730dc2e7b0529a415dfa3111af7397fe17f306fd7e594` |
| `research/benchmarks/G4_AUER_MATCHED_QUERY_RESULT_v3_R6_SCHEMA.json` | `a580feb637d91bee16ec2adf29361324d36cd9cabc8d15eb7f103c99907ec3e9` |
| `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R6.json` | `56de9b89ed0d6bc0d4b46e88163b37e3254e61c4dbf2f95a306fcc8b83205c72` |
| `research/benchmarks/G4_AUER_MATCHED_TRANSITIVE_IMPORT_AUDIT_v3_R6.json` | `65aaf17d6872e5751bfcef456d29e16da6eb58abb6d684b27026ab5c6c8743a9` |
| `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v6.json` | `f722ac6f2df39cc1f2fdbae8ea3df7b1684c91659efb708aeba01fb5b436fa65` |
| `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v6.sha256` | contains the matching manifest digest and filename |

The closure contains **92 exact-byte dependencies**. The AST import audit found **23 reachable local modules**, **69 directed import edges**, and **0 unresolved local imports**. A final independent pass recomputed every dependency digest. Rebuilding the candidate produced the same closure and manifest digests.

The manifest's result-schema pointer now names the R6 schema. It records 1,944 unique ordered IDs, digest `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`, every row `NOT_RUN`, and `matched_query_evaluations=0`.

### Principal versioned source identities

| Source | SHA-256 |
|---|---|
| `validation/g4/auer_matched_query_worker_v3_r6.py` | `f75646cb2cb0d6fbb064ce02257c9d0dbe5412095ebd83a05f231901796063c9` |
| `validation/g4/r3_matched_query_worker_v3_r6.py` | `5c6efc03b57de1115fa391b8a69b192756500b1a996853fe4a762a1af9cf4e61` |
| `validation/g4/matched_worker_common_v3_r6.py` | `922b436e6eccccf9fb46c9d5f67fc63ac46462b6b057b3df83cdba2d38d52004` |
| `validation/g4/replay_common_check_record_v3_r6.py` | `c8610ff9ac0667e2010225f766a596aac96433b282e9988000c0f53af3600853` |
| `validation/g4/verify_matched_composition_v3_r6.py` | `d19bfebcb1bfa6381d627cb8985add36ec3bc2ce047ef9a9a44fa8a94e289730` |
| `validation/g4/validate_matched_result_v3_r6.py` | `fc52c866df453d5652117324ea7c421fd09ef9786c697bc994080015e2266ca6` |
| `validation/g4/run_matched_worker_guard_v3_r6.py` | `95e0d3b8396483f789784bb3565456344887ba01cab865cf8262d2a8e228eb5d` |
| `validation/g4/run_matched_composition_audit_guard_v3_r6.py` | `6a7e9ad8c68983d446c2c126e39303cbe45bc8af9d9e9ef3fde80f7a82dfafc6` |
| `validation/g4/protocol_v3_r6_composition_fixture.py` | `c68dd227abeefa6fe3a1ebd047f2823b59319dc9ba73cb121f05d804513cadcc` |
| `validation/baselines/auer2013/residual_ivp_g4_matched_v3_r6.py` | `6664156486e7b9fe7c030a82ad66d6f98e66dc3efa846af71f0a9900c60172a7` |
| `validation/scripts/build_g4_auer_v3_r6_candidate.py` | `29245de790261f761756dba51d98c99b05cebf8cf41732713d2968d0a629d62d` |

| R6 profile | SHA-256 |
|---|---|
| `validation/configs/auer_g4_matched_profile_v3_r6.json` | `b1d00ca7ad8dfb4f4cceb2b278a71654ce44800632a3cdbe446925ba975df8ea` |
| `validation/configs/r3_g4_matched_profile_v3_r6.json` | `60136804dd5b6374b7f1020f564f43bb43c59c440393884a0aaaf046a208db48` |
| `validation/configs/g4_common_predicate_profile_v3_r6.json` | `2ab9999bd96c389f353c570c7f51562b8bc8bfb1e15fa134498431d484a8a36e` |
| `validation/configs/g4_equal_resource_guard_v3_r6.json` | `eaa01039cf99d232bd690838b954fe5cd0da97d7813478a02fe62e5d3d1eda10` |

## 3. Source changes and proof-to-common premises

The R6 protocol and schema version the candidate contract. The Auer and R3 workers, common binding helper, result validator, worker guard, composition verifier, separate audit guard, common-record replay helper, fixture runner, and candidate builder are all R6-specific and hash-bound by the closure.

**Native proof replay and common predicate replay are distinct acceptance premises.** The verifier independently replays the native Auer proof or R3 record against the reconstructed frozen query. It then reconstructs the expected common segments from that replayed proof and separately recomputes the common predicate. A stored status flag alone cannot satisfy either premise.

For Auer, reconstructed segments use each proof step's full-time total hull, closed times, endpoints, unchanged frozen label image, `NATIVE_TOTAL_HULL`, and zero radius expansion. Segment provenance binds the native proof body digest, proof file digest, native method, and proof source-snapshot identity.

For R3, the verifier uses the declared `r3_record_to_common_segment` adapter and `CENTER_PLUS_RADIUS_ONCE` semantics, with one radius expansion. It serializes the adapter output and reparses it using the common-stage budget before predicate evaluation. The R3 reparse consumes that stage's existing cap; no extra cap was granted. The common integer-string ceiling is set to the profile's declared 10,000 digits, consistent with its 32,768-bit rational ceiling.

For both methods, the verifier binds the common record's benchmark, scene, horizon, and initial state to the reconstructed query. It compares every serialized segment field, the full recomputed predicate payload, status, segment checks, margins, and delivered collision/contact margin vectors. Replay-only `work` counts differ because replay parses inputs again; the R6 replay helper validates the stored work schema and cap consistency separately from exact predicate-field equality.

The archived R4 Auer proof uses a legacy native input hash. The fixture retains that archived hash separately from the reconstructed R6 candidate query hash and validates the frozen `query_action_binding`; it does not relabel the legacy proof as a prospective R6 worker output.

## 4. Full-composition archived-proof fixture

Selected final evidence:

- Fixture report: `results/validation/g4/auer2013/protocol_v3_r6_composition_fixtures_retry6/composition_fixture_suite_report.json` — SHA-256 `41572aee0145f8ba696ad8d5139c92701bd47ab66d40c1a68fd0b4b31aff0c0c`.
- Separate Job Object guard: `results/validation/g4/auer2013/protocol_v3_r6_fixture_guard_retry6/fixture_suite_guard.json` — SHA-256 `1e02a54ee709e362081f0a3b828d430d261e6e48e36060830a0403efd8025569`.
- Both records bind closure `56de9b89ed0d6bc0d4b46e88163b37e3254e61c4dbf2f95a306fcc8b83205c72`.

The fixture reused one archived R4 Auer proof and one archived R3 native record for the same selected ID, `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`. It created fixture-only delivered-result/common-record/receipt files and ran the full disk-backed composition verifier. It created no trajectory proof and invoked no Auer producer, R3 evaluator, or matched worker. Both pristine archived compositions passed native replay and common predicate replay, with one segment each and fixture status `CERTIFIED`.

| Method | Frozen method-input SHA-256 | Native proof/record SHA-256 | Radius semantics | Common predicate |
|---|---|---|---|---|
| Auer | `b59dc0f4bd05bf277384387115e7138d6df6450c187d2eefd38cae577a474e94` | `8d394d836c5b92b733403b16b1786cb7fe410ab8fb8610c694c0a7c88e5dde4e` | `NATIVE_TOTAL_HULL`, expansion count 0 | `PASS_ON_SUPPLIED_TUBE` |
| R3 | `497d6fee06f8dde5c54905ecc1a32c0c17dbb85710e54bcea95ce85531030d5f` | `e6b396f557f68967c1648493a08239456c2669cfd44157d3f868b0efab4ab000` | `CENTER_PLUS_RADIUS_ONCE`, expansion count 1 | `PASS_ON_SUPPLIED_TUBE` |

All 13 mutation trials recomputed dependent artifact digests and guard receipts before verifier execution. All 13 were rejected, and each observed premise error matched its expected error:

| Method | Mutation | Expected and observed premise error |
|---|---|---|
| Auer | Changed scene binding | `COMMON_INPUT_SCENE_MISMATCH` |
| Auer | Substituted segment hull | `COMMON_SEGMENT_HULL_MISMATCH` |
| Auer | Changed segment endpoint | `COMMON_SEGMENT_ENDPOINT_MISMATCH` |
| Auer | Altered proof provenance | `COMMON_SEGMENT_PROVENANCE_MISMATCH` |
| Auer | Mutated delivered contact margin vector | `RESULT_CONTACT_MARGIN_VECTOR_MISMATCH` |
| Auer | Changed frozen input hash | `FROZEN_INPUT_HASH_MISMATCH` |
| Auer | Altered native proof source binding | `NATIVE_PROOF_SOURCE_BINDING_MISMATCH` |
| R3 | Changed scene binding | `COMMON_INPUT_SCENE_MISMATCH` |
| R3 | Substituted segment hull | `COMMON_SEGMENT_HULL_MISMATCH` |
| R3 | Changed segment endpoint | `COMMON_SEGMENT_ENDPOINT_MISMATCH` |
| R3 | Altered proof provenance | `COMMON_SEGMENT_PROVENANCE_MISMATCH` |
| R3 | Mutated delivered contact margin vector | `RESULT_CONTACT_MARGIN_VECTOR_MISMATCH` |
| R3 | Altered native proof input binding | `NATIVE_PROOF_INPUT_BINDING_MISMATCH` |

The pristine reports confirm that result, proof, common record, and guard receipt were loaded from disk; the frozen query was reconstructed; native replay passed; serialized proof-derived segments matched; common inputs matched the frozen query; the common predicate was replayed; and delivered margin vectors matched the recomputation.

## 5. Resource accounting

| Activity | Guard and scope | Observed result | Interpretation |
|---|---|---|---|
| Auer worker common-stage helper on archived proof | Separate 120 s / 1 GiB Job Object | `PASS_ON_SUPPLIED_TUBE`; 6,039 total operations under the 2,000,000 method cap; 0.172 s outer wall; 18,116,608-byte peak | Called `_run_common_stage` only. No producer, IVP solver, evaluator, or matched query ran. It is a helper diagnostic, not a method-worker measurement. |
| Full archived-proof composition fixture | Separate 600 s / 1 GiB Job Object | PASS; 3.156 s outer wall; 52,826,112-byte peak | Includes pristine replay and all mutations for both archived arms. This use is isolated from any method-worker measurement. |
| R3 fixture adapter conversion | Declared 2,000,000-operation conversion cap | 1,251 operations | Separate from the common stage. |
| R3 fixture common stage, including serialized-segment reparse | Declared 2,000,000-operation common-stage cap | 2,415 operations | Reparse is charged to the common-stage budget. |
| Auer fixture common stage | Archived fixture cap 1,799,969 operations | 2,415 operations | Fixture audit accounting; distinct from the direct worker helper's 6,039 operations and 2,000,000 cap. |
| Auer 64-MiB guard probe | 64 MiB cap; requested allocation 256 MiB | Enforcement PASS; 66,445,312-byte peak | Probe command only; it did not run a query. |
| R3 64-MiB guard probe | 64 MiB cap; requested allocation 256 MiB | Enforcement PASS; 66,592,768-byte peak | Probe command only; it did not run a query. |

The full method worker's declared 120-second / 1-GiB boundary covers input validation, producer, proof serialization, native replay, common adaptation, common predicate/common-record replay, common serialization, and worker result serialization. No such worker pipeline was run, so its timing and memory remain unmeasured.

The post-worker composition verifier is specified as a separate read-only 120-second / 1-GiB process. No prospective post-worker audit was possible without a matched result. The archived-proof fixture exercised the verifier under its separate 600-second / 1-GiB fixture guard; its elapsed time and peak memory are reported above, not added to either method's worker measurement.

## 6. Query universe and authorization boundary

Independent checks reconstructed the 1,944 ordered IDs from the frozen benchmark and source universe. IDs match exactly; all candidate rows remain `NOT_RUN`; the LF-joined ID digest is unchanged at `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`.

The R6 manifest records `comparison_run=false`, `query_1_authorized=false`, `batch_start_authorized=false`, and `matched_query_evaluations=0`. No `solve_ddwmr_case`, R3 `run_query`, matched worker, query 1, or 1,944-query batch was invoked.

## 7. Preservation and development corrections

The R4 candidate v5 remains unchanged at SHA-256 `735a36130916f4cbbc28924b3f937cd2a5acb70e4e78d28af5d46b5b959d66f4`; its source closure remains `33ec3437d55136117e9c322ce588458aa484060702e7fb46c579ccb47447762b`. The R6 builder revalidated every inherited R4 dependency hash. Candidate manifests v1–v5 remain present and their exact-byte digests are recorded in R6 manifest v6.

The R6 manifest also hashes the archived R5 composition manifest (`48196f1f3ebb5cf9787c68bc98f6ad88a0678ebd92683014fe877d015f18dd44`), pristine replay report (`66ff923d3fe037eae0a96f5a33381ff9a9a1994121cbd0232d0d1cb0c174e84f`), and v11 snapshot manifest (`d6ed85d98f630889912e30baaf00314ac4069c4dc846525c639832c64ff959eb`). It records all listed R5 source/profile hashes and `NO_R5_FILE_EDITED`. R3 archive selection, adapter fixture, and archived record are also hash-bound. New evidence was written to fresh numbered R6 directories; retry4/retry5 and earlier records were left in place.

The following implementation issues were encountered and corrected before selecting retry6:

- A preliminary fixture launch encountered an existing output root; subsequent runs used distinct numbered output paths. A stale retry4 path in the fixture guard was updated before final evidence generation.
- Retry1 hit CPython's default 4,300-digit integer-string conversion limit while serializing a valid archived rational. R6 now applies the profile-declared 10,000-digit limit; the arithmetic bit and operation caps did not change.
- Retry2 exposed that the historical R3 development profile does not carry the R6-only `internal_method_limits`. The fixture now reconstructs the archived query from the historical manifest while using the explicitly declared R6 candidate profile for adapter-cap accounting.
- Retry3's changed-scene mutation still referenced the pristine proof path through its receipt, so it was rejected at the delivery-path premise first. The fixture now recomputes the mutation artifact links and guard receipt, allowing the intended scene-binding premise to be exercised.
- A diagnostic showed common-record predicate payloads matched while `work` counters differed because replay parses inputs a second time. R6 now compares all non-work predicate fields exactly and checks stored work fields independently for schema, consistency, and declared caps.
- The manifest's inherited schema pointer was found to name the R4 schema. The final builder now points to the R6 schema; fixture and probe evidence were refreshed under the resulting closure.

Retry4 and retry5 had passed against earlier closure identities. Final selected evidence is retry6 and probe refresh3, bound to closure `56de9b89ed0d6bc0d4b46e88163b37e3254e61c4dbf2f95a306fcc8b83205c72`.

## 8. Review disposition

R6 closes the identified source-level proof-to-common composition gap on the two archived fixtures and exercises named artifact mutations. It is still a **review candidate**, not a final freeze and not evidence that a prospective matched worker completes within the method caps. The 1,944-query batch remains at **0/1,944**. No commit or push was made.

Independent review should inspect the R6 closure, verifier premises, R3 budget ownership, fixture report and guard, and the unchanged zero-query manifest before any separate decision about query 1 or batch start.
