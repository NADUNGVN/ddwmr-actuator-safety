Session: DDWMR | LUNA-G2-SCOPE

# Luna → Codex — G2 R5 one-query runner preparation handoff

**Date:** 2026-10-03  
**Assignment:** `docs/CODEX_TO_LUNA_G2_DECISION_DOMAIN_R5_ONE_QUERY_RUNNER_PREPARATION.md`  
**R4 review read before implementation:** `docs/reviews/CODEX_G2_DECISION_DOMAIN_R4_INTEGRITY_REVIEW.md`  
**Repository:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Branch / HEAD:** `main` / `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe` (unchanged)  
**Disposition:** R5 one-query candidate, sealed runner source, independent bundle auditor, fixture suite and authorization-receipt template prepared. No real query was run. **800/800 `NOT_RUN`.**

## Decision

**NO-GO for a later one-query execution at this point.** The R4 candidate remains accepted only as a non-query integrity preflight. R5 now supplies the exact-index runner and independent replay auditor, but Codex has not yet reviewed the R5 bytes, the R5 accepted-review file does not exist, and no explicit user authorization receipt exists. The runner stops before `run_query` when either receipt is absent. The receipt artifact created here is only a template and says `TEMPLATE_NOT_AUTHORIZED`.

The selected row remains manifest index `0`, `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1`; its canonical query hash and native R3 payload hash match the hashes already declared by the R4 proposal. It is a plumbing row chosen by frozen order, not evidence of task usefulness or voltage-selection value.

## Finding 1 — candidate bytes and exact predecessor binding

**Finding.** R5 creates a separate, unfrozen candidate and source closure. It preserves the full ordered R4/R3 v6 study universe and binds the selected index-0 query to the proposal.

**Evidence.** `validation/g2/decision_domain_adapter_r5.py` loads and verifies R4 v1, all 57 R4 closure inputs, the R5 config, manifest, sidecars and 74-entry R5 closure. It checks that the 800 R5 row objects exactly equal R4, including order, profile and `NOT_RUN` markers; it also requires every inherited R4 closure entry to remain present in R5's closure. The selected row is reconstructed with the unchanged R4/R3 adapter. Its canonical query raw SHA-256 is `3668b9fb3bf30e11b8b177508f8b519855e8d4e96e33d7352335cbaea838db17`; its R3 `input_sha256` payload semantic SHA-256 is `dde72762c6a6feb8932d0d617c11cefbe271ecaba288bc6d282d8be19bcbb0a5`.

The R5 lineage pins R4 config/manifest/closure raw SHA-256 values `50cb4387eb436af4da903483299fc1b338820a86083ec35fd1bccfef2d5389db`, `2036404e02c32da25eb94cee803da6be4723bc67b6e23d80189d5a0e1ea0113b`, and `b267d0963b2e8e7d51ba5dbe852f27d0b25a417be1b85b9ae1e1c4c4aee29fcc`. The native R3 v6 manifest raw/semantic hashes remain `5ca87bc92429290d0c3967b3331f2a6cfec3b9482c7b5a7cc7532fbb5db20907` / `f6744f4e5b75026c0ba83fc51740f60f75ad98bca0d5a0d72129cf54128f40fb`; its closure raw hash is `b6b5c8b91fdc7c7dbc3c3b02fefb719f5aeeeaf9576ddf7cbbd584c9864b3469`; profile semantic hash is `868b9efef503335f04fd65ec3635f5ba6713717dfcbde64fea186cf291af9b37`. The R4 proposal raw SHA-256 is `a302c144a919a1e4501afe973593bf479e8e93f7e66064e5375c6f96d97cbabf`; accepted R4 review raw SHA-256 is `21994d1e5da979c05ddaa292a538713f8b291395a919bf155ff111eeadb29597`.

R5 candidate/closure artifacts and raw hashes:

