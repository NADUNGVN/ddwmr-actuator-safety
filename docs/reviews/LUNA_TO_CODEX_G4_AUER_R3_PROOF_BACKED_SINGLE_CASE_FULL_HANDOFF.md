# Luna → Codex — G4 Auer R3 proof-backed single-case handoff

**Package:** `G4_AUER_R3_PROOF_BACKED_SINGLE_CASE`  
**Date:** 2026-09-30  
**Disposition:** **BLOCKED/PARTIAL — no Auer IVP proof produced; one archived R3 proof replayed and adapted**  
**Branch / HEAD:** `luna/g2-validation-v1` / `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`  
**Matched comparison count:** **0 of 1,944**. No commit or push.

## 1. Decision and scope

The method, arithmetic, and small-case resource contracts are frozen. The Auer solver branch stopped **before the first IVP** because the worktree contains no source-faithful piecewise residual/Picard DDWMR solver, native full-time inclusion-record producer, independent inclusion replay checker, or process-level memory enforcement for the frozen 1,024 MiB limit. No numerical inclusion or arithmetic premise was attempted for either Auer IVP. This is an implementation blocker, not a failed numerical inclusion, arithmetic counterexample, or `UNKNOWN` result from a run.

The independent archive task did complete: the first proof-bearing row in the frozen R3 continuation order was selected and replayed from the archived R3 JSONL, then passed through `r3_record_to_common_segment` and the shared common-tube checker. The native R3 result and the common supplied-hull result are reported separately below. The R3 evaluator was not rerun.

Research status is unchanged: **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED.** No G3, controller, hardware, experiment, GO, or gate promotion is included.

## 2. Frozen method, arithmetic, and resource contracts

The method contract is [G4_AUER_METHOD_CONTRACT_v1.md](G4_AUER_METHOD_CONTRACT_v1.md), SHA-256 `b047e6edf4045540c3ba2ad52aab56bc39a0aca60033cb96a28b0017c237e379`. It labels the result a **paper-faithful method reconstruction**, not reproduction of the original VALENCIA application.

| Contract | Frozen artifact | SHA-256 | Disposition |
|---|---|---|---|
| Method / equation-to-code map | `docs/reviews/G4_AUER_METHOD_CONTRACT_v1.md` | `b047e6edf4045540c3ba2ad52aab56bc39a0aca60033cb96a28b0017c237e379` | Frozen; solver integration missing |
| Arithmetic prose | `validation/baselines/auer2013/ARITHMETIC_BACKEND.md` | `dfb0afc6e5d962a8e0f51f647d52979e9598513afeff253178d41e834dcd87eb` | Exact-rational candidate; independent audit pending |
| Arithmetic manifest | `validation/baselines/auer2013/ARITHMETIC_BACKEND_MANIFEST_v1.json` | `a1f3760b7be06d6cd95b1f3137c4776128bcc5a62ef9a7211b7c1d406a35b5f9` | Runtime and all four source-file hashes replayed successfully |
| Auer small-case profile | `validation/baselines/auer2013/small_case_resource_profile_v1.json` | `ab9a842d693862319e91351fae738af67aba0ceb4ea80bf2637d6ce0cadf35c2` | Frozen before either Auer IVP; execution disabled |

### Method/source-fidelity map

The selected primary method is Auer, Kiel & Rauh (2013), “A Verified Method for Solving Piecewise Smooth Initial Value Problems,” DOI `10.2478/amcs-2013-0055`, §§4.1–4.2, Eqs. (27), (28), (31), (33), (40), (42), and (43). The residual operator is cross-checked against Rauh & Auer (2011), §2, Algorithm 1, Eqs. (3)–(6). Both papers and the pinned VALENCIA source/terms are in `research/third_party/auer2013/` and `external/valencia-basic/` and are retained in the source snapshot.

