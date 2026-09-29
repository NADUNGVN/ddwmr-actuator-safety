# Luna → Codex — G2 validation R2 full handoff

**Date:** 2026-09-30  
**Disposition:** **PARTIAL; HOLD unchanged.** Correctness, checker replay, hash portability, and bounded pilot work completed. The separate predeclared positive plumbing fixture did not complete under its frozen bit cap; that blocker is recorded below. No gate is promoted.

## 1. Scope, branch, and provenance

- Repository: `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`
- Branch: `luna/g2-validation-v1`
- Starting SHA: `695923836add60add64a6acac9909b8b7b942bf0`
- Evidence end SHA (parent of this handoff report): `b2a7408f3b74c334965d3ba808f12812b7495969`
- Working tree was clean at the start. The original v1 records, summary, manifest, and hash ledger were not edited or overwritten.

Commits added after the starting SHA:

| Commit | Contents |
|---|---|
| `dec84d7c0b75003adbc7eb341684b2979bfaaeae` | Radius correction; checker, arithmetic telemetry, semantic hashing, and R2 verification code |
| `8667685e660c25b51e384e18cb97a32a8776fe17` | Radius regression and hash protocol evidence |
| `b2422d2626cf559329345d4ddbc86ba4b88bc7bc` | Manifest generator correction before freeze |
| `87026c67f6188d4cccc7fada272b326a242eee8b` | Frozen R2 profile, unchanged selection, and pre-evaluation hashes |
| `3a1271cdde1a7e4d67b29847f6e5a7c209eb9cf6` | Partial-fixture reporting changes |
| `aa8cc4e17e41a70895f357f41427320c0a682c5e` | Proof fixture outcomes |
| `8038d1ed77cb4a76a2d39962ead231e0aae7c373` | Positive pilot certificate tamper verifier |
| `b2a7408f3b74c334965d3ba808f12812b7495969` | 216-query pilot, replay report, summary, ledgers, and result hashes |

The R2 result hash ledger covers 17 artifacts and was independently recomputed successfully. The R2 method remains the one-hold finite-cell interval-hull fallback with predictor depth `n=1`. No MASTER, hardware, controller, estimator, wheel-lock, or G4 baseline work was added.

## 2. Findings and dispositions

### R2-01 — radius-series factorial defect: corrected

The evaluator recurrence already carries `T^(k+1)/(k+1)!`; the duplicate factorial division was removed. The checker recurrence continues to use the coefficient directly. The independent regression constructs `T**(k+1) / factorial(k+1)` and the matrix powers directly for `K=0,1,2,16`, then compares the evaluator and checker separately.

Command: `python -m validation.verification.verify_radius_series_r2` — **15/15 checks passed**. Locked `N00=1, q0=1, T=1/10, K=1` values are partial `21/200`, tail `1/2000`, total upper `211/2000`; the checks also cover `N=0` and `q=0`. This is a coefficient/tail regression, not a plant trajectory proof.

Evidence: `results/validation/g2/r2/radius_series_regression_r2_v1.json`.

### R2-02 — proof-path coverage: pilot positive path passed; separate safe fixture is resource-limited

The R2 plumbing fixture was declared in `validation/configs/g2_proof_pipeline_fixture_r2_v1.json` and included in the frozen manifest before its run. It produced:

- One completed inconclusive proof; independent replay passed with status `UNKNOWN` and `COLLISION_SUFFICIENT_MARGIN_NEGATIVE`.
- One deliberately operation-limited record; the checker verified its resource telemetry as record integrity, without claiming arithmetic replay.
- The designated safe positive fixture did **not** finish. It stopped in `collision.full_hold_margin` at `fraction.mul`: pre-operation upper estimate **42,448 bits** exceeded its frozen **32,768-bit** cap. Each operand had a 21,224-bit numerator and 21,210-bit denominator; the largest completed result was 21,224 bits. I did not raise the frozen cap after seeing this result.

The partial fixture report has 10/10 applicable alias/query/hash/coverage tamper rejections. Its three certificate-specific checks (reduce radius, increase margin, change positive status) are explicitly marked not applicable because this fixture produced no positive certificate. Therefore this separate positive-fixture requirement remains **PARTIAL**.

The actual 216-query pilot did produce **54 completed positive certificates**, all 54 independently replayed. A separate tamper report replays one such pilot certificate with six nonzero `eta_scaled` components and rejects all three mutations: halve a serialized comparison radius, increase both serialized collision margins, and change `CERTIFIED` to `UNKNOWN`. This validates the positive record path on a pilot result, but does not relabel the failed separate fixture as successful.

