# Codex review — G4 Auer R16 provenance and timestamp candidate

**Date:** 2026-10-04  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_R16_R3_PROVENANCE_AND_TIMESTAMP_FULL_HANDOFF.md`  
**Disposition:** accept the source-locked, non-executed preparation; **NEEDS REVISION before any exact-stage GO**.

I read `AGENTS.md`, the four canonical `research_context` files, the handoff, R16 protocol/manifest/closure/schedule, the R3 and Auer adapter paths, checker, composition verifier, timestamp helper and stored fixture report. I independently checked all 501 R16 dependency path/size/SHA-256 records and all 467 inherited R15 dependency tuples. I checked that the 1,940 continuation IDs are exactly the R12 continuation order after removing the two consumed R15 IDs, with a ten-ID first-stage prefix and no R16 batch directory. I did not invoke a query, producer, auditor, stage, fixture suite or checker.

## Finding 1 — prospective identity and consumed-ID accounting

**Evidence.** The R16 manifest, closure, schedule and non-query report raw hashes match the handoff. The R9 snapshot manifest is 718 members with raw SHA-256 `fe3309d5b17c6d2968c826eaf1a0759c3b9fbf848432b72842fff5b4db726d91`; the distinct R9 source closure hash is `7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533`. The fixed denominator is 1,944: one R9 preflight, one R11 consumed ID, two R15 attempted IDs and 1,940 never attempted. The new ten-ID prefix starts with the eight R15 `NOT_RUN` IDs and then two further unattempted IDs. All proposed groups are marked prospective.

**Consequence.** R16 does not retry, resume or silently pool R15. Its locked schedule is a valid candidate for later source review. The stored eight-case fixture report claims 8/8 expected outcomes but stubs native proof replay and does not include a live Auer positive-output path.

**Status:** **VALID** accounting and source-file identity; execution remains **NO-GO**.

**Required action.** Preserve all R9–R16 source and results. Keep the historical four attempted IDs in separate strata and retain the fixed 1,944 denominator.

## Finding 2 — Auer does not satisfy the declared five-field segment schema

**Evidence.** `G4_AUER_COMMON_SEGMENT_PROVENANCE_v3_R16_SCHEMA.json` requires `native_proof_file_sha256`, `source_snapshot_manifest_path`, `source_snapshot_manifest_sha256`, `source_closure_path` and `source_closure_sha256` on every positive segment. The R16 R3 adapter emits these fields. In contrast, `auer_matched_query_worker_v3_r16.py::_make_segments` and `verify_matched_composition_v3_r16.py::_segments_from_auer` emit the proof hash and both source hashes but omit **both source path fields**. The composition verifier checks only the first segment's proof/snapshot/closure hashes, not the required paths. The stored non-query fixture exercises R3, not the Auer positive-output adapter. No stage checker applies the JSON schema to a live Auer segment.

**Consequence.** A positive Auer common record could pass the current R16 producer/composition path while violating the R16 protocol's explicit per-segment schema. The source mismatch is deterministic and is independent of the R15 historical stop.

**Status:** **BLOCKER** for R16 as a matched production contract.

**Required action.** Make the Auer producer and independent proof-derived reconstruction emit and verify the same five exact path/hash fields as the R3 path. Validate the declared schema in both positive branches and reject deletion or alteration of either path, not only the hash fields. Include an Auer positive-output non-query replay case before a new GO review.

## Finding 3 — actual R16 execution source is not directly bound in result metadata

**Evidence.** The R16 R3 worker imports and executes `r3_common_adapter_v3_r16.py`, yet its `common_adapter_source_sha256` result field is still set to the hash of `validation/g4/common_tube.py`. The Auer R16 worker uses the same legacy field. `validate_matched_result_v3_r9.py` expects that R9 field, so retaining it permits R9 result validation but does not identify the R16 adapter implementation. The R16 segment's `source_closure_path` and hash name the R9 closure, which does **not** contain the R16 worker, adapter, composition verifier or checker. R16's separate 501-entry closure pins these files at candidate level, but the current source-only runner has no executable stage/receipt binding an actual result to that R16 closure. The R3 adapter also expands a full `source_hashes` map into each segment provenance, beyond the declared five-field identity and with avoidable output cost.

**Consequence.** The R9 numeric baseline identity and the actual R16 execution/adapter identity are different facts. The new raw-proof binding is a real improvement, but the complete producer-to-common source claim is not yet direct or unambiguous. Reusing the R9 validation field as though it identified the new adapter would obscure that distinction.

**Status:** **NEEDS REVISION** for source/proof provenance and future cross-version comparison.

**Required action.** Version the result/validator contract or add separately checked fields for the actual R16-or-later worker/adapter and stage source closure. Preserve the R9 native-method baseline identity under an explicitly named field. Bind both identities to every accepted result through an independent checker. Keep segment provenance compact; include only required identities rather than copying the whole R9 dependency map per segment.

## Finding 4 — timestamp correction is a helper, not an executed-stage guarantee

**Evidence.** `batch_timestamp_contract_v3_r16.py` captures UTC and monotonic starts together, and its validator checks UTC ordering, start equality with the stage intent and finite nonnegative elapsed time. `batch_stage_runner_v3_r16.py` exposes only `--verify-only`; it cannot execute a stage or emit a real terminal. The stored timestamp fixtures check the helper contract, while R15's mislabeled start remains preserved.

**Consequence.** The timestamp design is sound as a prospective component, but no production stage has yet demonstrated that it writes and independently replays these fields under stop and partial-intent paths.

**Status:** **VALID component preparation**; stage integration **UNVERIFIED**.

**Required action.** Integrate the helper into a new one-shot stage runner and public read-only stage checker before any execution GO. Test the real producer-to-checker interfaces without new benchmark queries, using isolated copies of archived proof artifacts where useful.

## Gate disposition

**HOLD**. G1 remains PASS for the restricted reduced model. G2/G3/G4 and physical-platform correspondence remain UNVERIFIED. This review grants no R16 stage, query, batch, novelty or G3 authority.
