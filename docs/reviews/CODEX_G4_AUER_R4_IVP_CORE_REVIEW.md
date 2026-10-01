# Codex review — G4 Auer R4 residual IVP core

**Date:** 2026-10-01  
**Repository / branch:** `ddwmr-actuator-safety` / `luna/g2-validation-v1`  
**Reviewed HEAD:** `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`  
**Source snapshot:** `results/validation/g4/auer2013/source_snapshot_v10`  
**Snapshot manifest SHA-256:** `29ca0f22791ccc740ef377b232522dee88bbaf00367213bfc45cc07925c5bcd5`  
**R4 handoff:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_R4_IVP_CORE_FULL_HANDOFF.md`

MASTER v2.1 is authoritative. This review is a source and artifact audit of the two frozen R4 cases, not a new IVP run or a matched-batch comparison. I did not run the producer, native checker, common checker, tamper suite, or 1,944-query batch. The user mediates Luna/GPT work on this laptop; no commit, push, cleanup, branch switch, gate edit, or MASTER edit was made.

## Disposition

**ACCEPT in the restricted R4 sense:** the analytic branch-crossing fixture and the preselected DDWMR query contain complete, replayed native residual-IVP records under the frozen v10 source/profile. The DDWMR full-time hull was passed to the common collision/contact predicate in the same guarded worker after native replay; the stored common result is `PASS_ON_SUPPLIED_TUBE` with positive rational margins. This is one proof-backed synthetic DDWMR case, not a 1,944-query Auer comparison.

**QUALIFY the composition claim:** the three reported “composition tamper” checks do not provide an independent, persistent proof-to-common verifier. They compare modified in-memory dictionaries to the unchanged original dictionary. The real worker control flow does link a successfully replayed frozen proof to the common check, but a later reader cannot yet replay the stored proof, segment adaptation, common record, and composition as one checked artifact.

**Research status remains:** **HOLD; G1 PASS only for the restricted reduced model; G2/G3/G4 UNVERIFIED; physical-platform correspondence UNVERIFIED.** No G3, operational implementation, physical-safety claim, or GO follows.

## 1. Frozen artifacts and exact case identity

**Finding.** The reviewed files are internally bound and present. The DDWMR case is the previously selected first candidate, not an outcome-based replacement.

**Evidence.** I independently recomputed file hashes and sizes for all **720/720** v10 snapshot members and all **34/34** output-manifest artifacts; no mismatch was found. The snapshot-manifest hash and output-manifest hash match the handoff (`6a8d5501972cbb1351cb9ea09500427cb37f8b30c37673ee9e573e156ab6b1a7` for the latter). The DDWMR native file hash is `8d394d836c5b92b733403b16b1786cb7fe410ab8fb8610c694c0a7c88e5dde4e`. The selected input file hash is `3176cdc76861314cb6aaff1f47304ab61b8fd7040270f0504e45498e05b5bd76`. Its `query_id` and candidate input hash equal the first row of the frozen 1,944-row candidate manifest: `state_low_neg__scene_d020_l-200__T_020__V_m1_m1` and `b59dc0f4bd05bf277384387115e7138d6df6450c187d2eefd38cae577a474e94`. The output manifest records zero matched-batch evaluations and preserves the failed v9 attempt.

**Consequence.** The reported v10 evidence has a checkable source/output identity. One selected DDWMR IVP run occurred; **0/1,944 matched-batch evaluations** occurred.

**Status:** VALID for artifact integrity and selection identity.

**Required action:** Preserve v8–v10 snapshots, failed attempts, and output hashes. Do not describe this as a completed matched comparison.

## 2. Residual inclusion and fixed parameter semantics

**Finding.** The accepted-step inclusion has a sound mathematical route for this continuous clip-law IVP, subject to the stated exact-rational and Taylor enclosure primitives.

**Evidence.** The producer forms a 21-coordinate augmented system: nine physical states plus all twelve parameter labels with zero derivative. Its linear DDWMR approximate path uses constant labels at their midpoints, while the initial residual label intervals recover the complete original label image. On the closed slab, it computes

\[
R_{\mathrm{old}}=R_0+[0,h]D_{\mathrm{old}},\qquad
Q=x_{\mathrm{app}}([0,h])+R_{\mathrm{old}},
\]

\[
D_{\mathrm{new}}=f(x_{\mathrm{app}}([0,h]))-\dot x_{\mathrm{app}}
 +J(Q)R_{\mathrm{old}}.
\]

The accepted step requires both componentwise `D_new ⊆ D_old` and `R_0+[0,h]D_new ⊆ R_old`. Because `Q` is a convex interval box containing each segment from the approximate path to any path in the rough tube, the generalized Jacobian enclosure bounds the componentwise secants of the locally Lipschitz vector field. The continuous `clip(q,-1,1)` has derivative hull `{0}`, `{1}`, or `[0,1]` as appropriate at the two corners; no discontinuity jump exists. The validated Picard image lies inside the rough tube. The exact fixed-label coordinates have zero derivative and their endpoint intervals are checked unchanged. This encloses the formal ODE family with one execution-fixed label vector, while interval dependency loss may widen the result.

`replay_ivp.py` separately rebuilds the DDWMR RHS, 21-by-21 interval AD Jacobian, residual iterates, both inclusions, total full-time hull, and endpoint. It does not import the producer's `residual_ivp.py` or `rhs.py`. It does share `validation.g2` rational intervals and Taylor sine/cosine, as disclosed. The stored DDWMR step has one accepted closed interval `[0,1/50]`, one residual iteration, both inclusion flags true, zero rejected steps, and `PROOF_COMPLETE`; native replay reports `replayed=true`.

**Consequence.** The native record supports a complete-time **formal reduced-model** enclosure for this one frozen state/action/parameter box. Replay independence is algorithmic, not independent arithmetic implementation or a formal proof of the shared arithmetic source.

**Status:** VALID in the restricted single-case scope on source-level review.

**Required action:** Preserve the complete 21-coordinate proof and its independent replay. State the shared arithmetic dependency in any later comparison.

## 3. Analytic crossing fixture

**Finding.** The fixture is a genuine branch crossing with a correct exact reference.

**Evidence.** For `x'=1`, `y'=clip(x,-1,1)`, `x(0)∈[0.9,0.91]`, `y(0)=0`, and `T=0.2`, the switch time is `[0.09,0.10]`. Direct integration gives `x(T)∈[1.10,1.11]` and `y(T)∈[0.195,0.19595]`. The chosen midpoint path has `x_mid=0.905`, switch time `0.095`, and `y_app(T)=0.1954875`. Its `y_app` is continuously differentiable at the switch and its derivative equals `clip(x_app)` on both pieces. With initial `x` error `[-0.005,0.005]`, the accepted generalized-Jacobian correction gives `y` derivative residual inside `[-0.005,0.005]`, contained in the seed `[-1,1]`. The stored full-time hull `[0.9,1.11]×[-0.001,0.1964875]` and endpoint `[1.10,1.11]×[0.1944875,0.1964875]` contain the exact references. Native replay and seven native tamper trials report success/rejection as declared.

**Consequence.** The analytic fixture meets the prerequisite for attempting the selected DDWMR case. It does not reproduce Auer §5.

**Status:** VALID.

**Required action:** Keep the “independent analytic Auer-method fixture” label.

## 4. Common collision/contact predicate and composition

**Finding.** The common predicate calculation is applied to a proof-derived total hull **within the R4 worker**, after successful native replay, with no second radius expansion. The serialized composition is not yet independently replayable as a whole.

**Evidence.** `r4_worker.py` reads the native proof bytes back from disk, calls `replay_native_proof`, and exits on replay failure. Only after a successful replay does `_common_check` construct each `TubeSegment` directly from that frozen envelope's `full_time_total_hull_augmented`, `endpoint_start_augmented`, and `endpoint_end_augmented`. It sets `NATIVE_TOTAL_HULL` and expansion count zero. `check_tube_segments` verifies complete closed-hold coverage, unchanged full label intervals, endpoint inclusion and collision/contact margins. The stored exact collision lower margin has positive numerator `3217536069938172178905080151780338213` and denominator `85070591730234615865843651857942052864`; the contact lower margin has positive numerator `97189909371752867237790996600749227846061205518751` and denominator `51922968585348276285304963292200960000000000000000`. The common layer correctly records `certificate_emitted=false` and `ode_tube_proof_replayed=false`.

However, `_composition_valid(composition, expected)` is only `composition == expected`. The three “composition tamper” trials mutate a copy and compare it with the original in memory. They demonstrate that unequal dictionaries compare unequal; they do not read the stored native proof and common record, rerun native proof replay, derive the segment anew, recompute the predicate, and verify the serialized composition bindings. The existing `replay_common_check_record` can replay a supplied common result in isolation, but it does not bind that result to the native proof.

**Consequence.** The **runtime linkage in this specific guarded worker is supported** by the control flow and hashes. The claim of an independently replayable combined proof/predicate artifact remains **UNVERIFIED**. The three composition tamper counts should not be presented as strong independent binding evidence.

**Status:** VALID for same-worker proof-derived predicate; PARTIAL for persistent proof-to-common composition replay.

**Required action:** Before a matched batch or scientific comparison claim, add a standalone read-only composition verifier. It should load the frozen input, native proof, common result and composition from disk; verify file/digest/source/profile bindings; replay the native proof; reconstruct `NATIVE_TOTAL_HULL` segments from the replayed proof; replay/recompute the common predicate; and compare every serialized composition field. Tamper checks must invoke that verifier on altered **stored artifacts** and reject with a specific premise mismatch. Preserve R4 artifacts unchanged.

## 5. Resources and source fidelity

**Finding.** The reported R4 runs stayed within the frozen profile and are appropriately labeled as a published-method reconstruction.

**Evidence.** The DDWMR evidence records 43,917 producer, 39,081 native replay, 117,033 tamper replay, and 2,415 common-predicate rational operations, totaling **202,446 / 2,000,000**; RHS/Jacobian evaluations total **20 / 100,000**. Maximum recorded rational width is 598 bits versus 32,768. The guarded worker reports about 0.782 s wall time and 17,805,312 bytes peak process memory versus a 1,024 MiB process cap. The v10 memory probe reports cap enforcement; the failed one-shot v8 probe and failed v9 DDWMR wiring attempt are retained. The process runner creates the child suspended, assigns the Windows Job Object with a process-memory limit, then resumes it and enforces a monotonic deadline. The source contract identifies Auer 2013 Eqs. (42)–(43) and Rauh–Auer 2011 Algorithm 1 as the method basis while distinguishing this exact-rational reconstruction from original VALENCIA software.

**Consequence.** The small-case resource evidence is usable for this one case. It says nothing about 1,944-query throughput or method superiority.

**Status:** VALID for the reported scoped run; matched-batch tractability UNVERIFIED.

**Required action:** Retain all guard and failure records. Do not infer whole-grid runtime from this case.

## Next research decision

The immediate technical obligation is a standalone proof-to-common artifact verifier and its independent review. Then request a source-level scientific review of the frozen Auer reconstruction, input matching and proof theorem before authorizing any matched 1,944-query run. A local path or summary alone is insufficient for an external reviewer who cannot access this uncommitted working tree; provide the actual source, contracts, input and proof artifacts or a hash-bound review bundle. Keep matched protocol, inputs, profile and method identity fixed during that review.

No generic-method novelty claim follows from R4. G4 still requires a matched-assumption, proof-backed comparison against the G2/R3 method, including inconclusive results and resource use. The current project status remains **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**.
