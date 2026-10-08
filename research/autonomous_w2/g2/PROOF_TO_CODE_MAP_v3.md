Session: DDWMR | LUNA-G2-SCOPE

# W2 G2 candidate v3 — fixed-grid arithmetic correction

**Status:** versioned development candidate only. The frozen model, one-hold task, parameter family, actions and threshold are unchanged from v1/v2. The v3 change replaces uncontrolled exact-rational endpoint growth with exact outward rounding after every interval primitive; it does not change the enclosure theorem or claim a tighter reachable set.

## Inclusion claim and task quantifiers

For each one of the frozen voltages, if every exact interval obligation is replayed, the result encloses every trajectory from the complete positive-width nine-state box, for every one execution-fixed label in the complete positive-width twelve-label image, under that same voltage through the full two-second hold. The supported traction law is `clip(s,-1,1)` and is usable only after every slab's interval slip lies strictly inside `(-1,1)` for each side. The fixed physical constants, parameter maps, static circle, 16 contiguous slabs, progress measure and independent `7/20 m` threshold remain exactly as bound by `task_protocol_v1.json` and `profile_v3.json`.

The exact affine augmented model is unchanged from the v2 map. For each fixed parameter label and constant voltage, `z=(u,r,omega_L,omega_R,i_L,i_R)` follows `z'=A(vartheta)z+B(vartheta)V`; `y=(z,1)` follows `y'=A_aug(vartheta,V)y`. The signed matrix keeps terminal-voltage/current/back-EMF/wheel/contact/body/yaw coupling. Interval matrix powers relax correlations, but the label-image hash and the same interval label image are carried across every slab; this only enlarges the set.

## Directed dyadic interval lemma

Let `D=2^P` where frozen profile `P=96`. Define

\[
\operatorname{down}_P(q)=\lfloor Dq\rfloor/D,\qquad
\operatorname{up}_P(q)=\lceil Dq\rceil/D.
\]

Each interval construction maps raw endpoints `a<=b` to

\[
[a,b]\subseteq[\operatorname{down}_P(a),\operatorname{up}_P(b)],
\]

because `floor(x)<=x<=ceil(x)` for every exact rational `x`. The interval addition and four-corner multiplication first compute exact rational extrema, then apply this constructor; reciprocal rejects any denominator containing zero and uses the exact endpoint images before outward construction. By induction on the expression tree, every primitive result contains the exact image of its input boxes. Each constructor expands each side by less than one grid unit; the total added width per construction is less than `2/D`. There is no floating-point operation in this arithmetic path.

The tail term also remains exact rational: the computed matrix infinity-norm upper bound is multiplied by the dyadic slab length, then the frozen Taylor remainder formula is evaluated with `Fraction` and checked against the declared bit cap. A pre-run inequality verifies the worst profile-scale denominator growth is below `rational_bit_cap`; an actual cap breach still returns `RESOURCE_UNKNOWN`. The series tail is a symmetric outward radius. No discarded roundoff term exists because each rounded interval is already outward.

For degree `N=20`, `h=1/8` and `q=h*||A_aug||_inf`, the Taylor tail is

\[
\|R_{21}(\tau)y\|_\infty\le
\|y\|_\infty\frac{q^{21}}{21!}\frac{1}{1-q/22},\quad 0\le\tau\le h,
\]

subject to the exact replayed guard `q/22<1`. Partial slabs bound every `tau^n` by `[0,h^n]`; endpoint slabs use `h^n`. The next slab starts from the prior endpoint enclosure. One label image and one voltage stay fixed for the full chain.

## Scientific obligations and code map

| Obligation | Producer | Independent proof replay |
|---|---|---|
| Protocol, state/label widths, voltage actions, fixed input semantics | `producer_v3.py::parse_protocol` | `checker_v3.py::_read_and_validate` |
| Exact outward endpoint quantization, interval addition/multiplication/reciprocal | `rational_interval_v3.py::I` | same disclosed arithmetic trust root, exercised by `fixed_grid_arithmetic_fixtures_v3.py` |
| Signed DDWMR affine matrix | `producer_v3.py::build_augmented_matrix` | rederived in `checker_v3.py::_assemble` |
| Taylor partial range, endpoint and tail | `producer_v3.py::exp_range` | separate loop/formula in `checker_v3.py::_flow` |
| Clip interior and first-exit inclusion | `producer_v3.py::evaluate` | recomputed for every slab in `checker_v3.py::_reconstruct` |
| Fixed-label/voltage semantics, slab coverage and endpoint carry | producer row + `run_stage_v3.py` | `checker_v3.py::audit`, mutation replay |
| Full-slab contact reserve and body demand | `producer_v3.py::evaluate` | independently recalculated in `checker_v3.py::_reconstruct` |
| Pose, full-slab static-circle distance and progress | `producer_v3.py::evaluate` | independently recalculated in `checker_v3.py::_reconstruct` |
| Source/input binding, one launch, no retries, resource capture | `freeze_development_v3.py`, `run_stage_v3.py`, Windows job supervisor | immutable bindings, receipts, captured worker/replay outputs |

Producer and checker do not import each other's model, propagation or margin logic. They share `Fraction` and the exact outward interval primitive; this common arithmetic root is a disclosed finite-validation dependency, not independent arithmetic validation. The checker replays every inequality and slab rather than trusting the producer's status field.

## Applicability and limitations

The arithmetic correction controls rational denominator growth. It does not cure interval dependency, broad labels, clip-branch failure, pose-box overlap, contact reserve loss, a failed progress target, or prior-art overlap. A `CERTIFIED` row can only support the stipulated reduced model and frozen synthetic family. `UNKNOWN` does not prove collision, contact loss, physical unsafety or task impossibility. No physical-platform provenance, recursive G3 result, G4 novelty result or gate pass is claimed.
