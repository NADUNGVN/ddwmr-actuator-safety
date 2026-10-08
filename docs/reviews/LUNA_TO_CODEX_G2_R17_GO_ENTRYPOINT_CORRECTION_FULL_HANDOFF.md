Session: DDWMR | LUNA-G2-SCOPE

# G2 R17 — GO entrypoint correction

**Date:** 2026-10-05  
**Assignment:** `docs/CODEX_TO_LUNA_G2_R17_GO_ENTRYPOINT_CORRECTION.md`  
**Parent review:** `docs/reviews/CODEX_G2_R16_FULL_STAGE_RECEIPT_PARITY_REVIEW.md`  
**Disposition:** R17 NO-GO correction candidate prepared for Codex review. This handoff grants no execution authority.

## 1. Scope and execution ledger

| Item | Result |
|---|---|
| Fixed R5 pair | Index **62**, then **74**, unchanged from R16 |
| R17 real rows | **0/2 NOT_RUN** |
| R5 study | **800/800 NOT_RUN** |
| Consumed indices | **0, 12, 24** preserved |
| Native query calls | 0 |
| Worker launches | 0; worker import closure was statically inspected only |
| R10/R11 record replay | 0 |
| Retry | None |
| Canonical R17 GO / review / stage | Absent |
| R16, R5/R6/R10–R16 and G4 files | No writes by this task |
| Commit / push | None |

All fake decisions and stages used by the positive and regression fixtures lived in a disposable operating-system temporary repository mirror. No canonical R17 GO, stage, or fixture intent was created in the repository. The R16 review text was temporarily replaced only inside that mirror for the R16 synthetic-GO regression and restored before R17 source-binding tests; the temporary tree was then removed.

## 2. R16 blocker and R17 correction

R16’s `load_r16_candidate()` rejects whenever its canonical GO decision or stage directory exists. The R16 runner calls that loader before GO validation, and `audit_stage()` calls it before reading a stage. As a result, a valid exact-scope GO cannot reach either the runner’s authorization check or the independent stage audit.

R17 uses a new `load_r17_candidate()` that verifies the pinned R16 parent, the R17 manifest and closure, every listed source hash, required R17 source/schema/fixture paths, and the worker import closure. It does not inspect GO or stage existence. The unstarted-state check is isolated in `preflight_unstarted_no_go()`. The runner does not use that pristine-state preflight: it loads the source-bound candidate, checks the exact GO, and only then attempts exclusive stage creation. The read-only checker uses the same state-agnostic loader, then authenticates the stage authorization against the current GO before replaying and comparing the receipt.

The R17 GO check retains exact key-set validation and binds the decision to the raw hashes of the manifest, source closure, and review. It requires the exact ordered pair `[62, 74]`, at most two worker calls, zero native queries, zero study rows, a 60-second worker timeout, the 65,536-byte per-stream diagnostic cap, `retry_permitted: false`, and the R17 review marker. The inert NO-GO template remains non-executable.

## 3. Isolated entrypoint fixture outcomes

The fixtures ran against a disposable mirror. The positive R17 path calls the production candidate loader, production GO validator, and production `audit_stage()` with an exact-scope synthetic decision plus an empty synthetic stage containing only authorization and receipt files. It does not call `run_stage()` with GO, because that would proceed to a worker. No fixture writes an intent, record, or mathematical certificate.

| Fixture | Exact result |
|---|---|
| Unchanged R16 runner with synthetic exact-scope GO and stage | `R16BindingError:R16_CANONICAL_STAGE_OR_GO_ALREADY_EXISTS` before worker execution |
| Unchanged R16 `audit_stage()` with that GO and stage | `INVALID_OR_INTERRUPTED`; reason `R16BindingError:R16_CANONICAL_STAGE_OR_GO_ALREADY_EXISTS` |
| R17 unstarted NO-GO preflight | `READY_NO_GO_STAGE_UNSTARTED` |
| R17 runner with missing GO | `R17AuditError:ARTIFACT_MISSING:research/benchmarks/G2_R17_CODEX_SCOPE_DECISION_v1.json`; stage not created |
| R17 runner with a NO_GO decision | `R17AuditError:R17_CODEX_GO_BINDING_OR_SCOPE_INVALID`; stage not created |
| R17 candidate loader → exact-scope GO validation → stage audit | `PASS_R17_ENTRYPOINT_CHAIN`; audit status `STOPPED_INTERRUPTED`, `receipt_valid: true`, zero rows |
| R17 receipt tamper check | `R17AuditError:STAGE_RECEIPT_RECOMPUTATION_MISMATCH` |

