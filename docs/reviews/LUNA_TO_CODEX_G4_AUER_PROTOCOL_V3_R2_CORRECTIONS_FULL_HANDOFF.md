# Luna to Codex ? G4 Auer protocol-v3 R2 corrections handoff

**Date:** 2026-10-01  
**Package:** `G4_AUER_MATCHED_PROTOCOL_V3_R2_CORRECTIONS`  
**Repository:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Authority:** MASTER v2.1. Status remains **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**.  
**Disposition:** Versioned source-closure candidate prepared for independent review. It is not finally frozen and it does not authorize a matched query.

## Finding 1 ? protocol policy now describes the accepted Auer core

**Evidence.** The selected route preserves the accepted residual/Picard mathematics and its ?remaining horizon; bisect after failed native inclusion only? policy. Common checking occurs after complete native proof and replay. The R2 protocol is [G4_AUER_MATCHED_PROTOCOL_v3_R2.md](../../research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R2.md), SHA-256 `4f4640094609eb1bb130ffce63f57e4d0d149bd2254829b17e582fed75b2e545`.

The accepted solver remains `validation/baselines/auer2013/residual_ivp.py`, SHA-256 `3f15779ee772c7090951942186ef56ee5956d9569d2a1ff4c2f7e010646bf70f`. A versioned candidate copy, `validation/baselines/auer2013/residual_ivp_g4_matched_v3_r2.py`, has SHA-256 `27384ab4ff74bce48c4459ae6e6da6a573df6587c176b41fcfeccf0d006ba464`. Its code diff is limited to the matched input schema, arbitrary manifest-bound query ID, and declared benchmark horizon/voltage validation. The residual/Picard proof-producing body is unchanged. The frozen replay source remains `validation/baselines/auer2013/replay_ivp.py`, SHA-256 `c8ebcb30b890090a0dcb45e6f80c93b15e1bb63f8401c33af3c288c88bfbc913`.

**Consequence.** R1's 0.01-second base slabs, depth-five refinement, and common-predicate-guided subdivision are withdrawn. No proposed policy is represented as existing R4 behavior. The new solver copy and its wider input acceptance are proof-critical review targets.

**Status.** Source-aligned policy and versioned solver copy materialized; independent proof-critical review remains pending.

**Required action.** Independently review the solver diff, exact input binding, proof binding, and replay acceptance scope before final freeze.

## Finding 2 ? UNKNOWN status and proof retention are explicit

**Evidence.** Common predicates run only once, after whole-hold native proof and native replay. There is no common-driven refinement or rollback. A proof-complete native tube remains valid IVP evidence if the supplied-tube predicate is `UNKNOWN_ON_SUPPLIED_TUBE`; the final status retains `PROOF_COMPLETE_COMMON_UNKNOWN`. An actual resource stop is recorded at its stage while preserving the native proof status.

The Auer worker maps raw `UNKNOWN` to `INCLUSION_NOT_ESTABLISHED` only when the termination reason is `PICARD_INCLUSION_FAILURE_AFTER_FROZEN_HALVINGS`. Other raw uncertainty remains `UNKNOWN`. Both workers preserve `native_raw_status`, raw reason codes, native proof path, exact-byte proof-file hash, and the method's proof-record digest. The output schema is `research/benchmarks/G4_AUER_MATCHED_QUERY_RESULT_v3_R2_SCHEMA.json`, SHA-256 `4dcdb499d8bdde5400400960c672ee8beaf6b44f7b892f3ff74cd3001b2b53b3`.

**Consequence.** Common uncertainty is not reclassified as a failed IVP inclusion, collision, or resource failure. Final `CERTIFIED` requires complete/certified native evidence, passing native replay, and `PASS_ON_SUPPLIED_TUBE`.

**Status.** Raw and normalized status fields, no-refinement policy, and output schema are materialized; independent mapping review remains pending.

**Required action.** Review raw-to-normalized statuses for each worker, including UNKNOWN and resource exits, and confirm the proof-complete UNKNOWN path retains its native evidence.

## Finding 3 ? equal external limits and stage-specific work are versioned

**Evidence.** Candidate profiles and guard are hash-bound:

