Session: DDWMR | LUNA-G4-AUER

# G4 Auer R18 stage-stop replay and GO correction — full handoff

**Disposition: source candidate complete; NO-GO pending independent Codex review.** R18 is prepared as a new candidate. No real query, method producer, live composition audit, matched stage, stage runner, executable GO receipt, or batch was run or created. No commit or push was made.

## 1. Assignment and review basis

Read `AGENTS.md`, the four canonical `research_context` files, the R17 full handoff, and `docs/reviews/CODEX_G4_AUER_R17_COMPLETE_PROVENANCE_STAGE_REVIEW.md` before modifying R18. The R17 review accepted the narrow provenance/source preparation but blocked Stage 1 because stopped artifacts could not all be replayed, the review-hash gate did not require a GO decision, and launcher/checker reads were unbounded.

R18 addresses those source blockers while preserving R17 lineage. It is a prospective candidate only. Its manifest sets `execution_authorized`, `query_workers_authorized`, `batch_start_authorized`, and `go_receipt_created` to false.

## 2. Frozen accounting and Stage 1 scope

The fixed universe remains **1,944 IDs**. Four historical IDs stay consumed in separate strata: one R9 carry-in, one R11 attempt, and two R15 attempts. R15 remains **2/10 consumed**. R17 Stage 1 remains **0/10 attempts**. The R17 continuation contains the same ordered **1,940 never-attempted IDs**; R18 proposes its first ten without retry, substitution, or pooling. The four consumed IDs remain:

- R9 carry-in: `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`
- R11 attempt: `state_low_mid__scene_d020_l+000__T_050__V_m1_0`
- R15 attempt 1: `state_low_pos__scene_d020_l+200__T_100__V_m1_p1`
- R15 attempt 2: `state_high_neg__scene_d050_l-200__T_020__V_0_m1`

R18 proposes these first ten:

```text
state_high_mid__scene_d050_l+000__T_050__V_0_0
state_high_pos__scene_d050_l+200__T_100__V_0_p1
state_low_neg__scene_d100_l-200__T_020__V_p1_m1
state_low_mid__scene_d100_l+000__T_050__V_p1_0
state_low_pos__scene_d100_l+200__T_100__V_p1_p1
state_high_neg__scene_d200_l-200__T_020__V_m1_m1
state_high_mid__scene_d200_l+000__T_050__V_m1_0
state_high_pos__scene_d200_l+200__T_100__V_m1_p1
state_low_neg__scene_d020_l-200__T_020__V_m1_0
state_low_neg__scene_d020_l-200__T_020__V_m1_p1
```

R18 real Stage 1 is still **0/10 attempts**. The canonical output root `results/validation/g4/auer2013/protocol_v3_r18_batch` and canonical authorization receipt are absent. The 1,940-ID schedule retains the frozen `10, 34, 96, 450, 450, 450, 450` partition. All R9–R17 source, result, GO, stop, timestamp, and receipt bytes were left untouched; the R17 builder lineage check and independent hash audit verified all 525 inherited dependency records unchanged.

## 3. Candidate artifacts and independent hash ledger

| Artifact | SHA-256 of exact bytes | SHA-256 of `.sha256` sidecar |
|---|---|---|
| `research/benchmarks/G4_AUER_BATCH_FREEZE_MANIFEST_CANDIDATE_v18_PROSPECTIVE.json` | `22e95160333fcd0551b3ce83ecbaea3c91a2fb32cb988383c0ef02812b6f54bc` | `d8efefa19aca531cc5154448a74e4aace23ae6478549b53c5985c1acdb584ccc` |
| `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R18_PROSPECTIVE.json` | `3b40c3feb3c2f2d5c44735e456a4176c606ffb4235f8f416bdf5dc2a83ed0bae` | `48fa059c96ccc115f745c977968d97551c73e1394541efc64b7a1a24582862df` |
| `research/benchmarks/G4_AUER_R18_CONTINUATION_SCHEDULE.json` | `4051f7503d692395197481c673701930217286fd301953ffb026c338e76a0f48` | `216f90a4d6c012f4ca91fc4290503cf03ccd22bb5c9b0cdbf58ef984f31f7258` |
| `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v3_R18_PROSPECTIVE_CANDIDATE.md` | `29e7aa3991fe5bbaaab6a76b547b571d210a4f11cc3277481cc8488c58f377cc` | `6b5d332bbfc7e06e51256d0d8fb197480f588191cfbbd04d9100fe5dcae5ac1e` |
| `results/validation/g4/auer2013/protocol_v3_r18_candidate/nonquery_conformance_v4.json` | `ae3aa672b6bf8ea7e3d2f1e18e6c0db3c2447c764704c2fb189fe75e607c84fb` | `3f71950cc8e8411c22ee3c25b9535cda3a006a4518e85a8a25a59154cd958923` |

