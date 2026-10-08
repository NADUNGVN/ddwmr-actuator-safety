# G3 J2 novelty audit — energy/contact backup seed

**Candidate:** `research/theorem_notes/G3_ZERO_VOLTAGE_ENERGY_BACKUP_SEED_v1.md`  
**J1 proof audit:** `docs/reviews/G3_ENERGY_BACKUP_SEED_J1_INDEPENDENT_PROOF_AUDIT.md`  
**Disposition:** `NOVELTY_HYPOTHESIS_SURVIVES_NARROWLY`  
**Meaning:** no exact overlap was found in the closest inspected sources for the full combination claimed below; this is not a completed systematic novelty proof and does not justify any `first` claim.  
**Gate effect:** none. Overall `HOLD`; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.

## 1. Candidate contribution under review

The candidate is **not**:

- a new backup-set concept;
- a new Lyapunov sublevel-set concept;
- a new energy-based CBF concept;
- a new robust backup CBF concept;
- a new adaptive safety concept for unknown parameters;
- a new sampled-data predecessor/invariance concept;
- a generic vehicle braking method.

The only contribution hypothesis that survives initial screening is the narrower conjunction:

> For the adopted voltage-driven nine-state DDWMR, use the exact electromechanical/contact power identity to construct a closed-form state-only terminal backup seed under one common held terminal voltage, with independent execution-fixed hidden tangential capacities, simultaneous continuous collision and algebraic contact-admissibility guarantees, and an explicit sufficient penalty quantifying full-parameter state-only rechecking when energy weights are hidden.

Even this hypothesis must still prove decision value in a larger recoverability/action construction before it can carry a paper.

---

## 2. Closest prior art inspected

### 2.1 Chen, Jankovic, Santillo, Ames — Backup Control Barrier Functions

**Citation:** Y. Chen, M. Jankovic, M. Santillo, A. D. Ames, “Backup Control Barrier Functions: Formulation and Comparative Study,” 60th IEEE CDC, 2021, pp. 6835–6841. DOI `10.1109/CDC45484.2021.9683111`. Author preprint/arXiv `2104.11332`.

**Inspected content:** author/publisher abstract and full-text formulation identified in prior repository audit; backup set based on a fixed backup policy, forward integration of backup flow, and enlargement into a control-invariant set.

**Established overlap:**

- fixed backup policy;
- backup set / recoverability construction;
- control-invariant safety logic;
- online forward prediction of the backup flow;
- comparison to invariant-set baselines.

**Not found in inspected scope:**

- terminal-voltage DDWMR electromechanical power identity;
- wheel-current-slip/contact coupling of the adopted plant;
- independent fixed hidden per-wheel capacity intervals with the MASTER quantifier order;
- simultaneous algebraic contact-domain and collision certificate specialized to this model;
- the proposed `rho` state-only fixed-parameter rechecking penalty.

**Conclusion:** generic backup-set logic is blocked as novelty; the plant-specific theorem remains potentially distinct.

---

### 2.2 van Wijk et al. — Disturbance-Robust Backup Control Barrier Functions

**Citation:** D. E. J. van Wijk, S. Coogan, T. G. Molnar, M. Majji, K. L. Hobbs, “Disturbance-Robust Backup Control Barrier Functions: Safety Under Uncertain Dynamics,” IEEE Control Systems Letters, 2024. DOI `10.1109/LCSYS.2024.3514998`.

**Primary source inspected:** author page and author-hosted PDF.

**Established overlap:**

- robust backup safety under uncertain dynamics;
- backup-flow uncertainty bounds;
- robust forward-invariant set construction;
- safety constraints tightened around an uncertain flow.

**Difference relevant to this candidate:**

The paper addresses unmodeled disturbances by bounding deviation between nominal and disturbed backup flows. The DDWMR candidate instead exploits an exact dissipativity identity that holds for every fixed capacity realization and derives a closed-form low-energy contact-safe seed without treating the hidden capacity as an arbitrary switching disturbance.

**Novelty caution:** “robust backup under uncertainty” is fully unavailable as a claim. The distinction must be the exact fixed-parameter voltage/contact structure and the resulting closed-form certificate.

---

### 2.3 Daş et al. — Robust Adaptive Backup Control Barrier Functions

**Citation:** E. Daş, D. E. J. van Wijk, T. G. Molnar, A. D. Ames, J. W. Burdick, “Robust Adaptive Backup Control Barrier Functions,” arXiv `2607.20842`, 2026.

**Primary source inspected:** arXiv abstract and available full-text/author repository metadata.

**Established overlap:**

