Session: DDWMR | LUNA-G4-AUER

# G4 Auer R8 single-query preflight handoff

**Date:** 2026-10-03  
**Repository:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Branch / HEAD:** `main` / `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`  
**Assignment:** `docs/CODEX_TO_LUNA_G4_AUER_R8_SINGLE_QUERY_PREFLIGHT.md`  
**Review authorization:** `docs/reviews/CODEX_G4_AUER_PROTOCOL_V3_R8_SOURCE_REVIEW.md`  
**Candidate:** R8, manifest SHA-256 `263305153edd39b60110e1a275956391dd19da4ba2ee339c6cf53c4d31c3bb86`  
**Research disposition:** HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.

## Summary

The review authorizes exactly the first frozen ID for both Auer and R3, conditional on the pre-run hash-lock check. The preflight found five source-hash pins embedded in `validation/configs/g4_equal_resource_guard_v3_r8.json` that disagree with the current R8 source bytes and the source hashes in the R8 candidate manifest. The assignment says to stop with `NOT_RUN` if any hash differs. I therefore stopped before invoking either worker.

The other preflight checks passed: all **214/214** source-closure dependency hashes match; the protocol, candidate manifest, top-level profiles and ordered-ID digest match their candidate locks; and static in-memory input reconstruction produced the expected first-ID inputs. The guard profile file itself is byte-identical to its candidate-manifest entry, but its embedded worker, shared-binding, validator and launcher hashes do not describe the files in that locked tree.

**Execution outcome:** Auer `NOT_RUN`; R3 `NOT_RUN`; worker invocations **0**; matched-query evaluations **0**; producer invocations **0**; offline audit invocations **0**; new proofs **0**. The frozen comparison remains **0/1,944**. No batch, other ID, commit or push occurred. The R8 candidate and predecessor artifacts were not modified.

## Finding 1 — Embedded source hashes in the R8 external guard profile do not match the locked source tree

**Finding.** The top-level SHA-256 of the external guard profile is correctly bound, while five source hashes declared inside that profile disagree with the current source files.

**Evidence.** The profile at `validation/configs/g4_equal_resource_guard_v3_r8.json` hashes to `b2718f4b19dd01cfff929e1dbe449c2f19d00d03dc53f6d1d96ed6a3704b9a23`; that value matches the R8 manifest's `external_guard` entry and the closure dependency. Its embedded source-hash fields compare as follows:

| Profile field | Source path | Hash declared in profile | Current file hash / R8 manifest hash | Match |
|---|---|---|---|---|
| `worker_modules.auer.source_sha256` | `validation/g4/auer_matched_query_worker_v3_r8.py` | `f75646cb2cb0d6fbb064ce02257c9d0dbe5412095ebd83a05f231901796063c9` | `c81d80e58446107a429c3fbd76b1db514f790e5876b901632adc097da82569c2` | No |
| `worker_modules.r3.source_sha256` | `validation/g4/r3_matched_query_worker_v3_r8.py` | `5c6efc03b57de1115fa391b8a69b192756500b1a996853fe4a762a1af9cf4e61` | `b633344c2e76e42f80367d70599603b4fc90815b777c6ca7ce4d543e347c5f61` | No |
| `worker_modules.shared_binding.source_sha256` | `validation/g4/matched_worker_common_v3_r8.py` | `922b436e6eccccf9fb46c9d5f67fc63ac46462b6b057b3df83cdba2d38d52004` | `9331cc64b969bb05acae8de73f2e74458a98bc541420a65e5e388b662d0e1ca8` | No |
| `worker_modules.result_validator.source_sha256` | `validation/g4/validate_matched_result_v3_r8.py` | `fc52c866df453d5652117324ea7c421fd09ef9786c697bc994080015e2266ca6` | `5305cfb88e1e37c6a8491e4f9c3e6af248c919635712922d3ceb69e8bb250cf4` | No |
| `worker_launcher.source_sha256` | `validation/g4/run_matched_worker_guard_v3_r8.py` | `95e0d3b8396483f789784bb3565456344887ba01cab865cf8262d2a8e228eb5d` | `040709b0ea85c265b4cd07c12f594de19badb24bbea1bf728abc57aeef65da85` | No |

