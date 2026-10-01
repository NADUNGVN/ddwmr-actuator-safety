# Luna to Codex — G4 Auer preflight handoff

**Date:** 2026-09-30  
**Readiness:** **BLOCKED/PARTIAL** — isolated clip extension and the §4.1 scalar reference are ready for review; the full VALENCIA-IVP/DDWMR baseline is not ready to run.  
**Comparison:** 1,944 original IDs prepared; **zero query evaluations**; all Auer statuses are `NOT_RUN`.  
**Version control:** no commit, push, reset, clean, stash, or branch switch.

## 1. Disposition

The requested source audit, a local implementation of the continuous clip derivative specialization, targeted checks, an exact reproduction of the Auer paper’s scalar §4.1 illustration, and a matched-protocol candidate are prepared. The pinned legacy VALENCIA-IVP seed passed a syntax-only compile against the locally retrieved dependency headers.

The complete selected baseline is **not implemented or verified**. No source-faithful executable was produced, no VALENCIA residual/Picard loop was adapted to the 21-coordinate DDWMR, no full-time DDWMR tube or endpoint was computed, and no common collision/contact checker adapter was run. The paper’s §5 friction/hysteresis result was not reproduced because its printed static-friction interval has reversed endpoints and it reports curves rather than exact enclosure data. These are blockers to a matched run, not evidence that R3 is better.

The 2013 method remains a plausible candidate. It may not be described as a completed or source-faithful comparator from the work here. The preflight requires independent review of baseline soundness and source fidelity before the 1,944-query run; that prerequisite remains open.

## 2. Starting state, workspace and source freeze

- Repository: `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`
- Starting branch: `luna/g2-validation-v1`, tracking `origin/luna/g2-validation-v1`
- Starting and final HEAD: `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`
- Initial untracked user files preserved: `docs/CODEX_TO_LUNA_G4_AUER_PREFLIGHT_v1.md` and `docs/reviews/GPT_TO_CODEX_G2_VALIDATION_R3_SCIENTIFIC_REVIEW_FULL_HANDOFF.md`.
- No tracked source or canonical research-context file was modified. The worktree is not clean; the new documents, code, source downloads and results remain untracked.

The runs used a local snapshot at `results/validation/g4/auer2013/source_snapshot_v1/`, tagged `LOCAL_UNCOMMITTED_SNAPSHOT`, with 324 hashed source/config/specification members. Its manifest is `snapshot_manifest.json`, SHA-256 `f64ff41901ff99412965785c56bf9abef68b85c5efcf8e8c9dd0ae81e30724b2`; the sidecar is `snapshot_manifest.sha256`. The recorded base revision, branch and dirty status are in the manifest. The source manifest and sidecar passed before- and after-run checks with no mismatches; see `runs/source_integrity_pre_run.json` and `runs/source_integrity_post_run.json`.

The manifest covers the baseline code, all shared `validation/g2` dependencies, the benchmark and frozen R2 universe, the research specifications, the Auer/VALENCIA sources, extracted dependency sources, and their terms. The output files are outside the hashed source-member set and have their own hashes below. The handoff was written after the preflight runs; it was not an input to them.

Snapshot/document boundary: the snapshot contains an earlier version of `docs/reviews/G4_AUER_SOURCE_AND_APPLICABILITY_v1.md` (12,223 bytes; SHA-256 `42f0b6aef420a1865428388c633d2cbee672ed789626fcd83f4c00adfe8371d6`). The audit document was updated after snapshot creation (current file: 12,598 bytes; SHA-256 `d5a3068de729d099ea8f4335424c675c2d27a653be9b55a9bf7d279ee7ba5322`) to include the Rauh & Auer (2011) residual-inclusion finding and the limits on access to its cited proof sources. The 2011 paper PDF itself was already a hashed snapshot member. The later audit-text revision was not an input to the executed checks; the source snapshot and run-integrity results remain unchanged and internally valid.

## 3. Source audit

### Paper and solver source

The primary paper is Auer, Kiel and Rauh, “A Verified Method for Solving Piecewise Smooth Initial Value Problems,” *International Journal of Applied Mathematics and Computer Science* 23(4), 2013, pp. 731–747, DOI `10.2478/amcs-2013-0055`. The journal-repository PDF is retained at `research/third_party/auer2013/auer-kiel-rauh-2013.pdf` (531,313 bytes; SHA-256 `d6310c8fd32280addda3f50e3367f9923940641d39de0e70a0932869a2d0ead2`).

