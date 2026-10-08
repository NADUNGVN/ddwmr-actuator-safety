Session: DDWMR | LUNA-G2-SCOPE

# G2 R13 worker-failure postmortem and diagnostic-capture candidate

**Date:** 2026-10-04  
**Assignment:** `docs/CODEX_TO_LUNA_G2_R13_WORKER_FAILURE_POSTMORTEM_AND_DIAGNOSTIC_CANDIDATE.md`  
**Prior review:** `docs/reviews/CODEX_G2_R12_TWO_OFFLINE_ROWS_RESULT_REVIEW.md`  
**Disposition:** **DONE — synthetic diagnostics candidate and postmortem prepared; zero new real rows; R5 study remains 800/800 NOT_RUN.** The R12 stage and captures were preserved. No R12 retry, R12 row-01 call, native `run_query`, study row, commit, or push was performed. G2 remains **UNVERIFIED** and the overall disposition remains **HOLD**.

## 1. Result

The source proves a deterministic diagnostic-loss defect in the R12 runner: child stdout/stderr are captured only in memory and discarded on failure/timeout, while the temporary worker directory is deleted. R12 row 00's exact exit-code-1 cause is still **UNVERIFIED** because its worker stderr was not retained; this report does not infer an exception.

A separately versioned R13 candidate now defines a bounded streaming capture transport, write-once intent/terminal evidence, a read-only independent replay checker, JSON schemas, a source closure, and a NO-GO candidate manifest. Its runner remains synthetic-fixture-only and has no production-row CLI or GO path. The final suite passed all 13 synthetic groups in a temporary directory. No real DDWMR row was evaluated.

## 2. R12 source postmortem

### Proven defect

In `validation/g2/r12_stage_runner.py:518-550`, `_worker_invoker` runs the worker using `subprocess.run(..., stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)`. This buffers both streams in memory. On `TimeoutExpired`, it returns `(None, None, "HARD_TIME_LIMIT")` without persisting or forwarding `exc.stdout`/`exc.stderr`. On nonzero exit or missing output, it returns only `WORKER_FAILED` and the exit code. The `TemporaryDirectory` scope then cleans up the worker's temporary `record.json` path and any other temporary output. Thus diagnostics are lost on the observed R12 failure path, and stream accumulation is not byte-bounded.

The top-level R12 console capture is not worker stderr: the retained outer stderr file is empty. `validation/scripts/run_g2_r12_picard_row_worker.py:30-52` does not catch exceptions around source loading, record production, or record writing, so an uncaught exception could have emitted a traceback to the child stderr before exit 1. `validation/g2/time_slab_picard_r10.py:304-427` converts Picard inclusion exhaustion and `ResourceLimit` into `UNKNOWN`; other exceptions may escape. This source-level possibility does not identify what happened in row 00.

### Root cause and evidence limits

| Question | Finding |
|---|---|
| Why is the R12 attempt stopped? | **Established:** the worker exited with code 1 before producing a record; terminal outcome is `INVALID_OR_INTERRUPTED` / `WORKER_FAILED`; row checker was `NOT_RUN`. |
| What exact exception caused exit 1? | **UNVERIFIED:** worker stdout/stderr were not retained. No exception text is present in the R12 evidence. |
| Is this an `UNKNOWN` certificate? | No. There is no record or certificate. It is an invalid/interrupted worker attempt, with no margin or task-progress result. |
| Can row 00 be retried? | No. Its durable intent consumed the attempt. |
| Was R12 row 01 invoked? | No. It has no intent, record, terminal, or row directory. R5 index 24 was already consumed in the earlier R6 stage. |

The exact R12 raw hashes and byte counts are listed in Appendix B. The R12 candidate builder below rechecked the pinned R12 source/evidence bytes before it wrote the R13 candidate. The stage inventory remains exactly `authorization.json`, `receipt.json`, `row_00/intent.json`, and `row_00/terminal.json`.

## 3. R13 diagnostic-capture candidate

### Durable bounded capture

`validation/g2/r13_worker_diagnostics.py` drains stdout and stderr concurrently in 4,096-byte chunks. It stores a prefix capped at no more than 65,536 bytes per stream, with a default cap of 65,536. The transport tracks observed and captured byte counts, the raw hash of the stored prefix, and a raw hash of bytes actually drained. It does not accumulate complete output in `subprocess.run` result buffers. Each stored chunk is flushed and `fsync`ed; artifacts use exclusive creation and directory metadata is flushed.

When output exceeds a cap, the runner stops the child and reports `DIAGNOSTIC_OVERFLOW` if capture completed. The stored file is the first-N-byte prefix. `observed_byte_count` and `observed_stream_sha256_raw` describe bytes drained up to child termination; they do not claim to describe output the worker might have written after termination. Capture I/O errors yield `CAPTURE_INCOMPLETE` and preserve partial artifacts. Timeout and catchable interruption paths also preserve the streams read so far. If the parent is killed before a terminal is durable, its intent remains consumed and partial artifacts are replayed as `STOPPED_INTERRUPTED`; no retry is permitted.

