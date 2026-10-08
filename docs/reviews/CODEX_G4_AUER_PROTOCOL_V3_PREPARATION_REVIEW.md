# Codex review — G4 Auer protocol-v3 preparation

**Date:** 2026-10-01  
**Input:** `LUNA_TO_CODEX_G4_AUER_PROTOCOL_V3_PREPARATION_FULL_HANDOFF.md` and its protocol, manifest, erratum, and archived R3 fixture.  
**Disposition:** **PARTIAL. Accept as a review candidate; not final freeze and not batch ready.**  
**Research state:** HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED; matched Auer evaluations 0/1,944.

## 1. Query universe and artifact identity

**Finding.** The candidate preserves the declared 1,944-ID universe and its order. The principal newly reported byte hashes match the local files.

**Evidence.** I read the v2 candidate manifest and independently obtained 1,944 rows, 1,944 unique IDs, all `NOT_RUN`, and LF-joined ID SHA-256 `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`. Its `execution.comparison_run` is false. I recomputed exact-byte SHA-256 for protocol v3 `302db359dd622aeb78fc692a08db09cc7f88fcdf4eddb2d23f46952adf2f84f7`, candidate freeze manifest `c4f5e8200f4c197c7ce0c60ec0a3a00fc4b63e8c6d6d3919d879aec0a9f81525`, bibliographic erratum `d2713cefdf04a8af0df642ab8067af72b6a896eb2507b81716ef9d23f91540a1`, and the existing R3 adapter fixture `1b3a97e171d12585bc8918b819b6b28403467926889dc9c5488786c01c69b92b`; all match the handoff. This review did not independently rehash every field of the 75-hash candidate manifest.

**Consequence.** The scientific query universe is a sound candidate for a later frozen comparison. Hash agreement does not establish an executable paired pipeline.

**Status.** **VALID for the checked identities; full candidate source closure UNVERIFIED.**

**Required action.** Keep the ID universe fixed and complete the clean-source closure at final freeze.

## 2. Existing R3 parity fixture

**Finding.** The v5 archived R3 proof-to-common fixture satisfies the narrow interface-parity obligation identified in the previous Codex disposition. It cannot be counted as a matched equal-resource observation.

**Evidence.** The published selection and adapter records bind `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`; native R3 proof replay is recorded PASS. The segment is `CENTER_PLUS_RADIUS_ONCE`, count 1, covers `[0,1/50]`, and retains all 12 fixed labels. The common result is `PASS_ON_SUPPLIED_TUBE` with positive recorded collision/contact lower bounds; common and proof-to-common composition replays pass. The archived native R3 profile used 15 s, 16,384 bits and 1,000,000 operations without the proposed external memory guard; common-adapter v4 used a separate 60 s stage cap.

**Consequence.** No duplicate parity fixture is needed absent a named missing premise. Prospective R3 runs under the same external resource policy as Auer are required for the primary matched view.

**Status.** **VALID interface evidence; matched-resource applicability UNVERIFIED.**

**Required action.** Keep the v5 fixture as historical proof-to-common evidence and bind it explicitly in the final review request.

## 3. The proposed step policy is not implemented by frozen R4 source

**Finding.** Protocol v3 Section 6 is a legitimate *candidate algorithm specification*, but it is not an executable profile of the published R4/R5 solver.

**Evidence.** `validation/baselines/auer2013/residual_ivp.py::solve_ddwmr_case` currently begins each step with `step_width = horizon - current_time` and halves only after a native Picard/inclusion attempt fails (approximately lines 500–551). It has no 0.01 s base partition, depth-five base-slab rule, or common-predicate-guided refinement. `r4_worker.py` hardcodes the R4 single-case input/profile and calls the common predicate after native full-hold proof production. Its common call takes the R4 profile's 128 square-root bisections; v3 proposes one 24-bisection common profile. A new per-query worker, source/profile binding and independently reviewed replay path are still required.

