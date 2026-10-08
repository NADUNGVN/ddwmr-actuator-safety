Session: DDWMR | LUNA-G2-SCOPE

# W2 G2 autonomous completion handoff

**Date:** 2026-10-07  
**Disposition:** `PARTIAL` — the frozen v6 producer/checker certifies a prospective voltage choice on the declared synthetic task. Release-scoped independent G4 review is still pending, so this is not a final G2 acceptance or gate PASS.

## Finding

The centered residual enclosure made a task-relevant distinction on one prospective, positive-width, moving-state synthetic domain. For a 2 s static-circle hold, zero and the predeclared nominal voltage both receive full-hold contact and collision certificates, but their progress upper bounds are below the task threshold. The alternative voltage receives the same safety certificates and its progress lower bound exceeds the threshold. Thus the frozen selector has a certified task action where the predeclared zero-only and nominal-only rules do not.

This establishes a certificate-level action-selection result for this one declared model task. It does not show that an UNKNOWN method is unsafe, that the alternative is physically necessary, that R3 is inferior, or that the synthetic constants describe a real platform. G2 remains `UNVERIFIED` pending independent release audit and matched confirmation.

## Frozen task and supported scope

The input is `research/autonomous_w2/g2/task_protocol_v1.json` (SHA-256 `8bc1c8fd460a62dc3f7ff1c8e4bef2dbaddbcaffbadd75d6c2c487e9e311c15a`). It was frozen before v6 row evaluation and preserves the task introduced for W2:

- Nine-state order: `(p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R)`. Every initial coordinate has positive width; the box is moving, with `u in [0.3,0.3001] m/s` and wheel rates in `[0.2499,0.25] rad/s`.
- Known law `phi(s)=clip(s,-1,1)`, `L_phi=1`; `m=I_z=R_w=b=v_s=c_u=c_r=V_max=1`.
- Twelve independent fixed labels in `[0.9999,1.0001]`, mapped as `J_j=1/rho_j` and `L_j=lambda_j`. A label vector is chosen once per trajectory and reused for the full hold.
- One common voltage pair is held for the entire `T=2 s`: zero `(0,0)`, nominal `(1/2,1/2)`, or alternative `(1,1)` V.
- Static circle center `(0.5,0.1) m`, inflated radius `0.06 m`. Task rule: displacement `p_x(T)-p_x(0) >= 0.35 m`, set before evaluator outputs as a 0.175 m/s mean-forward-progress requirement.
- Selector: keep nominal if it meets the task and full-hold predicates; otherwise use alternative if it meets them; otherwise no certified task action. The comparator rules are zero-only and nominal-only.

This is a formal synthetic design domain. The contact capacities are reduced-model parameters; they are not verified normal-load/friction products. The result says nothing about G3 recursive safety, closed-loop behavior, tire/support mechanics, or hardware.

## Candidate proof

For the allowed symmetric initial reference with every parameter label equal to one, equal held voltages preserve symmetry. While the reference is inside the clip-affine branch, its equations are

`u_c'=-3u_c+2w_c`, `w_c'=u_c-2w_c+i_c`, `i_c'=-w_c-i_c+V`, `p_xc'=u_c`.

The center path is enclosed on all 256 contiguous slabs of length `h=1/128 s`. Each partial Taylor enclosure covers every `tau in [0,h]`; its endpoint enclosure becomes the next slab's initial interval. No monotonicity shortcut is used for center position.

Let `z=(u,r,omega_L,omega_R,i_L,i_R)`, `y=(z,1)`, `A(theta,V)` be the six internal affine dynamics plus the affine voltage column for one fixed parameter vector, and `A_0(V)` its all-one reference matrix. The outward interval image gives `delta_A >= sup_theta ||A(theta,V)-A_0(V)||_infinity`; the row logarithmic-norm bounds enclose both `mu_inf(A(theta,V)[:6,:6])` and the augmented reference logarithmic norm. For `e=z-z_c`,

`e' = A(theta,V)[:6,:6] e + (A(theta,V)-A_0(V)) y_c`.

With `mu` the common outward upper bound, `||y_c(0)||_infinity=1`, and the complete initial internal box radius `e0=1/10000`, logarithmic-norm comparison gives for each fixed label and all `t in [0,T]`:

`||e(t)||_infinity <= exp(mu*t) * (e0 + t*delta_A)`.

The computed uniform radius is `E=ceil(exp(mu*T)*(e0+T*delta_A))`. Taking interval suprema over the fixed label image is conservative, but does not permit true labels to vary between slabs. Across the three voltages, the row values are `delta_A=0.00100005`, `mu_p=1.00100001`, `mu_0=1`, `mu=1.00100001`, `exp(mu*T)<=7.403849148`, and `E=0.015548823594`.