The `STOPPED_INTERRUPTED` positive-fixture status reflects a deliberately empty synthetic stage, not a run result. The fixtures establish entrypoint ordering, source/GO binding, and read-only receipt comparison only. They do not exercise worker execution or R11 mathematical replay, and no synthetic artifact is a safety certificate.

The final fixture report is `results/validation/g2/r17_go_entrypoint_fixtures_v1/fixture_report.json`, raw SHA-256 `0b3892ec5ff4504f3f4e0482d993d22a8b284b35194b71b65f6f5accaaddb891`.

## 4. Production-path inspection beyond the R16 receipt fixtures

The R16 synthetic receipt tests exercised row construction and receipt comparison but did not traverse authorization and canonical stage handling. R17 inspected and covered those omitted deterministic branches:

- The runner reaches GO validation only after candidate/source checks and the worker import audit. Missing and NO_GO cases both stop before stage creation.
- The stage namespace is still write-once: the runner uses exclusive directory creation and exclusive file writes. It does not overwrite a prior stage or retry a row.
- GO validation requires exact candidate and closure raw hashes, exact review raw hash and marker, exact scope, exact keys, and no retry.
- The checker first requires the exact candidate stage path, checks the stage inventory for unexpected files/reparse points, rereads the current GO, and requires byte equality with `authorization.json` before receipt replay.
- The positive empty-stage case reaches full receipt rebuilding and exact comparison. The tamper fixture confirms the production checker rejects a changed receipt.
- The ordered row loop and stop rules remain the R16 behavior: resource-limit and invalid/interrupted outcomes stop; no retry path was added.

The successful-GO production runner and worker were not executed. Therefore the two real rows, worker transport, R10 output, R11 replay on those rows, and any mathematical result remain untested. G2 stays UNVERIFIED; G1 remains PASS only for the restricted reduced-model scope; G3/G4 and physical-platform correspondence remain UNVERIFIED; overall disposition remains HOLD.

## 5. Candidate provenance and hashes

R17 is bound to the reviewed R16 manifest and closure. The new closure inherits all **192** R16 source-input hashes and adds **25** R17/context inputs, for **217** verified source inputs total. The loader rehashed the complete closure successfully; the audited source byte total was approximately **66.7 MB**.

| Artifact | Raw SHA-256 |
|---|---|
| R16 parent manifest | `e8eaa59c676f85431e3ddcbd777a2690cfa57bfb88e00bfed96d9b4b693bba65` |
| R16 parent source closure | `2217cc2c5e1ac1fce812efc9fe42a9b95f1ae2ada82ca40bb49215f1414ad759` |
| R17 candidate manifest | `a4913d3d0282de6a5d1a16c4c88e3c402a91f1c3dee2df1ea99afd44a71c6bb9` |
| R17 manifest sidecar | `ef48cfbbe78e93365246726b104fb3522c58b9dbd65d09cbc5e34d31b0f0917b` |
| R17 source closure | `5b6838c8da6ae55e33ad4b50c9182122943f669e63e0fa9d92e6a8de3b83ce86` |
| R17 closure sidecar | `c89273e8a6b8533c7e9bddeca6de08d3ad1110f27cfcfa7324d8d89c000bb03f` |

The new closure pins the R17 executable, fixture, schema, template, and fixture-report bytes. Main R17 source and schema hashes are:

| File | Raw SHA-256 |
|---|---|
| `validation/g2/r17_source_binding.py` | `6fbd24e2b9a202bb87b8d492e9610b32f5c775ba797db1c63d437a0ceba85040` |
| `validation/g2/r17_worker_import_audit.py` | `e3828ba684aaef7affb083e692dc134a4aedd35738792bc62f61228801b0089f` |
| `validation/g2/r17_stage_contract.py` | `f0144a805fc5a0cd22de90d4de78420329bf46745a9a4589186185c9b4036b27` |
| `validation/g2/r17_stage_runner.py` | `7b021ad9aab8fdff690017134b9ff7af9ec820e3f06a11eaa8bf20c3f9ae6f02` |
| `validation/g2/r17_execution_checker.py` | `59b45ff570251ddc0b1011716527cfa3e3b2180751aa231dce9099288026f50e` |
| `validation/g2/r17_nonquery_entrypoint_fixtures.py` | `2f2b272c60b78834f6c8fa537a5044d2ce12a0a8f70a55a311f294e8766ffac5` |
| `validation/scripts/build_g2_r17_candidate.py` | `db2d3eb3b7304007809593c64f4c319754b86d3c4000e5653acd67113faea907` |
| `validation/scripts/audit_g2_r17_candidate.py` | `5af25de908870fa7262a8a96cb219d3702efec91ec9a5dabbeb5faefabf1e87b` |
| `validation/scripts/run_g2_r17_picard_stage.py` | `4e0c4fb0950a870caf9da5beb7beae8d6b1a8e4b6b0cc64fe99b997464a21846` |
| `validation/scripts/run_g2_r17_picard_row_worker.py` | `d315e42988df29df59e9edb8391385735e8e7a5f1e09648fbcea5fc22bffb755` |
| `validation/scripts/verify_g2_r17_entrypoint_fixtures.py` | `5ea0e29127659939f57381e46f1a74dba5642c817b923132fd2d89c7ae670027` |
| `G2_R17_CODEX_SCOPE_DECISION_SCHEMA_v1.json` | `83ecac62e1d9dd529ff73d07864d61e3a58eaa5cc1d723b72c54110302a8a74e` |
| `G2_R17_CODEX_SCOPE_DECISION_NO_GO_TEMPLATE_v1.json` | `c94fb6da536b968a9c95f484e37e8c26b363254f4c0dd8221368189b954adba7` |
| `G2_R17_ROW_RECEIPT_SCHEMA_v1.json` | `28a771630ad67ac5a35d24f387ee9b9ff7f0b48454955ce2c8ce4c05cbf586be` |
| `G2_R17_ROW_INTENT_SCHEMA_v1.json` | `2de69ea205308282e77f1a5d135d4945a977649d0a1e4ea8fe6b3cba51746472` |
| `G2_R17_ROW_TERMINAL_SCHEMA_v1.json` | `1fce8da3a3377327c254f70ca62964ce1657212ca672ccbd78a720483bc480d9` |
| `G2_R17_STAGE_RECEIPT_SCHEMA_v1.json` | `5d014c638f98bb890f6c925912937186c24c6108010fd4ad5483f6183b99d4fe` |
| `fixture_report.json` | `0b3892ec5ff4504f3f4e0482d993d22a8b284b35194b71b65f6f5accaaddb891` |

The source-binding audit returned `VALID_SOURCE_BOUND_NO_GO_CANDIDATE`; the real canonical GO was missing and refused with `ARTIFACT_MISSING:research/benchmarks/G2_R17_CODEX_SCOPE_DECISION_v1.json`. The read-only stage audit returned `NOT_RUN`, zero worker calls, and an empty artifact inventory. R16 parent manifest/closure raw hashes still match their reviewed values.

## 6. Verification and limits

- `python validation/scripts/build_g2_r17_candidate.py` — candidate and closure built; 217 source inputs, 192 inherited from R16.
- `python validation/scripts/verify_g2_r17_entrypoint_fixtures.py` — `PASS_R17_NONQUERY_ENTRYPOINT_FIXTURES`; repeated after final closure generation with the same report bytes.
- `python validation/scripts/audit_g2_r17_candidate.py` — `VALID_SOURCE_BOUND_NO_GO_CANDIDATE`.
- The R17 worker import audit reached eight pinned local Python files and found no process-creation, dynamic-import, or code-execution API. This is static inspection only.
- Candidate source binding verified all 217 closure inputs and the fixed pair/ledger. No `py_compile`, worker, query, record replay, real row, or study was run.

R17 is a source/fixture correction candidate for Codex review only. The R16 receipt-parity and R11 mathematical replay boundaries remain explicit; no result here certifies a physical plant or mathematical safety claim.
