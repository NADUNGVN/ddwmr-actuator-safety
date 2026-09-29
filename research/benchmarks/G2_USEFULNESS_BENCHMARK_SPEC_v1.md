# G2 usefulness benchmark — proposed protocol v1

2026-09-29. **DRAFT FOR REVIEW; NOT LOCKED; NO RESULTS.** MASTER v2.1 remains authoritative. G1 restricted PASS; G2/G3/G4 UNVERIFIED; HOLD. This is a synthetic mathematical benchmark proposal under analytic G2 authority, not implementation authorization or a physical parameter identification.

## 1. Question and scope

Does a voltage-dependent certified enclosure give usable one-hold collision/contact certificates on nonzero-width moving-state regions, with independent uncertain actuators, at a defensible finite work cost? Can its structured kernel improve certification relative to matched alternatives?

The first question is G2 usefulness; the second is a possible contribution hypothesis requiring the separate G4 comparison. Neither is answered here. Passing one easy cell is not automatically sufficient evidence of usefulness. No selected action is executed, no trajectory is tracked, and no K_T or repeated-hold safety is constructed.

Initial cells represent a batch of exact sampled initial states. Requiring a common held voltage to certify a whole cell is an offline sufficient test stronger than the pointwise information assumption; it does not introduce an estimator or change MASTER.

## 2. Synthetic parameter family and units

Use SI units and one-unit coordinate reference scales before matrix norms: metres, radians, metres/second, radians/second and amperes in the relevant coordinates; reference time is one second. Numeric ones below denote coefficients with the units required by MASTER, not a dimensional identification of unrelated quantities.

Known coefficients:

\[
m=I_z=R_w=b=v_s=c_u=c_r=1,\quad V_{\max}=1,
\qquad \phi(q)=\max(-1,\min(q,1)),\quad L_\phi=1.
\]

For each side independently, use fixed labels

\[
\rho_j,C_j\in[1,11/10],\qquad
\lambda_j,R_j,B_j,k_j\in[9/10,11/10],
\qquad J_j=1/\rho_j,\quad L_j=\lambda_j.
\]

Thus the label domain is a 12-dimensional rational box. Its image in physical parameters is the declared family; do not treat J and rho as independent. R denotes winding resistance here, not obstacle radius. The two sides need not match. All labels remain fixed throughout the entire hold and across verification subdivisions. A voltage is common to all labels.

An ideal gear witness is n_j=10, k_j^m=k_j/10, J_wheel,j=1/10, J_motor,j=(1/rho_j-1/10)/100, B_wheel,j=0, B_motor,j=B_j/100. Every rotor inertia is positive since 1/rho_j>=10/11>1/10. This witnesses the formal conventions; it identifies no actual motor or robot. No gear relation is asserted for the independently stipulated electrical inductance.

These order-one values deliberately define a nonstiff synthetic benchmark. Hardware relevance and stiffness robustness remain outside any result on this family. Later literature-backed data or a stiff family require a separate version/provenance record, not relabeling these data.

## 3. Six original state cells

All cells have

\[
p_x,p_y\in[-1/100,1/100],\quad
\theta\in[-1/20,1/20],\quad i_L,i_R\in[-1/10,1/10].
\]

Choose one speed interval U and one yaw interval R from

\[
U\in\{[1/5,3/10],[3/5,7/10]\},
\]
\[
R\in\{[-1/5,-1/10],[-1/20,1/20],[1/10,1/5]\}.
\]

Let u_c and r_c be their exact rational midpoints. Set independently

\[
\omega_L\in[u_c-r_c-1/10,u_c-r_c+1/10],\qquad
\omega_R\in[u_c+r_c-1/10,u_c+r_c+1/10].
\]

Together these form six full nine-dimensional boxes, with nonzero width in every state coordinate and strictly positive body speed. The wheel bounds only center each cell around rolling kinematics; they do not impose exact rolling or initial-state correlations. Both signed turning families are retained.

These initial boxes are not selected from favorable evaluator outputs. They may produce UNKNOWN. Input validity and initial contact/collision admissibility must not be conflated: a well-formed state cell that cannot be certified initially remains a tested cell. No silent removal is permitted.

## 4. Geometry and hold durations

Use one static obstacle per scene, inflated collision radius R_s=1/2 m. Positions are

\[
p_o=(R_s+d,\ell),\quad
d\in\{1/50,1/20,1/10,1/5\},\quad
\ell\in\{-1/5,0,1/5\}.
\]

The values span a declared range of frontal clearance and both lateral offsets. They are chosen before any compared enclosure is evaluated; none is adjusted to sit between observed tube widths. There are 12 scenes. Pose uncertainty belongs to each original state cell and must be retained by every method.

Hold durations are

\[
T\in\{1/50,1/20,1/10\}\ \mathrm{s}.
\]

Each duration defines a separate fixed-period one-hold question, not a change of voltage during the hold. Internal time subdivisions are verification work, never controller updates.

## 5. Admissible action list and decision context

Evaluate all nine actions

\[
\mathcal V_{\mathrm{bench}}=\{-1,0,1\}^2\ \mathrm{V}.
\]

The common offline query is which held voltages, if any, this evaluator certifies during forward motion near an obstacle. Include symmetric positive, zero, negative and differential actions. Negative voltage is not assumed to brake immediately, and zero voltage is not assumed to be a safe backup.

Report the full action-status vector for each original state/scene/horizon combination. A difference between CERTIFIED and UNKNOWN is a difference in sufficient-test outputs, not proof that one action is physically necessary or another unsafe. No artificial task-performance score or closed-loop tracker is introduced.

