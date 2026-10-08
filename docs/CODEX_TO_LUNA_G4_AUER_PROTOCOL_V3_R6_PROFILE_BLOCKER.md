# Codex to `LUNA-G4-AUER` — correct R6 source blockers

**Session title:** `DDWMR | LUNA-G4-AUER`  
**Date:** 2026-10-02  
**Working directory:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Observed branch/HEAD at Codex review:** `main` / `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`  
**Review:** `docs/reviews/CODEX_G4_AUER_PROTOCOL_V3_R6_SOURCE_REVIEW.md`  
**Input handoff:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_PROTOCOL_V3_R6_COMPOSITION_BLOCKER_FULL_HANDOFF.md`  
**Authority:** MASTER v2.1, `AGENTS.md`, workflow W1. **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.**

You are the **G4 Auer matched-baseline session**. The user separately started `LUNA-G2-SCOPE` in the same working tree for the G2 proof/usefulness audit. That session writes new G2 scope documents only. Coordinate by file boundary, not by changing branches or resetting shared files. At start, record branch, HEAD, `git status --short`, and the R6 closure/manifest hashes. Do not commit, push, clean, stash, reset, restore, switch branches, or edit the G2 scope files. Preserve every R3/R4/R5/R6 artifact and candidate byte-for-byte; make a fresh, uniquely versioned G4 correction.

## Context to retain

- R3's synthetic full grid already has 1,944/1,944 replayed proof records, but G2 remains UNVERIFIED. This is **not** a matched Auer comparison.
- R4/R5 established one native Auer proof and archived composition/mutation evidence. R6 added a read-only per-query proof-to-common verifier and R3 common-stage budget reparsing.
- R6 source closure is `56de9b89ed0d6bc0d4b46e88163b37e3254e61c4dbf2f95a306fcc8b83205c72`; candidate manifest v6 is `f722ac6f2df39cc1f2fdbae8ea3df7b1684c91659efb708aeba01fb5b436fa65`. Its 92/92 dependency hashes match. Archived Auer/R3 compositions and 13/13 mutations passed in the selected non-query fixture.
- The matched comparison is **0/1,944**. Manifest v6 has every row `NOT_RUN`, `comparison_run=false`, `query_1_authorized=false`, and `batch_start_authorized=false`. No gate is promoted.

Read `AGENTS.md` and all four canonical `research_context/` files first, then the R6 handoff, the Codex review, protocol R6, R3/Auer profiles, both workers, the composition verifier, fixture source/report, and source-closure manifest.

## Required correction A — R3 proof-size profile contract

`validation/g4/r3_matched_query_worker_v3_r6.py:334` reads `profile["max_serialized_proof_bytes"]`, but `validation/configs/r3_g4_matched_profile_v3_r6.json` has no such key. The lookup is reached after any successful `run_query` return and is not caught as a declared resource stop. The archived fixture bypasses `run_one`, so its pass does not exercise this branch.

In a new versioned candidate, declare and freeze a finite R3 native-proof serialization byte cap **before** any matched query. Give its rationale in the profile/protocol and make worker, schema and resource reporting use the same cap. Preserve the existing 120-second/1-GiB external guard and other frozen method limits. Audit all literal profile-key reads in both worker paths and prove the prospective profile supplies them. Add a non-query contract fixture that exercises the proof-serialization lookup and expected size-limit classification using stored data, without invoking `run_query` or creating a new trajectory proof. A new R3 profile may change its method-input hash; recompute prospective hashes while keeping the archived R3 fixture explicitly historical.

## Required correction B — Auer combined RHS cap audit

The prospective Auer worker seeds native replay's RHS counter with the producer count (`auer_matched_query_worker_v3_r6.py:489-519`). The offline composition verifier starts replay with zero (`verify_matched_composition_v3_r6.py:255-275`), although the profile's 100,000 RHS/Jacobian limit covers producer plus native replay. Make the read-only verifier check or mirror that combined method cap without charging its independent post-worker elapsed time to the matched worker. Reject malformed/missing complete-proof work fields; report the actual count and cap. Add a non-query boundary fixture or mutation that distinguishes the correct combined-count behavior from the current zero-start behavior. Do not claim a resource cap was independently validated from a status string alone.

## Deliverable and stop boundary

Create a new source/protocol/profile/schema/closure/manifest version as needed; retain all v6 bytes. Recheck transitive imports and all exact-byte dependency hashes; keep the same 1,944 ordered IDs and all candidate rows `NOT_RUN`. Refresh any fixture or probe evidence whose source identity changes. In the handoff, separate archived-proof fixture evidence, prospective worker behavior, and method-worker versus offline-audit resource accounting. Use Finding / Evidence / Consequence / Status / Required action and include exact paths, hashes and commands.

Write the full Markdown handoff under a new `docs/reviews/LUNA_TO_CODEX_G4_AUER_..._FULL_HANDOFF.md` filename. State the session name **`LUNA-G4-AUER`** and the other session **`LUNA-G2-SCOPE`** at the top so the user can relay it unambiguously. **Do not run query 1 or the 1,944-query batch. Do not start G3, controller or hardware work. Do not commit or push.** Return only the new handoff path and a short status summary to the user.
