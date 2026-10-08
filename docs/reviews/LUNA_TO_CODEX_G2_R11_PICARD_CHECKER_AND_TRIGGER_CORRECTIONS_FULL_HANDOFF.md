Session: DDWMR | LUNA-G2-SCOPE

# G2 R11 Picard checker, trigger, and one-shot runner — full handoff

**Date:** 2026-10-04  
**Assignment:** `docs/CODEX_TO_LUNA_G2_R11_PICARD_CHECKER_AND_TRIGGER_CORRECTIONS.md`  
**Disposition:** checker and paired-decision defects corrected in the R11 namespace; a source-bound runner, independent receipt checker, schemas, and source closure are prepared. This is still an unreviewed, unauthorized candidate.  
**Execution:** 0 R11 row evaluations; 0 native query calls; 0 R6 input evaluations; R5 remains 800/800 `NOT_RUN`. No commit, push, or branch switch.

## 1. Scope and result

The R10 review’s two implementation blockers are addressed without overwriting its reviewed files:

1. The R11 checker now uses the exact interval image of the monotone saturating clip on both fully saturated and corner-crossing intervals. It applies that enclosure in the interval RHS and the contact reserve calculation.
2. The paired decision rule is now one exact 36-row truth table. It has one and only one broader-study preparation trigger: both actions have checked safety certificates, the positive action is task-eligible, and the nominal action is safety-certified but not task-eligible. Positive-certified versus nominal `UNKNOWN` stays inconclusive and does not trigger broader-study preparation.

The R11 source-bound two-row runner and independent receipt/checker path are prepared but were not run on either real R10 row. The only runner calls exercised were injected synthetic callbacks in temporary directories. The public runner was also invoked with the checked-in authorization template and rejected it before creating the R11 results directory.

This is not a new safety or voltage-usefulness result. The R10 conditional whole-hold Picard theorem and reduced-model assumptions remain the mathematical scope. G2 remains `UNVERIFIED`; physical-platform correspondence remains unverified; no gate is promoted.

## 2. Saturating clip correction and proof scope

For the unchanged clip law

\[
\kappa(x)=\min(1,\max(-1,x)),
\]

monotonicity gives the exact image of any nonempty interval \([a,b]\):

\[
\kappa([a,b])=[\kappa(a),\kappa(b)]
=\left[\min(1,\max(-1,a)),\min(1,\max(-1,b))\right].
\]

The endpoint map preserves order. Intersecting \([a,b]\) with \([-1,1]\) does not compute this image when the interval lies wholly outside the clip domain and can construct a reversed interval.

| Normalized slip interval | Correct clipped image |
|---|---|
| `[3/2, 2]` | `[1, 1]` |
| `[-2, -3/2]` | `[-1, -1]` |
| `[4/5, 6/5]` | `[4/5, 1]` |
| `[-6/5, -4/5]` | `[-1, -4/5]` |

In the RHS, the corrected image encloses each force term \(C_j\kappa(S_jz/v_s)\) on the candidate box, including a fully saturated branch. In contact replay, the corrected clipped interval gives \(\beta_j=\sup|\kappa(\sigma_j/v_s)|\in[0,1]\); a fully saturated interval yields \(\beta_j=1\) and a zero lower lateral-reserve term \(\underline C_j\sqrt{1-\beta_j^2}=0\). That may leave contact unproved and produce `UNKNOWN`; it is not a malformed interval or a finding of physical contact failure.

The R11 checker independently rebuilds all slabs, RHS images, closed-box Picard inclusions, endpoints, pose tubes/carries, contact and collision bounds, progress, and status. It matches the R10 producer’s deterministic RHS addition order, \((BV+Az)+DF\). Producer and checker still share the audited rational interval primitives and `ModelIntervals` parser; the trajectory transition, proof checks, carry, geometry/contact aggregation, and record comparison are separate implementations. The shared primitives and parser remain a review surface.

