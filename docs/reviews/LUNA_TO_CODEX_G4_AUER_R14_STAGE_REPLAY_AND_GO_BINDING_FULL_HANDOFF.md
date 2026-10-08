# G4 Auer R14 stage replay and GO-binding corrections — full handoff

Session: DDWMR | LUNA-G4-AUER  
Status: R14 prospective candidate prepared for independent Codex review; execution remains NO-GO.  
Execution: no live query, retry, stage, Codex GO decision, or canonical GO receipt was created. R13 remains 0/10 attempted; R12 continuation remains 0/1,942 attempted.

## 1. Scope completed

Read the controlling R13 review at `docs/reviews/CODEX_G4_AUER_R13_PROSPECTIVE_RUNNER_AND_CHECKER_REVIEW.md`, its R13 handoff and protocol, the R14 assignment, `AGENTS.md`, and all four canonical research-context files. Implemented the R14 stage-replay and exact-scope review-decision corrections in new R14 files. R9, R11, R12, and R13 artifacts were left unchanged. No commit or push was made.

R14 retains the fixed 1,944-ID universe, separate R9 and R11 observed strata, the 1,942-ID R12 continuation order, and the exact ten-ID first-stage prefix. R14 is a prospective source candidate only; no execution authority is included.

## 2. Stage replay correction

The R14 checker handles `STOPPED_BEFORE_FIRST_INTENT` before requiring ten completed rows. It accepts that stage-level stop only when the original stage intent, exact GO authorization and review links, terminal receipt, and all counters reconcile, with:

- no attempted IDs and an empty progress ledger;
- no query output directories;
- zero method intents, worker-guard launches, or unresolved worker launches;
- zero audit intents, audit-guard launches, or unresolved audit launches;
- ten `NOT_RUN` rows for each method.

The checker now binds stage intent and stage terminal records to the exact candidate hashes, stage/order digest, authorization path/hash, review Markdown path/hash, and review-decision JSON path/hash. A terminal must reconcile those identities, the attempted-ID prefix, output directories, method order, intent/launch counters, pair outcomes, and the stage stop disposition. A stage-level class-3 stop must identify the final attempted ID and class-3 method outcome. If R3 is class 3, any Auer output namespace is rejected. A missing stage terminal is raised as unresolved class 3. An unresolved method or audit intent is class 3. The runner provides a read-only completion replay and refuses restart for stopped or unresolved state.

The corrected R3-before-Auer branch also removes the prior undefined counter reference and does not apply the ten-row completion guard before checking a zero-attempt prelaunch terminal.

## 3. Exact-scope GO decision binding

Added `G4_AUER_R14_CODEX_REVIEW_DECISION_SCHEMA.json` and a separate null-pinned NO-GO decision template. For a later execution, a machine-readable Codex decision must bind the exact R14 manifest, source closure, schedule, runner, checker, stage ID, ten ordered IDs, count, and ordered-ID digest. It must link the exact review Markdown path/hash, and the review must link back to the same decision artifact.

The checker requires one matching machine-readable marker in the review, the exact line `R14 stage decision: GO`, and rejects a conflicting explicit NO-GO disposition. The GO receipt is accepted only at the canonical R14 authorization path and only when its candidate pins, stage scope, caps, output namespace, and review/decision path+hash links match. Unrelated reviews, NO-GO reviews, missing candidate pins, wrong stage IDs, wrong ordered IDs, or a wrong digest fail closed.

The only checked-in authorization artifacts are the non-executable NO-GO templates. The fixture suite creates synthetic GO-shaped review/decision/receipt records only inside temporary directories to exercise the production validators; these are clearly marked fixture-only, do not cite the live candidate hashes, are not Codex decisions, are not under the canonical authorization namespace, and are removed automatically. No actual Codex GO decision or executable authorization receipt was created.

## 4. Non-query evidence

`python -m py_compile` completed successfully for the R14 checker, runner, fixture runner, and candidate builder.

