Session: DDWMR | LUNA-G2-SCOPE

# G2 R20 — structured feasibility witness on the consumed R17 pair

**Date:** 2026-10-06  
**Disposition:** **DONE as a bounded feasibility attempt; STOP this degree-zero representation on the R17 pair.** The full-hold predicates do not pass for either action.  
**Execution:** zero new native queries, workers, or stages; R5 study remains **800/800 `NOT_RUN`**. No commit or push.

## Finding

I instantiated one exact-rational shared-state residual tube on the unchanged R17 indices 62 and 74. The predictor preserves the complete initial box as common variables, the whole fixed-label parameter image, and the same held voltage through each archived time slab. The residual and nine-state Lipschitz bounds close numerically, including a rational upper bound on the exponential tail. The resulting Grönwall position radius already makes the collision lower bound `-3/50` on the first slab of both rows. Row 62 also fails contact and progress; row 74 has a positive contact lower bound on slab 0, but fails collision on both slabs, contact on slab 1, and the whole-hold progress criterion.

The first blocking result in the assigned row order is therefore R5 index 62 / slab 0: the outward radius expands the initial position box across the obstacle center, so the sufficient distance lower bound is zero. This is an enclosure failure. It does **not** prove that either true trajectory collides or loses contact. I stop this constant-in-time predictor representation here; R20 does not build or test a higher-degree predictor.

## Scope, inputs, and identity

The assignment and the governing sources read for this work were:

- `AGENTS.md`, `research_context/MASTER_RESEARCH_CONTEXT_v2.md`, `DECISION_LOG.md`, `LITERATURE_MATRIX.md`, and `REVIEW_GATE.md`;
- `docs/reviews/CODEX_G2_R19_STRUCTURE_PRESERVING_ENCLOSURE_REVIEW.md` and `docs/reviews/LUNA_TO_CODEX_G2_R19_STRUCTURE_PRESERVING_ENCLOSURE_RESEARCH.md`;
- `docs/reviews/CODEX_G4_AUER_R22_CONTRIBUTION_FALSIFICATION_REVIEW.md`;
- the archived R17 source manifest/closure and records, plus the source-bound R10 model and R11 replay contract.

R17 selected the consumed development rows in this order. The raw hashes below were checked by the R20 prototype before calculation.

| R5 index | Query / held voltage | Canonical query SHA-256 | Input payload semantic SHA-256 | Saved R17 record SHA-256 |
|---:|---|---|---|---|
| 62 | `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_L0_R0`, `(0,0)` | `38839995032bd4328a7c4d1059d2e3e674f3f3586a12f6f2d6c76842dfcfa8f0` | `aacb6dd0639c5d5c603ca227066352a9d04a1d2d0e92fc77ab3499f59f10db37` | `316434ab6eacb7e221eca4feb1062001a8b576b450b725bbc1246d5e744f5cf3` |
| 74 | `S_LOW_NEG__D_OFFSET_LEFT__T_250MS__V_Lp1_Rp1`, `(1,1)` | `1bab855c36a6cba051736320002ea40370c793f57a04cc5a8454a71b79d2c858` | `b4ad72b1cf4e1fcc37de3bf3ed080ba4797e637e3f37919873df740043645c3b` | `fbb23303ff218e3ddf56453ccea7ca41a70d40f0ff1e85335341eff7e5651421` |

The checked R17 manifest and source-closure raw SHA-256 values are `a4913d3d0282de6a5d1a16c4c88e3c402a91f1c3dee2df1ea99afd44a71c6bb9` and `5b6838c8da6ae55e33ad4b50c9182122943f669e63e0fa9d92e6a8de3b83ce86`. The records are the R10 whole-hold Picard records saved at:

- `results/validation/g2/decision_domain_r17_go_entrypoint_correction_stage_v1/row_00/record.json`;
- `results/validation/g2/decision_domain_r17_go_entrypoint_correction_stage_v1/row_01/record.json`.

