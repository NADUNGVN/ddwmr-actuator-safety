Session: DDWMR | LUNA-G4-AUER

# R19 Stage 1 execution - full handoff

**Date:** 2026-10-05  
**Disposition:** **BLOCKED at final stage verification.** The one authorized stage wrote terminal `COMPLETE` for 10/10 matched pairs, but the runner and the independent R19 checker both exited 2 on a guard/result path-binding contract error. All stage evidence is preserved.  
**G4/project gate:** HOLD remains in force. This exact Stage 1 GO is not a batch GO and does not accept the comparison.

## Execution summary

- Executed the one-shot `r19_continuation_01` Stage 1 entrypoint once with the exact GO receipt.
- The stage terminal records 10 attempted, 10 completed pairs, 0 unattempted IDs; 20 method intents and terminals; 20 audit intents and terminals; zero retries and substitutions; no stage-level query stop. Stage elapsed time was 203.5 s.
- The stage terminal says `ALL_TEN_PAIR_ARTIFACTS_REPLAYED`. The runner then returned exit code 2 with `NO-GO: ContractError`, and the single independent stage replay also returned exit code 2. The exact blocker appears below. The stage artifacts are retained as one-shot consumed evidence; no query or ID was rerun.
- No later stage, retry, substitution, full 1,944-query batch, commit, or push was performed.

## GO receipt and pre-execution checks

The reviewed authorization was scoped to **exactly** `r19_continuation_01` and its ten ordered IDs. The Codex review decision is GO with `execution_authorized: true`; the receipt sets `one_shot: true`, `allow_retry: false`, `allow_substitution: false`, `allow_auto_advance: false`, and `allow_full_batch: false`.

Before stage launch, the review/receipt hashes, R19 candidate pins, exact ordered-ID digest, pinned CPython path/hash, source closure, and absence of the canonical R19 batch output directory were checked. The canonical output directory was absent before execution. The post-stage read-only closure rehash again matched all **575/575** dependency records (path, byte size, and SHA-256); zero drift was found. This includes all 549 inherited R18 dependency records and the earlier 525 inherited R17 records.

| Authority or candidate artifact | SHA-256 |
|---|---|
| GO review `docs/reviews/CODEX_G4_AUER_R19_STAGE_01_REVIEW.md` | `b5a233a9994b12bd8dd8eabe913a298d96bc92358bd9117003dda35f82b472e0` |
| Exact-scope GO receipt `results/validation/g4/auer2013/protocol_v3_r19_candidate/authorizations/r19_continuation_01.json` | `1ef1e7acbbb4376117737e0b1d601dbb7dd20185ac70a772b41418b23048fa51` |
| R19 candidate manifest | `9f926ddc17b4a7711ba4a9e1d8658832ac5e21a50bb2a953d41adef3c6064c2c` |
| R19 source closure | `a50bc0452e6b8f164988a4af8d669e563381f157f86188ca8c7ee1fb1518ca76` |
| R19 continuation schedule | `4271fd9339788e8372cdd4b8b48ecd9d61b7a0c10bdd7cebc7f79f9fcf1a5fd6` |
| R19 protocol candidate | `07219588dab800cb14990ac9f6b19f18d9077c0d706b96832f993ee0c785ece5` |
| R19 runner | `327b559f1363dec7bae0b61cb8bcef464c6ec174d812b5584b63b8a765b739ae` |
| R19 checker | `e97be3562e88563b49affefa0621b56157ea1a4676b9b4a3f87b731e3e99d537` |
| R19 timestamp contract | `5bae6675acab8b93eb05b6265c61893c045b54c7c986115a7c46c691033356cd` |
| Pinned CPython `C:/msys64/ucrt64/bin/python.exe` | `b5c33df60c2a8421dcf8117a67e848436b5d395c71ec1c0dfd96bad10f441d7f` |
| Stored non-query fixture report (not matched data) | `a5d892ac5546ca37b02938c61dd7028c24b91c68e40dd0415867dcfbe6702e63` |


The GO receipt binds the following candidate identities:

- Manifest: `9f926ddc17b4a7711ba4a9e1d8658832ac5e21a50bb2a953d41adef3c6064c2c`
- Source closure: `a50bc0452e6b8f164988a4af8d669e563381f157f86188ca8c7ee1fb1518ca76`
- Schedule: `4271fd9339788e8372cdd4b8b48ecd9d61b7a0c10bdd7cebc7f79f9fcf1a5fd6`
- Review SHA in receipt: `b5a233a9994b12bd8dd8eabe913a298d96bc92358bd9117003dda35f82b472e0`
- Receipt SHA: `1ef1e7acbbb4376117737e0b1d601dbb7dd20185ac70a772b41418b23048fa51`
- Pinned runtime: CPython at `C:/msys64/ucrt64/bin/python.exe`; observed SHA-256 `b5c33df60c2a8421dcf8117a67e848436b5d395c71ec1c0dfd96bad10f441d7f`.
- Stage ID: `r19_continuation_01`; query count: 10; ordered-ID digest (LF): `555297305b09d9676e401c10b5e33772463e43e2379778c0ce806d2c7f9e649d`.

The issued resource policy was: method worker 1 GiB / 120 s; composition auditor 1 GiB / 120 s; launcher 150 s with 1 MiB stdout capture; checker JSON read 16 MiB; checker artifact read 64 MiB; review-file read 65,536 bytes. The GO review also discloses that the runner/checker do not have an independent Job Object cap and that process-tree termination beyond the guarded worker/auditor is not fully enforced.

## Fixed-denominator accounting

The universe remains **1,944 IDs**. Historical IDs stay in their original strata and were not retried or pooled:

| Historical stratum | Consumed ID | Prior disposition |
|---|---|---|
| R9 carry-in | `state_low_neg__scene_d020_l-200__T_020__V_m1_m1` | Historical consumed ID; excluded from continuation |
| R11 attempt | `state_low_mid__scene_d020_l+000__T_050__V_m1_0` | Historical consumed ID; excluded from continuation |
| R15 attempt 1 | `state_low_pos__scene_d020_l+200__T_100__V_m1_p1` | R3 `UNKNOWN`; Auer `CERTIFIED`; consumed and not retried |
| R15 attempt 2 | `state_high_neg__scene_d050_l-200__T_020__V_0_m1` | R3 produced `CERTIFIED` output, but R15 common provenance stopped class 3 before Auer invocation; consumed and not retried |

R15 remains **2/10 consumed**. R17 and R18 Stage 1 remain **0/10**. R19 began with 1,940 never-attempted continuation IDs in the preserved order. After this one authorized Stage 1:

| Accounting stratum | Count |
|---|---:|
| Fixed universe | 1,944 |
| Historical consumed IDs (R9/R11/R15), separate from R19 | 4 |
| R19 Stage 1 attempted and terminalized | 10 |
| R19 Stage 1 completed matched pairs in stage terminal | 10 |
| R19 Stage 1 unattempted IDs | 0 |
| Remaining never-attempted continuation IDs | 1,930 |
| Retries / substitutions / later-stage IDs | 0 / 0 / 0 |

