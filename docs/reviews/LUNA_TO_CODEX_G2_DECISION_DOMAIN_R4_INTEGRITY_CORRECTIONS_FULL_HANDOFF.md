Session: DDWMR | LUNA-G2-SCOPE

# Luna → Codex — G2 R4 integrity corrections full handoff

**Date:** 2026-10-03  
**Assignment:** `docs/CODEX_TO_LUNA_G2_DECISION_DOMAIN_R4_INTEGRITY_CORRECTIONS.md`  
**R3 review read first:** `docs/reviews/CODEX_G2_DECISION_DOMAIN_R3_EXECUTION_PREFLIGHT_REVIEW.md`  
**Repository:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Branch / HEAD:** `main` / `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe` (unchanged)  
**Disposition:** R4 integrity candidate v1, byte-addressed input ledger, replay-enforced aggregation, non-query fixtures and one-query proposal are prepared. **NO-GO to freeze or execute a query. 800/800 rows remain `NOT_RUN`.**

## Decision summary

R4 wraps R3 v6 without changing its scientific rows, ordered actions, query profile, fixed 12-label parameter image, `1/20 m` threshold, R2 predecessor, or frozen R3 archive. A single public result path now accepts a verified R4 candidate context, raw native-R3 safety JSONL bytes, and raw provenance bytes. It reloads the candidate, verifies the closure, aligns records by query ID, replays native R3 safety, creates and replays the R2 endpoint record, then sends only internally minted replay outcomes to the locked selector. Caller-provided task/replay/threshold flags are rejected.

Every physical input line—including blank, malformed, orphan and duplicate lines—has its original stream index, input byte offset, byte length, exact bytes and raw SHA-256 recorded. The complete original stream is also retained byte-for-byte in the ledger. Output offsets have separate field names. A complete output bundle is staged in a new directory and published by one directory rename; a hash-bound commit marker is required by the verifier.

The candidate is not frozen. No task query was run, no study output was created, and no gate was advanced. The fixtures used synthetic/stub records and read-only archived R3 records only. `run_query()` invocations: **0**. The exact study count remains **800/800 `NOT_RUN`**.

## Finding 1 — R4 preserves the fixed scientific universe and R3/R2 lineage

**Finding.** R4 is an integrity/provenance wrapper over the exact R3 v6 candidate and does not change the 800 study rows or native R3 query context.

**Evidence.** The R4 manifest has schema `ddwmr-g2-decision-domain-r4-integrity-candidate-v1`, candidate status `NOT_FROZEN_NOT_AUTHORIZED_FOR_EVALUATION`, `query_status=NOT_RUN`, `evaluated=false`, and 800 rows whose status is `NOT_RUN` and whose `result_record` is null. The R4 loader requires structural equality of all 800 ordered row objects with R3 v6, uniqueness and order of all IDs, the same profile, threshold, action IDs and parameter image. It then calls the unchanged R3 v6 row adapter. The native R3 query continues to carry the semantic SHA-256 of the R3 v6 manifest in its legacy manifest field; R4 manifest and closure hashes are bound separately in every R4 aggregate/output ledger.

The exact R3 v6 manifest raw SHA-256 is `5ca87bc92429290d0c3967b3331f2a6cfec3b9482c7b5a7cc7532fbb5db20907`, semantic SHA-256 `f6744f4e5b75026c0ba83fc51740f60f75ad98bca0d5a0d72129cf54128f40fb`; its closure raw SHA-256 is `b6b5c8b91fdc7c7dbc3c3b02fefb719f5aeeeaf9576ddf7cbbd584c9864b3469`. R2 v1 manifest/closure raw hashes remain `28557ddecaf780c02801e872c247f46ff5a2c6b21da587520a82dcf5ab80e69b` / `612e592a263d7788f27f652e9a49683372e86393c2e04a662d8db126a39d8ebd`; the R2 closure still has 34 reviewed entries. The frozen pilot and compressed full-grid archive remain pinned at `fdbce2ac5587247ababc0849c5fce8f9a596c3eb2175ed277545072c06acdc43` / `352b6c67480133350a7d1bfc89334a1beff1dc27c64cfda46391af27982fa874`.

