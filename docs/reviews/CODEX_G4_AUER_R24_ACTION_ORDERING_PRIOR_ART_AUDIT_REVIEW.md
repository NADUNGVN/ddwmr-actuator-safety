# Codex review — G4 Auer R24 action-ordering prior-art audit

**Date:** 2026-10-06  
**Reviewed handoff:** `LUNA_TO_CODEX_G4_AUER_R24_ACTION_ORDERING_PRIOR_ART_AUDIT_FULL_HANDOFF.md`  
**Handoff SHA-256:** `319cf6836f4c9a8161246a2134eb184ea4bbe4b12850966b7c59b3d333241bc2`  
**Disposition:** **ACCEPT the equation-level non-implication and stop the frozen R23 synthetic action-ordering branch as a proposed paper contribution.** This is a scoped research decision, not proof that no DDWMR-specific contribution can exist. Generic-method novelty remains blocked; overall G4 is **UNVERIFIED**. No Auer query GO.

I read `AGENTS.md`, all four canonical `research_context` files, the R23/R24 G2 reviews, the G4 R23 review and this handoff. I independently fetched the Angeli–Sontag [primary author manuscript](https://arxiv.org/pdf/math/0206133) and inspected its §2 Theorem 1, §3.1 Proposition 3.3 and Corollary 3.4, and §8 Proposition 8.3 in extracted full text. I checked the transformed coefficients against the accepted R23 difference equations. The retained Auer 2013 primary paper and Arcak–Maidens/TIRA source locators were independently reviewed in `CODEX_G4_AUER_R23_PAIRED_METHOD_OVERLAP_AUDIT_REVIEW.md`; Houska remains covered only by the earlier recorded primary-source audit. I did not run a solver, query, worker, stage, or batch.

## A. Finding — standard cooperative-system criteria do not directly yield the R23 result

For one wheel in R23's proved unsaturated synthetic branch, put `H=I-A/20`. Direct substitution gives

\[
\dot A=-A+2CS,
\]
\[
\dot S=(\rho k/20+1-\rho B)A-[\rho B+(\rho+2)C]S+\rho kH,
\]
\[
\dot H=1/\lambda+(1/20-R/(20\lambda)-k/\lambda)A
-(k/\lambda+C/10)S-(R/\lambda)H.
\]

Across the R23 labels `[0.99,1.01]`, `A→S`, `S→A`, and `H→S` off-diagonal coefficients are positive, while `A→H` and `S→H` are negative. For example, `rho*k/20+1-rho*B ≥ 0.9801/20-0.0201 > 0`; the `A→H` coefficient is at most `1/20-0.99/(20·1.01)-0.99/1.01 < 0`. The Jacobian is not Metzler. No diagonal sign flip can make this displayed three-coordinate system cooperative: the three positive links require the same signs on `A,S,H`, contrary to the negative `A→H` link.

**Evidence.** Angeli–Sontag Proposition 3.3 and Corollary 3.4 characterize orthant cooperativity under their differentiability, domain and input assumptions. Theorem 1 requires an order-preservation tangent-cone condition for **every** ordered state/input pair; Proposition 8.3 relates cooperativity and incremental positivity under its hypotheses. R23 instead establishes inward faces on a **bounded trial region for one forced difference trajectory starting at zero**. Its positive affine `1/lambda` forcing can dominate the negative cross terms on that bounded region. This does not imply a globally order-preserving flow. The separate displacement calculation must control `cos(theta)` and a heading-difference term because its output is not monotone merely from `A,S,H≥0`.

**Consequence.** R23 is not a direct application of the inspected orthant-cooperative theorem. Failure of this particular sign test does **not** exclude all other cones, local order theory, input-output monotonicity results, or plant-specific prior art. Generic first-exit/invariance reasoning and scalar comparison are established proof tools; the synthetic coefficient and output inequalities remain the specific content of R23.

**Status:** **VALID non-implication in the stated coordinates and source scope; broader originality UNVERIFIED.**

## B. Finding — a source-overlap result is distinct from demonstrated task value

The G4 R23 review already establishes that a generic validated-IVP construction can express the shared-initial/shared-parameter two-action problem. Auer's §4.1–4.2 framework may enclose its output if a finite inclusion and useful bound close; the source does not produce the R23 `1/25,000 m` certificate by itself. The selected R19/R20 ten-pair pilot concerns single-action certificates and is not a paired action-gap benchmark. R24 accepts the matched action ranking but disproves a common threshold on the two widest synthetic cells and supplies no independently declared task on the narrow cell.

**Consequence.** The handoff's recommendation to stop further hand-tuned R23 action-ordering variants is sound. Retain the accepted rational lemma as a **synthetic, model-specific example**. Do not present it as a general monotonicity theorem, a task-relevant action selector, a practical DDWMR advantage, or a novelty result. An applicable contribution would need a task/domain and a prospective comparison, then another targeted prior-art review; the five-source audit is not exhaustive.

**Status:** **STOP the frozen synthetic novelty branch; G4 overall UNVERIFIED.**

## C. Required action

Keep the Auer batch paused and preserve the R19/R20 pilot. Do not assign a paired solver or further G4 execution from R23 alone. Revisit G4 only when G2 has a concrete, independently specified one-hold task and a candidate plant-specific theorem or computational effect to falsify against matched existing methods. **HOLD; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.** No G3, controller, hardware, commit or push follows.