**Consequence.** The candidate cannot be frozen and run by changing JSON limits alone. One option is to revise the protocol to a deterministic policy compatible with the existing residual core and put common checking after native full-hold proof. The other is to implement a **versioned** producer/runner and replay contract for the new policy, then independently review the affected proof logic. The frozen R4/R5 artifacts and their source hashes must remain intact.

**Status.** **BLOCKER for executable freeze; not a defect in the accepted R4/R5 single-case proof.**

**Required action.** Select one of those routes before asking GPT to accept protocol v3 for batch start. Identify exactly which source files and proof fields must be versioned.

## 4. Proof-complete predicate UNKNOWN is misclassified at the depth limit

**Finding.** Protocol v3 Section 6 currently says to bisect after a native-proof-complete slab whose common predicate is `UNKNOWN_ON_SUPPLIED_TUBE`, but at a refinement limit it directs termination as `INCLUSION_NOT_ESTABLISHED` or `RESOURCE_LIMIT`. That loses the distinction the same protocol correctly requires in Section 8.

**Evidence.** A native `PROOF_COMPLETE` slab may have a valid full-time tube while its supplied-hull collision/contact test is inconclusive. Refining that slab may remain inconclusive or stop at depth five. Neither outcome retracts its previously completed native inclusion proof. The common predicate's UNKNOWN is not an inclusion failure and need not be a resource stop. The candidate does not specify whether a proof-complete parent tube is retained if a child refinement fails, how a right child inherits the left endpoint, or how the final all-hold status is formed from mixed accepted and unresolved slabs.

**Consequence.** Status counts would be scientifically misleading. Preserve a proof-complete parent when trying optional predicate refinement, or specify a different sound rollback policy. If full-time proof coverage survives but predicates remain unresolved, report native proof complete and final predicate UNKNOWN. Use `INCLUSION_NOT_ESTABLISHED` only for an unproved IVP segment and `RESOURCE_LIMIT` only for an actual declared resource stop.

**Status.** **BLOCKER for protocol consistency and final status taxonomy.**

**Required action.** Version the protocol candidate and define parent/child proof, endpoint-chaining, full-time coverage and final-status rules exactly.

## 5. Resource accounting is still a specification

**Finding.** The proposed 120 s / 1 GiB external pair and common 32,768-bit / 2,000,000-operation policy are explicit, but neither matched method has a materialized, reviewed pipeline under them.

**Evidence.** The manifest marks both future matched profiles `materialized=false`, calls for a new R3 external worker and memory probe, and leaves source closure pending. Existing R4 worker is tied to the single-case 120 s/1 GiB profile; historical R3 and common-adapter v4 have different limits. The protocol's one 2,000,000-operation ledger across producer, replay, adapter and common predicate does not yet have a demonstrated accounting path for both arms. The 24-bisection common profile differs from the R4 small-case common setting.

**Consequence.** Equal external limits are a fair candidate; equivalence of measured stage boundaries and rational-operation accounting remains to be established. The current manifest is correctly labeled a candidate, not a freeze record.

**Status.** **PARTIAL; implementation and resource fairness UNVERIFIED.**

**Required action.** Materialize versioned profiles and paired workers, exercise the external guard on both arms, and review stage/total accounting before final freeze. Do not relabel archived R3 or R4/R5 development results as matched output.

## 6. Bibliographic correction

**Finding.** The sidecar erratum is a sound way to correct the unsupported Rauh–Auer DOI while preserving the v2 contract bytes that bind frozen proofs.

**Evidence.** The erratum gives the verified *Reliable Computing* 15(4):370–381 article and Algorithm 1/Eqs. (3)–(6), omits the unverified DOI, and explicitly makes no mathematical change.

**Status.** **VALID as bibliography metadata; no proof or gate change.**

## Decision and next work

**Accept the v3 package as preparation, not as the final comparison protocol.** The existing R3 parity fixture is sufficient in its interface scope. Before a single consolidated GPT batch-start review, resolve Findings 3–5 with a versioned protocol/manifest candidate and concrete paired execution contracts. Continue to report **0/1,944 matched Auer queries**, **HOLD**, and **G2/G3/G4 UNVERIFIED**.
