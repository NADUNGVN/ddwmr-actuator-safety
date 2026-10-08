Session: DDWMR | LUNA-G2-SCOPE

# Luna → Codex — G2 decision-domain R3 execution preflight

**Date:** 2026-10-03  
**Assignment:** `docs/CODEX_TO_LUNA_G2_DECISION_DOMAIN_R3_EXECUTION_PREFLIGHT.md`  
**Repository:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Branch / HEAD:** `main` / `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe` (unchanged)  
**Disposition:** R3 offline pre-run candidate v6, row adapter, safety/endpoint replay path, locked selector, denominator aggregator, source closure and fixtures are prepared. **NO-GO to freeze or run pending Codex review. 800/800 rows remain NOT_RUN.**

## Decision summary

The versioned R3 path now verifies the exact candidate manifest and its source closure without writing in check or validation modes. It binds an ordered manifest row to the existing `run_query` input shape, checks raw and semantic benchmark hashes and the fixed 12-label image, then requires native R3 safety replay followed by R2 endpoint-record replay. Only replayed `CERTIFIED` safety with a replayed terminal-progress lower bound of at least `1/20 m` becomes task-eligible.

The nominal-preserving selector and full-denominator aggregation are implemented. The pre-run fixtures passed using synthetic/stub outcomes and read-only archived R3 records. **No study `run_query()` call was made; no task result was generated; no manifest was frozen; no status or research gate changed.**

The handoff recommends **NO-GO for a later freeze or staged run until Codex reviews the new adapter, worker, selector, closure and the documented legacy-field binding**. This preflight does not pass G2 or establish practical or physical usefulness.

## Finding 1 — scoped worktree and immutable evidence

**Finding.** Work stayed on the existing branch and added new G2 R3 artifacts only. Frozen R3 records, the R2 predecessor artifacts, G4/Auer files, the pre-existing dirty tree and existing evaluator/checker sources were left unchanged.

**Evidence.** HEAD was `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe` at entry and report time. The R3 mismatch fixtures compared SHA-256 values for 79 protected paths before and after each failing check. Both checks asserted exact dictionary equality. The table below gives key selected paths; all displayed before/after values are equal.

| Protected artifact | SHA-256 before | SHA-256 after |
|---|---|---|
| `results/validation/g2/r3/dev_pilot_records_r3_v1.jsonl` | `fdbce2ac5587247ababc0849c5fce8f9a596c3eb2175ed277545072c06acdc43` | `fdbce2ac5587247ababc0849c5fce8f9a596c3eb2175ed277545072c06acdc43` |
| `results/validation/g2/r3/conditional_full_grid_records_r3_v1.jsonl.gz` | `352b6c67480133350a7d1bfc89334a1beff1dc27c64cfda46391af27982fa874` | `352b6c67480133350a7d1bfc89334a1beff1dc27c64cfda46391af27982fa874` |
| `results/validation/g2/r3/development_manifest_r3_v1.json` | `794b314341e0c1ce7ff4fdbc7ddcde3f7d591e12b501e5ac7dd43175377be4e9` | `794b314341e0c1ce7ff4fdbc7ddcde3f7d591e12b501e5ac7dd43175377be4e9` |
| `validation/configs/g2_decision_domain_r3_mismatch_fixture_v6.json` | `5d553ff3e9ed3bf7dee486d2d46a13eec165c8e6505c948a4aac3b01424eb060` | `5d553ff3e9ed3bf7dee486d2d46a13eec165c8e6505c948a4aac3b01424eb060` |
| `research/benchmarks/G2_DECISION_DOMAIN_R2_MANIFEST_CANDIDATE_v1.json` | `28557ddecaf780c02801e872c247f46ff5a2c6b21da587520a82dcf5ab80e69b` | `28557ddecaf780c02801e872c247f46ff5a2c6b21da587520a82dcf5ab80e69b` |
| `research/benchmarks/G2_DECISION_DOMAIN_R2_SOURCE_CLOSURE_v1.json` | `612e592a263d7788f27f652e9a49683372e86393c2e04a662d8db126a39d8ebd` | `612e592a263d7788f27f652e9a49683372e86393c2e04a662d8db126a39d8ebd` |
| `validation/configs/r3_g4_matched_profile_v3_r9.json` | `13b632073c0bf8e5894d54e72fffb119961626d340517592723b829711d57863` | `13b632073c0bf8e5894d54e72fffb119961626d340517592723b829711d57863` |
| `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R9.json` | `7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533` | `7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533` |
| `validation/g4/r3_matched_query_worker_v3_r9.py` | `37abd9b980bc60424c51c7eb8832b2846b2b42b747946de5696de982f17af6f3` | `37abd9b980bc60424c51c7eb8832b2846b2b42b747946de5696de982f17af6f3` |
| `docs/reviews/G4_AUER_R5_GITHUB_SOURCE_INDEX.md` | `4509ee293b50e432f6d7169ba21f0ea85af257e490e0975d62b18ddc4969b0f7` | `4509ee293b50e432f6d7169ba21f0ea85af257e490e0975d62b18ddc4969b0f7` |

