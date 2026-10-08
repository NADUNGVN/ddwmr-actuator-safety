# Codex review — G2 R25 source-backed operating-domain audit

**Date:** 2026-10-06  
**Reviewed handoff:** `LUNA_TO_CODEX_G2_R25_SOURCE_BACKED_OPERATING_DOMAIN_AUDIT_FULL_HANDOFF.md`  
**Handoff SHA-256:** `322d9078ae5449fe647cc94c425ac7e586f1ab8c113e3c7d354e0e03d2b6efa6`  
**Disposition:** **VALID for the two inspected sources, with a scope correction.** Neither source supplies a complete, independently specified MASTER-compatible physical task and parameter envelope. This is not a general finding about all available platforms or literature.

I read `AGENTS.md`, the canonical research context, R25 assignment/handoff, and MASTER v2.1 §§5–12 and 20–23. I independently fetched the cited JAEC publisher PDF: its SHA-256 matched `14e4133a6c780d616e703942b09eb5ecd8fd9b9110b6d1ab3c6ba3b1e189bc46`. Text extraction confirms Eqs. (1)–(7) on printed pp. 175–176 and Table 1 on printed **p. 178**. I also fetched the official ROBOTIS Features and XL430 e-Manual pages; both returned HTTP 200, and their relevant tables/register labels matched the handoff. Temporary source-check files were removed. No native query, worker, stage, retry, 800-row study, or G4 comparison was run.

## A. Finding

Candidate A offers attributed model **point values**, but uses a no-slip reduction, unequal wheel radii and non-unit unequal gearbox efficiencies. Candidate B's Burger parts list confirms two XL430-W250-T actuators and one ball caster; its digital smart-servo interface and supply rating do not establish MASTER's ideal held winding-terminal voltage or the stipulated two-drive-contact reaction model. Neither inspected source provides a known fixed slip-force law, per-wheel effective capacities that also support the lateral force budget, joint execution-fixed uncertainty bounds, a complete initial-state/obstacle domain, and an independently specified displacement/clearance deadline.

## B. Evidence

- JAEC Table 1, printed p. 178, reports `J_z=0.35`, body mass `15 kg`, half-track `0.2 m`, different left/right wheel radii `0.0825/0.0675 m`, gearbox efficiencies `72.25%/97.75%`, and motor `R/L/K_t` point values. Its p. 175 Eq. (2) explicitly invokes rolling without slipping. Eq. (5), p. 176, models applied armature voltage but does not document a symmetric four-quadrant terminal drive or fixed zero-delay ZOH. The previous `G2_PARAMETER_CONTACT_PROVENANCE_MATRIX_v1.md` cites the table as p. 177; **p. 178 is the corrected printed locator**. The existing matrix was not changed in this review.
- The ROBOTIS Features page's parts list identifies Burger's two XL430-W250-T actuators and ball caster. The XL430 manual gives gear ratio `258.5:1`, input supply `6.5–12.0 V`, a digital packet interface, PWM/velocity modes, and Goal PWM/Goal Velocity control-table entries. These are product/command specifications; they do not by themselves expose commanded/observed winding voltage and current with MASTER's ideal driver semantics.
- The handoff keeps specified values separate from measured intervals and does not import the paper's asymmetric motor points or the manufacturer's supply limits as a complete `Theta` or `V_max`. This separation is scientifically necessary.

## C. Consequence

Candidate A may provide **source-attributed scales for a clearly synthetic sensitivity study**, after missing values are declared synthetic. Candidate B is a lead for a future measured platform study, not a direct realization of the unchanged MASTER plant. Neither supports a physical safety claim or a task-aware G2 experiment now. R22–R24's computed progress interval cannot be used to invent a task threshold.

The phrase “no defensible published/manufacturer-backed envelope was found” must be read **only over these two inspected candidates**. R25 is not an exhaustive platform search. It does not prove that every alternative platform or public data source lacks the needed information.

## D. Status

- **VALID:** source extraction and the negative readiness decision for these two candidates under unchanged MASTER v2.1.
- **NEEDS REVISION in wording only:** qualify the opening/global-sounding negative finding to “neither of the two inspected candidates.” Preserve the p. 178 locator correction in future provenance records.
- **UNVERIFIED:** any other platform's correspondence, independently meaningful task/domain, G2 practical usefulness, and G4 novelty.
- **UNCHANGED:** **HOLD; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED; R5 800/800 NOT_RUN**.

## E. Required action

Do not create a task manifest or run further G2 queries from these source fragments. Incorporate the p. 178 locator and two-candidate scope correction when the provenance matrix is next revised. Await the separate G4 paired-method overlap audit before deciding whether an additional synthetic evaluator is worth building. A physical task-specific study requires an independently declared task and a compatible, measured/model-bounded operating domain; no G3 or hardware work follows from R25.
