# Codex review — G2 decision-domain R3 execution preflight

**Date:** 2026-10-03  
**Session reviewed:** `DDWMR | LUNA-G2-SCOPE`  
**Handoff:** `docs/reviews/LUNA_TO_CODEX_G2_DECISION_DOMAIN_R3_EXECUTION_PREFLIGHT_FULL_HANDOFF.md`  
**Repository state:** `main` at `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`, shared uncommitted worktree.  
**Authority:** MASTER v2.1 and `AGENTS.md`. This review does not change a gate or plant assumption.

## Decision

**ACCEPT the R3 v6 artifacts as a reviewable execution preflight, with the exact limits below. NO-GO to freeze or run the 800-query study.** The read-only candidate check, manifest-to-query adapter, and safety-then-endpoint replay path are useful progress. The current result aggregation can count unverified outcomes as successes, and its provenance contract overstates what the input ledger records. These are blockers at the study decision boundary, not counterexamples to the conditional R3 safety inclusion or the R2 endpoint inequality.

The candidate remains **800/800 `NOT_RUN`**. Overall **HOLD**; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED. The separate G4/Auer R9 review and one-query assignment already exist and are not reopened here.

## Finding 1 — candidate integrity and fixed universe

**Evidence.** I inspected `validation/scripts/build_g2_decision_domain_r3_candidate.py`, `validation/g2/decision_domain_adapter_r3.py`, the v6 manifest and closure, and ran the R3 builder's source-inspected, read-only `--check-only` path. It returned exit 0 with manifest raw SHA-256 `5ca87bc92429290d0c3967b3331f2a6cfec3b9482c7b5a7cc7532fbb5db20907`, closure raw SHA-256 `b6b5c8b91fdc7c7dbc3c3b02fefb719f5aeeeaf9576ddf7cbbd584c9864b3469`, and 70 verified source/input entries. A separate raw-byte hash comparison found 0 mismatches in those 70 entries. Direct JSON inspection found 800 unique query IDs, 32 groups, 400 development and 400 held-out rows, 400 rows at each horizon, and 800 `NOT_RUN` rows with null result records. The R3 read-only path does not invoke the historical R2 builder's write-prone check path.

**Consequence.** The exact v6 pre-run bytes are sufficiently identified for review. The builder check is a consistency check against the current working tree, not a study execution or an external freeze receipt.

**Status:** VALID pre-run integrity evidence. No query result accepted.

## Finding 2 — row binding and conditional proof path

**Evidence.** `load_candidate_context` checks the raw and semantic manifest hashes, both sidecars, closure entries, benchmark raw and semantic hashes, specification bundle, and 12-label parameter image. `bind_manifest_row` requires parsed-row equality at the ordered index and constructs the native R3 query from that row. The legacy `development_manifest_sha256` field is explicitly assigned the semantic SHA-256 of the complete 800-row candidate manifest; the raw manifest hash is carried separately. `validate_safety_record` calls native R3 `replay_record` against that bound query, then constructs and replays the R2 endpoint record. It marks task eligibility only for replayed `CERTIFIED` safety and replayed progress above the exact threshold. No `run_study_manifest_row` call was made in this review.

**Consequence.** These components provide a conditional path from a bound row to a checked one-hold task result. They do not by themselves ensure that the later aggregate uses only results from this path.

**Status:** ACCEPT as a source-inspected preflight component; future proof-bearing records require their own replay.

## Finding 3 — unverified outcomes can enter success counts

**Evidence.** `decision_selector_r3.py::aggregate_outcomes` accepts arbitrary outcome dictionaries and passes them directly to `choose_group_action`. `_eligible` checks `status`, four caller-supplied flags/fields and a rational lower bound; it does not require a safety record, endpoint record, hash ledger, manifest binding, or replay at the aggregation boundary. No locked production call chain connects `validate_record_stream` or `run_study_manifest_row` to this aggregator. In a read-only in-memory counterexample on one held-out group, I supplied a `TASK_ELIGIBLE` outcome with `safety_record=None`, `endpoint_record=None`, `hash_ledger=None`, and favorable Boolean flags. The aggregate reported `selector_success=true` for that group. This exercises only the aggregator; it does not forge a record that passes either checker.

`_eligible` also calls `_q` on caller-supplied rational fields without converting malformed values into a row-level non-success. A malformed asserted-eligible outcome can raise rather than remain in the fixed denominator.

