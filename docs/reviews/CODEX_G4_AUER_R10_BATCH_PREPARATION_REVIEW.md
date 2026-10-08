# Codex review — G4 Auer R10 staged-batch preparation

**Date:** 2026-10-03  
**Session reviewed:** `DDWMR | LUNA-G4-AUER`  
**Handoff:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_R10_BATCH_PREPARATION_FULL_HANDOFF.md`  
**Authority:** MASTER v2.1 and `AGENTS.md`.

## Decision

**ACCEPT the R10 source snapshot and static schedule as preparation evidence. NO-GO for Stage 1 or any other R10 batch query.** No stage-authorization receipt is issued by this review. The R9 first-ID preflight remains one separate complete pair; the R10 batch remains **0/1,944**. This review does not promote G4, novelty, or any physical-safety claim.

## Finding 1 — source identity and fixed schedule

**Evidence.** I independently recomputed the exact-byte SHA-256 of the R10 manifest (`e03d7987b671bfb9065a1dc04b0c7bad5995e928656a15293982d14615567d23`), closure (`f9a742502c8f4586bfeda4f30e30f257b1c0667365b2e0646fc6b5fbf6901b87`), schedule (`212b6a09526379188acad46aa05070626b5248a76bc64047d18dd47f9c136e9c`), runner, summary builder, schemas, receipt template and fixture report. All 359 listed R10 dependency paths exist and match their recorded hashes; all 316 R9 dependency path/hash pairs are preserved. I independently reconstructed the scene/state/horizon/action seed rule from the R9 source manifest: it gives the recorded 12 seeds, with the first as the read-only carry-in. The seven stage arrays partition the other 1,943 distinct IDs at sizes 11, 36, 96, 450, 450, 450, 450; their seven LF-joined digests match. The manifest still says `batch_start_authorized=false` and zero attempted rows.

**Consequence.** Static identity, ordering and carry-in accounting are valid. The selection rule is prospective for the remaining batch outcomes; the R9 preflight outcome was already known when R10 was prepared, so the protocol should not say the entire rule was fixed before *any* query outcome was seen.

**Status:** VALID static preparation only.

**Required action:** Retain the exact R10 bytes and report the preflight as a separate stratum. Describe the chronology precisely.

## Finding 2 — one-stage receipt does not enforce one global run

**Evidence.** `run_authorized_stage` accepts any caller-supplied `output_root` within `results/validation/g4/auer2013` (`validation/g4/batch_stage_runner_v3_r10.py`, lines 1067–1076). `validate_stage_authorization` binds manifest, closure, schedule, stage and ordered-ID digest, but not the output root (lines 533–562). The existing-stage refusal looks only for a terminal receipt inside the selected root (lines 1087–1090). Thus the *same* authorization receipt can be reused against a second empty root to launch the same stage and ID again. Per-path exclusive creation does not enforce the declared one-invocation policy across roots.

**Consequence.** The no-retry and stage authorization claims are not enforced at the batch boundary.

**Status:** BLOCKER before Stage 1.

**Required action:** Bind one canonical batch root to the candidate/authorization and enforce a single stage namespace. Reject another root and any prior attempt or intent for that stage. Add a non-query duplicate-root fixture.

## Finding 3 — resume and stage progression can trust incomplete receipts

**Evidence.** `_verify_record_artifacts` checks only artifact entries that a receipt happens to list with non-null hashes (lines 692–702). `_read_verified_terminal` validates an R9 result only *if* the receipt lists a hashed `result` path (lines 705–727); it does not require the invocation intent, verify `intent_sha256`, require result/guard/proof/common artifacts for a positive result, or reconcile `raw_outcome` with the result and guard bytes. `_validate_audit_receipt` likewise does not require or parse its report and guard artifacts or reconcile the receipt's `audit_status` with the stored report and guard (lines 730–751). `pair_disposition` then accepts `PASS`, `CERTIFIED` and `PASS_ON_SUPPLIED_TUBE` directly from those receipt fields (lines 613–633). Prior-stage progression uses these same readers (lines 1009–1065). The eleven published fixtures are stub-level checks and do not exercise this missing-artifact/false-status path.

**Consequence.** A receipt with missing evidence and favorable status fields can be counted as a complete valid pair on resume or as a prior-stage prerequisite. This falls short of the protocol's independently verified completion rule.

**Status:** BLOCKER before Stage 1.

**Required action:** Require and verify the write-once intent, its exact hash and matching command/bindings; require the expected terminal artifacts for each positive status; reconcile raw receipt fields with result, worker guard, audit report and audit guard; verify the R9 result and stored audit bindings before counting a valid pair. Reject missing or contradictory evidence. Add non-query fixtures for absent artifacts, altered intent, favorable raw status with rejected/missing audit and changed result/guard bytes.

## Finding 4 — malformed output may leave an unclassified attempt

**Evidence.** After a guarded worker exits, `_run_guarded_arm` parses `result.json` and the guard using `strict_json` before writing the terminal receipt (lines 820–865). `_run_guarded_audit` does the same for its report/guard (lines 932–965). A malformed JSON file raises `LockError` before the write-once terminal receipt. `run_authorized_stage` then exits without its stage terminal receipt (lines 1103–1169). The already-written intent prevents a retry, which is appropriate, but the promised lossless terminal classification is absent. The code also loops over both arms before auditing available artifacts, so an exception in the first arm prevents the separate audit of any available first-arm output.

**Consequence.** A real malformed proof/result/guard or interrupted wrapper can stop the stage without the complete attempt classification claimed in the protocol. The summary may detect an intent but cannot recover the raw outcome from a terminal receipt that was never written.

**Status:** BLOCKER for the claimed attempt ledger; no real-process recovery evidence yet.

**Required action:** Hash and preserve every raw artifact even when parsing fails; write a terminal classification for normal wrapper return, timeout or parse failure where possible; keep the intent-only interruption state if the process is killed before classification. Make the stage summary preserve that distinction. Add non-query failure-path fixtures, including malformed result/guard and audit output. Do not retry consumed intents.

## Finding 5 — derived summary does not verify authorization or stage completion

**Evidence.** `summarize_matched_batch_v3_r10.py` reads per-arm and audit receipts with `authorization_sha256=None` (lines 52–105) and never verifies the stage authorization receipt, its review hash or the stage terminal receipt before labeling a row valid (lines 152–351). It takes method status from receipt `raw_outcome`. The text at line 340 says setup time *and memory* are recorded in each immutable stage receipt, while the stage receipt at runner lines 1146–1168 contains neither such measurement. The present empty summary is internally consistent and contains all 1,944 rows; it does not exercise these post-run paths.

**Consequence.** A later summary could present an unauthorized or insufficiently verified row as comparable evidence, and its resource-accounting description overstates the stored data.

**Status:** BLOCKER for a trusted batch comparison; empty-summary accounting VALID.

**Required action:** Verify stage authorization/review and stage receipt against the canonical root for every attempted row; preserve interrupted stages distinctly. Derive comparison eligibility only from fully checked arm/audit artifacts. Record actual setup metrics or correct the description. Keep all 1,944 IDs, the preflight stratum, UNKNOWN and method asymmetry.

## Finding 6 — scientific and execution scope

**Evidence.** R10 contains 11 synthetic non-query fixture results, an empty summary and the earlier one-pair R9 preflight. I did not invoke either producer, launch any R10 stage, or rerun a fixture. The source inspection cannot establish real-process interruption recovery, wrapper/Job Object behavior for all rows, comparative performance or an inferential analysis under stagewise stopping. Stopping at the first nonvalid pair can leave outcome-dependent unobserved rows.

**Consequence.** The static schedule is useful preparation, but execution and scientific comparison require a corrected, separately reviewed candidate. A 1,944-ID denominator must not be presented as 1,944 observed independent samples.

**Status:** G4 UNVERIFIED; batch **0/1,944**.

**Required action:** Prepare a versioned correction without modifying R9/R10 evidence. Review source and non-query failure paths before any separate Stage 1 decision. A statistical interpretation plan remains necessary before comparative claims.

## Final disposition

**R10 preparation: PARTIAL ACCEPT. Stage 1: NO-GO.** Preserve **HOLD; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED**. The next assignment is `docs/CODEX_TO_LUNA_G4_AUER_R11_BATCH_INTEGRITY_CORRECTIONS.md`.
