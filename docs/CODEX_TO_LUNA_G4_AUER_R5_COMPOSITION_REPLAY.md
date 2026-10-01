# Codex to Luna — G4 Auer R5 stored-artifact composition replay

**Date:** 2026-10-01  
**Working folder:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Branch / reviewed HEAD:** `luna/g2-validation-v1` / `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`

The user relays this assignment. Do not commit, push, reset, clean, stash, switch branches, or alter any v8–v10 snapshot or R4 output. Existing scoped offline G2/G4 validation authorization applies. No G3, controller, hardware, physical claim, GO, or gate promotion.

## 1. Read and target

Read `AGENTS.md`, all four canonical `research_context/` files, then:

1. `docs/reviews/CODEX_G4_AUER_R4_IVP_CORE_REVIEW.md`;
2. `docs/reviews/LUNA_TO_CODEX_G4_AUER_R4_IVP_CORE_FULL_HANDOFF.md`;
3. `docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md`;
4. `validation/baselines/auer2013/{residual_ivp.py,replay_ivp.py,r4_worker.py}` and `validation/g4/common_tube.py`;
5. the v10 DDWMR native proof, evidence, selected input, common record, output manifest and source-snapshot manifest.

R4's one native IVP proof and same-worker common predicate are accepted in their restricted scope. The remaining R4 audit gap is that its three composition tamper trials only compare a changed dictionary with an unchanged in-memory dictionary. Create a **standalone, read-only verifier of the stored proof-to-common composition**. This is an artifact-verification task, not another IVP solver or matched comparison.

## 2. Verifier obligation

From explicit file paths, a standalone verifier must read the frozen selected input, benchmark, resource profile, method/arithmetic/source manifests, native proof envelope, R4 evidence/common record, and serialized composition. It must:

1. Check the expected case/query/action, exact file hashes and canonical proof-body digest against the frozen bindings. Verify the v10 snapshot manifest and output-artifact manifest without rewriting either.
2. Call the separate native proof checker on the **stored proof bytes** and reject unless its complete-time 21-coordinate IVP replay succeeds under the declared profile.
3. Reconstruct every common `NATIVE_TOTAL_HULL` segment from the replayed proof's accepted closed slabs, exact physical hulls, endpoints, complete original label image and frozen scene. Enforce radius expansion count zero and exact `[0,T]` coverage.
4. Recompute the collision/contact predicates with the common checker. Compare the complete recomputed record to the **stored** common record, including segment hash, input hashes, exact rational margins, status, and `certificate_emitted=false` / `ode_tube_proof_replayed=false`.
5. Recompute the expected composition record from the proof and recomputed common result. Compare every field to the **stored** composition. Do not use the stored composition itself as the expected value.
6. Emit a small replay report with `PASS` only if every obligation holds; otherwise give the first exact premise mismatch. Distinguish invalid/tampered input, native proof failure, common-predicate mismatch, composition mismatch, and resource limit. The verifier itself emits no safety certificate.

The verifier may reuse the existing native replay and common-predicate arithmetic; disclose that dependency. It must not import the producer or trust the producer's `PROOF_COMPLETE`, common `PASS_ON_SUPPLIED_TUBE`, composition hash, or a prior replay flag without recomputing them.

## 3. Artifact-based mutation checks

Use **copies outside the frozen R4 artifact paths** to demonstrate rejection by the standalone verifier when each of these stored inputs changes:

- native proof total hull, residual iterate, endpoint, proof digest, or action;
- common segment hull, endpoint, radius mode/count, exact margin or segment hash;
- composition proof digest, common-check digest, segment digest, query/action, or source-snapshot digest.

Report each trial's verifier reason. A changed dictionary compared with its original is not sufficient. Keep the copies and trial outputs versioned and hash-bound; preserve the pristine R4 files. Keep the number of cases small and do not rerun the IVP producer merely to exercise this verifier.

## 4. Freeze, scope and handoff

Freeze the new verifier source/profile/protocol in a new versioned snapshot before its replay runs. Preserve every failed attempt, source hash, output hash and resource record. Keep the profile and input semantics fixed. Run only the R4 analytic fixture if needed for verifier wiring and the same preselected DDWMR case. **Do not run any of the 1,944 matched-batch queries.** The matched-batch count remains zero.

Write `docs/reviews/LUNA_TO_CODEX_G4_AUER_R5_COMPOSITION_REPLAY_FULL_HANDOFF.md` with source crosswalk, exact commands, hash ledger, pristine replay report, mutation outcomes, failures, and the remaining scientific limits. Return its absolute path to the user. Do not commit or push.

The project remains **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**. After R5, Codex will prepare a source-backed independent scientific review package before deciding whether a matched comparison may proceed.
