# GPT scientific review request — G4 Auer R5, one proof-backed DDWMR composition

**Repository:** `NADUNGVN/ddwmr-actuator-safety`  
**Review branch:** `main` at the publication commit supplied by Codex in the handoff message. Record the exact commit SHA you read.  
**Authority:** MASTER v2.1  
**Current status:** HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED  
**Review input:** inspect the repository files on `main` directly. Start with `docs/reviews/G4_AUER_R5_GITHUB_SOURCE_INDEX.md` for paths and publication limits. No ZIP upload is needed.

## Task

Conduct an independent, source-level scientific review of the **single frozen R4/R5 Auer-method reconstruction**, then decide whether its proof-producing method and artifact composition are sufficiently sound to begin a separately controlled matched comparison. Do not execute the 1,944-query batch, modify the plant, propose G3/controller/hardware work, or promote a gate based on this one case.

Read in this order:

1. `AGENTS.md` and all four files in `research_context/`; MASTER v2.1 prevails over handoffs.
2. The primary [Auer 2013 paper](https://doi.org/10.2478/amcs-2013-0055) and [Rauh–Auer 2011 paper](https://doi.org/10.1007/s11128-010-0165-6); check printed page/equation locators. The project does not republish their PDFs. Treat any source you cannot actually read as inaccessible. The [pinned public VALENCIA seed](https://github.com/ValEncIA-IVP/basic/tree/d1a09ceb3f68deb40357bdc89944b28997e9fb30) is historical context, not the implemented R4 method.
3. `docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md`, `research/theorem_notes/G4_AUER_BASELINE_CONTRACT_v1.md`, and `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v2.md`.
4. Published proof-critical source in `validation/baselines/auer2013/`, `validation/g4/`, `validation/g2/`, and `validation/scripts/verify_auer_composition_replay_v1.py`. Compare source hashes to the v10/v11 snapshot manifests. The complete local v10/v11 snapshot trees are not republished on GitHub because they duplicate prior outputs and retained third-party material; do not claim a full 720/726-member snapshot recheck from GitHub alone.
5. Exact R4 native analytic/DDWMR proof records and evidence, R5 pristine replay report, 17-trial ledger and trial files, selected input/benchmark/profiles, published v10/v11 manifests, R4 output manifest, R5 registry and pre-freeze setup-attempt record under `results/validation/g4/auer2013/`.
6. Luna R4/R5 handoffs and Codex R4/R5 reviews as claims to audit, not as authority.

## Questions to resolve

1. **Method mapping.** Does the implemented residual step meet the relevant Auer 2013 Eq. (42)–(43) and Rauh–Auer 2011 Algorithm 1 inclusion obligations for this continuous piecewise `clip` specialization? State precisely where the reconstruction differs from published VALENCIA software, and whether the label “paper-faithful method reconstruction” is defensible.
2. **Mathematical inclusion.** Is the 21-coordinate interval Jacobian on `Q = x_app([0,h]) + R_old` a valid enclosure of all required secants of the DDWMR vector field, including both clip corners, rational parameter-image correlations and trigonometric terms? Does `D_new ⊆ D_old` with the integrated-tube inclusion establish a full-time tube and separately propagated endpoint for every fixed label realization? Identify any hidden strictness, regularity, continuation, or parameter-switching issue.
3. **Arithmetic and replay.** Inspect the exact-rational interval/Taylor primitives and the independent `replay_ivp.py` route. Distinguish algorithmic replay independence from the shared arithmetic dependency. Audit the analytic switch fixture and the selected DDWMR proof values sufficiently to support or reject the `PROOF_COMPLETE` claim; do not infer soundness merely from stored flags.
4. **Composition.** Does R5 actually read the saved proof, replay it, derive `NATIVE_TOTAL_HULL` segments, recompute the common predicate and compare the entire saved composition? Check no radius is added twice, labels/time/endpoint/action are bound, positive collision/contact margins have the stated meaning, and all 17 file-based mutations are classified accurately. Keep `PASS_ON_SUPPLIED_TUBE`, native proof replay and a safety certificate separate.
5. **Provenance and resources.** Check the published proof-critical source hashes against the v10/v11 manifests, R4/R5 output hash chains, guarded resource records, and the two pre-freeze setup failures. Full local snapshot membership is not independently available from the GitHub publication; assess that limit separately. Assess the effect of missing transient source hashes/raw stdout for the setup failures. Do not overstate complete provenance.
6. **Comparison fairness and G4.** Is the frozen G4 protocol sufficiently matched on query universe, formal plant, uncertainty, full-time predicates, status categories and resource accounting to permit a future batch? If not, give exact corrections that can be made without changing R4/R5 outcomes or cherry-picking. Generic predictor/validation and parametric-IVP originality remain blocked unless a distinct useful DDWMR-specific result is demonstrated.

For every material finding use **Finding / Evidence / Consequence / Status / Required action**. Separate analytic soundness, finite replay, computational usefulness, method-comparison fairness, novelty and physical transfer. Use `VALID`, `PARTIAL`, `UNVERIFIED` or `BLOCKER` precisely. A sufficient test returning UNKNOWN is not evidence of actual unsafety or method failure.

## Required deliverable

Create one **downloadable Markdown file** named exactly:

`GPT_TO_CODEX_G4_AUER_R5_SCIENTIFIC_REVIEW_FULL_HANDOFF.md`

Write the complete review into that `.md` file and return the file, not only a chat summary. Include the exact `main` commit, reviewed file hashes/manifest identity, source/equation locators, explicit acceptance or rejection of the restricted R4/R5 claims, unresolved obligations, a go/no-go disposition for starting a *separately frozen* matched batch, and unchanged gate status unless authoritative evidence truly warrants a different decision. If a published file or primary source is inaccessible, identify it and leave affected conclusions UNVERIFIED.

The expected default project disposition is **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**. Neither one accepted Auer case nor a future matched batch automatically establishes G4 novelty or authorizes G3/GO.
