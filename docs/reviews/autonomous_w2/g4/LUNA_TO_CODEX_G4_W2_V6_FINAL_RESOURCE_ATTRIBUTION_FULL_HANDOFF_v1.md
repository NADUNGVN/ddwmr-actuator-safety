Session: DDWMR | LUNA-G4-AUER

# W2 G4 final resource attribution — corrected v6 matched task

**Issued:** 2026-10-08 (UTC)  
**Repository:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Scope:** read-only attribution of the three already-saved Auer outcomes against the three already-saved v6 outcomes. No query, worker, replay, fixture, retry, or stage was run for this handoff.

## Finding and scoped conclusion

The corrected matched comparison contains three previously consumed development actions per method. v6 completed native replay and common scoring for all three; only the alternative action `(1,1)` met the frozen task threshold. Local Auer returned `RESOURCE_LIMIT` on all three before accepting any time step, so it produced no proof-complete certificate for native or common replay.

The Auer stop is specifically attributable to the frozen exact-rational intermediate-bit guard: each first, full-horizon step attempt reached a `fraction.pow` pre-operation upper estimate above Auer's 32,768-bit cap. The largest completed rational values recorded before each stop remained below that cap. The stored diagnostic labels its stage `unclassified`; this report does not infer which higher-level expression requested the power.

**Scientific disposition for the proposed method contribution: `NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE`.** The evidence supports one narrow operational observation: on these three disclosed development actions and under these frozen pipelines, v6 produced one replay-validated task-eligible action, while local Auer produced no replayable result because of the configured bit guard. The attempted powers have no materialized or measured output width in these runs; this report does not substitute the estimate for an actual result. The comparison does not establish that Auer's mathematics cannot certify an action, that v6 is generally superior, or that the method has a contribution beyond this tested scope. It is not a timing comparison: only v6 completed proof and predicate processing. The cross-method evidence remains development evidence, not held-out confirmation.

## Attribution: configured cap, estimate, and observed arithmetic

The Auer profile pins exact reduced rational arithmetic and checks every numerator, denominator, and intermediate against `max_rational_bits = 32,768`. Its bit diagnostic has `estimate_kind = preoperation_intermediate_upper_estimate`, `primitive_id = fraction.pow`, and `stage_id = unclassified`.

| Matched action | Voltage | Configured Auer cap | Pre-operation estimate | Estimate over cap | Highest completed-result width | Headroom below cap | Auer status |
|---|---:|---:|---:|---:|---:|---:|---|
| zero | `(0,0)` | 32,768 bits | 33,327 bits | 559 bits | 32,167 bits | 601 bits | `RESOURCE_LIMIT` |
| nominal | `(1/2,1/2)` | 32,768 bits | 33,327 bits | 559 bits | 32,167 bits | 601 bits | `RESOURCE_LIMIT` |
| alternative | `(1,1)` | 32,768 bits | 33,285 bits | 517 bits | 32,134 bits | 634 bits | `RESOURCE_LIMIT` |

These columns mean different things:

- **Configured cap:** the frozen per-rational width ceiling, not a measured value.
- **Pre-operation estimate:** an upper-width estimate checked before the requested power is constructed. In the frozen `validation/g2/rational.py`, `Budget.pow` computes `max(numerator_bits, denominator_bits) * exponent`, calls `_tick`, and only then evaluates `a**exponent` (source lines 252–270). `_tick` raises when that estimate exceeds the cap before it increments `operations` (lines 91–110). The saved estimate is therefore not the width of a materialized result.
- **Observed completed results:** the saved maximum widths from operations that finished before the stop. They are below the cap by 601, 601, and 634 bits. They do not report the result width of the rejected power: that operation was not evaluated, so its actual output width is unknown from these artifacts. The evidence shows no completed rational result above 32,768 bits; it also does not establish that the rejected operation's result would have fit.

Consequently, “the rational result exceeded 32,768 bits” would misstate the evidence. The supported statement is “the pre-operation upper estimate exceeded the configured cap, and the checked operation was stopped before its result was computed.”

## Stop location and retry semantics

All three proof envelopes record the first attempted closed-hold interval as `[0,2] s`, with `step_width_s = 2`, `accepted_steps = 0`, one recorded rejected/resource-stop attempt, 30 Picard iterations, and 34 RHS/Jacobian evaluations. The counters also report 424,707 completed rational results, 426,577 operations started, and 426,578 operation attempts. The extra attempt is the cap-rejected operation; it was not counted as an operation started.

