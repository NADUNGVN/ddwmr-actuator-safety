# Auer 2013 source and applicability audit — R2 update

**Date:** 2026-09-30  
**Base revision:** `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46` on `luna/g2-validation-v1`  
**Status:** `BLOCKED/PARTIAL`; no validated DDWMR Auer solver or matched result.

This update supplements, rather than overwrites, `G4_AUER_SOURCE_AND_APPLICABILITY_v1.md`. MASTER v2.1 remains authoritative. Research disposition remains **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**.

## 1. Source and compatibility disposition

The pinned VALENCIA-IVP `basic` source revision is `d1a09ceb3f68deb40357bdc89944b28997e9fb30`. Its `ValEncIA-IVP_0.92_2e.cpp` is the smooth legacy core, not the C++ piecewise derivative class described by Auer et al. (2013), §4.1. It implements a double-pendulum example; it does not implement the adopted nine-state DDWMR equations or the 12 fixed parameter labels. No patch was made to this third-party source.

The seed documentation requests PROFIL/BIAS 2.0.2 and reports testing 2.0.4. The locally retained official source is PROFIL/BIAS 2.0.8. FADBAD++ 1.4 is retained; the later 2011 VALENCIA publication identifies PROFIL/BIAS 2.0.6 and FADBAD++ 2.1. Compatibility of this older seed with the available 2.0.8/1.4 pair is not established by compilation. The 2013 article says its reported application used a separate C++ class implementing its §4.1 derivative; that extension is not present in the pinned seed.

## 2. Build target investigated

A project-local WSL2 Ubuntu 24.04.3 x86-64 build was investigated after the Windows MSYS2 target failed to provide a supported PROFIL/BIAS configuration. Recorded environment: WSL2 Linux kernel 6.18.33.2, GCC/G++ 13.3.0, GNU make 4.3, glibc 2.39. No system-wide installation was performed; the 2.0.8 build/install is under `results/validation/g4/auer2013/wsl_probe/Profil-2.0.8`.

The 2.0.8 library build and install completed. Its `make check` reported 2/2 (`TBias` and `TBiasF`). The `TBiasF` test is narrow and does not validate all sine/cosine interval cases. A separate BIAS probe compiled and 19 finite checks passed: directed addition, multiplication and division against exact rationals, plus sine/cosine point and `[-0.25,0.25]` range checks against rational Taylor enclosures. The Taylor remainder uses a derivative bound of 1 at those tested points/ranges. These checks establish only those finite cases; they do not prove correct rounding for every operation or establish a global glibc/libm transcendental error bound.

The x86-64 PROFIL/BIAS profile sets `__BIASSTDFUNCINVALIDBITS__` to zero and expands sine/cosine results by one predecessor and successor around the host libm result. The profile's documentation flags the glibc/libm error-bound limitation. Since the exact outward error over all DDWMR inputs has not been proved, this profile is not accepted for certificate output.

The pinned smooth VALENCIA seed was compiled and linked against the project-local 2.0.8 build after adding `-llr`. Compiler flags included `-O2 -frounding-math -fno-fast-math -ffp-contract=off`; the link also emitted format warnings (`%d` against `long int`) and a missing `.note.GNU-stack` warning. This demonstrates a runnable legacy program on the candidate Linux build, not validated arithmetic, source compatibility, or implementation of the Auer 2013 piecewise method.

The legacy smooth example executable returned exit code 0, but its own output says `Condition not fulfilled: bounds are getting larger at time-step! 3062`; it retries/reinitializes and does not complete its requested 3,751-step example. This four-state pendulum case is not Auer §5 and is not the DDWMR.

## 3. Equation-to-code crosswalk and adaptation status

