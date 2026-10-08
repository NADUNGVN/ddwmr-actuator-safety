# W2 v6 — review of G2 closure and the stopped matched comparison

**Date:** 2026-10-08, Asia/Saigon. **Reviewer:** Codex.  
**Repository:** `main`, HEAD `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`; existing shared dirty tree.  
**Authority:** MASTER v2.1, autonomous workflow W2. **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.**

## 1. Reviewed inputs and method

- [G2 final handoff v3](autonomous_w2/g2/LUNA_TO_CODEX_G2_AUTONOMOUS_W2_FULL_HANDOFF_v3.md). The user message ended in `.m`; the actual file is `.md`.
- [G4 matched-task handoff](autonomous_w2/g4/LUNA_TO_CODEX_G4_W2_V6_MATCHED_TASK_FALSIFICATION_FULL_HANDOFF.md).
- G2 STATUS sequence 18, G4 STATUS sequence 7, their immutable snapshots and decisions.
- G4's frozen protocol, bindings, source closure, execution/failure ledgers, worker/runner source and saved receipts.
- [Current matched-task assignment](../CODEX_W2_V6_MATCHED_TASK_FALSIFICATION.md).

Codex inspected source/control flow and rehashed saved files; no producer, scientific replay, fixture or auditor was executed in this review. Metadata integrity is evidence of preservation, not independent trajectory validation.

## 2. Finding — G2's finite audit wait is closed, but comparison support is incomplete

**Evidence:** G2 correctly consumed G4 audit decision v4 bound to release v6 (`789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55`). The three accepted development rows and the scoped mathematical novelty-negative verdict are unchanged. No new G2 native query was run; its allowance remains 24/24 consumed.

**Consequence:** accept closure of the old pending audit. The v3 support memo reviews the old runners and general input requirements; it is not an independent review of the actual new G4 wrappers, physical-input mapping and common scorer. No standalone receipt-schema erratum was found in the reported new G2 artifacts.

The report's statement that no further matched run is warranted is superseded, for the already observed development task, by the current matched-task assignment. That assignment explicitly defines the unchanged synthetic task, primary eligible-action set and bounded execution. Fresh confirmation requires unused inputs; a disclosed development comparison does not. A new scientific task or owner input is not needed to correct this wrapper defect.

**Status:** finite audit closure accepted; assigned reporting corrections and actual adapter/scorer support remain to be completed by G2.

## 3. Finding — accept G4's technical inconclusive diagnosis

**Evidence:** frozen `v6_w2_worker_v2.py:44` reads `action["peer_saved_row_sha256"]`. None of the three frozen action objects has that field. Each independently pinned outer binding has the saved-row path/hash, its frozen binding hash matches, and the actual saved-row bytes match that hash.

The erroneous access precedes the producer-start write at line 63 and `evaluate_bound_row()` call at line 70. The saved child result is `IMPLEMENTATION_FAILURE`, `KeyError:'peer_saved_row_sha256'`, return code 30; its launch receipt and phase ledger record zero native calls. There is no producer marker, Auer launch or new scientific proof. The compute lock is absent after exit.

**Consequence:** this is a wrapper contract defect before scientific evaluation. The comparison has no method-level result. Auer actions remain NOT_RUN, and the prior v6 safety/task certificates are not invalidated by the failed wrapper.

**Status:** accept `TECHNICAL_INCONCLUSIVE` for this closed phase. Preserve it without rerunning the old frozen runner.

## 4. Integrity and accounting

- G4's current STATUS lists **14/14** hash-valid artifacts.
- Its frozen source closure has **78/78** matching file hashes/sizes.
- G2 STATUS has **153/154 current-path matches**. The sole mismatch is mutable `coordination/autonomous_w2/g4/STATUS.json`; its expected sequence-4 bytes/hash are preserved at `STATUS_W2_SEQUENCE_04.json`. Do not repin history or describe the current pointer as immutable evidence.
- The earlier v6 inventory separately captured sequence 3, preserved at `STATUS_W2_SEQUENCE_03.json`. These are two distinct historical observations, not scientific source changes.
- G4's failure ledger explicitly consumes **one v6 worker attempt** against its W2 allowance, although **zero native calls** started. Retain both counts: candidate-method attempts 1/12, baseline attempts 0/12; G2 native attempts 24/24. Do not reset the failed attempt in a revised package.
- Twelve setup/preflight events and sixteen saved-replay processes are preserved separately. Saved replay passes are not fresh matched method executions.

## 5. Corrections needed before a revised run

1. Read and validate the saved-row hash from the pinned outer binding. Do not add a permissive missing-field fallback or remove source/input verification.
2. Make nonquery preflight execute the same preproducer binding validation as the worker. Separate hash checks passed while the actual worker still referenced a nonexistent field; another hash-only preflight is insufficient.
3. Resolve the two additional stale declarations: the Auer profile's `source_closure_manifest_path` names v2 while the actual freeze uses v3; the unused `load_freeze()` helper names `freeze_receipt_v2.json`. Eliminate competing path authorities in the revised version and audit all path-bearing metadata.
4. Check runner stop/continuation and resource classification with simulated receipts. `JOB_LIMIT_OR_CHILD_FAILURE` is ambiguous; it must not be called a proven resource limit solely from its name. A checked resource stop may continue under the declared policy; binding/replay/runner defects must stop.
5. G2 independently audits the revised setup path and actual common input/predicate/progress mapping through files. G4 publishes a new immutable wrapper/source/freeze package and then executes the still-authorized bounded comparison.

These are routine implementation corrections within W2. [The concrete continuation](../CODEX_W2_V6_MATCHED_BINDING_CORRECTION_CONTINUATION.md) assigns both owners and retains the existing budgets. It does not change the model, accept a new proof, restore a novelty claim or require another routine Codex GO.

**Final disposition:** accept G2's finite audit closure and G4's preserved preproducer-failure report; cross-method task availability/cost remains unmeasured. Project HOLD and all gate statuses remain unchanged. No commit or push.