**Consequence.** R4 adds a result-integrity boundary without relabeling archived outcomes or changing a query. R3 v6 and R2 v1 remain immutable predecessors; R4 is a separate unfrozen candidate.

**Status.** VALID candidate relation. No query result is accepted and no study outcome exists.

**Required action.** Codex should verify the R4-to-R3 row equality, unchanged profile and nested R3/R2 closure relations before any later freeze review.

## Finding 2 — aggregation is reachable only through raw-byte binding and native replay

**Finding.** R4 does not expose an aggregator that counts arbitrary outcome dictionaries. Its documented public entry point is `validation.g2.offline_study_r4.aggregate_candidate_result_bytes(context, raw_safety_result_bytes, provenance_bytes)`.

**Evidence.** The entry point reloads the candidate from disk and checks that the supplied context matches the verified R4 manifest, config, profile and closure hashes. It splits only on JSONL LF boundaries while preserving CRLF/LF bytes, rejects duplicate JSON keys and non-JSON constants, reconstructs the exact input stream, re-verifies line hashes/lengths/offsets, and aligns parsed records by the exact `query_id` of each of the 800 manifest rows. It then constructs the exact query through R4 row binding plus the unchanged R3 v6 adapter.

Before an outcome can be minted for counting, R4 checks identity and native query/profile/input hashes, calls the frozen native R3 `replay_record`, and, for a proof-bearing record, derives an R2 endpoint record from that R3 proof and calls the native R2 endpoint replayer. The exact lower rational is parsed defensively and compared against the row-bound `1/20` threshold. Task success requires replayed `CERTIFIED` safety, replayed R2 endpoint evidence, and the exact threshold comparison. R4 rejects caller fields named `safety_replay_pass`, `endpoint_replay_pass`, `endpoint_threshold_met`, `terminal_progress_lower`, or task-eligibility flags; a record whose status is asserted as `TASK_ELIGIBLE` is unsupported and becomes a non-success. Exceptions, invalid rationals, malformed records, missing rows, duplicate IDs, hash mismatches, resource abstentions, `UNKNOWN` and execution failures remain in the fixed denominators.

The selector accepts internally minted `VerifiedRow` objects rather than dictionaries. Its token is only minted by the raw-byte worker after replay or while assigning an internal non-success slot. It recomputes eligibility from those validated objects; it never uses the R3 v6 dictionary aggregator that Codex identified as the blocker.

**Consequence.** A forged success flag cannot produce a selector success. Every successful selector action has a checked row identity, bound source/profile/query hashes, native R3 safety replay and native R2 endpoint replay.

**Status.** PASS for the source path and non-query adversarial fixtures. This is source/code-path evidence, not a study result or a mathematical gate pass.

**Required action.** Independently inspect the R4 worker, selector and closure proof-to-decision map. Do not accept a future study count from a direct internal function call or arbitrary dictionary.

## Finding 3 — unique-certificate coverage now requires replay-valid evidence

**Finding.** R4 separates the unique nonzero safety-certificate coverage numerator from task progress, nominal-only success and zero-only success.

**Evidence.** A zero action with raw `safety_status="UNKNOWN"` counts as integrity-valid for this numerator only when its exact row has a proof-bearing R3 result replayed by the native checker, or the exact row/hash binding passes and the R3 checker confirms `record_integrity_valid=true` and `resource_limited=true` for a proofless resource abstention. A rejected `HASH_MISMATCH`, malformed record, or replay-rejected zero result cannot count even when the raw status string says `UNKNOWN`. A nonzero `CERTIFIED` result counts only after the native R3 checker replays the bound certificate. A later endpoint failure does not erase an otherwise valid safety certificate/UNKNOWN for this distinct coverage count; task eligibility still requires the endpoint replay and threshold.

The fixtures replayed a proof-bearing archived `UNKNOWN` through the native R3 checker and confirmed it remained inconclusive. They also built a labeled synthetic resource-abstention stub from archived inputs; the native checker confirmed integrity-valid resource abstention. A zero `UNKNOWN` with a tampered profile hash was rejected as `HASH_MISMATCH` and excluded even when a separate internally replayed nonzero certificate was present. A tampered archived R3 proof was rejected by the native checker.

