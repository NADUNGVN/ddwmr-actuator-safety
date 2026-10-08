# Codex review — G2 R17 two offline rows

**Date:** 2026-10-05  
**Reviewed handoff:** `LUNA_TO_CODEX_G2_R17_TWO_OFFLINE_ROWS_EXECUTION_FULL_HANDOFF.md`  
**Disposition:** **ACCEPT the exact two-row execution and replay evidence; both rows are inconclusive.** No broader study GO and no G2 gate promotion follow.

I read the R17 handoff against the existing exact-scope GO review and decision. I independently recomputed the raw SHA-256 and byte size of **15/15** files in the handoff ledger, including the stored stage authorization, row intents, terminals, records, diagnostic streams and top-level captures. The stage authorization is byte-identical to the current GO decision. I ran the pinned R17 `audit_stage()` read-only against the stored stage. It returned `COMPLETED`, `receipt_valid: true`, `native_query_calls: 0`, two replayed rows and the exact pair decision stated below. This review did not run a worker, native query, stage runner or R5 study.

## Finding 1 — exact-scope execution

**Evidence.** The stage contains ordered R5 indices **62 then 74**. The independent audit accepted both source-bound intents, worker terminals, captured stdout/stderr, R10 records, R11 replays and the recomputed stage receipt. Both transports are `PRODUCER_COMPLETED`; both captures are complete without overflow. Row 62 was `VALID_UNKNOWN`, which permits row 74 under the fixed stop rule. The GO permits at most these two offline workers, zero native query calls, zero study rows and no retry. The stored receipt and audit report the same accounting.

**Consequence.** The authorized one-shot stage was completed and its evidence can be used as a development pilot. **Status: VALID for execution provenance and replay.** This does not authorize another row or a retry.

## Finding 2 — mathematical output

**Evidence.** The independent R11 checker replay returned `UNKNOWN` for both rows with `safety_certified: false`, `task_eligible: false` and reason `NONNEGATIVE_SAFETY_MARGIN_NOT_ESTABLISHED_ON_EVERY_SLAB`. I read the exact stored `margin_lower` fields:

| R5 index | Slab | Collision lower bound | Contact lower bound |
|---:|---:|---:|---:|
| 62 | 0 | `-3/50` | `-23885717/4000000` |
| 74 | 0 | `-67047611924271/1759218604441600` | `-25852257/16000000` |
| 74 | 1 | `-3/50` | `-991988257/655360000` |

Every displayed sufficient lower bound is negative. A negative lower bound is failure to certify; it is **not** a proof of collision, invalid contact or physical unsafety. **Status: VALID inconclusive outputs.**

The stored contact calculation sets `beta_upper = (1,1)` on every slab, so its guaranteed lateral reserve is zero while its body-demand upper bound is positive. The collision distance lower bound is zero on row 62 slab 0 and row 74 slab 1. These are concrete enclosure bottlenecks, not conclusions about the actual trajectory. In particular, the records do not distinguish a truly unsafe realization from an overly wide sufficient tube.

## Finding 3 — paired decision and gate effect

**Evidence.** Recomputing the locked pair rule gives `NO_PREDECLARED_TASK_SELECTION_SEPARATION`, `broader_study_preparation_trigger: false` and `broader_study_execution_authority: NOT_GRANTED`. The R5 study remains **800/800 `NOT_RUN`**. The two attempted R17 indices are consumed, with no substitution or retry. The records demonstrate that this particular selected pair did not yield a decision-relevant certified distinction under the current evaluator.

**Consequence.** **NO-GO for the 800-row study from this trigger.** No action can be ranked as safer from these two `UNKNOWN` outputs. G2 usefulness, practical conservatism and general evaluability remain UNVERIFIED. G1 stays PASS only for the restricted reduced-model scope; G2/G3/G4 and physical-platform correspondence remain UNVERIFIED; project status remains **HOLD**.

## Required action

Preserve the R17 stage and its GO bytes. Analyze the two stored records without new execution to locate the dominant enclosure loss in collision and contact bounds, and decide whether a defensible method improvement exists under MASTER v2.1. Any revised method and evaluation pair must be source-bound and reviewed prospectively. Do not reuse the consumed indices as fresh evidence, infer unsafety from `UNKNOWN`, or launch the 800-row study under the current false trigger.
