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

## Version maintenance

For a substantive decision: update MASTER, increment its declared version, append decision/reason/consequence here, update matrix/gates if affected, and mark old claims superseded. The current filename is the canonical entry point; if renamed for a future version, update AGENTS.md and README together. Do not leave two current masters.