The inherited conditional proof remains: for each fixed voltage and one fixed joint parameter label, an exact interval RHS enclosure \(G_k\) on \(B_k\), together with \(X_k\subseteq B_k\) and \(X_k+[0,h_k]G_k\subseteq B_k\), makes the Picard map self-mapping on the closed slab. The uniform fixed-label Lipschitz upper bound \(L\) and Bielecki parameter \(\lambda=L+1\) give contraction factor at most \(L/\lambda<1\). Each endpoint is enclosed by \(X_{k+1}=X_k+h_kG_k\); exact contiguous slab durations sum to the complete hold. Pose endpoints are carried between slabs, and collision/contact sufficient bounds and additive progress are checked on every slab. The claim is conditional on the R10 interval-RHS, positive-denominator, fixed-label, and unchanged reduced-model assumptions. It does not establish physical tire/support correspondence.

## 3. Synthetic whole-record evidence

`validation/scripts/verify_g2_r11_picard_fixtures.py` passed all 17 declared non-query groups:

- The two-slab synthetic whole-hold record replayed as `CERTIFIED` and task-eligible.
- The adaptive case used one binary split node, produced two accepted half-slabs, and replayed as `CERTIFIED`.
- A 10-operation cap produced an `UNKNOWN` record that independently replayed as `UNKNOWN`.
- At the exact observed cap of 4,534 rational operations, producer and checker both completed and the checker accepted the full record as `CERTIFIED`. This demonstrates matching operation accounting at that declared fixture boundary; it does not guarantee that other inputs complete within their caps.
- Seventeen negative/mutated binding cases were rejected.

Four additional **whole-record** synthetic cases exercised RHS and pose/contact replay at saturation. Each produced one complete slab with producer status `UNKNOWN`; R11 independently replayed each as a valid `UNKNOWN` record:

| Fixture | Replayed normalized left-slip interval | Producer | Independent replay |
|---|---:|---|---|
| Wholly above `+1` | `[959507/640000, 960493/640000]` | `UNKNOWN` | `UNKNOWN`, replayed |
| Wholly below `-1` | `[-960493/640000, -959507/640000]` | `UNKNOWN` | `UNKNOWN`, replayed |
| Crosses `+1` | `[639379/800000, 960621/800000]` | `UNKNOWN` | `UNKNOWN`, replayed |
| Crosses `-1` | `[-960621/800000, -639379/800000]` | `UNKNOWN` | `UNKNOWN`, replayed |

These are interval/checker contract fixtures only. They are not R6 results, physical safety evidence, or voltage-necessity evidence.

## 4. Predeclared paired decision rule

The fixed row order and prior lineage remain R5 index 12 at \((0,0)\), followed by R5 index 24 at \((+1,+1)\). Both are development-overlap rows, not independent tests. The progress threshold remains \(1/20\) m.

| Positive action \((+1,+1)\) | Nominal action \((0,0)\) | Interpretation | Prepare a broader study protocol? |
|---|---|---|---:|
| `CERTIFIED_TASK_ELIGIBLE` | `CERTIFIED_TASK_NOT_ELIGIBLE` | Strong two-safe-action task-certification separation: both have safety certificates; only positive has a sufficient progress lower bound at threshold | **Yes, preparation only** |
| `CERTIFIED_TASK_ELIGIBLE` | `VALID_UNKNOWN` | One certificate versus one valid abstention; inconclusive | **No** |
| Either row is `RESOURCE_LIMIT`, `INVALID_OR_INTERRUPTED`, or `NOT_RUN` | Any class | Stop or incomplete pair; no decision outcome | **No** |
| Any other valid pair | Any valid class | No predeclared task-selection separation | **No** |

The manifest binds the complete 36-combination table and exactly one true trigger. `UNKNOWN` is never treated as unsafe or task-ineligible. A safety-certified but task-ineligible result only means the sufficient progress lower bound did not establish the threshold; it does not prove actual task failure. Even the strong synthetic trigger grants no study execution authority. The rule was bound before any R11 result, and no real R11 result was observed.

## 5. Source-bound runner and independent receipt path

The prepared entry point is `validation/scripts/run_g2_r11_picard_stage.py`; its only accepted result path is `results/validation/g2/decision_domain_r11_whole_hold_picard_v1/`. It invokes the offline R10 producer through `validation/scripts/run_g2_r11_picard_row_worker.py`; it has no native evaluator call. The worker reloads the exact source-bound row, closure, manifest, and query hash before producing a record.

