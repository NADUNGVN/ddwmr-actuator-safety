Session: DDWMR | LUNA-G2-SCOPE

# G2 R6 Provenance and Next-Query Plan - Full Handoff

**Date:** 2026-10-03  
**Assignment:** `docs/CODEX_TO_LUNA_G2_DECISION_DOMAIN_R6_PROVENANCE_AND_NEXT_QUERY_PLAN.md`  
**R5 result review read first:** `docs/reviews/CODEX_G2_DECISION_DOMAIN_R5_ONE_QUERY_RESULT_REVIEW.md`  
**R5 accepted runner review:** `docs/reviews/CODEX_G2_DECISION_DOMAIN_R5_ONE_QUERY_RUNNER_REVIEW.md`  
**Repository / branch / HEAD:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety` / `main` / `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`

## Disposition

No native query was invoked during this R6 assignment. The R5 receipt and published bundle remain unchanged. I created (1) a separate append-only R5 provenance erratum and (2) a versioned, unrun two-row matched-action protocol candidate. The R5 result remains a replayable `UNKNOWN` diagnostic whose receipt fails the exact-text provenance requirement. The fixed 800-row study remains **800/800 `NOT_RUN`**. No gate status changes.

| New artifact | Raw SHA-256 | State |
|---|---|---|
| `docs/reviews/LUNA_G2_R5_AUTHORIZATION_RECEIPT_PROVENANCE_ERRATUM_v1.md` | `9f2b939785998408a77f7d486606e54d74e84e929d594d35ea091a2fc6532df4` | Append-only v1; does not replace receipt |
| `research/benchmarks/G2_DECISION_DOMAIN_R6_MATCHED_ACTION_STAGE_PROTOCOL_CANDIDATE_v1.md` | `8ea158a2533c963ba66571be182659742dbe40f048f71de18f677f7aae5c6a79` | Draft only; no R6 query executed |

## Finding 1 - R5 quotation, damaged receipt, and limits of provenance

**Finding.** The UTF-8 hash `13e209f5a3f0de042998618b4703b9fc379b40a3b6ab8f5041dddbae20ade1b6` is the hash of the Vietnamese instruction quotation preserved in the R5 handoff and visible in the conversation. The active write-once receipt contains an ASCII-damaged version and its hash `4e5e84ad4357445ad9fb622fa2ae0301bde88e43d18d8a2de86772a4b1871a2f`. The receipt is not a verbatim authorization transcript.

**Evidence.** The quote, distinction between a handoff transcription and an authenticated original event, both hashes, the full ASCII-damaged receipt field, and the R5 result review's disposition are recorded in the separate append-only erratum above. The R5 result review `docs/reviews/CODEX_G2_DECISION_DOMAIN_R5_ONE_QUERY_RESULT_REVIEW.md` has raw SHA-256 `6a2610425b43a75c269b0742f0ab6fc0bf4ffe6cc9a4b31ad5786d2a8611fa54`; it explicitly retains the call/bundle, rejects the receipt as verbatim, and says the original conversation event cannot be independently authenticated from repository files. The R5 full handoff raw SHA-256 is `9c46dcdbbb4b4ef23dea183b82d4677c7ca64731ca7b7eef4a33a4f13954c37a`.

The exact R5 evidence hashes are:

| R5 evidence | Raw SHA-256 |
|---|---|
| Active receipt (left unchanged) | `5672096c8c3c636dd51bef77f109bc7496cb410dfb82b49a00aa776ae51d62d0` |
| One-shot attempt marker | `74c53f36686bbb67ce2420c2b9975b2029ebeb93b6b39db394f35ba2a090b31d` |
| Native-call checkpoint | `2b36fee53b1da17810c36ca311dc0626eb78f193a2ca7e449d85f4f110cac24e` |
| Published bundle `COMMIT.json` | `2b6f6b1bab90a072998e94ae2f5df2d871bd925715540471a838a01bb0cb8756` |
| Bundle safety record | `aa12f85b94b41d2f267be985ae93e8fc3abe73c97936add4504f7072bd072c23` |
| Bundle R2 endpoint record | `b81b408e7d446dc3af1eb69b757418a872d425d985cd076caeb2adf1d5cb58d6` |

The receipt raw hash and those marker/checkpoint/commit/record hashes match the R5 handoff and were re-read in this task. The active conversation displays the user's permission text; the receipt by itself cannot reconstruct the lost diacritics or prove the identity, timing, or original bytes of the conversation event. The quotation hash must not be represented as a signed or otherwise independently authenticated user-event hash.

**Consequence.** The receipt defect is a lossy provenance failure, not a reason to delete or alter execution evidence. The consumed attempt remains consumed. The append-only erratum adds a transparent record and does not repair or supersede the original receipt.

**Status:** R5 quote hash confirmed as a handoff/conversation quotation; receipt string/hash confirmed damaged; original event is not independently authenticated by repository artifacts.

**Required action:** Preserve the original receipt, marker, checkpoint and bundle. Treat the erratum only as an additional provenance note.

## Finding 2 - Encoding-loss cause and safe future serialization

**Finding.** The loss mechanism was reproduced at the PowerShell 5.1 native-stdin boundary. A Unicode literal in a PowerShell here-string piped to `python -` was converted using US-ASCII `$OutputEncoding` before Python parsed the source. JSON serialization then stored the already damaged ASCII string; it did not cause the character loss.

**Evidence.** A non-query reproduction reported PowerShell `5.1.26100.9444` and `$OutputEncoding=US-ASCII`. A Python-source literal containing Vietnamese arrived with `?` in place of each non-ASCII character and `literal_non_ascii_count: 0`. An ASCII-only Python source form with Unicode escapes parsed into the intended Unicode (`escaped_non_ascii_count: 13` for the test sample), whose UTF-8 SHA-256 was `811aa55895fc3f5c6bcf7bbf31ac6be6ed98d0da65e8e0670372b87ef09402e4`. This reproduction wrote no files and called no evaluator. The R5 receipt-generation invocation visible in the tool history used the same literal-here-string-to-Python-pipe pattern. The exact `$OutputEncoding` value was not separately logged at the historical instant, so this is a reproduced and strongly supported boundary cause, not a recoverable byte trace from the receipt alone.

A safe process for a future, new receipt is specified in the erratum and protocol candidate: assemble text from ASCII-only Python source with Unicode escapes or verified UTF-8 bytes; calculate an expected UTF-8 SHA-256; serialize to UTF-8; create the new receipt exclusively; read it back and assert exact decoded text equality and matching hashes before runner preparation. A second in-memory non-query fixture constructed the full quoted instruction from ASCII-only Unicode escapes, serialized/deserialized JSON as UTF-8, and passed exact Unicode and instruction-hash round-trip checks: expected instruction hash `13e209f5a3f0de042998618b4703b9fc379b40a3b6ab8f5041dddbae20ade1b6`, JSON byte hash `3a99b049dc92190e0578275aa3182d3e34f8e8a1b0276d469f4aa78b5c48197b`, zero filesystem writes, zero native calls. Do not pipe unverified Unicode literals through the PowerShell 5.1 US-ASCII native stdin default. No R5 artifact was rewritten and no global encoding setting was changed.

**Consequence.** A receipt's self-hash check only establishes consistency of the value that reached Python. It does not prove that value was the text supplied by the user. A round-trip assertion against the expected exact instruction is required before any future one-shot call.

**Status:** Encoding boundary reproduced without query use; R5 provenance remains rejected.

**Required action:** Use the verified UTF-8 procedure only for a future, separately reviewed receipt. This finding authorizes no query.

## Finding 3 - R5 UNKNOWN and the next G2 question

**Finding.** R5 is an inconclusive sufficient-certificate result. The R3 collision sufficient lower bound and contact sufficient lower bound are both negative; the R2 terminal-progress lower bound is also negative. These negative sufficient bounds do not prove actual collision, contact failure, or actual negative progress for every trajectory; they mean the configured evaluator did not certify the required conditions.

**Evidence.** R5 query `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1` returned `UNKNOWN` with reason codes `COLLISION_SUFFICIENT_MARGIN_NEGATIVE` and `CONTACT_SUFFICIENT_MARGIN_NEGATIVE`. In the exact rational replay diagnostics (bundle `diagnostics.json`, raw SHA-256 `30c4f3dfad68db8a6b2ccbed95204200d77d6330735bc2ada49ad4cd848fe365`), the R3 collision sufficient lower bound displays approximately `-0.486611937573` and the contact sufficient lower bound approximately `-4.04776690104`; the R2 terminal-progress lower bound displays approximately `-0.434444975903`. These decimal values are display approximations of the stored rational values, not new calculations by the candidate evaluator. The durable R3 proof replay and R2 endpoint replay passed integrity/replay checks while retaining `UNKNOWN` and `PROGRESS_BOUND_ONLY_SAFETY_UNKNOWN`, respectively; the endpoint result is not task-eligible. Codex's R5 result review recomputed the bundle payload hashes and reports the same dispositions. No R6 evaluator was called.

The useful next local question is whether the same fixed cell/scene/horizon/parameter image yields materially different sufficient bounds under two predeclared held-voltage actions: nominal zero `(0, 0)` and positive full `(1, 1)`. Read-only R4 row reconstruction confirmed the shared non-action fields equal for source indices 0, 12, and 24; the candidate stage uses only rows 12 and 24. It excludes the R5 row from its denominator because of the receipt-provenance defect. Exact query bindings are:

| Stage order | R5 source index | Query ID | Canonical raw SHA-256 | Native input-payload semantic SHA-256 |
|---:|---:|---|---|---|
| 0 | 12 | `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_L0_R0` | `d5648569b11c576c8cc0ecb07c5096c21b06fe3a5e849358f254770649465471` | `422afd0448a184f4f67262c6338593c871739b41fb677e8ab1d6b566d18b93ac` |
| 1 | 24 | `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lp1_Rp1` | `105a0710185446312933ec8c92922acd1db0f3af0e999d67207ccd70534b4808` | `70301bc5df76aab2dfdb8bef5135592fbf0063af6799b0f0eb119f4873b2cf9a` |

Both rows are currently `NOT_RUN` in the unchanged R5 800-row manifest. Their R5 manifest indices are references for exact row reconstruction only; the proposed R6 stage uses its own order `0,1`, denominator, result namespace, and fixed ledger. The R5 manifest raw SHA-256 remains `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b`.

**Consequence.** If separately reviewed and run later, this two-action pair can answer a local certificate-output/progress-bound question under a matched reduced-model input. Even a `CERTIFIED`/`UNKNOWN` contrast would not demonstrate a useful selector, voltage necessity, task success, physical safety, recursive safety, or G2 PASS.

**Status:** R5 remains `UNKNOWN`; R6 pair is a design candidate only, with two rows `NOT_RUN` and zero R6 native calls.

**Required action:** Do not infer that either candidate voltage will improve a bound. Any later conclusion requires valid replay of both fixed rows and remains local to this comparison.

## Finding 4 - Source closure, one-shot controls, hard limits, and state preservation

**Finding.** The new R6 protocol is concrete enough for independent review but is deliberately not executable or frozen. R5's fixed-index runner cannot run the proposed rows 12 and 24. A separately implemented and sealed R6 source closure is required before any call.

**Evidence.** The R6 protocol candidate `research/benchmarks/G2_DECISION_DOMAIN_R6_MATCHED_ACTION_STAGE_PROTOCOL_CANDIDATE_v1.md` has raw SHA-256 `8ea158a2533c963ba66571be182659742dbe40f048f71de18f677f7aae5c6a79`. It fixes two stage rows, denominator `2`, one invocation per ID, no retries/substitutions, a predeclared two-row attempt ledger, a fresh exact UTF-8 authorization receipt schema, an independent R3/R2 auditor, and a separate R6 result namespace. Its present closure state is `DRAFT_PLAN_ONLY_NOT_SEALED`.

The immutable predecessor source references are R5 config `8e2816468bf682290a91535857f2c3f9ad4ff2ba8be99ec5c77acc0ca19a6e19`, R5 manifest `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b`, and R5 source closure `53a923a0be15bd9be977040b996dc2104a763a061e2bad9ef848241a530a55e9` (74 entries, including nested R4/R3 dependencies). The candidate lists the R5 receipt/reviews, erratum, attempt/checkpoint, result records, and the required future R6 config/manifest/adapter/runner/supervisor/auditor/CLI/fixture files. New R6 source bytes and their hashes do not yet exist; they are expressly unpinned. The accepted R5 source closure cannot stand in for closure of a changed-index R6 runner.

The hard-bound proposal uses a Windows supervisor/Job Object, 30 seconds per query, 75 seconds per stage, 20 CPU seconds per query, 1 GiB memory per query, one active process with no breakaway, 8 MiB stdout/stderr caps, and a 16-file / 64 MiB total / 32 MiB per-member staged-output cap. Timeout consumes the row attempt and aborts the rest of the stage without shrinking denominator 2. Non-query fixtures must prove timeout/process-tree termination and all output caps before source review. These limits have not been implemented or tested; the R5 cooperative 15-second check is not a hard bound.

Read-only comparison confirmed receipt, attempt marker, checkpoint and R5 `COMMIT.json` still hash to `5672096c8c3c636dd51bef77f109bc7496cb410dfb82b49a00aa776ae51d62d0`, `74c53f36686bbb67ce2420c2b9975b2029ebeb93b6b39db394f35ba2a090b31d`, `2b36fee53b1da17810c36ca311dc0626eb78f193a2ca7e449d85f4f110cac24e`, and `2b6f6b1bab90a072998e94ae2f5df2d871bd925715540471a838a01bb0cb8756`, respectively. Repository remained on `main` at HEAD `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`. This task wrote only the two new artifacts listed at the top and this handoff; it did not edit R5 artifacts, manifests, source code, or G4/Auer files, and it did not switch branches, commit, or push.

**Consequence.** The next stage remains blocked on implementation, a complete exact R6 closure, non-query resource/provenance fixtures, Codex review, and a fresh user authorization for exactly the two IDs. No current permission or R5 receipt can authorize that stage.

**Status:** R6 protocol drafted, not frozen, not authorized, not run. No new query. Study **800/800 `NOT_RUN`**. G2, G3, G4, and physical-platform correspondence remain `UNVERIFIED`; overall disposition remains `HOLD`.

**Required action:** Codex reviews the append-only erratum and R6 candidate, then issues a new implementation assignment if the protocol is accepted. Do not run either row until the new sources and hard-bound fixtures are reviewed and a separate exact-scope user receipt passes UTF-8 round-trip validation.
