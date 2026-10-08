Session: DDWMR | LUNA-G4-AUER

# G4 Auer R9 profile-pin correction assignment

**Execution instruction for this session:** You are `LUNA-G4-AUER`, the executor. The user has delivered this assignment to you. Perform the work directly in the repository; do not hand it to another Luna or wait for another agent. Read `AGENTS.md`, all four canonical `research_context/` files, `docs/reviews/CODEX_G4_AUER_R8_SINGLE_QUERY_PREFLIGHT_REVIEW.md`, the R8 preflight handoff and R8 protocol first. MASTER v2.1 is authoritative.

## Objective and execution boundary

Create a **review-only R9 candidate** that repairs all six active R8 path/hash-pin mismatches and prevents the same error at build/preflight time. Preserve every R8 and earlier source, profile, manifest, fixture, probe, ledger and receipt byte-identically. Preserve the parallel G2 working tree. **Do not run query 1, any matched-query worker, a trajectory producer or the 1,944-query batch in this assignment.** Memory-only probe commands and read-only archived-proof fixtures are permitted and must be labeled as such. Do not commit or push. HOLD and all gate statuses remain unchanged.

## Required correction

1. Version the affected active sources/profiles/builder as R9. After all R9 source bytes are finalized, compute exact SHA-256 from the named files and populate the R9 guard profile's Auer worker, R3 worker, shared binding, result validator and launcher pins. Populate the Auer profile's `versioned_solver_sha256` from the finalized R9 solver. Keep process-limiter and Python executable pins checked. Do not copy R6/R7/R8 hashes based on similar filenames.
2. Add a fail-closed machine check in the R9 builder and preflight for **every active local path/hash assertion** in the Auer, R3, common and guard profiles. Include `source_path/source_sha256`, `versioned_solver_path/versioned_solver_sha256`, process-limiter and executable pairs and any other active hash-bearing reference discovered. Compare these to the active closure/manifest identities; reject duplicates, missing files, malformed hashes and mismatches. The candidate must contain a machine-readable active-pin ledger with the checked count and zero mismatches. Whole-file closure hashing alone is insufficient.
3. Rebuild the R9 source closure and transitive import audit, protocol/profile/schema/result bindings, prospective input hashes and candidate manifest. Keep the exact ordered 1,944-ID universe and every row `NOT_RUN`; keep `comparison_run=false`, matched evaluations 0, query 1 unauthorized pending a new Codex review, and batch unauthorized. Explicitly account for changed profile/source-closure hashes in both methods' first-ID static input reconstructions.
4. Refresh non-query composition fixtures and memory-only probe evidence as needed so their hashes bind the **R9** closure. These are not prospective worker measurements. Show R8/R7 preservation hashes and a focused R8→R9 source diff; confirm no method formula, MASTER plant, frozen query or resource cap was silently changed. Retain Auer 100,000 combined RHS/Jacobian calls, R3 4-MiB proof cap, and 120-second/1-GiB per-method worker guard.
5. Perform a read-only final integrity pass that would have rejected the R8 six-pin defect. Record exact paths, expected/actual hashes and independent checker result. If any binding cannot be made self-consistent, stop with a precise blocker and leave the candidate `NOT_RUN`.

## Deliverable

Write `docs/reviews/LUNA_TO_CODEX_G4_AUER_R9_PROFILE_PIN_CORRECTION_FULL_HANDOFF.md` with Finding / Evidence / Consequence / Status / Required action, new artifact paths and SHA-256 values, all active-pin results, closure/import counts, fixture/probe scope, preservation ledger and the static first-ID input hashes. State **0/1,944 queries run** and recommend GO/NO-GO for a later single-query review. Do not treat this assignment as permission to execute that query.