Evidence:

- `results/validation/g2/r2/proof_fixture_records_r2_v1.jsonl`
- `results/validation/g2/r2/proof_fixture_metadata_r2_v1.json`
- `results/validation/g2/r2/proof_fixture_check_r2_v1.json`
- `results/validation/g2/r2/pilot_positive_tamper_check_r2_v1.json`

### R2-03 — resource diagnostics: instrumented and exercised

`Budget` now records stage, primitive, operand numerator/denominator widths, estimate kind, configured cap, attempts, started operations, completed results, maximum pre-operation estimate, maximum completed result, and maximum observed rational width. Pre-operation estimates and reduced-result failures are distinct. Oversized decimal inputs also produce bounded input-width diagnostics before large integer construction. Exact zero/one, cancellation, and unit-base power cases avoid false intermediate-size estimates while keeping operation accounting.

`python -m validation.verification.verify_primitives` passed **26/26** checks, including identity behavior and telemetry for bit, operation, and input-digit limits. `python -m validation.verification.verify_hand_cases` passed **32/32** exact hand inequalities. `python -m compileall -q validation` completed successfully.

The single frozen pilot diagnostic profile changed only the rational-bit cap from the v1 development profile: **16,384 bits**, **1,000,000 rational operations**, and **15 seconds/query**. The same 216 IDs and physics/scenes/actions were retained. Across 216 queries, 108 stopped at `collision.full_hold_margin` / `fraction.mul` with `RATIONAL_BIT_LIMIT`; estimates were 17,482–20,974 bits (lower median 19,016), while the largest completed rational result was 10,487 bits. No pilot query hit the operation or wall-time cap. This identifies a conservative pre-operation growth bottleneck; it does not show the guard is unsound or justify further cap increases.

### R2-04 — line-ending-dependent hashes: versioned protocol added

R2 uses `ddwmr-semantic-json-sha256-v2`: parsed JSON is serialized as sorted-key compact UTF-8 JSON with non-finite numbers rejected; JSONL records are canonicalized in order using physical LF delimiters. LF/CRLF checks include JSON and JSONL, and no global Git setting was changed. The v1 raw-byte files and ledgers remain untouched.

The current Windows working-copy raw hashes still match the old v1 manifest while the corresponding Git blob raw hashes differ. The new semantic input hashes are:

| Input | Semantic SHA-256 |
|---|---|
| `benchmark_v1.json` | `21632e1eebf58a5d7fea14224254738d0ff11ba689b94343afa47adbccea166b` |
| `dev_pilot_r2_v1.json` | `3b04dd91ed5f3330cc9e6f032edb970a6f1e4b8054cd92c85f969f72ba8060a6` |
| R2 development manifest | `e56342ab6a3bfceb5a9596836c0a905a1a75f521b0b9debc52e730b59766277d` |
| Proof plumbing fixture | `ee22d63de39ff06166059c640db1f3e0c2dbe3bd6814eac45f09b27f3df4d8f7` |

The selected-ID digest is `e6ae1e90775051a579f862b72ac8ee2e97facbdbbe99bc64552e1bcaa37ec9d0`. The frozen selection is the original **216/1,944**, with **1,728 NOT_RUN**.

Evidence: `results/validation/g2/r2/hash_protocol_check_r2_v1.json`, `SHA256SUMS_PRE_EVAL_R2.json`, and `SHA256SUMS_RESULTS_R2.json`.

### R2-05 — checker and execution provenance: tightened

The checker now validates the effective supported query contract, state coordinate order/shape, voltage limit, positive horizon and obstacle radius, profile bounds, and parameter-cell binding. It whitelists `CERTIFIED`/`UNKNOWN`, binds query aliases, protocol/method, benchmark/profile/specification hashes and quantifiers, and rechecks serialized margins, radii, widths, reason codes, and work counters. Malformed replay inputs return an explicit rejection. Proofless resource UNKNOWN can pass **record integrity only** when its bounded failure telemetry matches; it is never counted as arithmetic replay.

The runner records the actual interpreter argv (`sys.orig_argv`), executable, Python version, working directory, source revision, and frozen hashes. `verify_records` separately reports record integrity, proof replay, and positive-certificate replay.

## 3. Frozen pilot results

Run command:

```text
python -m validation.scripts.run_pilot --output results/validation/g2/r2/dev_pilot_records_r2_v1.jsonl --metadata results/validation/g2/r2/dev_pilot_run_metadata_r2_v1.json --benchmark validation/configs/benchmark_v1.json --pilot validation/configs/dev_pilot_r2_v1.json --manifest results/validation/g2/r2/development_manifest_r2_v1.json --hash-protocol ddwmr-semantic-json-sha256-v2
```

