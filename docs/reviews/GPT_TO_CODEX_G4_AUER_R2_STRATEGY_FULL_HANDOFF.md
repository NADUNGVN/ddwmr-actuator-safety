# GPT → CODEX G4 AUER R2 STRATEGY REVIEW — FULL HANDOFF

**Intended repository path:** `docs/reviews/GPT_TO_CODEX_G4_AUER_R2_STRATEGY_FULL_HANDOFF.md`  
**Repository:** `NADUNGVN/ddwmr-actuator-safety`  
**Branch:** `luna/g2-validation-v1`  
**Committed HEAD reviewed:** `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`  
**Authority:** MASTER v2.1  
**Project status:** **HOLD**  
**G1:** PASS — restricted reduced-model scope  
**G2/G3/G4:** UNVERIFIED  
**Physical-platform correspondence:** UNVERIFIED  
**Workflow:** W1 authorizes scoped G2/G4 validation coding only; no G3, operational controller, hardware, GO or gate promotion follows from this review.

---

# 0. Executive disposition

## R2 partial handoff

\[
\boxed{\textbf{CORRECT — retain BLOCKED/PARTIAL}}
\]

The reported `BLOCKED/PARTIAL` scope is appropriate. I do not recommend promoting the Auer comparator to READY, but I also do not recommend abandoning the Auer direction.

The scientifically relevant blockers remain:

1. no proof-complete DDWMR Auer full-time tube or endpoint is established;
2. the reported adapter does not yet establish/replay the native Picard/inclusion proof that makes a supplied hull a reachable-set enclosure;
3. the x86-64 PROFIL/BIAS/glibc-libm caveat prevents finite arithmetic probes from serving as a global rounding-correctness proof;
4. the retained legacy smooth seed lacks the 2013 piecewise extension;
5. Auer §5 is not a clean exact numerical oracle from the presently accessible publication text;
6. the proposed matched protocol is not yet locked.

## One comparator decision

\[
\boxed{\textbf{CONTINUE AUER 2013}}
\]

but explicitly as:

> **Auer-2013 paper-faithful piecewise-smooth validated-IVP reconstruction with a certified directed-rounding backend.**

Do **not** call it an original ValEncIA binary/software reproduction unless that stronger reproduction is independently demonstrated.

Auer 2013 is a particularly suitable comparator because its source method directly addresses piecewise-smooth scalar primitives and couples a generalized derivative with a verified full-time IVP tube.

## Next bounded milestone

Do **not** run the 1,944-query Auer comparison.

The next Luna package should prove only:

1. a source-faithful `clip` interval range/generalized-derivative implementation;
2. a certified arithmetic backend contract;
3. one analytic branch-crossing IVP fixture with a proof-complete full-time tube;
4. one predeclared DDWMR query-action with native inclusion proof, full-time tube and endpoint;
5. proof-record binding through the common checker;
6. one archived historical R3 proof routed through that same comparison interface.

Only after independent review of those items should a later review decide whether to authorize the 1,944 matched run.

---

# 1. Evidence boundary and read ledger

## 1.1 Canonical committed context read

At commit `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`, I independently read:

- `AGENTS.md`
- `research_context/MASTER_RESEARCH_CONTEXT_v2.md`
- `research_context/DECISION_LOG.md`
- `research_context/LITERATURE_MATRIX.md`
- `research_context/REVIEW_GATE.md`
- `docs/reviews/CODEX_G2_VALIDATION_R3_REVIEW.md`
- `docs/reviews/LUNA_TO_CODEX_G2_VALIDATION_R3_FULL_HANDOFF.md`
- `research/theorem_notes/G2_FINITE_EVALUATOR_SPEC_v1.md`
- `research/benchmarks/G2_USEFULNESS_BENCHMARK_SPEC_v1.md`
- `docs/reviews/G4_MATCHED_PRIOR_ART_COMPARISON_v1.md`

Canonical context confirms:

- overall **HOLD**;
- G1 restricted PASS;
- G2/G3/G4 UNVERIFIED;
- physical correspondence UNVERIFIED;
- workflow W1 already authorizes scoped G2/G4 validation implementation;
- G3 and operational/hardware work remain outside scope.

## 1.2 Local/uncommitted Auer R2 artifacts were not accessible

