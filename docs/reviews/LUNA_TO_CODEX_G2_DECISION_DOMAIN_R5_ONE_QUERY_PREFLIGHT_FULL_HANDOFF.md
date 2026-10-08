Session: DDWMR | LUNA-G2-SCOPE

# G2 R5 One-Query Preflight - Full Handoff

**Date:** 2026-10-03  
**Repository:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Assignment:** `docs/CODEX_TO_LUNA_G2_DECISION_DOMAIN_R5_ONE_QUERY_PREFLIGHT.md`  
**Accepted runner review:** `docs/reviews/CODEX_G2_DECISION_DOMAIN_R5_ONE_QUERY_RUNNER_REVIEW.md`  
**Branch / HEAD:** `main` / `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe` (unchanged)

## Disposition

Exactly one native `run_query` call was attempted for manifest index `0`, `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1`; it returned normally. The user's conversation message explicitly granted that one call. However, the active receipt's `exact_instruction` was written with ASCII `?` in place of Vietnamese diacritics, so its recorded instruction hash does not bind the verbatim user message. The independent published-bundle auditor passed its R3 and R2 proof replays, but the receipt-provenance requirement is BLOCKED. Do not retry or rewrite the consumed write-once receipt/bundle. The R3 result is `UNKNOWN`; the 800-row study remains **800/800 `NOT_RUN`**. No source, candidate, manifest, or G4/Auer artifact was edited; no branch switch, commit, or push occurred.
## Finding 1 - User authorization and exact preflight binding

**Finding.** The separate user instruction explicitly authorizes exactly one native call for the selected query. A write-once runtime receipt was created from the template, and the runner's read-only preparation accepted all bindings before the call.

**Evidence.** Before the receipt existed, the required read-only command

```text
python -B -m validation.scripts.build_g2_decision_domain_r5_candidate --check-only
```

exited `0` with `PASS_READ_ONLY`, 74/74 closure inputs checked, the selected query ID reported, and `rows_not_run: 800`. At that time the runtime receipt, attempt marker, checkpoint and final output directory were all absent. Exact-byte and query bindings were:

| Binding | SHA-256 / value |
|---|---|
| R5 config raw bytes | `8e2816468bf682290a91535857f2c3f9ad4ff2ba8be99ec5c77acc0ca19a6e19` |
| R5 candidate manifest raw bytes | `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b` |
| R5 source closure raw bytes | `53a923a0be15bd9be977040b996dc2104a763a061e2bad9ef848241a530a55e9` |
| Sealed one-query CLI raw bytes | `4a5885528a5c9aebab76ad38b3278a66e75cb44e5b90f6f5fc52fbd41b1fe66a` |
| Accepted R5 review raw bytes | `867a967c157040627a897ecb5c9889a3d0dfde7a2f34af4ae0e13620a1c073c9` |
| Canonical selected-query raw hash | `3668b9fb3bf30e11b8b177508f8b519855e8d4e96e33d7352335cbaea838db17` |
| R3 native input-payload semantic hash | `dde72762c6a6feb8932d0d617c11cefbe271ecaba288bc6d282d8be19bcbb0a5` |

The preserved exact authorization instruction was:

> 2. Nếu bạn muốn cho chạy preflight: Tôi cho phép `LUNA-G2-SCOPE` gọi native `run_query` **đúng một lần** cho `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1`, theo assignment G2 R5 one-query preflight. Không chạy query khác hoặc batch 800 hàng.

Its truthful reference is `current conversation: user's 2026-10-03 instruction, item 2 (explicit one-query authorization)`. UTF-8 instruction SHA-256: `13e209f5a3f0de042998618b4703b9fc379b40a3b6ab8f5041dddbae20ade1b6`.

The one-time receipt is `research/benchmarks/G2_DECISION_DOMAIN_R5_ONE_QUERY_FREEZE_AUTHORIZATION_RECEIPT_v1.json`, raw SHA-256 `5672096c8c3c636dd51bef77f109bc7496cb410dfb82b49a00aa776ae51d62d0`. It records `AUTHORIZED`, `ONE_QUERY_ONLY`, maximum native calls `1`, index `0`, the selected query, and the accepted review hash. The read-only `prepare_authorized_call` path returned `PASS_READ_ONLY_PREPARE_AUTHORIZED_CALL` after verifying 74 closure entries and internal receipt/review/query bindings, with marker, checkpoint, and final output path absent. That check validated receipt self-consistency; it did not compare the instruction field with the user's conversation message.