The runner completed all **216** selected records at source revision `aa8cc4e17e41a70895f357f41427320c0a682c5e`:

| Result class | Count | Checker disposition |
|---|---:|---|
| `CERTIFIED` | 54 | 54/54 positive certificate replays passed |
| `UNKNOWN` with completed proof and negative sufficient margin | 54 | 54/54 inconclusive proof replays passed |
| `UNKNOWN` from `RATIONAL_BIT_LIMIT` | 108 | 108 resource-record integrity checks passed; no arithmetic replay claimed |
| `INVALID_INPUT` / `EXECUTION_FAILURE` | 0 | — |

All 216 IDs and frozen hashes matched. `verify_records` reported `all_pass=true`, with `record_integrity_pass=true`, `proof_replay_pass=true`, and `positive_certificate_replay_pass=true`. It checked 108 completed proofs (54 positive, 54 inconclusive) and 108 resource-limited records. The semantic JSONL digest of the pilot records is `f3fff950792aedb785784612b02bed16e4d1ae632d6d830e72514d5a81027e59`.

Safety margins were completed for 108 queries. Decimal values below are rounded to 9 places; the summary contains the exact rational bounds:

| Lower margin | Minimum | Lower median | Maximum |
|---|---:|---:|---:|
| Collision (m) | -0.067683644 | -0.000680736 | 0.033366825 |
| Contact (N) | -0.583586121 | 1.451017474 | 1.838304558 |

Among the 54 completed proof UNKNOWN records, 54 carry `COLLISION_SUFFICIENT_MARGIN_NEGATIVE` and 36 also carry `CONTACT_SUFFICIENT_MARGIN_NEGATIVE`. These are failures of sufficient certification margins and do not establish that a query is unsafe. The other 108 UNKNOWN records are resource-limited, with no completed safety margins.

The summary found 6 state/scene/horizon groups with at least one certified action; 12 groups had all nine actions resource-limited. Display-only evaluator time was 0.093–0.172 seconds/query (median 0.156, total 31.31 seconds); it is not a safety predicate.

Exact pilot verification and summary commands:

```text
python -m validation.scripts.verify_records --records results/validation/g2/r2/dev_pilot_records_r2_v1.jsonl --metadata results/validation/g2/r2/dev_pilot_run_metadata_r2_v1.json --report results/validation/g2/r2/dev_pilot_record_check_r2_v1.json --benchmark validation/configs/benchmark_v1.json --pilot validation/configs/dev_pilot_r2_v1.json --manifest results/validation/g2/r2/development_manifest_r2_v1.json
python -m validation.scripts.summarize_pilot --records results/validation/g2/r2/dev_pilot_records_r2_v1.jsonl --summary results/validation/g2/r2/dev_pilot_summary_r2_v1.json --unknown-ledger results/validation/g2/r2/dev_pilot_unknown_ledger_r2_v1.jsonl --failure-ledger results/validation/g2/r2/dev_pilot_failure_ledger_r2_v1.jsonl --benchmark validation/configs/benchmark_v1.json --pilot validation/configs/dev_pilot_r2_v1.json --manifest results/validation/g2/r2/development_manifest_r2_v1.json
```

Runtime provenance recorded Python **3.12.12**, executable `C:\msys64\ucrt64\bin\python.exe`, cwd `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`, and the complete actual argv in the run metadata.

## 4. Evidence paths and final limits

R2 evidence is under `results/validation/g2/r2/`: frozen pilot config/manifest, pre-evaluation ledger, corrected-radius regression, hash protocol check, partial proof fixture records/report, full 216-query records and run metadata, checker report, summary, UNKNOWN/failure ledgers, positive tamper report, and result hash ledger. All 17 entries in `SHA256SUMS_RESULTS_R2.json` were recalculated and matched.

**Gate remains HOLD.** G1 restricted status is unchanged; G2/G3/G4 and physical correspondence remain UNVERIFIED. G4 external-baseline work remains open. The 216-query pilot does not estimate the 1,944-query grid rate; 1,728 IDs remain NOT_RUN. The separate positive plumbing fixture did not complete under its predeclared 32,768-bit cap, so its positive-fixture-specific tamper cases remain unexercised there. Pilot positive certificates and their independent replay/tamper checks do not remove the need for Codex’s independent review of the method and artifacts.

No further cap was tried after the frozen R2 pilot or fixture outcomes. No merge or force-push was performed.
