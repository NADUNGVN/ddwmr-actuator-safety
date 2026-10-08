Session: DDWMR | LUNA-G2-SCOPE

# G2 R7 stage implementation preparation — full handoff

**Date:** 2026-10-03  
**Assignment:** `docs/CODEX_TO_LUNA_G2_DECISION_DOMAIN_R7_STAGE_IMPLEMENTATION_PREPARATION.md`  
**Repository / branch / HEAD:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety` / `main` / `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`  
**R6 review read first:** `docs/reviews/CODEX_G2_DECISION_DOMAIN_R6_PROVENANCE_AND_PLAN_REVIEW.md`  
**R5 result review read first:** `docs/reviews/CODEX_G2_DECISION_DOMAIN_R5_ONE_QUERY_RESULT_REVIEW.md`

## Disposition

R7 preparation is complete for Codex source review. The two-row R6 candidate remains **unfrozen and unrun**. No native `run_query`, producer alias, retry, or 800-row batch was executed. The non-query suite passed **22/22** with both producer-call sentinels at zero. The R6 pilot remains **0/2 run**; the immutable R5 study manifest remains **800/800 `NOT_RUN`**. No research gate changed.

**Recommendation:** GO to Codex review of the exact source and non-query evidence; **NO-GO to execute either query now**. The runtime execution receipt is absent and the template remains `NOT_AUTHORIZED`. This R7 assignment authorized preparation only. A later run requires an accepted source review and a separate exact-scope Codex run assignment with a receipt bound to that review, the source closure, both ordered rows, limits, runtime, and stage namespace. The receipt records the existing scoped G2 validation authority by reference; no new verbatim user instruction is fabricated.

## Finding 1 — exact matched rows and study overlap are fixed

**Evidence.** The pair retains the exact R6 IDs and order reviewed at R6. The R6 adapter reconstructed the rows through the reviewed read-only R4 binder and passed both canonical-query and native-input hash checks. The two rows share the state cell, scene, 250 ms horizon, parameter image, R3 profile, and progress threshold; only held voltage differs.

| Stage order | R5 study index | Query ID | Voltage | Canonical query raw SHA-256 | Native input semantic SHA-256 |
|---:|---:|---|---|---|---|
| 0 | 12 | `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_L0_R0` | `(0,0)` | `d5648569b11c576c8cc0ecb07c5096c21b06fe3a5e849358f254770649465471` | `422afd0448a184f4f67262c6338593c871739b41fb677e8ab1d6b566d18b93ac` |
| 1 | 24 | `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lp1_Rp1` | `(+1,+1)` | `105a0710185446312933ec8c92922acd1db0f3af0e999d67207ccd70534b4808` | `70301bc5df76aab2dfdb8bef5135592fbf0063af6799b0f0eb119f4873b2cf9a` |

R5 `UNKNOWN` informed selection of this development pair; it is not a blind holdout. Both IDs overlap the 800-row study universe at indices 12 and 24 and are marked `development_overlap=true`, `selected_after_r5_unknown=true`, and `independent_test=false`.

**Overlap and lineage policy.** Keep the full study denominator at 800 and retain indices 12/24. Exclude both from any held-out or confirmatory subgroup and report them separately as development overlap. For exact query hashes under the identical accepted executable/source closure, reuse each R6 record at its study index once; never count the same evaluation once as pilot and again as a new independent observation. If query, checker, evaluator, runtime, profile, or resource identity differs, a later study may evaluate that row once under its own one-shot identity, but must disclose the repeat and lineage; do not silently replace, pool, or double-count. A 798-row confirmatory subset may be reported only as a subset while keeping the 800-row denominator visible. The R5 manifest's `800/800 NOT_RUN` describes that immutable artifact and does not mean the project has never evaluated the overlapping inputs.

**Consequence.** Even a replayable CERTIFIED/UNKNOWN contrast can support only a local development diagnostic. The predeclared trigger for a broader matched-action study is positive voltage `CERTIFIED`, task-eligible, with the replayed progress lower bound meeting `1/20`, while nominal zero is not certified or not task-eligible at the same threshold. This is a study-design trigger only. Two UNKNOWNs, malformed/incomplete records, invalid replay, resource stop, identical task-eligibility outcome, or loss of the positive-action safety certificate stops the usefulness claim for this pair. No result is inferred before the two rows are run under a future assignment.

## Finding 2 — source-bound implementation, manifest, and receipt package

**Evidence.** The stage uses a fixed no-argument public CLI, exact-row adapter, one-shot two-row runner, Windows Job Object supervisor, private single-row worker, read-only auditor, and non-query fixtures. Write-once stage/row intents, checkpoints, evaluations, terminals, summary, and publication are kept in the dedicated R6 namespace. A row intent consumes its allowance; duplicate namespace/intent is rejected. Worker exceptions, malformed/partial output, resource stops, and incomplete publication remain distinguishable. A normal row `UNKNOWN` is retained and does not suppress the already-ordered second row; a hard first-row failure leaves row two explicitly `NOT_ATTEMPTED_STAGE_ABORTED` in fixed-denominator accounting.

The R6 source closure contains **95 entries**: the **74 R5 predecessor dependencies unchanged byte-for-byte**, followed by **21 R6/R7 dependencies**. The six R5 diagnostic/erratum artifacts are separately pinned. The closure also pins the exact R6 protocol/config/manifest, executable and transitive G2 sources, receipt/schema artifacts, config and manifest sidecars, Windows runtime, and resource guard. `load_stage_context(..., verify_all_sources=True)` passed after closure regeneration and checked every source hash, the unchanged 74-entry prefix, exact rows, candidate sidecars, and all 800 R5 records.

The execution receipt schema and template bind the ordered rows, raw/semantic candidate hashes, all resource limits, runtime, code hashes, namespace, accepted R7 review, and a unique Codex run-assignment ID. The template remains `NOT_AUTHORIZED`; the runtime receipt and accepted R7 review file do not exist. A read-only receipt-gate check failed closed with `SOURCE_FILE_MISSING:research/benchmarks/G2_DECISION_DOMAIN_R6_STAGE_EXECUTION_RECEIPT_v1.json`. No stage directory was created.

## Finding 3 — Windows process-tree/resource guard

**Evidence.** Query workers are created suspended, assigned to a Windows Job Object, checked as members, then resumed. Each query Job Object limits the active process count to one, sets process and job memory limits, enables kill-on-close, and disallows breakaway. The stage coordinator is supervised from the public CLI under a Job Object with a two-process limit; its query worker runs in a nested one-process Job. The publisher runs afterward in a separate one-process Job. One monotonic 75-second deadline is shared from stage-intent creation across the stage coordinator and publisher; the parent passes only the remaining budget to the publisher. If the deadline expires before publication, the stage is left incomplete and cannot be retried. Receipt/source preflight is before stage intent and outside that execution timer.

| Resource | Candidate cap | Enforcement / evidence |
|---|---:|---|
| Native calls | 2 total; 1 per exact row | Fixed two-row worker loop plus exclusive intent and consumed namespace |
| Per-query wall | 30 s | Out-of-job parent polls and terminates the query Job Object |
| Per-query CPU | 20 user-CPU s | Job Object user-time quota plus parent polling every 5 ms |
| Per-query memory | 1 GiB | Job process and job commit limits |
| Query process tree | 1 active process; no breakaway | Job active-process limit; nested stage tree cap is 2 (stage + worker) |
| Stage wall | 75 s through replay and publication | Shared monotonic deadline across separately guarded stage and publisher processes |
| Stage process-tree memory | 2 GiB | Stage Job Object process and job commit limits |
| Publisher | 1 process; 10 CPU s; 512 MiB; 256 KiB stdin | Separate publisher Job Object plus parent input-size rejection |
| Worker stdin | 16 MiB | Rejected before process creation if exceeded |
| Query stdout/stderr | 4 MiB retained prefix per stream | Separate drains, prefix hash and byte count; kill on first observed crossing chunk |
| Stage-supervisor stdout/stderr | 64 KiB per stream | Same bounded drain and kill behavior |
| Published artifacts | 16 files; 64 MiB total; 32 MiB/member | Write-once publisher premeasures; auditor rechecks file set, hashes, and caps |

The Windows fixtures confirmed assignment-before-resume; process membership; max-one-process rejection of ordinary descendants and `CREATE_BREAKAWAY_FROM_JOB`; nested stage/worker Job behavior; a 20-second sleeper killed under a reduced 0.35-second wall cap with no active Job member; a reduced 96 MiB commit cap rejecting a touched 512 MiB allocation; a 0.35-second CPU quota terminating a burner within the fixture's 0.1-second accounting tolerance; and stdout and stderr overflow handling with exactly 1,024 retained bytes and a prefix digest under reduced 1 KiB caps. Artifact fixtures reject member, total-byte, and file-count overflows. These are Windows implementation tests, not a platform-independent scheduling theorem.

**Limit.** A Windows Job Object does not sandbox arbitrary host filesystem writes. The stage/publisher artifact cap applies to the supervisor-owned R6 namespace and publication writer. The sealed worker receives no stage-output destination and the pinned worker code performs no stage artifact writes. Output hashes cover the retained prefix and observed crossing chunk only; discarded pipe tails are not claimed as preserved. A forced termination can leave incomplete records/publication; those consume the intent and never enable retry.

## Finding 4 — non-query fixture and validation results

**Evidence.** Fixture report: `results/validation/g2/decision_domain_r6_stage_preparation_v3/nonquery_fixture_report.json`, raw SHA-256 `23fc1c2a31ea90a6003796d8af18d4052a487d10550d2945018ff1c5475205f7`; sidecar SHA-256 `e5a01f4b5b60963fee5ea60ce8e9a29e02f4f6e20a178535c3948422ac58a76d`. The report records **22/22 pass**, `native_run_query_calls=0`, `native_producer_alias_calls=0`, no stage execution, and pilot rows 0/2. Covered cases include exact ID/canonical/native-input hash drift; source drift; UTF-8 text and receipt round-trip; missing execution receipt fail-closed; duplicate namespace/intent and no retry; reduced-cap probes for timeout, child kill, process-tree/breakaway, nested Jobs, CPU, memory, stdout/stderr; staged artifact caps; malformed/partial records; two UNKNOWNs; one valid plus one invalid; fixed denominator; and incomplete-stage publication with both unattempted rows explicit. Earlier v1/v2 fixture reports are retained as intermediate runs; v3 is the report bound to the final closure.

The read-only auditor CLI rejected the absent stage namespace with `REJECTED_READ_ONLY` / `R6_STAGE_NAMESPACE_MISSING`, as expected; it did not call a producer. The pinned runtime observed for source binding is CPython 3.12.12 at `C:\msys64\ucrt64\bin\python.exe`, SHA-256 `b5c33df60c2a8421dcf8117a67e848436b5d395c71ec1c0dfd96bad10f441d7f`, on Windows 11 build prefix `Windows-11-10.0.26200-SP0`.

Fixtures establish contract and Windows guard behavior only. They are not query results, R3/R2 certificate evidence, or evidence of voltage usefulness. The incomplete-stage publication fixture calls the publication/accounting helper against a temporary namespace; it does not launch the private `--internal-finalize` mode under its production Job Object or exercise the two-phase shared deadline end-to-end. The end-to-end R6 public runner was not invoked because the required execution receipt and accepted Codex review are absent. Codex should review this remaining process-level gap before issuing any run assignment.

## Finding 5 — R5 and shared-tree preservation

**Evidence.** R5 config `8e2816468bf682290a91535857f2c3f9ad4ff2ba8be99ec5c77acc0ca19a6e19`, R5 manifest `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b`, and R5 source closure `53a923a0be15bd9be977040b996dc2104a763a061e2bad9ef848241a530a55e9` remain pinned. The R5 manifest still has exactly 800 records, all `NOT_RUN` with no result records. The R5 receipt hash remains `5672096c8c3c636dd51bef77f109bc7496cb410dfb82b49a00aa776ae51d62d0`; its provenance defect was not repaired. All **9/9** files listed in the R5 `COMMIT.json` were rehashed and matched; `COMMIT.json` raw hash remains `2b6f6b1bab90a072998e94ae2f5df2d871bd925715540471a838a01bb0cb8756`.

The R6 namespace `results/validation/g2/decision_domain_r6_matched_action_stage_v1/` does not exist. Branch remains `main`, HEAD remains `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`; no branch switch, commit, or push occurred. The tracked diff list remains the two pre-existing shared-tree files `.gitattributes` and `docs/reviews/G4_AUER_R5_GITHUB_SOURCE_INDEX.md`; neither was edited in this task. No G4/Auer source or manifest was modified.

## Exact R7/R6 candidate hashes

Raw SHA-256 unless a semantic hash is explicitly labeled. The full 95-entry dependency list and each path/hash are in the source-closure JSON.

| Artifact | SHA-256 |
|---|---|
| R7 assignment | `854c40bf3992b115b6f042c34bc0c6137327bd8a13be313a437a1668306a831c` |
| Codex R6 review | `577ca0de6efe262f4ff7f9feed6c1a571948823a2bf8ba5a0aa616c6972b4cb0` |
| R6 full handoff | `7f4bf4a596f0ced8f8a82c5235e5605f95adc7510ff27b051cdc9ce9e04a1aef` |
| R6 protocol candidate v2 | `65477a96f2a2966577782a13777750e919879e6e692296f9c9f7c1d1745f5013` |
| R6 config v1 raw / semantic | `df9fd6647aca54932137a8cc589e588d95f6911a07ef1b70d38f9aa005282d58` / `8087a4a63a4cea0bd5d53a848b4215238b87a4f2eef35e011a6ca3f0e8eb0943` |
| R6 config sidecar | `57d07714ec5a85cb0f3e91a096e0117d4466388ed2645431b6e4795e6e2d2bf4` |
| R6 stage manifest v1 raw / semantic | `9d9e9ba3f5448d985de4da5298155f9f5fdd3e191039c627370f1f48fd085cfa` / `ade8191409155fd666c113a9140e5f870692e8c8c4c41bffa68d36a3dad86951` |
| R6 manifest sidecar | `ad31983b794d2f0ef8f1390f5dc07ff607f8aaf28621fccdc5c35e03011ebf0a` |
| R6 source closure v1 raw / semantic | `df8622ce0515c84846d1504cbd6304807ccac82ce1c69526a3fe9aedac06809a` / `e0b4b3bb16e5d66e81f308b7e5a59b629769f6953a4dfd5de93acbe708c015e9` |
| R6 source-closure sidecar | `b2d032e51e3e1e72a37c5e9b3def6aa79e3a0c80c4c6853b531d3888bf41cba2` |
| R6 execution-receipt schema | `501c5100df360071595cc9598e8c1a679b05df5d7cf76b53d621145433092e40` |
| R6 exact-scope receipt template (`NOT_AUTHORIZED`) | `e6bd01324db2c92a3d1bc2940daa8a6183871d066d069aaa155fa628e84953fa` |
| R6 stage record schemas | `3575cdbdaf504274d4dbc37c262748c8bffbeb2235e7e7e579b66c480e534db3` |

| R6 executable dependency | SHA-256 |
|---|---|
| `validation/g2/decision_domain_adapter_r6.py` | `e0deace94e4e111dc833f8e305b7bf01cd65a36a03797fd14660eea8fe566480` |
| `validation/g2/matched_action_stage_runner_r6.py` | `abf494da370c3396c25aa4431cdfe58bb2719419444a5a2f4870efa465e70dc0` |
| `validation/g2/r6_windows_job_supervisor.py` | `46aa4ba242569024e4279dbe50775d3286813d76407e019fb545feba3fd3a603` |
| `validation/g2/matched_action_stage_auditor_r6.py` | `8ec039edbc2a3d9240a84e525705292054274420e7f85761f78874bdbe74097e` |
| `validation/g2/r6_query_worker.py` | `9d81ef6d84c5c11ff3aceddfa3c408949ef39f8d9bd0d800f451060f245d00ed` |
| `validation/g2/r6_nonquery_fixtures.py` | `444b0b8addb0aca6d31eeea942f5e06b964b09c760793b2498c3cc35d90a9a5c` |
| `validation/scripts/run_g2_decision_domain_r6_stage.py` | `706a52a805c18edddf325c16eaccf7f9bffeb20e248d9727401df3cbbe69eef4` |
| `validation/scripts/audit_g2_decision_domain_r6_stage.py` | `fceae6bfa2e611769c890f6d2c6b2840dcc88fc6bb1fe12f10d8f6865d60eaf9` |
| `validation/scripts/verify_g2_decision_domain_r6_nonquery_fixtures.py` | `e32b0b5b4e56f7c6e3ba9fe5945f81838b0d57556f8a4c8f00e4a22ecaf5d165` |

## Consequence

R7 supplies reviewable implementation and non-query contract evidence but does not resolve G2's general enclosure, practical usefulness, parameter relevance, runtime tractability, recursive-safety, physical-correspondence, or novelty obligations. A result in this one development cell cannot establish a useful voltage selector or G2 PASS.

## Status

**Preparation complete; source not yet accepted; no native stage execution authorized by this assignment.** G1 remains PASS only for the restricted reduced model; G2/G3/G4 and physical-platform correspondence remain UNVERIFIED; overall disposition remains HOLD. Pilot **0/2 run**; study manifest **800/800 `NOT_RUN`**.

## Required action

Codex should review the complete 95-entry closure, exact row binding, receipt gate, Windows Job Object tree, shared wall deadline across stage and publisher, incomplete-publication handling, and 22 non-query fixtures. If accepted, issue a distinct exact R6 run assignment and create a new write-once receipt from the reviewed hashes and limits. Do not mutate this candidate after that receipt is prepared, do not repair/retry R5, and preserve the overlap accounting above. Until that review and run assignment exist, do not call either R6 query.
