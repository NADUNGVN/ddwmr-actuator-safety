# DDWMR G2/G4 validation prototype

This package implements the finite exact-rational **whole-hold fallback** for the authorized W1 research-validation scope. It does not implement an operational controller, a safety filter, G3 recursion, closed-loop simulation, hardware experiments, an exact-kernel refinement, or an external validated-reachability baseline.

## Effective input class

Supported plant data are MASTER v2.1 parameters represented by a finite JSON rational AST: reduced exact constants, declared label variables, addition, subtraction, multiplication and division by a rational interval with a checked strictly positive lower endpoint. Parameter labels form one closed rational box and remain fixed for the complete hold. The selected law is exactly `clip(q,-1,1)` with `L_phi=1`. Initial states are closed rational nine-state boxes in MASTER order; the query has one exact common held voltage, one fixed parameter-label cell, rational `T`, and a static circular obstacle.

Ideal gear witnesses are checked by exact polynomial identities after clearing the validated positive denominators. Rational-map range evaluation, interval matrix arithmetic, predictor propagation and the contact/collision checks may lose arithmetic dependencies. Such losses create a named **outer interval hull**; they do not change the plant to a time-varying parameter model. Arbitrary compact parameter sets, other force laws, Bernstein witnesses, voltage search, and parameter/state subdivision are unsupported.

## Arithmetic and status meanings

Every safety predicate uses `fractions.Fraction` and closed rational intervals. The evaluator uses an interval Taylor polynomial for `exp(A t)` with a finite norm tail, exact interval integrals over `[0,T]`, predictor depth `n=1`, a nonnegative comparison matrix and finite positive-series tail, a full-hold pose box, coordinatewise box-to-circle distance, exact clip bounds, and nonnegative square-root bisection. No floating value decides safety. Display timing is a float and is never used in a safety predicate.

- `CERTIFIED`: the record checker replayed all stored interval inclusions and every full-hold collision/contact lower bound is nonnegative for the complete encoded state/label cells under the one voltage. Review acceptance is still pending.
- `UNKNOWN`: the supported query was inconclusive, a sufficient margin was negative, or a finite resource cap was reached. It does not mean unsafe.
- `INVALID_INPUT`: the query violates this narrower representation contract; this says nothing about physical safety.
- `EXECUTION_FAILURE`: an unexpected implementation failure; it is never converted to a mathematical result.

The pilot uses one unsplit initial cell and one unsplit 12-label parameter cell, one whole-hold interval hull and no-op slab refinement. The hull conservatively encloses all time in `[0,T]`; repeating the same hull on more time slabs would not tighten it. The archived v1 profile used an 8192-bit cap. R2/R3 development profiles use 16384 bits, 1,000,000 rational operations and 15 seconds/query, with 16 exponential terms, degree 18 trigonometric ranges, comparison order 16 and 24 root bisections. These are frozen development settings, not scientifically justified equal-cost method settings.

## Frozen benchmark and pilot

`configs/benchmark_v1.json` encodes the complete proposed synthetic grid: six nonzero-width moving nine-state cells, twelve fixed parameter labels with the reciprocal `J=1/rho` maps and gear witnesses, twelve scenes, three hold durations and nine actions: **1944** original state/scene/horizon/action queries per method/profile.

`configs/dev_pilot_v1.json` and `../results/validation/g2/development_manifest_v1.json` freeze the pilot selection before evaluator outputs: four cells crossing low/high speed with negative/positive yaw; two predeclared scenes with different clearances; all three horizons; all nine actions. This is 216 queries. The manifest lists all 1944 original IDs and marks the other 1728 `NOT_RUN`. The pilot is development data, not held-out data or a locked comparison. No minimum coverage threshold has been set.

## Reproduction (Python 3.12; standard library only)

Run from the repository root:

```powershell
python -m validation.scripts.generate_manifest
python -m validation.verification.verify_manifest
python -m validation.verification.verify_hand_cases
python -m validation.verification.verify_primitives
python -m validation.scripts.run_pilot --output results/validation/g2/dev_pilot_reproduction_v1.jsonl
python -m validation.scripts.verify_records --records results/validation/g2/dev_pilot_reproduction_v1.jsonl --metadata results/validation/g2/dev_pilot_reproduction_v1_run_metadata.json
python -m validation.scripts.summarize_pilot --records results/validation/g2/dev_pilot_reproduction_v1.jsonl
```

For the originally archived run, regenerate its artifact hash ledger with `python -m validation.scripts.hash_results` after the checker and summary have been generated.

