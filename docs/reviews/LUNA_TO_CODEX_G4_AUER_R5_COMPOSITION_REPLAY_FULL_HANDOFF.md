# Luna to Codex — G4 Auer R5 stored-artifact composition replay

**Date:** 2026-10-01  
**Repository:** ddwmr-actuator-safety  
**Branch / HEAD:** luna/g2-validation-v1 / aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46  
**R5 snapshot:** results/validation/g4/auer2013/r5_composition_replay_v1/source_snapshot_v11  
**R5 snapshot manifest SHA-256:** d6ed85d98f630889912e30baaf00314ac4069c4dc846525c639832c64ff959eb

## Disposition

**R5 replay PASS for the frozen single R4 DDWMR composition.** The verifier read the stored native proof envelope, replayed the accepted 21-coordinate slab, rebuilt the common NATIVE_TOTAL_HULL segment, recomputed the collision/contact record, and rebuilt the expected composition before comparing the stored records. Every common-record and composition field matched.

All 17 file-based mutations were rejected by the expected verifier layer. Final integrity checks found all 720 v10 manifest members and all 34 R4 output-manifest artifacts unchanged. Matched-query evaluations remain zero.

Research status remains **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**. The common result is PASS_ON_SUPPLIED_TUBE; no safety certificate was emitted.

## Scope and controls

- Read the R5 assignment, AGENTS.md, all four canonical research-context files, R4 review/handoff, method contract v2, native replay checker, R4 worker, common tube checker, v10 snapshot, proof/evidence, selected input and output manifest.
- Kept R4 proof/evidence, source snapshots v8–v10 and R4 output manifest read-only. No producer run, analytic-fixture run, matched batch, G3/controller/hardware activity, gate change, commit or push occurred.
- Fixed case: state_low_neg__scene_d020_l-200__T_020__V_m1_m1; T=1/50; V=(-1,-1).
- Common and composition JSON copies under the R5 inputs folder were extracted from the hash-bound R4 evidence. The R4 evidence itself was not rewritten.
- The v10 tree contains Python cache artifacts. All 720 manifest-listed files, including any listed cache member, were verified. V11 copied all listed members and omitted only unlisted generated .pyc/__pycache__ extras.

## Source crosswalk

| Obligation | Frozen implementation | Action |
|---|---|---|
| Native proof replay | validation/baselines/auer2013/replay_ivp.py, replay_native_proof | Rebuilds proof premises from stored envelope bytes, fixed case/benchmark/profile and source bindings; checks proof digest, action, residual iterations, inclusion, all 21 coordinates, endpoints and complete [0,T] coverage. Does not import the producer. |
| Proof-to-common adaptation | validation/scripts/verify_auer_composition_replay_v1.py | Builds segments from replay-validated slabs, all nine physical coordinates/endpoints and the complete twelve-label image; radius expansion count is zero. |
| Collision/contact predicate | validation/g4/common_tube.py, check_tube_segments | Recomputes margins, segment digest, input hashes, status and both false certificate/replay flags. |
| Composition verification | validation/scripts/verify_auer_composition_replay_v1.py | Constructs expected composition from replayed proof and recomputed common result, then compares every stored field and reports the first differing path. |
| Fixed resources | validation/configs/auer_r5_composition_replay_profile_v1.json; existing validation/baselines/auer2013/process_limiter.py | Each verifier child ran under a Windows Job Object with a 1,024 MiB process cap and 120-second timeout. |
| Frozen sources/protocol | Source snapshot v11; validation/baselines/auer2013/R5_COMPOSITION_REPLAY_PROTOCOL_v1.md | V11 was verified before and after replay. V10 and the complete R4 output manifest were checked read-only. |
| Mutation runner | validation/scripts/run_auer_composition_mutation_trials_v1.py | Creates separate artifact copies and records input/report/stdout/resource/source hashes and commands. |

**Arithmetic dependency:** the native checker uses separate local AD/RHS replay and does not import the producer, but shares validation.g2 exact Fraction/Interval/Budget and Taylor sine/cosine arithmetic. The common predicate reuses validation.g4.common_tube. This is stored-artifact replay with shared arithmetic, not an independent arithmetic-library implementation.

## Exact commands

