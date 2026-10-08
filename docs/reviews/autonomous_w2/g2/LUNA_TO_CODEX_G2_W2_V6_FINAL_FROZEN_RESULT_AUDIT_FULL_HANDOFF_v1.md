Session: DDWMR | LUNA-G2-SCOPE

# G2 W2 v6 final frozen-result audit and resource attribution

**Issued:** 2026-10-08 (Asia/Saigon).  
**Mode:** read-only audit of the already frozen v4 package and its six saved
results.  This turn did not run a query, native replay, producer, worker,
fixture, preflight runner, retry, new stage, legacy study, or resource-cap
increase.  No G4-owned file was edited.

## 1. Finding and scoped disposition

The final v4 package is internally bound and auditable.  The 77-file closure,
final protocol, freeze manifest, freeze receipt, nonquery preflight, ordered
phase receipt, result manifest, six result groups, and the current bytes of the
closure entries agree with their recorded SHA-256 values.  The frozen phase ran
exactly three v6 calls followed by exactly three local-Auer calls, one call per
action and no retry.

The three v6 rows are proof-complete for the declared narrow synthetic task.
`ZERO` and `NOMINAL` are `CERTIFIED_SAFETY_TASK_INELIGIBLE`: collision/contact
predicates pass, but their progress upper bounds are below the common `7/20 m`
lower-bound target.  `ALTERNATIVE` is `CERTIFIED` and meets that target.  These
labels must remain separate; safety certification does not imply task
eligibility.

All three Auer rows are `RESOURCE_LIMIT`.  They stopped before accepting a
full-hold step at the frozen exact-rational intermediate bit cap.  This is an
incomplete proof and a local implementation/profile availability observation,
not a mathematical impossibility result.  The saved evidence therefore
supports the following scoped statement:

- centered-residual G2 contribution: **`NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE`**;
- cross-method result on the three already-consumed development rows:
  **scoped local implementation/profile availability asymmetry** (`v6` eligible
  set `{ALTERNATIVE}`, Auer eligible set empty under the frozen profile), with
  cross-method task utility still **`UNMEASURED_NOT_REFUTED`** and no general
  superiority, speed, or mathematical-impossibility claim;
- confirmation and held-out utility remain unmeasured, because these rows were
  already observed G2 development rows.

The gate statuses remain unchanged: G1 is `PASS_RESTRICTED_REDUCED_MODEL_SCOPE`,
G2/G3/G4 and physical-platform correspondence are `UNVERIFIED`, and the overall
project status is `HOLD`.

## 2. Frozen identity and hash audit

The following hashes were recomputed from the current bytes and match the
assignment pins and the cross-references in the freeze/receipt/result files.

| Artifact | Path | SHA-256 | Audit |
|---|---|---|---|
| Final protocol | `research/autonomous_w2/g4/matched_v6_task_development_v3/protocol_v3.json` | `bd285159ac9067e27338ff81426effde924c2e480c7c05d678ae73262532ef62` | PASS |
| Freeze manifest | `research/autonomous_w2/g4/matched_v6_task_development_v3/freeze_manifest_v4.json` | `067995e0e60873c4c582946444a732ebc9d05eeb16eb1c601173d7ffc7c4a91e` | PASS |
| Freeze receipt | `results/validation/autonomous_w2/g4/matched_v6_task_development_v3/freeze_receipt_v4.json` | `7dbab64e3d3e2279ef10e1198416cf500713ff19a4d4e32444be3f5d1bf56458` | PASS |
| Source closure | `results/validation/autonomous_w2/g4/matched_v6_task_development_v3/source_closure_v4.json` | `4a138dbd9eb26f1ba81f9d6b367c86e57dbce5ceab20d97bba3f4fe201fb7097` | PASS, 77/77 entries |
| Nonquery preflight | `results/validation/autonomous_w2/g4/matched_v6_task_development_v3/nonquery_fixtures_v5/preflight_report_v4.json` | `4e73485b549d357a8b4f9d2e5bb27e0d36849dd3205d977c075928464c5a21ee` | PASS, 74/74 |
| Ordered phase receipt | `results/validation/autonomous_w2/g4/matched_v6_task_development_v3/matched_phase_receipt_v4.json` | `d904e421c62ec02932f9f2d6e146c5571eaae8b736753c16f925c9c0a3a1e994` | PASS |
| Compact result manifest | `results/validation/autonomous_w2/g4/matched_v6_task_development_v3/matched_result_manifest_v1.json` | `d35fc3a804a37f2230d99d45e2f86c4e45c3dfc0c6334b5a5f5bcfd9562604ac` | PASS |

