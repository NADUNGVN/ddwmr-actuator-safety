# G4 Auer R5 stored-artifact composition replay protocol

**Status:** Frozen before the first R5 verifier replay  
**Scope:** The single R4 DDWMR case state_low_neg__scene_d020_l-200__T_020__V_m1_m1, its stored native proof, one common predicate record, and the serialized proof-to-common composition.

## Inputs and immutable bindings

The verifier receives explicit paths for the selected input, benchmark, R4 resource profile, method contract, arithmetic backend manifest, source snapshot v10, R4 output manifest, native proof envelope, R4 evidence, common record, and composition. The fixed project inputs are checked against SHA-256 values in the frozen R5 profile. The verifier checks all 720 source-snapshot-v10 members and all 34 R4 output-manifest artifacts, including their exact byte lengths and SHA-256 values. The source and output manifest bytes are checked against the profile's frozen hashes.

Two extracted JSON files under results/validation/g4/auer2013/r5_composition_replay_v1/inputs/ copy the common predicate record and typed composition from the hash-bound R4 evidence. The original R4 evidence, proof, snapshots, and output manifest remain unchanged.

## Replay procedure

1. Verify the frozen R5 snapshot v11 and profile membership, then verify source snapshot v10, its sidecar, and every manifest-listed member. Unlisted runtime-generated `__pycache__`/`.pyc` files are tolerated as extras; manifest-listed cache members are still checked and copied. No source member is ignored.
2. Verify the R4 output artifact manifest and every listed artifact. The R4 manifest must retain matched_query_evaluations = 0.
3. Rebuild the expected native proof binding from the fixed inputs and v10 source hashes. Parse the stored proof envelope and invoke replay_native_proof on those stored bytes. Require exact proof digest and a complete replay of every 21-coordinate slab, residual iterate, accepted inclusion, total hull, endpoint, and [0,T] coverage.
4. For every replay-validated slab, build a common TubeSegment from its nine physical coordinates and endpoints, carry the entire frozen twelve-label image, attach the frozen scene, and set NATIVE_TOTAL_HULL with expansion count zero. Re-run check_tube_segments across exact [0,T].
5. Compare every field of the recomputed common record with the stored common record using type-sensitive recursive equality. This covers the segment hash, input hashes, exact rational collision/contact margins, status, and both false certificate/replay flags.
6. Recompute every composition field from the validated proof and recomputed common result. Only then compare the stored composition field-by-field.

The standalone checker does not import the R4 producer and does not treat prior replay flags, stored common status, or stored composition digests as proof. It shares the v10 native checker's validation.g2 exact-rational interval and Taylor arithmetic, and uses validation.g4.common_tube.check_tube_segments for the common predicate. This is algorithmic replay with shared arithmetic dependencies, not an independent arithmetic implementation.

## Work and process limits

Native replay uses an exact-rational cap of 32,768 bits, 2,000,000 operations, a 120-second deadline, and the frozen 100,000 RHS/Jacobian evaluation cap. The common predicate gets 1,799,969 operations so its serialized work record matches the R4 accounting: 2,000,000 - 43,917 producer - 39,081 native replay - 117,033 tamper replay. A separate frozen runner wraps each verifier child with the existing Windows Job Object launcher, capped at 1,024 MiB and 120 seconds. Any arithmetic, wall-time, proof-size, process-memory, or child timeout is recorded as resource_limit, never as a pass.

## Stored-artifact mutation trials

The trial runner creates one copy per mutation under the R5 trials directory. It invokes the frozen v11 verifier on each copied artifact. The five proof trials recompute the envelope digest for field edits except the dedicated proof-digest trial. The six common-record trials alter a segment hull, endpoint, radius mode, radius count, exact margin, or segment hash. The six composition trials alter proof digest, common-check digest, segment digest, query ID, held action, or source-snapshot digest. R4 files are never modified.

Each trial retains the original/copy SHA-256 values, verifier report and report SHA-256, child stdout SHA-256, Windows Job Object resource record, verifier reason, and first mismatch detail. Required outcome classes are native_proof_failure, common_predicate_mismatch, and composition_mismatch for their respective mutation families. A resource guard failure is separately reported and is not counted as a tamper rejection.

## Output limits

A pristine PASS means only that the stored R4 native proof, proof-derived common result, and serialized composition replay consistently for this one synthetic query. The common result remains PASS_ON_SUPPLIED_TUBE; certificate_emitted = false. This does not establish G2, G3, G4, physical correspondence, a matched comparison, or controller safety. Matched-query evaluation count remains zero; overall disposition stays **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**.
