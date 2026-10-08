# Luna to Codex - G4 Auer protocol v3 R4 source-blockers full handoff

**Date:** 2026-10-02  
**Input handoff:** `docs/CODEX_TO_LUNA_G4_AUER_PROTOCOL_V3_R3_SOURCE_BLOCKERS.md`  
**Review read first:** `docs/reviews/CODEX_G4_AUER_PROTOCOL_V3_R3_SOURCE_REVIEW.md`  
**Disposition:** R4 source-contract correction candidate assembled for independent review; **not a final freeze**.  
**Research state:** HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.  
**Batch:** **0/1,944**; every candidate row remains `NOT_RUN`; `comparison_run=false`; `query_1_authorized=false`; no commit or push.

## Candidate package

- **Protocol:** `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R4.md`
- **Freeze-manifest candidate v5:** `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v5.json`
- **Result schema:** `research/benchmarks/G4_AUER_MATCHED_QUERY_RESULT_v3_R4_SCHEMA.json`
- **Source closure:** `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R4.json`
- **Transitive import audit:** `research/benchmarks/G4_AUER_MATCHED_TRANSITIVE_IMPORT_AUDIT_v3_R4.json`
- **Auer input/worker/solver/validator/guard:** `validation/g4/auer_matched_query_worker_v3_r4.py; validation/baselines/auer2013/residual_ivp_g4_matched_v3_r4.py; validation/g4/validate_matched_result_v3_r4.py; validation/g4/run_matched_worker_guard_v3_r4.py`
- **Non-query contract fixture:** `validation/g4/protocol_v3_r4_contract_fixture.py`
- **Contract fixture report:** `docs/reviews/G4_AUER_PROTOCOL_V3_R4_NONQUERY_CONTRACT_FIXTURE_REPORT.md`
- **Clean-copy verification:** `docs/reviews/G4_AUER_PROTOCOL_V3_R4_CLEAN_COPY_VERIFICATION.md`
- **Fresh-probe index:** `results/validation/g4/auer2013/protocol_v3_r4_source_blockers_probes/probe_refresh_index.json`

## Candidate identity

| Artifact | SHA-256 |
|---|---|
| Manifest candidate v5 | `735a36130916f4cbbc28924b3f937cd2a5acb70e4e78d28af5d46b5b959d66f4` |
| Protocol | `845aeae78726e5f2c30b4c1fff4dea9dbbb093a8c42765b998670c7561681a27` |
| Result schema | `cefdfafe3a98f56741f8201f12bf31b204755a94e94928c6b6073988927927ad` |
| Source closure | `33ec3437d55136117e9c322ce588458aa484060702e7fb46c579ccb47447762b` |
| Transitive import audit | `4b7cbf8a82cfd71e5596b6b74d40a56acff1b9aedbcbda23e74084bff4333cf7` |
| Auer solver | `eb38a9985955fcfb77e105be8df5718e2902f54fec5f18be8ab85db897f2cd5a` |
| Auer worker | `728119637c0b4da6198dd608d1cfc22dce19a9644d643be3c4974238755d9b14` |
| Shared helper | `12af057d0f21632938f0ce511a012d66163d65818f1dbe9fe74a3900200066f6` |
| Artifact validator | `5aa2525d35a096254d7b911a71dbdfb4bc3de20898b375a1e82ec04b0cc61041` |
| External guard launcher | `710f32bbf6fbab6787ae1892aae31a940ef80fc5d7568b2af03e6efd1dc65d30` |
| Guard profile | `65834637c2d398de5ac819a0245a652034d50158c210a2fe6b2eb2101952d0ae` |
| Probe-refresh index | `fe9eaf4e9a5d44dff0745b987ebe720d2807b9902a17dafdbe2b09eb09444454` |

The new candidate files are additive. Candidate manifests v1-v4 and all v3/R3/R4/R5 historical artifacts remain present and unchanged. The solver source is explicitly a new version, not byte-identical to its predecessor.

## R3 blocker dispositions

### 1. Helper and solver input schema

The shared helper emits `ddwmr-g4-auer-matched-query-input-v3-r4`. The versioned solver calls its explicit schema guard before matched-case processing and accepts that same value. The non-query fixture confirms that the prior `v3-r3` schema is rejected. No IVP solver call was made.

