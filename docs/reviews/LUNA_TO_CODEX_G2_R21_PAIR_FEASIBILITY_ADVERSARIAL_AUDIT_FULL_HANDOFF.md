Session: DDWMR | LUNA-G2-SCOPE

# G2 R21 — adversarial audit of the R20 pair-feasibility witness

**Date:** 2026-10-06  
**Disposition:** **VALID** for the exact nominal counterexample and its limited pair consequence. **BLOCKER** for using the consumed R17 indices 62/74 as the locked strong task-selection challenge. **UNVERIFIED** for any new nontrivial operating cell or usefulness claim.  
**Execution:** read-only audit and rational derivation only; zero new native rows, workers, stages, retries, or studies. R5 study remains **800/800 `NOT_RUN`**. No archived record or G4 file was changed.

## 1. Scope and sources

I read `AGENTS.md`, all four canonical files under `research_context/`, the R21 assignment, the Codex R20 review, the Luna R20 handoff, MASTER v2.1 §§5–11, the endpoint-progress identity in `validation/g2/endpoint_checker_r2.py`, and the exact paired query payloads embedded in the R17 candidate manifest. I derived the witness from MASTER's equations and then checked its point against the manifest; the derivation below does not rely on the equations printed in the R20 review.

The exact locked rows are:

| R5 index | Query / held action | Query SHA-256 | Semantic input SHA-256 | Saved record SHA-256 |
|---:|---|---|---|---|
| 62 | `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_L0_R0`, `(0,0)` | `38839995032bd4328a7c4d1059d2e3e674f3f3586a12f6f2d6c76842dfcfa8f0` | `aacb6dd0639c5d5c603ca227066352a9d04a1d2d0e92fc77ab3499f59f10db37` | `316434ab6eacb7e221eca4feb1062001a8b576b450b725bbc1246d5e744f5cf3` |
| 74 | `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_Lp1_Rp1`, `(1,1)` | `1bab855c36a6cba051736320002ea40370c793f57a04cc5a8454a71b79d2c858` | `b4ad72b1cf4e1fcc37de3bf3ed080ba4797e637e3f37919873df740043645c3b` | `fbb23303ff218e3ddf56453ccea7ca41a70d40f0ff1e85335341eff7e5651421` |

The manifest raw SHA-256 is `a4913d3d0282de6a5d1a16c4c88e3c402a91f1c3dee2df1ea99afd44a71c6bb9`; the bound source-closure raw SHA-256 is `5b6838c8da6ae55e33ad4b50c9182122943f669e63e0fa9d92e6a8de3b83ce86`. I independently recomputed the raw hashes of both saved records and obtained the values in the table. The archive and R17 runner/checker audit continue to report both records as `VALID_UNKNOWN`; those records are left unchanged.

The shared R17 query cell has state order `[p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R]`, with `u ∈ [1/5,1/4]`, `r ∈ [-1/50,0]`, `omega_L,omega_R ∈ [0,1/4]`, and zero contained in each of the other state-coordinate intervals. All twelve fixed parameter labels contain `1`: `rho_L/rho_R,C_L/C_R ∈ [1,11/10]`; `lambda_L/lambda_R,R_L/R_R,B_L/B_R,k_L/k_R ∈ [9/10,11/10]`. The fixed maps give `m=I_z=R_w=b=v_s=c_u=c_r=1`, `J_j=1/rho_j`, `L_j=lambda_j`, and the remaining named parameters equal their labels. Both rows use the explicit `clip` law, the same obstacle `(1/5,1/20)` with radius `3/50`, hold `T=1/4`, and frozen required progress `1/20 m`; only the held voltage changes.

Consequently the counterexample point

\[
x_0=(0,0,0,1/5,0,0,0,0,0),\qquad
\vartheta_{labels}=(1,1,\ldots,1)
\]

belongs to each exact R17 product cell. At that point all fixed model parameters are exactly `1`, including `J_L=J_R=1`. This is one admissible fixed parameter realization, not a parameter-switching construction.