The independently recomputed source pins for changed R18 code are:

| Executable source | SHA-256 | SHA-256 of `.sha256` sidecar |
|---|---|---|
| `validation/g4/check_matched_batch_v3_r18.py` | `b38ed66d28adc80117d4715eed9fcc715cbc939e0d47d5bf1d136154f51c521b` | `7d06da0b4070690828d8dd45860ddb7ab0677080d5135fdbfb555752b1b3f46a` |
| `validation/g4/batch_stage_runner_v3_r18.py` | `f4a5f96d097f16eb2dda403ac2583b3367320bf7c0d5ef0db0f7fd7ed53af671` | `a58c6204e75f63d3b03ac78f773f57e120574b1ae768e77a463e6a4fc904123c` |
| `validation/g4/batch_timestamp_contract_v3_r18.py` | `5bae6675acab8b93eb05b6265c61893c045b54c7c986115a7c46c691033356cd` | `a7f7aa2ba96dc8ac96d326081069b7427075ca936b17a57d1cedee83ebd08eaf` |
| `validation/g4/protocol_v3_r18_nonquery_fixtures.py` | `54d3b0e1119b0374f720a8e3de19760e14955b07212acbde95dd7c0d5a51d2fb` | `7d61a8ef39d2b6f3ff66b3c7a20235f9fcc3d0a6421d510d13b46c49397a8787` |
| `validation/scripts/build_g4_auer_v3_r18_candidate.py` | `de1eb96401d045d1acd0a1c7a8d3738a0d77b3346c0e8832993c71387e727dc1` | `64378fd9e022d84f6bfa0b4afd9c24392220246c70c0265acef8cc31ee703d9b` |

The source closure has **549 dependency records**: all **525 R17 records** are byte-identical, plus 24 R18 lineage/candidate records. Its **20 manifest components** agree with closure path/hash entries. An independent PowerShell SHA-256 recomputation found **0 mismatches across 549/549 dependencies**, **0 differences across the 525 inherited R17 entries**, **0 component mismatches**, and **0 errors across the 10 checked sidecars**. The closure and manifest avoid circular self-hashing; their exact raw hashes and sidecars are separately listed above.

The candidate also contains the R18 authorization schema and NO-GO template, the Codex exact-scope review-decision schema and NO-GO template, and a Markdown review template. These are source/contract artifacts only. The review-decision path `docs/reviews/CODEX_G4_AUER_R18_STAGE_01_REVIEW.md` has no GO decision, and the executable receipt path has no receipt.

## 4. Stage-stop replay and checker changes

R18 versions the R17 checker and runner. The on-disk checker now accepts a correctly bound stopped stage for durable method intent without terminal, a failed guard or absent result, an audit intent without terminal, a failed audit, and a stop before the next arm's intent. It derives attempted IDs from durable method intents and checks the exact ordered prefix, stop ID, unattempted suffix, count conservation, method/audit terminal counts, no retry/substitution/auto-advance, and both partial-intent and pre-intent namespace paths. Serialized path lists use POSIX separators consistently across platforms. Launcher captures must use a recognized status and internally consistent byte counts, truncation state, raw file size, and hash; unknown capture statuses are rejected.

Any failed arm yields `NONE_STOPPED_CLASS3`; a `CERTIFIED` string in an untrusted or failed arm cannot establish a safety conclusion. A complete-stage disposition still requires all ten method pairs and accepted independent result/audit replay. Malformed stopped-stage accounting is rejected.

