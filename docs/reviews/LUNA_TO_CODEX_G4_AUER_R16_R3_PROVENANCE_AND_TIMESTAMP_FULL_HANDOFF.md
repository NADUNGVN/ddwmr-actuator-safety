Session: DDWMR | LUNA-G4-AUER

# G4 Auer R16 R3 provenance and timestamp candidate — full handoff

**Status:** source/protocol candidate prepared for Codex review; **NO-GO**. No real query, query worker, native producer, composition audit, stage, batch, or GO receipt was run or created. G4 remains **UNVERIFIED** and the overall research disposition remains **HOLD**. No commit or push was made.

## 1. R9 source-level root cause

The failure is a missing direct binding at the R3 producer-to-common-record boundary:

1. `validation/g4/r3_matched_query_worker_v3_r9.py` serializes the native result as `proof.json` and later records its path and raw digest in `result.json` (serialization near line 360; result fields near lines 375–377). But `_run_common` calls `r3_record_to_common_segment(record, query, conversion_budget)` near line 166 with only the in-memory record, query, and budget. The proof path, exact-byte digest, and source identity are not passed to that adapter.
2. `validation/g4/common_tube.py::r3_record_to_common_segment` constructs segment provenance containing the semantic record digest, `native_proof_replay=PASS`, and the full-hold enclosure description (near lines 272–330). It has no raw proof-file hash or source snapshot binding. The common predicate serializes these segments and computes `segments_sha256` over the resulting deficient records (near line 496).
3. The R9 composition verifier later opens and replays the proof, reconstructs the expected segment through the same adapter, and records proof/source evidence in its composition report. This is useful transitive audit evidence, but it neither changes nor directly binds the already stored common segment.
4. R15's `_common_and_proof` checker recomputes the proof-file digest and requires every common segment to contain `native_proof_file_sha256` and `source_snapshot_manifest_sha256` (near lines 635–667 of `validation/g4/check_matched_batch_v3_r15.py`). R3's stored segment lacks those fields, so the second R15 ID stopped at class 3 before Auer was invoked. R15 also compares the legacy field named `source_snapshot_manifest_sha256` against the R9 **source closure** digest, reflecting the old naming conflation.

A semantic JSON digest is not a substitute for a raw file digest: different byte serializations can represent the same record. Likewise, an outer composition report or result-level source field cannot prove which exact proof bytes and immutable source snapshot produced each serialized segment. The required association must be present in the segment and independently recomputed from files.

## 2. R16 direct provenance and replay contract

The new schema is `research/benchmarks/G4_AUER_COMMON_SEGMENT_PROVENANCE_v3_R16_SCHEMA.json`, SHA-256 `2c531d459a5d3c3ffd358254dc76c4d1a4264ef0860bc972209cd6007ca64be7`. Each positive common segment requires:

```json
{
  "native_proof_file_sha256": "<SHA-256 of exact raw proof.json bytes>",
  "source_snapshot_manifest_path": "results/validation/g4/auer2013/source_snapshot_v9/snapshot_manifest.json",
  "source_snapshot_manifest_sha256": "fe3309d5b17c6d2968c826eaf1a0759c3b9fbf848432b72842fff5b4db726d91",
  "source_closure_path": "research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R9.json",
  "source_closure_sha256": "7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533"
}
```

The R16 R3 path serializes the proof first. Its versioned adapter then opens the exact proof bytes, recomputes their SHA-256, strictly parses them, rejects a mismatch with the in-memory record, verifies the immutable R9 snapshot and source closure, independently replays the record, and adds the direct fields before common-record serialization. The common segment list digest is recomputed after provenance is attached. No producer-declared hash is trusted in place of reading and hashing the referenced file.

The Auer candidate records the same separated snapshot-manifest and source-closure identities on each segment. The composition verifier derives the expected provenance from opened proof bytes and verified source files. The independent checker verifies the proof path and raw digest, source files and member hashes, proof replay, equality of stored and proof-derived segments, `segments_sha256`, common-predicate replay, and the result/common/proof/composition report links. Missing or altered direct bindings fail closed. The common predicate and fixed-label/full-hold semantics are unchanged.

## 3. R16 versioned artifacts and exact pins

The prospective protocol is `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R16_PROSPECTIVE_CANDIDATE.md`, SHA-256 `1c371c4e34f3ef75a061f9a30670b3ffb863917349f60c4d4318885021e9dd03`.