The G4 files shown above were already part of the initial dirty shared tree. These are before/after integrity sentinels; this execution did not edit them. No branch switch, clean, commit or push occurred.

**Consequence.** R3 v6 binds the preserved archive bytes and R2 v1 artifacts while keeping the R2 closure’s 34 reviewed entries immutable. G4/Auer evidence remains other-lane material.

**Status.** PASS for the scoped artifact boundary.

**Required action.** Review the new R3 files in place. Do not use the superseded local R3 drafts listed in the closure as candidates.

## Finding 2 — fail-closed read-only checks

**Finding.** R3 check and closure-validation paths are read-only, including on a specification-bundle hash mismatch. Intentional generation has its own explicit command and writes only new versioned R3 artifacts.

**Evidence.** `validation/scripts/build_g2_decision_domain_r3_candidate.py` exposes `--check-only`, `--validate-closure-only`, and `--write-candidate` as mutually exclusive modes. Both validation modes call the pure read path; it verifies declared specification source hashes and the computed bundle hash before comparing the R3 manifest, closure, sidecars and complete source/input hash list. `--write-candidate` refuses to overwrite nonidentical versioned artifacts. The deliberately mismatched config has a syntactically valid source list but a zeroed bundle hash.

The fixture ran both failing validation modes. Each exited `2`, returned the specific `SPECIFICATION_BUNDLE_SHA256_MISMATCH`, and left all 79 guarded-path SHA-256 values unchanged:

| Mode | Exit | Specific mismatch | Before/after hashes |
|---|---:|---|---|
| `--check-only --config validation/configs/g2_decision_domain_r3_mismatch_fixture_v6.json` | 2 | Yes | Equal for all 79 paths |
| `--validate-closure-only --config validation/configs/g2_decision_domain_r3_mismatch_fixture_v6.json` | 2 | Yes | Equal for all 79 paths |

Explicit versioned generation command:

```powershell
python -m validation.scripts.build_g2_decision_domain_r3_candidate --write-candidate
```

The reviewed R2 v1 config, manifest and closure remain byte-identical. Its historical builder source is hashed into the R3 closure as predecessor context but is not called by the R3 read-only check or generation path. The legacy R2 builder itself was not edited because it is part of the immutable reviewed predecessor closure; its previously reviewed write-prone check behavior remains a legacy-path caveat. Use the R3 v6 path for this candidate.

**Consequence.** A specification or source mismatch fails before artifact mutation. A check cannot silently rewrite the R2 candidate or repair a new R3 candidate.

**Status.** PASS for the R3 candidate path; historical R2 CLI behavior remains unchanged and out of this candidate’s execution path.

**Required action.** Codex should confirm that the versioned R3 validation path sufficiently isolates the previously identified R2 integrity blocker while preserving R2 v1 as an immutable predecessor.

## Finding 3 — exact manifest-row to `run_query` binding

**Finding.** The new adapter binds one ordered R3 candidate row to the full native R3 query shape and rejects rows that only reuse a valid ID.

**Evidence.** `validation/g2/decision_domain_adapter_r3.py` loads manifest, closure, benchmark and config bytes; checks manifest raw and semantic SHA-256 against the closure and sidecar; checks every closure source/input hash; and validates the benchmark’s raw and semantic SHA-256. It recomputes the semantic identity of the exact 12-label parameter image, verifies that image in the manifest and every row, and confirms the manifest is still 800/800 `NOT_RUN`.

`bind_manifest_row()` requires exact parsed-row equality at the requested `manifest_order_index`, checks the ordered unique query ID, then builds a query containing:

