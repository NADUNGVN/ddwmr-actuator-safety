# G4 Auer matched-comparison protocol — candidate v2

**Date:** 2026-09-30. **Status:** PREPARATION ONLY; NOT LOCKED; no matched outputs.  
**Disposition:** `BLOCKED/PARTIAL` pending a source-faithful validated-IVP solver and independent review.

This version replaces the v1 resource draft for future review. It does not change MASTER v2.1 or any gate. The 1,944-query comparison remains unrun and must not start from this preparation package.

## 1. Input universe and stop condition

The candidate manifest v2 preserves the frozen R2 `original_query_ids` in order: 6 nonzero-width nine-state initial cells × 12 static-obstacle scenes × 3 hold durations × 9 voltage actions = **1,944 unique IDs**. Its LF-joined ID digest is `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`. Each row remains `NOT_RUN`; `comparison_run=false`; no R3 result is joined.

The manifest records a proposed cap of 1,000 steps/query. The 0.1 s maximum hold needs at least 100 steps if every accepted step has width at most 0.001 s. A 1,000-step cap therefore permits up to tenfold subdivision relative to that starting width. This is resource headroom, not evidence that the inclusion converges or that the cap is adequate. The profile is unapproved until an actual solver and its inclusion costs are reviewed.

## 2. Shared input and tube representation

Both methods must use the same MASTER v2.1 nine-state equations, one common held voltage, the same initial cell and complete 12-label parameter image. The labels are execution-fixed across the entire hold; an analytical augmentation uses `dot(label)=0`. No label resampling or switching is allowed.

The common interface is `validation.g4.common_tube.TubeSegment` (`ddwmr-g4-full-time-tube-segment-v1`):

- exact rational closed time boundaries covering every point of `[0,T]`, with adjacent slabs sharing the same exact boundary;
- a total nine-state interval hull for the entire closed slab, in `[p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R]` order;
- all 12 fixed-label intervals, in the benchmark's canonical order and equal to the full declared image on every slab;
- separate start/end endpoint hulls contained in the slab hull, with adjacent endpoint hulls equal at a shared boundary;
- native proof provenance and an expansion mode/count.

The collision checker consumes the total state hull. A native total hull has expansion count 0. A center plus radius/residual adapter expands once and records count 1. The checker never expands a radius. Every finite binary64 Auer state bound is converted from its hexadecimal float representation to the exact rational represented by that float; this preserves the float exactly but does not prove that upstream rounding was outward.

The Auer adapter schema requires full-step `x_app_step_range_hex` and `residual_step_range_hex`; their interval sum forms the total slab hull. Endpoint-only samples do not satisfy the schema. The adapter requires a proof-record digest for provenance but **does not replay or validate that proof**. It cannot produce a certificate until a separately reviewed Auer proof checker establishes the upstream outward bounds and residual inclusion.

R3 adaptation replays its native record before applying its stored radius once. Any result produced through the shared representation must be labeled `R3_COMMON_CHECK`; original R3 outputs remain untouched.

## 3. Common predicates and current fixture evidence

The common checker runs on every closed slab, including common boundaries, and every obstacle in the scene. It computes an outward rational lower distance from the complete position box to each obstacle center and subtracts the obstacle exclusion radius. Its contact predicate uses the exact clip value interval, lower capacity reserves, and an upper bound on `|m u r|`. It requires the full parameter-label image on every slab. A nonnegative result is named `PASS_ON_SUPPLIED_TUBE`; a negative or inconclusive supplied hull is `UNKNOWN_ON_SUPPLIED_TUBE`. The checker always emits `certificate_emitted=false` and `ode_tube_proof_replayed=false`.

The replayable v2 preflight has nine synthetic interface checks, including a positive two-slab fixture, a full-time hull that crosses an obstacle while both endpoint boxes are clear, a rejected coverage gap, a rejected label change, one-time radius expansion, exact binary64-to-rational conversion, a saturated clip corner, and rejection of a tampered enclosure. These are interface fixtures only: not ODE trajectories, not benchmark evaluations, and not safety certificates. They do not test tampering with an Auer inclusion proof because no such proof checker exists yet.

## 4. Proposed resource profile

| Resource | Candidate setting, pending review |
|---|---|
| Maximum accepted step width | 0.001 s; adaptive proof subdivision, not a control update |
| Maximum steps | 1,000/query; proposed tenfold subdivision allowance for the 0.1 s maximum hold |
| Piecewise range splits | 10/component/step, inherited as a starting point from legacy `Max_split_calc=10` |
| Inclusion recovery attempts | 5/step, inherited as a starting point from legacy `number_rep_max=5`; retries never waive inclusion |
| RHS plus Jacobian calls | 1,000,000/query |
| Wall time | 15 s/query |
| Peak memory | 512 MiB/query |
| Candidate runtime | WSL2 Ubuntu 24.04 x86-64; GCC 13.3; glibc 2.39; local PROFIL/BIAS 2.0.8 build |
| Candidate compile flags | `-O2 -frounding-math -fno-fast-math -ffp-contract=off`; record actual compile and link commands |
| Failure | Failed inclusion, invalid arithmetic, unsupported input, or exhausted work is `UNKNOWN` or a separately named implementation failure, never `CERTIFIED` |

The candidate PROFIL/BIAS build and finite directed-rounding probes are recorded in the R2 handoff. PROFIL/BIAS 2.0.8 is newer than the pinned seed's documented 2.0.2/2.0.4. Its x86-64 profile documents a glibc/libm caveat. The finite probes do not establish a global libm error bound, so this runtime remains **not approved for certificate output**. Any solver must validate every transcendental operation it actually uses. The WSL build is not itself an Auer baseline.

R3 retains the frozen 16,384-bit and 1,000,000 rational-operation primitive budgets and 15 s/query wall cap. Report each method's native work vector and checker cost separately; these unlike arithmetic counters are not equal-work units. Apply the 512 MiB/query ceiling to both workers if a future comparison is authorized.

## 5. Proof record and acceptance contract

Every future Auer step must carry replayable source-native evidence for the rough domain, approximate path, interval RHS/Jacobian, residual derivative ranges, every Picard iterate, the verified residual inclusion, the full-time `x_app(t)+R(t)` enclosure, and the propagated endpoint. A checker must recompute inclusion premises from frozen inputs rather than trusting a solver Boolean. The common checker verifies only coverage, representation and collision/contact predicates on the supplied hull; it does not establish an ODE solution or the Auer fixed-point theorem's hypotheses.

Before any comparison, independent review must accept (i) source fidelity of the piecewise derivative in the interval mean-value/Jacobian calculation, (ii) the replay checker and full-step tube, (iii) arithmetic and libm soundness, (iv) the nine-state/twelve-fixed-label map, (v) both common adapters and predicates, and (vi) small positive and UNKNOWN reference cases. The current package does not meet this gate.

## 6. Reporting and protocol status

Keep all 1,944 IDs in the denominator of any future report. Separate proof-complete UNKNOWN, resource UNKNOWN, invalid input, and implementation failure. Record full-time and endpoint widths separately, all collision/contact margins, solver counters, exact-rational checker operations/bits, and per-query termination. Do not interpret failure to reproduce Auer as evidence for R3 superiority.

**Current status:** not locked; not executable as a validated baseline; **matched query evaluations = 0**. Revisit this protocol only in a new version after source-fidelity and soundness review.
