# Assignment — DDWMR | LUNA-G2-SCOPE — R10 whole-hold Picard candidate

Read `AGENTS.md`, all four `research_context` files, `docs/reviews/CODEX_G2_R9_ENCLOSURE_BOTTLENECK_RESEARCH_REVIEW.md`, and the R9 handoff first. Work in a new versioned G2 namespace on the current shared branch. Keep R3/R5/R6 source, the two consumed R6 records and the 800-row R5 manifest byte-for-byte unchanged. This assignment authorizes source/proof preparation and synthetic non-query validation only: **no native R6 query, no producer alias, no 800-row study, no G4 work, no commit or push**.

## 1. Complete the mathematical contract

Replace the R9 first-exit proof with a complete Picard fixed-point proof for a closed rational candidate box. State the exact assumptions on the interval RHS, local Lipschitz continuity, fixed hidden parameter label, one voltage held over the complete `T`, and endpoint carry. Distinguish an interval outer relaxation that forgets label/state correlations from a physical parameter that actually switches.

Specify a deterministic rational construction for each candidate `B_k` and slab duration `h_k`, including a finite split/expansion and operation budget. Failed inclusion or exhausted budget must return `UNKNOWN`. A reported positive result must contain a finite sequence covering `[0,T]` exactly, with `X_0` enclosing the declared initial internal-state cell and `X_{k+1}=X_k+h_kG_k` enclosed by the next slab. Bind the initial pose box, every pose endpoint carry, and the terminal progress sum. The same joint parameter image and voltage must be used for all slabs and all initial states. If splitting the joint parameter labels, assign stable leaf IDs once and carry each leaf unchanged throughout the hold.

## 2. Implement a replayable candidate, without running R6 inputs

Prepare a versioned offline producer/checker pair. The checker must reconstruct the exact declared query and model from source-bound inputs and independently recompute `G_k`, `X_k+[0,h_k]G_k subseteq B_k`, `X_{k+1}`, pose time tubes/endpoints, collision/contact lower margins, and the accumulated progress lower bound for every slab. It must reject a fabricated `PICARD_INCLUSION_PASS` dictionary, mismatched voltage, initial internal or pose box, model/parameter image, reordered or missing slab, endpoint-carry mismatch, incomplete `[0,T]` coverage, altered margin, malformed output and resource-limit ambiguity. Do not treat the R9 helper's status/hash check as independent proof replay.

Keep the R6 physical quantities and unchanged `1/20` m task threshold. Preserve the exact reduced plant and clip law; do not amend MASTER. Include explicit operation/bit/time caps and separate `CERTIFIED`, `UNKNOWN`, and malformed/invalid-record outcomes. Put finite synthetic non-query cases and negative binding cases in a new source closure. Report exact source hashes, fixture scope and any unresolved soundness condition. If a whole-hold proof/checker cannot be completed, stop the affected implementation branch and state the precise missing inequality or binding.

## 3. Prepare the later two-action development stage

Draft, but do not issue, a source-bound minimal-stage manifest for the **same two logical inputs** used in R6: R5 indices 12 `(0,0)` and 24 `(+1,+1)`, in that order. Retain their exact input hashes, the consumed R6 outcomes, the existing R5 denominator and the fact that these are observed development inputs. State the predeclared decision trigger and one-shot stop rules. A new native evaluation requires an independent Codex review of the complete R10 producer/checker and a separate exact-scope execution authorization; this assignment grants neither.

Write a full handoff under `docs/reviews/LUNA_TO_CODEX_G2_R10_WHOLE_HOLD_PICARD_CANDIDATE_FULL_HANDOFF.md`. Reply to the user in only three short lines:

`Session: DDWMR | LUNA-G2-SCOPE`  
`Status: <DONE or BLOCKED; zero new native queries; R5 800/800 NOT_RUN>`  
`Handoff: <absolute Markdown path>`
