# Codex review — G4 Auer R13 prospective runner/checker candidate

**Date:** 2026-10-04  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_R13_PROSPECTIVE_RUNNER_AND_CHECKER_FULL_HANDOFF.md`  
**Disposition:** ACCEPT the checked source inventory, ten-ID schedule and synthetic **method-bundle** contract evidence in their limited scope. **NO-GO for a first R13 stage or any query** because stage-level replay and GO binding still have the defects below.

I read `AGENTS.md`, all four canonical `research_context` files, the R12 review/assignment, R13 handoff, protocol, runner, checker, fixture source/report, manifest, closure, schedule and no-GO template. This was read-only source/artifact review. I did not run a worker, producer, auditor, batch stage or fixture suite.

## Finding 1 — source and schedule identity

**Evidence.** Independent SHA-256 checks matched the handoff's exact manifest (`a583703d84eb9285b1ff12647bbfb40c7a45e2b4b92cfba0035c8bbf49c4ba82`), closure (`3ed81f9fd5ca532ca1e51f845a1c1933cc51b918972972e669904a451bd8fbd1`), schedule (`bb50b4fda8d0bb53bd7554a6cc4147e59cb53bc0044545176d1df2015c3de075`), runner (`0e6be68dbba7a1f3feb1ad97616c7a4ce45ddc8329a2156a7641667efa4f160f`) and checker (`66e5db8ebefba3e5341d712a842b26e1efec8b30bff794edb712db3691470d01`). All 432/432 closure dependency path/size/hash tuples matched the live files. The R13 first-stage list equals the first ten IDs of R12's 1,942-ID continuation sequence, which equals the R10 eligible order after deleting the one consumed R11 ID. The ten-ID digest `58a888845732cc8f5220656444d0b6ae9aa19a96eed1c014a7f907e9fac55bbd` and 1,942-ID digest `8cdd5717aa8a64c50a07ba569353b1e34fd08a353f60cb39b01c64c4b25aac1d` recompute with LF joins and no trailing newline. The R13 batch directory and GO receipt do not exist.

**Consequence.** The current candidate has the intended fixed 1,944-ID denominator and exact first-stage scope. It creates no execution authority.

**Status:** VALID source/order identity; R13 0/10 and R12 0/1,942 attempted.

**Required action:** Preserve R9/R11/R12 artifacts and the two observed strata. Do not retry them, replace an ID or advance to another stage.

## Finding 2 — synthetic method-bundle evidence

**Evidence.** The stored fixture report is pinned by the candidate manifest and records 31/31 expected outcomes: six accepted synthetic receipt classes and 25 class-3 rejections. Source inspection shows the fixture runner calls the R13 `check_method_bundle` contract with synthetic proof/common/audit bytes. It does not invoke a live R3/Auer worker, native proof replay or composition auditor. The prospective checker uses the actual R9 common schema and transitive query/input/result/proof/common/audit bindings; it distinguishes positive, nonpositive and ambiguous records and keeps resource/audit accounting separate.

**Consequence.** These fixtures exercise method-receipt classification only. A synthetic fixture marked `CLASS_1_VERIFIED_CERTIFICATE` is **not** a scientific certificate, and no matched baseline result or runtime conclusion follows. The fixture suite does not establish complete stage-level interruption/replay behavior.

**Status:** VALID as stored synthetic contract evidence; live behavior UNVERIFIED. I did not rerun the fixture suite.

**Required action:** Continue to label synthetic receipts as contract fixtures. Do not pool the R9/R11 observed strata into R13 yield.

## Finding 3 — valid prelaunch stop cannot be replayed

**Evidence.** `batch_stage_runner_v3_r13.py:370-403` explicitly records `STOPPED_BEFORE_FIRST_INTENT` with no attempted ID if a failure occurs before the first R3 invocation intent. The checker intends to validate that record in `check_matched_batch_v3_r13.py:1321-1332`, but its earlier `if not class3 and (len(attempted_ids) != 10 or terminal_state != "STAGE_COMPLETE")` branch at line 1288 rejects a zero-attempt prelaunch stop before reaching that validator. If that guard is corrected alone, line 1327 then references undefined `expected_worker_intents` rather than the computed `expected_method_intents`. The 31 fixtures contain no complete stage receipt for this path; their stage checks exercise prefix/name rejection helpers only.

**Consequence.** A specifically promised, source-generated class-3 stage stop cannot produce a verified fixed-denominator summary. This does not create a false positive certificate, but it breaks the one-shot interruption/accounting contract needed before executing the stage.

**Status:** **BLOCKER** for R13 stage execution and source approval.

**Required action:** Move/check the prelaunch branch before the ten-row-complete assertion, correct the variable reference, and add a synthetic full-stage receipt fixture proving zero attempted IDs, zero worker/audit intents and a verified class-3 stop. Exercise a subsequent read-only restart refusal without launching a query.

## Finding 4 — GO review identity does not establish a GO decision

**Evidence.** `check_matched_batch_v3_r13.py:987-1036` checks that a future receipt says `decision=GO` and cites a hash-matching file whose path begins `docs/reviews/`. It does not check that the cited review actually grants this exact ten-ID stage, nor that it names the reviewed R13 hashes and an explicit GO disposition. Thus a receipt referring to an unrelated or NO-GO review would satisfy this part of the machine check if its other fields were filled. The current no-GO template is correctly non-executable, and no GO receipt currently exists.

**Consequence.** The source-level claim that execution is tied to an independent exact-scope GO review is not yet enforced by the checker. The human workflow still requires Codex to issue an actual authorization, but the prospective runner should reject a contradictory review/receipt pair.

**Status:** **BLOCKER** for automated GO-bound stage launch.

**Required action:** Bind the future GO receipt to a dedicated, machine-checkable exact-scope Codex GO decision artifact or equivalent reviewed decision field, including candidate hashes, ten ordered IDs and stage ID. Reject an unrelated or NO-GO review, and include negative fixtures. Do not create such a GO decision in the correction assignment.

## Final disposition

R13 improves the prospective method-bundle contract, but the exact stage runner/checker pair has not completed its one-shot replay obligations. No first-stage query, retry, GO receipt, G4 comparison, novelty claim or gate promotion is authorized. The previous R11 batch has **1/1,944** attempted universe IDs, with one separate R9 preflight carry-in; R13 remains **0/10**, R12 continuation **0/1,942**. Preserve **HOLD; G1 restricted reduced-model PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED**. The next G4 assignment is `docs/CODEX_TO_LUNA_G4_AUER_R14_STAGE_REPLAY_AND_GO_BINDING_CORRECTIONS.md`.
