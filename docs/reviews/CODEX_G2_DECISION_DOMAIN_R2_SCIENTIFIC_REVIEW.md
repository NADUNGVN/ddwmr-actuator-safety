# Codex review — G2 decision-domain R2 candidate

**Date:** 2026-10-03  
**Session under review:** DDWMR | LUNA-G2-SCOPE  
**Handoff:** `docs/reviews/LUNA_TO_CODEX_G2_DECISION_DOMAIN_R2_FULL_HANDOFF.md`  
**Repository snapshot inspected:** `main` at `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`, with a shared, uncommitted working tree.  
**Authority:** MASTER v2.1 and AGENTS.md. This review changes no canonical gate or plant assumption.

## Decision

**ACCEPT** the R2 terminal-progress inequality and its producer/checker source path as a *conditional, conservative endpoint certificate* for the declared synthetic clip-law family. **ACCEPT** the corrected study protocol and the 800-row manifest as reviewable candidates, with the limitations below. **NO-GO to freeze or run the 800-row study yet.**

The inherited R3 full-hold `P1_scaled`/`eta_physical` inclusion was previously accepted for its frozen 0.1 s batch. I additionally inspected the same source formulas for the proposed 0.25 s and 0.5 s holds: their exponential, Picard, comparison-series and elementary-function remainder arguments require a finite positive `T`, not `T <= 0.1`. This supports the conditional source-to-inclusion argument for a new positive proof-bearing record that completes under the locked rational caps and replays. It does not pre-accept a future record, its runtime, or the complete 800-row result.

**HOLD remains. G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.**

## Finding 1 — terminal-progress inclusion

**Evidence.** For one fixed label and one held voltage, the MASTER identity is

\[
p_x(T)-p_x(0)=\int_0^T u(t)\cos\theta(t)\,dt.
\]

If the replayed R3 proof encloses every internal state over the closed hold by `P1_scaled` plus `eta_physical`, physical conversion of the first two predictor coordinates gives (u(t)\in U) and (r(t)\in P_r+[-\eta_r,\eta_r]). The code then encloses every heading by

\[
\Theta_0+[0,T]P_r+[-T\eta_r,T\eta_r]=:\Theta.
\]

For (M=\max(|\Theta_-|,|\Theta_+|)), the global inequalities \(-1\le\cos x\le1\) and \(\cos x\ge1-x^2/2\) give (\cos\theta(t)\in[\max(-1,1-M^2/2),1]\). The exact four-corner interval product supplies a lower integrand bound (g_-), hence (p_x(T)-p_x(0)\ge T g_-\). This is valid for either sign of `u`, across cosine turning points, and over all initial states and execution-fixed labels. The common initial `p_x` cancels in the identity; no independent endpoint-position intervals are subtracted.

`validation/g2/endpoint_r2.py` performs these operations with `Fraction` and rational `Interval`; `validation/g2/endpoint_checker_r2.py` independently reconstructs the serialized endpoint fields after replaying the R3 safety proof. It shares the R3 arithmetic/model trusted base, so it is a separate record calculation rather than an independent safety solver. `task_eligible` can become true only when the safety record replays as `CERTIFIED` and the exact lower bound meets 1/20 m. The arithmetic fixture claims in the handoff were source-inspected; I did not rerun that suite.

**Consequence.** The endpoint derivation and implementation path are sound as a sufficient formal-model bound, conditional on a valid full-hold R3 tube and exact query binding. A subthreshold bound or `UNKNOWN` safety status proves no unsafe motion or insufficient actual progress.

**Status:** VALID within the stated conditional scope.

**Required action:** Preserve the full-hold inclusion premise and the shared trusted base when reporting any later task action.

## Finding 2 — inherited R3 formulas at the new horizons

**Evidence.** `validation/g2/interval.py::interval_matrix_exponential` builds the interval exponential over `[0,T]` and adds a global (e^q q^{d+1}/(d+1)!\) remainder majorized by (3^{\lceil q\rceil}\). `validation/g2/evaluator.py::_predictor_level` uses the full `[0,T]` integrand range, not an endpoint sample. Its residual uses the clip-law Lipschitz and amplitude bounds. `_bound_model_matrices` constructs a Metzler comparison majorant, and `_radius_series` bounds the nonnegative series remainder for any finite positive (T\). The pose/contact and collision sufficient tests are likewise full-hold bounds. The proposed profile keeps the clip law, the R3 distance method, one full-hold cell, and the same formula orders and exact-rational caps. The R3 checker independently reconstructs the relevant proof fields; it will reject an unproved resource `UNKNOWN` as a task success.

No code-level assumption `T <= 0.1` was found in this source-to-bound route. At 0.25 s or 0.5 s, the bounds may be very loose or exceed arithmetic caps. Such outcomes must be recorded as non-success, not treated as unsafety.

**Consequence.** The earlier R3 review was limited to its frozen outputs, but the mathematical route used by the new endpoint bound is not restricted to the archived horizon. This finding does not establish that any new query will complete or certify.

**Status:** VALID conditional route; new-grid outcomes UNVERIFIED.

**Required action:** Bind each future query to the frozen profile and manifest, and require safety and endpoint proof replay before counting it.

## Finding 3 — protocol and exact candidate universe