- exact state cell, scene, horizon and action;
- the complete hashed benchmark and matching parameter cell;
- the R3 candidate profile, hash protocol and specification-bundle hash;
- benchmark semantic hash and candidate-manifest semantic hash;
- the exact task-progress threshold.

Fixture tests changed the action while preserving the row ID and supplied a different row at the requested index. Both were rejected. Benchmark identity is pinned as raw SHA-256 `b2bc12cd578229cfb6df4b426f93e0f472d69f6be36929df93e797ff79396a9e` and semantic SHA-256 `21632e1eebf58a5d7fea14224254738d0ff11ba689b94343afa47adbccea166b`. The fixed parameter image semantic hash is `c653a4f0f0b76e5d36fffa6e0cab822eac3c949955a2348e98ae9cdf597fe6be` (12 labels).

**Legacy field meaning.** In the frozen R3 records, `development_manifest_sha256` contains the **semantic JSON SHA-256** of the original 1,944-row development manifest, `e5c796fcfe8275b1b7106f112813d24b36d18626400ba149f29f4bee7b9c155d`; it is not that manifest’s raw-byte hash. In the R3 candidate query, the legacy field carries the semantic SHA-256 of the complete ordered 800-row R3 candidate manifest, `f6744f4e5b75026c0ba83fc51740f60f75ad98bca0d5a0d72129cf54128f40fb`. The corresponding raw candidate-manifest SHA-256, `5ca87bc92429290d0c3967b3331f2a6cfec3b9482c7b5a7cc7532fbb5db20907`, is separately bound by the closure, sidecar and output hash ledger. The adapter documents this extension explicitly; the frozen evaluator/checker were not changed to fit the new IDs.

**Consequence.** Candidate records cannot enter the study result path by ID matching alone. The adapter’s manifest-byte, ordered-row, parameter-image and input-hash checks bind each query before evaluation.

**Status.** PASS in the candidate adapter and fixtures; independent source review remains required.

**Required action.** Codex should review the legacy-field reinterpretation and confirm the adapter plus closure provide the required manifest binding before any row is enabled.

## Finding 4 — ordered safety replay, endpoint replay and outcome classes

**Finding.** The offline worker requires native safety replay against the exact constructed query before making the R2 endpoint record, then replays that endpoint record against the same query and safety record. It counts a task action only when safety is `CERTIFIED` and the endpoint lower bound meets `1/20 m`.

**Evidence.** `validation/g2/offline_study_r3.py` provides the explicit `run_study_manifest_row()` one-row entry point and a separate stream validator. The preflight fixtures use the validator/stub paths only; the study entry point was not called. A proof-bearing safety record is replayed using the existing `replay_record`; `make_progress_record` is then followed by `replay_progress_record`. No R3 evaluator/checker source was changed.

The path distinguishes at least these non-success statuses: `RESOURCE_ABSTENTION` (integrity-valid proofless resource `UNKNOWN`, but no proof replay), `SAFETY_UNKNOWN_PROOF_REPLAYED`, `MALFORMED_RECORD`, `MISSING_ROW`, `DUPLICATE_ROW`, `IDENTITY_MISMATCH`, `HASH_MISMATCH`, `SAFETY_REPLAY_REJECTED`, `INVALID_INPUT`, `EXECUTION_FAILURE`, endpoint resource/execution failures, endpoint replay rejection, and `BELOW_PROGRESS_THRESHOLD`. `UNKNOWN` is never relabeled unsafe. Every query uses one action voltage and the same execution-fixed parameter image.

Each result retains the safety and endpoint record objects, raw bytes (exact input line when validating a stream; canonical JSON bytes for in-process records), byte length, raw SHA-256, semantic SHA-256 when parseable, and original stream index/byte offset. The batch hash ledger retains duplicate/orphan input records too. The aggregator carries the raw records and ledgers into its per-row table.

The effective profile keeps the one-cell full-hold method, arithmetic caps, orders and dyadic distance method: one state cell, one parameter cell, one full-hold panel, 16,384-bit and 1,000,000-operation caps, and 15 seconds. **The 15-second evaluator check is cooperative:** it is polled every 256 metered operations and has no successful-return deadline check. There is no separately reviewed outer process guard.

**Consequence.** Proofless resource abstentions and execution/data-integrity failures cannot be confused with task success. Raw evidence is available for later audit without dropping bad rows.

