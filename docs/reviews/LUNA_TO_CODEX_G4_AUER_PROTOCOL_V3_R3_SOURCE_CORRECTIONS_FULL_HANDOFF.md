# Luna to Codex — G4 Auer protocol v3 R3 source-corrections full handoff

**Date:** 2026-10-02  
**Input handoff:** `docs/CODEX_TO_LUNA_G4_AUER_PROTOCOL_V3_R2_SOURCE_CORRECTIONS.md`  
**Read first:** `docs/reviews/CODEX_G4_AUER_PROTOCOL_V3_R2_SOURCE_REVIEW.md`  
**Disposition:** R3 source-corrections candidate assembled for independent review; **not a final freeze**.  
**Research state:** HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.  
**Batch:** **0/1,944**; no matched query, no commit, no push.

## Candidate package

- Protocol: `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R3.md`
- Freeze-manifest candidate v4: `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v4.json`
- Result schema: `research/benchmarks/G4_AUER_MATCHED_QUERY_RESULT_v3_R3_SCHEMA.json`
- Source closure: `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R3.json`
- Transitive import audit: `research/benchmarks/G4_AUER_MATCHED_TRANSITIVE_IMPORT_AUDIT_v3_R3.json`
- Fresh-probe index: `results/validation/g4/auer2013/protocol_v3_r3_source_corrections_probes/probe_refresh_index.json`
- Independent review request: `docs/reviews/GPT_REVIEW_REQUEST_G4_AUER_PROTOCOL_V3_R3_SOURCE_CORRECTIONS.md`

The earlier candidate manifests v1, v2, and v3, the R2 protocol and code, and the retained R3 v5/R4/R5 evidence remain unchanged. Candidate v4 records a new manifest over the R3 protocol and evidence. It does not authorize query 1 or the batch.

## Findings

### Finding 1 — Complete proof-relevant source closure

**Finding.** The R2 inventory omitted `validation/g2/polynomial.py`, imported by `validation/g2/model.py` in both prospective proof paths.

**Evidence.** The R2 closure contained 49 dependencies (SHA-256 `f63707d34118fe78fbf8e0e3ce73be9329bb6824ef3523e1375a91d11abc3bea`); the R3 closure contains 53 exact-byte dependencies, including the missing module and the newly versioned validator, import audit, and control-flow probe. The missing module is now bound as SHA-256 `48e3ff7dcce8353cb9d58b31f6986e12fcaaaf320cd06896f95e0813740b66a4`. The recursive AST audit begins at both workers, the guard, and result validator; it records 18 local modules, 47 directed local-import edges, and no unresolved local imports. Closure SHA-256 is `4e19ddf5f4fdfa28bc47bcd12baf96f82ee1682021f74b28dc375a9098400bf8`.

A new copied-package check copied all 53 listed dependencies, verified every byte hash, compiled 25 Python source files, and imported all 18 reachable local modules from inside the copy. The evidence is `results/validation/g4/auer2013/protocol_v3_r3_source_corrections_clean_copy_verification.json`, SHA-256 `0081a507d01592acab640c27e7f5c8f3210125f16e2b9cf011ace1fa39d3c328`. It statically checked the 1,944 frozen IDs without invoking a worker.

**Consequence.** The omitted local proof dependency is included and the candidate package resolves its local import graph in a clean copy. This is source-identity evidence, not independent proof acceptance.

**Status.** **RESOLVED FOR THIS REVIEW CANDIDATE; independent review pending.** The complete local v10/v11 snapshot trees are still unavailable for external member-by-member audit; no claim is made that every one of the 720/726 snapshot members was externally checked.

**Required action.** Independently inspect the import roots, closure inventory, and copied-package report before final freeze. Preserve the stated v10/v11 audit limitation.

### Finding 2 — Preserve native proof and common-stage evidence across late resource stops

**Finding.** An outer timeout or memory stop must control the final outcome without erasing completed native proof, replay, or common-predicate facts.

