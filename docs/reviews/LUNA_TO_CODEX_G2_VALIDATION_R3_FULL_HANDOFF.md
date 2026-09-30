# Luna → Codex — G2 validation R3 full handoff

**Date:** 2026-09-30

**Disposition:** R3 development batch complete and archived; **HOLD remains unchanged**. This is Luna's execution and artifact handoff for Codex review, not an independent Codex replay or a promotion of any research gate.

## 1. Scope, branch, and commits

- Repository: `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`
- Branch: `luna/g2-validation-v1`
- Starting SHA: `4df4dfef65a5addb040fbd2f059a62727189cd88`; the branch was clean and matched `origin/luna/g2-validation-v1` at the start of this R3 assignment.
- Evidence end SHA (parent of this handoff report): `28e962ec6e2085656e4dd1b7bc254186835cefb8`. The report is committed immediately after that evidence checkpoint; the final branch tip is returned with this handoff.
- Python: `3.12.12`; Windows 11 AMD64; executable recorded as `C:\msys64\ucrt64\bin\python.exe`.

R3 commits added after the starting SHA:

| Commit | Contents |
|---|---|
| `c7f06727b33775c41b7c841d5c43269467ab217b` | R3 addendum, directed dyadic distance implementation, checker, provenance, regressions, and runner/hash tools |
| `e7fac74d69a5f117045416d688cc808e50ac1a6a` | Frozen R3 profile, unchanged pilot selection, and conditional remaining-ID manifest |
| `ab5fef68a0726b9d49b10c6bbd86f86b297b2efd` | Pre-evaluation specification/source ledger and main R3 manifest |
| `78aba4ddc100eb2fdb5c966e6d124ddac90ac8bc` | Corrected a regression-fixture manifest-field lookup before any R3 evaluator query |
| `667a8e4a5e840ff33e823f353bed8c6328c0a443` | Pilot records, R3 and R2 replay reports, summaries, and pilot hash ledger |
| `266f979a6c2aaf3ca97ead522d18d33633d97e41` | Deterministic gzip archive helper and compressed-record hashing support |
| `28e962ec6e2085656e4dd1b7bc254186835cefb8` | Conditional full-grid results, replay report, transitions, grouped summary, final result ledger, and archive instructions |

The R2 and earlier R3 artifacts were left in their existing paths. The only generated data file removed after verification was the new 147,589,521-byte R3 conditional full-grid JSONL; its exact byte stream is preserved in the committed gzip archive and bound by the archive manifest below.

## 2. Frozen input and source provenance

The ordered specification-content ledger was frozen before evaluation. It hashes immutable Git blob bytes and records each source revision, repository path, Git blob object ID, and SHA-256. All source rows below were recorded at revision `c7f06727b33775c41b7c841d5c43269467ab217b`.

| Source path | Git blob object ID | SHA-256 of Git blob bytes |
|---|---|---|
| `AGENTS.md` | `edb04bf4474dc89022a9b912dc2523e0b884c418` | `d40542cc226351ec13b0adb85e16bc7702d5d1931520cd4ff49ac98b63a23f58` |
| `research_context/MASTER_RESEARCH_CONTEXT_v2.md` | `5a5022cf7870ad42e84773abec873ce29dc4ab32` | `d8158e5e74d9e29d40003d3157b10b1ba22df37ae43e5356eefca1ccec55a58e` |
| `research_context/DECISION_LOG.md` | `039f4f1d4979c4a4a91d6389cd30772fb11a49e9` | `5b50b834a340bfa216497844493a0c69446d6713856a99b9e879eae34b7b2879` |
| `research_context/LITERATURE_MATRIX.md` | `82e6295bef78c45bf57d9b7e8303d2fa2ed153f1` | `56131915ab0c94cff5bc82783f14cacc1de41b6210becd6dc5feb06a18a0c1e3` |
| `research_context/REVIEW_GATE.md` | `00fce47037796e94161ebf2ae13804a966573679` | `2064b826af63abbcabb241810391bc0850c41da6014daefb488307910122640f` |
| `docs/LUNA_VALIDATION_HANDOFF_v1.md` | `c94050f0b84ecae29d434a9ba23f6db8745a8a92` | `d45f5192626904925fef4fc5912ebd99da51b3dce0c9db14a674742eb4a959a9` |
| `docs/CODEX_TO_LUNA_G2_VALIDATION_R3.md` | `2c38a032c00ffbd9b4206c79f8cd5e0229c6b463` | `7cdc90aae09d9f148d3d35851c77e5abb8f6c7ff89721a75ed014196ed2da09e` |
| `research/theorem_notes/G2_FINITE_EVALUATOR_SPEC_v1.md` | `1c66126399af1f893f42acd2ee4f75a7bf2b0f96` | `5b11fe7d9e8f21ff259b86e44e3648f34f56d78410492ca4a7c9b73a43ea7908` |
| `research/benchmarks/G2_USEFULNESS_BENCHMARK_SPEC_v1.md` | `2fb15ccdef3b4710b94900c0b32a840f2c380231` | `a16a55230754a915b21616392ce508a6d7f1abb8694ce4e25933ea1435523912` |
| `docs/LUNA_G2_DISTANCE_ADDENDUM_R3_v1.md` | `ec8ba763e2835ffd7dffbeca7f9ac910300afff2` | `fe730d2bf7e172c781d4f05f5ad7fe4ab6d6e6f5f1f80d657232f5e1a891cc7e` |