**Status.** PASS for the offline contract and read-only fixtures. No study row was executed.

**Required action.** Keep the cooperative timing statement. If a hard deadline is required later, separately implement and review an outer process guard, bind its source and test kill/reap behavior before locking.

## Finding 5 — locked selector and all fixed denominators

**Finding.** The selector and aggregation implement protocol v2’s exact rational tie-breaks and retain all candidate, development and held-out denominators.

**Evidence.** `validation/g2/decision_selector_r3.py` requires complete ordered 25-action groups. It retains nominal `(1,1)` whenever eligible. Otherwise it minimizes exact rational L1 distance to nominal, then prefers the larger exact endpoint lower bound, then the earlier manifest action order. The zero-only comparator tests only zero; nominal-only tests only nominal. Unique nonzero safety-certificate coverage is counted separately when zero is `UNKNOWN`.

The fixtures confirmed:

- nominal retention when alternatives tie the nominal-only result (preservation, not improvement);
- exact L1 tie resolution by higher progress, followed by manifest order when progress also ties;
- one extra held-out group produces a positive `1/16` paired gain over nominal-only;
- the primary selector-vs-zero rule stays false in that one-group synthetic fixture;
- a unique nonzero safety certificate is counted separately from task success.

Aggregation emits every 800 row status and every one of 32 groups. The held-out denominators are always 400 rows and 16 groups, including all 8 groups and 200 rows at each horizon. The primary per-horizon gate is at least 4/8 selector successes and at least two additional successes over zero-only at each horizon. Nominal-only improvement begins at a positive paired gain of 1/16; a tie means preservation.

Missing/duplicate/malformed fixtures kept all 800 rows and 32 groups in the output denominators. The synthetic one-missing/one-duplicate aggregation fixture reported both statuses without dropping either row slot.

**Consequence.** No pooled total can hide a failing horizon, and `UNKNOWN`, missing, duplicate, invalid or failed rows remain non-successes in the original denominators.

**Status.** PASS for the locked selector and denominator fixtures; no study outcomes exist.

**Required action.** Review selector source before any later freeze. Do not alter its criteria after inspecting held-out results.

## Finding 6 — fixture record and observed scope

**Finding.** The pre-run fixtures exercised the binding, checker, endpoint, abstention and selector paths using synthetic records and read-only R3 records only.

**Evidence.** `python -m validation.scripts.verify_g2_decision_domain_r3_fixtures` completed with these results:

| Fixture | Result |
|---|---|
| Exact R3 row binding; altered row and wrong manifest index rejection | PASS |
| Archived pilot R3 safety record replay | PASS (read-only stream record 0) |
| Archived compressed full-grid R3 safety record replay | PASS (read-only stream record 0) |
| Archived R2 endpoint record creation and checker replay | PASS; sample endpoint status `SAFETY_CERTIFIED_BELOW_PROGRESS_THRESHOLD` |
| Tampered archived R3 proof rejected | PASS |
| Proofless resource `UNKNOWN` | PASS as a **synthetic integrity-valid stub**; classified `RESOURCE_ABSTENTION`, not eligible |
| Archived R3 `UNKNOWN` record shape | The sampled/archive records are proof-bearing; no archived proofless resource row was claimed |
| Identity mismatch vs hash mismatch | PASS; separate statuses |
| Synthetic runner exception | PASS as `EXECUTION_FAILURE` |
| Nominal tie, exact rational L1/progress/order ties | PASS |
| One-group paired gain and unique nonzero certificate accounting | PASS; separate finite-grid counters |
| Missing, duplicate and malformed rows; denominator preservation | PASS |
| Read-only spec mismatch through both validation modes | PASS; both exit 2 with specific error and preserve 79 hashes |
| Study `run_query()` invocations | 0 |
| 800-query studies run | 0 |

The resource-abstention fixture does not claim an archive contained such a row. It starts with archived record inputs as a stub basis, substitutes an integrity-valid resource-failure diagnostic and no proof, then checks the separate classification path. Archive bytes remained unchanged.

**Consequence.** The fixtures establish input plumbing and outcome semantics before the task universe is run. They establish no task performance or 800-row success counts.

**Status.** PASS for pre-run fixtures only.

**Required action.** Treat the fixtures as code-path evidence, not R3 study results.

## Finding 7 — source closure and R2 predecessor relation

