# Decision log

MASTER_RESEARCH_CONTEXT_v2.md is authoritative. This log records history; it does not silently amend MASTER.

## 2026-09-28 — HOLD — initial audit

- Rejected global relative-degree-three HOCBF: the seven-state model's voltage row vanishes at tangency.
- Rejected amplitude-only slip bounds as sufficient for differentiated HOCBF.
- Rejected instantaneous QP feasibility as recursive safety or exact viability; infeasibility does not prove inevitable collision.
- Distinguished sample-invariance of a certified endpoint set from continuous collision safety.

## 2026-09-28 — workflow

- User is the intermediary with GPT; no further browser/computer automation for GPT exchange.
- Luna max stopped at a usage limit after initial plant/derivative documents. Root supplied subsequent review documents. No controller, simulator, tests or experiments were implemented/run.

## 2026-09-28 — HOLD — adopt user-supplied MASTER v2

- Imported `C:/Users/Dawin/Downloads/MASTER_RESEARCH_CONTEXT_v2.md` verbatim. Source/destination SHA-256 matched at import.
- Import SHA-256: `56938695AFC4B9FAC66285B794AA759101D1E7C93531BC734C878F001D63265B`.
- Replaced the seven-state rolling model as current candidate with the nine-state body/contact model `[p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R]`.
- Current uncertainty: bounded uncertain longitudinal traction. Longitudinal body motion at wheel lock is admitted; arbitrary lateral skid is outside scope.
- Promoted plant-structured reachable-tube/predecessor reasoning to candidate core. HOCBF is optional/baseline.
- Adopted G1 plant consistency, G2 certified enclosure, G3 nontrivial sampled recursive safe set, G4 novelty audit. None has passed.
- Earlier research notes are superseded supporting history; their seven-state algebra does not establish a nine-state result.
- Initialized a 24-entry evidence-tiered literature register; contact/friction/tube coverage and closest full-text comparisons remain open. No systematic novelty closure is claimed.

## 2026-09-28 — HOLD — G1 review evidence, no formulation change

- User relayed GPT's context confirmation at commit `8ad80a20b5a58dafb135a89210cb8f990f3ccadf`; this does not constitute a G1 pass.
- Root produced `docs/reviews/G1_PHYSICAL_MODEL_AUDIT_v2.md`: twelve findings with conditional derivations, counterexamples, affected branches and proposed exact MASTER edits.
- Contact signs are conditionally consistent. Physical lateral/contact validity, geometry, braking authority, sustained lock, state information, drive conventions and uncertainty/symmetry assumptions remain unresolved.
- All proposed assumption changes await independent review. MASTER v2 remains byte-for-byte unchanged; G1 NEEDS REVISION and G2–G4 UNVERIFIED. No implementation authorized or performed.
- GitHub CLI confirmed the repository is now PUBLIC. Corrected outdated private-repository wording in README and the GPT review request; no visibility setting was changed by this review.

## v2.1 - adopted reduced-model formulation - HOLD

Adoption provenance — 2026-09-29 (Asia/Saigon): the user explicitly authorized application with “Đồng ý áp dụng v2.1 theo bản diff đã được GPT ACCEPT”. Applied only `docs/proposals/v2_1_finalization/ADOPTION_FINALIZATION.patch`, reviewed at `fdefbebc4b59d848e2234da37eb9ad6395d61fdf` and accepted in `docs/reviews/GPT_TO_CODEX_FINALIZATION_REVIEW_fdefbebc_ACCEPT.md` (archived in commit `a15424e`). This dated provenance record is the sole addition to the six reviewed target texts. Formulation adoption only; HOLD, G1 NEEDS REVISION and G2/G3/G4 UNVERIFIED remain unchanged.

This decision adopts the reduced C_j-based formulation as the authoritative research context. It does not pass G1, validate a physical platform or authorize implementation. The actual dated adoption/authorization event is recorded with the authoritative adoption commit.