The specification bundle SHA-256 is `84b444d0be6e18c946697c3b95662ffd0f30dd228ae7ca5e742cee47d446c850`. Frozen JSON/input commitments are recorded in `results/validation/g2/r3/SHA256SUMS_PRE_EVAL_R3.json` and the final result ledger. Key semantic digests are:

| Object | Semantic SHA-256 |
|---|---|
| Pilot configuration | `7a93c4824b859d8dbc5816c2d7edac005a7a87282399678fc8beebb49192b7b0` |
| Effective profile | `74cd7964c9e6d0f55c24269518034f8fdf0bc7a3124063ec4fb3900b5e8c0295` |
| Main development manifest | `e5c796fcfe8275b1b7106f112813d24b36d18626400ba149f29f4bee7b9c155d` |
| Conditional 1,728-ID manifest | `17cd7eefad56d74a2d487eae90298c6db62775945596a1946980198e52c9fe7a` |
| Frozen selected pilot IDs (LF) | `e6ae1e90775051a579f862b72ac8ee2e97facbdbbe99bc64552e1bcaa37ec9d0` |
| Conditional remaining-ID selection (LF) | `220042c90b0b31278c7900e3518608f611a85cee812bbe04edb8afa7bb464211` |

The frozen pre-evaluation input-file Git-blob commitments (source revision `e7fac74d69a5f117045416d688cc808e50ac1a6a`) are:

| Input | Git blob object ID | SHA-256 of Git blob bytes |
|---|---|---|
| `validation/configs/benchmark_v1.json` | `d3d43627af5b9979604a5a427ae8c64a6c1807f2` | `3d13b1681ba89d54097f61cf59c18581b445531dc9361e9b6f7b0c0fcaf1c306` |
| `validation/configs/dev_pilot_r3_v1.json` | `c33646c864b8d67befc5f9eaa16b35afe1445e95` | `e65507d0f42368fa4366b03e59a8e7b311c258d9766b166fbdf83ac61fdfe52a` |
| `results/validation/g2/r3/full_grid_continuation_manifest_r3_v1.json` | `04f42d6156b99967b7d609288c63b1c9751f4d53` | `ecddff5f5679534bc1204922029e93dc06b84508357b323d2cd218ca876d9dbb` |
| `results/validation/g2/r3/specification_content_ledger_r3_v1.json` | `5ee77c51b35a3bf09a8507e138cc286b7d3f3b8c` | `84928fe65dd788b7248d52e264832e4bcd3ca277633644ba3157cf16fb3efa45` |

The run metadata additionally binds the frozen input-set bundle as `899486281746bc795bb96f655daaf5c08895b5a37dfa1d02b5d35027aa665896`.