Intent is written and flushed before process creation. The write-once terminal binds the intent raw SHA-256, worker argv SHA-256, process-start state, exit code, termination reason, outcome, capture policy, each stream's cap/counts/overflow/hash descriptor, and overall capture status. The terminal's semantic digest is checked with its own digest field omitted.

### Independent checker

`validation/g2/r13_execution_checker.py` reads without writing and owns local copies of protocol constants rather than importing producer constants. It recomputes terminal semantic and artifact raw hashes; checks the exact inventory and required stdout/stderr filenames; rejects missing, extra, symlinked, non-regular, size-mismatched, or hash-mismatched artifacts; checks cross-field counts, caps, overflow flags, termination state, and outcome; and rejects booleans where JSON integers are required. An intent without a terminal consumes one call and returns `STOPPED_INTERRUPTED` with `receipt_valid=false`.

### Candidate-only limitations

The runner core accepts only a task identifier beginning with `fixture:` and is exercised only with synthetic workers in a temporary directory. That label is an interface guard, not a security boundary. The R13 runner is not integrated with R12 source binding, an R5 manifest, a real-row stage, or an authorization/GO artifact. A real-row implementation would need a new source-bound version, fresh reviewed scope and separate exact-scope authorization. No prospective pair was selected in this assignment.

The contract is at `research/benchmarks/G2_R13_WORKER_DIAGNOSTIC_CAPTURE_CONTRACT_v1.md`. Intent, capture and terminal schemas are at the three `G2_R13_*_SCHEMA_v1.json` files. The candidate manifest explicitly records `NOT_AUTHORIZED`, zero new real rows, `R5 800/800 NOT_RUN`, G2 `UNVERIFIED`, and overall `HOLD`.

## 4. Synthetic interface evidence and checks

Final command:

```text
python -B validation/scripts/verify_g2_r13_diagnostic_capture_fixtures.py --report results/validation/g2/r13_diagnostic_capture_fixtures_v1/fixture_report_r2.json
```

Result: `PASS_R13_SYNTHETIC_DIAGNOSTIC_CAPTURE_FIXTURES`, 13/13 groups passed, all workers were synthetic and ran in temporary directories, `real_rows_evaluated=0`, `native_query_calls=0`, and `r5_study_rows_evaluated=0`.

| Fixture group | Result |
|---|---|
| Success: both streams retained and replayed | PASS |
| Nonzero worker exit: both streams retained | PASS |
| Process-start failure: empty streams and failed launch replayed | PASS |
| Hard timeout: partial streams retained | PASS |
| Catchable runner interruption: partial streams retained | PASS |
| Stdout cap overflow is explicit | PASS |
| Stderr cap overflow is explicit | PASS |
| Intent without terminal counts as consumed; partial diagnostics inventoried | PASS |
| Missing stream artifact rejected | PASS |
| Extra stream artifact rejected | PASS |
| Raw stream hash mismatch rejected | PASS |
| Boolean rejected as an integer count | PASS |
| Retry over consumed intent rejected | PASS |

The earlier 12-group synthetic report is retained as history. The 13-group R2 report is the final fixture evidence referenced by the candidate manifest. Python AST parsing passed for all five R13 Python files; JSON parsing passed for the seven R13 config/schema/closure/manifest/report files checked. A `jsonschema` validator package is not installed in this environment, so JSON Schema meta-validation was not performed; Codex may validate the three schema documents during review.

Candidate build command:

```text
python -B validation/scripts/build_g2_r13_diagnostic_candidate.py
```

It returned `PASS_R13_HASH_LOCKED_DIAGNOSTIC_CANDIDATE_PREPARED_NOT_AUTHORIZED`, with 18 source-input entries, 12 audit-evidence entries, zero native calls, zero new real rows, and R5 study 800 rows not run. The builder verifies fixed raw hashes for the preserved R12 worker/runner/binding/Picard/checker, candidate manifest/closure and execution artifacts before publishing the R13 manifest.

## 5. Preserved consumed-ID ledger

| R5 source index | Query ID | Prior use and outcome | R12 state | R13 action |
|---:|---|---|---|---|
| 0 | `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1` | R5 one-query preflight; native call completed as `UNKNOWN` | Not part of R12 pair | No new attempt |
| 12 | `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_L0_R0` | R6 consumed, `UNKNOWN`; R12 row 00 worker attempt exited 1 without a record | Intent consumed; terminal `WORKER_FAILED`; no retry | No new attempt |
| 24 | `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lp1_Rp1` | R6 consumed, `UNKNOWN` | R12 row 01 was not called; no R12 artifacts | No new attempt |

