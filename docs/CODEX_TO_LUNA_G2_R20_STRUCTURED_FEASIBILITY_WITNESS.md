# Assignment — DDWMR | LUNA-G2-SCOPE — R20 structured feasibility witness

Read `AGENTS.md`, the four canonical `research_context` files, `docs/reviews/CODEX_G2_R19_STRUCTURE_PRESERVING_ENCLOSURE_REVIEW.md`, the R19 handoff, and the R22 G4 review first. MASTER v2.1 remains authoritative. The R17 indices 62 and 74 are consumed **development** inputs.

## Goal

Make one bounded, mathematical feasibility attempt for the proposed shared-variable enclosure on the **unchanged** R17 pair. Produce concrete outward bounds or a precise stopping result. Do not build a general Taylor-model framework before seeing whether a small source-backed instance can retain enough dependence to address the contact, collision and progress bottlenecks.

## Required work

1. State one finite, reproducible representation: shared initial-state and fixed parameter-label variables, time slabs, rational predictor degree, branch/leaf policy, arithmetic limits and all disclosed development choices. Cover the complete declared input box and parameter image with no gaps. The same label and held voltage must persist through every slab.
2. Derive a **numerical outward** nine-state Lipschitz bound on a proved domain, a whole-cell predictor-defect bound, a Grönwall error radius and endpoint carry for every slab. Use the coarse verified R10 tube as an existence/domain aid only if its actual coverage is cited. Handle the clip corners by a global Lipschitz or exact piecewise range rule; do not differentiate `clip` at a corner or the square-root contact reserve at saturation. If the required polynomial/trigonometric range or exponential tail cannot be bounded, name that exact missing primitive.
3. Compute **joint** full-time lower bounds for collision distance and contact margin and an outward task-progress lower bound. Include the entire residual radius in all three predicates. A polynomial-center distance alone is insufficient. Avoid falling back to two independent wheel `beta` maxima plus an independent body-demand product without explaining why that does not repeat R19's zero-reserve loss. Report every leaf/slab bound, including failed ones.
4. Compare the resulting exact bounds with the archived R17 and R19 values for the same two actions, obstacle, horizon, parameter cell and `1/20` progress threshold. A positive result requires nonnegative full-hold collision **and** contact margins plus the frozen progress criterion for at least one action. If that is not obtained, report the first bound that prevents it and decide whether this particular representation should stop. Do not label a failed sufficient bound as an unsafe true trajectory.
5. Distinguish any DDWMR-specific dependence retained by the construction from generic Taylor/residual validated-IVP machinery and from the Auer reconstruction. Do not assert novelty. Give a compact work/size estimate for the attempted representation; a proof that is computationally unmanageable is not a useful G2 result.

## Execution boundary

Exact-rational offline development calculations on the two **saved R17 query inputs** are within this assignment. They are not fresh native rows or validation evidence. Do not call the R5 `run_query`, a native worker, stage, retry, 800-row study, G4 comparison query, controller or experiment. Do not alter saved R17 or G4 artifacts, and do not commit or push. A small isolated prototype and its source may be retained if needed for the numerical bounds, but no general producer/checker build-out is requested in R20. If a required proof obligation fails, stop and report it rather than repairing the plant or query silently.

Save a full Markdown handoff in `docs/reviews/`, naming all source and saved input artifacts and separating proved bounds from conjectures. Reply to the user in exactly three short lines:

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE or BLOCKED; zero new native rows; R5 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
