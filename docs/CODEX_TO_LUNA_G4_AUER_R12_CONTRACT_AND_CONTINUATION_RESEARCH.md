# Assignment for DDWMR | LUNA-G4-AUER — R12 contract and continuation research

Read `AGENTS.md`, all four `research_context` files, and `docs/reviews/CODEX_G4_AUER_R11_R2_STAGE_01_RESULT_REVIEW.md` first. Work only in `projects/ddwmr-actuator-safety` on the shared current branch. Preserve the R9 preflight, R11 Stage 1 output, authorization, manifest, source closure and derived summary byte-for-byte. Do not commit, push, clean, retry the consumed ID, run a new query, or start another stage in this assignment.

## Deliverable A — contract correction candidate

Trace the R9 common-record producer, R9 result/guard/composition audit, R11 arm reader and R11 summary. Prepare a **versioned** read-only verifier/summary candidate that accepts the actual R9 common-record schema through exact path/hash/size, result-to-query/input, native proof and independent composition-audit bindings. The current R11 demand for `query_id` and `method_input_sha256` *inside* the common JSON conflicts with the producer; do not add those fields to preserved artifacts or simply disable all binding checks. Specify exactly how an existing common record is tied to the frozen query and method input, including the `UNKNOWN_ON_SUPPLIED_TUBE` case. Retain strict rejection for missing or changed favorable proof/common/audit evidence.

Re-adjudicate the preserved single Stage 1 pair **read-only** under this candidate and report both classifications side by side: original R11 classification and candidate classification. Report Auer's raw execution, proof replay, audit, common `UNKNOWN`, and verification status separately. R3 remains `UNKNOWN` with no common predicate evaluation; do not manufacture a common record or convert it to unsafe. Include exact old/new source hashes and a negative mutation matrix for the binding checks in the handoff. No query worker or producer may be invoked.

## Deliverable B — scientifically usable continuation protocol candidate

Design a versioned continuation for the prespecified ordered universe. Keep 1,944 IDs in the reporting denominator and show the R9 preflight and consumed R11 ID as two already observed strata; only 1,942 IDs remain unattempted. Preserve their original order and membership. State explicitly that no retry is permitted and that the new protocol was designed after observing the first R11 outcome.

Separate at least these outcomes:

1. Verified `CERTIFIED` with an independently replayed full-time common predicate.
2. Authenticated terminal `UNKNOWN` or resource-limited outcome with no positive certificate.
3. Integrity, source-lock, authorization, artifact-binding or unresolved-intent failure.

Propose when the batch may continue after class 2 and when it must stop for class 3. Give separate denominator, certification-yield, inconclusive, resource and audit-rejection accounting. Never score `UNKNOWN` as unsafe or as a method failure. Retain method-specific runtime and memory, with setup and audit costs distinguished. Explain what matched conclusions are possible when one method has a complete positive common predicate and the other has only an authenticated `UNKNOWN`. Do not claim statistical independence of the operating cells, novelty, or method superiority from a count alone.

Prepare source-bound manifest/schedule/authorization **candidates** and a non-query verification plan for the remaining IDs and the two observed strata. In particular, a later-stage design must not pretend that the immutable R11 Stage 1 receipt says `STAGE_COMPLETE`. Do not issue a GO receipt. End with a concrete `GO/NO-GO` recommendation for independent Codex review; query execution remains NO-GO until that review and a separate exact-scope authorization.

## Handoff and short terminal reply

Write a detailed Markdown handoff under `docs/reviews/LUNA_TO_CODEX_G4_AUER_R12_..._FULL_HANDOFF.md` containing exact paths, hashes, source findings, the read-only re-adjudication, accounting and unresolved issues. The chat reply should contain only these three lines:

`Session: DDWMR | LUNA-G4-AUER`  
`Status: <DONE or BLOCKED; no new query; 1/1,944 attempted>`  
`Handoff: <absolute path to Markdown file>`
