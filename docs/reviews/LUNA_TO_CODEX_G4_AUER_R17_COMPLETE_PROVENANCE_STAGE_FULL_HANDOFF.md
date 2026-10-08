Session: DDWMR | LUNA-G4-AUER

# G4 Auer R17 complete provenance and stage candidate — full handoff

**Status: source candidate complete; NO-GO.** R17 source/provenance, stage-runner, checker, timestamp and non-query fixture work is prepared for Codex review. No query, method worker/producer, live composition audit, matched stage, GO receipt, later stage, or full batch was run or created. No commit or push was made. G4 remains **UNVERIFIED**; overall disposition remains **HOLD**.

## 1. Candidate lock and exact hashes

| Candidate artifact | SHA-256 of exact bytes |
|---|---|
| `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v17_PROSPECTIVE.json` | `278e5c0dd07625972f2d6ff259dda18bcf2c591e4ec85ef01d89e46ae2127bb7` |
| Manifest `.sha256` sidecar | `a03692e1bb833567b256fcb6fe2bdff5298fb2f87bc3e7dcf362ce21e76ff4ea` |
| `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R17_PROSPECTIVE.json` | `13a522bc76492a34a8a14be0afe6c941a937894b01fe6b061d75cb7cefe83b4b` |
| Source-closure `.sha256` sidecar | `80e0e5046892d48ad61ea40291ab147b1c5457a54d2ca24d2336a4dc6a07a60a` |
| `research/benchmarks/G4_AUER_R17_CONTINUATION_SCHEDULE.json` | `9ad2f811c12d1884dbc7ed3e93c909362e705da21926c6cbbf88c28e3dfbbfd8` |
| Schedule `.sha256` sidecar | `2552125a946ed92eb12688cc0afcaf862fd48fbed02727681110fdfc47d9e755` |
| `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R17_PROSPECTIVE_CANDIDATE.md` | `de1d0fd8c51b2055e5168f93a410dc8f93f565adb448754e0878d360c35d3d5b` |
| `results/validation/g4/auer2013/protocol_v3_r17_candidate/nonquery_conformance_v1.json` | `49bc66b120ace9eadc321653aa52ff69de04c538160833aec2a3b9695949cbe6` |
| Non-query report `.sha256` sidecar | `cd97912d560193cafadce284cadbcb241c0f7e1fc058f0288156fafcc0870c27` |

The candidate manifest is explicitly `INDEPENDENT_REVIEW_REQUIRED_NO_QUERY_AUTHORITY`; execution, worker, and batch-start authority are false. The canonical R17 batch namespace `results/validation/g4/auer2013/protocol_v3_r17_batch` is absent. The canonical receipt `results/validation/g4/auer2013/protocol_v3_r17_candidate/authorizations/r17_continuation_01.json` is absent. The only source-time authorization artifact is a NO-GO template.

The R17 source closure has 525 dependency records: all 501 R16 dependency tuples are preserved with identical path, byte count and SHA-256, plus 24 R17 source/schedule records. The closure intentionally omits the R17 manifest and its own sidecar to avoid a circular digest; the manifest binds the raw closure digest, and each candidate file has a SHA-256 sidecar where required. The non-query report and sidecar are outside the source closure for the same reason: the report records the final closure and manifest identity. Its exact bytes are independently recorded above and validated by the read-only preflight.

## 2. Versioned R17 source pins

The manifest component inventory contains 23 files. Key execution and contract pins are:

| R17 component | SHA-256 |
|---|---|
| R3 common adapter `validation/g4/r3_common_adapter_v3_r17.py` | `cc72eb4b2154b30792db455821495a592f51b6d20767c68bbebda3ed67b07df8` |
| Auer common adapter `validation/g4/auer_common_adapter_v3_r17.py` | `f5fb8df05dc415d359987ce26f22f5fb38ea6ac0fcdb7aa1193370e5dda7a00c` |
| R3 query worker `validation/g4/r3_matched_query_worker_v3_r17.py` | `5890ace1ab41fc1086dd377df1550e11a2624a5704a5776c8a32648315bd8076` |
| Auer query worker `validation/g4/auer_matched_query_worker_v3_r17.py` | `64cf3dea3b10a5471576853955e0babbbd829fd2e1a1f770d9f16b5c3d913daa` |
| Independent composition verifier `validation/g4/verify_matched_composition_v3_r17.py` | `60dd68ec59f27662514569b1b50dc0bf379c5297aa5d4d9692f32089ffd48e0e` |
| Result validator `validation/g4/validate_matched_result_v3_r17.py` | `3ced9276bd50fef3b4e73debbf14eb4dde389e6c127e555ecbd1cdb3aad049fd` |
| R17 source identity `validation/g4/r17_source_identity.py` | `22c2ccebf08ee800dd517f1437928a7f3d0c8dbf1c6459e5a1e7f276f1200715` |
| Result schema `research/benchmarks/G4_AUER_MATCHED_QUERY_RESULT_v3_R17_SCHEMA.json` | `abb243586335719c40eeb95c7eca9042ccd17599deefedcb049abc1b888c32ea` |
| Common-segment five-field schema `research/benchmarks/G4_AUER_COMMON_SEGMENT_PROVENANCE_v3_R17_SCHEMA.json` | `b5dded4adb0009959b9c65c6240bc762c7e58c9eee0878edc25131e91016be9e` |
| Stage runner `validation/g4/batch_stage_runner_v3_r17.py` | `232c17824c358718f2ab0e583e6e951b5416242c7ff283b3a7c6e61e83766c3d` |
| Independent stage checker `validation/g4/check_matched_batch_v3_r17.py` | `982062d69dea7ed03abcb38270572a171df075a8439c65dd4fa5579504dcbff7` |
| UTC/monotonic timestamp helper `validation/g4/batch_timestamp_contract_v3_r17.py` | `5bae6675acab8b93eb05b6265c61893c045b54c7c986115a7c46c691033356cd` |
| Method worker guard `validation/g4/run_matched_worker_guard_v3_r17.py` | `d1775f700d26d3f659d6c9742d193c830d10e992890540c927215ffbe31495ab` |
| Composition audit guard `validation/g4/run_matched_composition_audit_guard_v3_r17.py` | `eea225c59747991b8743bad8eb0adeb4c06beeda8c990902734fdf9739bf8f02` |
| Non-query fixture runner `validation/g4/protocol_v3_r17_nonquery_fixtures.py` | `e879f07168784f9319cbb30f4bd488eba496d58a29146519709cae314e346af1` |
| Candidate builder `validation/scripts/build_g4_auer_v3_r17_candidate.py` | `f06336ccc032f40fdc90d17d6e9520bf440f3afe55dc68b017fc010e2890de90` |

The full 525-path inventory is in the source-closure JSON; every entry was rehashed by the independent R17 preflight. The source closure separately pins the R9 numerical baseline, R16 predecessor, R17 workers/adapters/verifier/checker, schemas, guards, fixtures and builder.

## 3. Provenance contract and source derivation

Every positive R3 and Auer common segment carries all five direct fields and only the compact segment-level source identities:

```json
{
  "native_proof_file_sha256": "<raw proof.json byte digest>",
  "source_snapshot_manifest_path": "results/validation/g4/auer2013/source_snapshot_v9/snapshot_manifest.json",
  "source_snapshot_manifest_sha256": "fe3309d5b17c6d2968c826eaf1a0759c3b9fbf848432b72842fff5b4db726d91",
  "source_closure_path": "research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R9.json",
  "source_closure_sha256": "7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533"
}
```

Each adapter opens and hashes the serialized proof itself. The R3 path replays the stored record before adapting it. The Auer path reopens the proof envelope, checks its embedded semantic digest, checks the legacy native source binding, and reconstructs the total-hull segments. The common segment digest is computed after the provenance is attached. The independent composition verifier independently reconstructs both method paths from proof bytes, checks all five fields on every segment, compares the full segment object, recomputes `segments_sha256`, and recomputes the fixed-label/full-hold common predicate. The R17 schema and code reject any deletion or changed value among the five fields.

**R9 numerical identity remains distinct from R17 execution identity.** The R9 snapshot-manifest SHA-256 is `fe3309d5b17c6d2968c826eaf1a0759c3b9fbf848432b72842fff5b4db726d91`; the distinct R9 source-closure SHA-256 is `7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533`. R3's evaluator/checker, profiles and the Auer solver/replay/method contract/backend remain the historical numerical baseline and native-proof premises. The Auer proof's legacy `binding.source_snapshot_manifest_sha256` is still checked against the R9 **source closure** hash because that is what the historical producer emitted. R17 emits both correct R9 paths and hashes in common segments.