For each slip, its difference from the symmetric center is at most `3E`. The full-hold clip bound is `beta=beta_c+3E`, where `beta_c` is bounded over every center partial slab. If `beta<1`, a first-exit argument proves the true trajectory cannot reach `|sigma_j|=1`: until a proposed first hit the affine comparison applies, while the resulting tube remains strictly inside that hit set. If the strict inequality fails, v6 does not use the affine-branch certificate.

On the proved branch, `a_j=C_j*sqrt(1-sigma_j^2)`. For `q in [0,1]`, `sqrt(q)>=q`, so each wheel reserve is at least `C_min*(1-beta^2)`, with `C_min=9999/10000`. The reference has `r_c=0`, giving `|m*u*r| <= (U_c+E)E`, where `U_c` bounds the center speed over the hold. Therefore

`contact_margin_lower = 2*C_min*(1-beta^2) - (U_c+E)E`.

A nonnegative value proves the stipulated algebraic lateral-reaction feasibility condition `a_L+a_R >= |m*u*r|`. No derivative of the square-root reserve is used.

The heading bound is `theta_H=theta_0+T*E`. From `|1-cos(theta)|<=theta^2/2` and `|sin(theta)|<=|theta|`, the endpoint-progress error and position errors are bounded by

`E_J=T*E + T*U_c*theta_H^2/2`,  
`E_px=|p_x(0)|_max+E_J`,  
`E_py=|p_y(0)|_max+T*(U_c+E)*theta_H`.

The center reference has `p_yc=0`. Its full time `p_x` range is obtained from the contiguous partial slabs. The distance from obstacle center to the center path is bounded below by the distance to `[P_min,P_max] x {0}`. Subtracting `E_px+E_py` (an upper bound on Euclidean position deviation) and the inflated obstacle radius gives the collision-margin lower bound. The task displacement interval is `[p_xc(T)-E_J,p_xc(T)+E_J]`.

The detailed equation-to-code map is [PROOF_TO_CODE_MAP_v6.md](../../../../research/autonomous_w2/g2/PROOF_TO_CODE_MAP_v6.md); the preimplementation hypothesis is [HYPOTHESIS_CENTERED_RESIDUAL_TUBE_v1.md](../../../../research/autonomous_w2/g2/HYPOTHESIS_CENTERED_RESIDUAL_TUBE_v1.md).

## V6 action results

All three producer rows replayed successfully through the independent checker. Displayed decimals are rounded; exact rational values, full slab records, resource receipts and hashes are preserved in the row files and evidence inventory.

| Action | Safety | Progress enclosure (m) | Contact margin lower (N) | Collision margin lower (m) | Clip beta upper | Task eligible |
|---|---:|---:|---:|---:|---:|---:|
| Zero `(0,0)` | CERTIFIED | `[0.177602288, 0.240378241]` | `1.975592543` | `0.196669519` | `0.098241017` | No; upper below 0.35 |
| Nominal `(0.5,0.5)` | CERTIFIED | `[0.270778521, 0.333554474]` | `1.969295159` | `0.110629683` | `0.113138430` | No; upper below 0.35 |
| Alternative `(1,1)` | CERTIFIED | `[0.363954753, 0.426730706]` | `1.920548346` | `0.033710549` | `0.192811173` | Yes; lower exceeds 0.35 |

The alternative has the tightest collision margin but remains strictly positive. Its contact lower margin is also positive. The predeclared threshold falls between the nominal upper bound and alternative lower bound; it was not placed from a computed margin or action-gap bound.

## Implementation, replay, and mutation checks

The released producer is `validation.autonomous_w2.g2.producer_centered_v6`; the checker is `validation.autonomous_w2.g2.checker_centered_v6`. They do not import one another. The checker independently assembles the parameter matrix and center matrix, recomputes residual/log-norm/exponential bounds, reconstructs contact, clip, collision and progress fields, and checks fixed labels, fixed voltage, complete contiguous slab coverage and chained endpoints. Shared trusted arithmetic is disclosed: Python `Fraction` and `rational_interval_v3.I/Budget`; the producer reuses `producer_v4`'s outward interval matrix and Taylor primitive. The release source closure binds those dependencies.

All row arithmetic used a 96-bit dyadic outward grid, order-20 Taylor bounds, 256 slabs, a 5,000,000 interval-operation cap and 16,384 rational-bit cap. Each v6 row used 1,643,414 counted interval operations and at most 2,040 observed rational bits. Workers ran for 9.969–20.109 s; checker replays took 10.047–10.156 s. Peak worker/checker memory was about 14–15 MB, below the 1 GiB cap. The complete stage took 70.671 s, below the 2 h phase limit. Every worker and replay had a 60 s wall/CPU cap, 1 GiB memory cap, one-process limit, 8 MiB stdout cap and 1 MiB stderr cap.

