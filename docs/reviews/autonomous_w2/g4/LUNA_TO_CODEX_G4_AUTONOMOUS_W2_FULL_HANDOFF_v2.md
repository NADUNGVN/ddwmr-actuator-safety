Session: DDWMR | LUNA-G4-AUER

# G4 W2 — release v6 audit and scoped contribution verdict

**Date:** 2026-10-08 (Asia/Saigon). **Disposition:** `ACCEPT_FOR_SCOPED_VALIDATION` for the exact three-row G2 v6 development release; `NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE` for the proposed centered-residual contribution. Cross-method task utility remains **unmeasured**, not refuted. No matched comparison was run. **Project status remains HOLD; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.**

This is the versioned follow-up to the earlier no-release handoff. The old no-release observation and `RELEASE_AUDIT_STATE_v1/v2` remain preserved as history. Workflow W2 supersedes routine per-iteration Codex GO waits for this authorized G4 scope; this package therefore reached a release-scoped decision without waiting for a new GO. No G2 source, status, release, result, or snapshot was edited.

## 1. Finding — finite release evidence is internally consistent in the declared scope

G2 release v6 is present and immutable at `coordination/autonomous_w2/g2/releases/RELEASE_v6.json`, SHA-256 `789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55`. The release sidecar agrees. The observed G2 `STATUS.json` is sequence 17, SHA-256 `04542186C6122529157AD9A5F51398B5958DDBD197882DF4C75BA417F56AAEBC`, and points to that release. The release declares 31 source/dependency files and 139 evidence-inventory entries; all **31/31** source hashes and all **139/139** evidence byte-size/hash pairs were verified.

I replayed only the three already saved G2 checker records. The G2 checker returned replay success for **3/3** rows, recomputing 46 proof fields and 256 ordered center slabs per row. A separate G4 implementation using only Python `fractions.Fraction` independently rebuilt the parameter-dependent matrices, logarithmic-norm and residual bounds, Taylor partial-slab ranges, first-exit clip bound, contact, collision, endpoint-progress inequalities, and task classification. It imports no G2 producer, checker, or interval package. All three rows passed this finite audit.

The supervised repeat of the exact-fraction audit completed under a Windows Job Object in **17.968 s**, with peak memory **14,295,040 B**, one process, return code 0, and no output overflow. The configured limits were 60 s wall, 60 s CPU, 1 GiB memory, one process, 8 MiB stdout and 1 MiB stderr. It added zero native attempts and invoked zero producers.

During self-audit, I found that exact-bound audit v1 did not independently rebuild the stored `position_error_l1_upper_m` composition used by the collision inequality. The G2 checker had recomputed it, but relying only on that shared candidate checker would not meet the independent pose/collision audit requirement. I therefore added a second G4-only `Fraction` audit. It recomputes heading growth, progress error, x/y pose errors, their L1 sum, center distance and collision margin for all three rows. It passed under the same Windows Job Object limits in **0.125 s**, peak **12,034,048 B**, return code 0, with no native attempt or producer invocation. This closes that explicit audit gap; the earlier audit result remains preserved unchanged.

**Scope limit.** This is a release-scoped audit of three frozen development rows and their declared two-second clip-interior synthetic task. It does not establish arbitrary-input support, a general implementation theorem, recursive safety, physical tire/support correspondence, or a G2/G4 gate pass. The independent G4 arithmetic implementation is distinct, while the G2 producer and checker share `rational_interval_v3.I/Budget`; Python rational arithmetic, the plant equations, and the supervising module remain disclosed trust components.

## 2. Evidence — independently checked equations and outputs

The frozen v6 subclass uses the reduced nine-state model, `phi(s)=clip(s,-1,1)`, twelve fixed labels in `[0.9999,1.0001]`, one symmetric held voltage per two-second hold, a positive-width moving initial box, a static circle, and the already declared `7/20 m` endpoint-progress threshold. Only actions `(0,0)`, `(1/2,1/2)`, and `(1,1)` are in the frozen action list. The symmetric all-one reference is a proof device; true left/right parameter labels remain independent and fixed for each complete trajectory.

