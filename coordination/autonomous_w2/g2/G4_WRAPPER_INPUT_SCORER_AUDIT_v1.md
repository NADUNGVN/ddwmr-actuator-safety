Session: DDWMR | LUNA-G2-SCOPE

# G2 peer audit — G4 wrapper, inputs, and common scorer

**Issued:** 2026-10-08. **Candidate disposition:** `REVISION_REQUIRED_BEFORE_V3_FREEZE_OR_PRODUCER`. **Scope:** read-only inspection of G4 v2's stopped execution and the v3 candidate present at the audit boundary. This review does not modify G4-owned files and does not authorize or perform a query.

## Frozen v2 failure and bounded audit

G4 v2 source closure `results/validation/autonomous_w2/g4/matched_v6_task_development_v2/source_closure_v3.json` (SHA-256 `02b562d7f9bbb748efe8fa1fdb44bc29a2c63a6fc38233625771d5ccb8c7b113`) was independently rehashed read-only: **78/78 listed path, size, and SHA-256 pairs match**. The source pins therefore identify the v2 code that was audited.

The v2 runner's first v6 worker attempt stopped at `v6_w2_worker_v2.py:44`, which reads `peer_saved_row_sha256` from a protocol action that has no such field. The separately pinned outer binding contains the row path and digest. This was a wrapper/binding defect before the producer-start marker, not a native method result. G4's preserved phase record reports one v6 worker invocation, zero v6 native calls, zero Auer worker invocations/calls, and no retry. G2 remains 24/24 native attempts consumed.

V2 also left inconsistent path declarations: the Auer profile named the earlier closure file and `load_freeze()` named the earlier freeze receipt; arbitrary exception text containing `LIMIT` could be treated as a resource stop; the runner collapsed `JOB_LIMIT_OR_CHILD_FAILURE` into an invalid execution result; and the phase timer began at runner launch rather than preparation. These are historical v2 findings. V3 has versioned corresponding paths and starts deriving its remaining deadline from `phase_started_epoch`; its final frozen path set and stop accounting still require a source-closed fixture/freeze review.

## V3 input mapping actually inspected

At the observed candidate boundary, the three v3 protocol actions, copied G2 bindings/rows, Auer input manifest/case files, and Auer proof-binding objects were read directly. A read-only exact-rational comparison confirmed all three mappings:

| G4 pair | G2 peer action | Voltage | Canonical physical-input SHA-256 |
|---|---|---:|---|
| `W2_G4_V6_ZERO` / `W2_G4_AUER_ZERO` | `W2_G2_DEV_001_ZERO` | `(0,0)` | `dc0dcda534dd56e7a1a409977efb5c0565e25c0ca976dcebae189609c4342fa6` |
| `W2_G4_V6_NOMINAL` / `W2_G4_AUER_NOMINAL` | `W2_G2_DEV_001_NOMINAL` | `(1/2,1/2)` | `80f15195b6a29757fa4bd03a20acc0f25b82a4f7e946d6f0308984ca9d6bec4b` |
| `W2_G4_V6_ALTERNATIVE` / `W2_G4_AUER_ALTERNATIVE` | `W2_G2_DEV_001_ALTERNATIVE` | `(1,1)` | `3d5844de37384fa3f0b52b1cea6a7580f42d1b4fd84fbc2e857e5aecc593d0bb` |

For each pair, the current protocol digest, case/manifest digest, canonical physical digest fields, Auer proof-binding digest, voltage, 2 s horizon, nine-state initial box, static inflated-circle scene, and all twelve positive-width fixed labels agreed semantically. The G2 saved-row and core-binding bytes also match their path/hash pairs. This is a positive inspection of the present files; it does not substitute for runtime semantic guards or a frozen v3 source closure.

## Required corrections before the v3 candidate is frozen or run

1. **Fail closed on the actual v6 action and native proof.** `validate_v6_setup()` now reads saved-row path/hash from the outer binding and is called before the producer marker, which fixes v2's missing-field location error. Add explicit, structured checks that `action_id`, the binding's embedded `action`, `peer_action_id`, protocol action, task-protocol action, and frozen voltage all describe the same action; parse the pinned saved row and cross-check its action ID, held voltage, fixed-label image, task/protocol/profile digests, and the row/core binding relation. Require the full set of runtime binding fields and types before direct indexing, returning a structured rejection rather than `KeyError` or another raw exception. The current data match, but the wrapper does not yet prove those semantic equalities before producer entry.

2. **Do not promote a common-predicate pass to task eligibility without a valid native v6 certificate.** Both worker summaries currently compute `task_eligible` from `common_record.predicate_status == PASS_ON_SUPPLIED_TUBE` and progress alone. V6's error-tube inclusion depends on the strict clip-interior premise; `common_tube` explicitly checks only predicates on a supplied tube and sets `ode_tube_proof_replayed` false. Require the recomputed native status to be `CERTIFIED`, full-hold coverage, and `clip_strict_interior_proved == true` before a v6 result can enter the eligible action set. A replayed native `UNKNOWN` must remain unknown and cannot become eligible from a passing geometry check. The common record may still be retained as a diagnostic result.

3. **Give Auer one shared setup validator used by worker and nonquery preflight.** `auer_w2_worker_v3.run()` checks many important hashes before its producer marker, but it has no `validate_auer_setup()` used by mutation fixtures. It selects an action with `next(...)`, indexes required fields directly, and checks protocol/manifest digest strings without reconstructing all task semantics. Before the marker, compare the protocol Auer action and outer v6 action to the unique manifest case and native binding; require exact voltage, peer action, canonical physical digest, case path and file hash, full initial box, full twelve-label image, horizon, benchmark, scene, and source/profile snapshot. Recompute or independently verify the canonical physical-input digest from the case's semantic input. Missing, duplicate, stale, escaping, or mismatched entries need stable rejection codes. Keep all such checks ahead of `producer_start.json`.

