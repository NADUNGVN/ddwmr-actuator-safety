# G2 R3 scoped acceptance candidate v1

**Date:** 2026-10-02  
**Disposition sought:** independent review of one frozen synthetic finite-evaluation scope.  
**Canonical status:** HOLD; G1 PASS for restricted reduced-model consistency; G2/G3/G4 and physical-platform correspondence UNVERIFIED.

## Finding — supported theorem/code/result scope

R3 supports a bounded **recorded computational result** for the frozen `G2-COMP-clip` fallback profile and the exact synthetic benchmark below. For a record labeled `CERTIFIED`, the intended one-hold statement is:

> For every initial state in that query's closed rational state box, every fixed label in the query's complete 12-dimensional rational label box and its declared parameter image, and every time `t` in the closed hold `[0,T]`, the formal MASTER v2.1 reduced nine-state trajectory under that query's single common rational held voltage satisfies the static circular collision predicate `h(p(t)) >= 0` and stays in the parameter-specific ideal contact-admissibility domain `D_c(theta)`.

This is the sufficient one-hold statement encoded by the frozen evaluator. Its mathematical truth for all admitted query data is conditional on the interval and comparison inclusions being sound. The R3 records and reviews provide substantial evidence for this exact implementation/profile; they do not amount to a fresh, independently implemented proof engine or universal implementation-soundness theorem.

## Evidence — exact supported subclass

The supported numerical law is `phi(q)=clip(q,-1,1)` with `L_phi=1`. It is a known fixed law, including both clip corners. The formal internal vector is `z=(u,r,omega_L,omega_R,i_L,i_R)` and the implementation uses `zdot=A(theta)z+B(theta)V+D(theta)F(z,theta)` with the slip rows `S(theta)z`. Inputs use finite exact rational JSON, a closed rational initial box, one circular obstacle, one common voltage, one full-hold parameter-label cell, and the profile frozen below. This is a strict subclass of MASTER v2.1, not a result for every Lipschitz `phi`, compact `Theta`, scene, horizon, or resource profile.

The synthetic parameter image has independent fixed labels on each side:

| Parameter or label | Frozen value/range | Units and origin |
|---|---:|---|
| `m, I_z, R_w, b, v_s, c_u, c_r, V_max` | all numeric values `1` | SI units implied by MASTER's equations; deliberately synthetic unit-scale assignments |
| `phi, L_phi` | `clip(q,-1,1)`, `1` | dimensionless law and Lipschitz constant; selected for effective evaluation, not measured tire data |
| `rho_j, C_j` | `[1,11/10]` | `rho_j` is the reciprocal-inertia label; `C_j` in N |
| `lambda_j, R_j, B_j, k_j` | each `[9/10,11/10]` | H, ohm, wheel-side damping units, and matched wheel-side motor conversion units respectively |
| `J_j, L_j` | `J_j=1/rho_j`, `L_j=lambda_j` | `J_j` lies in `[10/11,1]` in the units implied by `I_z`; inductance is independently assigned, not gear-derived |
| ideal gear witness | `n=10`, `k_motor=k/10`, `J_wheel=1/10`, `J_motor=(1/rho-1/10)/100`, `B_wheel=0`, `B_motor=B/100` | algebraic consistency witness only; it identifies no motor, gearbox, or robot |

The geometric/state grid is likewise stipulated, not sourced from a platform: six nonzero-width nine-state cells with `u` in `[0.2,0.3]` or `[0.6,0.7] m/s`, yaw in `[-0.2,-0.1]`, `[-0.05,0.05]`, or `[0.1,0.2] rad/s`; 12 static-circle scenes with declared inflated radius `R_s=0.5 m`; holds `T=0.02,0.05,0.1 s`; and all nine `V_L,V_R in {-1,0,1} V`. The boxes have positive width in every state coordinate. The row-wise rational family and exact values are in `research/benchmarks/G2_USEFULNESS_BENCHMARK_SPEC_v1.md` and `validation/configs/benchmark_v1.json`.

## Evidence — finite enclosure and proof-field crosswalk

