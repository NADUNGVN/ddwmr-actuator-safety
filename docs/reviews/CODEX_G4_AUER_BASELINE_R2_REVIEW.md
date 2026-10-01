# Codex review — G4 Auer baseline R2

**Date:** 2026-09-30  
**Reviewed handoff:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_BASELINE_R2_FULL_HANDOFF.md`  
**Branch / HEAD:** `luna/g2-validation-v1` / `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`  
**Disposition:** **ACCEPT as a traceable BLOCKED/PARTIAL preparation record. Do not accept it as an Auer validated-IVP baseline.**

MASTER v2.1 remains authoritative. **HOLD; G1 PASS in restricted reduced-model scope; G2/G3/G4 UNVERIFIED; physical-platform correspondence UNVERIFIED.** No commit or push was made during this review.

## 1. Artifact and comparison status

**Finding.** The R2 package and the zero-evaluation claim are internally consistent.

**Evidence.** I independently recomputed sizes and SHA-256 for all **681/681** members listed in `source_snapshot_v2/snapshot_manifest.json`; there were no mismatches. The manifest digest is `c78523df6616dc46c062841169a7e584fcb622d64acfa4cde1ba4b53c2cb6af1` and matches its sidecar. The v2 candidate manifest hash is `77024610eab603a1ee2085feb5b6e7da0719ddd0641efa3804df6190492e59ad`. Its query rows are identical to v1: **1,944 unique IDs**, in both benchmark and frozen R2 order; all are `NOT_RUN`, with `comparison_run=false` and no R3 join. The v2 profile metadata raises the proposed step cap to 1,000 and documents the unapproved WSL arithmetic target.

**Consequence / status.** **VALID traceability for preparation.** There is no matched baseline observation to compare with R3.

## 2. Build, arithmetic, and smooth reference

**Finding.** The WSL2 work establishes that the legacy smooth seed can be linked and executed against a local PROFIL/BIAS 2.0.8 build. It does not establish validated arithmetic or the 2013 method.

**Evidence.** `make check` reports 2/2 dependency checks, and the separate probe covers 19 finite arithmetic/trigonometric cases. The retained PROFIL/BIAS README explicitly warns of the x86-64 glibc/libm rounding issue. Neither those finite probes nor compiler flags provide an all-input outward sine/cosine contract. The seed was written for older PROFIL/BIAS versions and lacks the 2013 piecewise derivative class. Its smooth pendulum run printed `Condition not fulfilled: bounds are getting larger at time-step! 3062` before the requested 3,751 steps, although the process exited 0. Future automation must classify this by the solver's own completion condition, not only by process exit code.

**Consequence / status.** **Build feasibility only; arithmetic soundness and source fidelity UNVERIFIED.** This partial legacy example is not an Auer §5 or DDWMR trajectory reproduction.

## 3. Common tube layer

**Finding.** The supplied-hull predicate layer is a useful interface scaffold. By source inspection, its position-box distance lower bound and clipped-slip lateral-reserve lower bound are conservative when given a genuine full-time outer state hull. It deliberately cannot certify an ODE trajectory.

**Evidence.** `TubeSegment` uses a total state hull, exact closed time bounds, full label intervals, endpoints contained in the slab, and a recorded radius expansion count of zero or one. The checker consumes the total hull once. Its result always says `certificate_emitted=false` and `ode_tube_proof_replayed=false`. The stored nine synthetic fixture groups exercise a positive supplied hull, an UNKNOWN hull despite clear endpoint boxes, coverage/label rejection, exact float representation conversion and a tampered-hull replay. The Auer adapter accepts a 64-character `proof_record_sha256` for provenance but does not open, hash or replay any native proof. The fixture module invokes the Auer adapter with a synthetic record, but **does not invoke the R3 adapter on an actual R3 proof record**.

The common predicate record binds benchmark, scene, horizon and initial box, but has no held-voltage/action binding of its own. This is acceptable for a predicate on a supplied hull. Before composition into a certificate, the upstream proof and every segment must be cryptographically and semantically bound to the same query ID, held voltage, initial box, parameter image, horizon and source snapshot. An arbitrary digest string is not such a binding.

The chain currently requires exactly equal adjacent endpoint intervals. That is a sound sufficient interface rule, though a valid solver using outward reboxing might need a documented containment rule instead. Any relaxation must retain a verified propagation inclusion; interval overlap alone is insufficient.

**Consequence / status.** **ACCEPT only as an interface and supplied-hull checker draft.** Actual R3 adapter replay, Auer inclusion replay, proof-to-query binding and a full-time solver remain open. The nine fixtures cannot be counted as safety certificates or matched queries.

## 4. Missing scientific comparator

**Finding.** The decisive task remains almost entirely unimplemented: a source-faithful piecewise VALENCIA residual inclusion with a DDWMR full-step tube and endpoint. The R2 handoff accurately reports this.

**Evidence.** The exact-rational Python clip/RHS components do not feed the linked C++ solver. There is no 21-coordinate solver port, checked residual/Picard inclusion, full-time DDWMR segment proof, endpoint propagation or independent replay checker. The scalar §4.1 arithmetic check is not an IVP reference run; §5 still lacks unambiguous source data. The v2 protocol is a candidate, not a frozen executable comparison profile.

**Consequence / status.** **G4 comparison UNVERIFIED.** Failed reproduction, a partial smooth run, or a proposed 1,000-step cap cannot be interpreted as R3 superiority. Do not run the 1,944-query batch or promote G2/G4.

## 5. Scientific next decision

Repeated setup work has reduced the environment uncertainty but has not produced the published baseline. Before another substantial Auer port, obtain an independent scientific choice between:

1. a source-faithful Auer reconstruction with a defensible all-input arithmetic backend, explicit proof obligations, a replayed full-time step and a small independent IVP reference; or
2. a different, actually available validated piecewise-smooth/parametric IVP comparator under matched assumptions, with the Auer reproduction limitation disclosed.

The review request `docs/GPT_G4_AUER_R2_STRATEGY_REVIEW_REQUEST.md` asks GPT to make this decision in one returned Markdown file. During that review, the R3 adapter can be checked against a real historical proof record and the future proof-to-query binding can be specified without implying a baseline result. No plant amendment is supported.

**Final disposition:** **R2 partial handoff ACCEPTED in its declared scope; Auer baseline BLOCKED/PARTIAL; matched comparison NOT RUN; project HOLD.**
