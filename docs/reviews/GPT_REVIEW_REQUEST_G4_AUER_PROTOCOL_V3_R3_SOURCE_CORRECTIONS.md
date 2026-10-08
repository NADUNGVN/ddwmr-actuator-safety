# Independent review request — G4 Auer protocol v3 R3 source corrections

**Review package:** `G4_AUER_MATCHED_PROTOCOL_V3_R3_SOURCE_CORRECTIONS`  
**Candidate manifest:** `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v4.json`  
**Protocol:** `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R3.md`  
**Source closure SHA-256:** `4e19ddf5f4fdfa28bc47bcd12baf96f82ee1682021f74b28dc375a9098400bf8`

Please read the prior review `docs/reviews/CODEX_G4_AUER_PROTOCOL_V3_R2_SOURCE_REVIEW.md` and the correction handoff `docs/CODEX_TO_LUNA_G4_AUER_PROTOCOL_V3_R2_SOURCE_CORRECTIONS.md`, then independently assess this concrete R3 candidate.

Review these items:

1. Whether the 53-file source closure and 18-module/47-edge AST import inventory include all proof-relevant local imports, especially `validation/g2/polynomial.py`, and whether the copied-package hash/import report supports the stated source identity.
2. Whether digest-bound stage checkpoints and the guard preserve established native status/raw status, proof bytes, native replay, and common status across outer timeout/memory stops; assess partial/uncheckpointed artifacts and unavailable fallback input bindings.
3. Whether proof-size exhaustion and process-memory exhaustion are classified as `RESOURCE_LIMIT` while retaining producer status/work, and whether malformed input remains separate.
4. Whether worker and parent timing boundaries are non-self-referential and consistent with the equal-resource comparison contract.
5. Whether the result validator checks the schema, frozen query/source/profile/proof/common identities, and the `CERTIFIED` / proof-complete-common-UNKNOWN implications; identify any mutation or corruption path it accepts incorrectly.
6. What the fresh 64-MiB Job Object probes establish and what remains unmeasured for the 120-second/1-GiB query pipeline.
7. Whether the separate fresh-probe index is an adequate binding for the preserved execution profile, whose embedded probe file links still point to earlier closure-bound records, or whether a separately versioned profile rebinding is needed before freeze.

Also inspect `results/validation/g4/auer2013/protocol_v3_r3_source_corrections_probes/probe_refresh_index.json`, which records the fresh probe binding and identifies the preserved profile?s earlier evidence links. The probe and control-flow reports are non-query evidence. Synthetic control-flow artifacts are not mathematical proof evidence. No matched query ran: all 1,944 candidate rows remain `NOT_RUN`, `comparison_run=false`, `query_1_authorized=false`, and the batch is 0/1,944. R3 v5/R4/R5 evidence is retained. The v10/v11 complete snapshot trees remain unavailable for external member-by-member audit.

Return a **downloadable Markdown file** with sections **Finding / Evidence / Consequence / Status / Required action**. Give an independent source/proof/resource disposition and explicit limitations. Do not infer G4 novelty, promote a research gate, declare the candidate finally frozen, or authorize query 1/the batch.