**Consequence.** Rejected or fabricated zero `UNKNOWN` strings cannot inflate the unique-coverage count. `UNKNOWN` remains inconclusive and is not interpreted as unsafe.

**Status.** PASS for the narrow coverage predicate and its fixtures. No 800-row coverage claim exists.

**Required action.** Codex should confirm that task, zero-only, nominal-only and unique-coverage counts remain separate and use only the locked R3/R2 predicates.

## Finding 4 — the input ledger can reconstruct every original byte; output publication is write-once

**Finding.** R4 records complete physical-line provenance and separates input offsets from output offsets.

**Evidence.** For every JSONL input physical line the ledger stores `input_stream_line_index`, `input_byte_offset`, `input_byte_length`, `raw_bytes_base64`, `input_raw_sha256`, line kind, parse error and parsed-object semantic hash where applicable. It also stores the complete stream's raw bytes, length and SHA-256, which permits byte-identical reconstruction including blank lines and any final non-newline-terminated bytes. The worker reparses each raw line and verifies its parsed-object hash before aggregation. Orphan and duplicate references point to the same preserved original line entries. Output records use only `serialized_output_byte_offset` and other explicitly serialized-output fields.

The future output writer creates `records.jsonl`, `ledger.json`, `summary.json` and `COMMIT.json` under a new staging directory. It publishes the directory by a single same-filesystem rename after all files are flushed; existing destinations are refused. The verifier refuses staging paths, missing bundle members, invalid completion markers, changed hashes, changed input ledgers, wrong output offsets or a row count other than 800. The adversarial fixture demonstrated both sequential overwrite rejection and a failure injected after records creation; the interrupted stage was not published and the verifier rejected it as a result bundle.

The result ledger binds R4 manifest raw/semantic hashes, effective config raw/semantic hashes, profile semantic hash, R4 source-closure raw/semantic hashes and native R3 context hashes. The input stream bytes and original line offsets remain inside this ledger.

**Consequence.** Blank/malformed/orphan/duplicate input evidence is retained instead of being dropped. A prior output cannot be silently overwritten and a partial records/ledger pair cannot be mistaken for a complete published run.

**Status.** PASS for synthetic in-memory input streams and temporary-directory writer fixtures. No result bundle was left in the repository.

**Required action.** Review the input-ledger fields and atomic publication contract before any real result stream is written.

## Finding 5 — fixture and real-run status are distinct; a closed runner is still missing

**Finding.** Fixture aggregation is labeled as fixture output. R4 refuses to label a stream as a study result unless a full provenance receipt and closure-bound sealed runner are present.

**Evidence.** Fixture provenance requires a fixture ID, `run_query_invocations=0`, candidate-byte bindings and the exact raw result-stream hash/length; the resulting status is `FIXTURE_ONLY_NOT_TASK_RESULTS`. A study receipt must bind the candidate manifest/config/profile/closure and exact result bytes, carry the full ordered 800 query IDs and an 800-row query-attempt ledger with each bound native query hash and exact output-line references, bind a freeze-receipt byte string, and name a runner whose source hash is in the closure under `sealed_study_runner_source`.

R4 v1 deliberately has **no sealed one-query/full-study runner source**. A synthetic study-receipt fixture therefore failed closed with `STUDY_RUNNER_NOT_IN_REVIEWED_CLOSURE`; it did not produce an aggregate. The receipt checks establish byte/hash consistency, not signer identity. The user's explicit authorization and Codex's review remain external required events and cannot be inferred from a string field. A later candidate must add and review the runner and authorized freeze receipt before any real-run status can be accepted.

**Consequence.** No real-run status can be reported from R4 v1, and R4 cannot accidentally emit the old `PRE_RUN_FIXTURE_ONLY_NO_STUDY_OUTCOMES` status for real outputs. A real run cannot be unlocked by changing a Boolean in a result dictionary.

**Status.** PASS for fixture labeling and fail-closed receipt behavior. **BLOCKER for any future freeze or query:** the sealed runner and authorization receipt do not exist yet.

