Session: DDWMR | LUNA-G2-SCOPE

# G2 R19 — structure-preserving enclosure research

**Date:** 2026-10-06  
**Disposition:** **PURSUE** a shared-variable validated Taylor-model enclosure with a source-bound residual checker. **STOP** the nested axis-box contraction as a stand-alone certifier; retain it only as a cheap preconditioner/development diagnostic.  
**Execution:** zero new real rows, zero native queries/workers/stages; R5 remains **800/800 `NOT_RUN`**.

## Finding

R19 tested an exact-rational postfixed-hull contraction on the already consumed R17 rows 62 and 74. It materially narrows the saved interval boxes and improves one collision slab and both task-progress lower bounds. It does **not** recover a positive reserve on any slab, does not separate the complete collision tube on either row, and leaves progress below the frozen threshold. The result validates a useful inexpensive contraction step, not a full-hold success.

The next mathematical direction is to preserve the common initial-state, fixed-parameter and time variables in one parameterized enclosure for all nine states. A validated Taylor-model predictor with an outward residual tube can retain those dependencies while using the existing Picard boxes as coarse domains for local Lipschitz bounds. Its soundness can be reduced to a directly checkable defect bound and Grönwall comparison; this requires no derivative of the clipped traction law or of the square-root contact reserve.

## Scope and evidence identity

The governing assignment is `docs/CODEX_TO_LUNA_G2_R19_STRUCTURE_PRESERVING_ENCLOSURE_RESEARCH.md`. I read `AGENTS.md`, all four canonical `research_context` files, the R18 handoff/review, the accepted G2 enclosure and scoped-acceptance candidates, and the finite synthetic Cases A/B/C. The accepted cases do not establish a general practical evaluator or voltage-selection value; G2, G3, G4, physical-platform correspondence and overall HOLD remain unchanged.

The diagnostic reads and verifies the R17 GO, manifest, source closure, authorization, receipt and both records before evaluating the saved query payloads. It checks the bindings against the ordered manifest and checks the R10 arithmetic-source pins. The exact hashes are:

| Bound artifact | Raw SHA-256 |
|---|---|
| R19 diagnostic script `validation/scripts/prototype_g2_r19_picard_hull_contractor.py` | `daa53366d305deaf759fec40fb1551f9619f93f36fb1a02044945322f31df357` |
| R17 manifest | `a4913d3d0282de6a5d1a16c4c88e3c402a91f1c3dee2df1ea99afd44a71c6bb9` |
| R17 source closure | `5b6838c8da6ae55e33ad4b50c9182122943f669e63e0fa9d92e6a8de3b83ce86` |
| R17 GO and stored authorization | `314dcce10a10db9c862b99694e5b1cda6e72bcae27fdabaeefa17f105a6af30f` |
| R17 stage receipt raw | `52a1aaec3eadf8d729c036e7f181e4e57e702068c1d76df53b120e1a34baddef` |
| R17 receipt semantic | `a5608e619c4699743446c9ca7ea5806681684826307d9d7bce8797852194614f` |
| R17 row 62 record | `316434ab6eacb7e221eca4feb1062001a8b576b450b725bbc1246d5e744f5cf3` |
| R17 row 74 record | `fbb23303ff218e3ddf56453ccea7ca41a70d40f0ff1e85335341eff7e5651421` |

The diagnostic command that succeeds from the repository root is:

```text
python -m validation.scripts.prototype_g2_r19_picard_hull_contractor
```

Calling the script by its documented file path currently raises `ModuleNotFoundError: No module named 'validation'`; the module invocation works. The script is read-only with respect to the R17 stage and has no producer, worker, runner, `run_query`, native-query, controller or experiment call. It imports `_rhs`, `_picard_images` and `_pose_contact` from the R10 producer, so its arithmetic output is a bound development diagnostic, **not independent replay**. It prints the diagnostic JSON rather than writing a certificate record.

The inspected source closure includes:

| Source | Raw SHA-256 |
|---|---|
| `validation/g2/time_slab_picard_r10.py` | `e9fa6672649d675e27bb4f419e28259b9546b01bb6592f3388396ecd2a211c47` |
| `validation/g2/whole_hold_picard_checker_r11.py` | `2a794e8f46c4b029331a2548dccd1948b78d3f5d5d7a96efa118d9353ba56f7e` |
| `validation/g2/model.py` | `93e9a96d640ad09a7eb7dbff51ebfb8f2d783296ce5afff57af41e81e30a8508` |
| `validation/g2/interval.py` | `e49e2e3880485d9a658e2435cfa06b784f98257b13c51fa4a2bf464f9c73e5c6` |
| `validation/g2/rational.py` | `8a2c16778b33898afd16c8da44945c2d41fd7d187cb11c7cb071745e68ed5c6e` |

R17 row 62 is `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_L0_R0`, held voltage (0,0); row 74 is `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_Lp1_Rp1`, held voltage (1,1). Both bind the same initial-state cell, complete parameter-label cell, obstacle, horizon T=1/4, radius R_s=3/50 and progress threshold 1/20. They are consumed development-overlap rows, not fresh validation. Row 62 has one slab of duration 1/4; row 74 has two carried slabs of duration 1/8. The complete parameter image and held voltage are reused on every slab, with no parameter subdivision.

## Comparison of enclosure representations

| Representation | What it encloses | Dependence retained/lost | Consequence here |
|---|---|---|---|
| R10 interval Picard | Six coordinate intervals for internal states plus separate pose intervals on each slab. It checks the source-defined Picard tube inclusion and carries interval endpoints. | The full parameter image and held voltage are common, so the physical parameter is not assumed to switch. Coordinatewise interval RHS, endpoint carry and pose/slip projections still forget correlations among state coordinates, labels, position coordinates and time. | Sound conditional full-hold outer proof; R17 boxes saturate both slip tests and overlap/approach the obstacle in the sufficient rectangular-distance test. |
| R19 hull contraction | Repeats the nested-box contractor B_next = hull(X, X + [0,h]G(B)) on each saved slab; it checks nesting and recomputes the final postfixed inclusion. | Contracts coordinate bounds, but the result is still an axis-aligned box; it adds no state/label/time correlation. | Improves pose and progress ranges; all tested contact bounds remain at clip saturation, and at least one collision slab per row remains inconclusive. |
| Proposed shared-variable residual tube | One Taylor-model predictor for all nine states on each covered initial/parameter cell, enlarged by a certified residual-error radius. | Keeps the same initial/parameter variables across the hold and jointly represents all nine states and time. Piecewise clip branches or direct corner-safe interval composition bound the declared clip law. | Supports joint pose-distance and same-cell contact/progress checks. Its usefulness is a hypothesis until an independent checker and full-cell computation are completed. |

The clip-specific fact available here is phi(q) = clip(q,-1,1), a monotone, globally 1-Lipschitz, piecewise-affine function including both corners. The design below uses only this declared instance. It assumes no monotonicity or differentiability for a general MASTER traction law.

## Exact R17 development diagnostics

The prototype performs 12 passes per archived slab. On each pass it computes the rational interval RHS over the current box, forms the tube X + [0,h]G(B), takes its coordinate hull with X, and rejects any non-nested result. It then recomputes the RHS on the final box and checks X is contained in B and the full Picard tube is contained in B. The R10 closed-slab theorem is conditional on that uniform RHS inclusion plus its fixed-label Lipschitz bound; final postfixed inclusion is checked in the diagnostic, but there is no new independent R19 checker.

All decimal brackets in the diagnostic tables are outward rational enclosures rounded to millionths; they supplement the exact fractions and do not replace them.

### Slip and contact

The slip intervals below are outward rational roundings of the exact R19 interval endpoints to millionths; they are display enclosures. R17 baseline values are exact values from the saved-record diagnosis.