| Mathematical step | Implementation and serialized witness | Scope/qualification |
|---|---|---|
| Exact fixed-label rational parameter image, positive denominators/parameters, gear identities | `validation/g2/model.py` (`_checked_parameter_images`, `_check_gear_witness`, `build_model`); `validation/g2/polynomial.py` (`parse_expression`, `rational_functions_equal`); proof fields `parameter_label_cell`, `parameter_intervals`, `parameter_label_order`, `A_scaled`, `B_scaled`, `D_scaled`, `S_scaled`, `QF_scaled` | Label maps are fixed across the hold. The coefficient interval hull forgets some label correlations but is an outer enclosure; it can enlarge the result. |
| Outward exponential and full-hold `n=1` interval Picard predictor | `validation/g2/interval.py` (`interval_matrix_exponential`); `validation/g2/evaluator.py` (`_force_ranges`, `_predictor_level`); fields `exp_range`, `exp_remainder`, `P0_scaled`, `P1_scaled`, `force_at_initial_predictor`, `force_at_P0` | Taylor interval terms plus the norm tail and `[0,T]` integrand hull bound the complete hold. R3 has one whole-hold hull; it does not check only endpoints or add controller updates. |
| Picard defect, Lipschitz/amplitude force residual, comparison radius | `validation/g2/evaluator.py` (`_evaluate_bounds`, `_bound_model_matrices`, `_radius_series`); fields `delta_abs_scaled`, `residual_force_upper`, `M_upper`, `D_abs_upper`, `N_nonnegative_majorant`, `comparison_forcing`, `comparison_tail`, `eta_scaled`, `eta_physical` | `N=max(0,M_upper)` is a nonnegative majorant, `D_abs_upper` bounds `|D|`, and the finite nonnegative series includes its rational exponential tail. |
| Pose lift over `[0,T]` | `validation/g2/evaluator.py` (`_evaluate_bounds`); `validation/g2/interval.py` (`interval_sine`, `interval_cosine`); fields `center_heading_range`, `center_position_x_range`, `center_position_y_range`, `E_theta`, `E_p` | The code bounds the entire pose-center rectangle and adds the whole-hold position/heading error. No endpoint return set is required or produced. |
| Clip-corner-safe contact reserve | `validation/g2/evaluator.py` (`_clip_interval`, contact block of `_evaluate_bounds`); fields `beta_upper`, `contact_available_lower`, `contact_demand_upper`, `contact_margin_lower` | The full predictor-slip interval is clipped, then enlarged by `L_phi |S| eta/v_s`; `sum C_j^- sqrt_lower(1-beta_j^2) - m^+ U R` is sufficient for the stipulated algebraic contact domain. No derivative of the square-root margin is used. |
| Directed minimum distance and static-circle predicate | `validation/g2/evaluator.py` (`_dyadic_gap_bound`, `_bounded_collision_distance`); `validation/g2/checker.py` (`_checker_r3_distance_witness`); proof fields include dyadic coordinate brackets, squared-distance brackets, root brackets and `margin_lower` | With `p=24`, exact floor/ceiling bounds precede squaring; the lower distance minus `R_s` and `E_p` is the collision sufficient margin. This is the minimum distance to the predictor rectangle, not a maximum distance of every trajectory point. |
| Result binding and replay | `validation/g2/evaluator.py` (`_proof_json`, `run_query`); `validation/g2/checker.py` (`_replay_record_impl`, `replay_record`); outer runner `validation/scripts/verify_records_r3.py` | The checker reconstructs and exactly compares serialized arithmetic/status fields. It shares rational, interval, model and validated elementary-function code, and imports parsing/hash helpers from the evaluator; it is not an independent numerical engine. |

The discrete proof record asserts universal initial-box, fixed-label and closed-time quantifiers and binds one held voltage. The proof replay re-evaluates the stored interval proof rather than trusting the status label. R3's `UNKNOWN` is inconclusive: negative sufficient collision/contact bounds do not prove actual collision, actual contact failure, or unavoidable danger.

## Evidence — archived R3 outcomes and narrow usefulness

