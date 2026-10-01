# Codex to Luna — G4 Auer R3 proof-backed single case

**Package ID:** `G4_AUER_R3_PROOF_BACKED_SINGLE_CASE`  
**Date:** 2026-09-30  
**Working folder:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Starting branch / HEAD:** `luna/g2-validation-v1` / `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`.

The user mediates all exchanges on the same laptop. **Do not commit, push, reset, clean, stash or switch branches.** Preserve all earlier R3 and Auer v1/v2 artifacts. W1 authorizes this scoped offline G2/G4 work. No G3, controller, hardware, experiment, GO or gate promotion is in scope.

## 0. Read and scientific disposition

Read `AGENTS.md` and all four canonical `research_context/` files first, then:

1. `docs/reviews/GPT_TO_CODEX_G4_AUER_R2_STRATEGY_FULL_HANDOFF.md`;
2. `docs/reviews/CODEX_G4_AUER_R2_STRATEGY_DISPOSITION.md`;
3. `docs/reviews/LUNA_TO_CODEX_G4_AUER_BASELINE_R2_FULL_HANDOFF.md` and `docs/reviews/CODEX_G4_AUER_BASELINE_R2_REVIEW.md`;
4. `research/theorem_notes/G4_AUER_BASELINE_CONTRACT_v1.md` and `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v2.md`;
5. the retained Auer 2013 and Rauh–Auer 2011 primary papers, pinned VALENCIA source and dependency terms.

GPT selected **Auer 2013** as the principal comparator, but only as a **paper-faithful method reconstruction with certified arithmetic**. GPT could not inspect the local uncommitted R2 source from its GitHub environment. Do not claim that its strategy review independently validated the local implementation. A successful historical smooth seed build is not the 2013 method.

This package ends after **one analytic IVP fixture, one predeclared DDWMR query-action, and one historical R3 proof fixture**. Do **not** run the 1,944-query matched batch.

## 1. Freeze the method and arithmetic contracts before results

Write `docs/reviews/G4_AUER_METHOD_CONTRACT_v1.md` with an equation-to-code crosswalk for Auer 2013 Eqs. (27), (28), (33)/(40), (42)/(43) and the Rauh–Auer residual inclusion. Specify the clip range and generalized derivative at both corners, the full-time inclusion condition, endpoint propagation, fixed labels and termination semantics. Identify every place where the reconstruction changes the legacy source. Label the result a **method reconstruction**, not original-software reproduction.

Write `validation/baselines/auer2013/ARITHMETIC_BACKEND.md` plus a machine-readable backend manifest. Prefer a locally built MPFR-directed/MPFI-style backend. Pin source and binary versions/hashes, compiler/link flags, precision and rounding modes. Audit outward `+`, `-`, `*`, `/`, `sqrt`, `exp`, `sin`, `cos` and every other operation actually used. Document trigonometric range reduction/extrema, parsing, underflow/subnormals, overflow/infinity, NaN/domain handling and exact outward serialization. The legacy PROFIL/BIAS/glibc sine/cosine path remains disallowed for proof output until its all-input error contract is resolved. Finite probes may supplement, never replace, the backend contract.

Before either IVP run, freeze a **separate small-case development resource profile** with finite wall time, memory, precision or precision ladder, accepted/rejected steps, Picard iterations, branch splits and RHS/Jacobian work limits. Give the exact profile hash and rationale. Do not relabel this development profile as the future 15-second matched profile. Preserve failed attempts and use a new profile/version for any later change; no post-hoc cap increase inside one result series.

## 2. Build a replayable native full-time inclusion path

Connect the source-faithful piecewise `clip` range/derivative to the solver's interval mean-value/Jacobian path. Implement the paper's residual/Picard acceptance test on each complete closed step. Store the approximate path, rough domain, interval RHS/Jacobian and every residual iterate needed to recompute the final inclusion. A checker independent of the producer's Boolean must replay the premises with outward arithmetic. Store a full-time tube and a **separate** certified endpoint for each accepted step.

For multi-step propagation, the next start enclosure must contain the previous certified endpoint. Keep one held voltage and one hidden 12-label realization throughout the DDWMR hold (`dot(label)=0` is an allowed augmentation). Never narrow to a favorable label between steps. Distinguish mathematical UNKNOWN, resource limit, invalid input and implementation failure. A process exit code of zero is insufficient if the solver reports `Condition not fulfilled` or fails to reach the requested endpoint.

The common checker presently validates only a supplied total hull. Keep its `certificate_emitted=false` behavior until the native proof checker succeeds and a separately reviewed composition layer binds proof, tube and predicate. An Auer `proof_record_sha256` string by itself is provenance, not proof replay.

## 3. Analytic branch-crossing IVP fixture