## 2. Independent derivation from MASTER §§5–11

MASTER gives `ṗ_x=u cos(theta)`, `ṗ_y=u sin(theta)`, `thetȧ=r`; `sigma_L=R_w omega_L-(u-br)`, `sigma_R=R_w omega_R-(u+br)`; `F_j=C_j clip(sigma_j/v_s)` for these `clip` queries; and the body, wheel, and current equations in §§9–11. At the selected point the left/right data and held voltages agree. The symmetric subspace `r=theta=0`, `omega_L=omega_R=w`, `i_L=i_R=i` is invariant by uniqueness of the locally Lipschitz ODE. Put `d=u-w`.

For `(1,1)`, on a region where `u>0`, `w>=0`, `i>=0`, and `d>0`, the slip on both sides is `sigma=w-u=-d`. Since `w<=u` and `u` decreases from `1/5`, `0<d<=1/5<1`; therefore the clip is unsaturated and `F_L=F_R=-d`. Substitution into MASTER's equations gives

\[
\dot u=-u-2d,\qquad
\dot w=i+u-2w,\qquad
\dot i=1-i-w,\qquad
\dot d=-4d-i.
\]

This agrees with the R20 displayed reduced system, now obtained directly from MASTER.

### Bootstrap and rational lower bound for `d`

The region closes through `T=1/4`:

* `w=0` has `ẇ=i+u>0`; `i=0` has `i̇=1-w>=4/5` while `w<=u<=1/5`.
* `u=w+d>0`; while in the region, `u̇<0`, so `u<=1/5`. Also `d<=u<=1/5`.
* From `i̇=1-i-w<=1` and `i(0)=0`, `i(t)<=t`.
* Variation of constants for `ḋ+4d=-i` yields

  \[
  d(t)=\tfrac15e^{-4t}-\int_0^t e^{-4(t-s)}i(s)\,ds
  \ge \tfrac15e^{-4t}-\tfrac{t^2}{2}
  > \tfrac1{15}-\tfrac1{32}=\tfrac{17}{480}>0,
  \]

  for `0<=t<=1/4`; here `e^{-4t}>=e^{-1}>1/3` follows from `e<3`, and the integral is at most `∫₀ᵗ s ds=t²/2`.

The lower bound rules out `d=0` as a first exit. The inward boundary derivatives rule out exits through `w=0` or `i=0`, and `u=w+d` rules out `u=0`. Thus the bootstrap is self-consistent; the clip remains on its linear branch throughout this trajectory.

It follows that `u̇=-u-2d<=-17/240`. Integrating once for `u` and again for `p_x` gives

\[
J=p_x(T)-p_x(0)=\int_0^{1/4}u(t)\,dt
\le \frac1{20}-\frac{17}{7680}
=\frac{367}{7680}<\frac1{20}.
\]

The bound is strict against the R17 task threshold by `17/7680 m`. The task identity itself follows from the exact kinematics and `theta=0`; it is also the identity named `PX_TERMINAL_DIFFERENCE_INTEGRAL_U_COS_THETA` in the endpoint checker.

### Zero-voltage energy check

At the same point under `(0,0)`, MASTER's energy identity gives

\[
\dot E=-u^2-\sum_{j=L,R}(w_j^2+i_j^2+F_j\sigma_j)\le0,
\]

because `clip(z)` is sign-preserving, so `F_j sigma_j>=0`. Initially `E(0)=u(0)^2/2=1/50`; initially `F_j sigma_j=1/25` for each wheel, hence `Ė(0)=-3/25`. Continuity and nonincrease imply `E(t)<1/50` for every `t>0`. In particular `|u(t)|<1/5` for `t>0`, while `|u(0)|=1/5`. Since `theta=0`,

\[
J=\int_0^{1/4}u(t)\,dt
\le\int_0^{1/4}|u(t)|\,dt<\frac1{20}.
\]