- parametric uncertainty in drift and actuation matrix;
- backup-flow safety with unknown parameters;
- certified parameter-estimation error bounds;
- robust adaptive backup constraints;
- input constraints.

**Difference relevant to this candidate:**

The candidate does not estimate or adapt hidden parameters. It uses a state-only common action valid for the whole fixed hidden set, with the exact MASTER non-oracle quantifier. The candidate’s `rho` term explicitly quantifies conservatism caused by rechecking the whole parameter set at each sample rather than exploiting learned compatible parameters.

**Novelty caution:** unknown-parameter backup safety is prior art. Any paper must explain why deliberately state-only robust recursion is scientifically relevant and must not imply that fixed unknown parameters are a new safety setting.

---

### 2.4 Gacsi, Kiss, Molnar — Braking within Barriers

**Citation:** L. Gacsi, A. K. Kiss, T. G. Molnar, “Braking within Barriers: Constructive Safety-Critical Control for Input-Constrained Vehicles via the Backup Set Method,” arXiv `2510.15797`, 2025.

**Primary source inspected:** arXiv metadata and accessible full-text excerpts.

**Established overlap:**

- vehicle braking as safety-critical backup control;
- input-constrained backup controller;
- systematic backup set/controller pair construction;
- Lyapunov-equation-based invariant backup set;
- asymmetric road/friction vehicle example;
- stopping-distance relevance.

**Difference relevant to this candidate:**

The DDWMR seed is not a generic braking controller or a maximum/decelerating brake law. It uses `V=(0,0)` strictly as the modeled RL terminal condition, and safety follows from the full electromechanical stored-energy balance plus the contact-power sign, not from assuming a wheel braking force or feedback-linearized vehicle deceleration model.

The candidate also includes the adopted algebraic contact-validity constraint and hidden fixed per-wheel capacity semantics.

**Novelty caution:** “constructive braking backup set under friction/input constraints” is not available as a claim.

---

### 2.5 Kolathaya — Energy-based Control Barrier Functions for Robotic Systems

**Citation:** S. Kolathaya, “Energy based Control Barrier Functions for Robotic Systems,” TechRxiv preprint, 2020, DOI `10.36227/techrxiv.12831503`.

**Primary/full-text source inspected:** accessible preprint text.

**Established overlap:**

- safety barriers augmented by kinetic energy;
- robotic-system energy used directly in a safety certificate;
- forward invariance under actuator limits;
- damping/energy reasoning as a safety mechanism.

**Difference relevant to this candidate:**

The DDWMR construction includes electrical inductive energy, wheel rotational energy, body translational/yaw energy, explicit terminal voltage, and slip/contact dissipation. It also derives a geometric clearance-vs-energy terminal seed and a separate algebraic contact-admissibility energy threshold under hidden capacity uncertainty.

**Novelty caution:** “energy-based CBF” or “energy-based safety set” cannot be claimed as new.

---

### 2.6 Califano, Logmans, Roozing — kinetic-energy limiting CBF

**Citation:** F. Califano, D. Logmans, W. Roozing, “Limiting Kinetic Energy Through Control Barrier Functions: Analysis and Experimental Validation,” IEEE Robotics and Automation Letters 10(7), 2025, 7595–7602. DOI `10.1109/LRA.2025.3578847`.

**Inspected source:** article metadata/full-text abstract available.

**Established overlap:**

- kinetic-energy safety constraints;
- damping injection;
- energy-limiting CBF control;
- robotic experimental validation.

**Difference relevant to candidate:**

This prior art reinforces that energy limiting itself is established. The candidate’s possible distinction is not energy limitation; it is the exact voltage-driven DDWMR energy/contact structure and robust terminal seed with fixed hidden contact capacities.

---

## 3. Sampled-data and recursive-set prior art remains binding

The previous G3 feasibility audit already established direct overlap with:

- Mitchell et al. sampled-data discriminating kernels;
- Singletary et al. sampled-data/ZOH safety;
- Chen et al. backup invariant sets;
- Li–Liu validated one-period fixed-point synthesis;
- zero-order sampled-data barrier methods.

Therefore no part of the following can carry novelty:

\[
K\subseteq\operatorname{Pre}_T(K),
\]

one-step predecessor iteration, fixed-point recursion, held-input induction, or generic “safe between samples” logic.

---

## 4. Exact overlap table

