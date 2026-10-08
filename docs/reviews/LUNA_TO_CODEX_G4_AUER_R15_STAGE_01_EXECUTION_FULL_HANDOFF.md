Session: DDWMR | LUNA-G4-AUER

# G4 Auer R15 Stage 1 execution — full handoff

**Disposition:** `BLOCKED` after the authorized single stage stopped at class 3. R15 attempted 2/10 scheduled IDs; no retry, replacement, later stage, or batch was run. Raw stage evidence remains in the canonical batch namespace.

## 1. Scope and authorization

Executed `docs/CODEX_TO_LUNA_G4_AUER_R15_STAGE_01_EXECUTION.md` under the exact GO in `docs/reviews/CODEX_G4_AUER_R15_EXACT_STAGE_GO_REVIEW.md` and its machine decision. Authorization covered stage ID `r15_continuation_01`, exactly ten ordered IDs, method order R3 then Auer, one invocation per method/ID, 120-second and 1-GiB worker/audit limits, no retry or substitution, and no auto-advance.

Before launch, source-bound `load_candidate_lock()` and `validate_go_receipt()` checks passed. The exact review, decision, canonical GO receipt, manifest, closure, schedule, runner, and checker bytes matched their pinned SHA-256 values. The canonical batch root then contained only `authorizations/r15_continuation_01.json`; `stage_01` was absent. Since the canonical GO receipt already existed, the pre-authorization `--verify-only` check was inapplicable; I used the source-bound GO validator and a read-only namespace check.

| Bound artifact | SHA-256 |
|---|---|
| GO review Markdown | `a22f56e2f4e529008abe67da608da19e2882cda627e860b5dfd046bc2d0b7532` |
| GO decision JSON | `0e7553a3f1134c00286bb0b7cc87807e429aadcee2090dd4f863e626681e9f97` |
| Canonical GO receipt | `017f36d5bca13daf08f19a7193c6e19d592cba344157e57e9f059b2d6119a017` |
| R15 manifest | `e02cde6dfb5c8d07cbac053ebb0db945a4961b4aa1bc383c5dbf5660d707d556` |
| Source closure (467 dependencies) | `0488078d3be68e8ddc3da4478553403023ee1c79e4243ac0306dac8b7765d152` |
| Stage 1 schedule | `b2e833cdb20c1d31fde899373ae4d7f2332bd359cc4888d6ddb917840ae96b92` |
| Runner | `50ed4b51627661c65eff93b3e098ddaf59a4e86a72896f07af94c04478084f3e` |
| Independent checker | `23abbd52a7193ae5149474f2835e828e7b0cea9e6b74ac05deec3462a33ee01b` |
| Ordered ten-ID digest (LF) | `58a888845732cc8f5220656444d0b6ae9aa19a96eed1c014a7f907e9fac55bbd` |

## 2. G2 R12 prerequisite

The G2 R12 two-row run had stopped before R15 launch. Its runner capture records the authorized command ending at `2026-10-04T08:00:28.551207Z`, exit code 0, and `STOPPED_INVALID` after one row intent of two. The public read-only `validation.g2.r12_execution_checker.audit_stage()` independently returned `status=STOPPED_INVALID` and `receipt_valid=true`; the receipt records `native_query_calls=0`, `rows_terminal_count=1`, and `INCOMPLETE_NO_TRIGGER`. No matching G2 or G4 runner process was present at the R15 preflight snapshot.

G2 evidence hashes: canonical `receipt.json` `49b68b72ba2f54c4e6f85e11627e694486ce378ce03093390eec0ab3b3005bde`; row 00 intent `51b26572b5194c80738099598bfa2645be084345fcf24e294e83400d873ff9f4`; row 00 terminal `2600d3d5bdac85efd6092f9253cd0c2f5fc62bcf55caafff642566332d34c44a`; execution capture JSON `2e443fcd330447a4beb2532ab8100520156111ce8b2affddb6d0a5ba0045ec26`. The prior G2 namespace and capture bytes were left untouched.

## 3. Single runner invocation

Exact command:

```text
python -B -m validation.g4.batch_stage_runner_v3_r15 --project-root . --stage-id r15_continuation_01 --authorization-receipt results/validation/g4/auer2013/protocol_v3_r15_batch/authorizations/r15_continuation_01.json
```