The profile ID is `DEV_FALLBACK_N1_PILOT_R3_DYADIC_P24_BITS16384_V1`; the method ID is `G2_COMP_CLIP_WHOLE_HOLD_DYADIC_DISTANCE_N1_R3`; the distance method ID is `DIRECTED_DYADIC_EUCLIDEAN_MIN_DISTANCE_V1`. The pre-evaluation ledger says `frozen_before_any_r3_evaluator_output: true`, with freeze source commit `e7fac74d69a5f117045416d688cc808e50ac1a6a`. The original universe remains 1,944 IDs; pilot selection is the same 216 IDs as R2, with the other 1,728 listed explicitly before pilot output.

Frozen Git-blob SHA-256 commitments for producer and checker source files are:

| Role | Source path | SHA-256 of Git blob bytes |
|---|---|---|
| Producer | `validation/g2/evaluator.py` | `62dd355684c53fdd104ad051d2f06486e256e3489f1a72263a8432b9af9cc26e` |
| Producer | `validation/scripts/run_pilot_r3.py` | `ba564cb1ee10ab095ef58d1c4cbb07313f54359364a97e805e59484ae9f8b8be` |
| Checker | `validation/g2/checker.py` | `b2605941cc2620f19d0c6001736bec8e292b2e0dbb819f043c5dcd44fbc5e526` |
| Checker | `validation/scripts/verify_records_r3.py` | `3f9086221365128f7eee2b583008371a8b27043304a5ee409265320411029e72` |
| Producer and checker | `validation/g2/rational.py` | `8a2c16778b33898afd16c8da44945c2d41fd7d187cb11c7cb071745e68ed5c6e` |
| Producer and checker | `validation/g2/interval.py` | `e49e2e3880485d9a658e2435cfa06b784f98257b13c51fa4a2bf464f9c73e5c6` |
| Producer and checker | `validation/g2/model.py` | `93e9a96d640ad09a7eb7dbff51ebfb8f2d783296ce5afff57af41e81e30a8508` |
| Producer and checker | `validation/g2/hashing.py` | `0d5137359e19c80b20c097d49c8d7246e48effcaef9e3649b142120136c13aab` |
| Producer and checker | `validation/g2/provenance.py` | `8830bb334c459e7b319ee5eb3ada43c5057aef55237f6b46a886b6fc90bfa56d` |

Runtime metadata records pilot producer revision `78aba4ddc100eb2fdb5c966e6d124ddac90ac8bc` and conditional-phase producer revision `667a8e4a5e840ff33e823f353bed8c6328c0a443`. The pilot checker revision is `78aba4ddc100eb2fdb5c966e6d124ddac90ac8bc`; the combined full-grid checker revision is `667a8e4a5e840ff33e823f353bed8c6328c0a443`. Both reports say producer/checker source commitments match the frozen manifest. Both producer runs recorded a clean source tree before evaluation. The later `266f979` commit only added archive and result-hash tooling; it did not change evaluator or checker source.

## 3. R3 distance method and budget

R3 changes only the numerical enclosure for the minimum distance from the existing predictor-position rectangle to a static obstacle center. For exact nonnegative rational coordinate gaps `dx,dy` and fixed `p=24`, it forms

```text
dx_lower = floor(2^p dx) / 2^p     dx_upper = ceil(2^p dx) / 2^p
dy_lower = floor(2^p dy) / 2^p     dy_upper = ceil(2^p dy) / 2^p
a_lower = dx_lower^2 + dy_lower^2  a_upper = dx_upper^2 + dy_upper^2
```

Exact monotonicity gives `a_lower <= dx^2 + dy^2 <= a_upper`. Validated rational root brackets on these radicands give `l <= d <= h`, where `[l,h]` encloses the rectangle's minimum distance. The collision sufficient lower margin remains `l - R_s - E_p`. The upper endpoint `h` is not an upper bound on every trajectory-to-obstacle distance. Coordinate rounding loss is bounded separately by `sqrt(2) 2^-p <= 2^(1-p)`; square-root bracket width remains separately represented.

