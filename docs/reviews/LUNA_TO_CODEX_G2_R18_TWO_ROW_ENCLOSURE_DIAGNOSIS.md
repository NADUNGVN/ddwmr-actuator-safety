Session: DDWMR | LUNA-G2-SCOPE

# G2 R18 — source-backed diagnosis of the R17 two-row `UNKNOWN` results

**Date:** 2026-10-05  
**Status:** `DONE` — read-only analysis of saved R17 artifacts. Zero new rows, zero worker/native query/stage calls, and R5 remains 800/800 `NOT_RUN`.

## Finding and disposition

Both R17 records replay as `VALID_UNKNOWN` (`checker_status=UNKNOWN`, `safety_certified=false`, `task_eligible=false`; reason `NONNEGATIVE_SAFETY_MARGIN_NOT_ESTABLISHED_ON_EVERY_SLAB`) because the accepted interval state boxes are far wider than the declared initial state box. In those boxes, normalized slip intervals span the clip-law saturation range, so the certified lateral reserve lower bound becomes exactly zero on both wheels. The interval body-demand upper bounds remain positive. Independently, the lifted axis-aligned pose tubes overlap the obstacle center on row 62 slab 0 and row 74 slab 1, giving an exact zero distance lower bound. Row 74 slab 0 has a positive but insufficient distance lower bound. These are failures of sufficient lower bounds on broad outer enclosures; they do **not** prove collision, loss of contact, an unsafe true trajectory, or physical-platform failure.

The saved initial state box itself is collision-safe and contact-admissible for every declared fixed parameter label, with large positive margins under the formal reduced-model equations. That is an initial-time result only; it does not imply either property over the hold.

Research decision: keep the zero-voltage versus positive-voltage, 250 ms, near-obstacle configuration as a plausible **method-development target** after a proof-backed tightening. The consumed R17 rows are development-overlap evidence and cannot be presented as fresh validation. Any new usefulness claim requires a prospectively frozen challenge using fresh source-bound evaluation identities and an independent replay; the current pair rule gave no separation and authorizes no study.

## Scope and evidence identity

I read the R18 assignment, `AGENTS.md`, all four canonical `research_context` files, the R17 execution handoff, and `docs/reviews/CODEX_G2_R17_TWO_OFFLINE_ROWS_REVIEW.md` (raw SHA-256 `653c9a98db66906a8280d84726bd4a497c880932bc893f92a6b013fcf07581c`). Codex accepted the exact execution/replay provenance, confirmed both outputs are inconclusive, and required this saved-artifact bottleneck analysis.

The extraction was read-only. `validation/scripts/extract_g2_r18_enclosure_diagnosis.py` verifies the R17 GO, manifest, source-closure, stored authorization, receipt, record hashes, query bindings, and the R10/R11 source hashes before reporting rational fields. It does not import or invoke a producer, worker, stage runner, native query, controller, or experiment. Run from the repository root with `python validation/scripts/extract_g2_r18_enclosure_diagnosis.py` to reproduce the summary.

| Bound item | Raw SHA-256 |
|---|---|
| R17 GO and stored `authorization.json` | `314dcce10a10db9c862b99694e5b1cda6e72bcae27fdabaeefa17f105a6af30f` |
| R17 candidate manifest | `a4913d3d0282de6a5d1a16c4c88e3c402a91f1c3dee2df1ea99afd44a71c6bb9` |
| R17 source closure | `5b6838c8da6ae55e33ad4b50c9182122943f669e63e0fa9d92e6a8de3b83ce86` |
| R17 stage receipt raw | `52a1aaec3eadf8d729c036e7f181e4e57e702068c1d76df53b120e1a34baddef` |
| R17 receipt semantic | `a5608e619c4699743446c9ca7ea5806681684826307d9d7bce8797852194614f` |
| Row 62 `record.json` | `316434ab6eacb7e221eca4feb1062001a8b576b450b725bbc1246d5e744f5cf3` |
| Row 74 `record.json` | `fbb23303ff218e3ddf56453ccea7ca41a70d40f0ff1e85335341eff7e5651421` |