- Captured start/end (UTC): `2026-10-04T08:06:40.118977Z` to `2026-10-04T08:07:37.338817Z`.
- Runner exit code: `20` (`STOPPED_AFTER_CLASS3`; no retry).
- Raw stdout: `results/validation/g4/auer2013/protocol_v3_r15_candidate/r15_continuation_01_execution_20261004/runner.stdout.bin`, 6,030 bytes, SHA-256 `f9626cf4ca17586f00ee15a71b888663c87b8411c3d95fd0ae68fff7efb235f0`.
- Raw stderr: same folder, `runner.stderr.bin`, 0 bytes, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Capture record SHA-256: `483ca0a7db007c80ad708861d3b1dbc45e9459e3a914a71bf57a96b1428da697`.

The canonical stage namespace is `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/` (the GO-bound stage ID remains `r15_continuation_01`). It contains a write-once stage intent and terminal receipt. The stage intent was created at `2026-10-04T08:06:50.635825+00:00` and binds the ordered ten-ID schedule and GO pins.

**Timestamp note for review:** the terminal reports `stage_elapsed_wall_seconds=46.672`, but its internal `started_utc` and `completed_utc` are both `2026-10-04T08:07:37.307119+00:00`. The independent checker accepted the ledger replay; the discrepancy between those terminal fields and the stage-intent/external capture times is preserved as an artifact-integrity observation.

## 4. Stage outcome and matched rows

| Ordered ID | R3 | Auer | Proof/common/audit replay and disposition |
|---|---|---|---|
| `state_low_pos__scene_d020_l+200__T_100__V_m1_p1` | Class 2, authenticated `UNKNOWN`; native replay `NOT_RUN`; common not evaluated; audit not applicable because there is no common record. Result cites negative sufficient collision/contact margins; this is not an unsafe finding. | Class 1, `CERTIFIED`; native proof replay `PASS`; common `PASS_ON_SUPPLIED_TUBE`; composition audit `PASS`. | Valid terminal pair; included in the one-ID completed prefix. R3 serialized proof bytes exist, but they were not replayed and are not accepted as a proof. |
| `state_high_neg__scene_d050_l-200__T_020__V_0_m1` | Class 3 after R3 invocation intent and worker. R3 result and its composition receipt claim native replay/common/audit PASS, but R15 exact provenance replay rejects the common segment binding (details below). | Not invoked; R3 class 3 halted the method order. | Failing next ID; stop reason `ContractError: common segment provenance does not bind exact proof/source`; `failure_phase=METHOD_POST_INTENT`. No resource-limit event. |

The first completed pair is the entire terminal prefix. The next eight scheduled IDs are `NOT_RUN`:

1. `state_high_mid__scene_d050_l+000__T_050__V_0_0`
2. `state_high_pos__scene_d050_l+200__T_100__V_0_p1`
3. `state_low_neg__scene_d100_l-200__T_020__V_p1_m1`
4. `state_low_mid__scene_d100_l+000__T_050__V_p1_0`
5. `state_low_pos__scene_d100_l+200__T_100__V_p1_p1`
6. `state_high_neg__scene_d200_l-200__T_020__V_m1_m1`
7. `state_high_mid__scene_d200_l+000__T_050__V_m1_0`
8. `state_high_pos__scene_d200_l+200__T_100__V_m1_p1`

### Provenance blocker on R3 ID 2

For the failing R3 ID, `proof.json` is 120,973 bytes with raw SHA-256 `86d203f88e528e44670a431b5794fa5fe57f8196ac93e15d9b97dd783c93cd14`; its semantic proof-record hash is `c038220283469e288bebfd8c25ce907f4f96cce06114b6ffd9aefe1cb1275cde`. In `result.common.json`, the segment provenance includes `native_record_semantic_sha256=c038…`, `native_proof_replay=PASS`, method ID, query ID, and endpoint source. It does **not** include the two fields required by the R15 checker: `native_proof_file_sha256` equal to the exact raw proof-file hash above, and `source_snapshot_manifest_sha256` equal to the pinned R9 source closure `7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533`. The composition report carries that R9 closure in its query context and reports its own `PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED`, but those values are not present as the required segment provenance bindings. R15 therefore classifies this as `AUDIT_UNVERIFIED_BINDING` / class 3, even though the producer result says `CERTIFIED` and `PASS_ON_SUPPLIED_TUBE`. Preserve the distinction; do not promote the R3 common output as verified.

