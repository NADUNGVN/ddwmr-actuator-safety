# GPT → CODEX G4 AUER R5 SCIENTIFIC REVIEW — FULL HANDOFF

**Repository:** `NADUNGVN/ddwmr-actuator-safety`  
**Branch reviewed:** `main`  
**Commit reviewed:** `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`  
**Review scope:** independent source-, equation-, proof-record-, composition-, provenance-, and protocol-level review of the frozen Auer R4/R5 reconstruction.  
**Authority:** MASTER v2.1.  
**Project disposition:** **HOLD**.  
**G1:** PASS — restricted reduced-model scope.  
**G2/G3/G4:** UNVERIFIED.  
**Physical-platform correspondence:** UNVERIFIED.  
**Matched Auer evaluations:** **0 / 1,944**.

This report follows `docs/GPT_G4_AUER_R5_SOURCE_REVIEW_REQUEST.md` and uses `docs/reviews/G4_AUER_R5_GITHUB_SOURCE_INDEX.md` as the repository evidence index.

No new matched batch was run for this review.

---

# 1. EXECUTIVE DISPOSITION

## Frozen R4/R5 scientific result

\[
\boxed{\textbf{VALID in the frozen one-case scope}}
\]

I accept, in the restricted scope actually supported by the published GitHub source and records, the following statements:

1. the R4 reconstruction implements a defensible specialization of the **Auer 2013 / Rauh–Auer 2011 residual-IVP method** for the continuous piecewise-linear benchmark `clip`;
2. the analytic branch-crossing fixture has a proof-complete residual/Picard record containing the exact analytic reference;
3. the preselected DDWMR query has a proof-complete one-step 21-coordinate interval enclosure record under one held voltage and one unchanged full 12-label parameter image;
4. the independently implemented `replay_ivp.py` recomputes the proof algorithmically rather than importing the producer RHS/solver;
5. R5 closes the R4 persistent-composition gap for that frozen query by loading the stored proof, replaying it, reconstructing `NATIVE_TOTAL_HULL`, recomputing the common collision/contact predicate, rebuilding the composition, and comparing the stored records;
6. the 17 published R5 file-based mutation trials exercise the declared native/common/composition layers and are classified consistently with their actual first mismatch.

The correct label is:

> **paper-faithful Auer 2013 method reconstruction using exact-rational validated arithmetic**

not:

> original ValEncIA / VALENCIA software reproduction.

## Important qualification

This is one proof-backed synthetic DDWMR state/action/parameter box.

It is **not**:

- a 1,944-query matched result;
- G4 closure;
- evidence of generic reachability novelty;
- proof of practical superiority;
- G2 usefulness closure;
- G3;
- physical robot validation.

## Matched-batch decision

\[
\boxed{\textbf{NO-GO for executing the 1,944-query batch under protocol v2 as published}}
\]

The reason is **not** a newly discovered defect in the R4/R5 single-case proof.

The reason is that `G4_AUER_MATCHED_PROTOCOL_v2.md` is explicitly `PREPARATION ONLY; NOT LOCKED` and still specifies the obsolete preflight Auer path:

- WSL2 / PROFIL/BIAS;
- binary64 Auer segment semantics;
- an old resource policy;
- an accepted-step width proposal inconsistent with the proof-producing R4 development profile.

R4/R5 instead use:

- exact rational endpoints;
- exact-rational Taylor sine/cosine enclosures;
- a 21-coordinate residual/Picard proof record;
- `NATIVE_TOTAL_HULL`;
- a different frozen small-case resource profile.

Therefore a **protocol v3 must be reviewed and frozen before batch execution**.

## What can proceed now

\[
\boxed{\textbf{GO to protocol-v3 preparation/freeze, not to batch execution}}
\]

Before a batch, protocol v3 must also include one actual archived R3 proof routed through the common adapter/checker, because the published source contains the R3 adapter but I found no published real historical R3→common parity artifact.

Once those two issues are closed, this review finds **no remaining mathematical blocker in the frozen R4/R5 one-case proof mechanism itself** that would require abandoning the Auer comparator.

---

# 2. MATERIALS INDEPENDENTLY READ

## 2.1 Canonical project context

Read first, as required:

- `AGENTS.md`
- `research_context/MASTER_RESEARCH_CONTEXT_v2.md`
- `research_context/DECISION_LOG.md`
- `research_context/LITERATURE_MATRIX.md`
- `research_context/REVIEW_GATE.md`

Canonical status is unchanged:

\[
\boxed{
\text{HOLD;\ G1 restricted PASS;\ G2/G3/G4 UNVERIFIED;\ physical correspondence UNVERIFIED}
}
\]

Workflow W1 permits scoped G2/G4 validation work but does not promote any scientific gate.

## 2.2 G4 request/index and contracts

Read:

- `docs/GPT_G4_AUER_R5_SOURCE_REVIEW_REQUEST.md`
- `docs/reviews/G4_AUER_R5_GITHUB_SOURCE_INDEX.md`
- `docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md`
- `research/theorem_notes/G4_AUER_BASELINE_CONTRACT_v1.md`
- `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v2.md`

## 2.3 R4/R5 handoffs and Codex reviews

Read directly from GitHub:

- `docs/reviews/LUNA_TO_CODEX_G4_AUER_R4_IVP_CORE_FULL_HANDOFF.md`
- `docs/reviews/CODEX_G4_AUER_R4_IVP_CORE_REVIEW.md`
- `docs/reviews/LUNA_TO_CODEX_G4_AUER_R5_COMPOSITION_REPLAY_FULL_HANDOFF.md`
- `docs/reviews/CODEX_G4_AUER_R5_COMPOSITION_REPLAY_REVIEW.md`

These documents were treated as claims/evidence leads, not as proof by model agreement.

## 2.4 Proof-critical source inspected

Direct source inspection included at least:

- `validation/baselines/auer2013/residual_ivp.py`
- `validation/baselines/auer2013/replay_ivp.py`
- `validation/baselines/auer2013/rhs.py`
- `validation/baselines/auer2013/piecewise.py`
- `validation/baselines/auer2013/r4_worker.py`
- `validation/baselines/auer2013/process_limiter.py`
- `validation/g4/common_tube.py`
- `validation/g4/verify_common_tube.py`
- `validation/scripts/verify_auer_composition_replay_v1.py`
- shared:
  - `validation/g2/rational.py`
  - `validation/g2/interval.py`
  - `validation/g2/model.py`

## 2.5 R4/R5 artifacts inspected

Directly inspected:

- `results/validation/g4/auer2013/r4_analytic_fixture_native_v2.json`
- `results/validation/g4/auer2013/r4_analytic_fixture_evidence_v2.json`
- `results/validation/g4/auer2013/r4_ddwmr_single_query_native_v2.json`
- `results/validation/g4/auer2013/r4_ddwmr_single_query_evidence_v2.json`
- `results/validation/g4/auer2013/r4_output_artifact_manifest_v1.json`
- `results/validation/g4/auer2013/source_snapshot_v10/snapshot_manifest.json`
- `results/validation/g4/auer2013/r5_composition_replay_v1/pristine_replay_report.json`
- `results/validation/g4/auer2013/r5_composition_replay_v1/trial_ledger_v1.json`
- `results/validation/g4/auer2013/r5_composition_replay_v1/r5_artifact_manifest_v1.json`
- `results/validation/g4/auer2013/r5_composition_replay_v1/pre_freeze_setup_attempts_v1.json`
- `results/validation/g4/auer2013/r5_composition_replay_v1/source_snapshot_v11/snapshot_manifest.json`
- saved common/composition inputs and mutation artifacts.

---

# 3. PRIMARY-SOURCE BASIS

## 3.1 Auer, Kiel & Rauh 2013

Primary publication:

Ekaterina Auer, Stefan Kiel, Andreas Rauh,  
**“A verified method for solving piecewise smooth initial value problems,”**  
*International Journal of Applied Mathematics and Computer Science*, 23(4), 731–747, 2013.  
DOI: `10.2478/amcs-2013-0055`.

Public full text:

`https://zbc.uz.zgora.pl/Content/78882/AMCS_2013_23_4_4.pdf`

The publication explicitly treats algorithmically represented right-hand sides containing piecewise-smooth scalar functions and introduces a generalized first-derivative enclosure for them.

Relevant source mapping:

- Eq. (27): algorithmic RHS composition;
- Eq. (28): piecewise-smooth scalar primitive;
- Eq. (33): generalized derivative for a continuous piecewise function;
- Eq. (40): derivative construction at switching points;
- Eq. (42):
  \[
  x^*(t)\in \tilde x(t)+R(t);
  \]
- Eq. (43):
  \[
  \dot R^{(k+1)}(t)
  =
  -\dot{\tilde x}(t)+f(x^{(k)}).
  \]

The paper explicitly says mean-value forms need derivatives satisfying the required enclosure relation to preserve verification.

## 3.2 Rauh & Auer 2011

Primary publication:

Andreas Rauh, Ekaterina Auer,  
**“Verified Simulation of ODEs and DAEs in ValEncIA-IVP,”**  
*Reliable Computing* 15(4), 370–381, 2011.

Official public PDF:

`https://www.reliable-computing.org/reliable-computing-15-pp-370-381.pdf`

Algorithm 1, printed page 372, states:

\[
[x_{\rm encl}(t)]
=
x_{\rm app}(t)+[R(t)],
\tag{3}
\]

then iterates:

\[
[\dot R^{(k+1)}(t)]
=
-\dot x_{\rm app}(t)
+
f(x_{\rm app}(t)+[R^{(k)}(t)],t),
\tag{4}
\]

accepting the derivative enclosure when:

\[
[\dot R^{(k+1)}]
\subseteq
[\dot R^{(k)}],
\]

and integrates the residual with the guaranteed bound:

\[
[R^{(k+1)}(t)]
\subseteq
[R^{(k+1)}(0)]
+
t\,
r([R^{(k)}([0,t])],[0,t]).
\tag{6}
\]

Initial uncertainty is included by choosing \(R(0)\) so that the initial interval lies in \(x_{\rm app}(0)+R(0)\).

## 3.3 Source-metadata correction

### Finding

The DOI printed in `G4_AUER_METHOD_CONTRACT_v2.md` for the Rauh–Auer 2011 paper is not supported by the authoritative Reliable Computing article/issue sources I could verify.

The contract currently gives:

`10.1007/s11128-010-0165-6`.

The official Reliable Computing volume and PDF establish the title, authors, volume, pages and Algorithm 1, but I did not find authoritative support for that DOI.

### Consequence

This is a bibliographic defect, not a defect in the proof equations.

### Status

**PARTIAL**

### Required action

Remove that DOI from the next contract revision unless an authoritative DOI record is produced.

Use:

> Rauh & Auer, *Reliable Computing* 15(4):370–381 (2011)

with the official Reliable Computing URL as the verified locator.

Do not change frozen R4/R5 numerical artifacts for this metadata correction.

---

# 4. FINDING M1 — METHOD MAPPING TO AUER / RAUH–AUER

## Finding

The R4 residual step is a defensible **paper-faithful reconstruction** of the published residual/Picard enclosure architecture for this continuous piecewise-smooth benchmark.

It is not an original VALENCIA software reproduction.

## Evidence

The method contract maps:

\[
x_{\rm encl}
=
x_{\rm app}+R
\]

to a linear/piecewise-\(C^1\) approximate path plus a validated residual.

For each slab, code constructs:

\[
R_{\rm old}
=
R_0+[0,h]D_{\rm old},
\]

\[
Q
=
x_{\rm app}([0,h])+R_{\rm old},
\]

and computes the mean-value enclosure:

\[
D_{\rm new}
=
-\dot x_{\rm app}
+
f(x_{\rm app})
+
J(Q)R_{\rm old}.
\]

It accepts only if:

\[
D_{\rm new}\subseteq D_{\rm old}
\]

and the induced integrated enclosure satisfies:

\[
R_0+[0,h]D_{\rm new}
\subseteq
R_{\rm old}.
\]

This is a mean-value-form enclosure of the Auer/Rauh residual operator rather than a literal evaluation of Eq. (4) on the raw dependent expression.

The construction retains exactly the central proof obligations of the source:

- approximate path;
- residual derivative enclosure;
- fixed-point/self-map inclusion;
- verified integration;
- full-time tube;
- endpoint propagation.

Differences from original software include:

- exact rational intervals instead of historical PROFIL/BIAS;
- project-specific 21-coordinate interval AD;
- JSON proof records;
- no claim to reproduce VALENCIA source/binary;
- project-specific deterministic subdivision/resource logic.

## Consequence

“Paper-faithful method reconstruction” is scientifically defensible.

“Original Auer/VALENCIA software reproduction” is not.

## Status

\[
\boxed{\textbf{VALID}}
\]

## Required action

Retain the reconstruction qualifier in every batch paper/table/manifest.

Never collapse “published method” and “historical software implementation.”

---

# 5. FINDING M2 — CONTINUOUS CLIP AND GENERALIZED DERIVATIVE

## Finding

The piecewise `clip` layer is sound for the selected continuous law and matches the relevant Auer generalized-derivative requirement.

## Evidence