| Candidate element | Prior art status | Novelty availability |
|---|---|---|
| Backup controller / terminal set | Established | **No** |
| Lyapunov/energy sublevel safe set | Established | **No** |
| Energy-based robotic CBF | Established | **No** |
| Robust backup under disturbances | Established | **No** |
| Adaptive backup under parametric uncertainty | Established | **No** |
| Vehicle braking backup set with friction/input constraints | Established | **No** |
| Sampled robust invariant/predecessor set | Established | **No** |
| Fixed common held voltage for recursive sampled safety | Generic logic established | **No**, by itself |
| Voltage/current/wheel/body/contact power identity for this DDWMR | Plant-specific derivation | **Potentially** |
| Contact dissipation `-F_j sigma_j` used to remove hidden `C_j` from the decay rate | Not found in closest sources | **Potentially** |
| Closed-form clearance `>= Gamma sqrt(E)` plus explicit algebraic contact-energy threshold for this plant | No exact match found | **Potentially** |
| Independent fixed hidden `C_L,C_R` without matched-side symmetry in that seed | No exact match found | **Potentially** |
| State-only full-Theta rechecking penalty `sqrt(rho)e^{-lambda T/2}` / `Gamma_T` | No exact match found | **Potentially**, but likely a sufficient-bound observation rather than standalone main contribution |
| Useful recoverability/action set with decision advantage | Not yet constructed | **Unknown; required** |

---

## 5. Contribution sentence that survives J2

The strongest defensible hypothesis after this audit is:

> We exploit the exact voltage-level electromechanical/contact power balance of a reduced DDWMR to construct a closed-form robust terminal safety seed that simultaneously bounds collision excursion and algebraic contact admissibility under independent execution-fixed hidden contact capacities, and use this seed to build a sampled recoverability filter whose certified action set is demonstrably less conservative than a matched generic backup/reachability baseline.

The final clause is not yet established and is mandatory for journal value.

Without the recoverability/action-set advantage, the current seed is likely best characterized as a useful plant-specific adaptation/theorem rather than a strong standalone contribution.

---

## 6. Claims forbidden after J2

Do not claim:

- first backup CBF;
- first energy-based safety barrier;
- first robust backup under uncertainty;
- first safe braking set;
- first friction-aware vehicle safety method;
- first sampled-data invariant safe set;
- first fixed-parameter safe controller;
- first use of a Lyapunov energy sublevel as a terminal set;
- generic superiority over prior-art reachability/backup methods;
- novelty solely from adding electrical dynamics to an existing backup method.

Do not use “first” at all unless a later systematic G4 closure supports the exact statement.

---

## 7. What must be proved next for the novelty to matter

A journal-relevant construction must turn the terminal seed into a **decision-making object**.

Minimum next theorem target:

\[
K_{rec}
=\left\{x:\exists V\in\mathcal U\ \forall\vartheta\in\Theta:
\begin{array}{l}
x_\vartheta(t;x,V)\in\mathcal S\cap D_c(\vartheta),\quad t\in[0,T],\\
x_\vartheta(T;x,V)\in K_E
\end{array}
\right\}.
\]

The proposed method must then show at least one of:

1. a strictly larger certified recoverability set than a matched generic backup-flow/tube construction;
2. a state where the plant-structured method certifies a task-compatible nonzero voltage and the matched baseline is proof-complete `UNKNOWN`;
3. a provable reduction in a declared conservatism term that changes an action decision;
4. an analytic complexity reduction enabling certification of a domain that a generic method cannot tractably evaluate under a matched resource contract.

A smaller enclosure width with no decision consequence is insufficient.

---

## 8. J2 disposition

### Finding

The broad ideas surrounding the candidate are heavily populated prior art, but no exact overlap was found for the complete voltage-DDWMR/contact/fixed-capacity closed-form seed plus the proposed state-only parameter-rechecking penalty.

### Evidence

The closest inspected works establish backup-set logic, robust/adaptive backup safety, vehicle braking backup construction, energy-based robotic safety and sampled-data recursive invariance. None of the inspected sources was found to contain the candidate’s exact combination of terminal voltage, inductive/wheel/body energy, slip-contact power cancellation, independent fixed hidden per-wheel capacities and simultaneous algebraic contact/collision threshold.

### Consequence

The branch remains scientifically worth pursuing **only** as a plant-specific construction leading to a useful recoverability/action filter and matched decision advantage. The seed alone should not be marketed as a strong journal contribution.

### Status

`NOVELTY_HYPOTHESIS_SURVIVES_NARROWLY`.

### Required action

Proceed to J3 analytic recoverability/action construction. Do not launch a numerical campaign yet. Predeclare the generic matched baseline and the exact decision criterion before any comparative execution.

**Gate statuses remain unchanged:** `HOLD`; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.