Floor/ceiling uses exact numerator shifts, integer quotient/remainder, a conditional increment, and rational construction. Shifts, divisions, increments, squaring, sums, and root bisection all use the same budget guard. There is no floating safety arithmetic, cap increase, or bypass. The R2 profile caps and other settings remain fixed: **16,384 rational bits, 1,000,000 rational operations, 15 seconds/query**, Taylor degree 16 for `exp`, degree 18 for trigonometric ranges, comparison order 16, one predictor step, one whole-hold hull, and 24 square-root bisections. Unknown method variants are rejected. R3 stores and checks gap bounds, radicands, root brackets, precision, margins, query/voltage binding, and status.

## 4. Results and conditional continuation

The pilot continuation rule was frozen before output. The 216-query pilot had no resource-limited, invalid, or execution-failure record; every completed proof replayed, and hashes/provenance passed. `dev_pilot_record_check_r3_v1.json` reported `continuation_allowed: true`. The one permitted conditional continuation therefore ran all 1,728 remaining original IDs exactly once under the same profile.

| Phase | Evaluated IDs | `CERTIFIED` | Completed-proof `UNKNOWN` | Resource `UNKNOWN` | Invalid / execution failure | `NOT_RUN` after phase |
|---|---:|---:|---:|---:|---:|---:|
| Pilot | 216 | 126 | 90 | 0 | 0 | 1,728 before continuation |
| Conditional remaining IDs | 1,728 | 1,070 | 658 | 0 | 0 | 0 |
| Combined original universe | 1,944 | 1,196 | 748 | 0 | 0 | 0 |

The full-grid checker validated exact 1,944-ID coverage and replayed **1,944/1,944 completed proofs**. It reported `all_pass: true`, record integrity, frozen input hashes, specification blob commitments, producer/checker provenance, and metadata bindings all passing; there were zero resource-only records. Its `continuation_allowed: false` field means continuation is no longer applicable after the single permitted run (`NOT_APPLICABLE_AFTER_SINGLE_CONTINUATION`), not that the pre-run pilot condition failed.

R2's same 216 selected IDs had 54 `CERTIFIED`, 54 completed-proof `UNKNOWN`, and 108 resource-limited `UNKNOWN`. The R3 transition table reports 54 `CERTIFIED → CERTIFIED`, 72 `UNKNOWN → CERTIFIED`, and 90 `UNKNOWN → UNKNOWN`. The 1,728 IDs marked `NOT_RUN` in R2 transition to 1,070 R3 `CERTIFIED` and 658 R3 `UNKNOWN`. The old R2 checker was replayed separately against its original records and hashes: 54 positive and 54 inconclusive proof replays passed; the 108 proofless resource records received integrity checks only. Its report remained under the new R3 result directory.

For the combined 748 proof-complete `UNKNOWN` records, the sufficient-margin reason codes occurred 405 times for collision and 636 times for contact (some records have both). A negative sufficient margin means the encoded sufficient test did not certify that query; it is not a collision finding or an unsafe-action conclusion.

Action-group summary by the 216 state/scene/horizon groups (nine actions per group):

| Group outcome | Count |
|---|---:|
| All nine actions `CERTIFIED` | 132 |
| All nine actions `UNKNOWN` | 76 |
| Mixed: one `CERTIFIED`, eight `UNKNOWN` | 8 |
| Groups with at least one `CERTIFIED` action | 140 |
| Groups with at least one `UNKNOWN` action | 84 |
| Resource-censored actions | 0 |

All 216 groups have action-varying exact collision-margin and contact-margin ranges; the per-group rational minima and maxima are in `full_grid_action_group_summary_r3_v1.json`. The pilot subset alone had 24 groups: 14 with at least one certified action, 10 all-unknown, and no mixed-status group. This records some certificate-status separation in the full development grid, but does not establish useful voltage selection, action necessity, unsafety of UNKNOWN actions, or recursive feasibility.

## 5. Responses to R3 review findings

### R3-01 — corrected radius and completed proof path

The existing R2 radius recurrence/regression was retained. R3 adds the fixed-precision dyadic enclosure and serialized witnesses described above. Exact tests cover zero and exactly dyadic gaps, non-dyadic fractions, one/two nonzero gaps, zero/positive/negative margins, bit and operation limits, full proof replay, and mutations of directed endpoints, witness shape, precision, query/voltage, margin, and status. The completed R3 pilot and grid proofs all replayed. This resolves the R2 distance-stage completion issue for this frozen batch only; it is not a general soundness proof.