The request states that the Auer R2 work is local/uncommitted. Those files are not present in committed GitHub HEAD `aac7...`.

Requested paths that are absent from the committed snapshot include:

- `docs/reviews/GPT_TO_CODEX_G2_VALIDATION_R3_SCIENTIFIC_REVIEW_FULL_HANDOFF.md`
- `docs/reviews/CODEX_G4_AUER_PREFLIGHT_REVIEW.md`
- `docs/CODEX_TO_LUNA_G4_AUER_BASELINE_R2.md`
- `docs/reviews/LUNA_TO_CODEX_G4_AUER_BASELINE_R2_FULL_HANDOFF.md`
- `docs/reviews/CODEX_G4_AUER_BASELINE_R2_REVIEW.md`
- `docs/reviews/G4_AUER_SOURCE_AND_APPLICABILITY_v2.md`
- `research/theorem_notes/G4_AUER_BASELINE_CONTRACT_v1.md`
- `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v2.md`

The committed tree also lacks:

- `validation/g4/`
- `validation/baselines/`
- `results/validation/g4/`

Therefore this GPT pass could not directly inspect:

- `validation/g4/common_tube.py`
- `validation/g4/verify_common_tube.py`
- the local Auer adapter;
- the local source snapshot;
- `snapshot_manifest.json`;
- the nine reported interface fixtures;
- the reported 681 snapshot hashes;
- the exact 19 arithmetic/trigonometric probe records.

Those facts remain **reported but not independently reverified in this GPT environment**.

This is not evidence that the local artifacts are wrong. It means I will not invent line-level defects or accept implementation correctness from a handoff summary alone.

## 1.3 Primary sources independently inspected

### Auer, Kiel & Rauh 2013

Ekaterina Auer, Stefan Kiel, Andreas Rauh,  
**A verified method for solving piecewise smooth initial value problems**,  
*International Journal of Applied Mathematics and Computer Science* 23(4), 731–747 (2013).  
DOI: `10.2478/amcs-2013-0055`.

Sources:
- `https://doi.org/10.2478/amcs-2013-0055`
- author-uploaded full text:
  `https://www.researchgate.net/publication/265778391_A_verified_method_for_solving_piecewise_smooth_initial_value_problems`

Relevant locators checked:

- §4.1;
- Eq. (26): interval-initial-value IVP;
- Eq. (27): algorithmic RHS composition;
- Eq. (28): scalar piecewise-smooth primitive;
- Eq. (33): generalized derivative for continuous piecewise functions;
- Property 2 following Eq. (33);
- Eq. (40): generalized derivative at a switching point;
- discussion of intervals containing multiple switches;
- §4.2;
- Eq. (42): verified functional tube
  \[
  x^*(t)\in x(t):=\tilde x(t)+R(t);
  \]
- Eq. (43): Picard error iteration;
- §5/Table 2 as a qualitative reference.

### Rauh & Auer 2011

Andreas Rauh, Ekaterina Auer,  
**Verified simulation of ODEs and DAEs in ValEncIA-IVP**,  
*Reliable Computing* 15(4), 370–381 (2011).

Source:
`https://www.researchgate.net/publication/228941872_Verified_simulation_of_ODEs_and_DAEs_in_ValEncIA-IVP`

Relevant scope: verified ODE reachable-state enclosures and the historical ValEncIA-IVP framework.

### PROFIL/BIAS

Official TU Hamburg page:
`https://www.tuhh.de/ti3/keil/profil/index_e.html`

The Version 2.0.8 release notes explicitly state that the x86-64 configuration suffers from a glibc `libm` bug affecting rounding-mode handling.

Documentation:
`https://www.tuhh.de/ti3/keil/profil1/docu/Profil.texinfo_19.html`

### GNU MPFR

Official manual:
`https://www.mpfr.org/mpfr-current/mpfr.html`

MPFR explicitly supports:

- `MPFR_RNDD`: directed downward rounding;
- `MPFR_RNDU`: directed upward rounding;

and documents correct rounding semantics for supported functions.

---

# 2. Preflight judgment

## Finding

`BLOCKED/PARTIAL` is the correct R2 status.

## Evidence

Even accepting every locally reported build/hash/probe observation, the package still reports:

- zero matched query evaluations;
- no proof-complete Auer DDWMR full-time tube;
- no endpoint enclosure;
- no adapter replay/establishment of the native inclusion proof;
- unresolved arithmetic proof;
- incomplete legacy piecewise implementation;
- unapproved protocol.

These are sufficient scientific blockers.

## Consequence

No coverage/tightness/cost comparison against R3 is scientifically available yet.

## Status

\[
\boxed{\textbf{CORRECT — BLOCKED/PARTIAL}}
\]

## Required action

Proceed only to the bounded proof-backed single-case milestone in Section 10.

---

# 3. Clip/RHS mathematical applicability

## Finding

I found no source-level mathematical incompatibility between Auer 2013 and the benchmark's continuous `clip` contact law.

## Evidence

The selected law is

\[
\phi(q)=
\begin{cases}
-1,&q<-1,\\
q,&-1\le q\le1,\\
1,&q>1.
\end{cases}
\]

It is continuous piecewise smooth with switch points \(-1,1\).

Its branch derivatives are:

\[
0,\quad 1,\quad 0.
\]

Auer Eq. (28) explicitly permits scalar piecewise-smooth primitives, and Eq. (33)/(40) supplies generalized derivative enclosures across switching points.

A source-faithful derivative enclosure for `clip` is therefore:

\[
D\phi(X)=
\begin{cases}
[0,0],&X\subset(-\infty,-1)\text{ or }X\subset(1,\infty),\\
[1,1],&X\subset(-1,1),\\
[0,1],&X\text{ intersects a switching point}.
\end{cases}
\]

If a box spans both switching points, `[0,1]` is still a sound derivative hull for this continuous function.

Because `clip` is monotone, its exact scalar interval range is:

\[
\phi([a,b])=[\phi(a),\phi(b)].
\]

## Consequence

The Auer comparator need not replace the benchmark's `clip` with a smooth surrogate.

A smooth-only comparator would be less directly matched.

## Status

**VALID source-level applicability**

## Required action

Freeze these range/generalized-derivative rules in the Auer method contract and independently audit the local implementation.

---

# 4. Defect versus unimplemented proof obligation

## Finding

No specific local source-code defect can be established because the relevant local source is unavailable here.

Several **proof obligations** are definitely incomplete from the request's own description.

## Evidence

| Item | Classification |
|---|---|
| Auer 2013 supports continuous piecewise `clip` | Source fact; no defect |
| Legacy smooth seed lacks 2013 piecewise extension | Implementation incompleteness |
| Adapter does not establish/replay Picard/inclusion proof | Unimplemented proof obligation; blocker |
| Common checker only receives supplied hull | Conditional safety layer, not reachability proof |
| No historical real R3 proof fixture through common layer | Interface-validation gap |
| PROFIL/BIAS x86-64 caveat | Arithmetic-proof blocker |
| 19 finite probes | Smoke evidence only |
| 1,000-step cap | Resource allowance, not proof |
| §5 ambiguity | Reference-data limitation |
| No §5 exact output table | Reference-oracle limitation |
| Zero matched Auer evaluations | Preflight state, not a failure result |

## Consequence

Do not “fix” checker mathematics without line-level evidence.

Instead, complete and expose the missing proof contracts.

## Status

**IMPLEMENTATION CORRECTNESS UNVERIFIED**

## Required action

Supply proof-backed artifacts in the next package.

---

# 5. Comparator decision

## Finding

Continue **Auer 2013** rather than switching the principal published comparator.

## Evidence

Auer 2013 matches the benchmark on the issue most likely to disqualify a generic validated integrator: the non-differentiable continuous piecewise contact law.

The method explicitly combines:

- interval evaluation of piecewise primitives;
- generalized derivatives;
- ValEncIA-IVP's verified functional tube.

A smooth-only tool would require either a separate common smooth-law subbenchmark or an additional extension.

The reported failure of the legacy smooth seed to include the 2013 extension is not evidence against the published method.

## Consequence

The project should reconstruct the **method**, not chase exact historical binary equivalence.

## Status

\[
\boxed{\textbf{SELECT AUER 2013}}
\]

## Required action

Use this exact label:

> **Auer-2013 paper-faithful piecewise-smooth validated-IVP reconstruction with certified interval arithmetic.**