`validation/g4/protocol_v3_r14_contract_fixtures.py` completed with **50/50 expected outcomes**: 11 accepted fixture behaviors and 39 expected class-3 rejections. Coverage includes the existing method-bundle contract plus:

- prelaunch failure before the first method intent, zero-attempt replay, ten `NOT_RUN` rows, and restart refusal;
- an unresolved R3 intent classified class 3 before Auer;
- a complete ten-ID stage with class-1/2 pairs, R3 class 2 followed by Auer class 1, then continuation to the next ID;
- a complete stage containing an authenticated resource-limit class 2;
- an unresolved audit intent classified class 3 and stopped before Auer;
- parent interruption with a method intent but no stage terminal;
- rejection of hidden unresolved-audit counts, reordered prefixes, stage auto-advance, mismatched stage/review links, and changed candidate pins;
- negative exact-scope review-decision checks for unrelated review, explicit NO-GO disposition, missing manifest/closure/schedule pins, wrong stage ID, wrong ordered IDs, and wrong digest.

Fixture report counts: workers 0; producers/IVPs 0; native proof replays 0; composition auditors 0; live query inputs 0; batch-runner invocations 0; canonical R14 authorization/GO receipt created: false. Positive fixture data is contract-only and is not scientific or matched-result evidence.

After the final source edit, rebuilt the fixture report and R14 candidate, then ran:

1. `python -m validation.scripts.build_g4_auer_v3_r14_candidate --replace-unreviewed-candidate` — `R14_CANDIDATE_BUILT_NO_GO`, 10 scheduled IDs, 0 attempted, 420 inherited R12 dependencies checked, 448 total closure dependencies, no worker or GO receipt.
2. `python -m validation.g4.batch_stage_runner_v3_r14 --project-root . --verify-only` — `R14_SOURCE_SCHEDULE_NO_GO_PREFLIGHT_PASS`, fixed universe 1,944, R12 continuation 1,942, R14 attempts 0, output namespace not created, worker/producer/auditor counts 0.
3. `python -m validation.g4.check_matched_batch_v3_r14 --project-root . --verify-unstarted` — `R14_SOURCE_SCHEDULE_NO_GO_PREFLIGHT_PASS`, R14 attempts 0, worker/producer/auditor counts 0.
4. Read-only fixed-denominator replay — `READ_ONLY_REPLAY_COMPLETE`, R14 attempted 0, R14 not run 10.
5. Independent SHA-256/path/size review of the 448 R14 closure entries, sidecars, all 420 inherited R12 dependency records, all 11 R13 handoff pins, and manifest component pins — no mismatch found.

No fixture called a worker, producer, IVP, native replay, composition auditor, or live batch runner. The only stage and authorization records produced were temporary synthetic fixture data in directories that were removed after each fixture run.

## 5. Candidate identities

All values are SHA-256 of exact file bytes.