Run from the repository root in PowerShell using the frozen Python runtime:

    & 'C:/msys64/ucrt64/bin/python.exe' validation/scripts/create_auer_source_snapshot_v11.py

    & 'C:/msys64/ucrt64/bin/python.exe' validation/scripts/verify_auer_source_snapshot_v11.py --snapshot results/validation/g4/auer2013/r5_composition_replay_v1/source_snapshot_v11 --expected-manifest-sha256 d6ed85d98f630889912e30baaf00314ac4069c4dc846525c639832c64ff959eb --output results/validation/g4/auer2013/r5_composition_replay_v1/source_integrity_v11_pre_replay.json

    & 'C:/msys64/ucrt64/bin/python.exe' validation/scripts/run_auer_composition_mutation_trials_v1.py --workspace-root 'D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety' --r5-artifact-root 'D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety\results\validation\g4\auer2013\r5_composition_replay_v1' --r5-snapshot 'D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety\results\validation\g4\auer2013\r5_composition_replay_v1\source_snapshot_v11' --r5-snapshot-manifest-sha256 d6ed85d98f630889912e30baaf00314ac4069c4dc846525c639832c64ff959eb

    & 'C:/msys64/ucrt64/bin/python.exe' validation/scripts/verify_auer_source_snapshot_v11.py --snapshot results/validation/g4/auer2013/r5_composition_replay_v1/source_snapshot_v11 --expected-manifest-sha256 d6ed85d98f630889912e30baaf00314ac4069c4dc846525c639832c64ff959eb --output results/validation/g4/auer2013/r5_composition_replay_v1/source_integrity_v11_post_replay.json

The runner called the verifier once on pristine artifacts and once per mutation. Every complete child command and output path is retained in trial_ledger_v1.json.

## Hash ledger

| Artifact | SHA-256 |
|---|---|
| V10 snapshot manifest | 29ca0f22791ccc740ef377b232522dee88bbaf00367213bfc45cc07925c5bcd5 |
| R4 output-artifact manifest | 6a8d5501972cbb1351cb9ea09500427cb37f8b30c37673ee9e573e156ab6b1a7 |
| Selected input | 3176cdc76861314cb6aaff1f47304ab61b8fd7040270f0504e45498e05b5bd76 |
| Benchmark | b2bc12cd578229cfb6df4b426f93e0f472d69f6be36929df93e797ff79396a9e |
| R4 resource profile v2 | 539c59734fb949e4eab2d71ea0761dcd1032bf6ae92fa17fac53e520462a2cc4 |
| Method contract v2 | 2a5d74de613ccf5f716035732b31ee1dcca69ad3d11d45d1d1267a517a63fc63 |
| Arithmetic backend manifest v2 | 254b448b5458fb9f9ebcd84e9a4e03cc7251124d3241ad00f4626aba7bcef085 |
| R4 native proof file | 8d394d836c5b92b733403b16b1786cb7fe410ab8fb8610c694c0a7c88e5dde4e |
| R4 canonical proof-body digest | 4e49a66b69d869758f28ecfdba84eccefde4e38d8a1fa4f70d3c6e3f2701be70 |
| R4 evidence | e05945b62bf058b76a121c32d316184e577158d3fc7789a6bfed1356c354ec4a |
| R5 common-record copy | 1df9c6d5c146e96ca8e693542573f30c534b7e1428c0bbedbfb5fec421a53482 |
| R5 composition copy | 06386fd01a20503deb233817ac01f3359c2dbc6293a09e008030fab04249fb36 |
| R5 profile | 4b0fa779b67c3a5dff3a38b8909b6246264f66f7039c34157cdf3828fe4e6851 |
| R5 verifier source | 6ee77141052c8281a3b56d691dca46cf90141a3a24677f5b2db3e6b42f8d3fba |
| R5 mutation-runner source | 93b208a41079743cd613403a6455bf824dfb76b2ec7f00b09b1d4822cd1679ef |
| R5 protocol | 2e6421baa131518f8804174f35f0aab0561afe73195bc6177aa9c6f005f07384 |
| V11 snapshot manifest | d6ed85d98f630889912e30baaf00314ac4069c4dc846525c639832c64ff959eb |
| Pristine replay report | 66ff923d3fe037eae0a96f5a33381ff9a9a1994121cbd0232d0d1cb0c174e84f |
| Pristine Job Object record | 797ba26ba6123417b0fd66c317d718e21c239fe8e52f7560b21a0e7852b7fe1e |
| Mutation/trial ledger | fb319214ea01503108427e4e0925b6cac14d26ffa05a532d50f0052ced5eb4fb |
| Final R4 integrity check | e410b92a35cdf6be574ada73b1677cc4734293bb86b4fb514f70a03f2fd5e620 |

The versioned R5 output registry is results/validation/g4/auer2013/r5_composition_replay_v1/r5_artifact_manifest_v1.json with its .sha256 sidecar. It hashes this handoff and the R5 sources, copied inputs, reports, trial files and records.

The full per-trial ledger includes each original/copied-input SHA-256, report SHA-256, stdout SHA-256, resource-record SHA-256, exact first mismatch, expected/actual reason, exit status and verifier command.

## Pristine replay

