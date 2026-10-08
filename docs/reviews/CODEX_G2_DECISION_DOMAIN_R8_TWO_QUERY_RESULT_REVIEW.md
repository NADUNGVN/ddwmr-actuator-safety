# Codex review — G2 R8 exact two-query development pilot

**Date:** 2026-10-03  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G2_DECISION_DOMAIN_R8_TWO_QUERY_EXECUTION_FULL_HANDOFF.md`  
**Disposition:** **ACCEPT the two stored `UNKNOWN` outcomes as complete, replayable development-pilot evidence. The usefulness trigger is false. NO-GO to the 800-row study or another native query under this result.**

## Finding 1 — source, authorization, one-shot accounting

**Evidence.** The stored execution receipt still hashes to `eb0ad0dd54554d954ecb6e097277bfc07d131c925777fa9c17931feb48cf0c80`, and the accepted R7 review still hashes to `4348fdd2716e36999a4cafb28369b7f403fe9f262c3f0e07fa092ac64b4431c4`. The publication record hashes to `3e55c3b967b661f3a3c3b5aa70ae4bc7cf8e9bab463ec484a4e5865f3db5b33d`; I independently checked all 12 published payload hashes, with zero mismatches. The read-only stage auditor returned `PASS_READ_ONLY_STAGE_AUDIT`, two attempted rows and two `VALID_UNKNOWN` terminals. The stage summary says `COMPLETED_TWO_ROWS`, two consumed calls and `broader_usefulness_study_trigger=false`. Both row supervisor records say `COMPLETED`, exit code zero, assigned before resume and present in their Windows Job Objects. They report 0.234 seconds each and memory peaks below 30 MiB. No native producer was invoked in this Codex review.

The unchanged R5 manifest hashes to `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b` and still contains exactly 800 `NOT_RUN` records. This is the status of that immutable artifact; two overlapping exact inputs have now been evaluated in the separate R6 development pilot.

**Consequence.** Both authorized pilot attempts are consumed, traceable and independently replayable at the stored-record level. The R6 namespace must not be retried or used as if it were an unrun study.

**Status:** VALID for exact-pilot provenance and publication accounting.

**Required action:** Preserve every R6 artifact and the R5 study manifest byte-for-byte. Record indices 12/24 as development overlap in any later analysis.

## Finding 2 — safety and endpoint outcomes

**Evidence.** I inspected the two `evaluation.json` records and reran the existing read-only stage auditor. Each native R3 status is `UNKNOWN`, each R3 replay is `UNKNOWN` with integrity and proof replay passing, and each R2 endpoint replay is `PROGRESS_BOUND_ONLY_SAFETY_UNKNOWN`. Their R3 reason codes are `CONTACT_SUFFICIENT_MARGIN_NEGATIVE` and `COLLISION_SUFFICIENT_MARGIN_NEGATIVE`. Approximate replayed sufficient values are:

| Held voltage | Collision lower margin | Contact available lower | Contact demand upper | Progress lower | Task eligible |
|---|---:|---:|---:|---:|---|
| `(0,0)` | -0.430723 | 0 | 3.268571 | -0.377191 | No |
| `(+1,+1)` | -0.514757 | 0 | 4.345043 | -0.439829 | No |

Both progress lower bounds are below the fixed `1/20` m threshold. Resource counters and job outcomes show these `UNKNOWN` classifications came from sufficient-bound signs, not a wall, memory or arithmetic-cap stop. The checker shares exact arithmetic and model-construction components with the producer; the replay is a strong stored-proof consistency check, not a wholly independent mathematical derivation of the underlying enclosure.

**Consequence.** The predeclared trigger for a broader voltage-choice usefulness study is false. The more negative positive-voltage sufficient bounds do not rank true trajectories or show actual collision, contact failure or negative progress.

**Status:** VALID `UNKNOWN`/`UNKNOWN` result; practical usefulness remains UNVERIFIED.

**Required action:** Do not characterize either voltage as unsafe or inferior. Do not launch the 800-row study with the current evidence.

## Finding 3 — two distinct enclosure bottlenecks

**Evidence.** The locked geometric test uses inflated obstacle radius `R_s=3/50=0.06` m. Its center-hull minimum-distance lower bounds are approximately 0.030593 m for `(0,0)` and 0.018064 m for `(+1,+1)`. Therefore `d_center_lower-R_s` is already negative by about 0.029407 and 0.041936 m, respectively, **before** subtracting the pose-error budgets `E_p≈0.401316` and `0.472821` m. Tightening only `E_p` cannot make this same center-hull collision test positive. In the contact test both clipped slip bounds are `beta_L=beta_R=1`, so the certified lateral reserve is zero; the positive demand upper bounds then make both contact lower margins negative. The internal comparison radii for body velocity and yaw are approximately 1.423/1.423 and 1.658/1.658, respectively, much larger than the initial body-state widths.

**Consequence.** A useful successor needs a sounder time/geometry enclosure as well as a tighter coupled slip/contact estimate. A change to one scalar remainder alone cannot rescue the present locked sufficient tests. The data do not establish whether a stronger method could certify either true trajectory family.

**Status:** Derived diagnostic from the preserved rational records, not a safety or impossibility theorem.

**Required action:** Before another native query, derive and review a source-backed refinement or a new predeclared development domain. Preserve execution-fixed parameter semantics and expose any correlation lost by outer relaxation.

## Final disposition

**R8 pilot ACCEPTED as two replayable `UNKNOWN` results; usefulness trigger FALSE.** This closes the exact R6 execution obligation and consumes both one-shot calls. The R5 study remains an untouched 800-row candidate, with two logical input overlaps now known from R6. Next assignment: `docs/CODEX_TO_LUNA_G2_R9_ENCLOSURE_BOTTLENECK_RESEARCH.md`; it authorizes proof/source preparation and non-query validation only. **HOLD; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.**
