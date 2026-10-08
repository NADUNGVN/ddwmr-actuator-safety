# Codex review — G4 Auer R20 path binding

**Date:** 2026-10-05  
**Reviewed handoff:** `LUNA_TO_CODEX_G4_AUER_R20_PATH_BINDING_FULL_HANDOFF.md`  
**Disposition:** **VALID for retrospective, read-only replay of the ten preserved R19 Stage 1 pairs.** This is not a prospective stage GO, full-batch authorization, G4 PASS, or a physical safety result.

I read `AGENTS.md` and the four canonical `research_context` files, then inspected the R19 execution handoff, R20 helper, R19-to-R20 checker diff, non-query fixture source, saved reports and representative emitted audit schema. I independently checked the raw hashes of the five R20 candidate sources and both saved reports against the handoff. The preserved R19 Stage 1 tree contains no Windows reparse-point entries. I executed the R20 checker once against the saved R19 stage and authorization, in read-only mode; it exited 0 with `PASS_R20_REPLAY_OF_R19_STAGE`, ten attempted and completed pairs, 20 method terminals, 20 audit terminals, zero retries and zero substitutions. No producer, query, stage runner or composition auditor was invoked by this review.

## Finding 1 — path binding

**Evidence.** The R19 checker compared the guard and terminal `result_path` as raw strings. The saved first pair uses Windows backslashes in the guard and forward slashes in the terminal for the same absolute `result.json`, so the original R19 checker exited 2. R20 derives the allowed result path from the checker-controlled stage, query index and method. It requires both recorded paths to be absolute, free of parent traversal, inside the stage, at the exact expected resolved path and the same filesystem file. The pre-existing one-invocation, size and SHA-256 checks remain. The seven executable non-query fixtures accept both slash directions and reject an outside path, traversal and another in-stage artifact.

**Consequence.** The original path-string failure is repaired for the preserved R19 stage without changing its data. **Status: VALID for this read-only replay.** The symlink fixture was `NOT_RUN_PLATFORM_LIMIT` because this Windows account could not create a symlink. The helper source checks symbolic-link components, and the actual saved stage has no reparse points. A prospective checker still needs an executable Windows reparse/junction negative check or an equally explicit, independently audited guard.

## Finding 2 — audit schema compatibility

**Evidence.** The R20 diff changes only the path-binding calls, two audit-field lookups and the replay status label. The pinned emitted audit guard uses `status: PASS`; its composition report records zero auditor invocations in `resource_accounting`. R19 looked for the absent `audit_status` and absent root-level invocation counters. R20 checks the emitted fields and still requires zero auditor producer/matched/batch invocations and the stored report/guard hashes. A representative saved audit record has these exact fields, and the full R20 checker traversed all applicable audits.

**Consequence.** This is a schema correction, not a change to the producer, mathematical proof, query results or common predicate. **Status: VALID within the pinned R19 artifact schema.**

## Finding 3 — interpretation of the ten pairs

**Evidence.** The saved R19 runner/checker logs record the original exit-2 contract blocker. The independent R20 replay now accepts all ten preserved pairs. Within those ten, R3 has six `CERTIFIED` and four `UNKNOWN`; Auer has nine `CERTIFIED` and one proof-complete common `UNKNOWN`. `UNKNOWN` is inconclusive. Four historical IDs remain separate, ten R19 IDs are consumed, and 1,930 continuation IDs have never been attempted.

**Consequence.** The ten pairs are usable as a **post hoc revalidated pilot**, with the original R19 checker failure and R20 correction disclosed. They are not a locked prospective full-grid comparison, evidence of method superiority, G4 novelty closure or G2 usefulness. The pilot does not show a certification-coverage advantage for R3. **Status: VALID as bounded pilot evidence; broader scientific comparison UNVERIFIED.**

## Required action

Keep all R19 artifacts immutable and do not retry their ten IDs. Before any new G4 stage, prepare a separately versioned prospective runner/checker, source closure, exact ordered schedule and GO binding. First analyze the ten preserved pairs at matched assumptions, including each `UNKNOWN` reason, proof size, runtime and common predicate, to decide whether a larger comparison is scientifically justified. No later stage or 1,944-query batch is authorized by this review.

Project status remains **HOLD**. G1 is PASS only for the restricted reduced model; G2/G3/G4 and physical-platform correspondence remain UNVERIFIED.