| Artifact | Repository path | SHA-256 |
|---|---|---|
| R14 manifest | `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v14_PROSPECTIVE.json` | `2ff466a12f1a0eec341c741066c405b655fe7f51582d33eec9c3670c43cf6171` |
| R14 source closure | `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R14_PROSPECTIVE.json` | `50b13234e89993dbbfde644c642ff8a5b25147b45878fbcc5aa27cca80e4f0b9` |
| R14 Stage 1 schedule | `research/benchmarks/G4_AUER_R14_STAGE_01_SCHEDULE.json` | `c6caa2a059e47f281d4864bbb2308d3b8895f5469f012a7729a3dcf247693083` |
| R14 protocol | `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R14_PROSPECTIVE_CANDIDATE.md` | `5ca4a3b149fd94af9c72368cc861091364e4f4a587ade42863c85f3bd410a521` |
| R14 runner | `validation/g4/batch_stage_runner_v3_r14.py` | `56789799bc720b0466ffaf5728c05441f24e1167126ecee3e2685e5988051720` |
| R14 checker | `validation/g4/check_matched_batch_v3_r14.py` | `f6e7f112c732a773d12faed8d8a1a90758ef37420a3808da9ea6eec13988add5` |
| R14 synthetic fixture runner | `validation/g4/protocol_v3_r14_contract_fixtures.py` | `dd5e33af1afa770beba30de18e5cc01dd2060a43ff76f78ea42a1f860db2daf7` |
| R14 fixture report | `results/validation/g4/auer2013/protocol_v3_r14_candidate/nonquery_conformance_v1.json` | `7ee063e0081ece7261dd2048e933cced15f7cf957c3ee7418d77cd6a4f64fb70` |
| R14 candidate builder | `validation/scripts/build_g4_auer_v3_r14_candidate.py` | `3d6331fedd4eaa4d7402209d8155eb93c917c11aa04ecf6f4af5f9d33207a9b5` |
| Review-decision schema | `research/benchmarks/G4_AUER_R14_CODEX_REVIEW_DECISION_SCHEMA.json` | `6c44a9510b24f7687640e8988b42958b8ed0ecae09ac07a6904dffc25e43f472` |
| Review-decision NO-GO template | `research/benchmarks/G4_AUER_R14_CODEX_REVIEW_DECISION_NO_GO_TEMPLATE.json` | `9863b9f708e84df4cd26a58a1127dbf864dd95705e0e3d8f96d842693ba27791` |
| Stage authorization NO-GO template | `research/benchmarks/G4_AUER_R14_STAGE_01_AUTHORIZATION_NO_GO_TEMPLATE.json` | `dd19670476f50d1514616b21551bc4eea53f19948c73303c0d1cacfccc09c9ec` |
| Fixed-denominator read-only summary | `results/validation/g4/auer2013/protocol_v3_r14_candidate/fixed_denominator_preflight_v1.json` | `26c71855868076da53404030bd0ff1d3b2a7168be1ee6f75b89a52d9030db7a5` |

The manifest, closure, and schedule sidecars match their exact file bytes and canonical basenames. The 448-entry closure contains 420 unchanged inherited R12 path/size/hash records plus 28 new R14 dependency records.

### New R14 closure dependencies

The following 28 paths are the closure additions beyond the inherited R12 inventory:

```text
docs/CODEX_TO_LUNA_G4_AUER_R14_STAGE_REPLAY_AND_GO_BINDING_CORRECTIONS.md
docs/reviews/CODEX_G4_AUER_R12_CONTRACT_AND_CONTINUATION_REVIEW.md
docs/reviews/CODEX_G4_AUER_R13_PROSPECTIVE_RUNNER_AND_CHECKER_REVIEW.md
docs/reviews/LUNA_TO_CODEX_G4_AUER_R12_CONTRACT_AND_CONTINUATION_FULL_HANDOFF.md
docs/reviews/LUNA_TO_CODEX_G4_AUER_R13_PROSPECTIVE_RUNNER_AND_CHECKER_FULL_HANDOFF.md
research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v13_PROSPECTIVE.json
research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v13_PROSPECTIVE.json.sha256
research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R13_PROSPECTIVE_CANDIDATE.md
research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R14_PROSPECTIVE_CANDIDATE.md
research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R13_PROSPECTIVE.json
research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R13_PROSPECTIVE.json.sha256
research/benchmarks/G4_AUER_R13_STAGE_01_AUTHORIZATION_NO_GO_TEMPLATE.json
research/benchmarks/G4_AUER_R13_STAGE_01_SCHEDULE.json
research/benchmarks/G4_AUER_R13_STAGE_01_SCHEDULE.json.sha256
research/benchmarks/G4_AUER_R14_CODEX_REVIEW_DECISION_NO_GO_TEMPLATE.json
research/benchmarks/G4_AUER_R14_CODEX_REVIEW_DECISION_SCHEMA.json
research/benchmarks/G4_AUER_R14_STAGE_01_AUTHORIZATION_NO_GO_TEMPLATE.json
research/benchmarks/G4_AUER_R14_STAGE_01_SCHEDULE.json
research/benchmarks/G4_AUER_R14_STAGE_01_SCHEDULE.json.sha256
results/validation/g4/auer2013/protocol_v3_r13_candidate/nonquery_conformance_v1.json
results/validation/g4/auer2013/protocol_v3_r14_candidate/nonquery_conformance_v1.json
validation/g4/batch_stage_runner_v3_r13.py
validation/g4/batch_stage_runner_v3_r14.py
validation/g4/check_matched_batch_v3_r13.py
validation/g4/check_matched_batch_v3_r14.py
validation/g4/protocol_v3_r13_contract_fixtures.py
validation/g4/protocol_v3_r14_contract_fixtures.py
validation/scripts/build_g4_auer_v3_r14_candidate.py
```