Thus 4 historical IDs + 10 new R19 Stage 1 IDs + 1,930 not yet attempted = 1,944. `UNKNOWN` is reported as inconclusive and is not interpreted as unsafe. Synthetic fixtures are not counted as matched data.

## R19 Stage 1 matched-pair outcomes

The ten rows below follow the authorized schedule order. `R3 native / common / final` and `Auer native / common / final` are taken from the stored per-method result artifacts. The composition column is the per-method audit terminal; `AUDIT_NOT_APPLICABLE` means no proof-to-common audit was launched for an R3 `UNKNOWN` result.

| # | Query ID | R3 native / common / final | R3 composition audit | Auer native / common / final | Auer composition audit |
|---:|---|---|---|---|---|
| 1 | `state_high_mid__scene_d050_l+000__T_050__V_0_0` | UNKNOWN / NOT_EVALUATED / UNKNOWN | AUDIT_NOT_APPLICABLE | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 2 | `state_high_pos__scene_d050_l+200__T_100__V_0_p1` | UNKNOWN / NOT_EVALUATED / UNKNOWN | AUDIT_NOT_APPLICABLE | PROOF_COMPLETE / UNKNOWN_ON_SUPPLIED_TUBE / PROOF_COMPLETE_COMMON_UNKNOWN | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 3 | `state_low_neg__scene_d100_l-200__T_020__V_p1_m1` | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 4 | `state_low_mid__scene_d100_l+000__T_050__V_p1_0` | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 5 | `state_low_pos__scene_d100_l+200__T_100__V_p1_p1` | UNKNOWN / NOT_EVALUATED / UNKNOWN | AUDIT_NOT_APPLICABLE | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 6 | `state_high_neg__scene_d200_l-200__T_020__V_m1_m1` | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 7 | `state_high_mid__scene_d200_l+000__T_050__V_m1_0` | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 8 | `state_high_pos__scene_d200_l+200__T_100__V_m1_p1` | UNKNOWN / NOT_EVALUATED / UNKNOWN | AUDIT_NOT_APPLICABLE | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 9 | `state_low_neg__scene_d020_l-200__T_020__V_m1_0` | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 10 | `state_low_neg__scene_d020_l-200__T_020__V_m1_p1` | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |


**Counts:** R3: 6 `CERTIFIED` with common `PASS_ON_SUPPLIED_TUBE`; 4 `UNKNOWN` with common `NOT_EVALUATED`. Auer: 10 native `PROOF_COMPLETE`; 9 common `PASS_ON_SUPPLIED_TUBE` and final `CERTIFIED`; 1 common `UNKNOWN_ON_SUPPLIED_TUBE` and final `PROOF_COMPLETE_COMMON_UNKNOWN`. Per-method proof-to-common audit records: 10/10 Auer `PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED`; 6/10 R3 pass; 4/10 R3 `AUDIT_NOT_APPLICABLE`. These per-method composition reports do not override the blocked top-level stage checker.

Inconclusive records are preserved as reported:

| # | Method | Native reason codes / termination reason | Stored final status |
|---:|---|---|---|
| 1 | r3 | `COLLISION_SUFFICIENT_MARGIN_NEGATIVE` | `UNKNOWN` |
| 2 | r3 | `CONTACT_SUFFICIENT_MARGIN_NEGATIVE, COLLISION_SUFFICIENT_MARGIN_NEGATIVE` | `UNKNOWN` |
| 2 | auer | `PROOF_COMPLETE` / `COMMON_PREDICATE_UNKNOWN_ON_PROOF_COMPLETE_SUPPLIED_TUBE` | `PROOF_COMPLETE_COMMON_UNKNOWN` |
| 5 | r3 | `CONTACT_SUFFICIENT_MARGIN_NEGATIVE` | `UNKNOWN` |
| 8 | r3 | `CONTACT_SUFFICIENT_MARGIN_NEGATIVE` | `UNKNOWN` |


## Timing and measured resources

The authorized caps and measured maxima from the stored guard/audit records are summarized here. All measurements are evidence records; this summary does not claim acceptance of the stage.

| Scope | Maximum observed wall time | Maximum observed peak memory | Applicable cap |
|---|---:|---:|---:|
| R3 method worker | 2.469 s | 56,332,288 bytes | 120 s / 1,073,741,824 bytes |
| Auer method worker | 5.500 s | 123,445,248 bytes | 120 s / 1,073,741,824 bytes |
| R3 composition auditor | 5.750 s | 55,582,720 bytes | 120 s / 1,073,741,824 bytes |
| Auer composition auditor | 7.656 s | 91,844,608 bytes | 120 s / 1,073,741,824 bytes |


Maximum serialized proof sizes were R3 121,132 / 4,194,304 bytes and Auer 11,524,568 / 536,870,912 bytes. Across the ten Auer composition reports, RHS/Jacobian accounting sums to 121 producer evaluations plus 51 offline replay evaluations; the largest per-query combined count was 51 against the 100,000 per-query cap. Maximum offline common-stage operation counts were R3 2,415 and Auer 3,621.

Per-query wall times are in seconds; `n/a` means no composition audit was applicable:

| # | R3 worker | R3 audit | Auer worker | Auer audit |
|---:|---:|---:|---:|---:|
| 1 | 0.719 | n/a | 1.359 | 7.656 |
| 2 | 0.765 | n/a | 5.500 | 3.797 |
| 3 | 2.063 | 3.719 | 1.360 | 3.125 |
| 4 | 2.156 | 5.750 | 2.015 | 3.125 |
| 5 | 0.765 | n/a | 1.797 | 3.594 |
| 6 | 2.094 | 3.313 | 1.391 | 2.890 |
| 7 | 1.782 | 3.188 | 1.406 | 2.985 |
| 8 | 0.688 | n/a | 5.266 | 3.407 |
| 9 | 2.094 | 4.016 | 1.734 | 3.421 |
| 10 | 2.469 | 4.219 | 1.531 | 4.063 |


Stage intent start: `2026-10-05T08:16:46.138660+00:00`. Stage terminal completion: `2026-10-05T08:20:09.641863+00:00`. Stage elapsed wall: `203.5` seconds. Method and auditor stdout capture records show complete bounded captures; stderr logs are empty for the final runner/checker processes. Guarded worker/auditor process memory stayed below the authorized per-process limits.

## Runner and independent replay blocker

The runner's saved stdout is:

```text

NO-GO: ContractError: state_high_mid__scene_d050_l+000__T_050__V_0_0/r3: successful guard is not bound to the one result invocation

```

Runner stderr was empty. The runner process returned exit code 2 after the stage terminal was written. The assignment-required independent stage replay was run exactly once with the same receipt and the existing stage root:

```powershell
C:/msys64/ucrt64/bin/python.exe -m validation.g4.check_matched_batch_v3_r19 --stage-root results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01 --authorization results/validation/g4/auer2013/protocol_v3_r19_candidate/authorizations/r19_continuation_01.json
```

It returned exit code `2`; saved stdout:

```text

BLOCKED: ContractError: state_high_mid__scene_d050_l+000__T_050__V_0_0/r3: successful guard is not bound to the one result invocation

```

