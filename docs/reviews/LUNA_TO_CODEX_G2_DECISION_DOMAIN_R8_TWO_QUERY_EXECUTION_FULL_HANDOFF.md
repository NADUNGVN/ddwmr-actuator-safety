Session: DDWMR | LUNA-G2-SCOPE

# R8 exact two-query execution handoff

**Date:** 2026-10-03  
**Disposition:** `COMPLETED_TWO_ROWS`; both authorized pilot calls were consumed and independently replayed by the read-only stage auditor.  
**Study status:** the separate R5 study manifest remains **800/800 `NOT_RUN`**.  
**Research status:** this is a development diagnostic only. It does not promote G2 or establish a useful voltage-selection rule.

## 1. Authorization and preflight

Read the R8 assignment, R6 execution receipt, Codex R7 review, R6 protocol v2, `AGENTS.md`, and the four canonical `research_context` files before launch. The Codex review decision is `ACCEPT_R7_STAGE_IMPLEMENTATION_FOR_EXACT_TWO_QUERY_RUN`; its exact two-row GO is reflected in the source-bound receipt.

The R8 assignment raw SHA-256 is `3fdd0b4db944c99102a3fa4090a6bbd86e7e0d58691210f3d2904893436026ef`, matching the suffix of receipt run-assignment ID `CODEX_G2_R8_TWO_QUERY_EXECUTION_SHA256_3fdd0b4db944c99102a3fa4090a6bbd86e7e0d58691210f3d2904893436026ef`. `load_stage_context(..., verify_all_sources=True)` and `validate_execution_receipt(...)` passed before launch:

- All **95/95** source-closure entries matched; the R5 predecessor closure and diagnostic context also matched.
- R5 manifest: 800 records, all 800 `NOT_RUN`, no result records; raw SHA-256 `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b`.
- R6 config / manifest / source-closure raw SHA-256 values matched the receipt: `df9fd6647aca54932137a8cc589e588d95f6911a07ef1b70d38f9aa005282d58` / `9d9e9ba3f5448d985de4da5298155f9f5fdd3e191039c627370f1f48fd085cfa` / `df8622ce0515c84846d1504cbd6304807ccac82ce1c69526a3fe9aedac06809a`.
- Receipt status: `AUTHORIZED_FOR_THIS_EXACT_CODEX_RUN_ASSIGNMENT`; receipt raw SHA-256 `eb0ad0dd54554d954ecb6e097277bfc07d131c925777fa9c17931feb48cf0c80`.
- Accepted R7 review raw SHA-256: `4348fdd2716e36999a4cafb28369b7f403fe9f262c3f0e07fa092ac64b4431c4`.
- Runtime was `C:\msys64\ucrt64\bin\python.exe`, CPython 3.12.12, SHA-256 `b5c33df60c2a8421dcf8117a67e848436b5d395c71ec1c0dfd96bad10f441d7f`; the Windows platform binding matched.
- The canonical R6 stage namespace did not exist before launch.

The fixed public runner was invoked once: `validation/scripts/run_g2_decision_domain_r6_stage.py`. No other native query or batch was run. Its captured parent revision is `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`. The R6 source-closure-bound inputs passed again during the post-publication audit. No G4/Auer source was edited; there was no branch switch, commit, or push.

## 2. Fixed rows, results, and replay

Both rows use the same declared initial-state cell, scene, horizon (`T=250 ms`), progress threshold, R3 profile, and parameter image. They are the exact R5 indices 12 and 24 in the predeclared order.

| Order | R5 index | Query ID | Held voltage | Canonical query SHA-256 | Input semantic SHA-256 | R3 result | R3 replay | R2 endpoint replay |
|---:|---:|---|---|---|---|---|---|---|
| 0 | 12 | `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_L0_R0` | `(0,0)` | `d5648569b11c576c8cc0ecb07c5096c21b06fe3a5e849358f254770649465471` | `422afd0448a184f4f67262c6338593c871739b41fb677e8ab1d6b566d18b93ac` | `UNKNOWN` / `VALID_UNKNOWN` | Pass | Pass; safety remains `UNKNOWN` |
| 1 | 24 | `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lp1_Rp1` | `(+1,+1)` | `105a0710185446312933ec8c92922acd1db0f3af0e999d67207ccd70534b4808` | `70301bc5df76aab2dfdb8bef5135592fbf0063af6799b0f0eb119f4873b2cf9a` | `UNKNOWN` / `VALID_UNKNOWN` | Pass | Pass; safety remains `UNKNOWN` |

