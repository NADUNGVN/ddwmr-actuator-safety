# Codex to Luna — Auer baseline preflight and matched-comparison preparation

2026-09-30. Local assignment, **no commit or push**.

## 0. Start here

Working directory:

`D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`

Current branch: `luna/g2-validation-v1`; known starting HEAD:
`aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`.

Read `AGENTS.md`, all four canonical `research_context/` documents, then:

1. `docs/reviews/GPT_TO_CODEX_G2_VALIDATION_R3_SCIENTIFIC_REVIEW_FULL_HANDOFF.md`;
2. `docs/reviews/CODEX_G2_VALIDATION_R3_REVIEW.md`;
3. this assignment;
4. `docs/reviews/G4_MATCHED_PRIOR_ART_COMPARISON_v1.md`;
5. the G2 enclosure/evaluator and benchmark specifications referenced there.

The user mediates all exchanges. Do not spawn or contact other agents. Luna owns implementation; Codex/GPT review returned evidence. W1 already permits this scoped offline validation and baseline work.

**Latest user instruction supersedes older commit requirements:** everyone is using the same laptop/folder; do not commit, push, reset, clean, stash or switch branches. Preserve the untracked GPT handoff and all existing results. Do not modify sibling projects, global compiler/environment settings or global Git configuration. Use project-local builds/dependencies where needed. Existing uncommitted files are expected and are not a reason to require another permission request.

Keep **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**. The proposed canonical evidence edits in GPT's section R3-SR-09 remain proposed; this assignment does not apply them or change the plant.

## 1. Codex disposition of the received review

### Finding

The external review agrees with retaining R3 as a completed scoped synthetic computational result and prioritizes a matched existing-method comparison. No further R3 arithmetic repair or favorable hand case is presently justified.

### Evidence

R3 completed 1,944 queries: 1,196 CERTIFIED and 748 proof-complete UNKNOWN. All 140 groups admitting any certified enumerated action also certify zero voltage. The eight mixed groups are one moving state/horizon contact-bound distinction repeated across scenes. These facts and the offline timing limitation remain the basis of the next investigation.

