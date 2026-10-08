Session: DDWMR | LUNA-G4-AUER

# G4 Auer R22 — contribution falsification and scientific triage

**Date:** 2026-10-06  
**Disposition:** **PAUSE the G4 comparison-query branch.** Current evidence does not support another matched query or a DDWMR-specific superiority claim. One conditional method hypothesis is recorded below for possible reopening after the missing need and enclosure evidence are supplied.  
**Gate state:** G4 remains UNVERIFIED; G2/G3 and physical-platform correspondence remain UNVERIFIED; project HOLD remains in force.

## Decision summary

R3's much smaller proof files and lower measured peak worker memory leave a possible resource-use angle. The R19 pilot does not show a useful advantage at matched certification: R3 certified fewer of the ten selected cases, and on the six jointly certified cases its worker and separate offline audit times were higher. The measured proof and memory savings do not establish an operating benefit because no binding deployment resource or required coverage has been declared. Four R3 `UNKNOWN` rows did not reach the common predicate, so their predicate margins cannot be compared as if both methods had supplied tubes.

The single remaining hypothesis worth retaining is conditional: a DDWMR-specific enclosure that preserves the voltage–actuator–slip–contact and pose dependencies may recover useful common-predicate coverage at a lower *declared, operationally binding* cost than the current Auer reconstruction. This is a research conjecture, not a result. The G2 R18 diagnosis identifies a plausible enclosure bottleneck, but the G2 R19 prototype has no reviewed result here. Do not run a new G4 query until that bottleneck is addressed mathematically and the intended operating need is declared.

## Scope and execution record

I read `AGENTS.md`, all four canonical `research_context/` files, the R21 Codex review and handoff, the G2 R18 handoff and review, the G2 R19 assignment and the available primary Auer 2013 paper. I also inspected the R3 evaluator/checker, the matched Auer residual-IVP producer/replayer, the R21 saved analysis reference and the read-only G2 R19 prototype source.

This handoff is based on saved sources and artifacts only. **No query, worker, auditor, stage, retry, batch, GO receipt, G3 work, source mutation, commit or push was performed.** R19/R20 evidence was not changed. The planned 1,944-query batch remains unrun; the ten R19 matched IDs remain consumed development evidence.

## 1. Preserved R19 pilot: what it does and does not establish

Codex's R21 review accepted the descriptive extraction after independently rehashing all 156 input artifacts, checking the proof byte counts and recomputing the reported status and cost totals. The ten IDs were deliberately selected and are not a representative or independent sample.

| Saved pilot measure | R3 | Auer reconstruction | Interpretation |
|---|---:|---:|---|
| Final `CERTIFIED` | 6/10 | 9/10 | Three Auer-certified/R3-unknown pairs; no reverse pair. |
| Final `UNKNOWN` | 4/10 | 1/10 | Inconclusive results; not unsafe outcomes. |
| Total native proof bytes | 1,137,484 | 25,332,478 | R3 files are much smaller in this selected pilot. |
| Worker wall, all ten | 15.595 s | 23.359 s | R3's quick `UNKNOWN` exits make this total misleading as a useful-work comparison. |
| Worker wall, six jointly certified | 12.658 s | 9.437 s | R3 took longer on these same six cases. |
| Separate offline audit wall, those six | 24.205 s | 19.609 s | R3 also took longer in the applicable audit measurements. |
| Peak matched-worker memory | 56,332,288 B | 123,445,248 B | R3 used less measured peak memory; both are below the shared 1 GiB research cap. |

The four R3 `UNKNOWN` records did not enter the common predicate. R3's recorded negative sufficient margins were collision for query 1, collision and contact for query 2, and contact for queries 5 and 8. Auer supplied proof-complete tubes that passed the common predicate on queries 1, 5 and 8. Query 2 remained `UNKNOWN` for Auer as well because a supplied-tube segment had a negative collision lower bound. Thus `UNKNOWN` is not evidence of a collision, contact loss, or unsafe physical trajectory; nor may the four R3 native margins be described as common-predicate evaluations.