**Evidence.** The R3 workers write bounded (at most 256 KiB), atomic stage checkpoints bound to query, method, profile, protocol, full source-hash map, method-input hash, and a checkpoint digest. The outer guard restores only a matching intact checkpoint. It keeps final `RESOURCE_LIMIT` separate from native status/raw status, proof byte identity, replay status, and any completed common status. If an artifact exists without a validated checkpoint, the guard records its bytes as partial evidence and does not assert native proof completion, replay PASS, or completed common status. A fallback without a recoverable input binding records `method_input_sha256=null` with `input_binding_status=UNAVAILABLE` rather than a zero placeholder.

The closure-bound non-query control-flow probe reports PASS for timeout and memory-stop retention, partial proof/common byte identity, and the uncheckpointed-status rules. Its output is `results/validation/g4/auer2013/protocol_v3_r3_guard_probes/control_flow_semantics_probe.json`, SHA-256 `d1273dc91f6ae1d42316eeff1213f7bbc056310ff39108604fa4a2aef4443108`; it binds to closure SHA `4e19ddf5f4fdfa28bc47bcd12baf96f82ee1682021f74b28dc375a9098400bf8`.

**Consequence.** Late resource exhaustion can be represented without converting a completed proof stage into a native failure or treating an orphan partial file as a proof.

**Status.** **IMPLEMENTED AND CONTROL-FLOW-PROBED WITH SYNTHETIC ARTIFACTS.** The probe's synthetic proof/common records test checkpoint and status logic only; they are not mathematical evidence.

**Required action.** Review checkpoint trust boundaries and status implications independently. Keep synthetic control-flow evidence distinct from any future real proof result.

### Finding 3 — Classify proof-size exhaustion as a resource limit

**Finding.** Exceeding a declared proof serialization cap is resource exhaustion, not invalid input or implementation failure.

**Evidence.** `OutputSizeLimitError` is distinct from `CandidateInputError`; both workers catch it at proof serialization and emit a bounded structured `RESOURCE_LIMIT` record containing the attempted byte count while retaining producer status/raw status and producer work. Genuine malformed or out-of-universe input remains `INVALID_INPUT`. In-process `MemoryError` during proof JSON construction is classified as `RESOURCE_LIMIT`; an external Job Object memory stop is also an outer `RESOURCE_LIMIT` and recovers the last valid checkpoint when available. An orphan partial output is byte-identified but not promoted to a complete proof.

The closure-bound control-flow probe reports PASS for proof-size classification and producer-status/work retention. The probe's artifacts are synthetic and do not exercise a real proof producer.

**Consequence.** A future proof-size stop will be counted in the resource-limit category and retain the work/status already established by its producer.

**Status.** **IMPLEMENTED AND CONTROL-FLOW-PROBED; actual proof-size behavior on a query has not been run.**

**Required action.** Independently review the exception boundary, bounded result path, and external-memory-stop classification. Do not infer query-level memory behavior from this probe.

### Finding 4 — Use non-self-referential timing and one worker result write

**Finding.** A result cannot contain a measured duration for its own final write without rewriting the delivered result.

**Evidence.** Each worker now performs one atomic final result write. Stage timers and `worker_pre_final_write_seconds` stop immediately before that write; the worker has no `final_result_serialization` field. The parent monotonic `total_wall_seconds` is the primary equal-resource measurement from immediately before launch through worker exit and stdout/output flush. The guard sidecar separately records parent finalization time, final result write time, and post-write validation time.

The control-flow probe reports PASS for one worker result write and the non-self-referential timing contract. No matched query has been run, so none of these fields is a measured proof-pipeline duration.

**Consequence.** Worker-local stages and the parent outer wall have distinct, reviewable boundaries. Equal-resource query timing remains unmeasured.

**Status.** **TIMING CONTRACT IMPLEMENTED; query-level timing not measured.**

**Required action.** Review the actual timer boundaries and sidecar before matched execution. Keep the parent's outer wall through worker exit/output flush as the primary comparison metric.

### Finding 5 — Make result acceptance independently checkable

**Finding.** JSON annotations alone cannot enforce that `CERTIFIED` implies a complete native proof, replay PASS, and common predicate PASS.