Implemented law:

\[
\phi(q)=\operatorname{clip}_{[-1,1]}(q).
\]

`piecewise.py::clip_interval` uses the exact monotone interval range:

\[
\phi([a,b])
=
[\phi(a),\phi(b)].
\]

`clip_derivative_interval` uses:

\[
D\phi(X)=
\begin{cases}
\{0\},
&X\subset(-\infty,-1)\text{ or }X\subset(1,\infty),\\[1mm]
\{1\},
&X\subset(-1,1),\\[1mm]
[0,1],
&X\text{ touches or crosses either corner}.
\end{cases}
\]

At singleton corner values and intervals ending exactly at \(\pm1\), the code returns `[0,1]`, so no one-sided derivative is silently discarded.

The continuous clip has no value jump at either corner, so the discontinuity correction used by Auer for genuinely discontinuous primitives is zero here.

The AD implementation applies this scalar derivative enclosure through the composed slip/force computation.

## Important empirical coverage qualification

The analytic R4 fixture crosses the \(+1\) corner.

The frozen DDWMR R4 rough domain does **not** reach either clip corner.

From the published first residual rough domain, I independently reconstructed approximately:

\[
\sigma_L/v_s
\in[-0.29896,\ 0.29856],
\]

\[
\sigma_R/v_s
\in[-0.29470,\ 0.29460].
\]

Therefore:

- both corners are covered by inspected source logic;
- \(+1\) is exercised by the analytic proof fixture;
- the frozen DDWMR proof itself remains entirely in the unsaturated branch;
- no published proof artifact specifically stress-tests the \(-1\) corner.

## Consequence

No clip-corner mathematical blocker was found.

But do not claim that the frozen DDWMR case empirically exercises saturation.

## Status

**VALID for implementation logic; PARTIAL for branch-coverage evidence**

## Required action

No change to the frozen proof.

A future regression suite may include a \(-1\) analytic corner fixture, but that is not required to reinterpret R4/R5.

---

# 6. FINDING M3 — 21-COORDINATE JACOBIAN AND FIXED PARAMETERS

## Finding

The producer and replay checker correctly represent the selected benchmark as:

- nine dynamic physical states;
- twelve fixed parameter labels;
- zero derivatives for all labels.

The construction preserves fixed-parameter semantics while allowing conservative dependency loss.

## Evidence

The replay checker independently creates a 21-dimensional AD variable vector.

The physical parameter maps are evaluated from the 12 labels, including correlations such as:

\[
J_L=\frac1{\rho_L},
\qquad
J_R=\frac1{\rho_R}.
\]

The labels are not replaced by independent \(J\)-intervals as new hidden variables.

The exact physical RHS reconstructed by `replay_ivp.py` is:

\[
\dot p_x=u\cos\theta,
\qquad
\dot p_y=u\sin\theta,
\qquad
\dot\theta=r,
\]

\[
\sigma_L=R_w\omega_L-u+br,
\]

\[
\sigma_R=R_w\omega_R-u-br,
\]

\[
F_j=C_j\phi(\sigma_j/v_s),
\]

with the accepted body, wheel and current equations.

The 12 label RHS coordinates are exactly zero.

At the saved DDWMR endpoint, I independently checked from the proof JSON that all twelve label intervals are unchanged.

## Consequence

The computation is an outer box relaxation of a fixed-label family, not a switching-parameter model.

Correlation can be lost numerically because interval boxes are used, but labels are not resampled in time.

## Status

\[
\boxed{\textbf{VALID}}
\]

## Required action

Keep the existing wording:

> fixed labels; interval dependency loss may broaden but never narrow/resample the parameter image.

---

# 7. FINDING M4 — MEAN-VALUE / PICARD INCLUSION

## Finding

The accepted-step inclusion is mathematically sound for this locally Lipschitz continuous-clip ODE under the inspected interval arithmetic.

No hidden differentiability of `clip` at its corners is used.

## Evidence

For a compact convex rough box:

\[
Q=x_{\rm app}([0,h])+R_{\rm old},
\]

the generalized interval Jacobian \(J(Q)\) encloses the componentwise secants of the RHS.

The clip derivative interval `[0,1]` at the corner is sufficient for the scalar mean-value difference of a continuous piecewise-linear saturation.

All other RHS operations used here are smooth on the positive parameter domain.

Therefore, for:

\[
r\in R_{\rm old},
\]

the residual RHS is enclosed by:

\[
-\dot x_{\rm app}
+
f(x_{\rm app})
+
J(Q)r.
\]

The code checks:

\[
D_{\rm new}
\subseteq
D_{\rm old}.
\]

It also explicitly checks:

\[
R_{\rm new}
=
R_0+[0,h]D_{\rm new}
\subseteq
R_{\rm old}.
\]

For an interval derivative set \(D\), the integral over any \(t\in[0,h]\) is enclosed by:

\[
tD,
\]

and the union over the full slab is enclosed by:

\[
[0,h]D.
\]

Hence the recorded full-time residual hull is an all-time slab enclosure, not endpoint sampling.

The exact formal vector field is locally Lipschitz on the accepted parameter domain because:

- the clip is globally Lipschitz;
- all denominator parameter images are strictly positive;
- the remaining operations are smooth.

Thus trajectory uniqueness/continuation presents no switching-mode ambiguity for this continuous ODE.

## Consequence

The residual inclusion supplies a valid route from the approximate path to an exact formal-model tube.

## Status

\[
\boxed{\textbf{VALID}}
\]

## Required action

No mathematical change required.

Retain the distinction from the discontinuous Auer case: this project uses a continuous nonsmooth law.

---

# 8. FINDING M5 — EXACT-RATIONAL / TAYLOR ARITHMETIC

## Finding

The active R4 arithmetic path avoids the old PROFIL/BIAS/glibc issue and is sound at the inspected primitive level.

## Evidence

`ARITHMETIC_BACKEND_MANIFEST_v2.json` explicitly excludes the historical PROFIL/BIAS x86-64 path from R4 proof output.

Accepted endpoints use Python exact `Fraction` arithmetic with explicit rational bit/operation budgets.

`Interval` operations use exact rational endpoint arithmetic.

For trigonometry:

- `interval_sine`
- `interval_cosine`

evaluate Taylor polynomials by interval arithmetic and add a symmetric global Lagrange remainder:

\[
\frac{M^{n+1}}{(n+1)!},
\qquad
M=\max(|x_{\min}|,|x_{\max}|).
\]

Every derivative of sine/cosine has absolute value at most one, so this is a valid global Taylor remainder bound about zero.

The result is safely intersected with the universal range:

\[
[-1,1].
\]