| Candidate artifact | SHA-256 |
|---|---|
| Freeze manifest, `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v16_PROSPECTIVE.json` | `14c69e603db726d0cc5967f54c631e2b39721d9d4e7bffeefc8941abcad52426` |
| Source closure, `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R16_PROSPECTIVE.json` | `5599c5cde9292478b7a5155e3c7db728af9df811ef150d917b1f0d432713149c` |
| Continuation schedule, `research/benchmarks/G4_AUER_R16_CONTINUATION_SCHEDULE.json` | `ce454815b3c052632b222a1085de9d79af3ae603f54434ab8af0e922c6b6c48a` |
| Non-query conformance report, `results/validation/g4/auer2013/protocol_v3_r16_candidate/nonquery_conformance_v1.json` | `1a2c0fd0265e4bba8611ef4c148acef398958c7946973e2ed33db125c218e9e8` |

The R16 source closure contains 501 dependencies, preserves the inherited R15 closure dependencies, and pins the R16 protocol, schema, implementation, fixtures, report, schedule sidecar, and inherited R15 source/evidence. The R9 identity is pinned independently as snapshot manifest SHA-256 `fe3309d5b17c6d2968c826eaf1a0759c3b9fbf848432b72842fff5b4db726d91` and source closure SHA-256 `7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533`.

Key source pins included in that closure:

| Source | SHA-256 |
|---|---|
| R16 R3 common adapter | `da4ffc2fcfcd67fb9307e1a2f1d59c0844bbc2b67aeb8b22bd50773734367b10` |
| R16 R3 query-worker candidate | `a6e82483cf8337640e4345eadbafa946d0178dc09f07544dd8725110e9df2a1e` |
| R16 Auer query-worker candidate | `9d1958f46364c994bbb49150f21764d35ad9aa1030b431ce4cf16fcd5b14968b` |
| R16 composition verifier | `9bca6fe5d0aa51facaebc812e9d29de5922e9bf01a8137398ec2c2ae8ae47880` |
| R16 independent R3 common replay/checker | `e9bba0b1182dc9a7f37fb3acbe7df36d65ffd9a4931762c136a0a90a9cce10ac` |
| R16 batch checker | `70d9b74d5ded7843441c539c0aba19c6c94cef03794f41652cd8ec3d5156989d` |
| R16 timestamp contract | `5bae6675acab8b93eb05b6265c61893c045b54c7c986115a7c46c691033356cd` |
| R16 source-only stage runner | `3d7d1ea8ebf4a6ba8cf3a8e8f8b1f12fcb65b588b8f65cdea11d18110a63c462` |
| R16 candidate builder | `2b68681130e2164d75a253fcd70db78053c0f546dfc5af1a3deac7ada7b54f2c` |

The builder was corrected to include the complete 1,940-item `continuation_query_ids` list as well as the descriptive never-attempted list. Its refresh path is limited to the three R16 prospective candidate files and their sidecars, and it refuses a partial, sidecar-mismatched, or non-NO-GO existing candidate. R9–R15 files were not modified. The manifest and closure remain un-authorized and create no stage namespace.

The inherited R15 pins are manifest `e02cde6dfb5c8d07cbac053ebb0db945a4961b4aa1bc383c5dbf5660d707d556`, source closure `0488078d3be68e8ddc3da4478553403023ee1c79e4243ac0306dac8b7765d152`, schedule `b2e833cdb20c1d31fde899373ae4d7f2332bd359cc4888d6ddb917840ae96b92`, and terminal receipt `04335cbd0be227f67ea76b47459265e9cfcf1e16d080e51ad5c517dd98278dcb`. R15's 42-file output inventory hash is listed in Section 5.

## 4. Fixed denominator and consumed-ID ledger

The fixed benchmark denominator remains **1,944**. The R16 schedule separates historical attempts and contains only never-attempted IDs.

| Stratum | ID | Recorded outcome / treatment |
|---|---|---|
| R9 preflight carry-in | `state_low_neg__scene_d020_l-200__T_020__V_m1_m1` | Separate historical stratum; not an R16 attempt; no retry. |
| R11 consumed | `state_low_mid__scene_d020_l+000__T_050__V_m1_0` | Separate historical stratum; not an R16 attempt; no retry. |
| R15 attempt 1 | `state_low_pos__scene_d020_l+200__T_100__V_m1_p1` | R3 `UNKNOWN`; Auer `CERTIFIED`; consumed and immutable. |
| R15 attempt 2 | `state_high_neg__scene_d050_l-200__T_020__V_0_m1` | R3 produced a `CERTIFIED` output but direct provenance failed; class-3 stop before Auer, which was `NOT_INVOKED`; consumed and immutable. |
| R16 never-attempted continuation | Remaining IDs in original continuation order | 1,940 IDs; no R16 attempts. |