R6 intent/terminal raw hashes: index 12 `e1585a513b9a76a506c5952ec5bbc56c48f81d332d8b90dfcd309e54152905f` / `9d4efa58c94903031c04ffa84ac6c6b9712f55e29466b931021e36e6326e3e78`; index 24 `c533ed2ce4e7890d2faf40a4165203d3a19d6e10e3f282cb5f8430d0347d21ba` / `414a20e09586503a5ac103ce99e6b654c8c32931c713259e17b593edcf261064`. R12 row 00 intent/terminal are `51b26572b5194c80738099598bfa2645be084345fcf24e294e83400d873ff9f4` / `2600d3d5bdac85efd6092f9253cd0c2f5fc62bcf55caafff642566332d34c44a`.

R5 study count is still **800/800 NOT_RUN**; the historical one-query preflight and R6 diagnostics are not R5 study rows. R12 index 12 stays consumed, R12 row 01 was not invoked, and no replacement pair was designed or run.

## 6. Exact hash inventory

All hashes below are raw SHA-256 of the listed file bytes. The source-closure JSON repeats the same full source/evidence inventory and is referenced by the candidate manifest.

### R13 source inputs

| Path | Bytes | SHA-256 raw |
|---|---:|---|
| `docs/CODEX_TO_LUNA_G2_R13_WORKER_FAILURE_POSTMORTEM_AND_DIAGNOSTIC_CANDIDATE.md` | 2,389 | `7b29e5b24cd6f5052b885cb4ea6534985c73260afb85cb4ed92a1b69f833f6e1` |
| `research/benchmarks/G2_R13_WORKER_DIAGNOSTIC_CAPTURE_CONTRACT_v1.md` | 5,265 | `f4b30e43cf064700e7208f05910a128b4e910d304e9883178d632c0275f0d90e` |
| `research/benchmarks/G2_R13_ROW_INTENT_SCHEMA_v1.json` | 1,498 | `7b43161a9523eb68533be3517c71f8afb04396f87498c154bddfeddc9537d41a` |
| `research/benchmarks/G2_R13_DIAGNOSTIC_CAPTURE_SCHEMA_v1.json` | 2,827 | `97440602cfea6607e62d678adf51c2e7e0e30fb3f8d02877cebea68fe921c66c` |
| `research/benchmarks/G2_R13_ROW_TERMINAL_SCHEMA_v1.json` | 1,716 | `c986b19f3f1ff066938792758ad1df850e17045682eabc15060af9f45efd4cf5` |
| `validation/g2/r13_worker_diagnostics.py` | 12,944 | `a6712021a7ceaad38e0c992008f6dd51f1da4ad625deeea1c0ba01e5a36bcbfa` |
| `validation/g2/r13_stage_runner.py` | 6,917 | `f99e42aa5c27af34020abfa3a4241de0bf0ce04e8fd9a6b9f2a1000ee06c8c99` |
| `validation/g2/r13_execution_checker.py` | 18,531 | `1810345c34246472fe49b49a3d12b26396619445cac0b43fed2eab7ba23be438` |
| `validation/configs/g2_r13_diagnostic_capture_fixtures_v1.json` | 1,503 | `ec23858d6a25cf86b73e0cd442893d1062516ab1e0befed3d8160336f4175c72` |
| `validation/scripts/verify_g2_r13_diagnostic_capture_fixtures.py` | 12,076 | `1c30020351c8fdfe50725fcf63cc6c1e4df9839d441db1edae01b6d399e0495a` |
| `validation/scripts/build_g2_r13_diagnostic_candidate.py` | 11,982 | `062f95ae438f25dd84b0ac09eb4a07d8541b8894c14cbbda9275f29a9fa17870` |
| `validation/g2/r12_stage_runner.py` | 29,001 | `a9f8582625b8ee0364d634a672dfae87e29d74cf3dd9f7b6481b024f830555e4` |
| `validation/g2/r12_scope_binding.py` | 11,637 | `8d7f8cce01d873345b99b4a3bd2f61bee692be8aa650ff484d7c72eeb057533a` |
| `validation/g2/time_slab_picard_r10.py` | 22,572 | `e9fa6672649d675e27bb4f419e28259b9546b01bb6592f3388396ecd2a211c47` |
| `validation/scripts/run_g2_r12_picard_row_worker.py` | 2,191 | `7e9078da16ccc4baf71159e175137d7115834ccc353a8b600ff570c34e19ad5c` |
| `validation/g2/r12_execution_checker.py` | 30,171 | `f4e6b2aa753802cf8649037b3a2b83d47f2d458eaf248dfdad18942e8a77e15f` |
| `research/benchmarks/G2_R12_WHOLE_HOLD_PICARD_STAGE_CANDIDATE_v1.json` | 117,172 | `f0094dda957ba8e165fda21982fadee20bd2c5839ed309b1b377acc17764337f` |
| `research/benchmarks/G2_R12_WHOLE_HOLD_PICARD_SOURCE_CLOSURE_v1.json` | 41,905 | `adbde039053db9438e989f9d74987421aad3f5f46db4ee88af7d9d5c41c98d62` |

