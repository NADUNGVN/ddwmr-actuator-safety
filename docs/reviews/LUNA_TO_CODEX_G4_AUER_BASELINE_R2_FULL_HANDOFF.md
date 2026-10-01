# G4 Auer baseline R2 — full handoff for independent review

**Date:** 2026-09-30  
**Readiness:** **`BLOCKED/PARTIAL`** — source/build preparation and common-checker interface work are reviewable; a source-faithful validated Auer solver is not available.  
**Repository / branch / base HEAD:** `ddwmr-actuator-safety` / `luna/g2-validation-v1` / `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`  
**Research disposition:** **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED.**

## 1. Decision and stop condition

The requested Auer baseline is **not complete or validated**. WSL2 provided a project-local candidate build for the pinned smooth VALENCIA seed and PROFIL/BIAS 2.0.8. The available seed does not contain the 2013 piecewise derivative extension. The WSL build therefore establishes compilation/link feasibility for the legacy core only. A finite BIAS rounding probe and a legacy smooth example also ran, with the limits below.

There is no adapted nine-state/twelve-label Auer solver, replayable Picard/residual inclusion checker, DDWMR full-time tube, or propagated DDWMR endpoint. The common tube checker evaluates predicates on a supplied hull and intentionally emits no certificate. The 2013 §5 numerical example also remains unreproduced because the printed friction interval is reversed and exact reference enclosures are absent.

**Matched Auer query evaluations: 0.** All 1,944 prepared IDs remain `NOT_RUN`; no R3 result was joined. The 1,944-query comparison was not run. No G3 or hardware work was started. No commit, push, reset, clean, stash, or branch change was made.

## 2. Frozen package and principal hashes

The final local snapshot is:

`D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety\results\validation\g4\auer2013\source_snapshot_v2`

Its manifest lists 681 files across `project/`, `environment/`, and `runs/`. Every listed file's size and SHA-256 was recomputed after the snapshot-local replays; there are no member mismatches. The manifest sidecar matches. The v1 snapshot was independently checked by the v2 builder before reuse: all 324/324 original member hashes and its `f64ff41901ff99412965785c56bf9abef68b85c5efcf8e8c9dd0ae81e30724b2` manifest digest match.

| Artifact | SHA-256 |
|---|---|
| v2 snapshot manifest | `c78523df6616dc46c062841169a7e584fcb622d64acfa4cde1ba4b53c2cb6af1` |
| candidate manifest v2 | `77024610eab603a1ee2085feb5b6e7da0719ddd0641efa3804df6190492e59ad` |
| common tube fixture result and snapshot replay | `93ad73bd4d330951e15afd17196c163ad694a6c8fb48aaa6659c741522e932ca` |
| rebuilt legacy smooth seed binary | `bc3fdf7005f2fe18b1ef34439872c14fe87e90c39e2a531920d273245eb0eb67` |
| original WSL legacy smooth binary | `47a0ddf576718a8b451dd084f1afaa5800a0a4a6124b8d7cd2bf17e137aa225b` |
| BIAS rounding probe binary | `c42d1a1444d3b82ab02d0bca5553609789611b370fe4a9ad4ad94f7884672819` |
| PROFIL/BIAS 2.0.8 source archive | `1706e684166360d60f33b4c9301cfe48a6153fc0c624f2087efa9bc94aa07c20` |
| Auer et al. 2013 paper PDF | `d6310c8fd32280addda3f50e3367f9923940641d39de0e70a0932869a2d0ead2` |
| Rauh & Auer 2011 paper PDF | `1405b54eaa25c5d3874af74ac71087364f3a84ddada675c336e378779e902265` |
| `validation/g4/common_tube.py` | `564c0ffe608be6d0413def643a5dff7b455613c61b56f0ea42684cc7c6874d25` |
| `validation/g4/verify_common_tube.py` | `67c940a10675947fa2812cd2442e6751370f74d719da6d8a9528459958b372dc` |
| candidate protocol v2 | `16d252d769a3a760fec9dbb0bacc0bc5f6f5714f3b81ff94e60d7772948057d5` |
| source/applicability audit v2 | `08acab13e6f21b18eefd19f1e93fe7e9a39db6adba2a0e28a03b2fd1018dc42e` |