Each R17 result uses schema `ddwmr-g4-auer-matched-query-result-v3-r17`. Its `source_identity` object reports R9 snapshot/closure paths and hashes separately from the R17 manifest, source closure, schedule, actual method worker, actual method adapter, composition verifier, and result schema. `common_adapter_source_sha256` now binds the executing versioned adapter (`cc72...` for R3 or `f5fb...` for Auer); it no longer mislabels the R9 `common_tube.py` hash as the new adapter. The complete R17 closure and actual adapter bytes are also rechecked by the result validator, worker guard, composition verifier and future stage receipts.

## 4. Frozen query ledger and exact R17 Stage 1

The denominator remains **1,944**. Four IDs remain historical consumed strata: R9 carry-in `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`; R11 `state_low_mid__scene_d020_l+000__T_050__V_m1_0`; R15 attempt 1 `state_low_pos__scene_d020_l+200__T_100__V_m1_p1` (R3 UNKNOWN, Auer CERTIFIED); and R15 attempt 2 `state_high_neg__scene_d050_l-200__T_020__V_0_m1` (R3 produced CERTIFIED output but its R15 common provenance stopped class 3 before Auer was invoked). R15 remains **2/10 consumed**; R17 does not retry either ID.

The 1,940 never-attempted IDs are exactly the R16 continuation after removing only the two R15 consumed IDs from the locked R12 order. R17 Stage 1 reuses the first ten never-attempted IDs as a new candidate stage identity:

```text
state_high_mid__scene_d050_l+000__T_050__V_0_0
state_high_pos__scene_d050_l+200__T_100__V_0_p1
state_low_neg__scene_d100_l-200__T_020__V_p1_m1
state_low_mid__scene_d100_l+000__T_050__V_p1_0
state_low_pos__scene_d100_l+200__T_100__V_p1_p1
state_high_neg__scene_d200_l-200__T_020__V_m1_m1
state_high_mid__scene_d200_l+000__T_050__V_m1_0
state_high_pos__scene_d200_l+200__T_100__V_m1_p1
state_low_neg__scene_d020_l-200__T_020__V_m1_0
state_low_neg__scene_d020_l-200__T_020__V_m1_p1
```

All seven groups remain `PROSPECTIVE_NOT_AUTHORIZED` with sizes `10, 34, 96, 450, 450, 450, 450`. No ID substitution, retry, relabeling, cross-version pooling, or auto-advance is permitted. R9, R11 and both R15 attempts remain separate historical strata.

## 5. Stage runner, checker and timestamp contract

`batch_stage_runner_v3_r17.py` has a read-only `--verify-only` mode and a dormant execution mode requiring exactly `--execute-stage r17_continuation_01` plus the canonical later Codex GO receipt. It verifies the receipt and candidate before creating the canonical output namespace. It writes stage/method/audit intents and terminals once; an existing output or intent blocks retries and resume. It uses the existing method and audit guards under their separate 1 GiB/120-second caps.

The external GO receipt schema fixes the manifest, source closure, schedule, all ten ordered IDs, exact resource caps, one-shot rule, and explicit false flags for retry, substitution, auto-advance and full-batch authority. The only checked-in authorization object is `G4_AUER_R17_STAGE_AUTHORIZATION_NO_GO_TEMPLATE.json`; no executable receipt is present.

The runner captures UTC and monotonic stage-start clocks immediately before the write-once stage intent, copies the same UTC start into the terminal, and captures finish UTC plus elapsed monotonic time at termination. The read-only stage checker validates timestamp ordering and intent equality, exact candidate/GO pins, worker result/guard bytes, separate audit reports/guards, attempted prefix and unattempted suffix, method/audit/pair counts, stop ID, partial intents and pre-intent namespaces, and zero retries/substitutions/auto-advance. The non-query fixture exercises the shared stop-accounting and timestamp checks. It does not create a simulated canonical stage or GO receipt.

The resource policy remains 1 GiB and 120 seconds per method worker, and 1 GiB and 120 seconds per separate composition audit. The GO receipt cannot raise these values.

## 6. Non-query proof and interface evidence

