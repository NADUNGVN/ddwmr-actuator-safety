Session: DDWMR | LUNA-G2-SCOPE

# W2 G2 v3 development failure postmortem

**Date:** 2026-10-07. **Disposition:** preserve v3 as an immutable failed development release; correct in a new version. No proof row was written and no replay ran.

## Finding

All three v3 worker launches returned the same `EXECUTION_FAILURE`: `KeyError:'collision_margin_lower'`. The directed-dyadic arithmetic allowed execution to reach the producer's post-slab certificate-status aggregation. That aggregation looked for flat slab keys, while the serialized slab schema (and producer's own construction) stores the collision bound at `slab["collision"]["margin_lower_m"]` and contact bound at `slab["contact"]["margin_lower_N"]`. The same key mismatch existed for contact and would have failed after correcting collision.

This is a producer bookkeeping defect, not evidence for or against the full-hold inequalities. Worker output contains a traceback; because the producer never returned a proof row, the independent checker was correctly not invoked. No status, safety margin, progress interval or task eligibility can be inferred from the v3 attempts.

## Evidence identity and counts

| Item | SHA-256 / count |
|---|---|
| v3 release manifest `coordination/autonomous_w2/g2/releases/RELEASE_v3.json` | `fdc8b393a3dff8e26af67922c52cd025e9e8f9eab141adf4d91403b864697693` |
| v3 frozen development plan | `c0c50e98dd1abff6def0347cf44215e0109b7300bd02d581496608216b10b4da` |
| v3 freeze receipt | `deb9eeb5af4148e911dc0f69ebe91ec788a12b2487435055ae0ee0d07c6880ea` |
| v3 stage receipt | `results/validation/autonomous_w2/g2/development_v3/stage_receipt.json` (three attempts, all `EXECUTION_FAILURE`) |
| worker stdout, each attempt | `f14891645603be138b80f36589844eb9add8739dee751e9e60dced45b197df1d` (1,646 bytes) |
| v3 producer source | `validation/autonomous_w2/g2/producer_v3.py`, frozen in the v3 source closure |

The traceback enters `evaluate`, completes its slab loop, calls `_certificate_status`, and fails at its flat collision-key lookup. Three action IDs were attempted once each, in frozen order: zero, nominal, alternative. There were no retries. Since no proof row was emitted, checker/replay count for this stage is 0/3. The failed launches count as ordinals 13–15; cumulative development count is **15/24**, with **9 remaining** before a new plan.

The v1 and v2 stages remain intact: v1 has 3 execution failures and 3 R3 replay binding failures; v2 has 3 candidate `RESOURCE_UNKNOWN / RATIONAL_BIT_CAP` and 3 R3 `UNKNOWN` records replayed. Across all versions, native development attempts are **15**, held-out rows are **0**, G4 confirmation rows are **0**, and legacy R5 remains **800/800 NOT_RUN**.

## Correction boundary

The next version changes only the schema lookups used to aggregate slab collision/contact predicates and the versioned source/profile bindings needed for a clean replay. It must retain the same task/protocol and 96-bit outward interval primitive. A nonquery fixture must cover safe aggregation, negative collision, negative contact and clip failure before the new source is frozen. The v3 sources, plan, release, stage and worker traces are not edited or retried.

No gate status changes. Overall **HOLD**; **G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED**.
