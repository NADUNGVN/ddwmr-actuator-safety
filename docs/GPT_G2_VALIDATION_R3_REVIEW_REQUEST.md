# GPT review request — G2 computational R3 and next scientific decision

## Required returned artifact

**Create a complete downloadable Markdown file named `GPT_TO_CODEX_G2_VALIDATION_R3_SCIENTIFIC_REVIEW_FULL_HANDOFF.md`.** The user is the intermediary and must be able to send that file to Codex. Do not return only a chat summary. If your environment cannot attach a file, provide its entire Markdown contents in one copyable block and explicitly state that attachment creation was unavailable.

Repository: `NADUNGVN/ddwmr-actuator-safety`.
Branch: `luna/g2-validation-v1`.
Review the implementation/evidence snapshot **`4fd0451146ab9567a51499183db5a08f20ae8de5`** and the subsequent Codex review/request documents. Record the exact commits you actually read. Use immutable links when possible; do not silently substitute a later implementation.

Local repository for the user's return to Codex:
`D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`.

## Authority and purpose

Read `AGENTS.md` and all four canonical `research_context/` files first. MASTER v2.1 remains authoritative; W1 authorizes scoped G2/G4 validation coding. **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.** Do not resurrect the superseded blanket code prohibition. Do not amend the plant or begin G3/controller/hardware work.

We now have a completed computational grid after the accepted synthetic hand Cases A/B/C. The purpose is a consolidated scientific review of what that evidence establishes and a concrete next matched-comparison assignment, not another open-ended series of arithmetic examples.

The generic architecture “predictor + validated residual/tube + set containment” remains prior art. No novelty from dyadic rounding, proof serialization, exact fractions or gzip is claimed.

## Read order

1. `AGENTS.md`, the four canonical context files.
2. `docs/reviews/CODEX_G2_VALIDATION_R3_REVIEW.md` — Codex's inspected findings and independent artifact analysis.
3. `docs/reviews/LUNA_TO_CODEX_G2_VALIDATION_R3_FULL_HANDOFF.md` — execution evidence, revisions and commands.
4. `docs/CODEX_TO_LUNA_G2_VALIDATION_R3.md` and `docs/LUNA_G2_DISTANCE_ADDENDUM_R3_v1.md` — assigned contract and implemented arithmetic.
5. `research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md`, `research/theorem_notes/G2_FINITE_EVALUATOR_SPEC_v1.md`, and `research/benchmarks/G2_USEFULNESS_BENCHMARK_SPEC_v1.md` — analytical dependencies and synthetic scope.
6. `validation/g2/evaluator.py`, `checker.py`, `rational.py`, `interval.py`, `model.py`, `polynomial.py`, `provenance.py`, plus `validation/scripts/verify_records_r3.py` and `run_pilot_r3.py`. Review the applicable mathematical path and trust boundary, not merely the pass counts.
7. R3 result summary, action-group summary, metadata, specification ledger, hash ledger and checker reports under `results/validation/g2/r3/`.
8. `docs/reviews/G4_MATCHED_PRIOR_ART_COMPARISON_v1.md`, `G2_PRIOR_ART_SUPPLEMENT_R2.md` and the prior consolidated GPT review. Existing source-access limitations remain explicit.

The 1,728 continuation proofs are losslessly stored as `conditional_full_grid_records_r3_v1.jsonl.gz`; the pilot proofs are `dev_pilot_records_r3_v1.jsonl`. The archive manifest gives the logical uncompressed path and hashes. If you cannot retrieve/decompress or execute these, state that limit and do not claim a new full-proof replay. The small summaries and code can still support a bounded scientific review.

## Evidence to challenge, not merely repeat

- Entire original development grid: **1,944/1,944 queries**, **1,196 CERTIFIED**, **748 proof-complete UNKNOWN**, zero resource UNKNOWN, invalid inputs or execution failures.
- Luna's checker reports **1,944 completed proof replays**. Codex did not rerun that engine; Codex independently checked coverage, hashes and exact stored distance inequalities/status signs.
- **21/21** result-ledger entries match; archive round-trip is 147,589,521 bytes with its recorded hash.
- Six nonzero-width moving-state cells, 12 obstacle scenes, three holds, nine voltages, one full uncertain 12-label parameter cell. No hardware identification, stiffness study, closed-loop trajectory or recursive set is included.
- 216 action groups: **132 all certified**, **76 all unknown**, **8 mixed**.
- All eight mixed groups use the same moving cell `state_low_mid`, `T=0.1 s`; **only V=(0,0)** is certified. All actions have positive collision lower margins in those groups. The other eight voltages return UNKNOWN solely through the sufficient contact bound. The eight geometries are not independent mechanisms.
- **Every group with any certified action also certifies zero voltage: 140/140.** This grid does not show increased existential group coverage from selecting nonzero voltage over checking zero alone.
- Recorded evaluator time: **0.109–0.313 s/query**, upper median **0.203 s**. Every query took longer than its tested hold. This is offline completion evidence, not a demonstration of an online policy.
- The method evaluated is the conservative finite-cell fallback. General computational signed-kernel/global-refinement superiority is not established by these artifacts.

