# Full handoff — G4 Auer protocol v3 R7 profile corrections

**Session:** `LUNA-G4-AUER`  
**Separate shared-tree session:** `LUNA-G2-SCOPE`  
**Date:** 2026-10-02  
**Repository:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Branch / HEAD:** `main` / `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`  
**Input handoff:** `docs/CODEX_TO_LUNA_G4_AUER_PROTOCOL_V3_R6_PROFILE_BLOCKER.md`  
**Review addressed:** `docs/reviews/CODEX_G4_AUER_PROTOCOL_V3_R6_SOURCE_REVIEW.md`

**Research state:** HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED. This is a review candidate. The matched comparison remains **0/1,944**; query 1, batch start, G3, controller, and hardware work remain unauthorized. No commit or push was made.

## Summary

Created versioned R7 artifacts to address both R6 blockers: the R3 worker now has a frozen finite serialized-proof cap, and the offline Auer verifier now applies the combined producer-plus-native-replay RHS/Jacobian cap. Archived-proof/resource-contract fixtures and fresh memory-only probes pass against the R7 source closure. The candidate manifest was rebuilt and binds these artifacts. R6 and prior R5 evidence remain byte-identical.

No matched query, producer invocation, or trajectory proof was run or created in this turn. The R7 fixture uses the previously archived Auer proof and R3 record. The 64-MiB probes invoke only each worker's memory-probe command.

## Finding 1 — R3 serialized-proof cap

**Finding.** R7 declares and consistently applies a finite R3 native-proof serialization cap of **4,194,304 bytes (4 MiB)**.

**Evidence.** The rationale and contract are in `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R7.md` (§2; SHA-256 `b988838f52cc152878ec5edbeda7767fdfd05cc6bc4c768f4911d3f296cdd782`) and `validation/configs/r3_g4_matched_profile_v3_r7.json` (SHA-256 `4ba1d2527eca48846933d51068202a985a3947f20ca716b6a3229a8abbb573da`). The historical JSONL gzip archive contains 1,728 records; the largest JSON payload is 93,663 bytes (93,664 bytes including its LF delimiter). The cap is about 44.8 times the largest payload and 0.390625% of the unchanged 1-GiB process-commit limit. The archive is sizing evidence only and does not bound future proof sizes.

`validation/g4/r3_matched_query_worker_v3_r7.py` (SHA-256 `4e218bc7dd813be9e07d290f508ae7e2215caf27a4844e72dea675b56e7b793a`) reads and validates the top-level cap before producer execution, requires its internal profile cap to match, places the cap in the result/work vector, and passes it to the shared bounded serializer. `OutputSizeLimitError` is classified as `RESOURCE_LIMIT`; attempted bytes are retained and an over-limit proof is not written. The R7 schema requires `proof_size_cap_bytes` (SHA-256 `732f49f79df90b9fea1b75926c4dccc091cfe481b3de8c592445efb66eeda1f8`); the validator binds it to the selected profile and checks complete-proof byte length and cap-stop classification (validator SHA-256 `cc38cf85d06eee3ca2621b894982fbd56d233f329ebe2e15c4943ee8ed8982c9`). The offline verifier checks the same cap against the result and stored proof bytes.

The builder's AST audit enumerated literal profile reads in both R7 worker paths and reports that each selected profile supplies every read key, with no unresolved dynamic keys. The non-query fixture exercised the production R3 serialization helper on a stored historical record: a 120,847-byte copy fits the 4-MiB cap; a fixture cap of 120,846 bytes causes a 120,847-byte attempt to return `RESOURCE_LIMIT` without writing the over-limit artifact. It reports `PASS_PROFILE_LOOKUP_AND_RESOURCE_LIMIT_CLASSIFICATION`, zero producer/IVP calls, zero `run_query` calls, and zero new trajectory proofs.

