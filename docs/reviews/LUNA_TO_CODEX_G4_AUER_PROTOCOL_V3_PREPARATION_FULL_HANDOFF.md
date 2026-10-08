# Luna to Codex — G4 Auer protocol-v3 preparation handoff

**Date:** 2026-10-01  
**Package:** `G4_AUER_MATCHED_PROTOCOL_V3_PREPARATION`  
**Repository:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Authority:** MASTER v2.1; project status remains **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**.  
**Review status:** Prepared for independent review. Protocol and freeze manifest are candidates; neither is accepted or locked.

## Finding 1 — protocol v3 candidate prepared

**Evidence.** `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3.md` records the existing 1,944-ID universe and digest `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`; defines the reconstructed exact-rational/Taylor Auer method, native proof replay, common-tube predicate and status contract; proposes a deterministic dyadic step/rejection policy; and specifies candidate equal-resource limits and output fields. Its exact-byte SHA-256 is `302db359dd622aeb78fc692a08db09cc7f88fcdf4eddb2d23f46952adf2f84f7`.

The policy distinguishes the paper-method reconstruction from execution of the historical VALENCIA software. Auer supplies `NATIVE_TOTAL_HULL` with expansion count 0; R3 supplies `CENTER_PLUS_RADIUS_ONCE` with expansion count 1. Only native proof completion/replay together with `PASS_ON_SUPPLIED_TUBE` is `CERTIFIED`.

**Consequence.** The protocol provides a reviewable candidate while preserving the model, IDs/order, initial cells, scenes, horizons, actions, full twelve-label image and fixed-label semantics. It does not authorize query 1 or change prior proof records.

**Status.** `REVIEW CANDIDATE — NOT LOCKED; NO BATCH START`.

**Required action.** Independently review the scientific invariants, deterministic step and rejection policy, native/common status mapping, output schema, and the proposed resource limits before any final freeze.

## Finding 2 — existing R3-to-common v5 artifact satisfies the interface-parity obligation

**Evidence.** The published fixture is bound to the following exact artifacts:

| Artifact | SHA-256 |
|---|---|
| `results/validation/g4/auer2013/r3_archived_fixture_selection_v5.json` | `4c6e6becc3a7e165ab3821fe0bf0436b06a79f0c1bb9745fde00e39d5a9db19f` |
| `results/validation/g4/auer2013/r3_archived_adapter_fixture_v5.json` | `1b3a97e171d12585bc8918b819b6b28403467926889dc9c5488786c01c69b92b` |
| `results/validation/g2/r3/conditional_full_grid_records_r3_v1.jsonl.gz` | `352b6c67480133350a7d1bfc89334a1beff1dc27c64cfda46391af27982fa874` |
| `results/validation/g2/r3/conditional_full_grid_archive_manifest_r3_v1.json` | `052c12ba33e05820449d29796c567d90a9c6cf68cd17255f622744d8589b99ac` |
| `validation/g4/verify_r3_archived_fixture.py` | `106b46506dbf35f03bd6d1b6f05acb834324e08a494becd299b6efc460b5eb72` |
| `validation/g4/common_tube.py` | `564c0ffe608be6d0413def643a5dff7b455613c61b56f0ea42684cc7c6874d25` |
| `validation/g4/r3_common_adapter_profile_v4.json` | `1e5f081e65fc8c6420ced12f0082b557262e81ca9503aef3be241cc35638a69e` |
| Reconstructed common-check semantic record (committed by the fixture) | `1232b4484de311e02d11e61c45d1b7b05e84d04aa8ac1f6443efe146ce0fdf5f` |

The selected ID is `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`. Its archive line-byte hash and canonical-record semantic hash are both `a46c6472271fd93f20154e9696c10a865ce97615de6c0aeda69c845f2f0254d3`. Native R3 status is `CERTIFIED`; independent native replay is recorded PASS. The adapter expands the center/radius representation once (`CENTER_PLUS_RADIUS_ONCE`, count 1), includes all 12 fixed labels, and covers the entire closed hold `[0, 1/50]`. The common predicate replay is `PASS_ON_SUPPLIED_TUBE`, with approximately `0.03776109218597412 m` collision clearance and `1.8380586882546766 N` contact reserve. Proof-to-common composition replay passes; all five stored mutation trials are rejected.

The common record explicitly has `certificate_emitted=false` and `ode_tube_proof_replayed=false`: it checks predicates on the supplied tube, while native proof replay and the bound composition establish the upstream proof relationship. The existing verifier was replayed against the stored fixture during this preparation; the manifest and selection/source bindings were also rechecked. No native R3 record was rerun for this fixture.

**Consequence.** The existing v5 artifact satisfies the v3 pre-batch interface-parity obligation. It is one-query interface and proof-to-common evidence, not an equal-resource matched observation and not evidence that all 1,944 queries have been evaluated. No replacement fixture is indicated unless review names a missing field or premise.