The proposed comparator is Auer, Kiel and Rauh (2013), *A Verified Method for Solving Piecewise Smooth Initial Value Problems*, DOI [10.2478/amcs-2013-0055](https://doi.org/10.2478/amcs-2013-0055). Codex independently accessed the [primary article](https://zbc.uz.zgora.pl/repozytorium/Content/78882/download/) and inspected §4.1–4.2, Property 3 and the switching/mean-value discussion, Eqs. (40)–(43), plus the opening of §5. The paper describes a generalized-derivative extension to VALENCIA-IVP. §4.2 refers to additional solver publications for algorithmic details. These locators support selecting a candidate; they do not establish a reproduced DDWMR baseline.

Codex did not retrieve/build the pinned software archive in this turn. Its inventory/hash and missing-extension description below are GPT-reported leads to be independently checked by Luna.

### Consequence

Use this as a **method reproduction candidate**, not an already validated tool comparator. Replacing the published method with an arbitrary interval Picard routine and keeping its name would be invalid. A build failure would establish a reproduction limitation, not R3 superiority.

### Status

R3 scoped evidence accepted; baseline applicability plausible but implementation/source fidelity UNVERIFIED. No gate promotion.

### Required action

Complete the preparation, local implementation and reference validation below in one return. Produce a reviewable baseline contract before any matched DDWMR comparison output is enabled.

## 2. Work package A — source and environment audit

Primary paper: use the DOI and PDF above. Record retrieval URL/date, exact downloaded bytes/hash and version. Read §4 and all cited dependencies needed to close the actual solver algorithm; do not fill missing steps by guessing.

GPT supplied this software lead:

- repository [ValEncIA-IVP/basic](https://github.com/ValEncIA-IVP/basic/tree/d1a09ceb3f68deb40357bdc89944b28997e9fb30);
- revision `d1a09ceb3f68deb40357bdc89944b28997e9fb30`;
- `ValEncIA-basic.zip` blob `af0c6bd1bd5ac10bbdf0fc71b1d6da125f60f9db`;
- reported archive SHA-256 `1e0adfdec371a6ad74348a175b107c82640fb7129891bcca7f53db0c88f1986a`;
- reported simplified source `ValEncIA-IVP_0.92_2e.cpp`, with PROFIL/BIAS and FADBAD++ dependencies and without the specialized 2013 nonsmooth class.

Verify these claims, inspect licenses/redistribution terms and pin actual dependency versions. Retain downloads and build logs locally within the project, with a source inventory; do not publish source whose redistribution status is unknown. Do not execute uninspected installation scripts. Record compiler flags affecting floating arithmetic, interval rounding mode, optimization, architecture, compiler/runtime and build commands.

Create `docs/reviews/G4_AUER_SOURCE_AND_APPLICABILITY_v1.md` with equation-to-code mapping: source locator, mathematical operation, implementation path, adaptation, proof obligation, status. Identify whether the old core can reproduce the paper's required validator. Record every algorithmic substitution and whether it changes fidelity. Routine build portability fixes are allowed if semantics are preserved and documented.

A missing original extension is a reason to implement and audit the published extension, not to claim the basic package already includes it. If source access, licensing, dependencies or missing algorithm details prevent a faithful implementation, document the exact blocker and complete the independent preparation that remains possible.

## 3. Work package B — mathematical contract and reference implementation

### 3.1 Clip law: derive, do not smooth

Use exactly `clip(q,-1,1)`. The following elementary specialization is a **Codex-derived candidate contract**, not a substitute for the complete Auer algorithm:

For a real interval I, a conservative slope enclosure is `{0}` if I lies strictly in either saturated exterior, `{1}` if I lies strictly inside (-1,1), and `[0,1]` otherwise. The last choice includes intervals touching either threshold and intervals spanning both thresholds. For all a,b in I,

`clip(a)-clip(b) in D(I)*(a-b)`.

For a != b this follows because the secant slope is the fraction of the segment between a and b that lies in (-1,1), hence lies in [0,1]; on a single strict branch it is its constant slope. For a=b the difference is zero. Broad `[0,1]` at a threshold is conservative. Compose this scalar contract with a sound multivariate mean-value/Jacobian construction; demonstrate rather than assume that independent interval composition contains every required derivative/mean-value selection.

Crosswalk this continuous two-corner specialization to the paper's branch construction. Do not carry jump terms through a zero denominator merely because the general discontinuous formula has them; the clip jump is zero. This does not permit replacing the whole published enclosure iteration with a custom coarse method.

Write `research/theorem_notes/G4_AUER_BASELINE_CONTRACT_v1.md` covering the derivative contract, rough-domain/inclusion conditions, validated residual iteration, full-time tube and endpoint propagation, termination, rounding and resource failure semantics. Bounded iteration without a verified inclusion/fixed-point condition is UNKNOWN, not a certificate. Justify any step-size requirement, rather than assuming contraction from Lipschitz continuity alone over an arbitrary hold.

### 3.2 Same physical problem

Encode all nine physical states plus twelve constant uncertainty labels (`dot xi=0`, 21 augmented coordinates total). The added labels are bookkeeping, not measured physical states. Prove that the rational map and positive denominators remain valid. Use the original parameter image, initial boxes, common held voltage and exact clip law. No hidden switching of parameters, favorable-label selection, contact projection or smoothing is allowed. A state-only interval relaxation is permitted only as a disclosed outer enclosure.

Contact admissibility is a predicate on the full-time tube; do not differentiate its square root at saturation as part of the ODE validator. Preserve it even if the generic integrator can propagate the formal ODE outside the contact domain.

### 3.3 Implement and validate reference behavior

Use new baseline paths (suggested `validation/baselines/auer2013/`) and dedicated preflight outputs. Preserve R3 producer/checker code and artifacts. Build the pinned seed when feasible, implement the documented extension, and reproduce a published reference problem before describing the implementation as faithful. Declare reference settings and success criteria before obtaining results.

If the chosen published example involves discontinuity/hysteresis absent from clip, state the additional reference-only machinery explicitly; never add it to the DDWMR model. If the paper does not supply data sufficient for the proposed reproduction, document what is missing. Do not invent plotted reference values or claim exact numeric agreement from a visual curve.

Execute targeted checks for both clip corners, intervals crossing one/both thresholds, exact arithmetic secant bounds, multivariate mean-value inclusion, parameter augmentation, domain/inclusion rejection, outward arithmetic, invalid inputs and tampered proof data. A floating trajectory is only a diagnostic. Retain logs and machine-readable check outcomes. Shared arithmetic/models must be named; avoid calling them an independently implemented second engine.

Prepare an independently reviewable source-faithfulness and soundness note. Luna's own checks are development evidence; a second document written by the same execution model is not independent review.

## 4. Work package C — matched protocol ready for review

Create `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v1.md` and a machine-readable candidate manifest for the same **1,944 original IDs**. The input universe is already observed development data, not held-out data.

### 4.1 Common checks and representation fairness

Specify a common outward collision/contact predicate on a clearly typed full-time state/parameter enclosure. Make the adapter from each method explicit. R3 stores a center enclosure plus an error radius; the generic method may provide a direct tube or many time segments. Do not subtract a radius twice, omit it, or let one method use endpoint samples while the other must cover every time.

Preserve native R3 results as historical evidence. If a common representation/checker changes its tightness or outputs, write a separate `R3_COMMON_CHECK` result series, never overwrite native R3 certificates. Report enclosure-only versus checker-inclusive comparisons separately. If segments are used, all segments and closed boundaries must pass; time subdivision is verification work, not a voltage update.

Define comparable width measurements: full-hold hull widths for both, endpoint widths separately, and any segment metrics with a common declared aggregation. Unlike partitions must not generate an artificial sample count. Use the same physical coordinate scaling and units. Separate enclosure, post-check and total execution costs.

### 4.2 Fixed resource policy

R3 retains its existing settings: 16,384 rational bits, 1,000,000 metered arithmetic operations, 15 seconds/query. Comparator wall-time cap is also 15 seconds/query. Freeze comparator step/order/precision/subdivision/work limits before matched results. For a different numerical backend, specify its own auditable precision and counters; do not label different primitive counts “equal work.” Include initialization/caching rules and CPU/wall time, memory, function/Jacobian calls, accepted/rejected steps and subdivisions.

Reference-case debugging may precede the matched freeze. Do not use selected DDWMR result statuses to tune the comparator while calling the final protocol predeclared. If development queries are needed, list them and keep all outputs; a later revision is a new development version.

### 4.3 Claim and falsification plan

Keep all original IDs. Distinguish CERTIFIED, proof-complete UNKNOWN, resource UNKNOWN, unsupported/invalid input and implementation failure. Report per-ID margins, widths, proof checks and per-group action vectors, including zero-action coverage. No statistical independence assumption for cells or scenes.

Compare coverage/width/cost trade-offs without a post-hoc scalar winner. If the reproduced method matches or dominates R3 on this domain, report the lack of demonstrated advantage. If it fails to build or is not applicable, do not count this as a scientific win for R3. A matched development comparison alone does not prove firstness or complete G4.

## 5. Local freezing replaces commit-based freezing

The user has requested **no commits yet**. Follow that instruction without weakening source traceability:

1. Record starting HEAD, actual Git status and all relevant untracked/modified files. Never report `source_tree_clean=true` when it is false.
2. Before each reference/validation run, copy the complete scientific dependency set, configs, specifications and licenses into a versioned local source snapshot. Include transitive dependencies such as evaluator helpers and polynomial/model parsing, plus exact external-library sources or immutable source commitments and the built executable hash.
3. Store path, byte size and SHA-256 for each snapshot member; hash the manifest. Mark the run as `LOCAL_UNCOMMITTED_SNAPSHOT` with base Git revision and snapshot digest. Execute against that snapshot, or enforce hash equality of every executed source and input immediately before and after the run.
4. Store exact command, environment and runtime/binary hashes. A later source change creates a new snapshot/output directory. Preserve older failed attempts; never make a later manifest appear to predate a run.
5. Do not disable guards in the historical R3 runner or forge clean-tree metadata just to bypass its old committed-source requirement. Any new local runner belongs to the new baseline work and must disclose its snapshot protocol.

An explicit hash-bound local snapshot is sufficient for this preparation workflow. Committing or pushing it later is a separate user decision, not a prerequisite for authorized preflight work.

## 6. End of this assignment and stop conditions

This assignment includes source retrieval/audit, project-local setup, baseline/reference implementation, targeted checks, reference reproduction and a complete candidate matched protocol. **Return after those are reviewable; do not launch the 1,944-query matched baseline run yet.**

Reason: GPT's R3-SR-08 requires independent review of the new baseline's soundness/faithfulness and common checker before comparison. The previous R3 review cannot validate code that has not yet been written. This is a scientific prerequisite for baseline evidence, not a renewed code-permission request. There is no prohibition on completing all useful preflight work now under W1.

Stop only the affected branch if inclusion, corner handling, fixed-label semantics, source faithfulness, rounding or checker agreement fails. Preserve evidence and continue independent documentation/setup tasks. Do not silently select another baseline, smooth the plant, change the R3 grid or construct G3 to work around a blocker.

## 7. Required return file

Create:

**`docs/reviews/LUNA_TO_CODEX_G4_AUER_PREFLIGHT_FULL_HANDOFF.md`**

It must be complete enough for the user to relay once to Codex/GPT. Include:

- starting revision, local status, source-snapshot manifests and exact run paths; **no final commit is expected**;
- source/license/dependency inventory with verified versus GPT-reported claims distinguished;
- equation-to-code crosswalk and full-time proof obligations;
- all adaptations, unresolved assumptions and complete reference-case outcomes;
- check commands/results and failure logs, with no fabricated independent review;
- candidate common-checker and matched protocol, work/precision limits and frozen-input plan;
- explicit readiness: `READY_FOR_INDEPENDENT_BASELINE_REVIEW` or precise `BLOCKED/PARTIAL` with evidence;
- all local paths changed, including untracked files, and any external downloads/build outputs;
- proposed evidence-only context diff, if useful, **as a separate proposal**, without editing authoritative assumptions or gate statuses;
- **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**.

No commit, push or autonomous agent handoff. Return the absolute Markdown path to the user.