### 2. Matched resource-profile proof binding

The solver seed now receives `resource_profile_path` explicitly. The worker supplies `validation/configs/auer_g4_matched_profile_v3_r4.json` and its exact SHA-256 in the expected binding. Strict native replay still compares the entire binding object. The fixture compares the producer seed against the worker binding and rejects the old `small_case_resource_profile_v2.json` path.

### 3. Auer result/schema key agreement

The worker emits the declared `common_adapter_source_sha256` and no longer adds undeclared `shared_common_source_sha256`. The R4 schema retains root `additionalProperties: false`; the fixture confirms the old extra key is rejected.

### 4. Proof digest and reconstructed query-action validation

Artifact validation reads `proof.binding.input_sha256`, checks the complete expected `proof.binding` (including the matched profile path and hash), and reconstructs `query_action_binding` from the frozen query case. It rejects a missing digest at the binding location, an ambiguous top-level `input_sha256`, a changed profile path, and a mutated action binding. Exact proof-byte and embedded-record digests remain enforced; native replay was not weakened.

### Guard-profile probe-link blocker

The new `g4_equal_resource_guard_v3_r4.json` contains no probe-result paths. Manifest v5 binds the guard profile, final source-closure hash, probe-index hash and each fresh probe output downstream. This avoids a profile -> probe-index -> closure -> profile hash cycle.

## Non-query contract and source checks

The source-shape fixture passed all listed checks. It reconstructed one case ID from the frozen manifest only for schema and metadata inspection, checked all 1,944 IDs statically, and exercised in-memory result shapes for proof-size `RESOURCE_LIMIT`, outer-memory `RESOURCE_LIMIT`, `INVALID_INPUT`, `PROOF_COMPLETE_COMMON_UNKNOWN` and `CERTIFIED` against the R4 schema.

- Matched worker invocations: `0`
- Solver proof calls and native replays: `0`
- Proof/result artifact written by the fixture: `false`
- Trajectory proof produced: `false`
- Fixture report SHA-256: `8159f34f4492a734ac5d9200e88cc72231136a3a3c72e204f41d228182002e8f`

The source closure has **53** exact-byte dependencies. The transitive AST audit reaches **19** local Python modules over **53** edges, with **0** unresolved imports. Clean-copy verification matched **53/53** hashes, compiled **25** Python files, and imported **19/19** reachable modules from the temporary copy. These are packaging/control checks, not mathematical proof evidence.

- Source-closure SHA-256: `33ec3437d55136117e9c322ce588458aa484060702e7fb46c579ccb47447762b`
- Transitive import-audit SHA-256: `4b7cbf8a82cfd71e5596b6b74d40a56acff1b9aedbcbda23e74084bff4333cf7`
- Clean-copy report SHA-256: `57715a8a1d5f83c97a84c3d1972c057ee787f91737addc305ecd3884691f1ccc`

## Fresh 64-MiB memory-only probes

Each prospective worker was created suspended and assigned to a Windows Job Object before resume. Both probe commands requested 256 MiB and received `MemoryError` under the installed 64-MiB process-commit cap. The records bind to the R4 source closure.

| Arm | Limit | Requested | Job peak | Guard | Result SHA-256 |
|---|---:|---:|---:|---|---|
| AUER | 67,108,864 B | 268,435,456 B | 66,387,968 B | PASS | `ec736cbbb7843601f483dc3c12758ac0f355eeda2f0131ae266521a302643743` |
| R3 | 67,108,864 B | 268,435,456 B | 66,666,496 B | PASS | `f00fcdbbbb50acb72e16792ffd31d158e7172ab2e41eccf0814549574c662c6e` |

Probe stdout SHA-256: Auer `c4c9bc0b90bcc7ef88cf994d2ee87884f934c135fa8b151d7418a2e344612068`; R3 `c4c9bc0b90bcc7ef88cf994d2ee87884f934c135fa8b151d7418a2e344612068`. Batch evaluations and matched-query invocations were zero for both arms.

These probes test allocation-failure enforcement for the probe command only. They did **not** execute a matched query, serialize/replay a proof, or measure the full 120-second/1-GiB proof pipeline. That pipeline and actual-query `PeakProcessMemoryUsed` remain unmeasured.