The freeze receipt cross-binds the protocol, freeze manifest, source-closure
path/hash and preflight path/hash.  The phase receipt repeats the protocol,
freeze-manifest and freeze-receipt pins.  The result manifest binds its phase
receipt, freeze artifacts and source closure.  No stale v3 report was used as
the final package identity.

Secondary pins consumed during this audit are:

| Item | SHA-256 |
|---|---|
| G2 release `coordination/autonomous_w2/g2/releases/RELEASE_v6.json` | `789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55` |
| Task protocol `research/autonomous_w2/g4/matched_v6_task_development_v3/g2_task_protocol_v1.json` | `8bc1c8fd460a62dc3f7ff1c8e4bef2dbaddbcaffbadd75d6c2c487e9e311c15a` |
| Native source snapshot map | `6417ee7e27aed8bf95186229c6630f2eb1a828387aa4370119a0f08a1fee75b8` |
| Benchmark v3 | `afb48622180ce526f2c4412a094d696d92dd4c84c2e80a0b8e8507f147c3be94` |
| Auer input manifest v3 | `2fffaf0fbf715ca9943404663c7318992007d5391860dd81f3d95b58207fef20` |
| Auer bindings v3 | `5d43a7dae1498d0806e45b5d5a33e1476d37ce9c1b2542f0f69b6cd5c798bab2` |
| v6 profile | `8252ceecd3a07c9811fd601945d16b9f33318d120340441c3fff94b117ee03a2` |
| Auer profile | `df1af1bc14e99755a46b9a662255419b4d169501496b7e4b71517192e16a90f1` |
| Common profile | `2c1199a71e676fc29c8a44da6e1db45611252dfd678845808b926ed025d178d2` |

The source closure itself has 77 path/size/hash rows.  Every listed path exists;
every current size and SHA-256 equals the closure row.  The preflight report
also contains 10 executable source hashes and 71 input hashes.  Rechecking all
10 + 71 entries produced no missing path or digest mismatch.  The final audit
report and new G2 status files are post-freeze audit outputs and are not
retroactively inserted into the frozen G4 closure.

Key current source identities from that closure are:

| Component | Path | SHA-256 |
|---|---|---|
| v6 worker/setup | `validation/autonomous_w2/g4/v6_w2_worker_v3.py` | `53cb35ad203a2839f4a6a77d51693070652160fcecf7a572b7f3c392e71b0699` |
| v6 adapter | `validation/autonomous_w2/g4/v6_w2_adapter_v3.py` | `b0209eefc47574dd4a7c7acfaaa36ece3cb90ee55b912c6e913e614d429ba5d1` |
| Auer worker/setup | `validation/autonomous_w2/g4/auer_w2_worker_v3.py` | `4e50a92441c9312ca19600b97267ec9e3508d95297cf4ee5a196ef026e7324fc` |
| Auer adapter | `validation/autonomous_w2/g4/auer_w2_adapter_v3.py` | `5b3129906b648e1d9377b9d198fce16a1187a8288cf8e77ff6b623fb269a1bd7` |
| Common scorer/replay | `validation/autonomous_w2/g4/matched_v6_common_v3.py` | `a76eabcb94aff0469e4c5d1af4a7b557272ec2f9a22aac8e7c8540db786c7efc` |
| Full-time tube checker | `validation/g4/common_tube.py` | `564c0ffe608be6d0413def643a5dff7b455613c61b56f0ea42684cc7c6874d25` |
| Bounded phase runner | `validation/autonomous_w2/g4/run_matched_v6_w2_v3.py` | `ea3650973dd6d703e2063f1c887673f93e008dbcab0c07e6659a516673bca281` |
| Nonquery preflight source | `validation/autonomous_w2/g4/preflight_matched_v6_v3.py` | `45f22ecaec639906783c9af4647e3206da686a1cb8eb214320900faa50caca2e` |
| Child supervisor | `validation/autonomous_w2/g4/windows_job_supervisor_v3.py` | `443fda557ef40ea6253996a329bc07f28ed017c134a1114a8bfc8a09880354c0` |

## 3. Frozen task and common predicate

The task is explicitly `G2_W2_VOF_TASK_V1` with state order
`[p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R]`, a positive-width nine-state
initial box, and twelve independent positive-width fixed labels in
`[9999/10000,10001/10000]`.  One label image is reused unchanged for the whole
trajectory and across all slabs.  The clip law is `clip(s,-1,1)` with the
frozen constants and two-second held voltage.  The synthetic static circle has
center `(1/2,1/10)` and inflated radius `3/50`.  The progress rule is

