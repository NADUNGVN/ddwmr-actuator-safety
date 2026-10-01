# Codex to Luna — finish the Auer baseline for independent review

**Date:** 2026-09-30. **Local assignment; no commit or push.**  
**Working folder:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Starting branch / HEAD:** `luna/g2-validation-v1` / `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`.

The user mediates Codex and Luna on one laptop. Preserve all untracked files and R3 artifacts. Do not reset, clean, stash, switch branches, commit or push. Do not alter MASTER v2.1 or the gate status. W1 already permits this scoped offline baseline work.

## 1. Read and disposition

Read `AGENTS.md` and all four canonical `research_context/` files, then:

1. `docs/reviews/LUNA_TO_CODEX_G4_AUER_PREFLIGHT_FULL_HANDOFF.md`;
2. `docs/reviews/CODEX_G4_AUER_PREFLIGHT_REVIEW.md`;
3. `docs/reviews/G4_AUER_SOURCE_AND_APPLICABILITY_v1.md`;
4. `research/theorem_notes/G4_AUER_BASELINE_CONTRACT_v1.md`;
5. `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v1.md`;
6. the pinned 2013 Auer paper, 2011 VALENCIA paper, and relevant source/readmes in the local snapshot.

Codex accepts the preflight only as **partial preparation**: 324/324 snapshot members and the five recorded outputs match their hashes; all 1,944 prepared IDs are unique, match R2 and remain `NOT_RUN`; the isolated clip and scalar-reference records have the stated limited scope. The validated solver, complete tube and common checker are missing. **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.**

## 2. Establish an actual validated build target

WSL2 Ubuntu is available on this laptop and has `g++` and `make`. Investigate it as a **project-local candidate** for the pinned VALENCIA seed plus pinned dependency sources. Do not assume that Linux itself solves the PROFIL/BIAS rounding issue. Record exact distro, compiler, libc, architecture, dependency versions, source hashes, compiler/link flags and resulting binary hash. Inspect the source's rounding-mode implementation and the documented glibc/libm caveat. Provide focused directed-rounding checks for interval arithmetic and every transcendental operation actually used by the adapted DDWMR solver; explain what the checks do and do not establish. Reject fast-math, unsupported rounding or an unreviewed substitution. A mere successful link is not validation.

Resolve the 2.0.8 versus historical 2.0.2/2.0.4 compatibility question explicitly. Keep any patches as reviewable diffs from the pinned source. Respect the recorded academic/noncommercial and GPL terms; keep source local. If no defensible target can be established, record commands/logs and the exact blocker, then continue the independent checker/interface work below. Do not silently replace the published method with a custom Picard routine or call a nonvalidated binary a baseline.

## 3. Complete the source-faithful solver proof path

Patch/adapt the solver path so that the 2013 continuous-clip piecewise derivative is used by its interval mean-value/Jacobian evaluation, with the nine MASTER states and twelve **constant** parameter labels. Maintain one hidden label realization over the whole hold and one common held voltage. Preserve positive-denominator checks and the benchmark parameter image. Document every change against the 2013/2011 equations and the pinned source lines; distinguish published-method machinery from application-specific wiring and any new algorithmic substitution.

For each closed step, retain a machine-readable proof record of the rough domain, approximate path, interval RHS/Jacobian, residual derivative ranges, every Picard iterate, the **verified residual inclusion**, full-time `x_app(t)+R(t)` enclosure and propagated endpoint. Make the inclusion checker recompute its premises from frozen inputs rather than trusting a Boolean produced by the solver. A finite number of iterations, numerical convergence, or validated endpoints alone is insufficient. Failed inclusion, missing time coverage, invalid rounding or resource exhaustion must never emit CERTIFIED.

Use a small, predeclared set of reference/development cases first. The existing §4.1 scalar Eq. (34)–(35) check is **not** an IVP reference run. If the paper's §5 example cannot be reproduced from authoritative values because of the reversed printed interval and absent exact output data, retain that limitation. A separately identified analytic clip IVP and a legacy smooth source example can check implementation behavior, but must not be described as reproducing §5. Record all attempted cases and outcomes, including failures.

## 4. Implement the common full-time check without double counting

Define one typed `TubeSegment` with exact closed time boundaries, nine physical interval hulls, twelve fixed-label hulls, native segment provenance and a separately tagged endpoint. Choose **one** common representation for pose: either an already expanded state hull or a center plus a separately applied radius. State and enforce the invariant that no radius is added or subtracted twice. The Auer adapter must enclose the full trajectory across each closed step; endpoint samples alone do not qualify. Convert every outward binary64 bound to its exact binary rational value before the common predicates.

Implement the same outward collision and algebraic contact sufficient predicates for both adapters. Preserve the full parameter-image cover and every obstacle. Check every closed segment, including common boundaries. Keep original R3 certificates and files unchanged; any R3 result under the new checker is a distinct `R3_COMMON_CHECK` series. Add focused checks for shared boundaries, full-time versus endpoint-only behavior, parameter constancy, a saturated clip corner, pose-radius application once, and rejection after tampering with an enclosure or inclusion record. Produce a replayable small positive and small UNKNOWN case before any batch run.

## 5. Freeze, review and stop condition

Revise the draft protocol if necessary **before** it is locked. In particular, the proposed 100 steps at 0.001 s leave no subdivision allowance for a 0.1 s hold; justify or change this cap with a new protocol version. Report solver precision/work counters and rational checker costs separately. Use the same 1,944 frozen input IDs and preserve all statuses in the future denominator. Never tune against selected R3 outcomes while calling the profile predeclared.

Create a new versioned local source snapshot after the implementation and protocol are finalized; the current source-audit text changed after snapshot v1. Hash every transitive source, configuration, paper/source archive and terms file needed to explain the run, plus the executable and environment. Run only small declared reference/development cases from that snapshot. Record source hashes before and after. An independently reviewable source diff, build/rounding evidence, full-time proof records, replay checker and common adapters are the return target.

**Do not launch the 1,944-query matched comparison.** Return the completed baseline package for Codex/GPT soundness and source-fidelity review first. If the baseline cannot be completed faithfully, return the exact blocker, preservation evidence and what independent work was completed; do not report R3 superiority from the blockage. Do not start G3 or hardware work.

## 6. Required return file

Write **`docs/reviews/LUNA_TO_CODEX_G4_AUER_BASELINE_R2_FULL_HANDOFF.md`**. Include:

- readiness `READY_FOR_INDEPENDENT_BASELINE_REVIEW` or precise `BLOCKED/PARTIAL`;
- source revision, local snapshot/manifest/binary hashes, build and rounding evidence, licenses and all local paths changed;
- equation-to-code diff and every solver adaptation;
- per-step inclusion/tube/end-point proof format and checker replay results;
- reference/development case commands, success and failure records, and limits of §5 reproduction;
- typed common adapters/checker results, radius-once rule, boundary/parameter coverage;
- proposed final matched protocol/resource profile, with any revisions clearly versioned;
- explicit count of matched query evaluations (expected **zero** in this assignment);
- **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**.

Give the user the absolute Markdown path. No commit, push or autonomous agent handoff.
