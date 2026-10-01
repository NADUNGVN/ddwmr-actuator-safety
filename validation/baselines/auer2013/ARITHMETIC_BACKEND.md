# Auer reconstruction arithmetic backend contract

**Backend ID:** `DDWMR_EXACT_RATIONAL_TAYLOR_INTERVAL_V1`  
**Status:** selected and pinned as a candidate backend; independent soundness review pending. No Auer IVP was run.  
**Machine-readable companion:** `ARITHMETIC_BACKEND_MANIFEST_v1.json`.

## Arithmetic model

The intended Auer reconstruction uses Python `fractions.Fraction` intervals with arbitrary-size integers, the project's exact rational `Interval` operations, and explicit `Budget` limits. Finite rational endpoints are represented exactly; `+`, `-`, `*`, `/`, integer powers, comparisons, and JSON numerator/denominator serialization perform no binary floating-point rounding. The resource budget may stop an operation before a result is accepted; a cap is a resource `UNKNOWN`, never a rounded result. Division is rejected if its interval denominator contains zero. NaN, signed infinity, and non-finite interval endpoints are not in the proof domain.

The method uses no system `exp`, `sin`, `cos`, or `sqrt` library. `validation/g2/interval.py` encloses sine and cosine with exact-rational Taylor polynomials and a Lagrange remainder using `|sin^(n)|, |cos^(n)| ≤ 1`; it does not use argument reduction or extrema detection. The range is safely intersected with `[-1,1]`. Large arguments can make this enclosure too wide and cause `UNKNOWN`; they do not authorize an unverified fallback. The interval matrix exponential is bounded by a Taylor polynomial plus a rational remainder using `e^q ≤ 3^ceil(q)`. Square roots used by the common predicate checker are bracketed by rational bisection and exact square comparisons. Every endpoint is serialized as a reduced signed numerator and positive denominator, so export is exact and round-trip preserving.

Underflow, subnormals, signed zero, and hardware overflow do not arise in the exact-rational proof values. Decimal or binary64 inputs must be parsed into an explicitly specified exact rational image before entering this backend. A malformed rational, zero-containing divisor, negative square-root radicand, unsupported transcendental, or invalid domain fails closed. Wall-clock observation is not part of a numerical premise.

## Pinning and executable availability

This is a source-level exact-arithmetic backend, not MPFR/MPFI and not the legacy PROFIL/BIAS build. The companion manifest binds the actual Python interpreter path/version/hash, the rational and transcendental source hashes, and the method source hashes. Python does not execute a project-specific compile or link step; native compiler/link flags are therefore `NOT_APPLICABLE`. No Auer executable or compiled binary exists. The retained PROFIL/BIAS 2.0.8 build and legacy VALENCIA binary are excluded from proof output: its x86-64 BIAS sine/cosine wrapper depends on glibc/libm error bounds that have not been established for all inputs. The 19 finite probes and dependency smoke checks do not close that gap.

The source functions covered by this contract are `Budget` and `Interval` in `validation/g2/rational.py`; `interval_sine`, `interval_cosine`, `interval_matrix_exponential`, and `sqrt_lower` in `validation/g2/interval.py`; `clip_derivative_interval`, `DualInterval`, and clip range code in `validation/baselines/auer2013/piecewise.py`; and the 21-coordinate RHS/Jacobian composition in `validation/baselines/auer2013/rhs.py`. These functions are shared with the prior R3 evaluator. Their presence does not mean the absent Auer residual solver or its proof checker is covered.

## Arithmetic operation audit

| Operation | Contract / implementation | Proof-use status |
|---|---|---|
| `+`, `-`, `*`, `/` | Exact rational endpoint arithmetic; interval hull operations; division requires denominator exclusion of zero. | Exact at the arithmetic layer; solver premises not implemented. |
| `sqrt` | `sqrt_lower` returns a rational lower/upper bracket checked by exact square comparisons and fixed bisection count. | Available for common predicates, not the ODE solver. |
| `exp` | No generic host `exp`. Matrix exponential enclosure is a finite Taylor sum with the rational `3^ceil(q)` remainder majorant. | Available in shared interval module; independent review pending. |
| `sin`, `cos` | Exact-rational Taylor polynomial, Lagrange remainder, and safe intersection with `[-1,1]`; no libm, range reduction, or extrema search. | Available for interval RHS/Jacobian evaluation; interval accuracy may deteriorate for wide/large angle boxes. |
| Parsing / serialization | Strict rational pairs; exact signed numerator and positive denominator; no decimal output used as proof input. | Available in interval modules; Auer native record/parser not implemented. |
| Overflow / underflow / NaN / infinity | Not representable as a proof interval endpoint. Resource growth is bounded by the frozen rational bit/operation profile; invalid values fail closed. | Profile is frozen, but no Auer process is enabled because memory/time enforcement and solver integration are not implemented. |

The profile, source hashes, runtime identity, and any later audit findings must be checked before enabling a proof-producing run. No successful build, finite probe, or process exit is treated as proof of an ODE inclusion.