The frozen solver makes the stop route explicit. In `solver_r9_w2.py`, the trial step raises `ResourceLimit`; the solver catches it and returns a `RESOURCE_LIMIT` proof immediately (lines 519–543). Step halving happens later, only when a trial returns `step is None` after a completed native Picard/inclusion failure (lines 554–570). The saved runs therefore did **not** halve the two-second interval: they stopped on the arithmetic guard before the inclusion-failure retry branch. The evidence cannot tell whether a shorter step would have completed an inclusion or produced a useful certificate.

Other declared caps were not the reported cause. Per Auer action, the 2.86–3.00 s bounded-worker wall time and 2.609–2.906 s CPU time were below the 60 s limits; peak memory was 30,916,608–31,035,392 bytes against 1 GiB; 426,577 started operations were below the 2,000,000 cap; 30 Picard iterations were below 32; and 34 RHS/Jacobian evaluations were below 100,000. Each bounded child completed with return code 0 and emitted a structured method `RESOURCE_LIMIT` result. No proof-complete Auer output existed to replay or score.

## Matched 3+3 outcomes

| Action | v6 saved outcome | Local Auer saved outcome | Task-level reading |
|---|---|---|---|
| zero `(0,0)` | `CERTIFIED_SAFETY_TASK_INELIGIBLE`; native replay `PASS`; common replay `PASS` | `RESOURCE_LIMIT`; no proof-complete native/common replay | Neither is task eligible under the frozen threshold; Auer supplied no certificate result. |
| nominal `(1/2,1/2)` | `CERTIFIED_SAFETY_TASK_INELIGIBLE`; native replay `PASS`; common replay `PASS` | `RESOURCE_LIMIT`; no proof-complete native/common replay | Neither is task eligible under the frozen threshold; Auer supplied no certificate result. |
| alternative `(1,1)` | `CERTIFIED`; native replay `PASS`; common replay `PASS` | `RESOURCE_LIMIT`; no proof-complete native/common replay | v6 is the sole verified eligible action in this saved 3+3 comparison; Auer's result is profile-limited. |

The v6 alternative's saved common progress lower bound is approximately `0.363934753325 m`, above the frozen `7/20 m` threshold. The exact eligible sets in the result manifest are `v6={W2_G4_V6_ALTERNATIVE}` and `Auer={}` **under the frozen producer/profile pipeline**. The empty Auer set means no eligible Auer certificate was verified; it is not a theorem that the method cannot certify the action.

## Numerical-policy asymmetry and attribution boundary

The methods shared the declared external one-process, 60 s, 1 GiB worker envelope, but their internal arithmetic policies were different and frozen separately:

- v6 used outward rational intervals rounded to multiples of `2^-96`, 256 center slabs, a 16,384-bit rational cap, and a 5,000,000-operation cap.
- Local Auer used exact reduced rationals, a 32,768-bit per-intermediate cap, and a 2,000,000-operation cap, with a Taylor/residual/Picard reconstruction.

The Auer profile states that its accepted residual-Picard formulas were unchanged. The comparison tests a local Auer reconstruction, not the VALENCIA binary. Its arithmetic dependency is the shared `validation.g2.rational` `Fraction`/`Interval`/`Budget` implementation; the source closure pins that implementation and the Auer solver. Thus this is an observed interaction between the exact-rational local pipeline and its pre-operation guard, not an isolated measurement of the Auer theorem independent of implementation, nor a controlled same-arithmetic experiment.

This internal-policy difference prevents a blanket interpretation of the eligible-set gap as a pure mathematical-method effect. The result establishes the saved certificate availability of these frozen pipelines on these inputs. It does not establish general computational advantage, runtime advantage, or mathematical inability of either method.

## Frozen artifacts and integrity anchors

The corrected execution's compact result manifest binds the six action records and their per-action file hashes. Its recorded SHA-256 is `d35fc3a804a37f2230d99d45e2f86c4e45c3dfc0c6334b5a5f5bcfd9562604ac`. Other primary anchors:

| Artifact | Repository path | SHA-256 |
|---|---|---|
| G2 release v6 | `coordination/autonomous_w2/g2/releases/RELEASE_v6.json` | `789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55` |
| Frozen protocol v3 | `research/autonomous_w2/g4/matched_v6_task_development_v3/protocol_v3.json` | `bd285159ac9067e27338ff81426effde924c2e480c7c05d678ae73262532ef62` |
| Freeze manifest v4 | `research/autonomous_w2/g4/matched_v6_task_development_v3/freeze_manifest_v4.json` | `067995e0e60873c4c582946444a732ebc9d05eeb16eb1c601173d7ffc7c4a91e` |
| Freeze receipt v4 | `results/validation/autonomous_w2/g4/matched_v6_task_development_v3/freeze_receipt_v4.json` | `7dbab64e3d3e2279ef10e1198416cf500713ff19a4d4e32444be3f5d1bf56458` |
| Source closure v4 | `results/validation/autonomous_w2/g4/matched_v6_task_development_v3/source_closure_v4.json` | `4a138dbd9eb26f1ba81f9d6b367c86e57dbce5ceab20d97bba3f4fe201fb7097` |
| Nonquery preflight | `results/validation/autonomous_w2/g4/matched_v6_task_development_v3/nonquery_fixtures_v5/preflight_report_v4.json` | `4e73485b549d357a8b4f9d2e5bb27e0d36849dd3205d977c075928464c5a21ee` |
| Ordered phase receipt v4 | `results/validation/autonomous_w2/g4/matched_v6_task_development_v3/matched_phase_receipt_v4.json` | `d904e421c62ec02932f9f2d6e146c5571eaae8b736753c16f925c9c0a3a1e994` |
| Auer profile v3 | `research/autonomous_w2/g4/matched_v6_task_development_v3/auer_profile_v3.json` | `df1af1bc14e99755a46b9a662255419b4d169501496b7e4b71517192e16a90f1` |
| Auer solver snapshot | `validation/autonomous_w2/g4/auer_snapshot_v3/solver_r9_w2.py` | `69fc2a55412da02542f4fed5bf2dff1e4b8fe63c55468743a98e5f4ed76f62fa` |
| Shared rational budget source | `validation/g2/rational.py` | `8a2c16778b33898afd16c8da44945c2d41fd7d187cb11c7cb071745e68ed5c6e` |

The recorded closure contains 77 entries, with 77 reverified and zero mismatches after execution. For each Auer action, `matched_result_manifest_v1.json` binds one `native_proof.json` and one `worker_result.json`:

| Auer action | Native proof SHA-256 | Worker result SHA-256 |
|---|---|---|
| `W2_G4_AUER_ZERO` | `7cb6e2de2def168ccec006d6119d691ddae3490b5e256524acfd420c0c4735b1` | `2e41673d613872e3d10882947871205028667c8a95531f0ef763bf24bd34ba16` |
| `W2_G4_AUER_NOMINAL` | `62c70f27d8fd08397b5600de273bbec6349abac06389da9d61ce6c4fa3900511` | `3ed33d6bea26ad4c8daefeb35b5f8d304818b5bd45ac7f09435d2256df88b2c8` |
| `W2_G4_AUER_ALTERNATIVE` | `4506bbbf0b2a89143bc27566467d355ef978dc72364ff58879d3a74dc26f5472` | `2de8b1a94cb1e6d147a18e02e7f0f87ac559db3bbed6a971bbcb3081148068f7` |

The three source hashes above were recomputed read-only while preparing this report and agree with the frozen closure. No producer, native replay, or test was invoked.

## Counts, preserved history, and peer handoff

- Corrected matched phase: v6 native calls `3/3`; Auer native calls `3/3`; retries `0`; v6 native/common replay `3/3 PASS`; Auer proof-complete replays `0` because no complete proof existed.
- W2 counters remain: G2 native allowance `24/24` consumed; G4 candidate worker attempts `4/12` including the preserved earlier preproducer setup failure; G4 Auer worker attempts `3/12`; fresh confirmation `0/24` per method.
- Legacy Auer `1,944` batch remains `NOT_RUN`; legacy R5 `800/800` remains `NOT_RUN`. No commit or push was made.
- The earlier v2 setup failure and all v1/v2/v3 candidate evidence remain preserved. This report does not amend the six saved rows or reclassify prior evidence.

At issuance, G2's final frozen-result audit handoff was not yet present at `docs/reviews/autonomous_w2/g2/LUNA_TO_CODEX_G2_W2_V6_FINAL_FROZEN_RESULT_AUDIT_FULL_HANDOFF_v1.md`; the latest G2 status available for observation was sequence 19, SHA-256 `feedd8ef25ba5f7dfc1155354419bf31ae3456d7931e0b870e3b02f1e9348d2d`, which predates the corrected v4 freeze and execution. This G4 report therefore cannot bind a final G2 audit. G4 status records that peer handoff as pending. Once G2 publishes its final audit, its exact path/hash can be recorded in a new status/report version without changing the completed six outcomes.

## Final W2 boundary

This closes G4's attribution report for the saved `3+3` development comparison. It does not pass G2, G3, or G4, establish physical-platform correspondence, authorize controller/hardware work, or change the project gate. **Overall remains HOLD; G1 remains restricted PASS; G2/G3/G4 and physical-platform correspondence remain UNVERIFIED.**
