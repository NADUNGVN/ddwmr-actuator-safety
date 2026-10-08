# DDWMR — Journal paper gate and research roadmap

**Status:** research roadmap only; does not change MASTER, DECISION_LOG, REVIEW_GATE or any gate status.  
**Current project status:** `HOLD`.  
**G1:** `PASS_RESTRICTED_REDUCED_MODEL_SCOPE`.  
**G2/G3/G4:** `UNVERIFIED`.  
**Physical-platform correspondence:** `UNVERIFIED`.

## 1. End goal

The project is complete for paper purposes only when there is a defensible journal-grade scientific package, not merely when an internal G3 artifact exists.

The target paper question is:

> Can a voltage-driven reduced DDWMR with execution-fixed hidden contact uncertainty admit a useful sampled recursive-safety construction in which one non-oracle voltage action guarantees continuous collision/contact safety over every hold and preserves future safe operation, with a plant-structured advantage over matched generic prior-art machinery?

The intended contribution is **not** generic predecessor recursion, backup-set logic, parameter augmentation, interval reachability, or a rest-state invariant set.

The intended contribution must be a specific theorem/computation exploiting the electromechanical/contact structure

`voltage -> current -> wheel dynamics -> slip -> contact force -> body/yaw -> collision/contact`

to produce a decision-relevant result unavailable to a matched generic baseline under the same assumptions.

## 2. Paper Gate

Define

`PAPER_READY = THEORY_SOUND && USEFUL_G3 && NOVELTY_CLOSED && MATCHED_EVIDENCE && REPRODUCIBLE_ARTIFACT`.

All five must be true.

### PG-1 — THEORY_SOUND

Required:

- adopted nine-state reduced model and information pattern remain explicit;
- one-hold enclosure/certificate soundness is independently audited;
- continuous collision and contact admissibility are proved over the entire hold;
- fixed hidden parameters are not reset;
- no oracle voltage selection;
- all theorem-local restrictions are explicit and scientifically defensible.

Failure condition: a proof needs an undeclared brake, symmetry, parameter reset, unobserved parameter, or unsound contact-margin regularity.

### PG-2 — USEFUL_G3

Required:

- a nonempty moving set with positive extent beyond rest states;
- an admissible state-only policy or action relation;
- robust endpoint return for every hidden realization;
- repeated operation follows by a proved recursion theorem;
- at least one task-compatible nonzero action is available from a meaningful moving domain, or a finite-step recoverability set returns to a certified terminal seed.

A terminal rest/decay set alone is not enough.

### PG-3 — NOVELTY_CLOSED

Required:

- closest sampled-data discriminating-kernel / invariant-set work audited;
- backup CBF / backup-set work audited;
- robust/adaptive backup under parametric uncertainty audited;
- force/friction-realizable mobile-robot safety audited;
- generic validated reachability audited;
- exact paper contribution distinguished at equation/theorem/computation level.

No `first` claim without this closure.

### PG-4 — MATCHED_EVIDENCE

Required:

- predeclared moving-state benchmark/domain;
- positive-width uncertainty;
- task/safety criterion frozen before outcome inspection;
- same plant, same uncertainty, same input set, same collision/contact predicates across methods;
- matched generic prior-art baseline;
- at least one decision-relevant separation, or a statistically/coverage meaningful domain result;
- resource caps and arithmetic policies disclosed and not mistaken for mathematical method superiority.

W2 development rows are historical development evidence, not confirmation.

### PG-5 — REPRODUCIBLE_ARTIFACT

Required:

- immutable source/result closure;
- independent replay/checker path;
- theorem assumptions bound to benchmark inputs;
- figures/tables generated from frozen artifacts;
- manuscript claims cross-referenced to proof/result objects;
- final independent scientific review before submission.

## 3. Current best theorem path

The current leading seed candidate is:

`research/theorem_notes/G3_ZERO_VOLTAGE_ENERGY_BACKUP_SEED_v1.md`.

It proposes a zero-terminal-voltage energy backup seed using the adopted nine-state power identity. Its scientific role is a **terminal recursive seed**, not the final useful controller.

Candidate strengths:

- common non-oracle action `V=(0,0)`;
- moving positive-extent states allowed;
- no `C_L=C_R` assumption;
- independent positive-width contact capacities allowed;
- no wheel-lock assumption;
- continuous collision and contact conditions treated simultaneously;
- fixed hidden parameter semantics retained;
- possible explicit penalty for state-only rechecking under broader hidden parameter uncertainty.

Candidate risks:

- strict positive mechanical damping lower bounds are theorem-local and must be justified or removed;
- backup/energy-set machinery has strong prior art;
- `V=0` terminal decay does not by itself supply task usefulness;
- exact novelty of the voltage/contact construction is not established;
- physical-platform correspondence remains outside the theorem.

## 4. Required sequence

### Phase J1 — Independent proof falsification

Do not implement G3 yet.

Audit the seed candidate adversarially:

1. rederive exact energy identity and contact-power signs;
2. check units and all extrema used in `lambda`, `Gamma`, `e_c`;
3. verify `E=0` and obstacle-distance nonsmooth cases;
4. verify state-only endpoint-return derivation for hidden energy weights;
5. determine whether strict mechanical damping is necessary or can be weakened;
6. construct a counterexample if any theorem statement is too broad.

Exit:

- `SEED_PROOF_SURVIVES`, or
- `SEED_REVISE`, or
- `SEED_STOP`.

### Phase J2 — Equation-level novelty audit

Only if J1 survives.

Compare exact construction with:

- sampled-data discriminating kernels;
- backup CBF / backup-set methods;
- disturbance-robust backup CBF;
- robust-adaptive backup CBF;
- constructive vehicle braking backup-set methods;
- energy/kinetic-energy CBF methods;
- friction/force-realizable mobile-robot safety.

Required output:

- exact overlap table;
- exact non-overlap hypothesis;
- prohibited novelty claims;
- one falsifiable contribution sentence.

Exit:

- `NOVELTY_HYPOTHESIS_SURVIVES`, or
- `GENERIC_ADAPTATION_ONLY`.

If `GENERIC_ADAPTATION_ONLY`, do not build a large G3 implementation for the current paper claim.

### Phase J3 — Useful recoverability construction

Only if J1 and J2 survive.

Use the certified energy seed as terminal set and construct a larger moving recoverability/action set:

\[
K_{rec}=\{x:\exists V\in\mathcal U\ \forall\vartheta\in\Theta,
\ x_\vartheta([0,T])\subseteq\mathscr S_c,
\ x_\vartheta(T)\in K_E\}.
\]

Then extend from one-step recoverability toward a useful recursive operating set/action relation.

Required scientific property:

- task-compatible nonzero actions exist from declared moving states;
- safe action selection changes with state;
- same voltage must remain valid for all hidden labels;
- repeated operation is proved rather than assumed.

### Phase J4 — Matched baseline protocol

Freeze before execution:

- operating domain;
- uncertainty domain;
- obstacle geometry;
- action set/optimizer;
- success metric;
- baseline implementation contract;
- resource policy;
- confirmation split.

Primary criterion should be decision-relevant, e.g. certified safe-action availability / recoverability coverage on a predeclared moving domain, not enclosure width alone.

### Phase J5 — Confirmation evidence

Run only after protocol freeze.

Required:

- unused confirmation inputs;
- independent replay/check;
- results separated into `CERTIFIED`, proof-complete `UNKNOWN`, resource-limited, audit failure and not-run;
- no post-hoc task threshold changes;
- no reuse of W2 development rows as confirmation.

### Phase J6 — Manuscript construction

Suggested journal paper structure:

1. Introduction and precise gap
2. Related work and contribution boundary
3. Reduced voltage-driven DDWMR model and information pattern
4. Sampled robust safety problem
5. Plant-structured energy/contact terminal seed
6. Recoverability / recursive safe-action construction
7. Soundness and recursive-safety theorems
8. Matched prior-art baseline
9. Frozen numerical study
10. Limitations and physical correspondence
11. Conclusion

The abstract must contain:

`problem -> construction -> theorem -> decision-relevant evidence -> scope limitation`.

## 5. Minimum theorem package for a journal submission

A strong manuscript should contain at least:

### T1 — One-hold soundness

A computable construction encloses every admissible fixed-parameter trajectory under one common held voltage.

### T2 — Continuous collision/contact theorem

The certificate implies continuous geometric collision safety and parameter-specific algebraic contact admissibility on the entire hold.

### T3 — Recursive-safety theorem

A useful moving set/action relation satisfies robust endpoint return, yielding repeated sampled operation by induction.

### T4 — Plant-structured discriminator

A theorem/proposition identifies the exact DDWMR electromechanical/contact structure responsible for a stricter or less conservative decision than a matched generic baseline.

T4 is the expected contribution carrier. T1–T3 alone may still be a competent application/adaptation paper, but not necessarily the intended strong journal contribution.

## 6. Stop rules

Stop or revise the current paper direction if any of the following occurs:

- the only provable recursive set is rest/singleton/symmetric-zero-width;
- common voltage fails under independent positive-width uncertainty on every meaningful moving domain;
- the energy seed needs scientifically unjustified damping assumptions;
- the exact construction is already covered by prior art with no material DDWMR-specific distinction;
- matched evidence shows no decision/coverage value beyond generic methods;
- proposed superiority depends on unmatched arithmetic/resource policies;
- physical claims become necessary for the story but physical correspondence remains unsupported.

A negative result should end the branch rather than trigger another large metadata/batch cycle.

## 7. Current position

Current evidence supports the following status:

- model/formulation foundation: advanced;
- finite one-hold certification machinery: substantial but not yet accepted as useful contribution;
- recursive terminal seed: now a concrete candidate, not yet independently accepted;
- useful multi-hold action policy: absent;
- novelty closure: absent;
- journal confirmation evidence: absent;
- manuscript-ready contribution: absent.

Therefore the immediate project phase is:

`J1 — INDEPENDENT PROOF FALSIFICATION OF THE ENERGY BACKUP SEED`.

No gate status changes from this roadmap.
