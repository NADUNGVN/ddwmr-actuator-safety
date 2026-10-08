Session: DDWMR | LUNA-G4-AUER

# G4 W2 — DDWMR audit checklist and Auer source crosswalk

**Date:** 2026-10-07. **Branch/HEAD at audit start:** `main` / `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`. **Status:** pre-release audit framework complete; no G2 W2 release exists in the peer namespace yet.

## Scope and current decision boundary

This is a candidate-independent audit instrument for the MASTER v2.1 reduced nine-state, ideal constrained-contact DDWMR. It does not accept an unissued G2 release, establish an IVP certificate, promote G4, or authorize a matched run. The initial G2 W2 STATUS has `sequence=1`, `artifacts=[]`, and `peer_release_consumed=null`; therefore there is no immutable source/proof hash on which to issue `ACCEPT_FOR_SCOPED_VALIDATION`, `REVISION_REQUIRED`, or `MATHEMATICAL_BLOCKER`.

The historical ten R19/R20 pairs remain descriptive consumed development evidence only. Their previously accepted status counts are Auer 9/10 and R3 6/10; three were Auer-only and none R3-only. Four R3 UNKNOWN results never entered the common predicate. Their R3-native margins are not common-predicate outputs. No old or new query is run in this W2 pass.

## Source-to-code crosswalk

| Source / artifact | Exact scope and location | Implementation / evidence mapping | Audit conclusion |
|---|---|---|---|
| Auer, Kiel & Rauh (2013), “A Verified Method for Solving Piecewise Smooth Initial Value Problems,” *IJAMCS* 23(4), 731–747, DOI 10.2478/amcs-2013-0055 | Retained primary PDF SHA-256 `D6310C8FD32280ADDDA3F50E3367F9923940641D39DE0E70A0932869A2D0EAD2`. §4.1 Eq. (26) allows an autonomous IVP with interval initial values; Eqs. (31)/(33)/(40) define piecewise ranges and generalized derivative handling; Eqs. (35)/(41) add jump treatment for discontinuities; §4.2 Eqs. (42)–(43), printed p. 742, describe a functional tube around a non-verified approximate path and use of VALENCIA-IVP. | `validation/baselines/auer2013/piecewise.py`, `rhs.py`, `residual_ivp_g4_matched_v3_r9.py`, and `replay_ivp.py`. The reconstruction specializes the piecewise method to the continuous clip law and the DDWMR equations. | Supports a method-level reconstruction. It supplies neither this DDWMR system nor the repository's 21-coordinate run, proof records, matched queries, or a DDWMR-specific novelty claim. The zero jump at clip corners makes the discontinuity-gap correction zero; it does not remove the generalized-derivative or IVP-inclusion obligations. |
| Rauh & Auer (2011), “Verified Simulation of ODEs and DAEs in ValEncIA-IVP,” *Reliable Computing* 15, 370–381, DOI 10.1007/s11128-010-0165-6 | Source crosswalk in `docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md`: Algorithm 1 and Eqs. (3)–(6), printed pp. 371–372, for smooth residual iteration. | Local residual step construction in `residual_ivp_g4_matched_v3_r9.py::_ddwmr_trial_step`; independent native record replay in `replay_ivp.py`. | Supports residual/Picard method context; not evidence that this local code is the original software. |
| Pinned VALENCIA-IVP 0.92_2e source | `external/valencia-basic/free-source/ValEncIA/ValEncIA-IVP_0.92_2e.cpp`, SHA-256 `C00D8CC674F616114B319BC796123A142B0973C0D21418401E43D358E3B63CA4`. The local method contract identifies it as an older smooth application seed, without the 2013 piecewise extension or adopted DDWMR equations. | Historical source-build disposition: `results/validation/g4/auer2013/auer_seed_full_build_disposition_v1.json`. | Native executable is unavailable: record status `BLOCKED_BEFORE_LINK`; the successful syntax-only check is not a linked binary, directed-rounding proof, or method-fidelity check. The R19 worker is not the VALENCIA binary. |
| Frozen local Auer method contract v2 | `docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md`, SHA-256 `50C6883E694F91D7E2FE183D1E771A4E1C75B574D909E781F22632F6326C1E19`. | Explains specialization, equation-to-code mapping, 21-coordinate augmented labels, interval arithmetic, native replay and resource semantics. | Accurate reconstruction label is mandatory. Contract status and a fixture are not by themselves a finite IVP certificate. |
| R19 prospective Auer/R3 source closure | `research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R19_PROSPECTIVE.json`, SHA-256 `A50BC0452E6B8F164988A4AF8D669E563381F157F86188CA8C7EE1FB1518CA76`; it lists 575 dependency paths. Read-only rehash: **571/575** byte/hash pairs match. The four mismatches are `AGENTS.md`, `research_context/DECISION_LOG.md`, `research_context/MASTER_RESEARCH_CONTEXT_v2.md`, and `research_context/REVIEW_GATE.md`; these current governing files differ from their R19-pinned versions in the shared tree. The R9 residual solver, RHS, clip code, replay, Auer adapter, common checker, composition checker and R3 adapter individually match their R19 closure rows. | Closure rows include Auer R9 producer/replayer, R17 adapter/composition layer, common tube, benchmark/profile/protocol, and retained fixture/result inputs. The audit command uses `validation/autonomous_w2/g4/audit_source_closure.py` and does not write the pinned manifest or dependencies. | Historical R19 binding only. The four current context-file mismatches are not silently accepted or repaired. R19 cannot serve as the current G2 W2 release closure or new W2 comparison snapshot. Rebind current governing inputs and code in a new immutable W2 closure; do not rely on its older 120 s common profile for W2. |
| Historical local-source snapshot v9 | `results/validation/g4/auer2013/source_snapshot_v9/snapshot_manifest.json`, SHA-256 `FE3309D5B17C6D2968C826EAF1A0759C3B9FBF848432B72842FFF5B4DB726D91`; 718 members. | Snapshot predates later R9/R17 matched comparison sources; later code and artifacts are covered by the R19 prospective closure. | Historical context only, not a complete W2 source snapshot. |
| Shared rational and transcendental arithmetic | `validation/g2/rational.py`, SHA-256 `8A2C16778B33898AFD16C8DA44945C2D41FD7D187CB11C7CB071745E68ED5C6E`; `validation/g2/interval.py`, SHA-256 `E49E2E3880485D9A658E2435CFA06B784F98257B13C51FA4A2BF464F9C73E5C6`. | Exact `Fraction` interval endpoints and budgeted operations; sine/cosine use the shared rational Taylor-plus-remainder implementation. `rhs.py` imports the G2 parameter map and interval trig; native replay and common predicate also reuse shared arithmetic. | No host floating-point interval rounding in this path, but producer, replay and common checker do not have independent arithmetic kernels. Record this shared trust dependency and do not characterize producer/checker agreement as independent arithmetic validation. |