| Row / slab | R17 slip intervals (left; right) | R19 contracted slip intervals (left; right) | R19 beta upper (L, R) | Reserve lower | Demand upper (approx.) | Contact margin |
|---|---|---|---|---:|---:|---:|
| 62 / 0 | [-6.8219,6.6019];[-6.8987,6.7187] | [-2.377907,2.183948];[-2.362030,2.200071] | (1,1) | 0 | 0.714417 to 0.714418 | -804363101269925426357/1125899906842624000000 < 0 |
| 74 / 0 | [-3.54595,3.32595];[-3.57435,3.39435] | [-1.046021,0.904066];[-1.032749,0.920299] | (1,1) | 0 | 0.165771 to 0.165772 | -15545814828495078235801531282739374122423347040288614005471670365185041339001164933113/93778296809785602500326041059328000000000000000000000000000000000000000000000000000000 < 0 |
| 74 / 1 | [-331391833489/86400000000,314192833489/86400000000];[-330896914477/86400000000,316721914477/86400000000] | [-2.016695,1.930961];[-2.005388,1.945984] | (1,1) | 0 | 0.581933 to 0.581934 | -477245661116309209152810879897118739052905677099700886272581312663049979932368659818134996295226511541871439/820102751250246121894274084667900875057053645878067200000000000000000000000000000000000000000000000000000000 < 0 |

Every R19 slip interval still reaches a saturation value after clipping, so both certified beta upper bounds are exactly 1. The square-root reserve lower bound is therefore exactly zero on every slab. The positive demand bounds make all contact-margin lower bounds strictly negative. The slip intervals are narrower than the R17 intervals, especially row 74 slab 0, but this contractor does **not** improve the reserve certification. By the stipulated contact test, these negative margins mean `UNKNOWN`; they do not prove that an actual trajectory loses contact.

### Joint pose distance and task progress

Collision lower bounds use the source-pinned rational pose, trigonometric and square-root interval routines applied to each **axis-aligned** contracted position tube; they are not a new joint Taylor-model distance bound. The unchanged obstacle radius is 3/50 = 0.06.

| Row / slab | R17 distance lower | R19 distance lower | R19 collision margin lower | Result on this slab |
|---|---:|---:|---:|---|
| 62 / 0 | 0 | 368597051113/140737488355328 (outward decimal bracket 0.002619 to 0.002620) | -201891306255167/3518437208883200 (outward decimal bracket -0.057381 to -0.057380) | Inconclusive |
| 74 / 0 | 1540220173689/70368744177664 (about 0.0219) | 9980868345273/70368744177664 (outward decimal bracket 0.141836 to 0.141837) | 143968592365329/1759218604441600 (outward decimal bracket 0.081836 to 0.081837) | Positive slab bound |
| 74 / 1 | 0 | 1464827558261/35184372088832 (outward decimal bracket 0.041632 to 0.041633) | -16155869176723/879609302220800 (outward decimal bracket -0.018368 to -0.018367) | Inconclusive |

The R19 box contraction recovers a positive collision margin on row 74 slab 0, but not the entire hold: slab 1 remains below the unchanged radius. Row 62 also remains below it. These are improvements to outer bounds and do not establish a collision or noncollision of a true path.

| Row | R17 progress lower | R19 progress lower | Frozen threshold (1/20) | Outcome |
|---|---:|---:|---:|---|
| 62 | -6301/8000 = -0.787625 | -19685271901/134217728000 (outward decimal bracket -0.146667 to -0.146666) | 1/20 = 0.05 | Fails the sufficient task test |
| 74 | -322837/1024000 (about -0.31527) | -1038229544751489153144496499988278335958285043496181281/12548295830113635610059079680000000000000000000000000000 (outward decimal bracket -0.082739 to -0.082738) | 1/20 = 0.05 | Fails the sufficient task test |

Thus the contractor improves both progress lower bounds but certifies neither task threshold. No voltage-selection value follows from two consumed rows where both safety outcomes remain `UNKNOWN` and both task tests fail.

