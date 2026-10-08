Session: DDWMR | LUNA-G2-SCOPE

# G2 R9 enclosure bottleneck research handoff

**Date:** 2026-10-03  
**Assignment:** `docs/CODEX_TO_LUNA_G2_R9_ENCLOSURE_BOTTLENECK_RESEARCH.md`  
**Disposition:** analysis and a versioned Picard-slab proof-contract candidate are complete; four synthetic non-query fixtures pass. The candidate has **not** been applied to either R6 row because no slab boxes for those rows have yet passed the required self-inclusion inequalities.
**Native query calls this assignment:** 0.  
**R6 / study status:** the two R6 `UNKNOWN` records remain unchanged and consumed; R5 remains 800/800 `NOT_RUN`.

## 1. Inputs reviewed and integrity

Read `AGENTS.md`, all four canonical `research_context` files, the R8 Codex result review, the R8 execution handoff, R6 protocol v2, and the pinned R3 evaluator/source closure. The R8 review accepts the two stored results as replayable `UNKNOWN`, records the usefulness trigger as false, and says no new query or 800-row study should follow from those outcomes alone.

The R3 v6 source closure is raw SHA-256 `b6b5c8b91fdc7c7dbc3c3b02fefb719f5aeeeaf9576ddf7cbbd584c9864b3469`; all **70/70** listed inputs were rehashed with zero missing files or mismatches. The R6 source closure is raw SHA-256 `df8622ce0515c84846d1504cbd6304807ccac82ce1c69526a3fe9aedac06809a`; all **95/95** inputs and all 13 published stage artifacts were rehashed with zero mismatches. The R6 publication raw SHA-256 remains `3e55c3b967b661f3a3c3b5aa70ae4bc7cf8e9bab463ec484a4e5865f3db5b33d`.

The R6 rows remain bound to input semantic hashes `422afd0448a184f4f67262c6338593c871739b41fb677e8ab1d6b566d18b93ac` (R5 index 12, `(0,0)`) and `70301bc5df76aab2dfdb8bef5135592fbf0063af6799b0f0eb119f4873b2cf9a` (index 24, `(+1,+1)`). Their canonical query raw hashes are `d5648569b11c576c8cc0ecb07c5096c21b06fe3a5e849358f254770649465471` and `105a0710185446312933ec8c92922acd1db0f3af0e999d67207ccd70534b4808`. R6 evaluation hashes remain `8d8f48d4c8bd3c6840d09ed32579e3796f81499e58b7a8ed60fba3b825487306` and `d93419ed11d68082c1f6676468326e88e66913d871c8edf1e37f003076686ece`.

No R3, R5, R6, or G4/Auer source or result was changed. No branch switch, commit, or push occurred. The only executed computation was the R9 synthetic fixture script; it does not import or invoke the R3 evaluator, `run_query`, or a study/producer runner.

## 2. Exact R6 bottleneck data

The exact rational records and their R3/R2 replays are in the immutable R6 evaluation files listed above. Decimal values below are readable renderings of those rational fields, not floating-point re-evaluations used to decide status.

### Collision decomposition

For both rows the configured obstacle is centered at (p_o=(4/25,0)=(0.16,0)), with inflated exclusion radius (R_s=3/50=0.06) m. R3 forms one full-hold rectangular center-pose hull, calculates a directed lower bound on its minimum distance to (p_o), then subtracts (R_s) and the pose error (E_p):

\[
m_{\rm coll}^{-}=d_{\rm center}^{-}-R_s-E_p.
\]

| Voltage | Center-hull gap to obstacle | Directed distance lower bound | (d^- - R_s), before pose error | (E_p) | Final R3 lower margin |
|---|---:|---:|---:|---:|---:|
| `(0,0)` | 0.030593338663 m | (513271/16777216\approx0.030593335629) m | (-0.029406664371) m | 0.401316031 m | (-0.430722695226) m |
| `(+1,+1)` | 0.018064002003 m | (303063/16777216\approx0.018063962460) m | (-0.041936037540) m | 0.472821261 m | (-0.514757298248) m |

At directed dyadic precision 24, each coordinate gap is rounded down/up and the serialized bound reports coordinate-rounding allowance (2/2^{24}=1/2^{23}\approx1.192092896\cdot10^{-7}) m. The exact center gap minus the reported lower distance is about (3.03\cdot10^{-9}) m for `(0,0)` and (3.95\cdot10^{-8}) m for `(+1,+1)`; the lower/upper root brackets are also recorded. These rounding terms are tiny beside the geometric deficit and pose error.

The pose error formula is

\[
E_p=T\left(\eta_u+U\min(T\eta_r,2)\right),
\]

