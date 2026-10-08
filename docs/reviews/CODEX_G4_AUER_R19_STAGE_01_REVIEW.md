# Codex review — G4 Auer R19 Stage 1

**Date:** 2026-10-05  
**Reviewed handoff:** `LUNA_TO_CODEX_G4_AUER_R19_SUCCESS_ARM_BINDING_CORRECTION_FULL_HANDOFF.md`  
**Disposition:** **GO for the exact R19 Stage 1 only**. This is authority to acquire one bounded matched stage of evidence, not acceptance of the Auer comparison or a G4 gate pass.

I read `AGENTS.md`, the four canonical `research_context` files, the R18 review, the R19 handoff, manifest, closure, schedule, protocol, runner, checker, successful-arm fixture source and stored report, and the exact-scope decision/authorization contracts. I independently rehashed all **575/575** R19 dependency files and found zero path, size or hash mismatches. All **549** R18 inherited records match, including the **525** earlier R17 records. The manifest, closure, schedule and non-query report hash respectively to `9f926ddc17b4a7711ba4a9e1d8658832ac5e21a50bb2a953d41adef3c6064c2c`, `a50bc0452e6b8f164988a4af8d669e563381f157f86188ca8c7ee1fb1518ca76`, `4271fd9339788e8372cdd4b8b48ecd9d61b7a0c10bdd7cebc7f79f9fcf1a5fd6`, and `a5d892ac5546ca37b02938c61dd7028c24b91c68e40dd0415867dcfbe6702e63`. At review time, the canonical R19 Stage 1 output and executable authorization receipt were absent. I did not run a fixture, worker, producer, composition audit, query or stage.

## Findings

1. **Successful-arm binding corrected.** The R18 runner's undefined `_bound_result_references` is now an explicit `checker._bound_result_references` call in `batch_stage_runner_v3_r19.py::_write_method()`. The helper exists in the pinned R19 checker and bounds proof/common references before the R17 independent result validator. The stored non-query fixture drives the production method branch through a stubbed launcher: unchanged R18 records the `NameError`; R19 reaches the independent validator once. Its intentionally incomplete synthetic result is rejected. This is a control-flow check, not a successful scientific result.
2. **Source and accounting preserved.** The 1,940 never-attempted continuation IDs retain R17/R18 order, and this stage is exactly the first ten. The four historical consumed IDs remain separate. The R19 checker binds the executable receipt to this manifest, closure, schedule, ordered ID digest, resource policy and a hashed review block containing an explicit exact-scope GO. The runner refuses an existing output root, records durable one-shot intents and stops on class 3. The stored non-query fixtures cover partial/stopped stage replay and NO-GO review refusal. They do not establish live method behavior.
3. **Limited execution decision.** No further deterministic source contradiction was found in the inspected successful method/audit and stage entry paths. A first live stage is needed to observe whether the methods, composition audit and independent checker complete under the fixed resource limits. A `CERTIFIED` label is usable only after its native proof and common composition independently replay. `UNKNOWN` remains inconclusive. If an intent, guard, audit, capture or replay stops, preserve all bytes and consumed-ID accounting; do not retry that ID, substitute an ID or advance a stage.

The launcher and checker have the resource limits in the decision below. The runner/checker processes do not have an independent Job Object memory cap, and descendant-tree termination beyond the guarded worker/auditor remains an enforcement limit. These limits are recorded; this GO makes no claim of complete process-tree containment.

## Exact decision

<!-- DDWMR_G4_R19_EXACT_SCOPE_DECISION_BEGIN -->
{
  "schema": "ddwmr-g4-r19-codex-exact-stage-review-v1",
  "reviewer": "Codex",
  "scope": "G4_AUER_R19_STAGE_01_ONLY",
  "decision": "GO",
  "execution_authorized": true,
  "candidate": {
    "manifest_path": "research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v19_PROSPECTIVE.json",
    "manifest_sha256": "9f926ddc17b4a7711ba4a9e1d8658832ac5e21a50bb2a953d41adef3c6064c2c",
    "source_closure_path": "research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R19_PROSPECTIVE.json",
    "source_closure_sha256": "a50bc0452e6b8f164988a4af8d669e563381f157f86188ca8c7ee1fb1518ca76",
    "schedule_path": "research/benchmarks/G4_AUER_R19_CONTINUATION_SCHEDULE.json",
    "schedule_sha256": "4271fd9339788e8372cdd4b8b48ecd9d61b7a0c10bdd7cebc7f79f9fcf1a5fd6"
  },
  "stage": {
    "stage_id": "r19_continuation_01",
    "query_ids": [
      "state_high_mid__scene_d050_l+000__T_050__V_0_0",
      "state_high_pos__scene_d050_l+200__T_100__V_0_p1",
      "state_low_neg__scene_d100_l-200__T_020__V_p1_m1",
      "state_low_mid__scene_d100_l+000__T_050__V_p1_0",
      "state_low_pos__scene_d100_l+200__T_100__V_p1_p1",
      "state_high_neg__scene_d200_l-200__T_020__V_m1_m1",
      "state_high_mid__scene_d200_l+000__T_050__V_m1_0",
      "state_high_pos__scene_d200_l+200__T_100__V_m1_p1",
      "state_low_neg__scene_d020_l-200__T_020__V_m1_0",
      "state_low_neg__scene_d020_l-200__T_020__V_m1_p1"
    ],
    "query_count": 10,
    "ordered_ids_sha256_lf": "555297305b09d9676e401c10b5e33772463e43e2379778c0ce806d2c7f9e649d"
  },
  "resource_policy": {
    "method_worker_memory_cap_bytes": 1073741824,
    "method_worker_wall_cap_seconds": 120,
    "composition_audit_memory_cap_bytes": 1073741824,
    "composition_audit_wall_cap_seconds": 120,
    "launcher_wall_cap_seconds": 150,
    "launcher_stdout_capture_cap_bytes": 1048576,
    "checker_json_read_cap_bytes": 16777216,
    "checker_artifact_read_cap_bytes": 67108864,
    "review_file_read_cap_bytes": 65536
  },
  "one_shot": true,
  "no_retry_rule": "ONE_SHOT_PER_METHOD_QUERY; NO_RETRY; unresolved intent is terminal class 3"
}
<!-- DDWMR_G4_R19_EXACT_SCOPE_DECISION_END -->

## Reporting obligation and gate

Run at most this single ten-ID matched stage. Stop on the first class-3 outcome. Return a full Markdown handoff with the receipt and artifact hash ledger, attempted/completed/unattempted IDs, native proof and independent composition replay outcomes, any resource/stop evidence, and fixed-denominator accounting. No later stage or full 1,944-query comparison is authorized here.

**HOLD persists.** G1 PASS applies only to the restricted reduced model. G2/G3/G4 and physical-platform correspondence remain UNVERIFIED. No G3, operational controller, closed-loop, experiment or hardware work is authorized.
