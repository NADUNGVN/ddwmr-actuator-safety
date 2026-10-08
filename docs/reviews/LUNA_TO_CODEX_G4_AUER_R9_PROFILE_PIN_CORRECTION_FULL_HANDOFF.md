Session: DDWMR | LUNA-G4-AUER

# G4 Auer R9 profile-pin correction — full handoff

**Date:** 2026-10-03  
**Repository:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Assignment:** `docs/CODEX_TO_LUNA_G4_AUER_R9_PROFILE_PIN_CORRECTION.md`  
**R8 review:** `docs/reviews/CODEX_G4_AUER_PROTOCOL_V3_R8_SOURCE_REVIEW.md`  
**R8 preflight review:** `docs/reviews/CODEX_G4_AUER_R8_SINGLE_QUERY_PREFLIGHT_REVIEW.md`  
**R9 candidate manifest:** `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v9.json`  
**Manifest SHA-256:** `db0df35c634b91df0e498819d1480ee18c694608b2b68538a0580044132c74d8`  
**Research disposition:** HOLD; G1 restricted reduced-model PASS; G2/G3/G4 and physical correspondence UNVERIFIED.

## Summary

R9 repairs the six active R8 profile pins identified by Codex and adds a recursive fail-closed checker for active profile path/hash assertions. The checker runs in the R9 builder and at the start of the R9 worker-guard preflight, before that launcher can create a matched-query worker. The completed independent read-only integrity report passes all **8/8** local/runtime path/hash pairs across the four profiles and separately validates the R3 semantic specification-bundle digest. It reports zero hash mismatches, duplicate assertions, missing files, malformed digests, closure mismatches, or manifest mismatches.

The R8 control run with the same checker detected the six stale pins: **6 mismatches out of 8 pairs**, with the process-limiter and CPython executable pairs matching. Synthetic fail-closed probes also confirmed rejection of duplicate targets, missing targets, malformed digests, and a well-formed but incorrect digest.

R9 preserves the exact 1,944-ID order and digest. Every candidate row remains `NOT_RUN`; `comparison_run=false`, matched evaluations `0`, `query_1_authorized=false`, and `batch_start_authorized=false`. **No first query, matched-query worker, producer, or batch was run.** Only two isolated memory-limit probe commands and the read-only archived-proof fixture suite ran. No commit or push occurred.

## Finding 1 — Six stale profile pins corrected

**Finding.** All six R8 mismatches were copied forward into versioned R9 files and replaced with hashes computed from the exact named R9 files after the versioned source copies were finalized.

**Evidence.** The R8 declaration and named-file values below reproduce the Codex R8 source review. The last column is the matching R9 declaration and exact current R9 file SHA-256.

| Pin | R8 declared SHA-256 (stale) | R8 named-file SHA-256 | R9 target path | R9 declared = actual SHA-256 |
|---|---|---|---|---|
| Auer versioned solver | `4add47d63ddfb513f3a59038a948ccf60fed4783caea18990d284bf149c1766d` | `9ec23ccfe59b8e08ea54061a20f50501dd35a1a136c561347d38ff0ae5e56717` | `validation/baselines/auer2013/residual_ivp_g4_matched_v3_r9.py` | `a72b3dd3af804d24c6edbaa023b4ef528cd276345752454eedece9d234650df9` |
| Auer worker | `f75646cb2cb0d6fbb064ce02257c9d0dbe5412095ebd83a05f231901796063c9` | `c81d80e58446107a429c3fbd76b1db514f790e5876b901632adc097da82569c2` | `validation/g4/auer_matched_query_worker_v3_r9.py` | `60b71504c044309fd83a54cfb7c81c75e265ceaa7acd4414beef820006706e24` |
| R3 worker | `5c6efc03b57de1115fa391b8a69b192756500b1a996853fe4a762a1af9cf4e61` | `b633344c2e76e42f80367d70599603b4fc90815b777c6ca7ce4d543e347c5f61` | `validation/g4/r3_matched_query_worker_v3_r9.py` | `37abd9b980bc60424c51c7eb8832b2846b2b42b747946de5696de982f17af6f3` |
| Shared binding | `922b436e6eccccf9fb46c9d5f67fc63ac46462b6b057b3df83cdba2d38d52004` | `9331cc64b969bb05acae8de73f2e74458a98bc541420a65e5e388b662d0e1ca8` | `validation/g4/matched_worker_common_v3_r9.py` | `2e7ea726adadb7cae43ce9ff5df366802c2cf55a1ea2ee5e8e097be973faad79` |
| Result validator | `fc52c866df453d5652117324ea7c421fd09ef9786c697bc994080015e2266ca6` | `5305cfb88e1e37c6a8491e4f9c3e6af248c919635712922d3ceb69e8bb250cf4` | `validation/g4/validate_matched_result_v3_r9.py` | `021bdae6b3a103ce6b68954c40797dff7e8270540e08b00e0052f02817de5614` |
| Worker launcher | `95e0d3b8396483f789784bb3565456344887ba01cab865cf8262d2a8e228eb5d` | `040709b0ea85c265b4cd07c12f594de19badb24bbea1bf728abc57aeef65da85` | `validation/g4/run_matched_worker_guard_v3_r9.py` | `d26347b587d76d37fadccbffd459411ab45f862a89714d7a35e3e22a7fb32a94` |

