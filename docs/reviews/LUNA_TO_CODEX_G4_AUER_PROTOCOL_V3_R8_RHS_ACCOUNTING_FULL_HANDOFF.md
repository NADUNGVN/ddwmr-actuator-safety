# Full handoff — G4 Auer protocol v3 R8 RHS-accounting correction

**Session:** `LUNA-G4-AUER`  
**Date:** 2026-10-03  
**Repository:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Branch / HEAD:** `main` / `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`  
**Input blocker:** `docs/CODEX_TO_LUNA_G4_AUER_PROTOCOL_V3_R7_RHS_ACCOUNTING_BLOCKER.md`  
**Review addressed:** `docs/reviews/CODEX_G4_AUER_PROTOCOL_V3_R7_SOURCE_REVIEW.md`  
**Research disposition:** HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.

## Summary

Created and rebuilt the review candidate **R8** to correct successful Auer RHS/Jacobian replay accounting. Successful counts now come from the top-level fields returned by `replay_native_proof`; R8 checks exact nonnegative integer types, the producer-plus-replay sum, agreement with the seeded counter, and the 100,000-evaluation cap. The live audit still compares these corrected counts with the worker work vector.

The read-only archived-proof regression reports **4 producer + 4 replay = 8 combined**. Five successful-replay counter tamper cases were rejected. Existing at-cap and R3 4-MiB proof-serialization fixtures remain in the suite. The fixture suite reports 13/13 mutation rejections and zero producer calls, matched-query evaluations, or new proofs.

R8 has a rebuilt 214-dependency source closure and a refreshed manifest bound to the R8 fixture and memory-probe evidence. The static ordered query universe remains 1,944 unique IDs with the same digest as R7; every row is `NOT_RUN`. The candidate manifest records **0/1,944**, `query_1_authorized=false`, and `batch_start_authorized=false`.

**No query 1, matched query, or batch was run. No new trajectory proof was produced. No G3, controller, or hardware work was done. No commit or push was made.** R7 and earlier artifact bytes listed by the R8 preservation inventories were verified unchanged.

## Finding 1 — Successful Auer replay counts now use the returned top-level fields

**Finding.** R8 repairs the R7 mismatch between the successful replay result and the verifier's reported RHS/Jacobian work.

**Evidence.** In `validation/g4/verify_matched_composition_v3_r8.py` (SHA-256 `84b87b82c15a06057a0044ace329c79f2ffee51a3ada29e06ab4dd1ab3142a54`), `_validated_auer_rhs_replay_counts` reads `rhs_jacobian_replay_evaluations` and `rhs_jacobian_combined_count` from the successful replay object at the top level (lines 255–314). It requires exact nonnegative `int` values, so Boolean and numeric-string values fail; checks `combined == producer + replay`; checks agreement with the seeded mutable counter; and rejects totals above the frozen profile cap. `_replay_auer_envelope` seeds the counter with the producer's recorded count and writes the validated values into the reported work object (lines 317–373).

The live branch remains in `audit_artifact_bundle` (lines 539–552). It compares the worker vector's producer, replay, combined, and cap fields against the values reconstructed by the corrected replay path and raises `RESULT_RHS_ACCOUNTING_MISMATCH` on a difference.

**Consequence.** The R7 successful archived proof no longer reports replay 0 / combined 4 when replay actually used 4 evaluations. A future complete live result with 4 producer and 4 replay evaluations can be audited against 4/4/8.

**Status.** **R8 source correction present; independent Codex review pending.** The live equality branch is retained in source. This non-query archived-proof fixture does not invoke a matched worker; the fixture report explicitly records `live_worker_vector_equality_exercised=false`. Prospective live-result behavior therefore remains unverified.

**Required action.** Review the top-level field binding, exact-type checks, seeded-counter reconciliation, cap check, and live work-vector comparison before considering a final protocol freeze. Do not infer prospective worker behavior from the archived fixture.

## Finding 2 — Archived successful-proof regression and tamper coverage

**Finding.** The R8 non-query fixture exercises positive successful replay work and the reported combined count using the archived Auer proof.

