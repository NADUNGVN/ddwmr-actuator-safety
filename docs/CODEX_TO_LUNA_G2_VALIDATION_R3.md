# Codex to Luna — R2 review and bounded R3 assignment

Date: 2026-09-30. Reviewed branch: `luna/g2-validation-v1`.
Reviewed HEAD: `90830712a86af8779cf7765810cea8c50ba01924`.
Pilot execution revision: `aa8cc4e17e41a70895f357f41427320c0a682c5e`.

## 0. Disposition and scope

**R2 is accepted as scoped development progress. The previously identified radius-coefficient implementation blocker is resolved by the inspected correction. Overall HOLD remains; G2/G3/G4 and physical correspondence remain UNVERIFIED.**

This is a source/artifact review, not a fresh execution of the evaluator or checker and not a proof of general implementation soundness. Codex read the returned handoff, source changes, verification routines, frozen inputs, records and reports, and independently recalculated the result-ledger hashes and grouped the recorded outcomes. Reported checker executions remain Luna's execution evidence; do not describe them as a second Codex replay.

W1 already authorizes this validation work. Continue in the same repository and branch. The user relays this file to Luna; Codex does not delegate through agents. No MASTER assumption changes, gate promotion, G3 construction, controller, closed-loop experiment or hardware work are assigned here.

## 1. Review findings

### R3-01 — corrected radius and completed proof path

**Finding:** The extra factorial division is removed. R2 now exercises the completed, nonzero-radius proof path.

**Evidence:** `_radius_series` uses the coefficient `T^(k+1)/(k+1)!` directly and updates it by multiplication by `T/(k+2)`. The new regression constructs expected coefficients separately using powers/factorials. The stored pilot contains 108 completed proofs. `dev_pilot_record_check_r2_v1.json` reports 54 positive and 54 inconclusive successful replays. `pilot_positive_tamper_check_r2_v1.json` records six nonzero radius components and rejection of three mutations on a pilot positive proof. The replay shares arithmetic, model and primitive components with the evaluator; that trusted code remains part of the validation boundary.

**Consequence:** The specific R2-01 formula blocker and the previous absence of any exercised positive/nonzero proof path are resolved in this limited review. This does not validate every future input or all shared primitives.

**Status:** ACCEPT — scoped correction and development evidence.

**Required action:** Preserve the radius regression and replay distinctions. Keep the failed standalone fixture as recorded history. Do not require that fixture to become positive merely to repeat evidence already supplied by the pilot, and do not raise its cap after its observed failure.

### R3-02 — reproducible recorded counts and hashes

**Finding:** The returned counts agree with the stored records, and the semantic hash ledger is reproducible in the current checkout.

**Evidence:** Codex independently parsed JSON/JSONL and recomputed SHA-256 under the declared canonical serialization, without importing the evaluator/checker. All **17/17** ledger entries match. The 216 records contain **54 CERTIFIED**, **54 UNKNOWN with completed proof**, and **108 UNKNOWN without proof due to RATIONAL_BIT_LIMIT**. The original denominator remains 1,944; 1,728 are NOT_RUN.

**Consequence:** There is traceable evidence of completed certificates on a subset of this synthetic development pilot. UNKNOWN is neither a collision assertion nor evidence that no admissible action exists.

**Status:** ACCEPT — artifact consistency; no full-grid or usefulness conclusion.

**Required action:** Preserve v1 and R2 artifacts and their ledgers. Write all R3 evidence to new paths.

### R3-03 — no observed voltage decision separation

**Finding:** R2 does not yet demonstrate voltage-selection value.

**Evidence:** Grouping records by the same state, scene and horizon gives 24 groups, each with nine actions. Exactly six groups have nine CERTIFIED actions; six groups have nine completed-proof UNKNOWN actions; twelve groups have nine resource-limited UNKNOWN actions. There are **zero mixed CERTIFIED/UNKNOWN groups**. This observation concerns certificate status; it does not assert that the numerical margins are voltage-independent.

**Consequence:** `54/216` is a development certification fraction, not a demonstrated advantage of choosing one voltage over another. Twelve groups remain censored by arithmetic resources, so no conclusion about their eventual action separation is justified.

**Status:** UNVERIFIED — decision-relevant usefulness.

**Required action:** Include action-group tables in R3. Report certificate status, margin range over actions, and resource censoring separately. Do not move obstacles, replace actions, prune difficult IDs or tune parameters to manufacture separation.

### R3-04 — localized arithmetic bottleneck

