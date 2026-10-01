# Luna → Codex — G4 Auer R4 IVP core handoff

**Date:** 2026-10-01  
**Branch / base revision:** `luna/g2-validation-v1` / `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`  
**Final source snapshot:** `results/validation/g4/auer2013/source_snapshot_v10`  
**Snapshot manifest SHA-256:** `29ca0f22791ccc740ef377b232522dee88bbaf00367213bfc45cc07925c5bcd5`  
**Output artifact manifest:** `results/validation/g4/auer2013/r4_output_artifact_manifest_v1.json`  
**Output artifact manifest SHA-256:** `6a8d5501972cbb1351cb9ea09500427cb37f8b30c37673ee9e573e156ab6b1a7`

## 1. Disposition

The R4 residual IVP producer and separate native-proof checker are implemented and exercised on the predeclared analytic fixture and the one preselected DDWMR query. Both final v10 runs produced a proof-complete native record, passed independent replay, and remained within the frozen resource limits. The selected DDWMR tube also passed the common collision/contact predicate.

The common result is `PASS_ON_SUPPLIED_TUBE`. The common layer emitted no certificate and did not replay an ODE tube proof itself. This result applies to this one supplied tube; it does not establish physical correspondence or promote a project gate.

The matched 1,944-query batch was not run: **0 matched-query evaluations**. No commit or push was made.

## 2. Frozen inputs and selected query

The conditional DDWMR case was the already selected first query:

```text
query_id: state_low_neg__scene_d020_l-200__T_020__V_m1_m1
T:        1/50 s
voltage:  (-1, -1)
```

The query remains bound to candidate-manifest-v2 input SHA-256 `b59dc0f4bd05bf277384387115e7138d6df6450c187d2eefd38cae577a474e94`, selected-input file SHA-256 `3176cdc76861314cb6aaff1f47304ab61b8fd7040270f0504e45498e05b5bd76`, and benchmark file SHA-256 `b2bc12cd578229cfb6df4b426f93e0f472d69f6be36929df93e797ff79396a9e`. The proof binds the initial nine-state box, all twelve fixed labels, scene, voltage, horizon, method contract, arithmetic manifest, profile, solver/checker sources, and v10 snapshot manifest.

The physical state order is `(p_x, p_y, theta, u, r, omega_L, omega_R, i_L, i_R)`. The twelve declared parameter labels are appended as augmented coordinates with zero derivative. One unchanged full label image and the same held voltage apply over the complete hold.

## 3. Method reconstruction and code crosswalk

This is a **paper-faithful method reconstruction**, not a reproduction of the original VALENCIA binary or application. The implementation specializes Auer's continuous piecewise-smooth method to the benchmark's exact continuous `clip(q,-1,1)` law and uses exact-rational validated arithmetic.

| Published obligation | R4 implementation and check |
|---|---|
| Auer 2013 Eq. (27), scalar expression composition | `validation/baselines/auer2013/rhs.py::augmented_rhs` evaluates the declared nine-state DDWMR RHS over state and label intervals and rejects divisor intervals containing zero. |
| Auer 2013 Eqs. (28), (31), piecewise value/range | `piecewise.py::clip_value` and `clip_interval` retain the unsmoothed continuous clip. |
| Auer 2013 Eqs. (33), (40), generalized derivative | `DualInterval.clip` returns `[0,1]` when an interval touches or crosses either corner, including a singleton corner; it is composed through the normalized slip and the DDWMR RHS. `replay_ivp.py` has its own interval AD and clip derivative implementation. |
| Auer 2013 Eqs. (35)/(41), branch-gap correction | Both clip corners have zero value jump, so the continuous-law correction is exactly zero. No zero-over-switch-distance expression is evaluated. Discontinuous laws are out of scope. |
| Auer 2013 Eq. (42), full-time functional tube | `residual_ivp.py` records the approximate path range, residual range over the complete closed slab, total hull, and separate propagated endpoint. |
| Auer 2013 Eq. (43); Rauh–Auer 2011 Algorithm 1, Eqs. (3)–(6) | Each step computes `D_next = -xdot_app + f(x_app) + J(Q)R_old`, integrates `R_next([0,h]) = R_0 + [0,h]D_next`, and accepts only after componentwise `D_next ⊆ D_old` and induced integrated-tube inclusion pass. |
| Fixed-parameter family | The producer and checker carry all 21 coordinates; all twelve labels retain the same initial intervals and have zero derivatives. Interval boxing may widen through dependency loss, but it cannot narrow or resample labels. |

