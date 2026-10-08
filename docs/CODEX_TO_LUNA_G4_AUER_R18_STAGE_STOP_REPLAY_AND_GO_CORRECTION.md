# Assignment — DDWMR | LUNA-G4-AUER — R18 stage-stop replay and GO correction

Read `AGENTS.md`, all four canonical `research_context` files, the R17 handoff, and `docs/reviews/CODEX_G4_AUER_R17_COMPLETE_PROVENANCE_STAGE_REVIEW.md` first. Prepare a **NO-GO source candidate**. Do not run a real query, native producer, live composition audit, matched stage, later stage or full batch. Do not commit or push.

Current state: four historical IDs are consumed in separate R9/R11/R15 strata, R15 remains 2/10 consumed, and the R17 first stage has 0/10 attempts. The R17 continuation has 1,940 never-attempted IDs in the fixed 1,944 universe. Preserve that order and all R9–R17 source/result/GO/stop bytes. Do not retry, substitute or pool consumed IDs.

1. Version the R17 runner/checker into a new R18 candidate. Repair the full on-disk stage checker so it can independently accept a **well-formed stopped stage** with a durable method intent but no terminal, or with a failed guard/result/audit, while rejecting any safety conclusion from that failed arm. Validate exact attempted prefix, stop ID, partial/pre-intent paths, count conservation, unattempted suffix and no retry. A malformed stopped stage must still fail.
2. Add isolated **non-query** on-disk fixtures that exercise the full stage-artifact checker for partial method intent, failed guard or absent result, failed audit, and one complete pair. The present R17 fixture only calls `validate_stop_accounting`; extend coverage to the actual checker path. Use archived proofs for positive interface evidence where useful; label synthetic and copied evidence precisely. No fixture may create the canonical batch output or an executable GO receipt.
3. Make the prospective GO check require an explicit exact-scope Codex **GO** decision in the hashed review file, bound to the new manifest, closure, schedule and ten ordered IDs. A receipt referencing a NO-GO review must refuse before stage creation. Keep the decision external; do not self-issue it.
4. Bound launcher stdout capture and independent checker JSON/file reads before loading or parsing. Record overflow/incomplete capture as a stopped class-3 outcome, preserving bounded raw evidence and its hashes. Keep the existing 1 GiB/120-second child and audit caps and do not raise them. Report any remaining process-tree or resource limit that cannot be enforced as declared.
5. Preserve the corrected five-field R3/Auer proof provenance and the distinct R9 numerical versus R18 execution source identities. Produce a new manifest, closure, schedule, protocol and sidecars that pin every changed executable file. Return one detailed Markdown handoff with independent hash ledger, fixture scope, 0 new queries, 0/10 new stage attempts and an explicit NO-GO recommendation pending Codex review.

Reply to the user in exactly three short chat lines:

`Session: DDWMR | LUNA-G4-AUER`  
`Status: <DONE or BLOCKED; zero new queries; R18 first stage 0/10>`  
`Handoff: <absolute Markdown path>`