**Finding:** Remaining pilot resource failures are localized to the collision-distance stage.

**Evidence:** The 108 recorded failures are `collision.full_hold_margin / fraction.mul`, with pre-operation estimates 17,482–20,974 bits under the frozen 16,384-bit cap. The code squares exact rational coordinate gaps before square-root bracketing. Large accumulated denominators make this expensive. The separate positive fixture reaches the same stage with a 42,448-bit estimate under its 32,768-bit cap.

**Consequence:** This is evidence about arithmetic representation, not physical infeasibility or a defect in conservative resource guards. A sound, bounded-precision enclosure of the distance primitive is a targeted remedy worth evaluating.

**Status:** NEEDS REVISION — computational completion, not a demonstrated safety-certificate error.

**Required action:** Implement the bounded distance variant in section 2, under a new frozen profile. Do not merely raise the bit cap or disable accounting.

### R3-05 — specification and checker provenance

**Finding:** R2 improves query binding, but `specification_sha256` is named more strongly than its content warrants. Checker source provenance also needs an explicit interpretation.

**Evidence:** `make_query`/record generation and `verify_records` derive that hash from the hash-protocol ID, benchmark hash and manifest hash. The manifest includes a `benchmark_spec` path, not the contents of the mathematical specification. `source_revision_matches` in `verify_records` checks equality between records and run metadata; it does not independently identify the source executing the checker. For this reviewed return, inspection of the Git diff found no evaluator/checker changes from the pilot revision to HEAD, so this is not evidence that R2 was actually checked with incompatible code.

**Consequence:** The current field binds a configuration bundle. It is not a direct content commitment to all governing equations, nor is revision-string equality a checker-source attestation. This provenance limitation does not by itself refute any of the 54 positive records.

**Status:** NEEDS REVISION — metadata semantics and future reproducibility.

**Required action:** Version the next schema. Preserve interpretation of historical R2 fields. Bind actual specification contents and distinguish producer/checker revisions as set out below.

## 2. R3 implementation task: certified bounded distance

First read AGENTS, the four canonical context files, the W1 handoff, this review, and the finite-evaluator and benchmark specifications. Write a short versioned implementation addendum before running R3 queries. This changes the numerical enclosure procedure, not MASTER physics.

### 2.1 Mathematical contract — derived sufficient enclosure

Let `dx,dy >= 0` be the exact coordinate gaps between the obstacle center and the existing predictor-position rectangle. Its minimum Euclidean distance is

\[
d=\sqrt{d_x^2+d_y^2}.
\]

Choose a fixed nonnegative integer precision `p` before evaluation. Define exact directed dyadic bounds

\[
d_j^- = 2^{-p}\lfloor 2^p d_j\rfloor,\qquad
d_j^+ = 2^{-p}\lceil 2^p d_j\rceil.
\]

Nonnegativity and monotonicity give

\[
a^-=(d_x^-)^2+(d_y^-)^2
\le d^2\le
a^+=(d_x^+)^2+(d_y^+)^2.
\]

If the validated square-root primitive provides `l <= sqrt(a^-)` and `h >= sqrt(a^+)`, then

\[
l\le d\le h,\qquad
g_p\ge l-R_s-E_p.
\]

Here `[l,h]` encloses the rectangle's minimum distance. Its upper endpoint is **not** an upper bound on every trajectory-to-obstacle distance. Likewise, a bracket for `sqrt(a^-)` alone must not be mislabeled as a bracket for `d`.

The lower-distance loss due solely to coordinate rounding is bounded by

\[
0\le d-\sqrt{a^-}\le \sqrt{2}\,2^{-p}\le 2^{1-p}.
\]

Any additional square-root enclosure width must be accounted for separately. These inequalities follow from componentwise squaring on nonnegative inputs and the reverse triangle inequality. They require no differentiability or new plant assumption.

### 2.2 Implementation and checking

