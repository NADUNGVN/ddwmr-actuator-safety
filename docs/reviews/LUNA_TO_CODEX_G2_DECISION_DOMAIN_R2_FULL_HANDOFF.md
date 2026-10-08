Session: DDWMR | LUNA-G2-SCOPE

# Luna → Codex — G2 decision-domain R2 full handoff

**Date:** 2026-10-03  
**Assignment:** docs/CODEX_TO_LUNA_G2_DECISION_DOMAIN_R2_ASSIGNMENT.md  
**Repository:** D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety  
**Branch / HEAD:** main / 94c60f627a2ce1a8d52101050bdc0ce9d2e59afe  
**Disposition:** R2 protocol, endpoint-progress derivation/code/replay, candidate manifest and source closure prepared. **800/800 study rows are NOT_RUN. NO-GO to freeze or run pending independent review.**

## Finding 1 — execution scope and working-tree isolation

**Finding.** The assignment was executed directly in the shared repository on the existing branch.

**Evidence.** The initial working tree was already dirty with parallel G4 artifacts. This work added only new G2 R2 protocol, theorem, endpoint, fixture, configuration, manifest, closure and handoff files. It did not edit any existing evaluator/checker source, R3 archive or predecessor report; it did not touch G4 source or manifests, switch branches, commit or push. R3 pilot and compressed full-grid raw SHA-256 values remain unchanged:

| Frozen input | SHA-256 before/after |
|---|---|
| results/validation/g2/r3/dev_pilot_records_r3_v1.jsonl | fdbce2ac5587247ababc0849c5fce8f9a596c3eb2175ed277545072c06acdc43 |
| results/validation/g2/r3/conditional_full_grid_records_r3_v1.jsonl.gz | 352b6c67480133350a7d1bfc89334a1beff1dc27c64cfda46391af27982fa874 |

**Consequence.** Existing R3 and G4 work remains in the shared tree and must continue to be treated as other-lane material.

**Status.** PASS for the assigned file/scope boundary. Branch and HEAD are unchanged; no commit or push.

**Required action.** Review the new G2 R2 artifacts in place without cleaning or restoring the shared tree.

## Finding 2 — protocol R2 and decision logic

**Finding.** The v1 study candidate has been preserved and a separate v2 corrects the nominal-only criterion and the task description.

**Evidence.**

- Geometry is one static circular obstacle per scene. There are no two aisle walls; the study is named and described as a single-circle forward-progress task.
- The target remains exactly 1/20 m. Claims are stratified by horizon: 5 cm over 1/4 s implies 0.20 m/s average displacement rate, while over 1/2 s implies 0.10 m/s. Acceptance requires each horizon stratum to meet its own count; a pooled total cannot mask a failing horizon.
- The 400/400 split holds out scene geometry only. It is explicitly non-blind: the R3 archive and R2 task design have both been inspected. It does not claim state, parameter, random-sample or population generalization.
- The selector admits an action only when its whole-hold safety record replays as CERTIFIED and the endpoint lower bound is at least 1/20 m. It retains nominal (1,1) whenever eligible; otherwise it selects the eligible voltage nearest nominal in L1, with the declared progress and manifest-order tie breaks.
- Nominal retention is reported independently. The nominal-only success set is contained in the selector success set by construction. Alternatives claim improvement only for a positive paired gain: selector-minus-nominal-only must be at least 1 of 16 held-out groups. A tie is preservation, not improvement; exactly one additional success is a positive gain.
- The selector-vs-zero-only task question remains separate from unique nonzero-certificate coverage. Primary selector-vs-zero acceptance requires at least 4/8 successes and at least 2 more successes than zero-only at each horizon. The separate unique-coverage count requires a nonzero safety CERTIFIED action in a group whose zero action is UNKNOWN.
- All numerators retain their fixed denominators. Invalid, incomplete, UNKNOWN, resource-limited, execution-failure and NOT_RUN rows are never omitted.

**Consequence.** The nominal-only rule no longer treats a tie as improvement or rejects a one-group gain while accepting a tie. Task success, nominal preservation, zero-only task value and nonzero-exclusive certificate coverage answer different questions.

**Status.** Candidate protocol logic is internally consistent and predeclared. It is not frozen, and no candidate outcome exists.

**Required action.** Review the outcome rule and selector before any later freeze request; do not change scenes, target, thresholds, actions or profile after viewing held-out results.

## Finding 3 — terminal-progress proof

**Finding.** A sound rational lower bound for p_x(T)-p_x(0) is derived using a full-hold enclosure of u and theta and the integral identity. It avoids subtracting independently enclosed endpoint positions.