## 5. Exact-scope GO binding

Before creating the canonical R18 output directory, the runner verifies a receipt at the single canonical path. The receipt is bound to the exact R18 manifest, source closure, schedule, Stage 1 ID order and hash, one-shot rule, resource policy, and false retry/substitution/advance/full-batch flags.

The receipt also names a bounded Markdown Codex review file and its SHA-256. The checker parses the decision block from bounded bytes and verifies that the parsed bytes have the same digest as the receipt. The block must have exactly one decision, `reviewer=Codex`, exact scope `G4_AUER_R18_STAGE_01_ONLY`, `decision=GO`, `execution_authorized=true`, and the precise candidate/stage/resource fields. An offline fixture supplied a correctly hashed NO-GO decision with an otherwise GO-shaped receipt; the checker refused it before any stage namespace was created. No review decision or executable GO receipt was created by this work.

## 6. Resource limits and remaining enforcement limits

| Process/artifact | Frozen cap |
|---|---:|
| Method worker | 1 GiB / 120 seconds |
| Separate composition audit | 1 GiB / 120 seconds |
| R18 launcher wall time | 150 seconds |
| Captured merged launcher stdout | 1 MiB per method/audit launcher |
| Checker JSON reads | 16 MiB |
| Referenced artifact reads/hashes | 64 MiB |
| Codex review Markdown | 64 KiB |

Method and audit caps remain at the R17 values. The launcher drains output while retaining no more than 1 MiB, preserves the captured prefix and SHA-256, records byte counts/completeness, and maps overflow, timeout, or incomplete drain to a class-3 stop. Both overflow and incomplete-capture records were replayed through the full on-disk stage checker. The stage checker checks file size before loading/parsing JSON and uses capped streaming hashes for referenced files.

The existing guarded worker/auditor child uses its Windows Job Object policy. The R18 runner/checker process itself has no independent Job Object memory cap. The launcher terminates the immediate child on overflow/timeout; this candidate does not claim kernel-enforced termination or memory limits for the entire descendant process tree outside the guarded worker/auditor. JSON parser memory amplification within the explicit file caps also remains an enforcement limit and is disclosed for Codex review.

## 7. Provenance and identity separation

Common R3/Auer segments retain all five direct proof/source provenance fields:

1. `native_proof_file_sha256`
2. `source_snapshot_manifest_path`
3. `source_snapshot_manifest_sha256`
4. `source_closure_path`
5. `source_closure_sha256`

The fixture copied and separately replayed archived positive proof/result/common/guard artifacts. The R3 proof belongs to `state_high_neg__scene_d050_l-200__T_020__V_0_m1` and has SHA-256 `86d203f88e528e44670a431b5794fa5fe57f8196ac93e15d9b97dd783c93cd14`. The Auer proof belongs to `state_low_pos__scene_d020_l+200__T_100__V_m1_p1` and has SHA-256 `a0bc4d9d39c91dd4933f0219a27095d40c70fde5769cad13a483232a2ab06858`. Each copy matched its source hash and each archived proof-to-common offline audit returned `PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED`. These are **different historical IDs**; they were not paired, pooled, or treated as a matched comparison.

Numerical proof/source identity remains the R9 snapshot/closure (`fe3309d5b17c6d2968c826eaf1a0759c3b9fbf848432b72842fff5b4db726d91` and `7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533`). Existing method result artifacts retain their R17 worker/adapter identity. R18 stage intents and terminals bind the new R18 manifest, closure, and schedule; the closure pins the R18 runner/checker/fixture/builder source and their sidecars. The timestamp contract records UTC start/finish and monotonic elapsed duration; it validates UTC ordering and the start-intent binding.

## 8. Non-query fixture report and scope

The final fixture artifacts are under the noncanonical `results/validation/g4/auer2013/protocol_v3_r18_candidate/nonquery_fixture_artifacts_v8/` namespace. The final report is `results/validation/g4/auer2013/protocol_v3_r18_candidate/nonquery_conformance_v4.json`.

