Session: DDWMR | LUNA-G4-AUER

# G4 Auer R12 contract and continuation handoff

**Date:** 2026-10-04  
**Assignment:** docs/CODEX_TO_LUNA_G4_AUER_R12_CONTRACT_AND_CONTINUATION_RESEARCH.md  
**Reviewed first:** docs/reviews/CODEX_G4_AUER_R11_R2_STAGE_01_RESULT_REVIEW.md  
**Candidate:** R12 continuation R2; source-bound and read-only adjudication complete  
**Query execution:** NO-GO; no query, retry, stage, producer, or auditor was launched  
**Fixed universe:** 1,944 IDs; 1 R9 carry-in and 1 consumed R11 ID; 1,942 continuation IDs remain unattempted

## 1. Executive disposition

Prepared a versioned contract correction, an outcome-sensitive continuation protocol, fixed continuation schedule, source closure, manifest, non-executable authorization template, read-only adjudicator, and builder. The R12 R2 source closure pins 420 exact path/hash/size dependency records, including the entire 376-dependency R11 R2 closure, the preserved Stage 1 output tree, the R9 preflight evidence, the four canonical research-context files, and the R12 candidate sources.

The read-only candidate adjudicator verified the live R9/R11 source locks, checked the preserved Stage 1 receipts and artifacts, and generated a 1,944-row fixed-denominator accounting artifact. It invoked zero method workers, producers, or composition-auditor processes and made no change to the R9 or R11 records.

Original R11 accounting remains unchanged and still says the Stage 1 pair is INCOMPLETE_PAIR, the stage stopped after the first nonvalid pair, and the pair is not comparison eligible. Under the R12 candidate contract, both arms authenticate as class 2 inconclusive outcomes:

- R3 is an authenticated terminal UNKNOWN with common_status NOT_EVALUATED, no common artifact, and an original audit rejection caused by the expected absence of that artifact on this non-evaluated branch.
- Auer has an authenticated terminal proof-complete result, native replay PASS, a stored composition-audit PASS, and a common predicate result of UNKNOWN_ON_SUPPLIED_TUBE. Its common record is bound transitively through the result and audit chain without inventing query/input fields inside the legacy common schema.

R12 would permit continuation after a complete class 1/class 2 pair only under a later exact-scope GO. This candidate and its NO-GO template authorize nothing. R11's consumed ID remains permanently non-retryable, and its immutable Stage 1 receipt is not relabelled as complete.

## 2. Governing findings from the Stage 1 review

I read the R11 result review before preparing the candidate. Its two independent blockers govern this handoff:

1. R11's reader demanded direct query_id and method_input_sha256 members inside result.common.json. The R9 producer does not emit those fields in the common record. Auer's result, terminal receipt, proof, common file, and independent audit report do bind; the consumer imposed a field that is absent from the actual frozen schema.
2. R11 stops at any UNKNOWN/nonvalid pair. That stopped after one of the eleven Stage 1 IDs and left 1,942 IDs unattempted. A continuation that treats every authenticated UNKNOWN as a batch stop cannot estimate certification yield over the prespecified continuation cells.

The review accepted the R11 execution stop and fixed-denominator accounting, but blocked R11 continuation and scientific comparison. It required a versioned read-only consumer correction, preservation of all source records, and a continuation rule designed after the observed first R11 result.

## 3. R12 candidate artifacts

All paths are project-relative to D:/Research/Teacher_Vien/projects/ddwmr-actuator-safety unless marked absolute.