The first proposed R16 stage has 10 IDs: the eight R15 `NOT_RUN` IDs followed by the next two never-attempted IDs in original order. The schedule has seven prospective groups with sizes `10, 34, 96, 450, 450, 450, 450`; every group is `PROSPECTIVE_NOT_AUTHORIZED`. This is a new stage identity, not a retry or resume. The fixed accounting is 1 R9 carry-in + 1 R11 consumed + 2 R15 consumed + 1,940 never attempted = 1,944.

The locked first-stage IDs are:

```text
state_high_mid__scene_d050_l+000__T_050__V_0_0
state_high_pos__scene_d050_l+200__T_100__V_0_p1
state_low_neg__scene_d100_l-200__T_020__V_p1_m1
state_low_mid__scene_d100_l+000__T_050__V_p1_0
state_low_pos__scene_d100_l+200__T_100__V_p1_p1
state_high_neg__scene_d200_l-200__T_020__V_m1_m1
state_high_mid__scene_d200_l+000__T_050__V_m1_0
state_high_pos__scene_d200_l+200__T_100__V_m1_p1
state_low_neg__scene_d020_l-200__T_020__V_m1_0
state_low_neg__scene_d020_l-200__T_020__V_m1_p1
```

R9, R11, R15, and any future R16 outcomes remain separate by source/protocol version. Same-ID outcomes may be shown side by side for sensitivity review. Pooling requires explicit equivalence review of source closure, proof/provenance semantics, common predicate, resource policy, query input, and attempt accounting; no pooling is assumed.

## 5. Timestamp correction and preserved R15 evidence

The prospective terminal contract captures `started_utc` and the monotonic start clock at stage start, before writing stage intent. The same UTC start is bound into intent and terminal receipt. At finish, it captures `completed_utc` and calculates elapsed time from the monotonic clock. The checker requires explicit UTC offsets, terminal/intent start equality, `completed_utc >= started_utc`, and finite nonnegative elapsed seconds.

R15's timestamp evidence remains byte-for-byte unchanged: `started_utc` and `completed_utc` are both `2026-10-04T08:07:37.307119+00:00`, while `stage_elapsed_wall_seconds` is `46.671999999991385` (about 46.672 seconds). The R15 terminal remains `STOPPED_AFTER_CLASS3`; it records two attempted IDs, eight `NOT_RUN` IDs, zero retries, and zero substitutions. Its 42-file inventory is pinned at SHA-256 `3cf9d0116a66fd60f7f69f6576dc09c421119f7602b300e78803b62935c24988`. No historical timestamp or R15 receipt was rewritten.

## 6. Non-query evidence and verification

The isolated R16 fixture exercises the actual positive-output R3 adapter path with a synthetic query-shaped input and an archived proof-shaped record. It stubs the native proof replay; it does not invoke a real query worker, producer, native replay, composition auditor, stage, or GO receipt. It checks raw proof and source binding, independent synthetic bundle replay, rejection after removal of each required raw-proof/snapshot/closure field, valid timestamp order, completion-before-start rejection, and intent/terminal start mismatch rejection.

- Fixture: `PASS_ALL_R16_NONQUERY_CONTRACT_FIXTURES`, 8/8; zero real queries, query workers, native producers, composition auditors, stages, and GO receipts.
- Candidate builder: `R16_PROSPECTIVE_CANDIDATE_FROZEN_NO_GO`; 501 dependencies; 1,940 never-attempted IDs; zero real queries, stages, or GO receipts.
- Read-only checker: `PASS_R16_PROSPECTIVE_SOURCE_PREFLIGHT_UNSTARTED`; schedule, manifest, closure, sidecars and all 501 locked dependencies verified; R16 batch output namespace absent; execution disabled.

The read-only command used was `python -B -m validation.g4.check_matched_batch_v3_r16 --verify-only`. No production composition audit or stage was run. Execution remains **NO-GO pending independent Codex review**; G4 remains **UNVERIFIED** and overall HOLD.
