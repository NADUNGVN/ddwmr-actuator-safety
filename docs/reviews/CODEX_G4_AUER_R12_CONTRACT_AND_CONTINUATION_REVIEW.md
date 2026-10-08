# Codex review — G4 Auer R12 continuation candidate

**Date:** 2026-10-04  
**Disposition:** ACCEPT the narrow read-only re-adjudication and the 1,942-ID continuation schedule as candidate evidence. **NO-GO for any R12 query or stage execution.**  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_R12_CONTRACT_AND_CONTINUATION_FULL_HANDOFF.md`.

I read the project operating contract and canonical research context, the R11 result review, the R12 R2 protocol, schedule, manifest, source closure, read-only adjudicator and its stored final output. I inspected the relevant R11 audit and artifact validators. This review did not invoke a method worker, producer, composition auditor, batch runner, or native proof replay.

## 1. Source identity and execution boundary

**Finding.** The R12 R2 candidate is a source-bound preparation artifact, not an executable authorization.

**Evidence.** Independent byte checks matched the protocol (`3f3b05e3dd92949741d0eb453826fb16581cdbe5c3a3a79ecd1e1ad07abda140`), schedule (`24c65838b62ea6c12d1377f00dd543752ad9090131881a4441b6ce56232cc8ca`), source closure (`dcea79c74218145ae9d87ef429b7c3ab9b1299d2ba73dbe5c14fe72b6dbb01a9`), manifest (`1cd84aa55de7d9f85b66ae18e53c121f1a2a46ff23d4d1add45d7b40c84e9104`), adjudicator (`da2a294eeadefa8d67eb7fcb46239b6c9394e7d05e3a91ebc45766975b32303c`), and final read-only output (`f1fff1db7cfcfff59a60045ad4d32f5a3bd6d77b19b169d5eb1d321927c01c3e`). Both sidecars match their target files. All 420 source-closure path, size and SHA-256 records matched the live files. The R12 output root contains only derived read-only adjudication records; there is no stage or GO authorization directory. The R12 authorization file explicitly says `REVIEW_REQUIRED_NO_GO_TEMPLATE_NOT_EXECUTABLE`.

**Consequence.** The stored output can be examined as a candidate analysis. Hash consistency does not itself confer execution authority or independently replay the native proof.

**Status:** VALID local source/artifact consistency; execution **NO-GO**.

**Required action:** Preserve R9 and R11 artifacts byte-for-byte. Do not reuse the R11 GO receipt or treat the R12 no-GO template as authorization.

## 2. Exact continuation universe and order

**Finding.** The R12 schedule removes exactly the consumed R11 first Stage 1 ID from the frozen R10 eligible sequence. It preserves the remaining order and stage partitions.

**Evidence.** The R10 eligible schedule has 1,943 IDs: 11, 36, 96, 450, 450, 450, 450. Its first ID is the one attempted by R11. The R12 list equals the R10 flattened list after removing that first ID, byte-for-byte by ID and relative order. Its seven groups contain 10, 36, 96, 450, 450, 450, 450 IDs, totaling 1,942 unique unattempted IDs. I recomputed every declared ordered-ID SHA-256 and the aggregate digest using the builder's convention, `SHA256("\n".join(ids))` with **no trailing newline**; all eight digests match. The R9 preflight ID remains a separate carry-in and was never in the R10 eligible sequence.

**Consequence.** The fixed 1,944-ID universe can be reported as one R9 preflight carry-in, one consumed R11 Stage 1 ID, and 1,942 R12 scheduled IDs. This is a design made after the two observed strata, and those strata cannot be pooled into a wholly prospective R12 yield.

**Status:** VALID for the frozen candidate schedule.

**Required action:** A prospective runner must verify the exact schedule and predecessor ordering at launch and on replay, including stage digests, rather than trusting only set membership. No consumed ID may be retried or substituted.

## 3. Historical R11 pair: narrow contract correction

**Finding.** The read-only R12 consumer repairs the specific R11/R9 common-record schema mismatch without changing historical bytes. It supports a **narrow candidate classification** of both preserved method outcomes as authenticated inconclusive terminals. It does not convert either into a positive certificate.

**Evidence.** The R9 common JSON has no direct `query_id` or `method_input_sha256` fields. For Auer's present common record, the R12 reader checks its canonical path, exact hash and size; the result's direct query/input binding; the write-once intent and terminal receipt; the native proof hash and segment provenance; and the stored PASS composition report's result, common, proof-input and segment bindings. The inherited R11 audit validator also checks the exact audit intent, terminal artifacts, report/guard status and reviewed R9 source closure. The preserved Auer result says `PROOF_COMPLETE_COMMON_UNKNOWN`, native replay PASS, common predicate `UNKNOWN_ON_SUPPLIED_TUBE`, and composition audit PASS. Thus its common record is transitively bound without inventing fields absent from the R9 schema.

R3's preserved result says `UNKNOWN`, `common_status=NOT_EVALUATED`, with no common record or common hash. Its historical audit remains `ARTIFACT_REJECTED`, with the exact missing-common diagnostic; R12 verifies that diagnostic rather than rewriting the rejection as PASS. The exception is pinned to this preserved nonpositive R11 case by the source closure and exact records. The old R11 summary still says `INCOMPLETE_PAIR` and remains unchanged. The final R12 read-only output says `CLASS_2_AUTHENTICATED_INCONCLUSIVE_PAIR`, zero new query invocations, zero retries and zero positive certificates for this pair.

**Consequence.** The raw Auer invocation is evidenced; the old R11 summary's indeterminate invocation field was caused by its stricter, incompatible consumer. The R11 stop remains valid. An `UNKNOWN` result says nothing about collision or unsafety. The R12 classification is a versioned interpretation of one frozen historical pair, not a completed matched-method yield study.

**Status:** ACCEPT for this exact read-only historical re-adjudication. The stored R9 composition audit was inspected through its bindings, not rerun by this review.

**Required action:** Keep the original R11 summary and historical audit rejection visible next to the candidate R12 interpretation. The missing-common exception must not silently apply to a favorable result, a claimed evaluated common predicate, or a different unexplained audit rejection.

## 4. Prospective classification and execution gap

**Finding.** The proposed three-class continuation policy is scientifically appropriate in outline, but this candidate does **not** implement or validate the future stage execution path.

**Evidence.** The R12 adjudicator is hard-coded to the one preserved R11 pair. Its class-2 code accepts the two stored `UNKNOWN` forms; it does not authenticate prospective wall/memory/resource-limit terminals, no-common audit-not-applicable records, unresolved intents, one-shot interruption states, or positive class-1 outcomes from new R12 directories. The protocol describes these branches, but no R12 stage runner, future receipt writer, general checker or completed negative mutation matrix is supplied. The handoff's mutation matrix is a proposed check plan, not observed mutation results. The current read-only summary verifies that the candidate schedule partitions the universe; its own prospective execution controls do not yet exist.

**Consequence.** Accepting the historical correction cannot justify a GO receipt. In particular, an unauthenticated process limit, a missing favorable artifact or an unresolved write-once intent must stop the sequence as class 3. A future class-2 outcome can permit continuation only after both arms, their applicable audits and their accounting have been checked under an exact source lock.

**Status:** Prospective policy **CONDITIONAL**; runnable matched batch **UNVERIFIED / NO-GO**.

**Required action:** Build a versioned, source-bound prospective R12 runner and independent checker with non-query conformance evidence for class 1, authenticated class 2 (including resource termination), and class 3. Review that exact candidate before any stage GO. Keep each stage's authorization separate; no automatic advancement.

## 5. Scientific disposition

The proposed reporting denominators, separate historical strata, per-method positive yield, inconclusive/resource counts, and separate worker/setup/audit resource measurements are appropriate. They do not establish independent samples, practical superiority, novelty, physical transfer or G4 acceptance. A cell where one arm has a verified positive common certificate and the other has authenticated class 2 would show only a **one-sided verified certificate outcome on that cell**.

**Final decision:** R12 R2 historical contract correction and ordered schedule **ACCEPTED in the scopes above**. R12 query execution **NO-GO**. The R11 batch remains **1/1,944 attempted**; R12 continuation remains **0/1,942 attempted**, with one separate R9 preflight carry-in. The project remains **HOLD; G1 PASS for restricted reduced-model scope; G2/G3/G4 and physical-platform correspondence UNVERIFIED**. No G3, operational controller or hardware work follows from this review.