| Artifact | Path | SHA-256 |
|---|---|---|
| R12 R2 protocol | research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R12_CONTINUATION_R2_CANDIDATE.md | 3f3b05e3dd92949741d0eb453826fb16581cdbe5c3a3a79ecd1e1ad07abda140 |
| R12 R2 schedule | research/benchmarks/G4_AUER_R12_CONTINUATION_R2_SCHEDULE.json | 24c65838b62ea6c12d1377f00dd543752ad9090131881a4441b6ce56232cc8ca |
| R12 R2 source closure | research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R12_CONTINUATION_R2.json | dcea79c74218145ae9d87ef429b7c3ab9b1299d2ba73dbe5c14fe72b6dbb01a9 |
| R12 source-closure sidecar | research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R12_CONTINUATION_R2.json.sha256 | daef55f957efb439c739f6a48ad97fc90efcb0abaa20f35c4aef76fb7383f6d1 |
| R12 R2 manifest | research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v12_CONTINUATION_R2.json | 1cd84aa55de7d9f85b66ae18e53c121f1a2a46ff23d4d1add45d7b40c84e9104 |
| R12 manifest sidecar | research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v12_CONTINUATION_R2.json.sha256 | 3d14282f36ead18214a27f83a0391faafd812dc61d325b201be1ea89761afc76 |
| R12 R2 authorization template | research/benchmarks/G4_AUER_R12_R2_STAGE_AUTHORIZATION_NO_GO_TEMPLATE.json | 1ca3f0e27a70a16ca53c4d85c34e2e8d6e63b940e6699f7d05738e85be603472 |
| Read-only adjudicator | validation/g4/summarize_matched_batch_v3_r12_r2_candidate.py | da2a294eeadefa8d67eb7fcb46239b6c9394e7d05e3a91ebc45766975b32303c |
| Candidate builder | validation/scripts/build_g4_auer_v3_r12_r2_candidate.py | 458ece448c485b224127d2ab2d88882a80333bdb34d27bb84dc8f69a320a7493 |
| Final read-only adjudication | results/validation/g4/auer2013/protocol_v3_r12_continuation_candidate_r2/observed_pair_read_only_adjudication_v3.json | f1fff1db7cfcfff59a60045ad4d32f5a3bd6d77b19b169d5eb1d321927c01c3e |

Manifest and source-closure sidecars passed exact-byte verification during the final R2 adjudication. The source closure contains 420 dependency records with exact path, SHA-256 and byte size. The prior R11 R2 closure contributes all 376 source records; R12 adds the candidate sources and exact preserved evidence inputs.

The authorization template states REVIEW_REQUIRED_NO_GO_TEMPLATE_NOT_EXECUTABLE, batch_start_authorized=false, query_workers_authorized=false, effect NONE, and candidate_manifest_sha256=null. It proposes only a future scope binding for r12_continuation_01 (10 IDs), R3 then Auer, one invocation per method/ID, with no retry or substitution. It is not a receipt and cannot start work.

## 4. Old/new source contract and exact source hashes

The R11 sources and records remain unchanged. R12 adds a separate read-only consumer. These are the exact code hashes used for source review:

| Role | Exact path | SHA-256 |
|---|---|---|
| Old R11 Stage 1 reader/runner | validation/g4/batch_stage_runner_v3_r11_r2.py | e5e08a84ddb9eb9a2d65d5a60d0dc14cfd179e843e7418b5ea85e924c0e04294 |
| Old R11 summary consumer | validation/g4/summarize_matched_batch_v3_r11_r2.py | a700ffdfc3e9a63bc3ebecae90f017082fd321df2a26851873817ad87fba256b |
| Frozen R9 common-record producer | validation/g4/common_tube.py | 564c0ffe608be6d0413def643a5dff7b455613c61b56f0ea42684cc7c6874d25 |
| Frozen R9 Auer worker | validation/g4/auer_matched_query_worker_v3_r9.py | 60b71504c044309fd83a54cfb7c81c75e265ceaa7acd4414beef820006706e24 |
| Frozen R9 independent composition verifier | validation/g4/verify_matched_composition_v3_r9.py | 336ef1504353e6b82287be43888fe612b1ecff18fefd179f038fbaa8a23bbdc9 |
| Frozen R9 audit guard | validation/g4/run_matched_composition_audit_guard_v3_r9.py | 3607343bfc5568cc249542673306a919556c05274399a6a24b070a291da5210d |
| Frozen R9 result validator | validation/g4/validate_matched_result_v3_r9.py | 021bdae6b3a103ce6b68954c40797dff7e8270540e08b00e0052f02817de5614 |
| New R12 R2 read-only adjudicator | validation/g4/summarize_matched_batch_v3_r12_r2_candidate.py | da2a294eeadefa8d67eb7fcb46239b6c9394e7d05e3a91ebc45766975b32303c |

The R11 faulty direct-field predicate was not edited in place. R12's verifier binds the actual legacy record using the frozen method-input index, query-bound result, original intent and terminal, exact result/common/proof artifact bytes and sizes, plus the independent audit report and receipt. It retains fail-closed rejection for missing or changed favorable evidence.

