Session: DDWMR | LUNA-G4-AUER

# W2 v6 versus local Auer matched-task falsification — full handoff

**Date:** 2026-10-08, Asia/Saigon.  
**Disposition:** `TECHNICAL_INCONCLUSIVE`; the frozen comparison stopped on a v6 wrapper-to-protocol binding defect before any native producer call.  
**Final path:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety\docs\reviews\autonomous_w2\g4\LUNA_TO_CODEX_G4_W2_V6_MATCHED_TASK_FALSIFICATION_FULL_HANDOFF.md`

## Finding

The v6 and local Auer reconstruction were not validly compared. Candidate preparation, non-query mapping, path/hash checks, saved-row replay, resource-probe validation, and a v3 freeze completed. The one execution of the frozen runner stopped on the first v6 action because the worker looked for `peer_saved_row_sha256` on a protocol action that does not contain that field. The value is present in the separate outer binding. The worker stopped before writing a producer-start marker; the runner counted zero native calls, launched no Auer worker, made no retry, and released the compute lock.

This is a binding/implementation defect. It says nothing about whether the local Auer reconstruction could or could not certify the task. No cross-method action-availability or cost conclusion follows. The correct scientific classification under the frozen stop policy is **technical inconclusive; do not infer baseline unavailability or v6 superiority**.

The old G2 v6 rows were independently replayed by G4 before the new producer phase: all three saved native replays and all three common replays passed. Those are already observed development records, not fresh matched v6 execution, held-out data, or confirmation. Their result is summarized separately below for context.

## Scope frozen before the producer phase

The authoritative task is `research/autonomous_w2/g2/task_protocol_v1.json`, SHA-256 `8bc1c8fd460a62dc3f7ff1c8e4bef2dbaddbcaffbadd75d6c2c487e9e311c15a`. It specifies the reduced nine-state model `[p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R]`, the fixed clip law and constants, the full positive-width initial box, twelve independently labeled fixed parameters in `[0.9999,1.0001]`, one common 2 s voltage hold, a static circle centered at `(1/2,1/10) m` with inflated radius `3/50 m`, full-hold collision and contact admissibility, and progress `p_x(T)-p_x(0) >= 7/20 m`.

The three ordered action pairs were:

| External action | Peer G2 action | Held voltage | Canonical physical-input SHA-256 |
|---|---|---:|---|
| `W2_G4_V6_ZERO` / `W2_G4_AUER_ZERO` | `W2_G2_DEV_001_ZERO` | `(0,0)` | `dc0dcda534dd56e7a1a409977efb5c0565e25c0ca976dcebae189609c4342fa6` |
| `W2_G4_V6_NOMINAL` / `W2_G4_AUER_NOMINAL` | `W2_G2_DEV_001_NOMINAL` | `(1/2,1/2)` | `80f15195b6a29757fa4bd03a20acc0f25b82a4f7e946d6f0308984ca9d6bec4b` |
| `W2_G4_V6_ALTERNATIVE` / `W2_G4_AUER_ALTERNATIVE` | `W2_G2_DEV_001_ALTERNATIVE` | `(1,1)` | `3d5844de37384fa3f0b52b1cea6a7580f42d1b4fd84fbc2e857e5aecc593d0bb` |

Each pair was bound to one canonical physical-input digest. Mapping preflight checked 3 pairs, 9 states, 12 labels and equality of the task, initial box, label image, clip law, hold, obstacle and progress threshold; `fresh_native_calls=0`. Binding preflight passed 3/3 pairs and checked 73 v6 source/path/hash pairs, 12 Auer source/method/path/hash pairs and 8 snapshot entries; `fresh_native_calls=0`.

The primary criterion frozen in the protocol is the set of actions for which method-native replay, common full-hold collision/contact replay, and a common progress lower bound at least `7/20 m` all pass. The common progress rule intersects the closed-slab sum of `duration * interval(u*cos(theta))` with the same endpoint-displacement enclosure for both methods. The secondary metrics are common interval width and margins, proof bytes, producer/replay wall and CPU time, peak memory, and combined offline validation cost.

These three actions had already been used by G2 and therefore are **consumed development data**, not held-out inputs or confirmation. G2's native allowance remains 24/24. The compared baseline is the **local Auer-method reconstruction**, using the G4 snapshot of the residual/Picard solver and replay path; it is not the VALENCIA binary.

## Frozen methods, profiles and artifacts

- Candidate protocol: `research/autonomous_w2/g4/matched_v6_task_development_v2/protocol_v2.json`, SHA-256 `262bde676e676fa10763295f329ae0134daa2264919e33156dcd3abd758d8ecc`.
- Common benchmark: `research/autonomous_w2/g4/matched_v6_task_development_v2/benchmark_v2.json`, SHA-256 `6bdc22747e8248b1ae5eb7141c5fea0f8020e14a4e8b85529d38461bad7546f1`.
- v6 source profile: `g2_profile_centered_v6.json`, SHA-256 `8252ceecd3a07c9811fd601945d16b9f33318d120340441c3fff94b117ee03a2`; 256 slabs, degree-20 Taylor, outward 96-bit endpoints, full parameter image and no subdivision/relabeling.
- Local Auer profile: `auer_profile_v2.json`, SHA-256 `d43d05b8697900970b8259e786a110398c5e6c89acf6942abe1f7b0487e3576a`; exact rational/Taylor residual Picard method with full-hold inclusion/replay. Its internal operation/step controls are method-specific and disclosed in the profile.
- Common scorer profile: `common_profile_v2.json`, SHA-256 `7f52084e5658c733f731734b88b0019ebd097354f22858e20ceb189a45a15057`; same full-hold predicates and progress target. The Auer profile allows a 2,000,000 rational-operation combined IVP/replay/common-check budget; v6's profile has a 5,000,000 interval-operation cap. The top-level Windows Job Object envelope is equal at 60 s, 1 GiB, one process per worker, with frozen output caps. Those different internal work counters are not a matched cost superiority result.
- G4 adapters/scorer: `v6_w2_adapter_v2.py` SHA-256 `798792327dcf76f693e4d8e0ce63b7a2315d04573eae92c71d53c6e2a176dc00`; `auer_w2_adapter_v2.py` SHA-256 `ae65571913f0b7243b09f24f282a61f3d94a402b5f2db6e16db9deae5c861130`; `matched_v6_common_v2.py` SHA-256 `f56b9e1d093a3bcad74f55139dd59fdb8914f0f54bf9124f2e172858f71738f4`.
- Frozen v6 solver/checker snapshot hashes: `producer_centered_v6.py` `a6c84356595d6e3b634a86272ef278eae7034117de58075b6c1ddff601600ec4`; `checker_centered_v6.py` `f90bd5194698b1afb038a9ada28310b33eef0f11a8f00bb3afe0b50f79345458`.
- Frozen local Auer solver/replay snapshot hashes: `solver_r9_w2.py` `68ecd4b92f2d26eea936c7b1601236f464ea4aeb75873c54cdc13db5dde5bab4`; `replay_r9_w2.py` `c8ebcb30b890090a0dcb45e6f80c93b15e1bb63f8401c33af3c288c88bfbc913`; `rhs.py` `c0ae8a05c0455ea0692773466c5fa239ff374d364f51ac58438cf3e91eed1282`; `piecewise.py` `9ae8fb192d279c41cf278529907a20a91febc388707732099ecd61df5fe5797e`.
- Peer release: `coordination/autonomous_w2/g2/releases/RELEASE_v6.json`, SHA-256 `789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55`.
- Peer STATUS snapshot consumed: `coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_18.json`, SHA-256 `5151843465cbfe9685a6fdcf2a80145471536063b9868087ac85d036219d1187`.
- G2 input/criterion support read: `coordination/autonomous_w2/g2/G4_INPUT_CRITERION_SUPPORT_v1.md`, SHA-256 `7a7779550fb737622739dc40e7937d5c10475dc6e5b2e390df0e24d8f80ebda6`.
- Freeze manifest v3: `research/autonomous_w2/g4/matched_v6_task_development_v2/freeze_manifest_v3.json`, SHA-256 `b5637ae30f0e20c7cdd8621a94c323ba25db620c4531feb5b56fc5b3a97d81ff`.
- Freeze receipt v3: `results/validation/autonomous_w2/g4/matched_v6_task_development_v2/freeze_receipt_v3.json`, SHA-256 `ea9ddaa5c6c2f991c78e253f1cb0d921b69a5819ce2d15c94c7cc52491d1c18f`.
- Source closure v3: `results/validation/autonomous_w2/g4/matched_v6_task_development_v2/source_closure_v3.json`, SHA-256 `02b562d7f9bbb748efe8fa1fdb44bc29a2c63a6fc38233625771d5ccb8c7b113`.

The closure contains 78 source/evidence entries and was verified after freeze against every listed file size and hash. It includes the compact final saved-row replay summary but excludes the expanded multi-megabyte preflight output directories. The two failed pre-run freeze attempts were retained separately; they did not replace the v3 source closure. The second produced a partial `source_closure_v2.json` (19,466 bytes, SHA-256 `6685475e715926ee9424219ed21ac78f85cba8150c81d3b8d3d5c30780beee26`) before stopping; no worker used it.

The Windows Job Object probe passed before freeze: the process was assigned before resume, exactly one process was observed, peak memory was 6,430,720 bytes, and no native call was made. The freeze receipt records zero v6/Auer native calls before execution, three frozen actions each, no retries, no held-out rows, R5/800 not run, and the 1,944-query batch not run.

## Execution and replay result

The runner was invoked once using:

```powershell
python -B -m validation.autonomous_w2.g4.run_matched_v6_w2_v2
```

It acquired `coordination/autonomous_w2/COMPUTE.lock`, launched one bounded child for v6 zero, and then stopped according to the frozen `stop_after: input/source/binding defect` rule.

| Quantity | Recorded result |
|---|---:|
| v6 worker invocations | 1 |
| v6 native calls started | 0 |
| Auer worker invocations | 0 |
| Auer native calls started | 0 |
| native proof replays in the new phase | 0 |
| retries | 0 |
| later v6 actions | 0 |
| compute lock after exit | released |

Failure: `KeyError:'peer_saved_row_sha256'` at [v6_w2_worker_v2.py](/D:/Research/Teacher_Vien/projects/ddwmr-actuator-safety/validation/autonomous_w2/g4/v6_w2_worker_v2.py:44). The frozen protocol action has fields `auer_id`, input digests/bindings, `comparison_id`, `external_id`, `ordinal`, `peer_action_id`, and voltage; it has no `peer_saved_row_sha256` key. The separate v6 binding has `peer_saved_row_path` and `peer_saved_row_sha256`, and the worker already validates that binding and the actual saved-row bytes. The launch receipt therefore records `producer_start_marker_path=null` and `native_calls_counted=0`. This is a concrete G4 wrapper/protocol contract defect; it is not a method solver result.

The bounded Job Object record for the failed child reports 0.172 s wall, 0.09375 s CPU, peak memory 13,197,312 bytes, one process, process assignment before resume, and return code 30. Stdout contains the compact worker failure JSON; stderr is empty. These resource numbers describe only the failing pre-producer setup and cannot be compared as method cost.

Read-only review after the stop found two additional stale path declarations that were not exercised and did not cause this KeyError: the frozen Auer profile's descriptive `source_closure_manifest_path` still names `source_closure_v2.json`, while the freeze manifest and worker pass `source_closure_v3.json` directly; and the included generic `matched_v6_common_v2.load_freeze()` helper still names `freeze_receipt_v2.json`, with no call sites in the frozen workers. The profile field is not read by the current solver/adapter path, but the mismatch is evidence that the preflight did not validate all path-bearing profile metadata. Both declarations must be resolved and audited in any new candidate before it can be called ready.

Execution artifacts are preserved under `results/validation/autonomous_w2/g4/matched_v6_task_development_v2/v6/01_W2_G4_V6_ZERO/`. The phase receipt is `matched_phase_receipt_v3.json`, SHA-256 `cba039075e1c6d9143bae7dc3dc3b319056ad10be023e5c246049848bcb11661`. A separate post-freeze failure ledger is `matched_execution_failure_ledger_v1.json`, SHA-256 `9ef3d81f21928da458b61da97e1914fb681a77f48179beda6e37168141ff6a95`.

No new Auer native proof, v6 proof, native replay, or common replay was produced. Do not label any Auer action `UNKNOWN`, ineligible, unsupported, or failed based on this stopped phase; Auer was not launched.

## Prior saved v6 development evidence, kept separate from this phase

The read-only saved replay preflight `saved_replay_preflight_v8.json`, SHA-256 `d20c1bb699a6ffdee4afa3ba123a4e4438f883d9823e861e09db5f44e6327e75`, reports 3/3 native saved-row replays and 3/3 common replays passed, with zero fresh native calls. Each native replay recomputed 46 proof fields and 256 center slabs. The common replay re-evaluated 256 full-hold slabs and progress from the serialized tubes. Recorded work counters were explicitly not trusted in the common replay; semantic predicate fields were compared. This preflight is evidence for the saved v6 rows only and does not substitute for fresh matched worker timing.

| Previously saved v6 action | Common progress enclosure (m) | Width (m) | Minimum common collision margin (m) | Minimum common contact margin (N) | Common safety replay | Saved-row task eligible |
|---|---:|---:|---:|---:|---|---|
| `(0,0)` | `[0.177582288184, 0.240398241242]` | `0.062815953058` | `0.211762546558` | `1.985219477442` | PASS | No; upper bound below `0.35` |
| `(1/2,1/2)` | `[0.270758520755, 0.333574473811]` | `0.062815953056` | `0.124818706764` | `1.984873966584` | PASS | No; upper bound below `0.35` |
| `(1,1)` | `[0.363934753325, 0.426750706380]` | `0.062815953054` | `0.048738648906` | `1.958480522039` | PASS | Yes; lower bound at least `0.35` |

Thus the prior saved-v6 eligible set on these consumed development rows was `{(1,1)}`. It is not an observed cross-method result because there is no Auer result for these inputs from this phase. The task is synthetic; the 60-second offline cap is not an independently justified robot deadline.

The final v8 read-only replay pass took 74.844 s total across the three child jobs (25.313, 24.594, and 24.828 s); combined child CPU was 74.250 s and peak child memory was 60,911,616 bytes. The three stored G2 row files were 506,904, 506,804, and 507,414 bytes, while their serialized common records were 4,225,239, 4,228,533, and 4,231,803 bytes. These sizes are saved-development record/diagnostic sizes, not fresh method proof sizes. Per-stage replay versus common-check timings were not captured in the compact replay preflight. No successful new v6 or Auer outputs exist from which to compute comparable producer/replay cost or fresh proof size.

## Failure accounting and preserved evidence

Preflight/setup failures are recorded in `preflight_failure_ledger_v5.json`, SHA-256 `e24c150481d9668e17de00f9624674030a8a58cae7026f92bf12858b3fba2bc9`. It records 12 pre-producer events, 16 bounded read-only replay processes, and zero native producers. In sequence, the recorded events are: (1) initial candidate builder referenced an unbound snapshot digest; (2) a saved replay lookup used `comparison_id` instead of the frozen `external_id`; (3) the next saved replay parser treated rational hold string `2` as a numerator/denominator object; (4) common diagnostic work counters were compared after shared-budget accumulation; (5) serialized numerator/denominator strings were passed to `Fraction` without integer conversion; (6) three read-only child replays completed but the parent aggregate receipt was not persisted; (7) one aggregate exceeded the 1 MiB cap at 1,897,939 bytes; (8) a later compact replay preflight passed; (9) the versioned binding preflight correctly refused to overwrite its existing receipt; (10) final read-only v8 replay passed; (11) first freeze attempt failed on an undefined `snapshot` variable before closure output; and (12) second freeze attempt failed on undefined `LOCK_REL` after writing the partial v2 closure. The final v3 freeze then completed successfully.

The actual worker failure is recorded in the separate post-freeze ledger because the source closure, freeze manifest and receipt are immutable. Both freeze tracebacks are retained as `freeze_attempt_01.stderr.txt` and `freeze_attempt_02.stderr.txt`; the partial v2 closure remains in place. The successful v3 closure and receipt bind the final executable worker/runner bytes. No result or source was silently overwritten to hide a failure.

## G2 coordination and ownership

G4 read G2's sequence-18 status and the source-backed `G4_INPUT_CRITERION_SUPPORT_v1.md` above, then published both the existing mapping memo `coordination/autonomous_w2/g4/G4_TO_G2_V6_MATCHED_INPUT_MAPPING_V4.md` and the phase result `coordination/autonomous_w2/g4/G4_TO_G2_MATCHED_TASK_RESULT_v1.md`. Both use G4's own coordination prefix. No G2 source, release, STATUS, task protocol, or saved row was edited; G2 ran no producer and consumed no further native allowance.

G4's terminal STATUS pointer in `coordination/autonomous_w2/g4/STATUS.json` binds this report's SHA-256. Historical G4 status sequences and audit-state releases remain unchanged.

## Reproduction and audit commands

The non-query candidate preparation and versioned preflights are recorded in the result ledger and versioned receipts. The successful freeze can be regenerated only in a fresh versioned artifact namespace because the v3 outputs use exclusive creation. The one execution attempt and its exact output are recorded by:

```powershell
python -B -m validation.autonomous_w2.g4.run_matched_v6_w2_v2
```

Do **not** rerun that command against the current frozen candidate: it would be a retry after an implementation/binding defect and would violate the frozen stop policy. Read the immutable `freeze_manifest_v3.json`, source closure, `matched_phase_receipt_v3.json`, worker Job Object record, stdout/result, and the two ledgers to audit this finding. The historical R19/R20 artifacts were not read as comparison inputs or altered.

## Final scientific disposition

**Finding:** the frozen matched-task implementation could not start its first v6 native producer.  
**Evidence:** one bounded setup failure before the producer marker; zero v6/Auer native calls and zero new proof replays; Auer was never invoked.  
**Consequence:** the local Auer baseline's task-certificate availability and all cross-method costs remain unmeasured. The previously saved v6 eligible set `{(1,1)}` on G2 development rows does not establish an Auer gap or v6 advantage.  
**Status:** `TECHNICAL_INCONCLUSIVE`; no method contribution verdict is available from this comparison.  
**Required action:** if continuing, create a new G4-owned wrapper/protocol version that takes the saved-row hash from the separately pinned binding, add non-query fixtures for present/missing/tampered binding fields, freeze a new source closure/receipt, and obtain independent path/hash/replay preflight before any producer call. Treat the three known inputs as development again; they cannot become pristine confirmation by renaming them. The present phase is closed without retry.

Project disposition remains **HOLD; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED**. No 1,944-query batch, R5/800 run, fresh confirmation rows, retry, commit, or push occurred.
