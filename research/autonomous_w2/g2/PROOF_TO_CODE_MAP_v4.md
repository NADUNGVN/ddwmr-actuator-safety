Session: DDWMR | LUNA-G2-SCOPE

# W2 G2 candidate v4 — nested proof-key correction

**State:** candidate for bounded development; v3's three failed launches remain preserved and counted. V4 changes only the producer's post-slab safety-status aggregation paths and the versioned source/profile bindings. Task, threshold, model, signed matrix, fixed-grid arithmetic, Taylor degree, slab partition and contact/collision/progress formulas remain as in `PROOF_TO_CODE_MAP_v3.md`.

## Exact correction

Each v4 slab record stores collision under:

```text
slab["collision"]["margin_lower_m"]
```

and contact under:

```text
slab["contact"]["margin_lower_N"]
```

The v3 producer constructed those nested records and its independent checker already consumed those paths, but `producer_v3.py::_certificate_status` incorrectly requested flat `collision_margin_lower` and `contact_margin_lower` keys. V4's `_certificate_status` reads the nested fields and emits the same reasons as the checker. It does not alter or bypass either inequality:

\[
\text{collision certified only if } d_{\mathrm{lower}}-R_s\ge0\text{ on every slab},
\qquad
\text{contact certified only if } a_{L,\mathrm{lower}}+a_{R,\mathrm{lower}}-|mur|_{\mathrm{upper}}\ge0\text{ on every slab}.
\]

The selector still requires the recomputed full-hold safety status and progress lower bound at least `7/20 m`. A negative margin returns `UNKNOWN`; a margin is never clipped to zero.

## Version-bound verification map

| Obligation | Producer | Independent replay |
|---|---|---|
| Fixed-grid outward arithmetic | shared `rational_interval_v3.py` | same disclosed scalar arithmetic trust root, analytic rational fixtures |
| Signed model, Taylor tail, slab/endpoint chaining, pose and margins | `producer_v4.py` | separately reconstructed by `checker_v4.py` |
| Nested status aggregation | `producer_v4.py::_certificate_status` | status independently rebuilt in `checker_v4.py::_reconstruct` from its own nested margin calculations |
| Producer output, voltage/labels/protocol, source hashes, slab completeness | `worker_v4.py`, frozen v4 binding, `run_stage_v4.py` | `checker_v4.py::audit` recomputes proof fields; mutation replay rejects changed sources/input, omitted slab, label reset and altered inequality |

Before freezing v4, `status_aggregation_fixtures_v4.py` exercises: a fully nonnegative two-slab case, a negative collision margin, a negative contact margin, and a failed clip branch. It asserts exact reason lists and expected Boolean status. The fixture contains no benchmark row. This is a local regression check, not a substitute for the three source-bound row replays.

Producer/checker still share `Fraction` and the fixed-grid primitive; they do not share model, Taylor, pose, status or margin functions. Source independence is limited to those separate reconstructions and is not a claim of independent arithmetic implementation. All mathematical scope and limitations stated in v3 continue unchanged.