The actual pilot JSONL plus the decompressed conditional JSONL contain 1,944 unique original queries and 1,944 proof objects. Direct independent parsing yields:

| Evidence | Count/result |
|---|---:|
| `CERTIFIED` | 1,196 |
| proof-complete `UNKNOWN` | 748 |
| resource-limited, invalid-input, execution-failure rows | 0 |
| state/scene/horizon groups | 216 |
| all nine actions certified / all unknown / mixed | 132 / 76 / 8 |
| groups with any certified action / with certified zero voltage | 140 / 140 |
| groups certified only by a nonzero voltage | 0 |

There are 1,056 certified nonzero-action rows inside the 132 all-actions-certified groups. Thus R3 does certify nonzero voltages, but it finds **no group-coverage gain** over evaluating `V=(0,0)` alone. Each of the eight mixed groups has the same `state_low_mid` moving box and `T=0.1 s`; they differ only by obstacle geometry. In every such group all collision lower margins are positive, `V=(0,0)` has contact lower margin approximately `+0.127641589 N`, and the other eight actions have a negative sufficient contact margin. The eight geometries repeat one state/horizon/contact-bound distinction; they are not eight independent mechanisms. Negative contact bounds remain UNKNOWN, not unsafe.

Recorded per-query evaluator times span `0.109–0.313 s`; the upper median is `0.203 s` (the conventional midpoint median for 1,944 rows is `0.1955 s`). All 648 rows at each horizon exceed that horizon (`0.02`, `0.05`, or `0.1 s`). This establishes offline finite execution on the recorded Windows/Python configuration only; it does not establish a deadline-safe online filter, action-selection policy, or G3 recursion.

## Status — what this candidate accepts and leaves open

| Claim | Status | Boundary |
|---|---|---|
| Recorded completion, row counts, proof-object presence and R3 artifacts | **ACCEPTABLE as scoped computational evidence** | The accepted object is the frozen synthetic R3 batch. This candidate independently recounted raw records and decompression hashes, but did not rerun evaluator/checker replay. |
| Directed-dyadic distance correction | **VALID in its stated role** | It bounds the minimum distance to the complete predictor-position rectangle; it does not validate the upstream tube by itself. |
| Full R3 `CERTIFIED` interpretation | **PARTIAL pending exact source-to-theorem review** | Prior GPT review found no unsound branch in the inspected frozen path; no reviewer has established universal implementation soundness for the full class. |
| Usefulness/action selection | **PARTIAL** | Nonzero-width moving synthetic cells certify, but zero voltage attains identical existential group coverage; mixed statuses are contact-bound-only. |
| Physical parameter relevance and practical operating domain | **UNVERIFIED** | All R3 dynamics, geometry, and scales are synthetic; no DDWMR platform or primary-source parameter/contact-law package justifies them. |
| Online timing, endpoint return, repeated feasibility, recursive safety | **UNVERIFIED / outside R3** | Offline query timing is longer than each hold; no policy, target set, or G3 argument is present. |
| Generic method novelty | **Not a G2 acceptance condition; G4 remains UNVERIFIED** | The comparison/interval/Picard machinery is established generic methodology. The Auer comparison is a separate G4 lane. |

## Finding — concrete residual implementation/provenance obligations

The frozen producer profile declares a 15-second/query cap. `validation/g2/rational.py` checks the deadline only after every 256th metered operation, while the successful return in `validation/g2/evaluator.py` has no final deadline check. The R3 timings are all far below 15 seconds, so this does not change any recorded R3 row. It does mean the wall limit is a checkpointed best-effort stop, not a hard per-query bound for future inputs/runs. The fixed rational-operation and bit caps remain finite.

R3's role-specific source lists are not a complete transitive closure: `checker.py` imports query/profile/hash helpers from `evaluator.py`, which `CHECKER_PATHS` omits; `model.py` imports `polynomial.py`, which neither role list includes. The full Git revision still identifies these files, and the omission does not show the frozen R3 run used different code. It does weaken the explicit dependency manifest. The R3 spec-content ledger also binds `G2_FINITE_EVALUATOR_SPEC_v1.md` and the usefulness benchmark, but not the separate analytic `G2_ENCLOSURE_CANDIDATE_v1.md`; theorem-to-code correspondence is therefore a review-time link, not part of that frozen spec ledger.

