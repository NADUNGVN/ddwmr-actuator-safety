# Codex review — corrected W2 v6/local-Auer development comparison

**Date:** 2026-10-08 (Asia/Saigon)  
**Repository:** `NADUNGVN/ddwmr-actuator-safety`  
**Branch/HEAD:** `main` / `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`  
**Scope:** saved-artifact inspection and source review of the corrected three-action-per-method development comparison. No producer, native replay, fixture or query was run by Codex. Codex wrote only its own review/continuation documents and inspection ledger.

## Finding

The corrected G4 execution is internally hash-consistent and completed the authorized development comparison: three v6 calls followed by three local-Auer calls, no retry, no reported binding/replay error, and the compute lock was released. The scientific result is limited to the disclosed synthetic development task.

The independent G2 audit currently available (`G2_W2_G4_WRAPPER_INPUT_SCORER_AUDIT_FULL_HANDOFF_v3.md`) predates the final corrected freeze and therefore does not close the final peer-audit dependency.

## Evidence

- `source_closure_v4.json`: 77/77 entries; Codex rehashed all entries with zero mismatch.
- Cross-file path/hash scan over the freeze, receipt, source closure, preflight, phase receipt and result manifest: 181 references, 135 unique files, zero mismatches.
- The saved preflight's 10 source-hash pins and 71 input-hash pins match current bytes. Inspection results are in `CODEX_W2_V6_CORRECTED_EXECUTION_INSPECTION_2026_10_08.json` in this directory.
- `preflight_report_v4.json`: 74/74 nonquery checks, zero numeric producer calls, three v6 fixture stubs and three Auer fixture stubs.
- `matched_phase_receipt_v4.json`: six ordered results, v6 calls 3, Auer calls 3, retries 0, errors empty, lock released.
- The live protocol, manifest, benchmark, native snapshot and freeze agree on the benchmark and snapshot hashes.

### Matched development outcome

| Method | Zero | Nominal | Alternative | Verified eligible set |
|---|---|---|---|---|
| v6 | safety certified; progress upper `< 7/20` | safety certified; progress upper `< 7/20` | safety certified; progress lower `>= 7/20` | `{alternative}` |
| local Auer reconstruction | `RATIONAL_BIT_LIMIT` | `RATIONAL_BIT_LIMIT` | `RATIONAL_BIT_LIMIT` | `{}` under the frozen profile |

The v6 progress intervals are `[0.177582288184, 0.240398241242]`, `[0.270758520755, 0.333574473811]`, and `[0.363934753325, 0.426750706380]` m. Native and common replay passed for all three v6 rows. Their collision and contact lower margins are positive.

Each Auer run stopped before accepting a step at the declared 32,768-bit cap. The pre-operation estimates were 33,327, 33,327 and 33,285 bits; completed-result maxima were 32,167, 32,167 and 32,134 bits. The saved diagnostics identify `fraction.pow` and `RATIONAL_BIT_LIMIT`. All three began with one attempted two-second step. The solver halves only after completed native inclusion failure; its resource exception exits before that branch. Its exact rational arithmetic differs from v6's outward 96-bit grid. These are material qualifications when interpreting the local availability result.

The failure primitive and operand widths are preserved, but the diagnostic stage is `unclassified`; the records do not by themselves pinpoint which caller of `fraction.pow` stopped or capture its operand values. A source-based hypothesis about the transcendental remainder must be labelled as such. No replayable accepted Auer step exists in this phase, and no Auer collision/contact or progress output was measured.

The three paired actions were already observed G2 development actions. They are not held-out confirmation data. Legacy R5 (800 rows) and the Auer 1,944-row batch remain `NOT_RUN`.

Counters remain G2 24/24 native development attempts, G4 candidate 4/12 worker attempts including the prior preproducer failure, G4 Auer 3/12, and confirmation 0/24 per method. Codex added no numerical attempts.

## Consequence

The comparison supports only this statement:

> On the disclosed synthetic two-second development task, the frozen v6 pipeline replayed one task-eligible action, while the frozen local Auer reconstruction produced no proof-complete row because all three attempts reached its declared rational-bit limit.

It does not support universal method superiority, generic novelty, practical robot timing, held-out generalization, physical-platform correspondence, or mathematical infeasibility of Auer.

The prior audit's conclusion that generic centered-residual mathematical novelty is unsupported remains active. The new cross-method observation is a qualified local profile/implementation availability asymmetry, pending final semantic audit. It does not establish a publishable contribution. G2/G3/G4 remain unverified pending separate gate decisions.

## Status

**PARTIAL — execution evidence accepted for narrow development accounting; final G2 peer audit still pending.**

Project status remains:

`HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical-platform correspondence UNVERIFIED.`

## Required action

1. `DDWMR | LUNA-G2-SCOPE`: perform a read-only final audit of the exact v4 freeze, all six saved outcomes, the 74/74 preflight and the final worker/setup/common-scorer sources. Verify the empty-intersection progress rule, full-hold/label/endpoint bindings, fail-before-marker mutations, and the Auer bit-limit attribution. Do not run a producer, query, retry or cap change. Publish the final W2 handoff and updated STATUS.
2. `DDWMR | LUNA-G4-AUER`: independently finish resource/profile attribution from saved records and source. Explain the exact-rational versus fixed-grid policies, first-step/halving behavior, observed versus estimated bit widths, and limitations of the unclassified failure stage. Assess whether this supports a meaningful confirmation hypothesis. Do not run new queries, change the closed freeze or increase caps from these outcomes. A terminal scoped negative/partial conclusion is appropriate; a proposed new diagnostic must be explicitly prospective and separate from the completed run.
3. Both owners close their verification reports and exchange conclusions through files under W2; no routine Codex GO wait. Codex reviews the consolidated package for any subsequent scientific decision. Do not promote any gate or start G3 from this comparison alone.

Follow [the continuation assignment](../../CODEX_W2_V6_FINAL_RESULT_AUDIT_AND_RESOURCE_ATTRIBUTION.md) for the two completion products and chat format.