| Artifact | Path | Raw SHA-256 |
|---|---|---|
| Effective config | `validation/configs/g2_decision_domain_r5_v1.json` | `8e2816468bf682290a91535857f2c3d8d6d5acd4c5edf14e23a4623a205f1d5` |
| Config sidecar | `validation/configs/g2_decision_domain_r5_v1.json.sha256` | `ef171c622d537f6ce2877f3c66936cda3dcebffbdd26be0040f96b44f285c873` |
| Candidate manifest | `research/benchmarks/G2_DECISION_DOMAIN_R5_MANIFEST_CANDIDATE_v1.json` | `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b` |
| Manifest sidecar | `research/benchmarks/G2_DECISION_DOMAIN_R5_MANIFEST_CANDIDATE_v1.json.sha256` | `d88848aa6ce9fecd794a8f18a3a6c8a8cce9c26c30cc9536aa4e6f1416cef18d` |
| Source closure | `research/benchmarks/G2_DECISION_DOMAIN_R5_SOURCE_CLOSURE_v1.json` | `53a923a0be15bd9be977040b996dc2104a763a061e2bad9ef848241a530a55e9` |
| Closure sidecar | `research/benchmarks/G2_DECISION_DOMAIN_R5_SOURCE_CLOSURE_v1.json.sha256` | `cfa45032c42375f700469f417e3af7776df6d409c73a7b9f6ce611e5087f58bf` |
| Freeze/authorization template | `research/benchmarks/G2_DECISION_DOMAIN_R5_ONE_QUERY_FREEZE_AUTHORIZATION_RECEIPT_TEMPLATE_v1.json` | `0db20b58822efd618fd6eeec9551a5ef4ce42837d1b683151883dda90ee25ca0` |

**Consequence.** The new files pin an exact plumbing row without freezing or changing the R4 candidate. The 74-entry closure identifies every R5 source/input and carries the R4 lineage; it does not claim a study outcome.

**Status.** PASS for candidate structure, lineage and read-only closure verification. Candidate remains unfrozen; all **800/800 rows remain `NOT_RUN`**.

**Required action.** Codex should review the R5 candidate and its 74 closure entries, especially the exact row/query binding and source-to-decision map, before considering any execution stage.

## Finding 2 — sealed one-query call boundary and durable evidence capture

**Finding.** `validation/scripts/run_g2_decision_domain_r5_one_query.py` is a fixed-index CLI. It accepts no arguments, has no row override or batch loop, and only prepares index 0. It cannot proceed without an exact R5 review and one-query authorization receipt.

**Evidence.** The runner reloads and validates R5/R4/R3 bytes and the closure-bound runner/module hashes; reconstructs the row; checks both predeclared query hashes; binds the proposal and accepted R4 review; then validates the exact R5 candidate/closure, selected-row, runner, accepted R5 review and user-authorization fields in the receipt. It refuses changed row IDs, alternate CLI arguments, stale source bytes/hashes, absent review/authorization, an existing final output path, an existing attempt marker or checkpoint. A write-once attempt marker is flushed immediately before the native call. The R3 evaluator's returned Python record is serialized once to canonical JSON and checkpointed with `fsync` before replay; caught exceptions are checkpointed the same way. Resource `UNKNOWN` records retain their resource diagnostics. The R3 checker is replayed against the reconstructed query; if a safety record exists, the R2 endpoint record is created and replayed against the same query. Exceptions and replay failures remain explicit non-successes; `UNKNOWN` is not relabeled unsafe.

On a complete call, the output directory is write-once and atomically published with `COMMIT.json`. The bundle is labeled exactly `ONE_QUERY_PREFLIGHT_ONLY_NOT_STUDY_RESULT`, contains the exact safety and endpoint record bytes, the durable call checkpoint, R3/R2 diagnostics, timing, runner/review/receipt and candidate hashes, and cannot be passed to the R4 800-row aggregate. It leaves the manifest unchanged. The evaluator wall-time limit is recorded as cooperative; no hard outer timeout is claimed.

Runner/source hashes:

| Source | Path | Raw SHA-256 |
|---|---|---|
| R5 candidate adapter | `validation/g2/decision_domain_adapter_r5.py` | `ea7cfbcd624b11e0e26352f6a8a524b8ab5d24b389e4767b923438aa133663c2` |
| Runner module | `validation/g2/one_query_runner_r5.py` | `3a15aed792eca24e036657f4613f5bc28f609885d7c966d739fe13064cd1711e` |
| Sealed runner CLI | `validation/scripts/run_g2_decision_domain_r5_one_query.py` | `4a5885528a5c9aebab76ad38b3278a66e75cb44e5b90f6f5fc52fbd41b1fe66a` |
| Candidate builder | `validation/scripts/build_g2_decision_domain_r5_candidate.py` | `29dc8f191a4d499595dec20f5f836b6b1ffc9b5ffffeae3956df3c000e70f787` |

**Consequence.** A later valid call has one fixed row and one persisted attempt slot. If output publication fails after the call, the attempt remains consumed; a checkpoint/staging artifact is evidence of an incomplete attempt and cannot be mistaken for a complete bundle. A process or system failure during the narrow interval after native return and before the checkpoint is durably written can still leave only the attempt marker; no retry is allowed under the one-call cap.

**Status.** PASS for source-bound preconditions and synthetic call-path fixtures. No real `run_query` call occurred. The attempt/review/authorization limits are not cryptographic authentication: Codex acceptance and the user's explicit instruction remain separate human events.

