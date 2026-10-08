Session: DDWMR | LUNA-G2-SCOPE

# G2 R14 — source-bound two-row candidate

**Date:** 2026-10-04  
**Assignment:** `docs/CODEX_TO_LUNA_G2_R14_SOURCE_BOUND_TWO_ROW_CANDIDATE.md`  
**Prior review:** `docs/reviews/CODEX_G2_R13_DIAGNOSTIC_CANDIDATE_REVIEW.md`  
**Disposition:** **DONE — v3 NO-GO candidate prepared for independent Codex review.** The candidate is not frozen or authorized. R14 real rows are **0/2 NOT_RUN**; the R5 800-row study is **800/800 NOT_RUN**. G2 remains **UNVERIFIED** and the overall research disposition remains **HOLD**.

## 1. Scope and execution ledger

The work prepared and audited a source-bound candidate for exactly R5 indices 62 and 74. It did not execute either row, start the R10 worker, call native `run_query`, invoke the R12 stage, or run any R5 study row. No execution authorization or receipt was created. The R14 stage directory and the v3 Codex decision artifact are absent. The synthetic interface fixture reports zero worker calls and zero native query calls.

| Item | State |
|---|---|
| R14 selected rows 62 and 74 | `NOT_RUN` / `0 of 2` |
| R5 study | `800/800 NOT_RUN` |
| R14 worker calls | `0` |
| Native `run_query` calls in this assignment | `0` |
| Codex GO / executable receipt | Absent; separate exact-scope Codex GO is required |
| Retry authority | None; any future invalid, resource, interrupted, timeout, overflow, or incomplete-capture outcome consumes its intent and stops the pair |
| Commit or push | None |

The R5 manifest continues to declare all 800 study rows `NOT_RUN`. Existing R5/R6/R10/R11/R12/R13 evidence was source-checked and retained. No G4 file was edited in this R14 work.

## 2. Predeclared pair and source selection

The locked rule is: starting after the R12 anchor group, select the first later group in canonical R5 manifest order with the same state `S_LOW_NEG` and horizon `T_250MS`, for which both the zero action and symmetric positive action have no prior attempt. If the pair, order, raw query bytes, or consumed ledger differs, the selector fails without substituting another pair.

The first qualifying group is `S_LOW_NEG__D_OFFSET_LEFT__T_250MS`. The independent R5 source binder confirmed the exact IDs, statuses, canonical query hashes, payload semantic hashes, and consumed-index ledger:

| Stage order | R5 index | Query ID | Action | Canonical query raw SHA-256 | Payload semantic SHA-256 | R5 status |
|---:|---:|---|---|---|---|---|
| 0 | 62 | `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_L0_R0` | `V_L0_R0` (0, 0) | `38839995032bd4328a7c4d1059d2e3e674f3f3586a12f6f2d6c76842dfcfa8f0` | `aacb6dd0639c5d5c603ca227066352a9d04a1d2d0e92fc77ab3499f59f10db37` | `NOT_RUN` |
| 1 | 74 | `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_Lp1_Rp1` | `V_Lp1_Rp1` (+1, +1) | `1bab855c36a6cba051736320002ea40370c793f57a04cc5a8454a71b79d2c858` | `b4ad72b1cf4e1fcc37de3bf3ed080ba4797e637e3f37919873df740043645c3b` | `NOT_RUN` |

### Consumed development observations

The source audit found only R5 indices **0, 12, and 24** in the prior consumed-intent ledger. They remain consumed and were excluded from selection:

| R5 index | Prior evidence | Disposition and raw evidence |
|---:|---|---|
| 0 | `results/validation/g2/decision_domain_r5_one_query_v1/attempt.json`; query `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1` | One-query preflight attempt marker; raw SHA-256 `74c53f36686bbb67ce2420c2b9975b2029ebeb93b6b39db394f35ba2a090b31d`. Its presence consumes the attempt. |
| 12 | R6 row 00 intent/terminal and R12 row 00 intent/terminal; query `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_L0_R0` | R6 was `VALID_UNKNOWN` (intent `e1585a513b9a76a506c5952ec5bbc56c48f81d332d8b90dfcd309e54152905f1`, terminal `9d4efa58c94903031c04ffa84ac6c6b9712f55e29466b931021e36e6326e3e78`). R12 row 00 exited 1 as `INVALID_OR_INTERRUPTED`; its intent is `51b26572b5194c80738099598bfa2645be084345fcf24e294e83400d873ff9f4` and terminal `2600d3d5bdac85efd6092f9253cd0c2f5fc62bcf55caafff642566332d34c44a`. R12's stored evidence does not establish the exception that caused exit 1. |
| 24 | R6 row 01 intent/terminal; query `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lp1_Rp1` | R6 was `VALID_UNKNOWN` (intent `c533ed2ce4e7890d2faf40a4165203d3a19d6e10e3f282cb5f8430d0347d21ba`, terminal `414a20e09586503a5ac103ce99e6b654c8c32931c713259e17b593edcf261064`). R12 row 01 has no intent or call. |