## 5. Read-only re-adjudication of the preserved R11 pair

### Original R11 classification

The preserved Stage 1 record remains:

- stage status STOPPED_AFTER_FIRST_NONVALID_PAIR;
- one attempted ID, zero complete valid pairs, one incomplete/nonvalid pair, ten scheduled Stage 1 IDs remaining;
- no retries, no ID substitutions, no unresolved query ID, and stage_exception=null;
- R11 derived summary row status AUDIT_REJECTED, pair status INCOMPLETE_PAIR, comparison_eligible=false;
- R11 summary verifies the R3 invocation and reports Auer invocation as indeterminate because it rejects the Auer common record on the extra direct-field requirement.

These are the exact original status and accounting bytes. R12 does not replace them.

### R12 candidate classification

| Method | Authenticated stored outcome | Native/common and audit evidence | Candidate class |
|---|---|---|---|
| R3 | Terminal final_status UNKNOWN; guard and artifact validation PASS; native status UNKNOWN; no common predicate evaluation | Native proof file hash matches result.native_proof_sha256. No common file/hash is emitted. Historical audit says ARTIFACT_REJECTED with exact diagnostic common_record_path is missing; its zero producer/IVP and zero matched/batch-evaluation counts are retained. | CLASS_2_AUTHENTICATED_INCONCLUSIVE |
| Auer | Terminal final_status PROOF_COMPLETE_COMMON_UNKNOWN; guard/artifact validation PASS; result says method input and scheduled query | Native replay PASS. Stored independent composition report and audit receipt PASS and bind the query, method input, delivered result SHA, proof input, common-record SHA/size and segment digest. The common predicate remains UNKNOWN_ON_SUPPLIED_TUBE. | CLASS_2_AUTHENTICATED_INCONCLUSIVE |

Candidate pair classification: CLASS_2_AUTHENTICATED_INCONCLUSIVE_PAIR. A later protocol may continue to the next unattempted ID after both arms are terminally classified under class 1 or 2, but this is not an execution authorization. The R11 ID remains consumed and no retry is permitted.

### Exact transitive binding for the legacy Auer common record

The R9 common schema is ddwmr-g4-common-tube-check-v1. Its JSON has neither query_id nor method_input_sha256. That is the producer's actual schema, not a defect in the preserved bytes.

The accepted candidate binding is:

1. R9's frozen candidate and active pins derive the exact Auer input SHA for the scheduled ID.
2. Auer invocation intent binds the stage, ID, method, method-input SHA, R11 manifest/closure, exact command, and GO receipt hash. The terminal receipt binds the immutable intent bytes.
3. Auer result.json itself directly binds the scheduled query ID and Auer method-input SHA. The terminal artifact map binds result path, byte size, and SHA-256.
4. result.json binds result.common.json by its canonical absolute path and common_record_sha256. The terminal artifact map independently binds the common file's exact path, byte size and SHA-256. The current common file is 16,627 bytes with SHA-256 23b9c80c49f26a5021d3c78589d8ba8cc3834aad99f016dbb672e0d614ee2659.
5. Each common segment carries provenance native_proof_file_sha256 equal to the exact native proof file SHA and the R9 source snapshot closure SHA. The common record's semantic segment digest is checked.
6. The audit intent binds exact result and worker-guard bytes. The audit terminal binds that intent and stage authorization. The independently produced PASS report names the scheduled query and Auer input, proof input, exact result hash/final status, exact common hash/size, and semantic segment hash/count. The pinned R9 composition verifier independently reconstructs the common record from the proof-derived segments.

Thus query and input identity flow through the exact result and audit report, while the common record's own schema stays unchanged. For Auer the audit establishes proof-to-common composition, not a passing common predicate. UNKNOWN_ON_SUPPLIED_TUBE remains class 2.

For R3, result.json directly binds query/input and its proof hash. Its common status is NOT_EVALUATED, result common hash/path are absent, and the common file is absent. The historical audit rejection is retained as an audit rejection count; R12 recognizes this one exact, source-verified nonpositive branch as AUDIT_NOT_APPLICABLE_NO_COMMON_UNKNOWN for continuation classification. No common record is synthesized and the result is not converted to unsafe.

## 6. Negative mutation matrix for R12 bindings

The matrix below specifies the candidate's required fail-closed response. No mutation was applied to the preserved files; the live R2 adjudication verified the unmodified chain.