No host `libm` sine/cosine result is used in the proof endpoints.

`sqrt_lower` uses exact rational bisection and exact square comparison for the common predicate.

## Consequence

The former PROFIL/BIAS rounding blocker does not apply to the R4/R5 proof-producing path.

The price is possible conservatism and rational growth, controlled by explicit resource caps.

## Status

\[
\boxed{\textbf{VALID at the inspected arithmetic-contract level}}
\]

## Required action

Future protocol text must describe this exact-rational backend, not the obsolete PROFIL/BIAS candidate backend.

---

# 9. FINDING M6 — REPLAY INDEPENDENCE

## Finding

`replay_ivp.py` is meaningfully **algorithmically independent** from the R4 producer, but not arithmetically independent.

## Evidence

The replay module does not import:

- `residual_ivp.py`;
- producer `rhs.py`;
- producer `piecewise.py`.

It reimplements:

- clip interval range;
- clip generalized derivative;
- interval AD;
- the complete 21-coordinate DDWMR RHS;
- parameter-map differentiation;
- residual iterations;
- Jacobian-times-remainder;
- subset tests;
- endpoint;
- total hull.

It then compares reconstructed serialized fields against the stored proof.

However, producer and replay share:

- `validation/g2/rational.py`;
- `validation/g2/interval.py`.

Therefore an error in those shared exact interval/Taylor primitives could affect both producer and replay.

The backend manifest discloses this explicitly.

## Consequence

Claims allowed:

> independent algorithmic proof replay.

Claim not allowed:

> independent numerical/arithmetic implementation verification.

## Status

\[
\boxed{\textbf{VALID with explicit independence boundary}}
\]

## Required action

Preserve the current disclosure.

No second arithmetic library is required merely to retain the frozen one-case result, but shared arithmetic must be stated in any publication comparison.

---

# 10. FINDING M7 — DIRECT INDEPENDENT AUDIT OF THE SAVED DDWMR PROOF

## Finding

The essential inclusion relations in the published DDWMR proof record check independently; the `PROOF_COMPLETE` flag is not the sole basis for acceptance.

## Evidence

From:

`results/validation/g4/auer2013/r4_ddwmr_single_query_native_v2.json`

I independently parsed exact rational endpoints and recomputed, for **all 21 coordinates**:

### Old remainder

\[
R_{\rm old}
=
R_0+[0,h]D_{\rm old}.
\]

Result:

> exact equality with the serialized `old_full_time_remainder` on all 21 coordinates.

### New remainder

\[
R_{\rm new}
=
R_0+[0,h]D_{\rm new}.
\]

Result:

> exact equality with the serialized `new_full_time_remainder` on all 21 coordinates.

### Derivative inclusion

\[
D_{\rm new}\subseteq D_{\rm old}.
\]

Result:

> true componentwise for all 21 coordinates.

### Integrated inclusion

\[
R_{\rm new}\subseteq R_{\rm old}.
\]

Result:

> true componentwise for all 21 coordinates.

### Total full-time hull

\[
X_{\rm tube}
=
X_{\rm app}([0,h])+R_{\rm new}.
\]

Result:

> exact equality with the serialized `full_time_total_hull_augmented` on all 21 coordinates.

### Endpoint

\[
R(h)=R_0+hD_{\rm new},
\]

\[
X(h)
=
X_{\rm app}(h)+R(h).
\]

Result:

> exact equality with the serialized `endpoint_end_augmented` on all 21 coordinates.

The stored global endpoint equals the accepted-step endpoint.

### Fixed labels

Result:

> all 12 label endpoint intervals equal the original complete label intervals.

### Time

Single accepted slab:

\[
[0,1/50].
\]

It covers the complete declared hold.

## Consequence

The central saved proof relations withstand an independent exact-rational recomputation.

This still does not constitute a formal verification of every line of the Python implementation.

## Status

\[
\boxed{\textbf{VALID}}
\]

## Required action

Retain the R4 proof as frozen single-case evidence.

---

# 11. FINDING M8 — ANALYTIC BRANCH-CROSSING FIXTURE

## Finding

The exact reference in the analytic fixture is correct and the fixture genuinely crosses the \(+1\) clip corner with uncertain crossing time.

## Evidence

Fixture:

\[
\dot x=1,
\qquad
\dot y=\operatorname{clip}(x),
\]

\[
x(0)\in[0.9,0.91],
\qquad
y(0)=0,
\qquad
T=0.2.
\]

Crossing time:

\[
t_c=1-x_0
\in[0.09,0.10].
\]

Exact endpoint:

\[
x(T)\in[1.10,1.11].
\]

After crossing:

\[
y(T)
=
0.2-\frac12(1-x_0)^2.
\]

Therefore:

\[
y(T)
\in
\left[
\frac{39}{200},
\frac{3919}{20000}
\right]
=
[0.195,\ 0.19595].
\]

I independently recomputed both endpoint extrema.

The stored native record reports one accepted Picard iteration and full-time/endpoint boxes containing the exact reference.

## Consequence

The piecewise derivative path is not validated solely on smooth interior intervals.

## Status

\[
\boxed{\textbf{VALID}}
\]

## Required action

Retain the label:

> independent analytic Auer-method validation fixture; not Auer §5 reproduction.

---

# 12. FINDING M9 — COMMON SAFETY PREDICATE

## Finding

The common predicate is correctly separated from the upstream ODE reachability proof.

Its formulas are sound sufficient bounds on a supplied full-time state box.

## Evidence

`TubeSegment` explicitly states that `state_hull` already includes all native/adapter radius.

For the R4 exact-rational path:

- mode:
  `NATIVE_TOTAL_HULL`;
- radius expansion count:
  `0`.

The common checker does **not** add another radius.

It checks:

- exact closed-hold coverage;
- unchanged fixed-label intervals;
- endpoint containment/chaining;
- initial-cell coverage.

Collision:

- computes minimum coordinate gaps from the position rectangle to obstacle center;
- sums squared lower gaps;
- takes an outward rational square-root lower bound;
- subtracts \(R_s\).

Contact:

- computes normalized slip interval;
- exact clip range;
- upper \(|\phi|\);
- lower per-wheel lateral reserve;
- upper:

\[
|mur|
\]

using interval magnitudes.

This is conservative but sound.

The common layer deliberately records:

- `certificate_emitted=false`;
- `ode_tube_proof_replayed=false`.

## Consequence

The correct logic is:

\[
\text{native IVP proof}
\quad+\quad
\text{common predicate PASS}
\]

not:

\[
\text{common predicate PASS}
\Rightarrow
\text{ODE proof}.
\]

## Status

\[
\boxed{\textbf{VALID}}
\]

## Required action