Do not call it original-software reproduction.

---

# 6. Source-faithful Auer method contract

The next package should freeze a method contract before evaluating a DDWMR batch.

## 6.1 Scalar interval range

For an interval \(X=[l,u]\):

\[
\Phi(X)=[\phi(l),\phi(u)].
\]

A possible switch at \(\pm1\) must never be discarded by a floating comparison.

## 6.2 Generalized derivative

Use the enclosure in Section 3.

If an interval reaches a switching point exactly, include all limiting branch derivatives.

Do not use the nominal unsaturated derivative `[1,1]` on an interval that can enter saturation.

## 6.3 RHS composition

The DDWMR RHS is a composition of:

- smooth elementary operations;
- the scalar piecewise `clip`.

Hidden parameter labels remain fixed for the entire hold.

If represented as augmented states:

\[
\dot\vartheta=0.
\]

If represented as interval coefficients, they cannot be reset to favorable values per step.

## 6.4 Native full-time inclusion

An accepted Auer step must establish an analogue of Auer Eq. (42):

\[
x^*(t)\in\tilde x(t)+R(t)
\quad
\forall t\in[t_k,t_{k+1}].
\]

The inclusion cannot be inferred merely from a serialized hull.

The package must expose the native fixed-point/Picard validity condition corresponding to Eq. (43).

## 6.5 Endpoint

Each valid step needs a separate certified endpoint enclosure:

\[
X_{k+1}^{\rm end}\supseteq x(t_{k+1}).
\]

For a multi-step trajectory:

\[
X_{k+1}^{\rm init}\supseteq X_{k+1}^{\rm end}.
\]

No favorable narrowing between steps is permitted.

---

# 7. Arithmetic proof

## Finding

Finite probes cannot resolve the PROFIL/BIAS/glibc-libm limitation globally.

## Evidence

The official 2.0.8 page itself records an x86-64 rounding-mode caveat.

A finite list of arithmetic/trigonometric tests can reveal failures but cannot prove all argument values and all proof-critical functions are outward.

## Consequence

The current historical-backend path remains blocked as a proof foundation.

## Status

**BLOCKER for proof use of the unresolved backend**

## Required action

Use a certified correctly-rounded backend.

---

# 7.1 Minimum acceptable backend substitution

Recommended:

> **MPFR-directed interval arithmetic**, optionally through an interval package whose enclosure contract is explicitly based on MPFR.

For every proof-critical lower endpoint use an appropriate downward-rounded evaluation; for every upper endpoint use upward rounding.

Required proof surface includes:

- `+`, `-`, `*`, `/`;
- `sqrt`;
- `exp`;
- `sin`;
- `cos`;
- any additional elementary function actually used.

No proof-critical operation may silently fall back to ordinary `libm` without a rigorous error enclosure.

## Evidence required

Record:

1. exact arithmetic backend/version;
2. source/package digest;
3. compiler/version;
4. compile flags;
5. precision policy;
6. directed rounding policy;
7. trigonometric range-reduction implementation;
8. handling of extrema in interval `sin/cos`;
9. subnormal/underflow behavior;
10. overflow/infinity behavior;
11. NaN/domain handling;
12. decimal/input parsing direction;
13. output serialization direction;
14. prohibition or justification of unsafe optimization such as `-ffast-math`.

Smoke probes may supplement this record, but do not replace the backend's correctness contract.

---

# 7.2 Does backend substitution remain a fair Auer comparator?

## Finding

Yes — at the **method** level.

No — if described as an exact **software reproduction**.

## Evidence

Auer's mathematical correctness depends on interval containment, generalized derivatives and Picard inclusion, not on exact historical PROFIL/BIAS bit patterns.

A backend that produces certified supersets while leaving the Auer method equations/acceptance tests unchanged implements the same scientific method.

## Consequence

This wording is acceptable:

> Auer-2013 method reconstruction using a modern certified arithmetic backend.

This wording is not established:

> exact reproduction of the original Auer/ValEncIA implementation.

## Status

**ACCEPTABLE**

## Required action

Record the substitution in every manifest and result.

---

# 8. Auer §5 and the independent reference

## Finding

Auer §5 should not be the primary correctness oracle.