## Equation-to-code audit map

Formal state and law (MASTER v2.1, nine-state order):

\[
x=(p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R),\quad
\sigma_L=R_w\omega_L-u+br,\quad \sigma_R=R_w\omega_R-u-br,
\]
\[
F_j=C_j\,\operatorname{clip}(\sigma_j/v_s),\quad
\dot p_x=u\cos\theta,\quad \dot p_y=u\sin\theta,\quad \dot\theta=r,
\]
\[
m\dot u=F_L+F_R-c_u u,\quad I_z\dot r=b(F_R-F_L)-c_r r,
\]
\[
J_j\dot\omega_j=k_j i_j-B_j\omega_j-R_wF_j,\quad
L_j\dot i_j=V_j-R_j i_j-k_j\omega_j.
\]

| Proof obligation | Existing source location | G4 review action when a bound release appears |
|---|---|---|
| Nine physical coordinates plus twelve exact constant parameter labels; `dot(label)=0`. | `rhs.py::augmented_rhs`; 21×21 dual interval Jacobian; `residual_ivp_g4_matched_v3_r9.py::_ddwmr_trial_step` | Recompute order/dimension and inspect all label derivatives, every parameter image and cross-step identity. A hull may outer-relax fixed labels but may not resample them. |
| One common held voltage for a full hold; correct motor voltage, resistance, back-EMF, torque, force and slip signs. | `rhs.py::augmented_rhs`; `solve_ddwmr_case` | Derive each term from MASTER and bind one exact `V` across all steps and all states/labels in a query. |
| Exact clip range and generalized derivative at both corners. | `piecewise.py::clip_interval`, `clip_derivative_interval`, `DualInterval.clip`; residual Jacobian | Require `[0,1]` at/touching either clip corner; never smooth only one method. Check chain derivative against the entire rational parameter/state image. |
| Full-time IVP inclusion and closed slab coverage. | `_ddwmr_trial_step`; `replay_ivp.py` | Recompute residual range, derivative inclusion `D_next ⊆ D_old`, integrated tube inclusion, compact convex rough domain, endpoint, and contiguous coverage of `[0,T]`. Failure is UNKNOWN, not CERTIFIED. |
| Endpoint chaining under unchanged labels. | `solve_ddwmr_case`; Auer adapter checks every saved step endpoint | Verify each next start contains the entire previous endpoint; verify label intervals are exactly unchanged; keep one voltage and one full task duration. |
| Full-hold collision and algebraic contact predicates. | `validation/g4/common_tube.py::_collision_margin`, `_contact_margin`, `check_tube_segments`; `verify_matched_composition_v3_r17.py` | Recompute on every closed segment. Collision uses the full footprint exclusion radius and a lower distance bound. Contact checks `sqrt(C_j^2-F_j^2)` on a nonnegative radicand and `a_L+a_R-|mur|`; no derivative of the contact square root is allowed at saturation. Reject negative/unsupported lower bounds as no pass. |
| Proof/result/input/source identity and terminal semantics. | R17 composition auditor; R19 stage runner/checker; R20 path binding; R21/R22 review records | Bind exact immutable G2 release, both producer closures, task inputs/IDs, profile, proof bytes and checker version. Keep resource UNKNOWN, proof-complete UNKNOWN, invalid/unsupported, execution failure, audit failure and NOT_RUN distinct. |
| Resource envelope. | Historical R19 profile uses 120 s for common checking. | W2 comparison must rebind a new ≤60 s wall limit and ≤1 GiB per numeric worker/replay/audit, plus a ≤2 h phase cap and explicit arithmetic-operation/precision limits. Do not reuse the historical 120 s cap as W2-compliant. |