Each row has `replayed=true`, `record_integrity_valid=true`, and `proof_replay_pass=true` for both R3 and R2. R3 replay used 29,405 checker operations per row; R2 replay used 1,236 per row. R3 records report the shared trusted components `exact Fraction interval primitives`, `parameter-map and model matrix constructor`, and `validated exp/trig/root primitives`; these are disclosed as replay lineage, not a claim of disjoint code bases.

### Why both R3 rows are `UNKNOWN`

Both native records have reason codes `CONTACT_SUFFICIENT_MARGIN_NEGATIVE` and `COLLISION_SUFFICIENT_MARGIN_NEGATIVE`. The replayed sufficient lower bounds are:

| Voltage | Collision sufficient margin lower bound | Contact available lower bound | Contact demand upper bound | Contact sufficient margin lower bound |
|---|---:|---:|---:|---:|
| `(0,0)` | approximately `-0.430722695226` | `0` | approximately `3.268571368324` | approximately `-3.268571368324` |
| `(+1,+1)` | approximately `-0.514757298248` | `0` | approximately `4.345042656703` | approximately `-4.345042656703` |

These are negative sufficient bounds from the certified outer-evaluation records. They mean the R3 inclusion checks did not establish nonnegative collision and contact margins for either held action. They do **not** establish that the underlying trajectory collides, violates the contact model, or is physically unsafe. The exact rational margins are preserved in each `evaluation.json` and bound by its hash below.

The returned R3 work counters were within their configured arithmetic caps: one parameter leaf, one initial-state leaf, one time slab, 29,456 rational-operation attempts, and a 1,000,000-operation / 16,384-bit cap. Maximum completed / pre-operation-estimate bits were 7,867 / 7,868 for order 0 and 7,914 / 7,915 for order 1. Neither row was resource-stopped; `UNKNOWN` came from negative sufficient margins, not a timeout or exhausted arithmetic budget.

### Endpoint-progress evidence and trigger

R2 replay status is `PROGRESS_BOUND_ONLY_SAFETY_UNKNOWN` on both rows. The endpoint record is integrity-valid and replayed, but `task_eligible=false` because safety is still `UNKNOWN` and the sufficient progress lower bound is below the predeclared `1/20` threshold:

| Voltage | Replayed terminal-progress lower bound | Threshold | Threshold met | Task eligible |
|---|---:|---:|---|---|
| `(0,0)` | approximately `-0.377190894528` | `0.05` | No | No |
| `(+1,+1)` | approximately `-0.439829217355` | `0.05` | No | No |

Both are lower bounds only; a negative lower bound does not show that actual endpoint progress is negative. The broader usefulness-study trigger is **false**: the positive-voltage row is neither R3 `CERTIFIED` nor task-eligible with progress at least `1/20`, and the nominal row also has neither result. The numerically less favorable positive-action sufficient bounds are diagnostic only; this pair does not establish a trajectory-level voltage effect or usefulness.

## 3. One-shot intent, overlap, and denominator accounting

The write-once stage intent fixed the denominator at 2 and recorded both rows initially `NOT_ATTEMPTED`. One row intent was then consumed for each exact predeclared input, in order. Each worker output reports `native_call_attempt_count=1`; both row intents have `row_call_cap_consumed=true`; both terminal records say `row_call_cap_consumed=true`. The stage reports 2 consumed calls, 2 returned results, and `COMPLETED_TWO_ROWS`. There was no retry, replacement, or reordering.

Both rows are `development_overlap=true`, `selected_after_r5_unknown=true`, and `independent_test=false`. Each is explicitly linked to its exact R5 study manifest index and hashes shown above. They remain development observations selected after an R5 `UNKNOWN`, not a holdout or independent confirmation. The R5 manifest still contains all 800 rows as `NOT_RUN`; its raw hash is unchanged. Stage summary records `study_manifest_modified=false` and `study_manifest_rows_not_run=800`. The R6 outputs remain only in `results/validation/g2/decision_domain_r6_matched_action_stage_v1/`; they were not inserted into the R5 manifest.

## 4. Resource and publication audit

The run completed below the receipt's limits. Observed values are supervisor measurements; displayed elapsed times are diagnostic, not platform-independent scheduling guarantees.

| Scope | Receipt cap | Observed |
|---|---|---|
| Per-query wall time | 30 s | 0.234 s each |
| Per-query user CPU | 20 s | 0.125 s (order 0); 0.15625 s (order 1) |
| Per-query memory | 1 GiB | 29,290,496 B; 28,942,336 B |
| Per-query stdout / stderr | 4 MiB each | 71,073 B / 0 B; 70,956 B / 0 B; no overflow |
| Whole-stage wall | 75 s | 3.218 s displayed; stage worker 2.109 s |
| Stage process-tree memory | 2 GiB | 89,214,976 B peak; 3 total processes; 0 terminated |
| Publisher | 10 s user CPU, 512 MiB memory, 1 process | 1.109 s displayed; 0.6875 s user CPU; 88,838,144 B peak; one process; completed with exit 0 |
| Published artifacts | 16 files, 64 MiB total, 32 MiB/member | 12 payload files plus `publication.json` (13 total); 441,434 payload bytes; auditor passed caps |