For the six internal coordinates `z=(u,r,omega_L,omega_R,i_L,i_R)` and affine state `y=(z,1)`, the centered construction has `z'=A(theta,V)y` on the affine clip branch. With the all-one reference matrix `A0(V)`, `e=z-z_c` obeys

\[
\dot e=A_6(\theta,V)e+(A(\theta,V)-A_0(V))y_c.
\]

The release bounds `delta_A >= sup_theta ||A-A0||_infinity` and an outward logarithmic-norm bound `mu` give

\[
\|e(t)\|_\infty \le e^{\mu t}(e_0+t\,\delta_A),\qquad 0\le t\le 2.
\]

The fixed-label quantifier is retained: taking a supremum over labels in this inequality does not model a label switching between slabs. The center path uses order-20 Taylor enclosures over 256 closed slabs of width `1/128 s`, with 96-bit outward dyadic rounding. The full-time center ranges—not only endpoints—are checked.

For each wheel, `|sigma_j| <= beta_c+3E`; the strict first-exit bound below one certifies that the true paths stay on the affine clip branch. The stored contact lower bound follows from

\[
2 C_{min}(1-\beta^2)-(U_c+E)E,
\]

using `sqrt(q)>=q` on `[0,1]` and the center yaw-rate value zero. The collision calculation encloses the complete center `p_x` path and subtracts an upper bound on pose deviation plus the inflated obstacle radius. Progress is the endpoint interval around the integrated center speed/heading path. These same saved inequalities and output fields were checked independently; the conclusion is limited to the release's inputs and source pins.

| Action | Safety result | Replayed progress enclosure (m) | `7/20 m` task result |
|---|---|---:|---|
| Zero `(0,0)` | Collision/contact certified | `[0.177602288, 0.240378241]` | Ineligible: upper bound below threshold |
| Nominal `(1/2,1/2)` | Collision/contact certified | `[0.270778521, 0.333554474]` | Ineligible: upper bound below threshold |
| Alternative `(1,1)` | Collision/contact certified | `[0.363954753, 0.426730706]` | Eligible: lower bound above threshold |

Thus the finite evidence supports one task-eligible action in this synthetic domain relative to the frozen zero/nominal action comparators. It does not show that Auer or R3 cannot certify the same action, and an ineligible action under this task criterion is not thereby unsafe.

### Reporting defect

The saved per-attempt receipts carry the schema label `G2_W2_V6_ATTEMPT_INTENT_v1`. Their stage receipt, row schema, source bindings, replay hashes, and independently recomputed mathematical fields remain intact. I classify this as a nonblocking reporting/schema-label defect for the three saved proofs, not as evidence that the physical predicates passed by a different claim. It must be corrected in a new G2 artifact before any later stage; v6 remains byte-for-byte unchanged.

The complete prior attempt history is preserved in `results/validation/autonomous_w2/g4/audit_attempts_v1.json`. It records two replay-harness preflight failures, one exact-rational audit stopped at its 60-second cap, and one path error before the corrected successful audit. `audit_attempts_v2.json` adds the successful supervised exact-bound and pose/collision runs. These were replay/audit development events, not producer queries, and none consumed a G4 native attempt.

## 3. Finding — the centered bound is not a supported new mathematical contribution

The exact v6 construction specializes established techniques: a validated Taylor reference path, affine/variation-of-constants comparison, logarithmic-norm growth, interval parameter augmentation, residual tubes, and full-time tube predicates. The plant-specific matrices, coefficient signs, fixed-label interpretation, contact reserve, pose deviation, and obstacle geometry require careful derivation and implementation, but the v6 hypothesis identifies no additional general inequality beyond specialization and coefficient accounting. G4 found no DDWMR-specific original inequality in this release.