## Endpoint-progress inclusion independently derived

The already recorded `research/theorem_notes/G2_ENDPOINT_PROGRESS_R2.md` derives a conservative x-displacement lower bound for R3 conditional on a replayed full-time tube. I inspected its `endpoint_r2.py` and `endpoint_checker_r2.py` path and the accepted `CODEX_G2_DECISION_DOMAIN_R2_SCIENTIFIC_REVIEW.md`. The R19 common profile itself checks only full-time collision and contact; it has no progress/task-output predicate. G4 therefore extends the derivation to any method that supplies a replayed full-time `u`, `r` range and the common initial heading interval.

Let `U=[u_-,u_+]` and `R=[r_-,r_+]` enclose the true body speed and yaw rate for **every** time on the same certified tube. Let `Theta0` be the full initial heading interval and `T>0` the exact hold duration. From `dot(theta)=r`,

\[
\Theta=\Theta_0+[0,T]R \supseteq \{\theta(t):0\le t\le T\}.
\]

Set `M=max(|Theta_-|,|Theta_+|)`, `c_-=max(-1,1-M^2/2)`, and `C=[c_-,1]`. The global inequality `1-cos(q) <= q^2/2` gives `cos(theta(t))∈C`, without assuming a small-angle or monotone-cosine branch. Compute

\[
g_- = \min\{u_-c_-,u_-,u_+c_-,u_+\},\qquad
J_x^- = T g_-.
\]

The four-corner minimum encloses either sign of `u` and `c_-`; hence, on the same voltage and fixed-label execution,

\[
p_x(T)-p_x(0)=\int_0^T u(t)\cos(\theta(t))\,dt\ \ge J_x^-.
\]

This is a sufficient interval lower bound. It may be inconclusive because it drops state/parameter correlation. A task threshold must come from the prospective task definition, not from this bound or R22–R24 outputs. For R3 the intervals must be reconstructed from the replayed `P1_scaled`, `eta_physical` and benchmark scale; for Auer they can be hulled from replay-validated per-slab total tubes. Subtracting independent `p_x(T)` and `p_x(0)` boxes is sound but can be needlessly wide; the integral form makes the shared initial position cancel exactly. The endpoint helper does not establish the upstream IVP tube, collision/contact pass, or physical progress. A future common progress evaluator must bind and replay those premises before applying the exact rational formula to both methods.

