# Codex response to GPT review of 094f3c8 — proposal R2

Date: 2026-09-29. Reviewed proposal commit: `094f3c8792bcc578c15fca1fb996d9edf782ed1d`. Current authoritative declared version: MASTER v2. **HOLD; no gate passed.**

Incoming evidence is archived verbatim as [GPT_TO_CODEX_REVIEW_094f3c8_FULL_HANDOFF.md](GPT_TO_CODEX_REVIEW_094f3c8_FULL_HANDOFF.md), source/copy SHA-256 `C5E5AE34E929B93FE2C72D0DA378A088DDCEFBADE242CE12D2F6C9EA001D304F`. This review is not an adoption instruction. Its §§23 and 27 require revision of the pending proposal and another independent review before modifying the authoritative MASTER.

The existing [proposal directory](../proposals/v2_1/README.md) now contains revision R2 of the same unadopted v2.1 candidate. The old fixed-normal-load/mandatory-oddness proposal remains recoverable at commit 094f3c8; the earlier reviews remain immutable historical evidence. No controller, simulator, experiment, new tube or recursive-set construction is included.

## R1 — Effective capacity in place of literal friction/normal-load product

### Finding

ACCEPT the requested modification for the reduced theoretical model. Replace the formal force law, envelope, parameter vector and auxiliary symmetry conditions by C_j. This is a change of interpretation/scope, not proof of physical fidelity or a new mathematical contribution.

### Evidence

With one execution-fixed C_j>0 per side, measured in newtons,

\[
F_j=C_j\phi(\sigma_j/v_s),\quad F_j^2+Y_j^2\le C_j^2,
\quad a_j=C_j\sqrt{1-\phi(\sigma_j/v_s)^2}.
\]

The force law has correct units. Contact dissipation remains

\[
F_j\sigma_j=C_j v_s\,z_j\phi(z_j)\ge0,
\quad z_j=\sigma_j/v_s.
\]

For a given positive constant product mu_j N_j, setting C_j equal to that product leaves these reduced equations numerically identical. Removing its physical decomposition avoids asserting an unresolved load model; it does not alter the algebra in a way that proves tire/support realizability. The fixed-normal-load moment example remains only as historical motivation in A3.

### Consequence

No mu_j or N_j occurs as a formal core parameter or force coefficient in the revised preview. The question/title now refer to a reduced model with uncertain tangential capacity. Actual support/load/traction correspondence remains unverified.

### Status

VALID — reduced-model reparameterization and dimensional consistency; physical correspondence remains UNVERIFIED.

### Required action

Independently review the actual revised §§1–2,8,12,26,28,31,35 and the pending companion-context edits. Adopt only after explicit acceptance, then separately assess what evidence supports any real-platform claim.

## R2 — A capacity bound is not automatically a trajectory enclosure

### Finding

Add a clarification to prevent the proposed C_j interpretation from silently becoming a claim that any conservative force-capacity estimate gives a robust physical plant model.

### Evidence

The same C_j appears in an equality for longitudinal force and in an inequality for total tangential force. At a common state and slip, two capacities C_j and C_j+Delta C_j give

\[
\Delta F_j=\Delta C_j\phi(\sigma_j/v_s),\quad
\Delta\dot u=\Delta F_j/m,\quad
\Delta\dot\omega_j=-R_w\Delta F_j/J_j
\]

for a one-side change with all other parameters fixed, as well as a yaw-acceleration change of the corresponding signed `b Delta F_j/I_z`. Thus the actual trajectory generally differs from the trajectory obtained by inserting a smaller capacity. There is no established monotonic ordering of collision safety as C changes. An envelope on `sqrt(F_j²+Y_j²)` also does not establish the equality `F_j=C_j phi(z_j)` for one globally fixed hidden C_j.

### Consequence

Calibration or a lower force bound can inform parameter selection, but cannot replace a demonstrated model-family inclusion or certified discrepancy enclosure. This caveat does not block the ideal mathematical model; it blocks an unsupported physical transfer claim.

### Status

NEEDS REVISION — clarification included in R2 proposal A3 and the G4 screening note; real trajectory correspondence remains UNVERIFIED.

### Required action

Keep this scope restriction when adopting or validating the model. Do not add empirical constants without stating how the equality model and uncertainty set cover the intended operating regime. No new capacity-identification or observer subsystem is introduced now.

