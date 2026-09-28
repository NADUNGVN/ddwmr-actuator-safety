> HISTORICAL / SUPERSEDED BY MASTER v2 (2026-09-28). Read [MASTER_RESEARCH_CONTEXT_v2.md](../../research_context/MASTER_RESEARCH_CONTEXT_v2.md), DECISION_LOG, LITERATURE_MATRIX and REVIEW_GATE first. This note records earlier analysis, not the current nine-state plant or an implementation authorization. Seven-state results must not be transferred to the current plant without a new derivation.

# GPT research exchange — reviewed summary

Date: 2026-09-28. Conversation: [Định hướng nghiên cứu MATLAB](https://chatgpt.com/c/6ab9cdf1-cd48-83ec-b6d7-d1285c3b9105).

This is a research-only summary of the authorized exchange, not a verbatim transcript. It records suggestions and disagreements, not independent scientific evidence. Source claims are checked separately in the literature matrix and root novelty notes.

## Request sent by root

Root sent the conditional seven-state derivative calculation and six blockers: singular voltage coefficient; insufficient slip regularity; instantaneous versus recursive feasibility; incomplete contact mechanics; impossibility of invariance of all position-safe actuator states; and uncertainty in the input channel/multiple constraints invalidating a simple scalar voltage test.

GPT was asked to challenge the equations, propose a defensible minimum scope, give a HOLD/GO decision, and identify additional primary-source literature threats. The existing GPT conversation contained the original research handoff, so no unrelated project material was sent.

## GPT's first response

- **HOLD formulation freeze and implementation**, while continuing the physical-realizability research question.
- Confirmed the third-derivative calculation under the stated frozen-slip assumptions and the vanishing voltage coefficient at `rho=0`.
- Recommended considering a robust reachable tube and robust predecessor as candidate core tools, retaining HOCBF as a local comparison/baseline. This is a proposal, not an accepted change of method.
- Distinguished a certificate-feasible set, a one-hold-safe set, a recursively certified set, and a viability kernel for a specified policy class.
- Proposed a conditional induction argument: enclose every uncertain trajectory over a hold inside the collision-free set and return every endpoint to a certified set. Explicitly recognized that this induction is generic and cannot be sold as novelty.
- Suggested exploiting the motor subsystem's constant-voltage matrix-exponential response to bound wheel/current evolution, then heading and position error, rather than using only a global Lipschitz radius.
- Suggested a provisional title using “Bounded Wheel-Ground Uncertainty” instead of an unrestricted wheel-slip claim.
- Identified further leads: ZOCBF, SACBF, segment-safe MPC, Bitar–Maalouf variable sampling, Ovalle et al. sampling/authority limits, Ma et al. generalized discrete-time CBF, and Brunke et al. nonuniform-relative-degree safety filters.

## Root's follow-up corrections

Root did not accept all wording of the response:

1. At `rho=0`, write `A_u=a^T F_i L^-1`, `B_u=b^T F_i L^-1`. The coefficient of constant held voltage in the **actual fourth time derivative** is `(8v+6eta*Omega)A_u+2eta*v*B_u`. The Lie row `L_g L_f^3 h` is instead `(6v+4eta*Omega)A_u+2eta*v*B_u` there. The difference comes from differentiating the earlier voltage coefficient `2rho A_u`. Because that earlier coefficient does not vanish throughout a neighborhood, neither expression establishes a regular relative-degree-four neighborhood. GPT's phrase suggesting a switch to degree four needs this qualification.
2. Safe path containment plus endpoint return proves sample-invariance of the certified set and continuous collision safety. It does not prove continuous invariance of the endpoint set itself. A continuous invariant description requires further conditions or a hold-clock/held-input augmentation.
3. Bounded wheel-ground transmission factors force zero body velocity when the wheels are locked. A bounded load-torque residual cannot repair that kinematic limitation. A seven-state version must explicitly exclude braking skid and justify its operating envelope; including skid requires independent body motion/contact closure and a new audit.

These corrections were sent back to GPT. The first response is useful for reformulation, but neither agreement nor the existence of a generic predecessor definition supplies the missing physical enclosure or a nontrivial recursively safe set.

## Follow-up response received

GPT explicitly accepted all three corrections. It withdrew the phrase that the relative degree becomes four, adopted “robust recursively feasible sampled-state set” instead of continuous invariance of the endpoint set, and acknowledged that bounded load uncertainty does not repair the missing chassis-sliding dynamics. Its final recommendation remains HOLD, with a possible seven-state scope restricted to rolling/transmission uncertainty and no wheel lock or sustained body skid. That restricted scope has not been frozen or accepted as the final project model.

## Research decision retained

Continue two candidate formulations at the research level: a carefully scoped smooth/frozen-transmission HOCBF analysis and a bounded-measurable-uncertainty reachability analysis. Select only after physical assumptions, computational tractability, and novelty have been demonstrated. No full controller is authorized by this exchange.