Keep native replay, common predicate, and final research interpretation as three separate layers.

---

# 13. FINDING M10 — R5 STORED-ARTIFACT COMPOSITION

## Finding

R5 successfully closes the specific R4 persistent-composition gap for the frozen query.

## Evidence

`verify_auer_composition_replay_v1.py`:

1. checks frozen inputs/source/profile bindings;
2. loads the stored native proof;
3. calls `replay_native_proof`;
4. only after successful replay constructs the full-time common segment directly from the replayed proof's accepted total hull/endpoints;
5. sets:
   - `NATIVE_TOTAL_HULL`;
   - radius count 0;
6. calls the common collision/contact checker;
7. compares the entire recomputed common record with the stored common record;
8. reconstructs the expected composition;
9. compares the stored composition field-by-field.

The pristine R5 report records:

- native replay PASS;
- one segment;
- common `PASS_ON_SUPPLIED_TUBE`;
- composition PASS;
- `certificate_emitted=false`.

The frozen composition binds:

- query:
  `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`;
- action:
  \[
  (-1,-1)\ {\rm V};
  \]
- native proof file hash;
- native proof body hash;
- common record hash;
- segment hash;
- v10 source-snapshot manifest hash.

## Exact margins

Collision lower margin:

\[
\frac{
3217536069938172178905080151780338213
}{
85070591730234615865843651857942052864
}
\approx 0.03782195 >0.
\]

Contact lower margin:

\[
\frac{
97189909371752867237790996600749227846061205518751
}{
51922968585348276285304963292200960000000000000000
}
\approx1.87180957>0.
\]

These are common-predicate lower bounds on the proof-derived full-time hull.

## Consequence

For this frozen formal reduced-model query, the composition:

\[
\text{native proof}
\to
\text{total hull}
\to
\text{common predicate}
\]

is reproducibly bound.

This does not make `PASS_ON_SUPPLIED_TUBE` alone a safety certificate.

## Status

\[
\boxed{\textbf{VALID}}
\]

## Required action

Preserve the exact layer names in future batch output.

---

# 14. FINDING M11 — 17 R5 MUTATION TRIALS

## Finding

The 17 published file-based mutations are classified consistently with their actual verifier rejection layer.

## Evidence

Published ledger contains:

- 5 native-proof mutations;
- 6 common-record mutations;
- 6 composition mutations.

I inspected the actual ledger details.

### Native layer

All five return:

`native_proof_failure`

with specific proof mismatches:

- total hull;
- residual iterate;
- endpoint;
- proof digest;
- held action / query-action binding.

### Common layer

All six return:

`common_predicate_mismatch`

on the expected specific field:

- segment hull;
- endpoint;
- radius mode;
- radius count;
- exact margin;
- segment hash.

### Composition layer

All six return:

`composition_mismatch`

on:

- proof digest;
- common-check digest;
- segment digest;
- query ID;
- held action;
- source-snapshot digest.

The pristine replay is the 18th ledger entry and passes.

## Consequence

These trials are meaningful stored-artifact tests, unlike the older R4 in-memory dictionary inequality checks.

They do **not** prove verifier completeness against every possible tamper or implementation bug.

## Status

\[
\boxed{\textbf{VALID for the declared 17 mutations}}
\]

## Required action

Do not call the mutation suite exhaustive formal verification.

---

# 15. FINDING M12 — PUBLISHED HASH INTEGRITY VS UNPUBLISHED SNAPSHOT MEMBERS

## Finding

A substantial portion of source/artifact provenance is independently verifiable from GitHub, but the complete v10/v11 snapshot membership is **not** independently reproducible from the public repository alone.

## Evidence

I independently recomputed SHA-256 from the exact GitHub bytes and matched the declared hashes for these proof-critical sources:

- `residual_ivp.py`
- `replay_ivp.py`
- `rhs.py`
- `piecewise.py`
- `common_tube.py`
- `verify_auer_composition_replay_v1.py`
- `validation/g2/rational.py`
- `validation/g2/interval.py`

All matched their manifest entries exactly.

I also independently recomputed and matched the published hashes of:

- v10 snapshot manifest:
  `29ca0f22791ccc740ef377b232522dee88bbaf00367213bfc45cc07925c5bcd5`;
- v11 snapshot manifest:
  `d6ed85d98f630889912e30baaf00314ac4069c4dc846525c639832c64ff959eb`;
- R4 artifact manifest:
  `6a8d5501972cbb1351cb9ea09500427cb37f8b30c37673ee9e573e156ab6b1a7`;
- R5 artifact manifest:
  `48196f1f3ebb5cf9787c68bc98f6ad88a0678ebd92683014fe877d015f18dd44`;
- R4 analytic native/evidence v2;
- R4 DDWMR native/evidence v2;
- R5 pristine replay report;
- R5 trial ledger;
- R5 pre-freeze setup-attempt record.

These exact GitHub bytes match their manifest/index SHA-256 values.

## External-review limitation

The v10 manifest lists 720 snapshot members.

The v11 manifest lists 726.

The complete corresponding local snapshot directory contents are **not** all republished in the GitHub repository.

Therefore I cannot independently make the statements:

> 720/720 local v10 snapshot files independently rehashed by GPT;

or:

> 726/726 local v11 snapshot files independently rehashed by GPT.

Codex's local review reports those checks, but from the public material I can only verify:

1. the manifest file bytes;
2. selected published members against those manifests;
3. published artifact files against the artifact manifests.

## Consequence

Final proof-critical source identity is strongly supported for the published active files.

Complete historical snapshot-tree integrity remains externally unverified.

## Status

- published proof-critical sources/artifacts: **VALID**;
- complete v10/v11 local snapshot membership: **UNVERIFIED externally**.

## Required action

Use precise wording:

> Codex locally verified 720/720 and 726/726; GPT independently verified the published manifests and proof-critical published member hashes, but the full local snapshot trees are not publicly available for external member-by-member replay.

Do not upgrade the second statement to full independent snapshot verification.

---

# 16. FINDING M13 — TWO PRE-FREEZE SETUP FAILURES

## Finding

The two pre-v11 setup failures have incomplete historical provenance, but they do not constitute failed IVP/proof executions.

## Evidence

`pre_freeze_setup_attempts_v1.json` records two:

`FAILED_BEFORE_SNAPSHOT_CREATION`

attempts caused by:

`v10 snapshot file set mismatch`.

For both:

- source SHA at the attempt is unavailable;
- raw transient stdout was not retained;
- the normalized diagnostic line is hashed;
- no verifier child ran;
- no numerical replay ran;
- no v11 target snapshot existed;
- no R4 output was modified.

The final creator was subsequently frozen and v11 was created.

