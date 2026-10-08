# Codex review — G4 Auer R11 R2, Stage 1 only

**Date:** 2026-10-03  
**Decision:** **GO for one exact `stage_01` execution under a separate source-bound authorization receipt.** This accepts the batch integrity controls for a limited validation run. It does not accept a scientific comparison, a novelty claim, G4 PASS, or any later stage.

## Finding 1 — candidate and predecessor identity

**Evidence.** I read `AGENTS.md` and the four canonical `research_context` files, the R11 R2 handoff, protocol, runner, summary, fixture implementation/report, receipt template and the stored R9 preflight records. I independently rehashed the R11 R2 manifest (`193dbead525d1a1c2fae00920a2ff385e7281a6a28aae00e69d72ea7778d106d`) and source closure (`dbe23888fac40caf518009dd96f888e1da45eace388d9ace8cffe906074cbf7b`); 376/376 listed dependency path/hash pairs match the live files. The R11 closure preserves all 359 R10 and 316 R9 predecessor path/hash pairs. The fixed R10 schedule contains eleven Stage 1 IDs after excluding the already observed R9 preflight carry-in; its Stage 1 ordered-ID digest is `80383e5344268b6a7f402579615d9dbe076fd38c30b9a0bd8741951cc359c8f2`.

**Consequence.** The reviewed implementation is the R11 **R2** candidate, not the superseded R11 first build. The R9 preflight is a separate observed stratum, so its seed rule cannot be described as wholly prospective.

**Status:** VALID for exact-byte source and schedule identity.

**Required action:** Preserve these bytes for Stage 1. Any source change voids this review and its receipt.

## Finding 2 — stage, attempt and evidence controls

**Evidence.** `batch_stage_runner_v3_r11_r2.py` restricts authorization to the canonical `authorizations/stage_01.json` path, exact root, manifest/closure/schedule hashes, review hash, eleven-ID digest and method order. A write-once stage intent precedes work. Each arm and audit has a write-once intent, one attempt, an exact command/input binding and a terminal or unresolved state. The reader and summary check original intent bytes, artifact names/paths/sizes/hashes, result/guard contents, proof/common-record bytes, audit input hashes and report/guard cross-hashes before a pair is comparison-eligible. I checked the actual R9 preflight R3 and Auer records: both use `native_proof_sha256`, `common_record_sha256`, nested `guard_result.worker_stdout_sha256`, one worker invocation, and the audited result/common bindings that R11 expects. The R9 result validator resolves artifact paths generically; it is not tied to the old preflight output directory.

The R11 R2 fixture implementation contains 27 non-query cases; its stored report records 27/27 PASS with zero producers. I inspected the cases and report, but did not rerun the fixture suite or invoke a prospective query in this review.

**Consequence.** The former R10 root-reuse, unbound favorable-receipt and lost-interruption routes are addressed for the reviewed source. A favorable stage-level row still requires the separately rederived summary and composition-audit evidence before scientific use.

**Status:** ACCEPT for a limited live Stage 1 integrity check; live Windows behavior remains to be observed.

**Required action:** Run only Stage 1 once; preserve raw records even if the stage stops or the parent is interrupted. Do not retry a consumed intent.

## Finding 3 — interpretation and resource scope

**Evidence.** The schedule and runner retain R3-then-Auer order and stop on the first nonvalid matched pair. `UNKNOWN` is inconclusive. The summary retains all 1,944 universe IDs, the one separate preflight carry-in, attempted and unrun batch rows, method asymmetry, audit status and stop reasons. The 120-second/1-GiB limits apply to each R9 method worker and separately to each read-only audit verifier inside its Job Object; R11 parent/launcher setup is outside those worker limits. Its outer method/audit wrapper timeouts are 150/630 seconds. Setup memory was not measured. The eleven seed cases and 1,944 operating cells are not independent random samples.

**Consequence.** Stage 1 can check whether the source-bound batch plumbing works on real pairs. It cannot by itself justify superiority, a matched-population estimate, a novelty result or a paper claim.

**Status:** VALID as a restricted execution and reporting plan; G4 remains UNVERIFIED.

**Required action:** After Stage 1, replay its stored records and review the fixed-denominator summary before any Stage 2 decision. Do not turn a stopped or `UNKNOWN` pair into an unsafe or negative method outcome.

## Final disposition

**GO: exact `stage_01` only**, with a separate authorization receipt at the canonical path and the assignment `docs/CODEX_TO_LUNA_G4_AUER_R11_R2_STAGE_01_EXECUTION.md`. No Stage 2–7 authority is granted. Batch state at review: **0/1,944**; R9 single-query preflight remains one separate completed pair. Research status: **HOLD; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED**.

**Pre-issue receipt correction.** During receipt creation I appended literal backtick/`n` bytes after the closing JSON brace. The invalid, unparseable file was archived byte-for-byte as `docs/reviews/G4_R11_R2_STAGE_01_INVALID_PREISSUE_RECEIPT_6440a210.json` (SHA-256 `6440a210cabeff7174502c8408be2ac0dce5041067fa7e2d47e5f61887dfe94b`). It was removed from the canonical authorization path before any stage intent, worker, audit or query existed. It is not an authorization. Only the later valid JSON at the canonical path, bound to this final review hash, is executable.