Six synthetic, non-task fixtures passed, covering affine-column residuals, log-norm bounds, center-matrix signs and voltage, outward exponential/grid bounds, `sqrt(q)>=q`, and strict first-exit behavior. Pre-run gate v3 passed compilation, producer/checker synthetic matrix parity, positive-width domain, resource caps, clean compute lock, repository branch/HEAD and remaining-attempt checks. Pre-run receipt v1 failed only because the gate's raw UTF-8 `compile()` path did not strip the producer/checker BOM; `py_compile` had passed. The gate was corrected to read `utf-8-sig`; the failed receipt is preserved, and v2/v3 pass receipts are retained.

Five post-run mutations were rejected by v2 of the saved-record audit, each with an individual 60 s / 1 GiB Job Object limit: changed source bytes, changed protocol input, omitted final slab, changed center label, and inflated contact margin. Audit v1 is preserved as a harness failure: it misread the supervisor's flattened Job Object result and reported FAIL even though the checker stdout contained rejection records. V2 corrected the harness and reports all five rejected. No producer/query ran in either mutation audit; native attempts added were zero.

One non-mathematical receipt defect remains visible: the stage runner's per-attempt receipt object retains the `G2_W2_V6_ATTEMPT_INTENT_v1` schema label when written as `attempt_receipt.json`. The stage-level receipt, row schema and checker replay schema are correct and their hashes are present. This labeling issue does not affect any recomputed proof field, but should be corrected in a future versioned reporting runner; the frozen v6 release and its outputs were left unchanged.

## Attempt ledger and failed evidence

The W2 G2 cap is 24 native development attempts. The ledger is complete; fixtures and saved-record checker mutations are separate and add zero native attempts.

| Ordinals | Version | Count/status | Recorded reason or result |
|---|---|---:|---|
| 1–6 | v1 | 3 execution failures; 3 audit failures | First three stopped at Python's 4,300-digit integer-string limit. Next three produced rows but checker exited 3, so no valid replay was accepted. |
| 7–12 | v2 | 3 resource UNKNOWN; 3 replayed UNKNOWN | First three hit `RATIONAL_BIT_CAP`. Next three replayed, but contact and collision sufficient margins were negative. |
| 13–15 | v3 | 3 execution failures | All three workers returned `KeyError:'collision_margin_lower'`. |
| 16–18 | v4 | 3 replayed UNKNOWN | Clip interior was not established on every slab and contact margin was negative; nominal/alternative also had negative collision slabs. |
| 19–21 | v5 | 3 replayed UNKNOWN | Clip-interior proof failed and contact margin was negative on a slab for all three actions. |
| 22–24 | v6 | 3 replayed CERTIFIED | All three proved contact/collision/clip. Zero and nominal missed the progress threshold by their upper bounds; alternative met it by its lower bound. |

Totals: 6 execution failures, 3 checker/audit failures, 3 resource UNKNOWN, 9 proof-complete safety UNKNOWN, and 3 v6 replayed safety certificates. Task-eligible actions: one of three v6 actions. No retry was made after any frozen attempt.

No direct R3 run was added on the v6 task rows. With only three attempts left, evaluating all three v6 actions used the remaining W2 allowance; adding even one R3 matched row would exceed that cap. Earlier R3 artifacts are not the same initial-state/task inputs and are not a matched comparison. G4 owns any fresh matched confirmation. No held-out action outcome was evaluated by G2.

## Release, peer exchange, and reproduction

The release is [RELEASE_v6.json](../../../../coordination/autonomous_w2/g2/releases/RELEASE_v6.json), SHA-256 `789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55`. It binds the frozen protocol, 31 source/dependency files, proof map, profile, ordered IDs, plan and three bindings. The source map is in the release and [freeze receipt](../../../../results/validation/autonomous_w2/g2/development_centered_v6/freeze_receipt_v6.json), SHA-256 `d57bcec7cf992dae258bc65ebaf6ffba444ee0df5ebe00845df939d3f4ab87e8`; the plan SHA-256 is `c9d6abfd689a2f6db59dbaf7aeb7f4b86c0769739930ef5747c422b37996f5bb`.

