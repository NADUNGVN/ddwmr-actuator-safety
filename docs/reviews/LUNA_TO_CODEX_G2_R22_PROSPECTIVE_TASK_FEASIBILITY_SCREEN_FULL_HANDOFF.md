Session: DDWMR | LUNA-G2-SCOPE

# G2 R22 — positive-width prospective task-feasibility screen

**Date:** 2026-10-06  
**Disposition:** **VALID** as a synthetic, full-hold analytic separation on one very narrow positive-width cell. The mathematical threshold interval is nonempty, but it is not a task specification or practical-usefulness result. **UNVERIFIED** for a meaningful operating domain, platform correspondence, G2, and cost.  
**Execution:** zero native rows, workers, stages, retries, G4 comparisons, or 800-row study queries. No manifest or query IDs were created. R5 remains **800/800 `NOT_RUN`**. R17–R21 and G4 evidence remain untouched; **G4 stays paused**.

## 1. Question and exploratory ledger

This report screens exactly one pair of held voltages on a shared state cell of positive width and a shared execution-fixed parameter set of positive width. The candidate extends the R21 rest-point calculation by perturbation bounds; no saved row result was used as a selection criterion. The R21 Codex review and handoff were consulted as required. The formal obstacle geometry below is a declared synthetic screen, not a claimed operating scene.

**Source basis:** `research_context/MASTER_RESEARCH_CONTEXT_v2.md` §§5–12 for the state, kinematics, slip, contact, body, wheel, and electrical equations; `docs/reviews/CODEX_G2_R21_PAIR_FEASIBILITY_ADVERSARIAL_AUDIT_REVIEW.md` and `docs/reviews/LUNA_TO_CODEX_G2_R21_PAIR_FEASIBILITY_ADVERSARIAL_AUDIT_FULL_HANDOFF.md` for the accepted nominal rest screen and scope limits. The four canonical `research_context/` files and `AGENTS.md` were also read. All bounds below are freshly derived for the declared positive-width candidate from MASTER, not copied as an all-cell result from R21.

| Candidate | Definition | Ledger status |
|---|---|---|
| A — R21 exact rest | Singleton rest point, all labels 1; `(1,1)` versus `(0,0)` | Retained as the nominal comparison only; it has no positive-width robustness claim. |
| B — R22 positive-width rest neighborhood | Cell and pair specified below; same nominal point and pair as A | Screened here; no later candidate was substituted and no manifest was made. |

## 2. Candidate declaration — fixed before bounds

The state order is MASTER v2.1's `[p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R]`. Let `eta=10^-6`. The initial-state cell is

\[
X_0=[-\eta,\eta]^9.
\]

Thus each coordinate has full width `2 eta = 1/500000`, including both pose coordinates, body speed/yaw rate, both wheel rates, and both currents. These are synthetic normalized widths, not measured uncertainty specifications.

Let the execution-fixed joint parameter-label cell be the product

\[
\Theta_{lab}=[1-\eta,1+\eta]^{12},
\]

with label order `(rho_L,C_L,lambda_L,R_L,B_L,k_L,rho_R,C_R,lambda_R,R_R,B_R,k_R)`. Every label has positive width `2 eta`. Labels are selected once per trajectory and held fixed over the whole hold; the same product set is used for both actions. The declared maps are

\[
m=I_z=R_w=b=v_s=c_u=c_r=1,\quad
J_j=1/\rho_j,\quad L_j=\lambda_j,
\]

with `C_j,R_j,B_j,k_j` equal to their labels. This retains the `rho_j`–`J_j` dependence. To make the effective shaft values consistent with MASTER §10, use direct drive `n_j=1`, `J_{wheel,j}=1/2`, `J_{motor,j}=1/rho_j-1/2>0`, `B_{wheel,j}=0`, `B_{motor,j}=B_j`, and `k_j^m=k_j`. There are no other cross-label correlations; left/right labels vary independently but remain fixed within each trajectory.