A future run requires a separate GO authorization matching `research/benchmarks/G2_R11_EXECUTION_AUTHORIZATION_SCHEMA_v1.json`. It must pin the exact R11 manifest and closure hashes, both row indices/query/input hashes in order, zero study rows, zero native-query authority, at most two row calls, a 35–60 second outer worker timeout, and a Codex review path/raw hash that the runner rechecks. The only checked-in authorization is `TEMPLATE_ONLY`; it cannot pass the runner’s gate. No real GO object or `authorization.json` was created. The synthetic GO object used in protocol fixtures existed only in memory and referenced a temporary synthetic review file.

Before a future worker starts, the runner writes and flushes the exact authorization copy, then writes an exclusive source-bound intent with manifest, closure, authorization, query/input, R5, and consumed R6 hashes. It flushes the intent and parent directory before starting the worker. It never overwrites an intent. A valid replayed `UNKNOWN` is a completed abstention and may be followed by row 24. A rational resource-limit record, outer timeout, worker failure, invalid replay, mismatch, or interrupted intent stops the pair. If a process stops after an intent without a terminal, the receipt checker reports `STOPPED_INTERRUPTED`; a later runner invocation refuses to call that row again.

Terminals bind intent and record hashes. The independent public audit has no candidate-injection argument: it reloads the R11/R10/R6/R5 lineage, checks the copied authorization and review hash, validates each intent/terminal/record, replays available records, preserves the 800-row R5 denominator and two consumed R6 observations, and derives the decision from the bound truth table. Each actual receipt will bind the manifest, closure, and authorization raw hashes. `G2_R11_STAGE_RECEIPT_SCHEMA_v1.json`, `G2_R11_ROW_INTENT_SCHEMA_v1.json`, and `G2_R11_ROW_TERMINAL_SCHEMA_v1.json` define those records. An R10 manifest is not an execution receipt.

Nine synthetic stage-protocol fixtures passed: durable intent was visible before the worker callback; a valid `UNKNOWN` did not block the second prescribed row; resource-cap `UNKNOWN` and timeout were distinct resource stops; interrupted intent was not retried; the sole strong trigger remained preparation-only; a changed receipt was rejected; the inert template was rejected; and the independent authorization checker accepted a synthetic review binding then rejected a changed review file hash.

## 6. Read-only row audit and preserved lineage

`validation/scripts/audit_g2_r11_candidate_manifest.py` passed using source/hash reads only. It reconstructed the two exact query bindings and their already-consumed R6 observations; it did not call the producer or native query evaluator.

| Order | R5 index | Query | Canonical query SHA-256 | Input payload semantic SHA-256 | Preserved R6 outcome | R6 evaluation SHA-256 | R6 terminal SHA-256 |
|---:|---:|---|---|---|---|---|---|
| 0 | 12 | `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_L0_R0` | `d5648569b11c576c8cc0ecb07c5096c21b06fe3a5e849358f254770649465471` | `422afd0448a184f4f67262c6338593c871739b41fb677e8ab1d6b566d18b93ac` | Consumed `UNKNOWN` | `8d8f48d4c8bd3c6840d09ed32579e3796f81499e58b7a8ed60fba3b825487306` | `9d4efa58c94903031c04ffa84ac6c6b9712f55e29466b931021e36e6326e3e78` |
| 1 | 24 | `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lp1_Rp1` | `105a0710185446312933ec8c92922acd1db0f3af0e999d67207ccd70534b4808` | `70301bc5df76aab2dfdb8bef5135592fbf0063af6799b0f0eb119f4873b2cf9a` | Consumed `UNKNOWN` | `d93419ed11d68082c1f6676468326e88e66913d871c8edf1e37f003076686ece` | `414a20e0958653a5ac103ce99e6b654c8c32931c713259e17b593edcf261064` |

R5 manifest raw SHA-256 remains `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b`; its 800 rows remain `NOT_RUN`. The consumed R6 publication raw SHA-256 remains `3e55c3b967b661f3a3c3b5aa70ae4bc7cf8e9bab463ec484a4e5865f3db5b33d`. No R6 rows were rerun.

## 7. Source identities and preservation checks

The R11 closure directly rehashes 186 sources: all 163 entries from the reviewed R10 closure plus 23 R11 additions. The R11 source audit found no path/hash mismatch. The R10 parent manifest, closure, producer, and checker still have their reviewed raw hashes; the R11 builder verified every direct parent source entry against the current bytes.