## Proposed sound alternative: shared-variable Taylor predictor plus defect tube

This is a candidate design, not a completed implementation or an R17 certificate. It keeps the exact nine-state reduced plant, clip law, full initial cell, full joint parameter image and held voltage unchanged.

1. Cover the exact product of the initial-state cell X0 and parameter cell Theta by finitely many closed rational cells Xi_i; overlaps on cell boundaries are allowed, gaps are not. Store the original variable map xi -> (x0, theta) for each leaf. Any further branch in a slab restricts that same leaf and keeps the same xi and fixed theta through every later slab.
2. On slab k, over [t_k,t_(k+1)] with duration h_k, form one differentiable rational Taylor-model predictor P_(i,k)(xi,tau), for 0 <= tau <= h_k, for all nine states. Use a rational polynomial as the explicit comparison path. A practical center is the variation-of-constants predictor for the linear actuator/state block, with the motor matrix exponential and integrals approximated by rational Taylor truncations. Evaluate the clipped-force contribution with a piecewise-affine clip composition or direct corner-safe interval composition. Keep exact polynomial coefficients and outward range bounds over the shared variables; include truncation, interval-evaluation and arithmetic remainders in the residual bound, not as unspecified terms whose derivatives are assumed to exist. This is where the representation preserves common state, parameter, pose and time dependence.
3. Choose a verified compact convex domain D_(i,k) containing the predictor range and the current coarse R10 enclosure. Convexity places every segment between the exact path in that enclosure and the predictor in this domain. Compute an outward infinity-norm Lipschitz bound L_(i,k) for the **nine-state** reduced vector field and a residual bound
   $$
   \rho_{i,k}\ \ge\ \sup_{\xi\in\Xi_i,\,0\le\tau\le h_k}
   \left\|\partial_\tau P_{i,k}(\xi,\tau)-
   f_9(P_{i,k}(\xi,\tau),V;\vartheta(\xi))\right\|_\infty.
   $$
   Rational polynomial range bounds, certified trigonometric ranges, the exact clip graph and outward residual bounds must be checked over the **whole** cell and slab. Differentiate only the explicit polynomial comparison path; evaluate and range the generally nonsmooth f9 without differentiating it. Do not use a floating-point matrix exponential, unbounded series tail, point samples, or a derivative of `clip` at its corners.
4. If the start error for this same xi is bounded by E_(i,k)^0, Grönwall's inequality gives for every point in the closed slab
   $$
   E_{i,k}(\tau)=e^{L_{i,k}\tau}E_{i,k}^0+
   \rho_{i,k}\frac{e^{L_{i,k}\tau}-1}{L_{i,k}},
   $$
   with E_(i,k)(tau) = E_(i,k)^0 + rho_(i,k) tau when L_(i,k) = 0. The reported exponential and division are outward rational bounds. This follows by applying the uniform state-Lipschitz inequality to the exact path and the predictor, then the scalar Grönwall inequality. It does not differentiate the exact solution or require smoothness of the clip law.
5. Initialize P_(i,0)(xi,0) = x0(xi) and E_(i,0)^0 = 0, or explicitly enclose any initialization defect. At every boundary require P_(i,k+1)(xi,0) = P_(i,k)(xi,h_k) for the same xi, or add a checked reset defect to E_(i,k+1)^0 >= E_(i,k)(h_k). Check contiguous times and exact sum of slab durations h_k = T. The single label and voltage remain fixed; never choose a favorable parameter anew on the next slab.

### Joint safety and task tests on the structured tube

For every covered leaf and complete slab, range the two position coordinates from the same predictor and add the certified error radius in each coordinate. Use a directed lower bound on
$$
q_{i,k}^-\ \le\ \inf_{\xi,\tau}
\left((p_x-o_x)^2+(p_y-o_y)^2\right),\qquad
g_{p,i,k}^-=\sqrt{\max(0,q_{i,k}^-)}-R_s.
$$
The square/root and polynomial range are rounded outward. A shared-variable polynomial range or branch-and-bound lower bound can retain the px, py, time, parameter and initial-state relationships that the rectangle discards. Every branch and every slab must have a nonnegative collision lower bound.