All 20 method records use the same locked ten IDs and common-profile SHA-256 `35731201512145219327ea862ffc7ef37c5a100f66740cde80dcdc5eb021adfe`. R19's original checker exited 2 on the guard/terminal path-string comparison. R20 retrospectively replayed all ten saved pairs with the corrected path binding and exited 0; it did not rerun any query or change R19 bytes. Both facts remain part of the evidence record. Four historical IDs are separate from the ten R19 IDs; the fixed universe is 1,944, with 1,930 continuation IDs unattempted.

**Inference limit:** smaller proof bytes and lower peak memory are real descriptive observations on these ten cases. They do not establish a deployment advantage, especially while R3 has lower certified coverage and higher measured worker and audit wall on the jointly certified subset. The 1 GiB memory and 120-second wall limits are the research harness profile, not declared platform requirements. No statistical, population-rate, or universal-dominance claim follows from the selected ten.

## 2. Source-level comparison on the same reduced plant

The compared benchmark fixes one nine-state voltage-driven reduced DDWMR, one held two-wheel voltage, the same initial-state cell and full parameter image, and the same common collision/contact predicate. The core plant has

\[
\dot p_x=u\cos\theta,\quad \dot p_y=u\sin\theta,\quad \dot\theta=r,
\]
\[
\sigma_L=R_w\omega_L-u+br,\qquad
\sigma_R=R_w\omega_R-u-br,
\]
\[
F_j=C_j\,\phi(\sigma_j/v_s),\quad
m\dot u=F_L+F_R-c_u u,\quad
I_z\dot r=b(F_R-F_L)-c_r r,
\]
with wheel and electrical dynamics driven by the same held terminal voltage. The matched benchmark uses its fixed `clip` instance for \(\phi\). MASTER v2.1 treats the hidden labels as fixed for the entire execution and requires full-hold collision and parameter-specific algebraic contact admissibility. It does not establish physical tire/support correspondence.

### R3 enclosure actually used

The R3 path is the `G2_COMP_CLIP_WHOLE_HOLD_DYADIC_DISTANCE_N1_R3` evaluator, with R17 worker/provenance wrappers and the R9-pinned numerical method. In the six internal coordinates \(z=(u,r,\omega_L,\omega_R,i_L,i_R)\), it evaluates a parameter-interval linear part and the clip contact force. The implementation forms an interval matrix exponential \(E\), then two full-hold predictor ranges of the form

\[
P_0=EX+[0,T]E(BV+DF(X)),\qquad
P_1=EX+[0,T]E(BV+DF(P_0)).
\]

Here \(A,B,D\), and the slip map \(S\) are derived from the DDWMR model and evaluated over the complete parameter-label image. The code bounds the predictor change, converts it through the contact-force Lipschitz bounds into a residual forcing, and propagates a nonnegative comparison-matrix series plus an explicit tail bound to an internal error radius \(\eta\). The full-hold internal range is the interval predictor enlarged by that radius. The implementation uses one initial-state leaf, one parameter leaf and one whole-hold predictor panel; interval operations can discard state/parameter and time correlations.

R3 then lifts its internal range to pose, slip and contact checks. Its sufficient contact lower bound has the form

\[
\underline c=\sum_{j\in\{L,R\}} C_{j,\min}\sqrt{1-\beta_j^2}
 -m_{\max}(U+\eta_u)(R+\eta_r),\qquad
\beta_j=\min\{1,\ \overline{|\operatorname{clip}(\sigma_j/v_s)|}
                  +\text{slip-radius}_j\}.
\]