**Receipt integrity caveat (detected after the call).** The decoded receipt instruction is ASCII-only and reads `2. N?u b?n mu?n cho ch?y preflight: T?i cho ph?p ... Kh?ng ch?y query kh?c ho?c batch 800 h?ng.`; every Vietnamese diacritic was lost as `?`. Stored instruction SHA-256 `4e5e84ad4357445ad9fb622fa2ae0301bde88e43d18d8a2de86772a4b1871a2f` correctly hashes that corrupted string, but the verbatim user instruction above has UTF-8 SHA-256 `13e209f5a3f0de042998618b4703b9fc379b40a3b6ab8f5041dddbae20ade1b6`. The conversation contains the user's explicit one-call authorization, so the call was authorized by the user; the receipt nevertheless fails the assignment's exact-text provenance requirement.

**Consequence.** Candidate, review, selected-row, and source bindings matched, but the authorization-text receipt is not verbatim. This was detected after the one-shot marker and final bundle were written. Preserve both write-once artifacts unchanged; the call cap is consumed, so this defect cannot be repaired by rewriting the receipt or retrying. The config-hash erratum remains corrected using the verified 64-character config hash above.

**Status:** BLOCKED for exact-verbatim receipt provenance; the user's direct one-call permission was present, one call returned, and the published bundle independently replays.

**Required action:** Codex should review this provenance discrepancy together with the raw receipt and bundle. Do not retry, rewrite the receipt, or run another row under the consumed authorization.

## Finding 2 - One native call and result

**Finding.** The sealed runner was invoked once with no arguments and completed one native `run_query` call.

**Evidence.** Exact command:

```text
python -B -m validation.scripts.run_g2_decision_domain_r5_one_query
```

Exit code: `0`. Captured stdout:

```json
{"bundle_path": "D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety\results\validation\g2\decision_domain_r5_one_query_v1", "files": 10, "native_call_completed": true, "status": "ONE_QUERY_PREFLIGHT_ONLY_NOT_STUDY_RESULT"}
```

The attempt marker records one attempt beginning at `2026-10-03T12:07:24.274501Z`; the durable checkpoint records one completed call, `native_exception: null`, a 70,616-byte returned safety record, and its raw SHA-256 `aa12f85b94b41d2f267be985ae93e8fc3abe73c97936add4504f7072bd072c23`. The summary ended at `2026-10-03T12:07:24.387105Z`; its display-only elapsed value is `0.10999999999967258` seconds. The R3 evaluator's 15-second limit remains cooperative, not a hard outer timeout.

The raw R3 record reports:

- `status: UNKNOWN`;
- `reason_codes: CONTACT_SUFFICIENT_MARGIN_NEGATIVE, COLLISION_SUFFICIENT_MARGIN_NEGATIVE`;
- query `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1` and action `V_Lm1_Rm1`;
- `review_status: PENDING_INDEPENDENT_AUDIT` in the native record.

The negative interval lower/sufficient margins mean this evaluation could not establish the required collision and contact-domain margins. They do not prove an actual collision or contact violation. On independent replay, R3 reports `proof_replay_pass: true` and `record_integrity_valid: true` while retaining `UNKNOWN`; checker operations: `29405`. The R2 endpoint was created and replayed, with status `PROGRESS_BOUND_ONLY_SAFETY_UNKNOWN`, `task_eligible: false`, and checker operations `1236`. Its progress lower bound is negative, so it supplies no positive endpoint-progress result.

**Consequence.** The native function returned and its record was durably checkpointed, but the outcome is inconclusive. It does not certify safety, establish unsafety, establish endpoint progress, or show that voltage selection helps a task.

**Status:** One call attempted; one call returned; raw safety status `UNKNOWN`; R3 and R2 replay diagnostics preserve that inconclusive status.

**Required action:** Keep `UNKNOWN` and the negative sufficient-margin reasons explicit in any later synthesis. Do not reinterpret this row as `CERTIFIED`, `UNSAFE`, or a task-success result.

## Finding 3 - Independent published-bundle audit

**Finding.** The independent read-only auditor accepted the exact published bundle and independently replayed both R3 and R2.

**Evidence.** Command:

```text
python -B -m validation.scripts.audit_g2_decision_domain_r5_one_query_bundle
```

Exit code: `0`. Complete auditor diagnostic:

```json
{
  "bundle_status": "ONE_QUERY_PREFLIGHT_ONLY_NOT_STUDY_RESULT",
  "commit_sha256_raw": "2b6f6b1bab90a072998e94ae2f5df2d871bd925715540471a838a01bb0cb8756",
  "query_id": "S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1",
  "r2_endpoint_replayed": true,
  "r3_replayed": true,
  "receipt_sha256_raw": "5672096c8c3c636dd51bef77f109bc7496cb410dfb82b49a00aa776ae51d62d0",
  "run_query_call_attempt_count": 1,
  "status": "PASS_READ_ONLY_PROOF_REPLAY",
  "study_denominators_touched": false,
  "study_rows_not_run": 800
}
```

Raw SHA-256 for every published bundle member:

| Bundle member | Bytes | SHA-256 |
|---|---:|---|
| `attempt.json` | 853 | `74c53f36686bbb67ce2420c2b9975b2029ebeb93b6b39db394f35ba2a090b31d` |
| `authorization/r5_codex_review.md` | 7,184 | `867a967c157040627a897ecb5c9889a3d0dfde7a2f34af4ae0e13620a1c073c9` |
| `authorization/receipt.json` | 3,167 | `5672096c8c3c636dd51bef77f109bc7496cb410dfb82b49a00aa776ae51d62d0` |
| `COMMIT.json` | 952 | `2b6f6b1bab90a072998e94ae2f5df2d871bd925715540471a838a01bb0cb8756` |
| `diagnostics.json` | 2,868 | `30c4f3dfad68db8a6b2ccbed95204200d77d6330735bc2ada49ad4cd848fe365` |
| `endpoint_record.json` | 11,022 | `b81b408e7d446dc3af1eb69b757418a872d425d985cd076caeb2adf1d5cb58d6` |
| `ledger.json` | 113,260 | `b8ae0e835ac9f71187a93eb09fd7651411bfc0b9ca9f4ee4e26a879bfaccf297` |
| `native_call_checkpoint.json` | 95,108 | `2b36fee53b1da17810c36ca311dc0626eb78f193a2ca7e449d85f4f110cac24e` |
| `safety_record.jsonl` | 70,616 | `aa12f85b94b41d2f267be985ae93e8fc3abe73c97936add4504f7072bd072c23` |
| `summary.json` | 765 | `400eb54dbee533397c8b9c090aa43e8b73a9ecf30bcc128692483e2fd5c4674d` |

External write-once attempt marker `results/validation/g2/decision_domain_r5_one_query_attempt_v1.json` SHA-256: `74c53f36686bbb67ce2420c2b9975b2029ebeb93b6b39db394f35ba2a090b31d`. External durable checkpoint `results/validation/g2/decision_domain_r5_one_query_attempt_v1.json.native_call_checkpoint.json` SHA-256: `2b36fee53b1da17810c36ca311dc0626eb78f193a2ca7e449d85f4f110cac24e`.

**Consequence.** Bundle bytes, receipt/review/source bindings and proof/status recomputation passed the independent auditor. This validates artifact integrity and replay consistency only; it does not change the native `UNKNOWN` into a positive safety result.

**Status:** `PASS_READ_ONLY_PROOF_REPLAY`; one call attempt; 800 study rows not run.

**Required action:** Preserve the bundle and its raw hashes unchanged for Codex review.

## Finding 4 - Study isolation, scientific scope and repository state

**Finding.** The preflight result stayed outside the fixed 800-row study and did not alter its manifest or denominators.

**Evidence.** Post-run read-only manifest inspection found 800 records, all with `status: NOT_RUN` and null result records; `task_rows_not_run: 800`, `query_status: NOT_RUN`, and `evaluated: false`. Its raw SHA-256 remains `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b`, identical to the pre-call binding. The published summary states `manifest_status_changed: false`, `study_denominators_touched: false`, `study_row_attempt_count: 0`, and `study_result: false`; the auditor also reports `study_denominators_touched: false` and `study_rows_not_run: 800`.

The repository remained on `main` at HEAD `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`. Only the authorized runtime receipt, runner-generated attempt/checkpoint/bundle, and this designated handoff were written by this task. Existing shared dirty files and G4/Auer artifacts were not edited. No commit or push was made.

**Consequence.** The preflight does not supply the missing decision-relevant voltage-selection evidence, useful operating domain, or general G2 enclosure evidence. G2, G3, G4 and physical-platform correspondence remain `UNVERIFIED`; overall research disposition remains `HOLD`.

**Status:** Study isolation confirmed; **800/800 `NOT_RUN`**.

**Required action:** Codex may review the receipt and audit bundle. Any further query requires a separate authorization and a fresh reviewed one-shot path; this consumed authorization does not permit another call or an 800-row batch.
