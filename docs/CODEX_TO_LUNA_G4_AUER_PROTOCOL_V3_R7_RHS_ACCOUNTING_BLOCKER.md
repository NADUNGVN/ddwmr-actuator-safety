# Codex to `LUNA-G4-AUER` — R7 successful-replay RHS accounting blocker

**Session title:** `DDWMR | LUNA-G4-AUER`  
**Other session:** `DDWMR | LUNA-G2-SCOPE` has completed its separate G2 audit.  
**Repository:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Review:** `docs/reviews/CODEX_G4_AUER_PROTOCOL_V3_R7_SOURCE_REVIEW.md`  
**Authority/status:** MASTER v2.1; **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.**

R7 correctly adds the 4-MiB R3 proof cap and enforces the Auer combined RHS limit during replay. It has one remaining blocker in the **successful Auer replay accounting**. Preserve R7 and all earlier artifacts byte-for-byte. Make a new versioned correction; do not switch branches, commit, push, clean, reset or edit the G2 lane.

## Exact failure to repair

`validation/baselines/auer2013/replay_ivp.py` returns successful `rhs_jacobian_replay_evaluations` and `rhs_jacobian_combined_count` at the top level. `validation/g4/verify_matched_composition_v3_r7.py:303-307` reads those names from nested `replay["work"]`, where they are absent, and defaults to replay zero and combined equal to producer.

Codex's read-only replay of the archived proof observed top-level `replay=4`, `combined=8`, while the R7 verifier reports nested `replay=0`, `combined=4`. The fixture report repeats 0/4. A complete live worker result records the actual replay count, so R7's live audit would raise `RESULT_RHS_ACCOUNTING_MISMATCH` on a successful Auer proof.

## Required correction

1. In a fresh version, take the successful replay/combined counts from the fields actually returned by `replay_native_proof`. Require exact nonnegative integer types; reject missing or inconsistent values. Check `combined == producer + replay` and `combined <= max_rhs_jacobian_evaluations_per_ivp` before reporting them.
2. Keep the live worker-vector equality check, using these corrected values. Keep the producer work-field validation and the at-cap rejection fixture.
3. Add a **non-query archived-proof success regression** that checks positive replay work and the exact combined total (the archived example is 4 producer + 4 replay = 8). Ensure the generated report shows 4/4/8, not 4/0/4. Add one tamper case for wrong successful replay accounting if the fixture framework supports it.
4. Rebuild the source closure, transitive import audit, candidate manifest and all affected fixture/guard bindings. Verify the unchanged 1,944 ordered IDs remain `NOT_RUN`, the R3 cap still binds across profile/worker/schema/validator, and prior R5/R6/R7 artifacts remain intact. Keep method-worker resource use separate from offline verifier/fixture use.

Write a new full Markdown handoff in `docs/reviews/` with Finding / Evidence / Consequence / Status / Required action, exact paths, source/artifact hashes, commands and execution counts. State clearly that the batch is **0/1,944** and that no matched query or new trajectory proof was run in this correction.

**Stop boundary:** no query 1, no 1,944-query batch, no G3/controller/hardware work, no gate promotion, no commit or push. Return the new handoff path to the user for Codex review.
