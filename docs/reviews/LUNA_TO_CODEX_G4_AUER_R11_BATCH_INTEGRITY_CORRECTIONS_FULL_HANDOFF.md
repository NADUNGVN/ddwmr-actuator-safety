Session: DDWMR | LUNA-G4-AUER

# G4 Auer R11 batch-integrity corrections — full handoff

**Date:** 2026-10-03  
**Disposition:** R11 R2 source-bound preparation candidate completed for independent review.  
**Recommendation:** **GO to independent Codex review of the exact Stage 1 candidate; NO-GO to run Stage 1 under this handoff.** A separate reviewed, exact-stage GO authorization receipt is still required.  
**Batch state:** 0/1,944. The R9 single-query preflight remains one separate completed matched pair.

## Executive summary

R11 R2 implements the R10 batch-integrity corrections in a new candidate. It binds one canonical output root and stage namespace, verifies original write-once intents and positive arm/audit artifacts, classifies malformed and absent output while the parent survives, reconstructs interruptions without retrying consumed intents, and makes comparison eligibility depend on the exact stage authorization/review and verified pair records. It also binds proof bytes through the field used by actual R9 results, `native_proof_sha256`, and cross-checks the worker-stdout hash.

The candidate reuses the exact R10 seven-stage schedule and the fixed 1,944-ID universe. Its source lock passed with 316 R9 dependencies, 359 preserved R10 dependencies, the unchanged 21-artifact R9 preflight ledger, and 376 total R11 closure dependencies. Twenty-seven non-query fixtures passed. The R11 canonical output root is absent; no stage authorization, query, producer, preflight rerun, or batch row was created.

The first R11 build at `G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v11.json` is preserved but superseded before handoff: its positive-result check expected `proof_sha256`, while the exact R9 result uses `native_proof_sha256`. **Review and use only the R11 R2 candidate below.**

## Finding 1 — source identity, R9 carry-in, and fixed schedule

**Evidence.** The R11 builder and source-lock verifier independently checked the predecessor bytes and schedule:

- R9 manifest SHA-256: `db0df35c634b91df0e498819d1480ee18c694608b2b68538a0580044132c74d8`.
- R9 closure SHA-256: `7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533`; 316/316 dependency path/hash pairs preserved.
- R9 preflight artifact ledger: `results/validation/g4/auer2013/protocol_v3_r9_single_query_preflight_v1/artifact_hash_ledger.json`, SHA-256 `f3d4733400bd6348ef56a5212f3d29ffee974a97787fe1111fe1859d2e9533c9`; 21/21 artifacts verified.
- R10 manifest SHA-256: `e03d7987b671bfb9065a1dc04b0c7bad5995e928656a15293982d14615567d23`.
- R10 closure SHA-256: `f9a742502c8f4586bfeda4f30e30f257b1c0667365b2e0646fc6b5fbf6901b87`; 359/359 dependency path/hash pairs preserved.
- R10 schedule SHA-256: `212b6a09526379188acad46aa05070626b5248a76bc64047d18dd47f9c136e9c`.
- Ordered 1,944-ID universe digest: `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`.

R11 uses the R10 schedule bytes unchanged. Stage sizes are 11, 36, 96, 450, 450, 450, and 450. Their ordered-ID digests are:

| Stage | Rows | Ordered-ID SHA-256 |
|---|---:|---|
| `stage_01` | 11 | `80383e5344268b6a7f402579615d9dbe076fd38c30b9a0bd8741951cc359c8f2` |
| `stage_02` | 36 | `7535c6047cecc7a9215d3b54f0786e91c5fbd7848661cef32fced9155d1a3043` |
| `stage_03` | 96 | `8b83929fb282983777890eb48844a1e73fdd58a3a6e97ed74f39b827f1b54a8f` |
| `stage_04` | 450 | `078bd5fe943bcc585cd983b2bf201d54c05a48012c785a59533f6b9a487584b6` |
| `stage_05` | 450 | `b6403373f7702e59f4f92bdecb5d5fa22dac3799621b6dea15dd8368baf6aaa5` |
| `stage_06` | 450 | `717f8a9153bb2dcd793df6f212f4946ae9f8ca26c6f5b058253875313a5497e9` |
| `stage_07` | 450 | `3cf6af5f84fa8223e51baea1c2b7f8d6efbd8091ecd328bfeb10fe5a5d99c42c` |

