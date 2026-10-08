Session: DDWMR | LUNA-G2-SCOPE

# G2 R16 — full-stage receipt parity correction

**Date:** 2026-10-05  
**Assignment:** `docs/CODEX_TO_LUNA_G2_R16_FULL_STAGE_RECEIPT_PARITY_CORRECTION.md`  
**Parent review:** `docs/reviews/CODEX_G2_R15_RUNNER_CONTROL_FLOW_REVIEW.md`  
**Disposition:** **DONE — source-bound R16 NO-GO candidate prepared for independent Codex review.** No execution authority is present.

## 1. Scope and execution ledger

R16 corrects the deterministic runner/checker row-shape mismatch, exercises the production receipt path against isolated synthetic full-stage evidence, audits the remaining transport and partial-evidence cases, and pins the new candidate and its source closure.

| Item | State |
|---|---|
| Fixed R5 pair, indices 62 then 74 | `NOT_RUN`; R16 real rows **0/2** |
| R5 study | **800/800 NOT_RUN** |
| Consumed indices | **0, 12, 24** remain consumed |
| Native `run_query` calls | 0 |
| R10 worker launches | 0 |
| Retry | None |
| Canonical R16 stage | Absent |
| Executable R16 Codex GO | Absent; inert NO-GO template only |
| Commit or push | None |

The fixtures created temporary synthetic stage trees under `tmp/` and removed them on completion. They did not create intents or a receipt under the canonical R16 stage path. R15, R5/R6/R10–R15 source/result/intent artifacts and G4 artifacts were not edited.

## 2. R15 mismatch and R16 correction

R15’s runner stored 14 row fields. Its independent checker added five fields before rebuilding the receipt, so the runner’s own completed stage could not equal the checker’s receipt. R16 defines the exact 19-field row schema in `research/benchmarks/G2_R16_ROW_RECEIPT_SCHEMA_v1.json` and enforces the field set in `validation/g2/r16_stage_contract.py`.

The row schema fields are:

`stage_order`, `r5_source_index`, `query_id`, `canonical_query_raw_sha256`, `input_payload_semantic_sha256`, `development_overlap`, `intent_sha256_raw`, `terminal_sha256_raw`, `record_sha256_raw`, `outcome`, `reason_code`, `checker_status`, `checker_replayed`, `checker_safety_certified`, `checker_task_eligible`, `transport_status`, `termination_reason`, `diagnostic_overflow`, and `capture_status`.

The runner’s `_run_row()` now records all declared fields and `_build_receipt()` rejects missing or extra fields. The checker derives the row again from the selected manifest row, on-disk intent/terminal/record, bounded diagnostic bytes, transport summary, and R11 replay result. It recomputes the transport status, summary validity, outcome, reason code, raw hashes, and checker fields before returning the row. `_audit_stage_evidence()` is the shared production receipt path: `audit_stage()` calls it after authenticating the exact GO, and the isolated fixtures call it directly without creating or accepting a GO.

The R10 producer, R11 proof replay, R12 paired truth table, and R15 stop and summary rules remain unchanged in meaning. New intent, terminal, stage-receipt, and Codex decision schemas are versioned separately for R16.

## 3. Isolated synthetic full-stage fixtures

`results/validation/g2/r16_full_stage_receipt_parity_fixtures_v1/fixture_report.json` records six on-disk full-stage cases. The fixtures call the production runner `_run_row()`, `_execute_row_loop()`, and `_build_receipt()`, then independently call checker `_audit_stage_evidence()`, `_audit_row()`, and `_receipt()`. The diagnostic transport is stubbed and checker results are explicitly synthetic; the R10 worker and real mathematical replay are not called.

| Fixture | Rows | Runner/checker result |
|---|---:|---|
| Valid `UNKNOWN` first row permits the second row | 2 | `COMPLETED`; `WEAK_CERTIFICATE_SEPARATION_INCONCLUSIVE`; no preparation trigger |
| Resource-limit first row | 1 | `STOPPED_RESOURCE`; `STOP_NO_TRIGGER` |
| Worker-failed first row | 1 | `STOPPED_INVALID_OR_INTERRUPTED`; `STOP_NO_TRIGGER` |
| Mismatched worker summary | 1 | Checker independently derives `WORKER_FAILED`; `STOPPED_INVALID_OR_INTERRUPTED` |
| No producer record | 1 | `NO_RECORD`; `STOPPED_INVALID_OR_INTERRUPTED` |
| Completed synthetic pair: task-ineligible then task-eligible | 2 | `COMPLETED`; `STRONG_TWO_SAFE_TASK_CERTIFICATION_SELECTION`; preparation trigger true, execution authority still `NOT_GRANTED` |