The query jobs were assigned before resume and confirmed inside their Job Objects; both returned exit code 0 and had zero terminated processes. Stage and publisher supervisors completed without overflow. Publication status is `PUBLISHED_COMPLETE`; both row results and the final publication are present. The required read-only auditor was then run once and returned `PASS_READ_ONLY_STAGE_AUDIT`, with `pilot_rows_attempted=2`, `stage_publication_present=true`, and R5 `800/800 NOT_RUN`.

## 5. Artifact and binding hashes

All hashes below are raw-byte SHA-256 unless the row table explicitly says “input semantic”. The publication record binds all 12 payload files by hash.

| Artifact | SHA-256 |
|---|---|
| R8 assignment | `3fdd0b4db944c99102a3fa4090a6bbd86e7e0d58691210f3d2904893436026ef` |
| R6 config | `df9fd6647aca54932137a8cc589e588d95f6911a07ef1b70d38f9aa005282d58` |
| R6 stage manifest | `9d9e9ba3f5448d985de4da5298155f9f5fdd3e191039c627370f1f48fd085cfa` |
| R6 source closure | `df8622ce0515c84846d1504cbd6304807ccac82ce1c69526a3fe9aedac06809a` |
| R5 study manifest | `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b` |
| R6 execution receipt | `eb0ad0dd54554d954ecb6e097277bfc07d131c925777fa9c17931feb48cf0c80` |
| Accepted R7 review | `4348fdd2716e36999a4cafb28369b7f403fe9f262c3f0e07fa092ac64b4431c4` |
| R6 protocol v2 | `65477a96f2a2966577782a13777750e919879e6e692296f9c9f7c1d1745f5013` |
| Pinned Python executable | `b5c33df60c2a8421dcf8117a67e848436b5d395c71ec1c0dfd96bad10f441d7f` |

| R6 publication artifact | SHA-256 |
|---|---|
| `stage_intent.json` | `c7f219a297b71d577c318362123bbd0175593028795aa282aee064f5953ef94a` |
| `stage_summary.json` | `8fdf4303384bb688745219b8e466c05d5093987dcda1442193478795143c3fc4` |
| `stage_supervisor_checkpoint.json` | `2587cba6c910c43cd8002d17ffb2bd9b88b3b8068d6bcbad2820f2d79f324da1` |
| `stage_terminal.json` | `c237076a14ef144b64ea3dd2f44a14c911e27cd63712c0414cdf088218ef13b6` |
| `publication.json` | `3e55c3b967b661f3a3c3b5aa70ae4bc7cf8e9bab463ec484a4e5865f3db5b33d` |

| Row | Intent SHA-256 | Checkpoint SHA-256 | Evaluation SHA-256 | Terminal SHA-256 |
|---:|---|---|---|---|
| 0 | `e1585a513b9a76a506c5952ec5bbc56c48f81d332d8b90dfcd309e54152905f1` | `29bcbcf97c3ec7491dc00636012f3aa279330aec59f528ac3a8bc0e8ee0f7604` | `8d8f48d4c8bd3c6840d09ed32579e3796f81499e58b7a8ed60fba3b825487306` | `9d4efa58c94903031c04ffa84ac6c6b9712f55e29466b931021e36e6326e3e78` |
| 1 | `c533ed2ce4e7890d2faf40a4165203d3a19d6e10e3f282cb5f8430d0347d21ba` | `a7a4426c4c3d837c3bba3820b714bfc3cd003d69da5e4701b50f17d4609d98a2` | `d93419ed11d68082c1f6676468326e88e66913d871c8edf1e37f003076686ece` | `414a20e09586503a5ac103ce99e6b654c8c32931c713259e17b593edcf261064` |

## 6. Disposition for Codex review

The authorized R6 pilot is complete and auditable: 2/2 exact calls returned valid `UNKNOWN`; both R3 records and R2 endpoint records replay successfully; the predeclared broader-study trigger was not met. The two negative sufficient margin sets do not prove collision, contact invalidity, or actual negative task progress. Treat this pair only as selected development overlap. G2, G3, G4, and physical-platform correspondence remain `UNVERIFIED`; overall research disposition remains `HOLD`. Keep the R5 study manifest at 800/800 `NOT_RUN` unless a distinct future assignment authorizes a separate study.