The R9 preflight ID is one read-only carry-in; the remaining 1,943 IDs are the fixed batch-eligible denominator. R11 does not claim the seed rule predates the already-observed R9 preflight result.

**Consequence.** R9 evidence and the R10 stage ordering remain the candidate's fixed source basis. No prospective query outcome was used to select or reorder IDs.

**Status:** PASS for exact-byte source identity and static schedule preparation.

**Required action:** Codex should independently recompute the R11 closure and manifest hashes and confirm the inherited R9/R10 path/hash sets before any later stage decision.

## Finding 2 — canonical root and exact-stage authorization

**Evidence.** R11 binds the manifest, future authorization, stage intent, and stage receipt to one project-relative and resolved absolute output root:

`D:/Research/Teacher_Vien/projects/ddwmr-actuator-safety/results/validation/g4/auer2013/protocol_v3_r11_batch`

Only `<root>/authorizations/<stage_id>.json` is an accepted stage-authorization path. The authorization includes the candidate manifest, closure, unchanged schedule, exact stage ID digest/count, review path/hash, and canonical root/stage namespace. The runner rejects an alternate output root and a receipt whose root binding names a second namespace. The authorization template is not a GO receipt. Non-query fixtures `duplicate_output_root_reused_authorization` and `authorization_bound_to_second_root` both passed.

**Consequence.** The R10 route for replaying one authorization into a second empty root is rejected by the R11 contract.

**Status:** PASS in source and synthetic contract fixtures; not a live Windows execution test.

**Required action:** Any later run requires Codex review of this exact candidate and a separate GO receipt for exactly one stage at the canonical authorization path. No receipt was created here.

## Finding 3 — arm and audit evidence binding

**Evidence.** A resumed positive arm must have its original invocation intent, matching `intent_sha256`, stage/ID/method/input/authorization/command bindings, and the expected result, proof, common record, worker guard, worker log, and launcher log. Positive evidence is checked against the stored R9 result validator; receipt statuses are reconciled with result and guard content. Proof-file bytes must match the R9 `native_proof_sha256` field, common-record bytes must match `common_record_sha256`, and the worker guard's nested `worker_stdout_sha256` must match the preserved worker log. Missing or changed evidence cannot be accepted as a favorable pair.

An audit receipt is bound to its original audit intent and exact result/worker-guard input hashes. PASS requires the audit report, audit guard, audit stdout and launcher log. The verifier reconciles ID, method, report/guard status, producer-call count and cross-artifact hashes; it rejects a favorable receipt field without matching stored evidence. If valid inputs are unavailable, a write-once audit-not-run record carries a reason, zero-call accounting, and hashes of available result/guard bytes; those hashes are checked on resume and summary.

The R11 summary also rejects conflicting audit terminal and audit-not-run records, unexplained arm artifacts, unbound intents, and unexpected additional attempt records before a row may be comparison-eligible.

**Consequence.** A favorable field in an arm or audit receipt is insufficient by itself to complete a pair or qualify it for comparison.

**Status:** PASS in source checks and non-query contract fixtures. No positive R11 batch evidence exists because the batch has not run.

**Required action:** Independent review should inspect the R9 result validator's compatibility with the R11 positive-artifact contract and verify that future R9 worker/auditor artifacts populate all cross-hashes as required.

## Finding 4 — malformed output and interruption accounting

**Evidence.** After a normal wrapper return, timeout, malformed JSON, or absent output, the live R11 parent preserves each available raw artifact and writes a terminal classification. Audit execution is attempted for an available arm with valid identity-bound inputs; otherwise a not-run reason is preserved. Intent-only interruption remains unresolved and is never retried. The stage ledger stores the ordered progress, per-arm/audit intent and receipt hashes, attempted IDs, complete/incomplete counts, unresolved IDs, stop reasons, and authorization/review bindings. If the parent dies before its stage receipt is written, the summary reconstructs state from the write-once stage/arm intents and available files, checks the fixed-order prefix, and does not modify an existing receipt.