The remaining active guard pairs were checked without changing their declarations:

| Pair | Path | SHA-256 | Result |
|---|---|---|---|
| Process limiter | `validation/baselines/auer2013/process_limiter.py` | `a8d6edf16f092f15334ad94e715af3d9a3db5319c82b0488d5ddb1da50bc0a82` | Match |
| Pinned CPython runtime | `C:\msys64\ucrt64\bin\python.exe` | `b5c33df60c2a8421dcf8117a67e848436b5d395c71ec1c0dfd96bad10f441d7f` | Match |

The R3 profile's `specification_bundle_sha256` is a semantic digest rather than a path/hash pair. It remains `84b444d0be6e18c946697c3b95662ffd0f30dd228ae7ca5e742cee47d446c850`, matching the R3 development manifest, specification-content ledger, and an independent recomputation of the ledger's semantic digest.

**Consequence.** R9 profiles now name the exact worker, solver, shared binding, validator, launcher, limiter and runtime bytes used by the candidate. The old R8 declarations remain untouched as historical stop evidence.

**Status.** **PASS — six corrected; two unchanged active pairs matched; one semantic R3 digest matched.**

**Required action.** Codex should review the versioned profile and candidate bindings before issuing any later query authorization.

## Finding 2 — Builder and preflight reject inconsistent active pins

**Finding.** The R9 builder runs the recursive profile-pin audit before generating its source closure and fails if any discovered pin is malformed or inconsistent. The R9 worker guard invokes the same checker against the final candidate manifest and source closure before any normal worker launch.

**Evidence.** The checker is `validation/g4/check_active_profile_pins_v3_r9.py`, SHA-256 `4e355900a2986db9be8475afe41cdc6c4fb8ef41a3542a7ef82e116bedba7cdd`. It recursively discovers fields ending in `_sha256`, requires their path companion, and validates the target file, exact digest, unique closure dependency, and candidate-manifest identity. It rejects duplicate JSON keys while parsing; repeated assertions/targets, missing files, malformed SHA-256 values, and mismatches fail closed. The R3 semantic digest is audited separately.

The machine-readable active-pin ledger is `results/validation/g4/auer2013/protocol_v3_r9_active_pin_integrity/active_pin_ledger.json`, SHA-256 `bf57c8893912f01a785ca977a266ad2ef584786f828007dfd1147a59ca4a271c`. It records 4 profiles, 8 active path/hash pairs, 1 non-path semantic digest, 0 mismatches, 0 duplicates, 0 missing files, and 0 malformed hashes.

The read-only final integrity report is `results/validation/g4/auer2013/protocol_v3_r9_active_pin_integrity/final_integrity_report.json`, SHA-256 `f3a36fb4cf0ce841a8a7b83baad06f5c8043578cd831381b3b88fd39010cf367`. It independently checked each profile and its closure/manifest identities against candidate manifest SHA-256 `db0df35c634b91df0e498819d1480ee18c694608b2b68538a0580044132c74d8`; result **PASS**, 8 matched, 0 mismatches, 0 duplicate assertions, 0 missing files, 0 malformed hashes, 0 closure mismatches, and 0 manifest mismatches. The report also confirms the R3 semantic digest.

As an R8 defect control, the same final checker scanned the preserved R8 profiles, closure and manifest. `results/validation/g4/auer2013/protocol_v3_r9_active_pin_integrity/r8_known_defect_control_final.json` (SHA-256 `3f573944a05e5c06d6cdfd2840210630b22d9d883b1981e153568ab4cfd44e86`) records 8 checked pairs, 6 file/closure/manifest pin mismatches, 0 duplicates, 0 missing files, and 0 malformed hashes. The two matches are the limiter and runtime. This control did not modify R8.