The candidate manifest binds row 62 to canonical query SHA-256 `38839995032bd4328a7c4d1059d2e3e674f3f3586a12f6f2d6c76842dfcfa8f0` and row 74 to `1bab855c36a6cba051736320002ea40370c793f57a04cc5a8454a71b79d2c858`. The current R17 source closure pins the inspected producer/checker arithmetic: `time_slab_picard_r10.py` (`e9fa6672649d675e27bb4f419e28259b9546b01bb6592f3388396ecd2a211c47`), `whole_hold_picard_checker_r11.py` (`2a794e8f46c4b029331a2548dccd1948b78d3f5d5d7a96efa118d9353ba56f7e`), `model.py` (`93e9a96d640ad09a7eb7dbff51ebfb8f2d783296ce5afff57af41e81e30a8508`), `rational.py` (`8a2c16778b33898afd16c8da44945c2d41fd7d187cb11c7cb071745e68ed5c6e`), and `interval.py` (`e49e2e3880485d9a658e2435cfa06b784f98257b13c51fa4a2bf464f9c73e5c6`). The assignment and prior GO/stage bytes were preserved.

## 1. First loss of useful separation in the saved bounds

The two rows share the same initial cell, obstacle, parameter-label box, horizon, and progress threshold. Row 62 holds (V=(0,0)); row 74 holds (V=(1,1)); both use (T=1/4), obstacle center (p_o=(1/5,1/20)), radius (R_s=3/50), and progress threshold (1/20). The full 12-label parameter cell has (C_L,C_R\in[1,11/10]), with the remaining listed motor labels bounded around their nominal values.

The R10 producer first constructs a six-coordinate interval candidate with `_try_internal_slab()`. It seeds componentwise radii from the interval RHS, inflates the trial candidate geometrically by (1,2,4,\ldots), and accepts when the interval Picard image is contained in that box (`validation/g2/time_slab_picard_r10.py:138`, `:145`, `:147`, `:148`). The first accepted candidate for row 62 and row 74 slab 0 has `expansion_index=4`, i.e. the (16\times) trial expansion; row 74 slab 1 has `expansion_index=1`. This is the first saved enclosure object at which the downstream collision/contact tests lose useful separation. It is a sufficient outer box; its extrema are not claimed to be jointly attainable.

All coordinates are scaled by one in these queries. The initial (u\in[1/5,1/4]), (r\in[-1/50,0]) boxes have become:

| Row / slab | Accepted interval candidate (u) | Accepted interval candidate (r) | Refinement |
|---|---|---|---|
| 62 / 0 | `[-6301/2000, 7201/2000]` | `[-3317/2000, 3277/2000]` | (h=1/4), depth 0, expansion 4 |
| 74 / 0 | `[-5901/4000, 7701/4000]` | `[-3357/4000, 3277/4000]` | (h=1/8), depth 1, expansion 4 |
| 74 / 1 | `[-26801/25600, 36881/25600]` | `[-26897/25600, 26449/25600]` | (h=1/8), depth 1, expansion 1 |

### Collision enclosure

R10 lifts each accepted internal box to pose intervals using interval products for heading, sine/cosine, velocity, and elapsed time (`time_slab_picard_r10.py:156`, `:172`). It measures distance to the obstacle from the axis-wise gaps between the pose rectangle and the obstacle center (`:178`); `sqrt_lower(0)` is exactly zero (`validation/g2/interval.py:148`). Thus:

| Row / slab | Stored pose/collision evidence | Stored exact lower margin |
|---|---|---|
| 62 / 0 | `pose_tube` contains the center coordinatewise; `coordinate_gaps=(0,0)`, `distance_lower=0` | `0 - 3/50 = -3/50` |
| 74 / 0 | (x)-interval `[-5933/32000, 7733/32000]` contains (1/5); (y)-gap is positive; `distance_lower=1540220173689/70368744177664` | `-67047611924271/1759218604441600` |
| 74 / 1 | (x)-interval `[-323861/1024000, 431861/1024000]` contains (1/5); `coordinate_gaps=(0,0)`, `distance_lower=0` | `0 - 3/50 = -3/50` |