**Evidence.** Fix one query, its one rational voltage V, its closed initial box, its full fixed-label image and T>0. Conditional on the R3 proof inclusion that, for every t in [0,T],

\[
z(t)\in P_1+[-\eta(T),\eta(T)],\qquad z=(u,r,\omega_L,\omega_R,i_L,i_R),
\]

let P_u=[u_-,u_+] and P_r=[r_-,r_+] be the physical u/r components of P_1, and eta_u, eta_r their physical error radii. The implementation first replays the R3 proof and uses only the replay-validated P1_scaled and eta_physical fields. Then

\[
u(t)\in U=[u_- - \eta_u,\;u_+ + \eta_u]
\]

for all times and all initial states/labels. From MASTER dot(theta)=r and the initial heading interval Theta_0,

\[
\theta(t)=\theta(0)+\int_0^t r(s)\,ds
\in \Theta_0+[0,T]P_r+[-T\eta_r,T\eta_r]=:\Theta.
\]

This is an outer bound over every state and label. It discards correlations among heading, velocity, initial coordinates and parameters only by enlarging the set. Each execution keeps its fixed label and the same query voltage throughout; the interval coefficient hull may further relax fixed-label dependence but is used only outwardly.

Set M=max(|Theta_-|,|Theta_+|), c_-=max(-1,1-M^2/2), and C=[c_-,1]. The global inequality

\[
1-\cos x=2\sin^2(x/2)\le x^2/2
\]

proves cos(theta(t)) in C for every real angle in Theta. With the exact four-corner interval product, let g_-=lower(U C). It follows that u(t)cos(theta(t))>=g_- at all t and therefore

\[
p_x(T)-p_x(0)
=\int_0^T u(t)\cos(\theta(t))\,dt
\ge T g_-=:J^-.
\]

The initial p_x cancels in the identity; no independent p_x(0) interval is subtracted from an independently built p_x(T) hull. The product bound is valid for either sign of u and remains conservative for wide heading intervals. Task threshold comparison J^->=1/20 is exact rational ordering.

**Outward arithmetic and semantics.** Input endpoints, operations, comparisons and output bounds use exact Python Fraction/rational Interval arithmetic and reduced numerator/positive-denominator pairs. There is no floating-point trigonometry or decimal rounding in the progress proof. T is the exact positive query horizon; the internal tube and heading bound cover the closed hold, and the integral gives the terminal difference. Equality at the threshold passes. An UNKNOWN safety result, proof mismatch, malformed input, unsupported profile, operation/bit cap or execution failure cannot become a task success.

**Consequence.** The endpoint claim covers every initial state and every fixed label under one shared voltage, conditional on the inherited whole-hold P1/eta inclusion. The progress checker re-derives the endpoint record but shares the R3 replay checker, exact arithmetic primitives and model constructor; it is not a second safety engine.

**Status.** The endpoint inclusion argument is derived and fixtures pass. No mathematical blocker was found in this endpoint branch. Independent review of the inherited R3 inclusion and this source path is still required; therefore G2 remains UNVERIFIED.

**Required action.** Independently review the R3 full-hold P1/eta inclusion and the R2 exact-field checker before any endpoint bound can be used for a task result.

## Finding 4 — proof-to-code and trusted arithmetic map

**Finding.** The endpoint calculator, endpoint record checker and candidate manifest generator are new, isolated G2 files. Existing R3 producer/checker sources are read-only dependencies.

**Evidence.**

| Mathematical/provenance step | Source path | Relation to the bound |
|---|---|---|
| Full-hold predictor P1 and error radius eta | validation/g2/evaluator.py | Produces the R3 proof fields P1_scaled and eta_physical from the whole-hold Picard/comparison construction. |
| Replay of safety proof and query binding | validation/g2/checker.py | Independently rebuilds and exactly compares R3 proof fields, input/profile hashes and safety status before endpoint code consumes them. It shares model and arithmetic primitives. |
| Fixed-label maps, positivity and physical coordinate scaling | validation/g2/model.py | Reconstructs the benchmark map and scaling used to convert predictor u/r to physical units. |
| Rational expressions and gear identities | validation/g2/polynomial.py | Supports the model builder’s exact label-map and ideal gear-witness checks. |
| Rational interval and resource arithmetic | validation/g2/rational.py | Implements exact Fraction endpoints, interval arithmetic, bit and operation budgets. |
| Exponential, predictor and inherited pose/contact primitives | validation/g2/interval.py | Supplies the R3 whole-hold matrix exponential and its rational series/remainder operations. The new progress bound itself uses no trig approximation. |
| Semantic query/record binding | validation/g2/hashing.py | Binds the safety query and supplemental progress record. |
| Endpoint witness producer | validation/g2/endpoint_r2.py | Replays safety first; maps P1/eta to U and Theta, applies the global cosine bound and serializes every rational intermediate. |
| Endpoint witness replay | validation/g2/endpoint_checker_r2.py | Does not import the producer; replays safety, recomputes the endpoint fields separately and rejects altered fields/bindings. |
| Candidate input generation/checks | validation/scripts/build_g2_decision_domain_r2_candidate.py | Generates the ordered rational manifest only; checks IDs, counts, split, fixed-label image, state widths, voltage limits and NOT_RUN status. It does not invoke the evaluator. |
| Closure and fixtures | validation/scripts/write_g2_decision_domain_r2_source_closure.py; validation/scripts/verify_g2_endpoint_r2_fixtures.py | Hashes the full path/input closure and runs arithmetic/tamper fixtures, including one read-only archived R3 record. |