## R3-to-R4 source diff

Hashes and line-count deltas are exact. `+` and `-` report added and removed lines respectively. The Auer solver diff consists of the new input-schema guard, explicit profile-path parameter in the seed binding, extracted action-binding builder, and versioned source text; residual/Picard mathematics is unchanged.

| Artifact | Previous SHA-256 | R4 SHA-256 | + / - lines |
|---|---|---|---:|
| `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R4.md` | `252370f3a90120bb61a286bfe0f844f1f53904a48a16446a1d78a02def1f62e8` | `845aeae78726e5f2c30b4c1fff4dea9dbbb093a8c42765b998670c7561681a27` | +20 / -10 |
| `research/benchmarks/G4_AUER_MATCHED_QUERY_RESULT_v3_R4_SCHEMA.json` | `edfbecfbab3cc6f3713faf04ebb8f864d7f4aadfe0378b028219cff5efb4bdb0` | `cefdfafe3a98f56741f8201f12bf31b204755a94e94928c6b6073988927927ad` | +3 / -3 |
| `validation/g4/auer_matched_query_worker_v3_r4.py` | `18539052484b41350b581c38d31424b8f3913c8f7c2e32370650f57c05e42805` | `728119637c0b4da6198dd608d1cfc22dce19a9644d643be3c4974238755d9b14` | +36 / -25 |
| `validation/g4/r3_matched_query_worker_v3_r4.py` | `8bedaf635c50216e18c981b627622d7ebb099d3eb4166eb8c83f753c034c1e68` | `dd527edc68ac16edffe6cbe4c3ca3769514754566664ead4b49dce6257dd3acb` | +8 / -8 |
| `validation/g4/matched_worker_common_v3_r4.py` | `1e3c56169f1984b79a4213429c35ae2d3609d7bce4895da1fff4f9c6d43d9432` | `12af057d0f21632938f0ce511a012d66163d65818f1dbe9fe74a3900200066f6` | +13 / -7 |
| `validation/g4/run_matched_worker_guard_v3_r4.py` | `f0b3de3bb21270ea669503e9747c765eca78ccb7f7c540a162931d2f4182d40f` | `710f32bbf6fbab6787ae1892aae31a940ef80fc5d7568b2af03e6efd1dc65d30` | +16 / -16 |
| `validation/g4/validate_matched_result_v3_r4.py` | `aa7d8012aaf946891a91e7565e5c40500553c17ae43a40decefc1d990a12ef2f` | `5aa2525d35a096254d7b911a71dbdfb4bc3de20898b375a1e82ec04b0cc61041` | +115 / -18 |
| `validation/baselines/auer2013/residual_ivp_g4_matched_v3_r4.py` | `27384ab4ff74bce48c4459ae6e6da6a573df6587c176b41fcfeccf0d006ba464` | `eb38a9985955fcfb77e105be8df5718e2902f54fec5f18be8ab85db897f2cd5a` | +28 / -15 |
| `validation/configs/auer_g4_matched_profile_v3_r4.json` | `3ace015b3aa5056e0736713d8e850b70918cfe96aec6412ca298f06a9dcc51bd` | `4883ea73ebf5c290a4d17df86860c0e8432b1594b1ff32ca8bef1aaef12a698f` | +11 / -11 |
| `validation/configs/r3_g4_matched_profile_v3_r4.json` | `29e41c43aa774a222440bab878a40a0eefd71fc757070fac33cb642dff8ffccf` | `f65c6558c00ab4c08718e476677c38f2f397b3abf516d125faf609d9f34fcb1c` | +9 / -9 |
| `validation/configs/g4_common_predicate_profile_v3_r4.json` | `52c592d8fd94ba438f4cd678b58753e5372fb341d8410ec32c775336f28ca794` | `dbe8caac70935cbc3df9cc10442746bca12fcb739e5277e1ffb3cbd96a63a582` | +5 / -5 |
| `validation/configs/g4_equal_resource_guard_v3_r4.json` | `7b8bf4b7b28d76f0108c406195985e967ed2d24d7355e4cbe5892a9e648bad5c` | `65834637c2d398de5ac819a0245a652034d50158c210a2fe6b2eb2101952d0ae` | +24 / -36 |
| `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R4.json` | `4e19ddf5f4fdfa28bc47bcd12baf96f82ee1682021f74b28dc375a9098400bf8` | `33ec3437d55136117e9c322ce588458aa484060702e7fb46c579ccb47447762b` | +229 / -214 |
| `research/benchmarks/G4_AUER_MATCHED_TRANSITIVE_IMPORT_AUDIT_v3_R4.json` | `da6b3b7429184ccefa16835659a3cb57a5e8e07da0fcf800c6c9561ed30c7970` | `4b7cbf8a82cfd71e5596b6b74d40a56acff1b9aedbcbda23e74084bff4333cf7` | +113 / -83 |
| `validation/g4/protocol_v3_r4_contract_fixture.py` | new file | `64c9f49621ab41f9b4c329fa0a1461eb871d8bc06a1598ed64a17f718871001c` | +270 / -0 |