**Evidence.** `validation/g4/validate_matched_result_v3_r3.py` checks the output schema; frozen query and method-input binding; source, protocol, profile, and schema hashes; native proof file and embedded record digests; common-record bytes and embedded segment digest; artifact paths constrained to the project; and cross-field status implications. It accepts `CERTIFIED` only with the method-native success status, a byte-validated proof, native replay PASS, and common PASS. It preserves `PROOF_COMPLETE_COMMON_UNKNOWN` only with the corresponding proof/replay and common UNKNOWN evidence. Mutation/corruption is rejected as artifact validation failure rather than converted to mathematical UNKNOWN.

The control-flow probe reports PASS for schema/status mutation rejection and post-hash proof corruption rejection. These synthetic records test validator behavior and do not replace native mathematical replay or independently establish a theorem.

**Consequence.** Candidate result files now have an explicit acceptance path beyond free-form schema annotations, while proof validity still depends on the native replay and correct method implementation.

**Status.** **VALIDATOR IMPLEMENTED AND MUTATION-PROBED; independent source/proof review pending.**

**Required action.** Independently review the schema subset, exact query/source binding, artifact digest checks, and each cross-field implication before final freeze.

## Fresh memory-only probes

The two new probes were run through the versioned Windows Job Object guard after the R3 source closure was final. Both probe result files bind to closure SHA-256 `4e19ddf5f4fdfa28bc47bcd12baf96f82ee1682021f74b28dc375a9098400bf8`. The preserved execution-profile file still contains links to earlier probe outputs bound to closure `6f83fae5f78c0bfd8ad886c2091aeb53d1963a5e24fa261e9952ff3aca4ef03c`; those links are explicitly superseded for this candidate by the fresh-probe index. The profile and earlier candidate files were left unchanged. Codex should review this separate evidence binding before final freeze.

| Arm | Limit installed | Allocation requested | Job peak | Enforcement | Result SHA-256 |
|---|---:|---:|---:|---|---|
| Auer | 67,108,864 B (64 MiB) | 268,435,456 B (256 MiB) | 66,502,656 B | PASS; allocation stopped with `MemoryError` | `c66cf9621da7485a2823f5bef8cf28e2fa51dbd915d490449d49f76514ef144a` |
| R3 | 67,108,864 B (64 MiB) | 268,435,456 B (256 MiB) | 66,637,824 B | PASS; allocation stopped with `MemoryError` | `1ed529f65f142d3d6ad2416c87c579b108b9fc41b5ead55c9aeb3089d84f6228` |

Both workers were created suspended and assigned before resume; the Job Object reported the exact configured limit. Stdout SHA-256 for each is `c4c9bc0b90bcc7ef88cf994d2ee87884f934c135fa8b151d7418a2e344612068`. The records and logs are in `results/validation/g4/auer2013/protocol_v3_r3_source_corrections_probes/`.

These probes test only the memory-probe command's allocation-failure enforcement. They did **not** invoke a matched query, serialize a proof, or measure the 120-second/1-GiB query pipeline. Actual query `PeakProcessMemoryUsed` remains unavailable.

## Source changes from R2 to R3

The exact old/new hashes and line deltas for the protocol, schema, workers, helper, guard, solver, and four profiles are recorded in `r2_to_r3_source_diff` in the v4 candidate manifest. The key entries are:

| Artifact | R2 SHA-256 | R3 SHA-256 | Change |
|---|---|---|---|
| Protocol | `4f4640094609eb1bb130ffce63f57e4d0d149bd2254829b17e582fed75b2e545` | `252370f3a90120bb61a286bfe0f844f1f53904a48a16446a1d78a02def1f62e8` | Adds checkpoint, resource-stop, proof-size, timing, and validator contracts |
| Result schema | `4dcdb499d8bdde5400400960c672ee8beaf6b44f7b892f3ff74cd3001b2b53b3` | `edfbecfbab3cc6f3713faf04ebb8f864d7f4aadfe0378b028219cff5efb4bdb0` | Adds retained-stage, partial-artifact, timing, and binding fields |
| Auer worker | `ff966f15e7ce74248f20c76569883f3db2e49583da7e3f605d9ad3e657cb2094` | `18539052484b41350b581c38d31424b8f3913c8f7c2e32370650f57c05e42805` | Adds structured resource stops/checkpoints/finalization handling |
| R3 worker | `ae50f20e13630521bb468abaa92b603b83fa209996eed537f25aa9495c714c3e` | `8bedaf635c50216e18c981b627622d7ebb099d3eb4166eb8c83f753c034c1e68` | Same status/resource/timing corrections for R3 path |
| Shared helper | `72d93b8e004d0094d8408b243605035234a1af2de1625951547995dc69f9abbe` | `1e3c56169f1984b79a4213429c35ae2d3609d7bce4895da1fff4f9c6d43d9432` | Adds atomic bounded checkpoints, partial byte identity, distinct size-limit exception |
| Outer guard | `b77cde0b4842872d7e94b302604446e1f89d4a5da356e329d910739614ebb7c8` | `f0b3de3bb21270ea669503e9747c765eca78ccb7f7c540a162931d2f4182d40f` | Adds checkpoint recovery, artifact validation, parent timing, sidecar |
| Auer profile | `1306c900a3985193d131a3a000d4af9b62624ead1b86fdeb6e0b824e202a2431` | `3ace015b3aa5056e0736713d8e850b70918cfe96aec6412ca298f06a9dcc51bd` | Rebinds the Auer worker to R3 candidate settings |
| R3 profile | `ed53368ba9588e5785c682ae430ca695ab704d4462b7c85b4256d6d1ca91a102` | `29e41c43aa774a222440bab878a40a0eefd71fc757070fac33cb642dff8ffccf` | Versions the R3 worker/resource settings |
| Common predicate profile | `b18e3bc83e364d883200bfef0db08322ca52be4fb6c792a501d8f3326edcb75d` | `52c592d8fd94ba438f4cd678b58753e5372fb341d8410ec32c775336f28ca794` | Versions shared predicate settings |
| External guard profile | `35a97d7618bb0c20c87390eefca1cbc4a0269b2dab8f7a7ef734bf078358e880` | `7b8bf4b7b28d76f0108c406195985e967ed2d24d7355e4cbe5892a9e648bad5c` | Adds checkpoint, probe-scope, and finalization metadata |
| Versioned Auer solver | `27384ab4ff74bce48c4459ae6e6da6a573df6587c176b41fcfeccf0d006ba464` | `27384ab4ff74bce48c4459ae6e6da6a573df6587c176b41fcfeccf0d006ba464` | Byte-identical; no proof-formula change |

The new result validator is `validation/g4/validate_matched_result_v3_r3.py`, SHA-256 `aa7d8012aaf946891a91e7565e5c40500553c17ae43a40decefc1d990a12ef2f`. The closure adds `validation/g2/polynomial.py`; it leaves Auer residual/Picard math, R3 producer/checker math, the shared common predicate math, and historical R3/R4/R5 proof mathematics unchanged.

## Candidate identity and retained evidence

| Item | Path | SHA-256 |
|---|---|---|
| Freeze-manifest candidate v4 | `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v4.json` | `9a5994399a5296af1671369c7e08b79a96193d0d0037d10fa522fbf48b7146ca` |
| Protocol | `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R3.md` | `252370f3a90120bb61a286bfe0f844f1f53904a48a16446a1d78a02def1f62e8` |
| Source closure | `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R3.json` | `4e19ddf5f4fdfa28bc47bcd12baf96f82ee1682021f74b28dc375a9098400bf8` |
| Import audit | `research/benchmarks/G4_AUER_MATCHED_TRANSITIVE_IMPORT_AUDIT_v3_R3.json` | `da6b3b7429184ccefa16835659a3cb57a5e8e07da0fcf800c6c9561ed30c7970` |
| Clean-copy report | `results/validation/g4/auer2013/protocol_v3_r3_source_corrections_clean_copy_verification.json` | `0081a507d01592acab640c27e7f5c8f3210125f16e2b9cf011ace1fa39d3c328` |
| Control-flow report | `results/validation/g4/auer2013/protocol_v3_r3_guard_probes/control_flow_semantics_probe.json` | `d1273dc91f6ae1d42316eeff1213f7bbc056310ff39108604fa4a2aef4443108` |
| Fresh-probe index | `results/validation/g4/auer2013/protocol_v3_r3_source_corrections_probes/probe_refresh_index.json` | `7ad462fac15e167a6e5486c2635e8ac4233b3b2206406c4abf46ab5a644382c3` |

