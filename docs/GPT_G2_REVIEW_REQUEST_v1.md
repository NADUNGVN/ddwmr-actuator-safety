# Independent G2 review request v1

2026-09-29. User authorized opening **G2 research only** after G1 status commit `4ee3c82c1c944119ad2b9923bfd830a1b6480503`. Overall HOLD. G1 PASS for restricted reduced-model consistency; G2/G3/G4 UNVERIFIED; physical-platform correspondence UNVERIFIED. No implementation is authorized.

Read AGENTS and all four canonical context files first. Then read:

1. [G2 analytic candidate](../research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md).
2. [Prior-art overlap and blockers](reviews/G2_PRIOR_ART_AND_BLOCKERS_v1.md).
3. [Luna supporting audit](reviews/LUNA_G2_AUDIT_v1.md); do not substitute model agreement for your own equation-level review.

## Exact review questions

Use Finding / Evidence / Consequence / Status / Required action, and identify equations explicitly.

1. Check A,B,D,S against MASTER's nine-state plant, including signs, gear conventions and mixed coordinate units.
2. Check the finite predictor and residual bound for every n, including n=0 and the reason n>=1 is needed to feed voltage into the body center.
3. Check the Dini derivative comparison under merely Lipschitz phi; reject any implicit monotonicity/differentiability assumption.
4. Check the exact impulse-response refinement: soundness, E_(n,ell+1)<=E_(n,ell), and dimensions/order of convolution factors.
5. Check pose lifting, parameter-labeled joint union, and the common-voltage quantifier. A parameter-dependent predictor must not become a controller oracle.
6. Check contact admissibility at beta=1 and zero reserve, and absence of circular dependence on unknown domain invariance.
7. Check the full-time/parameter-cell evaluation contract, including the finite-cell comparison fallback in G2.28 and G2.29. Distinguish analytic inclusion, finite certified evaluation, and useful nonconservatism. No numerical samples or ordinary quadrature can replace uniform bounds.
8. Check local iteration orders and the O(t^4) upper voltage-to-position response claim. It is not a relative-degree or lower-authority claim.
9. Challenge novelty against the inspected componentwise/growth-bound literature and identify additional closest primary sources. Generic methodology is explicitly not claimed as new.
10. Give separate dispositions for analytic soundness, computational specification, practical usefulness, and G2 overall. Do not pass G2 merely because a proof template is coherent.

## Boundaries

No G3 recursive set construction is requested. No controller/simulator/experiment implementation, GO, hardware validation or novelty closure is requested. If a new assumption is needed, state the exact proposal and halt that branch; do not amend the plant silently. Return corrections to the research note as review evidence before any theorem is promoted into authoritative claims.