Primary-source scope was checked against the retained Auer–Kiel–Rauh (2013) text, PDF SHA-256 `D6310C8FD32280ADDDA3F50E3367F9923940641D39DE0E70A0932869A2D0EAD2`: §4.1 Eq. (26), Eqs. (31), (33), (35), (40)–(41), and §4.2 Eqs. (42)–(43) cover interval IVPs, generalized derivative handling, and a verified tube around an approximate path. These support method-level overlap, not the repository's DDWMR equations, its code, or a claim that this is the original VALENCIA-IVP executable. The local solver is a reconstruction. The source crosswalk also records the relevant Rauh–Auer smooth residual method and the applicable growth/comparison and predictor-validation literature (Arcak–Maidens; TIRA; Houska et al.) with their assumptions and access limits.

Earlier G4 R23 review accepts that a shared-initial/shared-parameter paired-IVP is generic validated-reachability methodology. R24 accepts the narrow equation-level non-implication for the displayed cooperative-system test and stops the frozen synthetic action-ordering branch as a paper contribution. Neither result rules out every possible DDWMR-specific result; neither supplies a task-relevant advantage for v6.

**Contribution disposition:** `NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE` for the *new-method* claim. This is a scoped negative result for mathematical distinctness in v6, not a global novelty-absence claim. The demonstrated action-eligibility effect within the fixed G2 task is finite and supported; whether the same action is certifiable by Auer/R3, or whether v6 offers a useful resource/coverage advantage over them, remains unresolved because no W2 matched comparison was run.

## 4. Consequence — no W2 matched workload was justified or run