The exact row-level source records are `results/validation/g2/decision_domain_r17_go_entrypoint_correction_stage_v1/row_00/record.json` (62) and `.../row_01/record.json` (74). The first useful loss for row 62 and row 74 slab 1 is therefore geometric: the rectangular pose outer bound contains the obstacle center, so the lower-distance primitive cannot separate the obstacle even though the true reachable set may occupy only a correlated subset of that rectangle. Row 74 slab 0 is already inconclusive because its certified distance lower bound is less than the obstacle radius. This is a dependency/shape relaxation in the set representation, not a square-root rounding failure.

### Contact enclosure

The recorded normalized-slip intervals and contact arithmetic identify an even more direct bottleneck. R10 forms

\[
\sigma_L/v_s=(R_w\omega_L-u+br)/v_s,\qquad
\sigma_R/v_s=(R_w\omega_R-u-br)/v_s,
\]
then computes `beta = abs_upper(clip(slip_interval))`, reserve lower bounds (C_{j,\min}\sqrt{1-\beta_j^2}), and demand upper bound (m_{\max}|u|_{\max}|r|_{\max}) (`time_slab_picard_r10.py:185`). R11 independently repeats these calculations (`whole_hold_picard_checker_r11.py:191`).

| Row / slab | Normalized slip intervals ((L,R)) | β upper | Reserve lower | Body-demand upper | Contact margin lower |
|---|---|---|---:|---:|---:|
| 62 / 0 | `[-68219/10000, 66019/10000]`; `[-68987/10000, 67187/10000]` | `(1,1)` | `0` | `23885717/4000000` | `-23885717/4000000` |
| 74 / 0 | `[-70919/20000, 66519/20000]`; `[-71487/20000, 67887/20000]` | `(1,1)` | `0` | `25852257/16000000` | `-25852257/16000000` |
| 74 / 1 | `[-331391833489/86400000000, 314192833489/86400000000]`; `[-330896914477/86400000000, 316721914477/86400000000]` | `(1,1)` | `0` | `991988257/655360000` | `-991988257/655360000` |

Each interval crosses the clip saturation thresholds, so the sound upper bound is β=1 for each wheel. This makes both square-root radicands exactly zero and therefore each guaranteed lateral reserve exactly zero; it is not a floating-point or rational-precision artifact. The positive demand products follow directly from the broad candidate (u,r) intervals; they also discard their correlation. The zero reserve and positive demand establish that this particular sufficient contact test cannot certify any of the slabs. They do not establish that the real slip reaches saturation or that contact is actually lost.

The accepted boxes are much wider than the initial box, and the producer uses interval matrix/state operations over them. The 12 fixed parameter labels are soundly covered as intervals through `model._checked_parameter_images()` and `build_model()` (`validation/g2/model.py:75`, `:149`); interval images and componentwise arithmetic can forget relationships among labels and states. The R10 proof contract explicitly permits this outer-relaxation conservatism while retaining a single fixed full parameter image over all slabs (`time_slab_picard_r10.py:374`, `:376`). For row 74, the Picard inclusion fallback splits the hold and carries a componentwise endpoint interval into the next slab; the split did not recover useful slip/contact or pose separation. No evidence indicates a transport, overflow, arithmetic-cap, or checker-integrity failure: both workers completed, captures were complete, and R11 replay accepted the records as `UNKNOWN`.

## 2. Initial-time state versus full-hold truth

The initial pose box is (p_x,p_y\in[-1/1000,1/1000]); the obstacle center is ((1/5,1/20)). Exact coordinate gaps are `199/1000` and `49/1000`, so

\[
d_{0,\min}^2=21001/500000>1/25=(1/5)^2,
\]

hence (d_{0,\min}>1/5>3/50=R_s). The declared initial set is collision-safe with clearance greater than (7/50), independent of the parameter labels.

At the same initial box, the exact normalized-slip intervals are `[-27/100,1/20]` and `[-1/4,7/100]`, so β bounds are `27/100` and `1/4`. The declared model has (C_L,C_R\ge1), (m=R_w=b=v_s=1), and `clip` ϕ. The root radicands are `9271/10000` and `15/16`; each root exceeds `24/25` because ((24/25)^2=576/625<9271/10000<15/16). The initial body-demand upper bound is `1/200`. Therefore an exact rational contact-margin lower witness is

