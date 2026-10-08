# Assignment for DDWMR | LUNA-G4-AUER — R13 prospective continuation implementation

Read `AGENTS.md`, all four `research_context` files, `docs/reviews/CODEX_G4_AUER_R11_R2_STAGE_01_RESULT_REVIEW.md`, `docs/reviews/CODEX_G4_AUER_R12_CONTRACT_AND_CONTINUATION_REVIEW.md`, and the R12 R2 protocol/handoff first. Work only in this shared repository. Preserve the R9 preflight, R11 Stage 1, R12 R2 candidate and all existing results byte-for-byte. Do not commit, push, clean, retry either observed ID, start a query, invoke a producer/auditor on a live query, or issue a GO receipt in this assignment.

## Goal

Turn the reviewed **candidate continuation policy** into a versioned, prospective, source-bound runner and independently replayable checker, ready for a separate Codex source review. Prepare the exact first R12 stage scope only; this assignment authorizes **zero** of the 1,942 continuation queries.

## Required implementation

1. Bind the 1,944-ID R9 universe, R10 flattened eligible order, separate R9 carry-in, immutable consumed R11 ID, and exact R12 1,942-ID schedule. Check seven group counts and ordered-ID SHA-256 digests using the no-trailing-newline convention. Reject any duplicated, skipped, reordered, retried or substituted ID. Use a new R13 candidate namespace; do not resume the stopped R11 Stage 1 directory or relabel its receipt complete.
2. Implement a future arm/audit contract checker that verifies source/profile/input/authorization pins, original write-once intent, terminal receipt, canonical command, artifact path/size/hash, result/guard/resource status and proof/common/audit bindings. For present common records, use the actual R9 schema and the exact transitive binding accepted in the R12 review. Class 1 requires a fully verified positive native proof, complete full-hold common predicate and PASS independent composition audit. Class 2 needs an authenticated terminal nonpositive outcome. All ambiguous or favorable-but-incomplete records are class 3.
3. Define the future no-common `UNKNOWN` path as an explicit `AUDIT_NOT_APPLICABLE_NO_COMMON_UNKNOWN` record checked without launching the composition auditor. Keep the preserved R11 R3 `ARTIFACT_REJECTED` audit only as historical evidence; do not generalize that rejection into a prospective class-2 rule. A present proof plus common record requires the independent audit even if its common predicate is UNKNOWN.
4. Specify and verify resource-limited class 2 precisely: declared wall/memory limit, installed enforcement, worker termination, raw reason, available artifact hashes, no favorable status, and a matching terminal receipt. Missing termination evidence, parent interruption, unresolved intent or inconsistent resource records are class 3. Keep method worker, launcher/setup and composition-audit time/memory separate; label any unmeasured setup memory `NOT_MEASURED`.
5. Enforce R3-then-Auer order for each ID. If the first arm is class 3, stop before Auer. Advance to the next ID only when both arms have verified terminal class 1 or 2 and every applicable audit is accounted for. Any class 3 stops before another ID. Write intent before launch and terminal receipt after completion; never retry a consumed intent. A restart must reconcile files read-only and fail closed on an unresolved intent. Do not auto-advance stages; each stage needs a later, separately reviewed exact-scope GO receipt.
6. Produce a deterministic fixed-denominator summary and an **independent** replay checker over the R13 receipts. Keep R9 and R11 historical strata separate from R13 planned/attempted/not-run counts; distinguish class-1, class-2 UNKNOWN, class-2 authenticated resource limit, class-3, audit PASS/not-applicable/rejected/unresolved, and both absolute planned yield and conditional observed yield. Do not interpret `UNKNOWN` as unsafe or a failed mathematical method. Do not claim the operating cells are independent samples.

## Non-query verification package

Prepare synthetic receipt fixtures or mutation checks that exercise each class and failure boundary, without invoking a live R3/Auer worker: valid positive proof/common/audit binding; valid no-common UNKNOWN; valid proof-complete common UNKNOWN; authenticated wall and memory stops; missing favorable proof/common/audit; altered result/common/proof bytes or size; wrong query/input/source/GO hash; duplicate intent; unresolved intent; mismatched or absent resource termination; stage reorder; cross-stage auto-advance. Record the exact observed pass/reject outcomes and source hashes. If a fixture cannot faithfully represent a native proof, label it a contract fixture, not a scientific certificate.

Before requesting stage execution, freeze a new manifest/source closure, versioned runner/checker, first-stage no-GO authorization template and source-closure inventory. Verify them on a clean read-only copy or an isolated candidate namespace. Report any incomplete branch explicitly. The first-stage schedule must contain the **ten remaining IDs** from old Stage 1 in frozen order. Do not create an executable GO receipt; Codex must review the exact final source and artifacts first.

## Handoff and short terminal reply

Write a detailed Markdown handoff under `docs/reviews/LUNA_TO_CODEX_G4_AUER_R13_..._FULL_HANDOFF.md`, including source locations, exact hashes, fixture outcomes, stage accounting, remaining blockers and a clear GO-to-review / NO-GO-to-query recommendation. The chat reply should contain only:

`Session: DDWMR | LUNA-G4-AUER`  
`Status: <DONE or BLOCKED; no new query; R12 0/1,942 attempted>`  
`Handoff: <absolute path to Markdown file>`