Fixture report SHA-256: `1a6b1c1a73bb103eba46ea1c27e3f3be7e0e7a1aa4f9b6644d69385ad2526d99`. Guard sidecar SHA-256: `0c3415ef10ebf1af0569af94dfeef3eda6b7f4001ab395a1a71474d26693b40d`; it reports PASS, binds closure `48006dcd4d1e1491e4cade78cf1fff4e895cebf30400764cbf384459f8fdbf9f`, and records zero producer and matched-worker invocations.

**Consequence.** The deterministic missing-profile-key path identified in R6 is addressed in the R7 source candidate. The cap boundary and classification have stored-data fixture coverage. No prospective R3 query has yet demonstrated that a generated proof fits the cap.

**Status.** **R7 source/profile contract and non-query boundary fixture PASS; independent review and prospective query behavior PENDING.**

**Required action.** Review the 4-MiB rationale, serializer's byte-count boundary, failure-result fields, and profile/schema/validator agreement before considering any query authorization.

## Finding 2 — Auer combined RHS/Jacobian cap in offline verification

**Finding.** The R7 read-only Auer verifier starts replay accounting at the producer's recorded RHS/Jacobian count and checks the frozen **100,000 combined cap**.

**Evidence.** In `validation/g4/verify_matched_composition_v3_r7.py` (SHA-256 `c9893926f1a426246c03a1e5e480bd391a9afcc02fbf433634a4fc4c20f8c7c7`), complete Auer proofs must include a work object and a nonnegative integer `rhs_jacobian_evaluations`; booleans, strings, negative values, and missing values are rejected. The verifier validates the profile cap, seeds native replay with the producer count, and records producer, offline replay, combined, and cap values in the report. An overflow fails the audit. The R7 protocol explicitly keeps offline audit wall time and peak memory under a separate 120-second/1-GiB guard, outside the matched method worker measurement.

The fixture copies the archived proof, sets producer count to 100,000, and recomputes the body digest. The recorded zero-start control replay accepts the altered work count; R7 rejects with `NATIVE_PROOF_RHS_CAP_EXCEEDED` before any further RHS evaluation (`producer=100000; replay=0; combined=100000; cap=100000`). Four digest-recomputed malformed-work trials—missing, Boolean, numeric string, and negative—are rejected as `NATIVE_PROOF_WORK_FIELDS_INVALID`. No producer or IVP was invoked.

**Consequence.** The archived proof-to-common audit now checks the same combined RHS premise the Auer worker applies. The separate offline audit resource use remains separate from method-worker timing and memory. This fixture verifies the source contract at the boundary; it does not measure a prospective matched worker.

**Status.** **Combined-cap source behavior and archived-proof boundary fixture PASS; independent review and prospective query behavior PENDING.**

**Required action.** Review the producer work-field trust boundary, replay counter seeding, and reported counter semantics. Preserve the separate accounting for offline audit time/memory and method-worker time/memory.

## Finding 3 — R7 source closure, manifest, query universe, and preservation

**Finding.** The new R7 source closure and candidate manifest are reproducibly bound to the checked source, profiles, fixture, and probes. All 1,944 rows remain `NOT_RUN`.

**Evidence.**

| Artifact | Path | SHA-256 |
|---|---|---|
| R7 protocol | `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R7.md` | `b988838f52cc152878ec5edbeda7767fdfd05cc6bc4c768f4911d3f296cdd782` |
| R7 transitive import audit | `research/benchmarks/G4_AUER_MATCHED_TRANSITIVE_IMPORT_AUDIT_v3_R7.json` | `287248f1fa45b3a28113bcd806e8b459ff8ee6cc5fc91c96e59f965dc7bf2b82` |
| R7 source closure | `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R7.json` | `48006dcd4d1e1491e4cade78cf1fff4e895cebf30400764cbf384459f8fdbf9f` |
| R7 candidate manifest | `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v7.json` | `181dfad5ef58088fb192449ff8ebb31546c41dfb57c2d8a3e0768f78511ddc82` |
| R7 manifest sidecar | `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v7.sha256` | `ee4d2bf52f96b03f500a59daecbee0ec8b650ca357d080b9f4d5e4f8e649cab5` |
| Prospective R3 input-hash inventory | `research/benchmarks/G4_AUER_R3_PROSPECTIVE_INPUT_HASHES_v3_R7.json` | `95d3483898303567df180bcdd62b466b1d5507b427c8574c6fc6a960562609a2` |

