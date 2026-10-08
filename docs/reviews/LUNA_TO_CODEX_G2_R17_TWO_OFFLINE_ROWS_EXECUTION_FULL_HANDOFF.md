Session: DDWMR | LUNA-G2-SCOPE

# G2 R17 two offline rows — execution handoff

**Date:** 2026-10-05  
**Disposition:** `DONE` — one authorized R17 stage completed, indices 62 then 74, with no retry. The R5 800-row study remains `NOT_RUN`.

## Scope and authorization

The run followed `docs/CODEX_TO_LUNA_G2_R17_TWO_OFFLINE_ROWS_EXECUTION.md` and the exact Codex GO at `research/benchmarks/G2_R17_CODEX_SCOPE_DECISION_v1.json`. The GO validator accepted only the ordered R5 pair 62 then 74, at most two source-bound offline workers, zero native query calls, zero study rows, and no retry. The GO and source bytes were preserved. Before execution, the canonical stage directory was absent; the source loader and exact GO validator were used because the unstarted NO-GO audit is expected to refuse after a GO exists. The run used CPython 3.12.12. No overlapping G4 R19 stage was running.

`validation/scripts/run_g2_r17_picard_stage.py` was called once. It attempted index 62 first; that row returned `VALID_UNKNOWN`, which does not trigger the fixed stop rule, so index 74 was permitted and attempted second. Both workers completed. There was no retry, substituted row, native R3 query, or 800-row study run. The runner exit code was 0.

## Preflight identity

| Bound item | Raw SHA-256 / identity |
|---|---|
| Codex review `docs/reviews/CODEX_G2_R17_GO_ENTRYPOINT_CORRECTION_REVIEW.md` | `833bc5559b186e15210275672e656da613628a99878b51450a0f4cc976416706` |
| GO decision and stored `authorization.json` | `314dcce10a10db9c862b99694e5b1cda6e72bcae27fdabaeefa17f105a6af30f` |
| R17 candidate manifest | `a4913d3d0282de6a5d1a16c4c88e3c402a91f1c3dee2df1ea99afd44a71c6bb9` |
| R17 source closure | `5b6838c8da6ae55e33ad4b50c9182122943f669e63e0fa9d92e6a8de3b83ce86` |
| Runtime | CPython 3.12.12, 64-bit Windows |

The actual selected query IDs and pinned payload identities are:

| Order / R5 index | Query ID | Canonical query raw SHA-256 | Input payload semantic SHA-256 |
|---:|---|---|---|
| 1 / 62 | `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_L0_R0` | `38839995032bd4328a7c4d1059d2e3e674f3f3586a12f6f2d6c76842dfcfa8f0` | `aacb6dd0639c5d5c603ca227066352a9d04a1d2d0e92fc77ab3499f59f10db37` |
| 2 / 74 | `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_Lp1_Rp1` | `1bab855c36a6cba051736320002ea40370c793f57a04cc5a8454a71b79d2c858` | `b4ad72b1cf4e1fcc37de3bf3ed080ba4797e637e3f37919873df740043645c3b` |

## Worker, capture, and R11 replay results

| R5 index | Worker / transport | Capture | Independent R11 replay | Outcome |
|---:|---|---|---|---|
| 62 | started; exit 0; `WORKER_EXITED`; `PRODUCER_COMPLETED` | `CAPTURE_COMPLETE`; no overflow; stdout 230 bytes, stderr 0 bytes | replayed; `UNKNOWN`; `safety_certified=false`; `task_eligible=false` | `VALID_UNKNOWN`, `NONNEGATIVE_SAFETY_MARGIN_NOT_ESTABLISHED_ON_EVERY_SLAB` |
| 74 | started; exit 0; `WORKER_EXITED`; `PRODUCER_COMPLETED` | `CAPTURE_COMPLETE`; no overflow; stdout 232 bytes, stderr 0 bytes | replayed; `UNKNOWN`; `safety_certified=false`; `task_eligible=false` | `VALID_UNKNOWN`, `NONNEGATIVE_SAFETY_MARGIN_NOT_ESTABLISHED_ON_EVERY_SLAB` |

Both worker stderr streams were empty and both stdout streams contained a source-bound worker summary with `native_query_calls: 0` and the corresponding record hash. The runner's diagnostic cap was 65,536 bytes per stream; no capture errors or overflows were recorded.

