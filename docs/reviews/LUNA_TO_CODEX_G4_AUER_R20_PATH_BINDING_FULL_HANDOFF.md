Session: DDWMR | LUNA-G4-AUER

# G4 Auer R20 path-binding correction — full handoff

**Date:** 2026-10-05  
**Disposition:** R20 is a prospective checker candidate pending Codex review. The R20 checker passes a read-only replay of the preserved R19 Stage 1 artifacts; the original R19 checker still blocks at the first path comparison.  
**Research gate:** G4 remains UNVERIFIED and overall HOLD remains in force. R20 does not accept the Auer comparison, pass G4, authorize another stage, or authorize the full batch.

## Scope and execution boundary

This work addresses the R19 mismatch between a successful worker guard’s Windows-backslash result_path and the method terminal’s forward-slash spelling. It adds a versioned path-binding helper, R20 checker, synthetic non-query fixtures, replay driver, protocol candidate, and this handoff.

Only the already saved ten R19 matched pairs were read by the checkers. The R19 Stage 1 was not rerun. No new query, worker, producer, composition audit, retry, later stage, or full-batch execution occurred. The replay report records query_invocations: 0, producer_invocations: 0, composition_audit_invocations: 0, stage_executed: false, retries: 0, and execution_authorized: false. No commit or push was made.

## Path-binding contract

The R20 helper derives the allowed path from the checker-controlled stage root, scheduled query index, method name, and required result.json filename. It then requires both the worker-guard path and method-terminal path to resolve to that exact file. The helper:

- accepts absolute Windows path spellings using either / or \, including mixed separator directions between guard and terminal;
- checks the canonical expected artifact is under the canonical stage root and is a regular file;
- rejects empty, non-string, NUL-containing, relative, or parent-traversal recorded paths;
- rejects a recorded path that escapes the stage root, names a different in-stage artifact, or resolves through a symbolic-link component;
- checks both recorded paths identify the same filesystem file as the expected result, then retains the checker’s existing size and SHA-256 validation.

Separator replacement by itself is not the acceptance rule. The normalized spelling is accepted only after containment, exact expected-location, regular-file, resolved-path, and filesystem identity checks.

## Checker replay comparison

Both commands below were read-only and used the exact preserved R19 stage root and R19 authorization receipt.

| Checker | Exit | Result |
|---|---:|---|
| Original R19 checker, validation.g4.check_matched_batch_v3_r19 | 2 | Stops at the first ordered pair, R3 path binding |
| Candidate R20 checker, validation.g4.check_matched_batch_v3_r20 | 0 | PASS; validates all 10 saved matched pairs |

Original R19 stdout:

> BLOCKED: ContractError: state_high_mid__scene_d050_l+000__T_050__V_0_0/r3: successful guard is not bound to the one result invocation

The R19 Stage 1 handoff records that guard and terminal paths use backslash and slash spellings of the same absolute path, and their result hashes and one-invocation counts agree. The R19 checker compares the raw strings, so it blocks before reviewing the rest of the stage.

R20 stdout reports PASS_R20_REPLAY_OF_R19_STAGE, stage_status: COMPLETE, completed_query_pairs: 10, and stage_safety_conclusion: ALL_TEN_PAIR_ARTIFACTS_REPLAYED. It reports no failed arm, partial or pre-intent namespace, retry, substitution, or unattempted ID. The R20 replay verifies the already stored result, proof, common-result, guard, terminal, provenance, timestamp, audit, and stage-accounting records.

After correcting the path comparison, the replay also exposed two R19 checker/schema mismatches, corrected in the R20 checker only: the pinned audit guard writes status, while R19 looked for audit_status; audit invocation counters are nested under resource_accounting, while R19 looked for them at the report root. R20 checks the emitted schema fields. No R19 artifact was rewritten or reclassified.

Replay commands recorded in the report:

- R19: C:\msys64\ucrt64\bin\python.exe -B -m validation.g4.check_matched_batch_v3_r19 --stage-root results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01 --authorization results/validation/g4/auer2013/protocol_v3_r19_candidate/authorizations/r19_continuation_01.json
- R20: C:\msys64\ucrt64\bin\python.exe -B -m validation.g4.check_matched_batch_v3_r20 --stage-root results/validation/g4/auer2013/protocol_v3_r19_batch/stage_01 --authorization results/validation/g4/auer2013/protocol_v3_r19_candidate/authorizations/r19_continuation_01.json

## Saved R19 pair outcomes

Statuses below are taken from the preserved result and composition-audit records replayed by R20. AUDIT_NOT_APPLICABLE means the R3 result was UNKNOWN and no proof-to-common audit was applicable to that method.