The trusted proof arithmetic is exact rational Python arithmetic. The inherited R3 exponential/trigonometric remainder code uses exact rational polynomial arithmetic and integer factorials; time.monotonic is used only by the cooperative timing check/display path. The progress proof itself evaluates no floating-point elementary function.

**Consequence.** The checker is independent at the endpoint formula/record-recomputation layer, while sharing R3’s trusted base arithmetic/model machinery and safety replay. No fully independent safety engine or universal implementation-soundness theorem is claimed.

**Status.** Source paths and mathematical roles are explicitly bound in the closure file.

**Required action.** Review every source-to-bound relationship, including the transitive polynomial import omitted from earlier role-only R3 lists.

## Finding 5 — fixtures and scoped validation

**Finding.** Exact arithmetic edge cases and tamper-replay behavior passed without evaluating the candidate task universe.

**Evidence.**

The fixture verifier checked six tube-arithmetic cases:

| Fixture | Exact lower bound | Result |
|---|---:|---|
| Exact threshold equality | 1/20 | meets threshold |
| Negative speed, heading 0 | -1/4 | below threshold |
| Velocity interval crosses zero | -1/8 | below threshold |
| Wide heading interval, global cosine clamp | -1/4 | below threshold |
| Heading accumulation with r error | 309799/6400000 | below threshold |
| Negative velocity with negative cosine lower bound | -1/2 | below threshold |

It also changed only the initial p_x interval in a paired arithmetic fixture and obtained the identical progress bound, as required by the integral identity. These are supplied interval-arithmetic fixtures, not trajectory simulations or task results.

For record integration, the fixture runner read the first archived R3 pilot row, state_low_neg / scene_d050_l+000 / T_020 / V_m1_m1. The existing R3 checker replayed it as CERTIFIED; the supplemental progress record replay passed; a changed endpoint bound was rejected; and a tampered underlying safety proof was rejected. The R3 bytes were read-only. The fixture output explicitly reports candidate_study_query_evaluated=false and archive_write_performed=false.

Commands passed:

- python -B -m validation.scripts.build_g2_decision_domain_r2_candidate --check-only
- python -B -m validation.scripts.write_g2_decision_domain_r2_source_closure
- python -B -m validation.scripts.verify_g2_endpoint_r2_fixtures

**Consequence.** These tests establish deterministic arithmetic/record behavior for the listed fixtures. They do not establish general soundness of the underlying R3 safety inclusion or any task outcome.

**Status.** PASS for these scoped fixtures only.

**Required action.** Codex should independently review the included fixtures and source path; no additional study rows are needed for this review.

## Finding 6 — manifest, source closure and exact hashes

**Finding.** A deterministic 800-ID rational manifest candidate is prepared and verified. It is explicitly unfrozen and every row is NOT_RUN.

**Evidence.** The manifest contains 32 complete groups with 25 ordered actions each; 400 development and 400 scene-held-out rows; 16 groups in each split; 12 fixed execution labels with the same semantic parameter-image hash for every action in a group; positive width in all nine initial-state coordinates; and voltage components within V_max=1. All 800 row status fields are NOT_RUN and result_record is null. The deterministic regeneration check returned the same bytes. The manifest source/input list has 34 entries: 13 transitive source files, 17 effective/review inputs, two test-fixture configs and two read-only frozen R3 fixture inputs.

Parameter/contact provenance remains synthetic. The benchmark fixes m, I_z, R_w, b, v_s, c_u, c_r and V_max at unit scale; phi is the clip law; the twelve actuator/capacity labels use the exact ranges and maps from benchmark_v1.json. In particular, C_j is an effective tangential capacity stipulated to enter both longitudinal force and algebraic lateral reserve. The inspected sources do not establish that coupling or the support/contact model for a physical platform.