The source modules used or relied on are `validation/g2/model.py` (raw SHA-256 `93e9a96d640ad09a7eb7dbff51ebfb8f2d783296ce5afff57af41e81e30a8508`), `validation/g2/interval.py` (`e49e2e3880485d9a658e2435cfa06b784f98257b13c51fa4a2bf464f9c73e5c6`), `validation/g2/rational.py` (`8a2c16778b33898afd16c8da44945c2d41fd7d187cb11c7cb071745e68ed5c6e`), `validation/g2/time_slab_picard_r10.py` (`e9fa6672649d675e27bb4f419e28259b9546b01bb6592f3388396ecd2a211c47`), and `validation/g2/whole_hold_picard_checker_r11.py` (`2a794e8f46c4b029331a2548dccd1948b78d3f5d5d7a96efa118d9353ba56f7e`). These are the R19-reviewed raw pins in the inherited R17/R10 source closure; R20 adds no edits to them.

Both archived records have a complete closed-slab R10 proof and status `UNKNOWN`. The R17 handoff records the independent read-only R11 replay of both records and the stage audit at `results/validation/g2/r17_one_shot_execution_v1/independent_checker_audit_stdout.bin` (SHA-256 `4b53c8df2f474ff33633fc63257dc5ee37cd7f9920c3c129b35b1737d143c511`). R20 uses those replayed R10 boxes only as a domain aid. The prototype rechecks their hashes, input bindings, slab schedule, and recorded inclusion fields; it does not claim a second independent R11 replay.

The paired query inputs are identical in initial state cell, full parameter cell, obstacle, horizon, and task threshold; the held voltage is the changed field. Shared values are:

| Quantity | Exact value |
|---|---|
| Initial state order | `[p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R]` |
| Initial cell | `[-1/1000,1/1000]`, `[-1/1000,1/1000]`, `[-1/100,1/100]`, `[1/5,1/4]`, `[-1/50,0]`, `[0,1/4]`, `[0,1/4]`, `[-1/100,1/100]`, `[-1/100,1/100]` |
| Obstacle center and radius | `(1/5,1/20)`, `R_s=3/50` |
| Hold and task threshold | `T=1/4`, required progress `1/20` |
| Parameter labels | `rho_L,rho_R,C_L,C_R` in `[1,11/10]`; `lambda_L,lambda_R,R_L,R_R,B_L,B_R,k_L,k_R` in `[9/10,11/10]` |
| Fixed parameter maps | `m=I_z=R_w=b=v_s=c_u=c_r=1`; `J_j=1/rho_j`; `L_j=lambda_j`; remaining named parameters map to their labels |

Each parameter label denotes one fixed value for that trajectory across the complete hold. The R20 calculation uses the same whole parameter image on every slab and does not introduce parameter switching or reset a favorable value.

## Finite representation and arithmetic

For each row, define one closed leaf equal to the full product of the nine-coordinate initial-state box and all 12 declared label intervals. There is no subdivision, branch, or coverage gap. Use the rational predictor

\[
P_k(\xi,\tau)=x_0(\xi),\qquad 0\le\tau\le h_k,
\]

for every slab. It is degree zero in time and the identity polynomial in the shared initial-state coordinates. It has no parameter polynomial terms; the full parameter labels enter the defect and remain fixed through the hold. The same predictor value is used at adjacent slab boundaries, so the reset defect is exactly zero and the prior Grönwall radius is carried unchanged as the next slab's initial error.

The exact archived schedule is one `1/4` slab for row 62 and two contiguous `1/8` slabs for row 74. A 16th-degree positive Taylor sum plus a geometric remainder bounds `exp(x)` when `0 <= x < 18`:

\[
\exp_+(x)=\sum_{j=0}^{16}\frac{x^j}{j!}
+\frac{x^{17}}{17!}\frac{1}{1-x/18}.
\]

For the omitted terms, every later series ratio is at most `x/18`, so this is an exact rational upper bound. Here `Lh` is `19/10` for row 62 and `19/20` for each row 74 slab, both inside the stated range. Radius results are rounded upward to a dyadic grid no coarser than `2^-40`; square-root lower evaluations use 24 bisections.

The reproducible prototype is `validation/scripts/prototype_g2_r20_degree_zero_witness.py`. It checks the pinned manifest, R17 source closure, query and payload identities, record hashes, common paired inputs, and exact time coverage before producing bounds. Per-row caps are 8,192 rational bits, 500,000 budgeted rational operations, and 30 seconds. The saved R17 and G4 files are read-only inputs.

Prototype raw SHA-256 after these checks: `c4a86d61b3d22c303413a9c5635697175b8150bc60ef39e576c356c69ce3370e`.

## Nine-state Lipschitz and defect bounds