The known traction shape is `phi(z)=clip(z,-1,1)` with `L_phi=1`. Use the synthetic normalized voltage limit `V_max=1`, the same ideal obstacle for both actions with center `p_o=(1/5,1/20)` and radius `R_s=3/50`, and the same hold `T=1/4 s`. The only changed field is the held voltage:

| Role | Held voltage |
|---|---|
| Positive action | `V_+=(1,1)` |
| Baseline action | `V_0=(0,0)` |

The task quantity under examination is signed inertial-x displacement `J=p_x(T)-p_x(0)`, from MASTER's exact identity `J=∫₀ᵀ u cos(theta) dt`. **No `delta_task` is declared in this screen.**

## 3. Nominal dynamics derived from MASTER

At the cell center `x_*=0` and labels all 1, symmetry preserves `r=theta=0`, equal wheel rates `w`, and equal currents `i`. With `q=w-u`, MASTER §§6–11 reduce under `(1,1)` to

\[
\dot u=2q-u,\qquad \dot q=i-4q,\qquad \dot i=1-i-u-q,
\]

while the clip is unsaturated. Starting from rest, a first-exit argument gives `u,q,i>=0`; `i<=t`, `q<=t^2/2`, and `u<=t^3/3` for `0<=t<=1/4`, hence `q<=1/32<1` and the unsaturated branch is self-consistent. Also `u+q<=7/192`, so at `i=0` the current derivative is strictly positive.

For a rational lower bound, `i_dot>=137/192`, hence `i(t)>=(137/192)t`. Variation of constants and `e^{-z}>=1-z` give

\[
q(t)\ge \frac{137}{192}\left(\frac{t^2}{2}-\frac{2t^3}{3}\right)
\ge \frac{137}{576}t^2,
\]

\[
u(t)\ge \frac{137}{288}\left(\frac{t^3}{3}-\frac{t^4}{12}\right)
\ge \frac{685}{4608}t^3.
\]

Together with the upper comparison `u<=t^3/3`, this yields the nominal bounds

\[
\frac{685}{4718592}\le J_{+,*}\le\frac1{3072}\quad\text{at }T=1/4.
\]

The exact nominal `(0,0)` trajectory stays at rest and has `J_{0,*}=0`. These are analytic inequalities for two nominal trajectories, not numerical traces.

## 4. Uniform state/parameter tube for the positive-width cell

Here `||.||_∞` is the unscaled maximum norm on the nine coordinates. The constants below are rational outward bounds; no interval rounding is needed.

### 4.1 A priori domain

For all labels in `Theta_lab`, `C,rho,k,B<2`, `lambda>1/2`, and `|phi|<=1`. For either voltage and `R(t)=||x(t)||_∞`, MASTER's equations imply the upper Dini bound

\[
D^+R\le 8R+4.
\]

The initial norm is at most `eta`, so scalar comparison gives

\[
R(t)\le(\eta+1/2)e^{8t}-1/2
<(\eta+1/2)9-1/2=4+9\eta<5,
\]

for `t<=1/4`, using `e<3`. Thus every trajectory considered remains in `D=[-5,5]^9` throughout the hold. The right-hand side is locally Lipschitz, and this finite a priori bound gives existence and uniqueness through the complete hold for every declared initial state and fixed label vector.

### 4.2 State and parameter sensitivity

For a fixed label vector, the clip is globally 1-Lipschitz. On `D`, `C_j<1.01` and `|sigma_j|` has state row sum at most 3, so each force has state-Lipschitz row sum less than 4. The kinematic pose rows have row sum at most 6; the body and yaw rows at most 9; wheel rows at most `1.01(1.01+1.01+4)<7`; and current rows at most `2.02/0.99<3`. Hence `||f(x;vartheta,V)-f(y;vartheta,V)||_∞<=9||x-y||_∞` on D.

