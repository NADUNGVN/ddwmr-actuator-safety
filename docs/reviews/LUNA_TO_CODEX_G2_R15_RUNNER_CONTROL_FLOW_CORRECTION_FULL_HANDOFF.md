Session: DDWMR | LUNA-G2-SCOPE

# G2 R15 — runner control-flow correction

**Date:** 2026-10-05  
**Assignment:** `docs/CODEX_TO_LUNA_G2_R15_RUNNER_CONTROL_FLOW_CORRECTION.md`  
**Prior review:** `docs/reviews/CODEX_G2_R14_SOURCE_BOUND_TWO_ROW_CANDIDATE_REVIEW.md`  
**Disposition:** **DONE — source-bound R15 NO-GO candidate prepared for independent Codex review.** No execution authority is present.

## 1. Scope and execution ledger

R15 fixes the R14 runner control-flow defect, tests the ordered loop with injected synthetic outcomes, prepares a new source candidate and independently audits its NO-GO state. It did not run a real row, start the R10 worker, call native `run_query`, run any of the 800 R5 study rows, retry an intent, commit, or push.

| Item | State |
|---|---|
| Predeclared R5 indices 62 then 74 | `NOT_RUN`; R15 real rows **0/2** |
| R5 study | **800/800 NOT_RUN** |
| R15 worker calls | 0 |
| Native `run_query` calls | 0 |
| Canonical R15 intent or stage receipt | None; stage directory absent |
| Executable Codex GO artifact | Absent; template remains NO-GO and inert |
| Retry authority | None |
| Commit or push | None |

The only persisted execution-related R15 output is the clearly labeled synthetic fixture report. Fixture receipts were written in temporary directories under `tmp` and removed on fixture exit; they are not canonical stage evidence.

## 2. R14 defect and R15 correction

R14 review Finding 2 identified a deterministic `NameError`: after the first row returned, `r14_stage_runner.py` referenced `STOP_OUTCOMES`, which was not defined or imported there. The R14 source remains unchanged as a failed historical candidate.

R15 puts the stop set in one source-bound module, `validation/g2/r15_stage_contract.py`. It defines `STOP_OUTCOMES` once and exports `must_stop_after`. The R15 production runner and independent stage checker import that shared rule. The production `run_stage()` calls `_execute_row_loop()`, which performs the row-return, stop/continue decision, next-row gate, and receipt construction exercised by the synthetic fixture.

The fixture also calls the actual historical R14 `run_stage()` under patched candidate, authorization, path, and row-call dependencies. It observes `name 'STOP_OUTCOMES' is not defined`, while ensuring the probe creates no row directory or canonical intent. This confirms the fixture would have caught the R14 defect without calling a worker or touching the selected rows.

### Additional source-contract mismatch found during the required path audit

The R15 runner already mapped a malformed or mismatched worker summary to transport status `WORKER_FAILED`. The checker initially derived `PRODUCER_COMPLETED` from the process exit and record, so it would reject that terminal before replaying its fail-closed invalid outcome. R15 now has the checker independently recompute summary validity from the bounded stdout bytes and bind the final transport status accordingly. A bad summary is represented as `WORKER_FAILED` plus `INVALID_OR_INTERRUPTED`, which stops the pair. A new synthetic fixture checks the runner/checker transport contract for both matching and mismatched summaries.

Timeout, diagnostic overflow, incomplete capture, worker failure, and mathematical `UNKNOWN` remain distinguishable in the transport and checker fields. A valid mathematical `UNKNOWN` is `VALID_UNKNOWN` unless the record identifies an R10 resource limit; it continues to the second row. Timeout and overflow map to `RESOURCE_LIMIT`; capture-incomplete and other invalid execution states map to `INVALID_OR_INTERRUPTED`. The shared stop contract stops after `RESOURCE_LIMIT` or `INVALID_OR_INTERRUPTED`.

The R10 producer, R11 independent mathematical checker, and R12 paired-decision truth table were not edited. The R15 closure retains their source bytes through the inherited R14 closure and current exact-source bindings.

## 3. Synthetic control-flow and receipt evidence

The fixture report is `results/validation/g2/r15_nonquery_control_flow_fixtures_v1/fixture_report.json`. It reports `PASS_R15_SYNTHETIC_CONTROL_FLOW_FIXTURES` and records zero worker calls, zero canonical intents, zero native queries, 0/2 R15 rows, and 800/800 R5 rows `NOT_RUN`.