The R14 audit independently reports the only prior attempted query IDs as the near-center `V_Lm1_Rm1`, `V_L0_R0`, and `V_Lp1_Rp1` rows; it reports no R14-owned intent and no R14-owned R5 index. Neither selected offset-left query appears in that ledger.

## 3. Paired decision rule and interpretation

The exact R12 paired truth table is preserved in the candidate. Its semantic SHA-256 is `5f1d746577e10ab02dac0430e7909695c2cc78be0772ed4cca8b1fd4a537718a`; the six-group synthetic fixture checked the copied table for duplicate outcomes and replayed every table entry.

The sole predeclared trigger for preparing a broader study is the paired result:

> nominal action `CERTIFIED_TASK_NOT_ELIGIBLE` and positive action `CERTIFIED_TASK_ELIGIBLE` → `STRONG_TWO_SAFE_TASK_CERTIFICATION_SELECTION`; broader-study preparation trigger = `true`.

For example, nominal `VALID_UNKNOWN` paired with a task-eligible positive action is only `WEAK_CERTIFICATE_SEPARATION_INCONCLUSIVE` and does **not** trigger broader-study preparation. Resource-limit, invalid/interrupted, or not-run states stop or leave the pair incomplete; they do not trigger it. Other pairs do not establish the declared selection separation. Even the strong pair outcome would only be a preparation trigger: it grants no authority to run the 800-row study.

This is a deliberately selected **development** pair, not a holdout. It cannot estimate generalization or population performance, and no observation about voltage usefulness can be claimed before the two permitted rows are separately authorized and evaluated.

## 4. Provenance chain and source locks

The v3 candidate binds the R5 source, R4/R12 lineage, R13 diagnostic transport, R10 producer, R11 replay checker, R14 worker/runner/checker, schemas, fixture report, and audit context. The source closure contains 143 raw-hash entries (87 inherited from R4/R13 lineage and 56 added by R14). The loader streamed and checked every listed source against its locked raw SHA-256, and the candidate auditor rechecked the source and worker-import closure.

| Bound artifact | Raw SHA-256 |
|---|---|
| R5 config `validation/configs/g2_decision_domain_r5_v1.json` | `8e2816468bf682290a91535857f2c3f9ad4ff2ba8be99ec5c77acc0ca19a6e19` |
| R5 manifest | `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b` |
| R5 source closure | `53a923a0be15bd9be977040b996dc2104a763a061e2bad9ef848241a530a55e9` |
| R4 manifest / source closure | `2036404e02c32da25eb94cee803da6be4723bc67b6e23d80189d5a0e1ea0113b` / `b267d0963b2e8e7d51ba5dbe852f27d0b25a417be1b85b9ae1e1c4c4aee29fcc` |
| R12 manifest / source closure | `f0094dda957ba8e165fda21982fadee20bd2c5839ed309b1b377acc17764337f` / `adbde039053db9438e989f9d74987421aad3f5f46db4ee88af7d9d5c41c98d62` |
| R13 manifest / source closure | `d3bf7ee7ebee370c2457419169259228a17952f790c285d1d2e5cee9a0699fd8` / `51eb55764f54cba66327b3155982e64eca14d0bb785da7b6b1e122f72424f089` |
| R10 producer `validation/g2/time_slab_picard_r10.py` | `e9fa6672649d675e27bb4f419e28259b9546b01bb6592f3388396ecd2a211c47` |
| R11 independent checker `validation/g2/whole_hold_picard_checker_r11.py` | `2a794e8f46c4b029331a2548dccd1948b78d3f5d5d7a96efa118d9353ba56f7e` |
| R13 bounded capture transport `validation/g2/r13_worker_diagnostics.py` | `a6712021a7ceaad38e0c992008f6dd51f1da4ad625deeea1c0ba01e5a36bcbfa` |

### R14 candidate packet