- Use a single predeclared precision, recommended **p=24**, and the R2 pilot resource caps and Taylor settings. This is a development choice, not an optimality claim.
- Implement floor/ceiling through exact integer arithmetic; no floating conversion of safety quantities. Account for intermediate shifts, integer division and rational operations under the declared resource policy. No unmetered path around the bit guard.
- Serialize sufficient witnesses: rounding precision, gap bounds, radicand bounds and root bounds. The checker must reconstruct or independently check the directed rounding and enclosure inequalities from the original query/proof geometry, not trust rounded numbers supplied by the evaluator.
- Keep the original R2 distance method interpretable. Give the new method/profile a distinct ID and reject unknown variants.
- Add exact checks for zero gaps, exactly representable gaps, non-dyadic fractions, one and two nonzero gaps, zero/positive/negative final margins, and malformed rounding witnesses. Include mutation of lower endpoints upwards, upper endpoints downwards, precision, voltage/query binding and reported margin/status. Use exact inequalities as the reference, not sampled floating-point distances.
- Retain the corrected-radius regressions and positive/nonzero proof replay. If a primitive or proof mismatch appears, stop the affected evaluation branch and report it; do not alter the model to get a pass.

This is an arithmetic engineering remedy. It is not a new generic reachability method or a G4 novelty result.

## 3. Provenance task

Before R3 evaluation, record content commitments to at least:

- `research_context/MASTER_RESEARCH_CONTEXT_v2.md`;
- `research/theorem_notes/G2_FINITE_EVALUATOR_SPEC_v1.md`;
- `research/benchmarks/G2_USEFULNESS_BENCHMARK_SPEC_v1.md`;
- the R3 arithmetic addendum;
- input configuration, method/profile and manifest.

For Markdown/source use immutable Git blob bytes with explicit revision/path and SHA-256, or another explicitly defined cross-platform text protocol. Do not silently reuse raw Windows working-copy hashing. Hash the specification ledger as a separate bundle. A file path alone is insufficient. Historical `specification_sha256` stays historical; use unambiguous new fields and schema semantics.

Record both producer and checker revision/source-file commitments and the checker command/environment. Verify the committed code used, and record dirty-tree status. A later checker revision may legitimately replay an older producer: declare the revisions and compatibility rather than requiring equality or silently treating equality of metadata strings as code verification. List shared trusted components, including query/profile parsing, model construction and numerical primitives.

## 4. Execution plan — one bounded return

1. Commit the implementation, checks, addendum and new frozen profile/manifest before generating R3 evaluator output. Preserve the exact 216 pilot IDs and unchanged physical queries. Keep the original 1,944-ID universe and 1,728 remaining IDs visible.
2. Run the relevant checks and the R3 216-query pilot. Replay every completed proof, positive or inconclusive. Resource-only records receive integrity checks only. Produce an old/new transition table by query ID, not only aggregate totals.
3. The target is more completed sound evaluations. **Do not require all queries to be CERTIFIED**, and do not equate a negative sufficient margin with collision. Any new failure stage must be reported with the same diagnostic detail.
4. If the pilot has no resource-limited or invalid/execution-failure queries, every completed proof replays, and hash/provenance checks pass, a full-grid development run is allowed in this same assignment under the unchanged R3 method/profile. Freeze this conditional continuation rule and the full-grid manifest before the pilot. Evaluate the remaining 1,728 original IDs once; combine them with the 216 records without duplication and preserve phase provenance. A full-grid development run is not a held-out comparison.
5. If those continuation conditions are not met, stop expansion, return the diagnosed limitation and retain NOT_RUN accounting. Do not start another sequence of cap/precision tuning. The rule limits this development batch; it is not an added research gate or a new blanket code prohibition.
6. Report per-group action variation and mixed certificate outcomes for all evaluated groups. No separation is an admissible result. If none is observed, say so and identify conservatism/voltage-dependence questions for research review. Do not infer action necessity, unsafety of UNKNOWN actions or recursive feasibility.

G4's matched external baseline remains an open separate obligation. This arithmetic correction and any larger grid do not substitute for that comparison. Do not bundle unrelated controller work into this return.

## 5. Required return

Create **`docs/reviews/LUNA_TO_CODEX_G2_VALIDATION_R3_FULL_HANDOFF.md`**, with:

- reviewed starting commit and final commit; exact source/profile/specification commitments;
- response to every R3 finding; implemented equations and arithmetic-budget treatment;
- all executed commands, check counts and failures, distinguishing observed execution from source inspection;
- frozen manifests, complete records, replay reports, transition tables, action-group summaries and hash ledger;
- counts for CERTIFIED, proof-complete UNKNOWN, resource UNKNOWN, failures and NOT_RUN at each phase;
- whether conditional full-grid continuation occurred and why;
- limitations, shared checker dependencies, remaining usefulness and G4 obligations;
- explicit **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**.

Commit and push normally to `luna/g2-validation-v1`. Do not merge or force-push. Return the absolute handoff path so the user can relay it to Codex/GPT.
