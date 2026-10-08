# Codex review — G2 R3 scoped computational evidence

**Date:** 2026-10-02  
**Reviewed handoff:** `LUNA_TO_CODEX_G2_PARALLEL_SCOPE_AUDIT_FULL_HANDOFF.md` and `G2_R3_SCOPED_ACCEPTANCE_CANDIDATE_v1.md`  
**Repository snapshot inspected:** `main` at `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`  
**Authority:** MASTER v2.1 and workflow W1. No canonical gate or plant edit is made here.

## Decision

**ACCEPT the frozen R3 batch as a narrowly scoped finite synthetic one-hold computational result.** For each of its proof-replayed `CERTIFIED` records, the inspected source-to-inclusion path supports the continuous collision and ideal-contact claim for the declared formal nine-state model, rational initial box, fixed parameter image, one common held voltage, and entire hold. This acceptance is limited to the frozen `G2-COMP-clip` implementation/profile and hash-bound batch. It is neither a universal implementation-soundness theorem for every input admitted by the draft specification nor evidence of practical deployment.

**HOLD remains. G1 restricted PASS; G2/G3/G4 and physical-platform correspondence remain UNVERIFIED.**

## Finding 1 — the supported claim has a precise boundary

**Evidence.** The batch uses the selected `clip(q,-1,1)` law, 12 fixed rational labels, a correlated parameter image, nonzero-width nine-state initial boxes, one circle per query, `n=1`, one whole-hold interval panel, and a single voltage applied to every initial state and label in each query. The frozen profile uses Taylor degrees 16/18, comparison order 16, 24 root bisections, and 24-bit directed-dyadic collision gaps. The exact benchmark and profile, rather than arbitrary MASTER `Theta` or `phi`, define the computational claim. See `research/theorem_notes/G2_FINITE_EVALUATOR_SPEC_v1.md`, `validation/configs/benchmark_v1.json`, and the reviewed candidate note.

**Consequence.** A `CERTIFIED` record is a sufficient full-hold assertion for its own formal query. `UNKNOWN` asserts neither safety nor unsafety. It says nothing about endpoint return, repeated feasibility, an online policy, or a physical robot.

**Status.** VALID for this restricted interpretation.

**Required action.** Use this exact scope whenever citing the R3 batch.

## Finding 2 — independent source-to-inclusion check

**Evidence.** I inspected the frozen-byte versions of `validation/g2/{polynomial,model,rational,interval,evaluator,checker}.py` against MASTER §§8, 14–16 and the G2 candidate/specification equations. Their current SHA-256 digests match the Luna handoff; five are explicitly in the R3 role commitments, while the omitted `polynomial.py` matches its independently identified Git blob. The decisive path is:

| Inclusion premise | Source and proof field | Review result |
|---|---|---|
| One execution-fixed rational label image, positive parameters, gear identities | `polynomial.py` expression/identity checks; `model.py` parameter image and `A,B,D,S,QF`; proof `parameter_intervals`, scaled matrices | Direct interval images cover each fixed label; forgetting correlations in subsequent hulls enlarges the result. The gear equalities are checked as rational-function identities. |
| Full-hold finite predictor | `interval.py` interval matrix exponential; `evaluator.py` `_predictor_level`; proof `exp_range`, `P0_scaled`, `P1_scaled` | Interval powers enclose the same matrix power; the norm remainder is outward. `[0,T]` times a complete integrand range encloses every partial integral. Both predictor levels retain the same initial state/label in the underlying mathematical fiber. |
| Internal error | `evaluator.py` residual, `_bound_model_matrices`, `_radius_series`; proof `delta_abs_scaled`, `residual_force_upper`, `N_nonnegative_majorant`, `eta_scaled` | `P1-P0` is a conservative paired-increment bound. `min(QF·delta,2C)` bounds the force defect. The nonnegative `N` dominates the Metzler comparison matrix; the positive finite series and its exponential tail bound the error for all `t≤T`. |
| Pose and contact | `evaluator.py` full-hold lift/contact block; `interval.py` trig/root enclosures; proof `center_*_range`, `E_theta`, `E_p`, `beta_upper`, contact margins | The velocity/rate and trig ranges cover the complete hold. The pose error uses the heading unit-vector bound. Clip Lipschitz inflation and lower square-root brackets bound available lateral reserve, including at saturation corners; demand is upper bounded. |
| Static-circle clearance | `evaluator.py` `_bounded_collision_distance`; `checker.py` `_checker_r3_distance_witness`; proof dyadic gaps, radicands, root brackets, collision margin | Directed floor/ceiling gaps bracket the exact rectangle-to-point gaps before squaring. The **lower** root gives minimum distance to the whole predictor-position rectangle; subtracting `R_s+E_p` is a sufficient full-hold clearance check. |

The comparison uses the formal ODE outside the contact-validity set only as a bounding device; the final contact inequality separately establishes admissibility. No contact-law derivative, parameter reset, ordinary trajectory sampling, or endpoint-only clearance enters this path. I found no concrete false-`CERTIFIED` branch in the frozen R3 path inspected. The trusted base remains Python exact integer/`Fraction` arithmetic, the shared interval/model/elementary-function code, and correct binding of archived records to the frozen source and inputs.

**Consequence.** The independent equation-to-source review closes the particular source-to-inclusion question raised by the Luna handoff for **the frozen R3 batch**. It does not audit all possible future rational expressions, profiles or benchmark domains.

**Status.** VALID within the frozen R3 scope; general evaluator soundness UNVERIFIED.

**Required action.** Preserve the source hashes and the stated trusted base with every citation of this result.

