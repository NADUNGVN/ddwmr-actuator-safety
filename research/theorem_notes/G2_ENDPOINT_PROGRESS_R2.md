Session: DDWMR | LUNA-G2-SCOPE

# G2 terminal-progress endpoint bound — R2 proof note

**Date:** 2026-10-03  
**Status:** mathematical inclusion candidate for independent review; no study query evaluated.  
**Scope:** supplemental endpoint-progress bound for the existing G2-COMP-clip, one-hold synthetic profile. It does not amend MASTER v2.1, establish G2 PASS, or make a physical-platform claim.

## Finding

A rational lower bound for the common-hold terminal displacement can be obtained without subtracting two independently enclosed position endpoints. For one query with a single fixed voltage V over the full hold [0,T], use

\[
p_x(T)-p_x(0)=\int_0^T u(t)\cos(\theta(t))\,dt.
\]

The bound is conservative and valid for every initial state in the query box and every fixed parameter label in the declared image, conditional on the R3 full-hold internal tube inclusion being sound and replayed.

## Evidence — required full-hold tube input

Write the internal state as z=(u,r,omega_L,omega_R,i_L,i_R). For a fixed parameter label, the evaluator's comparison construction supplies a predictor range P1 over the entire closed interval [0,T] and a componentwise nonnegative error radius eta(T). The inclusion needed here is

\[
z(t)\in P_1 + [-\eta(T),\eta(T)] \quad \text{for every }t\in[0,T].
\]

The R3 implementation serializes P1 as P1_scaled and eta(T) as eta_physical. P1 is initially in scaled internal coordinates; the endpoint checker reconstructs physical units from the effective benchmark coordinate_scaling. Eta is serialized in physical coordinates. The code must reject a missing, malformed, un-replayed or unsupported safety proof; a status string alone is not evidence of this inclusion.

Let P_u=[u_-,u_+] and P_r=[r_-,r_+] be the physical predictor intervals for the first and second internal coordinates. Let eta_u and eta_r be their nonnegative physical error radii. For every t in [0,T],

\[
u(t)\in U=[u_- - \eta_u,\;u_+ + \eta_u].
\]

The heading is not an independent dynamic state in the six-dimensional interval predictor; MASTER gives dot(theta)=r exactly. Therefore, for any initial theta_0 in the initial heading interval Theta_0,

\[
\theta(t)=\theta_0+\int_0^t r(s)\,ds
\in \Theta_0 + [0,T]P_r + [-T\eta_r,T\eta_r]
=:\Theta.
\]

This includes every initial state and every label. It intentionally forgets correlations between theta_0, r, u and the fixed labels. Forgetting those correlations can only enlarge U and Theta. For each execution, the same rational V is used for all initial states and its parameter label remains fixed; interval coefficient hulls may relax label dependence and even admit more coefficient combinations than fixed-label trajectories, but they are used only as outer bounds. No state, label, time, or endpoint is assigned a different voltage.

## Evidence — global rational cosine and product bounds

Set

\[
M=\max(|\Theta_-|,|\Theta_+|),\qquad
c_-=\max(-1,1-M^2/2),\qquad c_+=1.
\]

For every real x, 1-cos(x)=2 sin^2(x/2) <= x^2/2 and -1 <= cos(x) <= 1. Thus cos(theta(t)) lies in C=[c_-,1] for all t, with no floating-point trigonometry and no assumption that Theta stays in a monotonic cosine region.

Using exact rational interval multiplication, define

\[
g_-=\min\{u_-^U c_-,\;u_-^U,\;u_+^U c_-,\;u_+^U\},
\]

where u_-^U and u_+^U denote the lower and upper endpoints of U. Then u(t)cos(theta(t)) >= g_- for every t. This four-corner minimum is valid for either sign of u and either sign of c_-. Integration gives the endpoint inclusion

\[
p_x(T)-p_x(0)\ge T g_- =: J^-.
\]

J^- is a lower bound for the infimum of the displacement over the complete initial-state box and the complete fixed-label image under that query's one common held voltage. It is not a bound on p_x(T) alone, a sampled estimate, or the width of a full-time position hull. The shared p_x(0) cancels algebraically in the integral identity; no independent p_x(0) interval is subtracted from a separately computed p_x(T) interval.

## Outward rounding, endpoint semantics and failure statuses

All input rationals are parsed as reduced exact Fraction values. The additions, products, max/min comparisons and T multiplication are exact rational operations under the declared operation and bit budgets; their results are serialized as numerator/positive-denominator pairs. There is no decimal rounding in the mathematical bound. Exact rational arithmetic is outward by construction relative to the rational input data. A bit or operation cap, malformed proof, replay mismatch, unsupported profile, nonpositive T or missing tube field yields an explicit non-success status and no task success.

T is the exact positive hold duration in the query. The internal enclosure covers every t in the closed hold, theta is bounded from its initial interval through T, and the integral is the exact terminal difference p_x(T)-p_x(0). A threshold comparison uses exact rational ordering: J^- >= 1/20 m. Equality passes the predeclared bound; failure to meet the sufficient lower-bound threshold means only that this sufficient task test did not pass.

For study eligibility, both predicates are required: (i) the independently replayed whole-hold collision/contact record is CERTIFIED and (ii) the independently replayed progress lower bound meets 1/20 m. A negative or subthreshold progress bound is not a physical failure claim. Safety UNKNOWN, invalid input, proof-replay rejection, execution failure or resource limit can never be converted into a task success.

## Inclusion chain to code

| Mathematical object | R2 code/data field | Required checker action |
|---|---|---|
| One exact query, one shared held V, T>0 | query.action.V, query.horizon.T, query.state_cell.box | Parse canonical rational pairs; validate IDs and action bounds in manifest validator. |
| Fixed-label outer coefficient image and physical coordinate scaling | validation/g2/model.py:build_model; benchmark_v1.json | Rebuild the declared label image and scales from the hashed benchmark; never infer units from display values. |
| P1 full-hold predictor and eta comparison radius | replayed safety proof fields P1_scaled and eta_physical | First call the R3 record replay; require exact proof-field equality. Use only replay-validated bounds. |
| U and Theta enclosures | validation/g2/endpoint_r2.py | Reconstruct P1_u/P1_r in physical units; add eta_u and T eta_r; exact rational interval operations. |
| C=[max(-1,1-M^2/2),1] | endpoint_r2.py | Evaluate the global cosine inequality with exact rational arithmetic. |
| g_- and J^-=T g_- | endpoint_r2.py | Four-corner interval product, exact min, exact positive-T multiply. |
| Independent progress record verification | validation/g2/endpoint_checker_r2.py | Replay the safety record, recompute every progress field from the validated input/proof, and compare exact serialized values and binding hashes. |
| 5 cm task eligibility | offline selector/post-processing in the R2 protocol | Count only safety CERTIFIED plus J^- >= 1/20; keep all rows and failures in the denominator. |

## Status and limitation

**Status:** analytic endpoint route is complete as a conservative derivation, conditional on the declared R3 full-hold inclusion. Its code and independent exact-field replay remain implementation/review obligations. The certificate is synthetic, one-hold, and sufficient. It proves neither recursive feasibility nor physical motion/contact behavior, and it does not establish that voltage selection is useful.

**Required action:** audit the R3 predictor/comparison inclusion and the new endpoint serialization/replay against this note. Reject any record whose safety replay does not pass. Do not freeze or evaluate the 800-row candidate until the protocol, source closure, manifest and both proof paths receive review.