The embedded process-limiter hash does match: `a8d6edf16f092f15334ad94e715af3d9a3db5319c82b0488d5ddb1da50bc0a82`. The current source hashes in the last column agree with the R8 manifest and all matching closure dependency records.

**Consequence.** The profile's own identity is locked, but the source identities it declares are internally inconsistent with the R8 worker tree. The single-query assignment requires stopping on a hash discrepancy; running with this inconsistency would make the preflight's declared guard/source identity ambiguous.

**Status.** **PRE-RUN HASH-PIN BLOCKER. Both arms remain `NOT_RUN`.** No worker or producer was invoked.

**Required action.** Reconcile the embedded hashes in a new versioned guard profile/candidate, rebuild its source closure and manifest, and obtain the required review/authorization for that candidate before attempting the query. Preserve the current R8 candidate bytes and do not retroactively change its manifest.

## Finding 2 — Remaining exact-byte and query-input checks passed

**Finding.** The hash discrepancy is isolated to the source pins embedded in the guard profile; the current closure and other checked candidate identities match.

**Evidence.** A read-only preflight recomputed every dependency in `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R8.json`: **214 matched, 0 mismatched**. The closure SHA-256 is `37fde1b2ba705fe9e44eba101989035643aeb1c9fd0e4dc84d1eff288b2ca276`. Its transitive import audit SHA-256 is `99ef2ccdaa1f613fc37095460aca53fd8e8cba6688d7a09b30044d54962dbb37`, with 23 reachable local modules, 73 directed import edges and zero unresolved local imports.

The following candidate and input identities were checked:

| Artifact | SHA-256 |
|---|---|
| R8 protocol `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R8.md` | `bf4275f4f7530dff877ec512c6adc8c344313e0f74bba98367f6a2a6ecd0f06b` |
| R8 manifest `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v8.json` | `263305153edd39b60110e1a275956391dd19da4ba2ee339c6cf53c4d31c3bb86` |
| Auer profile `validation/configs/auer_g4_matched_profile_v3_r8.json` | `487e58395691ff6b6fe71c4e20189a3d9bcda214a2f889e8d1a1df94a7310f8e` |
| R3 profile `validation/configs/r3_g4_matched_profile_v3_r8.json` | `c0880b9308db4a6c7e1f66994bbcee63fa8dba8aec0fc582b1a083b3631205dd` |
| Common profile `validation/configs/g4_common_predicate_profile_v3_r8.json` | `9e6323ce9a11dda97db2e1aed686df2a5eeaacae719331868b2a0d95b94de04c` |
| External guard profile `validation/configs/g4_equal_resource_guard_v3_r8.json` | `b2718f4b19dd01cfff929e1dbe449c2f19d00d03dc53f6d1d96ed6a3704b9a23` |
| Benchmark `validation/configs/benchmark_v1.json` | `b2bc12cd578229cfb6df4b426f93e0f472d69f6be36929df93e797ff79396a9e` |
| Auer query manifest `results/validation/g4/auer2013/auer_matched_candidate_manifest_v2.json` | `77024610eab603a1ee2085feb5b6e7da0719ddd0641efa3804df6190492e59ad` |
| R3 prospective input inventory `research/benchmarks/G4_AUER_R3_PROSPECTIVE_INPUT_HASHES_v3_R8.json` | `d851ddafa37e7af8265a893cd338ad689432a63389fd2267a0a919d11fed8408` |

The candidate's ordered-ID digest was independently reconstructed from 1,944 unique IDs, LF-joined without a trailing LF: `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`. It matches the manifest. The first ID is `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`, as authorized by the review and assignment.

