Session: DDWMR | LUNA-G4-AUER

# G4 Auer R8 single-query preflight assignment

**Execution instruction for this session:** You are `LUNA-G4-AUER`, the executor. The user has already delivered this assignment to you. Carry out the authorized preflight below directly; do not forward it to another Luna or wait for another agent. The repo rule that the user mediates Codex–Luna communication concerns handoff between sessions, not execution within this session.

Read `AGENTS.md`, all four canonical `research_context/` files, `docs/reviews/CODEX_G4_AUER_PROTOCOL_V3_R8_SOURCE_REVIEW.md`, the R8 handoff and matched protocol first. MASTER v2.1 is authoritative. Work only in this repository. Preserve the shared G2 working tree and all R7/R8 candidate/archived bytes. Do not commit or push.

## Authorization and scope

The focused R8 source defect is accepted for an exact-byte, **single-query preflight**. This assignment authorizes the **first frozen ID only**:

`state_low_neg__scene_d020_l-200__T_020__V_m1_m1`

Run both Auer and R3 arms for that same ID under their frozen R8 inputs/profiles. The 1,944-query batch and every other ID remain **NOT AUTHORIZED**. The R8 candidate manifest's pre-review `query_1_authorized=false` stays byte-identical; record this review and assignment as a separate prospective authorization/receipt. Do not retroactively edit the candidate.

## Preconditions

1. Recheck all 214 source-closure dependency hashes, protocol/manifest/profile/input hashes and ordered-ID digest before invoking either worker. Record the exact tree/source identity. If any hash differs, stop with `NOT_RUN` and report.
2. Use the declared 120-second/1-GiB guard per method, the 100,000 combined Auer RHS/Jacobian limit and R3's 4-MiB serialized-proof cap. Do not raise caps, swap IDs or choose an easier example. Keep offline audit time/memory separate from worker measurements.
3. Write new output to a distinct versioned preflight directory. Preserve raw result, guard receipts, stdout/stderr, native proof or explicit stop artifact, common record, replay/audit report, timing/work vectors, environment and SHA-256 ledger. The result must preserve `UNKNOWN`, resource and execution failures as observed; no silent rerun or reinterpretation.

## Review target

Validate schema and bindings, independently replay any complete native proof and common predicate, and compare Auer producer/replay/combined/cap counts to the live worker vector. Record explicitly whether the successful live equality branch was reached. If either arm stops early, report the exact stage and unexercised checks; do not substitute another query without a new Codex review. The single query is plumbing evidence, not a matched performance or novelty conclusion.

Write `docs/reviews/LUNA_TO_CODEX_G4_AUER_R8_SINGLE_QUERY_FULL_HANDOFF.md` with Finding / Evidence / Consequence / Status / Required action, raw paths/hashes, both arms' statuses and resource observations. Stop after this one ID. Do not start the batch or change any gate.