`p_x(T)-p_x(0) = integral_0^T u(t) cos(theta(t)) dt >= 7/20 m`.

The task protocol records this as a formal synthetic target chosen before the
W2 evaluator outputs.  It is not a source-backed mission requirement, physical
operating envelope, or robot deadline.

The saved common records use a total nine-state hull.  The read-only source
audit confirms these checks:

1. Every segment is a positive **closed** time slab; first start is `0` and
   final end is `T`.
2. Adjacent slabs share exactly the previous endpoint enclosure.  Endpoint
   timestamps must equal slab boundaries, and each endpoint must lie inside its
   slab hull.
3. Every slab carries the complete fixed-label image in the declared order;
   labels cannot be narrowed, reordered, reset, or selected per realization.
4. Collision is evaluated on every closed slab against the static circle, and
   contact is evaluated on every closed slab from the slip/contact-capacity
   envelope.  The common checker uses the supplied total hull and does not add
   a second pose/residual radius.
5. Progress is the intersection of the closed-slab integral enclosure and the
   endpoint displacement enclosure.  The scorer rejects an empty intersection;
   it does not silently choose one bound.

The common checker documents an important proof boundary: it audits predicates
on a supplied tube and sets `ode_tube_proof_replayed=false`.  Native method
replay is therefore a separate obligation.  A common `PASS_ON_SUPPLIED_TUBE`
record is not, by itself, a new ODE inclusion theorem.

## 4. Six saved actions and ordered phase receipt

The phase receipt contains exactly six completed bounded children in this order:
v6 `ZERO`, `NOMINAL`, `ALTERNATIVE`, then Auer `ZERO`, `NOMINAL`,
`ALTERNATIVE`.  Each has one counted call, return code 0, a producer marker,
worker/job receipt and no retry.  The lock was released, the runner reported no
errors, and no additional action was added.

### v6 rows

All three v6 rows have method-native replay `PASS`, common replay `PASS`, 256
ordered slabs and 46 recomputed native proof fields.  The intervals and exact
minimum predicate margins below are from the saved result manifest; decimals
are display values only.

| Action / voltage | Canonical physical-input SHA-256 | Progress enclosure (m) | Collision margin lower (m) | Contact margin lower (N) | Final status |
|---|---|---:|---:|---:|---|
| `W2_G4_V6_ZERO` / `(0,0)` | `dc0dcda534dd56e7a1a409977efb5c0565e25c0ca976dcebae189609c4342fa6` | `[0.177582288184, 0.240398241242]` | `0.211762546558` | `1.985219477442` | `CERTIFIED_SAFETY_TASK_INELIGIBLE` |
| `W2_G4_V6_NOMINAL` / `(1/2,1/2)` | `80f15195b6a29757fa4bd03a20acc0f25b82a4f7e946d6f0308984ca9d6bec4b` | `[0.270758520755, 0.333574473811]` | `0.124818706764` | `1.984873966584` | `CERTIFIED_SAFETY_TASK_INELIGIBLE` |
| `W2_G4_V6_ALTERNATIVE` / `(1,1)` | `3d5844de37384fa3f0b52b1cea6a7580f42d1b4fd84fbc2e857e5aecc593d0bb` | `[0.363934753325, 0.426750706380]` | `0.048738648906` | `1.958480522039` | `CERTIFIED` |

The first two upper bounds are below `0.35 m`; they are not failed safety
certificates.  The alternative lower bound is above `0.35 m`, so the exact v6
verified eligible set is `{W2_G4_V6_ALTERNATIVE}`.

The saved native-row SHA-256 values are, in order, zero
`3ef3ee1ef7a329a54268e6c383184c4fad41c950f02a60d245e3763bff335b51`, nominal
`a11a6d4a038dfb3ed92136115a42df45e92868a4991242f61bf3440340d6b5c3`, and
alternative `5288c6ca8f7a06539c7f23e9b83820b6004b7d25d4da2a6efc3671d1c1dc2241`.
Their common-record hashes are respectively
`a56371746ace86b2a81d14195df653035fcb5cc6d519ef35cd3a98cdda99a63d`,
`dd7206474a0e3cb2dc8df1b8f7cbf5a039bbd0f6d340132866743c4d0f2bad3e`, and
`5a6cd60a2a73509b7e7852c86fd64452e28023b2eed6b2e6945346e4fc636f3f`.

### Auer rows