## Evidence

The accessible publication text contains at least one ambiguous numerical rendering in Table 2; the extracted text presents:

\[
F_s[0.15,0.03]\ {\rm N},
\]

which is not an ordinary ordered interval as displayed.

The paper provides figures and runtime descriptions, not an exact output table suitable for numerical replay.

Therefore a mismatch cannot cleanly distinguish:

- a reconstruction defect;
- an input transcription issue;
- historical platform/library behavior.

## Consequence

§5 is suitable as a qualitative secondary reproduction check, not as the pass/fail oracle for the method implementation.

## Status

**REFERENCE LIMITATION**

## Required action

Use a separately labeled exact IVP fixture first.

---

# 8.1 Recommended analytic piecewise fixture

Label it:

> **Independent analytic Auer-method validation fixture — not Auer §5 reproduction**

Use:

\[
\dot x=1,
\qquad
\dot y=\operatorname{clip}_{[-1,1]}(x),
\]

\[
x(0)\in[0.9,0.91],
\qquad
y(0)=0,
\qquad
T=0.2.
\]

The uncertain crossing time is:

\[
t_c=1-x_0\in[0.09,0.10].
\]

Exact:

\[
x(t)=x_0+t.
\]

Before crossing:

\[
y(t)=x_0t+\frac12t^2.
\]

After crossing:

\[
y(t)
=
t-\frac12(1-x_0)^2.
\]

At \(T=0.2\):

\[
x(T)\in[1.10,1.11],
\]

\[
y(T)\in[0.195,0.19595].
\]

The Auer result need not equal the exact hull; it must rigorously contain it and carry a valid native full-time inclusion proof.

This fixture tests:

- interval initial state;
- uncertain switch time;
- continuous nonsmooth branch crossing;
- full-time enclosure;
- endpoint enclosure.

---

# 9. Common-check composition

# 9.1 Radius-once semantics

## Finding

Every common-tube record needs an explicit representation tag.

## Evidence

Auer already uses the conceptual tube:

\[
\tilde x+R.
\]

If the adapter exports final lower/upper hulls, adding `R` again is double inflation.

If it exports center plus radius, omitting the radius is unsound.

## Consequence

The checker must not guess representation semantics.

## Status

**REQUIRED**

## Required action

Define exactly one of:

- `ABSOLUTE_HULL`;
- `CENTER_PLUS_RADIUS`.

For `ABSOLUTE_HULL`: apply no second reachability radius.

For `CENTER_PLUS_RADIUS`: form the full hull exactly once.

---

# 9.2 Full-time collision/contact checking

## Finding

Safety predicates must be evaluated on every full-time slab hull, not endpoint-only data.

## Evidence

The project requires:

\[
\forall t\in[0,T].
\]

For each proof-valid slab, compute a certified lower collision margin and contact margin over the entire slab hull.

Negative lower bounds mean `UNKNOWN`, never unsafe.

## Consequence

A proof-complete endpoint without full-time hull is insufficient for G2 comparison.

## Status

**REQUIRED**

## Required action

Bind the full-time hull to every common-check result.

---

# 9.3 Endpoint chaining

## Finding

Endpoint and tube hulls must be separate objects.

## Evidence

The full-time hull may be much wider than the endpoint set.

Using a nominal endpoint is unsound; propagating the entire tube as the endpoint is sound but can introduce avoidable overestimation.

## Consequence

Each step needs:

- `tube_hull`;
- `endpoint_hull`.

Next-step input must contain the prior endpoint hull.

## Status

**REQUIRED**

## Required action

The verifier should check chaining explicitly.

---

# 9.4 Native proof record

## Finding

A safe supplied hull is not a reachability proof.

## Evidence

Two obligations are logically separate:

\[
\mathcal R_{\rm exact}
\subseteq
X_{\rm native},
\]

then:

\[
X_{\rm native}
\subseteq
\mathscr S_c.
\]

A common checker can verify the second obligation and still be fooled by an unjustified narrow hull.

The request reports that the Auer adapter currently does not replay a native Picard/inclusion proof.

## Consequence

No Auer output should be called proof-backed until native inclusion evidence is bound to the hull.

## Status

\[
\boxed{\textbf{BLOCKER}}
\]

## Required action

