# Codex to Luna — implement the Auer residual IVP core

**Date:** 2026-09-30  
**Working folder:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Branch / HEAD:** `luna/g2-validation-v1` / `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`.

The user mediates the work on the same laptop. **Do not commit, push, reset, clean, stash or switch branches.** Preserve all R3 and Auer v1–v7 snapshots and outputs. W1 already authorizes this scoped offline G2/G4 implementation. No G3, controller, hardware, experiment, GO or gate promotion is in scope.

## 0. Read and exact target

Read `AGENTS.md` and all four canonical `research_context/` files, then:

1. `docs/reviews/GPT_TO_CODEX_G4_AUER_R2_STRATEGY_FULL_HANDOFF.md`;
2. `docs/reviews/LUNA_TO_CODEX_G4_AUER_R3_PROOF_BACKED_SINGLE_CASE_FULL_HANDOFF.md` and `docs/reviews/CODEX_G4_AUER_R3_SINGLE_CASE_REVIEW.md`;
3. `docs/reviews/G4_AUER_METHOD_CONTRACT_v1.md`, `research/theorem_notes/G4_AUER_BASELINE_CONTRACT_v1.md`, and `validation/baselines/auer2013/ARITHMETIC_BACKEND.md`;
4. the Auer 2013 and Rauh–Auer 2011 primary PDFs and the pinned VALENCIA source around its mean-value/residual routines.

The R3 handoff completed an archived R3 adapter fixture. **Do not spend this package regenerating that fixture or writing another preflight-only contract.** The missing work is an Auer-style residual/Picard producer and independent checker that can establish a full-time IVP tube. GPT selected a **paper-faithful method reconstruction**, not original VALENCIA binary reproduction. Exact-rational arithmetic is a candidate backend; its shared G2/R3 source dependency must be disclosed.

## 1. Implement and audit one complete residual step

Build the smallest executable validated-IVP path for the two-state analytic fixture. Represent a closed step, approximate path and derivative, interval initial error, complete-time rough domain, clip interval value/generalized derivative, interval RHS/Jacobian, residual derivative iteration, outward integral bound, an explicitly checked inclusion/fixed-point premise, full-time total hull and separate endpoint hull. Map the mathematical tests to Auer 2013 Eq. (42)–(43) and Rauh–Auer 2011 §2 Algorithm 1, Eqs. (3)–(6), with source locators and all adaptations stated. Use the generalized derivative in the mean-value/Jacobian route rather than leaving `DualInterval.clip` disconnected from the solver.

Write a native proof record **and a separate checker** that recomputes the proof-critical interval operations and inclusion from frozen inputs. The checker must reject a fabricated narrow hull, altered residual iterate, changed switch interval, endpoint, action or source/profile binding. A small interval width, finite iteration count or ordinary trajectory sample is not acceptance. If you use a conservative specialization of the paper's residual operator, disclose it and prove that its inclusion condition still satisfies the published method contract; do not rename an unrelated generic interval integrator as Auer.

The interval RHS/Jacobian preflight and exact-rational primitives already exist; reuse them where sound. Review the proof-critical arithmetic source before enabling certificates. No host `libm` fallback is allowed. Retain the exact `clip(q,-1,1)` and its `[0,1]` derivative hull at both corners.

## 2. Enforce the frozen development budget

The v1 development profile declares 120 seconds, 1,024 MiB, 32,768 rational bits, 2,000,000 operations and finite step/Picard/split limits, but execution was disabled because process memory enforcement was absent. Implement a real process-level memory cap and timeout for the IVP worker, or version a justified alternative profile **before the first run**. Keep v1 and its hash unchanged. Record exact enforcement mechanism, observed peak memory, wall time and every failed/accepted step. Reject any run that exceeds its frozen limits; a process exit code of zero is not sufficient proof completion.

Source and profile changes require a new hash-bound local snapshot. Do not silently replace the v7 source while using its manifest. If a different exact-rational primitive is needed, version the arithmetic manifest and document the proof of its outward enclosure. Correct the primary-paper pagination in a new method-contract version after checking the retained PDFs; do not edit frozen v1 in place.

## 3. Execute the analytic branch-crossing fixture first

Run only this predeclared IVP first:

```text
x' = 1
y' = clip(x,-1,1)
x(0) in [0.9,0.91], y(0)=0, T=0.2
```

The true switch time lies in `[0.09,0.10]`. Exact endpoint ranges are `x(T)∈[1.10,1.11]` and `y(T)∈[0.195,0.19595]`. A proof-complete result must enclose every trajectory at **every time** on `[0,0.2]`, contain both exact endpoint ranges, propagate a separate validated endpoint across steps, and replay with the independent checker. Keep the complete step records and all rejected attempts. Label this an **independent analytic Auer-method fixture**, not Auer §5 reproduction.

If the fixture does not prove under the frozen profile, return the actual attempted rough box, residual iterates, inclusion test and termination reason. Distinguish a mathematical noninclusion, resource limit, unsupported arithmetic and implementation failure. Do not simply report “solver missing” again.

## 4. Conditional DDWMR single query

Only after the analytic fixture is proof-complete, apply the same reviewed residual path to the already selected first frozen query:

`state_low_neg__scene_d020_l-200__T_020__V_m1_m1`, with `T=1/50 s`, `V=(-1,-1)`.

Preserve all nine physical states, all twelve execution-fixed labels and the benchmark parameter image. Produce native inclusion records for every closed step, a complete-time tube and separate endpoint. Bind each record to the exact query, voltage, labels, source snapshot, arithmetic manifest and resource profile. Then apply the common collision/contact checker to the total hull once. The safety predicate may return `PASS_ON_SUPPLIED_TUBE` or `UNKNOWN_ON_SUPPLIED_TUBE`; proof completeness is the first scientific milestone. Do not pick another query based on R3 status or an Auer outcome.

If the analytic fixture proves but the DDWMR case cannot, report the exact failed proof premise and counters. Do not run any other Auer benchmark query or change the matched protocol based on the outcome.

## 5. Local freeze and return

Create a new versioned local snapshot before proof runs, with all transitive source, contracts, arithmetic backend, selected inputs, process-limit runner, third-party source/terms, compiler/runtime identities and exact commands. Hash executed members before and after; outputs remain separately hashed. Preserve every attempt and avoid any claim of independent GPT code review from a summary alone.

Write **`docs/reviews/LUNA_TO_CODEX_G4_AUER_R4_IVP_CORE_FULL_HANDOFF.md`**. Include:

- exact source diff/crosswalk to Auer 2013 and the separate checker algorithm;
- enforced resource profile, snapshot hash, run commands and source-integrity report;
- analytic fixture full-time tube, endpoint, native proof replay and exact-reference containment, or concrete failed inclusion/work evidence;
- conditional DDWMR single-case proof/tube/endpoint and common predicate, if the analytic fixture succeeds;
- tamper rejections, all attempts and failure classifications;
- shared arithmetic dependencies and bibliography correction;
- **zero** 1,944-query matched-batch evaluations and unchanged **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**.

Return the absolute Markdown path to the user. Do not commit or push. If a proof-complete analytic fixture remains impossible after a concrete solver attempt, stop this Auer reconstruction branch for scientific reassessment; do not treat that as R3 superiority.