| Hypothetical mutation | Binding that must reject it | Expected disposition |
|---|---|---|
| Change scheduled query ID in an invocation intent or result | Frozen ordered-ID/input map; exact intent-to-terminal binding; result query_id check | Class 3, halt before another ID |
| Change result.method_input_sha256 while leaving the frozen query unchanged | R9 input index, exact intent input hash, terminal raw/status reconciliation, direct result binding | Class 3 |
| Change native proof bytes but leave result hash unchanged | Exact proof file SHA versus native_proof_sha256; terminal path/size/hash map; common segment proof provenance | Class 3 |
| Change result.common_record_sha256 or result common path | Terminal result bytes; canonical path check; common artifact hash and size; audit report cross-binding | Class 3 |
| Change common-record bytes, size, or path | Receipt artifact map; raw common SHA; schema/segment digest; report common hash/size | Class 3 |
| Change common segment payload but preserve raw result hash fields | Semantic segments_sha256 and exact audit report segment digest/count; proof provenance | Class 3 |
| Change audit intent's result or guard input hash | Write-once audit intent and audit terminal byte binding | Class 3; no audit retry |
| Change audit report query/method/input/proof-input fields | Expected method input and scheduled ID; audit receipt/report identity checks | Class 3 |
| Change report's delivered result SHA, common SHA/size, or segment digest | Exact result/common bytes and R9 report-to-artifact comparisons | Class 3 |
| Change audit authorization, intent SHA, or terminal status | Canonical GO receipt hash; intent-terminal binding; terminal raw status and receipt artifact checks | Class 3 |
| Remove common record while result says CERTIFIED or common PASS/evaluated | Positive-artifact requirement; no-common exception is limited to verified NOT_EVALUATED UNKNOWN | Class 3 |
| Remove common record on the exact R3 UNKNOWN/NOT_EVALUATED branch and alter the stored diagnostic | R3 branch preconditions and exact expected legacy audit diagnostic | Class 3; only the preserved specific no-common diagnostic is recognized |
| Leave an intent unresolved or add a second attempt record | One-shot attempt number, terminal binding, unexpected-attempt scan, fixed stage/ID scope | Class 3; permanently consumed, no retry |

## 7. Continuation universe and schedule

The R9 ordered universe remains 1,944 IDs with digest 048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac. R10's frozen flattened eligible order contained 1,943 IDs and digest 212b6a09526379188acad46aa05070626b5248a76bc64047d18dd47f9c136e9c for the schedule file. The R9 preflight ID is not in that eligible list; it remains a separate carry-in. R11's first Stage 1 ID was first in the flattened eligible order and is removed exactly once. This leaves 1,942 IDs, in their original relative order, with no substitution.

| R12 candidate stage | Prior source stage | Count | Ordered-ID SHA-256 |
|---|---|---:|---|
| r12_continuation_01 | R10 stage_01 minus the consumed first ID | 10 | 58a888845732cc8f5220656444d0b6ae9aa19a96eed1c014a7f907e9fac55bbd |
| r12_continuation_02 | R10 stage_02 | 36 | 7535c6047cecc7a9215d3b54f0786e91c5fbd7848661cef32fced9155d1a3043 |
| r12_continuation_03 | R10 stage_03 | 96 | 8b83929fb282983777890eb48844a1e73fdd58a3a6e97ed74f39b827f1b54a8f |
| r12_continuation_04 | R10 stage_04 | 450 | 078bd5fe943bcc585cd983b2bf201d54c05a48012c785a59533f6b9a487584b6 |
| r12_continuation_05 | R10 stage_05 | 450 | b6403373f7702e59f4f92bdecb5d5fa22dac3799621b6dea15dd8368baf6aaa5 |
| r12_continuation_06 | R10 stage_06 | 450 | 717f8a9153bb2dcd793df6f212f4946ae9f8ca26c6f5b058253875313a5497e9 |
| r12_continuation_07 | R10 stage_07 | 450 | 3cf6af5f84fa8223e51baea1c2b7f8d6efbd8091ecd328bfeb10fe5a5d99c42c |
| **Total remaining** |  | **1,942** | **8cdd5717aa8a64c50a07ba569353b1e34fd08a353f60cb39b01c64c4b25aac1d** |