Let `D` be the closed coordinate box formed from the hull of the complete initial box and every R10 closed-slab Picard candidate/pose tube on that row. Each saved R10 candidate contains its complete slab tube under the reviewed R10 inclusion; the R17 R11 replay is the cited coverage evidence. This box is convex and contains both the R10 exact path and `P`. Its relevant speed bounds are:

| Row | `u` interval in `D` | `U = sup_D |u|` | Pose row bound `1+U` |
|---:|---:|---:|---:|
| 62 | `[-6301/2000,7201/2000]` | `7201/2000` | `9201/2000` |
| 74 | `[-5901/4000,7701/4000]` | `7701/4000` | `11701/4000` |

For any two states and each fixed label, clipping is globally 1-Lipschitz and sine/cosine are globally 1-Lipschitz. With `R_w=b=v_s=1`, `C_j^+=11/10`, each slip-force map satisfies

\[
|F_j(x)-F_j(y)|\le K_{F_j}\|x-y\|_\infty,
\qquad K_{F_j}=\frac{11}{10}(1+1+1)=\frac{33}{10}.
\]

The nine row-sum bounds are `L_px,L_py <= 1+U`, `L_theta=1`,
`L_u <= (K_FL+K_FR+c_u^+)/m^- = 38/5`,
`L_r <= (b^+(K_FL+K_FR)+c_r^+)/I_z^- = 38/5`,
`L_omega_j <= (k_j^+ + B_j^+ + R_w^+ K_Fj)/J_j^- = 121/20`, and
`L_i_j <= (R_j^+ + k_j^+)/L_j^- = 22/9`. Thus the outward nine-state infinity-norm Lipschitz bound is

\[
L_9=\max_i L_i=38/5
\]

on both convex domains `D`. This uses the same fixed label when taking state differences; the displayed parameter endpoints are uniform bounds over the complete label cell.

For `P=x0`, `\partial_\tau P=0`. Direct exact interval extension of the nine-state right-hand side over each full initial and parameter cell gives the following defect component ranges, in the nine-state order. The pose derivatives use only `|sin|,|cos|<=1`; no unbounded trigonometric or clip operation is left in the residual.

| Component | Row 62 whole-cell interval | Row 74 whole-cell interval |
|---|---:|---:|
| `p_x_dot`, `p_y_dot` | `[-1/4,1/4]` | `[-1/4,1/4]` |
| `theta_dot` | `[-1/50,0]` | `[-1/50,0]` |
| `u_dot` | `[-411/500,-17/250]` | `[-411/500,-17/250]` |
| `r_dot` | `[-33/100,197/500]` | `[-33/100,197/500]` |
| `omega_L_dot` | `[-3751/10000,847/2500]` | `[-3751/10000,847/2500]` |
| `omega_R_dot` | `[-3993/10000,1573/5000]` | `[-3993/10000,1573/5000]` |
| `i_L_dot`, `i_R_dot` | `[-143/450,11/900]` | `[357/550,337/300]` |
| `rho = sup ||dot P-f(P,V;vartheta)||_infinity` | **`411/500`** | **`337/300`** |

These are full-cell outward ranges, not point samples. They use the fixed voltage `(0,0)` or `(1,1)` assigned to the whole row, respectively. No derivative of `clip` or of the square-root contact reserve is used.

## Slab carry and all full-time predicate bounds

On each slab use

\[
E_{k+1}^{raw}=\exp_+(Lh_k)E_k+\rho\frac{\exp_+(Lh_k)-1}{L},
\]

then round upward to the stated dyadic grid. The resulting radii enclose the entire closed slab because the comparison bound is nondecreasing in time. At a boundary, `P_(k+1)(xi,0)=P_k(xi,h_k)=x0(xi)`, so there is no reset error; `E_(k+1)` begins with the previous rounded radius.

For each slab, the collision test expands both predictor position intervals by the **entire** `E`. Contact is evaluated by direct interval composition of both clipped slips, each square-root reserve, and `m|ur|`, with the same full error expansion. The task test expands `u` and `theta`; the global range `cos(theta) in [-1,1]` safely encloses every expanded heading. These bounds are deliberately simple and lose dependence in the residual cube, but none omits its radius.