| Artifact | Raw SHA-256 |
|---|---|
| R11 candidate manifest | `9ed8c4709c7b398702d73877bfe32c58ca7097777bab08ee7b67e3055cb8708a` |
| R11 candidate manifest semantic JSON | `22a3f87ace14ac8dc17db9dd665370b46588791e1b670aba53dd8c41974c1a6a` |
| R11 direct source closure | `6b4f1e144a7e9384e9c13f8e7edd8c67be41b97b3283f59de793886e32ae6f1e` |
| R11 source closure semantic JSON | `434bdfc6a8467f1549a884e605e27a310e5598fa9cb28ae0b2f66147072b4bc3` |
| R11 closure sidecar | `e44acff3054d2a470d88c414d125096cd9dbdbe60bbc834b44e12b385b25689e` |
| R11 Picard contract | `0cfdf79dc0ee6b5a054aaab42f22772e2db863339c466a227b4b267dd574fc8f` |
| R11 independent Picard checker | `2a794e8f46c4b029331a2548dccd1948b78d3f5d5d7a96efa118d9353ba56f7e` |
| R11 source binder | `174eca55af421dff4d3fb167e5ee4663c843035a3acb8cf351ba96fd3f31249a` |
| R11 independent receipt checker | `d613a3375d7c4c9de97392587195b09226c2d510da63ee8e81586acb350fe3a0` |
| R11 one-shot runner | `3980452e08ac5453acff7d2fc446dee6dd6db181788e5cfd91bf00dc35476b5f` |
| R11 source closure builder | `e5fe05b2af13d6757b1fc693b39864fd88a995fa91689a944d43d94ef0537331` |
| R11 read-only manifest audit | `39a126843f15f4f1add77fe7960a580ed73f99153faa177c7f727ce589c4f4ab` |
| R11 synthetic stage-protocol fixtures | `989367da6aa937df9b56deb7524ee75215d587d1eb6a2be55f6718c25c973a18` |

Preserved R10 identities: candidate manifest `0bddb54bc0c2ab97687921e44bb5f376807250277bd10192d70551f062fbd9e5`; source closure `63a7af65317b683345c54a0bc377935cf907260a944d1b1234473193fcedf6d9`; producer `e9fa6672649d675e27bb4f419e28259b9546b01bb6592f3388396ecd2a211c47`; checker `6ba67a808bc9e5125cbf8112265c3a074a9b005566ef02d06e6121825e150783`. R3/R5/R6 sources and stored R6 observations remained unchanged through parent-closure rehash. No G4 source or manifest was edited.

## 8. Verification, limits, and next gate

Executed and passed:

1. `python -B validation/scripts/verify_g2_r11_picard_fixtures.py` — 17 synthetic groups, including four saturated whole-record replays.
2. `python -B validation/scripts/verify_g2_r11_stage_protocol_fixtures.py` — 9 synthetic intent, stop, authorization, and receipt checks.
3. `python -B validation/scripts/build_g2_r11_source_closure.py` — 186/186 direct sources matched; 163 inherited, 23 added.
4. `python -B validation/scripts/audit_g2_r11_candidate_manifest.py` — exact R5 12 then 24 lineage; one strong trigger row; weak certificate-versus-UNKNOWN trigger false; 0/2 R11 rows run; 800/800 R5 rows not run.
5. AST parsing of 11 R11 Python files and JSON parsing of 9 R11 manifests/schemas/configurations — passed.
6. Public runner check with `G2_R11_EXECUTION_AUTHORIZATION_TEMPLATE_v1.json` — rejected with `AUTHORIZATION_NOT_EXACT_GO_FOR_CURRENT_CANDIDATE` before stage creation; R11 result directory remains absent.

No R10 real row, native query, R6 rerun, or 800-row study was run. No R11 row result or execution receipt exists. No physical-platform, useful-voltage-selection, voltage-necessity, or G2 PASS claim follows from these synthetic checks. No source or manifest under G4 was edited; no branch switch, commit, or push was performed.

The next gate is Codex review of this exact R11 closure, corrected checker, trigger, runner, and receipt checker. Only a later separate exact-scope GO authorization can permit the two locked offline row evaluations. R5 must remain 800/800 `NOT_RUN` unless separately authorized.
