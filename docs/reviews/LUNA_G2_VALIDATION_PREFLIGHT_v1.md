# G2/G4 validation preflight v1

Date: 2026-09-29. Baseline: W1 commit `6956022e93bf7f3d503c9995735cb380162df437`. Branch: `luna/g2-validation-v1`. Working tree was clean before this assignment. Governing plant: MASTER v2.1, unchanged. Scope: exact-rational research validation under W1; no G3, controller, closed-loop or hardware work.

## Finding — equation-to-code audit

| Equation/source | Planned implementation | Units/scaling and inclusion obligation | Status |
|---|---|---|---|
| MASTER §§5–11; G2 candidate (G2.1–G2.5) | `validation/g2/model.py`: six-state `z=(u,r,omega_L,omega_R,i_L,i_R)`, interval matrices `A,B,D,S`, clip force, `Q_F` | Query provides a positive rational diagonal scale `P_s`; benchmark uses the declared one-unit SI reference scales and identity `P_s`. Build `A_tilde=P_s^-1 A P_s`, `B_tilde=P_s^-1 B`, `D_tilde=P_s^-1 D`, `S_tilde=S P_s`; restore internal boxes/radii before pose and contact checks. | READY for the declared clip subclass |
| G2 candidate (G2.6–G2.8); evaluator spec §§3.1–3.2 | `validation/g2/predictor.py`: finite Picard levels `n=0,1`, exact rational interval matrix exponential and whole-hold interval integral, paired predictor-difference residual | All levels start from the same full initial cell and same parameter-label cell. `V` is one exact rational vector, constant through the hold. No oracle trajectory or midpoint initialization. | READY; interval hulls may be wide |
| Evaluator spec §3.1; G2 candidate (G2.9) | `validation/g2/interval.py`: interval Taylor matrix exponential with symmetric norm tail; exact rational sine/cosine Taylor ranges; nonnegative root bisection | Every interval operation uses reduced `Fraction` values with pre-operation bit and operation caps. `Q=0` is exact. Taylor remainders use rational upper bounds; no float affects predicates. | READY for fixed finite profile |
| Evaluator spec §3.2; G2 candidate (G2.8–G2.13) | `validation/g2/predictor.py`: rational upper `Q_F`, `M_bar`, `D_bar`; `N=max(0,M_bar)`; positive forced-series radius plus explicit tail | `N` dominates every `M(theta)` on the entire label cell; negative diagonal entries are replaced by zero. Radius is in scaled coordinates, then restored with `P_s`. | READY; no exact-kernel refinement implemented |
| Evaluator spec §3.3; G2 candidate (G2.14–G2.22) | `validation/g2/safety.py`: whole-hold heading/position interval lift, box-to-circle distance lower bound, clip/contact reserve and one-hold aggregation | Pose and contact computations use physical coordinates. Every initial-state and parameter cell, obstacle and full hold must pass under the same `V`. Root lower bounds are verified by exact squaring. | READY for the finite clip class |
| Evaluator spec §§1, 2, 4 | `validation/g2/records.py`: status schema and independent record replay | `CERTIFIED` only after all collision/contact lower margins are nonnegative and the checker verifies all leaves/obstacles. `UNKNOWN` is inconclusive; `INVALID_INPUT` means the declared encoding contract failed. | Planned before any certificate is enabled |
| Benchmark spec §§2–7 | `validation/configs/benchmark_v1.json`, deterministic generator and frozen development manifest | Preserve 12 label coordinates, reciprocal `J=1/rho` correlation, six nine-dimensional nonzero-width state cells, all 12 scenes, three horizons and nine original actions. Each result retains its original query ID and denominator. | Development-only pilot; not a locked comparison |

## Finding — effective class and finite profile

The implementation will support only exact rational constants, label variables, addition, subtraction, multiplication and division by expressions whose rational interval image is provably strictly positive or strictly negative. Expressions are parsed from a closed JSON AST; Python `eval` is prohibited. Polynomial/rational identities for the declared ideal gear witness are checked exactly after clearing validated denominators. Sign witnesses use direct outward rational interval evaluation; Bernstein certificates, arbitrary compact sets, arbitrary `phi`, and unbounded refinement are not implemented.