Checker stderr was empty. The failure occurs at the first ordered pair, `state_high_mid__scene_d050_l+000__T_050__V_0_0/r3`. In that pair:

- `worker.guard.json` records exactly one worker invocation and result SHA-256 `6f169aeab9a969a94e0af8fd08079333b4cc1c6f73d8544a63405ae746cf660a`.
- The guard's result path is recorded as `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety\results\validation\g4\auer2013\protocol_v3_r19_batch\stage_01\query_01\r3\result.json`, while the matching method terminal path is `D:/Research/Teacher_Vien/projects/ddwmr-actuator-safety/results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/r3/result.json`. These strings point to the same absolute filesystem location but use different slash conventions.
- The terminal result SHA-256 equals the guard SHA-256, and both records show one invocation. The checker nevertheless requires raw `guard.result_path == method_terminal.result_path` (checker source lines 800-804), so the path-string mismatch fails the literal binding check.
- Read-only inspection finds the same guard/terminal path-string mismatch in all 20 method records; hashes match. The independent checker stopped at the first failing record and did not accept the stage.

The runner's final refusal and the independent replay error therefore identify a R19 path-normalization contract defect, not an authorization mismatch. The stage is **BLOCKED for review/acceptance**; the consumed ten IDs and all bytes remain preserved. No retry or stage advance was made.

## Stop reasons and gate state

- **Stage-level query stop:** none in `stage_terminal_receipt.json` (`stop_query_id: null`, `stop_reason: null`); all ten pairs and 20 method terminals were recorded.
- **One-shot/retry state:** `retry_count: 0`, `substitution_count: 0`; no unresolved method intent is reported in the stage terminal.
- **Post-stage runner stop:** exit 2, `ContractError` at the first R3 successful-guard result-path binding.
- **Independent stage replay:** exit 2, same `ContractError`; replay was attempted once and preserved.
- **Later work:** no Stage 2 or other query was launched. No batch of 1,944 queries was run. No commit or push was made.
- **Disposition:** this GO was exact-scope Stage 1 only. G4 remains UNVERIFIED and project HOLD persists. The R19 terminal's `ALL_TEN_PAIR_ARTIFACTS_REPLAYED` field is not a substitute for the failed independent stage-verification contract.

## Authority and candidate hash ledger