The fixture copied these archived R15 proof bytes into `results/validation/g4/auer2013/protocol_v3_r17_candidate/nonquery_fixture_artifacts_r6/` without changing their R15 sources:

| Method | Archived ID | R15 proof SHA-256 | Fixture outcome |
|---|---|---|---|
| R3 | `state_high_neg__scene_d050_l-200__T_020__V_0_m1` | `86d203f88e528e44670a431b5794fa5fe57f8196ac93e15d9b97dd783c93cd14` | Native R3 replay PASS; R17 adapter, result validator and offline composition bundle PASS; common PASS_ON_SUPPLIED_TUBE |
| Auer | `state_low_pos__scene_d020_l+200__T_100__V_m1_p1` | `a0bc4d9d39c91dd4933f0219a27095d40c70fde5769cad13a483232a2ab06858` | Native Auer replay PASS; R17 adapter, result validator and offline composition bundle PASS; common PASS_ON_SUPPLIED_TUBE |

The fixture report records matching source/copy proof hashes, the result/common/guard fixture-file hashes, actual adapter hashes, and the proof-derived `segments_sha256`. It performed 10 rejection probes per method: deletion and alteration of each of the five required provenance fields. All 20 probes were rejected by the independent segment comparison. Its timestamp fixtures accept a valid interval and reject three bad cases: completion before start, start mismatch with intent, and a non-finite elapsed value. The synthetic class-3 stop accounting has one attempted ID, nine unattempted IDs, zero completed pairs, zero retry/substitution, and no partial intent paths.

The fixture invoked only archived-proof native replay, the versioned adapters/result validator, and the offline `audit_artifact_bundle(..., live=False)` reconstruction. It did not invoke a query producer/worker, Job Object guard, live composition audit guard, stage runner, or batch evaluator. The evidence is interface conformance, not a new matched benchmark result.

## 7. Verification performed and preserved evidence

Commands run in the repository root:

```text
python -B -m validation.scripts.build_g4_auer_v3_r17_candidate
python -B -m validation.g4.protocol_v3_r17_nonquery_fixtures
python -B -m validation.g4.check_matched_batch_v3_r17 --verify-only
python -B -m validation.g4.batch_stage_runner_v3_r17 --verify-only
```

Both read-only preflights returned `PASS_R17_PROSPECTIVE_SOURCE_PREFLIGHT_UNSTARTED`, verified all 525 closure entries and the 1,940-ID continuation, and reported the R17 batch namespace `ABSENT`, zero matched query invocations, zero stages and zero GO receipts. The non-query fixture returned `PASS_R17_NONQUERY_FIXTURES`; both method composition reports returned `PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED`. A Python AST parse passed for all 14 new/versioned R17 Python modules and the builder. The three candidate raw hashes and sidecars, and the non-query report hash/sidecar, were independently rechecked after the fixture run.

The immutable R16 candidate pins rechecked against the review values: manifest `14c69e603db726d0cc5967f54c631e2b39721d9d4e7bffeefc8941abcad52426`, closure `5599c5cde9292478b7a5155e3c7db728af9df811ef150d917b1f0d432713149c`, schedule `ce454815b3c052632b222a1085de9d79af3ae603f54434ab8af0e922c6b6c48a`. All 501 R16 dependency path/size/hash records were revalidated. The R15 output inventory hash remains `3cf9d0116a66fd60f7f69f6576dc09c421119f7602b300e78803b62935c24988`.

R15's timestamp discrepancy remains immutable: start and completion both `2026-10-04T08:07:37.307119+00:00`, elapsed `46.671999999991385` seconds. No R9–R16 source, result, authorization, stop receipt or historical timestamp was rewritten. The candidate checker also verified the exact R12 continuation hash `24c65838b62ea6c12d1377f00dd543752ad9090131881a4441b6ce56232cc8ca` and the fixed 1,944 denominator.

## 8. Gate and handoff disposition

**NO-GO; 0 new queries.** The historical ledger remains four consumed IDs plus 1,940 never attempted; R15 remains 2/10 consumed. No GO receipt or R17 batch output exists. This handoff requests independent Codex review of the R17 source closure, five-field per-segment provenance, separated result source identity, runner/checker contract, timestamp wiring and non-query evidence. It grants no stage execution or comparison authority.
