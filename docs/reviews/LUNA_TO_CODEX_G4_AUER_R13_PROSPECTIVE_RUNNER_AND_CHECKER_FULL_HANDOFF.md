# R13 prospective runner/checker — full handoff for Codex review

Session: DDWMR | LUNA-G4-AUER  
Status: R13 prospective candidate and non-query evidence prepared; independent source review required.  
Execution status: NO-GO. No query or batch was run; R12 remains 0/1,942 attempted; R13 remains 0/10 attempted.

## Recommendation

**GO to independent Codex source review of the exact R13 candidate bytes. NO-GO to query, retry, or stage execution.** This assignment created no GO receipt. A later execution decision requires Codex review and a separate exact-scope GO receipt bound to the reviewed manifest, closure, schedule, and canonical R13 namespace.

## Scope and preserved history

Implemented the prospective R13 first-stage runner/checker and synthetic non-query contract evidence requested by `docs/CODEX_TO_LUNA_G4_AUER_R13_PROSPECTIVE_RUNNER_AND_CHECKER.md`.

- The fixed universe remains 1,944 IDs: the R9 preflight carry-in, the already-consumed R11 ID, and 1,942 R12 continuation IDs are separate strata.
- The only candidate execution scope is the exact ten remaining IDs from former R10 Stage 1, in the frozen R12 order. The consumed R11 ID is not retried or relabelled complete.
- The R13 batch root, `stage_01` directory, and `authorizations` directory do not exist. No GO receipt exists. The supplied authorization artifact is a non-executable NO-GO template.
- No query worker, R3/Auer producer, IVP, native proof replay, composition auditor, or batch execution was invoked. No commit or push occurred.
- R11 and R12 predecessor pins validated successfully. Current exact-byte hashes are listed below; R12's 420 dependency path/size/hash records are preserved in the R13 closure, and all 432 R13 closure dependencies pass current path/size/hash verification.

## Candidate artifacts and exact identities

All hashes are SHA-256 of exact file bytes.

| Role | Repository path | SHA-256 |
|---|---|---|
| Protocol candidate | `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R13_PROSPECTIVE_CANDIDATE.md` | `c0d44147d80207a2947678a950b4eed455fa7a98bfd37232e5cceae7de3e63ad` |
| Stage runner | `validation/g4/batch_stage_runner_v3_r13.py` | `0e6be68dbba7a1f3feb1ad97616c7a4ce45ddc8329a2156a7641667efa4f160f` |
| Independent read-only checker | `validation/g4/check_matched_batch_v3_r13.py` | `66e5db8ebefba3e5341d712a842b26e1efec8b30bff794edb712db3691470d01` |
| Synthetic contract fixture runner | `validation/g4/protocol_v3_r13_contract_fixtures.py` | `c7944e650f6ca757e0ecff6c1a37f0ad28883e1d0eba782c44e909e467314e3e` |
| Candidate builder | `validation/scripts/build_g4_auer_v3_r13_candidate.py` | `7dd710e53084e3fb377a8a40efd982f7b9e96d9016761a45be8296a04604756b` |
| Non-query fixture report | `results/validation/g4/auer2013/protocol_v3_r13_candidate/nonquery_conformance_v1.json` | `541972154bdebcb92771a685e4eefe74397acc8a2cabd647bff544d46a855965` |
| NO-GO authorization template | `research/benchmarks/G4_AUER_R13_STAGE_01_AUTHORIZATION_NO_GO_TEMPLATE.json` | `44796720da1d7c31758193e2850110cd803eaaa08e9f13167d5c0bcc10e43e26` |
| R13 manifest candidate | `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v13_PROSPECTIVE.json` | `a583703d84eb9285b1ff12647bbfb40c7a45e2b4b92cfba0035c8bbf49c4ba82` |
| R13 source closure | `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R13_PROSPECTIVE.json` | `3ed81f9fd5ca532ca1e51f845a1c1933cc51b918972972e669904a451bd8fbd1` |
| R13 Stage 1 schedule | `research/benchmarks/G4_AUER_R13_STAGE_01_SCHEDULE.json` | `bb50b4fda8d0bb53bd7554a6cc4147e59cb53bc0044545176d1df2015c3de075` |
| Read-only fixed-denominator summary | `results/validation/g4/auer2013/protocol_v3_r13_candidate/fixed_denominator_preflight_v1.json` | `a2ece7758eebda8fb9ec285543817853c110e3cf42d951d1357c21c1fbcf9d61` |

The manifest, closure, and schedule `.sha256` sidecars each match the exact bytes and canonical basename of their target. The manifest pins the protocol, runner, checker, fixture runner/report, builder, and NO-GO template hashes shown above.