| Artifact | Raw SHA-256 / detail |
|---|---|
| Manifest `research/benchmarks/G2_R14_SOURCE_BOUND_TWO_ROW_CANDIDATE_MANIFEST_v3.json` | `5d6cd57cbb494c42ab4b2428af9ff6863fc9dc782cd461042dc35e6f01ef5b93` |
| Manifest semantic JSON SHA-256 | `d92c30d33012faccd729ea9afc0ad6ad351dacc66a44d8b632ec49e7c42537fb` |
| Manifest raw-hash sidecar | `768ac599e3d61631a847d6145475ba3fbddedb3d4242116a3696529df1981708` |
| Source closure `research/benchmarks/G2_R14_SOURCE_BOUND_TWO_ROW_SOURCE_CLOSURE_v3.json` | `642323e50f9e9d610c99e4e5a8cd5139e35b6e73a2bd33a141131c4052008f46` |
| Closure raw-hash sidecar | `9f58dd2ada97967c2d42462b61a68d97d8ba2be3ae55fff3b81f87e33e35bd41` |
| Non-query fixture report `results/validation/g2/r14_nonquery_fixtures_v3/fixture_report.json` | `2c91e8613f00056029c8e28059afb0b2210b017378d5104dba4121108a9b43f3` |
| v3 Codex decision schema / inert NO-GO template | `4f15b0511908bd4661d50f9b55984ca75c14588bfad1f4afe0f142092746f303` / `5a3e60940f4643c7e08c9e3adaba00c811c607bbbd29bb2bce745017afd5f611` |

The closure binds each manifest entry to a regular file and its raw hash. The closure itself binds the manifest path, raw hash, and semantic hash. The manifest is explicitly `PREPARED_NOT_FROZEN_NOT_AUTHORIZED`; its source-closure and future decision paths are the v3 paths above. The separate decision schema pins the exact candidate and closure paths and limits any future scope to indices `[62, 74]`, two worker calls, zero native queries, zero study rows, no retries, a 60-second outer worker timeout, and 65,536 diagnostic bytes per stream.

The earlier v1 and v2 R14 candidate files remain unchanged as superseded drafts. Their manifest/closure/report raw hashes are respectively:

| Draft namespace | Manifest raw SHA-256 | Closure raw SHA-256 | Fixture-report raw SHA-256 |
|---|---|---|---|
| v1 | `fa216aa9e7ac417d0897eb4f44c1bddbe1e67e00541faec8093decf07a6ccbb6` | `3c096c866b8ba276a2be9fd2ec906468aec0b7550f596b18dea276cf5a8c3189` | `1b1255ec3366ce662544bf38cab2a00e70c255a25a6d938792be6ca5207b60e2` |
| v2 | `b9a60879086d4d959888c287c050d81bfb4cbf4132b01131a1e1c557e49b353e` | `af451630db0872292c0227b7355af76248b02ef44e1cc34f85d6320cba556db6` | `3764f8695dd17b4e65c73f3104b3d4a87f024889c927047b1b9a56f66f2a8317` |

The v2 manifest builder retained v1 decision-schema/template paths while emitting v2 authorization artifacts; the read-only candidate audit caught that mismatch. No v1/v2 artifact was promoted as valid. The v3 closure includes the old draft artifacts as lineage evidence, and v3 consistently binds its v3 manifest, closure, decision schema, template, and fixture report.

## 5. Worker, process boundary, and bounded capture

The candidate binds one exact entry point: `validation/scripts/run_g2_r14_picard_row_worker.py`. It accepts only the two ordered candidate rows and receives their expected manifest, closure, and query hashes from the runner. It checks the v3 candidate hashes, row status, canonical query hash and payload semantic hash before passing the bound query to `produce_whole_hold_record`. It is launched with Python isolated/no-site flags (`-I -S`) and `shell=False`.

The source import-closure audit follows both package initializers and the worker's local imports. It found eight pinned local Python source files and no process-creation import/call, dynamic import, or code-execution call. The worker therefore has no source-level route to create descendant processes under this pinned Python import closure. No process-group flag is treated as descendant containment. This is a static source argument tied to the listed hashes, not a claim that an OS sandbox was exercised.

The R13 capture transport drains stdout and stderr concurrently in 4,096-byte chunks, persists at most 65,536 bytes per stream, and records byte counts, overflow, capture completeness, exit/termination state, and hashes. R14 writes and flushes a row intent before the worker call; it persists each diagnostic stream and a producer record when present, then writes a terminal binding the intent, source/authorization hashes, record, diagnostics, and outcome. The stage stops after the first non-success or incomplete result; a durable intent is consumed and cannot be retried. `TIMEOUT`, `OVERFLOW`, `CAPTURE_INCOMPLETE`, `RESOURCE_LIMIT`, and `INVALID_OR_INTERRUPTED` remain distinguishable.

The selected fixed R10 limits are:

| Limit | Value |
|---|---:|
| Rational bit limit | 8,192 bits |
| Rational operation limit | 500,000 |
| R10 cooperative wall limit | 30 seconds |
| Base slabs | 1 |
| Split depth | 4 |
| Candidate expansions | 8 |
| Trigonometric Taylor degree | 18 |
| Square-root bisections | 48 |
| R14 outer worker timeout | 60 seconds |
| Diagnostic prefix per stream / read chunk | 65,536 bytes / 4,096 bytes |
| Maximum producer record | 64 MiB |

The worker also caps manifest/closure reads at 4/16 MiB and JSON nesting depth at 64. The independent execution checker checks file type and size before content reads; rejects symlink/reparse paths and unlisted artifacts; hashes files in bounded streaming reads; caps JSON at 8 MiB and depth 80; caps authorization/review files at 256 KiB each; caps ordinary stage artifacts at 1 MiB, each record at 64 MiB, each diagnostic at 65,536 bytes, and total stage bytes at `2 × 64 MiB + 8 × 1 MiB + 4 × 65,536`. Source closure checking caps each source file at 64 MiB and aggregate source bytes at 512 MiB. The candidate also specifies exact GO binding to raw hashes of the v3 manifest, closure, and Codex review, including the required review marker. Missing, NO-GO, mismatched, or out-of-scope authorization is refused before stage creation.

The independent checker is prepared to replay each stored R10 record with the pinned R11 replay checker and recompute the paired decision from those replayed outcomes; it does not accept the worker's status as proof. There is no R14 producer record to replay in this candidate-only run, so no R10 record replay was performed.

## 6. Non-query checks and their limits

The stored v3 fixture report is `PASS_NONQUERY_INTERFACE_FIXTURES` for all six declared groups:

1. Source rows 62/74 and their `NOT_RUN` states, plus consumed indices 0/12/24.
2. Worker import closure has no process-creation API.
3. R12 paired truth-table copy is exact, unique, and replays entry by entry.
4. Bounded JSON parsing rejects duplicate keys and excessive depth.
5. Stage inventory rejects an extra artifact and an oversized file.
6. Missing future GO is a hard prelaunch refusal.

These are synthetic, non-query interface checks. They did not launch the R14 worker or validate a real record, stage receipt, row terminal, or paired row result. The six-group report does not establish theorem soundness, real-row execution behavior, generalization, or task-level voltage usefulness.

Final source-only commands and outcomes:

```text
python -B -m py_compile validation/g2/r14_source_binding.py validation/g2/r14_worker_import_audit.py validation/g2/r14_stage_runner.py validation/g2/r14_execution_checker.py validation/g2/r14_nonquery_fixtures.py validation/scripts/build_g2_r14_candidate.py validation/scripts/audit_g2_r14_candidate.py validation/scripts/run_g2_r14_picard_stage.py validation/scripts/run_g2_r14_picard_row_worker.py validation/scripts/verify_g2_r14_nonquery_fixtures.py  PASS
python -B validation/scripts/build_g2_r14_candidate.py --manifest-only       R14_MANIFEST_PREPARED_NOT_AUTHORIZED; rows 62/74; 0 native calls
python -B validation/scripts/verify_g2_r14_nonquery_fixtures.py               PASS_NONQUERY_INTERFACE_FIXTURES; six groups; 0 worker calls
python -B validation/scripts/build_g2_r14_candidate.py                        R14_CANDIDATE_PREPARED_NOT_AUTHORIZED; closure has 143 entries
python -B validation/scripts/audit_g2_r14_candidate.py                        VALID_SOURCE_BOUND_NO_GO_CANDIDATE
```

The final audit reports pair indices 62/74, consumed indices 0/12/24, no R14-owned intent, no stage artifacts (`stage_audit.status=NOT_RUN`), zero native calls, 0/2 real rows, and 800/800 R5 study rows `NOT_RUN`.

## 7. Review and gate disposition

This is a candidate package for Codex review, not a GO request that self-authorizes execution. Codex review should first confirm the source closure, pair selection, exact worker and process-source argument, checker resource bounds, replay/paired-decision binding, and NO-GO state. Any later authorization must be a separate exact-scope Codex decision that pins the v3 manifest and closure hashes and permits only indices 62 then 74, with no retry, native query, or R5 study row.

G1 remains PASS only for the restricted reduced-model scope. G2/G3/G4 and physical-platform correspondence remain UNVERIFIED. The two selected rows are development data and would still be insufficient to establish general performance. No operational controller integration, hardware claim, or broader study is authorized by this handoff.