| # | Query ID | R3 native / common / final | R3 composition audit | Auer native / common / final | Auer composition audit |
|---:|---|---|---|---|---|
| 1 | state_high_mid__scene_d050_l+000__T_050__V_0_0 | UNKNOWN / NOT_EVALUATED / UNKNOWN | AUDIT_NOT_APPLICABLE | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 2 | state_high_pos__scene_d050_l+200__T_100__V_0_p1 | UNKNOWN / NOT_EVALUATED / UNKNOWN | AUDIT_NOT_APPLICABLE | PROOF_COMPLETE / UNKNOWN_ON_SUPPLIED_TUBE / PROOF_COMPLETE_COMMON_UNKNOWN | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 3 | state_low_neg__scene_d100_l-200__T_020__V_p1_m1 | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 4 | state_low_mid__scene_d100_l+000__T_050__V_p1_0 | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 5 | state_low_pos__scene_d100_l+200__T_100__V_p1_p1 | UNKNOWN / NOT_EVALUATED / UNKNOWN | AUDIT_NOT_APPLICABLE | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 6 | state_high_neg__scene_d200_l-200__T_020__V_m1_m1 | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 7 | state_high_mid__scene_d200_l+000__T_050__V_m1_0 | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 8 | state_high_pos__scene_d200_l+200__T_100__V_m1_p1 | UNKNOWN / NOT_EVALUATED / UNKNOWN | AUDIT_NOT_APPLICABLE | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 9 | state_low_neg__scene_d020_l-200__T_020__V_m1_0 | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |
| 10 | state_low_neg__scene_d020_l-200__T_020__V_m1_p1 | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED |

Counts in the preserved stage: R3 has 6 CERTIFIED / common PASS_ON_SUPPLIED_TUBE and 4 UNKNOWN / NOT_EVALUATED; Auer has 10 native PROOF_COMPLETE, 9 common PASS_ON_SUPPLIED_TUBE and final CERTIFIED, and 1 common UNKNOWN_ON_SUPPLIED_TUBE and final PROOF_COMPLETE_COMMON_UNKNOWN. The Auer proof-to-common audit passes for all ten; the R3 audit passes for the six applicable results. UNKNOWN remains inconclusive.

## Synthetic non-query path fixtures

Fixture report: results/validation/g4/auer2013/protocol_v3_r20_candidate/attempt_03/path_binding_fixture_report.json

| Fixture | Expected | Observed |
|---|---|---|
| Guard backslash, terminal forward slash, same allowed artifact | ACCEPT | ACCEPT |
| Guard forward slash, terminal backslash, same allowed artifact | ACCEPT | ACCEPT |
| Identical spelling for the allowed artifact | ACCEPT | ACCEPT |
| Absolute path outside stage | REJECT | REJECT — stage escape |
| Parent traversal outside stage | REJECT | REJECT — traversal component |
| Path to another artifact inside stage | REJECT | REJECT — different artifact |
| Guard and terminal both changed to the same wrong artifact | REJECT | REJECT — different artifact |
| Symlink to an outside-stage artifact | REJECT | NOT RUN — platform limit |

The first seven cases pass. Fixture report has required_cases_pass: true and confirms zero query, producer, composition-audit, or stage invocations. Symlink creation was unavailable on this Windows account (WinError 1314: A required privilege is not held by the client). The helper explicitly rejects symbolic-link components, but the symlink tamper case has not been empirically exercised in this environment; this remains a review limitation.

## R19 preservation and accounting

The replay driver’s before/after inventory comparison reports all preserved namespaces unchanged:

| R19 namespace | Files | Before inventory SHA-256 | After inventory SHA-256 | Result |
|---|---:|---|---|---|
| Stage 1 output | 282 | 47c815b95cb5d0ab8ee8eb8c4259c6f2ad1c669d04fbf7171eac8b0fbf7d3a9a | 47c815b95cb5d0ab8ee8eb8c4259c6f2ad1c669d04fbf7171eac8b0fbf7d3a9a | unchanged |
| R19 candidate namespace | 99 | 97056a0c96f23abca7c1c75095af93d902617b229311d2c4fc03aaf6dc2ab0d0 | 97056a0c96f23abca7c1c75095af93d902617b229311d2c4fc03aaf6dc2ab0d0 | unchanged |
| R19 pinned source files | 10 | 948995f3a3241ebe0d5ef7f95c2c062af932ba339e85c9b4fbf6ee5452ee747e | 948995f3a3241ebe0d5ef7f95c2c062af932ba339e85c9b4fbf6ee5452ee747e | unchanged |
| R19 source dependency closure | 575 | c3f7df045eb7c34857da1276a3118376b623a7e4dde08ea77e9c88871152a4e7 | c3f7df045eb7c34857da1276a3118376b623a7e4dde08ea77e9c88871152a4e7 | unchanged |