At a fixed state in D, changing the twelve labels from their center by at most `eta` changes the force by at most `eta`; the body/yaw row changes are at most `2 eta`. For a wheel row, the `rho,k,B,C` changes together contribute less than `23 eta`; for a current row the `lambda,R,k` changes contribute less than `23 eta`. Thus the parameter row bound `30 eta` is conservative and valid for either fixed voltage. This accounts for the effective `J=1/rho` map by writing the wheel equation as `omega_dot=rho(k i-B omega-F)`.

For any one fixed `vartheta in Theta_lab`, compare its trajectory from any `x_0 in X_0` to the nominal trajectory for the **same held action** from `(x_*,vartheta_*)=(0,1)`. The common parameter vector is constant along that trajectory; the comparison does not switch or reselect labels over time. With `E(t)=||x(t)-x_*(t)||_∞`,

\[
D^+E\le9E+30\eta,\qquad E(0)\le\eta.
\]

Gronwall and `e^{9/4}<12` (from `e<3` and `3^{1/4}<4/3`) give the uniform full-hold tube

\[
E(t)\le\eta e^{9t}+\frac{30\eta}{9}(e^{9t}-1)
<\frac{146}{3}\eta<\bar E:=\frac{49}{10^6},\qquad 0\le t\le1/4.
\]

The same `Ebar` applies to every initial state, every fixed parameter vector, and both actions.

## 5. Full-hold task, collision, and contact bounds

The statements in this section are uniform over `X_0 × Theta_lab` and all `t in [0,T]`.

### 5.1 Terminal progress

For the baseline nominal rest path, `u_*=0`; the tube gives `|J_0|<=T Ebar=49/4000000`. Therefore

\[
J_0\in\left[-\frac{49}{4000000},\frac{49}{4000000}\right].
\]

For the positive action, `|u_*|<=1/192` and `theta_*=0`. By `|cos(theta)-1|<=|theta|` and the tube, the integrand difference is at most `Ebar(1+1/192)<2 Ebar`; thus `|J_+-J_{+,*}|<=Ebar/2`. Combining this with the nominal rational bounds yields

\[
J_+\in\left[
\frac{685}{4718592}-\frac{49}{2000000},
\frac1{3072}+\frac{49}{2000000}
\right]
=\left[\frac{8896789}{73728000000},\frac{16801}{48000000}\right].
\]

In particular, the full-cell progress gap is

\[
J_+^- - J_0^+
=\frac{7993621}{73728000000}\;\text{m}
\approx 0.0001084204\;\text{m}.
\]

### 5.2 Full-hold collision clearance

The nominal positive path has `p_y=0` and `0<=p_{x,*}(t)<=1/3072`; the nominal baseline remains at the origin. The tube puts actual position coordinates within `Ebar` of these references. Using horizontal separation alone as a lower bound on Euclidean distance gives

| Action | Uniform lower bound on `distance-to-obstacle - R_s` |
|---|---:|
| `(1,1)` | `> 7/50 - 1/3072 - 1/1000 = 53251/384000 m` |
| `(0,0)` | `> 7/50 - 1/1000 = 139/1000 m` |

Both bounds are positive and hold continuously for the complete hold, not only at the endpoint.

### 5.3 Full-hold contact margin and saturation

For both nominal paths, `r_*=0`; the positive nominal slip is `q<=1/32`, and the baseline slip is zero. In the perturbed cell each slip differs from its nominal slip by at most `3 Ebar`, since `sigma_L=omega_L-u+r` and `sigma_R=omega_R-u-r`. Hence for either action and either wheel,

\[
|\sigma_j|\le 1/32+3\bar E<1/16<1.
\]

The actual slips therefore remain strictly inside the clip's linear region. No derivative or Lipschitz assumption is made about the square-root contact margin at saturation. Directly from MASTER §8, `a_j=C_j sqrt(1-phi(sigma_j)^2)`. Since `C_j>1-eta>99/100` and `sqrt(1-(1/16)^2)>15/16`, each reserve is greater than `297/320`, so their sum is greater than `297/160`.

For the positive action, `|u|<=1/192+Ebar<1/100`, `|r|<=Ebar<1/1000`, giving `|u r|<1/100`. For the baseline, `|u|,|r|<=Ebar`, also giving `|u r|<1/100`. With `m=1`, both actions consequently satisfy the whole-hold contact margin bound

