# G4 Auer R5 — GitHub source index

This index is for independent review of the one frozen R4/R5 Auer-method reconstruction. Read `AGENTS.md` and the four canonical `research_context/` files first. MASTER v2.1 remains authoritative. Project status is **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**. No matched Auer batch was run (0/1,944 queries).

## Review entry points

- Request and required Markdown output: `docs/GPT_G4_AUER_R5_SOURCE_REVIEW_REQUEST.md`.
- Method and comparison protocol: `docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md`, `research/theorem_notes/G4_AUER_BASELINE_CONTRACT_v1.md`, `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v2.md`.
- R4/R5 claims and Codex audits: `docs/reviews/LUNA_TO_CODEX_G4_AUER_R4_IVP_CORE_FULL_HANDOFF.md`, `docs/reviews/CODEX_G4_AUER_R4_IVP_CORE_REVIEW.md`, `docs/reviews/LUNA_TO_CODEX_G4_AUER_R5_COMPOSITION_REPLAY_FULL_HANDOFF.md`, `docs/reviews/CODEX_G4_AUER_R5_COMPOSITION_REPLAY_REVIEW.md`.
- Proof producer and algorithmic replay: `validation/baselines/auer2013/residual_ivp.py`, `replay_ivp.py`, `rhs.py`, `piecewise.py`, `r4_worker.py`, `process_limiter.py`.
- Common predicate and R5 stored-artifact verifier: `validation/g4/common_tube.py`, `validation/scripts/verify_auer_composition_replay_v1.py`, `run_auer_composition_mutation_trials_v1.py`. Shared exact arithmetic and model mapping are under `validation/g2/`.
- Frozen input/profile: `validation/baselines/auer2013/auer_r4_ddwmr_single_case_input_v1.json`, `analytic_branch_crossing_fixture_v1.json`, `small_case_resource_profile_v2.json`, `ARITHMETIC_BACKEND_MANIFEST_v2.json`, `validation/configs/benchmark_v1.json`, `auer_r5_composition_replay_profile_v1.json`.
- R4 exact proof/evidence: `results/validation/g4/auer2013/r4_analytic_fixture_native_v2.json`, `r4_analytic_fixture_evidence_v2.json`, `r4_ddwmr_single_query_native_v2.json`, `r4_ddwmr_single_query_evidence_v2.json`.
- R5 records: `results/validation/g4/auer2013/r5_composition_replay_v1/pristine_replay_report.json`, `trial_ledger_v1.json`, `inputs/`, `trials/`, `pre_freeze_setup_attempts_v1.json`.
- Hash registries: `results/validation/g4/auer2013/r4_output_artifact_manifest_v1.json`, `r5_composition_replay_v1/r5_artifact_manifest_v1.json`, plus `source_snapshot_v10/snapshot_manifest.json` and `r5_composition_replay_v1/source_snapshot_v11/snapshot_manifest.json`.

The published active proof-critical source bytes were checked against v10/v11 manifest entries before publication. For example, SHA-256 is `3f15779ee772c7090951942186ef56ee5956d9569d2a1ff4c2f7e010646bf70f` for `residual_ivp.py`, `c8ebcb30b890090a0dcb45e6f80c93b15e1bb63f8401c33af3c288c88bfbc913` for `replay_ivp.py`, `564c0ffe608be6d0413def643a5dff7b455613c61b56f0ea42684cc7c6874d25` for `common_tube.py`, and `6ee77141052c8281a3b56d691dca46cf90141a3a24677f5b2db3e6b42f8d3fba` for the R5 verifier. The v10 manifest hash is `29ca0f22791ccc740ef377b232522dee88bbaf00367213bfc45cc07925c5bcd5`; v11 is `d6ed85d98f630889912e30baaf00314ac4069c4dc846525c639832c64ff959eb`. The R4 output registry has 34 entries; R5 has 88 entries and SHA-256 `48196f1f3ebb5cf9787c68bc98f6ad88a0678ebd92683014fe877d015f18dd44`.

## Public-source boundaries

The complete local v10/v11 snapshot trees are **not republished**. They contain duplicated historical outputs and third-party material. GitHub therefore permits checking the published proof-critical source hashes and R4/R5 output registries, but it does **not** permit an independent 720/720 or 726/726 snapshot-member recheck from this publication alone. Codex performed those local checks; an external reviewer must mark a full-snapshot audit unavailable unless given the local snapshots separately.

The primary papers are [Auer, Kiel & Rauh (2013)](https://doi.org/10.2478/amcs-2013-0055), especially printed pp. 740–742, Eqs. (27)–(43), and [Rauh & Auer (2011)](https://doi.org/10.1007/s11128-010-0165-6), printed pp. 371–372, Algorithm 1 and Eqs. (3)–(6). The [pinned public VALENCIA seed](https://github.com/ValEncIA-IVP/basic/tree/d1a09ceb3f68deb40357bdc89944b28997e9fb30) is historical context. The PDFs, third-party source/dependencies and local ZIP review bundle are not republished in this repository. If primary full text is inaccessible, record that as a source-access limit.

The two failed pre-freeze snapshot-assembly attempts lack their transient creator-source hashes and original stdout. Their provenance gap is recorded in `pre_freeze_setup_attempts_v1.json`; no verifier or IVP run occurred in those attempts. Do not infer a G4 gate result from the one R4/R5 case.