The schedule explicitly records designed_after_observing_r11_stage01=true, prospective_claim=false, retry_or_substitution_authorized=false, and r11_stage01_receipt_relabelled_complete=false. Candidate output namespace:

results/validation/g4/auer2013/protocol_v3_r12_continuation_candidate_r2

It is separate from the R11 namespace. The builder rejects pre-review rebuild if any R12 stage/authorization directory exists. The final R2 output root currently contains only derived read-only summaries; no stage or authorization directory exists.

## 8. Outcome classes, accounting and continuation rule

The protocol defines three distinct outcomes:

- Class 1: verified CERTIFIED plus native proof replay PASS, full-hold common predicate PASS_ON_SUPPLIED_TUBE, and independently replayed composition audit PASS with every path/hash/size and identity binding verified.
- Class 2: an authenticated terminal UNKNOWN or authenticated resource-limited outcome with no positive common certificate. It retains terminal reason, resource usage, method status and audit status. UNKNOWN is inconclusive and is never scored unsafe or as a method failure.
- Class 3: source/authorization/intent/artifact-binding failure, unexplained audit rejection, favorable status missing its artifacts, unresolved intent, or resource/process termination that cannot be authenticated. Stop immediately before another ID; do not retry or repair.

When the first method is class 1 or 2, run the second method for that same ID in frozen R3-then-Auer order. Continue to the next unattempted ID only after both arms have verified terminal classifications and required audits/accounting. Class 3 stops the sequence. Every initiated ID is permanently consumed. All later stages require separate exact-scope GO receipts.

Each final report must keep these denominators separate:

| Quantity | Value at candidate freeze |
|---|---:|
| Fixed universe | 1,944 |
| R9 preflight carry-in stratum | 1 |
| Consumed R11 Stage 1 stratum | 1 |
| R12 continuation schedule | 1,942 |
| R12 continuation attempts | 0 |
| R12 continuation not-run IDs | 1,942 |

Per method, the proposed summary reports verified class-1 certificates; class-1 / all 1,942 planned IDs; class-1 / IDs with verified method invocation and terminal classification; class-2 UNKNOWN; class-2 authenticated resource-limited outcomes; class-3 stop count/reasons; unresolved intents; and NOT_RUN separately. The R9 carry-in and R11 observed ID remain separate historical strata and are not pooled into the prospective R12 continuation yield.

Audit accounting distinguishes PASS, AUDIT_NOT_APPLICABLE_NO_COMMON_UNKNOWN, historical audit rejection, current unexplained rejection, and unresolved audit intent. Resource accounting distinguishes method-worker wall time and peak process memory from setup/launcher time and independent-audit wall/memory. Enforcement and termination evidence are reported; setup memory remains NOT_MEASURED unless measured by a predeclared monitor.

If one method has a verified positive certificate on an ID and the other has only authenticated class 2, the permitted description is one-sided verified certificate outcome on that cell. It does not mean the other method is unsafe, mathematically failed, or generally inferior. Certification yields do not imply independent sampling, method superiority, novelty, or G4 acceptance.

## 9. Preserved evidence and observed resource records

The source closure and final read-only adjudicator verified the R11 authorization, Stage 1 intent/terminal, arm/audit intents and receipts, raw results, guards, proofs, common file where present, diagnostic logs, R11 summary, R9 preflight ledger and R9 preflight evidence. No historical file was edited.

Key preserved R11 identities were rechecked against the earlier handoff:

| Artifact | Exact path | SHA-256 | Recheck |
|---|---|---|---|
| Stage 1 GO receipt | results/validation/g4/auer2013/protocol_v3_r11_batch/authorizations/stage_01.json | f275808e0b0a44c3a7b4c24496385d5178f82b22da837bbf65887df860e35a31 | Match |
| Stage 1 intent | results/validation/g4/auer2013/protocol_v3_r11_batch/stage_01/stage_intent.json | 90c3abf1400326b800f69bc72091f6ba2eea213ea79c039d94bc1145e33c5f50 | Match |
| Stage 1 terminal receipt | results/validation/g4/auer2013/protocol_v3_r11_batch/stage_01/stage_terminal_receipt.json | 67fcf72dcf5eebe32ef093311aa1f8bf5b8b640ab7a079251487d2672f5dde64 | Match |
| R11 derived fixed-denominator summary | results/validation/g4/auer2013/protocol_v3_r11_batch/derived_batch_summary.json | 6e3b073e0abe077536529b61e9278d5f7b257e3b470d4206fe3b61ef32a83f32 | Match |
| Codex Stage 1 GO review | docs/reviews/CODEX_G4_AUER_R11_R2_STAGE_01_REVIEW.md | 7659edc894324b6c138083c07057fa0a4bcee0acca3f19a455e1be335bfa4d6c | Match |
| Codex Stage 1 result review | docs/reviews/CODEX_G4_AUER_R11_R2_STAGE_01_RESULT_REVIEW.md | ebc21f70a79105c7a309881352f1654921a2d73dd5557df06fba49fc8fad229d | Match |