For all six cases, runner and checker row objects matched exactly on all 19 fields, and the stored runner receipt matched the checker’s rebuilt receipt. Stored terminal and record raw hashes are included in the fixture report.

The partial-intent fixture writes one bound intent plus two bounded synthetic diagnostic files without a terminal. The checker returns the exact row shape with `INVALID_OR_INTERRUPTED`, reason `INTENT_WITHOUT_TERMINAL`, and a null terminal hash, preserving partial evidence without retry. The no-record case independently covers a terminal with no record.

### R15-shape regression

The regression removes the same five fields from an R16 runner row to recreate the R15 shape. Both the R16 runner receipt builder and checker receipt builder reject it with `R16_ROW_RECEIPT_FIELD_SET_MISMATCH`. A second full-stage regression stores an otherwise well-formed legacy-shaped receipt with a recomputed semantic hash; the production checker rejects it with `STAGE_RECEIPT_RECOMPUTATION_MISMATCH` after independently rebuilding the full R16 row.

## 4. Fixed pair and provenance ledger

The pair remains the exact R15 pair; no substitute was selected.

| Order | R5 index | Query ID | Canonical query SHA-256 | Payload semantic SHA-256 |
|---:|---:|---|---|---|
| 0 | 62 | `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_L0_R0` | `38839995032bd4328a7c4d1059d2e3e674f3f3586a12f6f2d6c76842dfcfa8f0` | `aacb6dd0639c5d5c603ca227066352a9d04a1d2d0e92fc77ab3499f59f10db37` |
| 1 | 74 | `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_Lp1_Rp1` | `1bab855c36a6cba051736320002ea40370c793f57a04cc5a8454a71b79d2c858` | `b4ad72b1cf4e1fcc37de3bf3ed080ba4797e637e3f37919873df740043645c3b` |

The R16 candidate binds the accepted R15 parent bytes:

| Parent artifact | SHA-256 raw |
|---|---|
| R15 manifest | `01e35cf5763caa486b3741f78e9dee658d73f9d5cba81f651f310227ee332ed8` |
| R15 source closure | `6b7b178652fb6c17ebc518a571db105ba58b49e15f3351171bdf66d7b240b9c0` |

The closure inherits all **167** R15 source-input tuples and adds **25** R16/context lineage tuples. All **192** current closure inputs were independently rehashed after the final candidate build. This preserves the pinned parent lineage, including its R5/R6/R10–R15 source and evidence bindings.

## 5. Candidate and hash ledger

| Artifact | SHA-256 raw |
|---|---|
| R16 candidate manifest `G2_R16_FULL_STAGE_RECEIPT_PARITY_CANDIDATE_MANIFEST_v1.json` | `e8eaa59c676f85431e3ddcbd777a2690cfa57bfb88e00bfed96d9b4b693bba65` |
| Manifest sidecar | `b1b635e21555f903b49085cead6637d34e6b12ed7bbe432f12ea9de9944eaea1` |
| R16 source closure `G2_R16_FULL_STAGE_RECEIPT_PARITY_SOURCE_CLOSURE_v1.json` | `2217cc2c5e1ac1fce812efc9fe42a9b95f1ae2ada82ca40bb49215f1414ad759` |
| Closure sidecar | `0f12d8067e5c4e13c61bc3120db6dab850fa9517b1338522e4607c501f360f74` |
| Synthetic full-stage fixture report | `36bc1bb56fbd3a86ec09f0d19ff1ac83dab13e74780a43f7c7f8885ecbdd0c86` |
| Codex exact-scope decision schema | `7c8627edf779a58abb9aa89fc56785f4039a82f69103c761c6ff2f7f0fe6f9c2` |
| Inert NO-GO template | `d90d7c59728ee1a0c25c7ed89e1860098233e150e56358c933779bb053463677` |
| Exact row-receipt schema | `a57eea3a85057eebb14ee388226c3f532aa79260b34452477826d7c49791c5cf` |
| Row-intent schema | `eed857f0e3a820c3363de8af89b9982c9ebdd8844a6ec419c5ad722c53abbb59` |
| Row-terminal schema | `447fadcb70f9774757e7b2ffb738ae793f2600ae8df602070ee5170a770363fa` |
| Stage-receipt schema | `ad1da03539b53d17cc9f8657a815cc031d409b282bcf4466e9e34b53487bd663` |

The final source closure also pins the new executable and fixture bytes:

| R16 source | SHA-256 raw |
|---|---|
| `validation/g2/r16_execution_checker.py` | `d410e71caa524409a5e939e166c180c8f249ea27f457f254080363626f4c569a` |
| `validation/g2/r16_nonquery_full_stage_fixtures.py` | `ec03110fd9a4ddef4dde72a69a2bdb5a5ca51cdbf576e13b941a7cdf763941a7` |
| `validation/g2/r16_source_binding.py` | `70fe8e608562d840c3c750c5b8bb5d35970d44467a4255aeec47ecdbdb0bdd14` |
| `validation/g2/r16_stage_contract.py` | `40b15810fd021fac9d8dfe003d5c58458d188bccdd21ebe2b2e37c494d0820ce` |
| `validation/g2/r16_stage_runner.py` | `76c1b77d1a49a4e0f4e62ded708c6b344ac79735c91003b394409f01edafe7c2` |
| `validation/g2/r16_worker_import_audit.py` | `efef4e6f2a9e8ba8728ba959c4e696bfe92bc42560322c28e3f4adcf7440b3f5` |
| `validation/scripts/audit_g2_r16_candidate.py` | `fbac67b7e38dcd6557bffc1dadfe2aed4765e46838aacec21436d0f8915033e1` |
| `validation/scripts/build_g2_r16_candidate.py` | `3a4d62216ecf0d0607bed0537ba66500fc0a6842fc3de1ceb7208c66e40675dc` |
| `validation/scripts/run_g2_r16_picard_row_worker.py` | `1c48943c6419147fd57beddbaab3229234d7afb40c356fe97c702d639ddeac3a` |
| `validation/scripts/run_g2_r16_picard_stage.py` | `b88a0e64de7774fbbe8c00dd3b546adc1bdd1274e98320a300db6cda11c0e087` |
| `validation/scripts/verify_g2_r16_full_stage_fixtures.py` | `bd7e7476e885dfb4dd5e67d7b3f6e230b166d59b96c6f353198b799ec2f4e862` |

The manifest and closure sidecars both state `PREPARED_NOT_FROZEN_NOT_AUTHORIZED`, R16 `0/2 NOT_RUN`, and R5 study `800/800 NOT_RUN`. The NO-GO template sets `decision: NO_GO`, `template_is_executable: false`, `assignment_authorizes_execution: false`, and `retry_permitted: false`.

## 6. Verification performed

| Check | Result |
|---|---|
| CPython version | 3.12.12 |
| `py_compile` for R16 runner, checker, source binding, worker/import audit, fixture and scripts | PASS |
| R16 synthetic on-disk full-stage fixture suite | `PASS_R16_SYNTHETIC_FULL_STAGE_RECEIPT_PARITY_FIXTURES` |
| Candidate/source-closure audit | `VALID_SOURCE_BOUND_NO_GO_CANDIDATE` |
| Closure raw hashes | PASS — all 192 listed inputs recomputed |
| Missing-GO runner refusal | `ARTIFACT_MISSING:research/benchmarks/G2_R16_CODEX_SCOPE_DECISION_v1.json`; canonical stage remained absent |
| Read-only canonical stage audit | `NOT_RUN`; empty artifact inventory; zero worker calls |
| Canonical stage and executable GO presence | Both absent |
| Ruff `F821` lint | Not run: Ruff is not installed in the active Python environment (`No module named ruff`) |

The worker import audit found eight pinned local Python sources and no process-creation, dynamic-import, or code-execution API in that static closure. This is a source inspection, not an OS sandbox or worker launch test.

## 7. What the fixtures establish and what remains unverified

**Established by this candidate:** the runner and independent checker now emit/recompute the same declared 19-field row shape for the tested synthetic terminal, summary, no-record, resource-stop, invalid-stop, and complete-pair paths; terminal and record hashes are included in the parity check; the R15 row and stored-receipt shapes are rejected; `VALID_UNKNOWN` continues; stop outcomes stop; partial intent evidence remains visible and no retry path is introduced.

**Still unverified:** any real R10 worker execution or mathematical record replay; either selected row’s result; R10/R11 proof validity on these inputs; acceptance of the R16 candidate by Codex; actual behavior under an exact future GO; G2 certificate usefulness or decision-relevant voltage-selection value; G3/G4; and physical-platform correspondence. The synthetic checker outcomes are not mathematical evidence. The completed synthetic pair can set only the R12 broader-study **preparation** trigger; execution authority remains `NOT_GRANTED`.

**Disposition:** R16 is a NO-GO source candidate for Codex review only. A separate exact-scope GO would be required before either of the two real rows. No 800-row study is authorized or run. R16 remains **0/2 real rows** and the R5 study remains **800/800 NOT_RUN**.
