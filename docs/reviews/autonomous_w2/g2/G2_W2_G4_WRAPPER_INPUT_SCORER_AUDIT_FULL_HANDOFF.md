Session: DDWMR | LUNA-G2-SCOPE

# G2 W2 handoff — G4 wrapper, inputs, scorer, and v6 receipt erratum

**Date:** 2026-10-08 (Asia/Saigon). **G2 disposition:** `PARTIAL / G4 V3 REVISION REQUIRED BEFORE FREEZE OR PRODUCER`. **Audited phase:** the frozen G4 v2 stopped wrapper and the actual v3 candidate files available at this audit boundary. **Native work in this turn:** none.

## Summary

G2 completed the source-level audit requested in continuation section 3 and published its actionable peer comments in [`G4_WRAPPER_INPUT_SCORER_AUDIT_v1.md`](</D:/Research/Teacher_Vien/projects/ddwmr-actuator-safety/coordination/autonomous_w2/g2/G4_WRAPPER_INPUT_SCORER_AUDIT_v1.md>). The v2 closure rehash passed 78/78. The v2 matched attempt stopped before producer entry on a real wrapper bug: it read the saved-row SHA from an action object that does not carry it. The outer binding carries that SHA. G4 v2 recorded one candidate worker attempt and zero native calls; the comparison has no method result.

The v3 candidate now reads the row path/hash from the outer binding and has a shared v6 setup-validation function. Direct inspection of the three current candidate input mappings found all physical-input digests, action/voltage pairs, Auer binding hashes, case hashes, complete initial boxes, twelve positive-width fixed labels, two-second holds, and scene parameters consistent. The v3 artifact set is still a candidate, without its v4 freeze manifest, receipt, or source closure. Its setup contract still lacks required action/input semantic checks before producer entry, and its task-eligibility logic can combine a common geometry pass with a v6 native `UNKNOWN`. The common scorer geometry is conservative on a valid supplied tube; its serialized replay also needs to be bound independently to the frozen horizon and initial box.

These are routine wrapper/replay corrections. They are not a mathematical contradiction in G2's finite v6 proof derivation and do not change the saved-row results. They prevent G2 from accepting the current v3 candidate for freeze/execution until corrected source and nonquery fixture evidence is hash-bound.

## Work completed and ownership

- Read the W2 continuation, current workflow, project operating contract, four canonical research-context files, G2 seq18, G4 current STATUS/snapshots, G4's v2 matched-task report/result, v3 protocol, mappings, bindings, profiles, adapters, workers, runner, common scorer, and producer/replay interfaces.
- Independently rehashed G4's frozen v2 source closure: **78/78 path-size-hash matches**.
- Read-only exact-rational comparison of all three current v3 G2/Auer mappings: all three consistent with the frozen task and the listed physical digests.
- Audited full-time coverage, labels, endpoint chaining, radius use, collision/contact geometry, progress enclosure and replay logic in the actual common scorer.
- Published the v6 receipt-schema erratum at [`V6_ATTEMPT_RECEIPT_SCHEMA_ERRATUM_v1.md`](</D:/Research/Teacher_Vien/projects/ddwmr-actuator-safety/docs/reviews/autonomous_w2/g2/V6_ATTEMPT_RECEIPT_SCHEMA_ERRATUM_v1.md>), preserving historical bytes.
- Published G4 mutable STATUS provenance in [`G4_STATUS_POINTER_PROVENANCE_ADDENDUM_v1.md`](</D:/Research/Teacher_Vien/projects/ddwmr-actuator-safety/coordination/autonomous_w2/g2/G4_STATUS_POINTER_PROVENANCE_ADDENDUM_v1.md>).
- Updated only G2-owned W2 documentation and G2 STATUS sequence 19. G4 sources and reports remain read-only.

## Receipt erratum

The three terminal G2 `attempt_receipt.json` objects and their nested terminal records in the stage receipt have schema label `G2_W2_V6_ATTEMPT_INTENT_v1`. That identifier is the launch-intent label; the terminal objects contain `REPLAYED`, proof/replay hashes and result fields and must be interpreted as terminal receipts. The distinct `attempt_intent.json` objects correctly remain intent records. The erratum changes the interpretation only and preserves the four original file hashes. See the standalone erratum for every path and digest.

The error does not change G2 release v6, saved row/proof bytes, source pins, bindings, or attempt accounting. G2 remains 24/24 native attempts consumed; the three saved v6 rows remain three of those attempts. G4's old failed wrapper invocation is separate: one worker attempt, zero native calls. The R5 800-row study and Auer 1,944-query batch remain `NOT_RUN`.

## Mutable STATUS provenance

G2's v6 evidence inventory captured G4 sequence 3 at SHA-256 `38c88eaf048ec04478a1eb99bfd40977222b2149b10e84fced75d162c9468554`. G2 STATUS sequence 18 captured G4 sequence 4 at SHA-256 `98d8f9f98200f32db2fd0a74975b21a1dc7df929bffbed4a4b9a37cb1c6d16c7`. At this audit boundary G4 STATUS sequence 8 and its mutable pointer have matching SHA-256 `06d77d3ed5cdb942c92df5826d0d2c80f4eac0dac6caee871685e0569bd4c309`; sequence 8 is `ACTIVE`. G2 records sequence 8 as a new observation and does not rewrite the sequence-3 inventory or G2 sequence 18.

## Actual wrapper and input findings

### Historical v2

G4 v2 froze an exact three-action task mapping and a 78-entry closure. Its runner invoked the frozen candidate once. At the first v6 action, the worker requested `action["peer_saved_row_sha256"]`, although the field was absent from the protocol action and present in the signed outer binding. The failure happened before `producer_start.json`; the runner correctly stopped without retry and counted zero native calls. Auer was never invoked. Therefore the result is technical-inconclusive, not an Auer `UNKNOWN`, not baseline unavailability, and not v6 superiority.

