# Codex review — G2 R7 preparation and exact R6 two-query stage

**Date:** 2026-10-03  
**Decision:** **ACCEPT_R7_STAGE_IMPLEMENTATION_FOR_EXACT_TWO_QUERY_RUN**. This is technical acceptance of one development pilot under a separate exact-scope execution receipt. It does not accept a usefulness result, the 800-row study, G2 PASS, or physical correspondence.

## Finding 1 — exact data and provenance

**Evidence.** I read `AGENTS.md`, the four canonical `research_context` files, the R7 handoff, R6 protocol, adapter, runner, Windows supervisor, worker, auditor, fixture implementation/report and receipt schema/template. I independently rehashed the R6 manifest (`9d9e9ba3f5448d985de4da5298155f9f5fdd3e191039c627370f1f48fd085cfa`) and source closure (`df8622ce0515c84846d1504cbd6304807ccac82ce1c69526a3fe9aedac06809a`); 95/95 listed dependency hashes match. The first 74 entries exactly preserve the R5 source closure. The two ordered rows are:

1. `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_L0_R0`, R5 index 12, canonical query SHA-256 `d5648569b11c576c8cc0ecb07c5096c21b06fe3a5e849358f254770649465471`, native input SHA-256 `422afd0448a184f4f67262c6338593c871739b41fb677e8ab1d6b566d18b93ac`.
2. `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lp1_Rp1`, R5 index 24, canonical query SHA-256 `105a0710185446312933ec8c92922acd1db0f3af0e999d67207ccd70534b4808`, native input SHA-256 `70301bc5df76aab2dfdb8bef5135592fbf0063af6799b0f0eb119f4873b2cf9a`.

Both are development overlap selected after an R5 `UNKNOWN`; neither is a blind holdout. The R5 one-query provenance erratum remains in force.

**Consequence.** The pair can answer one local action-sensitivity question without changing the 800-row study artifact or its denominator.

**Status:** VALID for exact input binding and development-only lineage.

**Required action:** Report both overlap IDs separately in later work; keep the R5 manifest 800/800 `NOT_RUN` and preserve the R5 consumed result.

## Finding 2 — one-shot execution and read-only replay

**Evidence.** The public runner requires an exact receipt and this review before creating a stage directory. The receipt binds config, manifest, closure, both ordered row hashes, limits, runtime, namespace and code hashes. The stage is one-shot; row intents precede each native call. A valid `UNKNOWN` permits the already ordered second row, while malformed output, invalid replay or a resource stop aborts without retry. The worker accepts only the two pinned query hashes and calls `run_query` once. The auditor reads the publication bundle, checks exact file membership/hashes and stage/row bindings, then recomputes R3 and R2 proof results. The R6 source records 22 non-query fixtures; the stored report says 22/22 PASS with zero native calls. I inspected its fixture implementation and report, without rerunning the suite or invoking `run_query`.

**Consequence.** The stage has a bounded, independently replayable evidence path. End-to-end publication under the production receipt and live native query is still unobserved; this run is the first such check.

**Status:** ACCEPT for the exact two-query development run.

**Required action:** Preserve intent, checkpoint, terminal, publication and auditor output. If the stage is incomplete, report the consumed intents and stop; do not repair, substitute or retry.

## Finding 3 — resource and scientific limits

**Evidence.** The supervisor creates Windows processes suspended, assigns them to Job Objects before resume, enforces one query process, two stage processes, memory/CPU limits, bounded streams and kill-on-close. One 75-second monotonic deadline covers the stage coordinator and bounded publisher after preflight. The preflight itself is outside that timer. Fixture evidence includes reduced-cap timeout, memory, CPU, output and nested-Job checks. These fixtures are not a live R6 stage measurement. The protocol's positive-action trigger requires a replayed `CERTIFIED` safety record and task-eligible lower progress meeting `1/20`, while the nominal action lacks the corresponding certificate or task eligibility. This trigger only motivates a later study.

**Consequence.** Even a positive two-row contrast is local development evidence. It cannot establish general usefulness, a voltage selector, physical safety or recursive feasibility.

**Status:** VALID as a limited pilot plan; G2 remains UNVERIFIED.

**Required action:** Run the exact stage once under the source-bound receipt, then review raw proof and audit outcomes before deciding whether a new study design is warranted.

## Final disposition

**GO: the exact two R6 pilot rows only**, through `docs/CODEX_TO_LUNA_G2_DECISION_DOMAIN_R8_TWO_QUERY_EXECUTION.md` and a separate write-once receipt. Pilot at review: **0/2**; R5 study manifest: **800/800 `NOT_RUN`**. Research status: **HOLD; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED**.