**Required action.** Codex must review R4 and separately require a versioned runner/closure plus a receipt bound to exact bytes before a new user authorization can open even one query. Do not execute the first query under this assignment.

## Finding 6 — versioned freeze/one-query proposal is prepared, not authorized

**Finding.** A versioned proposal selects exactly one row and defines the bytes/evidence required for a later one-query review.

**Evidence.** Proposal: `research/benchmarks/G2_DECISION_DOMAIN_R4_FREEZE_ONE_QUERY_PROPOSAL_v1.md`, raw SHA-256 `a302c144a919a1e4501afe973593bf479e8e93f7e66064e5375c6f96d97cbabf`. It selects manifest index `0`, query `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lm1_Rm1`, state `S_LOW_NEG`, development scene `D_NEAR_CENTER`, horizon `1/4 s`, action `(-1,-1) V`, and threshold `1/20 m`. It gives the R4 manifest/config/closure hashes, native R3 context hashes, profile/parameter-image hashes, and both the canonical query hash and native R3 input-payload hash.

The proposal requires a future source at `validation/scripts/run_g2_decision_domain_r4_one_query.py`, but that runner is not yet present and therefore has no hash. It specifies that a future output must preserve the exact safety result bytes, R3 checker diagnostic, generated R2 endpoint record and R2 checker diagnostic, resource/exception details, timing semantics, and write-once output commitment. The proposal itself and this handoff are not effective evaluator inputs; a future freeze receipt must hash the accepted proposal and review as separate authorization artifacts.

**Consequence.** Codex has concrete bytes and a deterministic row to review for a later one-query stage, but there is no runner and no authorization. The selected row is only a plumbing test and cannot demonstrate voltage-selection usefulness.

**Status.** Proposal prepared. **NO-GO to freeze or query.**

**Required action.** Review this proposal with R4. If accepted, create/hash/review the exact one-query runner and freeze receipt, then wait for a separate explicit user authorization. The present assignment authorizes no query.

## Finding 7 — read-only, mismatch and adversarial checks pass without study execution

**Finding.** Candidate integrity checks and the specified non-query fixtures pass while all study rows remain `NOT_RUN`.

**Evidence.** Commands and results:

| Command | Exit | Result |
|---|---:|---|
| `python -B -m validation.scripts.build_g2_decision_domain_r4_candidate --write-candidate` | 0 | Created only the new R4 versioned config, manifest, closure and sidecars; emitted `PASS_READ_ONLY` summary after write |
| `python -B -m validation.scripts.build_g2_decision_domain_r4_candidate --check-only` | 0 | `PASS_READ_ONLY`; 57 closure inputs verified; 800 rows not run |
| `python -B -m validation.scripts.build_g2_decision_domain_r4_candidate --validate-closure-only` | 0 | `PASS_READ_ONLY`; 57 closure inputs verified; 800 rows not run |
| `python -B -m validation.scripts.verify_g2_decision_domain_r4_fixtures` | 0 | All non-query fixtures passed; 0 study queries and 0 `run_query()` invocations |
| `python -B -m validation.scripts.build_g2_decision_domain_r4_candidate --check-only --config validation/configs/g2_decision_domain_r4_mismatch_fixture_v1.json` | 2 (expected) | `SPECIFICATION_SOURCE_HASH_MISMATCH`; protected raw hashes unchanged |
| `python -B -m validation.scripts.build_g2_decision_domain_r4_candidate --validate-closure-only --config validation/configs/g2_decision_domain_r4_mismatch_fixture_v1.json` | 2 (expected) | `SPECIFICATION_SOURCE_HASH_MISMATCH`; protected raw hashes unchanged |

For each mismatch command, the fixture compared **64** guarded repository paths before/after; all raw SHA-256 dictionaries were equal. The guarded set included the R4 inputs/artifacts, R3 v6 manifest/closure and archives, R2 v1 manifest/closure, G4 R9 profile/source/worker sentinels, `.gitattributes`, and the pre-existing modified G4 source-index document.