\[
c=a_L+a_R-|m u r|>\frac{297}{160}-\frac1{100}
=\frac{1477}{800}>0.
\]

This checks the formal algebraic contact domain directly and does not differentiate its square root.

## 6. Threshold interval and scientific meaning

The rigorously enclosed interval

\[
J_{baseline}^+<\delta_{task}\le J_{positive}^-
\]

is nonempty:

\[
\frac{49}{4000000}
<\delta_{task}\le
\frac{8896789}{73728000000}\quad\text{m}.
\]

The gap has the positive rational width reported above. Because both sides are sound full-cell trajectory bounds, this nonempty interval reflects a true robust progress separation in this synthetic reduced-model cell, not just a gap between loose estimates. It remains only a **possible threshold interval**. No value inside it is selected or represented as a user task requirement. A baseline robust upper bound below a separately specified threshold would show the baseline actually misses that task on the cell; a baseline lower bound alone would not.

The action difference follows through the plant rather than an algebraic voltage-to-body-speed shortcut: voltage first changes `i_dot=(V-R i-k omega)/L`, current changes `omega_dot=(k i-B omega-R_w F)/J`, wheel/body relative speed changes `sigma`, clip force changes `F`, and body acceleration changes through `u_dot=(F_L+F_R-c_u u)/m`. At the center, zero voltage leaves rest invariant; positive voltage builds current, then wheel rate and slip force, then positive body progress. The tube shows this mechanism survives the declared nonzero cell widths.

This is more informative than the R21 exact-rest screen only in the mathematical sense that every one of the nine state coordinates and all twelve parameter labels now has nonzero width, and the same bounds certify both actions over that product set. It is not a practically useful operating-domain result: each width is only `2e-6` in the chosen normalized coordinates, the guaranteed gap is about `0.108 mm`, and all nominal physical values are synthetic. The scene, voltage scale, contact capacities, actuator constants, and uncertainty widths have no platform provenance; no runtime/cost comparison was made. Physical correspondence, measured parameter ranges, and actual support/contact mechanics remain unavailable.

## 7. Recommended next decision and disposition

**Recommend: request owner task/domain inputs.** The analytic screen is complete for this one pair and should not be expanded into a manifest until the owner supplies a meaningful displacement task and an operating domain. Required inputs are:

1. Task direction, minimum displacement in meters, and deadline/hold duration, declared independently of this computed interval.
2. A physically motivated positive-width initial-state domain, obstacle scene, voltage limit, and fixed joint parameter set/correlations. For any physical-platform claim, provide support/contact and actuator evidence mapping that domain into MASTER's reduced model.
3. For a cost claim, the baseline, platform, execution/query rate, time budget, and decision-relevant cost metric.

| Claim | Disposition | Reason |
|---|---|---|
| One shared positive-width state and parameter cell is analyzed | **VALID** | All nine state widths and all twelve label widths are `2e-6`; labels are fixed per trajectory. |
| Both actions have full-hold progress, collision, and contact bounds | **VALID, synthetic** | Exact rational comparison bounds and direct all-time predicate margins above. |
| `J_baseline^+ < delta <= J_positive^-` can hold mathematically | **VALID, possible interval only** | Nonempty robust interval; no task threshold selected. |
| Task relevance, practical width, physical correspondence, cost, G2 | **UNVERIFIED** | Owner task/domain/provenance inputs and broader evidence are absent. |
| Query/manifest/solver execution | **NOT RUN / NOT CREATED** | This assignment is derivation only; no IDs were allocated. |

Overall disposition remains **HOLD**; **G1 PASS only for the restricted reduced model**; **G2/G3/G4 and physical-platform correspondence UNVERIFIED**; **G4 remains paused**. The R17 indices 62/74 remain retired as a strong task-selection target; their archived records remain untouched. This exploratory calculation is not a certificate producer, a gate promotion, or authorization to execute a future query.
