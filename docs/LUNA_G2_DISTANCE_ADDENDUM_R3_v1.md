# G2 bounded-distance arithmetic addendum R3 v1

**Status:** implementation specification for the authorized R3 development run; not a MASTER change, theorem acceptance, G2 pass, or physical-platform claim. This addendum is frozen before any R3 evaluator query.

## Scope and method identity

R3 changes only the exact numerical enclosure used for the minimum distance from the existing rational predictor-position rectangle to each static obstacle center. It leaves the state/parameter queries, physical equations, full-hold predictor, pose error `E_p`, obstacle radius, contact check, Taylor settings, and finite resource caps unchanged from R2. R2 records continue to mean exact rational coordinate-gap squaring followed by square-root bisection.

R3 uses method ID `G2_COMP_CLIP_WHOLE_HOLD_DYADIC_DISTANCE_N1_R3` and distance method ID `DIRECTED_DYADIC_EUCLIDEAN_MIN_DISTANCE_V1`. The frozen distance precision is `p=24`. Unknown distance method IDs are rejected. R3 records use a new schema and the new `specification_bundle_sha256` / `input_configuration_bundle_sha256` fields; the historical R2 `specification_sha256` keeps its prior configuration-bundle meaning and is not written to R3 records.

## Exact enclosure

Let `dx,dy >= 0` be the exact rational coordinate gaps from the obstacle center to the complete predictor-position rectangle, and let `d=sqrt(dx^2+dy^2)` be its minimum Euclidean distance. For each coordinate `g`, compute using exact nonnegative integer arithmetic

`g_lower = floor(2^p g)/2^p`, `g_upper = ceil(2^p g)/2^p`.

The implementation shifts the reduced numerator left by `p`, divides by the positive denominator with quotient and remainder, and increments the quotient for the upper endpoint exactly when the remainder is nonzero. All shifts, integer divisions, upward increments, dyadic rational constructions, squares, sums, and root-bisection arithmetic are included in the per-query operation and bit budgets. It performs no floating conversion and does not raise or bypass either cap. A pre-operation estimate or observed integer/rational result over the cap yields a resource-limited `UNKNOWN` with the primitive and stage recorded.

Set `a_lower=gx_lower^2+gy_lower^2` and `a_upper=gx_upper^2+gy_upper^2`. Exact monotonicity gives `a_lower <= d^2 <= a_upper`. The existing validated rational square-root bisection returns brackets `[lo_lower,hi_lower]` for `sqrt(a_lower)` and `[lo_upper,hi_upper]` for `sqrt(a_upper)`. Thus `l=lo_lower <= d <= h=hi_upper`. The collision sufficient lower margin remains `l - R_s - E_p`.

Each coordinate rounding width is at most `2^-p`; by the reverse triangle inequality, coordinate rounding alone loses at most `sqrt(2)*2^-p <= 2^(1-p)` in distance. The witness reports that bound separately from each square-root bracket width. The upper endpoint `h` encloses the rectangle's **minimum distance only**; it is not an upper bound on all trajectory-to-obstacle distances. `E_p` remains the existing full-hold pose-error bound.

## Witness and checking

The proof stores the exact coordinate gaps, both dyadic bounds per coordinate, lower/upper squared-distance radicands, both root brackets, `l`, `h`, the coordinate-rounding loss bound, and the margin. The checker reconstructs coordinate gaps from the query and recomputed predictor rectangle, then independently repeats directed floor/ceiling division, checks exact coordinate inequalities and widths, rebuilds radicands, replays root brackets, and recomputes the margin and status. It does not trust witness endpoints or the reported status. It shares `Budget`, `Fraction` interval arithmetic, model construction, and validated root primitives with the evaluator; these remain in the trusted boundary and are to be named in the return report.

Required arithmetic regressions cover zero gaps, exactly representable and non-dyadic gaps, one/two nonzero coordinates, and zero/positive/negative sufficient margins. Proof mutation checks cover upward movement of the lower distance, downward movement of the upper distance, changed precision, query/voltage binding, margin/status, and malformed directed-rounding witnesses. Existing R2 radius regressions and proof replay remain required.

## Frozen-provenance fields

The specification-content ledger uses SHA-256 over immutable Git blob bytes and records each source revision, repository-relative path, Git blob object ID, and SHA-256 of the blob bytes. The separate specification bundle digest is the canonical semantic-JSON SHA-256 of that ordered ledger. JSON input/profile/manifest files use the existing `ddwmr-semantic-json-sha256-v2` protocol. R3 producer metadata and records distinguish the producer revision from the checker revision and include source-file commitments, exact command/environment, and pre-run worktree state. Historical R2 outputs and their hash interpretation remain unchanged.

This remains one bounded development pilot. A conditional manifest for the original 1,728 unselected IDs is frozen before the 216-query pilot; it may be run once only if every R3 pilot record is non-resource-limited, valid, and replayed as specified by the R3 assignment. No post-result precision/cap tuning is permitted.