## Predecessor lock and stage scope

The R13 builder and checker both verified the R12 R2 lock and the inherited source inventory. The 420 R12 path/size/hash records are byte-for-byte present in the R13 closure; the 376 inherited R11 path/hash records agree with R12. The R13 closure has 432 dependencies total, including 12 R13 additions. Every recorded R13 dependency currently matches its path, size, and SHA-256.

| Predecessor | Manifest SHA-256 | Source-closure SHA-256 | Schedule SHA-256 |
|---|---|---|---|
| R11 R2 | `193dbead525d1a1c2fae00920a2ff385e7281a6a28aae00e69d72ea7778d106d` | `dbe23888fac40caf518009dd96f888e1da45eace388d9ace8cffe906074cbf7b` | `212b6a09526379188acad46aa05070626b5248a76bc64047d18dd47f9c136e9c` |
| R12 continuation R2 | `1cd84aa55de7d9f85b66ae18e53c121f1a2a46ff23d4d1add45d7b40c84e9104` | `dcea79c74218145ae9d87ef429b7c3ab9b1299d2ba73dbe5c14fe72b6dbb01a9` | `24c65838b62ea6c12d1377f00dd543752ad9090131881a4441b6ce56232cc8ca` |

The R9 preflight carry-in remains `state_low_neg__scene_d020_l-200__T_020__V_m1_m1` (historical R9 artifact ledger pin: `f3d4733400bd6348ef56a5212f3d29ffee974a97787fe1111fe1859d2e9533c9`). The immutable R11-consumed ID is `state_low_mid__scene_d020_l+000__T_050__V_m1_0`. Neither is an R13 attempt.

The first R13 stage is `r13_continuation_01`, with 10 IDs and ordered-ID digest `58a888845732cc7a9215d3b54f0786e91c5fbd7848661cef32fced9155d1a3043` under UTF-8 LF join with no trailing newline:

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

The other six R12 groups remain in the denominator but outside this R13 launch scope. Automatic advancement, retries, and ID substitution are disabled.

## Non-query verification performed

The following checks completed successfully after the final source edits:

1. `python -m py_compile` on the R13 runner, checker, fixture runner, and builder.
2. `python -m validation.g4.protocol_v3_r13_contract_fixtures --project-root . --output <unique tmp report>`: `PASS_ALL_NONQUERY_CONTRACT_FIXTURES`, 31/31 fixture expectations matched (6 accepted synthetic contract cases; 25 Class 3 rejections). Query workers, producers/IVPs, native proof replays, and composition auditors invoked: 0. The report records the final checker, runner, and fixture-runner hashes.
3. `python -m validation.scripts.build_g4_auer_v3_r13_candidate --replace-unreviewed-candidate`: `R13_CANDIDATE_BUILT_NO_GO`; first stage 10 IDs; 420 R12 dependencies inherited and checked; R13 dependencies 432; R12 and R13 attempted IDs 0; query workers invoked 0; GO receipt created false.
4. `python -m validation.g4.batch_stage_runner_v3_r13 --project-root . --verify-only`: `R13_SOURCE_SCHEDULE_NO_GO_PREFLIGHT_PASS`; 1,944-ID universe and 1,942 R12 continuation IDs verified; first-stage count 10; R13 attempts 0; output namespace not created; workers, producers, and auditors invoked 0; GO receipt false.
5. `python -m validation.g4.check_matched_batch_v3_r13 --project-root . --verify-unstarted`: independent checker returned `R13_SOURCE_SCHEDULE_NO_GO_PREFLIGHT_PASS`, with 0 attempts and no worker/producer/auditor invocation.
6. `python -m validation.g4.check_matched_batch_v3_r13 --project-root . --output results/validation/g4/auer2013/protocol_v3_r13_candidate/fixed_denominator_preflight_v1.json`: wrote the deterministic, read-only summary. Status `READ_ONLY_REPLAY_COMPLETE`; `r13_attempted=0`; worker, producer, and auditor counts 0.
7. Independent hash inspection confirmed all 432 R13 closure dependency path/size/hash tuples, all 420 inherited R12 records, all 376 R11 path/hash pins, and all three R13 freeze sidecars.

### Exact synthetic fixture outcomes

Accepted contract fixtures (all use synthetic bytes; none are scientific certificates):

| Fixture | Observed outcome |
|---|---|
| positive proof/common/audit contract fixture | `CLASS_1_VERIFIED_CERTIFICATE` |
| no-common UNKNOWN without auditor | `CLASS_2_AUTHENTICATED_UNKNOWN` |
| proof-complete common UNKNOWN with auditor | `CLASS_2_AUTHENTICATED_UNKNOWN` |
| authenticated inclusion-not-established terminal | `CLASS_2_AUTHENTICATED_INCLUSION_NOT_ESTABLISHED` |
| authenticated wall-limit termination | `CLASS_2_AUTHENTICATED_RESOURCE_LIMIT` |
| authenticated memory-limit termination | `CLASS_2_AUTHENTICATED_RESOURCE_LIMIT` |