| Candidate | SHA-256 |
|---|---|
| `validation/configs/auer_g4_matched_profile_v3_r2.json` | `1306c900a3985193d131a3a000d4af9b62624ead1b86fdeb6e0b824e202a2431` |
| `validation/configs/r3_g4_matched_profile_v3_r2.json` | `ed53368ba9588e5785c682ae430ca695ab704d4462b7c85b4256d6d1ca91a102` |
| `validation/configs/g4_common_predicate_profile_v3_r2.json` | `b18e3bc83e364d883200bfef0db08322ca52be4fb6c792a501d8f3326edcb75d` |
| `validation/configs/g4_equal_resource_guard_v3_r2.json` | `35a97d7618bb0c20c87390eefca1cbc4a0269b2dab8f7a7ef734bf078358e880` |

The future primary pair has a 120-second parent monotonic deadline and a 1,073,741,824-byte Windows Job Object process-commit limit per method/query. The pinned CPython 3.12.12 UCRT executable SHA-256 is `b5c33df60c2a8421dcf8117a67e848436b5d395c71ec1c0dfd96bad10f441d7f`. Exact-rational operations remain method/stage-specific: no common operation cap or synthetic cost score is claimed. The shared future predicate profile uses 128 square-root bisections; the preserved R3 v5 fixture remains under its historical 24-bisection profile.

Both new worker modules passed the separate 64-MiB Job Object enforcement probe using a 256-MiB allocation attempt:

| Worker probe evidence | SHA-256 | Peak process commit under 64-MiB cap |
|---|---|---:|
| Auer `results/validation/g4/auer2013/protocol_v3_r2_guard_probes/auer_worker_memory_probe.json` | `0468837e69888152fa1038355f33670da29199751c677c318aa3b191b6f94feb` | 66,899,968 bytes |
| R3 `results/validation/g4/auer2013/protocol_v3_r2_guard_probes/r3_worker_memory_probe.json` | `21844849ba2151b5195118df66d2e0b67b786ebd4b2bcc797539995d7dec54de` | 66,961,408 bytes |

Each probe record reports the cap installed, suspended assignment before resume, `MemoryError`, and `probe_enforcement_verified=true`. Both records bind source-closure SHA-256 `f63707d34118fe78fbf8e0e3ce73be9329bb6824ef3523e1375a91d11abc3bea`.

**Consequence.** Memory enforcement was demonstrated for the probe commands only. No matched query worker was launched, so the 120-second and 1-GiB limits, query-stage timers, and peak-memory reporting have not been exercised on a proof computation.

**Status.** Equal resource candidates materialized; both 64-MiB enforcement probes PASS; actual query-run guard inspection and independent resource review remain pending.

**Required action.** Review both probe records and the resource accounting. Before any query is separately authorized, inspect the exact one-query launcher path and stage/total boundaries.

## Finding 4 ? candidate source closure and per-query workers are materialized

**Evidence.** The source-closure inventory `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R2.json` has SHA-256 `f63707d34118fe78fbf8e0e3ce73be9329bb6824ef3523e1375a91d11abc3bea` and 49 exact-byte dependencies. Its dependency checks pass for the protocol, profiles, schema, frozen inputs, Auer/R3 producer and replay sources, common predicate, new workers/guard, and preserved historical records.

The one-query candidate sources are:

| Source | SHA-256 |
|---|---|
| `validation/g4/auer_matched_query_worker_v3_r2.py` | `ff966f15e7ce74248f20c76569883f3db2e49583da7e3f605d9ad3e657cb2094` |
| `validation/g4/r3_matched_query_worker_v3_r2.py` | `ae50f20e13630521bb468abaa92b603b83fa209996eed537f25aa9495c714c3e` |
| `validation/g4/matched_worker_common_v3_r2.py` | `72d93b8e004d0094d8408b243605035234a1af2de1625951547995dc69f9abbe` |
| `validation/g4/run_matched_worker_guard_v3_r2.py` | `b77cde0b4842872d7e94b302604446e1f89d4a5da356e329d910739614ebb7c8` |