The law is exactly `clip(q,-1,1)` with `L_phi=1`. Every query uses a closed rational nine-state box, one finite rational parameter-label box, a fixed common rational voltage, static circular obstacles, positive rational `T,V_max,R_s`, identity or positive diagonal rational scaling, and a finite resource profile. The pilot profile and complete query-ID selection must be committed and hashed before evaluation. The evaluator will use predictor depth `n=1`, whole-hold predictor hulls, no parameter/state splitting, one full-hold verification slab, bounded Taylor degrees, bounded root bisections, a rational bit cap, and an operation cap. Verification slabs would be a no-op for this whole-hold hull, so no refinement benefit will be attributed to them.

## Finding — blockers and scope limits

### W1-PF-01 — interval-hull predictor dependency loss

**Evidence:** Predictor integrands are enclosed over the complete `[0,T]` range; interval matrix products discard shared time, state and label dependencies. Repeating that same hull on smaller time panels does not localize it.

**Consequence:** Valid inclusions may return `UNKNOWN` on easy cases. Splitting and exact-kernel refinements are outside the frozen pilot.

**Status:** UNVERIFIED for usefulness; not a soundness blocker for the declared outward hull operations.

**Required action:** Keep the loss visible in margins and width summaries; do not claim subdivision or a structured-kernel advantage.

### W1-PF-02 — generic rational-map/effective-set coverage

**Evidence:** MASTER permits abstract compact correlated parameter sets and arbitrary known Lipschitz laws; the evaluator spec requires effective finite encodings.

**Consequence:** The code result covers only represented `G2-COMP-clip` queries. Failed positivity, unsupported AST nodes or a failed gear identity are `INVALID_INPUT`; operation/bit exhaustion on supported data is `UNKNOWN`.

**Status:** UNVERIFIED outside the explicitly encoded subclass.

**Required action:** Do not generalize results to arbitrary `Theta` or `phi`.

### W1-PF-03 — benchmark lock, acceptance threshold and matched baseline

**Evidence:** The benchmark draft leaves work-cap alignment, usefulness thresholds and applicable external baseline open. The G4 comparison draft explicitly says a tool name alone is not a matched adapter.

**Consequence:** The selected pilot is development data only. No coverage threshold, method superiority or G4 conclusion is available. A validated external baseline is not part of this implementation.

**Status:** OPEN / NOT_IMPLEMENTED.

**Required action:** Report original denominators, queried IDs, `NOT_RUN`, `UNKNOWN`, invalid inputs and execution failures separately; do not relabel the pilot as locked or full-grid evidence.

### W1-PF-04 — status-label trust

**Evidence:** A self-reported `CERTIFIED` string does not prove its interval inclusions or complete-cell coverage.

**Consequence:** The evaluator may emit only provisional records until a separate checker replays the serialized arithmetic and universal-coverage obligations.

**Status:** OPEN before code output is treated as a certificate.

**Required action:** Implement the checker and run it on every exported positive record; disclose shared rational/interval primitives.

## Finding — independent work-package disposition

| Work package | Finding / evidence | Consequence | Status | Required action |
|---|---|---|---|---|
| L1 Preflight | Equation and unit mapping above; current effective subclass and exclusions declared | Soundness claims stay limited to the implemented finite contract | COMPLETE as a preflight document | Revisit if code departs from these equations |
| L2 Exact fallback/checker | No code exists at baseline; checker must precede certificate use | No `CERTIFIED` output is accepted until replay succeeds | IN PROGRESS | Implement, then audit exact inclusion checks |
| L3 Verification | A/B/C are separate accepted hand proofs, not evaluator outputs | Fixture reproduction cannot be hard-coded into generic evaluator | IN PROGRESS | Add independent hand-arithmetic fixtures and adversarial input/resource checks |
| L4 Benchmark | Draft grid is 1944 queries per method/profile; pilot needs prior hash and exact IDs | Pilot cannot close usefulness or be called held-out | IN PROGRESS | Freeze manifest before any evaluation |
| L5 Matched comparison | Generic overlap is established; compatible external baseline is not selected/reproduced | No external superiority claim | NOT_IMPLEMENTED | Preserve exact source/configuration gap in handoff |
| L6 Reproduction | Python 3.12.12 is available; implementation uses standard library only | Environment can be recorded without new packages | IN PROGRESS | Record commands, hashes and measured output after freezing inputs |

No plant equations, assumptions, version, gate status or archived review are modified by this audit.