This energy argument is valid for the exact fixed point and the zero-terminal-voltage RL boundary condition in MASTER §11; it does not treat zero voltage as open circuit or as a mechanical brake.

## 3. Domain and collision checks at the witness

These are checks of the two single witness trajectories, not of every point in either R17 cell.

* For `(1,1)`, `r=0` and `0<d<=1/5`. Each contact reserve is `sqrt(1-d^2)>0`; the body demand `|m u r|` is zero, so the formal contact margin is `2 sqrt(1-d^2)>0`. Also `p_y=0`, `p_x` increases from zero, and `p_x(t)<=J<=367/7680`. Its horizontal distance from obstacle center `1/5` is at least `1/5-367/7680=1169/7680>3/50`; the trajectory remains outside the declared disk.
* For `(0,0)`, the energy bound gives `|u|,|w_j|<=1/5` for the whole hold, hence `|sigma_j|=|w_j-u|<=2/5<1`. The reserves are strictly positive and the body demand is again zero, so the contact margin is positive. Also `|p_x(t)|<=1/20`; the horizontal distance to the obstacle center is at least `1/5-1/20=3/20>3/50`, so this trajectory also remains outside the disk.

Thus the task counterexamples are not collision or contact counterexamples. A failed outer enclosure bound in the archived records also remains inconclusive about actual safety.

## 4. Consequence for the locked R17 pair

The manifest's positive-action `CERTIFIED_TASK_ELIGIBLE` class requires a complete checked safety proof and progress lower bound at least `1/20 m`. The admissible `(1,1)` witness has true progress at most `367/7680 m`, so no sound all-cell lower-bound evaluator can certify the positive action task-eligible on this unchanged cell. The same point also shows that the zero action's true progress is below threshold. Therefore the strong locked truth-table separation for this pair cannot be obtained by refining the enclosure: its positive arm is mathematically false at one admissible point.

**Scope of this blocker:** the selected R17 pair cannot serve as the locked strong task-selection challenge. It does not show an unsafe trajectory, a general G2 failure, impossibility of a different voltage-selection challenge, or failure of every enclosure method. The archived R17 `VALID_UNKNOWN` records and receipts remain untouched. The R17 outcome label `CERTIFIED_TASK_NOT_ELIGIBLE` is defined through a sufficient lower-bound test; by itself it does not prove actual task failure.

## 5. Prospective challenge screen — not a run or frozen manifest

Do not assign row IDs or spend solver work until the owner declares a task and operating domain. A result-independent nominal screen for a *different* challenge is symmetric rest with `(1,1)` versus `(0,0)`, using the fixed nominal label values `1`, the same formal obstacle only as a mathematical screening geometry, and a prospective hold no longer than `1/4 s`. This is not reuse of the consumed R17 pair and has no query ID.

For the exact nominal rest point `x0=(0,0,0,0,0,0,0,0,0)`, all labels `1`, define `q=w-u`. On `0<=t<=1/4`, a first-exit argument gives `u,q,i>=0`, `q<=1`, and the symmetric equations

\[
\dot u=2q-u,\qquad \dot q=i-4q,\qquad \dot i=1-i-u-q.
\]

Indeed, while nonnegative, `i<=t`, `q<=t²/2`, and `u<=t³/3`; these imply `u+q<=7/192<1`, making `i̇>0` at `i=0`, while `q̇=i>=0` at `q=0` and `u̇=2q>=0` at `u=0`. The upper bound on `q` keeps the clip unsaturated. These same estimates give `i̇>=137/192`, so `i(t)>=(137/192)t`. Using `e^{-z}>=1-z` on the variation-of-constants formulas, for `T<=1/4`:

\[
q(t)\ge \frac{137}{192}\left(\frac{t^2}{2}-\frac{2t^3}{3}\right)
\ge \frac{137}{576}t^2,
\]

and

\[
u(t)\ge \frac{137}{288}\left(\frac{t^3}{3}-\frac{t^4}{12}\right)
\ge \frac{685}{4608}t^3.
\]