**Finding.** The final v6 manifest and closure are source-bound, explicitly linked to the reviewed R2 v1 candidate, and preserve that predecessor as an immutable 34-entry record.

**Evidence.** Final candidate paths and hashes:

| Artifact | Raw SHA-256 | Semantic SHA-256 |
|---|---|---|
| `validation/configs/g2_decision_domain_r3_v6.json` | `903577de5a6c2c9eda7e6e0c3a2353f93bdfe57c1837ba193b3c00b936247e41` | `b8f9fb8592a8ab681da25bf62db2762a7c7359604a29d54226142a6bd7946dbe` |
| `research/benchmarks/G2_DECISION_DOMAIN_R3_MANIFEST_CANDIDATE_v6.json` | `5ca87bc92429290d0c3967b3331f2a6cfec3b9482c7b5a7cc7532fbb5db20907` | `f6744f4e5b75026c0ba83fc51740f60f75ad98bca0d5a0d72129cf54128f40fb` |
| `research/benchmarks/G2_DECISION_DOMAIN_R3_SOURCE_CLOSURE_v6.json` | `b6b5c8b91fdc7c7dbc3c3b02fefb719f5aeeeaf9576ddf7cbbd584c9864b3469` | `d3b1f7d7acb54d9b9f4714e36a8c1cf0ce73e2be5c77a9ba1d6f3c711467fc38` |
| `validation/configs/benchmark_v1.json` | `b2bc12cd578229cfb6df4b426f93e0f472d69f6be36929df93e797ff79396a9e` | `21632e1eebf58a5d7fea14224254738d0ff11ba689b94343afa47adbccea166b` |
| R2 v1 predecessor manifest | `28557ddecaf780c02801e872c247f46ff5a2c6b21da587520a82dcf5ab80e69b` | `c72a04ffdf1fbe210cf073fe234255ffc67a4472c34b0f1519a1582291f9e223` |
| R2 v1 predecessor closure | `612e592a263d7788f27f652e9a49683372e86393c2e04a662d8db126a39d8ebd` | Preserved raw bytes; its 34-entry table remains inside the closure |

R3 v6’s `source_input_hashes` contains 70 entries: 15 transitive source files, 21 effective input/review-context files, four test/mismatch/archive inputs, and 30 explicitly superseded pre-run draft entries from R3 v1–v5. Those 30 entries are retained only to identify the local draft lineage; they are marked `superseded_pre_run_draft_not_effective`. The v6 manifest/closure are the final pre-run candidate pair from this handoff. No v1–v5 candidate is to be frozen or run.

The 15 transitive source paths and raw hashes are:

| Source | SHA-256 |
|---|---|
| `validation/g2/__init__.py` | `e263a290f1d402c7d233519c89d0f94ed1eaf731821c596486db7fc82ad624c8` |
| `validation/g2/evaluator.py` | `62dd355684c53fdd104ad051d2f06486e256e3489f1a72263a8432b9af9cc26e` |
| `validation/g2/checker.py` | `b2605941cc2620f19d0c6001736bec8e292b2e0dbb819f043c5dcd44fbc5e526` |
| `validation/g2/rational.py` | `8a2c16778b33898afd16c8da44945c2d41fd7d187cb11c7cb071745e68ed5c6e` |
| `validation/g2/interval.py` | `e49e2e3880485d9a658e2435cfa06b784f98257b13c51fa4a2bf464f9c73e5c6` |
| `validation/g2/model.py` | `93e9a96d640ad09a7eb7dbff51ebfb8f2d783296ce5afff57af41e81e30a8508` |
| `validation/g2/polynomial.py` | `48e3ff7dcce8353cb9d58b31f6986e12fcaaaf320cd06896f95e0813740b66a4` |
| `validation/g2/hashing.py` | `0d5137359e19c80b20c097d49c8d7246e48effcaef9e3649b142120136c13aab` |
| `validation/g2/endpoint_r2.py` | `21f35f62fe79b4782ed8446d319cb13b4813242af7621b2459111831bacbbb11` |
| `validation/g2/endpoint_checker_r2.py` | `d6b1611e4423e69c47852d2a3d848d98561475962b576e1ed05ed15dc65f007c` |
| `validation/g2/decision_domain_adapter_r3.py` | `bf9253ddc49f4462b6ab4fa809e315d048c82a50600e70c7951e961a3ffaef38` |
| `validation/g2/offline_study_r3.py` | `754a25e18940289fa7e2400fcbb35325bbc5c25a58905a322eedf1127bd6e327` |
| `validation/g2/decision_selector_r3.py` | `cb375b93108532dc7856fab1ee4fb29f43ff1fef0a73a5a91431070fc7dcfdb4` |
| `validation/scripts/build_g2_decision_domain_r3_candidate.py` | `1f9687e0a82b3ca8018a8f8848e8c92da9aa84ac9cbd593b25d65ab3892db500` |
| `validation/scripts/verify_g2_decision_domain_r3_fixtures.py` | `49478a93782ba9d6385aea2fc346d70c86ddcc3b199827640bdb6a7e9b2c27e7` |

