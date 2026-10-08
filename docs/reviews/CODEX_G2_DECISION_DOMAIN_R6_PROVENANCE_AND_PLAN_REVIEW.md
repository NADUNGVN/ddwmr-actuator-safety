# Codex review — G2 R6 provenance erratum and matched-action plan

**Date:** 2026-10-03  
**Session reviewed:** `DDWMR | LUNA-G2-SCOPE`  
**Handoff:** `docs/reviews/LUNA_TO_CODEX_G2_DECISION_DOMAIN_R6_PROVENANCE_AND_NEXT_QUERY_PLAN_FULL_HANDOFF.md`  
**Authority:** MASTER v2.1 and `AGENTS.md`.

## Decision

**ACCEPT the separate R5 provenance erratum. ACCEPT the two-action R6 document as a development-stage diagnostic design, subject to the corrections below. GO to scoped implementation preparation; NO-GO to execute either R6 query or the 800-row study under the present draft.** No R6 executable, source closure, independent auditor or hard resource supervisor has yet been reviewed. R5 remains one consumed, replayable `UNKNOWN` preflight with a damaged receipt. The locked 800-row manifest still has 800 `NOT_RUN` records.

## Finding 1 — erratum accurately preserves the provenance defect

**Evidence.** I recomputed the raw SHA-256 of the erratum (`9f2b939785998408a77f7d486606e54d74e84e929d594d35ea091a2fc6532df4`) and the R6 protocol (`8ea158a2533c963ba66571be182659742dbe40f048f71de18f677f7aae5c6a79`); both match the handoff. The R5 receipt hash is still `5672096c8c3c636dd51bef77f109bc7496cb410dfb82b49a00aa776ae51d62d0`. Its instruction field contains literal ASCII question marks and self-hashes to `4e5e84ad4357445ad9fb622fa2ae0301bde88e43d18d8a2de86772a4b1871a2f`, different from the handoff quotation's UTF-8 hash `13e209f5a3f0de042998618b4703b9fc379b40a3b6ab8f5041dddbae20ade1b6`. The erratum correctly states that this quotation hash does not authenticate the original conversation event. The reported PowerShell 5.1 native-stdin encoding mechanism is plausible and reproduced in the handoff, but I did not independently rerun that shell reproduction or recover the historical stdin bytes. All nine R5 bundle payload hashes in `COMMIT.json` still match; the locked R5 manifest still has 800/800 `NOT_RUN` records.

**Consequence.** The erratum documents the defect without altering the evidence that was actually consumed. It does not retroactively make the R5 receipt verbatim.

**Status:** VALID provenance correction, with the historical encoding path qualified as a reproduced mechanism rather than a recovered byte trace.

**Required action:** Preserve the receipt, attempt marker, checkpoint and bundle exactly. Use the erratum as a separate note; do not silently repair or retry R5.

## Finding 2 — proposed two rows are matched in their frozen inputs

**Evidence.** I inspected R5 source indices 12 and 24 and independently reconstructed their native queries through the existing read-only R4 row binder. Their canonical query hashes are respectively `d5648569b11c576c8cc0ecb07c5096c21b06fe3a5e849358f254770649465471` and `105a0710185446312933ec8c92922acd1db0f3af0e999d67207ccd70534b4808`; their native input-payload hashes are `422afd0448a184f4f67262c6338593c871739b41fb677e8ab1d6b566d18b93ac` and `70301bc5df76aab2dfdb8bef5135592fbf0063af6799b0f0eb119f4873b2cf9a`. These match the protocol. The rows share the same `S_LOW_NEG` state cell, `D_NEAR_CENTER` scene, 250 ms horizon, parameter-image hash `c653a4f0f0b76e5d36fffa6e0cab822eac3c949955a2348e98ae9cdf597fe6be`, evaluator profile and progress threshold. Their voltages are `(0,0)` and `(+1,+1)`.

**Consequence.** The proposed stage isolates held-voltage choice within this one formal-model cell. It may reveal different sufficient bounds, but no result for either proposed action is known yet.