**Status.** Existing fixture replay and binding checks PASS; historical resource comparability is NOT SATISFIED.

**Required action.** Review the archived native record, its query/source bindings, one-time radius expansion, full-hold and label coverage, common margins/status, and the limited scope of the common layer.

## Finding 3 — bibliographic erratum preserves the frozen mathematical contract

**Evidence.** `docs/reviews/G4_AUER_METHOD_CONTRACT_V2_BIBLIOGRAPHIC_ERRATUM_v1.md` has SHA-256 `d2713cefdf04a8af0df642ab8067af72b6a896eb2507b81716ef9d23f91540a1`. It corrects metadata for Rauh and Auer, *Reliable Computing* 15(4), 370–381 (2011), citing Algorithm 1 and Eqs. (3)–(6), and omits the unverified DOI. The official publisher PDF URL returned HTTP 200; the locally retained PDF is 640,240 bytes with SHA-256 `1405b54eaa25c5d3874af74ac71087364f3a84ddada675c336e378779e902265`. The frozen v2 method-contract bytes remain unchanged, SHA-256 `2a5d74de613ccf5f716035732b31ee1dcca69ad3d11d45d1d1267a517a63fc63`.

**Consequence.** The erratum changes bibliography metadata only; mathematical clauses and prior R4/R5 proof bindings are unchanged. The proposed future batch binds the exact v2 contract bytes plus this separate erratum. It does not relabel existing proofs as v3 outputs.

**Status.** Metadata correction verified; DOI remains unverified; no mathematical contract change proposed.

**Required action.** Confirm this contract-plus-erratum binding during review. If review instead requires a new proof-bound contract, version and independently review the producer/replay binding before query 1.

## Finding 4 — candidate source and resource manifest is complete enough for review, not final freeze

**Evidence.** `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v1.json` has SHA-256 `c4f5e8200f4c197c7ce0c60ec0a3a00fc4b63e8c6d6d3919d879aec0a9f81525`. Its 75 SHA-256 fields are well-formed; 74 file/artifact and record-binding checks pass. It binds the protocol hash, query/model inputs, R3 producer and checker sources, Auer R4/R5 proof-critical sources, arithmetic backend, method-contract/erratum pair, archived R3 selection and adapter, development evidence, output/status contract, and runtime. The ordered query list was checked as 1,944 unique IDs with the expected digest and endpoints.

The proposed runtime is Windows x86-64 / MSYS2 UCRT64 CPython 3.12.12 at `C:/msys64/ucrt64/bin/python.exe`, executable SHA-256 `b5c33df60c2a8421dcf8117a67e848436b5d395c71ec1c0dfd96bad10f441d7f`; the current preparation host executable and hash match. Candidate per-method/query limits are 120 seconds and 1 GiB process commit memory, enforced by a parent monotonic-clock deadline and a Windows Job Object assigned before worker resume; one worker, no children, serial queries; 32,768 rational bits; 2,000,000 rational operations across the complete pipeline; and 512 MiB serialized proof/output. These values remain proposed, not accepted.

Historical R3 used 15 seconds, 16,384 rational bits, 1,000,000 rational operations, and no recorded process-memory cap. Adapter profile v4 used a 60-second stage cap and had no separately enforced memory cap. Archived R3 records therefore cannot populate the candidate equal-resource comparison. The manifest calls for prospective evaluation of the unchanged 1,944-ID order under a new versioned R3 profile and the same tested external limiter. Candidate Auer/R3 matched profiles and the external memory-enforcement probe are not yet materialized/accepted.

The manifest preserves these frozen development identities: R4 output manifest SHA-256 `6a8d5501972cbb1351cb9ea09500427cb37f8b30c37673ee9e573e156ab6b1a7`; R4 single-query proof `8d394d836c5b92b733403b16b1786cb7fe410ab8fb8610c694c0a7c88e5dde4e` and evidence `e05945b62bf058b76a121c32d316184e577158d3fc7789a6bfed1356c354ec4a`; R5 artifact manifest `48196f1f3ebb5cf9787c68bc98f6ad88a0678ebd92683014fe877d015f18dd44` and pristine replay report `66ff923d3fe037eae0a96f5a33381ff9a9a1994121cbd0232d0d1cb0c174e84f`. The full local v10/v11 source snapshots are not republished for external member-by-member verification; the manifest does not claim an outside audit of every snapshot member.

**Consequence.** The candidate records a reproducible review target and makes the historical resource mismatch explicit. It is not a final frozen source package or a batch-start authorization.

**Status.** Candidate manifest validation PASS; resource/source freeze and external review PENDING.

**Required action.** Review the source closure from a clean copied package; resolve the local-only snapshot membership limitation; approve or revise the paired resource contract, work accounting, memory probe, new matched R3 profile, Auer step policy, and output/status schema; then produce a finalized hash-bound manifest.