**Required action:** Before relying on a hard wall-cap guarantee in a future version, check elapsed time before successful return or clearly relabel the cap as cooperative. Before another run, list the full transitive producer/checker closure and bind the analytic theorem note used for acceptance. Independently close the exact frozen source-to-inclusion argument; do not describe the shared checker as an independent engine.

## Required independent decision

Accept the following sentence only if the source-level inclusion path is independently reviewed:

> R3 completed 1,944 frozen synthetic G2-COMP-clip queries: the recorded fallback emitted 1,196 `CERTIFIED` results and 748 proof-complete `UNKNOWN` results with zero resource, invalid-input, or execution-failure records. Conditional on the frozen interval/Picard/comparison implementation satisfying its declared inclusions, each `CERTIFIED` result is a continuous full-hold collision and ideal-contact certificate for the stipulated nine-state reduced model, the particular fixed parameter image, state box, circle and held voltage in that query. This establishes a narrow finite synthetic computational result, not practical platform utility or the canonical G2 gate.

Do not change G2, G3, G4, physical-correspondence or overall HOLD statuses through this note.

## Provenance anchors

The R3 run-bound content ledger is `results/validation/g2/r3/specification_content_ledger_r3_v1.json`, SHA-256 `84928fe65dd788b7248d52e264832e4bcd3ca277633644ba3157cf16fb3efa45`; the spec bundle digest is `84b444d0be6e18c946697c3b95662ffd0f30dd228ae7ca5e742cee47d446c850`. Frozen spec Git-blob SHA-256 values: finite evaluator `5b11fe7d9e8f21ff259b86e44e3648f34f56d78410492ca4a7c9b73a43ea7908`; usefulness benchmark `a16a55230754a915b21616392ce508a6d7f1abb8694ce4e25933ea1435523912`; distance addendum `fe730d2bf7e172c781d4f05f5ad7fe4ab6d6e6f5f1f80d657232f5e1a891cc7e`. The analytic note read for this audit is `G2_ENCLOSURE_CANDIDATE_v1.md`, current main blob SHA-256 `38b5a8419ee429bf53a35a1d94639d9f911cedc3e6df089191da1bf8d3403d2a`; it is not in the R3 run-bound spec ledger.

R3 source-commitment SHA-256 values as recorded in producer/checker metadata:

| Path | SHA-256 of Git blob bytes |
|---|---|
| `validation/g2/evaluator.py` | `62dd355684c53fdd104ad051d2f06486e256e3489f1a72263a8432b9af9cc26e` |
| `validation/g2/checker.py` | `b2605941cc2620f19d0c6001736bec8e292b2e0dbb819f043c5dcd44fbc5e526` |
| `validation/g2/rational.py` | `8a2c16778b33898afd16c8da44945c2d41fd7d187cb11c7cb071745e68ed5c6e` |
| `validation/g2/interval.py` | `e49e2e3880485d9a658e2435cfa06b784f98257b13c51fa4a2bf464f9c73e5c6` |
| `validation/g2/model.py` | `93e9a96d640ad09a7eb7dbff51ebfb8f2d783296ce5afff57af41e81e30a8508` |
| `validation/g2/polynomial.py` | `48e3ff7dcce8353cb9d58b31f6986e12fcaaaf320cd06896f95e0813740b66a4` — imported transitively but omitted from role lists |
| `validation/g2/hashing.py` | `0d5137359e19c80b20c097d49c8d7246e48effcaef9e3649b142120136c13aab` |
| `validation/g2/provenance.py` | `8830bb334c459e7b319ee5eb3ada43c5057aef55237f6b46a886b6fc90bfa56d` |
| `validation/scripts/run_pilot_r3.py` | `ba564cb1ee10ab095ef58d1c4cbb07313f54359364a97e805e59484ae9f8b8be` |
| `validation/scripts/verify_records_r3.py` | `3f9086221365128f7eee2b583008371a8b27043304a5ee409265320411029e72` |