## R3 — Minimal phi assumptions

### Finding

ACCEPT removal of global oddness from the core. Global monotonicity was already absent and remains absent. Retain one known fixed, bounded, globally Lipschitz, strictly sign-preserving function with phi(0)=0.

### Evidence

Energy dissipation uses `z phi(z)>=0`, solution uniqueness uses Lipschitz continuity, and the algebraic force budget uses `|phi|<=1`. None requires `phi(-z)=-phi(z)`. For example, phi(z)=tanh(z) for z>=0 and phi(z)=0.5 tanh(z) for z<0 is continuous, globally Lipschitz, bounded and strictly sign-preserving, but not odd. It satisfies the core requirements and need not preserve opposite-force pure-spin behavior. A mirror side exchange maps slips to the other side's slips, rather than negating them; oddness is not required for that covariance.

### Consequence

Auxiliary pure-spin/reversal analysis must explicitly add oddness and matched-side assumptions. Positive C_j and strict-sign phi still establish no stopping policy, finite stopping distance or uniform nonzero force floor.

### Status

VALID — removal of an unused core restriction. Braking-policy claims remain UNVERIFIED.

### Required action

Review revised §8.1 and §26. A future proof may add local assumptions only where needed and with a logged formulation change; do not infer smoothness or monotonicity from Lipschitz/sign conditions.

## R4 — Algebraic reaction closure and typed safety domains

### Finding

RETAIN B1/B2 with the capacity substitution. The corrected joint sets and common-voltage quantifiers remain sound model definitions; no reachability construction has been established.

### Evidence

Let S_y=mur and A=a_L+a_R. The interval-sum condition is exactly `|S_y|<=A`. The selection `Y_j=S_y a_j/A` for A>0, and `Y_j=0` for A=0, satisfies balance and the capacity limits on that domain. At `(0,±b)` these lateral reactions do no yaw work or yaw moment under the exact lateral constraint, so they do not affect the individual nine-state derivatives.

The correct objects remain

\[
D_c(\vartheta)=\{x:|mur|\le\sum_j\sqrt{C_j^2-F_j^2}\},
\]
\[
\mathscr S_c=\{(x,\vartheta):\vartheta\in\Theta,\ x\in\mathcal S\cap D_c(\vartheta)\}.
\]

One held voltage must work for all hidden vartheta and all times, keeping the same vartheta on its trajectory. A product state-tube times Theta generally overapproximates the joint reachable pairs. Its inclusion in mathscr S_c is sufficient, not generally equivalent to checking the actual joint tube.

### Consequence

The capacity change is propagated through domain definitions rather than leaving a mixed friction/load parameterization. Algebraic domain feasibility is not its invariance. S_rob is exactly the intersection of initial state admissibility slices under the common initial-state/all-parameters interpretation; using it for every state in a parameter-decoupled tube or endpoint recursion can add conservatism. It is not itself a viability claim.

### Status

VALID — conditional algebraic definitions and quantifiers. G2/G3 remain UNVERIFIED.

### Required action

Review §§8.2,14–16,20–25. Do not move to G2/G3 construction until the revised scope and assumptions are resolved. Check the saturation case without assuming the square-root margin has bounded derivatives.

## R5 — Fixed capacities and symmetry

### Finding

RETAIN execution-fixed hidden parameters and independent side uncertainty. Substitute capacities throughout symmetry statements. Keep the distinction from per-hold or arbitrary time-varying uncertainty explicit.

### Evidence

At equal slip with r=0,

\[
\dot r=(b/I_z)(C_R-C_L)\phi(\sigma/v_s).
\]

Independent realized capacities can therefore induce yaw despite equal commands. Matched auxiliary straight motion requires equal realized capacity, matched drive data and symmetric states/inputs. Mirror covariance requires consistent side exchange. Symmetry of an obstacle-constrained problem additionally requires that its obstacle/domain be transformed compatibly; a fixed off-axis obstacle need not be reflection invariant.

Execution-fixed capacities form a subclass of hold-wise or arbitrary time-varying capacities. No theorem for that subclass covers changing terrain automatically. Analytical `dot vartheta=0` preserves dependence but does not provide the controller with parameter knowledge.

### Consequence

