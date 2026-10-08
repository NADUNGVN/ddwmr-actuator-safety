# Assignment — DDWMR | LUNA-G2-SCOPE — R26 prospective formal-task screen

Read `AGENTS.md`, all four canonical `research_context` files, MASTER v2.1 §§5–12 and 20–23, `docs/G2_TASK_DOMAIN_INPUT_REQUEST.md`, `docs/reviews/CODEX_G2_R24_PAIRED_BOUND_AND_THRESHOLD_AUDIT_REVIEW.md`, `docs/reviews/CODEX_G2_R25_SOURCE_BACKED_OPERATING_DOMAIN_AUDIT_REVIEW.md`, and `docs/reviews/CODEX_G4_AUER_R23_PAIRED_METHOD_OVERLAP_AUDIT_REVIEW.md` before research reasoning.

## Why this is the next G2 task

The R22–R24 calculations establish a narrow formal matched-action gap but supply no independent task requirement. R25 screened two physical-platform sources and found neither complete under MASTER. We now screen a **prospective task for a reduced-model paper**, without requiring a physical-platform claim. A published navigation/obstacle scenario may supply task geometry, progress/goal and deadline even if MASTER's actuator/contact parameters remain explicitly synthetic. This is a new task-definition search, not a restart of the plant derivation and not a new certificate run.

## Research question and bounded source search

Can a primary research paper or official benchmark specification supply a task with a pre-existing goal/progress measure, deadline or horizon, obstacle/footprint geometry, and initial domain that can be stated without looking at R22–R24 outputs?

1. Declare search terms and inclusion rules **before** comparing candidate scenarios with any computed DDWMR outcome. Inspect at most **three** candidate primary full texts/specifications. Record every inspected candidate, including rejections, with URL/DOI, access status and exact page/equation/table/figure locator. Do not reuse the R22–R24 obstacle, normalized all-one plant, or `40 micrometre` result as the task's rationale.
2. For each candidate, transcribe only what the source actually specifies: direction/goal, success threshold, horizon/deadline, obstacle geometry/motion, footprint/reference point, and initial-state information. Distinguish a task requirement from a reported result, capability limit or plot label. Record units and missing fields. A numerical rescaling or conversion must have a stated source-based reason; otherwise mark it as a new synthetic choice.
3. Map the **task** to MASTER's nine-state, fixed-voltage-hold formal problem without claiming the source's robot obeys MASTER. Keep model parameters/contact law/driver semantics separately labeled `source-supported`, `synthetic`, `incompatible`, or `unknown`. Preserve execution-fixed joint parameters and the full-hold collision/contact predicates.
4. Give a readiness decision for each candidate: `READY_FOR_PROTOCOL_REVIEW` only if one fixed prospective task and formal operating domain can be written without using certificate outputs; `NEEDS_OWNER_INPUT` if a short, named list of missing mission choices remains; or `INCOMPATIBLE` if the task cannot be mapped without changing MASTER. A source-inspired synthetic benchmark is allowed as such, but does not establish physical correspondence.
5. Recommend **one** path forward. If no candidate is ready after this bounded search, stop the source-search branch and provide the smallest owner decision needed to define a formal task. Do not start a fourth search cycle automatically. Do not set a threshold from R22–R24 intervals, pick a favorable result, or imply that matched ranking gives a common task threshold.

## Execution boundary

This is read-only source and protocol research. Run **zero** native G2 rows, queries, workers, stages, retries, 800-row study entries, Auer queries, or matched comparisons. Do not create a query manifest, use saved outputs to select cases, revise MASTER, build G3/controller/hardware code, commit, or push. A task candidate remains a proposal until Codex reviews its source and quantifiers. Preserve **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED**.

Write one complete Markdown handoff under `docs/reviews/`. Reply in exactly three short lines:

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE or BLOCKED; zero native rows; R5 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