Four temporary, in-memory checker behavior probes returned `FAIL` as required: duplicate target (duplicate count 1), missing target (missing count 1), malformed digest (malformed count 1), and wrong but well-formed digest (mismatch count 1). These probes created no repository artifacts and invoked no worker or producer.

**Consequence.** A hash-locked profile with a false internal assertion can no longer pass the R9 build or worker preflight on the strength of its outer profile hash alone.

**Status.** **PASS — R8 defect reproduced; R9 checker, builder gate, preflight gate, and final read-only check agree.**

**Required action.** Keep the active-pin checker in the exact R9 closure and use the R9 worker guard's preflight gate after any future review authorization.

## Finding 3 — R9 source closure, import audit and candidate are internally bound

**Finding.** The review-only R9 candidate is rebuilt from the preserved R8 closure and manifest, with exact-byte identities for the versioned sources, profiles, pin checker, pin ledger, predecessor evidence and prospective R3 input inventory.

**Evidence.**

| Artifact | Repository path | SHA-256 |
|---|---|---|
| Protocol | `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R9.md` | `de478993faa57d917e00cf8ba865cb72ab8e70de93755eb4efd9ab50e0b10af3` |
| Result schema | `research/benchmarks/G4_AUER_MATCHED_QUERY_RESULT_v3_R9_SCHEMA.json` | `e87df40882547390edde138cf567e367ecffb87edfbdd7483c9d957e62db9a5f` |
| Auer profile | `validation/configs/auer_g4_matched_profile_v3_r9.json` | `9a08ccdadcbc1e8d51376fa9bd402a2a66f39ed5df7338314e0a1c8a6c37864e` |
| R3 profile | `validation/configs/r3_g4_matched_profile_v3_r9.json` | `13b632073c0bf8e5894d54e72fffb119961626d340517592723b829711d57863` |
| Common-predicate profile | `validation/configs/g4_common_predicate_profile_v3_r9.json` | `35731201512145219327ea862ffc7ef37c5a100f66740cde80dcdc5eb021adfe` |
| External guard profile | `validation/configs/g4_equal_resource_guard_v3_r9.json` | `840e83b8251ad2cc447dd31105d748463cf0149e4c4c3776b6f0648be87f0f50` |
| Auer solver | `validation/baselines/auer2013/residual_ivp_g4_matched_v3_r9.py` | `a72b3dd3af804d24c6edbaa023b4ef528cd276345752454eedece9d234650df9` |
| Auer worker | `validation/g4/auer_matched_query_worker_v3_r9.py` | `60b71504c044309fd83a54cfb7c81c75e265ceaa7acd4414beef820006706e24` |
| R3 worker | `validation/g4/r3_matched_query_worker_v3_r9.py` | `37abd9b980bc60424c51c7eb8832b2846b2b42b747946de5696de982f17af6f3` |
| Shared binding | `validation/g4/matched_worker_common_v3_r9.py` | `2e7ea726adadb7cae43ce9ff5df366802c2cf55a1ea2ee5e8e097be973faad79` |
| Worker launcher | `validation/g4/run_matched_worker_guard_v3_r9.py` | `d26347b587d76d37fadccbffd459411ab45f862a89714d7a35e3e22a7fb32a94` |
| Result validator | `validation/g4/validate_matched_result_v3_r9.py` | `021bdae6b3a103ce6b68954c40797dff7e8270540e08b00e0052f02817de5614` |
| Common-record replay | `validation/g4/replay_common_check_record_v3_r9.py` | `747e79ab85fde88ca6071156cfac7a19bb257eab430b6de25e7254cb2cbee45c` |
| Composition verifier | `validation/g4/verify_matched_composition_v3_r9.py` | `336ef1504353e6b82287be43888fe612b1ecff18fefd179f038fbaa8a23bbdc9` |
| Separate audit guard | `validation/g4/run_matched_composition_audit_guard_v3_r9.py` | `3607343bfc5568cc249542673306a919556c05274399a6a24b070a291da5210d` |
| Archived fixture runner | `validation/g4/protocol_v3_r9_composition_fixture.py` | `0dcf873653f21d837ac76d5114f79bcd08b1eabf1cd0c3861615d6754453cede` |
| R9 candidate builder | `validation/scripts/build_g4_auer_v3_r9_candidate.py` | `be3e9c8f4c2e035486b33557888bdf0aa7e0b3b4f8acbc2d2cf4d8863f8085ba` |
| Active-pin checker | `validation/g4/check_active_profile_pins_v3_r9.py` | `4e355900a2986db9be8475afe41cdc6c4fb8ef41a3542a7ef82e116bedba7cdd` |
| Transitive import audit | `research/benchmarks/G4_AUER_MATCHED_TRANSITIVE_IMPORT_AUDIT_v3_R9.json` | `163e94ea6485ebf0cf96ad08ff57e4cdf36d6b9663ac161d5b80573cd5540b07` |
| Source closure | `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R9.json` | `7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533` |
| Prospective R3 input inventory | `research/benchmarks/G4_AUER_R3_PROSPECTIVE_INPUT_HASHES_v3_R9.json` | `a78d730dedc95058463dad31d3bacbdc7ad73eccd94dba420908fb21f77ab840` |
| Candidate manifest | `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v9.json` | `db0df35c634b91df0e498819d1480ee18c694608b2b68538a0580044132c74d8` |
| Manifest sidecar file | `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v9.sha256` | `c335e0daf4bcae5a6c9a9698bc92d5e32c052191b64634280581e1b3f4d5e1dc` |