| Obligation | Local implementation | Status |
|---|---|---|
| Eqs. (27), (28), (31): scalar expression evaluation and piecewise interval range | `validation/baselines/auer2013/rhs.py`; `piecewise.py::clip_value` and `clip_interval` | DDWMR RHS/Jacobian and exact clip range only; no integration |
| Eqs. (33), (40): generalized derivative and composition through slip | `piecewise.py::clip_derivative_interval`, `DualInterval.clip`; `rhs.py::augmented_rhs` | At a corner, or when an interval touches/crosses `-1` or `1`, derivative hull is `[0,1]`; strictly interior is `{1}`, strictly saturated is `{0}`. The 21-coordinate Jacobian preflight exists, but no IVP checker replays its mean-value inclusion. |
| Eqs. (35), (41): jump correction | No term in the clip specialization | The two clip branches agree at both corners, so their value gaps are exactly zero. Discontinuous Auer cases are out of scope. |
| Eq. (42): full-time functional tube and separate endpoint | No Auer step record, full-time tube producer, or endpoint propagator | Missing |
| Eq. (43) and Rauh–Auer residual iteration | No residual/Picard producer, full-slab inclusion checker, or native proof schema | Missing; decisive solver blocker |
| Fixed-label and held-action semantics | RHS preflight appends the twelve labels with zero derivatives | The preflight does not integrate trajectories or guarantee label propagation over steps. |

The pinned `ValEncIA-IVP_0.92_2e.cpp` is a smooth four-state double-pendulum seed. It lacks the 2013 piecewise derivative extension and the adopted nine-state DDWMR model. No patch was made to that source. Existing `validation/g4/common_tube.py` checks collision/contact predicates on a supplied total hull; it intentionally reports `certificate_emitted=false` and `ode_tube_proof_replayed=false`. A `proof_record_sha256` string alone is not replay evidence.

### Arithmetic contract

The frozen candidate is `DDWMR_EXACT_RATIONAL_TAYLOR_INTERVAL_V1`, based on Python `Fraction` and exact integer arithmetic. Runtime is `C:/msys64/ucrt64/bin/python.exe`, Python 3.12.12, executable SHA-256 `b5c33df60c2a8421dcf8117a67e848436b5d395c71ec1c0dfd96bad10f441d7f`. There is no Auer native executable, so project compile/link flags are not applicable. The manifest's hashes for `validation/g2/rational.py`, `validation/g2/interval.py`, `validation/baselines/auer2013/piecewise.py`, `rhs.py`, and the resource profile all match the working files.

Rational `+`, `-`, `*`, `/`, and serialization use exact numerator/denominator arithmetic; division rejects a denominator interval containing zero. `sqrt_lower` uses rational bisection and exact square comparisons. Sine/cosine use a rational Taylor polynomial plus a global Lagrange remainder and safe intersection with `[-1,1]`, with no host libm, argument reduction, or extrema search. The matrix exponential uses a Taylor polynomial and rational remainder majorant `e^q ≤ 3^ceil(q)`. Broad ranges may lead to `UNKNOWN`. The backend is a frozen candidate, not an independently accepted proof library; the Auer solver and checker that would consume it do not exist.

The legacy PROFIL/BIAS 2.0.8 x86-64 path remains excluded from proof output. It wraps host glibc/libm sine/cosine without a resolved all-input error bound. Its 19 finite probes and 2/2 dependency smoke checks do not establish directed transcendental soundness.

### Frozen Auer development profile

`AUER_EXACT_RATIONAL_SINGLE_CASE_DEV_V1` is separate from the proposed matched 15-second profile. It fixes 120 seconds/IVP, 1,024 MiB/IVP, 32,768 rational bits, 2,000,000 rational operations, 512 accepted steps, 1,024 rejected attempts, 32 Picard iterations/step, 64 clip branch splits/IVP, 100,000 RHS/Jacobian evaluations/IVP, and a 512 MiB proof-file cap. Taylor degrees are 20 for sine, cosine, and matrix exponential; square-root bisections are 128. No cap may be raised or retried inside this profile. **Memory enforcement is not implemented; this disables execution.**

The freeze and stop log is `results/validation/g4/auer2013/small_case_freeze_record_v1.json` and `auer_single_case_preflight_blocker_v1.json`. Both Auer run counts are zero.

