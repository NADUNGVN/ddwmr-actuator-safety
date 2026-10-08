# Assignment — DDWMR | LUNA-G4-AUER — R16 R3 provenance correction

Read `AGENTS.md`, all four canonical `research_context` files, the R15 execution handoff, and `docs/reviews/CODEX_G4_AUER_R15_STAGE_01_RESULT_REVIEW.md` first. This is a **prospective source/protocol correction**, not authority to execute another stage.

1. Preserve R9/R11/R12/R13/R14/R15 source, GO receipt, stopped stage, and external captures byte-for-byte. The first two R15 IDs have been attempted; never retry or reclassify them as `NOT_RUN`. Do not run any real query, native worker, composition audit, stage or full batch. Isolated non-query fixtures may use synthetic records. Do not commit or push.
2. Trace the real R9 R3 `proof.json` → native replay → `r3_record_to_common_segment` → common predicate → composition audit → R15 checker path. Explain why the actual R3 common provenance omits `native_proof_file_sha256` and `source_snapshot_manifest_sha256` while the checker requires them. Compare direct and transitive source/proof binding, then specify one sound prospective contract. Do not accept a producer-declared hash without recomputing the referenced raw bytes.
3. Prepare a **new versioned** producer/adapter/checker candidate that applies the selected binding consistently. If enriching R3 common segments, compute the raw native-proof file hash after serialization; bind the correct immutable source snapshot; include both in every segment before common-record serialization; recompute `segments_sha256`; and independently replay the proof, source, common predicate and composition links. Preserve the fixed-label and full-hold semantics. Do not edit historical R9/R15 artifacts to make them pass.
4. Correct the prospective terminal timestamp contract: capture `started_utc` at stage start alongside the monotonic clock, capture `completed_utc` at finish, and have the checker reject impossible ordering. Preserve the R15 timestamp discrepancy as historical evidence. Prepare production-path non-query interface evidence that exercises the actual R3 positive-output adapter and catches absent proof/source fields; synthetic hand-built segment fixtures alone are insufficient.
5. Predeclare any future continuation using only never-attempted IDs, with the fixed 1,944 denominator and R9, R11 and both R15 attempts as separate consumed strata. State how results under different source/protocol versions could be compared before proposing any pooling. Freeze a prospective manifest and source closure for review, but do not create a GO receipt or execute a new stage.
6. Return one Markdown handoff with the source-level root cause, exact schema/proof argument, hashes, consumed-ID ledger, prospective checker behavior, timestamp correction and explicit NO-GO execution status. Keep G4 UNVERIFIED and overall HOLD.

Reply in exactly three short chat lines:

`Session: DDWMR | LUNA-G4-AUER`  
`Status: <DONE or BLOCKED; zero new queries; R15 2/10 consumed>`  
`Handoff: <absolute Markdown path>`