The Auer residual/Picard equations, Jacobian, inclusion conditions and proof premises were not changed. R3 evaluator/checker formulae, common-predicate mathematics, and historical R3 v5/R4/R5 proof mathematics were not changed.

## Preserved evidence

The candidate rechecked the listed R3 v5 fixtures, R4 artifacts and R5 composition/replay evidence against the closure and clean copy; none was edited.

| Evidence | SHA-256 |
|---|---|
| `results/validation/g4/auer2013/r3_archived_fixture_selection_v5.json` | `4c6e6becc3a7e165ab3821fe0bf0436b06a79f0c1bb9745fde00e39d5a9db19f` |
| `results/validation/g4/auer2013/r3_archived_adapter_fixture_v5.json` | `1b3a97e171d12585bc8918b819b6b28403467926889dc9c5488786c01c69b92b` |
| `results/validation/g4/auer2013/r4_output_artifact_manifest_v1.json` | `6a8d5501972cbb1351cb9ea09500427cb37f8b30c37673ee9e573e156ab6b1a7` |
| `results/validation/g4/auer2013/r4_ddwmr_single_query_native_v2.json` | `8d394d836c5b92b733403b16b1786cb7fe410ab8fb8610c694c0a7c88e5dde4e` |
| `results/validation/g4/auer2013/r4_ddwmr_single_query_evidence_v2.json` | `e05945b62bf058b76a121c32d316184e577158d3fc7789a6bfed1356c354ec4a` |
| `results/validation/g4/auer2013/source_snapshot_v10/snapshot_manifest.json` | `29ca0f22791ccc740ef377b232522dee88bbaf00367213bfc45cc07925c5bcd5` |
| `results/validation/g4/auer2013/r5_composition_replay_v1/r5_artifact_manifest_v1.json` | `48196f1f3ebb5cf9787c68bc98f6ad88a0678ebd92683014fe877d015f18dd44` |
| `results/validation/g4/auer2013/r5_composition_replay_v1/pristine_replay_report.json` | `66ff923d3fe037eae0a96f5a33381ff9a9a1994121cbd0232d0d1cb0c174e84f` |
| `results/validation/g4/auer2013/r5_composition_replay_v1/source_snapshot_v11/snapshot_manifest.json` | `d6ed85d98f630889912e30baaf00314ac4069c4dc846525c639832c64ff959eb` |

Predecessor manifest v4 remains unchanged at `9a5994399a5296af1671369c7e08b79a96193d0d0037d10fa522fbf48b7146ca`. Earlier manifests v1-v3 are also preserved. The v10/v11 snapshot trees still lack external member-by-member audit; no claim is made that all 720/726 members were externally checked.

## Batch and review boundary

Manifest v5 records 1,944 unique ordered IDs with LF-joined SHA-256 `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`. `matched_query_evaluations=0`; `one_query_worker_invocations=0`; every candidate row is `NOT_RUN`; `comparison_run=false`; `query_1_authorized=false`; batch start is not authorized. No gate status changed.

R4 is a source-review candidate, not a final freeze package. Independent review remains required for the proof implementation and validator before any query. A separately approved one-query guard inspection and later batch-start review remain future gates. The 64-MiB probe evidence does not authorize either action.

No commit or push was made. No matched query or 1,944-query batch was run.