The summary only permits rows named in a verified stage's completed-pair list, or a fully verified completed prefix reconstructed before an interruption. Attempts after the first nonvalid interrupted pair are rejected.

**Consequence.** A consumed intent cannot be silently retried, and malformed or interrupted work remains visible as inconclusive/incomplete instead of disappearing from the stage record.

**Status:** PASS in synthetic failure-path fixtures; real wrapper interruption behavior remains unobserved.

**Required action:** Codex should review terminal classification behavior and the interrupted-prefix constraints. Live process termination and recovery require a separately authorized stage and are not established by this preparation.

## Finding 5 — fixed-denominator summary, interpretation, and process caps

**Evidence.** The in-memory R11 summary probe produced 1,944 ordered rows: one separate preflight carry-in, 1,943 batch-eligible rows, 0 attempted batch IDs, 1,943 not-run rows, 0 comparison-eligible rows, and batch progress `0/1,944`. It does not write a summary or create the canonical batch output root. Setup-memory measurement is explicitly unclaimed. Method asymmetry, UNKNOWN/inconclusive status, the preflight stratum, and the full denominator are retained.

The R9 process-limiter source was inspected. The 120-second wall deadline is monitored by the R9 guard wrapper's monotonic clock; on expiry it terminates the worker Job Object. The Windows Job Object enforces the 1-GiB process-commit limit, active-process limit of one, and kill-on-close for the pinned CPython method-worker process launched suspended and assigned before resume. The R9 guard wrapper itself is outside that Job Object and monitors the deadline. The R11 launcher and parent-side finalization are outside both method-worker limits. The read-only composition audit uses a separate pinned verifier process, its own 120-second wrapper-monitored deadline and 1-GiB process-commit Job Object limit. The R11 outer method-wrapper timeout is 150 seconds; the audit-wrapper timeout is 630 seconds. These are static source properties and do not prove future host enforcement.

**Consequence.** Resource claims now identify the bounded child process and distinguish its 120-second wrapper deadline from its 1-GiB Job Object process-commit limit. Setup memory is not represented as measured.

**Status:** PASS for static scope description and empty-summary accounting. Comparative statistical interpretation under stagewise stopping and clustered operating cells remains open.

**Required action:** Before treating any batch output as a scientific comparison, Codex should review stagewise stopping, clustered dependence, method asymmetry, UNKNOWN handling, and the inferential plan. Do not interpret the 1,944 denominator as 1,944 observed independent samples.

## Finding 6 — non-query fixtures and verification record

**Evidence.** Twenty-seven non-query fixtures passed, retaining the eleven R10 scenarios and covering duplicate/reused root authorization, missing positive arm/audit artifacts, changed intent/result/guard, R9 native-proof and worker-log hash binding, raw producer-count and cross-hash disagreement, malformed worker/audit JSON, audit-not-run input-hash mismatch, summary eligibility gates, interrupted-stage accounting/nonprefix rejection, and fixed-denominator preservation.

Verification used the pinned interpreter `C:/msys64/ucrt64/bin/python.exe`, SHA-256 `b5c33df60c2a8421dcf8117a67e848436b5d395c71ec1c0dfd96bad10f441d7f` (CPython 3.12.12): four R11 R2 Python sources compiled in memory; five R11 JSON schemas/templates parsed; all 27 fixtures passed with 0 R3 producer calls, 0 Auer producer calls, 0 `run_query` calls, 0 matched-query evaluations, and 0 batch evaluations. The R11 R2 `--verify-only` source-lock check passed with 0 workers invoked. The empty summary was derived in memory only.

The fixture report is the new R5 report so earlier write-once reports remain byte-preserved:

`results/validation/g4/auer2013/protocol_v3_r11_batch_preparation_r5/nonquery_fixture_report.json`  
SHA-256: `f3dd93e58a820169fdfeb370224040938d7d0d162358d4d818b1ac489d1916ae`.

**Consequence.** R11 has synthetic evidence for the listed source contracts without launching any G4 query or method producer.