I checked the runnable-input bindings before considering a comparison. The v6 release pins one protocol, one narrow parameter image, a two-second hold, the three action IDs, and a producer/checker that validates those frozen inputs. It does not expose a general confirmation-input interface. Reusing the three saved rows would be development only, not fresh confirmation. The local Auer R9 worker is bound to the R19 query manifest and its older candidate profile (including a 120-second per-IVP limit); it is not a frozen end-to-end adapter for the v6 task. A valid new comparison would need a G4-owned outer ID/input-digest map, a reviewed adapter and source closure, a common collision/contact/**endpoint progress** rule, a W2 60-second/1-GiB profile, and exact unused inputs frozen before either producer sees outputs.

Such an adapter is technically possible. The G2 task protocol prospectively fixes the `7/20 m` decision threshold and zero/nominal/alternative actions, so the task-level result itself is not post-selected. However, v6 did not predeclare a cross-method primary criterion or an independently justified binding resource target. The threshold is a formal synthetic requirement, not an externally grounded performance budget. The old R19/R20 pilot cannot supply either, and the three observed v6 rows cannot become confirmation data. Given the generic-method overlap and absent cross-method criterion, a fresh run now would test an unformulated method-specific claim. I did not spend the 12-per-method development or 24-per-method confirmation allowances. **This is a decision not to run; it is not evidence that Auer/R3 match or beat v6.**

Historical pilot accounting remains: ten selected development pairs, Auer `9/10 CERTIFIED`, R3 `6/10 CERTIFIED`, three Auer-only certifications and zero R3-only certifications. Those figures are descriptive and do not establish universal dominance or v6 performance. Legacy Auer `1,944` query batch remains **not run**; legacy R5 remains **800/800 NOT_RUN**.

### Finding / Evidence / Consequence / Status / Required action

- **Finding:** v6 provides internally consistent, finite evidence for the three pinned synthetic actions; its centered comparison machinery is established generic methodology.
- **Evidence:** release-bound 31/31 source checks, 139/139 evidence checks, 3/3 G2 checker replays, 3/3 independent exact-fraction row audits, and the primary-source crosswalk above.
- **Consequence:** retain the finite task distinction as development evidence, but do not present it as a new DDWMR theorem, a matched method advantage, physical safety, or recursive safety.
- **Status:** `ACCEPT_FOR_SCOPED_VALIDATION` for the frozen v6 evidence; `NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE` for the centered-residual claim; no matched comparison; G4 gate remains UNVERIFIED.
- **Required action:** a future study must first supply a new independently justified plant-specific inequality or a predeclared method-specific coverage/cost effect and task. It then needs a new G4-owned source/input/resource freeze; v6 development rows and R19/R20 pilot IDs cannot be relabeled as confirmation.

## 5. Counts, costs, and exact reproduction

| Work item | Count/status |
|---|---:|
| G2 native attempts | 24/24 consumed; no allowance remains |
| G2 v6 actions | 3 saved, replayed and audited; zero held-out rows |
| G4 saved checker replays | 3/3, read-only |
| G4 supervised nonquery audits | 2 successful: exact bounds 17.968 s / 14,295,040 B; pose/collision 0.125 s / 12,034,048 B |
| G4 native smoke/development producer attempts | 0 per method |
| G4 fresh confirmation rows | 0/24 per method |
| Auer 1,944-query batch | Not run |
| Legacy R5 | 800/800 NOT_RUN |
| Commits/pushes | None |

Environment: Windows/PowerShell, branch `main`, HEAD `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`. The shared worktree was already dirty; all new outputs from this continuation are in G4-owned W2 prefixes. No branch switch, reset, clean, commit, or push occurred.

Cost detail for the reused v6 development rows: G2 workers took **20.109 / 9.969 / 10.218 s** for zero/nominal/alternative (total **40.296 s**); their saved-stage checker passes took **10.156 / 10.078 / 10.047 s** (total **30.281 s**). The separate G4 read-only checker replay took **10.672 / 10.250 / 10.343 s** (total **31.265 s**). Maximum recorded peak memory was 14,983,168 B for a G2 worker, 14,524,416 B for its initial checker, and 14,741,504 B for the G4 replay. G2's stage receipt records a total phase duration of **70.671 s**. These are offline validation costs for a two-second hold, not an online control deadline.

Historical R19 pilot costs, which do not measure v6: the ten selected development pairs used 15.595 s R3 worker time and 23.359 s Auer worker time overall; on the six jointly certified pairs, 12.658 s R3 and 9.437 s Auer worker time, with separate common-audit totals 24.205 s and 19.609 s respectively. Proof sizes totaled 1,137,484 B R3 versus 25,332,478 B Auer; peak process memory was 56,332,288 B and 123,445,248 B. These are selected-pilot descriptive values only, not a predeclared W2 cost criterion. No Auer or R3 producer/replay cost was incurred in this v6 W2 continuation.

Commands used to produce the read-only G2 checker replay and independent audit evidence:

```powershell
python -B validation/autonomous_w2/g4/replay_g2_v6_saved.py
python -B validation/autonomous_w2/g4/run_exact_bound_audit_capped.py
python -B validation/autonomous_w2/g4/run_pose_collision_audit_capped.py
```

The replay runner preserves the three G2 rows and fails closed if its versioned output directory already exists. The capped audit runner acquires `coordination/autonomous_w2/COMPUTE.lock`, invokes only the G4 exact-fraction auditor inside the Windows Job Object, writes versioned `exact_bound_audit_v2_supervised` evidence, and releases only its own lock token. To repeat either run, create a new versioned output destination; do not overwrite the retained records.

## 6. Artifact ledger

Existing release-bound evidence retained and used:

- `coordination/autonomous_w2/g2/releases/RELEASE_v6.json` — `789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55`.
- `coordination/autonomous_w2/g2/STATUS.json` — sequence 17; observed digest is bound in `RELEASE_AUDIT_STATE_v4.json`.
- `results/validation/autonomous_w2/g4/replay_g2_v6_saved_789d6b37_r2/replay_receipt.json` — `26C17C0419C151A0CF6BB6E16671A12827207CB6EF608F085F685780D5542C43`.
- `results/validation/autonomous_w2/g4/exact_bound_audit_v1.json` — `D4077BCAFEBD31EDE5B6BD072E7F5FD510DA08C25A57FA10D015F154E88FCE5E`.
- `results/validation/autonomous_w2/g4/exact_bound_audit_v2_supervised/audit_result.json` — `D4077BCAFEBD31EDE5B6BD072E7F5FD510DA08C25A57FA10D015F154E88FCE5E` (identical mathematical result, new supervised receipt).
- `results/validation/autonomous_w2/g4/exact_bound_audit_v2_supervised/audit_receipt.json` — `1349DCEE00864C32DEA898A28094FCA2BF1F08B3689113872350E4F0610DB321`.
- `results/validation/autonomous_w2/g4/pose_collision_audit_v1.json` — `B5D13CDEF35597CC8E527B5022AB51CEA5C1A775D245C2066B91308214321D5D`.
- `results/validation/autonomous_w2/g4/pose_collision_audit_receipt_v1.json` — `416A837E9E72C18E60C0DB31E4911584F91CF0A0297C08335590181CFAA36400`.

New G4 follow-up artifacts:

- `validation/autonomous_w2/g4/run_exact_bound_audit_capped.py` — `8BF7C1570BC10991833AD1537FAA48E5092FAA71F159A3266231163A0ECD4AA0`.
- `validation/autonomous_w2/g4/audit_g2_v6_pose_collision.py` — `EA0A887C6859236F018088E4A8A8A471ED79459793D9A7B0B0B59F5B0F3472E7`.
- `validation/autonomous_w2/g4/run_pose_collision_audit_capped.py` — `FCC78F93117072E4FC93AAAF27C90ADCD7380A31C07C39782257D8F1E523676C`.
- `results/validation/autonomous_w2/g4/audit_attempts_v2.json` — versioned attempt supplement preserving v1 failures; hash is listed in STATUS sequence 4.
- `coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v4.json` — exact peer release/status binding and final audit/contribution decision. It supersedes provisional wording in v3 that could be read as refuting unmeasured matched utility; v3 is retained unchanged.
- `coordination/autonomous_w2/g4/STATUS_W2_SEQUENCE_04.json` and current `coordination/autonomous_w2/g4/STATUS.json` — package closure state.
- This report: `docs/reviews/autonomous_w2/g4/LUNA_TO_CODEX_G4_AUTONOMOUS_W2_FULL_HANDOFF_v2.md`.

The detailed earlier source/Auer crosswalk remains at `docs/reviews/autonomous_w2/g4/AUDIT_CHECKLIST_AND_SOURCE_CROSSWALK_v1.md`; the earlier no-release report is preserved at `docs/reviews/autonomous_w2/g4/LUNA_TO_CODEX_G4_AUTONOMOUS_W2_FULL_HANDOFF.md`.

## 7. Claim table and next scientific decision

| Claim | Disposition | Scope |
|---|---|---|
| The exact G2 v6 release and declared evidence inventory match their hashes/sizes | Supported | 31 source files and 139 evidence entries |
| The three saved rows replay and satisfy the checked v6 inequalities | Supported for scoped validation | Three consumed development actions only |
| One alternative voltage satisfies the frozen synthetic task while zero/nominal do not | Supported | Fixed narrow synthetic domain, threshold `7/20 m` |
| The centered logarithmic-norm/residual construction is a new general method | Not supported | It specializes established validated-ODE/comparison machinery |
| v6 beats Auer or R3 in matched coverage, cost, or task usefulness | Unresolved / unmeasured | No W2 matched workload or cross-method primary criterion was frozen or run |
| The result proves physical-platform safety or recursive viability | Not supported | Outside this finite one-hold reduced-model audit |
| All possible DDWMR-specific contributions are absent | Not claimed | Literature and contribution search is scoped, not exhaustive |

**Next scientific decision:** decide whether to formulate a new plant-specific inequality or a cross-method coverage/cost hypothesis with an independently justified task and primary metric. If pursued, freeze a G4-owned input adapter/source closure and unused confirmation IDs before either method sees results. If no such claim can be stated, end this centered-residual branch at `NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE`; do not reopen Auer 1,944 or relabel historical IDs.

**Final status:** `HOLD`; G1 `PASS_RESTRICTED_REDUCED_MODEL_SCOPE`; G2/G3/G4 and physical-platform correspondence `UNVERIFIED`. This package does not pass a gate or alter physical assumptions.