The R19 authorization and review bound to the preserved stage are:

| Artifact | SHA-256 |
|---|---|
| results/validation/g4/auer2013/protocol_v3_r19_candidate/authorizations/r19_continuation_01.json | 1ef1e7acbbb4376117737e0b1d601dbb7dd20185ac70a772b41418b23048fa51 |
| docs/reviews/CODEX_G4_AUER_R19_STAGE_01_REVIEW.md | b5a233a9994b12bd8dd8eabe913a298d96bc92358bd9117003dda35f82b472e0 |

Fixed-denominator accounting remains 1,944 IDs. Four historical consumed IDs remain separate from R19. R19 Stage 1 attempted and completed its authorized 10 pairs, leaving 1,930 continuation IDs not yet attempted. R20 replay added zero queries and did not alter that accounting. No retry, substitution, or later stage occurred.

## R20 candidate source ledger

The R20 source inventory recorded by the replay report is edcdbca9d45922c221defb92f1e2cd01062d2e0e37d2660f7ab803d43ff29c0c. All five pinned files and their SHA-256 sidecars were rehashed after replay; each sidecar’s digest matches the file content.

| R20 candidate file | Bytes | Content SHA-256 | SHA-256 of .sha256 sidecar |
|---|---:|---|---|
| research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R20_READONLY_REPLAY_CANDIDATE.md | 4,482 | f4f194e3da0a9f8946fb52198f8d87d962c4ceae6248ebff5ad705bc4345236c | 6bf89c0dba784421fea6f97eea6a1d87a47f5133aad0b5a891ff2d6697835f54 |
| validation/g4/check_matched_batch_v3_r20.py | 72,363 | 98673e30dd9d8d22f1288865dfecb1396081a08293ccdd95a692e5688946c821 | f17a1c8aba5b0d879ee180d6016217588d89a692b1af8a14502190f1d9031bab |
| validation/g4/protocol_v3_r20_path_binding.py | 5,303 | fe3664d0542fa856302c3bd4dec213a19d572ec928f19cdc83f49f0425dda2ec | 4934a8d6bd034265c711b1f166d6403ec6ebf8bbd35d47edaf5fe9e4b69557f3 |
| validation/g4/protocol_v3_r20_path_binding_fixtures.py | 5,698 | 3ed2166659f58f4d60627fe66807284bd9b8adc42a58e9eb3852cd72cb9dd96a | 3c522e17b70fbece9b9f4d3c00cb5071da27ea22a69f6e4fba15af735d8ce5f7 |
| validation/scripts/run_g4_auer_v3_r20_readonly_replay.py | 15,643 | 87c85b71a172ea9fd3f987a58c148cfc0f7c487a0dcc2ab62443f9cee316334c | aca4632f874641119a2d529f285b6fae748455171dc764884b00874c1f8b1fe5 |

## Replay evidence paths and hashes

All paths are project-relative to D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety.

| Evidence | Bytes | SHA-256 |
|---|---:|---|
| results/validation/g4/auer2013/protocol_v3_r20_candidate/attempt_03/r20_readonly_replay_report.json | 21,369 | a192b662a0703014c55c3f68caaac857bf04ef73b9da10ac612b118271c7955b |
| Replay-report sidecar file | 98 | d8baee0c812d83dfdb8dd2496343677d18996959b4015a945c07f5f3965ef4f6 |
| results/validation/g4/auer2013/protocol_v3_r20_candidate/attempt_03/path_binding_fixture_report.json | 3,338 | fa675599e057349629a744620276fc4d573cb5d868737a3a7aa05a7c2f971fde |
| R19 checker stdout | 134 | 98d62f7887915014c55c3f68caaac857bf04ef73b9da10ac612b118271c7955b |
| R19 checker exit-code file | 1 | d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35 |
| R20 checker stdout | 1,641 | e3cfbd46bba9df6241c689eecc1f825bc9ba7400132f62dc6ce07c86c15f2f40 |
| R20 checker exit-code file | 1 | 5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9 |
| R19 and R20 checker stderr files | 0 each | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |

Replay report: results/validation/g4/auer2013/protocol_v3_r20_candidate/attempt_03/r20_readonly_replay_report.json. Fixture report and preserved logs are in the same attempt_03 directory.

## Review disposition requested

Please review the R20 path-binding contract and its checker-only schema compatibility changes. The current evidence supports read-only acceptance of the ten preserved R19 result pairs by the R20 checker. The original R19 checker remains blocked, and the symlink fixture could not be created on this host. R20 grants no execution authority; any continuation or stage GO requires a separate review and authorization.

G4 remains UNVERIFIED. The fixed batch denominator remains 1,944. No new matched query or batch was run. No commit or push was made.
