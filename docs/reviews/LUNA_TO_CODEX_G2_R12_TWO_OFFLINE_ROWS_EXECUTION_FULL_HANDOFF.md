Session: DDWMR | LUNA-G2-SCOPE

# G2 R12 two-row offline execution — full handoff

**Date:** 2026-10-04  
**Assignment:** `docs/CODEX_TO_LUNA_G2_R12_TWO_OFFLINE_ROWS_EXECUTION.md`  
**Disposition:** **BLOCKED — one of two offline row calls was attempted; the worker exited 1 before producing a record.** The durable intent and terminal are preserved. No retry was made.

## Summary

The exact Codex GO decision passed its raw-hash binding, and the source audit verified all 202 R12 closure inputs before execution. The R12 result namespace was absent and the G4 R15 stage was idle at the pre-run check. I invoked the exact R12 runner once. It consumed row 0 (R5 source index 12) and stopped with `WORKER_FAILED`, worker exit code 1. The ordered second row (R5 index 24) was not invoked.

The public read-only R12 auditor accepted the receipt and inventory as a valid account of a stopped stage: `receipt_valid=true`, `status=STOPPED_INVALID`. The row producer status is `NOT_COMPLETED`; the row-level Picard checker status is `NOT_RUN`. There is no row record or certificate, so no safety margin or progress value exists for this attempt. The predeclared paired decision is `INCOMPLETE_NO_TRIGGER`; broader-study preparation and execution authority remain false/not granted.

## 1. Authorization and pre-run checks

The authorized scope was exactly R5 indices 12 then 24, at most two offline worker calls, a 60-second per-worker hard timeout, zero native `run_query` calls, no retry, and zero R5 study rows. The assignment, R12 contract and prior exact-scope handoff were read. The exact decision and review bytes matched the GO review's pins.

| Binding/check | Observed result |
|---|---|
| Machine decision `research/benchmarks/G2_R12_CODEX_SCOPE_DECISION_v1.json` | `2c4d16c8d529c55222f49cc0c76cf66c9020b35ee527c1e2c2cfa7bb7d0c8bd5` — match |
| Codex review `docs/reviews/CODEX_G2_R12_EXACT_SCOPE_GO_REVIEW.md` | `37bcabaf2e3d333f7bb8a1483d594279f33d098979514ae8c0be14fecdfc3519` — match |
| R12 candidate manifest | `f0094dda957ba8e165fda21982fadee20bd2c5839ed309b1b377acc17764337f` — match |
| R12 source closure | `adbde039053db9438e989f9d74987421aad3f5f46db4ee88af7d9d5c41c98d62` — match |
| Closure verification | `PASS_READ_ONLY_R12_SOURCE_AND_ARTIFACT_AUDIT`; 202/202 source inputs match (186 inherited R11, 16 R12 additions) |
| Pinned runner | `validation/g2/r12_stage_runner.py` — `a9f8582625b8ee0364d634a672dfae87e29d74cf3dd9f7b6481b024f830555e4` |
| Pinned Picard checker | `validation/g2/whole_hold_picard_checker_r11.py` — `2a794e8f46c4b029331a2548dccd1948b78d3f5d5d7a96efa118d9353ba56f7e` |
| Pinned receipt checker | `validation/g2/r12_execution_checker.py` — `f4e6b2aa753802cf8649037b3a2b83d47f2d458eaf248dfdad18942e8a77e15f` |
| R12 target stage before invocation | Absent |
| G4 idle check before invocation | No G4 Python/MATLAB stage process found; `protocol_v3_r15_batch/stage_01` absent. Its namespace contained only `authorizations/r15_continuation_01.json`. Read-only check only; no G4 source or manifest was edited. |
| R5 study state before/after | 800/800 `NOT_RUN` |

The read-only source audit was repeated after execution. It again verified the same 202 source inputs and reported the stage as `STOPPED_INVALID`. No R12 candidate source was changed.

## 2. One runner invocation and captured console evidence

Exact command, run from the repository root:

```text
python -B validation/scripts/run_g2_r12_picard_stage.py --root . --authorization research/benchmarks/G2_R12_CODEX_SCOPE_DECISION_v1.json --stage-dir results/validation/g2/decision_domain_r12_whole_hold_picard_v1
```

| Execution evidence | Value |
|---|---|
| Start (UTC) | `2026-10-04T08:00:24.003585Z` |
| End (UTC) | `2026-10-04T08:00:28.551207Z` |
| Runner process exit code | `0` (the runner published a terminal stop receipt) |
| Row calls/intents consumed | `1/2` |
| Runner stdout | [Raw stdout bytes](LUNA_TO_CODEX_G2_R12_TWO_OFFLINE_ROWS_EXECUTION_CAPTURE_20261004.stdout.bin), 2,556 bytes, SHA-256 `a551461679e33eb3c9beb36934fb0b0cb7d1ccc7f17856834a5c7556715d48c7` |
| Runner stderr | [Raw stderr bytes](LUNA_TO_CODEX_G2_R12_TWO_OFFLINE_ROWS_EXECUTION_CAPTURE_20261004.stderr.bin), 0 bytes, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Capture metadata | [Execution capture JSON](LUNA_TO_CODEX_G2_R12_TWO_OFFLINE_ROWS_EXECUTION_CAPTURE_20261004.json), SHA-256 `2e443fcd330447a4beb2532ab8100520156111ce8b2affddb6d0a5ba0045ec26` |

