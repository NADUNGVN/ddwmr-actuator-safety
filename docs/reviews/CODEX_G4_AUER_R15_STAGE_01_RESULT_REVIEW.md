# Codex review — G4 Auer R15 Stage 1 stopped execution

**Date:** 2026-10-04  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_R15_STAGE_01_EXECUTION_FULL_HANDOFF.md`  
**Disposition:** accept the one-shot stage accounting and the first terminal pair; **BLOCK** the second R3 output as an R15 verified certificate. No continuation or retry is authorized by this review.

I read `AGENTS.md`, the four canonical `research_context` files, the R15 handoff/protocol and pertinent R9/R15 producer/checker source. I independently checked the raw hashes of the stage intent, terminal, second-ID R3 proof, runner capture and stored inventory against the handoff. I inspected the actual second-ID common segment provenance and composition report. I did not invoke a query worker, producer, auditor, stage runner, or fixture suite.

## Finding 1 — exact stop accounting is supported

**Evidence.** The stage terminal reports two attempted IDs from the locked ten-ID schedule, one completed class-1/2 terminal pair, one class-3 stop on the next R3 arm, and eight remaining `NOT_RUN`. The runner exit was 20 (`STOPPED_AFTER_CLASS3`); the stored independent checker reports `READ_ONLY_REPLAY_COMPLETE`. The batch-root inventory contains 42 files. The stage intent and terminal hashes match the handoff. No Auer invocation exists on the failing second ID, and no later ID was run.

**Consequence.** The first pair is a valid protocol observation: R3 authenticated `UNKNOWN` and Auer replayed `CERTIFIED`. `UNKNOWN` is inconclusive, and one pair cannot establish overall method superiority or novelty. The second ID is a consumed, incomplete pair, not a verified R3 success. The R15 stage cannot resume.

**Status:** **VALID** stage accounting; **BLOCKER** for completing R15 Stage 1.

**Required action.** Preserve all R15 bytes. Report the first pair separately, the second ID as class 3, and the remaining eight as not run. Do not retry either attempted ID, auto-advance, or pool this partial stage as a ten-ID comparison.

## Finding 2 — real R3 producer and R15 checker have different provenance contracts

**Evidence.** The second R3 `proof.json` has raw SHA-256 `86d203f88e528e44670a431b5794fa5fe57f8196ac93e15d9b97dd783c93cd14`; its semantic record hash is `c038220283469e288bebfd8c25ce907f4f96cce06114b6ffd9aefe1cb1275cde`. The actual `result.common.json` segment provenance includes the semantic hash and `native_proof_replay=PASS`, but omits `native_proof_file_sha256` and `source_snapshot_manifest_sha256`. `validation/g4/common_tube.py::r3_record_to_common_segment` constructs exactly that smaller provenance map; the R9 R3 worker passes it through. `validation/g4/check_matched_batch_v3_r15.py::_common_and_proof` requires both omitted fields on every common segment, with the exact proof-file hash and pinned R9 source-closure hash. The composition report separately carries the R9 closure in query context and reports PASS, but it does not supply the two required common-segment bindings. The Auer segment producer already emits those fields.

**Consequence.** The R15 checker correctly fails closed under its declared contract: `AUDIT_UNVERIFIED_BINDING` / class 3. The R3 producer's own `CERTIFIED`, native replay PASS, common predicate PASS and composition PASS do not satisfy this stricter stage binding. This is a producer/checker interface defect, not evidence that the ODE proof is mathematically false. The pre-execution synthetic fixtures supplied the required fields and therefore did not exercise the live R3 producer-to-checker path; the earlier limited GO review missed this compatibility gap.

**Status:** **BLOCKER** for the R15 proof-backed comparison; mathematical truth of the second certificate **UNVERIFIED** under R15.

**Required action.** Prepare a new versioned protocol/source candidate. Bind each R3 common segment to the independently hashed raw proof file and the actual source snapshot before common-record serialization, and make the independent checker recompute those bindings. A different transitive-binding design requires an explicit soundness argument and equally strict replay; merely weakening the checker or trusting producer-declared hashes is insufficient. Add a production-path, non-query interface fixture to catch this mismatch before a new GO. Preserve R9 and R15 source/output bytes.

## Finding 3 — terminal UTC start field is mislabeled

**Evidence.** The stored stage terminal gives `stage_elapsed_wall_seconds=46.672` but equal `started_utc` and `completed_utc` at terminal creation. The R15 runner source sets both with `datetime.now(timezone.utc)` while constructing the terminal; its monotonic start is recorded earlier after writing stage intent. The external capture and stage intent show an earlier start.

**Consequence.** The elapsed field and external capture document duration, but the terminal's `started_utc` is not the actual stage start. This is a provenance defect, not the class-3 cause. Historical bytes must not be rewritten.

**Status:** **NEEDS REVISION** prospectively.

**Required action.** In the next version, record the UTC start at the same point as the monotonic start and check timestamp ordering on replay. Carry R9, R11 and both R15 attempted IDs as separate consumed strata; predeclare any later schedule using only never-attempted IDs. Do not pool results across changed protocols without a justified equivalence account.

## Gate disposition

**HOLD**. G1 remains PASS for the restricted reduced model. G2/G3/G4 and physical-platform correspondence remain UNVERIFIED. R15 Stage 1 is stopped and non-resumable; no later stage or full batch is authorized.