## Finding 5 — matched batch remains unstarted

**Evidence.** Candidate manifest records `matched_query_evaluations=0`, `comparison_run=false`, `query_1_authorized=false`, and `separate_batch_start_review_required=true`. Existing R4/R5 evidence remains historical development evidence and is not reinterpreted as v3 output.

**Consequence.** No result counts or method comparison can be reported from this preparation package.

**Status.** 0/1,944 matched queries evaluated; project status remains HOLD.

**Required action.** After protocol review and final freeze, request a separate batch-start review. Do not begin query 1 before that review explicitly authorizes the run.

## Artifact register

| Artifact | SHA-256 |
|---|---|
| `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3.md` | `302db359dd622aeb78fc692a08db09cc7f88fcdf4eddb2d23f46952adf2f84f7` |
| `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v1.json` | `c4f5e8200f4c197c7ce0c60ec0a3a00fc4b63e8c6d6d3919d879aec0a9f81525` |
| `docs/reviews/G4_AUER_METHOD_CONTRACT_V2_BIBLIOGRAPHIC_ERRATUM_v1.md` | `d2713cefdf04a8af0df642ab8067af72b6a896eb2507b81716ef9d23f91540a1` |
| `results/validation/g4/auer2013/auer_matched_candidate_manifest_v2.json` | `77024610eab603a1ee2085feb5b6e7da0719ddd0641efa3804df6190492e59ad` |
| `validation/configs/benchmark_v1.json` | `b2bc12cd578229cfb6df4b426f93e0f472d69f6be36929df93e797ff79396a9e` |
| `docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md` | `2a5d74de613ccf5f716035732b31ee1dcca69ad3d11d45d1d1267a517a63fc63` |
| `validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v2.json` | `254b448b5458fb9f9ebcd84e9a4e03cc7251124d3241ad00f4626aba7bcef085` |
| `C:/msys64/ucrt64/bin/python.exe` | `b5c33df60c2a8421dcf8117a67e848436b5d395c71ec1c0dfd96bad10f441d7f` |
| `results/validation/g4/auer2013/r3_archived_fixture_selection_v5.json` | `4c6e6becc3a7e165ab3821fe0bf0436b06a79f0c1bb9745fde00e39d5a9db19f` |
| `results/validation/g4/auer2013/r3_archived_adapter_fixture_v5.json` | `1b3a97e171d12585bc8918b819b6b28403467926889dc9c5488786c01c69b92b` |
| `results/validation/g2/r3/conditional_full_grid_records_r3_v1.jsonl.gz` | `352b6c67480133350a7d1bfc89334a1beff1dc27c64cfda46391af27982fa874` |
| `results/validation/g2/r3/conditional_full_grid_archive_manifest_r3_v1.json` | `052c12ba33e05820449d29796c567d90a9c6cf68cd17255f622744d8589b99ac` |
| `validation/g4/verify_r3_archived_fixture.py` | `106b46506dbf35f03bd6d1b6f05acb834324e08a494becd299b6efc460b5eb72` |
| `validation/g4/common_tube.py` | `564c0ffe608be6d0413def643a5dff7b455613c61b56f0ea42684cc7c6874d25` |
| `validation/g4/r3_common_adapter_profile_v4.json` | `1e5f081e65fc8c6420ced12f0082b557262e81ca9503aef3be241cc35638a69e` |
| R3-to-common check-record semantic commitment | `1232b4484de311e02d11e61c45d1b7b05e84d04aa8ac1f6443efe146ce0fdf5f` |
| R4 output artifact manifest | `6a8d5501972cbb1351cb9ea09500427cb37f8b30c37673ee9e573e156ab6b1a7` |
| R4 DDWMR proof / evidence | `8d394d836c5b92b733403b16b1786cb7fe410ab8fb8610c694c0a7c88e5dde4e` / `e05945b62bf058b76a121c32d316184e577158d3fc7789a6bfed1356c354ec4a` |
| R5 artifact manifest / pristine replay report | `48196f1f3ebb5cf9787c68bc98f6ad88a0678ebd92683014fe877d015f18dd44` / `66ff923d3fe037eae0a96f5a33381ff9a9a1994121cbd0232d0d1cb0c174e84f` |
| Official Rauh–Auer PDF retained in repo | `1405b54eaa25c5d3874af74ac71087364f3a84ddada675c336e378779e902265` |

## GPT review request

Please independently review `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3.md`, the **existing** R3 v5 archived proof-to-common fixture (do not request a duplicate without naming a missing premise), and `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v1.json`, including source closure and the proposed equal-resource policy. Identify blocking inconsistencies and decisions still required before final freeze and a separate batch-start review. Return your review as a downloadable `.md` file. This request does not imply that v3 has already been accepted.

**Preparation boundary:** no matched batch, G3/controller/hardware run, gate promotion, commit, or push was performed or authorized by this handoff.