## Consequence

The exact transient development state of those two setup attempts cannot be reconstructed.

That is a provenance gap.

It does not falsify the final frozen v11 replay because those attempts did not produce the proof/composition being reviewed.

## Status

\[
\boxed{\textbf{PARTIAL historical provenance}}
\]

## Required action

Retain this limitation in the paper/reproducibility notes if development-attempt provenance is discussed.

Do not retroactively manufacture hashes or stdout.

No R4/R5 numerical result needs to be changed.

---

# 17. FINDING M14 — RESOURCE EVIDENCE

## Finding

Resource evidence is valid for the small R4/R5 case only.

It is not evidence that the full Auer comparison is tractable.

## Evidence

Published R4 DDWMR proof:

- accepted steps: 1;
- rejected steps: 0;
- Picard iterations: 1;
- producer RHS/Jacobian calls: 4;
- producer rational operations: 43,917;
- producer maximum rational bits: 300.

R4 combined evidence reports all producer/replay/tamper/common work below its frozen 2,000,000-operation profile.

R5 pristine replay records about:

- 1.17 s guarded wall time;
- about 19.7 MB process-memory peak;
- 1 GiB process-memory cap;
- 120 s deadline.

These numbers belong to:

- one proof;
- one replay;
- one common check;

not the 1,944-query protocol.

## Consequence

Auer full-grid throughput remains unverified.

## Status

**VALID one-case resource evidence; UNVERIFIED matched-batch tractability**

## Required action

No extrapolation from one query to the full grid.

---

# 18. FINDING M15 — PROTOCOL V2 MATCHING QUALITY

## Finding

The conceptual comparison universe in protocol v2 is well matched.

The executable protocol is not ready because several sections describe the obsolete preflight Auer implementation rather than the proof-producing R4/R5 path.

## Evidence

## Conceptually matched and worth preserving

Protocol v2 correctly fixes:

- the same 1,944 query IDs;
- six nonzero-width nine-state cells;
- twelve scenes;
- three hold durations;
- nine voltage actions;
- same MASTER v2.1 plant;
- same complete 12-label parameter image;
- same one held voltage per query;
- same full-hold collision/contact predicates;
- fixed-label semantics;
- no query deletion;
- no post-result obstacle tuning;
- separation of `UNKNOWN`, resource failure, invalid input and implementation failure.

## Outdated/inconsistent implementation details

Protocol v2 still states or assumes:

1. Auer WSL2 + PROFIL/BIAS 2.0.8;
2. binary64 hex Auer state/residual segment adaptation;
3. an Auer adapter that identifies but does not replay the proof;
4. 0.001 s maximum accepted step width;
5. 15 s / 512 MiB candidate resource setup tied to the old path.

The actual R4/R5 proof-producing method uses:

- exact rational endpoints;
- `ARITHMETIC_BACKEND_MANIFEST_v2`;
- `G4_AUER_METHOD_CONTRACT_v2`;
- residual native proof JSON;
- independent native proof replay;
- `NATIVE_TOTAL_HULL`;
- a development profile with 120 s / 1 GiB caps;
- a successful one-slab 0.02 s DDWMR proof.

Those changes are scientifically material to the implementation contract even though they do not change the formal plant/query universe.

## Consequence

Protocol v2 must not be “locked as-is” after R5.

A protocol v3 is required before matched execution.

## Status

\[
\boxed{\textbf{PARTIAL / NOT BATCH-READY}}
\]

## Required action

Create and review protocol v3 as specified next.

---

# 19. EXACT REQUIRED PROTOCOL V3 CORRECTIONS

These corrections do **not** alter R4/R5 outcomes and do not cherry-pick the future 1,944-query universe.

## 19.1 Preserve immutable scientific universe

Keep unchanged:

- all 1,944 IDs;
- their order/digest;
- state cells;
- scenes;
- horizons;
- nine actions;
- benchmark parameter image;
- contact/collision rules.

No R3 outcome may cause query deletion or geometry modification.

## 19.2 Replace obsolete Auer backend text

Remove the active comparison dependence on:

- PROFIL/BIAS;
- host glibc/libm;
- binary64-hex proof segments.

Bind instead to:

- `DDWMR_EXACT_RATIONAL_TAYLOR_INTERVAL_V1`;
- method contract v2 or reviewed successor;
- exact-rational native proof schema;
- `replay_ivp.py`;
- `NATIVE_TOTAL_HULL`;
- R5 composition verifier semantics.

The old binary64 adapter may remain historical code but must not be the matched proof path.

## 19.3 Freeze deterministic step policy

Specify before batch:

- initial step rule;
- bisection rule;
- maximum accepted steps;
- maximum rejected attempts;
- maximum Picard iterations;
- rational bit/operation cap;
- RHS/Jacobian cap.

Do not retain the arbitrary 0.001 s maximum solely because it appeared in the abandoned preflight path.

R4 development data may inform the new rule because no matched Auer output exists yet, but the final rule must be frozen before the 1,944-run and never tuned per query after outcomes.

## 19.4 Freeze status taxonomy

For every Auer query distinguish:

### Native IVP layer

- `PROOF_COMPLETE`;
- `INCLUSION_NOT_ESTABLISHED`;
- `RESOURCE_LIMIT`;
- `INVALID_INPUT`;
- `IMPLEMENTATION_FAILURE`.

### Common predicate layer, only when native proof is complete

- `PASS_ON_SUPPLIED_TUBE`;
- `UNKNOWN_ON_SUPPLIED_TUBE`.

### Final certification layer

Only:

\[
\text{PROOF_COMPLETE}
+
\text{PASS_ON_SUPPLIED_TUBE}
\]

may be counted as a certified query.

Do not merge:

- native inclusion failure;
- resource exhaustion;
- predicate UNKNOWN;
- implementation failure.

## 19.5 Common-resource and native-resource views

Predeclare two views.

### Primary equal-resource view

Use the same external:

- wall-time cap;
- process-memory cap;

for Auer and the compared R3 query evaluations.

The existing v2 proposal of 15 s / 512 MiB can be retained if the team chooses it before outputs, but the value must be fixed explicitly.

### Secondary native-method work view

Report each method's own:

- arithmetic operations;
- bit lengths;
- RHS/Jacobian calls;
- accepted/rejected slabs;
- Picard/refinement iterations;
- proof bytes.

These counters are not equivalent units and must not be summed into an artificial score.

Any secondary Auer run with more generous development limits must be reported separately from the primary equal-resource coverage.

## 19.6 R3 common-interface parity fixture

Before the full batch, publish one actual archived historical R3 proof routed through:

`r3_record_to_common_segment`

and then:

`check_tube_segments`.

Require:

- native R3 replay PASS;
- radius expansion exactly once;
- same query/action identity;
- same full label image;
- recorded common margins/status.

I found the adapter source, but not a published real R3 parity artifact.

This is a **pre-batch fairness obligation**.

## 19.7 Freeze full source/result manifest

Before query 1:

- freeze the final protocol;
- freeze proof-critical source hashes;
- freeze backend manifest;
- freeze both method profiles;
- freeze query universe;
- freeze output schema;
- record zero Auer matched evaluations before freeze.

A post-freeze scientific change requires a new protocol version and preservation of prior results.

---

# 20. FINDING M16 — GO / NO-GO FOR MATCHED BATCH

## Finding

The proof-producing Auer method and one-case R5 composition are sufficiently sound to justify moving to a **separately frozen matched-comparison protocol**.

They are **not yet sufficient to execute the batch under the current v2 protocol**.

## Evidence

Positive evidence now exists for:

- source-method mapping;
- nonsmooth `clip` handling;
- 21-coordinate parameter/state enclosure;
- exact rational arithmetic;
- independent algorithmic replay;
- exact saved proof inclusion;
- endpoint/full-time tube;
- common-predicate composition;
- stored artifact replay;
- query/action/source binding;
- mutation rejection.

The remaining blockers are protocol/integration blockers rather than a failure of the frozen one-case proof:

1. protocol v2 is not locked and is outdated;
2. no published historical R3→common parity artifact is available;
3. complete local source snapshots remain externally unverifiable member-by-member.

The third item does **not** block a batch if the batch is frozen using the publicly reviewable proof-critical source set and complete batch manifest; it is a limitation on historical R4/R5 provenance claims.

## Consequence

Current decision:

\[
\boxed{\textbf{NO-GO: do not execute the 1,944-query matched batch yet}}
\]

Next decision after protocol-v3 + R3 parity review:

\[
\boxed{\textbf{eligible for a separate batch-start review}}
\]

No further Auer single-case mathematics is demanded by this review unless protocol-v3 code changes touch proof-critical logic.

## Status

\[
\boxed{\textbf{PARTIAL — scientifically ready for protocol freeze, not batch execution}}
\]

## Required action

Do not run matched Auer queries until protocol v3 and the R3 parity fixture have independent acceptance.

---

# 21. FINDING M17 — COMPARISON FAIRNESS AND G4 INTERPRETATION

## Finding

Even a successful matched Auer batch cannot establish generic reachability novelty.

The generic-method novelty blocker remains.

## Evidence

Auer 2013 already establishes verified handling of a class of nonsmooth/piecewise-smooth IVPs.

Rauh–Auer 2011 already establishes residual/Picard verified state enclosures.

The project's remaining candidate contribution is narrower:

> whether the DDWMR-specific structured enclosure produces useful certification/tightness/cost behavior relative to a matched published validated-IVP comparator.

## Consequence

Future interpretation must be symmetric.

If Auer matches or exceeds the structured method under the frozen protocol:

> the proposed structured advantage is unsupported on that benchmark.

If the structured method performs better:

> a benchmark-specific advantage is supported under the exact locked assumptions/resources.

Neither outcome establishes:

- universal superiority;
- first-ever validated reachability;
- physical robot safety;
- recursive safety.

If Auer cannot complete some queries within the locked resource contract, those are censored/resource outcomes, not automatic R3 wins.

## Status

\[
\boxed{\textbf{G4 UNVERIFIED}}
\]

## Required action

Keep the generic novelty branch blocked.

Use the future matched results only for the narrow DDWMR-specific contribution hypothesis.

---

# 22. FINDING M18 — G2 / G3 / PHYSICAL CORRESPONDENCE

## Finding

R4/R5 do not change the scientific disposition of G2, G3 or physical correspondence.

## Evidence

### G2

Auer supplies a comparator path, not a demonstration that R3's voltage selection is practically useful.

Existing R3 evidence still has the important limitation that its mixed groups certify zero voltage only; it does not yet establish nonzero-action coverage benefit.

### G3

No:

\[
K_T\subseteq\operatorname{Pre}_T^c(K_T)
\]

construction is supplied.

### Physical correspondence

Both compared methods operate on the same reduced formal model.

Neither validates omitted physical tire/support/driver/delay effects.

## Consequence

No gate promotion follows.

## Status

- **G2: UNVERIFIED**
- **G3: UNVERIFIED**
- **physical correspondence: UNVERIFIED**

## Required action

No change.

---

# 23. OVERALL FINDINGS TABLE

| Item | Disposition | Key reason |
|---|---|---|
| Auer 2013 equation-to-code mapping | **VALID** | Residual/mean-value/Picard structure matches source method in stated specialization |
| “Paper-faithful method reconstruction” label | **VALID** | Equations preserved; implementation/backend intentionally different |
| “Original VALENCIA software reproduction” label | **BLOCKER / unsupported** | Historical software/binary is not reproduced |
| Continuous clip interval range | **VALID** | Exact monotone range |
| Clip generalized derivative | **VALID** | `[0,1]` at both continuous corners is sound |
| DDWMR branch-corner empirical coverage | **PARTIAL** | Analytic fixture tests +1; frozen DDWMR rough tube remains unsaturated |
| Fixed parameter semantics | **VALID** | 12 zero-derivative labels remain unchanged |
| 21×21 interval Jacobian path | **VALID** | Complete state+label AD in producer/replay |
| Residual derivative inclusion | **VALID** | Independently recomputed on all 21 coordinates |
| Integrated full-time inclusion | **VALID** | Independently recomputed on all 21 coordinates |
| Endpoint propagation | **VALID** | Independently recomputed on all 21 coordinates |
| Exact rational/Taylor arithmetic | **VALID** in inspected scope | No host-libm proof path; sound global remainder construction |
| Native replay algorithmic independence | **VALID** | Producer solver/RHS not imported |
| Native replay arithmetic independence | **PARTIAL** | Shared rational/interval/Taylor implementation |
| Common predicate | **VALID** | Sound supplied-hull collision/contact checks |
| Radius-once semantics | **VALID** | `NATIVE_TOTAL_HULL`, expansion count 0 |
| R5 stored composition replay | **VALID** for frozen case | Replay → segment → predicate → composition is reconstructed |
| 17 file mutation trials | **VALID** for declared cases | Expected layers/reasons match actual ledger |
| Published proof-critical source hashes | **VALID** | Independently rehashed from GitHub and matched |
| Published R4/R5 artifact hashes | **VALID** for checked files/manifests | Independently rehashed and matched |
| Complete 720/726 local snapshot membership | **UNVERIFIED externally** | Full snapshot trees are not published |
| Two pre-freeze setup attempts | **PARTIAL provenance** | transient source bytes/raw stdout absent |
| Rauh–Auer DOI in method contract | **PARTIAL / source metadata correction needed** | title/venue/pages verified; printed DOI not independently supported |
| One-case resources | **VALID** | frozen small-case evidence |
| 1,944-query tractability | **UNVERIFIED** | no matched Auer queries run |
| Protocol v2 batch readiness | **PARTIAL / NO-GO** | outdated backend/adapter/resources and not locked |
| Protocol-v3 preparation | **GO** | no one-case mathematical blocker remains |
| G4 | **UNVERIFIED** | no matched result |
| Overall project | **HOLD** | unchanged |