The source closure contains **316 dependencies**, all of whose current file hashes were recomputed with zero mismatch. The recursive import audit covers **24 reachable local modules**, **77 directed import edges**, and **0 unresolved local imports**. The manifest sidecar's recorded digest equals the candidate manifest SHA-256 above.

Focused R8-to-R9 source comparison normalized the version labels. The R9 solver, Auer worker, R3 worker, shared binding, result validator, common-record replay, composition verifier, audit guard and archived-fixture runner then matched their R8 source text byte-for-byte. The R9 worker launcher adds the active-pin preflight gate; the new checker implements that gate. No producer, replay, plant, method, predicate, query-universe or resource-cap formula was changed. The six pin values are the profile metadata correction.

The source ID digest remains `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`. The first ID remains `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`. The R9 candidate records **1,944/1,944 `NOT_RUN`**, zero matched evaluations, `comparison_run=false`, `query_1_authorized=false`, and `batch_start_authorized=false`. The prospective R3 inventory has 1,944 `NOT_RUN` rows and zero `run_query` or producer calls.

**Consequence.** R9 has a reviewable exact-byte candidate identity, a closed local-import inventory, and rebuilt prospective method-input hashes. Its manifest remains an unexecuted candidate.

**Status.** **PASS for source and static binding identity; no matched comparison has run.**

**Required action.** Review the exact R9 manifest and its active-pin ledger together. R8's prior conditional query authorization does not transfer to R9.

## Finding 4 — First-ID static input bindings rebuilt without executing the query

**Finding.** Both methods' first-ID inputs were reconstructed in memory using the finalized R9 profiles and closure. The run-time proof/source binding hashes are explicitly distinguished from the canonical method-input hash.

**Evidence.**

| Field | R8 static value | R9 static value |
|---|---|---|
| First ordered query ID | `state_low_neg__scene_d020_l-200__T_020__V_m1_m1` | `state_low_neg__scene_d020_l-200__T_020__V_m1_m1` |
| Source closure SHA-256 | `37fde1b2ba705fe9e44eba101989035643aeb1c9fd0e4dc84d1eff288b2ca276` | `7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533` |
| Auer profile SHA-256 | `487e58395691ff6b6fe71c4e20189a3d9bcda214a2f889e8d1a1df94a7310f8e` | `9a08ccdadcbc1e8d51376fa9bd402a2a66f39ed5df7338314e0a1c8a6c37864e` |
| Auer canonical method-input SHA-256 | `b59dc0f4bd05bf277384387115e7138d6df6450c187d2eefd38cae577a474e94` | `b59dc0f4bd05bf277384387115e7138d6df6450c187d2eefd38cae577a474e94` |
| R3 profile SHA-256 | `c0880b9308db4a6c7e1f66994bbcee63fa8dba8aec0fc582b1a083b3631205dd` | `13b632073c0bf8e5894d54e72fffb119961626d340517592723b829711d57863` |
| R3 canonical method-input SHA-256 | `4a9257d3d0b601cf599f9887eb88d0a8689a1ac0d691ce115aca50a347e41b35` | `da25e1e32521792d576a6614f8f6ae6f595ba7aead7d15343aea51817504baf6` |