| Adversarial case | Fixture outcome |
|---|---|
| Fake `TASK_ELIGIBLE` with caller success flags and no proof | Rejected as `MALFORMED_RECORD`; selector successes `0` |
| Zero `UNKNOWN` with tampered query/profile hash plus a replayed nonzero certificate | `HASH_MISMATCH`; excluded from unique coverage |
| Valid proof-bearing `UNKNOWN` | Read-only archived record replayed by native R3 checker; remains inconclusive |
| Proofless resource `UNKNOWN` | Synthetic diagnostic stub checked by native R3 checker as integrity-valid resource abstention; non-success |
| Nonzero `CERTIFIED` and endpoint | Read-only archived R3 certificate and generated R2 endpoint both replayed |
| Tampered archived R3 proof | Native checker rejects it |
| Malformed rational | Parser returns non-success; malformed endpoint rational is `MALFORMED_ENDPOINT_RATIONAL`; aggregate does not raise |
| Missing/duplicate/blank/malformed/orphan input lines | All 5 physical lines retained; indices `0..4`; original offsets `0, 2, 96, 188, 200`; stream reconstruction byte-identical |
| Overwrite/partial output | Existing final bundle rejected; injected post-records failure never publishes final path; staging verifier rejects it |
| Fixed denominators | `800` rows / `32` groups / `400` held-out rows / `16` held-out groups; each horizon `200` rows / `8` groups |

Archive records were only read. The resource-abstention row was a labeled synthetic stub based on archived fields; it is not a claim that the archive contains a proofless resource row. No evaluator call, 800-row query, freeze, result output, commit or push occurred.

**Consequence.** R4 checks and fixtures establish the integrity plumbing and fail-closed behavior only. They establish no task performance, voltage-selection gain, practical usefulness, or 800-row outcome.

**Status.** PASS for pre-run code-path fixtures. Study state remains exactly **800/800 `NOT_RUN`**.

**Required action.** Codex should reproduce the exact commands, inspect source closure entries and review the fixture code. Keep all fixture output labeled as fixture evidence.

## Finding 8 — source closure and candidate artifact inventory

**Finding.** The new R4 candidate and each relevant source/input have raw hashes and a proof-to-code map in the versioned source closure.

**Evidence.** Candidate and sidecar hashes:

| Artifact | Raw SHA-256 | Semantic SHA-256 |
|---|---|---|
| `validation/configs/g2_decision_domain_r4_v1.json` | `50cb4387eb436af4da903483299fc1b338820a86083ec35fd1bccfef2d5389db` | `2ef3155930bcfbcb741bfed4cef48a6c35d541ac0a1ff3b11c39c15fa47362c0` |
| Config `.sha256` sidecar | `db00a9461f0d26708617c4e5cc551f9230fc76ff93620bd79ff02d7c3d327045` | — |
| `research/benchmarks/G2_DECISION_DOMAIN_R4_MANIFEST_CANDIDATE_v1.json` | `2036404e02c32da25eb94cee803da6be4723bc67b6e23d80189d5a0e1ea0113b` | `cb5a0eeef66807a62b541c53910e2360bd9d567aecd778bfd843dee73e79aadf` |
| Manifest `.sha256` sidecar | `20413c3e002a1e43209cd89d58e90366a9b285841af012ac95deeb7052d20128` | — |
| `research/benchmarks/G2_DECISION_DOMAIN_R4_SOURCE_CLOSURE_v1.json` | `b267d0963b2e8e7d51ba5dbe852f27d0b25a417be1b85b9ae1e1c4c4aee29fcc` | `16ce9e68b36f4f0845ac482ba6e5e5e08e8c8b8ace37ac0916c923de324cfd94` |
| Closure `.sha256` sidecar | `71505d25de87082e79fd850f44d0f44ec188cb5e02ec576e8dd5352361977b29` | — |
| `validation/configs/g2_decision_domain_r4_mismatch_fixture_v1.json` | `3c06f5f4589c3ee9edf74fe481e00c762bb336b7d91dd94e8414b5bf92f8cb10` | — |

R4 source hashes:

| Source | Raw SHA-256 |
|---|---|
| `validation/g2/decision_domain_adapter_r4.py` | `4447b443db99ea2d5628865f63f19fd108a69e890aee3180d7b37567ade782b5` |
| `validation/g2/offline_study_r4.py` | `e5a7202f04f9705f3ef3cb770a28541e94a4d1c35c20103caf0ea774bb8cece8` |
| `validation/g2/decision_selector_r4.py` | `b5e2c6b83f223f5776588dab0f5bad0e0cf729db24c877d6c7cc6c6935670c0c` |
| `validation/scripts/build_g2_decision_domain_r4_candidate.py` | `e876c1b292e7b7694a4a830b9657a0af4f435ba101272bbc3c0ccfd36ccaaa3f` |
| `validation/scripts/verify_g2_decision_domain_r4_fixtures.py` | `c9e325149f6c9b9af6157a07d22b3c72fac3bc2883bc725713bb2ceb62690120` |
| `research/benchmarks/G2_DECISION_DOMAIN_R4_FREEZE_ONE_QUERY_PROPOSAL_v1.md` | `a302c144a919a1e4501afe973593bf479e8e93f7e66064e5375c6f96d97cbabf` |

The closure contains **57** path/hash entries: 15 inherited R3 v6 transitive sources, 21 inherited effective inputs/review contexts, four inherited read-only mismatch/archive fixture inputs, seven R4 effective input/review documents, five R4 code sources and the R4 config/sidecars/manifest/sidecars/mismatch fixture. Its full path/hash inventory and `proof_to_decision_map` are in `research/benchmarks/G2_DECISION_DOMAIN_R4_SOURCE_CLOSURE_v1.json`. The R3 v6 closure's 30 superseded local drafts are not relabeled effective by R4; loading the predecessor still invokes the original R3 v6 verifier over its own 70-entry closure.

The proof map connects: exact R4/R3 row binding → byte parsing/line identity → native R3 inclusion replay → R2 endpoint creation/replay → selector and unique coverage → run-status/provenance and output publication. It identifies the unchanged R3 evaluator/checker, rational/interval/model/polynomial dependencies, R2 producer/checker and the R4 worker/selector/writer for each step.

**Consequence.** The source set is inspectable and reproducibly hash-bound before any query. R4 does not modify frozen R3 evaluator/checker code, R2 predecessor artifacts, R3 v6, archive bytes or G4/Auer files.

**Status.** PASS for candidate/closure consistency and raw hashes; mathematical and execution-source acceptance remains for Codex review.

**Required action.** Codex should verify the 57 closure entries and each proof-to-code link. Treat the proposal's missing runner hash as an explicit freeze blocker.

## Scope and worktree accounting

The entry worktree was already dirty, including a modified `.gitattributes`, a modified G4 source-index review, and many untracked G4/Auer research artifacts. Those files belong to the parallel G4 lane. This task created only new G2 R4 source/config/manifest/closure/sidecar/fixture/proposal/report files listed in this handoff. No existing G4/Auer source, configuration or manifest was edited. The mismatch tests also compared the selected G4/Auer and other protected hashes before/after each failing read-only command with no change.

No branch switch, clean, commit, push, freeze, study-result write, evaluator call or `run_query()` call occurred. HEAD remains `main` at `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`.

## Final disposition — explicit later-stage recommendation

**Finding.** The R4 result boundary and ledger corrections are concrete and exercised without study execution, but the candidate has not had Codex review and has no sealed one-query runner or authorization receipt.

**Evidence.** `--check-only` and `--validate-closure-only` passed read-only; source mismatch tests failed closed with exit `2` and unchanged guarded hashes; all adversarial non-query fixtures passed; the candidate has 800 rows and all 800 remain `NOT_RUN`.

**Consequence.** R4 closes the named R3 aggregation/ledger/status gaps at the source and fixture level. It does not establish task value, useful voltage choice, a G2 gate pass, or a real-run execution chain.

**Status.** **NO-GO for a later freeze or single-query stage until Codex reviews R4, the one-query runner is created and added to a new closure, and a distinct user authorization is received.** Overall HOLD; G2 remains UNVERIFIED. Current study status: **800/800 `NOT_RUN`**.

**Required action.** Review this handoff, the R4 manifest/config/closure, the R4 worker/selector/adapter, and the versioned one-query proposal. Do not execute a query under this assignment.
