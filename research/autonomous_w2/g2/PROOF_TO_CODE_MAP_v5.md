Session: DDWMR | LUNA-G2-SCOPE

# W2 G2 v5 — finer time-local VOF partition

**State:** bounded development candidate only. It retains the v4 producer/checker, fixed-grid arithmetic, signed model, task, initial box, parameter image, obstacle, actions and `7/20 m` threshold. The only numerical-profile change is from 16 slabs of `1/8 s` to 256 slabs of `1/128 s`.

## Reason for this refinement

V4 independently replayed all three proof rows but returned `UNKNOWN` for each. Its local interval state widths grew rapidly after `1.5 s`, and the strict clip-interior guard failed in the last two slabs. A separate exact-rational point fixture propagates the allowed center point with all labels equal to one and proves the symmetric slip remains strictly inside the clip interval for all three held voltages over the entire two-second hold. This shows that V4's branch failure is an enclosure overestimate for at least one allowed point; it does not establish the full positive-width cell or its safety.

The v5 hypothesis is that reducing each whole-slab time range by a factor of 16 will reduce matrix-Taylor interval wrapping and endpoint-box growth enough to preserve the same useful signed/coupled enclosure on the full cell. This is falsified if v5 again loses the branch, contact, collision or progress predicates, or exhausts the fixed per-worker caps. The threshold and geometry remain unchanged.

## Full-hold inclusion statement

Let the initial state (x_0) range over the complete closed nine-dimensional box in `task_protocol_v1.json`. Let one execution-fixed label vector ϑ range over the complete twelve-coordinate image `9999/10000 <= ϑ_k <= 10001/10000`; its physical derived parameters are the declared rational maps in the protocol. Fix one voltage action (V) for the entire (T=2) s hold. No label or voltage is resampled at a slab boundary.

For each fixed label and voltage, on a slab whose slip enclosure proves β_L,β_R < 1, the internal six-state dynamics equal the affine signed system (z'=A(ϑ,V)z+b(ϑ,V)). With (y=(z,1)), the producer encloses (e^{A_{aug}τ}Y_j) for every τ in ([0,h]), where (h=1/128), and encloses its endpoint at τ=h. Outward endpoint construction is repeated after every exact rational interval operation. The endpoint box is carried into the next contiguous slab. By induction, if each slab proves the strict clip-interior branch, the union of the 256 partial-slab enclosures contains every supported full-hold internal trajectory from every allowed initial state and fixed label.

For Taylor degree (N=20), (q=h\|A_{aug}\|_\infty), and (q/(N+2)<1), the omitted tail is bounded by

\[
\|R_{N+1}(\tau)y_j\|_\infty \le \|y_j\|_\infty\,
\frac{q^{N+1}}{(N+1)!}\frac{1}{1-q/(N+2)}, \qquad 0\le\tau\le h.
\]

The profile limits all worker and replay processes to 60 s, 1 GiB, 5,000,000 interval operations, 16,384 rational bits, 8 MiB stdout and the fixed 96-bit outward dyadic grid. Any cap or proof failure is `UNKNOWN`/`RESOURCE_UNKNOWN`; it is never converted into success.

## Contact, collision and task predicates

On every partial slab, compute the true normalized slips from the enclosed wheel/body/yaw states. If β_j is the absolute slip upper bound, use (C_{j,min}\sqrt{1-\beta_j^2}) only after proving β_j<1. Contact requires the sum of the two certified reserve lower bounds to dominate the upper bound on |mur|. The square-root reserve is not differentiated at saturation.

The pose enclosure uses the full heading range and the global inequalities \(1-\theta^2/2\le\cos\theta\le1\), \(|\sin\theta|\le|\theta|\), then integrates outward bounds over each partial slab. Collision compares the resulting full-slab position enclosure against the static inflated circle. Progress accumulates the endpoint displacement enclosure and is compared with the already locked `7/20 m` rule only after whole-hold safety is certified. A failed strict clip proof invalidates candidate use of the affine trajectory after that point; its later margin/progress numbers are diagnostics, not claims about the clipped plant.

## Proof-to-code map and trust boundary

| Obligation | Implementation / replay |
|---|---|
| Protocol, positive-width initial box and fixed positive-width label image | `producer_v4.py::parse_protocol`; recomputed in `checker_v4.py::_read_and_validate` |
| Signed motor/back-EMF, wheel/contact, body and yaw coupling | `producer_v4.py::build_augmented_matrix`; separately reassembled in `checker_v4.py::_assemble` |
| Outward exact dyadic interval operations | `rational_interval_v3.py::I`; producer/checker share this disclosed arithmetic root |
| Partial-slab Taylor range, endpoint and tail | `producer_v4.py::exp_range`; replayed independently in `checker_v4.py::_flow` |
| 256 contiguous slabs, one fixed voltage and label image, endpoint chaining | `run_stage_v5.py` plus row `time_coverage`; recomputed by `checker_v4.py::audit` |
| Strict clip branch, reserve/contact, pose/collision and endpoint progress | `producer_v4.py::evaluate`; independently reconstructed by `checker_v4.py::_reconstruct` |
| Source/input binding, ordered single launch and limits | v5 frozen plan/bindings, `run_stage_v5.py`, `windows_job_supervisor.py` |
| Changed source/input, omitted slab, label reset and altered inequality | `audit_mutations_v4.py` on a saved v5 proof row; rejections must all replay |

Producer/checker do not share model, Taylor, pose, contact, collision or status functions. They share Python `Fraction` and the fixed-grid interval primitive, which remains an explicit common trust dependency. Mutation replay and source hashes check finite evidence integrity; neither proves the continuous-time mathematics independently of the stated derivation.

## Applicability and limitations

The exact point witness is one fixture, not a full-cell witness. The v5 task is still synthetic and its parameter scales have no hardware provenance. A negative margin or failed strict branch is not proof of physical collision, contact loss or task impossibility. The finer slab count may improve width while increasing computation/output cost; all resource caps are held fixed. Generic validated Taylor propagation and interval reachability are known techniques; novelty remains unresolved by G2. G2/G3/G4 and physical-platform correspondence remain `UNVERIFIED`; overall disposition remains `HOLD`.
