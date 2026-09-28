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

## Version maintenance

For a substantive decision: update MASTER, increment its declared version, append decision/reason/consequence here, update matrix/gates if affected, and mark old claims superseded. The current filename is the canonical entry point; if renamed for a future version, update AGENTS.md and README together. Do not leave two current masters.