For each accepted slab, the full-time hull encloses `x_app([t_k,t_{k+1}]) + R([0,h])`. The endpoint is independently propagated as `x_app(h) + R(h)` and becomes the next slab's initial enclosure. The accepted-step rough domain is a compact convex interval box containing the path-plus-residual tube.

`replay_ivp.py` does not import `residual_ivp.py` or `rhs.py`. It independently reconstructs the clip law, DDWMR RHS and 21-coordinate interval Jacobian, residual iterations, integral enclosure, inclusion checks, full-time hull, and endpoint from the frozen input and proof record. Exact-rational interval operations and the Taylor sine/cosine enclosure are shared with `validation.g2`; this is algorithmic replay independence, not an independent arithmetic library.

The pinned VALENCIA 0.92_2e source remains an older smooth double-pendulum seed. Its mean-value routines around source lines 123–227, `MVR_d_R_i` around line 658, and `compute_R` around line 798 are historical implementation context. It contains neither the Auer 2013 clip generalized-derivative extension nor the adopted DDWMR equations. No third-party source was patched.

## 4. Primary-source locators

- E. Auer, S. Kiel, and A. Rauh, “A Verified Method for Solving Piecewise Smooth Initial Value Problems,” *International Journal of Applied Mathematics and Computer Science* 23(4), **731–747** (2013), DOI `10.2478/amcs-2013-0055`. Equations (42)–(43) are on printed p. **742**; §4.1 and piecewise derivative definitions are on pp. 740–742.
- A. Rauh and E. Auer, “Verified Simulation of ODEs and DAEs in ValEncIA-IVP,” *Reliable Computing* 15, **370–381** (2011), DOI `10.1007/s11128-010-0165-6`. Algorithm 1 and Eqs. (3)–(6) are on printed pp. **371–372**.

The retained primary PDFs are under `research/third_party/auer2013/`. Method contract v2 corrects the pagination while leaving frozen `G4_AUER_METHOD_CONTRACT_v1.md` unchanged.

## 5. Analytic branch-crossing fixture

The first final-snapshot run used the predeclared system

```text
x' = 1
y' = clip(x,-1,1)
x(0) in [0.9,0.91], y(0)=0, T=0.2
```

The switch-time interval recomputed from the initial box is `[0.09,0.10]`. The proof has one accepted closed slab, one residual iteration, no rejected attempts, and a passing derivative and integrated-remainder inclusion. The exact reference ranges are contained:

| Quantity | Validated enclosure | Exact reference |
|---|---:|---:|
| Full-time `x` | `[0.9, 1.11]` | `[0.9, 1.11]` |
| Full-time `y` | `[-0.001, 0.1964875]` | `[0, 0.19595]` |
| Endpoint `x(T)` | `[1.10, 1.11]` | `[1.10, 1.11]` |
| Endpoint `y(T)` | `[0.1944875, 0.1964875]` | `[0.195, 0.19595]` |

The native proof reports `PROOF_COMPLETE`; independent replay passes. All seven analytic tamper trials were rejected, including fabricated narrow hull, altered residual iterate, altered switch interval, altered endpoint, changed source binding, changed profile binding, and changed proof digest. Producer/replay/tamper rational work totaled 430 operations; RHS/Jacobian evaluations were zero for this analytic specialization. This is an independent analytic Auer-method fixture, not a reproduction of Auer §5.

Final-snapshot artifacts: `r4_analytic_fixture_native_v2.json`, `r4_analytic_fixture_evidence_v2.json`, `r4_analytic_fixture_resource_guard_v2.json`, and `r4_analytic_fixture_stdout_v2.log`.

## 6. DDWMR proof and common predicate

The v10 native proof covers the complete closed hold `[0,1/50]` in one accepted step, with one Picard iteration and zero rejected attempts. Both inclusion conditions pass. The full-time tube and separately propagated endpoint are shown below as rounded decimal renderings; the native proof file stores exact rational interval endpoints.