\[
(1+1)(24/25)-1/200=383/200>0.
\]

So every state in the declared initial box is contact-admissible for every fixed parameter label in the declared parameter cell. This does **not** prove contact-domain preservation for (t>0), full-hold collision safety, or recursive safety. The saved R17 enclosure records provide valid broad outer bounds and fail to prove nonnegative margins on the hold. They do not reveal whether any fixed-label true trajectory collides, becomes inadmissible, or remains safe/admissible throughout. A counterexample would need proof-backed trajectory error bounds; no simulation or point trajectory is used here.

## 3. Research decision and exact obligation for tightening

The two actions are exactly matched except for voltage: row 62 uses ((0,0)), row 74 uses ((1,1)), on the same state/parameter cell and scene for (1/4) s. Their task-progress threshold is `1/20`. This is a plausible diagnostic configuration for a future sound evaluator because it compares a nominal and forward-voltage action under the same initial uncertainty, and the initial collision/contact conditions have positive margins. The current records provide no evidence that either action succeeds or that voltage selection is useful: their certified progress lower bounds are `-6301/8000` and `-322837/1024000`, both below threshold, as a consequence of the broad boxes, and both safety outcomes are `UNKNOWN`.

**Decision:** retain these factors as a method-development hypothesis, but require a new prospectively declared, source-bound challenge before making a usefulness or validation claim. R5 indices 62 and 74 are consumed development-overlap rows, not fresh evidence; the current paired rule is `NO_PREDECLARED_TASK_SELECTION_SEPARATION`, the preparation trigger is false, and broader-study authority is `NOT_GRANTED`. If a new method cannot separate or usefully classify fresh matched rows, design a new challenge before execution. Do not tune a threshold to certify these consumed records.

Any refinement proposed must discharge all of the following mathematical obligations under the same fixed v2.1 assumptions:

1. **Outer coverage:** prove that the union of every refined initial/parameter subcell covers the exact full input domain; for each subcell, keep one execution-fixed parameter label and one held voltage through all time slabs. Never select different favorable labels on different slabs.
2. **Validated slab inclusion and carry:** prove each full-time slab enclosure, its endpoint inclusion in the next slab's initial box, and exact coverage of ([0,T]). Any splitting, Taylor/affine representation, exponential predictor, or correlation-preserving set must have independently checkable outward error bounds and fit the source-bound replay contract.
3. **Contact admissibility:** for every state and fixed label in every full-time enclosure, prove
   \[
   C_L\sqrt{1-\phi(\sigma_L/v_s)^2}+C_R\sqrt{1-\phi(\sigma_R/v_s)^2}-m|ur|\ge0.
   \]
   If a refinement uses differentiability/Lipschitz bounds for this square-root expression near saturation, it must prove the required regularity on the covered domain; otherwise use direct certified lower bounds. Do not infer admissibility from initial state or endpoints.
4. **Collision separation:** prove a directed lower bound on distance from the complete joint pose reachable set to the obstacle strictly exceeding `3/50` on every slab. Replacing axis boxes with a structured pose set is acceptable only if the new set is proved to contain all trajectories and the distance calculation is outward certified.
5. **Task and paired rule:** prove the locked progress condition against `1/20` wherever task eligibility is claimed, replay every record independently, and apply the predeclared pair truth table without changing thresholds or outcomes after seeing results.
6. **Provenance and scope:** bind source, parameters, inputs, limits, and checker to a reviewed manifest; obtain a new exact-scope GO before any fresh execution. A positive preparation trigger would still not authorize the R5 800-row study.

No theorem or physical-platform claim is added. G2 remains `UNVERIFIED`; G3/G4 and physical-platform correspondence remain `UNVERIFIED`; overall disposition remains `HOLD`.

## Artifact ledger and execution boundary

The extraction script SHA-256 is `97c30f4d968ecce1cadaad211e363b8a8a874fd8bc5d3f1f1828d8c446d9e3b6`. The full R17 R10/R11 interval source hashes are listed above and are verified by that script against the saved R17 closure. The stage, its GO authorization, both row records, and the 800-row study state were preserved. No native query, worker, stage, study, controller, experiment, or physical system was run for R18. No G4 source/manifest, other source, branch, commit, or push was changed.