The profile, schema, worker, validator, probe, closure, and report hashes are also enumerated in the candidate manifest. The previous manifest v3 remains byte-identical at SHA-256 `579b2ff675cbfff733bf539e8bb22bad5ce817b434807b8fa71417de5ff324bc`; v1 and v2 are also retained unchanged.

The copied package and source closure reverify these retained evidence bytes:

| Evidence | Path | SHA-256 |
|---|---|---|
| R3 v5 selection fixture | `results/validation/g4/auer2013/r3_archived_fixture_selection_v5.json` | `4c6e6becc3a7e165ab3821fe0bf0436b06a79f0c1bb9745fde00e39d5a9db19f` |
| R3 v5 adapter fixture | `results/validation/g4/auer2013/r3_archived_adapter_fixture_v5.json` | `1b3a97e171d12585bc8918b819b6b28403467926889dc9c5488786c01c69b92b` |
| R4 output manifest | `results/validation/g4/auer2013/r4_output_artifact_manifest_v1.json` | `6a8d5501972cbb1351cb9ea09500427cb37f8b30c37673ee9e573e156ab6b1a7` |
| R4 native record | `results/validation/g4/auer2013/r4_ddwmr_single_query_native_v2.json` | `8d394d836c5b92b733403b16b1786cb7fe410ab8fb8610c694c0a7c88e5dde4e` |
| R4 evidence record | `results/validation/g4/auer2013/r4_ddwmr_single_query_evidence_v2.json` | `e05945b62bf058b76a121c32d316184e577158d3fc7789a6bfed1356c354ec4a` |
| R5 artifact manifest | `results/validation/g4/auer2013/r5_composition_replay_v1/r5_artifact_manifest_v1.json` | `48196f1f3ebb5cf9787c68bc98f6ad88a0678ebd92683014fe877d015f18dd44` |
| R5 replay report | `results/validation/g4/auer2013/r5_composition_replay_v1/pristine_replay_report.json` | `66ff923d3fe037eae0a96f5a33381ff9a9a1994121cbd0232d0d1cb0c174e84f` |
| R4 snapshot manifest | `results/validation/g4/auer2013/source_snapshot_v10/snapshot_manifest.json` | `29ca0f22791ccc740ef377b232522dee88bbaf00367213bfc45cc07925c5bcd5` |
| R5 snapshot manifest | `results/validation/g4/auer2013/r5_composition_replay_v1/source_snapshot_v11/snapshot_manifest.json` | `d6ed85d98f630889912e30baaf00314ac4069c4dc846525c639832c64ff959eb` |

These artifacts were copied and hash-checked; no R3 v5 fixture, R4/R5 output, replay, or proof mathematics was regenerated or edited.

## Batch and review boundary

The candidate manifest independently rechecks 1,944 unique ordered IDs with LF-joined SHA-256 `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`. Every candidate row remains `NOT_RUN`; `comparison_run=false`; `query_1_authorized=false`; `matched_query_evaluations=0`; and one-query worker invocations for matched queries are zero. **Batch remains 0/1,944.**

The candidate is not finally frozen. The 64-MiB probes do not measure an actual proof pipeline under the 120-second/1-GiB limits, and v10/v11 member-by-member external auditing remains unavailable. A separate review and authorization is required before query 1 or any batch start. No gate or novelty disposition changes.

## Required independent review

Please use the accompanying `docs/reviews/GPT_REVIEW_REQUEST_G4_AUER_PROTOCOL_V3_R3_SOURCE_CORRECTIONS.md` for the independent source/proof/resource review. The requested output is a downloadable Markdown disposition with Finding / Evidence / Consequence / Status / Required action. It should assess this concrete candidate only; it should not infer G4 novelty or authorize matched execution.