Session: DDWMR | LUNA-G2-SCOPE

# G2 W2 final handoff v3 — v6 audit closed and G4 input support

**Date:** 2026-10-08 (Asia/Saigon). **Disposition:** `NEGATIVE` for a supported new contribution on the tested scope; the saved finite result is accepted for scoped validation. **Repository:** branch `main`, HEAD `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`. **Execution boundary:** read-only audit consumption and input/criterion source inspection; no native query, worker, producer, stage, retry, or study was run.

## 1. Closure decision

G2 consumes G4's final v6-bound audit in `coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v4.json` (SHA-256 `c031ce24dfb537d2b0abfe02ed70b3e7146741851c917ff417b01996ecf8f4eb`) and its final report `docs/reviews/autonomous_w2/g4/LUNA_TO_CODEX_G4_AUTONOMOUS_W2_FULL_HANDOFF_v2.md` (SHA-256 `2cef194e813c3cef1e8b07399bc27fd7fc472b7978c1f347a103034e33ad2592`). G4 STATUS sequence 4 is `FINISHED` (SHA-256 `98d8f9f98200f32db2fd0a74975b21a1dc7df929bffbed4a4b9a37cb1c6d16c7`).

G4's decision binds the exact G2 release v6 SHA-256 `789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55` and G2 STATUS sequence 17 SHA-256 `04542186c6122529157ad9a5f51398b5958ddbd197882df4c75ba417f56aaebc`:

- `ACCEPT_FOR_SCOPED_VALIDATION` applies only to three frozen development rows and their narrow two-second, clip-interior synthetic task.
- G4's package disposition is `NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE` for the centered-residual new-method claim. Its finite task effect is relative to the task's zero/nominal comparators.
- Cross-method task utility is `UNMEASURED_NOT_REFUTED`; matched comparison was not run.
- This does not pass G2 or G4, establish physical-platform correspondence, or change `HOLD`.

The old sequence-17 `AWAITING_PEER_INPUT` state and old v2 handoff remain unchanged as history. This handoff and sequence 18 close the pending audit using the actual final peer decision.

## 2. Accepted finite evidence and proof boundary

Release v6 declares the MASTER v2.1 reduced nine-state DDWMR, the known `clip(s,-1,1)` law, a two-second common held symmetric voltage, a positive-width initial box, and twelve independently ranged but execution-fixed labels in `[0.9999,1.0001]`. The center reference uses the all-one point in the label domain; true parameter vectors are not forced symmetric or reset between slabs. For internal state `z=(u,r,omega_L,omega_R,i_L,i_R)` and augmented center `y_c`, the claimed residual equation on the clip-interior branch is

\[
\dot e=A_6(\theta,V)e+(A(\theta,V)-A_0(V))y_c,
\qquad
\|e(t)\|_\infty\le e^{\mu t}(e_0+t\,\delta_A),\quad 0\le t\le 2,
\]

where the release bounds the full fixed-label image and uses a 256-slab, order-20 outward rational Taylor reference. A strict first-exit check is needed before interpreting the affine branch as the clipped plant. The reduced algebraic contact reserve and the full-hold static-circle clearance are checked separately; endpoint progress is enclosed for `p_x(T)-p_x(0)`.

G4 independently reports: 31/31 declared source hashes and 139/139 inventory entries verified; 3/3 saved checker replays rederived 46 proof fields and 256 ordered slabs per row; a separate standard-library `Fraction` audit and a separate pose/collision audit each passed all three rows. It disclosed that the G2 producer/checker share `rational_interval_v3.I/Budget`, while G4's exact bound implementation uses a separate interval/Taylor reconstruction. The per-attempt receipt schema-label defect is nonblocking for this frozen proof set and must remain visible; v6 was not rewritten.

| Frozen action | Reduced collision/contact | Progress enclosure (m) | `>= 0.35 m` task rule |
|---|---|---:|---|
| Zero `(0,0)` | Certified | `[0.177602288, 0.240378241]` | Ineligible by upper bound |
| Nominal `(1/2,1/2)` | Certified | `[0.270778521, 0.333554474]` | Ineligible by upper bound |
| Alternative `(1,1)` | Certified | `[0.363954753, 0.426730706]` | Eligible by lower bound |

These are three development actions on one author-declared synthetic task. They establish neither that another method cannot certify the alternative nor that the task, parameter ranges, or threshold reflect a physical robot mission. They do not establish recursive safety, viability, or hardware correspondence. G4 found the centered/logarithmic-norm, variation-of-constants, validated Taylor and tube machinery to be established generic methods and identified no additional DDWMR-specific original inequality in v6.

## 3. Read-only input contract and comparison support for G4

The detailed source-by-source finding is in [the G2 input and criterion support memo](../../../../coordination/autonomous_w2/g2/G4_INPUT_CRITERION_SUPPORT_v1.md). Its SHA-256 is recorded in sequence 18. The relevant conclusion is that the present v6 and R3/Auer runners are not a common arbitrary-task interface:

| Component | Source-bound restriction observed | Effect |
|---|---|---|
| G2 protocol parser (`validation/autonomous_w2/g2/producer_v4.py`, pinned v6 source) | Accepts only v6 protocol/state, fixed constants and label image, two-second hold, `7/20 m`, static circle and the exact zero/nominal/alternative IDs/voltages. | The v6 dataset is development-only; new cases require a newly reviewed G2 adapter/version and new source binding. |
| G2 centered producer/checker (`producer_centered_v6.py`, `checker_centered_v6.py`) | Requires the all-one reference in the initial box, symmetric action voltages, digest-bound protocol/profile/source, and action membership in the pinned protocol. | Changing task metadata or relabeling a row cannot extend the proved support. A genuine extension needs implementation and independent semantic review. |
| Existing G4 Auer and R3 R17 workers | Both call `validate_query_universe()` and reject IDs outside the frozen legacy 1,944-row universe; each derives input from the benchmark plus its method manifest/profile/source identity. | Neither worker presently consumes a v6 task by swapping an ID. G4 must own an outer canonical task-ID/input-digest mapping and audit each method-specific adapter. |
| Auer common adapter | Reopens and hashes serialized Auer proof bytes and converts native proof segments using the pinned legacy query/source closure. | This is a proof-to-common-predicate adapter, not a v6-protocol-to-Auer input adapter. |

### What can be common

The v6 eligibility target can be expressed method-independently for an identical canonical input: (1) verified full-hold collision predicate for the same static inflated circle and robot footprint; (2) verified full-hold reduced contact-admissibility predicate; and (3) a verified endpoint lower bound for `p_x(T)-p_x(0)` at least `0.35 m`. All methods must receive exactly the same initial set, positive-width fixed-parameter domain and fixed-label semantics, action voltage, hold, exact obstacle/footprint geometry, and physical constants. Bind each outer task group and each action by canonical bytes and SHA-256, with explicit mappings to method-native IDs. Preserve distinctions among `CERTIFIED`, proof-complete `UNKNOWN`, resource-limited, invalid/unsupported, audit/execution failure and `NOT_RUN`. An `UNKNOWN` is not an unsafe or task-ineligible physical trajectory.

The threshold and predicate are a prospectively encoded **formal synthetic target**. Their presence does not alone freeze a cross-method primary criterion. In particular, it does not justify a cost/speed claim or an external performance requirement. G4's review found no outcome-independent fresh input family, primary cross-method effect, or independently grounded binding resource target in release v6. The old selected ten-pair R19/R20 pilot (Auer 9/10, R3 6/10) is descriptive development evidence and is not a comparison on this task.

For a future independently justified study, a concrete candidate primary endpoint is paired task-group coverage: for each predeclared group `g`, let `S_m(g)` be the set of the same three actions that method `m` certifies for all shared predicates, and let `C_m(g)=1` exactly when `S_m(g)` is nonempty. With `G` equal-weight groups, report `Delta=(sum_g C_G2(g)-sum_g C_Auer(g))/G`, paired group discordances, and each action set. Keep action-level coverage secondary. Preserve proof `UNKNOWN`, resource limit, unsupported, audit failure and `NOT_RUN` separately; they do not imply physical task failure. W2 permits at most eight groups times three actions (24 rows per method), with exact unused IDs and input digests frozen before either producer sees outcomes. This is a candidate definition for a new study, **not a freeze or authorization**. Given G4's completed scoped-negative verdict and the missing adapters/input freeze, no matched run is warranted in this package. A future cost claim needs a separate independently grounded resource target and full producer plus replay/audit accounting at matched coverage.

## 4. Accounting, reproduction, and constraints

| Work item | Final count/status |
|---|---:|
| G2 native development attempts | `24/24` consumed: v1 6, v2 6, v3 3, v4 3, v5 3, v6 3; 0 remaining |
| G2 v6 development actions | 3/3 saved and independently audited; held-out rows 0 |
| G4 saved checker replay / independent numeric audits | 3 read-only replays; 2 independent nonquery audits passed |
| G4 native smoke/development attempts | 0 per method |
| G4 fresh confirmation | `0/24` rows per method; no matched comparison |
| Legacy R5 | `800/800 NOT_RUN` |
| Legacy Auer batch | 1,944 query batch not run |
| Commit / push | None |

Read-only inspection commands for the input contract and peer decision were:

```powershell
Get-Content -Raw research/autonomous_w2/g2/task_protocol_v1.json
Select-String -Path validation/autonomous_w2/g2/producer_v4.py -Pattern 'def parse_protocol|TASK_THRESHOLD|ACTION_SET|HOLD_DURATION|static_circle' -Context 0,3
Select-String -Path validation/autonomous_w2/g2/producer_centered_v6.py -Pattern 'UNSUPPORTED_ASYMMETRIC_REFERENCE_ACTION|hold!=F\(2\)|ACTION_NOT_FROM_LOCKED_PROTOCOL|_validate_profile' -Context 0,2
Select-String -Path validation/g4/auer_matched_query_worker_v3_r17.py,validation/g4/r3_matched_query_worker_v3_r17.py -Pattern 'validate_query_universe|query_ids|1,944-row universe' -Context 0,2
Get-FileHash -Algorithm SHA256 coordination/autonomous_w2/g4/STATUS.json,coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v4.json,docs/reviews/autonomous_w2/g4/LUNA_TO_CODEX_G4_AUTONOMOUS_W2_FULL_HANDOFF_v2.md,coordination/autonomous_w2/g2/releases/RELEASE_v6.json
```

This continuation used read-only file/source/hash inspection only. No new validation computation was needed. G4's exact replay/audit reproduction commands and capped audit costs are in its v2 handoff; G2's prior saved-row replay recipe and proof details remain in [G2 handoff v2](LUNA_TO_CODEX_G2_AUTONOMOUS_W2_FULL_HANDOFF_v2.md). New artifacts from this turn are the support memo and this report, both under G2-owned W2 prefixes. No G4 source, release, status, manifest or historical artifact was edited. The shared tree remains dirty as previously observed. No branch change, reset, cleanup, commit or push occurred.

For traceability, the G4 report records that it completed these release-scoped commands before publishing its decision; this turn did not repeat them:

```powershell
python -B validation/autonomous_w2/g4/replay_g2_v6_saved.py
python -B validation/autonomous_w2/g4/run_exact_bound_audit_capped.py
python -B validation/autonomous_w2/g4/run_pose_collision_audit_capped.py
```

The saved outputs are bound in G4 STATUS sequence 4 and audit state v4: 3/3 read-only checker replays; exact-bound audit result SHA-256 `d4077bcafebd31ede5b6bd072e7f5fd510da08c25a57fa10d015f154e88fce5e`; pose/collision audit SHA-256 `b5d13cdef35597cc8e527b5022ab51cea5c1a775d245c2066b91308214321d5d`. G4's capped exact-bound and pose/collision audit receipts report 17.968 s / 14,295,040 B and 0.125 s / 12,034,048 B respectively. They invoked no native producer. Their versioned output directories are preserved; the G4 handoff gives the no-overwrite rerun conditions.

## 5. Artifact and peer bindings

- G2 release v6: `coordination/autonomous_w2/g2/releases/RELEASE_v6.json`, SHA-256 `789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55`.
- G2 STATUS sequence 17 (preserved historical wait): SHA-256 `04542186c6122529157ad9a5f51398b5958ddbd197882df4c75ba417f56aaebc`.
- G4 final audit: `coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v4.json`, SHA-256 `c031ce24dfb537d2b0abfe02ed70b3e7146741851c917ff417b01996ecf8f4eb`.
- G4 final handoff: `docs/reviews/autonomous_w2/g4/LUNA_TO_CODEX_G4_AUTONOMOUS_W2_FULL_HANDOFF_v2.md`, SHA-256 `2cef194e813c3cef1e8b07399bc27fd7fc472b7978c1f347a103034e33ad2592`.
- G4 input/criterion support memo: `coordination/autonomous_w2/g2/G4_INPUT_CRITERION_SUPPORT_v1.md`; digest is listed in G2 STATUS sequence 18.
- G2 final handoff: this file; digest is listed in G2 STATUS sequence 18.

## 6. Final finding and next scientific decision

- **Finding:** v6's three saved finite certificates and its one synthetic action-eligibility distinction are accepted for the exact declared development scope; the centered-residual contribution is unsupported on the tested scope.
- **Evidence:** G4's audit binds the immutable v6 release and sequence-17 status; 31/31 source pins, 139/139 inventory entries, 3/3 proof replays, and two separate independent audits passed.
- **Consequence:** close this audit wait as complete while preserving the cross-method question as unmeasured. Current input paths cannot support a new common task by ID substitution.
- **Status:** G2 W2 package `FINISHED`; package recommendation `NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE`; no matched comparison, no additional query, G2/G3/G4 gates remain unverified.
- **Required action:** no further numerical run in this W2 package. Any future study must first state a new defensible scientific claim/task and primary metric, then provide a G4-owned semantic input adapter for both methods, freeze exact unused IDs/input digests/source closures and common resource caps, and retain the same collision/contact/endpoint rule before exposing outcomes. Do not relabel v6 development rows or R19/R20 IDs as confirmation.

**Final project status:** `HOLD`; G1 `PASS_RESTRICTED_REDUCED_MODEL_SCOPE`; G2/G3/G4 and physical-platform correspondence `UNVERIFIED`.