| State | Full-time hull on `[0, 0.02]` | Endpoint at `0.02` |
|---|---:|---:|
| `p_x` | `[-0.0117307054, 0.0166306833]` | `[-0.0067307054, 0.0166306833]` |
| `p_y` | `[-0.0106015152, 0.0105865153]` | `[-0.0106015152, 0.0105865153]` |
| `theta` | `[-0.0545960000, 0.0516560000]` | `[-0.0545960000, 0.0486560000]` |
| `u` | `[0.1831149200, 0.3119745800]` | `[0.1831149200, 0.3069745800]` |
| `r` | `[-0.2119366800, -0.0851170200]` | `[-0.2089366800, -0.0851170200]` |
| `omega_L` | `[0.2743606711, 0.5168365489]` | `[0.2743606711, 0.5084365489]` |
| `omega_R` | `[-0.0179699077, 0.2154542127]` | `[-0.0179699077, 0.2133542127]` |
| `i_L` | `[-0.1401417328, 0.1128697328]` | `[-0.1401417328, 0.0848697328]` |
| `i_R` | `[-0.1325795336, 0.1110615336]` | `[-0.1325795336, 0.0890615336]` |

Native status is `PROOF_COMPLETE`; independent replay passes. The seven native tamper trials all reject: fabricated narrow hull, altered residual iterate, altered endpoint, changed action, changed source binding, changed profile binding, and changed proof digest. Three typed-composition tamper trials also reject: altered radius mode, altered segment hull, and altered native-proof digest.

The common collision/contact checker was applied once to the proof-derived `NATIVE_TOTAL_HULL` segment, with zero additional radius expansion. It reports `PASS_ON_SUPPLIED_TUBE`, full closed-hold coverage, a positive collision margin lower bound of approximately `0.0378219547`, and a positive contact margin lower bound of approximately `1.8718095675`. The common record has `certificate_emitted=false` and `ode_tube_proof_replayed=false`; the separate native proof replay remains the evidence for the ODE tube.

Final-snapshot artifacts: `r4_ddwmr_single_query_native_v2.json`, `r4_ddwmr_single_query_evidence_v2.json`, `r4_ddwmr_single_query_resource_guard_v2.json`, and `r4_ddwmr_single_query_stdout_v2.log`.

## 7. Resource accounting

Profile v2 retains the v1 rational bit, operation, time, step, Picard, split, RHS/Jacobian, serialization, and Taylor limits. The v1 profile bytes/hash were preserved (`ab9a842d693862319e91351fae738af67aba0ceb4ea80bf2637d6ce0cadf35c2`). The v2 per-IVP limits include 120 seconds, 1,024 MiB, 32,768 rational bits, 2,000,000 combined rational operations, 512 accepted steps, 1,024 rejected attempts, 16 halvings per attempt, 32 Picard iterations per step, 64 clip splits, 100,000 combined RHS/Jacobian evaluations, and 512 MiB serialized proof size.

| DDWMR stage | Rational operations | RHS/Jacobian evaluations |
|---|---:|---:|
| Producer | 43,917 | 4 |
| Independent native replay | 39,081 | 4 |
| Seven tamper replays | 117,033 | 12 |
| Common predicate | 2,415 | 0 |
| **Combined** | **202,446 / 2,000,000** | **20 / 100,000** |

Maximum observed rational endpoint/intermediate width across the recorded stages was 598 bits, below the 32,768-bit cap. The outer guarded DDWMR worker took about 0.782 seconds and reached 17,805,312 bytes peak process memory, below the 1,073,741,824-byte per-IVP limit.

The Windows Job Object uses `JOB_OBJECT_LIMIT_PROCESS_MEMORY` and `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`. It starts the child suspended, assigns it to the job, installs the cap, then resumes it; the parent enforces the 120-second monotonic deadline and terminates the job on timeout. The final 64 MiB probe requested 256 MiB in retained 1 MiB chunks, reported `MemoryError` after 51,380,224 bytes, and reached a Job Object peak of 66,482,176 bytes under the 67,108,864-byte cap. The guard marked enforcement verified. The worker's expected probe exit code was 23; the guard command itself succeeded.