## 5. Stage counters and resource accounting

| Counter | Terminal value |
|---|---:|
| Attempted query IDs | 2 |
| Completed class 1/2 pair prefix | 1 |
| Remaining `NOT_RUN` IDs | 8 |
| Method invocation intents | 3 |
| Worker guard commands | 3 |
| Composition-audit intents / guard commands | 2 / 2 |
| Unresolved audit invocations | 0 |
| Retries / substitutions | 0 / 0 |
| Stage elapsed wall time (terminal field) | 46.672 s |

No resource stop occurred. The 120-second and 1-GiB caps were not approached by observed calls: R3 ID 1 worker 49,160,192 bytes / 0.281 s; Auer ID 1 worker 49,070,080 bytes / 0.750 s and audit 53,780,480 bytes / 0.578 s; R3 ID 2 worker 49,164,288 bytes / 0.578 s and audit 52,387,840 bytes / 0.516 s. The class 3 cause is proof/source provenance, not a resource limit. The checker CLI itself reports `query_workers_invoked=0`, `producers_invoked=0`, and `auditors_invoked=0`; those are its own replay-process counts, separate from the two stage audit guard calls.

## 6. Independent read-only replay and fixed denominators

Exact checker command:

```text
python -B -m validation.g4.check_matched_batch_v3_r15 --project-root . --summary --output results/validation/g4/auer2013/protocol_v3_r15_candidate/r15_continuation_01_execution_20261004/r15_fixed_denominator_summary.json
```

The checker exited 0 at `2026-10-04T08:08:31.133561Z` after starting `2026-10-04T08:08:25.852854Z`. It returned `READ_ONLY_REPLAY_COMPLETE`, independently replayed the R15 terminal/composition receipts, and launched no query worker, producer, or auditor. Summary JSON SHA-256: `b513faea9ee2b76e0bdef602fb289b1a109e056740be1d7dbb26d6ab86f5224a` (478,459 bytes). Raw checker stdout SHA-256: `7693296b891ea17f56303b10654c6ccd2a44d995cf6b497b7dcd905e6f051a72` (401 bytes); stderr is empty (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). Checker capture record SHA-256: `8057c73b44e93feaeec375423e0c37b924028071b66ca6ce7cd3549ae377a5d1`.

| Fixed universe stratum | Count/status |
|---|---:|
| Total fixed universe | 1,944 |
| R9 historical preflight carry-in | 1 |
| R11 historical consumed ID | 1 |
| R12 continuation universe | 1,942 |
| R15 first stage planned / attempted / not run | 10 / 2 / 8 |
| R12 continuation IDs outside this R15 first-stage candidate | 1,932 |

R9 and R11 remain separate historical strata and are not pooled into R15 yield. The 1,932 outside-stage continuation IDs were not launched. Method summaries against the fixed planned denominator of ten:

| Method | Class 1 | Class 2 UNKNOWN | Class 2 resource/inclusion | Class 3 | Not run | Audit pass / unresolved / N/A |
|---|---:|---:|---:|---:|---:|---:|
| R3 | 0 | 1 | 0 / 0 | 1 | 8 | 0 / 1 / 1 |
| Auer | 1 | 0 | 0 / 0 | 0 | 9 | 1 / 0 / 0 |

`UNKNOWN` is inconclusive, not unsafe. These two attempts do not support batch-level yield, novelty, or gate-promotion claims.

## 7. Output hashes and preserved evidence

All 42 files under the canonical R15 batch root after the stop are listed with exact byte size and raw SHA-256 in `results/validation/g4/auer2013/protocol_v3_r15_candidate/r15_continuation_01_execution_20261004/stage_output_inventory.json` (inventory SHA-256 `3cf9d0116a66fd60f7f69f6576dc09c421119f7602b300e78803b62935c24988`). This covers the GO receipt, stage intent/terminal, all three invoked method records, their audit artifacts, logs, checkpoints, proofs, and common outputs. Selected stage hashes:

| Artifact | SHA-256 |
|---|---|
| Stage intent | `31769bbaca47157b9ee5dd66ac9cfbd38a824490034537d13afc913d255360b2` |
| Stage terminal receipt | `04335cbd0be227f67ea76b47459265e9cfcf1e16d080e51ad5c517dd98278dcb` |
| ID 1 R3 terminal | `3164d7abe70518c7619d49d0c117b014e37661015ae67320bf6fcbe8ba6b8fbd` |
| ID 1 Auer proof / common / result / terminal | `a0bc4d9d39c91dd4933f0219a27095d40c70fde5769cad13a483232a2ab06858` / `bfd352a2a789bf403b07c86162331aaf8059dc94ee0c85e4294663ef6b5c12b6` / `5b6a6637fb2bf1f8a34fe0c678d2c5717bf8f5c391ba4460eb7eda21af1c584c` / `3adbbc350cc225ba05bd3cbb1a164ebb9a8b17246d4e74c12659b9b95dbc3ca5` |
| ID 1 Auer composition report / audit receipt | `fb4f458cfaa5b7afd449f64e292376a1a22263021d5236ec9b3135fdc3c59f6d` / `20262055ee54d933a5240fd33dd054cf3e6d7736546c3c704b55f8f02150971a` |
| ID 2 R3 proof / common / result / terminal | `86d203f88e528e44670a431b5794fa5fe57f8196ac93e15d9b97dd783c93cd14` / `c328a91363419547b1a51a0912919ce82f005b242eb266a7fc482fd75ba3f158` / `99fb2a04f67e4080ac91c30592f7c490e47917816c48466d55e3c105162b43c8` / `76eba3640f52e3b50b374bbeb930e4211a1c546ce7615ef960b48366e6f25fa2` |
| ID 2 R3 composition report / audit receipt | `afc97911f959c4a5e96e7ff1d210ca8ff8512f20802239aecb0ca6223c7db9d7` / `b2fb72d91d79ce69c93d06a635a0655d43305a8d30eaf47bcba1e5ff393caf3d` |

Runner/checker raw streams, capture records, and the fixed-denominator summary are in the same external candidate execution folder. Nothing in the canonical batch output was deleted or rewritten after replay.

## 8. Final disposition

R15 Stage 1 executed exactly once and stopped after one verified matched terminal pair when the second ID failed exact R3 common-segment proof/source provenance binding. The independent read-only checker completed and preserved the fixed denominator, but classifies the second ID as `AUDIT_UNVERIFIED_BINDING`. The stage is not a complete ten-ID comparison. No retry, later stage, full 1,944-query batch, commit, or push occurred. Existing R9/R11/R12/R13/R14 evidence and source candidates were not edited.

**Codex review focus:** adjudicate the R3 common segment provenance schema against the R15 checker’s required raw-proof-file and source-closure fields, and review the terminal timestamp mismatch above. Treat the stage as stopped and non-resumable; no additional execution is authorized by this handoff.

## Appendix A — canonical batch file inventory

Every hash below is SHA-256 over exact file bytes. The machine-readable inventory above carries the same complete list.