The Auer canonical input hash remains unchanged because the frozen input record is unchanged. Its separately reconstructed native proof binding now declares the R9 Auer profile hash `9a08ccdadcbc1e8d51376fa9bd402a2a66f39ed5df7338314e0a1c8a6c37864e` and `source_snapshot_manifest_sha256=7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533`, along with R9 solver hash `a72b3dd3af804d24c6edbaa023b4ef528cd276345752454eedece9d234650df9`. The R3 reconstruction uses the R9 profile and records the R9 closure, unchanged R3 development-manifest semantic hash `e5c796fcfe8275b1b7106f112813d24b36d18626400ba149f29f4bee7b9c155d`, and unchanged benchmark semantic hash `21632e1eebf58a5d7fea14224254738d0ff11ba689b94343afa47adbccea166b`. The first R3 inventory row exactly matches the in-memory R3 reconstruction.

These are static query-input/provenance reconstructions only. No query worker, method producer, native replay, or query evaluation was invoked by this step.

**Consequence.** The changed R9 profile and closure identities are accounted for in both methods' static provenance. The R3 method input is rebuilt under the R9 profile; the unchanged Auer canonical input remains bound to the new profile/closure through its separate proof binding.

**Status.** **PASS — static bindings reconstructed; first query remains `NOT_RUN`.**

**Required action.** If a later review authorizes the first query, re-run the exact-byte lock and static binding checks immediately before execution.

## Finding 5 — Non-query archived fixtures and memory-only probes refreshed under R9

**Finding.** Archived-proof composition and resource-boundary fixtures were refreshed against the R9 source closure. Two bounded memory-only commands exercised the R9 guard's memory enforcement. These records are not prospective worker measurements.

**Evidence.**

| Evidence | Path | SHA-256 | Recorded result |
|---|---|---|---|
| Archived composition/contract fixture report | `results/validation/g4/auer2013/protocol_v3_r9_nonquery_contract_fixtures/composition_fixture_suite_report.json` | `6719b6ea139301cd24a811f3b7e4e402fe2625e08ef16b363935c01d6e9508b4` | PASS; 13 mutation rejections |
| Fixture Job Object guard | `results/validation/g4/auer2013/protocol_v3_r9_fixture_guard/fixture_suite_guard.json` | `c060b11a434706514cd0e98985907e40f4e74e03f9bf731ffd8f88790fd4c983` | PASS; bound to R9 closure; 600-second / 1-GiB separate fixture cap |
| R9 probe refresh index | `results/validation/g4/auer2013/protocol_v3_r9_guard_probes/probe_refresh_index.json` | `c84076cc3a8f443ad8df8c3e2760bf11afad3c322337f5366313ca4819384e95` | PASS for both 64-MiB memory-probe commands only |
| Auer memory-probe record | `results/validation/g4/auer2013/protocol_v3_r9_guard_probes/auer_worker_memory_probe.json` | `aceb7d1acd483cb504a42b47e8fcd71252131a8896a18b392a726bbbf9d84bc6` | PASS; 66,531,328-byte peak under 67,108,864-byte cap |
| R3 memory-probe record | `results/validation/g4/auer2013/protocol_v3_r9_guard_probes/r3_worker_memory_probe.json` | `387cdec4a2971df9916a2fac65fcd368a7127406beedff5b8cd3679cbc30172d` | PASS; 66,543,616-byte peak under 67,108,864-byte cap |

The fixture suite reused stored historical Auer/R3 proof artifacts; it invoked no producer, generated no new trajectory proof, and performed zero matched-query evaluations. Its separate Job Object cap was 600 seconds and 1 GiB; observed fixture wall time was 3.375 seconds and peak process memory was 53,092,352 bytes. The two memory probes each requested 256 MiB under a 64-MiB Job Object cap and correctly stopped allocation with `MemoryError`; these test enforcement for probe commands only. They are not query wall-time, memory, proof-size, or performance measurements.

Unchanged prospective limits are: Auer combined producer plus native-replay RHS/Jacobian cap **100,000**; R3 serialized-proof cap **4,194,304 bytes**; and each method's worker guard **120 seconds / 1,073,741,824 bytes**. No cap was raised.

**Consequence.** R9 has refreshed non-query evidence for archived composition and confirms probe-command memory-cap enforcement. Prospective live worker behavior, matched performance and live worker-vector equality remain unmeasured.