- Replace the literal friction/normal-load product in the formal core with execution-fixed effective tangential capacities C_j in newtons. Physical support/contact correspondence remains unverified.
- Use exact axle-COM geometry, an exact lateral constraint and algebraic bounded reactions with correctly typed state/parameter contact domains.
- Keep one known fixed bounded globally Lipschitz strictly sign-preserving phi. Oddness is auxiliary only; monotonicity and differentiability are not core assumptions.
- Use an unknown fixed model-parameter vector for the complete execution, power-consistent wheel-side conversion, ideal four-quadrant terminal-voltage ZOH and exact sampled state/zero delay.
- Preserve the reduced-model question/title and its distinction from physical tire/support dynamics and changing-terrain uncertainty. Capacity reparameterization is not novelty; a lower force bound alone is not a trajectory enclosure.
- Retain qualified wheel-zero and symmetry statements. No stopping policy, certified enclosure or useful recursive subset is established.
- Historical fixed-normal-load diagnostic remains in docs/reviews/CODEX_RESPONSE_TO_GPT_G1_v2_1.md, B3; it is not part of active MASTER equations.
- Review evidence: docs/reviews/GPT_TO_CODEX_REVIEW_12edd1b_R2_FULL_HANDOFF.md accepts R2 with three mandatory finalization edits; docs/reviews/CODEX_FINALIZATION_RESPONSE_12edd1b.md records those edits. Actual adoption authorization is a separate event.
- G1 NEEDS REVISION; G2/G3/G4 UNVERIFIED; overall HOLD. Review actual authoritative v2.1 text for G1 separately. Adoption alone does not authorize G2/G3 construction or implementation.

## G1 status recording - restricted reduced-model scope - HOLD

Acceptance/application provenance — 2026-09-29 (Asia/Saigon): the user explicitly authorized “Đồng ý ghi nhận G1 PASS trong phạm vi mô hình rút gọn và áp dụng bản diff trạng thái”. Applied `docs/proposals/g1_status_8341014/G1_STATUS_PENDING.patch` from commit `81ff1cb43ea2ad19a04f45bc72b734048739bee6`, recording the independent disposition in `docs/reviews/GPT_TO_CODEX_G1_REVIEW_8341014e_PASS.md` for authoritative formulation commit `8341014eac52ea66fe38559d6e1baee92e8f9b96`. This dated record is the sole addition to the five proposed target texts. Physical-platform correspondence and G2/G3/G4 remain UNVERIFIED; overall HOLD. No next-phase construction or implementation authorization is recorded.

Independent G1 review of authoritative v2.1 at commit `8341014eac52ea66fe38559d6e1baee92e8f9b96` accepts internal consistency of the restricted nine-state reduced ideal planar model. Evidence: `docs/reviews/GPT_TO_CODEX_G1_REVIEW_8341014e_PASS.md`, G1-01 through G1-12 and disposition in section 14.

- G1 PASS - restricted reduced-model scope; physical-platform correspondence UNVERIFIED.
- G2/G3/G4 UNVERIFIED; overall HOLD. No G2/G3 construction or implementation authorization follows.
- Plant equations, assumptions, scientific scope and declared formulation version v2.1 are unchanged. This is review-status synchronization, not a new formulation.
- Prior entries retain their historical gate statuses. The actual dated user acceptance/application provenance is recorded when this status update is authorized and applied.

## 2026-09-29 - HOLD - authorize G2 analytic research only

- The user said "thực hiện" after Codex proposed opening G2 to construct and prove a one-hold reachable enclosure. Scope interpreted from that immediate proposal: G2 research only.
- G1 PASS remains restricted to model consistency; physical-platform correspondence remains UNVERIFIED. G2/G3/G4 remain UNVERIFIED. G3 construction and controller/simulator/experiment implementation are not authorized.
- Formulation version remains v2.1; plant assumptions and all displayed MASTER equations are unchanged. Only current-phase/evidence metadata is synchronized.
- Root prepared `research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md`: finite voltage-dependent integral predictors, residual comparison, joint parameter enclosure, and continuous collision/contact checks. These are candidate proofs for independent review, not accepted canonical theorem claims.
- Luna max was delegated a read-only adversarial proof audit under the existing requested division of research roles. Agreement is not evidence of theorem validity.
- Targeted primary-source screening found direct overlap with componentwise/growth-bound reachability and fixed-parameter augmentation. Standalone novelty from that machinery is BLOCKED; no first or G4 claim is made.
- Numerical computability requires a selected evaluable phi, an effective parameter-set description, validated arithmetic and full-time range bounds. No values or performance results were invented. No simulation, controller or implementation tests were added or run.