For contact, evaluate both slips, u and r over the polynomial predictor enlarged by its certified Grönwall error tube, then directly range the exact declared clipped slips
$$
s_L=(R_w\omega_L-u+br)/v_s,\qquad
s_R=(R_w\omega_R-u-br)/v_s,
$$
and let beta_j^+ be the supremum of the absolute clipped slip over the full leaf and slab, in [0,1]. The sufficient reserve lower bound and demand upper bound are
$$
A_{i,k}^- =\sum_{j\in\{L,R\}}\underline C_j
\sqrt{\max(0,1-(\beta_j^+)^2)},\qquad
D_{i,k}^+=\overline m\,\sup|u|\,\sup|r|,
$$
$$
g_{c,i,k}^-=A_{i,k}^- -D_{i,k}^+\ \ge0.
$$
For the contact margin, if a slip range reaches +1 or -1, that wheel contributes **zero** certified reserve; if both reach a corner, the sufficient test passes only if the other certified reserve(s) still cover demand (with two wheels here, both zero requires demand upper bound D+ = 0). A corner touch is not automatically proof of contact loss. Do not differentiate the square-root reserve near beta = 1, whose derivative is unbounded; use a direct monotone lower evaluation or a direct nonsmooth range of the complete margin.

For task progress, carry the same variables into J(xi) = integral from 0 to T of u(xi,t) cos(theta(xi,t)) dt. Integrate the Taylor polynomial with exact rational coefficients and add an outward bound for the integrand error from the certified state tube. For an all-cell task claim require the infimum over each Xi_i of J(xi) to be at least 1/20. Collision, contact and task checks cover the closed hold, not just the slab endpoints.

## Smallest reviewable artifact and prospective challenge

If the method is pursued, the smallest independent-review package is:

1. A versioned R20 Taylor-model producer defining the exact rational polynomial/remainder format, fixed-variable map, slab predictor, residual and outward bounds, contact/collision/progress fields, resource caps and deterministic `UNKNOWN` behavior.
2. A separately written checker that imports no producer transition, residual, margin or aggregation helpers; it reconstructs cell coverage, source/query hashes, model coefficients, (L), ρ, Grönwall radii, same-ξ endpoint carry, full time coverage and every leaf/slab bound. Its complete expected record is compared with the saved record, not only a self-hash or status string.
3. Finite non-query fixtures covering a non-singleton parameter/state cell; slab carry under one fixed label; exact clip interiors, wholly saturated intervals and both corner crossings; a pose tube whose joint-distance bound is tighter than its axis rectangle; square-root reserve touching a corner; task integration; mutated coefficients/remainders; missing coverage; and deterministic resource-limit `UNKNOWN`.

**Falsifiable archived-data exit:** after those fixtures and source review pass, evaluate only the saved R17 records offline. Without changing their inputs, continue this candidate only if independent replay establishes full-hold nonnegative contact and collision margins and the frozen progress threshold for at least one saved action. Otherwise stop the method and report the exact remaining enclosure loss. Passing this method-development check would still be consumed evidence, not a fresh voltage-selection result or execution GO.

**Prospective challenge protocol (design only; no execution).** Before method outputs are examined, an outcome-blind task/benchmark source must supply a new initial cell, joint parameter domain, scene/obstacle, horizon T, progress threshold and exact action set. Register those values, the source closure, fresh evaluation identities and the truth table before running the producer. Evaluate each declared action on the same initial/parameter cells, scene, horizon and task; voltage is the only changed query field within a matched pair. The strong selection outcome is a fully replayed, safety-certified, task-eligible candidate action while the nominal action is also safety-certified but task-ineligible. If either side is `UNKNOWN`, report the comparison as inconclusive, not as evidence of collision/contact failure. Do not reuse R17 indices 62/74 as fresh evidence, choose thresholds after results, or let such a pair trigger the separate 800-row study. Any future evaluation requires its own exact-scope GO; the 800-row study remains `NOT_RUN`.

