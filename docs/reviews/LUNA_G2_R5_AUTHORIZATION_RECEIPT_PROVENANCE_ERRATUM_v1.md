Session: DDWMR | LUNA-G2-SCOPE

# Append-only provenance erratum: G2 R5 one-query authorization receipt

**Erratum version:** v1, 2026-10-03  
**Purpose:** Preserve the R5 receipt/provenance discrepancy without altering the consumed receipt, bundle, or earlier R5 handoff. This file supplements the R5 handoff; it does not replace or repair the receipt. Future corrections must be appended in a new dated/versioned erratum.

## Finding - the receipt does not contain the quoted user text

**Finding.** The R5 handoff quotes an explicit one-call instruction and reports the hash of that quotation, but the active write-once receipt contains an ASCII-damaged version. The string and hash inside the receipt are self-consistent with each other; they are not the string/hash of the handoff quotation.

**Evidence.** The R5 handoff quote is recorded here exactly as it appears in that handoff and in the user instruction visible in this conversation:

> 2. Nếu bạn muốn cho chạy preflight: Tôi cho phép `LUNA-G2-SCOPE` gọi native `run_query` **đúng một lần** cho `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1`, theo assignment G2 R5 one-query preflight. Không chạy query khác hoặc batch 800 hàng.

UTF-8 SHA-256 of this quotation: `13e209f5a3f0de042998618b4703b9fc379b40a3b6ab8f5041dddbae20ade1b6`.

The active receipt `research/benchmarks/G2_DECISION_DOMAIN_R5_ONE_QUERY_FREEZE_AUTHORIZATION_RECEIPT_v1.json` has raw SHA-256 `5672096c8c3c636dd51bef77f109bc7496cb410dfb82b49a00aa776ae51d62d0`. Its `user_authorization.exact_instruction` is ASCII-only and reads:

```text
2. N?u b?n mu?n cho ch?y preflight: T?i cho ph?p `LUNA-G2-SCOPE` g?i native `run_query` **??ng m?t l?n** cho `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1`, theo assignment G2 R5 one-query preflight. Kh?ng ch?y query kh?c ho?c batch 800 h?ng.
```

SHA-256 of the UTF-8 encoding of that damaged string, as recorded in the receipt, is `4e5e84ad4357445ad9fb622fa2ae0301bde88e43d18d8a2de86772a4b1871a2f`. The damaged value contains zero non-ASCII code points. Recomputed quote and receipt hashes differ. Codex's result review `docs/reviews/CODEX_G2_DECISION_DOMAIN_R5_ONE_QUERY_RESULT_REVIEW.md` independently records this mismatch and rejects the receipt as a verbatim transcript.

The user message is visible in the active conversation and contains the quoted one-query permission. The repository artifacts alone do not authenticate the original conversation event, sender identity, or exact original message bytes. The hash `13e209f5a3f0de042998618b4703b9fc379b40a3b6ab8f5041dddbae20ade1b6` is the hash of the handoff/conversation quotation available here; it is not proof of an authenticated event signature.

## Finding - encoding-loss mechanism reproduced without evaluator use

**Finding.** The observed loss is consistent with PowerShell 5.1 converting the Unicode Python source sent through a native stdin pipeline using its default US-ASCII `$OutputEncoding`; the non-ASCII characters become `?` before Python parses the script. JSON serialization then faithfully writes the already-damaged Python string.

**Evidence.** The earlier receipt-creation command used a PowerShell single-quoted here-string piped to `python -`. A read-only, non-query reproduction in the same environment reported PowerShell `5.1.26100.9444` and `$OutputEncoding=US-ASCII`: a Python source literal containing Vietnamese characters arrived with ASCII `?` and `literal_non_ascii_count: 0`. In the same test, ASCII-only Python source containing `\uXXXX` escapes was parsed by Python into the intended Unicode characters (`escaped_non_ascii_count: 13`); its short sample string hashed to `811aa55895fc3f5c6bcf7bbf31ac6be6ed98d0da65e8e0670372b87ef09402e4`. No evaluator, `run_query`, receipt write, or bundle write was part of this reproduction. The original tool invocation's source text included Vietnamese characters and used the same here-string-to-Python-pipe pattern. The exact historical `$OutputEncoding` value at the moment of receipt creation was not separately logged, so the receipt alone cannot prove the byte-by-byte path; the reproduced shell boundary is the identified cause and matches the observed damage.

**Safe method for a future, separately authorized receipt.** Construct the instruction from ASCII-only Python source using explicit `\uXXXX` escapes (or read verified UTF-8 bytes from a separately prepared source), compute `sha256(exact_instruction.encode("utf-8"))`, and assert it equals an independently calculated expected hash before writing. Serialize with `json.dumps(..., ensure_ascii=False)` and explicitly encode the complete document as UTF-8. Create the new runtime receipt with exclusive-create semantics (`open(..., "xb")`); then read it back, assert the decoded field equals the exact intended string byte-for-byte as Unicode, and recompute both instruction and receipt raw hashes before any runner preflight. In Windows PowerShell 5.1, do not pipe Unicode source literals to a native command with the default US-ASCII `$OutputEncoding`; a session-local UTF-8 pipeline is another option but must itself be verified. This method is for a future new receipt and does not authorize or enable retry of R5.

## Finding - consumed R5 evidence remains intact

**Finding.** The authorization-text mismatch does not erase the R5 call's diagnostic data, and it does not justify repairing the consumed receipt or retrying the query.

**Evidence.** The exact R5 query was `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1`. One attempt marker exists with SHA-256 `74c53f36686bbb67ce2420c2b9975b2029ebeb93b6b39db394f35ba2a090b31d`; its durable native-call checkpoint has SHA-256 `2b36fee53b1da17810c36ca311dc0626eb78f193a2ca7e449d85f4f110cac24e`. The published bundle `results/validation/g2/decision_domain_r5_one_query_v1` has `COMMIT.json` SHA-256 `2b6f6b1bab90a072998e94ae2f5df2d871bd925715540471a838a01bb0cb8756`; its safety record hash is `aa12f85b94b41d2f267be985ae93e8fc3abe73c97936add4504f7072bd072c23`, and its endpoint record hash is `b81b408e7d446dc3af1eb69b757418a872d425d985cd076caeb2adf1d5cb58d6`. Codex's R5 result review is `6a2610425b43a75c269b0742f0ab6fc0bf4ffe6cc9a4b31ad5786d2a8611fa54`; the prior R5 handoff is `9c46dcdbbb4b4ef23dea183b82d4677c7ca64731ca7b7eef4a33a4f13954c37a`. That review retained one call and its replayable `UNKNOWN` bundle and rejected retry/repair. The native record's negative collision/contact sufficient bounds and negative endpoint-progress lower bound are inconclusive certificates, not proof of actual unsafety.

**Consequence.** The raw receipt, attempt marker, checkpoint, bundle and prior handoff remain the evidence of what the runner consumed and produced. This erratum is additional provenance context only. It must never be substituted for the missing verbatim value in the receipt or described as an authenticated replacement.

**Status:** `ERRATUM_RECORDED`; R5 call cap consumed; receipt provenance rejected; R5 query remains `UNKNOWN`; study remains **800/800 `NOT_RUN`**.

**Required action:** Preserve all R5 runtime artifacts unchanged. Any future execution requires a new query/stage candidate, separately reviewed source closure, a fresh receipt with verified UTF-8 round-trip, and explicit authorization for the exact new scope. Do not retry the R5 ID or run the 800-row study.
