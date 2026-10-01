# Codex review — G4 Auer R3 proof-backed single-case package

**Date:** 2026-09-30  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_R3_PROOF_BACKED_SINGLE_CASE_FULL_HANDOFF.md`  
**Branch / HEAD:** `luna/g2-validation-v1` / `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`  
**Disposition:** **PARTIAL. Accept the archived R3 adapter evidence within its scope; Auer single-case objective remains incomplete.**

MASTER v2.1 remains authoritative. **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical-platform correspondence UNVERIFIED.** No commit or push was made during this review.

## 1. Artifact integrity

**Finding.** The submitted files are present and internally traceable.

**Evidence.** I recomputed the handoff SHA-256 as `dc2c9ef5836c5fac10bf9869ee68b6a5be1c5088fde622b7143916e34a415978`. I independently recomputed the size and SHA-256 of all **703/703** files listed in `source_snapshot_v7/snapshot_manifest.json`, with no mismatches; its manifest hash `9bbb2462723d4ac4e8f37078689158e3653de9cf4c1071c75cd7833c97540e07` matches the sidecar. The hashes of the method, arithmetic, resource-profile, selection, adapter-output and archived-fixture runner files match those listed in the handoff. Git still shows local untracked work; HEAD is unchanged.

**Status.** **VALID provenance for this local package.** Hash agreement is not a proof of solver correctness.

## 2. Auer branch status

**Finding.** No Auer IVP was attempted. The analytic fixture and selected DDWMR query remain without a full-time tube, endpoint or native inclusion proof.

**Evidence.** The blocker record says `analytic_fixture.run_attempted=false` and `selected_ddwmr_query.run_attempted=false`. The method contract identifies absent residual/Picard producer, native step-record writer and replay checker; the pinned smooth VALENCIA seed is not a 2013 piecewise DDWMR solver. The resource profile also lacks process-level enforcement of its 1,024 MiB memory cap. No Auer comparison query was evaluated.

**Consequence.** `BLOCKED_BEFORE_IVP` is accurate as a **package execution state**. The missing producer/checker is the implementation task assigned in R3; its absence is not a failed inclusion test, proof that Auer cannot work, or an external scientific obstruction. The next engineering step is to implement and audit that path, not another contract-only preflight. Failure of a concrete implementation attempt should name the exact mathematical or resource premise that failed.

**Status.** **Auer objective incomplete; feasibility UNVERIFIED.** No Auer/R3 matched conclusion follows.

## 3. Arithmetic and source-fidelity boundary

**Finding.** Exact-rational interval arithmetic is a plausible way to avoid the unresolved PROFIL/BIAS/glibc-libm path, but the current arithmetic document only specifies available primitives. It has not established the complete Auer solver.

**Evidence.** `ARITHMETIC_BACKEND.md` names exact `Fraction` intervals, rational Taylor sine/cosine and exponential bounds, and rational square-root bracketing. These are shared with the G2/R3 implementation, so the future comparator must report that common arithmetic dependency. The documented Auer-specific residual operator, generalized-derivative use inside that operator, full-step inclusion and independent replay are still absent. There is no original VALENCIA software reproduction.

The frozen method contract gives Auer 2013 pages `739–750` and Rauh–Auer 2011 pages `371–382`, whereas the earlier source audit and GPT review cite `731–747` and `370–381`. Check the primary PDF pagination and correct these bibliographic locators in a **new version** of the contract. Do not alter the hashed frozen v1 contract in place.

**Status.** **Candidate arithmetic contract only; method fidelity and end-to-end soundness UNVERIFIED.**

## 4. Archived R3 adapter fixture

**Finding.** The new historical R3 adapter work fulfills a separate, useful interface obligation. It remains R3 evidence, not an Auer result.

**Evidence.** The selection stage binds the first replayable proof in frozen continuation order to the archived record, manifest, input digest and source snapshot before common checking. Source inspection shows the adapter reruns `replay_record`, constructs one full-hold total hull with `CENTER_PLUS_RADIUS_ONCE`, and recomputes the common predicate. The stored output reports native `CERTIFIED` with collision margin about `0.0378849178 m` and contact margin about `1.8380586883 N`. The common supplied-hull check reports `PASS_ON_SUPPLIED_TUBE` with collision margin about `0.0377610922 m` and the same contact margin. Its record sets `certificate_emitted=false` and `ode_tube_proof_replayed=false`; the separate composition replay is recorded as passing. Five altered composition fields are recorded as rejected.

I checked the file hashes, parsed the machine-readable result and inspected the selection/composition source. I did **not** execute the native/common checker again in this review. The R3 arithmetic and source dependencies are shared, not independent arithmetic implementations. The `Budget` work counters are reset between adapter conversion and common checking to report those phases separately; future cost comparisons must include both phases and the native proof replay.

**Status.** **ACCEPT as reported archived R3 interface evidence with the stated replay/provenance limits.** It does not close Auer source fidelity, G4 novelty, or practical usefulness.

## 5. Required next action

Use the local assignment `docs/CODEX_TO_LUNA_G4_AUER_R4_IVP_CORE.md`. It focuses on implementing the published residual inclusion and replay path, first for the exact two-state branch-crossing fixture, then for the already selected DDWMR query if the fixture is proof-complete. The archived R3 adapter need not be rebuilt. Freeze a profile with enforceable limits before executing either IVP; preserve the existing v1 profile and every prior attempt. If implementation cannot reach a proof-complete fixture, return the concrete attempted inclusion and failed premise, rather than citing the absence of a solver again.

**Final disposition:** R3 handoff is honest and hash-bound, with one archived R3 interface fixture completed. The central Auer proof-backed single-case milestone remains **UNVERIFIED**; **0/1,944** matched Auer queries were run. Project status remains **HOLD**.