## Review questions — answer together in one return

### A. Mathematical and computational scope

Audit the dyadic distance correction, its subtraction of `R_s+E_p`, full-hold semantics and distinction between rectangle minimum distance and all trajectory distances. Check preservation of fixed hidden parameters, common voltage, joint collision/contact predicates and initial-cell quantifiers. Identify any remaining branch that could emit an unsound CERTIFIED result, with equation/code evidence.

Give separate dispositions for (i) inspected local distance correction, (ii) upstream enclosure/finite evaluator contract, (iii) this complete synthetic development batch, and (iv) arbitrary supported inputs. Avoid treating a finite grid as a universal soundness proof or declining to acknowledge computational evidence merely because it is synthetic.

### B. G2 evidence accounting

Map the evidence to the existing G2 obligations. Explicitly distinguish:

1. finite evaluability and observed offline termination;
2. certificates on moving regions with nonzero widths and uncertain actuators;
3. voltage-dependent output versus practical voltage-selection value;
4. conservatism and preservation/relaxation of parameter dependence;
5. physical relevance and online timing.

State whether a scoped G2 disposition is supportable or G2 should remain UNVERIFIED, and identify the smallest remaining G2 evidence requirement under the existing criteria. Do not invent a post-result success-rate cutoff. Do not require G4 novelty as a substitute for a G2 soundness argument; conversely, numerical completion cannot establish novelty. Do not automatically promote any canonical gate.

### C. Meaning of the mixed groups and zero action

Assess the contact-driven distinction above. Is there a useful, narrowly defensible claim beyond the prior exact-rest Case C? What would falsify a claimed advantage? Zero is the stipulated closed zero-terminal-voltage condition; do not call it an instantaneous stop or recursive backup. Do not interpret UNKNOWN as physical contact violation or unavoidable collision.

The grid provides no nonzero action that certifies a group unavailable to zero. Decide whether the next informative step is a matched generic baseline on this domain, a justified prospective domain extension, or a sharper enclosure ablation. Choose and justify one priority; do not propose more hand cases solely to produce a favorable outcome.

### D. G4 comparator and one concrete next assignment

Provide a source-backed, applicable external comparator recommendation and a bounded implementation/comparison specification for Luna under existing W1 authorization. Inspect primary sources where needed; document source versions and exact assumptions. Existing nonsmooth clip behavior must be supported: a smooth-only theorem cannot be applied across clip corners without a sound extension. A shared smooth-law sub-benchmark is an alternative only if explicitly proposed and applied to both methods, not silently substituted in current R3.

Specify common input/uncertainty/state-cell/hold/collision/contact contracts, arithmetic requirements, comparison metrics and resource reporting. Distinguish internal ablations, a generic method implemented locally, and faithful reproduction of an established tool/method. A custom coarse method is not automatically an external baseline. Use the existing G4 comparison contract and identify exact unresolved applicability issues.

The R3 grid is development data already observed. It can support a transparently labeled development comparison; do not call reuse held-out. Any eventual locked confirmatory protocol must be prospectively declared. Do not select thresholds or omit UNKNOWNs after seeing comparator outputs.

If no justified comparator can be selected with available sources, report the exact applicability/access blocker and the smallest source-level task required, without pretending code permission is the blocker.

### E. Provenance and documentation

Assess Codex's small dependency-list issue: checker imports evaluator helpers, and model imports polynomial helpers, but the explicit source lists do not include all those transitive paths. Full Git revisions still identify them; no incompatible change was found in this batch. Classify proportionately and propose maintenance for the next version rather than retroactively rewriting R3 evidence.

Provide precise suggested evidence-status edits, if needed, for MASTER/DECISION_LOG/REVIEW_GATE so future sessions know that a full computational batch exists. Preserve plant assumptions and distinguish proposed gate changes from accepted evidence updates. Do not apply edits to the repository directly.

## Required output structure

For each finding use exactly:

**Finding / Evidence / Consequence / Status / Required action**.

The downloadable file must include:

- reviewed revisions and files, source-access and execution limits;
- separate acceptance/rejection scopes for R3 arithmetic, full-grid evidence, usefulness, runtime and novelty;
- a G2 obligation table separating resolved, partial and open items;
- explicit treatment of the eight contact-driven zero-action groups and 140/140 zero coverage;
- one consolidated next Luna assignment with prerequisites, outputs and stop conditions, or a precise applicability blocker;
- exact proposed context edits, if any, without silently adopting them;
- final project/gate disposition and whether any later decision requires the user's formulation authorization;
- the file name **`GPT_TO_CODEX_G2_VALIDATION_R3_SCIENTIFIC_REVIEW_FULL_HANDOFF.md`**.

Do not construct G3 or an operational controller. Do not finish with only “needs more work”: name the concrete scientific decision and minimal evidence that would resolve it.