**Evidence.** `validation/g4/protocol_v3_r8_composition_fixture.py` (SHA-256 `c3fc6ddf098d2b71b8f9a2d295b82b257117edf04516167ca5052a9d0299947b`, lines 460–517) asserts **producer 4 / replay 4 / combined 8** and confirms the replay's top-level fields are 4 and 8. The report records five rejected accounting mutations: missing replay count, Boolean count, negative count, numeric-string count, and wrong combined total. Each is rejected as `NATIVE_PROOF_RHS_ACCOUNTING_INVALID`.

The complete report is `results/validation/g4/auer2013/protocol_v3_r8_nonquery_contract_fixtures/composition_fixture_suite_report.json`, SHA-256 `4e684f6ad482faefb1f0dc5467003b7314ec3f299e2fa2e0428092acdbf66203`. It reports:

- Archived successful Auer replay: 4 producer / 4 offline replay / 8 combined; cap 100,000.
- Five successful-counter tamper cases rejected.
- The existing producer-at-cap boundary rejected at producer 100,000 / replay 0 / combined 100,000, before another RHS evaluation.
- The R3 archived serialization fixture retains the 4,194,304-byte proof cap and `RESOURCE_LIMIT` classification at its over-cap fixture boundary.
- The broader suite reports 13/13 mutation trials rejected, zero matched-query worker invocations, zero producer/IVP invocations, and zero new trajectory proofs.

The separate fixture guard sidecar `results/validation/g4/auer2013/protocol_v3_r8_fixture_guard/fixture_suite_guard.json` has SHA-256 `4e18630d8d3fa38ac2c8f6b666296f095eed4403e5e39bd79b201196a71a64a7`. It binds closure `37fde1b2ba705fe9e44eba101989035643aeb1c9fd0e4dc84d1eff288b2ca276`, reports PASS, zero producer/matched-query/batch calls, 4.375 seconds elapsed, and 54,120,448 bytes peak memory under its separate 600-second / 1-GiB fixture-process guard. These fixture resources are not charged to either method's matched worker measurement.

**Consequence.** The prior zero-replay fixture gap is covered by the archived positive-replay case. These are stored-proof and offline verifier results, not a new proof or a prospective matched-method result.

**Status.** **PASS for the recorded archived-proof/resource-contract fixture scope.** No query-level behavior is established.

**Required action.** Review the fixture report and guard sidecar alongside the source. Preserve the distinction between offline replay, method-worker measurements, and producer-generated proof evidence.

## Finding 3 — R3 proof-size cap and Auer combined cap remain bound

**Finding.** R8 carries forward the R3 finite proof-size contract and the Auer producer-plus-replay RHS/Jacobian cap.

**Evidence.** The R3 profile declares `max_serialized_proof_bytes=4,194,304` and the matching internal cap. The R8 worker reads and applies that value; the R8 result schema requires `proof_size_cap_bytes`; and the validator checks the result against the profile and the stored proof size. Verified identities:

| Artifact | SHA-256 |
|---|---|
| `validation/configs/r3_g4_matched_profile_v3_r8.json` | `c0880b9308db4a6c7e1f66994bbcee63fa8dba8aec0fc582b1a083b3631205dd` |
| `validation/g4/r3_matched_query_worker_v3_r8.py` | `b633344c2e76e42f80367d70599603b4fc90815b777c6ca7ce4d543e347c5f61` |
| `research/benchmarks/G4_AUER_MATCHED_QUERY_RESULT_v3_R8_SCHEMA.json` | `b074dd30f1de13e93f3d0dcf1932e0dbadbf41dac72a79a611182db0d7662008` |
| `validation/g4/validate_matched_result_v3_r8.py` | `5305cfb88e1e37c6a8491e4f9c3e6af248c919635712922d3ceb69e8bb250cf4` |

The R8 protocol and profile retain the **100,000 combined Auer RHS/Jacobian cap**. The fixture retains the at-cap stop case. Offline verifier resources remain separately guarded from method-worker timing and memory.

**Consequence.** The R7 correction does not remove the existing R3 serialization boundary or the Auer combined-cap boundary. Neither historical archive sizing nor a fixture proves that every future proof fits the cap.

**Status.** **Profile/source/schema/validator agreement and stored boundary fixtures verified in the R8 candidate.** Prospective proof sizing and query behavior remain unverified.

**Required action.** Include both resource boundaries in the independent review of R8; do not treat the archived fixture as a prospective size guarantee.

## Finding 4 — Fresh R8 memory-probe index binds the probe records to the R8 closure

