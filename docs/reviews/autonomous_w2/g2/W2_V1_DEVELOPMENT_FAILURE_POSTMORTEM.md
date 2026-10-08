Session: DDWMR | LUNA-G2-SCOPE

# W2 G2 — v1 development failure postmortem

**Recorded:** 2026-10-07 UTC. **Scope:** six predeclared v1 development attempts. **Disposition:** preserve all rows as failed development; no v1 certificate result is admissible.

## Counts and retained evidence

The frozen v1 plan ordered three signed-VOF rows followed by three R3 rows. All six worker launches occurred once, in that order, under the repository compute lock. The phase receipt records three `EXECUTION_FAILURE` results and three `AUDIT_FAILURE_OR_RESOURCE_UNKNOWN` results. The lock was removed by the runner's token-checked `finally` block. No row was retried under v1. The R5 800-row study remains `800/800 NOT_RUN`; no held-out G4 row was run.

Evidence is retained in `results/validation/autonomous_w2/g2/development_v1/`: each row directory contains its frozen binding hash, bounded-worker job record, captured stdout/stderr bytes, worker record where parseable, replay stdout and attempt receipt. `stage_receipt.json` is the ordered six-attempt summary. The immutable plan, freeze receipt, bindings and release v1 remain unchanged.

## Finding 1 — candidate result serialization exceeded Python's default digit guard

The three VOF workers reached output construction, then raised:

```text
ValueError: Exceeds the limit (4300 digits) for integer string conversion
```

The saved attempt 1 traceback locates the failure at `producer.py` while formatting the exact `distance_squared_lower_m2` through `rational_interval.py::qs`. The interval computation itself had not reported an arithmetic/resource cap, but the row was not serialized; therefore no safety, contact or task status may be inferred.

**Correction for v2:** declare a bounded integer-string conversion limit above the decimal width implied by the 16,384-bit rational cap; enforce the rational bit cap when serializing a fraction; classify a bound exceedance as `RESOURCE_UNKNOWN`. Add a non-query round-trip fixture above Python's default 4,300-digit limit and below the declared cap. Keep the worker/replay wall and memory limits unchanged.

## Finding 2 — R3 worker supplied a raw benchmark file hash where replay requires semantic JSON hash

All three R3 workers completed and emitted source-faithful evaluator records. Their replay checkers rejected the safety record with `benchmark_content_sha256`. `r3_baseline_worker.py::build_query` passed the byte-level SHA-256 of `r3_baseline_benchmark_v1.json` as `benchmark_sha256`; the legacy R3 checker recomputes `semantic_json_sha256(query["benchmark"])` and requires that semantic value in this field. The raw benchmark SHA remains necessary for file-integrity binding, but it is a different quantity.

The saved R3 evaluator rows report `UNKNOWN`, and their progress records report `SAFETY_REPLAY_REJECTED`. Because replay rejected the benchmark binding, none of those statuses or margins is accepted as a valid R3 comparison result. The actual R3 input bytes, benchmark bytes, profile bytes and native evaluator outputs remain preserved.

**Correction for v2:** preserve the raw benchmark file SHA in the immutable binding and use `semantic_json_sha256(benchmark_object)` in the query's `benchmark_sha256`, in both the R3 worker and its independent replay adapter. Recompute the query semantic fingerprint and require the replayed safety and progress records to validate before reporting any task eligibility.

## Consequence for the task hypothesis

The v1 stage does not answer whether the signed VOF method or R3 certifies any of the three actions. It establishes two implementation defects, consumes six of the 24 allowed native development attempts, and leaves 18 attempts for corrected, newly hashed configurations. The same three protocol rows may be re-evaluated only under a new versioned plan and will remain development evidence; they can never be relabeled held-out confirmation data.

The prospective task, threshold (`7/20 m`), state/parameter domain, action values, obstacle, 2 s hold and one-voltage/fixed-label semantics remain unchanged. No task or threshold retuning follows from these failures.