**Status.** **PASS within the stated archived-fixture and memory-probe scope only.**

**Required action.** Do not use these fixture/probe values as matched-query or method-performance results.

## Finding 6 — R8 and R7 historical artifacts preserved

**Finding.** R8 and predecessor files remain byte-identical. The R9 builder checks the reviewed R8 closure and manifest identities, verifies each R8 dependency, and records exact hashes for the preserved R8 candidate/evidence set.

**Evidence.**

| Preserved artifact identity | SHA-256 |
|---|---|
| R7 source closure `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R7.json` | `48006dcd4d1e1491e4cade78cf1fff4e895cebf30400764cbf384459f8fdbf9f` |
| R7 candidate manifest `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v7.json` | `181dfad5ef58088fb192449ff8ebb31546c41dfb57c2d8a3e0768f78511ddc82` |
| R8 source closure `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R8.json` | `37fde1b2ba705fe9e44eba101989035643aeb1c9fd0e4dc84d1eff288b2ca276` |
| R8 candidate manifest `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v8.json` | `263305153edd39b60110e1a275956391dd19da4ba2ee339c6cf53c4d31c3bb86` |
| R8 stopped-preflight ledger `results/validation/g4/auer2013/protocol_v3_r8_single_query_preflight_v1/preflight_hash_ledger.json` | `bb3c8554227425c8e50bc6a88b8673c3a8d625ffa2bc5398c8195b87244c014a` |
| R8 stopped-preflight receipt `results/validation/g4/auer2013/protocol_v3_r8_single_query_preflight_v1/run_authorization_receipt.json` | `6143710f0a0341b9e52d7ea1e9a37b47fc0cdc65f828f29f043899646e550336` |

The R9 candidate preservation ledger at `historical_evidence_preservation.r8_candidate_and_evidence_preserved_without_modification` contains **294 path/hash records**. All 294 current files matched their recorded hashes. The SHA-256 of the sorted `path<TAB>sha256` lines, LF-separated without a trailing LF, is `46d8aba7f7411277bbb5a0a4e899d9e1a98fe55da368db38b0eb8d8e9cdd0238`. The ledger includes the R8 closure dependencies, R8 source/protocol/profile/manifest files, R8 archived fixtures, R8 memory probes, and the stopped-preflight ledger and receipt. The existing R8/R7 source evidence was not regenerated or edited.

**Consequence.** R9 is a separate candidate with a traceable predecessor chain. The R8 stop remains valid evidence that its conditional single-query authorization was not consumed.

**Status.** **PASS — 294/294 R8 preservation hashes match; R7/R8 closure and manifest identities match their reviewed values.**

**Required action.** Keep predecessor candidates and receipts immutable during Codex review.

## Final disposition and review recommendation

**Finding.** The six stale pins are corrected; all discovered active path/hash assertions pass against current bytes, closure and candidate manifest; source closure/import audit and prospective static bindings are rebuilt; query execution remains absent.

**Evidence.** R9 manifest SHA-256 is `db0df35c634b91df0e498819d1480ee18c694608b2b68538a0580044132c74d8`; source closure SHA-256 is `7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533`; the final read-only report is PASS; all 1,944 rows are `NOT_RUN`; query 1 and batch authorization are false; matched evaluation count is zero.

**Consequence.** R9 is ready for independent Codex source/provenance review as a candidate. The prior R8 conditional authorization does not apply to R9.

**Status.** **GO for Codex review of a possible later single-query preflight. NO-GO for query 1 or the 1,944-query batch under this assignment.**

**Required action.** Codex should review R9 and issue a separate explicit decision before any query execution. No query, batch, commit, or push was performed by this session.

### Tóm tắt chuyển giao

R9 đã sửa đủ sáu pin cũ. Checker độc lập đối chiếu 8/8 cặp path/hash và semantic hash R3, tất cả đều PASS; control trên R8 tái hiện đúng sáu lỗi. Candidate khóa 316 dependency, import audit 24 module/77 cạnh, giữ toàn bộ 1.944 query ở `NOT_RUN`. Fixture chứng cứ lưu trữ và hai probe bộ nhớ đều PASS trong phạm vi phi-query. **Chưa chạy query đầu tiên hoặc batch; batch vẫn 0/1.944.** Đề nghị Codex review ứng viên R9 rồi ra quyết định riêng trước mọi lần chạy.