A native proof record should include or bind at least:

- step start enclosure;
- time interval;
- predictor/approximation identity;
- candidate full-time enclosure;
- RHS interval evaluation;
- generalized Jacobian/derivative enclosure;
- Picard/fixed-point inclusion criterion and result;
- endpoint enclosure;
- arithmetic backend/precision.

---

# 9.5 Query/action/source binding

Every proof record must bind to:

- query ID;
- action ID;
- initial state cell;
- complete parameter image/cell;
- horizon;
- slab number;
- obstacle/contact specification;
- source-snapshot digest;
- method-contract version;
- arithmetic-backend digest;
- source revision;
- build/compiler flags;
- resource profile;
- tube hull;
- endpoint hull.

No hull/proof may be reused under a different query or action.

---

# 9.6 Historical R3 interface fixture

## Finding

The shared comparison layer should consume at least one actual archived R3 proof.

## Evidence

Synthetic interface fixtures test format, but not necessarily the real historical R3 proof path.

## Consequence

Before any matched batch, route one frozen R3 proof through the common checker and verify its query/action identity, status and outward-equivalent margins against the archived R3 record.

## Status

**INTERFACE VALIDATION REQUIREMENT**

## Required action

Add one such fixture without rerunning the R3 batch.

---

# 10. Concrete next Luna work package

## Package ID

`G4_AUER_R3_PROOF_BACKED_SINGLE_CASE`

## Scope

No 1,944-query Auer run.

No G3.

No controller.

No hardware.

No new physical claim.

## D1 — Method contract

Create:

`docs/reviews/G4_AUER_METHOD_CONTRACT_v1.md`

Map:

- Auer Eq. (27) → algorithmic DDWMR RHS;
- Eq. (28) → `clip`;
- Eq. (33)/(40) → generalized derivative;
- Eq. (42)/(43) → native full-time inclusion;
- fixed hidden parameters → exact implementation semantics.

## D2 — Arithmetic contract

Create:

`validation/baselines/auer2013/ARITHMETIC_BACKEND.md`

and a machine-readable manifest with:

- backend version/digest;
- compiler/flags;
- primitive operation mapping;
- directed rounding;
- transcendental path;
- exceptional-value policy.

Recommended: MPFR-directed/MPFI-style certified interval arithmetic.

## D3 — Analytic fixture

Implement only the IVP from Section 8.1.

Return:

- full-time hull(s);
- endpoint;
- native proof record;
- exact-reference containment check.

Expected exact endpoint:

\[
x(0.2)\in[1.10,1.11],
\qquad
y(0.2)\in[0.195,0.19595].
\]

## D4 — One predeclared DDWMR query-action

Choose **before execution** one existing benchmark query-action by deterministic rule, preferably:

> lexicographically first original query/action in the frozen benchmark manifest.

Do not select a known favorable result after inspecting R3.

Run only this one Auer query-action.

Required:

- proof-complete full-time tube;
- proof-complete endpoint;
- fixed parameter semantics;
- resource counts;
- common checker outcome.

Scientific success criterion:

> proof completeness.

The outcome may be CERTIFIED or UNKNOWN.

## D5 — Common proof binding

Add/check fields such as:

- `tube_representation`;
- `native_proof_status`;
- `proof_record_hash`;
- `endpoint_record_hash`;
- `source_snapshot_digest`;
- `arithmetic_backend_digest`.

The common checker must refuse a safety verdict from an unproven Auer hull.

## D6 — One real R3 proof fixture

Route one archived historical R3 proof through the same common layer.

Do not rerun R3.

Verify identity and margins/status.

## D7 — Handoff

Return a single review package with:

- method contract;
- arithmetic evidence;
- analytic fixture;
- one DDWMR result;
- R3 interface fixture;
- hashes;
- unresolved items;
- explicit confirmation that the 1,944 Auer matched queries were **NOT RUN**.

---

# 10.1 Stop criteria for the next package

Stop the Auer branch at this milestone and return `BLOCKED` if:

1. no certified arithmetic path can be established;
2. `clip` generalized derivative cannot be made source-faithful;
3. the analytic branch-crossing fixture cannot pass native inclusion;
4. proof records cannot establish/bind native inclusion;
5. the single DDWMR case cannot produce one full-time proof within its predeclared resource cap;
6. the only proposed rescue is post-hoc cap/tolerance/model tuning.

