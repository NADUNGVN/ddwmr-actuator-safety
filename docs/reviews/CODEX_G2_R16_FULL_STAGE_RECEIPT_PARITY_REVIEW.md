# Codex review — G2 R16 full-stage receipt parity

**Date:** 2026-10-05  
**Reviewed handoff:** `LUNA_TO_CODEX_G2_R16_FULL_STAGE_RECEIPT_PARITY_CORRECTION_FULL_HANDOFF.md`  
**Disposition:** accept the narrow receipt-parity correction as source and synthetic-fixture progress; **NO-GO for the two real rows**.

I read `AGENTS.md` and the four canonical `research_context` files earlier in this review, then inspected the R15 review, R16 handoff, manifest, closure, schemas, runner, checker, source binding and fixture source. Independent hash comparison found 192/192 closure inputs matching, including the pinned R16 executable sources. The manifest, closure and fixture-report raw hashes match the handoff (`e8eaa59c676f85431e3ddcbd777a2690cfa57bfb88e00bfed96d9b4b693bba65`, `2217cc2c5e1ac1fce812efc9fe42a9b95f1ae2ada82ca40bb49215f1414ad759`, `36bc1bb56fbd3a86ec09f0d19ff1ac83dab13e74780a43f7c7f8885ecbdd0c86`). I did not run a fixture, worker, mathematical replay or real row. I did not modify source, create a GO, commit or push.

## Finding 1 — the R15 receipt field mismatch is corrected in the source candidate

`r16_stage_contract.py` declares an exact 19-field row shape. The runner's `_run_row()` fills those fields, including the five omitted by R15, and `_build_receipt()` validates the shape. The checker independently derives the same fields from the intent, terminal, diagnostics and record replay before exact receipt comparison in `_audit_stage_evidence()`. The stored synthetic on-disk fixture report covers continue, stop, no-record, partial-intent and complete-pair paths and rejects a stored R15-shaped receipt. These fixtures use stubbed replay and provide no mathematical result for indices 62 or 74.

**Status:** **VALID, narrowly for source/fixture receipt parity**. R16 remains 0/2 real rows; the R5 study remains 800/800 `NOT_RUN`.

## Finding 2 — the candidate loader makes an exact GO impossible to execute or replay

`validation/g2/r16_source_binding.py::load_r16_candidate()` rejects the candidate whenever the canonical GO decision **or** stage directory exists (lines 249–252). But `validation/g2/r16_stage_runner.py::run_stage()` calls that loader before `_load_codex_go()` (lines 376–381). Placing the required GO file therefore raises `R16_CANONICAL_STAGE_OR_GO_ALREADY_EXISTS` before authorization can be read and before a row can run. The independent `audit_stage()` also calls the same loader (checker lines 749–755), so it would reject a real stage directory even if one were created. The missing-GO fixture and synthetic `_audit_stage_evidence()` path cannot detect this production entrypoint contradiction.

**Status:** **BLOCKER for R16 GO**. Creating a GO now would not make the two-row stage executable; an attempted workaround could consume a stage namespace without an accepted result.

**Required action:** version a new candidate. Keep absence-of-stage/GO checks in the unstarted NO-GO preflight, while permitting the production loader and read-only stage audit to validate an exact, source-bound GO and the resulting write-once stage. Add isolated non-query entrypoint fixtures for both states: absent GO refuses before stage creation, and a synthetic exact-scope GO plus isolated stage reaches loader, receipt comparison and audit without a real worker. The latter must fail against unchanged R16. Do not create the canonical GO or stage during fixtures. Re-pin changed source and fixture bytes for a separate review.

## Finding 3 — the inert NO-GO template is not this blocker

The decision JSON Schema allows the optional `template_is_executable` and `assignment_authorizes_execution` fields, while the production `_load_codex_go()` requires an exact executable-key set and `decision=GO`. The template sets both optional fields false and says `NO_GO`; it is an inactive template, not an executable decision. This distinction should remain explicit.

## Gate disposition

**HOLD.** G1 remains PASS only for the restricted reduced model. G2/G3/G4 and physical-platform correspondence remain UNVERIFIED. No R16 row, 800-row study, G3, controller or hardware execution is authorized by this review. Indices 0, 12 and 24 remain consumed; indices 62 and 74 remain unattempted in this candidate. `UNKNOWN` does not mean unsafe.