4. **Bind common replay to the frozen task inputs.** The geometry scorer itself handles its supplied inputs correctly, but `replay_common_record_semantics()` takes `horizon` and `initial_state` back from the serialized common record, then recomputes using those same record values. Thus its replay equality alone does not establish that the record's horizon is the frozen 2 s hold or that its initial state is the frozen initial box. Pass expected horizon and initial state from the frozen task into replay; reject a mismatch before recomputing progress and predicates. Keep the benchmark/scene/input digest checks. This closes a replay-input binding gap; it is not evidence that the current generated scorer record used different values.

5. **Preserve stop semantics and complete secondary metrics.** The v3 runner currently treats every `JOB_LIMIT_OR_CHILD_FAILURE` as an implementation/execution failure. Separate a confirmed frozen wall/CPU/memory stop—which the protocol permits the run to continue after—from an ambiguous child failure, which must stop without being mislabeled as resource exhaustion. Keep arbitrary exception text from establishing a resource stop. Also map v6 result timing/work fields into launch/phase receipts using their actual names (`common_check_replay_progress_wall_seconds`, `worker_elapsed_wall_seconds`, adapter work), rather than silently omitting metrics expected under Auer-specific keys.

6. **Complete the source-bound nonquery gate before any producer.** The v3 candidate preparation receipt alone does not freeze executable inputs. At this audit boundary no v3 `freeze_manifest_v4.json`, `freeze_receipt_v4.json`, or `source_closure_v4.json` was present. Publish those artifacts only after the validators above and nonquery mutation fixtures have run with producer entry points replaced by fail-if-called stubs for all three actions. Fixtures must cover absent fields, wrong path/hash, action/voltage/digest mismatch, duplicate/missing mappings, stale closure/receipt references, and mismatched task semantics. Bind exact profile/protocol/source closure and phase start, then update G4 STATUS with the frozen hashes. G2 can review that corrected frozen version from its own prefix before G4 enters the already-authorized bounded development comparison.

## Common scorer review — accepted geometric logic on supplied tubes

The actual shared scorer in `validation/g4/common_tube.py`, as called through `matched_v6_common_v3.py`, has sound conservative structure for the declared reduced-model predicates:

- `TubeSegment` represents positive-width **closed** slabs, exactly nine states, endpoints contained in each full-time hull, one fixed full label image, and a declared radius-expansion mode/count. `check_tube_segments()` requires the slabs to cover `[0,T]`, rejects gaps/overlaps, chains identical adjacent endpoint boxes, and verifies the first endpoint contains the complete initial box.
- `_expected_labels()` compares every segment to the benchmark model's full declared label image. The G4 candidate uses the same twelve independent intervals, with positive width, on every slab; labels are not reset between slabs.
- The common check tests every closed slab. Collision uses the lower distance from the full position box to the static-circle center and subtracts the already-inflated radius. It does not add a second footprint/radius expansion. Contact interval-evaluates both normalized slips and the clip law, lower-bounds each wheel's algebraic reserve, upper-bounds the body contact demand, and rejects the supplied tube if any contact/collision margin is negative or unresolved.
- Common progress computes the closed-slab sum `Σ Δt [u] cos([theta])` and the endpoint difference enclosure for `p_x(T)-p_x(0)`. Each independently encloses the same displacement, so their intersection is a valid tightening when both upstream enclosures are valid. `lo > hi` raises an invalid-input error; it is not clipped into a certificate. The serialized progress replay recomputes from the parsed segment hulls.
- Native replay occurs before common scoring in both workers. The common checker explicitly states it does not validate the upstream ODE inclusion or emit a standalone certificate. Thus common PASS alone cannot repair a missing method-native proof premise.

This is a source-level semantic review, not a run of the v3 scorer or proof checker. The shared `Fraction`/`Interval`/`Budget` arithmetic and the G2-native replay dependencies remain disclosed shared trust, not independent arithmetic implementations.

## Task and comparison scope

The prospective synthetic task is the existing two-second forward-displacement task with threshold `7/20 m` (0.175 m/s mean progress), nine-state initial box, twelve narrow fixed labels, static inflated circle, and common three-voltage action set. G2's saved v6 development rows are already consumed development data. The W2 assignment already authorizes G4 to compare the two methods on these same task inputs; no replacement task or external physical-mission data is needed for this bounded development comparison. It cannot be described as held-out confirmation. Any later fresh confirmation requires its own prospectively frozen unused inputs and criterion.

G2's frozen records support the narrow statement that all three saved v6 rows replayed as reduced-model safety-certified and the `(1,1)` alternative alone met the frozen synthetic progress requirement. They do not establish an Auer gap or cross-method advantage. The stopped v2 comparison remains technical-inconclusive until a corrected v3 comparison produces valid evidence. G2 remains **24/24 consumed**, R5 remains **800/800 NOT_RUN**, the Auer 1,944 batch remains `NOT_RUN`, and the project gate remains **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED**.

## Snapshot binding and activity boundary

G4 STATUS sequence 8 snapshot SHA-256 is `06d77d3ed5cdb942c92df5826d0d2c80f4eac0dac6caee871685e0569bd4c309`; it remains `ACTIVE` and says v3 preparation/nonquery fixtures/freeze are next. This audit binds source files by the per-file hashes in the G2 full handoff and G2 STATUS sequence 19. Since v3 was not source-frozen at this boundary, the findings attach only to those observed candidate bytes; later edits require a new hash-bound review.

G2 ran no native query, worker, producer, fixture, preflight runner, proof replay, stage, or study for this audit. No G4 source, protocol, profile, manifest, snapshot, or result file was written by G2. No commit or push was made.
