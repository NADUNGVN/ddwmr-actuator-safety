# Codex review — G2 R5 one-query runner and auditor

**Date:** 2026-10-03  
**Handoff:** `docs/reviews/LUNA_TO_CODEX_G2_DECISION_DOMAIN_R5_ONE_QUERY_RUNNER_PREPARATION_FULL_HANDOFF.md`  
**Authority:** MASTER v2.1 and `AGENTS.md`; reviewed on shared `main` at `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe` without commit or push.

## Decision

**ACCEPT_R5_ONE_QUERY_RUNNER** for the exact source-bound, single-row preflight path. This accepts the runner and post-publication auditor in source and non-query fixture scope. It permits **one** native G2 R3 `run_query` call for manifest index 0 only after the user's exact one-query instruction is relayed and a fresh receipt binds that instruction, this review, the candidate and runner hashes. It does not authorize any of the 800 study rows as a study, query 2, or a batch. The current R5 template is `TEMPLATE_NOT_AUTHORIZED` and must never be treated as a run receipt.

The exact query ID is `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1`. The sealed CLI raw SHA-256 is `4a5885528a5c9aebab76ad38b3278a66e75cb44e5b90f6f5fc52fbd41b1fe66a`. The R5 source closure raw SHA-256 is `53a923a0be15bd9be977040b996dc2104a763a061e2bad9ef848241a530a55e9`. These three bindings are intentionally present in this review for the runner's exact-review precondition.

## Finding 1 — candidate bytes and corrected handoff hash

**Evidence.** The R5 `--check-only` command returned `PASS_READ_ONLY`: 74/74 source/input entries verified; manifest raw SHA-256 `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b`; closure raw SHA-256 `53a923a0be15bd9be977040b996dc2104a763a061e2bad9ef848241a530a55e9`; 800 rows `NOT_RUN`. I also recomputed all 74 raw entry hashes independently and found no mismatch. The selected canonical query hash `3668b9fb3bf30e11b8b177508f8b519855e8d4e96e33d7352335cbaea838db17` and native input-payload semantic hash `dde72762c6a6feb8932d0d617c11cefbe271ecaba288bc6d282d8be19bcbb0a5` are pinned in the R5 adapter/config/template.

The handoff's table gives the config raw hash as `8e2816468bf682290a91535857f2c3d8d6d5acd4c5edf14e23a4623a205f1d5`, a **63-character transcription error**. The actual config, sidecar and receipt template consistently give the correct 64-character SHA-256: `8e2816468bf682290a91535857f2c3f9ad4ff2ba8be99ec5c77acc0ca19a6e19`. The handoff must be read with this erratum; do not copy its malformed value into an authorization receipt. No candidate/source byte needs repair for this documentary error.

**Consequence.** R5 is an exact-byte preflight candidate with unchanged R4/R3 rows and profile. The typo is confined to the prose handoff; the executable bindings agree.

**Status:** VALID candidate binding with a documented handoff erratum.

## Finding 2 — one native-call boundary and evidence capture

**Evidence.** `validation/scripts/run_g2_decision_domain_r5_one_query.py` accepts no CLI arguments and delegates to the closure-bound runner module. Before the call, the runner reloads nested R5/R4/R3 closures, reconstructs index 0, checks both query hashes, the accepted review path/hash, exact user-instruction receipt, runner/module hashes and absent output/attempt/checkpoint paths. It writes a write-once attempt marker immediately before the native call. After a returned record or caught exception, it writes an `fsync` checkpoint before checker replay, then publishes a write-once bundle by staging-directory rename. A consumed attempt marker prevents retry at a second destination. The saved result is labeled `ONE_QUERY_PREFLIGHT_ONLY_NOT_STUDY_RESULT` and the 800-row manifest remains `NOT_RUN`.

The code's `call_completed` flag is set before its defensive non-dictionary return check. A non-dictionary stub return would therefore produce an inconsistent completion count and an auditor-rejected bundle. The bound native `run_query` source returns a dictionary on all explicit return paths, so this is outside the present exact-source path. Record the limitation and correct it in a later version if the runner is generalized; do not describe every arbitrary injected return as cleanly audited.

**Consequence.** The reviewed CLI constrains the exact preflight to one attempted native call and retains incomplete-attempt evidence. The evaluator's 15-second check is cooperative; this review does not assert a hard wall deadline.

**Status:** ACCEPT for the exact source and row; no real call has yet occurred.

## Finding 3 — independent published-output replay

**Evidence.** The auditor reloads the candidate and output bundle, checks the exact member list, raw hashes, source/receipt/review bindings, attempt marker, checkpoint and record bytes; then calls native R3 `replay_record`, reconstructs the R2 endpoint record and replays it. It compares stored checker diagnostics, status and counts with recomputation. The bundle's `COMMIT.json` hash consistency alone cannot make tampered proof/status fields pass. I reran `validation.scripts.verify_g2_decision_domain_r5_fixtures`: exit 0, `PASS_NONQUERY_FIXTURES`, three injected stub calls in temporary directories, **zero native `run_query` calls**, and 800 study rows untouched. The fixtures rejected changed ID, absent receipt/review, stale source, second attempt, altered status and altered proof; they audited resource `UNKNOWN` and an injected exception as non-success evidence.

**Consequence.** The published artifact has a read-only proof-to-status replay path suitable for one preflight result. Fixture success is not a safety or task-usefulness outcome.

**Status:** ACCEPT in source/non-query fixture scope.

## Finding 4 — authorization and scientific limits

**Evidence.** At review time the active receipt, accepted R5 review file, attempt marker, checkpoint and output bundle were absent. This review supplies the accepted-review file only. The R5 runner also requires a `user_authorization.exact_instruction` containing the exact query ID, its SHA-256 and an event reference. These fields cannot be fabricated from the template or from a Codex review: their truth depends on the user's relayed instruction. Hash checks verify consistency, not the author of an instruction. The broader user mandate covers scoped validation work, but the R5 implementation deliberately requires this additional exact text before it will run.

**Consequence.** The next concrete step is to relay one exact user instruction and create a separate receipt from it, then make a fresh read-only hash check before executing the sealed CLI once. A positive one-query result remains a plumbing result outside the 800-row study and cannot demonstrate voltage-selection usefulness.

**Status:** GO for exactly one preflight **only after** that instruction/receipt; current study state **800/800 `NOT_RUN`**. HOLD remains; G1 restricted PASS, G2/G3/G4 and physical correspondence UNVERIFIED.

## Final disposition

The R5 source/fixture review is complete and the handoff hash typo is corrected above. A single-query execution handoff is prepared separately in `docs/CODEX_TO_LUNA_G2_DECISION_DOMAIN_R5_ONE_QUERY_PREFLIGHT.md`. No controller, G3, hardware work, 800-query study, commit or push is authorized by this review.