where (U=\sup|u_{P_1}|), and (T=1/4) s. Its contributions are:

| Voltage | (T\eta_u) | (T U T\eta_r) | Sum (E_p) |
|---|---:|---:|---:|
| `(0,0)` | 0.355648406 m | 0.045667624 m | 0.401316031 m |
| `(+1,+1)` | 0.414415236 m | 0.058406025 m | 0.472821261 m |

**Why changing only (E_p) cannot certify either locked row:** even setting (E_p=0) and removing distance-rounding loss leaves (d_{\rm center}-R_s<0) in both rows by about 2.94 cm and 4.19 cm. The whole-hold center hull itself reaches within the obstacle exclusion radius. A refinement must localize/reduce that center hull (or alter the input domain under a separately declared protocol); shrinking only the error-radius term cannot flip this sufficient test. This says the current *outer hull test* fails. It does not establish that the true trajectory enters the obstacle.

### Contact reserve and body demand

For each wheel R3 computes an upper clipped-slip level

\[
\beta_j=\min\!\left(1,\ b_{\phi,j}+
\frac{\sum_i|S_{ji}|\eta_i}{\underline v_s}\right),
\qquad
A^- = \sum_j\underline C_j\sqrt{1-\beta_j^2},
\]

and subtracts the upper body demand (D^+=\overline m\,U_{\rm full}R_{\rm full}), where (U_{\rm full}=U+\eta_u) and (R_{\rm full}=R+\eta_r). The clipped-slip center term alone and its uncertainty-radius term are:

| Voltage | Left (b_\phi) | Left radius contribution | Right (b_\phi) | Right radius contribution | ((\beta_L,\beta_R)) | (A^-) | (D^+) | Contact lower margin |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| `(0,0)` | 0.926546 | 3.644328 | 0.908462 | 3.642572 | `(1,1)` | 0 N | 3.268571 N | (-3.268571) N |
| `(+1,+1)` | 1.000000 | 4.246366 | 1.000000 | 4.244610 | `(1,1)` | 0 N | 4.345043 N | (-4.345043) N |

Here (1/\underline v_s=1) for this parameter image. Thus both reserves collapse to zero because the certified whole-hold slip upper bound clips at one. For `(0,0)`, even though each predictor-only (b_\phi<1), the radius term drives both β values to one. For `(+1,+1)`, the left/right predictor clip already reaches one before the radius is added. The demand uses the same large full-hold body radii as the comparison enclosure.

The certified force reserve is parameter dependent: `C_j` is lower-bounded over the fixed 12-label parameter image; (v_s,R_w,b,m) and the slip matrix are also images of that joint label set. R3 evaluates interval coefficient hulls. They enclose every declared fixed label, but interval products forget some rational-map and state/parameter correlations. This is conservative outer relaxation; neither the interval label hull nor a negative margin describes a parameter resampled along the physical trajectory.

### Source of the wide radii and R2 progress bounds

The pinned profile uses one full-hold time slab, one parameter leaf, one initial-state leaf, predictor depth 1, and comparison series order 16. It computes a full-interval matrix exponential, two Picard predictor levels (P_0,P_1), residual force bounds, and a componentwise absolute comparison radius over all of (T=1/4) s. For both rows the majorant has

\[
\|N\|_\infty=28/5=5.6,\qquad Q=T\|N\|_\infty=1.4.
\]

The body components of the comparison forcing are approximately 3.021135 (zero voltage) and 3.520343 (positive voltage); their first (Tq) terms are about 0.755284 and 0.880086. The resulting uniform radii are 1.422594 m/s in both (u,r) components for `(0,0)`, and 1.657661 m/s for `(+1,+1)`. The comparison-series tail is only (3.24\cdot10^{-13}) and (3.77\cdot10^{-13}), respectively. Therefore the recorded radii are driven by the one-slab componentwise comparison forcing and its (N)-growth series, rather than a large Taylor tail or exhausted resource cap. The run counters were within the exact-arithmetic caps.

| Voltage | (P_1) range for (u) | (P_1) range for (r) | ((\eta_u,\eta_r)) | R2 full-hold (u) interval | R2 θ interval | R2 cosine lower | R2 progress lower |
|---|---|---|---|---|---|---:|---:|
| `(0,0)` | ([-0.086170,0.513627]) | ([-0.265526,0.246523]) | `(1.422594,1.422594)` | ([-1.508764,1.936220]) | ([-0.432030,0.427279]) | 0.906675 | (-0.377191) m |
| `(+1,+1)` | ([-0.101656,0.563744]) | ([-0.298328,0.279325]) | `(1.657661,1.657661)` | ([-1.759317,2.221405]) | ([-0.498997,0.494246]) | 0.875501 | (-0.439829) m |