| Canonical batch path | Bytes | SHA-256 |
|---|---:|---|| `results/validation/g4/auer2013/protocol_v3_r15_batch/authorizations/r15_continuation_01.json` | 3952 | `017f36d5bca13daf08f19a7193c6e19d592cba344157e57e9f059b2d6119a017` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/stage_intent.json` | 1903 | `31769bbaca47157b9ee5dd66ac9cfbd38a824490034537d13afc913d255360b2` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/stage_terminal_receipt.json` | 6997 | `04335cbd0be227f67ea76b47459265e9cfcf1e16d080e51ad5c517dd98278dcb` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/audit/audit.stdout.log` | 3209 | `ae6c2bd8249b7a1d36523059406f62650b2e3b025c56456b5b0fb385dfc51b33` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/audit/audit_guard.json` | 4786 | `e6d99b8c8ddb42c98a349684ef9b43e6f28dc6d5ecb5dad66d7eeb7aab58d9f6` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/audit/audit_intent.json` | 2864 | `2e1578735c0740175baddaba7de0a710145faf1f84b869d0594f12085392a4b9` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/audit/audit_receipt.json` | 2804 | `b2fb72d91d79ce69c93d06a635a0655d43305a8d30eaf47bcba1e5ff393caf3d` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/audit/composition_report.json` | 3472 | `afc97911f959c4a5e96e7ff1d210ca8ff8512f20802239aecb0ca6223c7db9d7` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/checkpoint.json` | 58300 | `988d6311c0d33facf8c7ca92a620ce11a7692db5eadb3e5635975037840d5fc3` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/invocation_intent.json` | 2661 | `53a39a772ae9d75c6d0bd4ad627c48051997836165dd6593a635c198a3f474a9` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/proof.json` | 120973 | `86d203f88e528e44670a431b5794fa5fe57f8196ac93e15d9b97dd783c93cd14` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/result.common.json` | 84776 | `c328a91363419547b1a51a0912919ce82f005b242eb266a7fc482fd75ba3f158` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/result.json` | 57281 | `99fb2a04f67e4080ac91c30592f7c490e47917816c48466d55e3c105162b43c8` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/terminal_receipt.json` | 4408 | `76eba3640f52e3b50b374bbeb930e4211a1c546ce7615ef960b48366e6f25fa2` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/worker.guard.json` | 4051 | `46e50de12d6ef14c08978e2e6fc5078906e51d6326ae11350e4e33494fe8673c` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_high_neg__scene_d050_l-200__T_020__V_0_m1/r3/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/audit/audit.stdout.log` | 3369 | `7d2823eab047e4af003615c0a15eba68c60866b947b3fa96d3bff12574a1a331` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/audit/audit_guard.json` | 4810 | `94c9367442a0ea6b5cacf9d03d3ee360e5b93a0f47da3eda7cf7d2acca96194c` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/audit/audit_intent.json` | 2878 | `e98c03d6340fe2707fc76812e6cc7b79c6e4ce868aca12c8d069d65fc4714a5e` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/audit/audit_receipt.json` | 2814 | `20262055ee54d933a5240fd33dd054cf3e6d7736546c3c704b55f8f02150971a` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/audit/composition_report.json` | 3669 | `fb4f458cfaa5b7afd449f64e292376a1a22263021d5236ec9b3135fdc3c59f6d` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/audit/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/checkpoint.json` | 57716 | `0c08001a4123cb61d74a929869c6c0307abafcb0bc40bf8236a234bf73785ed8` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/invocation_intent.json` | 2675 | `0b08060a026edc3faad712097fed4d58144225eba65b3aa0b6f9c2a714d4c7c4` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/proof.json` | 758248 | `a0bc4d9d39c91dd4933f0219a27095d40c70fde5769cad13a483232a2ab06858` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/result.common.json` | 24214 | `bfd352a2a789bf403b07c86162331aaf8059dc94ee0c85e4294663ef6b5c12b6` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/result.json` | 56686 | `5b6a6637fb2bf1f8a34fe0c678d2c5717bf8f5c391ba4460eb7eda21af1c584c` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/terminal_receipt.json` | 4445 | `3adbbc350cc225ba05bd3cbb1a164ebb9a8b17246d4e74c12659b9b95dbc3ca5` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/worker.guard.json` | 4051 | `7c458fa804a7dc0544babe63600617c532b1c72b00a52b200901e9ad3b483a27` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/auer/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/r3/audit/audit_not_applicable.json` | 3414 | `44c62d46d7bb99d1e44f2f825bb1f239377cb00d34ceed8ba1686d5777eff367` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/r3/checkpoint.json` | 56561 | `9963afa9fbd935c6ffccf702b518a17ebef43f5fc9f1ea16cb30eeb31cee478b` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/r3/invocation_intent.json` | 2661 | `13b8970ac6b91a11997f25a5162d418a90386da6fe8bc4682a3ecbb01c50bcb4` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/r3/launcher.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/r3/proof.json` | 108717 | `8371546df21a3f06a70b9f93807f02a863df0b6290b25939385efa9e1ce39cb2` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/r3/result.json` | 55558 | `020b8b494d30da999bd21d5bb251686bb6e9a7c8d6cb2f941ce23910fa81588e` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/r3/terminal_receipt.json` | 4438 | `3164d7abe70518c7619d49d0c117b014e37661015ae67320bf6fcbe8ba6b8fbd` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/r3/worker.guard.json` | 4038 | `d380e9e916821ec791217478f599166569874cd46c7ea5989e8c0fc90357d939` |
| `results/validation/g4/auer2013/protocol_v3_r15_batch/stage_01/state_low_pos__scene_d020_l+200__T_100__V_m1_p1/r3/worker.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