The snapshot includes the frozen configuration and R2 manifest, shared G2 arithmetic/model/checker sources, Auer clip/RHS preflight code, common checker and fixtures, versioned candidate manifest and protocol, Auer and 2011 VALENCIA papers, the pinned VALENCIA source archive, PROFIL/BIAS and FADBAD++ source/terms, project-local WSL build products, exact environment description, raw logs, and small-case outputs. The snapshot is `LOCAL_UNCOMMITTED_BLOCKED_PARTIAL_REVIEW_PACKAGE`; the worktree is intentionally not clean.

## 3. Source fidelity and equation-to-code map

The adopted plant is MASTER v2.1: nine physical states `[p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R]`; body speed is `u` and the held input is the two-wheel terminal voltage. The execution-fixed parameter vector is represented by twelve benchmark labels.

| Equation or proof obligation | Local evidence | Status |
|---|---|---|
| Pose kinematics `ṗ_x=u cos(theta)`, `ṗ_y=u sin(theta)`, `thetȧ=r` | `validation/baselines/auer2013/rhs.py:95-99` | Exact-rational interval/AD preflight evaluator; not integrated in VALENCIA |
| Slips `sigma_L=R_w omega_L-u+b r`, `sigma_R=R_w omega_R-u-b r`; `F_j=C_j clip(sigma_j/v_s,-1,1)` | `rhs.py:90-93` | Benchmark equations mapped for the local evaluator |
| Body and yaw dynamics | `rhs.py:100-103` | Mapped to force sum/difference and damping in the local evaluator |
| Wheel and electrical dynamics | `rhs.py:104-109` | Mapped with one constant voltage pair in the local evaluator |
| Continuous piecewise derivative of clip at both corners | `validation/baselines/auer2013/piecewise.py:27-36,167-169` | Clip-specific exact-rational specialization; derivative hull is `[0,1]` when a range touches/crosses a corner |
| Twelve constant hidden labels | `rhs.py:70-75,110-118` | Evaluator appends twelve coordinates with identically zero RHS and gradients; no trajectory solver enforces this augmentation yet |
| Piecewise mean-value/Jacobian path and residual inclusion | Pinned seed functions `state_eq_i` (line 88), `state_eq_mid_i` (126), `state_eq_F_i` (167), `MVR_d_R_i` (658 onward), `compute_R` (798 onward) | These are smooth double-pendulum seed functions. The Auer 2013 piecewise extension is absent and no DDWMR port was made |

The local `rhs.py` evaluates interval sine/cosine with the shared exact-rational Taylor enclosure, not the WSL BIAS runtime. This supports only the Python range/Jacobian preflight. No changes were made to the third-party VALENCIA or PROFIL/BIAS source, no custom Picard routine was introduced, and no plant or MASTER formulation was changed. The source-to-code gap remains the missing connection between Auer's piecewise derivative and the pinned VALENCIA interval mean-value/Jacobian evaluation.

The pin is VALENCIA `basic` revision `d1a09ceb3f68deb40357bdc89944b28997e9fb30`. The seed documents PROFIL/BIAS 2.0.2 and tested 2.0.4; the locally available official source is 2.0.8. The 2011 paper identifies PROFIL/BIAS 2.0.6 and FADBAD++ 2.1 for its later lineage. This version mismatch is unresolved. The seed is a core lead, not the full 2013 application.

## 4. Build and arithmetic evidence

**Environment:** WSL2 Ubuntu 24.04.3 LTS, x86-64; Linux kernel `6.18.33.2-microsoft-standard-WSL2`; GCC/G++ 13.3.0; glibc 2.39 (`2.39-0ubuntu8.9`); GNU Make 4.3. PROFIL/BIAS 2.0.8 was built and installed only under `results/validation/g4/auer2013/wsl_probe/Profil-2.0.8`.

`make all`, local `make install`, and `make check` completed for PROFIL/BIAS. The check reported **2/2 passed** (`TBias`, `TBiasF`). `TBiasF` is a narrow smoke test and does not establish a broad sine/cosine contract.

The BIAS profile uses the x86-64 Linux compatibility configuration. It sets `__BIASSTDFUNCINVALIDBITS__` to zero and wraps host sine/cosine results with a predecessor/successor. The profile documentation notes that glibc/libm's error bounds are not specified sufficiently to guarantee the desired result. The BIAS probe checked 19 finite cases: exact-rational directed addition, multiplication and division; sine and cosine at seven binary64 inputs; and both function ranges over `[-0.25,0.25]`. The rational Taylor remainder checks passed for those represented inputs. Replaying the probe from the v2 snapshot printed `PASS checks=19`. This finite set does not establish a global libm error bound or all-input directed transcendental soundness. The WSL arithmetic target is **not approved for certificates**.

