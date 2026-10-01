# G4 Auer matched-comparison protocol — candidate v1

**Date:** 2026-09-30. **Status:** PREPARED FOR REVIEW; NOT LOCKED; no matched outputs.  
**Question:** on the already observed 1,944 synthetic query IDs, does the structure-specific DDWMR enclosure produce a useful certification/width/cost trade-off relative to the Auer–Kiel–Rauh 2013 piecewise-smooth validated-IVP method?

This protocol does not claim held-out data, G4 novelty, G2 acceptance or physical-platform evidence. The input universe is existing development data. The full baseline is not yet built or reviewed; independent review is a prerequisite to running the comparison. No 1,944-query method evaluation was run while preparing this file.

## 1. Input universe and immutable local freeze

The query set is taken from the frozen R2 `original_query_ids` in `results/validation/g2/r2/development_manifest_r2_v1.json` and cross-checked in order against `validation/configs/benchmark_v1.json`:

- 6 nonzero-width, nine-state initial cells;
- 12 static-obstacle scenes;
- 3 fixed hold durations;
- 9 constant voltage actions;
- 1 complete 12-label parameter image per query;
- `6×12×3×9 = 1,944` original state/scene/horizon/action IDs.

The generated Auer candidate manifest includes all IDs in the exact R2 order, a SHA-256 for each canonical query input, and `NOT_RUN` for every Auer status. It includes no R3 result join and no evaluator output. The manifest status is preparation-only and not locked. The configuration and ID digests are recorded within the manifest.

For any later run, copy code, transitive shared arithmetic/model/checker dependencies, configuration, protocol, source snapshots, and license/terms files into a new versioned local snapshot. Hash each member and the manifest; identify `LOCAL_UNCOMMITTED_SNAPSHOT`, base Git revision, snapshot hash, command, environment, source/runtime/binary hashes. Hash executed source and input members immediately before and after. A changed source creates a new snapshot and output directory. The project is intentionally uncommitted; Git cleanliness is not claimed.

## 2. Scientific problem and common representation

Both methods must receive the exact same nine physical equations from MASTER v2.1 with `phi(q)=clip(q,-1,1)`, identical initial state box, full parameter-label image, common held voltage, horizon, obstacle and SI scales. Add the same twelve label coordinates with exact `dot(xi)=0`; they are fixed unknown parameters over the whole hold. No method may resample labels, select a favorable label, switch parameter values, alter voltage within a hold, smooth clip, add contact projection, differentiate the contact square root, or differentiate the contact predicate as part of the ODE.

Declare a typed `TubeSegment` adapter with:

- closed rational time interval `[t_a,t_b]`, preserving coverage at every boundary;
- interval hulls for physical `[p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R]`;
- unchanged fixed-label hulls in the same 12-coordinate order;
- per-coordinate center, radius, and total hull width fields where the native method provides them;
- provenance to the method-native segment and exact endpoint object.

**Auer adapter:** enclose every validated VALENCIA segment `x̃(t)+R(t)` over its full closed step. If the library outputs only samples, the full-step interpolation/error contract must be implemented and audited before use. Hull all segments for full-hold metrics; separately retain endpoint `t=T`.

**R3 adapter:** reconstruct the native center interval plus its error radius exactly once. Do not subtract or add the radius twice. Preserve all original R3 outputs. If a common checker or representation changes a result, create a distinct `R3_COMMON_CHECK` series, never overwrite R3 native records.

Convert each binary64 outward endpoint from Auer to its exact binary rational representation before the common checker. The common checker then uses the existing exact-rational interval primitives. This places the final geometry/contact predicates on one outward arithmetic layer; it does not erase upstream solver differences.

## 3. Common full-time checker

For each complete segment and each fixed-label cover cell, run the same collision and contact sufficient checks on the full segment state enclosure:

1. collision: a lower distance bound from each obstacle center to the complete position box, minus inflated radius and any declared pose enclosure radius;
2. contact: the existing algebraic capacity-reserve lower bound against the upper bound on `|m u r|`, using exact clip range and the same parameter-image cover;
3. any endpoint predicate, if later requested, is separately labeled and cannot substitute for checks on every closed interval.

The Auer-to-common and R3-to-common adapters, typed segment schema, and shared checker still require implementation/review. Until then the protocol has a precise checker target, not verified common-checker evidence. Separate enclosure-only status, checker-inclusive status, and total cost in any eventual report.