## 3. Required Auer IVPs: not run

### Analytic branch-crossing fixture

Required, labeled “analytic Auer-method validation fixture; not Auer §5 reproduction”:

```text
x' = 1
y' = clip(x,-1,1)
x(0) in [0.9,0.91], y(0)=0, T=0.2
```

The switch time is `[0.09,0.10]`; exact endpoint references are `x(T) ∈ [1.10,1.11]` and `y(T) ∈ [0.195,0.19595]`. These are the expected reference ranges only. No validated tube, endpoint enclosure, residual iterate, native inclusion record, or replay report was produced. Thus there is no proof-completeness or exact-reference containment result to report.

The precise pre-run blocker is the missing full-slab residual/Picard inclusion producer and independent checker. The isolated clip range and Jacobian preflight are not an IVP run. No numerical inclusion premise failed because none was evaluated.

### Predeclared DDWMR Auer query

The frozen Auer candidate manifest v2 row remains `NOT_RUN`:

- Query: `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`
- Horizon: `1/50 s`; held voltage `(-1,-1)`
- Auer candidate-manifest canonical input SHA-256: `b59dc0f4bd05bf277384387115e7138d6df6450c187d2eefd38cae577a474e94`
- Candidate-manifest SHA-256: `77024610eab603a1ee2085feb5b6e7da0719ddd0641efa3804df6190492e59ad`
- Result: no Auer run, no Auer proof, no Auer tube, no endpoint, and no Auer common-check outcome because the analytic fixture could not be attempted with the absent solver/checker.

The complete twelve-label image is retained exactly in the R3 adapter output and in the benchmark. The intervals are `B_L,B_R,R_L,R_R,k_L,k_R,lambda_L,lambda_R ∈ [0.9,1.1]` and `C_L,C_R,rho_L,rho_R ∈ [1,1.1]`. One label realization must remain fixed through a future hold; listing the image here does not imply an Auer trajectory was propagated.

## 4. Actual archived R3 proof fixture

This is the one completed case in the package. The source is `results/validation/g2/r3/conditional_full_grid_records_r3_v1.jsonl.gz`, frozen archive manifest `conditional_full_grid_archive_manifest_r3_v1.json`. The archive has 1,728 records; compressed SHA-256 `352b6c67480133350a7d1bfc89334a1beff1dc27c64cfda46391af27982fa874`; decompressed semantic SHA-256 `de339ffcb5ee5e0c83f8d25e3077d9fd9316f83293982189aaffba0bdcf3b196`.

Selection used the first ID in the frozen R3 conditional-continuation order that had a proof object and passed native replay. It was frozen in `results/validation/g4/auer2013/r3_archived_fixture_selection_v5.json` **before** the common-check stage:

- Frozen continuation index: 0; archived line index: 0
- Query ID: `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`
- R3 canonical input SHA-256: `497d6fee06f8dde5c54905ecc1a32c0c17dbb85710e54bcea95ce85531030d5f`
- Native record semantic SHA-256: `a46c6472271fd93f20154e9696c10a865ce97615de6c0aeda69c845f2f0254d3`
- Exact archived JSONL record-line SHA-256: `a46c6472271fd93f20154e9696c10aeda69c845f2f0254d3`
- Selection artifact SHA-256: `4c6e6becc3a7e165ab3821fe0bf0436b06a79f0c1bb9745fde00e39d5a9db19f`

The R3 and Auer input digests are different because they bind different frozen method profiles. They refer to the same declared query ID; neither digest was substituted for the other.

### Native R3 result

| Item | Native archived R3 replay |
|---|---|
| Record status | `CERTIFIED` |
| Independent proof replay | PASS (`proof_replay_pass=true`) |
| Collision margin | `+0.037884917791945964 m` (exact rational retained in the selection/output JSON) |
| Contact margin | `+1.8380586882546766 N` (exact rational retained) |
| Producer work | 29,601 rational operations; max rational size 10,435 bits; configured caps 1,000,000 operations / 16,384 bits; one state leaf, one parameter leaf, one time slab |
| Checker work | 29,550 rational operations |