Static in-memory input reconstruction for that ID gave Auer method-input SHA-256 `b59dc0f4bd05bf277384387115e7138d6df6450c187d2eefd38cae577a474e94` and R3 method-input SHA-256 `4a9257d3d0b601cf599f9887eb88d0a8689a1ac0d691ce115aca50a347e41b35`. The R3 value matches the first row of the R8 prospective input inventory, whose row remains `NOT_RUN`. This reconstruction invoked neither method worker nor producer.

**Consequence.** The intended query and per-method inputs are reproducible, and candidate closure bytes are intact. The guard-profile source-pin mismatch still prevents satisfying the precondition to invoke either arm.

**Status.** **PASS for closure, candidate identity, ordered IDs and static input reconstruction; overall preflight STOP.**

**Required action.** Resolve Finding 1 before running either worker. Keep the current manifest byte-identical and the rest of the ID universe `NOT_RUN`.

## Finding 3 — Separate preflight record documents the stop

**Finding.** The conditional single-query authorization was recorded separately without modifying the candidate manifest.

**Evidence.** The versioned preflight evidence directory is:

`D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety\results\validation\g4\auer2013\protocol_v3_r8_single_query_preflight_v1\`

It contains:

| Record | SHA-256 | Contents |
|---|---|---|
| `preflight_hash_ledger.json` | `bb3c8554227425c8e50bc6a88b8673c3a8d625ffa2bc5398c8195b87244c014a` | All 214 dependency expected/actual hashes, candidate and input identities, ordered-ID check, static input reconstructions, and five profile pin mismatches. |
| `run_authorization_receipt.json` | `6143710f0a0341b9e52d7ea1e9a37b47fc0cdc65f828f29f043899646e550336` | Review/assignment references, first-ID scope, stop reason and zero execution counts. |

The receipt status is `STOP_NOT_RUN_PRECONDITION_HASH_PIN_MISMATCH`. Auer and R3 each record zero worker invocations. No method result, native proof, common record, worker guard receipt or composition audit was created. Candidate manifest SHA-256 remains `263305153edd39b60110e1a275956391dd19da4ba2ee339c6cf53c4d31c3bb86`.

**Consequence.** There is a separate exact-byte record of why the review-authorized preflight did not proceed. The candidate's historical `query_1_authorized=false` field remains unchanged; no execution authorization was recorded as consumed.

**Status.** **NOT_RUN before worker launch.** Matched comparison remains 0/1,944; batch remains unauthorized.

**Required action.** Codex should review the five profile-pin differences and issue a corrected versioned candidate/assignment before any query execution. After any future approval, run only the same first ID for both methods and stop for review.

## Commands and counts

The preflight ran read-only SHA-256/dependency checks, ordered-ID reconstruction, and static per-method input reconstruction through R8's `build_live_context`. It did **not** invoke `run_matched_worker_guard_v3_r8`, either method worker, either producer, or the composition-audit guard.

| Count | Result |
|---|---:|
| Closure dependencies checked | 214; 214 matched |
| Embedded guard-profile source hash pins checked | 6; 5 mismatched, 1 matched |
| Ordered IDs reconstructed | 1,944 unique; digest matched |
| Static method-input hashes reconstructed | 2; R3 also matched the frozen inventory |
| Auer matched-query worker invocations | 0 |
| R3 matched-query worker invocations | 0 |
| Producer / trajectory-proof invocations | 0 |
| Offline composition audits | 0 |
| Matched-query evaluations | 0 |
| Batch evaluations | 0 |

The runtime limits remain 120 seconds and 1 GiB per worker, Auer combined RHS/Jacobian cap 100,000, and R3 proof serialization cap 4,194,304 bytes. No resource-measurement process was started for the query.

## Final status for review

**The preflight stopped as required by the hash-check gate. Query 1 was not run for either method.** R8's focused source/fixture acceptance and one-query review authorization remain as recorded, but this execution attempt did not pass the profile-pin precondition. Batch remains **0/1,944**, and G4 remains UNVERIFIED.