| Source/model obligation | Local implementation | Disposition |
|---|---|---|
| Auer 2013 §4.1, Eqs. (27)–(33), branch value and active derivative hull | `validation/baselines/auer2013/piecewise.py` implements the continuous `clip(q,-1,1)` specialization and its `[0,1]` corner derivative hull | Exact-rational local component only; no general SPW branch engine and no VALENCIA integration |
| Multivariate mean-value/Jacobian propagation through clip | `DualInterval.clip` in `piecewise.py`; `validation/baselines/auer2013/rhs.py` composes the nine-state RHS with 12 constant label directions | Mathematical preflight only; not the Auer solver's mean-value/Jacobian path |
| MASTER v2.1 nine physical states and one held two-wheel voltage | `rhs.py` maps pose kinematics, body force/yaw, wheel dynamics and motor current dynamics from `validation/configs/benchmark_v1.json` | RHS/Jacobian range evaluator only. Exact-rational trigonometric ranges are an implementation choice for this Python check, not a patch to PROFIL/BIAS or the VALENCIA core |
| Twelve execution-fixed parameters | `rhs.py` appends labels in the benchmark order and assigns identically zero RHS/gradient to those coordinates | Checks an augmented 21-coordinate function range; it does not prove a solver keeps one label realization for the trajectory |
| Auer §3.3/§4.2, full-step tube and residual inclusion | No adapted solver, Picard inclusion record, inclusion replay checker, or DDWMR endpoint propagator exists | Missing; no trajectory tube or endpoint is available |
| Shared full-time predicate layer | `validation/g4/common_tube.py` and `verify_common_tube.py` define total-hull segments, label/boundary checks, Auer/R3 adapters, and exact-rational collision/contact predicates | Synthetic interface evidence only. The Auer adapter does not replay an upstream inclusion proof and the checker always returns `certificate_emitted=false` |

No change was made to MASTER, plant equations, the pinned Auer/VALENCIA sources, the R3 records, or gates. The only proposed resource-profile change is versioned in `G4_AUER_MATCHED_PROTOCOL_v2.md` and the v2 candidate manifest: maximum 1,000 steps/query, retaining a proposed maximum accepted step width of 0.001 s. This gives a proposed tenfold subdivision allowance over the 100 minimum-width steps for a 0.1 s hold; it is not a convergence result.

## 4. Reproductions and limits

The exact-rational scalar illustration in Auer §4.1, Eqs. (34)–(35), reproduces the naive mean-value failure and jump-corrected enclosure. This is a scalar reference check, not an IVP run. Targeted piecewise/augmented-RHS checks are recorded in `clip_preflight_checks_v1.json` and remain isolated from solver validation.

The accessed Auer §5 paper prints the friction interval as `F_s=[0.15,0.03] N`, with reversed endpoints, and does not tabulate exact reference trajectory/enclosure outputs. No repair was inferred, and §5 was not reproduced. The smooth legacy example failure above is recorded as a separate behavior check only.

The v2 common checker ran nine synthetic interface fixture groups. It replayed a small positive supplied-hull predicate and a small UNKNOWN supplied-hull predicate; rejected a coverage gap, changing fixed labels, and a tampered hull; checked full-time versus endpoint-only behavior, radius-once handling, exact binary64 conversion, and a clip saturation corner. These are not ODE trajectories or benchmark query evaluations.

## 5. Terms and source preservation

The local PROFIL/BIAS source includes GNU GPL version 2 terms. FADBAD++ 1.4's retained copyright notice permits verbatim redistribution under its stated conditions and bars use in commercial packages without prior written permission. Source archives and papers remain local. The pinned VALENCIA package terms and academic/noncommercial conditions are retained with the source; no third-party source was published or modified. A reviewer should inspect the retained notices before any further distribution.

## 6. Readiness

**Readiness: `BLOCKED/PARTIAL`.** The local Linux build establishes a candidate build target for the legacy smooth core and the common exact-rational interface fixtures, but does not resolve the libm error-bound issue or historical dependency compatibility. More decisively, the source-faithful Auer piecewise derivative is not integrated with VALENCIA's interval mean-value/Jacobian evaluation; there is no replayable Picard/residual inclusion proof, full-time DDWMR tube, or endpoint result. Do not call this a completed or validated Auer baseline. Matched query evaluations remain **zero**.