G2 wrote [AUDIT_REQUEST_TO_G4_v6.md](../../../../coordination/autonomous_w2/g2/AUDIT_REQUEST_TO_G4_v6.md), SHA-256 `a61482e4bc07390f987b2bf495e6ddbd9c961c3b5996a2c6b60d2e9b132af088`, asking for an exact-hash audit decision in the G4-owned prefix. G4's files remain read-only. At the last observation, G4 `STATUS.json` was sequence 3 / `AWAITING_PEER_INPUT` and its audit state still said `NOT_ISSUED_NO_IMMUTABLE_G2_RELEASE`, bound to its earlier observation of G2 STATUS sequence 1. That stale decision is not a rejection of v6; it does not bind the v6 SHA. No G4 release consumption or confirmation rows are recorded.

Key evidence hashes:

- v6 stage receipt `9b906c008af8ff51f92bb55d4f1fe072f9a4ebdc48f4caf64c29feec58f0aa36`.
- Zero row / replay: `9aa7a3f86c8572be81349cc2ffb9a67d67e7bd4a67b37c95b2c7208548a1593a` / `6639ceaac7b87e063fdc6b5b91a686c3d56d7a04202efc6000c1d322630ac6fa`.
- Nominal row / replay: `f5ad26449b65a1ccae7af7f7029209e66fc2af656a7fe3956f91d55822420ca7` / `c53239caeedab91713ecbf41de7be71d7f8b1e66928d4554f4a819cf204cd171`.
- Alternative row / replay: `e69bf3594432cb33bd8285815c61fc5426d5fb2e57b38daf56d56f2798e70cb6` / `38ba67273d56c798347f37dae16b74e5a3751e52f3eebeb53d6291b3e7b6ad92`.
- Mutation audit v1 failed harness receipt: `d32fbb82434b6649329464590f2fc92d2ce82ed90de16e3376cdaa7494dbb81b`; corrected v2 pass receipt: `83039f92675e6d1ce2f52f1df40e67e8337dbeddaddc2124167bb84f2b736673`.
- Evidence inventory: [evidence_inventory_v1.json](../../../../results/validation/autonomous_w2/g2/development_centered_v6/evidence_inventory_v1.json), SHA-256 `5de4f15150a0df2a2ce52c6eff047a9e886895b1d14814eff40c0072e7f0933f`, with 139 file entries including saved failures, raw Job Object outputs, bindings, rows, replays, mutations and peer-state snapshots.
- Final G2 status is recorded in [STATUS.json](../../../../coordination/autonomous_w2/g2/STATUS.json), sequence 16, with immutable [STATUS_W2_SEQUENCE_16.json](../../../../coordination/autonomous_w2/g2/STATUS_W2_SEQUENCE_16.json). The atomic updater is `validation/autonomous_w2/g2/update_status_centered_v6.py`. The inventory predates the final status and handoff files; both are separately bound by sequence 16.

From repository root, the stage and saved-evidence reproduction commands are:

```powershell
python -m validation.autonomous_w2.g2.centered_v6_nonquery_fixtures
python -m validation.autonomous_w2.g2.pre_run_validation_centered_v6
python -m validation.autonomous_w2.g2.freeze_development_centered_v6
python -m validation.autonomous_w2.g2.publish_release_centered_v6
python -m validation.autonomous_w2.g2.run_stage_centered_v6 --plan research/autonomous_w2/g2/development_plan_centered_v6.json
python -m validation.autonomous_w2.g2.audit_mutations_centered_v6_v2
```

The first four commands create one-time frozen outputs and will refuse to overwrite them. Do not rerun the stage: all 24 W2 G2 development attempts have been consumed. Each saved row can be independently replayed with the checker, for example:

```powershell
python -m validation.autonomous_w2.g2.checker_centered_v6 --binding research/autonomous_w2/g2/bindings_centered_v6/attempt_03.json --record results/validation/autonomous_w2/g2/development_centered_v6/attempt_03_W2_G2_DEV_001_ALTERNATIVE/row.json
```

## Limitations and next decision

The result is one synthetic one-hold task, one symmetric voltage family, one known clip law and a narrow positive-width parameter image. The alternative has a smaller positive collision margin than zero or nominal. The generic centered validated-flow technique and fixed-label comparison are not claimed as novel; G4 must decide overlap and comparison value. No physical provenance, model-error bound, recursive safety, hardware experiment, R3 matched baseline, or held-out confirmation was produced. The old R5 study remains `800/800 NOT_RUN`.

**Concrete next decision:** G4 should publish `ACCEPT_FOR_SCOPED_VALIDATION` or exact defects, explicitly bound to release SHA `789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55`. If accepted, G4 owns a prospectively frozen matched confirmation under its W2 cap; if rejected, no additional G2 native attempt is available in this cycle.

Overall disposition remains `HOLD`. Gate statuses are unchanged: G1 restricted reduced-model scope `PASS`; G2, G3, G4 and physical-platform correspondence `UNVERIFIED`.