The v2 profile and helper retained stale closure/receipt paths, its exception classification and runner stop handling were broader than W2's declared resource/ambiguity rules, and the timer omitted preparation. Those historical issues are listed in the G2 peer memo with the source hashes bound to the v2 closure.

### V3 current input mapping

The candidate presently maps zero, nominal, and alternative to G2's saved development actions with voltages `(0,0)`, `(1/2,1/2)`, `(1,1)`, and physical-input digests `dc0d…42fa6`, `80f1…bec4b`, and `3d58…3d0bb`, respectively. For each mapping, the case and manifest byte hashes match; the Auer proof-binding semantic digest matches the protocol; and exact rational comparison confirms the case's held voltage, nine-state initial box, all twelve label intervals, 2 s horizon, obstacle center and inflated radius agree with the task. G2 row, core binding, and v6 outer-binding byte hashes also agree.

This positive data comparison does not show that every equality is enforced in the actual preproducer route. The v6 shared setup validator checks important hashes and action IDs, but should explicitly check the embedded action/voltage against the task and external mapping, and parse the saved row to cross-check its semantic action/proof fields. The Auer worker checks file and binding digests but lacks a shared setup validator used by nonquery mutation fixtures; several required fields are obtained with `next()` and direct dictionary indexing. It also relies on declared physical-digest strings without validating a complete semantic projection of the case against the frozen task.

## Actual scorer findings

The common scorer has the following conservative geometry:

- It receives a nine-state total hull on each positive-width closed slab. Endpoints must be contained by their slab hulls; full hold coverage, no gaps or overlaps, exact endpoint chaining and inclusion of the full initial state box are enforced.
- The benchmark's complete twelve-coordinate positive-width parameter image is reconstructed. Every segment must carry exactly that same image in the same order, so fixed labels are not reset between slabs.
- The collision bound measures a lower distance from the full position box to the declared static-circle center and subtracts the already inflated exclusion radius. The common checker adds no second radius expansion.
- Contact is checked across each full-state slab by interval-evaluating slip and clipping, lower-bounding wheel reserves, and upper-bounding required body contact demand. A negative or nonpositive lower margin cannot pass.
- Progress is enclosed both by the full-slab sum of `Δt · [u] · cos([theta])` and by endpoint displacement. Intersecting two valid enclosures of the same displacement is valid; an empty intersection throws an error instead of fabricating a narrower certificate. Serialized progress is reparsed and recomputed from the common tube segments.

These checks establish predicates only on the supplied tube; the module explicitly does not establish the upstream ODE inclusion or emit a standalone certificate. The v6 producer's strict clip-interior condition is a separate native proof premise. The v3 workers presently form `task_eligible` from common predicate pass and progress only; v6 must additionally require replayed native `CERTIFIED` plus the strict clip-interior/full-hold proof. A common geometry pass cannot repair a native `UNKNOWN`.

The independent common-record replay currently reconstructs horizon and initial state from the common record itself. Its equality check therefore does not independently show those values equal the frozen task's horizon and full initial box. Pass those expected task inputs into replay and reject mismatches before recomputing common predicates/progress. This is a replay-input binding correction; the current generated v3 result was not observed to use different task inputs.

## Required G4 actions

The full actionable requirements are in the G2 peer audit memo. In brief, G4 should:

1. Add fail-closed, structured validators for v6 and Auer setup; use the same functions in each worker and nonquery preflight. Cross-check action ID, voltage, physical-input digest, saved/native file bytes, peer action and complete task semantics.
2. Add all-three-action mutation fixtures with producer/replay entry points replaced by fail-if-called stubs. Verify missing, stale, duplicate, mismatched and path-escaping bindings reject before any marker.
3. Gate v6 task eligibility on method-native `CERTIFIED`, full-hold replay, and the strict clip-interior premise; retain common geometry results separately when the native method returns unknown.
4. Bind common semantic replay to the frozen 2 s horizon and full initial state; keep the progress intersection and reject-empty rule.
5. Separate confirmed external resource stops from ambiguous child failure, and retain complete method-specific worker/replay/common timing and work metrics.
6. Publish the revised v3 freeze receipt, source closure and profiles only after the setup fixtures pass; update G4 STATUS with exact hashes. G2 will review that corrected frozen candidate before G4 starts its bounded run.

G4 can continue under the W2 assignment on the existing synthetic task and its already-consumed development rows. This development comparison requires neither a newly invented task nor external physical-mission data. It is not fresh confirmation; a future confirmation claim requires new, unused inputs frozen prospectively.

## Scientific disposition and limits

The previously saved G2 records replay with all three reduced-model safety predicates certified, while only the `(1,1)` action meets the task's `7/20 m` progress threshold. The result is narrow and synthetic. G2's earlier finite audit accepted those records for their stated scope but concluded **NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE**; cross-method task utility is **UNMEASURED_NOT_REFUTED** because the prior G4 comparison stopped before native execution. Nothing in this wrapper/scorer audit supplies an Auer result or supports mathematical novelty, method superiority, physical-platform validity, or G2 gate promotion.

Project disposition remains **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED**.

## Activity and preserved evidence

G2 performed no query, worker, producer, stage, replay, preflight runner, mutation fixture or study for this audit. G4 sources, G4 protocol, profiles, manifests, snapshots, historical receipts and results remain unmodified by G2. No branch switch, commit or push occurred.

G2's final W2 status for this audit is `coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_19.json`; its mutable pointer is `coordination/autonomous_w2/g2/STATUS.json`. Those bind this report, the coordination memo, the schema erratum, the status-provenance addendum, and the observed G4 sequence-8 snapshot.
