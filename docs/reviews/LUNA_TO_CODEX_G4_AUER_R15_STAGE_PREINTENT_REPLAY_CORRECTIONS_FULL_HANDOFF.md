# G4 Auer R15 pre-intent replay corrections — full handoff

Session: DDWMR | LUNA-G4-AUER  
Status: R15 prospective candidate prepared for independent Codex review; execution remains NO-GO.  
Execution: **no new query, retry, or live stage**. R15 first stage remains 0/10 attempted; R12 continuation remains 0/1,942 attempted. No real GO decision or executable authorization receipt was created. No commit or push was made.

## 1. Assignment and review read

Read `AGENTS.md`, all four canonical `research_context` files, the R15 assignment `docs/CODEX_TO_LUNA_G4_AUER_R15_STAGE_PREINTENT_REPLAY_CORRECTIONS.md`, the R14 review `docs/reviews/CODEX_G4_AUER_R14_STAGE_REPLAY_AND_GO_BINDING_REVIEW.md`, the R14 handoff and protocol, and the exact R14 runner, checker, fixture runner, and candidate builder before changing source.

The R14 review accepted the R14 source inventory, zero-progress prelaunch replay, and exact-scope review-decision binding. It withheld GO because the R14 runner could write `prelaunch_stop` for R3 at a later ID after completed pairs, while the checker accepted that state only at an empty stage. The review also identified an empty method directory created before its invocation intent and an incorrect R13 manifest hash transcribed in the R14 handoff.

R15 is a new source candidate. R9, R11, R12, R13, and R14 reviewed artifacts and results were not edited. The R15 builder independently revalidates the R14 candidate lock and its 448 closure records; the R15 closure inherits those exact records.

## 2. R15 candidate files

| Artifact | Repository path |
|---|---|
| Protocol | `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R15_PROSPECTIVE_CANDIDATE.md` |
| Runner | `validation/g4/batch_stage_runner_v3_r15.py` |
| Independent checker | `validation/g4/check_matched_batch_v3_r15.py` |
| Non-query full-stage fixtures | `validation/g4/protocol_v3_r15_contract_fixtures.py` |
| Fixture report | `results/validation/g4/auer2013/protocol_v3_r15_candidate/nonquery_conformance_v1.json` |
| Candidate builder | `validation/scripts/build_g4_auer_v3_r15_candidate.py` |
| Manifest | `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v15_PROSPECTIVE.json` |
| Source closure | `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R15_PROSPECTIVE.json` |
| Stage 1 schedule | `research/benchmarks/G4_AUER_R15_STAGE_01_SCHEDULE.json` |
| Stage authorization template | `research/benchmarks/G4_AUER_R15_STAGE_01_AUTHORIZATION_NO_GO_TEMPLATE.json` |
| Review-decision schema | `research/benchmarks/G4_AUER_R15_CODEX_REVIEW_DECISION_SCHEMA.json` |
| Review-decision template | `research/benchmarks/G4_AUER_R15_CODEX_REVIEW_DECISION_NO_GO_TEMPLATE.json` |
| R14 handoff erratum | `docs/reviews/LUNA_TO_CODEX_G4_AUER_R14_R13_MANIFEST_HASH_ERRATUM.md` |

The R15 source closure contains 467 path/size/hash records: all 448 R14 dependencies unchanged, plus 19 R15-specific records. The R15 builder and checker retain the fixed 1,944-ID universe, the separate R9 and R11 historical strata, the exact R12 continuation order, and the same ten ordered first-stage IDs as R14.

Ordered-ID digest: `58a888845732cc8f5220656444d0b6ae9aa19a96eed1c014a7f907e9fac55bbd`.

1. `state_low_pos__scene_d020_l+200__T_100__V_m1_p1`
2. `state_high_neg__scene_d050_l-200__T_020__V_0_m1`
3. `state_high_mid__scene_d050_l+000__T_050__V_0_0`
4. `state_high_pos__scene_d050_l+200__T_100__V_0_p1`
5. `state_low_neg__scene_d100_l-200__T_020__V_p1_m1`
6. `state_low_mid__scene_d100_l+000__T_050__V_p1_0`
7. `state_low_pos__scene_d100_l+200__T_100__V_p1_p1`
8. `state_high_neg__scene_d200_l-200__T_020__V_m1_m1`
9. `state_high_mid__scene_d200_l+000__T_050__V_m1_0`
10. `state_high_pos__scene_d200_l+200__T_100__V_m1_p1`

## 3. Stop and replay behavior

### R3 before invocation intent, after any completed prefix

The runner now records one stage-level stop disposition for each completed-pair prefix length `k = 0..9`:

- `completed_pair_prefix_ids` is exactly the first `k` scheduled IDs, each independently replayed as a terminal class-1/2 pair.
- `failing_next_id` is exactly `schedule.ids[k]`, with method `r3` and failure phase `METHOD_PRE_INTENT`.
- Since no R3 invocation intent exists, the failing ID is not counted as an attempted query and no R3 worker is called for it. `attempted_query_ids` contains only the completed prefix.
- `remaining_not_run_ids` is exactly `schedule.ids[k:]`, including the failing ID and all later IDs.
- The failing query directory is either absent or contains only the retained empty `r3` method directory. The stop record binds which state occurred.
- Method/audit intents and worker/auditor launches are recomputed over the complete frozen ten-ID namespace. `pre_intent_method_namespaces_unresolved` accounts for an empty preserved method directory without inflating invocation or worker counts.
- At `k=0`, the terminal is `STOPPED_BEFORE_FIRST_INTENT`. For `k=1..9`, it is `STOPPED_AFTER_CLASS3`. Both are stopped and cannot restart or be reported as complete comparisons.

The R3 pre-intent fixture checks each of the ten prefix lengths. It includes an empty ID 1 method namespace, ID 2 after one valid pair, an empty namespace after a later prefix, absent namespaces, and the ID 10 boundary after nine valid pairs.

### Auer before invocation intent

If R3 has a terminal class-1/2 receipt and Auer fails before writing its invocation intent, the current ID is recorded as a partial class-3 pair. The R15 stop binds the completed prefix, failing ID and Auer method, plus the IDs after that partial pair as `NOT_RUN`. The R3 worker remains counted as invoked; the failing Auer method has no intent or worker launch. Its empty/absent directory is preserved and separately counted. Restart is refused.

### Audit handoff before audit intent

If R3 has returned positive proof/common artifacts but the audit handoff fails before `audit_intent.json`, the method worker remains counted as invoked. The audit intent and audit guard launch counts stay zero; `pre_intent_audit_namespaces_unresolved` records the retained empty audit directory. The method result is class 3 because the required composition replay is unresolved. Auer and later IDs are not launched, and restart is refused.

An intent file without its verifiable terminal remains an unresolved class-3 stop and is never retried. A stage namespace without its original stage intent is explicitly classified by the checker as unresolved class 3; the runner refuses restart. A stage intent without a terminal receipt is likewise class 3 and non-restartable. Unsupported bytes in a pre-intent namespace fail closed and are never deleted or treated as proof of a worker call.

## 4. Non-query fixture evidence

The R15 fixture report records **70/70 expected outcomes**: 24 accepted contract behaviors and 46 expected class-3 rejections. It includes 22 synthetic stage-orchestration runs with temporary fixture-only review/authorization shapes and patched no-op method entry points. These runs exercise the production R15 stage ledger and checker without launching workers, producers, auditors, or native replay.

Required stage cases include:

- R3 pre-intent stop replay for every completed prefix length 0–9;
- the exact first-pair then ID 2 failure case and a later-prefix failure;
- absent and empty method namespaces, including ID 1 and a later ID;
- Auer pre-intent failure after a valid R3 terminal;
- audit handoff before audit intent;
- read-only restart refusal after a stopped stage;
- a stage namespace without the initial write-once stage intent;
- negative prefix, failing-ID, remaining-`NOT_RUN`, method-counter, audit-counter, stop-phase, and candidate-link tampering.

All case records have matching `expected` and `observed` classifications. The exact report records:

- query workers: 0;
- method producers/IVPs: 0;
- native proof replays: 0;
- composition auditors: 0;
- live query inputs: 0;
- canonical/live batch-runner invocations: 0;
- synthetic worker guard launches: 0;
- synthetic audit guard launches: 0;
- canonical R15 GO/authorization receipt created: `false`.

The synthetic stage records and GO-shaped fixtures were confined to temporary directories, removed automatically after each run, and did not cite or authorize the live R15 candidate.

## 5. Exact candidate hashes

SHA-256 values below are over exact file bytes. The R15 checker independently validated the manifest, source closure, schedule sidecars, all 467 closure entries, component pins, templates, predecessor locks, and fixture source hashes.