Each Auer worker wrote a structured native proof/termination record and returned
`RESOURCE_LIMIT`; none produced `PROOF_COMPLETE`.  Consequently there is no
Auer native replay, common full-hold replay, progress record, or task-eligible
set to score.  The empty Auer set means “no certificate verified under this
frozen producer/profile pipeline,” not that the underlying mathematics cannot
certify an action.

| Action / voltage | Native proof file SHA-256 | Status | Common/native replay |
|---|---|---|---|
| `W2_G4_AUER_ZERO` / `(0,0)` | `7cb6e2de2def168ccec006d6119d691ddae3490b5e256524acfd420c0c4735b1` | `RESOURCE_LIMIT` | `NOT_RUN_NO_PROOF_COMPLETE_CERTIFICATE` |
| `W2_G4_AUER_NOMINAL` / `(1/2,1/2)` | `62c70f27d8fd08397b5600de273bbec6349abac06389da9d61ce6c4fa3900511` | `RESOURCE_LIMIT` | `NOT_RUN_NO_PROOF_COMPLETE_CERTIFICATE` |
| `W2_G4_AUER_ALTERNATIVE` / `(1,1)` | `4506bbbf0b2a89143bc27566467d355ef978dc72364ff58879d3a74dc26f5472` | `RESOURCE_LIMIT` | `NOT_RUN_NO_PROOF_COMPLETE_CERTIFICATE` |

The worker-result hashes are zero `2e41673d613872e3d10882947871205028667c8a95531f0ef763bf24bd34ba16`, nominal `3ed33d6bea26ad4c8daefeb35b5f8d304818b5bd45ac7f09435d2256df88b2c8`, and alternative `2de8b1a94cb1e6d147a18e02e7f0f87ac559db3bbed6a971bbcb3081148068f7`.

## 5. Resource attribution for Auer

The frozen Auer profile is an exact reduced-rational/Taylor/Picard residual
reconstruction with `max_rational_bits = 32768`.  It is not the VALENCIA binary
and must not be described as a speed or mathematical-complexity comparison.

| Action | Pre-operation estimate / cap (bits) | Maximum completed/observed result (bits) | Accepted steps | Picard / RHS-Jacobian | Rational operations |
|---|---:|---:|---:|---:|---:|
| zero | `33327 / 32768` | `32167 / 32167` | `0` | `30 / 34` | `426577` |
| nominal | `33327 / 32768` | `32167 / 32167` | `0` | `30 / 34` | `426577` |
| alternative | `33285 / 32768` | `32134 / 32134` | `0` | `30 / 34` | `426577` |

Each run attempted the first full-hold step of width 2 seconds and recorded one
rejected step attempt.  The bit-limit check was raised before a proof-complete
step could be accepted, after 426,577 operations started, 424,707 completed
rational results and 426,578 operation attempts in the resource diagnostic.
The outer process stayed within the declared worker CPU, wall and memory limits.  The structured
diagnostic identifies primitive `fraction.pow`; its caller/stage is explicitly
`unclassified`.  This audit does not infer a more specific caller.

The frozen solver policy halves a step only after a completed native
Picard/inclusion failure.  The saved control flow returns `RESOURCE_LIMIT`
immediately when the arithmetic budget raises its resource exception, so no
halving or retry occurred in these rows.  This explains both the zero accepted
steps and why these records are incomplete proof outcomes rather than
inclusion failures.

## 6. Setup routes, adapters and scorer audit

The final source closure pins the actual v3 worker modules and adapters.  A
read-only inspection of those pinned bytes found the following behavior.

### v6 route

`validate_v6_setup` checks the authoritative freeze/receipt/closure paths and
hashes, actual worker module routes, profiles, protocol and benchmark, the
three-way ordered action bijection, outer binding path/hash pairs, peer saved
row and core binding, source pins, full fixed-label image, task protocol,
positive-width initial box, horizon, scene and voltage.  The v6 worker writes
its producer marker only after this setup returns.  The adapter then checks the
native row schema, action/protocol/profile hashes, full label image, symmetric
voltage restriction, all 256 slab records, start hashes, endpoint hashes and
the final `[0,T]` coverage.  It forms one total hull per slab and marks it
`NATIVE_TOTAL_HULL`, so the common scorer does not expand it again.

### Auer route

`validate_auer_setup` checks the same authoritative freeze/receipt/closure and
actual-worker route, profile/guard/source-snapshot pins, benchmark/task
agreement, three canonical case mappings, physical-input digest, action voltage,
initial box, fixed labels, horizon, scene, parameter cell and native-case
bytes.  Its producer marker is written only after setup.  The Auer adapter
accepts only a byte/semantic-digest-matching `PROOF_COMPLETE` envelope, requires
nonempty step records, chains adjacent endpoints exactly, and requires the
first/last records to cover the closed hold.  The three saved Auer envelopes
fail that status precondition by being `RESOURCE_LIMIT`, so no adapter path was
claimed for them.