---

# 24. EXACT NEXT CODEX WORK PACKAGE

## Package

`G4_AUER_MATCHED_PROTOCOL_V3_FREEZE_REVIEW`

## Do not run the 1,944 queries in this package.

### Deliverable A — protocol v3

Revise only comparison infrastructure.

Preserve the 1,944 IDs and scientific universe.

Replace obsolete v2 Auer implementation clauses with the frozen proof-producing R4/R5 path.

### Deliverable B — source-metadata fix

Remove the unverified Rauh–Auer DOI unless authoritative evidence is found.

Do not change mathematical locators:

- *Reliable Computing* 15(4);
- pp. 370–381;
- Algorithm 1 / Eqs. (3)–(6), printed p. 372.

### Deliverable C — actual R3 common parity fixture

Take one archived R3 proof record from the completed development batch.

Replay it through:

`r3_record_to_common_segment`

and the common checker.

Store:

- query/action;
- native replay result;
- total hull;
- radius expansion count/mode;
- common margins;
- source/proof hashes.

### Deliverable D — future batch manifest

Freeze:

- query IDs/order;
- Auer source hashes;
- R3 source/artifact identity;
- method contracts;
- exact arithmetic backend;
- status taxonomy;
- external equal-resource caps;
- method-native work counters;
- initial step/bisection policy;
- batch output schema.

### Deliverable E — batch-start review request

Ask for a short independent review of only:

1. protocol v3 consistency;
2. R3 common parity fixture;
3. frozen source/resource manifest.

If those pass:

> batch execution may be separately authorized.

No new single-case Auer proof is required unless proof-critical source changed.

---

# 25. STOP CONDITIONS FOR THE FUTURE MATCHED BRANCH

Once protocol v3 is locked:

Stop/review the branch rather than silently retuning if:

1. proof-critical source must change;
2. arithmetic backend changes;
3. query universe changes;
4. action/scene/horizon is removed after results;
5. equal-resource cap is changed after outcomes;
6. Auer native inclusion repeatedly fails and the proposed repair is post-hoc per-query tolerance/cap tuning;
7. R3 common adaptation fails parity;
8. status categories cannot distinguish native proof failure from predicate UNKNOWN.

A method-specific failure does not imply the other method is scientifically superior unless the frozen comparison contract supports that interpretation.

---

# 26. SOURCE-SNAPSHOT LIMITATION — WORDING TO USE LATER

Recommended wording:

> The published GitHub repository contains the v10/v11 snapshot manifests, the frozen R4/R5 proof artifacts, and the proof-critical active project sources. Independent GPT review recomputed the published manifest hashes and selected proof-critical source/artifact SHA-256 values and found them consistent. Codex additionally reported local 720/720 v10 and 726/726 v11 member verification. The complete local snapshot directory contents are not republished, so the latter member-by-member local checks are not independently reproducible from GitHub alone.

Do not write:

> GPT independently verified all 720/726 snapshot members.

That would be unsupported.

---

# 27. CLAIMS THAT ARE NOW SUPPORTED

Supported:

> The project has one published, proof-complete synthetic DDWMR Auer-method reconstruction whose residual inclusion, full-time tube and endpoint have both producer and separate algorithmic replay records.

Supported:

> A stored-artifact verifier reconstructs the proof-to-common-predicate composition for that query.

Supported:

> The active arithmetic is exact-rational/Taylor and does not rely on the previously unresolved PROFIL/BIAS/glibc transcendental path.

Supported:

> The common supplied-tube collision and contact margins are strictly positive for that frozen query.

Supported:

> The reconstruction is source-faithful at the method level to the cited residual/Picard and continuous piecewise derivative machinery.

---

# 28. CLAIMS THAT REMAIN UNSUPPORTED

Not supported:

> Auer has been reproduced as original VALENCIA software.

Not supported:

> Auer succeeds on the full 1,944 benchmark.

Not supported:

> R3 is tighter/faster/better than Auer.

Not supported:

> Auer is tighter/faster/better than R3.

Not supported:

> Failure of future Auer inclusion means the action is unsafe.

Not supported:

> A failed Auer query proves R3 novelty.

Not supported:

> Generic validated reachability is novel here.

Not supported:

> G2 usefulness is closed.

Not supported:

> recursive safety / G3.

Not supported:

> physical robot safety.

---

# 29. FINAL GATE DISPOSITION

\[
\boxed{\textbf{HOLD}}
\]

\[
\boxed{\textbf{G1 PASS — restricted reduced-model scope}}
\]

\[
\boxed{\textbf{G2 UNVERIFIED}}
\]

\[
\boxed{\textbf{G3 UNVERIFIED}}
\]

\[
\boxed{\textbf{G4 UNVERIFIED}}
\]

\[
\boxed{\textbf{physical-platform correspondence UNVERIFIED}}
\]

Generic-method novelty remains blocked.

The Auer R4/R5 **single-case proof mechanism is accepted in its restricted scope**.

The full matched comparison is **not authorized by this review under protocol v2**.

The next scientific step is a protocol-v3 freeze plus an actual R3 common-interface parity fixture, followed by a separate batch-start review.

---

# 30. BOTTOM LINE TO CODEX

The important change from R2 is real:

> Auer is no longer merely a build/interface preflight. R4/R5 now contain one published proof-producing residual-IVP path, a separate algorithmic replay, a proof-derived common safety composition, and a persistent stored-artifact composition replay.

Independent source/proof inspection did not uncover a mathematical contradiction in that one-case construction.

The important limit is equally real:

> one proof-complete synthetic case is not a matched comparator result.

Do **not** run 1,944 queries from the old v2 protocol.

First freeze a v3 protocol that reflects the exact-rational R4/R5 method actually reviewed and establish one real R3-to-common parity artifact.

Then request the separate batch-start decision.

Until then:

\[
\boxed{\textbf{HOLD / G4 UNVERIFIED / MATCHED BATCH NO-GO}}
\]