Do not automatically raise caps and retry indefinitely.

---

# 11. Evidence required before a later 1,944-query run

A later full matched run should be authorized only after independent review confirms all of:

1. source-faithful Auer method contract;
2. certified arithmetic backend contract;
3. successful analytic clip-crossing fixture;
4. successful proof mechanics for one predeclared DDWMR query-action;
5. full-time tube + endpoint chaining;
6. proof/query/action/source/backend binding;
7. one historical R3 common-interface fixture;
8. protocol v2 or successor reviewed and locked;
9. exact source snapshot frozen;
10. work/step caps frozen before batch output;
11. output taxonomy frozen.

Recommended output taxonomy should distinguish at least:

- `CERTIFIED`;
- mathematical `UNKNOWN`;
- `NOT_RUN`;
- `IMPLEMENTATION_FAILURE`;
- `RESOURCE_LIMIT`;
- `INVALID_INPUT` where applicable.

Do not silently map implementation failure to mathematical UNKNOWN.

---

# 12. Branch-stop interpretation

If the source-faithful Auer comparator cannot be operationally established, the correct statement is:

> **Auer comparator not operationally established under the reviewed reconstruction and resource contract.**

Do **not** conclude:

- R3 is superior;
- R3 wins;
- Auer cannot solve the mathematical problem;
- prior art is absent;
- G4 passes.

If a proof-complete Auer batch later runs but returns UNKNOWN everywhere, report zero certified coverage under that exact locked method/configuration. That can inform a scoped comparison, but it is not a universal superiority theorem.

---

# 13. Auer §5 policy

## Finding

Do not make §5 exact reproduction mandatory.

## Evidence

The accessible publication data are not sufficient for an unambiguous exact reference-output replay.

## Consequence

Use the validation ladder:

1. source equations;
2. analytic exact clip fixture;
3. one proof-backed DDWMR case;
4. optional qualitative §5 reproduction;
5. matched batch.

## Status

**SECONDARY REFERENCE**

## Required action

If authoritative original input/output files later become available, add them as an extra reproduction test without replacing the analytic fixture.

---

# 14. Relation to G2 usefulness

## Finding

Auer comparison does not by itself close G2.

## Evidence

The committed R3 review records a 1,944-query synthetic development batch:

- 1,196 CERTIFIED;
- 748 proof-complete UNKNOWN.

It also records:

- eight mixed action groups;
- in every mixed group the only certified action is zero voltage;
- existential group coverage using all actions equals coverage using zero alone:
  \[
  140=140.
  \]

Thus R3 supplies meaningful finite validation on moving cells, but practical action-selection value is still unverified.

## Consequence

Auer mainly tests G4/method distinctiveness and may inform G2 conservatism.

It cannot be used to bypass the remaining G2 usefulness question.

## Status

\[
\boxed{\textbf{G2 UNVERIFIED}}
\]

## Required action

Keep G2 and G4 dispositions separate.

---

# 15. Relation to G4 novelty

## Finding

Auer is a strong novelty threat, not a baseline chosen to be weak.

## Evidence

Auer/ValEncIA already addresses:

- verified IVP integration;
- uncertain sets;
- piecewise-smooth RHS primitives;
- generalized derivatives;
- full-time functional tubes.

Therefore novelty cannot rest on merely obtaining a certified piecewise uncertain IVP tube.

The remaining hypothesis is narrower:

> DDWMR-specific actuator/contact structure yields useful certification/tightness/cost advantages under matched assumptions.

## Consequence

If Auer is operationally reconstructed, it becomes a meaningful test of that hypothesis.

If reconstruction fails, novelty remains unresolved.

## Status

\[
\boxed{\textbf{G4 UNVERIFIED}}
\]

## Required action

Do not treat comparator failure as novelty evidence.

---

# 16. Physical correspondence

## Finding

The comparator does not validate the physical robot.

## Evidence

Both methods integrate the same reduced mathematical plant.

Neither establishes:

- real tire/contact constitutive fidelity;
- load transfer;
- driver hardware behavior;
- sensor/delay model;
- platform trajectory inclusion.

## Consequence

Physical correspondence remains separate.