The runner refuses to start with a dirty source tree and refuses to overwrite an existing record file unless explicitly requested. Commit the evaluator first so each record binds to an immutable source revision. A separate checker replays the arithmetic proof stages instead of calling the top-level evaluator; it shares the exact rational/interval primitives, model-map checker, and exponential/trigonometric/root primitives, which remain part of the disclosed trusted base. `verify_records` also checks that each selected original ID appears exactly once and that no omitted ID is silently counted.

Actual pilot records, resource/UNKNOWN/failure ledgers, checker output, timing summaries and artifact hashes belong under `../results/validation/g2/`. Regenerating summaries does not rerun the evaluator. An alternate rerun should use a new `--output` path so committed evidence remains intact.

## R3 directed dyadic distance method

R3 adds method ID `G2_COMP_CLIP_WHOLE_HOLD_DYADIC_DISTANCE_N1_R3` while preserving all R2 code paths and artifacts. Before the R3 pilot, commit `docs/LUNA_G2_DISTANCE_ADDENDUM_R3_v1.md`, the implementation and verification code. Then freeze the R3 profile and the conditional remaining-ID list with `validation.scripts.freeze_r3_profile`, commit those files, freeze the content/provenance manifest with `validation.scripts.freeze_r3_manifest`, and commit that manifest before any R3 evaluator query.

The distance method rounds exact nonnegative coordinate gaps down/up to multiples of `2^-24` using metered integer shifts and quotient/remainder division. Exact squaring of the directed bounds gives radicand bounds; rational root bisection encloses the rectangle's minimum distance. The collision lower margin remains `minimum_distance_lower - R_s - E_p`. The serialized minimum-distance upper endpoint does not bound every trajectory distance. The checker reconstructs directed rounding from the original query geometry. All integer shifts, divisions, increments and rational constructions consume the same finite per-query bit and operation budgets; no floating safety arithmetic or cap increase is used.

Pilot reproduction, from the repository root after the freeze commits:

```powershell
python -m validation.verification.verify_bounded_distance_r3
python -m validation.scripts.run_pilot_r3 --phase pilot
python -m validation.scripts.verify_records_r3 --phase pilot
python -m validation.scripts.verify_records --records results/validation/g2/r2/dev_pilot_records_r2_v1.jsonl --metadata results/validation/g2/r2/dev_pilot_run_metadata_r2_v1.json --report results/validation/g2/r3/r2_compatibility_record_check_r3_v1.json --benchmark validation/configs/benchmark_v1.json --pilot validation/configs/dev_pilot_r2_v1.json --manifest results/validation/g2/r2/development_manifest_r2_v1.json
python -m validation.scripts.hash_results_r3 --phase pilot
```

The pilot checker writes a continuation decision. Only if it reports `continuation_allowed: true` and passes all hashes and replays, commit the pilot evidence checkpoint, then run the frozen remaining IDs once:

```powershell
python -m validation.scripts.run_pilot_r3 --phase conditional-full-grid --pilot-checker-report results/validation/g2/r3/dev_pilot_record_check_r3_v1.json
python -m validation.scripts.verify_records_r3 --phase conditional-full-grid
python -m validation.scripts.archive_records_r3 --remove-source-after-verification
python -m validation.scripts.hash_results_r3 --phase full-grid
```

The conditional full-grid JSONL can exceed common Git hosting blob limits. The archive command writes a deterministic gzip copy only after its record count and semantic hash match run metadata, then verifies that decompression has the exact source byte hash. Its archive manifest binds the compressed path to the runner's original logical JSONL path. To replay the full-grid checker again, decompress `conditional_full_grid_records_r3_v1.jsonl.gz` to the logical `.jsonl` path first.

Markdown commitments are SHA-256 of immutable Git blob bytes with revision/path/object ID recorded. The separate specification bundle is semantic JSON over that ledger; JSON profile, manifest and result hashes use `ddwmr-semantic-json-sha256-v2`. Producer/checker revisions and their source-file commitments are stored separately. If the pilot condition fails, do not run the remaining 1728 IDs or tune precision/caps.

## Scientific limits

The grid is synthetic, nonstiff and has no platform parameter provenance. Whole-hold interval hulls can be very conservative. A positive record supports only the encoded reduced-model query after independent audit. A development-pilot coverage fraction does not establish practical usefulness or method superiority. Generic predictor-validation/reachability novelty remains blocked; G2 and G4 remain unverified; G3 is outside scope; overall status remains HOLD.
