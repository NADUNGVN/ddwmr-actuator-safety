# Codex review — G4 Auer R15 exact first-stage validation

**Date:** 2026-10-04  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_R15_STAGE_PREINTENT_REPLAY_CORRECTIONS_FULL_HANDOFF.md`  
**Scope:** one prospective matched stage of the ten ordered R15 IDs.  
**Decision artifact:** [R15 exact-stage decision](CODEX_G4_AUER_R15_EXACT_STAGE_GO_DECISION.json).  

R15 stage decision: GO

<!-- DDWM_G4_AUER_R15_REVIEW_DECISION GO manifest_sha256=e02cde6dfb5c8d07cbac053ebb0db945a4961b4aa1bc383c5dbf5660d707d556 closure_sha256=0488078d3be68e8ddc3da4478553403023ee1c79e4243ac0306dac8b7765d152 schedule_sha256=b2e833cdb20c1d31fde899373ae4d7f2332bd359cc4888d6ddb917840ae96b92 runner_sha256=50ed4b51627661c65eff93b3e098ddaf59a4e86a72896f07af94c04478084f3e checker_sha256=23abbd52a7193ae5149474f2835e828e7b0cea9e6b74ac05deec3462a33ee01b stage_id=r15_continuation_01 query_count=10 ordered_ids_sha256_lf=58a888845732cc8f5220656444d0b6ae9aa19a96eed1c014a7f907e9fac55bbd -->

I read `AGENTS.md`, all four canonical `research_context` files, the R14 review and R15 assignment, the R15 handoff/protocol, manifest, closure, schedule, runner, checker, fixture source/report, candidate builder, review-decision schema and authorization template. This review used source and stored artifacts. I did not run a query, worker, producer, auditor or fixture suite.

## Finding 1 — exact source and stage identity

**Evidence.** Independent byte hashes match the five candidate identities in the marker. All 467/467 R15 closure path/size/hash records match the current files; the 448 inherited R14 tuples are preserved exactly by path. The manifest/closure/schedule sidecars match their raw bytes. The first-stage list has ten IDs and recomputes to the marked LF-joined digest. The corrected R13 manifest hash in `docs/reviews/LUNA_TO_CODEX_G4_AUER_R14_R13_MANIFEST_HASH_ERRATUM.md` matches the actual R13 file and the R14 source lock. The R15 batch root and canonical executable receipt were absent at review time.

**Consequence.** This review concerns one frozen source/schedule identity. It does not incorporate the separate R9 preflight ID or the consumed R11 ID into R15 yield.

**Status:** VALID source and order identity.

**Required action:** Preserve the predecessor artifacts byte-for-byte. Use only the named ten-ID stage, in its locked order.

## Finding 2 — one-shot stop and replay contract

**Evidence.** Source inspection shows the R15 runner records a pre-intent R3 stop after any completed prefix of length 0–9, with the failing next ID outside `attempted_query_ids`, an explicit namespace state and remaining `NOT_RUN` list. The checker reconstructs the completed prefix, failing ID, namespace, method/audit counters and stop state before accepting the terminal. Auer pre-intent and audit pre-intent failures become class-3 partial pairs; unresolved intents cannot restart. The stored non-query report records 70/70 expected outcomes: 24 accepted contract behaviors and 46 expected class-3 rejections. Its fixture source exercises production stage orchestration with temporary synthetic receipts and patched no-op method entry points for every R3 prefix length, Auer and audit pre-intent stops, and counter/prefix tampering. I verified the source and report hashes and their declared coverage; I did not rerun the suite.

**Consequence.** The R14 later-ID and empty-namespace mismatch is repaired in the prospective source. Synthetic contract receipts establish no native proof, Auer result, safety finding or method yield. If execution stops or source changes, preserve the stage and report the checker outcome without retry or substitution.

**Status:** ACCEPT the R15 one-stage source/contract candidate for limited execution; live behavior remains to be observed.

**Required action:** Run at most the one exact ten-ID stage with one R3 and, only after an R3 class-1/2 terminal, one Auer invocation per ID. Halt on class 3. Perform read-only independent composition and fixed-denominator replay on produced artifacts before any scientific comparison. Do not auto-advance or retry.

## Finding 3 — research interpretation and limits

**Evidence.** R15 has 0/10 attempted IDs at review time; R12 continuation has 0/1,942 attempted. The prior R9 preflight and R11 consumed observations remain separate. A future method `UNKNOWN` is inconclusive, and a stopped stage is not a completed matched batch.

**Consequence.** This GO is execution authority for a bounded evidence-acquisition stage only. It is not G4 acceptance, novelty, physical correspondence or a GO for all 1,944 queries. No controller, simulator, G3 or hardware work is included.

**Status:** **HOLD** overall; G1 restricted reduced-model PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.

**Required action:** Produce a detailed one-stage handoff with receipts, exact hashes, independent replay results, fixed denominators, all stops and resource outcomes. No later stage is authorized by this review.