The snapshot-local legacy seed rebuild used this exact command from `source_snapshot_v2/project`:

```text
wsl.exe --cd /mnt/d/Research/Teacher_Vien/projects/ddwmr-actuator-safety/results/validation/g4/auer2013/source_snapshot_v2/project g++ -std=gnu++98 -O2 -frounding-math -fno-fast-math -ffp-contract=off -I external/valencia-basic/dependencies/Profil-2.0.8/src -I external/valencia-basic/dependencies/Profil-2.0.8/src/Base -I external/valencia-basic/dependencies/Profil-2.0.8/src/BIAS -I external/valencia-basic/dependencies/Profil-2.0.8/src/Packages -I external/valencia-basic/dependencies/fadbad-1.4/FADBAD++ external/valencia-basic/free-source/ValEncIA/ValEncIA-IVP_0.92_2e.cpp -L ../environment/wsl_probe/Profil-2.0.8/lib -lProfilPackages -lProfil -lBias -llr -lm -o ../runs/ValEncIA-IVP_0.92_2e-smooth-rebuilt
```

Linking succeeded with exit code 0 and produced the rebuilt binary hash in §2. Diagnostics include a legacy `%d`/`long int` format mismatch and a linker warning that `fpRound.o` lacks `.note.GNU-stack` and implies an executable stack. A successful compile/link does not verify rounding, the Auer extension, Picard inclusion, or an ODE tube. The full command and replay record are retained at `source_snapshot_v2/runs/auer_seed_rebuild_record.md`.

**Terms:** PROFIL/BIAS source retains GNU GPL v2 terms. FADBAD++ 1.4's notice permits verbatim copies under its stated terms and prohibits inclusion in a commercial package without prior explicit written permission. Third-party source and papers remain local in this uncommitted project snapshot.

## 5. Common full-time tube interface and replay

`validation.g4.common_tube.TubeSegment` uses exact rational closed times; nine physical total-state hulls; all twelve full-image label intervals; separately tagged endpoints; provenance; and a radius expansion mode/count. `TubeSegment` verifies each endpoint is inside its slab's total hull. The chain checker requires `[0,T]` coverage, rejects gaps/overlaps, requires identical propagated endpoint intervals on adjacent boundaries, and compares labels to the complete declared image on every slab.

The one-time rule is: `NATIVE_TOTAL_HULL` has expansion count 0; `CENTER_PLUS_RADIUS_ONCE` and `CENTER_PLUS_RESIDUAL_ONCE` have count 1; a segment cannot claim multiple expansions. The Auer adapter requires full-step `x_app` and residual ranges in binary64 hexadecimal form, converts each represented value exactly to a rational, and sums the intervals once. It separately checks the provided start/end intervals against the resulting hull. **It does not verify that the binary64 values were outward rounded or replay the referenced native proof digest.** The R3 adapter first replays its native record, then expands the stored radius once; R3 native results are unchanged, and any shared-check result belongs to a separate `R3_COMMON_CHECK` series.

The common checker applies the same exact-rational collision lower bound and algebraic contact sufficient predicate to every closed slab and every obstacle. It checks the full parameter image, including shared boundaries. It reports only `PASS_ON_SUPPLIED_TUBE` or `UNKNOWN_ON_SUPPLIED_TUBE`, always with `certificate_emitted=false` and `ode_tube_proof_replayed=false`.

Replay from the frozen v2 snapshot:

```text
python -m validation.g4.verify_common_tube --output ../runs/common_tube_preflight_v2_replay.json
```

Result: **9 synthetic fixture groups passed**, the snapshot output is byte-identical to `common_tube_preflight_v2.json` (SHA-256 above), and matched-query evaluations are zero. Fixtures cover a positive two-slab supplied hull; an UNKNOWN full-time hull crossing an obstacle with clear endpoint boxes; boundary/gap behavior; rejection of changed labels; one-time radius expansion; exact binary64 conversion; clip saturation; and tampered-hull replay rejection. These are interface fixtures, not trajectories or safety certificates. No inclusion-record tampering test is possible because the Auer inclusion checker does not exist.

## 6. Solver proof record and unavailable trajectory evidence