The pinned VALENCIA-IVP repository claim was independently verified in the preflight: revision `d1a09ceb3f68deb40357bdc89944b28997e9fb30`, archive blob `af0c6bd1bd5ac10bbdf0fc71b1d6da125f60f9db`, and extracted `ValEncIA-basic.zip` SHA-256 `1e0adfdec371a6ad74348a175b107c82640fb7129891bcca7f53db0c88f1986a`. The seed is `ValEncIA-IVP_0.92_2e.cpp`, a simplified smooth double-pendulum core from 2007. It does not include the 2013 `pwFunc`/piecewise derivative extension; the 2013 article explicitly says that it added a C++ class implementing that derivative definition.

The additional primary solver paper by Rauh and Auer, “Verified Simulation of ODEs and DAEs in ValEncIA-IVP,” *Reliable Computing* 15 (2011), pp. 370–381, was retrieved from the journal archive. Its PDF is retained at `research/third_party/auer2013/references/rauh-auer-2011-valencia.pdf` (640,240 bytes; SHA-256 `1405b54eaa25c5d3874af74ac71087364f3a84ddada675c336e378779e902265`). Section 2, Algorithm 1, Eqs. (3)–(6), pp. 371–372 specifies the residual iteration

`Rdot^(k+1)(t) ⊇ -xdot_app(t) + f(x_app(t)+R^k(t),t)`

and requires `Rdot^(k+1)(t) ⊆ Rdot^k(t)` over the full step before treating the residual as verified. The paper bounds the time-varying error by an outward integral/range enclosure. It sends the detailed derivation/proofs to its references [2] and [8]; full text for those proof sources was not obtained here. The 2013 method adds the piecewise generalized derivative to this smooth solver core; neither component alone is a DDWMR tube proof.

The equation/code mapping and access limits are in `docs/reviews/G4_AUER_SOURCE_AND_APPLICABILITY_v1.md`.

### Dependencies and use terms

- VALENCIA-IVP README: private and academic use with citation; use in commercial products requires written permission.
- Pinned seed README: PROFIL/BIAS 2.0.2 and FADBAD++ 1.4 used in development; PROFIL/BIAS 2.0.4 tested and required for its GCC 4.1 note.
- Official TUHH PROFIL/BIAS source retrieved: 2.0.8, 210,788 bytes, SHA-256 `1706e684166360d60f33b4c9301cfe48a6153fc0c624f2087efa9bc94aa07c20`; the extracted `COPYING` is GPL v2. It is newer than the seed’s named versions. The source lists a Windows 32-bit GCC target as “under development”; its x86-64 profile targets Linux ELF and documents a glibc/libm rounding-mode caveat.
- Official FADBAD++ 1.4 source retrieved over HTTPS: ZIP SHA-256 `e1b5c35178dbfbc52cd623071695d0932e7c14daae76b2c202b1b2032932da9c`. Its official page/COPYRIGHT allows non-commercial use and bars commercial-package use without prior written permission. The 2011 VALENCIA paper identifies PROFIL/BIAS 2.0.6 and FADBAD++ 2.1; the later 0.92_4 examples also request FADBAD++ 2.1 and GSL 1.11+.

The dependency archives and extracted sources are kept locally under `external/valencia-basic/dependencies/`. No installation script was run and no global compiler, PATH, Git, or MATLAB configuration was changed. The project’s academic use is the current stated scope; no redistribution or commercial-use permission is inferred.

## 4. Implementation and targeted checks

New code under `validation/baselines/auer2013/` implements:

- exact interval value and derivative enclosures for `clip(q,-1,1)`;
- an interval first-order AD value/Jacobian wrapper that propagates the clip branch derivative;
- a DDWMR RHS adapter with nine physical states and twelve fixed labels (`dot(label)=0`), using the shared `validation.g2.rational` arithmetic and `validation.g2.model` parameter-image checks;
- a scalar reproduction of the article’s §4.1 Eqs. (34)–(35) discontinuity illustration.

For interval `I`, the clip derivative is `{0}` on a strict saturated branch, `{1}` on a strict linear branch, and `[0,1]` when touching or crossing either threshold (including an interval spanning both). Its secant inclusion is checked directly. This is the continuous two-corner specialization of the Auer branch derivative; it adds no smoothing and no jump term. A jump term is zero for this continuous clip law.

The targeted run produced `20/20` passing checks, status `PASS_FOR_CLIP_EXTENSION_AND_SCALAR_REFERENCE_ONLY`:

- strict branches, exact values at both clip corners, intervals touching/crossing either threshold and both thresholds;
- 212 ordered exact-rational secant pairs;
- an interval-Jacobian inclusion for a multivariate affine input;
- exact rational interval arithmetic;
- nine-state plus twelve fixed-label shape and zero label derivatives;
- rejection of a denominator range containing zero, malformed state dimension and reversed interval;
- round-trip of a clip mean-value evidence record and rejection after tampering;
- checks explicitly marked as not proving a Picard inclusion or ODE tube.

The check file is `results/validation/g4/auer2013/clip_preflight_checks_v1.json` (SHA-256 `4042eb4d517ba3640dbc9ccf214f4059c6d4e1adf00d7d220a8c0a3f3dce7ffc`). These are development checks from this execution, not independent soundness review.

### Reference reproduction

The exact scalar illustration in §4.1, Eqs. (34)–(35), p. 741 was reproduced:

- branch-range closure on `[-1,2]`: `[-1,6]`;
- the ordinary branch derivative hull `[1,2]` gives the paper’s mean-value enclosure `[-3/2,9/2]`, which misses 6;
- the jump-corrected Eq. (35) derivative enclosure is `[1,6]`; the resulting `[-7/2,29/2]` mean-value enclosure contains `[-1,6]`.

Machine-readable record: `results/validation/g4/auer2013/reference_eq34_reproduction_v1.json` (SHA-256 `5524eb15fb624ae5c65e8acafb61f0e51abf05e2db69f015556328e73e99fd85`). This is the published scalar formula illustration, not the paper’s §5 simulation and not a DDWMR trajectory.

The §5 friction/hysteresis experiment remains unreproduced. Table 2 prints `F_s=[0.15,0.03] N` with reversed endpoints. The article provides plots rather than exact numeric enclosures. No authoritative correction or exact output table was found, and no value was substituted.

## 5. Build disposition and unsatisfied proof work

Environment: Windows 11 x64, MSYS2 UCRT64, Python 3.12.12, GCC 15.2.0 (`x86_64-w64-mingw32`). The pinned seed passed a **syntax-only** C++98 compile using PROFIL/BIAS 2.0.8 source headers and FADBAD++ 1.4, with flags `-O2 -frounding-math -fno-fast-math -ffp-contract=off`. Command output was empty and exit code was 0. This checks parsing/header compatibility only.

No complete executable or interval-library build was attempted: the retrieved PROFIL/BIAS source has no reviewed x86-64 Windows directed-rounding profile. Its Win32 GCC configuration is explicitly under development and the x86-64 configuration is for Linux ELF with a documented rounding caveat. The seed also expects older PROFIL/BIAS versions, and it lacks the 2013 piecewise class. Using the Linux profile on Windows or claiming a round-to-nearest build as validated would not preserve the method’s proof basis. The exact disposition is `BLOCKED_BEFORE_LINK`; no binary hash exists. See `auer_seed_build_attempt.json`, `auer_seed_full_build_disposition_v1.json`, and the empty syntax compiler log.

Still required before a faithful baseline can be reviewed or run:

1. obtain/use a supported interval directed-rounding compiler target and decide historical dependency compatibility;
2. implement the paper’s piecewise derivative extension inside the source-faithful solver path, including its AD mapping;
3. implement the 21-coordinate parameter-augmented DDWMR and validate every positive denominator over the full label image;
4. implement the residual iteration with a checked per-step inclusion/fixed-point condition, complete closed time-step tubes, and endpoint propagation;
5. implement and test the typed common collision/contact checker adapters for both the full VALENCIA tube and R3 center-plus-radius representation;
6. obtain authoritative §5 static-friction data and sufficient exact reference outputs, or explicitly scope reference validation to the scalar example;
7. receive an independent review of source fidelity and soundness.

No finite iteration count, apparent convergence, or floating trajectory can stand in for the inclusion condition. Contact admissibility remains a full-time predicate; do not differentiate its square root at saturation. Failed inclusion, domain coverage or resource caps must return UNKNOWN, never a certificate.

## 6. Matched-protocol preparation

`research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v1.md` defines the same nine-state plant, twelve fixed labels, common voltage, full-time typed segment representation, adapters, common checker target, widths, aggregation, falsification rules and local snapshot plan. It separates method-native work from common-checker work and keeps all native R3 records untouched.