Report: results/validation/g4/auer2013/r5_composition_replay_v1/pristine_replay_report.json.

- Verifier: **PASS**.
- Native replay: **PASS**, 1 accepted slab, all 21 coordinates, 39,081 rational operations, maximum observed width 300 bits, 4 RHS/Jacobian evaluations.
- Common predicate: **PASS_ON_SUPPLIED_TUBE**, one segment over exactly [0, 1/50], NATIVE_TOTAL_HULL, expansion count zero; 2,415 operations under the fixed 1,799,969 cap.
- Recomputed segment digest: 298ca8c7282eb22045644f45131b3e5f65c6990dc184748564d669f809711cf4.
- Recomputed common-check digest: 9b41c31c83ba925a30321b8b1e1c07e2c0046125874beef6a09e161ca86e0cc0.
- Exact collision lower margin: 3217536069938172178905080151780338213 / 85070591730234615865843651857942052864.
- Exact contact lower margin: 97189909371752867237790996600749227846061205518751 / 51922968585348276285304963292200960000000000000000.
- certificate_emitted=false; the common record's ode_tube_proof_replayed=false flag is preserved. The R5 report separately records native replay PASS.
- Matched-query evaluations: 0.

## Stored-artifact mutation results

| Artifact family | Mutation | Rejection reason and first mismatch |
|---|---|---|
| Native proof | Total hull | native_proof_failure — replayed step 0 full-time tube differs |
| Native proof | Residual iterate | native_proof_failure — replayed step 0 Picard iteration 1 differs |
| Native proof | Endpoint | native_proof_failure — replayed DDWMR global endpoint differs |
| Native proof | Proof digest | native_proof_failure — native_proof_digest_mismatch |
| Native proof | Held action | native_proof_failure — replayed DDWMR query/action binding differs |
| Common record | Segment hull | common_predicate_mismatch — $.segments[0].state_hull[0][0].num differs |
| Common record | Endpoint | common_predicate_mismatch — $.segments[0].endpoint_end.state_hull[0][0].num differs |
| Common record | Radius mode | common_predicate_mismatch — stored CENTER_PLUS_RESIDUAL_ONCE, expected NATIVE_TOTAL_HULL |
| Common record | Radius count | common_predicate_mismatch — stored 1, expected 0 |
| Common record | Exact contact margin | common_predicate_mismatch — $.segment_checks[0].contact.margin_lower.num differs |
| Common record | Segment hash | common_predicate_mismatch — stored hash differs from recomputed hash |
| Composition | Native proof digest | composition_mismatch — $.native_proof_sha256 differs |
| Composition | Common-check digest | composition_mismatch — $.common_check_sha256 differs |
| Composition | Segment digest | composition_mismatch — $.segments_sha256 differs |
| Composition | Query ID | composition_mismatch — $.query_id differs |
| Composition | Held action | composition_mismatch — $.held_voltage[0].num differs |
| Composition | Source snapshot digest | composition_mismatch — $.source_snapshot_manifest_sha256 differs |

Each trial used a separate artifact copy outside the manifest-listed R4 files. All 17 reached the verifier and exited with the expected rejection code. All 18 guarded verifier processes (pristine plus trials) reported the 1,024 MiB cap installed and process assignment before resume; maximum peak was 20,291,584 bytes, maximum elapsed time 1.172 seconds, under the 120-second deadline.

## Failed setup attempts and retained limits

Before v11 was frozen, two source-snapshot assembly checks stopped with “v10 snapshot file set mismatch.” Both stopped before creating the v11 target and before any replay or R4 modification. The first check treated unlisted generated cache files as source members; the second excluded cache files that were actually manifest-listed. The final builder verifies every listed v10 member, tolerates only unlisted cache extras, copies every listed member and omits only unlisted cache extras.

The transient command sessions did not retain the exact creator-source hashes or raw stdout for those setup failures. pre_freeze_setup_attempts_v1.json records that provenance gap, normalized diagnostic hash and absence of a resource record. These were setup checks, not proof/predicate runs. All 18 actual verifier runs have source/input/output/resource hashes in trial_ledger_v1.json.

- V11 integrity passed before and after replay: 726/726 members.
- V10 integrity passed: 720/720 members.
- R4 output-manifest integrity passed: 34/34 artifacts. The final integrity record retains the original proof/evidence hashes.
- Branch and HEAD remained luna/g2-validation-v1 / aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46.
- No matched Auer comparison was run; tractability over 1,944 queries remains unknown.
- R5 shows this saved composition is replayable and that the specified stored-artifact mutations are rejected. It does not independently certify mathematical soundness of the verifier implementation, remove shared arithmetic dependencies, establish a matched scientific comparison or validate physical correspondence.

**Final status:** **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED; matched-query count 0.**
