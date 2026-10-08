# Codex review template — DDWMR G4 Auer R18 Stage 1

**Template status: NO-GO.** Codex must independently review the candidate and replace the decision block only if exact scope is approved. This template itself grants no authority.

<!-- DDWMR_G4_R18_EXACT_SCOPE_DECISION_BEGIN -->
{
  "candidate": {
    "manifest_path": "research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v18_PROSPECTIVE.json",
    "manifest_sha256": null,
    "schedule_path": "research/benchmarks/G4_AUER_R18_CONTINUATION_SCHEDULE.json",
    "schedule_sha256": null,
    "source_closure_path": "research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R18_PROSPECTIVE.json",
    "source_closure_sha256": null
  },
  "decision": "NO_GO",
  "execution_authorized": false,
  "no_retry_rule": "ONE_SHOT_PER_METHOD_QUERY; NO_RETRY; unresolved intent is terminal class 3",
  "one_shot": false,
  "resource_policy": {
    "checker_artifact_read_cap_bytes": 67108864,
    "checker_json_read_cap_bytes": 16777216,
    "composition_audit_memory_cap_bytes": 1073741824,
    "composition_audit_wall_cap_seconds": 120,
    "launcher_stdout_capture_cap_bytes": 1048576,
    "launcher_wall_cap_seconds": 150,
    "method_worker_memory_cap_bytes": 1073741824,
    "method_worker_wall_cap_seconds": 120,
    "review_file_read_cap_bytes": 65536
  },
  "reviewer": "TEMPLATE_NOT_A_REVIEW",
  "schema": "ddwmr-g4-r18-codex-exact-stage-review-v1",
  "scope": "G4_AUER_R18_STAGE_01_ONLY",
  "stage": {
    "ordered_ids_sha256_lf": "555297305b09d9676e401c10b5e33772463e43e2379778c0ce806d2c7f9e649d",
    "query_count": 10,
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
    "stage_id": "r18_continuation_01"
  }
}
<!-- DDWMR_G4_R18_EXACT_SCOPE_DECISION_END -->