## Status ledger

| Claim | Status | Reason |
|---|---|---|
| R17 binding/source hashes and preservation | **VALID** | The diagnostic verified pinned R17 artifacts and R10 inputs; this R19 work changed no R17 record or G4 source/manifest. |
| R19 nested box arithmetic for saved candidates | **VALID as development arithmetic** | Exact rational interval operations; nesting and final postfixed inclusion checked for every stored slab. The displayed slip decimals are outward enclosures. |
| Extension of R10 whole-hold theorem to the final boxes | **VALID conditionally** | Same interval RHS, fixed full parameter image, held voltage, whole-slab inclusion and carry; requires the uniform Lipschitz/model assumptions and an independent source-bound R19 replay before certificate use. |
| Use of the R19 prototype output as an independent certificate or fresh-row authorization | **BLOCKER** | The script imports the R10 producer's RHS/projection helpers, persists no certificate record and has no independent checker. It cannot authorize or establish a new-row result. |
| Improved row 74/slab 0 collision bound and improved progress bounds | **VALID as saved-input diagnostics** | Exact source-bound outward bounds show the changes; the two total task tests still fail and the full-hold collision conjunction still fails. |
| Full-hold contact, collision safety, or actual violation on either consumed row | **UNVERIFIED** | No complete nonnegative sufficient margin; `UNKNOWN` is not an unsafe-trajectory witness. |
| Nested box contraction sufficient by itself for both target margins | **NEEDS REVISION / STOP as stand-alone method** | Every contact reserve remains zero; row 62 and row 74/slab 1 collision margins remain negative. |
| Shared-variable Taylor residual enclosure | **NEEDS REVISION** | Sound conditional inclusion argument specified; producer, outward residual arithmetic, independent checker and fixtures do not yet exist. |
| Prototype's documented file-path invocation | **NEEDS REVISION** | Direct file invocation fails to import `validation`; running it as a module from the repository root succeeds. |
| Fresh voltage-selection usefulness, physical correspondence, G2/G3/G4 | **UNVERIFIED** | Consumed development pair and synthetic Cases A/B/C do not establish these claims. |
| R5 800-row study | **NOT_RUN** | No authorization or execution follows from this work. |

## Artifact references

- Assignment: `docs/CODEX_TO_LUNA_G2_R19_STRUCTURE_PRESERVING_ENCLOSURE_RESEARCH.md`.
- R18 accepted diagnosis: `docs/reviews/LUNA_TO_CODEX_G2_R18_TWO_ROW_ENCLOSURE_DIAGNOSIS.md`; Codex review: `docs/reviews/CODEX_G2_R18_TWO_ROW_ENCLOSURE_DIAGNOSIS_REVIEW.md`.
- Whole-hold Picard proof contract: `research/benchmarks/G2_R10_WHOLE_HOLD_PICARD_CONTRACT_v1.md`; implementation: `validation/g2/time_slab_picard_r10.py`; independent R11 checker: `validation/g2/whole_hold_picard_checker_r11.py`.
- Analytic candidate and scoped acceptance: `research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md`, `research/theorem_notes/G2_R3_SCOPED_ACCEPTANCE_CANDIDATE_v1.md`; finite synthetic cases: `G2_FINITE_CERTIFICATE_CASE_A_v1.md`, `G2_CHALLENGE_CASE_B_v1.md`, `G2_VOLTAGE_SELECTION_CASE_C_v1.md`.
- Source-bound R17 manifest, GO, closure, receipt and records are listed in the evidence-identity table above. Their bytes and G4 artifacts were left unchanged.

**Final decision:** pursue the shared-variable Taylor-model/residual-tube research candidate as an offline mathematical method; retain the R19 box contractor only as a preconditioner; do not claim a full-hold certificate, voltage-selection value, G2 progress, physical safety, or 800-row readiness from this work.