R2 uses the global integral identity (p_x(T)-p_x(0)=\int_0^T u\cos\theta\,dt), but combines the full-hold (u)-tube with a global cosine interval. Since the (u)-tube contains both signs and the cosine upper endpoint is one, the integrand lower is exactly its negative-side (u) lower (approximately (-1.508764) or (-1.759317) m/s), yielding the negative progress lower shown. That is a weak sufficient bound; it does not show the actual robot makes negative progress. `task_eligible=false` remains correct because R3 safety is `UNKNOWN` and the progress lower is below 0.05 m.

## 3. Refinement candidate and inclusion argument

The candidate is a rational **time-slab Picard enclosure with time-local pose/contact tests**. The objective is to replace one full-hold box with a sequence of verified local boxes, not to assert a smaller radius by tuning.

Write (z=(u,r,\omega_L,\omega_R,i_L,i_R)) and (\dot z=f(z,V;\vartheta)). Fix one declared parameter-label value (\vartheta\in\Theta) for the whole execution and keep the same exact voltage (V) on every slab. On slab (k), let the already-enclosing start box be (X_k), choose a rational candidate box (B_k\supseteq X_k), and compute a rational interval vector (G_k) satisfying

\[
f(z,V;\vartheta)\in G_k
\quad\forall z\in B_k,\ \forall\vartheta\in\Theta.
\]

Require the explicit, machine-checkable Picard inclusion

\[
\boxed{X_k+[0,h_k]G_k\ \subseteq\ B_k.}
\tag{R9-P}
\]

For any fixed (\vartheta), the vector field is locally Lipschitz in (z) because the declared clip law is globally Lipschitz and all parameter denominators have positive lower bounds. Suppose a solution starting in (X_k) first exits (B_k) at time (t^*\le h_k). Up to that first exit its derivative lies in (G_k), so coordinatewise integration gives (z(t^*)\in X_k+[0,t^*]G_k\subseteq X_k+[0,h_k]G_k\subseteq B_k), contradicting a first exit. Therefore the entire closed slab lies in (B_k), and integration also gives the endpoint inclusion

\[
z(t_k+h_k)\in X_k+h_kG_k=:X_{k+1}.
\]

This is the proof obligation at each step. The exact-rational helper computes `G_k`, the all-time image and endpoint image, and returns `PICARD_INCLUSION_PASS` only after checking both (X_k\subseteq B_k) and (R9-P). Failed inclusion is an abstention, never a certificate.

For pose, with physical body slices of (B_k), form

\[
\Theta_k=\Theta_{k,0}+[0,h_k]R_k,\quad
P_{x,k}=P_{x,k,0}+[0,h_k](U_k\cos\Theta_k),\quad
P_{y,k}=P_{y,k,0}+[0,h_k](U_k\sin\Theta_k).
\]

Validated rational sine/cosine ranges are used. The pose box covers every time in that slab; test its distance to the obstacle box/circle and subtract (R_s). For contact, compute each slab's slip interval, β upper, lateral reserve lower (\sum_j\underline C_j\sqrt{1-\beta_{j,k}^2}), and demand upper (\overline m\sup_{B_k}|u|\sup_{B_k}|r|). Require both collision and contact margins to be nonnegative on **every** slab. A progress lower can be accumulated as

\[
J^- = \sum_k h_k\inf(U_k\cos\Theta_k),
\]

which follows by additivity of the same integral used in R2. It must be compared with the unchanged (1/20) m threshold, and task eligibility still requires a complete safety certificate.

**Parameter and action semantics.** Each θ remains one execution-fixed joint label in Θ for every slab. The same `ModelIntervals` label image is used throughout; no slab receives a new draw or a different voltage. The componentwise interval extension may forget correlations among rational parameter maps and between state and labels, which only enlarges (G_k,B_k). If a future implementation splits Θ, partition the label set once before propagation, assign stable leaf IDs, and carry each leaf unchanged through all slabs; do not independently repartition/resample at each step. Keep a single shared held (V) for all labels and initial states.

### Source-to-theorem map

