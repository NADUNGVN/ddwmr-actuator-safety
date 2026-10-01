# GPT → Codex — Scientific review full handoff: G2 validation R3

**Review date:** 2026-09-30  
**Repository:** NADUNGVN/ddwmr-actuator-safety  
**Branch:** luna/g2-validation-v1  
**Requested output:** GPT_TO_CODEX_G2_VALIDATION_R3_SCIENTIFIC_REVIEW_FULL_HANDOFF.md  
**Authority:** MASTER_RESEARCH_CONTEXT_v2.md, adopted formulation v2.1, workflow W1

## Disposition

**Scoped conclusion:** R3 supports an accepted, bounded computational result for the frozen synthetic G2-COMP-clip development batch. The directed-distance witness is sound in its stated role, and the recorded finite evaluator completed the original 1,944-query grid with certificates on nonzero-width moving-state cells under one common held voltage and the full fixed uncertain label cell.

**Canonical project status remains:** **HOLD; G1 PASS — restricted reduced-model scope; G2/G3/G4 UNVERIFIED; physical-platform correspondence UNVERIFIED.** This review does not promote a gate, amend the plant, open G3, authorize a controller, or establish hardware safety.

**Next priority:** a matched comparison on the already observed R3 domain, using Auer, Kiel, and Rauh’s piecewise-smooth validated-integration method as a faithful method-level reproduction. The primary source directly covers known piecewise-smooth switching behavior, including the clip corners. The pinned public VALENCIA-IVP source package is an older simplified release and does not contain the 2013 paper’s non-smooth derivative extension; therefore the assignment must implement and audit that published extension before any result is called a faithful comparator run.

## Acceptance scope summary

| Question | Disposition | Boundary |
|---|---|---|
| R3 directed-dyadic distance correction | **ACCEPT — scoped** | Exact rational rounding and square-root witnesses are sound for the minimum distance to the predictor-position rectangle in the R3 path. This says nothing by itself about the upstream tube. |
| Frozen 1,944-query development batch | **ACCEPT — recorded computational evidence** | Exact coverage, archived bytes, hashes, outcomes, and reported proof replays are independently supported by the Codex review and artifacts. This review did not replay the engine or decompress the full archive again. |
| Upstream G2-COMP-clip evaluator | **PARTIAL — no unsound branch identified in the inspected path** | Formula/code mapping is consistent with the finite sufficient-enclosure argument, but this review is not a fresh end-to-end proof replay or a universal implementation proof. |
| Usefulness | **PARTIAL** | Moving, nonzero-width certificate outputs exist; the grid has no certified group available only through a nonzero action. Practical action-selection value and useful physical parameter scales remain open. |
| Runtime | **ACCEPT — offline finite completion only** | Reported timings establish finite offline batch completion. They do not establish an online filter, deadline guarantee, or recursive operation. |
| Generic-method novelty | **REJECTED as a standalone claim; G4 remains UNVERIFIED** | Predictor-plus-residual enclosure, fixed-parameter augmentation, interval arithmetic, proof serialization, and dyadic rounding are not novelty evidence. A plant/contact-specific advantage still needs matched results and source-level analysis. |
| Arbitrary supported inputs | **NOT ACCEPTED** | R3 covers a particular law, rational synthetic family, one-step whole-hold profile, and finite grid. It is not a universal soundness proof for all MASTER laws, parameter sets, horizons, or evaluator configurations. |

## Review basis and limits

### Revisions actually reviewed

- **Implementation/evidence snapshot:** 4fd0451146ab9567a51499183db5a08f20ae8de5.
- **Current documentation snapshot read:** aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46.
- The diff from 4fd0451146ab9567a51499183db5a08f20ae8de5 to aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46 contains only two additions: **docs/GPT_G2_VALIDATION_R3_REVIEW_REQUEST.md** and **docs/reviews/CODEX_G2_VALIDATION_R3_REVIEW.md**. Validation source and results are unchanged between the named implementation snapshot and current HEAD.
- The R3 handoff records this implementation/evidence chain: start **4df4dfef65a5addb040fbd2f059a62727189cd88**; implementation/addendum **c7f06727b33775c41b7c841d5c43269467ab217b**; frozen profile/selection **e7fac74d69a5f117045416d688cc808e50ac1a6a**; pre-evaluation manifests **ab5fef68a0726b9d49b10c6bbd86f86b297b2efd**; pre-run fixture correction **78aba4ddc100eb2fdb5c966e6d124ddac90ac8bc**; pilot output/replay **667a8e4a5e840ff33e823f353bed8c6328c0a443**; archive support **266f979a6c2aaf3ca97ead522d18d33633d97e41**; full-grid output/replay **28e962ec6e2085656e4dd1b7bc254186835cefb8**; handoff **4fd0451146ab9567a51499183db5a08f20ae8de5**.
- Historical context includes the accepted Case C review at **c9ff32d45ad7f500cc2492c3bc7a69480c29c636**. It remains a separate exact-rest synthetic result.

### Local material read