The table below records byte lengths and raw SHA-256 values for the assignment, GO decision/receipt, pinned candidate, runtime, and saved process outputs. The complete 575-file source closure is the R19 closure artifact listed above; the stage output and verification logs have their own exhaustive ledger below.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `docs/CODEX_TO_LUNA_G4_AUER_R19_STAGE_01_EXECUTION.md` | 2,485 | `933a337e1b2c28b66b820ea4e969a7db26b29bb94b7a1752fac6e87da9611613` |
| `docs/reviews/CODEX_G4_AUER_R19_STAGE_01_REVIEW.md` | 6,361 | `b5a233a9994b12bd8dd8eabe913a298d96bc92358bd9117003dda35f82b472e0` |
| `results/validation/g4/auer2013/protocol_v3_r19_candidate/authorizations/r19_continuation_01.json` | 2,302 | `1ef1e7acbbb4376117737e0b1d601dbb7dd20185ac70a772b41418b23048fa51` |
| `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v19_PROSPECTIVE.json` | 9,661 | `9f926ddc17b4a7711ba4a9e1d8658832ac5e21a50bb2a953d41adef3c6064c2c` |
| `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R19_PROSPECTIVE.json` | 130,427 | `a50bc0452e6b8f164988a4af8d669e563381f157f86188ca8c7ee1fb1518ca76` |
| `research/benchmarks/G4_AUER_R19_CONTINUATION_SCHEDULE.json` | 223,869 | `4271fd9339788e8372cdd4b8b48ecd9d61b7a0c10bdd7cebc7f79f9fcf1a5fd6` |
| `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R19_PROSPECTIVE_CANDIDATE.md` | 7,122 | `07219588dab800cb14990ac9f6b19f18d9077c0d706b96832f993ee0c785ece5` |
| `validation/g4/batch_stage_runner_v3_r19.py` | 28,629 | `327b559f1363dec7bae0b61cb8bcef464c6ec174d812b5584b63b8a765b739ae` |
| `validation/g4/check_matched_batch_v3_r19.py` | 70,876 | `e97be3562e88563b49affefa0621b56157ea1a4676b9b4a3f87b731e3e99d537` |
| `validation/g4/batch_timestamp_contract_v3_r19.py` | 2,917 | `5bae6675acab8b93eb05b6265c61893c045b54c7c986115a7c46c691033356cd` |
| `results/validation/g4/auer2013/protocol_v3_r19_candidate/nonquery_conformance_v5.json` | 43,746 | `a5d892ac5546ca37b02938c61dd7028c24b91c68e40dd0415867dcfbe6702e63` |
| `C:\msys64\ucrt64\bin\python.exe` | 101,651 | `b5c33df60c2a8421dcf8117a67e848436b5d395c71ec1c0dfd96bad10f441d7f` |
| `results/validation/g4/auer2013/protocol_v3_r19_candidate/execution_logs/r19_stage_01_runner.stdout.bin` | 133 | `cbb207cd73068430a60e296ba8294b58f6f48161716fc3a4b58c77b923ab6e3f` |
| `results/validation/g4/auer2013/protocol_v3_r19_candidate/execution_logs/r19_stage_01_runner.stderr.bin` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_candidate/execution_logs/r19_stage_01_independent_checker.stdout.log` | 135 | `25ff89ab4f4078044dfbd19dd7553a3d15ef9efd29fe83f177f3091fd5d56d66` |
| `results/validation/g4/auer2013/protocol_v3_r19_candidate/execution_logs/r19_stage_01_independent_checker.stderr.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_candidate/execution_logs/r19_stage_01_independent_checker.exit_code.txt` | 1 | `d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35` |


## Stage and verification artifact hash ledger

This ledger covers all **282 files** under `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01` and the five saved runner/checker process-output artifacts. Files are listed relative to the DDWMR project root, with exact byte size and raw SHA-256. No evidence file was rewritten during handoff preparation.

| Project-relative path | Bytes | SHA-256 |
|---|---:|---|
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/audit/audit.guard.json` | 4,456 | `dc23ecb7e49b2db0dac60fd4de520b68679d43677a408b62327db5021c2c8a01` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/audit/audit.stdout.log` | 3,564 | `c5b3514c9e13c3441656324054dccbe657cab7297aad64f626fc08af049bff25` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/audit/audit_intent.json` | 1,458 | `884b7a6deaa9c2245ee838d8b900a3e9edd0f267b7949a98546ad6446c6d3d60` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/audit/audit_terminal_receipt.json` | 2,390 | `4febba472e26a050dbad15a5dc4b83397fe8b7a0b40251a4a0880e3842be412d` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/audit/composition_report.json` | 3,874 | `64c87afa5908f2bf45eb88c91a0cc57e4d9823c41d8f09ea4c2ff398a6e7932f` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/checkpoint.json` | 59,484 | `aaa69d6fca8e88262edb9d1fcab2b57527dce5400edf1c0b67a45008fc535c36` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/invocation_intent.json` | 1,575 | `bf7dbfef34bb733d437f52698ff6f88cf4d7cf470774ab54b8d1dd84ca2dd4d8` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/proof.json` | 223,710 | `19a33a9ed8b42f20a63cb49ba57250637449544e3233c0ae1e05e6c587ce424a` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/result.common.json` | 16,972 | `936392b03eaf08a85d065b0b5cf0fb794b683a8a3340acd0c02902bdcfe721aa` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/result.json` | 58,406 | `513e3effd856c9da89e2b2a0bb7223b7d102ea8a1fa2afbdb15cfde3a8026682` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/terminal_receipt.json` | 4,124 | `e82d0bf1f2e514a834b2989e820ea77c1735dbf756162e4077c49bb68bbeca98` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/worker.guard.json` | 3,764 | `3946508cffeb425f76dafe4747348f43315da994f1f72c885715fe94cd9f7b61` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/auer/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/r3/audit/audit_intent.json` | 1,456 | `66ba1d8bc1b3f55954e8f48fc253f72e41b95bc5cdcf59cb4846831fe40b6998` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/r3/audit/audit_terminal_receipt.json` | 1,221 | `91f99aecc5699e73cd0d959846a9fec00fae1b79be21982960b393ea8e9c3ce3` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/r3/checkpoint.json` | 58,312 | `4a9443dc6b459416c937360d453f553a1899a999d975f694ebdcf68a342d46a0` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/r3/invocation_intent.json` | 1,573 | `3a930bd8e99153f6951353ca8ab3ebc56f48489fa2efa6e438d8d4adce76010a` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/r3/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/r3/proof.json` | 109,003 | `b6757cf9a9fb0239ace5d6e3bb8c98793646282977f7b654d4b3f1f0c9fb6292` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/r3/result.json` | 57,276 | `6f169aeab9a969a94e0af8fd08079333b4cc1c6f73d8544a63405ae746cf660a` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/r3/terminal_receipt.json` | 3,937 | `b3d2d8c5d52fdcf8a3f2aaa09ea4947f83c973c3f26768f21fd667dea639ea91` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/r3/worker.guard.json` | 3,735 | `c86824d7619b5c9bd7ae4b370d696313f139aaac885a922e65a557e0869b93f4` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_01/r3/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/audit/audit.guard.json` | 4,462 | `cccfae4a7acba8163975ef2dca28579c3dbfa865bb0a3b9c4d8b461c2a1095f9` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/audit/audit.stdout.log` | 3,592 | `cf715be0ce2b127795ec60a6da2dacee441ad7dbc21b210775b14c39e4be9620` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/audit/audit_intent.json` | 1,459 | `cbde7b1fdf81f04b460db38f0c5da8009ec467251a4e3e27d0107b91c2fb036e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/audit/audit_terminal_receipt.json` | 2,411 | `8ec92bf4eab9bb76e10858453792c676e604efdd7d9c7e59eb72a84fdb021070` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/audit/composition_report.json` | 3,902 | `867e80ed754982b443bcaee44dc7f0597d5e90dff90137e1b26f471c300b6e4c` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/checkpoint.json` | 60,091 | `b80943c2a299353e0e07eee6441b0192d73cc2af113c43a97abec1fd0a489476` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/invocation_intent.json` | 1,576 | `a85c5af64a9e4d218402cf54450b79ab53d0fd33d8f1919d1b4e5fecd8844be7` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/proof.json` | 11,524,568 | `ba2858eace2208753791d90c7fd6e3990b1ad5a736ef74d0ce3dfb3686bb8c9a` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/result.common.json` | 36,564 | `5277bc9ed9c657170458d88254fffc52e9386e4eb32a024458347b52273c4b06` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/result.json` | 58,970 | `4b5d0cf3ac0c22faa375d53c664e1cc94dcc08f62254d21f9e43e3abc5df617f` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/terminal_receipt.json` | 4,149 | `7a900789e3ac25eb63c68ea81c0e7aa2d04417a8c9fba0c326e7634deea083a3` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/worker.guard.json` | 3,759 | `c238701d0c36d05643c171b165abc6fe4f30d7309848d905293a85000c71aca5` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/auer/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/r3/audit/audit_intent.json` | 1,457 | `eb750992ca01b37e8dfc6ebd6d9bb48389326987e29108cace6bee40a0c3330f` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/r3/audit/audit_terminal_receipt.json` | 1,222 | `b45e7bcf6ccc26c9e62969d7fced47bc3ece1989d3a7cfae5f2bb902c8b45f15` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/r3/checkpoint.json` | 58,375 | `fdc88f5e159ce3b61e795c6667a168f0299bc1d3d26bf3c5c0291ecc519cfb9e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/r3/invocation_intent.json` | 1,574 | `51792b00a2caa138f64c15d233f7ff2ca47f5c367d7f0ccb6566e64ba5f6045b` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/r3/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/r3/proof.json` | 108,920 | `be319941cdff569c5842afe3801c0a6b26092f34b151359a15f76f5f6f42871e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/r3/result.json` | 57,337 | `8f675fac5014ca904db7936fbbc8883c4db8888fa893ca987753f13b3b9badfe` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/r3/terminal_receipt.json` | 3,939 | `2f0048b74b038ed47dc5bfd9335f3114ed7a9db598c339ec64d81948d5049619` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/r3/worker.guard.json` | 3,739 | `e815759dbaa97ec22047c3be6192cf3091f0ac369ff4c81bdfff78456d31f9dd` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_02/r3/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/audit/audit.guard.json` | 4,448 | `a8245c1be889af6330ebdb6879cb00888378509dbe93150bd7dfddeabad8ecbb` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/audit/audit.stdout.log` | 3,565 | `f7b7e970a6c79794c301aecc6a10d6e722cce820c1d60e1cab612c5ddc205a22` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/audit/audit_intent.json` | 1,459 | `e4832e463004cd7b2114e04ef62b0762117ccd0e85e132acf12b15c6cfd935c3` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/audit/audit_terminal_receipt.json` | 2,392 | `f4183854f3f6b3ba4a0567655b8f5fcdb60534d24777c76a6fb7ea6bd681a583` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/audit/composition_report.json` | 3,875 | `6a3c0de7745ed416c66e8c050a66fba817cab96c7b1a2a092e76af50ef80694d` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/checkpoint.json` | 59,477 | `5e9478049f1487bef73aaab4aaf4edbbcb98e6fee78d7afb7fbf47d60a7c969a` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/invocation_intent.json` | 1,576 | `cca4b6a6489ace72dcfc4cbee70f9ba8bd07e4c0e6eb84da0e02b0dbbda09cc2` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/proof.json` | 225,104 | `beb31a8e88a84a314cdb7b5a97deb1a44ed511343564f734f60a6d5f4dc0bc01` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/result.common.json` | 17,322 | `69cd732ac402685562630842740957bacc026898c2286b1800250520b2015074` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/result.json` | 58,398 | `50dd11e61462cdd4acbcf1b108d303d532da338107592c543107cd6ba1514ee4` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/terminal_receipt.json` | 4,125 | `885b1b848ea51b882250a74d6a2a91c673bc86dd2527d8e247a23f349a1aa1ce` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/worker.guard.json` | 3,766 | `55eb1ba4e473436c277d86b147de998daab9cb956469a0e8634eeb551da94cf7` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/auer/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/audit/audit.guard.json` | 4,438 | `647f36f0ea896ca2f207dfe81c8255229adb1d68c39cd32e9470dab40d0fdc8d` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/audit/audit.stdout.log` | 3,406 | `e538a3d5023a0cfb37ec5078b9d8351ece119c8f97e4bd8c4084ceb839a938ba` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/audit/audit_intent.json` | 1,457 | `0577d658415ee81b521fb509dea1e665eea39b6fd42c66f34883e062c192b214` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/audit/audit_terminal_receipt.json` | 2,369 | `ec1ef1f22f1cf7ccc70f857affd6717e1d8dffc6b32010357e0a1b7665fdeef5` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/audit/composition_report.json` | 3,679 | `9172e4b20825760f13ee9f56c04a301f52dea56bca4ecf73f83a961068e059b2` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/checkpoint.json` | 60,086 | `669b8eebc893cdf610e7bd289f243aeb3437b621077cd2f195b1f16182ed35b5` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/invocation_intent.json` | 1,574 | `46d55d8589a55acc313b3f1fa550e90c6a91719f9ccf07391c47dcf7d73a39cf` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/proof.json` | 121,004 | `af2460ef2da773fd2749c9749abf625e24a9d251f24a2ccddcb8c0bcb6428584` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/result.common.json` | 85,602 | `2769e3716a293a16b3b973f2f0fa802653882d54f0cedeaf3159405b13f13e0e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/result.json` | 59,017 | `36dfc00ed90f3f7123483bb3a130cd5b4e4be7feb81743257fe5c9ee89f1f406` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/terminal_receipt.json` | 4,096 | `0ea55c77aa9c5b3c4b283b1b04e47516323a9c418f481ae5c4cced1579f29f9d` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/worker.guard.json` | 3,738 | `65fccd4fbc84c1f0aacc7707692a2af9c92d6be6aa181d1f41283aaa303d7dd7` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_03/r3/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/audit/audit.guard.json` | 4,433 | `1cc432406131ef1663d9f921d404a6e7628576ff22d42340b753e0934638aa9b` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/audit/audit.stdout.log` | 3,564 | `de0d4be5a26ceabd4ed941157d6d09e05057124cb093745c275e0b24f0cc05a0` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/audit/audit_intent.json` | 1,458 | `ab3e9fa5c7b3fbf24669165d5aedcfcf12de739dda5e65aa6b3a8b56c378ad20` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/audit/audit_terminal_receipt.json` | 2,391 | `142fa9f1fc4764fd350bef58e7a48d375be330cc26ff8439299592a8091bcdac` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/audit/composition_report.json` | 3,874 | `629698e38d43148ae1edb5234b272a392d2de7b201b249e4bfb3d45b9ed1f37f` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/checkpoint.json` | 59,488 | `97040eee408f64c3d614d83c41db72076f5496dfbfc9d607d0e98e46311546aa` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/invocation_intent.json` | 1,575 | `b82d502fbedd1a425535928d260210038cf6bc968307b5492c296c401778b4e6` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/proof.json` | 223,364 | `81f581657879c8e9c4d77e40fa09ad75ab0dad6369292fd797e153bc68106b32` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/result.common.json` | 16,922 | `49164dae459f8e9106d13c5790446d058eec4568998c7f900c77164625296bf9` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/result.json` | 58,409 | `2c2144071c53c86b1b7baaa32492b6eb5bedc41a7a16e9d88bef07a05f1e4ac6` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/terminal_receipt.json` | 4,122 | `66b7650a2814bb22341eb560a0487b1bdf6d4c1e2598a5f4b3f959e8b343675e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/worker.guard.json` | 3,762 | `5fddccd824216fe11035f81153f08e84f0d625a383a07c548998c429373bde7a` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/auer/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/audit/audit.guard.json` | 4,420 | `66694c1424591cdac49cdcb4b30098ae843c2dcde481d0f265adf5e43608757f` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/audit/audit.stdout.log` | 3,405 | `ad18dba54c6897c2d7b670a1f0b9a583dc0134d21f7f5399f9406cab8737a24a` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/audit/audit_intent.json` | 1,456 | `ec974bb65a90fbc3c4ddcaee3a0e12ca45b8b10664912902b43994710a70d210` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/audit/audit_terminal_receipt.json` | 2,382 | `d20713f3a624f57ae1229f7ce03fd9f99e4838f3b1069367a7e111ec9749b606` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/audit/composition_report.json` | 3,678 | `3b8f679b714b2ac510c3372313b8f8ee7156b8758a5235f355278349153acf0d` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/checkpoint.json` | 59,994 | `3b1668826f57c0f48fb17ccbb63e0ffa7375bfe0c0198fc7b0d75afe4b795ca9` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/invocation_intent.json` | 1,573 | `206832728b494daddfd445a1bc6f69c586dc108a33bebcdacf6feafb2661554b` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/proof.json` | 109,023 | `1bdea1159ca1514ef822cad2c7e130604d12c22bdf684ff7eff8a9d351cd22f8` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/result.common.json` | 63,745 | `e0704de63a40f56fbcd31b237fe2e5a21c28fd34561eda5956522ead1bc0e998` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/result.json` | 58,926 | `363c87dd3fac2745ff25fb69c2c5f2744f595de9f34f5a88ec33ec0c30692698` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/terminal_receipt.json` | 4,094 | `3dd8e021cd9f9e107d1de1b2c22bbd26454d14476e8270878d7dac504037c4eb` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/worker.guard.json` | 3,736 | `65164d0a50b062c7438cec898bff0f60eda19f788dba31d9371661948ba8e58c` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_04/r3/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/audit/audit.guard.json` | 4,461 | `f4797adc611e1fd8498152372e87ae4ad1030126ef0a32e76e4c14227e0d6c0e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/audit/audit.stdout.log` | 3,566 | `37a1f8de7cae377b25a782b0b91d36340c01244de6189f0f4458a897fe97e5bd` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/audit/audit_intent.json` | 1,459 | `f9485a8439e410a2fe1ae67a4d28cd10725fde22bb4525e6182d50793318d732` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/audit/audit_terminal_receipt.json` | 2,392 | `a8cc7d3681627acbb738d584ca04f09ad7ad6cd84b811c6680be7d95d6a0b98e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/audit/composition_report.json` | 3,876 | `2b2c75b949e77109d30dc507daec91d3611b0df53db9e29e85b949ffdf9aa696` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/checkpoint.json` | 59,539 | `fc4312eb71e4dc6e4349cc8486197217cf85f3e5db52059ca169122d9dd2ae06` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/invocation_intent.json` | 1,576 | `6899b6ccb53b34465e562ebba5a69e6785e566445589bcfcfd543c2a463b3d3a` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/proof.json` | 756,435 | `7f92488baa2bca20c28ffd1a83c817e4704dab6f7f12588fa0e3f38707c01a90` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/result.common.json` | 24,106 | `e3381f2f358f7b65973f3a07a9889f7bd963e2a0211fa805c1c51cc6d674050c` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/result.json` | 58,474 | `02435adffd8264264db1db0079ff33df0d0d483f7665ae4fc7e03a47af05e3a1` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/terminal_receipt.json` | 4,113 | `354b5e98022b3922bf0f0959af8c3f3d29361ba446238cd19ef3d723d9baee8e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/worker.guard.json` | 3,768 | `22b244a46dc420165f8172651d84a20f94ba63ba29f73e805337b064dab96db3` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/auer/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/r3/audit/audit_intent.json` | 1,457 | `0063e6b706dbfb45c3512c1f6310963c27778da1c94bbe4f1532fc64ed4f79e5` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/r3/audit/audit_terminal_receipt.json` | 1,222 | `d018dc86ad8f2224c2f5d7b7adf5c857714f40f36d37afbd3b8c7484e1333383` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/r3/checkpoint.json` | 58,293 | `6e92a2861368842154e88a2b4124655950d593027ce2838c9b5ec31eb623ac61` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/r3/invocation_intent.json` | 1,574 | `221a423c7685589a9be1c378bcc40f4e6cda7df4d03da4091abb3ef82df8d891` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/r3/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/r3/proof.json` | 108,679 | `2165983850d5138c02b56b9dd206960c4b2394bba7aa189d0b931095463575ff` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/r3/result.json` | 57,257 | `d6fd3bb28f6c2cf138692c916fb7e206bd84dc9382af86d799fc00b0f6874426` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/r3/terminal_receipt.json` | 3,939 | `b510a6a07876ac7932018d731ee2f50e236b4f62c0fee9dc95bf44ad7a70e308` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/r3/worker.guard.json` | 3,739 | `7bc2e38ee175370e608fc4e3c76afb6edd318ac6a4a97f6dee876a19cbf36ccd` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_05/r3/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/audit/audit.guard.json` | 4,451 | `5e4625e19d7824138cefc0bb8cde6872fd705f2e08bffe421a658f9ca8e2acf7` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/audit/audit.stdout.log` | 3,566 | `b72c98d0e419cd01d049e8147a43648252d36ad955335967187034af378d81b1` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/audit/audit_intent.json` | 1,460 | `eaa25a8b2e7147dee23cff4ae6c1c346a5c37a79ac0ad9fc8a62d27f7769e2af` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/audit/audit_terminal_receipt.json` | 2,393 | `b0867899fe3420ade3e8a39154e076ecb04e9061dc946453976033fc04c6f02b` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/audit/composition_report.json` | 3,876 | `e19894c04543b0d8a280dd90381799252071f390a7ae47987219ea2b2328118b` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/checkpoint.json` | 59,500 | `dba50cbba39e8a354887932788eede3268420550b255dd08e84801cbe0ba8437` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/invocation_intent.json` | 1,577 | `56b0e893c85bad4963ed29529aaace4fd5a89c49b36c4d1aad1a2202abd22beb` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/proof.json` | 225,212 | `5f10753b4ff891767dd57511c0df1bf86e2f82500b7ac8a8ed081e3133463d33` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/result.common.json` | 17,343 | `326ad57ded8d661446ab74994ef07b1f06d11b530e7359cd4ecdd5eb72b569ee` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/result.json` | 58,422 | `269f5169db240dedf30b4b2e190add591f694be7dc3be4b0502fda6a0af28edc` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/terminal_receipt.json` | 4,128 | `5db2d5609b04f402543f01f298c9f22dad193662b39bc0871171465d5ae6e12e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/worker.guard.json` | 3,772 | `a6c6cdfc71329fd524f19980018f4d0791ba773fef38aa898f18416056143f49` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/auer/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/audit/audit.guard.json` | 4,439 | `94598542723e010817939a522ebf857c0f58a2b06d4ba58723de1f9f20be9eb8` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/audit/audit.stdout.log` | 3,407 | `eb0fa77918504f9e48b86519938200ec5864e47ca26249c95b981b41e0391841` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/audit/audit_intent.json` | 1,458 | `265550f5c531d47e5a4dea18cdec1523149c25ba7aeb548bde4ffdcb959a9e9b` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/audit/audit_terminal_receipt.json` | 2,385 | `cda05189d69fb8be2c9659e623b2060b9693618f364c552ba14a1714389db8af` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/audit/composition_report.json` | 3,680 | `a59d88236bf1635d2d655dde123ca21635a9e116381677f232557ae01b258bd3` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/checkpoint.json` | 60,112 | `1adc793a4bea8734874b92e052c5e19b317f4d7598aa366e94eec3cf1273794a` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/invocation_intent.json` | 1,575 | `c16fdc5446817cde38fa2c6ffcaacbc077f37ccb39d56857e0352871912718b9` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/proof.json` | 120,880 | `7e95712909c7f22f9089ca593b4ac2dc870e6fac268aeb120f88a6eae8f6203f` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/result.common.json` | 85,407 | `359a7432fb817291e300202a83475ba4203fdac756515bd6b5520879ef2c06da` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/result.json` | 59,043 | `9bbddfeb0d6c0c5720a380433acdc07623a1926ba536c2b2d3f673be6c4aac7f` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/terminal_receipt.json` | 4,098 | `b305855244e48ebee92f26d8e2e679909b2a76353ef96e74c96b560d5f849384` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/worker.guard.json` | 3,743 | `4c1296132fa9d3fdbf87863a20f9b64956553ed6730e68fbe06096efc2602ad4` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_06/r3/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/audit/audit.guard.json` | 4,461 | `d5d549ad6915eadb41ab79c71022849af2d524fc111744913bf650f22ba1853e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/audit/audit.stdout.log` | 3,565 | `73473781ddc054e271f4755d651233d849514568d615ddc1defa58599b30d1d0` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/audit/audit_intent.json` | 1,459 | `f6ed6729fc4d3eb5399a314ff85bdd5a7480d8ac376f0962f2cc9a651ed60da6` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/audit/audit_terminal_receipt.json` | 2,392 | `2027060a6656869bf4b32adfbc9f2bebd06d4139b5ea216f0ce3c48a4da226c0` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/audit/composition_report.json` | 3,875 | `5b852bc8cd64d88e035f0a5999a715394dcba626e0065aae4cc9082d5f4e5670` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/checkpoint.json` | 59,490 | `cc368ecae14ac75e4b6f30e8c029f28f4289986da409bf8d50e860e3d2534e56` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/invocation_intent.json` | 1,576 | `a96411b7a8e9d9137959ed58188216f0162e5689ac13cf06f2f023762b8893cf` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/proof.json` | 223,605 | `2c852378eb0f6ce415259a7bb3e7ee99a660ca777649fbe5448699fdc256b2b1` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/result.common.json` | 16,952 | `6aba9676f3f12a4ab93e82e07fcf548ae5cbe44e23d63cc3414ff18267ac6041` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/result.json` | 58,412 | `46b66f26197a0df66a5f96623bf63bf5881ddcbf0b53ea0886842e149b61c42c` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/terminal_receipt.json` | 4,125 | `c06fb072fcfa974fe369f3131def3ff546341981f5aca7c01629f8670b45b518` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/worker.guard.json` | 3,768 | `d1a82d3105304f58483bca3cde166958cee873617e073f978e6622d556278e10` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/auer/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/audit/audit.guard.json` | 4,437 | `fef23bd01e14d73b795bb0eaca3e8bad124c6e3251af7c9b66335bd00a1761d6` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/audit/audit.stdout.log` | 3,406 | `8b1b4932805aeabbc879c85f5975e5292049c3029b1e6e976341f9c958d40f96` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/audit/audit_intent.json` | 1,457 | `a50f426c7d585876c8704587980980f3463411c82a646bdaf952379dbd711333` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/audit/audit_terminal_receipt.json` | 2,384 | `6111f1f0b68c359a1eaa235b4f99fe92b76f0da7c65677a0016b624943636739` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/audit/composition_report.json` | 3,679 | `d7f7f6171d2452b96f53cbee7f755cd9eda8be957c9147388828fc744c7ce002` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/checkpoint.json` | 59,962 | `2a8f40a9673c63779a3f0304661e02029123669d65fba63b7e1082140b1cdf13` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/invocation_intent.json` | 1,574 | `619ff20211fe61beaceb34e5a9d8f7dab5efe0056a055eafb155cb499568159d` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/proof.json` | 109,056 | `f6926c55b88c4f364588fe4b831d81e7a56687b0a1e756aee7b2243557f8a6ac` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/result.common.json` | 63,719 | `7dafda6aad1a9f1832c1c67d8a28b925ca9776e9ef43fcc40bfc57c2b5e690c5` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/result.json` | 58,894 | `76d141997ea912636d8257815bf9ce5c4325999b86abca1f0226401b4d8d9709` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/terminal_receipt.json` | 4,096 | `d8efa4dba575d8e3f23d8e4579290bcd8874d8bf067cd60d2b6dbe68fe827d0a` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/worker.guard.json` | 3,739 | `e9202107fce916f6fd036bd9f014ca44357adc082e54841bd7830eeddc59c880` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_07/r3/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/audit/audit.guard.json` | 4,465 | `9d44a8836b8faf69c2a700f7605e0859692c900b3574d393e0250ad89473377a` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/audit/audit.stdout.log` | 3,570 | `f3a6da967fcaa1f1531cd707ccc593bb4634b32a5c16a74b7519044a6c9b484e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/audit/audit_intent.json` | 1,460 | `4a50844c635515e2022788d336b40e0f880fd66ef08a38c50beae6d18a2d50b2` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/audit/audit_terminal_receipt.json` | 2,393 | `76d5250bfb8a3e8b97f3a870f5a9246547c6ad655e47bbf267b74a33462c19e5` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/audit/composition_report.json` | 3,880 | `90684ae8739e2bd16f23139b8402efb1f608dfdfdd21bbad892ba64bf34626f5` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/checkpoint.json` | 60,061 | `215d5259878ad7e92bee695f6fa290217020a0bb198fcc58ad5861e21a0b4d8a` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/invocation_intent.json` | 1,577 | `b4778ac438c3282a15aeebe3deb2dedd3955fe0b6aaf2b9c87bba47dfe25216b` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/proof.json` | 11,480,237 | `af9cc1bf6def865c507c54f625ef106b46673a54a296cc45dbfc8f4984f41657` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/result.common.json` | 36,492 | `45b11e8074af0a393a8534b0b8b433e4fad006e9436b00f419a4075b5ebce4aa` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/result.json` | 58,954 | `7c2cd5ccefe5fdd2db4a08e4f9f9e01c20dbcb0af2fda1bdbc6a1135a0df221e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/terminal_receipt.json` | 4,128 | `9409212daf1947fc0eda1b6bc57ac2ef1a76f085db0510e0773ecfc32efebde2` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/worker.guard.json` | 3,771 | `124ddc9cda23b0a2908a7c894157b8bf9cd07ecac5c84ec754dc224b705a8fac` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/auer/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/r3/audit/audit_intent.json` | 1,458 | `78c92d2c715bef89d9ae997c61d788f1dc27f2e854971d5bcf61427141e6c630` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/r3/audit/audit_terminal_receipt.json` | 1,223 | `e285edebe3427f35d78d5fa4bda5b343da83bb2220280f498141d23d00def6d8` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/r3/checkpoint.json` | 58,308 | `8708becdc559faf63da15f55f42735ce7fcd04f52f24c4cd220385b9a5313d4e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/r3/invocation_intent.json` | 1,575 | `b66dcd67dda7680c0fc54d5ca093240fecc833628b4c5ab4e4866a44b2d05814` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/r3/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/r3/proof.json` | 108,787 | `18471b4c8c49c88d4cf6f319dab0638035aabc0d3f55643565b12ef52cdee070` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/r3/result.json` | 57,272 | `375356a9d5eaaba30cfce8740fd5f493e9134c4dac24c81e1b2f73cae316f79f` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/r3/terminal_receipt.json` | 3,940 | `842a68e5c7655f29fb1559f760775a6b53986518bf79ea5eb53ebf3951e6f5ce` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/r3/worker.guard.json` | 3,743 | `2446a4aa8da5bd1126881637425c21147a2fb00b06bda661a6c3dce579505fa1` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_08/r3/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/audit/audit.guard.json` | 4,459 | `581d29fdf7ecbd890275f877d73bad2a4cce9bbde7e5c08d9423f02bca7d4ca7` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/audit/audit.stdout.log` | 3,564 | `fb91e2a1efa8b1e998a3253aa8c0bcc851d6d3ef54acef2e811617900b81d600` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/audit/audit_intent.json` | 1,458 | `9074a64ee8f807522529185ec410e7f05856073a6cf619ca0b5a105abae1993a` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/audit/audit_terminal_receipt.json` | 2,391 | `ca1a60b5055291e50884e7dc7d61d1f0fe1230bb56ad0b4dfe5108cd509a6fa0` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/audit/composition_report.json` | 3,874 | `606816f7d3ff2981307ea192487d6477ede72370b2b575c3fb2f9b3ff43e76f3` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/checkpoint.json` | 59,474 | `9addbe115a6c9f1762ff74fd27f7cf8ebf49af88d1f478f4074b6cddad23db10` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/invocation_intent.json` | 1,575 | `32ccc095ae4923d14ebd97f9ae6c27b95deebee9146411b79b3d28cfe369ba8e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/proof.json` | 225,106 | `62f3a45f149dd8a727a503c041691a93412fb8ac3c5346d0a9970eda1a5e0595` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/result.common.json` | 17,323 | `417c60c0f28867830a5e87e35231c5dd36ecd87ab8a6a3dd53e6a0647df2b137` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/result.json` | 58,396 | `e3e267c38743cd32c12323ee15401e2ea50eb24c7c446cadbb7745dbcbb4257c` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/terminal_receipt.json` | 4,123 | `e1af66952e3c38b864e7a1a07679ee7203ae3f4b185ec2d41706e248fbf4a4e6` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/worker.guard.json` | 3,764 | `bbb2aa4243412af018496fb24a7e6c1a92244a8146d8af60306f4d8f56fedbb8` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/auer/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/audit/audit.guard.json` | 4,419 | `2de425096764378ce12f3198945cc37687634df7e22a1d54838be056635d2f2b` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/audit/audit.stdout.log` | 3,405 | `7d1d52c0501d7d2718c68b86248ebc6c8d0273eff5e047ad924e31304596ef30` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/audit/audit_intent.json` | 1,456 | `c8f9444e32ee3ccdb2a6e34d05314fa1106f265a269546b13a2de15c862783d1` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/audit/audit_terminal_receipt.json` | 2,382 | `27b60f19ec09e8662ab540b67ce1202cfcc8b6550a6d68179e985fd50aa5c977` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/audit/composition_report.json` | 3,678 | `da7b82d05beb7cefe3269d63e357bbb9f3daaa5b1d103e38f3bc0c7a59fd097e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/checkpoint.json` | 60,082 | `c166793d460a3fe904ae8a97bacdc3187a3193fc51e04b8b814b9ff05bb0d9ec` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/invocation_intent.json` | 1,573 | `6b69f2c7894227cffbe58d6d67275302caf90cbc4d5f3ba11181970ca3a32b20` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/proof.json` | 121,132 | `fd040b83b1d0235c5c6a1d63daaf5bb4dfb85f23ff55b6172d69bb4305ace0af` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/result.common.json` | 85,529 | `727a9199605edb03da69b82896706eb8ddeb21cd6312859233123227bfa5fd15` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/result.json` | 59,014 | `0b410ed95b109c7101192c0201e3bd0c7275fe536dd5a58f9e55dc1ccc691e55` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/terminal_receipt.json` | 4,094 | `15021e008470ce2bebe1c3db3e0224efb3a2096f3bfa28ac07e7dd816034794d` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/worker.guard.json` | 3,736 | `35a1833267877f1c5b6771af666d3d95605e6f540957456930eab0cbb42a09e3` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_09/r3/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/audit/audit.guard.json` | 4,460 | `157b3b1ced7d68d28e85bb29017e6ca3cc3d14349f9008c30fb38cb30f0db2e2` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/audit/audit.stdout.log` | 3,565 | `c1eae408173a24a3b148ffabdc202b7aafa14e9294136e5d3433e8612118b948` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/audit/audit_intent.json` | 1,460 | `d6476e11649405ce4c623435c99d1dbde9741d0d189d906586d9f81865a1f4d6` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/audit/audit_terminal_receipt.json` | 2,392 | `c5d0c4bd0c145f25f98737485d93bc95a8602f1d643b32a7a57e8276606bc5b9` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/audit/composition_report.json` | 3,875 | `7000e2c80f3ff07feba8d69fa7bb4ba3efef1a1234c12acf6b5d8a92b7005f5c` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/checkpoint.json` | 59,483 | `77fcd390c8f3fd3fff348845158f7ae656b2399f31ce733c82ab142608471b7e` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/invocation_intent.json` | 1,577 | `5335f8c788e8d6c21d4719ed86d9e9e08e862d7f607e6fe27a28c98ee2ac5d9d` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/proof.json` | 225,137 | `63def7c130588f51d113d393fd978f0adf5fa5b1d83e9241fe87bfecb9673b74` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/result.common.json` | 17,334 | `637859f1aeacaaf0d1fe051fd9b3dc2e34da0ec6da4725341d647e279720813a` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/result.json` | 58,405 | `b5f7071abec2432a8f97af9875ea9d3dac83e50dfbc3bcd6a05006528d353c10` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/terminal_receipt.json` | 4,126 | `fb7997ef6b5acc9956b0d1f60ca2b1db614303bbd583546d0ee91ef060b4dd8d` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/worker.guard.json` | 3,768 | `eb8a5747706a8395a4d1763b0220a2a1695e09c9ed792a1d634bb0e45bec4502` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/auer/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/audit/audit.guard.json` | 4,436 | `37ff37c489e72ca58c91df3360804e8ca611fe755e0f363a8c797b400548d42d` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/audit/audit.stdout.log` | 3,406 | `7e32f9d4a5bb40ad6dbf870adab19c65dbb3ec54a31e1b09d13f4ebdc37a9c40` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/audit/audit_intent.json` | 1,458 | `75abc2a76e11748b371127d8b24448a96a80b3a6d4562cec09529cc6c8fa9594` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/audit/audit_terminal_receipt.json` | 2,384 | `ce36518338319aff90fec374056365c410634320d090cb255f9790dda05af4d4` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/audit/composition_report.json` | 3,679 | `944499e1fe9b8c954491acba0f0f085d87281969d949d56b2d5c8084578506ab` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/checkpoint.json` | 60,102 | `d62f7d67e7b990e69c7808d6d2756e64700b6981a9f628f1946758193193627d` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/invocation_intent.json` | 1,575 | `526792098042f69e8e2ac74c76f4e1cb8ad5c40f972617fbcde6e62273cbaa1f` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/proof.json` | 121,000 | `b27c19ef5ad15cffc994619843f377961597ae4f28eace14d948284cf4356dff` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/result.common.json` | 85,603 | `9625dd7bd64056e06c2bb5c98e7c36714dbce957dbbe07fd0f0c81fd05e0ce43` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/result.json` | 59,020 | `5cf342beab793997a1c48e4cd68e1756e96833f9a032afc8692df8632b045670` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/terminal_receipt.json` | 4,096 | `daeccfc053d3676ac46af4443381dd43182f5ae6114c8e5aca5b7d31774f355d` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/worker.guard.json` | 3,726 | `923467090a0da7251d38cbf81ab191f3686acc666af26529abcd82140e7d01af` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/query_10/r3/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/stage_intent.json` | 2,460 | `9604c9fae13d338eebe86d57b98839168f8007dc571496721b6c2f636a750ea8` |
| `results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01/stage_terminal_receipt.json` | 3,405 | `662211f65c6b73449c86e2c2e3fdc0a0e2ba44c3f03682243df479130bbbd7a4` |
| `results/validation/g4/auer2013/protocol_v3_r19_candidate/execution_logs/r19_stage_01_runner.stdout.bin` | 133 | `cbb207cd73068430a60e296ba8294b58f6f48161716fc3a4b58c77b923ab6e3f` |
| `results/validation/g4/auer2013/protocol_v3_r19_candidate/execution_logs/r19_stage_01_runner.stderr.bin` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_candidate/execution_logs/r19_stage_01_independent_checker.stdout.log` | 135 | `25ff89ab4f4078044dfbd19dd7553a3d15ef9efd29fe83f177f3091fd5d56d66` |
| `results/validation/g4/auer2013/protocol_v3_r19_candidate/execution_logs/r19_stage_01_independent_checker.stderr.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r19_candidate/execution_logs/r19_stage_01_independent_checker.exit_code.txt` | 1 | `d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35` |