## 2026-09-29 - HOLD - record independent Case A acceptance; continue G2 only

- User relayed GPT's full G2 R2 review of `d2cd85407bb5ba4b4360836c49aa8a9c7ec83f28` and requested its recording. Structured record: `docs/reviews/GPT_G2_R2_d2cd854_ACCEPT_RECORD.md` (not a verbatim transcript).
- GPT accepted A.1--A.23 as one finite rational synthetic one-hold certificate, including full parameter/time coverage and all arithmetic primitives. Corrected voltage-dependence wording is VALID.
- The claim that no finite instantiated certificate exists is superseded. General evaluator, practical usefulness, runtime, physical correspondence and novelty remain unverified.
- Continue G2 analytic research with a Case B challenge involving parameter-dependent actuator matrices and explicitly scoped certificate-success versus UNKNOWN comparisons. No voltage-necessity, unavoidable-collision or generic-method originality claim follows.
- Submitted `research/theorem_notes/G2_CHALLENGE_CASE_B_v1.md` for independent review: synthetic correlated actuator/capacity family, contact saturation exit, and three locked sufficient evaluations. Its obstacle placement is intentionally tuned and disclosed; it does not establish practical usefulness or voltage necessity.
- G1 restricted PASS; G2/G3/G4 UNVERIFIED; HOLD. No G3, controller, simulator, interval solver, experiments or GO authorized. Generic-method novelty remains BLOCKED.
- This synchronizes review evidence within v2.1. Plant equations and assumptions remain unchanged; no formulation revision is adopted.

## 2026-09-29 - HOLD - record Case B acceptance; prioritize voltage selection

- User relayed GPT's 30-section review of `1da2166949ad12a0741c876c3a0daf8a5d957ddf`. Structured record: `docs/reviews/GPT_G2_R3_1da2166_ACCEPT_RECORD.md`, explicitly not a verbatim transcript.
- Case B B.1--B.25 ACCEPT as a finite synthetic hand certificate, including correlated actuator labels, explicit N domination, noncircular saturation exit and the narrowly locked three-evaluation separation. All displayed equations remain unchanged.
- Multiple accepted synthetic instances now exist. General evaluator, practical usefulness, defensible data, voltage-selection value and runtime remain unverified. Generic-method novelty remains BLOCKED.
- Next G2-only artifact: `research/theorem_notes/G2_VOLTAGE_SELECTION_CASE_C_v1.md`, a pending analytic comparison of two forward voltage candidates and zero with the same state/family/error budget/evaluation. Auxiliary matched sides and exact rest are disclosed restrictions of this case. No new general symmetry or physical-authority assumption is adopted.
- G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED; HOLD. No controller, simulator, interval solver, experiments, G3 or GO. Evidence synchronization only: authoritative formulation remains v2.1.

## 2026-09-29 - HOLD - record independent Case C acceptance

- Application provenance: on 2026-09-29 the user requested setup after clarifying that validation code is allowed, followed by "thực hiện". Synchronize the already received independent Case C evidence as part of this setup; no gate is promoted.
- GPT reviewed `c9ff32d45ad7f500cc2492c3bc7a69480c29c636`; archived verbatim review: `docs/reviews/GPT_TO_CODEX_DDWMR_CONSOLIDATED_REVIEW_FULL_HANDOFF.md`.
- C.1--C.16 ACCEPT in the exact synthetic scope. One locked rule gives zero/smaller voltage CERTIFIED and larger voltage UNKNOWN, not unsafe.
- No practical action-selection, necessity, n=1 advantage, physical correspondence, novelty or recursive-safety result follows.
- G1 restricted PASS; G2/G3/G4 UNVERIFIED; HOLD. Case acceptance itself grants no G3 or implementation authorization; the separate W1 user authorization is recorded below. Plant remains v2.1.