The existing R11 arm and audit measurements remain method-specific and are not a scientific comparison:

| Resource | R3 | Auer |
|---|---:|---:|
| Worker wall seconds in raw terminal | 0.281 | 0.485 |
| Worker peak process-commit bytes in raw terminal | 49,254,400 | 48,967,680 |
| Setup/launcher wall seconds | 1.531 | 1.672 |
| Independent audit wall seconds | 0.250 | 0.469 |
| Independent audit peak process memory bytes | 51,339,264 | 51,257,344 |

Auer's worker receipt and measurements are present and hash-verified; R11 summary's indeterminate invocation field arose from its common-record consumer mismatch. The R12 reader reports the authenticated raw record without rewriting that R11 summary. R3's historical audit rejection remains a separately counted rejection.

## 10. Preparation chronology and candidate revisions

R12 R1 was built as an unreviewed candidate. Its manifest sidecar used the generated .json.sha256 filename, while its first verifier expected a different sidecar path. The read-only adjudicator stopped at that candidate-lock check, before reading Stage 1 pair classifications or writing a summary. No worker, producer, auditor, query, or stage was launched. R1 remains preserved and superseded.

R12 R2 corrected the sidecar binding and was source-locked again. Preliminary R2 summary outputs were generated before the last contract hardening that also checks common-segment native-proof provenance and the audit report's segment digest/count. They remain preserved as interim artifacts. Final read-only adjudication v3 additionally verifies each live source-closure dependency's recorded byte size as well as its exact path and SHA-256. The source closure and manifest were rebuilt after this verifier change; `observed_pair_read_only_adjudication_v3.json` is the final R2 adjudication referenced here.

The final R2 adjudicator passed all 420 live source/artifact dependency path, size, and hash checks through its source-closure lock. It revalidated the inherited R11 R2 lock (376 dependencies, eight active profile pins and 21 R9 preflight artifact records), then read the R11/R9 evidence. It did not run the R9 auditor again. The final summary records zero producers, zero query workers, zero auditors, zero new IDs, zero retries, zero later stages, and zero historical artifact modifications. Candidate classification remains `CLASS_2_AUTHENTICATED_INCONCLUSIVE_PAIR`; fixed denominator remains 1,944, with 1,942 continuation IDs unattempted.

## 11. Remaining review questions

Codex should independently examine:

1. Whether the exact transitive common-record binding and semantic segment/proof provenance checks are sufficient for the legacy R9 schema, especially for all permitted future UNKNOWN/resource outcomes.
2. Whether the single explicit R3 no-common NOT_EVALUATED branch may be class 2 with its historical ARTIFACT_REJECTED audit counted separately, without weakening class-3 rejection for any unexplained or favorable-artifact mismatch.
3. Whether the proposed resource-limited terminal definition proves worker stop and one-shot accounting strongly enough for continuation.
4. Whether preserving old stage group boundaries while removing the consumed ID gives a suitable continuation order after the observed result.
5. Whether the proposed observed-strata and per-method yield denominators answer the scientific question without pooling post-observation outcomes or implying independent cells.
6. Whether any executable R12 worker runner is required before a future exact-stage authorization. This handoff intentionally prepares the contract, schedule, and non-executable template, not a GO receipt.

## 12. Recommendation

**GO:** send the R12 R2 contract, source-bound schedule/manifest/closure, no-GO authorization template, and read-only re-adjudication to independent Codex review.

**NO-GO:** query execution, retry, or stage start remains prohibited until Codex independently accepts the exact R12 candidate and creates a new source-bound GO receipt for one exact stage. The current recommendation grants no execution authority.