There are 6 x 12 x 3 = 216 original state/scene/horizon queries, and 216 x 9 = **1944 original state-action queries per method and declared work configuration**. All share the complete parameter family.

## 6. Methods and finite work settings

The evaluator specification must supply outward arithmetic and full-hold checking for every listed method. Proposed internal variants are: global comparison, one exact-kernel refinement, and conservative finite-cell fallback, with predictor depth n=1. **Only the fallback currently has a finite-recipe draft. General finite evaluation of the sharper global/refined variants remains OPEN.** These are proposed comparison obligations, not three ready evaluators. If n=0 or n=2 is later included, predeclare it as a distinct ablation for every query before evaluation; do not substitute it only on favorable cells.

Use a common initial cell and complete label domain, the same collision/contact checker, and the same mathematical precision policy. Comparison families must also include a reviewed generic Lipschitz enclosure and, before external superiority claims, an applicable established validated integrator. See `../../docs/reviews/G4_MATCHED_PRIOR_ART_COMPARISON_v1.md`. External baseline choice/configuration is **OPEN**, not an implemented comparator.

Proposed bounded work ladder for review:

| Level | Maximum depth per original initial/parameter cell | Uniform time slabs | Normalized integral panels | Exponential/trig polynomial degree | Root bisections |
|---|---:|---:|---:|---:|---:|
| W0 | 0 | 2 | 2 | 12 | 24 |
| W1 | 2 | 4 | 4 | 20 | 40 |
| W2 | 4 | 8 | 8 | 32 | 56 |

Depth is total binary bisection depth along a leaf, not depth per coordinate. Split the widest coordinate after division by its original width, tie-breaking by the declared coordinate order (state order of MASTER, then rho_L,C_L,lambda_L,R_L,B_L,k_L,rho_R,C_R,lambda_R,R_R,B_R,k_R). Initial-state and parameter cells have separate depth caps. Parameter leaves are universal obligations, not independently selectable alternatives. These numbers are proposed finite effort settings, not a runtime claim or equal-cost assertion across methods.

Before lock, align each primitive parameter with the reviewed finite evaluator and specify a global operation/bit-resource cap. These details are **OPEN pending evaluator review**. If a primitive prerequisite fails within a cap, return UNKNOWN with the reason; never silently increase work on selected methods. Runtime measurement requires separate authorization. Equal polynomial degree alone is not equal computational cost: report actual counts and, later, measured cost as well.

The current fallback draft uses whole-hold predictor hulls. Repeating that same hull on smaller time slabs does not establish localized improvement; the panel/slab ladder is not evidence that this draft becomes tighter. A localized range recipe and general refined-radius recipe require review before comparison configurations depending on them can be locked.

## 7. Aggregation and metrics

For a common voltage, an original query is CERTIFIED only when every initial-state leaf, every parameter leaf and every complete time slab passes every obstacle/contact check. Any unresolved valid leaf makes that original query UNKNOWN. Endpoint inclusion alone is insufficient. Shared cell boundaries must be covered; no favorable-label or favorable-initial-state selection is allowed.

Report at least:

- certification coverage over all 1944 valid original queries, plus per speed/yaw/clearance/horizon strata;
- fraction of the 216 state/scene/horizon queries with at least one certified action;
- full nine-action status vectors and all-action-UNKNOWN count;
- full-hold lower collision/contact margins, including negative sufficient lower bounds as inconclusive bounds;
- center range widths, error radii and total pose/internal enclosure widths separately;
- per-variant budget reductions and output changes on identical original queries;
- initial/parameter leaf counts, time slabs, primitive calls, rational bit lengths and termination reasons;
- runtime only after authorized implementation, with environment/version and timing protocol recorded.

Subdivision never increases the denominator or converts correlated cells into independent statistical samples. INVALID_INPUT means a violation of the effective representation contract, not a negative safety margin. A declared but invalid query requires a disclosed protocol correction and new version before lock. Implementation failures are reported separately with the original denominator retained; they are not quietly counted as mathematical UNKNOWN or dropped.

## 8. Lock and outcome interpretation

This proposal is **NOT LOCKED**. Lock requires independent review of the finite evaluator, primitive/resource settings and baseline applicability. Archive the exact protocol, immutable commit and a future machine-readable manifest before producing outputs. No evaluator is run in this drafting phase.

No minimum coverage threshold or runtime target has been scientifically justified yet. That is an explicit acceptance-policy gap; a threshold must not be selected after seeing outputs. The eventual evidence must show a declared nonzero-width moving region with usable certificates and transparent cost, not merely a singleton success. A mixed outcome warrants a scoped result; all UNKNOWN leaves usefulness unestablished. A matched generic method matching or dominating coverage/width/cost would undermine the proposed advantage on this benchmark.

Do not choose publication examples first and hide the full grid. Any changes after lock create a new protocol version, retain previous outputs and explain the reason. Development data, if later authorized, must be separate from the locked comparison grid. Synthetic certification alone never proves physical-platform safety, recursion, practical deployment or novelty.

## 9. Review checklist

1. Confirm unit scaling, parameter image/gear witness and nine-dimensional initial boxes.
2. Confirm complete labels/time coverage and 1944-query denominator.
3. Review action/geometry/horizon relevance and any changes before results exist.
4. Close work-cap/primitive compatibility and baseline-selection gaps before lock.
5. Set justified usefulness acceptance criteria before outputs, without claiming runtime in advance.
6. Obtain applicable user authorization before any evaluator, baseline adapter or benchmark implementation.