The independent read-only call to `validation.g2.r17_execution_checker.audit_stage()` returned `status: COMPLETED`, `receipt_valid: true`, `audit_read_only: true`, `native_query_calls: 0`, and `r5_study_rows_not_run: 800`. It independently replayed both records through R11 and rebuilt the receipt. Its exact JSON output is retained at `results/validation/g2/r17_one_shot_execution_v1/independent_checker_audit_stdout.bin` (SHA-256 `4b53c8df2f474ff33633fc63257dc5ee37cd7f9920c3c129b35b1737d143c511`).

## Collision and contact margin fields

No row has a certified nonnegative collision or contact margin: R11 returned `UNKNOWN` for both. The per-slab records contain the following exact `margin_lower` values, all negative. A negative lower bound fails to establish the required nonnegative margin; it does not by itself prove physical collision or unsafe contact.

| R5 index | Slab | Stored collision `margin_lower` | Stored contact `margin_lower` |
|---:|---:|---:|---:|
| 62 | 0 | `-3/50` | `-23885717/4000000` |
| 74 | 0 | `-67047611924271/1759218604441600` | `-25852257/16000000` |
| 74 | 1 | `-3/50` | `-991988257/655360000` |

## Paired result and remaining scope

The exact paired truth-table decision is `NO_PREDECLARED_TASK_SELECTION_SEPARATION`. The broader-study preparation trigger is `false`; broader-study execution authority is `NOT_GRANTED`. The R5 denominator remains **800/800 `NOT_RUN`**. Native query calls: **0**. No safety certificate, G2 PASS, or physical-platform claim follows; `UNKNOWN` is inconclusive. The overall disposition remains HOLD, with G2/G3/G4 and physical-platform correspondence UNVERIFIED.

## Hash ledger for preserved execution evidence

All byte counts and hashes below are raw-file values. Stage files remain under `results/validation/g2/decision_domain_r17_go_entrypoint_correction_stage_v1/`; runner captures and the independent audit output remain outside the stage under `results/validation/g2/r17_one_shot_execution_v1/`.

| Artifact | Bytes | Raw SHA-256 |
|---|---:|---|
| `authorization.json` | 974 | `314dcce10a10db9c862b99694e5b1cda6e72bcae27fdabaeefa17f105a6af30f` |
| `receipt.json` | 3,015 | `52a1aaec3eadf8d729c036e7f181e4e57e702068c1d76df53b120e1a34baddef` |
| `row_00/intent.json` | 752 | `aa1afb1eac94e5958b42dbdba6f4b9d9d8e605be3c88076f4fb5614624b5f395` |
| `row_00/terminal.json` | 2,404 | `f798e4e824a749ba95b0a756b91a71690701e4c236a72aea8e2988f0cf162842` |
| `row_00/record.json` | 21,164 | `316434ab6eacb7e221eca4feb1062001a8b576b450b725bbc1246d5e744f5cf3` |
| `row_00/diagnostics/worker_stdout.bin` | 230 | `f913f67d1ff1e668fe724c3a877bb4498eaf862a4c253c89a154f193552000e7` |
| `row_00/diagnostics/worker_stderr.bin` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `row_01/intent.json` | 816 | `0d07f5d6558bc176ff1e0b3550cd1fd85f02b5428a1ba5fe5b00845d74cab811` |
| `row_01/terminal.json` | 2,404 | `74b78097640a431a8be0c26ce4305baafaba0ec98e2e51eea77358aeb4259f0a` |
| `row_01/record.json` | 35,493 | `fbb23303ff218e3ddf56453ccea7ca41a70d40f0ff1e85335341eff7e5651421` |
| `row_01/diagnostics/worker_stdout.bin` | 232 | `72d8c39db317294829773f13d56ad48af769e1870d41b88776c0b707fb4f7721` |
| `row_01/diagnostics/worker_stderr.bin` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `runner_stdout.bin` | 5,787 | `8415b32ded80b864a4577d8e9b1ae1ff35793348fae9a32d5f9255890196ae17` |
| `runner_stderr.bin` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `runner_exit_code.txt` (`0` plus newline) | 2 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `independent_checker_audit_stdout.bin` | 7,723 | `4b53c8df2f474ff33633fc63257dc5ee37cd7f9920c3c129b35b1737d143c511` |

Receipt semantic SHA-256: `a5608e619c4699743446c9ca7ea5806681684826307d9d7bce8797852194614f`. The independent checker inventory records all 16 stage files/directories, including both row directories and diagnostic directories, with no unexpected artifact. No source or G4 artifact was edited for this execution handoff. No commit or push was made.