The closure has **120 dependencies**; I recomputed all 120 exact-byte hashes successfully. The recursive import audit reports 23 reachable local modules, 73 directed edges, and zero unresolved local imports. The builder reports 1,944 ordered IDs with digest `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`. I checked the original order against both the archived Auer candidate manifest and the R7 prospective R3 input-hash inventory; all 1,944 rows in both remain `NOT_RUN`.

Manifest v7 records `matched_query_evaluations=0`, `one_query_worker_invocations=0`, `comparison_run=false`, `query_1_authorized=false`, and `batch_start_authorized=false`. The sidecar matches the exact manifest bytes. R7 prospective R3 method-input hashes were regenerated under the R7 profile; the historical R3 fixture retains its original binding and is identified as historical data.

R6 identity checks passed: source closure SHA-256 remains `56de9b89ed0d6bc0d4b46e88163b37e3254e61c4dbf2f95a306fcc8b83205c72`, candidate manifest SHA-256 remains `f722ac6f2df39cc1f2fdbae8ea3df7b1684c91659efb708aeba01fb5b436fa65`, and all 92/92 R6 closure dependency hashes match. The manifest records 27 preserved R6 artifacts; their listed exact-byte hashes match. All 14 listed R5 candidate source/profile artifact hashes also match. No R6/R5 artifact was edited.

**Consequence.** R7 is a versioned, reviewable source/protocol candidate with an unchanged ordered comparison universe. It is not a completed matched comparison or authorization to start one.

**Status.** **Closure, dependency hashes, manifest sidecar, query order/statuses, and listed R5/R6 preservation hashes PASS. Candidate remains REVIEW CANDIDATE.**

**Required action.** Independently review the full 120-entry closure and R7 source diff. Resolve any source or methodological blockers before a separate authorization review for query 1 or batch start.

## Finding 4 — Fresh 64-MiB memory-only probes and resource accounting

**Finding.** Both versioned R7 worker memory-probe commands passed under the installed 64-MiB Job Object limit. These results cover the probe commands only.

**Evidence.** The unchanged per-method query guard remains 120 seconds and 1 GiB. Each probe requested a 256-MiB allocation under a 67,108,864-byte cap; the child was created suspended and assigned to the Job Object before resume, the cap was installed, and allocation failed with `MemoryError`.

| Arm | Guard record SHA-256 | Stdout SHA-256 | Peak bytes | Installed cap |
|---|---|---|---:|---:|
| Auer | `4dca358c43c5ab2769c67937dfbc30f4cd455f0e8a30001754419b338ce29a92` | `0df97e81a45efd33c99ee875c459aa067fdd3c8e298c70537609d756a514faf2` | 66,232,320 | 67,108,864 |
| R3 | `89e3434f6942390f9c8d1010a889c20da4a520bf9e83fc3da8f53a1cce84ce3c` | `c4c9bc0b90bcc7ef88cf994d2ee87884f934c135fa8b151d7418a2e344612068` | 66,646,016 | 67,108,864 |

The probe index `results/validation/g4/auer2013/protocol_v3_r7_guard_probes/probe_refresh_index.json` hashes to `d3859b97860471d243992f5dbe9c75efd9841720700ff4fc2ef5bf9dc8868cf9`; it binds closure `48006dcd4d1e1491e4cade78cf1fff4e895cebf30400764cbf384459f8fdbf9f` and reports `PASS_FOR_BOTH_64_MIB_MEMORY_PROBE_COMMANDS_ONLY`, zero matched-query invocations, zero batch evaluations, and zero producer invocations.

