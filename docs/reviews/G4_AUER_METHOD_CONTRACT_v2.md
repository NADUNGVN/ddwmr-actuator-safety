# Auer 2013 method contract — DDWMR residual IVP reconstruction

**Version:** v2 · **Date:** 2026-10-01  
**Status:** R4 implementation contract frozen before the IVP runs; scientific acceptance remains subject to the recorded proof replay and independent review.  
**Supersedes:** pagination and implementation-status fields in v1 only. `G4_AUER_METHOD_CONTRACT_v1.md` remains unchanged.  
**Method ID:** `AUER2013_PIECEWISE_RESIDUAL_RECONSTRUCTION_DDWMR_R4`  
**Scientific label:** paper-faithful method reconstruction using exact-rational validated arithmetic. This is not a reproduction of the original VALENCIA software or application.

## 1. Primary sources and corrected locators

The primary method source is E. Auer, S. Kiel, and A. Rauh, “A Verified Method for Solving Piecewise Smooth Initial Value Problems,” *International Journal of Applied Mathematics and Computer Science* 23(4), **731–747** (2013), DOI [10.2478/amcs-2013-0055](https://doi.org/10.2478/amcs-2013-0055). The retained PDF's first-page header gives the volume, issue, and 731–747 pagination. Equations (42)–(43) are on printed page **742**; §4.1 and the piecewise derivative definitions are on pp. 740–742.

The residual iteration is cross-checked against A. Rauh and E. Auer, “Verified Simulation of ODEs and DAEs in ValEncIA-IVP,” *Reliable Computing* 15, **370–381** (2011), DOI [10.1007/s11128-010-0165-6](https://doi.org/10.1007/s11128-010-0165-6). The retained PDF's title page is printed p. 370. Algorithm 1 and Eqs. (3)–(6) are printed pp. **371–372**. These locators correct the mistaken pp. 739–750 and 371–382 in frozen v1; the original PDFs are retained under `research/third_party/auer2013/`.

The pinned VALENCIA 0.92_2e source is retained in `external/valencia-basic/free-source/ValEncIA/ValEncIA-IVP_0.92_2e.cpp`. It is an older smooth application seed. Its mean-value AD routines and `compute_R` iteration are implementation context for the smooth residual solver; they do not contain the 2013 clip generalized-derivative extension or the adopted DDWMR equations. This work reconstructs the published method and does not claim original-software reproduction.

## 2. Frozen scope

The first required case is the two-state analytic branch-crossing fixture in `validation/baselines/auer2013/analytic_branch_crossing_fixture_v1.json`. It uses

\[
\dot x=1,\qquad \dot y=\operatorname{clip}(x,-1,1),\qquad
x(0)\in[0.9,0.91],\quad y(0)=0,\quad T=0.2.
\]

This is an independent analytic Auer-method validation fixture, not the paper's §5 friction/hysteresis reproduction. The DDWMR case is conditional on proof-complete analytic replay and is bound by `validation/baselines/auer2013/auer_r4_ddwmr_single_case_input_v1.json` to the already selected first query/action, complete twelve-label image, benchmark, obstacle, voltage, and 1/50-second horizon. No other query is eligible in this package.

The physical DDWMR state order is `(p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R)`. The same twelve execution-fixed benchmark labels are appended with exactly zero derivative. Cartesian interval boxes may lose parameter/state correlation and broaden the enclosure; labels and voltage remain unchanged and may never be narrowed or resampled between steps. Such boxing is an outer relaxation of the fixed-parameter family, not a switching-parameter model claim.

## 3. Equation-to-code and proof-obligation crosswalk

| Source item | R4 reconstruction | Source and implementation boundary |
|---|---|---|
| Auer 2013 Eq. (27), scalar expression composition | Evaluate the declared DDWMR scalar RHS over the state and parameter intervals; reject a divisor interval containing zero. | `validation/baselines/auer2013/rhs.py::augmented_rhs`; expression order follows the nine-state MASTER v2.1 equations and benchmark fixed-parameter maps. This source is shared with G2/R3 and is not an independent arithmetic engine. |
| Eqs. (28), (31), piecewise value/range | Use the exact continuous `clip(q,-1,1)` branches. Its range on `[a,b]` is `[clip(a),clip(b)]`; neither corner is smoothed. | `piecewise.py::clip_value` and `clip_interval`. The R4 analytic checker re-implements the clip interval range locally and compares the full step record. |
| Eqs. (33), (40), generalized derivative | Use `{0}` on strictly saturated intervals, `{1}` strictly inside `(-1,1)`, and `[0,1]` whenever an interval touches or crosses either corner, including singleton corners. Chain through normalized slip, fixed-label rational maps, and the remaining RHS operations. | Producer route: `DualInterval.clip` in `piecewise.py`, composed by `rhs.py`. The independent checker defines its own interval AD and clip generalized derivative in `replay_ivp.py`. The arithmetic primitive is shared. |
| Eq. (35)/(41), discontinuity correction | The continuous clip has zero value jump at both corners; its branch-gap correction is exactly zero. No zero divided by a switch-distance interval is evaluated. | This is a specialization to the continuous benchmark law; discontinuous Auer systems remain out of scope. |
| Eq. (42), functional tube | For each accepted closed step, bound every trajectory and every time in `x_app([t_k,t_{k+1}])+R([t_k,t_{k+1}])`; keep a separately propagated endpoint. | `residual_ivp.py` records approximate-path range, full-time residual range, total hull, and endpoint. The checker reconstructs these from the frozen case input and serialized iteration. |
| Eq. (43); Rauh–Auer Algorithm 1, Eqs. (3)–(6) | Iterate a residual-derivative enclosure, check componentwise inclusion, and integrate it with exact outward interval multiplication. | For the frozen linear/piecewise-C1 approximate paths, the proof uses `D^(k+1) ⊇ -xdot_app + f(x_app) + J(Q_k)R_k`, then verifies `D^(k+1) ⊆ D^k` and `R^(k+1)([0,h]) ⊆ R^k([0,h])`. The integrated range is `R(0)+[0,h]D`. No finite iteration count or small width substitutes for these subset checks. |
| Fixed-label augmentation | Append all twelve labels to the state with zero derivatives and preserve the same full input label image and voltage for the full hold. | `residual_ivp.py` and the independent `replay_ivp.py` bind and replay the 21-coordinate DDWMR path. Any interval dependency loss is conservative and remains explicit. |

## 4. Residual operator and accepted-step premise

Let `x_app(t)` be the declared differentiable rational approximate path, with interval initial error `R_0` chosen so the complete initial box lies in `x_app(0)+R_0`. Let `Q_k(t)` be a compact convex rough state/label tube containing `x_app(t)+R_k(t)` on the closed slab. The componentwise generalized-Jacobian interval `J(Q_k)` encloses the piecewise secants of the RHS on every segment from `x_app(t)` to `x_app(t)+r`, for `r∈R_k(t)`. For every such point, the mean-value form therefore gives

\[
f(x_{app}(t)+r)-f(x_{app}(t))\in J(Q_k)R_k(t).
\]

Define

\[
D_{k+1}=-\dot{x}_{app}([t_k,t_{k+1}])+f(x_{app}([t_k,t_{k+1}]))+J(Q_k)R_k([t_k,t_{k+1}]),
\]

and the outward integral enclosure

\[
R_{k+1}([0,h])=R_0+[0,h]D_{k+1},\qquad
R_{k+1}(h)=R_0+hD_{k+1}.
\]

The worker accepts a step only after the independent checker recomputes every interval and verifies both `D_(k+1) ⊆ D_k` and the induced integrated-tube inclusion on the complete closed slab. The time-parametrized Picard operator then maps the declared compact convex rough tube into itself. The interval vector field is continuous and locally Lipschitz on the checked rational domain, so the established IVP solution lies in the validated tube. The generalized-derivative mean-value form is applied componentwise; each output row may use its own mean-value selection.

For the analytic case, `x_app` is the exact piecewise integral of `clip(x_mid+t)` and its base residual is exactly zero; its derivative is continuous across the crossing. The interval generalized Jacobian encloses the complete crossing family. For the DDWMR case, the frozen approximate path is linear with exact rational slope equal to the midpoint of the starting interval RHS; its nonzero residual is retained in each iteration. A failed subset check is not proof of nonexistence or collision; it is an unresolved inclusion under this finite method/profile.

The approximation and all residual intervals are rational. The shared exact-rational interval operations perform no floating-point rounding. Sine/cosine are enclosed by the versioned Taylor-plus-Lagrange backend; a broad range may force a resource stop or an unresolved inclusion but cannot trigger a host `libm` fallback.

## 5. Independent native record checker

`validation/baselines/auer2013/replay_ivp.py` is a separate implementation; it does not import `residual_ivp.py` or `rhs.py`. It independently reconstructs the nine-state RHS, all 21-by-21 interval AD entries, clip range/generalized derivative, approximate path, residual derivative, integration bound, closed-slab tube, endpoint, and exact inclusion subset checks. It parses the serialized proof bytes and checks the canonical proof digest before replay.

The proof binds the exact input bytes, benchmark hash (for DDWMR), method-contract hash, backend-manifest hash, profile hash, source-snapshot manifest hash, solver/checker source hashes, query/action, all labels, voltage, horizon, and output tube. The replay rejects an altered hull, residual iterate, switch interval, endpoint, action, or source/profile binding. Exact interval addition/multiplication, and the certified rational Taylor sine/cosine range, remain shared arithmetic dependencies from `validation.g2`; the checker is algorithmically independent of the producer, not an independent arithmetic library.

## 6. Endpoint chaining and common safety predicates

Each accepted step has distinct start endpoint, full-time hull, and end endpoint records. Closed time slabs must cover exactly `[0,T]` with no gaps. A later step starts from an enclosure containing the complete previous endpoint; all label endpoints remain equal to their original full intervals. The common checker is called once on the proof-derived total hulls and evaluates its collision and algebraic contact lower bounds over every closed slab. The Auer residual radius is already included exactly once in each total hull; the common adapter uses `NATIVE_TOTAL_HULL` and adds no radius.

The common checker reports only `PASS_ON_SUPPLIED_TUBE` or `UNKNOWN_ON_SUPPLIED_TUBE`, with `certificate_emitted=false` and `ode_tube_proof_replayed=false` in its own layer. Native replay evidence and predicate evidence stay separately reported. A predicate pass is not physical-platform validation, G2 acceptance, a recursive set, G3, G4, or GO.

## 7. Resource and arithmetic binding

R4 freezes `small_case_resource_profile_v2.json` before IVP execution. It keeps the v1 rational bit, operation, time, step, Picard, split, RHS/Jacobian, serialization and Taylor limits unchanged, while replacing the disabled memory clause with a Windows Job Object per-process commit cap and a parent hard timeout. The worker is launched suspended, assigned to the job, and resumed only after the limit is installed. A capped allocation probe must pass before the analytic case. Exact observed peak process memory, wall time, all step attempts, and all work counters are stored with each run.

The arithmetic backend remains `DDWMR_EXACT_RATIONAL_TAYLOR_INTERVAL_V1`. It uses the existing exact `Fraction`/`Interval`/`Budget` source and Taylor-plus-Lagrange trigonometric enclosure; it is shared with G2/R3. PROFIL/BIAS x86-64 with host glibc/libm is excluded. No arithmetic primitive was replaced in this package, so the v1 source contract stays intact; `ARITHMETIC_BACKEND_MANIFEST_v2.json` hash-binds the residual core, independent checker, runtime guard, worker, method contract, and v2 resource profile.

## 8. Source-fidelity and claim boundary

This is a documented reconstruction: it specializes the published continuous-piecewise method to the benchmark clip law, uses exact rational arithmetic instead of historical PROFIL/BIAS, represents all state and labels as exact interval boxes, emits JSON proof records, and uses a separate checker. It does not patch the pinned VALENCIA source, reproduce its binary, or reproduce Auer §5. The numerical status of the two R4 cases, proof replay, resource use, and common predicate result are reported only in `LUNA_TO_CODEX_G4_AUER_R4_IVP_CORE_FULL_HANDOFF.md` after their frozen runs.