The raw runner stdout is the published JSON receipt; the separate binary captures preserve the exact runner stdout/stderr. The runner launches the row worker with stdout/stderr captured internally. On a nonzero worker exit, the pinned runner records `WORKER_FAILED` and the exit code but does not persist or forward the worker's captured diagnostic streams. Therefore the retained evidence identifies the failure class and exit code, but not the worker's underlying exception/message. I did not rerun or attempt to reconstruct it by executing the worker again.

## 3. Row-level producer evidence

Only the first authorized row reached a durable intent and worker process:

| Field | Row 0 |
|---|---|
| R5 source index / stage order | `12 / 0` |
| Query ID | `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_L0_R0` |
| Canonical query SHA-256 | `d5648569b11c576c8cc0ecb07c5096c21b06fe3a5e849358f254770649465471` |
| Input-payload semantic SHA-256 | `422afd0448a184f4f67262c6338593c871739b41fb677e8ab1d6b566d18b93ac` |
| Development overlap | `true` |
| Durable intent SHA-256 | `51b26572b5194c80738099598bfa2645be084345fcf24e294e83400d873ff9f4` |
| Terminal outcome / reason | `INVALID_OR_INTERRUPTED` / `WORKER_FAILED` |
| Worker exit code | `1` |
| Producer status | `NOT_COMPLETED` |
| Row-level checker status | `NOT_RUN` |
| Record SHA-256 | `null`; no `record.json` was produced |

The intent binds R5 manifest `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b` and the already-consumed R6 evaluation `8d8f48d4c8bd3c6840d09ed32579e3796f81499e58b7a8ed60fba3b825487306`. The terminal raw SHA-256 is `2600d3d5bdac85efd6092f9253cd0c2f5fc62bcf55caafff642566332d34c44a`; its semantic SHA-256 is `517b7e379fd755101f16a4492b92f57cf14bb3ed68ba2522ea7356daea4d2b3b`.

Row 1 (R5 index 24, `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lp1_Rp1`) was not invoked and has no directory, intent, record, or terminal. The consumed row-0 intent is not retryable. No native query was called; the earlier two R6 observations remain consumed and unchanged.

## 4. Independent public replay and artifact inventory

After the runner returned, I called the public read-only `validation.g2.r12_execution_checker.audit_stage` on the canonical stage directory. The command exited 0 and returned:

- `audit_read_only=true`
- `receipt_valid=true`
- Stage/replay status: `STOPPED_INVALID`
- Receipt run status: `STOPPED_INVALID`
- Row 0 outcome: `INVALID_OR_INTERRUPTED`
- Row terminals: `1`; row call intents consumed: `1`
- Native query calls: `0`
- R5 study rows not run: `800`
- Receipt semantic SHA-256: `fff443a6994d8a0e5440fa19fc835409fdb667393b127ea9263273d28442f11b`

The public auditor's complete stage inventory contains four files and one directory:

| Kind | Relative path | Size | Raw SHA-256 |
|---|---|---:|---|
| File | `authorization.json` | 2,586 bytes | `2c4d16c8d529c55222f49cc0c76cf66c9020b35ee527c1e2c2cfa7bb7d0c8bd5` |
| File | `receipt.json` | 1,536 bytes | `49b68b72ba2f54c4e6f85e11627e694486ce378ce03093390eec0ab3b3005bde` |
| Directory | `row_00/` | — | — |
| File | `row_00/intent.json` | 1,254 bytes | `51b26572b5194c80738099598bfa2645be084345fcf24e294e83400d873ff9f4` |
| File | `row_00/terminal.json` | 864 bytes | `2600d3d5bdac85efd6092f9253cd0c2f5fc62bcf55caafff642566332d34c44a` |

There is no row record or row-01 artifact. The receipt raw SHA-256 is `49b68b72ba2f54c4e6f85e11627e694486ce378ce03093390eec0ab3b3005bde`. The receipt truth-table result is `INCOMPLETE_NO_TRIGGER`; `broader_study_preparation_trigger=false` and `broader_study_execution_authority=NOT_GRANTED`.

The post-run convenience command `validation/scripts/audit_g2_r12_candidate_manifest.py` also exited 0 with source status `PASS_READ_ONLY_R12_SOURCE_AND_ARTIFACT_AUDIT`. Its `r12_rows_not_run: "0/2"` field is a fixed pre-run label in that helper, not a live row count; use the public stage receipt/inventory above for actual execution state, which is one consumed row intent and one terminal.

## 5. Interpretation and disposition

This is a worker execution failure, not a completed Picard result and not an `UNKNOWN` certificate. No certificate exists, so there are no safety margins or certified progress values to report. The available evidence does not establish safety or unsafety for row 12, and row 24 has no observation. The paired usefulness trigger did not fire. The larger study remains unauthorized and unrun; G2 remains unverified under the project gate.

**Disposition for Codex:** retain the R12 stage and capture logs unchanged; review the worker failure and the runner's omission of worker diagnostic streams. Do not retry this consumed intent, do not invoke row 24 in this stage, and do not start the 800-row study under this GO. R5 remains 800/800 `NOT_RUN`; native calls are zero. No G4 source/manifest, existing research result, or candidate source was edited. No branch switch, commit, or push occurred.