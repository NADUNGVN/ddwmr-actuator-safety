# Assignment — DDWMR | LUNA-G2-SCOPE — R19 enclosure research

Read `AGENTS.md`, all four canonical `research_context` files, `docs/reviews/CODEX_G2_R18_TWO_ROW_ENCLOSURE_DIAGNOSIS_REVIEW.md`, the R18 handoff, the accepted G2 analytic candidate and Cases A/B/C, and the R10/R11 source before doing research.

## Objective

Find **one mathematically sound, concrete improvement** to the one-hold enclosure that addresses the observed R17 loss of both slip/contact reserve and collision separation. Spend this iteration on the enclosure mathematics rather than another stage/receipt/guard revision. The exact reduced plant, clip law, held voltage, full initial box, joint parameter image and execution-fixed labels must remain intact.

## Required work

1. Compare the current interval Picard candidate, componentwise endpoint carry and pose/contact projections with one promising structured alternative. An exact linear actuator predictor plus certified nonlinear remainder, a centered or affine validated enclosure, or a rigorously covered subdivision are possible directions, not mandated solutions. Identify where the alternative retains the state/parameter/time dependence the present boxes discard. Do not assume monotonicity or differentiability of the general MASTER traction law; any use of a special property must be confined to the declared clip instance.
2. Write the inclusion argument for the **whole hold**, including outward error bounds, coverage of the complete initial and parameter cells, a single hidden label through all slabs, and carried endpoint containment. Give the contact and collision lower-bound formulas, including behavior when a slip interval reaches the clip corner. Do not differentiate the square-root reserve near saturation without a separate valid regularity proof.
3. Use the consumed R17 indices 62 and 74 as **development diagnostics only**. Report exact or certified outward bounds showing whether the candidate can improve the relevant quantities: at least one wheel's slip/reserve, joint pose distance, and task-progress lower bound. If a full proof-backed positive bound is not yet available, identify the exact missing lemma or data and give a falsifiable next step. Do not tune the obstacle, task threshold or two actions to obtain a desired outcome.
4. End with a scientific decision: pursue this candidate or stop it. If pursued, specify the smallest source/checker artifact needed for independent mathematical review and a **fresh, prospectively declared** matched voltage challenge. A result on the consumed pair will remain development evidence and cannot unlock the 800-row study.

## Execution boundary

This assignment authorizes source inspection, exact derivation and isolated candidate design. It grants **no native query, worker, stage, retry, new real row, 800-row study, G3, controller, experiment, commit or push**. Do not modify the R17 artifacts or the G4 branch. If the method cannot retain the required dependencies or cannot be checked independently, report the blocker directly rather than building more protocol machinery.

Save a source-backed Markdown handoff in `docs/reviews/` with precise formulas, file/record references and an explicit VALID / NEEDS REVISION / BLOCKER / UNVERIFIED disposition for each claim.

Reply to the user in exactly three short lines:

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE or BLOCKED; zero new native rows; R5 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
