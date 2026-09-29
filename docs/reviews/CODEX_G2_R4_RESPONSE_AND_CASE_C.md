# G2 R4 response — accepted Case B and pending voltage-selection Case C

2026-09-29. Response to the GPT review of `1da2166949ad12a0741c876c3a0daf8a5d957ddf` relayed by the user. **MASTER v2.1; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED; HOLD.**

## 1. Record the independent Case B acceptance

### Finding

Case B is recorded as accepted finite synthetic evidence, including the saturation-exit assertion and only the three locked sufficient-evaluation outputs.

### Evidence

[The review record](GPT_G2_R3_1da2166_ACCEPT_RECORD.md) identifies the reviewed commit and each accepted equation group. It is explicitly a summary of the user's pasted review, not a verbatim archive. MASTER, DECISION_LOG, REVIEW_GATE and Case B status prose now reflect the acceptance; displayed plant, G2, Case A and Case B equations are preserved.

### Consequence

Multiple finite hand cases now exist. This does not establish a general evaluator, practical value, voltage necessity, method superiority or a gate pass.

### Status

**VALID / ACCEPT for Case B**, per the independent GPT review.

### Required action

Retain the exact scope and UNKNOWN terminology. The all-upper-corner matrix shortcut remains prohibited; B.15's explicit majorant is retained.

## 2. Same-state voltage-selection challenge

### Finding

[Case C](../../research/theorem_notes/G2_VOLTAGE_SELECTION_CASE_C_v1.md) compares V=(1/4,1/4), V=(1,1) and V=(0,0), all under one fixed state, parameter family, horizon, obstacle and certificate rule.

### Evidence

C.1 declares a synthetic matched-side parameter image: common hidden rho and C, reflected J=L=1/rho in normalized units. C.2 starts at exact rest. These restrictions justify equal-side symmetry without imposing symmetry on the general MASTER uncertainty. The voltage is chosen before the hidden realization and held for 0.1 s.

### Consequence

This is a minimal decision example. It does not inherit Case B's independent side uncertainty or saturation crossing. The zero action is included and certifies, so no need to move forward or tracking benefit is claimed.

### Status

**UNVERIFIED** pending independent GPT review of the new derivation.

### Required action

Check the family, auxiliary symmetry and whether this scoped example meets the requested first voltage-selection distinction. Do not infer practical usefulness from exact rest.

## 3. Isolate voltage-dependent centers with a shared error bound

### Finding

The proposed output distinction is attributable to the voltage-dependent center; all candidates share the same conservative error budget and evaluation formula.

### Evidence

C.3--C.6 derive p^1=(aP,0), with (3/50)t^4<=P(t)<=t^4/9, from voltage through current, wheel speed, slip, contact force and body velocity. C.7--C.11 supply one common e_z=(18/25)t^4 and pose radius 3/2000000 m. C.13 uses the same parameter/time center segment [0,aT^4/9] and distance rule for all candidates. No alternative action receives an easier radius or higher refinement depth.

### Consequence

If accepted, this is a quantitative voltage effect within the selected data and an action-dependent output from one locked sufficient certificate. It is not a general lower-authority theorem for the abstract contact class.

### Status

**UNVERIFIED** pending independent review.

### Required action

Audit the residual using exact predictor Delta r=0, then verify that the error box and pose lift remain the generic six-state construction. All-time certification must not rely on trajectory samples or treating an entire error box as symmetric.

## 4. Exact proposed decisions and limitations

### Finding

The candidate finite evaluation certifies the smaller nonzero forward voltage and zero; it returns UNKNOWN for the larger forward voltage.

### Evidence

The common obstacle clearance is 8 micrometers. Evaluated lower margins in meters are:

| Voltage | Collision lower bound | Locked output |
|---|---:|---|
| (0,0) | 13/2000000 | CERTIFIED |
| (1/4,1/4) | 67/18000000 | CERTIFIED |
| (1,1) | -83/18000000 | UNKNOWN |

Contact lower margin exceeds 1999/1000 N for every candidate under the full generic tube. These are derived sufficient bounds, not empirical minima. The obstacle was intentionally placed near the bounds, and the micrometer scale is synthetic.

### Consequence

The negative lower bound does not prove collision, physical necessity of the smaller voltage or failure of other methods. Neither superiority over a properly validated n=0 construction nor a general voltage-selection algorithm has been shown. No repeated safety or G3 result follows.

### Status

**UNVERIFIED** pending arithmetic review; practical usefulness remains UNVERIFIED even if this case is accepted.

### Required action

Assess the exact certificate-output distinction. Identify the stronger remaining operating-domain requirement rather than extrapolating to practical superiority.

## 5. Practical and novelty gaps remain explicit

### Finding

This iteration supplies no realistic benchmark, general numerical evaluator, runtime result or new prior-art exclusion.

### Evidence

The case has exact rest, matched sides, a nonstiff correlated family, locally unsaturated contact, generous contact slack and an engineered obstacle. The existing prior-art supplement remains applicable. All work is analytic documentation; no solver, simulator, controller, experiment or recursive set is supplied.

### Consequence

Moving/turning states, defensible parameter data, useful margins and a matched generic-method comparison remain necessary before a practical or originality claim. Accumulating accepted synthetic cases alone will not satisfy these obligations.

### Status

**UNVERIFIED** for practical usefulness, general certification, tractability and overall novelty. **BLOCKER** for standalone generic-method novelty.

### Required action

Keep HOLD and the implementation boundary. After reviewing C, specify the next evidence requirement around useful operating conditions and fair comparison; do not authorize implementation implicitly.

## Summary table

| Item | Analytic soundness | Finite certification | Usefulness | Novelty | Gate effect |
|---|---|---|---|---|---|
| Case B | VALID per GPT | ACCEPT for exact case | UNVERIFIED practically | No new contribution | Evidence recorded only |
| C matched-side family/symmetry | Derived; review pending | Explicit rational image | Auxiliary restriction | Not claimed | None |
| C voltage-to-center response | Derived; review pending | Uniform rational envelopes | Scoped quantitative action effect | Not claimed | None |
| C shared tube/contact proof | Derived; review pending | Hand certificate submitted | Synthetic only | Generic machinery | None |
| C action outputs | Submitted for review | Same locked evaluation | Minimal voltage-output distinction; practical value UNVERIFIED | No superiority claim | G2 UNVERIFIED |
| General evaluator/runtime | Not implemented | UNVERIFIED | UNVERIFIED | UNVERIFIED | Implementation closed |
| G3 / physical transfer | Not established | Not established | UNVERIFIED | Not claimed | HOLD |