**Evidence.** Protocol v2 describes one static circle per scene and a non-blind scene-only 400/400 split. It stratifies the fixed 5 cm target by the 0.25 s and 0.5 s horizons. Its selector retains eligible nominal `(1,1)`; a tie with nominal-only is reported as preservation, while a positive paired gain of at least one of 16 held-out groups is the declared improvement criterion. Zero-only task success and unique nonzero safety-certificate coverage have distinct counts. Every invalid, incomplete, resource-limited, `UNKNOWN` and `NOT_RUN` row remains in the fixed denominator. These are finite-grid, synthetic criteria, not statistical generalization or physical relevance.

I read the manifest directly and checked it without invoking its generator: 800 unique IDs; 32 groups of 25 actions; 400 development and 400 held-out rows; 800 `NOT_RUN` rows with null result records. The manifest raw SHA-256 is `28557ddecaf780c02801e872c247f46ff5a2c6b21da587520a82dcf5ab80e69b`; the closure raw SHA-256 is `612e592a263d7788f27f652e9a49683372e86393c2e04a662d8db126a39d8ebd`; the closure binds the same manifest hash. All 34 declared source/input raw hashes matched files in the current working tree at review time. The candidate's 12-label parameter/contact family remains stipulated synthetic data.

**Consequence.** The protocol and static input universe are sufficiently explicit to review. They do not yet define a complete executable, source-bound study.

**Status:** ACCEPT as unfrozen candidates; 800/800 NOT_RUN.

**Required action:** Keep the geometry, threshold, split, action order and denominator fixed in the next candidate version unless a change is declared and reviewed before results are viewed.

## Finding 4 — read-only integrity check can rewrite an input

**Evidence.** `validation/scripts/build_g2_decision_domain_r2_candidate.py::build_manifest()` calls `refresh_specification_bundle(config)` and writes `g2_decision_domain_r2_v1.json` whenever the resulting bytes differ. Its `main()` calls `build_manifest()` before it considers `--check-only`. The source-closure builder also calls `build_manifest()`. Therefore a command presented as a check can mutate the effective configuration before reporting a mismatch. The verified hashes show no current mismatch; the problem is the behavior when one appears.

**Consequence.** Pre-freeze verification is not fail-closed/read-only. Silent repair of an input could obscure what exact bytes were checked. The current manifest/closure should not be frozen on that procedure.

**Status:** BLOCKER for freeze/run; no evidence that the existing R2 artifacts were altered during this review.

**Required action:** Make check and closure-validation modes strictly read-only. On any specification-bundle or source-hash mismatch, return a specific failure without writing. Put intentional regeneration behind an explicit new-version operation, and record before/after hashes. Do not overwrite this reviewed candidate silently.

## Finding 5 — row-to-query and result decision chain is not implemented

**Evidence.** The 800-row manifest contains the needed state, scene, horizon and action data, but `validation/g2/evaluator.py::make_query()` resolves IDs only from the archived `benchmark_v1.json` state/scene/horizon/action lists. The new R2 IDs and 0.25/0.5 s horizons are outside those lists. The protocol defines a selector and paired counts in prose; there is no locked R2 row-to-query constructor, batch/result validator, selector or full-denominator aggregator in the reviewed source closure. Endpoint fixtures consume one archived R3 record and synthetic tube inputs; they do not exercise that new-grid binding path.

**Consequence.** Running the reviewed candidate through `make_query()` is not a defined operation. A later task claim needs a source-bound path that checks each row against the immutable manifest, constructs its exact query, calls the R3 evaluator and both checkers, rejects mismatched identities/hashes, and aggregates all 800 statuses by the declared group/horizon rules. The legacy R3 field `development_manifest_sha256` needs an explicit documented binding to the new frozen manifest; its name alone cannot define that relation.

**Status:** BLOCKER for freeze/run; this is an execution/provenance gap, not a counterexample to the endpoint inequality.

**Required action:** Implement and review the complete offline binding, replay and aggregation path, with non-query or stub-record fixtures for malformed/missing/duplicate rows and denominator preservation. Add every new source to a versioned closure before authorizing any candidate query.

## Finding 6 — timing, usefulness and status

**Evidence.** The 15 s limit is polled internally every 256 metered operations, with no final successful-return deadline check. The protocol correctly calls it cooperative and does not claim a hard process deadline. R3's 748/1,944 `UNKNOWN` results, including 636 negative sufficient contact bounds, justify a material conservative-abstention risk; they do not determine the new 0.25/0.5 s outcomes. No R2 study row, task action or runtime has been measured. The parameter and contact family lacks physical-platform provenance.

**Consequence.** An eventual positive finite-grid result could support only the declared synthetic task comparison. Practical usefulness, online tractability, physical transfer and G2 PASS still require separate evidence.

**Status:** HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.

**Required action:** Report cooperative wall timing honestly; preserve all `UNKNOWN` and failure rows. Do not make task-success, online or physical claims from the candidate alone.

## Final disposition

The R2 endpoint mathematics and corrected protocol are accepted for their exact conditional scope. The **next task is a versioned execution preflight**, not an 800-query run: repair the read-only provenance path, bind each candidate row to an R3 query and endpoint replay, implement the predeclared selector/denominator accounting, and submit the new closure for review. Keep **800/800 NOT_RUN**. No G3, controller, experiment, Auer/G4 change, commit or push follows from this review.