| Artifact | SHA-256 |
|---|---|
| R15 manifest | `e02cde6dfb5c8d07cbac053ebb0db945a4961b4aa1bc383c5dbf5660d707d556` |
| R15 source closure | `0488078d3be68e8ddc3da4478553403023ee1c79e4243ac0306dac8b7765d152` |
| R15 Stage 1 schedule | `b2e833cdb20c1d31fde899373ae4d7f2332bd359cc4888d6ddb917840ae96b92` |
| R15 protocol | `56a1211268821e54fb441818acaf34bbae5d33cdf508e23a6bfb9ffa107d6c14` |
| R15 runner | `50ed4b51627661c65eff93b3e098ddaf59a4e86a72896f07af94c04478084f3e` |
| R15 checker | `23abbd52a7193ae5149474f2835e828e7b0cea9e6b74ac05deec3462a33ee01b` |
| R15 fixture runner | `dbca281ba9b5f9d4ac33b1bdde27fc5c00f782f3c8010fd75ad7c55d55cecd33` |
| R15 fixture report | `305b87717186224eab4d50ac885f9b63fd8c0e90b9112fa163e2abe128ea93d1` |
| R15 candidate builder | `a3936884766462ee6665c0399e7adf363f8134efe41c50e3bf26c7f838e798df` |
| R15 stage authorization NO-GO template | `ed894bd4693b1f151823cbd523152b23fd085fca9368abd65eb543f575b0d5d9` |
| R15 review-decision schema | `eeea42e25657eb13fb921f2f0f861140b79bcaf51d8f95ce929d20871f7675bd` |
| R15 review-decision NO-GO template | `c86ecf50c551f29b2e55276602e49720f0de8767091015eced7f0dbf04c41513` |
| R14 R13-manifest-hash erratum | `d5e441cc7d239b7a3dbce48a0a9d3975fa06f69650a716ae5116004226ab27a6` |

The R15 schedule sidecar is `b2e833cdb20c1d31fde899373ae4d7f2332bd359cc4888d6ddb917840ae96b92  G4_AUER_R15_STAGE_01_SCHEDULE.json`; the manifest and closure sidecars likewise match their respective candidate bytes and canonical basenames.

## 6. R14 predecessor and erratum

The R15 lock revalidated these R14 identities, all reported by the R14 review and confirmed from current bytes:

| R14 artifact | SHA-256 |
|---|---|
| Manifest | `2ff466a12f1a0eec341c741066c405b655fe7f51582d33eec9c3670c43cf6171` |
| Source closure | `50b13234e89993dbbfde644c642ff8a5b25147b45878fbcc5aa27cca80e4f0b9` |
| Schedule | `c6caa2a059e47f281d4864bbb2308d3b8895f5469f012a7729a3dcf247693083` |
| Runner | `56789799bc720b0466ffaf5728c05441f24e1167126ecee3e2685e5988051720` |
| Checker | `f6e7f112c732a773d12faed8d8a1a90758ef37420a3808da9ea6eec13988add5` |

The raw R13 manifest bytes hash to `a583703d84eb9285b1ff12647bbfb40c7a45e2b4b92cfba0035c8bbf49c4ba82`. The R14 handoff table transcribed `a583703d84eb9285b1ff12647bbfb40c7a45e2d7d8cb23119f4ed1b8b12633`; R14's closure and checker already used the correct value. The separate erratum records the correction. The R14 handoff itself was left byte-for-byte unchanged (raw SHA-256 `f5064132153181816b153e3f4fc2d3fef9cbf189a350be98b415bb3e5c10a1ed`).

R15 continues to record R9 carry-in 1, R11 consumed stratum 1, R12 continuation 1,942, and R15 stage 1 planned 10. R15 and R12 attempts remain zero; retries and substitutions remain zero.

## 7. Verification and execution boundary

Completed non-query checks:

1. `python -m py_compile` succeeded for the R15 runner, checker, fixture runner, and candidate builder.
2. The R15 fixture runner completed 70 expected outcomes, all matching; it recorded zero worker, producer, auditor, native-replay, live-input, or canonical batch-runner activity.
3. `python -m validation.scripts.build_g4_auer_v3_r15_candidate --replace-unreviewed-candidate` returned `R15_CANDIDATE_BUILT_NO_GO`, 10 scheduled IDs, 0 R15 attempts, 420 inherited R12 dependencies verified, and 467 total closure dependencies.
4. `python -m validation.g4.check_matched_batch_v3_r15 --project-root . --verify-unstarted` returned `R15_SOURCE_SCHEDULE_NO_GO_PREFLIGHT_PASS`, R15 attempted 0, query workers 0, producers 0, auditors 0.
5. `python -m validation.g4.batch_stage_runner_v3_r15 --project-root . --verify-only` returned `R15_SOURCE_SCHEDULE_NO_GO_PREFLIGHT_PASS`, R15 attempted 0, `output_namespace_created=false`, and `go_receipt_created=false`.
6. The R15 batch root, `stage_01`, and `authorizations` directory are absent. The R14 batch root remains absent.

No query 1, matched query, retry, batch stage, real GO decision, executable receipt, commit, or push occurred. R15 is ready for independent Codex source review only. A later execution still requires a separate exact-scope GO decision and matching canonical authorization receipt.