The first probe used one 256 MiB allocation. Windows rejected that allocation as a whole before peak usage reached the probe's 75% verification threshold. It was recorded as a failed probe, not treated as proof of cap enforcement. The chunked probe was used in v9 and repeated in v10.

## 8. Source snapshots, hashes, and run attempts

All snapshots v8, v9, and v10 remain preserved. The final run used only v10, whose 720 members passed pre-run and post-run integrity verification. Its manifest hash is `29ca0f22791ccc740ef377b232522dee88bbaf00367213bfc45cc07925c5bcd5`; active arithmetic-manifest hash is `254b448b5458fb9f9ebcd84e9a4e03cc7251124d3241ad00f4626aba7bcef085`; active profile hash is `539c59734fb949e4eab2d71ea0761dcd1032bf6ae92fa17fac53e520462a2cc4`. The arithmetic backend uses Python 3.12.12 at `C:/msys64/ucrt64/bin/python.exe`; no native Auer executable was compiled or linked.

The execution log preserves every attempt:

| Attempt | Result | Disposition |
|---|---|---|
| Probe v1, snapshot v8 | Failed verification | One-shot 256 MiB allocation was rejected atomically; measured peak was 14,643,200 bytes, below the required threshold. No IVP ran. |
| Probe v2, snapshot v9 | Pass | Chunked allocation reached 66,207,744 / 67,108,864 bytes; Job Object enforcement verified. |
| Analytic fixture v1, snapshot v9 | Proof complete and replayed | Exact references contained; all seven tamper trials rejected. |
| Selected DDWMR query v1, snapshot v9 | Implementation failure before computation | `_call_rhs()` was called for the approximate path without its required `budget` argument. The worker recorded a `TypeError`; RHS/Jacobian and rational-operation counters were both zero, no native proof file was emitted, and the common checker did not run. |
| Probe v3, snapshot v10 | Pass | Chunked allocation reached 66,482,176 / 67,108,864 bytes; Job Object enforcement verified again. |
| Analytic fixture v2, snapshot v10 | Proof complete and replayed | Exact references contained; all seven tamper trials rejected. |
| Selected DDWMR query v2, snapshot v10 | Proof complete and replayed | One accepted step; common predicate pass on the supplied tube. |

The missing `budget` argument was added before snapshot v10 was frozen. The same already selected DDWMR query was retried; no query was changed or selected from an outcome. Snapshot v10 records two pre-snapshot IVP worker runs (the analytic run and the failed DDWMR wiring attempt), one pre-snapshot DDWMR attempt, two prior memory-probe attempts, zero R3 evaluator reruns, and zero matched-batch evaluations.

`r4_output_artifact_manifest_v1.json` hashes 34 run, guard, integrity, and snapshot-manifest artifacts, including failed attempts. It records the v8, v9, and v10 snapshot manifest hashes. The native DDWMR proof file SHA-256 is `8d394d836c5b92b733403b16b1786cb7fe410ab8fb8610c694c0a7c88e5dde4e`; the canonical proof-body SHA-256 is `4e49a66b69d869758f28ecfdba84eccefde4e38d8a1fa4f70d3c6e3f2701be70`.

Exact PowerShell commands and the frozen execution order are in `validation/baselines/auer2013/R4_EXECUTION_PROTOCOL.md`. Post-run integrity report: `results/validation/g4/auer2013/source_integrity_post_ddwmr_v10.json` (`PASS`, 720/720 members).

## 9. Limits and research status

The arithmetic backend is shared with G2/R3 (`validation.g2.rational`, `validation.g2.interval`, and the Taylor trigonometric enclosure). It is not an independent interval-arithmetic library. PROFIL/BIAS with host `libm` was not used because an all-input directed transcendental error contract remains unresolved. No claim is made that the work reproduces the original VALENCIA binary or Auer §5.

This R4 handoff establishes a reproducible analytic fixture and one proof-backed DDWMR query under the frozen method/profile. It is not a matched performance comparison, recursive safety set, controller or hardware result, or physical validation. Research status remains exactly:

**HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED.**

No commit or push was made. The worktree remains on `luna/g2-validation-v1` at `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`.