| Row / slab | `h` | `Lh`, `exp_+(Lh)` | `E_start -> E_end` | Collision margin lower | Contact margin lower | Progress contribution lower |
|---|---:|---|---|---:|---:|---:|
| 62 / 0 | `1/4` | `19/10`; `3828722643900072919843183555115879 / 572656759234560000000000000000000` | `0 -> 676171473429/1099511627776` | **`-3/50`** | `-16599656446918358798245649/30223145490365729367654400` | `-951049380373/4398046511104` |
| 74 / 0 | `1/8` | `19/20`; `68511161104692643151000254051724920873 / 26496076563685048320000000000000000000` | `0 -> 257702452777/1099511627776` | **`-3/50`** | `12377876875824002618400727/30223145490365729367654400` | `-532580359721/8796093022208` |
| 74 / 1 | `1/8` | `19/20`; same exact exponential bound as row 74 / 0 | `257702452777/1099511627776 -> 115505771769/137438953472` | **`-3/50`** | `-443056964685615291731657/472236648286964521369600` | `-149865510137/1099511627776` |

The direct contact interval components show where reserve separation is retained and where it is lost:

| Row / slab | Clipped slip intervals `(L; R)` | Reserve lower `(L; R)` | Body-demand upper `D^+` | Contact margin lower |
|---|---|---:|---:|---:|
| 62 / 0 | `[-1,1];[-1,1]` | `(0,0)` | `16599656446918358798245649/30223145490365729367654400` | `-16599656446918358798245649/30223145490365729367654400` |
| 74 / 0 | `[-26749387445763/27487790694400,4140414698599/5497558138880]`; `[-1047985265275/1099511627776,21251829306883/27487790694400]` | `(3862561/16777216,317235/1048576)` | `3723970774143149052485673/30223145490365729367654400` | `12377876875824002618400727/30223145490365729367654400` |
| 74 / 1 | `[-1,1];[-1,1]` | `(0,0)` | `443056964685615291731657/472236648286964521369600` | `-443056964685615291731657/472236648286964521369600` |

This direct interval composition does **not** provide a genuinely joint Taylor range for the full contact function: the residual cube and interval multiplication still relax state correlations. It avoids R19's zero-reserve result specifically on row 74/slab 0 because both expanded clipped slip intervals stay strictly inside `[-1,1]`; the computed reserve lower bounds are then positive. The same saturation loss remains on row 62/slab 0 and row 74/slab 1. Even the improved row 74/slab 0 contact margin cannot rescue its negative collision margin.

The exact total task lower bounds are:

| Row | Total `J^-` | Frozen requirement | Result |
|---:|---:|---:|---|
| 62 | `-951049380373/4398046511104` | `1/20` | fails |
| 74 | `-1731504440817/8796093022208` | `1/20` | fails |

As an explicit collision check, the initial position cell is `[-1/1000,1/1000]^2`. On row 62, `E_0 > 201/1000` and `E_0 > 51/1000`; on row 74/slab 0, the same strict inequalities hold. Hence the expanded coordinate intervals contain obstacle center `(1/5,1/20)`, both coordinate gaps are exactly zero, distance lower is zero, and the margin is exactly `0-3/50=-3/50`. For row 74/slab 1 the radius is larger and the same conclusion follows. A zero distance lower from an outer set is inconclusive about the true path.

## Comparison with archived R17 and R19 bounds

The R20 table above is compared with the exact archived R17 row records and the R19 contraction handoff for the same input cells and actions. R17/R19 values below are not new validation data.

| Row / slab | R17 collision / contact | R19 collision / contact | R20 collision / contact |
|---|---|---|---|
| 62 / 0 | `-3/50`; `-23885717/4000000` | `-201891306255167/3518437208883200`; contact reserve `0`, demand `0.714417–0.714418` | `-3/50`; approximately `-0.549237` (exact fraction above) |
| 74 / 0 | `-67047611924271/1759218604441600`; `-25852257/16000000` | `+143968592365329/1759218604441600`; contact reserve `0`, demand `0.165771–0.165772` | `-3/50`; approximately `+0.409550` (exact fraction above) |
| 74 / 1 | `-3/50`; `-991988257/655360000` | `-16155869176723/879609302220800`; contact reserve `0`, demand `0.581933–0.581934` | `-3/50`; approximately `-0.938210` (exact fraction above) |

For exact R19 contact-margin values, the R19 handoff gives:

| Row / slab | R19 contact margin lower |
|---|---:|
| 62 / 0 | `-804363101269925426357/1125899906842624000000` |
| 74 / 0 | `-15545814828495078235801531282739374122423347040288614005471670365185041339001164933113/93778296809785602500326041059328000000000000000000000000000000000000000000000000000000` |
| 74 / 1 | `-477245661116309209152810879897118739052905677099700886272581312663049979932368659818134996295226511541871439/820102751250246121894274084667900875057053645878067200000000000000000000000000000000000000000000000000000000` |

R20's contact tube is tighter than R19 on row 74/slab 0, but its constant pose predictor cannot move with the trajectory: its full residual radius swallows the collision clearance on that same slab. On row 62 contact remains negative. The residual-box relaxation therefore supplies no full-hold positive result. R20 progress is also below the threshold on both rows. For reference, the archived R17 total progress lower bounds were `-6301/8000` (row 62) and `-322837/1024000` (row 74); R19 improved them to `-19685271901/134217728000` and `-1038229544751489153144496499988278335958285043496181281/12548295830113635610059079680000000000000000000000000000`, respectively. R20 remains negative on both.

The R17 `UNKNOWN` results, negative lower bounds, and R20 zero-distance outer boxes do not prove an unsafe trajectory. None of these consumed development rows establishes useful voltage selection or counts as fresh validation.

## DDWMR dependence, prior-art scope, and work size

The instance is tied to this DDWMR model through its nine-state kinematics, motor/wheel/body equations, wheel-slip coordinates, clip force law, fixed parameter-label maps, and algebraic contact margin. The calculated `L`, `rho`, and predicate values depend on those source-bound equations and these exact two archived inputs.

The proof pattern itself—polynomial comparison path, defect tube, Lipschitz bound, and Grönwall carry—is generic validated-IVP machinery. R20 establishes no new generic theorem and no DDWMR-specific advantage over the Auer reconstruction. The R22 G4 review retains the pause on new comparisons because no plant-specific effect or prospective cost advantage has been demonstrated. No novelty claim follows from these calculations.

The attempted representation is small: one leaf per row, nine identity predictor components, one or two slabs, no branch-and-bound, no Taylor terms in time, and exact residual/range operations. The prototype reports 1,723 budgeted rational operations and 312 maximum observed bits for row 62; 2,197 operations and 457 maximum observed bits for row 74. Both are well below the disclosed per-row caps. This is computationally manageable but too conservative to certify the target conjunction.

## Decision and status ledger

| Claim | Status | Reason |
|---|---|---|
| Saved R17 inputs and record bindings | **VALID for this offline attempt** | Pinned query/payload/record hashes, common paired fields, R17 manifest/closure hashes, and exact slab coverage checked by the prototype. |
| Nine-state Lipschitz bound and full-cell degree-zero defect | **VALID as exact outward development bounds** | Source-defined clip Lipschitz law, exact rational parameter intervals, and the row bounds and defect intervals shown above. |
| Grönwall radii and endpoint carry | **VALID for the stated comparison construction** | Rational geometric exponential tail, outward dyadic radius, zero predictor reset defect, and explicit same-row slab carry. Domain coverage relies on the archived R10 tubes and their R11 replay evidence. |
| Full-hold collision/contact/task certification | **NOT ESTABLISHED** | Collision is negative on every slab; contact fails for row 62 and row 74/slab 1; both total progress bounds are below `1/20`. |
| Actual collision, contact loss, or unsafe true trajectory | **UNVERIFIED** | A failed sufficient bound is not a trajectory counterexample. |
| Continued use of this constant predictor on R17 | **STOP** | It loses the collision separation on the first slab in row order and cannot satisfy the complete action test. R20 performs no higher-degree repair. |
| G2/G3/G4, physical-platform correspondence, and voltage-selection usefulness | **UNVERIFIED** | The pair is consumed development evidence; no fresh task distinction, recursion result, physical mapping, or novelty result is provided. |
| R5 800-row study | **NOT_RUN** | No study query or native work was performed. |

**Final decision:** stop this degree-zero shared-variable residual representation on the two R17 development rows. Its exact blocking bound is the collision distance lower `0` and margin `-3/50` caused by the carried radius; the other failed predicates are listed slab by slab above. Do not interpret this as a finding that the true path is unsafe, and do not extend this R20 attempt to new rows or the 800-row study.

## Reproduction

From the repository root:

```text
python -m validation.scripts.prototype_g2_r20_degree_zero_witness
```

The script prints the complete exact rational record to stdout and writes no query or stage artifacts.
