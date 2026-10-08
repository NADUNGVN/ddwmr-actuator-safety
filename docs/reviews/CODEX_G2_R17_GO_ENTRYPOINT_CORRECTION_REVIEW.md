# Codex review — G2 R17 GO entrypoint correction

**Date:** 2026-10-05  
**Reviewed handoff:** `LUNA_TO_CODEX_G2_R17_GO_ENTRYPOINT_CORRECTION_FULL_HANDOFF.md`  
**Disposition:** **GO for exactly the ordered offline R5 pair 62 then 74**. This is bounded evidence acquisition, not G2 PASS or authority for the 800-row study.

<!-- CODEX G2 R17 EXACT SCOPE GO -->

I read `AGENTS.md`, the four canonical `research_context` files, the R16 review, the R17 handoff, manifest, source closure, runner, checker, worker, source binding, entrypoint fixture source/report and exact-scope decision contract. I independently recomputed **217/217** R17 source-input hashes, including all **192** inherited R16 inputs. The R17 manifest, closure and stored fixture report hash respectively to `a4913d3d0282de6a5d1a16c4c88e3c402a91f1c3dee2df1ea99afd44a71c6bb9`, `5b6838c8da6ae55e33ad4b50c9182122943f669e63e0fa9d92e6a8de3b83ce86`, and `0b3892ec5ff4504f3f4e0482d993d22a8b284b35194b71b65f6f5accaaddb891`. At review time the canonical R17 GO and stage were absent; R17 real rows were 0/2 and R5 study rows were 800/800 `NOT_RUN`.

## Findings

1. **R16 entrypoint blocker repaired.** `load_r17_candidate()` checks source and lineage without rejecting the presence of an exact GO or stage. The absence check lives in `preflight_unstarted_no_go()` and is not called by the authorized runner or read-only stage audit. The runner checks GO before exclusive stage creation; the checker rereads the current GO, requires byte equality with the stored stage authorization, then rebuilds and compares the stage receipt. The stored temporary-mirror fixtures reproduce the R16 rejection, show R17 missing/NO_GO refusal before stage creation, and reach R17 loader → exact GO validation → full stage receipt comparison with a synthetic empty stage. The fixture is control-flow evidence, not a worker or mathematical result.
2. **Fixed pair and source identity preserved.** The manifest retains R5 indices **62, 74**, in that order, with their pinned query hashes. Development indices **0, 12, 24** remain consumed. The decision requires raw manifest/closure/review hashes, exact keys and scope, at most two worker calls, a 60-second worker timeout, 65,536 captured bytes per diagnostic stream, zero native-query calls, zero R5 study rows and no retry. The R17 worker imports a pinned local arithmetic closure and writes a single source-bound record; the independent checker replays any completed record through R11. The earlier R16 exact 19-field receipt parity and stop rule are retained.
3. **Execution limits and interpretation.** No R17 real worker, R10 record or R11 mathematical replay was executed by this review. I performed a non-query probe of the runner's directory-flush primitive on the existing G2 results directory; it completed on this Windows host. A live row can still return valid `UNKNOWN`, a resource stop or invalid/partial evidence. If row 62 stops with `RESOURCE_LIMIT` or `INVALID_OR_INTERRUPTED`, row 74 must remain unattempted. Any durable intent is consumed and cannot be retried. If a stage or checker stops, preserve its raw evidence; do not infer safety or unsafety from an incomplete result.

## Exact execution boundary

Authorize only the R17 one-shot stage for indices **62 then 74**, at most two offline R10 worker calls, with the source-bound GO decision file and limits stated above. The stage may evaluate row 74 only if the fixed stop rule permits it after row 62. Independently replay the produced record(s) and stage receipt, and report terminal hashes, diagnostics, exact outcomes, margins if present, stop reasons and the paired truth-table decision. A positive preparation trigger is not authority to run the 800-row study. No other index, substitution, retry, native R3 query, G3, controller, simulator, experiment or hardware execution is included.

**HOLD persists.** G1 PASS applies only to the restricted reduced model. G2/G3/G4 and physical-platform correspondence remain UNVERIFIED. `UNKNOWN` means inconclusive, not unsafe.