**Consequence.** The current aggregate is not a proof-enforcing result boundary. A study result produced by this API alone could claim task success without proof replay.

**Status:** **BLOCKER for freeze/run and task-usefulness claims.** Require an end-to-end entry point that binds the frozen manifest, parses raw records, replays both proofs, and only then computes counters. At the counting boundary, verify provenance rather than trusting supplied `status`/Boolean flags. Invalid inputs must remain non-successes in all fixed denominators.

## Finding 4 — unique-certificate counter admits a rejected zero record

**Evidence.** `choose_group_action` sets `zero_safety_unknown` from `zero_outcome.get("safety_status") == "UNKNOWN"` alone. It does not require the zero record to have passed integrity or replay. In the same in-memory counterexample, the zero outcome was `HASH_MISMATCH` with a caller-supplied `safety_status="UNKNOWN"`; the nonzero outcome had no proof records. The aggregate nevertheless reported `nonzero_safety_certificate_with_zero_unknown=true`. The current nonzero side checks `safety_replay_pass`, but that too is just a caller-supplied flag at this API boundary.

**Consequence.** The secondary coverage numerator can be inflated by rejected or tampered data. `UNKNOWN` remains inconclusive; this finding is about whether the `UNKNOWN` record is integrity-valid, not whether the zero action is unsafe.

**Status:** **BLOCKER for that coverage claim.** Count a zero `UNKNOWN` only when its exact bound record is either proof-replayed or is an integrity-valid, checker-classified resource abstention. Count nonzero `CERTIFIED` only after actual R3 replay.

## Finding 5 — ledger and reporting contract need correction

**Evidence.** `split_jsonl_records` computes each physical input line's `byte_offset`, but `record_ledger_entry` retains only `source_stream_record_index`, raw bytes/hash/length and semantic hash; `validate_record_stream` does not pass the offset into its row or orphan ledgers. Its `lossless_ledger_contract` and the v6 closure nonetheless state that original stream offsets are retained. `write_lossless_result_contract` computes offsets for the newly serialized **output** JSONL, which are different from input offsets. It writes both output paths with `write_bytes` and can overwrite prior evidence; a failure between writes can leave unmatched output and ledger files. Also, `aggregate_outcomes` hardcodes `candidate_status="PRE_RUN_FIXTURE_ONLY_NO_STUDY_OUTCOMES"`, even for future real outcomes.

**Consequence.** The present contract cannot truthfully claim byte-addressed provenance of every original input record, and a later real aggregate would carry a fixture-only status. This does not alter any R3 mathematical bound, but it prevents an auditable study run under the stated contract.

**Status:** **BLOCKER for freeze/run provenance.** Retain original input index, offset, length and exact bytes for valid, duplicate, orphan and malformed physical lines; verify parsed objects against their raw line bytes. Make output writing write-once or atomic and bind the result to frozen manifest/profile/source hashes. Label fixture and real-run aggregates according to verified execution provenance.

## Finding 6 — freeze and execution are still separate decisions

**Evidence.** The v6 manifest says `NOT_FROZEN_NOT_AUTHORIZED_FOR_EVALUATION`, and `load_candidate_context` requires that value. The sole production-oriented function, `run_study_manifest_row`, can invoke `run_query` for one row, but there is no reviewed freeze receipt or sealed study runner that connects it to persistent results and the trusted aggregate. The 15-second evaluator time check remains cooperative; no hard deadline was demonstrated.

**Consequence.** The current artifact is appropriate for pre-run review, not for a query. A later freeze must identify exactly which bytes are authorized and how one execution produces replayable, immutable evidence. Do not imply a hard 15-second bound.

**Status:** **NO-GO freeze/run now.** The next task is a versioned integrity correction and non-query adversarial fixture pass, followed by a new review. Do not inspect held-out outcomes because none exist.

## Final disposition

The R3 v6 work closes much of the R2 *preparation* gap, but not the proof-enforced aggregation/provenance boundary. The next assignment is `docs/CODEX_TO_LUNA_G2_DECISION_DOMAIN_R4_INTEGRITY_CORRECTIONS.md`, addressed directly to `LUNA-G2-SCOPE`. Keep 800/800 `NOT_RUN`; no G2 promotion, G3 construction, controller, physical experiment, G4/Auer change, commit or push follows from this review.