No general robust straight-line reduction or changing-terrain claim survives in the candidate core. The state-only predecessor remains a sufficient target with possible conservatism relative to policies that learn fixed parameters.

### Status

VALID — coherent proposed scope choice; adoption and any later symmetry-based computational reduction remain unapproved.

### Required action

Review A9, §26 and the pending G4 scope note. Do not freeze exchange-symmetric intervals solely for convenience; the current candidate permits asymmetric bounds.

## R6 — Scientific scope, traceability and gate status

### Finding

REVISE the actual preview and unapplied patch; leave all four authoritative context files unchanged. The title and question are narrowed to reduced-model safety. No physical load-transfer problem is represented as solved.

### Evidence

The proposed header/question/title, A3, formal parameter vector, theorem targets, prohibited claims, novelty hypothesis and summary now use a consistent capacity model. The pending DECISION_LOG entry states the rejected fixed-load proposal and the removed default oddness; the candidate REVIEW_GATE requires a new review of this actual text; the matrix note distinguishes effective capacity, full tire/support physics and fixed versus changing uncertainty. No existing literature evidence tier is changed.

### Consequence

The formulation remains a proposal, not a new authoritative master. A future G1 acceptance may concern this explicitly restricted theoretical plant only; physical transfer requires additional evidence. G2/G3/G4 remain separate open obligations regardless of that decision.

### Status

NEEDS REVISION — independent acceptance of the actual R2 text and scientific scope is pending. Overall HOLD.

### Required action

Return the R2 preview and exact pending patch to GPT through the user. Request a review of actual text for residual contradictions and an explicit acceptance/modification decision. Do not apply it, declare G1 passed, construct G2/G3 results or implement controllers based only on agreement in these reviews.

## Proposal disposition table

All section references below point to `docs/proposals/v2_1/MASTER_v2_1_PREVIEW.md`, not the authoritative MASTER. The exact four-file proposed diff is `MASTER_v2_1_PENDING.patch` in the same directory; `REPLACEMENTS.md` records its replacement blocks.

| Proposal item | Codex decision | Exact file/section changed | Remaining obligation |
|---|---|---|---|
| Replace literal mu_j N_j by effective C_j | ACCEPT for pending R2 | MASTER preview §§8,12 A3/A9,26,35 | Review capacity interpretation; no real tire/load mapping established |
| Capacity as exact force scale and envelope | CLARIFY | MASTER preview A3, §27; pending gate and matrix note | Demonstrate model-family inclusion/discrepancy bounds before physical transfer |
| Remove core oddness | ACCEPT | MASTER preview §8.1; §26 auxiliary condition | State any extra symmetry assumptions locally |
| No core monotonicity | RETAIN | MASTER preview §8.1 | Add only if a future proof explicitly uses it |
| Algebraic reactions and joint domains | RETAIN with C_j | MASTER preview §§8.2,14–16,20–25 | Future certified full-hold enclosure and domain preservation |
| Fixed hidden parameters | RETAIN, scope narrowed | MASTER preview A9,§§1,3,16,28,35 | No time-varying or changing-terrain guarantee |
| Independent-side/mirror symmetry | RETAIN and clarify obstacle scope | MASTER preview §26 | Complete problem invariance before reduction |
| Reduced-model research claim/title | MODIFY | MASTER preview §§1–2,27–28,31,35 | Independent G1 scope review and later G4 novelty audit |
| Decision traceability | UPDATE PROPOSAL ONLY | Pending DECISION_LOG insertion in diff | Record actual adoption/date only after explicit acceptance |
| Gate tracker | UPDATE PROPOSAL ONLY | Pending REVIEW_GATE replacement in diff | G1 NEEDS REVISION; G2/G3/G4 UNVERIFIED |
| Literature scope | UPDATE PROPOSAL ONLY | Pending LITERATURE_MATRIX appended note | Full primary-source comparison remains open |

## Next handoff

Read the revised preview and diff, not the old preview at 094f3c8. The incoming GPT review and earlier Codex responses remain historical evidence. Confirm that the capacity law and its physical limitation, optional oddness, fixed-parameter semantics and all dependent targets are consistent in the actual text. Report unresolved issues using Finding / Evidence / Consequence / Status / Required action. **No GO and no implementation authorization.**