The R14 lock also verifies the complete R13 closure against live dependency bytes before accepting R14. The R13 handoff's exact 11 recorded file hashes independently matched the current files:

| R13 artifact | SHA-256 |
|---|---|
| Manifest | `a583703d84eb9285b1ff12647bbfb40c7a45e2d7d8cb23119f4ed1b8b12633` |
| Source closure | `3ed81f9fd5ca532ca1e51f845a1c1933cc51b918972972e669904a451bd8fbd1` |
| Stage 1 schedule | `bb50b4fda8d0bb53bd7554a6cc4147e59cb53bc0044545176d1df2015c3de075` |
| Protocol | `c0d44147d80207a2947678a950b4eed455fa7a98bfd37232e5cceae7de3e63ad` |
| Runner | `0e6be68dbba7a1f3feb1ad97616c7a4ce45ddc8329a2156a7641667efa4f160f` |
| Checker | `66e5db8ebefba3e5341d712a842b26e1efec8b30bff794edb712db3691470d01` |
| Fixture runner | `c7944e650f6ca757e0ecff6c1a37f0ad28883e1d0eba782c44e909e467314e3e` |
| Fixture report | `541972154bdebcb92771a685e4eefe74397acc8a2cabd647bff544d46a855965` |
| Candidate builder | `7dd710e53084e3fb377a8a40efd982f7b9e96d9016761a45be8296a04604756b` |
| NO-GO authorization template | `44796720da1d7c31758193e2850110cd803eaaa08e9f13167d5c0bcc10e43e26` |
| Fixed-denominator summary | `a2ece7758eebda8fb9ec285543817853c110e3cf42d951d1357c21c1fbcf9d61` |

## 6. Frozen first-stage scope and counters

Stage ID: `r14_continuation_01`  
Ordered-ID digest (UTF-8 LF join, no trailing newline): `58a888845732cc8f5220656444d0b6ae9aa19a96eed1c014a7f907e9fac55bbd`

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

| Counter | Frozen/current value |
|---|---:|
| Fixed universe | 1,944 IDs |
| R9 preflight carry-in | 1 historical ID; excluded from R14 attempts |
| R11 consumed stratum | 1 historical ID; no retry |
| R12 continuation | 1,942 planned; 0 attempted |
| R14 first stage | 10 planned; 0 attempted; 10 `NOT_RUN` |
| Retries / substitutions | 0 / 0 |
| R14 canonical batch root | Absent |
| R14 `stage_01` / `authorizations` directories | Absent / absent |
| Canonical R14 GO receipt | Absent |

R13's canonical batch namespace is also absent. No existing R9, R11, R12, or R13 result was retried or altered.

## 7. Review limits and requested Codex action

This is a source-and-contract candidate for independent review, not permission to execute. Synthetic class-1/2 receipts do not represent scientific certificates; the suite did not run a query worker, native replay, or composition auditor. It establishes only that the reviewed source paths and receipt validators behaved as specified on synthetic, non-query fixtures. It supplies no G4 result, yield, baseline comparison, runtime estimate, safety finding, or gate promotion.

Please independently review the exact R14 manifest, closure, schedule and sidecars; protocol; runner/checker; review-decision schema and NO-GO template; stage authorization NO-GO template; fixture source/report; candidate builder; and the stage replay/GO-binding behavior. The later decision, if any, must cite the exact candidate hashes and exact first-stage scope. Until that separate review and authorization exist, the execution boundary remains NO-GO.