| Claim / obligation | R9 artifact | Mathematical meaning and limit |
|---|---|---|
| Exact interval RHS (G_k\supseteq f(B_k,V;\Theta)) | `validation/g2/time_slab_picard_r9.py:interval_rhs` | Uses the source-bound R3 `ModelIntervals`, exact `Fraction` interval primitives, clip hull, and fixed model image. It is an outer extension; coefficient correlation can be lost. |
| All-time and endpoint interval images | `time_slab_picard_r9.py:_time_sweep` | Computes (X+[0,h]G) and (X+hG) with exact rational interval products. |
| Slab theorem acceptance | `time_slab_picard_r9.py:verify_internal_slab` | Checks start containment and R9-P. It does not silently certify a failed candidate box. |
| Proof-to-model binding | `time_slab_picard_r9.py:model_image_sha256` and `verify_pose_contact_slab` | A canonical SHA-256 binds the proof to exact parameter intervals, matrices `A/B/D/S/QF`, state scales, label order and label box. Pose/contact rejects a successful Picard record made from a different model image. |
| Time-local pose, collision, contact and progress primitives | `time_slab_picard_r9.py:verify_pose_contact_slab` | Requires a successful internal slab proof for the same model image, candidate box and duration; applies the tube over the entire slab. This helper does not yet aggregate a full-hold sequence. The caller must bind `pose_initial` to an outer enclosure of that execution's slab-start pose. |
| Finite behavior fixtures | `validation/scripts/verify_g2_r9_picard_fixtures.py` and `validation/configs/g2_r9_picard_fixtures_v1.json` | Four synthetic cases: pass, fail-closed, local pose/contact/progress margins, and rejection of a proof/model mismatch. Zero native calls. |
| Existing plant/evaluator assumptions | R3 v6 closure and MASTER v2.1 | Same nine-state reduced plant, clip force law, fixed hidden parameter set, exact sampled state and common held voltage; no plant amendment. |

## 4. Application boundary / missing inequalities

The inclusion argument for the **conditional slab theorem** is complete, and the code implements its rational proof contract. The exact R6 rows have **not** been assigned candidate (B_k) boxes or endpoint carry boxes under this method. Consequently there is no checked value of (X_k+[0,h_k]G_k\subseteq B_k) for those inputs and no R9 collision/contact/progress margin for either row. That is the exact missing inequality, not an assertion that it cannot be satisfied.

The current candidate is therefore a reviewable proof primitive plus design, **not** a replacement R3 native producer, whole-hold checker, R6 replay, or safety result. A production R9 implementation still needs (i) a deterministic rational candidate-box construction/refinement rule with bounded work, (ii) a carried chain (X_{k+1}=X_k+h_kG_k\subseteq B_{k+1}) whose first `X_0` encloses the declared initial state and whose pose start box encloses the declared initial pose, (iii) full-hold aggregation and source-bound serialization/checker that enforces one common held voltage and one unchanged joint label domain, and (iv) demonstrated R9-P on each slab before its safety/contact values can be trusted. If a slab fails R9-P, split that slab deterministically under a predeclared budget; if it still fails, return `UNKNOWN` without changing the input or retrying a native call. The current helper checks the model fingerprint, `B_k`, and duration; a production input binder must additionally verify the caller-supplied pose start and carry box against the exact input/preceding slab.

No claim is made that the R9 refinement certifies either prior action. The two negative R6 margins remain sufficient-bound failures, not evidence of actual collision/contact violation. The R6 outcomes and R5 800-row manifest remain byte-for-byte unchanged.

## 5. Fixture result and source closure

Ran only:

```text
C:\msys64\ucrt64\bin\python.exe validation/scripts/verify_g2_r9_picard_fixtures.py
```

Result: `PASS_SYNTHETIC_NONQUERY_FIXTURES`; 4 fixtures; 2,245 exact rational operations; `native_query_calls=0`. The passing constant-field case produced the exact all-time (u\)-tube `[0,1/4]` and endpoint `[1/4,1/4]`. An undersized candidate returned `PICARD_INCLUSION_FAIL`. The separate local pose fixture had positive collision, contact and progress lower bounds, and a proof generated from a model with changed mass was rejected by the pose/contact helper. These are arithmetic/branch checks on synthetic models, not plant validation or evidence about R6 trajectories.

Versioned source closure: `research/benchmarks/G2_R9_SLAB_PICARD_SOURCE_CLOSURE_v1.json` (149 direct inputs; raw SHA-256 `2bcb15b82158d01684b8ec043b7279b41e6e95952c6238fb24d2a54f76ec10fa`; semantic SHA-256 `fb8d9c86c1d72dab8747d357613b4b996981fe3d83d9426f2884e0b4d15d9be6`). Its sidecar is `G2_R9_SLAB_PICARD_SOURCE_CLOSURE_v1.json.sha256`. The closure includes all 70 R3 v6 inputs, all 95 R6 source-closure inputs, all 13 immutable R6 publication artifacts, the assignment/reviews/context, and the new R9 module and fixture files. A full rehash returned 149/149 match, zero missing, zero mismatches.