| Full-checker case | Replay result |
|---|---|
| Partial method intent, no method terminal | Accepted as `STOPPED_CLASS3`; records `query_01/r3/invocation_intent.json`; no safety conclusion. |
| Failed guard and absent result | Accepted as `STOPPED_CLASS3`; no completed pair and no safety conclusion. |
| Partial audit intent, no audit terminal | Accepted as `STOPPED_CLASS3`; records `query_01/r3/audit/audit_intent.json`; no safety conclusion. |
| Pre-intent audit namespace | Accepted as `STOPPED_CLASS3`; records `query_01/r3/audit`; no safety conclusion. |
| Failed composition audit | Accepted as `STOPPED_CLASS3`; the audit failure is recorded and no safety conclusion is made. |
| One synthetic complete pair, then pre-intent stop | Accepted with one fixture-only completed pair and `query_02/r3` pre-intent namespace; the overall stage remains `STOPPED_CLASS3` with no safety conclusion. |
| Malformed stop/count conservation | Rejected by the full checker. |
| Launcher stdout overflow | Accepted as a class-3 stop with the bounded 1 MiB prefix and its hash. |
| Launcher stdout incomplete capture | Accepted as a class-3 stop with its bounded partial prefix and hash. |

The complete-pair case uses synthetic result/guard/audit/intent/terminal records under `r18_fixture_synthetic_pair`, an ID outside the frozen universe. Those success-shaped records exist solely to exercise the checker path; they contain no method proof and make no scientific safety claim. Archived R3 and Auer proofs are offline interface evidence only and belong to different historical IDs. The fixture report records zero matched-query invocations, zero producers, zero live composition-audit invocations, zero stage runs, and zero GO receipts.

Earlier non-query debug namespaces `nonquery_fixture_artifacts_v1` through `nonquery_fixture_artifacts_v7` and older reports `nonquery_conformance_v1.json` through `nonquery_conformance_v3.json` were left untouched. They are noncanonical, bind earlier candidate hashes, and are superseded by the v8 fixture namespace and v4 report above; do not treat them as current R18 evidence.

## 9. Verification record

| Command/check | Result |
|---|---|
| `python -m validation.scripts.build_g4_auer_v3_r18_candidate` | `R18_PROSPECTIVE_CANDIDATE_FROZEN_NO_GO`; 549 dependencies, 20 components, 1,940 continuation IDs; execution disabled. |
| `python -m validation.g4.protocol_v3_r18_nonquery_fixtures` | `PASS_R18_NONQUERY_FIXTURES`; 9 cases; report SHA-256 `ae3aa672b6bf8ea7e3d2f1e18e6c0db3c2447c764704c2fb189fe75e607c84fb`. |
| `python -m validation.g4.check_matched_batch_v3_r18 --verify-only` | `PASS_R18_PROSPECTIVE_SOURCE_PREFLIGHT_UNSTARTED`; batch namespace and authorization receipt absent; 0 matched-query invocations, 0 stage runs, R18 Stage 1 0/10. |
| `python -m validation.g4.batch_stage_runner_v3_r18 --verify-only` | Same unstarted PASS; no stage or authorization receipt. |
| Independent PowerShell SHA-256 recomputation | 549/549 closure dependencies match; 525/525 R17 entries preserved; 20/20 component references match; 10/10 checked sidecars match. |

The bounded-output probe was a non-query Python child emitting 129 bytes against a 64-byte test cap; it preserved exactly 64 bytes and reported `OVERFLOW`. The stage-overflow fixture independently replayed a synthetic 1 MiB capped-prefix receipt through the full checker. Neither probe invoked a method worker, producer, audit guard, or R18 stage runner.

## 10. Final recommendation

**NO-GO pending Codex review.** The source candidate and bounded non-query checker evidence are ready for review. Any future Stage 1 authorization must be an explicit exact-scope Codex GO decision in the hashed review file and a matching canonical receipt. This handoff grants no execution authority.

New R18 queries: **0**. R18 Stage 1: **0/10 attempts**. Full batch: **not run**. GO receipts: **0**. Commit/push: **none**.