This is the frozen R3 method result. It is not an Auer result and does not show Auer superiority or failure.

### Common adapter result

The adapter replays the native record, builds one closed segment `[0,1/50]`, maps the full twelve-label image, and applies the R3 center/radius expansion once (`CENTER_PLUS_RADIUS_ONCE`, count 1). The adapter reuses the full-hold hull as the end enclosure because the native record does not provide a tighter endpoint range. The segment and common record are stored in `results/validation/g4/auer2013/r3_archived_adapter_fixture_v5.json`.

| Item | Common supplied-hull check |
|---|---|
| Predicate status | `PASS_ON_SUPPLIED_TUBE` |
| Collision margin | `+0.03776109218597412 m` |
| Contact margin | `+1.8380586882546766 N` |
| Common-check record replay | PASS |
| Work | 2,688 operations; max intermediate 20,826 bits under the separate 32,768-bit common-adapter profile |
| `certificate_emitted` | `false` |
| Common record's `ode_tube_proof_replayed` field | `false`; the common checker itself consumes a supplied hull |

The common collision margin is slightly more conservative than the native R3 margin. The native proof replay and the common predicate result remain separately reported. The common status is not represented as an Auer certificate, and this handoff does not promote a gate.

### Typed R3 composition and tampering

The output carries a typed R3-native-to-common composition record binding the query ID/input digest, action and held voltage, initial box, all twelve label intervals, horizon, R3 specification bundle, native/checker source commitments, v7 source-snapshot hash, native and common resource profiles, archived record hashes, serialized segment, and common-check record. The native archived JSON bytes are identified by both exact line-byte hash and semantic record hash; they happen to be equal for this canonical JSONL line. The composition replay recomputes the native replay, segment, and common check.

Five altered compositions were rejected: action/held voltage, native record digest, certified endpoint, radius mode, and segment hull. The machine-readable result records the rejection reasons. This is a replay check for the **R3 adapter fixture only**. A typed Auer proof composition, Auer native proof hash, and tamper tests against a real Auer proof cannot be supplied until the Auer proof producer/checker exists.

## 5. Attempts and failures retained

Prior R2 source and arithmetic attempts remain unchanged and are summarized in `LUNA_TO_CODEX_G4_AUER_BASELINE_R2_FULL_HANDOFF.md` and `CODEX_G4_AUER_BASELINE_R2_REVIEW.md`:

- Exact-rational clip preflight and the scalar Auer §4.1 Eq. (34)–(35) illustration replayed; these are not IVP proofs.
- Project-local PROFIL/BIAS 2.0.8 built; its dependency checks reported 2/2 and a separate finite probe covered 19 cases. The glibc/libm all-input sine/cosine contract remains unresolved, so this path is not allowed for proof output.
- The smooth legacy VALENCIA binary exited zero but printed `Condition not fulfilled: bounds are getting larger at time-step! 3062` after five re-evaluations, before the requested 3,751 steps. It is a smooth double-pendulum example, not an Auer §5 or DDWMR run.
- Auer §5 remains unreproduced; the paper's printed static-friction interval `[0.15,0.03] N` is reversed and exact reference output enclosures are absent. No value was silently repaired.

The archived R3 common-adapter attempts are in `results/validation/g4/auer2013/r3_common_adapter_attempts_v4.json`. They preserve these stops, without changing native R3 data or rerunning R3:

1. Using the R3 16,384-bit profile for the common checker stopped at exact intermediate estimate 20,826 bits. No predicate result was emitted.
2. Common profile v1 stopped because the adapted segment and checker used different `Budget` objects.
3. Common profile v2 completed predicate arithmetic but Python's default 4,300-digit integer-to-string limit stopped exact JSON serialization.
4. Common profile v3 produced an in-memory result that failed independent common-record replay because adapter work was mixed into replay work counters.
5. Common profile v4 kept the same rational, operation, wall, and square-root limits; isolated adapter conversion from checker work and bounded integer serialization at 10,000 digits. The frozen record replayed, the supplied-hull check replayed, and all five composition tamper cases were rejected.