## Checklist for the actual DDWMR candidate

| Item | Audit requirement | Current W2 state |
|---|---|---|
| C1 | Supported law is explicit (`clip` only if that is the candidate profile); state order, units, geometry and parameter image match MASTER v2.1. | Auer R9 mapping source-read; exact G2 W2 profile unavailable. |
| C2 | Quantifiers cover every initial nine-state point and every complete fixed-label parameter value; one voltage is held for the whole query. | Historical Auer input guards cover complete labels and exact held voltage; candidate audit pending. |
| C3 | Derive signed motor/current/back-EMF/contact/pose propagation independently; verify forces and wheel/body coupling. | Auer equations cross-read; no G2 release proof to audit. |
| C4 | Prove every coefficient denominator positive on the full label image; retain label identities and time chaining. | Existing Auer model builder checks the benchmark image; candidate audit pending. |
| C5 | Prove the predictor/residual or alternative enclosure contains the complete solution on every closed slab, not just sampled points or endpoints. | Historical Auer R9 proof contract/source path present; no fresh W2 replay. |
| C6 | Recompute partial slabs, endpoint enclosures, source bindings, fixed labels, completeness, residual inequalities and failure classifications. | Release/source hashes absent; no release decision. |
| C7 | Recompute full-hold collision and contact margins on the same common target for both methods; check square-root domains without differentiating at saturation. | Historical common checker available; no task-specific W2 execution. |
| C8 | Bind an independently chosen endpoint progress/command-preservation predicate and threshold; independently replay the progress bound for both producers. | Formula above derived; R19 common layer has no progress field. G2 task and threshold unavailable. |
| C9 | Disclose shared model, arithmetic, interval-transcendental, checker and source dependencies; avoid overstating independence. | Shared `validation.g2` arithmetic/model identified. |
| C10 | Freeze candidate claim, task/group IDs, exact ordered inputs, source snapshots, resource profile, primary comparison criterion and result taxonomy before either confirmation producer runs. | Not ready: no candidate release or task/criterion. |
| C11 | Keep confirmation ≤8 groups×3 actions per method; worker/replay/audit ≤60 s and ≤1 GiB; phase ≤2 h; no selective cap increase. | No confirmation run; 0/24 fresh rows per method. |
| C12 | Preserve R19/R20 original checker failure and retrospective replay; never recycle consumed IDs or call historical pilot fresh evaluation. | Preserved; no W2 reads/writes to historical bytes. |

## Prior-art scope for the W2 candidate

The literature matrix rows 25–27 and the associated supplements identify directly relevant generic work: Arcak & Maidens (2017), §2 Proposition 1/Corollary 1, §3 Algorithm 1 and Example 1; Meyer, Devonport & Arcak (2019, TIRA), §3.1 Assumption 3, Eq. (4), Proposition 4 and remarks; Houska, Villanueva & Chachuat (2015), §3 assumptions A1–A3, Eqs. (3.1)–(3.4), Theorem 3.1/Corollary 3.2 as recorded in the primary-source audit; and Flow* (2013), whose full-text retrieval was partial in the project record. These cover generic validated-IVP, componentwise growth, fixed-parameter augmentation, predictor-validation or Taylor-model constructions at differing assumptions. Their direct DDWMR applicability and exact theorem overlap depend on the released candidate's formula and regularity domain.

R23/R24 is already resolved at the method level: shared-latent paired-IVP construction is generic validated-reachability methodology; the frozen synthetic action-ordering branch was stopped as a proposed paper contribution. Angeli–Sontag comparison theory was used to reject a direct monotone/cooperative-system implication in R23's displayed coordinates; that limited result does not exclude other cones or other DDWMR-specific contributions. The new W2 hypothesis in the G2 assignment—parameter-aware, time-local variation-of-constants retaining signed motor/body/slip dependence—cannot be classified as novel or redundant without its exact theorem, assumptions and computed bound. Exact motor propagation, residual validation, parameter augmentation, generic inclusion, and tube construction are established techniques. Any supported novelty must lie in a checkable DDWMR-specific inequality or effect and its independently reproduced impact on the frozen task.