**Required action.** Review the exact runner and checkpoint protocol. If accepted, create the R5 review and an actual receipt only after explicit one-query user authorization; do not reuse the template as authorization.

## Finding 3 — independent post-publication R3/R2 auditor

**Finding.** `validation/scripts/audit_g2_decision_domain_r5_one_query_bundle.py` invokes an independent read-only auditor. It checks bundle bytes and then recomputes the proof and status fields.

**Evidence.** `validation/g2/one_query_auditor_r5.py` rejects staging directories and non-final bundle names; checks the exact member set, completion marker and all payload hashes; reloads the R5/R4/R3 candidate; reconstructs the selected query; validates R5 runner/module source hashes, receipt/review hashes, attempt marker and checkpoint; verifies raw record bytes/lengths/offsets; replays the safety record through the native R3 checker; recreates and replays the R2 endpoint; then compares checker diagnostics and the stored outcome/status/count fields with recomputation. `COMMIT.json` hash consistency alone is not accepted as proof replay.

The auditor and CLI hashes are:

| Source | Path | Raw SHA-256 |
|---|---|---|
| Independent auditor | `validation/g2/one_query_auditor_r5.py` | `1987db2ad8c256da299d920a86eb04ab929d2dd06d54df64a57741b5a5824287` |
| Auditor CLI | `validation/scripts/audit_g2_decision_domain_r5_one_query_bundle.py` | `ab6e6e27696de8b70dc27819eac56a80860aa62d2c498ba71e28d5aedc5b7916` |

**Consequence.** Editing a summary or inserting a fake proof and recomputing the bundle's payload digest does not make the bundle pass. An output without all required members or with only a self-consistent marker is rejected.

**Status.** PASS on temporary fixture bundles. The production output path is absent, so the CLI correctly returned `REJECTED_READ_ONLY` for the absent bundle; there is no real bundle to audit.

**Required action.** Codex should inspect the auditor independently of the runner, including its R3/R2 replay and status/count recomputation.

## Finding 4 — non-query adversarial fixtures

**Finding.** The one-call path and independent auditor were exercised with injected stubs and read-only R3 archive records only.

**Evidence.** `python -B -m validation.scripts.verify_g2_decision_domain_r5_fixtures` exited `0` with `PASS_NONQUERY_FIXTURES`, `native_run_query_calls=0`, three injected stub calls in temporary directories, and no study denominator or manifest change. It demonstrated:

- Changed selected ID, alternate CLI row, stale runner hash and altered runner bytes all stop before the stub call.
- Missing freeze/authorization receipt, missing R5 review, missing user authorization, existing output path and consumed attempt marker all stop before the stub call.
- One injected resource `UNKNOWN` call produces an audited one-query bundle; a second invocation with another output location is rejected by the persistent attempt marker and does not call the stub again.
- One injected exception is captured in the immediate checkpoint and audited as a non-success.
- A write failure after the safety record leaves an unpublished staging directory and durable checkpoint; the auditor rejects the stage and the final bundle path remains absent.
- Summary tampering and proof insertion were each followed by recomputing the `COMMIT.json` payload digests. The auditor rejected them (`SUMMARY_STATUS_OR_COUNT_FIELDS_DIFFER_FROM_RECOMPUTATION` and `ENDPOINT_RECORD_DIFFERS_FROM_NATIVE_RECOMPUTATION`).
- A read-only archived proof-bearing `UNKNOWN` (pilot line 18) replayed as `UNKNOWN` under native R3 and its R2 endpoint replayed. A synthetic resource-abstention record built from archived certified bytes was checker-classified as integrity-valid/resource-limited; R2 kept its `SAFETY_REPLAY_REJECTED` diagnostic instead of turning it into task success.
- Candidate denominators were left untouched. The R4 manifest raw hash matched before and after; all 800 rows in R5 remain `NOT_RUN`.

Fixture source raw SHA-256: `validation/scripts/verify_g2_decision_domain_r5_fixtures.py` — `cc02945cb6882d1a5107f663619a186c13cac3deaff990bcfaba21ed215e4576`.

**Consequence.** These fixtures check fixed-row plumbing, rejection paths, durable capture and replay enforcement only. Stub calls and archived records are not R5 study outcomes, and no performance, usefulness or G2 claim follows.

**Status.** PASS for non-query adversarial fixtures. Native query calls: `0`; study rows: **800/800 `NOT_RUN`**.

**Required action.** Treat the fixture result as code-path evidence only. Re-run it after any source change; such a change invalidates the R5 source closure and requires a refreshed unreviewed draft before review.

## Finding 5 — receipt template and call-count semantics