**Status:** VALID exact-row design for a local diagnostic; two R6 calls remain unrun.

**Required action:** Preserve the exact IDs/order and input hashes if this diagnostic is implemented. Any changed row requires a new version and review.

## Finding 3 — development selection and overlapping study IDs need explicit accounting

**Evidence.** The R6 pair was chosen after the R5 negative-full-voltage `UNKNOWN` became known. The protocol calls it a fixed action contrast, which is true for prospective R6 outcomes, but it must not be described as selected before *all* related outcomes. Both R6 IDs are rows inside the unchanged 800-row R5 study manifest, at indices 12 and 24. A future separate R6 pilot would therefore evaluate exact inputs also present in that manifest, even if the manifest's stored status remains `NOT_RUN`.

**Consequence.** The stage may be reported as a two-row development pilot, not an independent test set. After it runs, “800/800 NOT_RUN” can describe the unchanged locked manifest artifact only; it cannot mean no project evaluation exists for those two inputs. Later study reporting must identify overlap and avoid treating pilot and study results for the same ID as independent observations or silently rerunning them under a one-shot rule.

**Status:** DESIGN CORRECTION REQUIRED before freeze or execution.

**Required action:** Version the protocol with a cross-study ID/lineage policy: fixed universe denominator, pilot overlap flag, reuse or rerun rule under matching or changed source identities, and explicit reporting of already evaluated exact inputs. State that R5 informed this development-stage selection.

## Finding 4 — the scientific target is diagnostic, not yet the G2 usefulness obligation

**Evidence.** The R5 exact rational replay has negative sufficient lower bounds for collision, contact and endpoint progress. The stored result is `UNKNOWN`; that does not predict either R6 action's result or prove unsafety. The proposed pair samples just one state/scene/horizon and has no predeclared decision policy or downstream task comparison. Even a certified/unknown contrast would be a local output distinction of the configured evaluator.

**Consequence.** The R6 pilot can diagnose action sensitivity and protocol operation. It cannot alone establish useful voltage selection, practical conservatism or a publishable G2 contribution. The main 800-row study and parameter-provenance questions remain open.

**Status:** VALID limited diagnostic purpose; G2 usefulness UNVERIFIED.

**Required action:** Specify in advance which result would motivate a broader matched-action study, and which outcomes (including two UNKNOWNs) stop the usefulness claim. Keep R5 as separate exploratory context.

## Finding 5 — execution controls and authorization basis

**Evidence.** R6 is `DRAFT_NOT_FROZEN_NOT_AUTHORIZED_NOT_RUN`: the adapter, runner, supervisor, auditor, receipt and exact source closure do not yet exist. The proposed Windows Job Object, wall/CPU/memory/output caps are design targets, not verified enforcement. The R5 15-second check was cooperative. MASTER v2.1 and `AGENTS.md` already record the user's authorization for scoped G2 validation coding and offline evaluation, with the user relaying Luna work. The protocol's demand for a *new* user permission message is a draft workflow choice, not a requirement of that authority. A future stage still needs an exact, reviewable technical scope and a source-bound execution receipt; it must not fabricate or misquote a fresh user event.

**Consequence.** Implementation can proceed under the existing scoped authorization. Query execution should wait for independent source/resource review, because the needed code and controls have not yet been built, not because permission for scoped validation is absent.

**Status:** GO to implementation preparation only; NO-GO to native R6 calls now.

**Required action:** Build a versioned R7 implementation candidate and non-query failure-path evidence. Bind any future receipt to the reviewed source, exact IDs, limits and current assignment. Record the existing W1 user authorization truthfully; do not require the user to send redundant permission or invent verbatim text. Source review will decide the exact run scope.

## Final disposition

R6 erratum **ACCEPT**; R6 pair **ACCEPT as a local draft diagnostic with accounting corrections**. No native R6 query was run in this review. Preserve **HOLD; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED**. Next assignment: `docs/CODEX_TO_LUNA_G2_DECISION_DOMAIN_R7_STAGE_IMPLEMENTATION_PREPARATION.md`.
