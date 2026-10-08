# Codex review — G4 Auer R9 one-query matched preflight result

**Date:** 2026-10-03  
**Handoff:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_R9_SINGLE_QUERY_PREFLIGHT_FULL_HANDOFF.md`, raw SHA-256 `a95d2ca412dd1cf410f64074c420bbc4a171ff7d6096429f265a8c98e5a567e8`.  
**Authority:** MASTER v2.1 and `AGENTS.md`; prior R9 permission covered this one ID only.

## Decision

**ACCEPT the first R9 matched pair as a complete, proof-replayed, hash-bound preflight for its exact ID. NO-GO to run the 1,944-query batch under the one-query assignment.** The next step is a source-bound staged batch runner and predeclared reporting protocol, reviewed before query 2. This review does not establish a method advantage, G4 novelty or a gate pass.

## Finding 1 — artifact identity and one-query accounting

**Evidence.** I independently recomputed the handoff hash above and all 21 artifact byte lengths and SHA-256 digests in `artifact_hash_ledger.json`; 21/21 match. The matched receipt records exactly one attempted ID, `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`, one R3 arm, one Auer arm, one complete pair, zero retries or substitutions, and zero batch rows. The pre-run lock ledger and both audit guard records have `PASS` status. Candidate manifest and closure hashes remain `db0df35c634b91df0e498819d1480ee18c694608b2b68538a0580044132c74d8` and `7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533`.

**Consequence.** The stored artifact set is internally traceable to the separately authorized first-ID preflight. The batch remains **0/1,944**, while preflight has **1/1,944** complete matched pair.

**Status:** VALID exact-byte receipt and scope.

## Finding 2 — native and common results

**Evidence.** The stored receipt reports R3 native `CERTIFIED`, Auer native `PROOF_COMPLETE`, both native replays `PASS`, both common predicates `PASS_ON_SUPPLIED_TUBE`, and both final statuses `CERTIFIED`. The independently stored composition-audit reports each say `PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED`, with frozen query reconstruction, loaded native proof, native replay, proof-derived common segments, recomputed common predicate and stored/recomputed common-record equality. The live Auer work-vector equality branch reports worker and audit values of producer 4, replay 4, combined 8, cap 100,000. The audit guards record zero producer/IVP and batch evaluations. These source/audit paths were reviewed in the R9 preflight review; I did not rerun either producer or native replay in this review.

**Consequence.** The evidence supports a successful execution-path check for this one formal-model input. One pair cannot measure cross-grid reliability, relative conservatism, runtime distribution or novelty. The worker times (R3 0.563 s, Auer 0.516 s) are individual observations, not a method-performance conclusion.

**Status:** ACCEPT in one-query preflight scope; broader comparison UNVERIFIED.

## Finding 3 — batch execution remains a separate source and decision

**Evidence.** The R9 protocol/candidate preserve 1,944 ordered IDs but mark `batch_start_authorized=false`. The reviewed guard accepts a single query and refuses overwrite; there is no reviewed batch scheduler, immutable per-row attempt ledger, no-retry/resume policy or complete batch denominator reporter. The one-query authorization receipt cannot supply those missing controls.

**Consequence.** A deterministic staged runner and its exact source/input closure must be prepared and reviewed before the remaining IDs are attempted. Stage selection and stopping rules must be fixed before viewing stage outcomes; `UNKNOWN` is inconclusive and resource stops remain recorded.

**Status:** **NO-GO batch now.** Prepare a versioned batch candidate without executing query 2.

## Final disposition

The R9 one-query preflight completed as reported. The next direct assignment is `docs/CODEX_TO_LUNA_G4_AUER_R10_BATCH_PREPARATION.md`. Preserve **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED**. No G3, controller, hardware work, novelty claim, commit or push follows.