## 2026-09-29 - HOLD - workflow W1; validation code and user-mediated Luna handoff

- User clarification: "tôi không cấm, hãy setup và tôi sẽ giao cho luna, giờ tôi là chung gian giữa bạn và luna", followed by "thực hiện". This supersedes the former blanket prohibition of pre-gate validation code and the pending policy proposal's additional launch-approval requirement.
- Authorized scope: G2/G4 arithmetic validation, one-hold fallback evaluator, certificate/checker artifacts, applicable baseline adapters and reproducible offline benchmark tooling. Entry point: `docs/LUNA_VALIDATION_HANDOFF_v1.md`; starting draft snapshot `44e4f90a71e8e9192a92b88b17ec527eb8e322b6`.
- Codex sets up the assignment and critically reviews returned work. User starts Luna and relays its files. No autonomous Luna/subagent delegation or implementation by Codex in this setup turn.
- Draft soundness, general refinement evaluation, external baseline applicability and benchmark-lock details remain review obligations. Permission to code does not certify them. Stop affected branches on unresolved contradictions; report exact evidence without silently changing assumptions.
- G3, operational controller/safety-filter integration, closed-loop and hardware work are not part of this assignment. G1 restricted PASS; G2/G3/G4 UNVERIFIED; HOLD. Scientific plant version remains v2.1; workflow revision W1 records the authorization change.
- The pending validation-only policy patch is superseded, not applied verbatim. Earlier records of prohibitions describe historical authority and must not override this entry or current MASTER sections 3/32.

## 2026-10-07 — HOLD — workflow W2; autonomous two-session G2/G4 verification

- Owner instruction: "ok vậy làm rỏ các đầu việc cần thực hiện để hoàn thiện, từ giờ tôi muốn 2 luna max tự đảm nhiệm 2 đầu việc kiểm chứng chứ không cần đợi bạn nữa".
- Adopt workflow revision W2, extending W1 without changing plant formulation v2.1. The owner starts/continues `DDWMR | LUNA-G2-SCOPE` and `DDWMR | LUNA-G4-AUER`; Codex does not launch execution agents.
- G2 owns sound enclosure/task usefulness research, implementation and development verification. G4 owns independent proof/code audit, primary-source contribution screening and bounded matched comparison. They exchange immutable releases and audit decisions through owned repository files, so routine corrections do not require user relay or another Codex GO.
- Current contract: `docs/DDWMR_AUTONOMOUS_VERIFICATION_WORKFLOW_W2.md`; assignments: `docs/CODEX_TO_LUNA_G2_AUTONOMOUS_COMPLETION_W2.md` and `docs/CODEX_TO_LUNA_G4_AUTONOMOUS_COMPLETION_W2.md`. Record all failures, source/profile changes and denominators; preserve historical R3/R5/Auer artifacts. Do not open legacy large batches or modify their counts under a new label.
- This supersedes old per-iteration Codex review/GO waits for the same authorized G2/G4 scope. It does not accept unsound proofs, authorize a plant change, erase mathematical blockers, or promote gates. Peer disagreement is resolved by derivation/evidence; model agreement is not proof.
- Keep work within the existing shared repo and assigned prefixes, with no branch switch, commit or push. Final reports remain detailed Markdown; Luna chat summaries are exactly Session / Status / Handoff.
- G3, operational controller/closed-loop/hardware work and physical correspondence remain separate. **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.** Scientific equations/assumptions and literature findings are unchanged; only workflow revision is incremented.

## Version maintenance (current)

For a substantive decision: update MASTER, increment its declared version, append decision/reason/consequence here, update matrix/gates if affected, and mark old claims superseded. The current filename is the canonical entry point; if renamed for a future version, update AGENTS.md and README together. Do not leave two current masters.