The archived composition/contract fixture ran in its separate 600-second/1-GiB fixture Job Object: the guard reports 3.469 seconds outer wall, 52,666,368-byte peak, zero matched-worker calls, and zero producer/IVP calls. Its stored fixture counters report Auer common-stage work of 2,415 operations under the remaining 1,799,969-operation cap; R3 adapter conversion work of 1,251/2,000,000; and R3 common-stage work of 2,415/2,000,000 including the segment reparse. These are archived-fixture counters. The verifier's own read-only audit has a separate 120-second/1-GiB guard. Neither offline audit nor fixture resource use is included in a method-worker measurement. The 64-MiB probes do not exercise the 120-second/1-GiB query pipeline, native proof serialization for a future trajectory, or any matched result.

**Consequence.** The evidence shows the R7 guard installed the requested memory cap for the memory-probe commands and stopped their deliberate allocations. It does not establish query-level wall time, memory, proof-size fit, or paired-method performance.

**Status.** **Both memory-probe commands PASS within their stated scope; matched-query resource behavior UNVERIFIED.**

**Required action.** Keep the probe scope explicit in any review. Do not use these probe results as query-level performance or feasibility evidence.

## Commands and execution record

The following worker-guard commands completed with exit code 0 and wrote the records above:

```powershell
python -m validation.g4.run_matched_worker_guard_v3_r7 --method auer --probe --probe-limit-mib 64 --probe-allocation-mib 256 --stdout-output results/validation/g4/auer2013/protocol_v3_r7_guard_probes/auer_worker_memory_probe_stdout.log --guard-output results/validation/g4/auer2013/protocol_v3_r7_guard_probes/auer_worker_memory_probe.json

python -m validation.g4.run_matched_worker_guard_v3_r7 --method r3 --probe --probe-limit-mib 64 --probe-allocation-mib 256 --stdout-output results/validation/g4/auer2013/protocol_v3_r7_guard_probes/r3_worker_memory_probe_stdout.log --guard-output results/validation/g4/auer2013/protocol_v3_r7_guard_probes/r3_worker_memory_probe.json
```

The manifest was rebuilt successfully after writing the probe index:

```powershell
python -m validation.scripts.build_g4_auer_v3_r7_candidate
```

Builder output reported closure SHA `48006dcd4d1e1491e4cade78cf1fff4e895cebf30400764cbf384459f8fdbf9f`, 120 dependencies, 23 transitive modules, 73 import edges, zero unresolved imports, manifest SHA `181dfad5ef58088fb192449ff8ebb31546c41dfb57c2d8a3e0768f78511ddc82`, 1,944 candidate IDs, zero matched-query evaluations, and every candidate row `NOT_RUN`.

The retained fixture guard records the executed child command `C:\msys64\ucrt64\bin\python.exe -m validation.g4.protocol_v3_r7_composition_fixture`, exit code 0, and report/closure hashes above. During CLI inspection, `python -m validation.g4.protocol_v3_r7_composition_fixture --help` was attempted; this entrypoint has no help parser and attempted its fixed output directory, then exited with `FileExistsError` because the successful retry2 directory already exists. It stopped at directory creation; it did not overwrite the passing report or guard and invoked no producer, matched worker, or query. I retained the existing successful retry2 evidence.

## Codex review request and stop boundary

Please review the R7 protocol, profile, workers, schema/validator, composition verifier, fixture report/guard, memory-probe index/records, 120-dependency source closure, candidate manifest, and preserved R5/R6 identities. In particular, check that the profile cap and `RESOURCE_LIMIT` path agree across worker, schema, validator, and offline report; check the Auer producer/replay counter semantics against the 100,000 cap; and keep method-worker resource measurements distinct from the separate read-only audit and fixture guards.

Return any blockers and the evidence needed to resolve them. The R7 candidate does not authorize query 1 or the 1,944-query batch. No query, G3, controller, or hardware work was started. No commit or push was made. The separate `LUNA-G2-SCOPE` work remains outside this G4 source boundary.