## Finding 3 — archived counts and replay evidence

**Evidence.** Independent streaming of the pilot JSONL and compressed continuation yielded 1,944 unique query IDs, **1,196 `CERTIFIED`**, **748 proof-complete `UNKNOWN`**, and 1,944 proof objects, with no resource, invalid-input or execution-failure records. The pilot SHA-256 is `fdbce2ac5587247ababc0849c5fce8f9a596c3eb2175ed277545072c06acdc43`; the compressed continuation SHA-256 is `352b6c67480133350a7d1bfc89334a1beff1dc27c64cfda46391af27982fa874`, whose decompressed bytes hash to `de339ffcb5ee5e0c83f8d25e3077d9fd9316f83293982189aaffba0bdcf3b196`. The 216 state/scene/horizon groups divide into 132 with all nine actions certified, 76 with none, and eight with only `V=(0,0)` certified. The archived `full_grid_record_check_r3_v1.json` reports `all_pass=true` and 1,944/1,944 proof replay. I did **not** rerun that full checker; I separately replayed one archived `CERTIFIED` and one archived `UNKNOWN` pilot record in memory against the unchanged checker, and both returned `replayed=true` and `record_integrity_valid=true`.

**Consequence.** The row counts, proof presence and recorded replay are accepted as evidence for this designed grid. The checker reconstructs exact arithmetic and statuses but shares `rational.py`, `interval.py`, `model.py`, and parsing/hash helpers from `evaluator.py`; it is not an independent numerical engine. The 1,944 rows are not independent statistical samples.

**Status.** VALID recorded batch/result accounting; full replay in this review is limited to two fresh representative records plus the archived full-check report.

**Required action.** Quote both the direct counting and the replay provenance accurately. Retain `PENDING_INDEPENDENT_AUDIT` in historical records; this review is an external decision note, not a rewrite of those records.

## Finding 4 — provenance and resource wording need correction in future runs

**Evidence.** `model.py` imports `polynomial.py`, omitted by both role-specific `PRODUCER_PATHS` and `CHECKER_PATHS`; `checker.py` imports helpers from `evaluator.py`, omitted from `CHECKER_PATHS`. The run-bound specification ledger omits `G2_ENCLOSURE_CANDIDATE_v1.md`. Immutable Git revisions and matching current file hashes still identify these source bytes, so the omissions do not establish a different R3 executable. Separately, `Budget._tick` checks the wall deadline every 256 metered operations and `run_query` has no final deadline check before a successful return. The declared 15 seconds is thus a cooperative checkpoint limit, not a hard per-query wall-time guarantee. Every archived displayed time was 0.109–0.313 seconds, far below 15 seconds.

**Consequence.** R3 proof arithmetic and outcomes are not overturned, but its explicit dependency closure and hard-time wording are incomplete. Exact rational bit/operation caps are separate from the wall-clock caveat.

**Status.** NEEDS REVISION for future provenance/profile wording; no retrospective R3 artifact edit required.

**Required action.** Bind the full transitive producer/checker source closure and analytic note in a future manifest. Either enforce a final deadline check or describe the time limit as cooperative. Keep the frozen R3 files intact.

## Finding 5 — usefulness and external relevance remain open

**Evidence.** All 140 groups with at least one certified action also certify zero voltage. The eight mixed groups repeat one `state_low_mid`, `T=0.1 s` contact-bound distinction across eight obstacle geometries; all nonzero actions return `UNKNOWN`, not unsafe. The 1,056 certified nonzero-action rows occur only in the 132 all-actions-certified groups. Every recorded query time exceeds its own hold duration. The benchmark's parameters, capacities, contact law and scenes are explicitly synthetic; the reviewed sources supply no compatible platform or literature-derived parameter/contact package. G4's matched Auer comparison is a separate novelty lane.

**Consequence.** R3 shows finite certificates on moving, nonzero-width synthetic cells with parameter-dependent actuators. It does not show that nonzero voltage expands existential group coverage, that the evaluator meets an online deadline, or that the synthetic model transfers to hardware.

**Status.** Narrow finite computational result ACCEPTED; practical usefulness, defensible operating-domain data, online feasibility and physical correspondence UNVERIFIED; G4 novelty UNVERIFIED.

**Required action.** Before a new usefulness study, register a source-backed reduced-model parameter/contact domain, its units and correlations, task-driven state/scene/horizon/action grid, and an application-based acceptance criterion. A later claim of nonzero-voltage coverage gain requires a predeclared group in which a nonzero action is certified while zero voltage is not. Preserve `UNKNOWN` as inconclusive.

## Final disposition

The Luna G2 scope handoff is **accepted with the qualifications above**. The next G2 work is evidence design and provenance for a decision-relevant domain, together with corrected source/resource declarations in any future run. This review authorizes no G3, controller, hardware work, Auer batch or gate promotion. The parallel `LUNA-G4-AUER` lane remains separate.

**Vietnamese forwarding summary:** R3 có 1.196 chứng nhận và 748 kết quả `UNKNOWN` trên đúng lưới tổng hợp 1.944 truy vấn; đường bao hàm source R3 đã được Codex rà độc lập và được chấp nhận trong phạm vi đóng băng này. Điện áp zero đã bao phủ toàn bộ 140 nhóm có chứng nhận, nên chưa có bằng chứng lợi ích chọn điện áp khác zero. Bộ tham số chưa có nguồn thực nghiệm, thời gian chạy chưa đạt yêu cầu online, và G2/G3/G4 vẫn UNVERIFIED; dự án tiếp tục HOLD.