## 4. Candidate Auer integration profile and resources

Proposed settings are in the candidate manifest and require independent review before freeze:

| Resource | Candidate limit / rule |
|---|---|
| Maximum step width | `0.001 s`, matching the step size reported for the §5 paper simulation; its transfer to the DDWMR family must be tested through the actual inclusion condition. Steps are proof subdivisions, never control updates. |
| Maximum steps | 100/query, enough for the benchmark's maximum 0.1 s horizon at the candidate width. |
| Piecewise range splits | At most 10 per component/step, matching the legacy core's `Max_split_calc=10` as a starting point. |
| Reinitialization/iteration recovery | At most 5 attempts/step, matching legacy `number_rep_max=5`; these attempts do not waive inclusion. |
| Function + Jacobian work | At most 1,000,000 calls/query, instrumented in the adapter. |
| Wall time | 15 s/query, same external wall cap as R3. Timeout is UNKNOWN or separately reported implementation failure; never CERTIFIED. |
| Peak resident memory | 512 MiB/query. |
| Arithmetic | IEEE-754 binary64 interval endpoints with proven PROFIL/BIAS directed rounding; nominal significand precision 53 bits. Reject a build/runtime for which the directed-rounding contract or libm caveats are unresolved. |
| Compiler target | Candidate `-O2 -frounding-math -fno-fast-math -ffp-contract=off`; record actual GCC, target triple, flags, runtime, architecture and rounding-mode checks. The unsupported MSYS2 build is not an allowed result backend. |
| Solver counters | RHS calls, Jacobian calls, accepted/rejected steps, Picard iterations, branch range evaluations/splits, arithmetic exception count, step segments, solver CPU/wall time, peak memory. |
| Checker counters | Exact rational operations/bits and checker CPU/wall time, recorded separately from solver work. |

R3 keeps its frozen 16,384 rational-bit cap, 1,000,000 rational-operation cap and 15 s/query wall cap. These primitive budgets are not numerically equal to Auer's binary64 work count. Report each method's native work vector and separate measured cost; do not call unlike primitive counts “equal work.” A 512 MiB per-query ceiling applies to both comparison workers.

The above values remain proposed because the original software does not compile/run on the current supported target. Any changed setting must produce a new protocol version before comparison outputs. No selected DDWMR statuses may tune the method.

## 5. Outcomes, aggregation and widths

Keep every original query ID in the denominator. For each ID report `CERTIFIED`, proof-complete `UNKNOWN`, resource `UNKNOWN`, `INVALID_INPUT`, or implementation failure as separate classes. A `CERTIFIED` result requires every state/label cell, every obstacle, and every closed segment to pass the common checker. A nonnegative endpoint result alone is insufficient. Any unresolved valid segment/cell makes the original query UNKNOWN.

Report per ID: lower collision/contact margins; parameter/time covers; center hull widths; error radii; total full-hold hull widths; endpoint widths separately; solver and checker work vectors; termination reason. If the native method uses multiple segments, full-hold width is the hull width over all segments, while endpoint width uses only the closed final endpoint. Do not compare sample counts from unlike partitions as if they were independent observations.

Report per group the entire nine-action vector, any certified zero action, and all-action-UNKNOWN counts. Coverage and width/cost trade-offs are shown across the predeclared strata. Do not assume statistical independence between scene, state and horizon cells. Do not choose a post-hoc scalar winner. If reproduced Auer matches or dominates R3 on this domain, report no demonstrated DDWMR advantage. Failure to build or lack of applicability is a reproduction limitation, not evidence for R3 superiority.

## 6. Falsification and lock gate

Before the matched run, an independent reviewer must audit (i) the full piecewise derivative and multivariate mean-value inclusion, (ii) VALENCIA residual/Picard inclusion and full-step tube, (iii) arithmetic rounding/build assumptions, (iv) nine-state/12-label fixed-parameter map, and (v) the common checker/adapters. Auer's §5 numeric reference should be reproduced from authoritative data or explicitly marked unavailable; no reversed interval may be silently repaired.

The current candidate manifest and this protocol are **not locked**. They can be independently reviewed as preparation artifacts. The 1,944-query baseline run remains prohibited by the requested stop condition until the independent baseline review is returned and the user reissues/continues the comparison phase.