This review read **AGENTS.md**; all four canonical **research_context/** files; the R3 review request, Codex R3 review, Luna R3 handoff, R3 distance addendum, R3 assignment, G2 enclosure/evaluator specifications, usefulness benchmark, G4 matched-comparison contract, prior-art supplements, and earlier consolidated GPT review. It inspected relevant paths in **validation/g2/evaluator.py**, **checker.py**, **rational.py**, **interval.py**, **model.py**, **polynomial.py**, **provenance.py**, **validation/scripts/verify_records_r3.py**, and **run_pilot_r3.py**, plus the R3 summary, action-group summary, run metadata, frozen manifests, archive manifest, and hash ledgers.

### Execution and source-access limits

- This review did **not** run the evaluator, checker, test suite, pilot, or full-grid replay. It did not decompress the 147,589,521-byte logical continuation JSONL itself.
- The prior Codex R3 review reports a separate read-only exact-fraction analysis: 21/21 result-ledger entries; full archive byte count/hash; ID coverage and counts; exact stored distance identities and inequalities for all 1,944 proof records; status/margin signs; source commitments; and group/timing summaries. It explicitly did not rerun the evaluator or full checker. The 1,944 successful proof replays are Luna’s recorded execution, not a second Codex execution.
- Comparator paper access below is to the 17-page primary article and the pinned public source archive identified below. No VALENCIA-IVP program was built or run during this review. No source for the paper’s 2013 non-smooth C++ extension was found in the inspected public basic-release archive.

---

## R3-SR-01 — Review scope, artifact provenance, and independence

**Finding:** The R3 snapshot is well bound to its inputs and code for a reproducible development batch. The checker is not an independent second numerical engine, and the explicit source lists omit transitive scientific dependencies.

**Evidence:** At the reviewed snapshot, R3 records bind a pre-evaluation specification-content ledger, frozen profile/configuration/manifest, producer and checker revisions, runtime metadata, and result hashes. The Codex R3 review reports 24 specification/producer/checker commitment entries matching immutable Git blobs and all 21 result-ledger rows matching. Pilot and continuation producer/checker revisions are recorded separately. Full Git revisions still identify source omitted from the explicit path lists.

The maintenance issue is exact:

- **validation/g2/checker.py** imports helpers from **evaluator.py**, but the explicit CHECKER_PATHS list omits evaluator.py.
- **validation/g2/model.py** imports **polynomial.py**, which is absent from both explicit producer and checker path lists.
- The checker also shares rational interval primitives, model construction, and validated exponential/trigonometric/root routines with the producer. Its replay is a separately executed proof-record path, not an independently implemented arithmetic/model engine.

The full immutable revisions are bound, and the Codex R3 review found no relevant incompatible edits to these files for the returned batch.

**Consequence:** These omissions weaken clarity and completeness of the declared dependency manifest for future runs. They do not show R3 used mismatched code and do not invalidate the frozen records. Rewriting the historical R3 manifest now would reduce provenance clarity.

**Status:** **VALID — provenance adequate for retaining R3; NEEDS REVISION for the next version’s dependency manifest and independence wording.**

**Required action:** Preserve every R3 hash, record, and manifest unchanged. In the next version, enumerate the complete transitive scientific call graph or bind the entire source tree, and state which shared components remain trusted. Describe checker independence proportionately. Do not rerun R3 solely to repair a manifest label.

## R3-SR-02 — Directed dyadic distance and full-hold collision inequality

**Finding:** The R3 distance correction is a sound bounded-precision enclosure of the predictor rectangle’s minimum distance. Its lower endpoint is the quantity needed for the collision sufficient test.

**Evidence:** For exact nonnegative coordinate gaps dx, dy and p=24, **evaluator.py** computes exact dyadic bounds:

~~~text
g_j^- = floor(2^p g_j) / 2^p
g_j^+ = ceil(2^p g_j) / 2^p
a^-   = (g_x^-)^2 + (g_y^-)^2
a^+   = (g_x^+)^2 + (g_y^+)^2
~~~

by numerator shifts, exact quotient/remainder, and an upward increment only when a remainder exists. Thus a^- ≤ dx²+dy² ≤ a^+. Validated rational bisection returns l ≤ sqrt(a^-) and an upper bracket endpoint h ≥ sqrt(a^+), so l ≤ d_rect ≤ h. The sufficient collision lower margin remains l − R_s − E_p.

The checker rebuilds exact gaps from the query and predictor-position rectangle, repeats directed division, verifies coordinate widths/order, recomputes radicands and root brackets, then binds the recomputed margin/status to the record. The Codex R3 review says it independently checked all stored directed-rounding identities, radicand bounds, distance-endpoint inequalities, and margin-sign/status agreement across 1,944 records using exact fractions. It found no witness mismatch.

For p=24, coordinate quantization alone loses at most sqrt(2)·2^-24 ≤ 2^-23 in distance. Separate square-root bisection widths remain separate losses. The R3 path is in **validation/g2/evaluator.py** around _dyadic_gap_bound, _bounded_collision_distance, and the full-hold collision loop; checker reconstruction is in **validation/g2/checker.py** around _checker_r3_distance_witness.

Crucially, h is an upper bound on the rectangle’s **minimum** distance only. It is not a maximum distance from all trajectory points to the obstacle. Collision soundness uses the lower bound l on that rectangle minimum, subtracts the obstacle’s inflated radius R_s, and subtracts the full-hold pose error E_p.

The reported R3 profile retains the R2 caps of 16,384 rational bits, 1,000,000 rational operations, and 15 seconds per query; it does not raise caps or bypass accounting.

**Consequence:** The specific R2 distance-arithmetic bottleneck is resolved for the frozen R3 profile and evidence. This corrects a numerical enclosure, not the underlying trajectory tube and not novelty status.

**Status:** **VALID — scoped formula and stored-witness arithmetic. No distance-correction blocker identified.**

**Required action:** Retain the versioned R3 distance method and checker. Keep the minimum-distance interpretation explicit. No additional precision tuning or cap increase is warranted for this completed batch.

## R3-SR-03 — Upstream evaluator, quantifiers, and possible unsound certification paths

**Finding:** The inspected R3 certificate path is consistent with the finite sufficient-enclosure argument. This review found no specific branch that appears able to emit an unsound CERTIFIED result under the declared G2-COMP-clip contract, but a finite replay and source inspection do not prove arbitrary-input implementation soundness.

**Evidence:** The code path corresponds to these required inclusions and sufficient tests:

1. **model.py** constructs the six internal motor/body coordinates from the declared equations, uses rational fixed-label maps, checks positive denominators/parameters, and verifies gear-witness identities symbolically. The twelve label coordinates parameterize the declared rational image. Interval evaluation may lose correlations between matrix entries; this widens the outer enclosure rather than selecting a favorable label.
2. One query fixes one exact held voltage V, one full initial-state box X, and one full fixed label cell. Query construction binds the action and state/scene/horizon; the runner evaluates each action as a separate query. Within an individual proof, no parameter-dependent action choice occurs.
3. The interval matrix exponential encloses exp(A(θ)t) for t in [0,T] with interval Taylor terms plus a norm remainder. The P0/P1 integral predictor uses the full interval t∈[0,T], so its range is not an endpoint-only rollout. The P1−P0 defect is converted by the clip Lipschitz bound and amplitude cap into a force residual bound.
4. The nonnegative matrix N and D̄d̄ forcing bound the comparison system for the same execution-fixed parameter fiber. The finite positive radius series has a separately bounded exponential tail. The parameter hull is an outer relaxation; replacing correlated coefficients by intervals cannot omit a trajectory of any fixed label.
5. E_theta and E_p lift internal predictor error to a full-hold heading/position error. P1 supplies full-time ranges for u and r; interval sine/cosine ranges and duration interval [0,T] enclose the integrated pose. The collision test then applies to every static circle in the query.
6. The contact test uses the full predictor slip range plus |S|η/v_s to upper-bound each clipped slip magnitude by β∈[0,1]. It lower-bounds available contact by Σ C_j^- sqrt_lower(1−β_j²) and upper-bounds demand by m^+(U+η_u)(R+η_r). It takes no derivative of the square-root contact margin. A certificate requires both every obstacle margin and the contact margin to be nonnegative.

The data contract quantifies over every state in the initial cell, every label in the complete fixed parameter image, and every time in the full hold, all under the same query voltage. The proof does not resample labels, allow V to vary by label, turn an endpoint test into continuous safety, or equate an inconclusive lower margin with an actual violation.

The arithmetic helper branches inspected are conservative by construction: exact rational intervals; monotone clip interval extension; Taylor remainder bounds with outward symmetric intervals; rational square-root brackets; and resource exhaustion returning UNKNOWN. The profile is limited to predictor depth n=1, a whole-hold hull, and a finite arithmetic cap.

**Consequence:** R3 supports a scoped one-hold synthetic certificate claim, not universal soundness over the abstract MASTER class. It does not automatically accept every clause of the draft finite-evaluator theorem for every future representation, nor replace a fresh independent end-to-end proof replay.

**Status:** **PARTIAL — no identified unsound CERTIFIED branch in the inspected frozen path; evaluator theorem/code contract is not universally closed by this review.**

**Required action:** Keep claims bounded to the frozen G2-COMP-clip method/profile and exact rational synthetic family. Preserve the distinction between a code/artifact review, a mathematical soundness proof, and successful finite replays. If future code expands the input class, re-review that class and its proof obligations before admitting certificates.

## R3-SR-04 — Full-grid completeness and stored computational evidence

**Finding:** The original finite development universe was completed under the frozen R3 rule, with no resource-censored or invalid records.

**Evidence:** Recorded counts are:

| Phase | Queries | CERTIFIED | Proof-complete UNKNOWN | Resource UNKNOWN | Invalid/failure |
|---|---:|---:|---:|---:|---:|
| Frozen pilot | 216 | 126 | 90 | 0 | 0 |
| Conditional continuation | 1,728 | 1,070 | 658 | 0 | 0 |
| Combined original universe | 1,944 | 1,196 | 748 | 0 | 0 |

There are 1,944 unique IDs, complete against the frozen 1,944-ID universe, with 1,944 stored proof objects. The Codex review reports 21/21 result-ledger entries matching and verifies the lossless continuation archive’s raw size of 147,589,521 bytes and SHA-256 de339ffcb5ee5e0c83f8d25e3077d9fd9316f83293982189aaffba0bdcf3b196. The recorded checker report says all_pass true, replayed 1,944/1,944 completed proofs, and found no resource-only record. The continuation compressed archive is 34,613,266 bytes and is bound by **conditional_full_grid_archive_manifest_r3_v1.json**.

The run contract was frozen before evaluator outputs. The same R3 method/profile was used for the frozen 216 pilot and the single permitted conditional run of the other 1,728 original IDs. The 1,728 continuation outputs were not a new held-out sample. The entire 1,944-query set was already the declared development universe.

These are six state cells × twelve scenes × three holds × nine voltages. The six state boxes have nonzero width in every state coordinate and strictly positive u; the contact labels form the full uncertain twelve-dimensional parameter cell. The synthetic family is deliberately nonstiff and is not calibrated to a physical robot.

**Consequence:** The claim “there is no completed finite computational batch” is superseded. The records show finite synthetic computation and certificates on a non-singleton moving-state domain. They are neither statistical trials nor evidence about a distribution of real-world states.

**Status:** **VALID — completed R3 development batch and archive integrity, relying on recorded execution and Codex’s independent artifact audit.**

**Required action:** Preserve the development/confirmatory distinction. Do not call the continuation held out, infer physical failure rates, or extrapolate the batch to arbitrary laws, parameter families, time horizons, or model stiffness.

## R3-SR-05 — Mixed groups, zero voltage, and the narrow usefulness claim

**Finding:** R3 provides a stronger moving-state certificate-output distinction than exact-rest Case C, but zero voltage alone attains the same existential group coverage as the nine-action set on this grid.

**Evidence:** The 216 state/scene/horizon groups contain 132 with all nine actions certified, 76 with all nine UNKNOWN, and eight mixed groups with exactly one certified action. All eight mixed groups are the same state_low_mid cell and same T=0.1 s hold. This cell has u∈[0.2,0.3] m/s, r∈[−0.05,0.05] rad/s, nonzero widths in the remaining state coordinates, and the full uncertain label cell. In each mixed group, the sole certified action is V=(0,0). All nine collision lower margins are positive. Each of the other eight actions is UNKNOWN solely because the sufficient contact margin is negative.

Rounded contact lower margins are identical across those eight obstacle geometries:

| Voltage | Contact lower margin |
|---|---:|
| (0,0) | +0.127641589 N |
| (−1,−1) | −0.211889782 N |
| (−1,0), (0,−1) | −0.103833460 N |
| (−1,+1), (+1,−1) | −0.213302737 N |
| (0,+1), (+1,0) | −0.108378014 N |
| (+1,+1) | −0.213006908 N |

Across all groups with any certified action, zero is certified in every one: **140/140**. Checking zero alone identifies exactly the same 140 groups with at least one certified action as checking all nine enumerated voltages. No group gains a certificate from selecting a nonzero voltage. The eight mixed groups repeat the same contact distinction across obstacle geometries; contact margins do not vary with those scene offsets.

The benchmark is not exact rest: u is strictly positive. It is still synthetic and nonstiff; obstacle and parameter scales have no hardware provenance. The code’s contact margin is a sufficient lower bound. A negative value says the sufficient check failed. It does not show actual contact inadmissibility, unsafe force demand, or inevitable collision. Zero is the adopted closed zero-terminal-voltage condition; it is not an instantaneous stop, braking guarantee, or recursive backup.

**Consequence:** A defensible narrow claim beyond Case C is: *on the frozen R3 synthetic moving-state grid, the same one-hold sufficient test has voltage-dependent certificate outputs for the full uncertain label cell, and the distinction is contact-bound-driven in one repeated state/horizon mechanism.* This is an observed certificate property, not a physical safety advantage. Claims that nonzero action expands certified-group coverage are already falsified on this grid. A broader claimed advantage is falsified on a matched domain if a generic validated method matches or dominates R3’s certificate coverage, enclosure widths, and cost.

**Status:** **VALID — narrow descriptive distinction. Practical decision-relevant advantage remains UNVERIFIED; existential group coverage has no nonzero-action gain over zero.**

**Required action:** Keep all eight groups and every UNKNOWN row in the comparison denominator. Do not tune obstacles, alter voltages, or invent a post-result coverage threshold. Compare the current method against an applicable validated method before describing the output difference as a distinctive construction.

## R3-SR-06 — G2 obligation map and scoped disposition

**Finding:** A scoped G2 computational disposition is supportable for the declared clip-law synthetic profile. The canonical G2 gate should remain UNVERIFIED.

**Evidence:** The finite-evaluator and usefulness documents distinguish finite evaluability, soundness, and usefulness. R3 supplies a full finite development batch with moving nonzero-width state cells, uncertain fixed actuators, common per-query voltage, full-hold sufficient checks, and transparent offline resource/timing outputs. The current development profile only implements the conservative n=1 whole-hold fallback. The benchmark is still marked not locked and explicitly records that no minimum coverage or runtime cutoff has been scientifically justified. No hardware parameter identification or real-plant correspondence exists. The Codex review reports no distance-stage defect but did not rerun the upstream evaluator/full checker.

| Existing G2 obligation | R3 evidence | Disposition |
|---|---|---|
| Finite evaluator halts on its declared bounded profile | 1,944/1,944 recorded proof objects; zero resource UNKNOWN, invalid input, or execution failure | **Resolved for this batch/profile.** Not a universal runtime or arbitrary-input theorem. |
| Joint state/parameter coverage with one fixed label and one common held voltage | Full twelve-label rational image, one exact voltage per query, all state/label cells in the query obligation | **Supported for this synthetic contract.** Parameter correlations are overapproximated in interval coefficient hulls; loss of tightness is not quantified against a structure-preserving method. |
| Full-hold coupled motor/wheel/body/contact enclosure | Predictor, residual radius, pose lift, collision and contact sufficient tests map to the frozen G2-COMP-clip formulas | **Strong scoped computational support;** independent end-to-end theorem/code closure remains incomplete. |
| Certificates on nonzero-width moving state regions with uncertain actuators | 1,196 certificates over six positive-speed state boxes and the full fixed uncertain label cell | **Resolved as existence evidence in the synthetic scope.** No coverage-rate threshold is inferred. |
| Voltage-dependent certificate output | Eight mixed groups; zero alone certified, with contact margins driving other outputs to UNKNOWN | **Resolved descriptively.** Does not show nonzero-action benefit or action necessity. |
| Useful operating domain, conservatism, and tractability | Many certificates and offline costs, but order-one nonstiff synthetic scales; no utility threshold was predeclared; no matched alternative | **Partial/open.** This is useful development evidence, not proof of practical operating scales or method advantage. |
| Physical parameter relevance/correspondence | No hardware identification or support/contact inclusion evidence | **Open and separate from G1’s restricted pass.** |
| Online timing, recursive feasibility, or safe policy | Offline query timings only; no online action-selection policy or endpoint recursion | **Open; G3 remains outside this review.** |

The smallest remaining **G2** evidence item is not another hand example, a post-hoc success-rate threshold, or a G4 novelty claim. It is an independently reviewed, decision-ready scope statement for usefulness under the existing benchmark: either accept the declared moving, nonzero-width synthetic clip-law region as a bounded computational-usefulness result, without physical or online extrapolation, or define before any new output what externally justified operating domain and observable G2 use requirement remain unmet. The finite G2-COMP-clip proof/code audit should be closed at the same scope. A matched external comparison is the next **G4** priority; it is not a substitute for soundness and is not required to accept a sound finite enclosure.

**Consequence:** G2 has materially stronger evidence than Cases A/B/C alone. A narrow synthetic G2 result can be recorded now; neither the benchmark’s open usefulness policy nor the universal/project-level G2 gate is thereby resolved.

**Status:** **SCOPED G2 COMPUTATIONAL EVIDENCE ACCEPTED; canonical G2 UNVERIFIED. No gate promotion.**

**Required action:** Preserve G2/G3/G4 and physical-correspondence statuses. Do not require novelty to accept soundness, or treat numeric completion as novelty. Resolve the narrow usefulness scope through independent review and documented acceptance criteria before a new confirmatory run; do not choose a numeric cutoff after seeing R3.

## R3-SR-07 — Comparator choice and source-backed applicability

**Finding:** The most applicable external method for a matched comparison on the existing clip-law R3 domain is Auer, Kiel, and Rauh’s verified piecewise-smooth IVP method implemented with VALENCIA-IVP. It is applicable at the published-method level, but the original 2013 extension is not yet reproduced in this repository or in the pinned public base package.

**Evidence:** The primary article is Auer, Kiel, and Rauh, “A Verified Method for Solving Piecewise Smooth Initial Value Problems,” *International Journal of Applied Mathematics and Computer Science*, vol. 23, no. 4, pp. 731–747 (2013), DOI 10.2478/amcs-2013-0055. Sections 4.1–4.2, especially IVP (26), algorithmic right-hand-side representation (27)–(28), generalized derivative (31), (33), (40)–(41), and validated enclosure equations (42)–(43), treat known switching points and a piecewise-smooth RHS. The paper explicitly applies its generalized-derivative construction in VALENCIA-IVP; its example is a mechanical model with friction and hysteresis. Primary full text: [article PDF](https://zbc.uz.zgora.pl/repozytorium/Content/78882/download/) and [DOI](https://doi.org/10.2478/amcs-2013-0055).

The R3 law is:

~~~text
clip(q,-1,1) = -1 for q < -1; q for -1 ≤ q ≤ 1; +1 for q > 1.
~~~

Its branch functions are bounded, smooth on their pieces, and continuous at the two known switches. The branch slopes are 0, 1, 0; at each switch the interval derivative must include both sides. If a state/slip interval spans both switches, implement the paper’s multiple-switch construction or sound subdivision; the one-switch formula alone must not be silently assumed to cover it.

The application’s other RHS operations are rational arithmetic and elementary trigonometric functions. Exact uncertain labels can be carried as constant augmented states (ξ̇=0); the voltage for each query is fixed and common to all labels. This is compatible with fixed-parameter semantics when the rational label map and positive denominators are preserved. Auer’s article starts from an interval of uncertain initial conditions and an algorithmic representation of the RHS. The VALENCIA-IVP basic release’s readme also describes adding time-invariant parameters as constant state components.

Pinned public software source inspected: [ValEncIA-IVP/basic at commit d1a09ceb3f68deb40357bdc89944b28997e9fb30](https://github.com/ValEncIA-IVP/basic/tree/d1a09ceb3f68deb40357bdc89944b28997e9fb30), initial commit 2021-05-14. Its ValEncIA-basic.zip Git blob is af0c6bd1bd5ac10bbdf0fc71b1d6da125f60f9db; downloaded archive SHA-256 is 1e0adfdec371a6ad74348a175b107c82640fb7129891bcca7f53db0c88f1986a. The archive readme calls this a “simplified version” and contains ValEncIA-IVP_0.92_2e.cpp; it identifies PROFIL/BIAS and FADBAD++ dependencies. It does not contain the 2013 paper’s specialized non-smooth derivative class. The paper is therefore the primary algorithm source, while the pinned package is a source seed, **not** the exact original 2013 tool build.

This is preferable for the current comparison to the already-inspected Houska–Villanueva–Chachuat smooth/factorable predictor-validation theorem, whose stated A1–A3 assumptions do not directly license a nonsmooth clip RHS. That source may be a future common-smooth-law comparator, but smoothing clip for only one method would be invalid. Arcak–Maidens and TIRA remain important generic reachability threats, but they do not offer a closer explicit clip-corner method contract in the current G4 source audit.

**Consequence:** A published, nonsmooth-applicable external algorithm is available for a bounded method-level reproduction. Until the method is implemented and audited, no VALENCIA baseline result, superiority, or G4 conclusion exists. Calling an arbitrary locally coded coarse Picard method “Auer” or “VALENCIA” would not satisfy this comparison.

**Status:** **COMPARATOR SELECTED — method-level reproduction candidate with a source-version prerequisite. The original tool extension is not reproduced.**

**Required action:** Use the consolidated assignment below. Stop the external-comparison claim if the published derivative enclosure cannot be implemented for both clip switches with a checked mean-value property, if the old solver core cannot be mapped to the paper’s algorithm, or if the pinned source/dependency build cannot be reproduced. In that case report the precise blocker and do not substitute a custom coarse method under an external label.

## R3-SR-08 — One bounded next Luna assignment: matched Auer-method development comparison

**Finding:** The most informative next computation is a matched method comparison on the existing R3 domain, not a favorable new domain and not an enclosure ablation in isolation.

**Evidence:** R3 shows that zero alone has the full 140-group existential certification coverage. The remaining plausible advantage is tighter or cheaper coupled enclosure/contact evaluation relative to an established general validated IVP method. A matched comparison directly tests that claim on the same inputs. A new domain would add uncalibrated choices before the existing result is understood; a sharper signed-kernel ablation would not meet the open external-comparator obligation.

**Consequence:** This work tests the surviving plant/contact-structure advantage without converting the observed R3 development set into held-out evidence. W1 already authorizes applicable baseline adapters and reproducible offline validation tools; no extra policy authorization is needed merely to start this bounded validation branch.

**Status:** **PRIORITY SELECTED — G4 matched development comparison; G2 soundness/usefulness remain separately scoped.**

**Required action:** Luna should perform one consolidated assignment in this order.

### Prerequisite A — pin and audit the comparator method

1. Use the primary Auer–Kiel–Rauh 2013 article and the pinned ValEncIA-IVP/basic source snapshot above. Record exact source hashes, compiler/runtime, PROFIL/BIAS and FADBAD++ versions, license/availability, patches, and build commands.
2. Before benchmarking, write a method-to-code crosswalk for relevant article equations and code. Identify which public source release is the base and every code difference needed to implement the paper’s piecewise-smooth generalized derivative.
3. Derive and implement the clip enclosure at thresholds −1 and +1. State the branch derivative intervals, boundary convention, multi-switch handling, and interval mean-value inclusion used by the ODE validator. Add an exact arithmetic unit argument for the piecewise clip derivative contract; do not smooth, sample, or differentiate through a corner as if clip were C1.
4. Encode the full nine-state MASTER v2.1 ODE, exact rational label map, ξ̇=0, one fixed query voltage common to every label, and the identical initial box. Prove positivity of every denominator on the label domain. Preserve correlations at the mathematical label level; any interval hull loss must be an outward relaxation and reported.
5. Produce a source-faithfulness audit against Auer §4 and reproduce a published reference case from that paper before labeling the implementation a faithful method-level reproduction. A mismatch in the switching derivative, mean-value inclusion, set semantics, or enclosure output stops the comparator branch for review.

### Prerequisite B — freeze the matched protocol before comparator outputs

1. Input universe: all 1,944 original R3 state/scene/horizon/action queries, with the complete twelve-label family. Keep every original state cell, obstacle scene, hold, voltage, UNKNOWN, and failure in the denominator. The R3 grid is **development data already observed**, never held out.
2. Scientific contract, identical for both methods: exact MASTER v2.1 reduced ODE; clip law exactly as specified; full static-circle set and inflated radius; all nine exact voltage actions; each query’s same nonzero-width initial-state cell; same entire fixed parameter-label image; a single common held voltage; full closed hold interval [0,T]; and both full-hold collision clearance and parameter-specific contact admissibility.
3. Method outputs must be complete time tubes, not only endpoint boxes. Apply a common independently reviewed outward collision/contact post-check to both tubes. Report tube-only enclosure widths separately from checker-inclusive certificates.
4. Arithmetic: every interval, rational map, trigonometric range, generalized derivative enclosure, tube remainder, contact square root, and distance lower bound must be outward and auditable. A floating reference trajectory may help diagnose but cannot support CERTIFIED. Bind the checker implementation and all transitive dependencies. Shared low-level interval arithmetic is permitted only if disclosed and independently reviewed; report it as shared trusted code.
5. Preserve the existing R3 limits for its method: 16,384 rational bits, 1,000,000 metered arithmetic operations, and 15 seconds wall time per query. The comparator must use the same 15-second wall cap. If it can use the same exact-rational backend, apply the same bit and operation caps; otherwise freeze an explicit comparator precision/operation cap and report it in its own units before any output. In that case compare coverage, widths, and measured cost as a Pareto trade-off; do not claim equal-work or equal-precision superiority from unlike counters. Freeze source-specific work settings (step size/order, subdivision, interval precision) in advance. No cap tuning after outputs. Report representation, precision, operation/function/Jacobian counts, bit widths, step counts, subdivisions, CPU time, wall time, and peak memory. Do not equate Taylor degree with equal cost.
6. Freeze source/content hashes, method/profile IDs, per-query manifest, source manifests, timeout/overflow behavior, result schema, and a pre-run clean-tree record before invoking the matched evaluator. No precision, state/parameter split, obstacle, action, or tolerance changes after seeing status output.

### Required outputs

1. Pinned source/method note and Auer-to-code crosswalk, including both clip switches and fixed-label augmentation.
2. Independently reviewed baseline soundness note for the complete full-time tube and common collision/contact post-check.
3. Reference-case reproduction record and exact arithmetic tests for clip values/slopes at, below, and above both thresholds, including intervals crossing one or both thresholds.
4. Pre-run frozen matched-comparison protocol, immutable source/profile/input commitments, and environment/command metadata.
5. Machine-readable result records for all 1,944 original action queries, with per-query CERTIFIED, proof-complete UNKNOWN, resource UNKNOWN, unsupported/invalid input, and implementation failure separated; all denominators retained.
6. Action-group table and per-cell/per-action collision/contact margins, tube widths, proof status, reason codes, operation/precision/time/step/split counts, and grouped comparisons against R3.
7. Falsification report. If the Auer-method reproduction matches or dominates R3 coverage at comparable or smaller widths and cost, report no R3 advantage on this domain. If neither dominates, report the coverage/width/cost trade-off without a scalar winner chosen after observing results. If the baseline cannot be reproduced or soundly handles clip, stop and report the exact prerequisite failure; do not relabel an internal ablation as an external method.

### Stop conditions

- Stop before comparison if the source crosswalk, build, multi-switch clip derivative, fixed-parameter augmentation, or full-time validation proof does not close.
- Preserve the full original denominator and label unsupported inputs/failures; never drop them or turn a baseline limitation into evidence of R3 superiority.
- Stop the affected CERTIFIED path on any lost inclusion, clip-corner omission, variable-parameter/action semantics, invalid arithmetic, or checker mismatch.
- Do not adapt the R3 profile, physical model, parameter values, obstacles, voltages, or target margin to make the comparator produce a desired result.
- This task is finite one-hold offline validation. It does not include G3 recursion, an operational controller, task tracking, hardware calibration, or experiments.

## R3-SR-09 — Proposed context and evidence-status updates (not applied)

**Finding:** MASTER and REVIEW_GATE should record that a full R3 computational batch now exists, while retaining every canonical gate status.

**Evidence:** Current context predates the R3 batch and still describes only hand Cases A/B/C as finite instances. R3 is a significant evidence update but does not satisfy unresolved usefulness policy, practical-domain, external-comparison, physical-correspondence, or recursive obligations. The current branch was clean before creation of this report. The review request explicitly says not to apply context edits directly.

**Consequence:** Leaving the context unchanged would understate current G2 evidence. Promoting G2 or modifying any plant assumption would overstate it.

**Status:** **PROPOSED documentation-only synchronization; NOT APPLIED. No plant or gate change recommended.**

**Required action:** If the user accepts this review record, apply a separately reviewed evidence-only patch. Suggested exact text follows; no wording below was changed in this task.

### Proposed addition to MASTER §3 / §35 evidence history

~~~text
Computational evidence update (2026-09-30; R3): the frozen G2-COMP-clip synthetic development batch at implementation/evidence commit 4fd0451146ab9567a51499183db5a08f20ae8de5 covers 1,944/1,944 declared state/scene/horizon/action queries. The recorded evaluator/checker reports 1,196 CERTIFIED and 748 proof-complete UNKNOWN, with zero resource UNKNOWN, invalid input, or execution failure; the Codex artifact review independently checked archive/hash integrity, coverage, and all stored R3 distance witnesses but did not rerun the evaluator. Certificates occur on declared nonzero-width moving-state boxes with the full fixed uncertain parameter-label cell. Every group with any certified action also has zero voltage certified (140/140). This is finite synthetic offline evidence for the frozen clip-law fallback profile, not arbitrary-input implementation soundness, a matched prior-art comparison, online feasibility, physical correspondence, recursive safety, or a G2/G4 gate pass. See docs/reviews/CODEX_G2_VALIDATION_R3_REVIEW.md and docs/reviews/GPT_TO_CODEX_G2_VALIDATION_R3_SCIENTIFIC_REVIEW_FULL_HANDOFF.md.
~~~

Keep existing statements that G2/G3/G4 remain unverified, practical physical parameter relevance is open, no useful recursive set exists, and project status is HOLD. Do not change MASTER equations or assumptions.

### Proposed DECISION_LOG entry

~~~text
## 2026-09-30 — HOLD — record scoped R3 computational evidence

- Record review of implementation/evidence commit 4fd0451146ab9567a51499183db5a08f20ae8de5 and supplemental documents at aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46.
- Accept the directed-dyadic minimum-distance correction and the recorded 1,944-query G2-COMP-clip synthetic development batch in their declared scope: 1,196 CERTIFIED, 748 proof-complete UNKNOWN, zero resource/invalid/execution failures.
- The eight mixed groups are one moving state/horizon mechanism repeated over obstacle geometries; only V=(0,0) certifies, through the sufficient contact bound. Every group with any certified action also certifies zero (140/140).
- This is computational evidence, not arbitrary-input soundness, physical or online feasibility, recursive safety, novelty, or G2/G4 promotion. Overall HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED. Plant assumptions/formulation remain unchanged.
- Next W1 priority: source-audited Auer–Kiel–Rauh piecewise-smooth validated IVP method reproduction and matched development comparison on the already observed R3 universe; see the scientific review handoff.
~~~

### Proposed REVIEW_GATE.md G2 evidence-row replacement

~~~text
| G2 Certified enclosure | UNVERIFIED | Joint outer enclosure for every execution-fixed parameter, one held voltage, all times and coupled motor/wheel/body/contact dynamics | Analytic framework and synthetic hand Cases A/B/C accepted in their stated scopes. R3 completed a frozen 1,944-query G2-COMP-clip synthetic development batch: 1,196 CERTIFIED; 748 proof-complete UNKNOWN; zero resource/invalid/failure. Certificates exist on nonzero-width moving-state boxes with the full fixed uncertain label cell. All 140 groups with any certified action also certify zero. See ../docs/reviews/CODEX_G2_VALIDATION_R3_REVIEW.md and ../docs/reviews/GPT_TO_CODEX_G2_VALIDATION_R3_SCIENTIFIC_REVIEW_FULL_HANDOFF.md. Practical domain/usefulness acceptance, arbitrary-input evaluator closure, online timing, matched G4 comparison, and physical correspondence remain unverified.|
~~~

Keep existing G2 usefulness and parameter-relevance checkboxes open until the scope/use decision and its evidence are explicitly accepted. Do not alter G1/G3/G4 statuses. If any context evidence/status update is adopted, follow the repository’s Decision Log/version-maintenance rule; user authorization is required for a formulation change or gate promotion, neither of which is proposed here.

## R3-SR-10 — Final project status and authorization boundary

**Finding:** This review supports a narrow R3 evidence acceptance and a concrete next W1 comparison, while the project remains on HOLD.

**Evidence:** The R3 arithmetic correction and completed synthetic batch address previously open finite-computation questions. The batch goes beyond exact-rest Case C by including moving state boxes with positive speed, nonzero width in all state coordinates, full uncertain fixed labels, and contact-dependent certificate variation. It does not show nonzero-action group-coverage gain, online execution, a useful recursive set, hardware correspondence, or matched-method advantage. W1 explicitly permits scoped G2/G4 validation code and baseline adapters.

**Consequence:** No new user authorization is required to begin the bounded validation/comparator work under W1, provided it remains an offline one-hold method comparison. Any formulation/plant change, G3/controller/hardware work, or canonical gate promotion is outside this assignment and requires its own explicit authorization and recorded decision.

**Status:** **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical-platform correspondence UNVERIFIED.**

**Required action:** Use R3 as completed development evidence, preserve the old artifacts, and relay this file for Codex review. Do not commit a context update or gate promotion from this review alone.
