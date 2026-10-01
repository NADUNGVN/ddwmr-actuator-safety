# Codex review — G4 Auer preflight

**Date:** 2026-09-30  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_PREFLIGHT_FULL_HANDOFF.md`  
**Repository / branch / HEAD:** `ddwmr-actuator-safety` / `luna/g2-validation-v1` / `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`  
**Disposition:** **ACCEPT as a partial preflight record; baseline BLOCKED/PARTIAL.** No matched Auer result exists.

MASTER v2.1 remains authoritative. The project stays **HOLD; G1 PASS in restricted reduced-model scope; G2/G3/G4 UNVERIFIED; physical-platform correspondence UNVERIFIED**. This review does not authorize G3, hardware work, or a novelty claim. No commit or push was made.

## 1. Provenance and prepared query universe

**Finding.** The locally frozen preparation artifacts are internally consistent. They do not contain comparison outcomes.

**Evidence.** I independently recomputed SHA-256 and size for all **324/324** source-snapshot members; there were no mismatches. The snapshot manifest hash is `f64ff41901ff99412965785c56bf9abef68b85c5efcf8e8c9dd0ae81e30724b2`, matching its sidecar. The five output hashes listed in `preflight_run_metadata.json` also match their files. The handoff correctly discloses that the current source-audit Markdown was revised after the snapshot; its older version was the hashed snapshot member. This does not alter the recorded preflight run, but the next run needs a new snapshot.

I independently reconstructed the Cartesian benchmark IDs and each query's canonical input SHA-256 from `benchmark_v1.json`. The candidate manifest contains **1,944 unique IDs** in the frozen R2 order, with **zero input-hash mismatches**. All 1,944 statuses are `NOT_RUN`; `comparison_run=false`. Its LF-joined ID digest is `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`.

**Status / consequence.** **VALID preparation and traceability.** This establishes neither an Auer certificate nor a comparative result.

## 2. Isolated mathematics and implementation

**Finding.** The clip specialization is conservative by source inspection for the continuous law `clip(q,-1,1)`. The 21-coordinate right-hand-side adapter has the declared nine physical equations and twelve zero label derivatives. The scalar Eq. (34)–(35) record has the stated arithmetic and narrow scope.

**Evidence.** `piecewise.py` returns derivative interval `{0}` on strictly saturated intervals, `{1}` strictly inside `(-1,1)`, and `[0,1]` at or across either corner. That includes every secant slope of the continuous clip on the interval. `rhs.py` uses the benchmark parameter image through the shared G2 model, applies the common held voltage, and appends `dot(label)=0`; it does not integrate an ODE. The stored preflight report says **20/20** development checks passed, including 212 rational secant pairs. Its own status is `PASS_FOR_CLIP_EXTENSION_AND_SCALAR_REFERENCE_ONLY`. The scalar reference record shows the ordinary enclosure `[-3/2,9/2]` misses the actual `[-1,6]`, while the corrected `[-7/2,29/2]` contains it.

**Limit.** I inspected the source and stored outputs and checked file identities; I did **not** execute the development checks again or prove the future multivariate solver loop. A finite point grid is supporting evidence for the scalar lemma, not a universal proof by itself. The mathematical clip secant argument in the contract supplies the general reason.

**Status / consequence.** **ACCEPT as isolated preflight components.** The scalar formula reproduction is not a solver reference run, a full-time DDWMR tube, or a safety certificate.

## 3. Source fidelity and build blocker

**Finding.** The selected published comparator has not been reproduced. The pinned 2007 `ValEncIA-IVP_0.92_2e.cpp` is a smooth example core and lacks the 2013 piecewise extension. Syntax-only compilation against retrieved headers is insufficient to validate a numerical executable.

**Evidence.** The retained source/readme and audit map the legacy residual functions but identify no 2013 piecewise class. `auer_seed_full_build_disposition_v1.json` says `BLOCKED_BEFORE_LINK`; `baseline_executable_sha256=null`. The locally retrieved PROFIL/BIAS 2.0.8 differs from the seed's named 2.0.2/2.0.4 versions. The Windows x64 UCRT64 target lacks a reviewed directed-rounding configuration, and the available Linux x64 profile has a documented glibc/libm caveat. The syntax-only compiler log is empty with exit code 0; no library link or numerical run occurred.

For environment triage, I checked this laptop read-only: WSL2 Ubuntu launches and has `/usr/bin/g++` and `/usr/bin/make`. The Docker Linux daemon was unavailable. WSL2 is therefore a **candidate build environment**, not a verified interval-arithmetic backend. Rounding behavior, math-library functions, binary compatibility and source fidelity must be checked there before any certificate is accepted.

**Status / consequence.** **BLOCKED** for a source-faithful validated baseline. An unavailable build would be a reproduction limitation, never evidence that R3 is superior.

## 4. Missing full-time proof and common comparison

**Finding.** The decisive validator and checker pieces are still specifications, not executable evidence.

**Evidence.** No DDWMR residual/Picard inclusion has been checked on a complete closed step; no full-step tube, endpoint propagation, Auer adapter, R3 common adapter, or shared collision/contact replay exists. The 2011 VALENCIA paper requires the residual derivative inclusion across the step; iteration count or apparent numerical convergence cannot replace it. The full 1,944-query manifest is preparation-only.

The proposed protocol correctly separates native R3 records from a possible `R3_COMMON_CHECK` series and requires every segment and label cover to pass. One wording issue needs resolution before implementation: the checker description says to test a complete position box and subtract “any declared pose enclosure radius.” If an adapter already expanded that box by its pose radius, subtracting the radius again would count it twice. Define a single canonical representation and an explicit invariant for each adapter. Likewise, binary64 endpoints may enter the rational checker only after their upstream intervals are proven outward and each finite endpoint is converted exactly.

The proposed 0.001 s maximum step and 100-step cap exactly fill a 0.1 s hold at nominal width, leaving no recovery room if inclusion forces subdivision. This is a **resource-design risk**, not a soundness defect; revise or justify the limits before freezing a matched run. All resource exhaustion must remain UNKNOWN.

**Status / consequence.** **UNVERIFIED** full baseline and common comparison. Do not run or characterize the 1,944-query comparison yet.

## 5. Required next work and gate effect

Proceed under the existing scoped offline G2/G4 authorization with the local assignment `docs/CODEX_TO_LUNA_G4_AUER_BASELINE_R2.md`. First establish a reviewed rounding/build route and a source-faithful full-time inclusion implementation. In parallel, make the typed common-checker contract executable and prove that each adapter adds the enclosure radius exactly once. Return all evidence for independent review before the matched batch. If faithful reproduction remains impossible, report the precise blocker and stop that comparator branch without relabeling a custom validator as Auer 2013.

**Final disposition:** The handoff accurately reports useful preparation and an honest blocker. **No Auer/DDWMR baseline result, G4 comparison, G2/G4 gate promotion, or R3 advantage is established.**