There is **no machine-readable per-step Auer proof record** to replay. A future step record must freeze and identify: query/input and source hashes; exact closed step times; rough domain; approximate path; interval RHS and full Jacobian; residual derivative ranges; every Picard iterate; recomputed verified residual inclusion and its premises; full-time `x_app(t)+R(t)` state and label enclosure; and the propagated endpoint. The checker must recompute the inclusion from those frozen inputs rather than trust a solver's Boolean. Failed inclusion, missing time coverage, invalid arithmetic, or a work cap must fail closed.

The common checker record is a different object: it replays the predicates on the supplied total hull. Its positive and UNKNOWN fixture records replay successfully; the tampered total hull does not. This does not validate VALENCIA's fixed-point hypotheses or any IVP trajectory. There are no DDWMR endpoint ranges, step counters, or solver cost measurements.

## 7. Reference and development cases

| Case and replay command | Outcome | Scope limit |
|---|---|---|
| `python -m validation.baselines.auer2013.verify_preflight --output ../runs/clip_preflight_checks_v2_replay.json --reference-output ../runs/reference_eq34_reproduction_v2_replay.json` | 20 exact-rational checks pass from the v2 snapshot; comparison queries 0 | Includes the §4.1 Eq. (34) naive mean-value failure and Eq. (35) correction. It is a scalar illustration, not an IVP run |
| `python -m validation.g4.verify_common_tube --output ../runs/common_tube_preflight_v2_replay.json` | 9 synthetic interface fixture groups pass and records replay | No physical trajectory or benchmark query |
| `python3 environment/wsl_probe/check_bias_rounding_probe.py environment/wsl_probe/bin/auer_bias_rounding_probe` | 19 finite checks pass | Does not settle global libm rounding |
| Rebuild command in §4, then run `../ValEncIA-IVP_0.92_2e-smooth-rebuilt` from `source_snapshot_v2/runs/legacy_smooth_replay` | Link exit 0; example process exit 0 but reports `Condition not fulfilled: bounds are getting larger at time-step! 3062` after five re-evaluations | Smooth four-state legacy pendulum only; not the DDWMR and not §5 |

The Auer §5 table prints `F_s=[0.15,0.03] N`, a reversed interval, and does not provide exact reference output enclosures. No endpoint order was silently repaired. **§5 was not reproduced.**

## 8. Candidate comparison protocol v2

`research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v2.md` is the revised, unapproved profile. It retains the maximum accepted step width `0.001 s`, raises the proposed step cap from 100 to **1,000/query**, and records why: 100 steps cover a 0.1 s hold at that maximum width, while 1,000 allows up to tenfold subdivision. This is resource allowance only, not evidence of inclusion convergence. Candidate resource values remain 10 range splits/component/step, five recovery attempts/step, 1,000,000 RHS+Jacobian calls/query, 15 s/query, and 512 MiB/query.

Candidate manifest v2 has 1,944 unique IDs exactly in R2 order; its ID digest is `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`. Verification found all rows `NOT_RUN`, `comparison_run=false`, no R3 join, and the v2 proposed cap of 1,000. The v2 protocol is **not locked**. It cannot authorize a matched run while the source-faithful solver, inclusion checker and arithmetic review are missing.

## 9. Local files and preservation record

New R2 review/interface artifacts are:

- `docs/reviews/G4_AUER_SOURCE_AND_APPLICABILITY_v2.md`
- `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v2.md`
- `validation/g4/common_tube.py`, `validation/g4/verify_common_tube.py`, `validation/g4/__init__.py`
- `validation/scripts/version_auer_candidate_manifest_v2.py`
- `validation/scripts/create_auer_source_snapshot_v2.py`
- `results/validation/g4/auer2013/auer_matched_candidate_manifest_v2.json`
- `results/validation/g4/auer2013/common_tube_preflight_v2.json`
- `results/validation/g4/auer2013/source_snapshot_v2/` including its 681-member manifest, WSL environment and replay records

Earlier uncommitted preflight artifacts, third-party sources and snapshot v1 remain present and were included or cross-checked as documented. `git status` shows the work as untracked local work; HEAD and branch remain the values above. Nothing was committed or pushed.

## 10. Reviewer action requested

Please review this package as a **blocked/partial preparation handoff**, especially the BIAS/glibc caveat, compatibility of PROFIL/BIAS 2.0.8 with the older seed, source fidelity of any future §4.1 derivative integration, the absent Picard inclusion checker, and the common checker/adapters. The matched comparison must remain stopped until those issues are resolved and independently reviewed.