**Status:** PASS for non-query fixtures and source-lock construction. Fixtures do not constitute a live process, native replay, or scientific comparison.

**Required action:** Codex should independently inspect the fixture implementations and report. No fixture report authorizes a stage.

## R11 candidate artifact identities

| Artifact | SHA-256 exact bytes |
|---|---|
| `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R11_R2.md` | `96ba1632684ea052e145afbb48f13715bb3775471cbb820cf20078264b620776` |
| `validation/g4/batch_stage_runner_v3_r11_r2.py` | `e5e08a84ddb9eb9a2d65d5a60d0dc14cfd179e843e7418b5ea85e924c0e04294` |
| `validation/g4/summarize_matched_batch_v3_r11_r2.py` | `a700ffdfc3e9a63bc3ebecae90f017082fd321df2a26851873817ad87fba256b` |
| `validation/g4/protocol_v3_r11_batch_fixtures_r2.py` | `6e3e4e860480fbcf748913f5c8ee95e55bc3dc1549fc104282cf98ddab63e0e8` |
| `validation/scripts/build_g4_auer_v3_r11_candidate_r2.py` | `72109133045a47dcc2e2cf8b949ce21fdd54b70cf24c9d3ae0f96a49e5f0a902` |
| `research/benchmarks/G4_AUER_R11_ATTEMPT_RECEIPT_SCHEMA.json` | `6b5b6e0800ed3c5afcae31a9c23746f5f4e897d70be7105de6e4c3851e8b7b05` |
| `research/benchmarks/G4_AUER_R11_BATCH_SUMMARY_SCHEMA.json` | `d4a6d5839433ade5edbb3c595053e92336bb2c175da270d8bfd9ab9dede5d426` |
| `research/benchmarks/G4_AUER_R11_STAGE_RECEIPT_SCHEMA.json` | `00ccd1c83f491d1cd20c410c6adb9ecd5ee61377fc6c8d558fcac7cd198b2c43` |
| `research/benchmarks/G4_AUER_R11_AUDIT_NOT_RUN_SCHEMA.json` | `8142c41bcd3badb1d60ff6ac51b8b4ce5f21d1adbac094154afeb925c73c392e` |
| `research/benchmarks/G4_AUER_R11_R2_STAGE_AUTHORIZATION_RECEIPT_TEMPLATE.json` | `61aeba95ec58f7bd4bac0cd6e0d01ba9abadc0b08d371891b401ceb67ade7eed` |
| R11 R2 fixture report `results/validation/g4/auer2013/protocol_v3_r11_batch_preparation_r5/nonquery_fixture_report.json` | `f3dd93e58a820169fdfeb370224040938d7d0d162358d4d818b1ac489d1916ae` |
| R11 R2 source closure `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R11_R2.json` | `dbe23888fac40caf518009dd96f888e1da45eace388d9ace8cffe906074cbf7b` |
| R11 R2 manifest `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v11_R2.json` | `193dbead525d1a1c2fae00920a2ff385e7281a6a28aae00e69d72ea7778d106d` |
| R11 R2 manifest sidecar `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v11_R2.sha256` | `d83228a31fa959e7aea4523c5692f3445afb60789fdd62d29f869b00af342b82` |

The closure contains 376 exact-byte dependencies; its verified R10 and R9 dependency subsets remain 359 and 316, respectively. The R10 schedule artifact and digest are unchanged. The manifest records `batch_start_authorized=false`, zero attempted batch rows, one preflight pair, and `separate_stage_authorization_required=true`.

## Final disposition and required next step

**Preparation status: DONE.** R11 R2 is ready for independent Codex source review. **Stage 1 status: NO-GO** until that review reaches an independent decision and a separate exact-stage authorization receipt is created at the canonical root. This handoff grants no execution authority.

No batch query, query 1, preflight rerun, producer, or audit worker was run. No R9 or R10 source/evidence file was edited. The R11 canonical output root remains absent; there is no R11 authorization receipt. Preserve the research disposition: HOLD; G1 restricted reduced-model PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED. No novelty, physical-safety, or comparative-performance claim is made.