## Status

\[
\boxed{\textbf{UNVERIFIED}}
\]

## Required action

None in this comparator package.

---

# 17. Gate table

| Item | Before review | Disposition here |
|---|---|---|
| Overall | HOLD | **HOLD** |
| G1 restricted model | PASS | **PASS unchanged** |
| G2 | UNVERIFIED | **UNVERIFIED** |
| G3 | UNVERIFIED | **UNVERIFIED** |
| G4 | UNVERIFIED | **UNVERIFIED** |
| Physical correspondence | UNVERIFIED | **UNVERIFIED** |
| Auer R2 preflight | BLOCKED/PARTIAL | **CORRECT — retain BLOCKED/PARTIAL** |
| Auer source applicability to clip | Partial | **SUPPORTED** |
| Auer implementation correctness | Not established | **UNVERIFIED** |
| Auer 1,944 matched run | NOT_RUN | **DO NOT RUN YET** |

No GO.

No G3.

No hardware.

---

# 18. Claim discipline

Permitted:

> Auer 2013 is a scientifically applicable comparator candidate for the continuous piecewise-linear clip benchmark.

Permitted:

> A modern certified arithmetic backend can implement a paper-faithful Auer-method reconstruction.

Permitted:

> The current R2 package remains preflight/partial and lacks a proof-backed DDWMR tube.

Not permitted:

> Original ValEncIA has been reproduced.

Not permitted:

> Auer failed on the DDWMR benchmark.

Not permitted:

> Finite arithmetic probes prove global rounding correctness.

Not permitted:

> A supplied safe hull proves reachability without native inclusion evidence.

Not permitted:

> UNKNOWN means unsafe.

Not permitted:

> Failure to reproduce Auer proves R3 superiority or novelty.

---

# 19. Exact Codex handoff instruction

Codex should issue **one bounded Luna assignment**:

`G4_AUER_R3_PROOF_BACKED_SINGLE_CASE`

with the deliverables and stop criteria in Section 10.

Do **not** request:

- 1,944-query Auer batch;
- G3 construction;
- controller/safety-filter implementation;
- hardware experiments;
- GO;
- commit/push as a condition of this review.

Because current Auer files are local/uncommitted, the returned handoff should expose exact local paths and content hashes so the next reviewer can inspect the actual artifacts.

After Codex audits that small package, relay the result for independent GPT scientific review.

Only then decide whether the full matched Auer run is justified.

---

# 20. Final disposition

## R2 partial handoff

\[
\boxed{\textbf{CORRECT}}
\]

with:

\[
\boxed{\textbf{BLOCKED/PARTIAL}}
\]

retained.

## Comparator

\[
\boxed{\textbf{CONTINUE AUER 2013}}
\]

as a paper-faithful method reconstruction.

## Arithmetic

\[
\boxed{\textbf{certified backend required before proof use}}
\]

A finite probe suite is insufficient.

## Common checker

Before proof-backed acceptance require:

\[
\boxed{
\text{native IVP proof}
+
\text{radius-once semantics}
+
\text{full-time safety}
+
\text{endpoint chaining}
+
\text{provenance binding}.
}
\]

## §5

Secondary qualitative reference only.

## Matched batch

\[
\boxed{\textbf{DO NOT RUN 1,944 AUER QUERIES YET}}
\]

## Project

\[
\boxed{\textbf{HOLD}}
\]

\[
\boxed{\textbf{G1 restricted PASS}}
\]

\[
\boxed{\textbf{G2/G3/G4 UNVERIFIED}}
\]

\[
\boxed{\textbf{physical correspondence UNVERIFIED}}
\]

A failed comparator reproduction is not an R3 win.

---

# 21. Bottom line

The next scientific milestone is not another build-only preflight and not a full batch.

It is:

> **one paper-faithful, arithmetic-certified, proof-backed Auer full-time IVP path that works on an exact branch-crossing reference and one predeclared DDWMR query-action, then composes with the common checker without double-counting radius or losing proof provenance.**

Auer 2013 remains the recommended published comparator because its method is directly matched to the selected continuous piecewise `clip`.

Until that proof-backed single-case milestone exists:

\[
\boxed{\textbf{HOLD / G4 UNVERIFIED}}
\]
