# Codex review — G2 R10 whole-hold Picard candidate

**Date:** 2026-10-04  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G2_R10_WHOLE_HOLD_PICARD_CANDIDATE_FULL_HANDOFF.md`  
**Disposition:** ACCEPT the conditional closed-slab/whole-hold mathematical argument. **NO-GO for the two real R10 rows, the 800-row study, and G2 promotion** until the checker and decision-trigger defects below are corrected and reviewed.

I read `AGENTS.md`, the four canonical `research_context` files, the R9 review, R10 assignment, handoff, proof contract, producer, checker, model/interval primitives, source binder, manifest and fixture declarations. I inspected source and stored evidence read-only. I did not run either R6 input, a native query, the R10 producer, or a fixture suite in this review.

## Finding 1 — source and execution identity

**Evidence.** The raw R10 closure SHA-256 is `63a7af65317b683345c54a0bc377935cf907260a944d1b1234473193fcedf6d9`; all 163/163 listed source-input path/hash records matched the current files in an independent read-only scan. The manifest hash is `0bddb54bc0c2ab97687921e44bb5f376807250277bd10192d70551f062fbd9e5`, producer `e9fa6672649d675e27bb4f419e28259b9546b01bb6592f3388396ecd2a211c47`, checker `6ba67a808bc9e5125cbf8112265c3a074a9b005566ef02d06e6121825e150783`, and binder `c3e7057a4d02353c496fd7d0481a577834a53d5f45baa0f3f5f343bdd2176d05`; these match the handoff. The manifest binds R5 indices 12 and 24 as observed development-overlap inputs and records no R10 evaluation authority. The handoff reports zero native queries, zero R10 evaluations of those rows, and R5 800/800 `NOT_RUN`.

**Consequence.** This is a prepared source-bound candidate and synthetic evidence, not a new safety result for either real row. The handoff-reported fixture outcomes were not independently rerun here.

**Status:** VALID identity and declared execution scope.

**Required action:** Preserve the R3/R5/R6 results and both consumed R6 outcomes byte-for-byte. Keep the two R10 rows marked development overlap.

## Finding 2 — closed-slab theorem

**Evidence.** For every fixed parameter label and fixed held voltage, the interval RHS must enclose the exact six-state vector field on the closed candidate box `B_k`. If `X_k ⊆ B_k` and `X_k + [0,h_k] G_k ⊆ B_k`, the Picard map sends continuous `B_k`-valued paths into themselves. The clip law is globally Lipschitz; the stated row-sum `L` is a uniform upper bound for every fixed label under the positive denominator assumptions. In the Bielecki norm with `lambda=L+1`, the map has contraction factor at most `L/lambda < 1`. The fixed point exists on the whole closed slab, and its endpoint lies in `X_k+h_kG_k`. Carrying that box and the pose endpoint through an exact contiguous partition of `[0,T]` gives a sound whole-hold outer enclosure. The code forms the pose tube from the slab's physical `u,r` intervals, uses rational trigonometric/root outer bounds, and applies sufficient full-slab collision/contact and additive progress lower bounds.

**Consequence.** The R9 first-exit boundary gap is resolved at the mathematical level. Forgetting parameter correlations in a uniform outer image increases conservatism; it does not require an execution parameter to switch. A negative sufficient margin remains `UNKNOWN`, not an actual collision/contact violation.

**Status:** VALID **conditional theorem** for the unchanged reduced model and the stated interval-RHS/positive-parameter assumptions. This is not a proof of physical correspondence or useful conservatism on the R6 inputs.

**Required action:** Retain those assumptions and the one-fixed-label quantifier in any later certificate claim.

## Finding 3 — checker mishandles fully saturated slip intervals

**Evidence.** The producer clamps *both* endpoints into `[-1,1]` in `validation/g2/time_slab_picard_r10.py:62`. The independent checker instead sets `low=max(-1,value.lo)` and `high=min(1,value.hi)` in `validation/g2/whole_hold_picard_checker_r10.py:58`. For an allowed slip interval `[3/2,2]`, it constructs `[3/2,1]`; for `[-2,-3/2]`, it constructs `[-1,-3/2]`. `Interval.__post_init__` rejects these reversed intervals. The checker calls this function both for the RHS and contact reserve. The 12 declared fixture groups include no whole-hold record on a fully saturated positive or negative clip branch.

**Consequence.** A valid producer record spanning such a branch can be rejected as `INVALID_RECORD` even when the clip-law enclosure is sound. This is a completeness/producer-checker mismatch, not evidence of a false positive certificate. Saturation is within the authoritative model and was deliberately exercised in earlier hand cases, so the current exact checker source cannot be accepted as the general R10 replay path.

**Status:** **BLOCKER** for approving these producer/checker bytes for real-row execution.

**Required action:** Version the checker correction; clamp each endpoint as the producer does. Add non-query full-record fixtures for intervals wholly above `+1`, wholly below `-1`, and crossing each clip corner, covering RHS and pose/contact replay. Rebuild the closure and report exact new hashes and outcomes.

## Finding 4 — decision trigger contradicts its stop rule

**Evidence.** The R10 manifest's `predeclared_decision_trigger` requires the positive-voltage row to be `CERTIFIED` and task-eligible while the zero-voltage row **lacks** that combined result. Its `one_shot_stop_rules` then says the trigger is false if **either** row is `UNKNOWN` or not task-eligible, among other conditions. A zero-voltage row that lacks the combined result through `UNKNOWN` or task ineligibility therefore both satisfies the intended contrast and forces the trigger false. The handoff repeats the same conflict in its Section 6.

**Consequence.** As written, the two-row trigger has no coherent success outcome. Any interpretation chosen after observing R10 results would be post-hoc. A valid `UNKNOWN` must remain inconclusive, and task ineligibility under a valid safety certificate is distinct from safety `UNKNOWN`.

**Status:** **BLOCKER** for a predeclared decision-relevant study or execution authorization.

**Required action:** Before evaluating either row, replace the conflicting text with one exact truth table. A strong task-selection distinction may require `(+1,+1)` verified safety plus `task_eligible=true` and `(0,0)` verified safety plus `task_eligible=false`; a separate weaker certificate separation may report `(0,0)=UNKNOWN` without calling it unsafe. State which, if either, motivates the later study and why. Bind the finalized rule in the next manifest and closure before any row is run.

## Finding 5 — evidence and next scope

The handoff reports a synthetic two-slab positive record, one adaptive split, a replayed arithmetic-cap `UNKNOWN`, and 17 rejected mutations. Those observations support development of the contract but contain no R10 enclosure, collision/contact margin or progress value for the two real inputs. The 30-second cap is cooperative during rational operations; it is not yet a separately enforced hard process limit. A later one-shot execution needs source-bound intent, terminal and replay accounting so a partial/interrupted row cannot be silently retried.

**Final disposition:** The mathematical Picard construction is conditionally sound, but the **R10 implementation and two-action decision protocol are not ready for real-row execution**. No G2 PASS or usefulness claim follows. Preserve **HOLD; G1 restricted reduced-model PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED**. The next G2 assignment is `docs/CODEX_TO_LUNA_G2_R11_PICARD_CHECKER_AND_TRIGGER_CORRECTIONS.md`.