The candidate manifest `results/validation/g4/auer2013/auer_matched_candidate_manifest_v1.json` contains the 1,944 original R2 IDs in the same order, each with a canonical input hash. Its ID-list SHA-256 over LF-joined IDs is `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`. It records every status as `NOT_RUN`, has no R3 status join, and states `comparison_run=false`. Manifest SHA-256: `2af5e7925f1043850e7769224a111c7217f2bebf9510645b002b9947c61ae7eb`.

The profile in the manifest proposes 0.001 s steps (the §5 article reports that reference step), at most 100 steps/query, 10 range splits, 5 recovery attempts, 1,000,000 RHS/Jacobian calls, 15 seconds and 512 MiB/query. It targets binary64 PROFIL/BIAS directed rounding and records solver/checker counters separately. R3 keeps its 16,384-bit, 1,000,000-rational-operation and 15-second caps. Unlike primitive counts are not called equal work. These are proposed settings only; a failed step/inclusion remains UNKNOWN.

The protocol and manifest are prepared for independent review, not locked for execution. The common checker/adapter is specified but not implemented. **Do not run the comparison** until the new baseline’s soundness and source fidelity have been independently reviewed and the user directs the next phase.

## 7. Exact commands and outputs

Snapshot creation from the project root:

```text
python validation/scripts/create_auer_source_snapshot.py
```

Working directory for the following runs:

```text
D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety\results\validation\g4\auer2013\source_snapshot_v1\project
```

Commands executed there:

```text
python -m validation.scripts.generate_auer_candidate_manifest --output ../runs/auer_matched_candidate_manifest_v1.json
python -m validation.baselines.auer2013.verify_preflight --output ../runs/clip_preflight_checks_v1.json --reference-output ../runs/reference_eq34_reproduction_v1.json
g++ -std=gnu++98 -O2 -frounding-math -fno-fast-math -ffp-contract=off -fsyntax-only -I external/valencia-basic/dependencies/Profil-2.0.8/src -I external/valencia-basic/dependencies/Profil-2.0.8/src/Base -I external/valencia-basic/dependencies/Profil-2.0.8/src/BIAS -I external/valencia-basic/dependencies/Profil-2.0.8/src/Packages -I external/valencia-basic/dependencies/fadbad-1.4/FADBAD++ external/valencia-basic/free-source/ValEncIA/ValEncIA-IVP_0.92_2e.cpp
```

The snapshot integrity reports passed for all 324 source members before and after the runs. Run environment and exact output hashes are recorded in `results/validation/g4/auer2013/preflight_run_metadata.json` (SHA-256 `b16a0a2e80d520b37e43742381829fe570521f307eb30b725992aa75e14d11ea`). No executable was produced; `baseline_executable_sha256=null`. The comparison count is explicitly zero.

## 8. Files added or retained

New project files:

- `docs/reviews/G4_AUER_SOURCE_AND_APPLICABILITY_v1.md`
- `docs/reviews/LUNA_TO_CODEX_G4_AUER_PREFLIGHT_FULL_HANDOFF.md`
- `research/theorem_notes/G4_AUER_BASELINE_CONTRACT_v1.md`
- `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v1.md`
- `validation/baselines/auer2013/__init__.py`
- `validation/baselines/auer2013/piecewise.py`
- `validation/baselines/auer2013/reference_eq34.py`
- `validation/baselines/auer2013/rhs.py`
- `validation/baselines/auer2013/verify_preflight.py`
- `validation/scripts/create_auer_source_snapshot.py`
- `validation/scripts/generate_auer_candidate_manifest.py`
- `results/validation/g4/auer2013/` including the manifest, check/reference records, build disposition, run metadata, and `source_snapshot_v1/`.

External/source materials retained locally, all untracked:

- `external/valencia-basic/` contains the pinned VALENCIA source/archive, extracted 0.92_2e source and README, official-source page copies, and the official PROFIL/BIAS 2.0.8 and FADBAD++ 1.4 archives plus extracted dependency sources/terms under `dependencies/`.
- `research/third_party/auer2013/` contains the primary 2013 article, extracted text and rendered pages; its `references/` subfolder contains the 2011 VALENCIA paper PDF and extracted text.

The two initial user-provided untracked files remain present. No R3 artifacts were edited or replaced. No tracked research-context formulation, decision or gate status was changed. A separate canonical-context diff is not proposed because no formulation change is supported by these results.

## 9. Research gate status

**HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED.** The scalar extension checks are method-development evidence only. They do not certify any DDWMR trajectory, obstacle clearance, contact preservation, recursive safety, physical validity or novelty.