**Finding.** The refreshed index binds both existing R8 worker memory-probe records to the exact R8 closure.

**Evidence.** `results/validation/g4/auer2013/protocol_v3_r8_guard_probes/probe_refresh_index.json` has SHA-256 `3e18d0c43e7d9ac93b8de8b782cd3e5206ed01bfc5884134105f256669377168` and closure SHA-256 `37fde1b2ba705fe9e44eba101989035643aeb1c9fd0e4dc84d1eff288b2ca276`. Each probe requested 256 MiB under a 64-MiB process cap and received `MemoryError`; both records show the cap installed and guard status PASS:

| Probe | Peak process memory | Limit | Record SHA-256 | Stdout SHA-256 |
|---|---:|---:|---|---|
| Auer | 66,387,968 B | 67,108,864 B | `2021e20461bcc1758ae0348ba4e6cbc21160c70e7fa2d82da7fa4010ff48cfa7` | `0df97e81a45efd33c99ee875c459aa067fdd3c8e298c70537609d756a514faf2` |
| R3 | 66,682,880 B | 67,108,864 B | `a29350c577605f1531fdb42d5fbdcc6ff252247efee917145df6c95de2ed248f` | `c4c9bc0b90bcc7ef88cf994d2ee87884f934c135fa8b151d7418a2e344612068` |

The probe records report zero matched-query invocations and zero batch evaluations. The refreshed index was generated from those existing R8 records and then bound into the rebuilt candidate; it is not a measurement of a matched query pipeline.

**Consequence.** These results verify the cap for the two memory-probe commands only. They do not measure prospective worker memory or execution time.

**Status.** **PASS for both 64-MiB memory-probe commands only.**

**Required action.** Preserve the memory-probe scope label when reviewing the manifest. Do not use these probe peaks as matched-query resource measurements.

## Finding 5 — R8 closure, candidate manifest, ordered universe, and preservation

**Finding.** The R8 closure, import audit, probe index, fixture evidence, and freeze candidate are hash-bound; the frozen 1,944-ID universe and all predecessor bytes remain intact.

**Evidence.**

| Artifact | SHA-256 |
|---|---|
| R8 protocol `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R8.md` | `bf4275f4f7530dff877ec512c6adc8c344313e0f74bba98367f6a2a6ecd0f06b` |
| R8 transitive import audit `research/benchmarks/G4_AUER_MATCHED_TRANSITIVE_IMPORT_AUDIT_v3_R8.json` | `99ef2ccdaa1f613fc37095460aca53fd8e8cba6688d7a09b30044d54962dbb37` |
| R8 source closure `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R8.json` | `37fde1b2ba705fe9e44eba101989035643aeb1c9fd0e4dc84d1eff288b2ca276` |
| R8 candidate manifest `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v8.json` | `263305153edd39b60110e1a275956391dd19da4ba2ee339c6cf53c4d31c3bb86` |
| Manifest sidecar `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v8.sha256` | `09e45e4020c764d70ea773ddf77586caf4fa1f41609e15928e1d6fc37650188f` |

The source closure contains **214 dependencies**; a post-build pass recomputed every dependency hash successfully. The transitive audit reports **23 reachable local modules, 73 directed import edges, and zero unresolved local imports**. The R8 manifest binds the closure, import audit, fixture report/guard, and probe index hashes.

The builder's frozen universe reconstruction and a post-build static check both found **1,944 unique ordered IDs** with ordered digest `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`, equal to R7's digest. The manifest records `1,944/1,944 NOT_RUN`; batch state is `matched_query_evaluations=0`, `one_query_worker_invocations=0`, `query_1_authorized=false`, `batch_start_authorized=false`, and `comparison_run=false`.

Post-build SHA checks matched all entries in the preservation inventories: R7 candidate **94/94**, R7 predecessor-closure dependencies **120/120**, R6 candidate **27/27**, R5 source candidate **14/14**, R5 evidence **3/3**, R4 evidence **4/4**, and R3 v5 fixture inputs **2/2**. R7's key identities remain:

| R7 artifact | SHA-256 |
|---|---|
| Protocol `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R7.md` | `b988838f52cc152878ec5edbeda7767fdfd05cc6bc4c768f4911d3f296cdd782` |
| Candidate manifest `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v7.json` | `181dfad5ef58088fb192449ff8ebb31546c41dfb57c2d8a3e0768f78511ddc82` |
| Source closure `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R7.json` | `48006dcd4d1e1491e4cade78cf1fff4e895cebf30400764cbf384459f8fdbf9f` |
| Import audit `research/benchmarks/G4_AUER_MATCHED_TRANSITIVE_IMPORT_AUDIT_v3_R7.json` | `287248f1fa45b3a28113bcd806e8b459ff8ee6cc5fc91c96e59f965dc7bf2b82` |
| R7 fixture report | `1a6b1c1a73bb103eba46ea1c27e3f3be7e0e7a1aa4f9b6644d69385ad2526d99` |
| R7 fixture guard | `0c3415ef10ebf1af0569af94dfeef3eda6b7f4001ab395a1a71474d26693b40d` |
| R7 probe index | `d3859b97860471d243992f5dbe9c75efd9841720700ff4fc2ef5bf9dc8868cf9` |

**Consequence.** The candidate has a reviewable exact-byte source boundary and the R7/R6/R5/R4/R3 artifacts listed in its inventories remain unchanged. This is a candidate identity and preservation result, not final-freeze acceptance or batch authorization.

**Status.** **R8_REVIEW_CANDIDATE_NOT_FINAL_FREEZE; MATCHED_BATCH_NOT_AUTHORIZED.**

**Required action.** Review the R8 source, evidence bindings, candidate manifest, and preservation inventories. Any query 1 or batch start requires a separate review/authorization; this handoff does not authorize it.

## Commands and execution boundary

Recorded guarded fixture invocation and child command:

```powershell
python -m validation.g4.run_matched_composition_audit_guard_v3_r8 --fixture-suite --stdout-output results/validation/g4/auer2013/protocol_v3_r8_fixture_guard/fixture_suite_stdout.log --guard-output results/validation/g4/auer2013/protocol_v3_r8_fixture_guard/fixture_suite_guard.json
C:\msys64\ucrt64\bin\python.exe -m validation.g4.protocol_v3_r8_composition_fixture
```

Recorded R8 memory-only guarded probe invocations:

```powershell
python -m validation.g4.run_matched_worker_guard_v3_r8 --method auer --probe --probe-limit-mib 64 --probe-allocation-mib 256 --stdout-output results/validation/g4/auer2013/protocol_v3_r8_guard_probes/auer_worker_memory_probe_stdout.log --guard-output results/validation/g4/auer2013/protocol_v3_r8_guard_probes/auer_worker_memory_probe.json
python -m validation.g4.run_matched_worker_guard_v3_r8 --method r3 --probe --probe-limit-mib 64 --probe-allocation-mib 256 --stdout-output results/validation/g4/auer2013/protocol_v3_r8_guard_probes/r3_worker_memory_probe_stdout.log --guard-output results/validation/g4/auer2013/protocol_v3_r8_guard_probes/r3_worker_memory_probe.json
```

The child worker commands recorded in the probe JSON files were:

```powershell
C:\msys64\ucrt64\bin\python.exe -m validation.g4.auer_matched_query_worker_v3_r8 --memory-probe-mib 256
C:\msys64\ucrt64\bin\python.exe -m validation.g4.r3_matched_query_worker_v3_r8 --memory-probe-mib 256
```

After deriving the probe index from the two existing probe records, rebuilt the candidate with:

```powershell
C:\msys64\ucrt64\bin\python.exe -m validation.scripts.build_g4_auer_v3_r8_candidate
```

The builder reported 214 closure dependencies, 23 reachable modules, 73 import edges, zero unresolved imports, 1,944 matched IDs, zero matched-query evaluations, all rows `NOT_RUN`, and `query_1_authorized=false`. A separate post-build check recomputed dependency and predecessor hashes, compared the R7/R8 ordered-ID digests, and checked the evidence bindings. Those checks enumerate the frozen IDs only; they do not call a matched query worker.

## Final status for Codex review

R8 corrects the reviewed R7 successful-replay accounting defect and supplies archived-proof evidence for positive replay work **4/4/8** plus five malformed/tampered successful-counter rejections. The retained live result-vector check uses those corrected counts, but no live matched worker was invoked. The candidate and all evidence remain review-only. **Batch remains 0/1,944; query 1 was not run or authorized.**