| Injected first/second outcomes | Calls reached in the actual R15 loop | Replayed fixture receipt |
|---|---:|---|
| `VALID_UNKNOWN`, then `CERTIFIED_TASK_ELIGIBLE` | 0 then 1 | `COMPLETED`; `WEAK_CERTIFICATE_SEPARATION_INCONCLUSIVE`; no broader-study trigger |
| `RESOURCE_LIMIT` | 0 only | `STOPPED_RESOURCE`; `STOP_NO_TRIGGER` |
| `INVALID_OR_INTERRUPTED` | 0 only | `STOPPED_INVALID_OR_INTERRUPTED`; `STOP_NO_TRIGGER` |
| `CERTIFIED_TASK_NOT_ELIGIBLE`, then `CERTIFIED_TASK_ELIGIBLE` | 0 then 1 | `COMPLETED`; synthetic `STRONG_TWO_SAFE_TASK_CERTIFICATION_SELECTION` |

For each case the fixture writes and rereads a synthetic-only receipt in a temporary directory. `r15_execution_checker.replay_fixture_receipt()` independently recomputes the call projection, stop status, pair decision, and semantic receipt hash. The strong synthetic pair sets only the truth-table preparation trigger; the receipt expressly keeps `broader_study_execution_authority` at `NOT_GRANTED`. Fixture replay is control-flow replay, not mathematical record replay.

The report additionally verifies the exact shared stop-contract import, the predeclared pair, consumed-index ledger, R12 table identity, summary-validation transport behavior, and absence of the canonical R15 stage and GO artifact.

## 4. Candidate, hashes, and authorization binding

The candidate is versioned as `G2_R15_RUNNER_CONTROL_FLOW_CANDIDATE_MANIFEST_v1.json`; it is `PREPARED_NOT_FROZEN_NOT_AUTHORIZED`. Its source closure contains 167 entries: all 143 inherited R14 entries plus 24 current R15/context/lineage entries. The closure binds the manifest’s raw and semantic hashes, each source’s current raw hash, exact candidate paths, the fixed pair, bounded worker contract, and no-retry/no-GO scope.

| Artifact | Raw SHA-256 |
|---|---|
| R15 candidate manifest | `01e35cf5763caa486b3741f78e9dee658d73f9d5cba81f651f310227ee332ed8` |
| Manifest `.sha256` sidecar | `c985e96a864a30b852777c667342d45ae6e7b8506193becb747e889835b15bb0` |
| R15 source closure | `6b7b178652fb6c17ebc518a571db105ba58b49e15f3351171bdf66d7b240b9c0` |
| Closure `.sha256` sidecar | `c235387b50d9e6a6135df7ce2c80059ab9d676713fb030104c4e90c959693399` |
| Non-query fixture report | `1071bd5dbb1a53d3fad9224f97f02ceda249c1aedc62bbc22869c1a9b9f667d0` |
| Exact-scope Codex decision schema | `62624b0093fdd532eea2791ea628b080a2c8d9d6defe25e675447befec6b14a3` |
| Inert NO-GO template | `2dd9b35cf9eb96a44d8657600eeb8e057ec45926d9a7d0cc7d77406de0409bd7` |

Selected source code hashes for the control-flow path:

| Source | Raw SHA-256 |
|---|---|
| `validation/g2/r15_stage_contract.py` | `f567bb77eed942de495db711c5d7c3dcfb522ac9d915aa42ac3321692a9c6a5c` |
| `validation/g2/r15_stage_runner.py` | `939525525d55f3cf0361b34a9f0d84e82631994f577ae9d33e16f2b66b5bec0d` |
| `validation/g2/r15_execution_checker.py` | `fc339e5cff1e685bd6c50ba584daf110d99269c507a18b9ef49712511f4746dd` |
| `validation/g2/r15_nonquery_fixtures.py` | `b0b88b2a65c05aa139f81163c4ad3c62239525667f2c02ea8d409c4c8ae41f79` |
| `validation/g2/r15_source_binding.py` | `bf6c4912ff1ced37a6bd92c5f7b70a5402ed2e226f3527eea03b8f38a335a2e6` |
| `validation/g2/r15_worker_import_audit.py` | `5be182f29463aed95b7ed6ca417a0b0e6e1ec243b1633aea814dff1997cb1c68` |
| `validation/scripts/build_g2_r15_candidate.py` | `8d7614446cd2c9110f3283aa9642b1f53a3c63db2658a83d4961344cfaf982bf` |
| `validation/scripts/audit_g2_r15_candidate.py` | `d467dac979d4d7d8d77efaf61c7f1a72214e25bb34e10956b8e3c242300b2d32` |
| `validation/scripts/verify_g2_r15_nonquery_fixtures.py` | `98f861912a4f5a21677b1bc5adcace4a602a1745cdde787d98a327453d840b40` |

The exact future authorization bindings are:

- Codex decision path: `research/benchmarks/G2_R15_CODEX_SCOPE_DECISION_v1.json`.
- Required review path: `docs/reviews/CODEX_G2_R15_RUNNER_CONTROL_FLOW_REVIEW.md`.
- The decision schema fixes the scope to at most two worker calls, indices `[62, 74]` in order, zero native-query calls, zero R5 study rows, a 60-second worker hard timeout, 65,536 diagnostic bytes per stream, and no retry.
- The review must separately bind the raw hashes of the exact manifest and closure. The R15 assignment itself grants no execution.

The NO-GO template contains no executable GO and explicitly has `decision: NO_GO`, `template_is_executable: false`, `assignment_authorizes_execution: false`, and `retry_permitted: false`. No Codex review or decision artifact was created.

## 5. Fixed pair and consumed-ID ledger

The selected pair is unchanged from R14 and remains `NOT_RUN`:

| Order | R5 index | Query ID | Canonical query SHA-256 | Payload semantic SHA-256 |
|---:|---:|---|---|---|
| 0 | 62 | `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_L0_R0` | `38839995032bd4328a7c4d1059d2e3e674f3f3586a12f6f2d6c76842dfcfa8f0` | `aacb6dd0639c5d5c603ca227066352a9d04a1d2d0e92fc77ab3499f59f10db37` |
| 1 | 74 | `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_Lp1_Rp1` | `1bab855c36a6cba051736320002ea40370c793f57a04cc5a8454a71b79d2c858` | `b4ad72b1cf4e1fcc37de3bf3ed080ba4797e637e3f37919873df740043645c3b` |

The R15 source binder scanned the existing ledger and found only the already consumed R5 indices **0, 12, and 24**. Their associated near-center attempted IDs remain `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1`, `...__V_L0_R0`, and `...__V_Lp1_Rp1`. R15 owns no prior intent, selected index, or query attempt. No replacement pair was selected.

The parent R14 manifest and closure raw hashes were revalidated unchanged as `5d6cd57cbb494c42ab4b2428af9ff6863fc9dc782cd461042dc35e6f01ef5b93` and `642323e50f9e9d610c99e4e5a8cd5139e35b6e73a2bd33a141131c4052008f46`. The R5 and R6/R10–R14 evidence remains bound through the parent closure lineage. No G4 source or manifest was modified.

## 6. Bounded execution and replay contract retained

R15 keeps the R14/R13 protections: exclusive write-once intents before worker calls; no retry; the fixed Python isolated worker entry point; source-bound query payloads; exact local worker import audit; bounded diagnostic capture; file-size/type checks before bounded checker reads; and independent R11 record replay before row outcome classification. Candidate constants retain the R10 arithmetic limits, a 60-second outer worker timeout, 65,536 diagnostic bytes per stream, 4,096-byte diagnostic read chunks, and a 64 MiB producer-record cap.

The worker import audit found eight local Python files in the pinned worker closure, including both package initializers and the R10 producer dependency graph. It found no process-creation, dynamic-import, or code-execution API in that pinned local source closure. This is a source-level audit; it does not claim an OS sandbox or a real worker launch was exercised.

No R10/R11 mathematical record was produced in R15. The synthetic receipt checker explicitly returns `mathematical_record_replay: false`; R10 mathematics and real record replay remain untested in this stage.

## 7. Verification performed

| Check | Result |
|---|---|
| CPython 3.12 `py_compile` for all R15 source and entry-point files | PASS |
| Ruff `--select F821` over the R15 source, fixture, builder, auditor, and entry-point files | PASS — no undefined names |
| R15 synthetic control-flow fixture | PASS — eight declared fixture groups, no worker calls |
| Candidate manifest and source-closure builder | PASS — 167 closure entries, 143 inherited from R14 |
| Read-only candidate/source/NO-GO audit | `VALID_SOURCE_BOUND_NO_GO_CANDIDATE` |
| Missing-GO refusal probe | `ARTIFACT_MISSING:research/benchmarks/G2_R15_CODEX_SCOPE_DECISION_v1.json`; stage directory remained absent |
| Read-only stage audit | `NOT_RUN`; empty artifact inventory; zero worker calls |

The final R15 candidate sidecars and every listed source-closure input passed raw-hash verification during candidate load/audit. The R5 study state remains **800/800 NOT_RUN**.

## 8. Limits and disposition

R15 establishes only source-bound candidate preparation and synthetic control-flow behavior. It does not establish a real R15 row, a valid real R10 record, a successful run under an exact GO, G2 acceptance, task-level voltage usefulness, generalization, or a pass of any additional research gate. The pair remains deliberately selected development data, not a holdout.

**R15 real rows: 0/2 NOT_RUN. R5 study: 800/800 NOT_RUN.** R14 remains a failed historical candidate and receives no GO. R15 is ready for independent Codex review only; any future execution requires a separate exact-scope Codex GO bound to the hashes above.
