# Auer 2013 source and applicability audit

**Date:** 2026-09-30  
**Disposition:** source candidate verified; complete VALENCIA-IVP reproduction and DDWMR applicability are **PARTIAL / UNVERIFIED**.  
**Research status:** HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED.

## 1. Primary source and software provenance

### Article

E. Auer, M. Kiel and A. Rauh, “A Verified Method for Solving Piecewise Smooth Initial Value Problems,” *International Journal of Applied Mathematics and Computer Science* 23(4), 2013, pp. 731–747, DOI [10.2478/amcs-2013-0055](https://doi.org/10.2478/amcs-2013-0055). The PDF was retrieved on 2026-09-30 from the journal repository at <https://zbc.uz.zgora.pl/repozytorium/Content/78882/download/>. It is retained as `research/third_party/auer2013/auer-kiel-rauh-2013.pdf` (531,313 bytes; SHA-256 `d6310c8fd32280addda3f50e3367f9923940641d39de0e70a0932869a2d0ead2`). Extracted searchable text and rendered pages are retained beside it.

### VALENCIA-IVP seed

The pinned `ValEncIA-IVP/basic` Git revision reported in the preflight is `d1a09ceb3f68deb40357bdc89944b28997e9fb30`; the source archive blob is `af0c6bd1bd5ac10bbdf0fc71b1d6da125f60f9db`. The extracted `ValEncIA-basic.zip` is 1,246,383 bytes and has the reported SHA-256 `1e0adfdec371a6ad74348a175b107c82640fb7129891bcca7f53db0c88f1986a`. The enclosing API download is 1,246,391 bytes, SHA-256 `790b981749bcf7de3348312aeb612f1db198f2c39846a48d7057bb1b7c51c84c`.

The extracted `ValEncIA-IVP_0.92_2e.cpp` is 33,711 bytes, SHA-256 `c00d8cc674f616114b319bc796123a142b0973c0d21418401e43d358e3b63ca4`; its adjacent README is 7,529 bytes, SHA-256 `88cf57f12caa5f67426161c0e0194462918b8670617288e9cf6be5ad2e76207b`. The source is a simplified 2007 core. Searches of the pinned package and the separately retained 0.92_4 examples did not find the 2013 piecewise derivative class. The 2013 article says its run used “a C++ class implementing the derivative definition from Section 4.1.” Therefore the pinned seed is a solver core lead, not the complete article implementation.

### Dependency versions and terms

| Dependency | Directly verified evidence | Version / terms | Applicability |
|---|---|---|---|
| VALENCIA-IVP | Pinned source README | Source use permitted for private and academic purposes with citation; use of software parts in commercial products requires written permission. | Retained locally for academic research. No source redistribution is asserted or performed. |
| PROFIL/BIAS | Seed README; official TUHH download page; extracted official source `NEWS` and `COPYING` | Seed says developed with PROFIL/BIAS 2.0.2 and tested with 2.0.4. The official available source retrieved here is 2.0.8, dated 2009-02-18, SHA-256 `1706e684166360d60f33b4c9301cfe48a6153fc0c624f2087efa9bc94aa07c20`; `COPYING` is GNU GPL version 2. | 2.0.8 is newer than the seed’s documented versions. The source has no preconfigured x86-64 Windows target. It is not a verified drop-in replacement for the historic environment. |
| FADBAD++ | Seed README; official FADBAD page; downloaded source `COPYRIGHT` | Seed’s core says FADBAD++ 1.4. Official site distributes 1.4 and 2.1. The 1.4 ZIP is 45,945 bytes, SHA-256 `e1b5c35178dbfbc52cd623071695d0932e7c14daae76b2c202b1b2032932da9c`. Official terms permit non-commercial use and prohibit commercial-package use without prior written permission. | The 1.4 dependency is available for this academic preflight. It does not supply the missing piecewise derivative class. |
| 2011 VALENCIA-IVP publication | Rauh & Auer (2011), §2 and bibliography, retained primary PDF | The implementation section identifies PROFIL/BIAS and FADBAD++; its bibliography specifies PROFIL/BIAS 2.0.6 and FADBAD++ 2.1. | Confirms that the 2013 solver lineage used a later dependency set than pinned 0.92_2e. It remains a source-level lead, not a local binary build. |
| FADBAD++ in later examples | Separately retained 0.92_4 README | Requests FADBAD++ 2.1 and GSL 1.11 or later. | This is not the pinned 0.92_2e seed configuration and is not used as its substitute. |

Official dependency sources: <https://www.tuhh.de/ti3/software/profil.shtml> and <https://uning.dk/fadbad.html>. The initial `www.fadbad.com` HTTPS request failed certificate validation; the official `uning.dk` HTTPS page and 1.4 archive succeeded. The source archives, retrieved page copies, extracted terms, and hashes are under `external/valencia-basic/dependencies/` and `external/valencia-basic/`. No installation script was run.

## 2. Solver algorithm and equation-to-code crosswalk

| Paper locator | Mathematical obligation | Source or preflight implementation | Adaptation / status |
|---|---|---|---|
| §4.1, Eq. (27) | Represent an ODE RHS as an ordered scalar-operation graph whose leaves include inputs, intermediate values and outputs. | `ValEncIA-IVP_0.92_2e.cpp`, user-defined `state_eq_i` (lines 85–121), `state_eq_mid_i` (123–162) and `state_eq_F_i` (164–225). | The source is a double-pendulum example template. Its state equations are not the DDWMR equations. An equation port remains required. |
| §4.1, Eqs. (28), (31) | Piecewise scalar branch values; interval range encloses every active branch and switch value. | `validation/baselines/auer2013/piecewise.py`: `clip_value`, `clip_interval`. The shared benchmark law is exactly continuous `clip(q,-1,1)`. | Exact monotonic range specialization for clip. No smoothing. General arbitrary `SPW` expression interpreter is not implemented. |
| §4.1, Eqs. (33), (40), Property 2 | Continuous piecewise branch derivative enclosure, including both one-sided values at a corner, and inclusion of every existing derivative. | `piecewise.py`: `clip_derivative_interval`; `DualInterval.clip`. Targeted exact-rational checks cover strict branches, both thresholds, both-corner intervals and a multivariate affine composition. | Clip-specific derivative contract implemented and checked. General multi-breakpoint branch construction remains unimplemented. |
| §4.1, Eqs. (35), (41), Property 3 | For a discontinuity, include jump-over-distance terms that preserve the mean-value enclosure. | `reference_eq34.py` reconstructs the single-switch Eq. (34) illustration and its Eq. (35) correction. | Reference-only scalar reproduction. The general two-switch and arbitrary-branch implementation is not present. The DDWMR clip is continuous and uses no jump term; clip jump is exactly zero. |
| §3.3 and §4.2, Eq. (42) | A full-time validated tube `x̃(t)+R(t)`, not just a floating trajectory or endpoints. | Legacy source has a nonvalidated Euler center and interval error/range objects; §4.2 identifies the target tube. | Full DDWMR tube implementation is not available in this preflight. No continuous-time safety result follows from the derivative module. |
| §4.2, Eq. (43) | Validated residual/error derivative and Picard iteration on each closed time step; interval mean-value Jacobian must enclose the RHS difference. | Legacy source `MVR_d_R_i` (line 658 onward), `d_R_computation` (442 onward), `compute_R` (798 onward). It combines interval RHS and a midpoint/gradient mean-value form, intersects the two enclosures, and integrates `d_R` across steps. | This establishes where the historic core performs the work, not proof of its suitability for this new vector field or modern target. The nonsmooth AD call remains absent. |
| §4.2 fixed-point argument | The interval integral operator maps the chosen compact convex tube domain into itself; continuity/upper semicontinuity and inclusion assumptions hold. | Article §4.2 proof discussion; not encoded in the seed README as an executable contract. | Candidate obligation only. Iteration termination or small apparent width is not a substitute for inclusion. |
| §5, Eqs. (45)–(47), Table 2, Fig. 1 | Reproduce the paper’s friction/hysteresis comparison with complete switching definitions, parameters and reference enclosures. | Article PDF pp. 743–745; Table 2 is rendered in `research/third_party/auer2013/rendered/auer-14.png`. | Not fully reproducible from the accessed article: Table 2 prints `F_s=[0.15,0.03] N` with reversed endpoints; no exact curve/enclosure values are tabulated. No correction is assumed. |

| Rauh & Auer (2011), §2, Algorithms 1–2, Eqs. (3)–(6), pp. 371–372 | Define the functional tube, derivative-residual iteration, verified integral bound and inclusion termination condition. | The primary journal PDF is retained at `research/third_party/auer2013/references/rauh-auer-2011-valencia.pdf` (640,240 bytes; SHA-256 `1405b54eaa25c5d3874af74ac71087364f3a84ddada675c336e378779e902265`). It says `Rdot^(k+1)(t)=-xdot_app(t)+f(xapp(t)+R^k(t),t)`; each iterate must satisfy `Rdot^(k+1)⊆Rdot^k`; and the validated error range uses `R^(k+1)(0)+t·r(R^k)([0,t],[0,t])`. | Closes the basic smooth-core algorithm description and confirms that mere iteration until widths stabilize is insufficient. The article states that derivation/proofs are in references [2] and [8], which were not retrieved here. |

The 2013 article also points to Doetschel et al. (2013) for algorithm details. The 2009 proof paper is identifiable by DOI `10.2478/v10006-009-0032-4`; publisher-page/PDF requests returned an access/challenge response during this preflight. The exact VALENCIA repository source gives a concrete residual iteration, but it is neither the article’s extended piecewise class nor a validated build on this Windows machine. Full proof-source access therefore remains partial.

## 3. Clip derivative and mean-value inclusion

For a scalar interval `I`, the implemented derivative enclosure is `{0}` if `I` lies strictly outside `[-1,1]`; `{1}` if `I` lies strictly inside `(-1,1)`; and `[0,1]` in every remaining case, including intervals that touch either threshold or cross both. This is the active-branch derivative hull from the paper’s continuous construction, specialized to the two clip corners.

For any `a,b∈I`, exact clip monotonicity and piecewise linearity give a secant slope in `[0,1]`; on a strict single branch the slope is exactly its branch derivative. Thus `clip(a)-clip(b) ∈ D(I)(a-b)`. If `a=b`, both sides contain zero. For an affine multivariate argument `q(x)=sᵀx+c`, the scalar secant multiplies `sᵀ(x-x₀)`; distributing it yields the row-wise interval Jacobian product. `DualInterval.clip` applies this rule through smooth interval-AD operations. The checks exercise exact rational points, not an independent ODE proof.

## 4. Build and fidelity outcome

The pinned source requires `Interval.h`, PROFIL/BIAS and FADBAD++. The machine has MSYS2 UCRT64 GCC 15.2.0. The official PROFIL/BIAS 2.0.8 and FADBAD++ 1.4 sources are now present locally, but their versions differ from or do not document the pinned source environment. PROFIL/BIAS 2.0.8 lists a Windows 32-bit GCC port as “under development”; its x86-64 profile is specifically for Linux ELF and the README documents an x86-64/glibc math rounding caveat. No tested x86-64 Windows directed-rounding backend was identified.

The full source-faithful solver build is therefore **BLOCKED** pending a supported directed-rounding toolchain/configuration and a compatibility decision on PROFIL/BIAS 2.0.8 versus historical 2.0.2/2.0.4. A floating or host-round-to-nearest build will not be accepted as a validated baseline. Exact build command and output are retained in the snapshot run log.

## 5. Scope and readiness

Implemented in this preflight:

- exact interval clip value and Eq. (33)/(40) derivative specialization;
- interval first-order AD that propagates that piecewise derivative;
- a 21-coordinate augmented RHS for nine physical states and the twelve execution-fixed labels, with `dot(label)=0` and positive parameter images checked by the shared model validator;
- exact reference reproduction of the scalar discontinuity illustration in §4.1, Eqs. (34)–(35);
- candidate query manifest and a comparison protocol draft.

Not implemented or established:

- full nonsmooth VALENCIA-IVP source port or patch;
- a validated Picard fixed-point/inclusion loop and per-step full-time tube for DDWMR;
- the §5 hysteresis simulation with corrected authoritative data;
- a sound common collision/contact checker adapter or any matched result;
- independent source-fidelity or soundness review.

**Readiness:** `BLOCKED/PARTIAL`. The scalar clip extension and §4.1 reference illustration are ready for independent review as isolated components. The result is not ready to run the 1,944-query comparison.