### R3-02 — reproducible counts and hashes

The pilot record semantic SHA-256 is `fdbce2ac5587247ababc0849c5fce8f9a596c3eb2175ed277545072c06acdc43`. The conditional remaining record semantic SHA-256 is `de339ffcb5ee5e0c83f8d25e3077d9fd9316f83293982189aaffba0bdcf3b196`. `SHA256SUMS_RESULTS_R3.json` has 21 entries. A separate recalculation of canonical JSON/JSONL semantic hashes, raw-byte SHA-256 values, and byte sizes matched **21/21** entries.

The raw conditional JSONL was 147,589,521 bytes, larger than a common Git-hosting single-blob limit. After the full checker completed, the file was archived losslessly as `conditional_full_grid_records_r3_v1.jsonl.gz` (34,613,266 bytes). The archive raw-byte SHA-256 is `352b6c67480133350a7d1bfc89334a1beff1dc27c64cfda46391af27982fa874`. Decompression matched the original raw byte SHA-256 and size; both the raw and canonical semantic digest are `de339ffcb5ee5e0c83f8d25e3077d9fd9316f83293982189aaffba0bdcf3b196`. `conditional_full_grid_archive_manifest_r3_v1.json` maps the compressed artifact to the runner's original logical `.jsonl` path and records the 1,728 rows, sizes, hashes, deterministic gzip settings, and archive tool revision. To replay the full-grid checker again, decompress the `.jsonl.gz` to that logical `.jsonl` path first.

### R3-03 — action/status variation

The full grid has eight mixed groups, each with one certified action and eight inconclusive actions. Every group also stores exact action-wise collision/contact margin ranges; all groups have varying ranges. This is descriptive certificate variation, not a demonstrated useful policy or comparison against a validated external method. Decision relevance remains unverified.

### R3-04 — localized arithmetic bottleneck

No resource-limited result occurred in the 1,944-query R3 grid under the unchanged R2 caps/settings. The targeted bounded distance representation completed this frozen batch without cap tuning. This demonstrates computational completion for this profile and input set; it does not establish broad efficiency or physical feasibility.

### R3-05 — specification and checker provenance

The new R3 schema uses explicit `specification_bundle_sha256` and `input_configuration_bundle_sha256`; historical R2 `specification_sha256` semantics and R2 artifacts were not rewritten. The frozen Git-blob specification ledger binds the governing Markdown contents. Producer and checker revisions and their source-file commitments are recorded separately, including the compatible later replay of the pilot outputs. Runtime metadata records actual argv, executable, Python version, platform, working directory, source revision, frozen hashes, and pre-run tree state. Producer/checker share exact rational and interval operations, parameter-map/model construction, validated exponential/trigonometric/root primitives, and query/profile parsing; these shared components remain in the trusted base.

## 6. Executed checks and run record

Commands and observed results:

| Command | Result |
|---|---|
| `python -m compileall -q validation` | Passed during implementation |
| `python -m validation.verification.verify_primitives` | 26/26 passed |
| `python -m validation.verification.verify_radius_series_r2 --check-only` | 15/15 passed |
| `python -m validation.verification.verify_hand_cases` | 32/32 passed |
| `python -m validation.verification.verify_pilot_positive_tamper_r2 --check-only` | Passed; existing positive/nonzero-radius replay and mutation checks retained |
| `python -m validation.verification.verify_hash_protocol_r2 --check-only` | Passed |
| `python -m validation.scripts.generate_manifest_r2 --verify` | Passed |
| `python -m validation.verification.verify_proof_pipeline_r2 --check-only` | Historical partial fixture remains resource-limited: safe positive fixture estimate 42,448 bits against its frozen 32,768-bit cap. It was run check-only; no cap was raised and no historical artifact overwritten. This is not an R3 pilot failure. |
| `python -m validation.verification.verify_bounded_distance_r3` | 25/25 R3 arithmetic, budget, replay, and tamper checks passed |
| `python -m validation.scripts.run_pilot_r3 --phase pilot` | Completed 216 frozen records |
| `python -m validation.scripts.verify_records_r3 --phase pilot` | `all_pass: true`; 216/216 IDs; proof replay and provenance passed; continuation allowed |
| `python -m validation.scripts.verify_records --records results/validation/g2/r2/dev_pilot_records_r2_v1.jsonl --metadata results/validation/g2/r2/dev_pilot_run_metadata_r2_v1.json --report results/validation/g2/r3/r2_compatibility_record_check_r3_v1.json --benchmark validation/configs/benchmark_v1.json --pilot validation/configs/dev_pilot_r2_v1.json --manifest results/validation/g2/r2/development_manifest_r2_v1.json` | R2 compatibility report `all_pass: true`; 54 positive + 54 inconclusive proofs replayed, 108 resource records integrity-checked, exact coverage and old hashes passed |
| `python -m validation.scripts.run_pilot_r3 --phase conditional-full-grid --pilot-checker-report results/validation/g2/r3/dev_pilot_record_check_r3_v1.json` | Completed all 1,728 remaining IDs; 1,070 `CERTIFIED`, 658 completed-proof `UNKNOWN` |
| `python -m validation.scripts.verify_records_r3 --phase conditional-full-grid` | `all_pass: true`; exact 1,944 combined IDs; 1,944/1,944 proof replay; zero resource/invalid/failure; provenance and hashes passed |
| `python -m validation.scripts.archive_records_r3 --remove-source-after-verification` | 1,728 rows; deterministic gzip written; decompression byte hash matched original before raw file removal |
| `python -m validation.scripts.hash_results_r3 --phase full-grid` | Wrote 21-entry full result hash ledger; independent 21/21 recalculation passed |
| `python -m py_compile validation/scripts/archive_records_r3.py validation/scripts/hash_results_r3.py` | Passed |
| `git diff --check` | Passed |

One initial invocation of the R3 arithmetic regression stopped with a fixture `KeyError` while looking up the frozen manifest's semantic hash; it stopped before calling the evaluator and emitted no query result. Commit `78aba4ddc100eb2fdb5c966e6d124ddac90ac8bc` corrected the fixture binding to the current canonical manifest fields. The subsequent R3 regression run passed 25/25 before the pilot. The archived pilot and full-grid checker runs report their own revisions and results above; this handoff does not describe them as a second independent Codex replay.

## 7. Artifact index and remaining limits

Principal R3 artifacts are under `results/validation/g2/r3/`:

- Frozen inputs/provenance: `specification_content_ledger_r3_v1.json`, `development_manifest_r3_v1.json`, `full_grid_continuation_manifest_r3_v1.json`, `SHA256SUMS_PRE_EVAL_R3.json`.
- Pilot: `dev_pilot_records_r3_v1.jsonl`, `dev_pilot_run_metadata_r3_v1.json`, `dev_pilot_record_check_r3_v1.json`, `dev_pilot_summary_r3_v1.json`, `r2_to_r3_query_transitions_r3_v1.jsonl`, `action_group_summary_r3_v1.json`.
- R2 compatibility: `r2_compatibility_record_check_r3_v1.json`.
- Conditional/full grid: `conditional_full_grid_records_r3_v1.jsonl.gz`, `conditional_full_grid_archive_manifest_r3_v1.json`, `conditional_full_grid_run_metadata_r3_v1.json`, `full_grid_record_check_r3_v1.json`, `full_grid_summary_r3_v1.json`, `r2_to_r3_full_grid_transitions_r3_v1.jsonl`, `full_grid_action_group_summary_r3_v1.json`, `SHA256SUMS_RESULTS_R3.json`.
- Method contract: `docs/LUNA_G2_DISTANCE_ADDENDUM_R3_v1.md`.

This is a finite synthetic development grid using one unsplit initial/parameter cell and one whole-hold interval hull. Checker replay shares trusted arithmetic/model primitives with the evaluator. No held-out comparison was run. G4's matched external baseline remains open. No MASTER assumptions changed; no G3/controller, closed-loop experiment, or hardware work was performed.

**Gate status: HOLD. G1 restricted PASS. G2, G3, and G4 UNVERIFIED. Physical correspondence UNVERIFIED.** The R3 evidence does not promote any gate or establish practical voltage-selection value, all-action safety, or hardware validity.