Rejected contract fixtures (each observed `REJECT_CLASS_3`):

| Fixture | Observed outcome |
|---|---|
| common UNKNOWN without required audit | `REJECT_CLASS_3` |
| no-common UNKNOWN missing explicit not-applicable record | `REJECT_CLASS_3` |
| no-common UNKNOWN rejects any launched-audit intent | `REJECT_CLASS_3` |
| missing favorable proof | `REJECT_CLASS_3` |
| missing favorable common record | `REJECT_CLASS_3` |
| missing favorable audit | `REJECT_CLASS_3` |
| altered result bytes | `REJECT_CLASS_3` |
| altered result size record | `REJECT_CLASS_3` |
| altered common bytes | `REJECT_CLASS_3` |
| altered common size record | `REJECT_CLASS_3` |
| altered proof bytes | `REJECT_CLASS_3` |
| altered proof size record | `REJECT_CLASS_3` |
| wrong query binding | `REJECT_CLASS_3` |
| wrong method-input binding | `REJECT_CLASS_3` |
| wrong R9 source pin | `REJECT_CLASS_3` |
| wrong GO receipt pin | `REJECT_CLASS_3` |
| duplicate intent/retry artifact | `REJECT_CLASS_3` |
| unresolved write-once intent | `REJECT_CLASS_3` |
| missing wall-job termination proof | `REJECT_CLASS_3` |
| missing memory-limit termination marker | `REJECT_CLASS_3` |
| missing memory worker exit evidence | `REJECT_CLASS_3` |
| mismatched resource terminal receipt | `REJECT_CLASS_3` |
| resource terminal cannot claim favorable common PASS | `REJECT_CLASS_3` |
| reordered/skipped stage IDs | `REJECT_CLASS_3` |
| cross-stage auto-advance namespace | `REJECT_CLASS_3` |

### Fixed-denominator preflight output

`fixed_denominator_preflight_v1.json` has SHA-256 `a2ece7758eebda8fb9ec285543817853c110e3cf42d951d1357c21c1fbcf9d61`. The checker reports:

- universe: 1,944;
- R9 preflight observed stratum: 1;
- R11 consumed observed stratum: 1;
- R12 continuation: 1,942;
- R13 first stage planned: 10; attempted: 0; not run: 10;
- remaining R12 IDs outside this R13 candidate: 1,932;
- stage status: `NOT_STARTED`;
- for both R3 and Auer: class 1 = 0, class 2 UNKNOWN = 0, class 2 resource limit = 0, class 2 inclusion-not-established = 0, class 3 = 0, NOT_RUN = 10; audit PASS/not-applicable/rejected/unresolved = 0.

No historical stratum enters an R13 yield. The summary reports no observed conditional yield (`null` denominator) and does not treat UNKNOWN as unsafe or a method failure.

## Corrections made while validating the candidate

Non-query checks caught and the final candidate source fixes the following preparation defects:

1. R11 dependency entries had path/hash fields; R12 adds `size_bytes`. The builder now checks inherited R11 path/hash pins while separately verifying each R12 size/hash against the current file, instead of requiring the old and new record dictionaries to have identical fields.
2. The candidate builder and R13 checker initially compared an ordered-ID digest to the exact-byte R10 schedule-file hash. Both now compare the locked schedule file hash to the R10 pin. ID order and group digests are independently verified from the R11/R12 schedules.
3. The candidate builder had one incorrect module alias reference; corrected before the successful build.
4. The checker’s unstarted-stage branch lacked zero-valued class-3 and audit counters, which prevented fixed-denominator summary generation. The branch now emits the complete counter schema; the read-only summary command then completed successfully.

The final fixture report, candidate build, both preflight paths, and summary were rerun after these corrections. The current hashes above are the final candidate identities for review.

## Remaining review gates and limits

- Independent Codex source review remains required for the exact R13 manifest, closure, schedule, protocol, runner, checker, builder, NO-GO template, fixture source, and fixture report.
- Synthetic acceptance cases validate only receipt/checker contract behavior. No live R3/Auer run, native proof replay, composition audit, or resource-limited worker termination was exercised here.
- No stage is authorized. Do not run query 1, retry either historical ID, continue any later stage, or infer a G4 result from these fixtures.
- R12 remains **0/1,942 attempted**; R13 first stage remains **0/10 attempted**.