Each invocation accepts exactly one `--query-id`; there is no batch loop. The candidate freeze manifest is `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v3.json`, SHA-256 `579b2ff675cbfff733bf539e8bb22bad5ce817b434807b8fa71417de5ff324bc`. It binds the closure, workers, profiles, schema, and probe evidence and retains 0 evaluations, `comparison_run=false`, and `query_1_authorized=false`.

**Consequence.** The package is substantially more reviewable, but the source closure is still a candidate: no independent source/replay review or clean-copy audit has been completed. The local R4/R5 v10/v11 snapshot-member limitation remains; do not claim external member-by-member verification of all 720/726 members.

**Status.** Workers and 49-dependency closure materialized; source/replay acceptance and final freeze remain pending.

**Required action.** Independently audit both workers, proof bindings, imports, dependency hashes and copied-source behavior. Keep the snapshot-member limitation explicit.

## Finding 5 ? the existing R3 v5 parity witness and R4/R5 evidence are preserved

**Evidence.** Existing R3 selection and adapter artifacts remain unchanged:

- `r3_archived_fixture_selection_v5.json`: SHA-256 `4c6e6becc3a7e165ab3821fe0bf0436b06a79f0c1bb9745fde00e39d5a9db19f`
- `r3_archived_adapter_fixture_v5.json`: SHA-256 `1b3a97e171d12585bc8918b819b6b28403467926889dc9c5488786c01c69b92b`

The prior recorded review identifies the selected native record by semantic and line-byte SHA-256 `a46c6472271fd93f20154e9696c10a865ce97615de6c0aeda69c845f2f0254d3`: replay PASS, full closed-hold and twelve-label coverage, one center-plus-radius expansion, common predicate PASS, proof-to-common replay PASS, and five mutations rejected. This remains interface-parity evidence only; its historical resource profile does not populate the equal-resource result.

Frozen R4/R5 identities remain unchanged: R4 output manifest `6a8d5501972cbb1351cb9ea09500427cb37f8b30c37673ee9e573e156ab6b1a7`; R4 native proof/evidence `8d394d836c5b92b733403b16b1786cb7fe410ab8fb8610c694c0a7c88e5dde4e` / `e05945b62bf058b76a121c32d316184e577158d3fc7789a6bfed1356c354ec4a`; R5 artifact manifest/pristine replay report `48196f1f3ebb5cf9787c68bc98f6ad88a0678ebd92683014fe877d015f18dd44` / `66ff923d3fe037eae0a96f5a33381ff9a9a1994121cbd0232d0d1cb0c174e84f`.

**Consequence.** No fixture duplicate was made and no R4/R5 proof/evidence was rewritten. Historical parity results are not recast as prospective matched observations.

**Status.** Exact-byte preservation checks PASS for the cited local artifacts; their stated historical scope is retained.

**Required action.** Review the existing R3 v5 witness within its interface-only scope; do not request a duplicate absent a specific missing premise.

## Finding 6 ? no comparison query was run or authorized

**Evidence.** The v3 manifest preserves 1,944 unique IDs in the existing order, with LF-joined SHA-256 `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`. The candidate row statuses remain `NOT_RUN`. The two operations performed on the new worker modules were memory-only guard probes and did not invoke a query worker.

**Consequence.** There is no comparison result, no G4 novelty evidence and no gate promotion. The research disposition remains HOLD.

**Status.** **0/1,944; query 1 unauthorized; no commit or push.**

**Required action.** Complete independent review, then prepare a final hash-bound freeze and obtain separate batch-start review/authorization before any query execution.

## GPT review request

Please independently review `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R2.md`, `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v3.json`, and the bound source-closure inventory. Evaluate protocol/source alignment and the versioned solver diff; raw and normalized UNKNOWN/resource semantics; the unchanged R3 v5 parity witness; equal-resource fairness, stage boundaries and the limits of the 64-MiB probes; all source/profile/schema/worker bindings; and the stated R4/R5 snapshot-member limitation. Identify blocking inconsistencies and the precise evidence required before final freeze. Return the review as a downloadable `.md` file. The matched batch remains **0/1,944 and is not authorized**.

**Preparation boundary:** no matched query, R3/R4/R5 rerun, controller/hardware experiment, gate promotion, commit, or push was performed.