Consequently this nominal positive-action trajectory satisfies

\[
\frac{685}{18432}T^4\le J_{(1,1)}\le\frac{T^4}{12};
\qquad
T=\tfrac14:\quad
\frac{685}{4718592}\le J_{(1,1)}\le\frac1{3072}\;\text{m}.
\]

At the same exact point, `(0,0)` leaves the system at rest and gives `J_(0,0)=0`. Both point paths are formally contact-admissible (`r=0`, `q<=1/32` for positive voltage) and clear the stated obstacle. This is an **analytic nominal feasibility screen only**. Its positive lower bound is about `0.000145 m`, and its upper bound is below `0.000326 m`; it cannot support the R17 `1/20 m` requirement at this horizon. The small lower bound must not be adopted as a task threshold just to pass the screen.

For a future all-cell comparison, require the owner to declare `delta_task>0` in meters before any candidate IDs, solver outputs, or outcomes are inspected. Use identical initial-state cell, fixed joint parameter set, obstacle, horizon, and the same whole-hold collision/contact predicate for both held actions. An action is task-eligible only if the full cell is certified safe and `J^- >= delta_task`. To claim substantive task-selection value, also establish for the baseline action `J^+ < delta_task` on that same cell; a baseline lower bound that merely misses the threshold supports only a certificate-level separation, not proof that the task is actually missed.

The next analytic gate should first compare the owner-declared threshold and operating cell with all-time progress, collision, and contact bounds. If the positive action cannot clear this gate, stop before making a source-bound manifest. If it can, freeze new prospective IDs without looking at stored outcomes, bind both actions to the same cell and predicate, and only then prepare a manifest. This assignment authorizes no subsequent execution.

### Owner inputs still needed

1. The task's physical interpretation, direction, minimum displacement, and deadline/hold duration; in particular a meaningful `delta_task` declared independently of the calculated bounds.
2. The operating domain: initial pose/body/wheel/current ranges, obstacle/environment and clearance, allowed voltage set, and the joint fixed-parameter ranges/correlations. If a physical-platform claim is intended, the owner must also identify the platform envelope and support/contact evidence that maps it to MASTER's reduced model.
3. For runtime or cost claims: the comparison baseline, hardware or compute platform, real-time budget, query/update rate, and the cost metric that matters to the task.

## 6. Disposition ledger

| Claim | Disposition | Basis |
|---|---|---|
| R17 exact cells contain the R20 state/label point | **VALID** | Direct comparison with both embedded manifest payloads and exact rational endpoints. |
| MASTER-derived symmetric equations for both held actions | **VALID** | Substitution into §§6–11; symmetry follows from equal point data and uniqueness. |
| Positive-voltage bootstrap and `J<=367/7680<1/20` | **VALID** | Inward boundary checks, `i<=t`, variation of constants, and exact rational arithmetic. |
| Zero-voltage energy bound and `J<1/20` | **VALID** | MASTER energy identity and sign-preserving `clip`; strict initial energy derivative. |
| Contact/collision admissibility of each exact witness path | **VALID** | Explicit positive reserve and obstacle-distance inequalities above. |
| Strong task-selection use of R17 indices 62/74 | **BLOCKER** | Positive action is truly below threshold at an admissible point; no sound all-cell task-eligible proof exists for this pair. |
| A different useful, robust voltage-selection challenge | **UNVERIFIED** | A nominal screen exists, but task, nontrivial operating cell, and owner threshold/cost inputs are absent. |
| Archived R17 statuses, R5 study, and G4 evidence | **UNCHANGED / NOT_RUN** | Both saved R17 rows remain `VALID_UNKNOWN`; study remains 800/800 `NOT_RUN`; no G4 action. |

**R21 decision:** accept the limited R20 pair-feasibility counterexample. Retire only the consumed 62/74 pair as a strong task-selection target. Keep G2/G3/G4 and practical voltage-selection usefulness **UNVERIFIED**.