### Common route

The common scorer checks every closed slab for collision and the reduced contact
capacity margin, retains the complete fixed-label image, verifies endpoint
containment and adjacency, serializes the total hull, reopens it, and replays
the supplied predicate record.  It separately recomputes the progress record
from all serialized slabs and endpoint boxes.  The final progress interval is
the declared intersection of the slab-integral and endpoint bounds.  An empty
intersection raises an input error.  This route provides a semantic predicate
check over a supplied enclosure; it does not replace native ODE inclusion proof.

## 7. Nonquery preflight and mutation evidence

`preflight_report_v4.json` records `PASS_NONQUERY_FIXTURES`, 74/74 checks,
`native_calls=0` and `numeric_producer_calls=0`.  It invoked three v6
producer-entrypoint stubs and three Auer solver stubs; any producer marker
created in this report is fixture-only.  The 74 cases divide into 41 positive
setup/route/scorer/classification checks and 33 `PASS_REJECTED` mutation checks.

The rejection set covers missing/wrong saved-row and core hashes, path escape,
wrong action and physical digest, changed peer release/source pins, duplicate
or missing mappings, stale freeze/receipt/closure/profile references, Auer
case path/digest/voltage/initial-box/label/horizon/scene/parameter-cell changes,
missing native binding fields, and the common scorer’s omitted/gapped slab,
altered label image, tampered contact, tampered progress, wrong horizon and
wrong initial-state records.  All 33 rejected cases report no producer marker
and zero producer-stub-call delta, so they failed before the marker boundary.

Runner fixtures also distinguish valid completion, proof-complete `UNKNOWN`,
explicit arithmetic/worker/supervisor resource outcomes, binding or replay
failure, ambiguous child exit and nonzero exit text that happens to contain
`LIMIT`.  `RESOURCE_LIMIT` is not inferred from an exception string alone.

The fixture package is not exhaustive mutation coverage.  It does not mutate
every native arithmetic coordinate or every per-slab proof field, has no
dedicated collision-margin-only tamper fixture, does not produce a completed
Auer proof for adapter/common replay, and does not prove the upstream ODE
inclusion merely by passing the common scorer fixture.  The common replay
recomputes collision margins from the serialized state hull; the missing
collision-only fixture is a test-coverage limit, not a claim that collision
values are trusted without recomputation.  These limits remain explicit rather
than silent evidence upgrades.

## 8. Accounting and preserved limits

| Work item | Final accounting |
|---|---:|
| G2 native development | `24/24 consumed` |
| G4 candidate worker attempts | `4/12` including the historical preproducer failure |
| G4 corrected v6 native calls | `3` |
| G4 corrected Auer native calls | `3` |
| G4 confirmation rows | `0/24` per method |
| Legacy R5 study | `800/800 NOT_RUN` |
| Legacy Auer batch | `1,944 NOT_RUN` |
| New calls added by this audit | `0` |

The G2 release, v6 rows, historical failed phases, old receipts and G4 final
artifacts remain untouched.  No branch switch, reset, cleanup, commit or push
occurred.  This report and the new G2 status are coordination outputs only.

## 9. Final G2 handoff decision

The final frozen package is accepted as a bounded, hash-consistent development
record for its exact synthetic scope.  It does not pass G2 or G4, establish a
useful recursive subset, establish physical tire/support correspondence, or
justify a controller/hardware claim.  The v6-versus-Auer difference is
attributable to the disclosed local exact-rational resource profile on these
three consumed rows.  It is not a generic method ranking, timing claim,
mathematical impossibility result, or held-out task-utility result.

No further numerical work belongs in this W2 package.  Any future study must
first freeze a defensible task and primary criterion, supported method-specific
input adapters, unused input IDs/digests, source closure and matched resource
policy.  It must preserve the same full-hold collision/contact and progress
intersection semantics and keep `CERTIFIED`, safety-task-ineligible,
proof-complete `UNKNOWN`, `RESOURCE_LIMIT`, audit failure and `NOT_RUN` as
distinct outcomes.

**Final status:** `HOLD`; G1 `PASS_RESTRICTED_REDUCED_MODEL_SCOPE`; G2/G3/G4 and
physical-platform correspondence `UNVERIFIED`.