Snapshot builder setup errors were also preserved in the execution transcript: the first v3 copy hit a read-only nested `.git` object, then one overlay path was corrected; v5/v6 builders exposed that prior manifests did not store `member_count`, so later builders derive it from the member list. These were snapshot-tool issues only; no prior R2/R3 artifacts were removed or edited.

## 6. Source snapshot, paths, and commands

The initial pre-case snapshot is `results/validation/g4/auer2013/source_snapshot_v3/`, manifest SHA-256 `e8152b1b71090b075fab6a9e1fe55c6c0927ae0325bba338b7f77693f805acc0` (683 members). The final runner used for the successful archived R3 adapter is in `results/validation/g4/auer2013/source_snapshot_v7/`, manifest SHA-256 `9bbb2462723d4ac4e8f37078689158e3653de9cf4c1071c75cd7833c97540e07` (703 members). V7 chains from v6 and preserves v3–v6. It contains the exact R3 archive and manifests, benchmark, method/backend/profile contracts, source code and terms, paper sources, old build logs/binaries, and adapter runner. No patch was applied to the pinned VALENCIA source.

After the final run, `results/validation/g4/auer2013/source_integrity_post_run_v7.json` verified the v7 manifest sidecar and **703/703** members with no mismatches. Adapter outputs were written outside the frozen snapshot. The snapshot manifest hash is also recorded in the selection and composition evidence.

The final archived-case commands, from the frozen v7 project directory, were:

```powershell
python -m validation.g4.verify_r3_archived_fixture select --output D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety\results\validation\g4\auer2013\r3_archived_fixture_selection_v5.json
python -m validation.g4.verify_r3_archived_fixture adapt --selection D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety\results\validation\g4\auer2013\r3_archived_fixture_selection_v5.json --common-profile validation/g4/r3_common_adapter_profile_v4.json --output D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety\results\validation\g4\auer2013\r3_archived_adapter_fixture_v5.json
```

The Auer source/profile freeze was produced with `python validation/scripts/create_auer_source_snapshot_v3.py`. After adapter-tool failures and versioned fixes, the final reviewed runner snapshot was produced with `python validation/scripts/create_auer_source_snapshot_v7.py`. Python syntax compilation passed for the adapter and snapshot scripts. No Auer IVP command was run.

Key output hashes:

- Selection: `r3_archived_fixture_selection_v5.json` — `4c6e6becc3a7e165ab3821fe0bf0436b06a79f0c1bb9745fde00e39d5a9db19f`
- Adapter result: `r3_archived_adapter_fixture_v5.json` — `1b3a97e171d12585bc8918b819b6b28403467926889dc9c5488786c01c69b92b`
- Final runner source in v7: `project/validation/g4/verify_r3_archived_fixture.py` — `106b46506dbf35f03bd6d1b6f05acb834324e08a494becd299b6efc460b5eb72`
- Common adapter profile v4 — `1e5f081e65fc8c6420ced12f0082b557262e81ca9503aef3be241cc35638a69e`
- Post-run source integrity: `source_integrity_post_run_v7.json` — status `PASS`, 703/703 members

## 7. Review boundary and remaining work

This package is **BLOCKED/PARTIAL** for Auer. It supplies the equation map, frozen candidate backend/profile, exact blocker, preserved attempts, and one real archived R3 adapter fixture. It does not supply the analytic Auer tube, a DDWMR Auer query tube, native inclusion replay, Auer composition/tamper replay, or an independent Auer source-level implementation review. The local reviewer should inspect the exact files in `source_snapshot_v7/`; the handoff is self-contained, but the uncommitted archive/snapshot may need to be provided if the review environment cannot access local files.

The 1,944-query matched comparison was **not run**; matched query count is **zero**. No Auer run, no controller, no hardware/experiment, no commit/push, and no research gate changed.