**Finding.** A concrete one-query freeze/authorization receipt template is bound to the exact R5 candidate bytes, selected query, R4 proposal, runner and accepted R4 Codex review. It explicitly does not claim authorization.

**Evidence.** `research/benchmarks/G2_DECISION_DOMAIN_R5_ONE_QUERY_FREEZE_AUTHORIZATION_RECEIPT_TEMPLATE_v1.json` records R5 config/manifest/closure/profile raw or semantic hashes; R4 config/manifest/closure; proposal hash; index `0`, query ID and both query hashes; runner path/hash; and the accepted R4 review path/hash/decision. Its status is `TEMPLATE_NOT_AUTHORIZED`; the R5 runner review hash and explicit user authorization are required future fields. Runtime receipt path `research/benchmarks/G2_DECISION_DOMAIN_R5_ONE_QUERY_FREEZE_AUTHORIZATION_RECEIPT_v1.json` and R5 review path `docs/reviews/CODEX_G2_DECISION_DOMAIN_R5_ONE_QUERY_RUNNER_REVIEW.md` are absent. Neither file was created by this assignment.

The R5 closure defines `run_query_invocations` as native function call attempts; `run_query_completed_count` separately counts calls that returned. A later full-study attempt ledger must still contain 800 row-attempt entries when a pre-call failure prevents a native call, with a distinct status explaining that no native invocation occurred. Thus pre-call row attempts remain in the fixed denominators while invocation count can be lower than 800.

**Consequence.** The template gives Codex and the user exact fields to approve later while leaving both required events pending. Hash consistency checks do not authenticate the author of a receipt; R5 code review and explicit user authorization must remain independent requirements.

**Status.** PASS as an unauthorized, byte-bound template. No review receipt, user authorization receipt, freeze or real query exists.

**Required action.** After Codex reviews R5, replace the placeholders only with the accepted R5 review hash and a separately received exact user instruction for this one row. Never use this template to infer permission.

## Finding 6 — commands, hashes and preserved state

**Finding.** The final R5 candidate validates read-only; fixtures invoke no native evaluator; the runner and auditor fail closed in the current unauthorized state.

**Evidence.** Final commands and outcomes:

| Command | Exit | Result |
|---|---:|---|
| `python -B -m validation.scripts.build_g2_decision_domain_r5_candidate --refresh-unreviewed-draft` | 0 | Refreshed only new R5 v1 artifacts after source stabilization; refused to run if an R5 review, authorization, attempt/checkpoint or output exists; never touched R4 v1 |
| `python -B -m validation.scripts.build_g2_decision_domain_r5_candidate --check-only` | 0 | `PASS_READ_ONLY`; 74 closure inputs; 800 rows not run |
| `python -B -m validation.scripts.build_g2_decision_domain_r5_candidate --validate-closure-only` | 0 | `PASS_READ_ONLY`; 74 closure inputs; all sidecars and source hashes verified |
| `python -B -m validation.scripts.verify_g2_decision_domain_r5_fixtures` | 0 | All listed non-query fixtures passed; 0 native `run_query` calls |
| `python -B -m validation.scripts.run_g2_decision_domain_r5_one_query` | 2 | `NO_CALL_PRECONDITION_STOP: MISSING_FREEZE_AUTHORIZATION_RECEIPT`; call-attempt count 0 |
| `python -B -m validation.scripts.audit_g2_decision_domain_r5_one_query_bundle` | 2 | `REJECTED_READ_ONLY: BUNDLE_MEMBER_MISSING:COMMIT.json`; expected because no output bundle exists |

Manifest inspection found exactly 800 records, all 800 `NOT_RUN` with null result records. R4 manifest raw SHA-256 stayed unchanged during fixtures. The active authorization receipt, R5 accepted review, one-shot marker, checkpoint and production output directory are all absent. HEAD remains `main` at `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`. Existing dirty `.gitattributes`, the G4 R5 source-index review and the other shared G4/Auer artifacts were left untouched. No branch switch, clean, commit or push occurred.

**Consequence.** R5 is a reviewable preparation package, not a frozen or executed one-query result. The accepted R4 review's NO-GO boundary remains in effect for actual execution until R5 itself is reviewed and the user separately authorizes the exact query.

**Status.** PASS for preparation and read-only validation. Overall HOLD; G2 remains UNVERIFIED; **800/800 `NOT_RUN`**.

**Required action.** **NO-GO** for a later exact one-query preflight until Codex accepts the R5 runner, auditor, closure and receipt template and a separate explicit user authorization is recorded. A future source change requires a new closure hash and review. Do not advance G2, G3, G4 or run the 800-query study.