Use exactly the independently proposed fixture, labeled **“analytic Auer-method validation fixture; not Auer §5 reproduction”**:

```text
x' = 1
y' = clip(x,-1,1)
x(0) in [0.9,0.91], y(0)=0, T=0.2
```

The switch time varies over `[0.09,0.10]`. Exact endpoint ranges are `x(T)∈[1.10,1.11]` and `y(T)∈[0.195,0.19595]`. The validated endpoint may be wider, but it must contain these ranges; the full-time tube must cover every real time and every initial value. Retain machine-readable native inclusion records for every step and a replay report. A plotted or sampled curve is not evidence.

If this fixture cannot obtain a proof-complete tube under the frozen development profile, stop the Auer solver branch for this package and return `BLOCKED` with the exact failed inclusion or arithmetic premise. Continue only independent documentation and R3 adapter work.

## 4. One predeclared DDWMR query-action

Use the **first original row** in the frozen R2 universe, selected before inspecting its R3 status:

`state_low_neg__scene_d020_l-200__T_020__V_m1_m1`

It has `T=1/50 s` and held voltage `V=(-1,-1)`. Record its canonical input SHA-256 from the existing candidate manifest and preserve the complete benchmark parameter image. Run only this one Auer query-action under the frozen small-case development profile. Required output is a proof-complete full-time tube, propagated endpoint, native replay report, resource counters and common-check outcome. The common predicate may return CERTIFIED or UNKNOWN; **proof completeness is the milestone**. Do not change the selected query because of its safety outcome or an inconvenient proof result.

If a validated tube cannot be produced within the declared cap, return the exact failed condition. Do not raise limits and retry under the same profile, switch parameters, alter clip, or substitute a nominal trajectory. Do not infer R3 superiority from the failure.

## 5. Bind the proof to the checker and exercise real R3 data

Define a typed composition record that binds the native proof and each exported `TubeSegment` to the same query ID, action/held voltage, initial box, full fixed-label image, horizon, slab number, method contract, arithmetic backend, source snapshot, resource profile, full-time hull and endpoint. Hash the actual native proof bytes and verify the hash and inclusion replay before any combined safety status. Preserve the existing **radius-once** total-hull invariant. Check every closed segment, all obstacles and full-time algebraic contact; endpoint-only checks cannot substitute. Tampering with action, proof digest, endpoint, radius mode or one segment must be rejected.

Route **one actual archived R3 proof record** through `r3_record_to_common_segment` and the shared checker without rerunning the R3 batch. Select it deterministically as the first frozen R3 record with a replayable proof; record its query ID and hash before viewing the common-check result. Verify input/action identity and native replay. Report native R3 status/margins and common status/margins separately; the common representation may be more conservative. Do not overwrite any R3 producer or checker artifact.

The current chain requires equal adjacent endpoint intervals. Keep that sufficient rule or replace it with a documented propagation containment check; mere overlap does not prove a valid chain. The Auer adapter's binary64-to-rational conversion may be used only after the upstream interval endpoints are proven outward.

## 6. Local freeze and independent-review return

After source/profile stabilization and **before** small-case runs, create a new versioned local source snapshot. Include all transitive scientific code, external arithmetic sources/terms, exact benchmark/configuration, method contract, profile, compiler commands, binary hashes and reviewable patches from the pinned VALENCIA seed. Hash executed inputs before and after. Keep older v1/v2 attempts intact. If the local GPT reviewer can only access committed GitHub content, make the returned Markdown self-contained enough to expose the exact proof algorithm, key source diffs, record schema, commands, hashes and failed premises, and identify any additional local archive it must receive for a real source-level review. Do not claim independent code review from a summary alone.

Create **`docs/reviews/LUNA_TO_CODEX_G4_AUER_R3_PROOF_BACKED_SINGLE_CASE_FULL_HANDOFF.md`**. Include:

- readiness `READY_FOR_INDEPENDENT_SINGLE_CASE_REVIEW` or precise `BLOCKED/PARTIAL`;
- method/source-fidelity map and arithmetic backend contract with hashes and proof-critical function coverage;
- frozen development profile and all attempts, including failure logs;
- analytic fixture exact-reference containment, full-time tube, endpoints and native inclusion replay;
- the selected DDWMR query's native proof, full-time tube, endpoint, common-check outcome and work counts, if reached;
- a real archived R3 adapter fixture with native and common results shown separately;
- proof-to-query/action/source/backend binding and tamper-rejection evidence;
- exact local paths/source snapshot/commands and all deviations from Auer 2013;
- explicit matched-batch count **zero** and the unchanged research status: **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**.

Return the absolute Markdown path to the user for Codex review. No commit, push or autonomous handoff. An independently reviewed small-case package is required before any decision to run the 1,944-query matched Auer batch.
