# Codex review — G2 R9 enclosure bottleneck research

**Date:** 2026-10-04  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G2_R9_ENCLOSURE_BOTTLENECK_RESEARCH_FULL_HANDOFF.md`  
**Disposition:** ACCEPT the R6 bottleneck diagnosis and the conditional Picard slab inclusion rule, subject to the proof correction below. ACCEPT R9 only as an offline proof-contract candidate. NO-GO for a new native query or the 800-row study.

## Finding 1 — source and preserved-result identity

**Evidence.** I read `AGENTS.md`, the four canonical `research_context` files, the R8 Codex review, the R9 assignment, the R9 handoff, the R9 source and fixtures, the `ModelIntervals` construction, and the two preserved R6 evaluation records. I independently rehashed the R9 closure: its raw SHA-256 is `2bcb15b82158d01684b8ec043b7279b41e6e95952c6238fb24d2a54f76ec10fa`, and all 149/149 listed path/hash pairs match the current files. The R9 module, fixture JSON and fixture script have the raw hashes reported in the handoff. The two R6 evaluation files still hash to `8d8f48d4c8bd3c6840d09ed32579e3796f81499e58b7a8ed60fba3b825487306` and `d93419ed11d68082c1f6676468326e88e66913d871c8edf1e37f003076686ece`. The R5 manifest has 800 records, all `NOT_RUN`; the R6 summary retains two consumed `VALID_UNKNOWN` rows and a false broader-study trigger.

**Consequence.** The handoff's provenance and no-new-query scope are consistent with the stored artifacts. The four synthetic fixture PASS result is reported in the handoff and supported by inspected fixture source; I did not rerun the fixture script in this review.

**Status:** VALID for the checked identities and preserved accounting.

**Required action:** Keep R5/R6 files and previous R3 source unchanged. Treat the two R6 inputs as observed development cases in any later method revision.

## Finding 2 — exact R6 bottleneck diagnosis

**Evidence.** Reading the serialized rational values as exact fractions, I independently checked the collision identity `margin = distance_lower - 3/50 - E_p` for both rows. For voltage `(0,0)`, the distance lower is `513271/16777216 = 0.0305933356...` m, the pre-error deficit is `-0.0294066644...` m, `E_p = 0.4013160309...` m, and the final lower margin is `-0.4307226952...` m. For `(+1,+1)`, the corresponding values are `303063/16777216 = 0.0180639625...` m, `-0.0419360375...` m, `0.4728212607...` m, and `-0.5147572982...` m. The exact center-hull coordinate gaps are also less than the exclusion radius in both rows. Removing only `E_p` or directed rounding cannot make this same full-hold center-hull test positive.

The records give `beta_L=beta_R=1`, zero certified lateral reserve, and positive demand upper bounds of approximately `3.268571368` N and `4.345042657` N. Their contact lower margins are the negatives of those demands. The stored comparison value is `Q=7/5`; the body radii are approximately `1.422593626` and `1.657660943` in both `u,r` coordinates. The R2 full-hold `u` ranges include negative values, and the exact progress lower values are approximately `-0.377190895` and `-0.439829217` m. The recorded series tail is tiny relative to the forcing and radii. These facts support the handoff's diagnosis of full-hold box/comparison conservatism; they do not isolate every source of that conservatism or characterize the true trajectories.

**Consequence.** The two R6 `UNKNOWN` outcomes result from negative sufficient collision/contact/progress bounds. Neither implies an actual collision, contact failure, or negative displacement. A local-time enclosure is a reasonable research direction, but no improvement on these exact inputs has yet been demonstrated.

**Status:** VALID diagnosis of stored sufficient bounds; usefulness remains UNVERIFIED.

**Required action:** Keep the separate center-hull, pose-error, slip-reserve and body-demand terms visible in future comparisons.

## Finding 3 — conditional Picard slab theorem and proof correction

**Evidence.** The R9 helper computes an interval `G_k` from the declared clip-law `ModelIntervals` image, a candidate internal-state box `B_k`, one held voltage and a parameter image. It checks `X_k subseteq B_k` and `X_k+[0,h_k]G_k subseteq B_k`, then returns `X_k+h_kG_k` as an endpoint outer box. Interval evaluation of the affine part and `C_j clip(S_j z/v_s)` is a sound outer extension when `ModelIntervals` itself encloses every declared fixed parameter label. Using the same outer image on every slab may forget state/parameter correlation and permits an outer switching interpretation, but it still encloses every trajectory with one fixed label.

The handoff's first-exit sentence is not a complete proof: at the first exit time, a continuous solution can be on the boundary of `B_k`, so membership in `B_k` alone is no contradiction. The sufficient inclusion can instead be proved with the Picard operator. For each fixed label and initial `z_0 in X_k`, define `Pz(t)=z_0+integral_0^t f(z(s),V;label) ds` on continuous paths valued in the closed convex box `B_k`. Since `f(B_k,V;label) subseteq G_k` and `X_k+[0,h_k]G_k subseteq B_k`, `P` maps that complete path space into itself. The clip-law vector field is Lipschitz on `B_k`; a sufficiently weighted sup norm makes `P` a contraction. Its unique fixed point remains in `B_k` throughout the closed slab and has endpoint in `X_k+h_kG_k`. This proves the conditional claim without a strict-interior assumption.

**Consequence.** The one-slab inclusion criterion is mathematically sound under the stated model-image and input assumptions, but the handoff's proof text must be corrected before it is used as a theorem statement. The synthetic fixtures exercise only conditional primitives, not the R6 inputs.

**Status:** CONDITIONAL VALID for the one-slab theorem; proof wording requires correction.

**Required action:** Replace the first-exit argument with a complete fixed-point or equivalent continuation argument, and state explicitly that `G_k` must uniformly enclose the exact RHS on `B_k` for every fixed label.

## Finding 4 — R9 is not yet a replayable full-hold certificate

**Evidence.** `verify_pose_contact_slab` checks a supplied dictionary's schema, `PICARD_INCLUSION_PASS` flag, model-image hash, duration and candidate box. It does not recompute the alleged derivative/inclusion from that dictionary. A caller can supply those few matching fields without a genuine Picard computation. The helper also does not bind the proof to the expected voltage, initial internal box or supplied pose-start box, and it does not chain slab endpoints or cover the full `T`. The returned pose/contact report has no complete query/source binding or independent serialized replay contract. The model-image hash identifies the interval image, not by itself the full raw correlated parameter map. The handoff acknowledges that a production input binder, deterministic candidate-box rule, carried chain and full-hold checker are still missing.

**Consequence.** The pose/contact helper is useful for conditional research calculations when fed an authentic result of `verify_internal_slab`. It must not issue a safety certificate from an untrusted serialized proof or be called a complete checker. Neither R6 row has a checked `X+[0,h]G subseteq B` sequence, a local pose/contact chain, or a new terminal progress lower bound.

**Status:** BLOCKER for R9 certificate issuance or query authorization.

**Required action:** Build a versioned whole-hold producer and an independent checker that reconstructs the exact frozen input and recomputes every slab inclusion, carry, pose/contact margin and progress sum. Do not accept a status flag or hash alone as proof.

## Final disposition

R9 is a sound **conditional one-slab research primitive** with a correctable proof presentation and verified source identity. It is not yet evidence that either `(0,0)` or `(+1,+1)` can be certified, and it does not satisfy the decision-relevant G2 usefulness obligation. No new R6/R5 query, stage or gate promotion follows. **HOLD; G1 PASS for restricted reduced-model scope; G2/G3/G4 and physical-platform correspondence UNVERIFIED.** The next assignment is `docs/CODEX_TO_LUNA_G2_R10_WHOLE_HOLD_PICARD_CANDIDATE.md`.