New file hashes:

| File | SHA-256 |
|---|---|
| `validation/g2/time_slab_picard_r9.py` | `0a9620ff30e663b0548615fc61ff05648d7a5d12ffb335153d7b5da41f2d8ce5` |
| `validation/configs/g2_r9_picard_fixtures_v1.json` | `4001f673a4ad698be9f68528d05bfd8c10fee24ff2fed53977aff6b5549f1386` |
| `validation/scripts/verify_g2_r9_picard_fixtures.py` | `3f27ee937614703cd2d74d3ae3f62d2590151e6087a37c25cd5a2e148d8b50e1` |
| `research/benchmarks/G2_R9_SLAB_PICARD_SOURCE_CLOSURE_v1.json` | `2bcb15b82158d01684b8ec043b7279b41e6e95952c6238fb24d2a54f76ec10fa` |

The closure currently excludes this report to avoid circular provenance. All additions are versioned R9 files. No other source was edited.

## 6. Minimal future query stage proposal — not authorized

Do not issue a query receipt from this handoff alone. After Codex accepts the proof contract and a complete R9 slab runner/checker is implemented and source-closed, the smallest action-discrimination pilot is the same matched pair of two exact R6 logical inputs, re-evaluated **once each under a new source/stage identity**:

| Order | Existing input | Query canonical raw SHA-256 | Input semantic SHA-256 | Role |
|---:|---|---|---|---|
| 0 | R5 index 12, `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_L0_R0`, (V=(0,0)) | `d5648569b11c576c8cc0ecb07c5096c21b06fe3a5e849358f254770649465471` | `422afd0448a184f4f67262c6338593c871739b41fb677e8ab1d6b566d18b93ac` | nominal comparator |
| 1 | R5 index 24, `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lp1_Rp1`, (V=(+1,+1)) | `105a0710185446312933ec8c92922acd1db0f3af0e999d67207ccd70534b4808` | `70301bc5df76aab2dfdb8bef5135592fbf0063af6799b0f0eb119f4873b2cf9a` | positive-action comparator |

The exact reviewed base identities for that proposed pair are R3 v6 closure `b6b5c8b91fdc7c7dbc3c3b02fefb719f5aeeeaf9576ddf7cbbd584c9864b3469`, R6 stage closure `df8622ce0515c84846d1504cbd6304807ccac82ce1c69526a3fe9aedac06809a`, R6 config `df9fd6647aca54932137a8cc589e588d95f6911a07ef1b70d38f9aa005282d58`, R6 manifest `9d9e9ba3f5448d985de4da5298155f9f5fdd3e191039c627370f1f48fd085cfa`, and fixed parameter image semantic hash `c653a4f0f0b76e5d36fffa6e0cab822eac3c949955a2348e98ae9cdf597fe6be`. The new R9 proof-helper closure is `2c3ed5244a0c4677c213e65c5187a08d60eced55e1029977ebeb5a156e6d61b1`; it is not yet a runnable native-stage closure.

**Prospective discriminating outcomes:** each returned row must include a complete list of slab (B_k,G_k), pass R9-P in every slab, nonnegative collision and contact lower margins throughout the hold, and a replayed R2-style terminal progress lower bound. The predeclared broader-study trigger remains the existing strict contrast: `(+, +)` must be safety-certified and task-eligible with lower progress at least (1/20) m, while `(0,0)` lacks that combined result. These are prospective conditions, not expected numerical results and not a prediction that either row will certify.

**Stop rules for any separately authorized stage:** stop on source/input/receipt mismatch, any slab inclusion failure after the predeclared split budget, invalid arithmetic/proof replay, timeout/resource limit, malformed/partial record, incomplete publication, or exhausted one-shot intent; do not retry or replace. If both rows remain `UNKNOWN`, the positive row loses collision/contact certification, or it fails the (1/20) m task threshold, the usefulness trigger is false and no larger study follows from this pair. Keep both rows tagged as development overlap selected after R5 `UNKNOWN`, never independent confirmation; do not alter the R5 denominator or its thresholds. A later R5 study requires its own Codex review and separate authorization.

## 7. Final status

The two bottlenecks have been decomposed from exact stored records. A sound conditional time-slab inclusion rule and exact-rational proof-contract implementation are prepared with finite synthetic fixtures and a 149-input source closure. The exact R6 application remains unestablished pending actual (B_k) self-inclusion proofs and full-hold aggregation. R6 stays two consumed `UNKNOWN`; R5 stays 800/800 `NOT_RUN`; G2 remains `UNVERIFIED`; overall research status remains `HOLD`.