| Artifact | SHA-256 of raw file bytes |
|---|---|
| research/theorem_notes/G2_ENDPOINT_PROGRESS_R2.md | 0e82cfe25bf5fee3da2d991559e0944c60a6972ab6160e3b148d3577e63ba472 |
| research/benchmarks/G2_DECISION_RELEVANT_STUDY_PROTOCOL_CANDIDATE_v2.md | 7f55070449a570ffbd806630ddfcd880ba54d36e1c7dd708b17e7153bfb4cbc2 |
| validation/g2/endpoint_r2.py | 21f35f62fe79b4782ed8446d319cb13b4813242af7621b2459111831bacbbb11 |
| validation/g2/endpoint_checker_r2.py | d6b1611e4423e69c47852d2a3d848d98561475962b576e1ed05ed15dc65f007c |
| validation/configs/g2_decision_domain_r2_v1.json | 9c3fe515d8b695429fdbe01baaee27448cb4714cb84f4c19f23bf51976b23f13 |
| validation/configs/g2_endpoint_progress_fixtures_r2_v1.json | 31b14c771edff1c748f84b8303c8e4566a3a3470178f7869e346c0428c67a6ad |
| validation/scripts/verify_g2_endpoint_r2_fixtures.py | 31df59f89fe2a0d4ab7d796262617fa1226f52bda4d105d5974099785ab518f0 |
| validation/scripts/build_g2_decision_domain_r2_candidate.py | c18ff94ef05545ff872c52ad4e751b4683a43a227e40486cbeeed48feb83f941 |
| validation/scripts/write_g2_decision_domain_r2_source_closure.py | 5b3e4bc77843e38c6575f6f3a15df3f3f5f2513c645a2670f6339a8c46a3de6f |
| research/benchmarks/G2_DECISION_DOMAIN_R2_MANIFEST_CANDIDATE_v1.json | 28557ddecaf780c02801e872c247f46ff5a2c6b21da587520a82dcf5ab80e69b |
| research/benchmarks/G2_DECISION_DOMAIN_R2_MANIFEST_CANDIDATE_v1.sha256 | 14d0b2fe9f1f7560f7683cbcf316be84bd71e75bbe58e52348f255830e1e67d0 |
| research/benchmarks/G2_DECISION_DOMAIN_R2_SOURCE_CLOSURE_v1.json | 612e592a263d7788f27f652e9a49683372e86393c2e04a662d8db126a39d8ebd |
| research/benchmarks/G2_DECISION_DOMAIN_R2_SOURCE_CLOSURE_v1.sha256 | f74b3611bc6d637f2c6f92c407e10dd7b738c647d94703704ac3de80fea4a5c5 |

The manifest has semantic SHA-256 c72a04ffdf1fbe210cf073fe234255ffc67a4472c34b0f1519a1582291f9e223. The closure has semantic SHA-256 24bd14b0cac7d3ca9f1bf6ad69e84decf490d8746d054c5789bf813e7845e227. The specification bundle SHA-256 is fad9048cce703e140a8a42e4e602fd9b1b3fc7eb0183efd1cf8890bad311b04f. The fixed parameter input raw/semantic hashes remain b2bc12cd578229cfb6df4b426f93e0f472d69f6be36929df93e797ff79396a9e / 21632e1eebf58a5d7fea14224254738d0ff11ba689b94343afa47adbccea166b. The effective R2 config raw/semantic hashes are 9c3fe515d8b695429fdbe01baaee27448cb4714cb84f4c19f23bf51976b23f13 / 264b2875ddfee862bd9eaea4d6202c6ef51e38a699e2445193c7fd7e840a8ddb. The exact semantic fixed-label image hash is c653a4f0f0b76e5d36fffa6e0cab822eac3c949955a2348e98ae9cdf597fe6be.

The source-closure JSON provides raw SHA-256 for all 34 entries. Its 13 transitive source hashes are:

| Transitive source | SHA-256 |
|---|---|
| validation/g2/__init__.py | e263a290f1d402c7d233519c89d0f94ed1eaf731821c596486db7fc82ad624c8 |
| validation/g2/evaluator.py | 62dd355684c53fdd104ad051d2f06486e256e3489f1a72263a8432b9af9cc26e |
| validation/g2/checker.py | b2605941cc2620f19d0c6001736bec8e292b2e0dbb819f043c5dcd44fbc5e526 |
| validation/g2/rational.py | 8a2c16778b33898afd16c8da44945c2d41fd7d187cb11c7cb071745e68ed5c6e |
| validation/g2/interval.py | e49e2e3880485d9a658e2435cfa06b784f98257b13c51fa4a2bf464f9c73e5c6 |
| validation/g2/model.py | 93e9a96d640ad09a7eb7dbff51ebfb8f2d783296ce5afff57af41e81e30a8508 |
| validation/g2/polynomial.py | 48e3ff7dcce8353cb9d58b31f6986e12fcaaaf320cd06896f95e0813740b66a4 |
| validation/g2/hashing.py | 0d5137359e19c80b20c097d49c8d7246e48effcaef9e3649b142120136c13aab |
| validation/g2/endpoint_r2.py | 21f35f62fe79b4782ed8446d319cb13b4813242af7621b2459111831bacbbb11 |
| validation/g2/endpoint_checker_r2.py | d6b1611e4423e69c47852d2a3d848d98561475962b576e1ed05ed15dc65f007c |
| validation/scripts/build_g2_decision_domain_r2_candidate.py | c18ff94ef05545ff872c52ad4e751b4683a43a227e40486cbeeed48feb83f941 |
| validation/scripts/verify_g2_endpoint_r2_fixtures.py | 31df59f89fe2a0d4ab7d796262617fa1226f52bda4d105d5974099785ab518f0 |
| validation/scripts/write_g2_decision_domain_r2_source_closure.py | 5b3e4bc77843e38c6575f6f3a15df3f3f5f2513c645a2670f6339a8c46a3de6f |

**Consequence.** Codex has deterministic candidate inputs, explicit exact hashes, source-to-bound mapping and fixture evidence to review before any freeze decision.

**Status.** Candidate manifest and closure validate; they are NOT_FROZEN. **800/800 NOT_RUN.**

**Required action.** Independently regenerate the manifest, verify all closure hashes, review the R3 and endpoint inclusions, and only then decide whether to authorize a later freeze.

## Finding 7 — R3 UNKNOWN risk and resource profile

**Finding.** Long holds and the whole-hold one-cell profile make a high UNKNOWN/resource-limitation rate plausible, but R3 does not determine the new outcomes.

**Evidence.** R3 had 748 UNKNOWN among 1,944 rows; 636 rows had negative sufficient contact margins, including 636/648 at T=0.10 s. Negative sufficient bounds mean the test failed to establish the predicate; they do not prove actual collision, physical contact loss or unavoidable danger. R2 holds are longer at 0.25 and 0.50 s and do not tune scenes or thresholds from held-out outputs.

R2 preserves the 16,384-bit and 1,000,000-operation caps, Taylor orders 16/18, comparison order 16, 24 square-root bisections, and the one full-hold state/parameter/time cell. State and parameter split depths are zero with one leaf each; time slab count and integration panels are one. Repeating the same global hull over nominal subpanels would be a no-op and is not claimed as refinement. The 15-second evaluator check is cooperative: it is polled every 256 metered rational operations and has no final successful-return check. No outer process guard was implemented or reviewed, so this is not a hard wall-time guarantee.

**Consequence.** Resource/certificate abstentions remain reportable study outcomes. They cannot be relabeled as unsafe or removed from the denominator. The protocol cannot promise a hard deadline.

**Status.** Material conservative-UNKNOWN risk; no R2 task output exists.

**Required action.** Preserve all UNKNOWN/resource/failure/NOT_RUN rows and the fixed denominator. If a hard wall limit is needed, implement and review an outer process guard before a later run.

## Final decision — NO-GO for freeze or run

**Finding.** The endpoint proof path and corrected finite study design are ready for Codex review, not for evaluation.

**Evidence.** The endpoint proof is conditional on the inherited R3 full-hold inclusion. The new endpoint checker shares trusted arithmetic/model code with R3. Codex has not yet reviewed this R2 source closure or accepted the source-to-inclusion chain. The manifest and all 800 per-row records remain NOT_RUN.

**Consequence.** A positive result cannot be interpreted until those proof dependencies are reviewed and the exact inputs are later frozen under explicit authorization. No G2, G3, G4 or physical-platform status changes.

**Status.** **NO-GO to freeze or run now. G1 remains PASS only for restricted reduced-model consistency; G2/G3/G4 and physical correspondence remain UNVERIFIED; overall HOLD.** No mathematical blocker was found in the supplemental endpoint derivation, but the inherited R3 inclusion remains an independent review prerequisite.

**Required action.** Codex should accept or return the R3 tube inclusion, R2 endpoint proof/checker, manifest/source closure, selector rules and cooperative timing treatment. Until that review and a later explicit run instruction, preserve 800/800 NOT_RUN.