When the outward slip bound reaches a clip saturation corner, \(\beta_j=1\) and that wheel's certified reserve is zero. R3's collision lower margin uses the distance from an axis-aligned pose enclosure to the obstacle, less its pose-error radius. These are sound sufficient checks for the declared formal model; negative lower margins yield `UNKNOWN`, not evidence that the underlying trajectory violates the condition. Source: [`validation/g2/evaluator.py`](../../validation/g2/evaluator.py#L53), especially `_bound_model_matrices`, `_radius_series`, `_predictor_level` and `_evaluate_bounds` at lines 57–422; independent native replay is in [`validation/g2/checker.py`](../../validation/g2/checker.py#L48).

### Auer residual-IVP core actually used

The primary source is E. Auer, S. Kiel and A. Rauh, “A Verified Method for Solving Piecewise Smooth Initial Value Problems,” *International Journal of Applied Mathematics and Computer Science* 23(4), 731–747 (2013), DOI 10.2478/amcs-2013-0055. The repository retains the complete paper PDF and extracted text at [`research/third_party/auer2013/auer-kiel-rauh-2013.pdf`](../../research/third_party/auer2013/auer-kiel-rauh-2013.pdf) and `.txt`. The PDF SHA-256 is `D6310C8FD32280ADDDA3F50E3367F9923940641D39DE0E70A0932869A2D0EAD2`.

Relevant source locations are §4.1, Eqs. (26)–(33) and Properties 1–2 (printed pp. 740–741); the generalized mean-value rule for a discontinuous branch is Eqs. (35)–(41) and Property 3 (pp. 741–742); and §4.2, functional tube Eq. (42), residual Picard update Eq. (43), and its fixed-point justification (pp. 742–743). In particular, Eq. (42) represents the exact solution in a tube around an approximate path, while Eq. (43) iterates a residual derivative. The mean-value inclusion is what permits the local implementation to use an interval generalized Jacobian. For this benchmark's continuous clip, the generalized derivative is `{0}` on saturated intervals, `{1}` in the interior and `[0,1]` at or across a clip corner; the discontinuity jump correction in Eqs. (35)/(41) is zero for this continuous law.

The matched reconstruction uses a linear rational approximate path over each trial slab, initialized at the midpoint of the augmented state/label box. It augments the nine physical coordinates with twelve parameter-label coordinates whose derivative is zero. With initial error \(R_0\), old residual derivative \(D_k\), rough tube \(Q_k=x_{app}([t_k,t_{k+1}])+R_k\), and generalized Jacobian interval \(J(Q_k)\), it computes

\[
R_k=R_0+[0,h]D_k,\qquad
D_{k+1}=f(x_{app})-\dot x_{app}+J(Q_k)R_k,
\]
then checks both \(D_{k+1}\subseteq D_k\) and the induced integrated-tube inclusion. The endpoint uses \(R_0+hD_{k+1}\); the full-time hull uses \(x_{app}([0,h])+R_k\). If a slab does not meet the frozen inclusion checks, the candidate halves its step and retries within the frozen profile; accepted endpoint and unchanged label intervals are carried forward. The R17 method calls the common predicate on these native total hulls without adding the radius again. Source: [`residual_ivp_g4_matched_v3_r9.py`](../../validation/baselines/auer2013/residual_ivp_g4_matched_v3_r9.py#L302) (trial-step construction) and lines 464–590 (held-label contract, step acceptance and endpoint carry); the independent checker is [`replay_ivp.py`](../../validation/baselines/auer2013/replay_ivp.py#L202) and its DDWMR replay at line 390 onward.

The paper's §5 example is a mechanical friction/hysteresis system, not a DDWMR. It does not supply a theorem for voltage-driven wheel/current/body coupling, the MASTER slip law, the algebraic contact domain, obstacle separation, or recursive safety. The local method is a documented reconstruction using exact-rational intervals and a separate checker; it is not reproduction of the original VALENCIA binary or the paper's §5 results. The legacy VALENCIA seed in the repository is not the 2013 piecewise extension. These limits are recorded in [`G4_AUER_METHOD_CONTRACT_v2.md`](G4_AUER_METHOD_CONTRACT_v2.md#1-primary-sources-and-corrected-locators) and the R4 review.

### Generic inclusion versus DDWMR-specific treatment

| Component | Generic validated-integration logic | DDWMR-specific use in the matched artifacts |
|---|---|---|
| R3 | Interval exponential prediction, componentwise comparison/growth bound, finite positive matrix-series enclosure and independent replay. Such enclosure/inclusion machinery is not original by itself; the research context already records overlap with Arcak–Maidens §2 Proposition 1/Corollary 1 and §3 Algorithm 1, and TIRA §3.1 Eq. (4)/Proposition 4. | The matrices map the voltage-driven actuator and wheel dynamics into body/slip states; `S`, clip force, contact-reserve formula and pose/obstacle lift come from the reduced DDWMR. |
| Auer | Piecewise interval evaluation, generalized derivative, mean-value/Jacobian tube, residual Picard inclusion and fixed-point argument are the source method's general machinery. The paper itself presents this for a class of piecewise-smooth IVPs. | The implementation evaluates the nine-state MASTER RHS and its 21-coordinate augmented Jacobian, including voltage, actuator states, slip-force feedback and fixed parameter labels. The separate common predicate supplies the DDWMR contact and obstacle tests; those tests are not Auer's 2013 theorem. |
| Both | Exact/outward interval arithmetic, proof replay and a common sufficient predicate are evidence of validated computation under pinned source assumptions, not by themselves novelty or platform safety. | Both use the same locked query inputs, profile hash and final common predicate. Neither result validates the ideal-contact reduction on a physical robot. |

The distinction matters: R3's matrix decomposition and common contact/pose bounds are more explicitly structured around this plant, while Auer's residual-IVP construction is a generic method instantiated on the same plant. Conversely, plant substitution and a smaller proof serialization are not enough to establish a novel enclosure. A contribution would need a reviewed mathematical construction that exploits the actuator–slip–contact and joint pose dependence in a way that yields decision-relevant results beyond generic validated integration.

## 3. Coordination with G2 R18/R19

G2 R18 is a separate two-row G2 development diagnosis (R5 indices 62 and 74), not the G4 ten-pair R19 pilot. Its saved R17 records are valid `UNKNOWN`: the initial boxes have positive exact collision/contact margins, but broad accepted boxes make clip-slip intervals reach saturation, yielding zero sufficient lateral reserve with positive demand; the pose rectangles also fail to separate the obstacle on affected slabs. The R18 review qualifies the causal explanation: the record identifies the first *saved* coarse enclosure where sufficient tests fail, but does not isolate the effects of predictor evaluation, box inflation, endpoint carry, parameter dependence and projection. It does not establish actual collision or contact loss.

The G2 R19 assignment requests a structured enclosure improvement on those saved rows and explicitly forbids fresh rows/stages. The repository contains `validation/scripts/prototype_g2_r19_picard_hull_contractor.py`, a source-level candidate for repeated nested Picard hull contraction. I inspected its source but did not execute it; no R19 output or independent review was used as evidence in this triage. Its existence does not establish that the contractor tightens the needed slip, pose or progress bounds, that its whole-hold argument is accepted, or that it preserves sufficient correlation. Any G2 R19 outcome must be reviewed against those obligations before it informs G4.

This coordination supports only the sequencing decision: first determine whether the saved G2 enclosure bottleneck has a sound, independently replayable remedy on the consumed G2 diagnostic rows; then assess whether that remedy creates a DDWMR-specific scientific contribution. It does not assume G2 R19 succeeds and does not transfer G2 development evidence into a fresh G4 validation result.

## 4. One conditional hypothesis and prospective falsifier

**Hypothesis H (conditional, not presently supported):** a source-bound DDWMR enclosure that retains useful dependence among held voltage, motor current, wheel rate, longitudinal slip, contact reserve and joint pose can achieve at least the Auer reconstruction's common-predicate certification coverage on a prospectively locked operational workload while reducing the resource that the actual application declares binding.

This is the only hypothesis retained. It is not a claim that an enclosure improvement exists or that it would be original relative to prior reachability and validated-IVP work. The existing pilot weighs against its usefulness/speed side: R3 certified 6/10 against Auer's 9/10, while its smaller proofs and lower peak memory were not tied to a declared constraint. The pilot is too selected and too small to prove universal inferiority or falsify H across an operational workload.

**Prospective matched criterion, to be frozen before selecting new IDs:**

1. The operating owner must first state the operational query set \(Q_{op}\), minimum needed certified coverage \(C_{req}\), and the resource that actually binds the decision path: for example worker deadline, online peak memory, or proof storage/transfer. If the audit is offline, report its time separately from the synchronous worker path. Supply actual limits from the intended workflow; do not substitute the pilot's measurements or the research harness's 1 GiB/120 s caps.
2. On the same fresh, predeclared IDs and the same fixed benchmark inputs, parameter image, held voltages, common profile and thresholds, count coverage only when the native proof replays and the unchanged common predicate returns `PASS_ON_SUPPLIED_TUBE`. Report `UNKNOWN`, resource stops and implementation failures separately; `UNKNOWN` is unavailable certification, not unsafe truth.
3. H passes this comparison only if the candidate reaches \(C_{req}\), has coverage no lower than Auer on that same locked set (zero non-inferiority allowance unless the owner prospectively specifies another one), and strictly improves the predeclared binding resource while meeting its actual limit. Continue to report worker time, independent replay/audit time, peak memory and proof bytes separately. Do not change the common threshold, eligible IDs or cost measure after seeing results.

**Falsifier:** after source/proof review, H fails for the declared workload if the candidate cannot prove the full-hold fixed-label inclusion, falls below \(C_{req}\), certifies fewer locked cases than Auer under the frozen rule, fails the actual resource limit, or does not improve the predeclared binding resource at matched coverage. Such a result is a blocker for this application/domain, not proof that all DDWMR enclosures are impossible.

At present \(Q_{op}\), \(C_{req}\), the binding resource and its operational limit are unspecified. Therefore the criterion cannot yet be instantiated without inventing requirements, and **no new G4 query is justified**. A theoretical candidate may be examined against saved development artifacts, but those consumed artifacts cannot be relabeled as prospective evidence.

## 5. Reopen conditions and evidence ledger

Reopen the query-level G4 branch only after:

1. A domain owner defines where the computation and proof checking occur, the actual resource constraint, and the minimum certification coverage needed for a decision.
2. The G2 R19 enclosure candidate, if returned, has a source-backed proof/replay review and quantified effects on the consumed G2 rows; otherwise record the exact mathematical blocker and stop that candidate.
3. The DDWMR-specific step is distinguished from generic validated integration and screened against the primary reachability/enclosure sources. `LITERATURE_MATRIX.md` rows 25–27 already identify generic overlap and incomplete source coverage; G4 novelty remains open, and unknown entries are not negative novelty evidence.
4. Any later matched sample is selected prospectively from unused IDs, with methods, common predicate, resource/cost rule and falsification threshold frozen before outcomes, followed by independent review and a separate exact-scope GO. This handoff grants no such GO and no batch authority.

| Claim | Disposition |
|---|---|
| R21 pilot counts, proof bytes and cost totals as descriptive results | **VALID** within the preserved, selected ten-pair pilot; R20 retrospective replay is recorded. |
| `UNKNOWN` implies unsafe or actual contact/collision failure | **REJECTED**; it is inconclusive. |
| R3 has a proof-size and peak-memory advantage on these ten records | **VALID** as a descriptive measurement only. |
| R3 has a demonstrated useful coverage or speed advantage | **NOT SUPPORTED** by the pilot. |
| Auer 2013 supplies generic piecewise-IVP residual/mean-value method locations | **VALID**, with the scope/access limits stated above. |
| Auer 2013 supplies a DDWMR voltage/contact/obstacle theorem | **NOT ESTABLISHED** by the source; do not infer novelty from that absence. |
| G2 R18 locates a saved enclosure bottleneck | **VALID** as a saved-artifact diagnosis, with the review's causal qualification. |
| G2 R19 contractor improves the bottleneck or establishes a contribution | **UNVERIFIED**; the prototype source was not executed or accepted here. |
| Any DDWMR-specific novelty or physical-platform relevance | **UNVERIFIED**; the literature and platform correspondence work remain open. |
| Another matched G4 query now | **PAUSE** until the reopen conditions and prospective criterion are met. |

### Source and artifact references

- R21 assignment, Codex review and accepted handoff: `docs/CODEX_TO_LUNA_G4_AUER_R21_PILOT_SCIENTIFIC_TRIAGE.md`, `docs/reviews/CODEX_G4_AUER_R21_PILOT_SCIENTIFIC_TRIAGE_REVIEW.md`, `docs/reviews/LUNA_TO_CODEX_G4_AUER_R21_PILOT_SCIENT_TRIAGE_FULL_HANDOFF.md`.
- Machine-readable pilot analysis (156-entry artifact ledger): `results/validation/g4/auer2013/protocol_v3_r21_pilot_triage/pilot_artifact_analysis.json`; extraction source: `validation/scripts/analyze_g4_auer_v3_r21_pilot.py`.
- R19 preserved execution and R20 retrospective replay: `docs/reviews/LUNA_TO_CODEX_G4_AUER_R19_STAGE_01_EXECUTION_FULL_HANDOFF.md`, `docs/reviews/LUNA_TO_CODEX_G4_AUER_R20_PATH_BINDING_FULL_HANDOFF.md`, `docs/reviews/CODEX_G4_AUER_R20_PATH_BINDING_REVIEW.md`.
- Auer primary PDF/text and reconstruction crosswalk: `research/third_party/auer2013/auer-kiel-rauh-2013.pdf`, `research/third_party/auer2013/auer-kiel-rauh-2013.txt`, `docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md`; R4 source review: `docs/reviews/CODEX_G4_AUER_R4_IVP_CORE_REVIEW.md`.
- R3 source and replay: `validation/g2/evaluator.py`, `validation/g2/checker.py`, `validation/g4/r3_matched_query_worker_v3_r17.py`, `validation/g4/r3_common_adapter_v3_r17.py`.
- Auer matched producer/replay: `validation/baselines/auer2013/residual_ivp_g4_matched_v3_r9.py`, `validation/baselines/auer2013/replay_ivp.py`, `validation/g4/auer_common_adapter_v3_r17.py`.
- G2 R18 diagnosis/review and pending G2 R19 assignment: `docs/reviews/LUNA_TO_CODEX_G2_R18_TWO_ROW_ENCLOSURE_DIAGNOSIS.md`, `docs/reviews/CODEX_G2_R18_TWO_ROW_ENCLOSURE_DIAGNOSIS_REVIEW.md`, `docs/CODEX_TO_LUNA_G2_R19_STRUCTURE_PRESERVING_ENCLOSURE_RESEARCH.md`, `validation/scripts/prototype_g2_r19_picard_hull_contractor.py`.
- Canonical scope and novelty limits: `AGENTS.md`, `research_context/MASTER_RESEARCH_CONTEXT_v2.md` §§1, 8–16, 20–32, `research_context/LITERATURE_MATRIX.md` rows 25–27, `research_context/REVIEW_GATE.md`.

**Final decision: PAUSE new G4 comparison execution.** G4 remains UNVERIFIED; the preserved R19/R20 evidence remains unchanged; no new query or stage was run.