### R12 and synthetic audit evidence

| Path | Bytes | SHA-256 raw |
|---|---:|---|
| `docs/CODEX_TO_LUNA_G2_R12_TWO_OFFLINE_ROWS_EXECUTION.md` | 2,648 | `758c433549e60a88bc69e405189afe49d519c936b197c68f7916eb4d09bfecc6` |
| `docs/reviews/CODEX_G2_R12_TWO_OFFLINE_ROWS_RESULT_REVIEW.md` | 3,789 | `0b4b66926bc9e15891af630ce10d8443c595cc4b98a1f7a21155084f22465bcd` |
| `docs/reviews/LUNA_TO_CODEX_G2_R12_TWO_OFFLINE_ROWS_EXECUTION_FULL_HANDOFF.md` | 9,405 | `d90fd5571b4504959deed0e2152c4e299de3bcee609802891dca99a8090931f4` |
| `results/validation/g2/decision_domain_r12_whole_hold_picard_v1/authorization.json` | 2,586 | `2c4d16c8d529c55222f49cc0c76cf66c9020b35ee527c1e2c2cfa7bb7d0c8bd5` |
| `results/validation/g2/decision_domain_r12_whole_hold_picard_v1/receipt.json` | 1,536 | `49b68b72ba2f54c4e6f85e11627e694486ce378ce03093390eec0ab3b3005bde` |
| `results/validation/g2/decision_domain_r12_whole_hold_picard_v1/row_00/intent.json` | 1,254 | `51b26572b5194c80738099598bfa2645be084345fcf24e294e83400d873ff9f4` |
| `results/validation/g2/decision_domain_r12_whole_hold_picard_v1/row_00/terminal.json` | 864 | `2600d3d5bdac85efd6092f9253cd0c2f5fc62bcf55caafff642566332d34c44a` |
| `docs/reviews/LUNA_TO_CODEX_G2_R12_TWO_OFFLINE_ROWS_EXECUTION_CAPTURE_20261004.json` | 1,216 | `2e443fcd330447a4beb2532ab8100520156111ce8b2affddb6d0a5ba0045ec26` |
| `docs/reviews/LUNA_TO_CODEX_G2_R12_TWO_OFFLINE_ROWS_EXECUTION_CAPTURE_20261004.stdout.bin` | 2,556 | `a551461679e33eb3c9beb36934fb0b0cb7d1ccc7f17856834a5c7556715d48c7` |
| `docs/reviews/LUNA_TO_CODEX_G2_R12_TWO_OFFLINE_ROWS_EXECUTION_CAPTURE_20261004.stderr.bin` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g2/r13_diagnostic_capture_fixtures_v1/fixture_report.json` | 1,925 | `50efefdfa4b40b8a86965e53a433be1a6501f7c512aa4306d7fa50a1c2c9f21b` |
| `results/validation/g2/r13_diagnostic_capture_fixtures_v1/fixture_report_r2.json` | 2,101 | `ade2cbcd571e02dc170e076318a07458bdee551fdc3e3ec1f10571eb9f3ce197` |

### R13 candidate envelope

| Artifact | SHA-256 raw |
|---|---|
| `research/benchmarks/G2_R13_WORKER_DIAGNOSTIC_CANDIDATE_MANIFEST_v1.json` | `d3bf7ee7ebee370c2457419169259228a17952f790c285d1d2e5cee9a0699fd8` |
| `research/benchmarks/G2_R13_WORKER_DIAGNOSTIC_SOURCE_CLOSURE_v1.json` | `51eb55764f54cba66327b3155982e64eca14d0bb785da7b6b1e122f72424f089` |
| `research/benchmarks/G2_R13_WORKER_DIAGNOSTIC_SOURCE_CLOSURE_v1.json.sha256` | `2f3c39b561285372236774cec1db449f414f67367b58e023c606976015235987` |

## 7. Next decision point

Codex should review the source postmortem, fixture-only capture API, checker edge cases, schema documents, and hash-closed candidate. This handoff does not authorize any real evaluation. If the diagnostic candidate is accepted, source-bound production integration and any prospective paired usefulness study require a new version and a fresh deterministic manifest that excludes consumed indices 0, 12, and 24, followed by an independent exact-scope GO decision. Keep R5 study at 800/800 `NOT_RUN`, G2 **UNVERIFIED**, and overall **HOLD** until separately reviewed evidence changes those gates.