The closure maps proof objects to these sources: full-hold R3 `P1_scaled`/`eta_physical` inclusion and collision/contact bounds; R3 query/proof replay; row/parameter/manifest binding; R2 endpoint lower bound and endpoint replay; distinct worker outcome/ledger handling; selector and denominator aggregation; and pre-run fixtures. The closure states that the endpoint replay shares the R3 checker, exact rational arithmetic and model-map trusted base; it is not an independent safety engine.

**Consequence.** The exact source/input set is inspectable before any task execution, and the R2 34-entry closure remains an immutable predecessor rather than being refreshed in place.

**Status.** PASS for source enumeration and hash validation. Mathematical and execution-source acceptance is still for Codex review.

**Required action.** Codex should verify the proof-to-code map and the 70 bound entries. Only after that review should a separate freeze/run decision be considered.

## Finding 8 — scope, limitations and gate status

**Finding.** The preflight prepares an offline finite-grid study path; it does not establish practical voltage-selection usefulness or physical-platform relevance.

**Evidence.** The deterministic universe remains 800 rows: 32 state/scene/horizon groups times 25 ordered voltage actions. It has 400 development rows, 400 held-out scene rows, 16 held-out groups and 8 held-out groups per horizon. Horizons remain `1/4 s` and `1/2 s`; the task threshold remains `1/20 m`. The split is non-blind and only varies scene geometry. Parameters are the exact synthetic 12-label image from the pinned benchmark, not measured or platform-calibrated data.

The endpoint-progress claim is conditional on the R3 full-hold `P1/eta` inclusion and safety replay. The R2 Codex scientific review accepted that conditional route and the endpoint method for its stated scope; the new row binding and aggregation source path still require review. The cooperative 15-second check is not a hard wall-time guarantee. The study has no task outcomes.

Gate state is unchanged: G1 PASS only for restricted reduced-model consistency; physical-platform correspondence UNVERIFIED; G2/G3/G4 UNVERIFIED; overall HOLD.

**Consequence.** Even a future positive result can support only the exact finite synthetic task comparison unless physical parameter/contact correspondence and broader usefulness are established separately. `UNKNOWN` is lack of certificate, not evidence of unsafe motion.

**Status.** No new mathematical blocker was found in row binding, rational threshold handling, or the conditional endpoint path. General certified-evaluator usefulness, tractability, physical relevance and G2 remain UNVERIFIED.

**Required action.** Keep the current claims within this synthetic, one-hold scope. Do not convert fixture outcomes into study outcomes or a gate pass.

## Final handoff — recommendation and required action

**Finding.** The offline execution candidate is concrete and source-bound, but has not received independent review.

**Evidence.** Candidate v6 is `NOT_FROZEN_NOT_AUTHORIZED_FOR_EVALUATION`; the manifest lists 800/800 `NOT_RUN`; check-only and closure-only pass on the candidate; both fail read-only on the hash mismatch; fixtures pass without `run_query()`; no archive, R2, G4 or Auer bytes changed.

**Consequence.** The R3 preflight closes the execution-plumbing gaps for Codex review. It does not itself authorize a task query, candidate freeze, G2 promotion or staged run.

**Status.** **NO-GO to freeze or run pending Codex review.** Overall HOLD; G2 remains UNVERIFIED.

**Required action.** Review the final R3 v6 manifest and closure, adapter’s legacy-field semantics, R3 safety replay boundary, R2 endpoint replay, exact selector/denominators, mismatch-path isolation from the legacy R2 builder, and the cooperative timing limitation. Keep **800/800 NOT_RUN** unless a separate subsequent authorization explicitly opens a staged run after review.
