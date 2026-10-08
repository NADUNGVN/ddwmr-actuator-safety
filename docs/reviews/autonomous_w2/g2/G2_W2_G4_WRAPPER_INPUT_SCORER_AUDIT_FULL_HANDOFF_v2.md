Session: DDWMR | LUNA-G2-SCOPE

# G2 W2 handoff v2 — actual G4 wrapper/input/scorer audit and v6 receipt erratum

**Date:** 2026-10-08 (Asia/Saigon). **Disposition:** PARTIAL; G4 v3 revision required before freeze or producer. **Audit mode:** source/data/hash inspection only. G2 did not run a query, worker, producer, fixture, replay, preflight runner, stage, or study.

## 1. Result and peer coordination

G2 completed the requested actual wrapper/input/scorer audit for the current G4 v3 candidate and sent actionable findings in [the G2 peer audit memo](../../../../coordination/autonomous_w2/g2/G4_WRAPPER_INPUT_SCORER_AUDIT_v2.md). The exact 57-file observation is bound by [the refreshed source/input inventory](../../../../coordination/autonomous_w2/g2/G4_V3_WRAPPER_INPUT_SCORER_HASH_INVENTORY_v2.json), SHA-256 82aed0bc3ceeb335a459e1f5ceadb05ac0830ea4e7056ac62d512b59e66cacbd.

**The current v3 candidate is not ready to freeze or run.** Its Auer setup validator deterministically rejects each mapped action because the manifest's semantic-object hashes omit a trailing LF while canonical_sha256() appends one. The same mismatch affects both physical-input digests and legacy payload digests. Independently, the protocol and Auer manifest benchmark pins are stale, and the Auer binding document has a stale top-level native-source-snapshot pin. The current preflight source reaches Auer's real worker setup for all three action routes with a solver stub, but has no Auer-specific mutation cases; the observed valid route is expected to fail at the physical digest check before reaching the stub.

G4 STATUS sequence 8 was observed at SHA-256 06d77d3ed5cdb942c92df5826d0d2c80f4eac0dac6caee871685e0569bd4c309; it remained ACTIVE and its next action still named nonquery fixtures and freeze. No v3 freeze manifest, receipt, source closure, or preflight report existed at this audit boundary. G2 wrote the comments under its own prefix for G4 to correct and continue.

## 2. Corrections since the prior G2 draft

The prior audit memo and this handoff are superseded for current-source findings by v2. The following current-source changes are recognized:

- V6's preproducer validator now binds the outer action, saved G2 row, core binding, voltage, task/profile information, and label order. Its task-eligibility gate now requires the native certificate, strict clip-interior proof, full-hold coverage, common-predicate pass, and progress.
- Auer now has a shared validate_auer_setup() called by its worker before producer_start.json. The validator checks the reconstructed canonical task mapping, action/case bindings, label image, task scene, hold and source/proof pins.
- Common semantic replay now receives expected horizon and initial state from the task and rejects serialized differences before recomputing.
- Runner summaries now preserve actual v6/Auer timing and work keys, including common replay/progress time, total worker time, stage_seconds, adapter_work, and resource_work.
- Current preflight source now imports Auer and exercises the valid worker route for all three actions with its numeric solver replaced by a fail-if-called stub. The prior statement that Auer setup was not invoked is stale.

These are source-review findings only. G2 did not run the G4 preflight or a fixture.

## 3. Exact input and digest audit

The three semantic mappings were confirmed by exact rational values and direct file reads:

| Pair | G2 action | Voltage | Declared semantic physical-input digest |
|---|---|---:|---|
| W2_G4_V6_ZERO / W2_G4_AUER_ZERO | W2_G2_DEV_001_ZERO | (0,0) | dc0dcda534dd56e7a1a409977efb5c0565e25c0ca976dcebae189609c4342fa6 |
| W2_G4_V6_NOMINAL / W2_G4_AUER_NOMINAL | W2_G2_DEV_001_NOMINAL | (1/2,1/2) | 80f15195b6a29757fa4bd03a20acc0f25b82a4f7e946d6f0308984ca9d6bec4b |
| W2_G4_V6_ALTERNATIVE / W2_G4_AUER_ALTERNATIVE | W2_G2_DEV_001_ALTERNATIVE | (1,1) | 3d5844de37384fa3f0b52b1cea6a7580f42d1b4fd84fbc2e857e5aecc593d0bb |

For each action, semantic object values agree with the saved G2 row, the nine-state positive-width initial box, twelve positive-width fixed labels, two-second hold, static inflated circle, and selected voltage. The problem is the digest encoding, not those semantic values.

auer_w2_adapter_v3.canonical_sha256() hashes sorted compact UTF-8 JSON plus LF. Existing canonical_physical_input and payload_sha256 entries use compact JSON without LF. Thus all three physical digests differ from the helper's recomputation, and all three payload digests differ as well. The worker compares the physical value at auer_w2_worker_v3.py:315-323, then the payload value at :338-342. The current first Auer case is therefore rejected as AUER_ACTION_PHYSICAL_DIGEST_MISMATCH:1; correcting that comparison alone exposes AUER_LEGACY_PAYLOAD_HASH_MISMATCH.

Required correction: select and document one canonical-byte convention, regenerate semantic digest fields and every dependent action, manifest, case, binding, protocol, freeze, and source-closure pin together, and add known-answer digest fixtures. Do not copy hash strings between conventions.

Additional provenance mismatches:

- Actual benchmark_v3.json SHA-256: afb48622180ce526f2c4412a094d696d92dd4c84c2e80a0b8e8507f147c3be94. The protocol benchmark pointer and Auer manifest benchmark pin both say 6bdc22747e8248b1ae5eb7141c5fea0f8020e14a4e8b85529d38461bad7546f1, while all three native case files point to the actual afb486... bytes.
- Actual native_source_snapshot_v3.json SHA-256: 6417ee7e27aed8bf95186229c6630f2eb1a828387aa4370119a0f08a1fee75b8. The top-level Auer bindings pointer says da932a19834aeea91a0bc8090db550225566a57b90813cdc981e48f405761e11; each of its three nested method bindings says the actual 6417... hash. The worker checks nested values but not the stale top-level pointer.

Rebuild all dependent hashes only after choosing the corrected source/input bytes, then freeze the exact resulting closure.

## 4. Wrapper, scorer, fixture, and resource findings

### Wrapper and eligibility

V6's current validation now addresses the previous action/saved-row checks. Its eligibility formula no longer treats common geometry as method proof: native_certificate_valid requires replayed CERTIFIED, strict clip interior, and contiguous full-hold coverage; safety_pass also requires common predicate and common replay. Auer reconstructs expected task semantics and runs native proof replay before common scoring. These corrections do not repair the digest/provenance blockers above.

### Common scorer

Static source audit confirmed conservative logic on a valid supplied tube: complete closed-slab coverage, no gaps/overlaps, identical adjacent endpoints, initial-set inclusion, unchanged fixed labels, full-slab collision/contact checks, no second radius expansion, and a progress enclosure intersecting slab integration with endpoint displacement while rejecting an empty intersection. replay_common_record_semantics() now checks its serialized horizon and initial state against frozen expected values.

The scorer does not prove an upstream ODE inclusion or create a method-native certificate. Its Fraction/interval arithmetic and the G2-native replay dependencies are shared trust and should not be described as independent arithmetic implementations.

### Nonquery tests still needed

The current G4 preflight source has valid-route stubs for v6 and Auer, but the mutation list only changes v6 binding/freeze/protocol inputs. No Auer mutations exercise stale/missing path or digest, action/voltage mismatch, duplicate or missing mapping, stale closure/receipt, changed state/label/scene/hold, or source snapshot mismatch. The common replay's expected horizon/initial-state checks and the v6 native-certificate eligibility gate also have no current preflight mutation case. G4 should add these as fixture-only assertions, with producer/replay calls stubbed, and assert invalid cases do not create a producer marker. No preflight report was present; G2 did not create one.

### Memory classification

The Windows job config applies a process/job memory ceiling and records peak memory. Its reason classifier explicitly identifies wall, CPU, and output caps; other terminated-child outcomes become JOB_LIMIT_OR_CHILD_FAILURE. The runner treats this ambiguous outcome as a stop, not as confirmed resource exhaustion. That is conservative. G4 should either add OS-level evidence that uniquely identifies a memory cap event, or keep it ambiguous and report it separately; a high peak alone must not be promoted to a confirmed memory-limit stop.

## 5. Completed v6 receipt erratum

The existing [v6 terminal-attempt receipt erratum](V6_ATTEMPT_RECEIPT_SCHEMA_ERRATUM_v1.md) is complete as an interpretive correction. G2 rechecked its four exact historical receipt hashes:

| Object | SHA-256 |
|---|---|
| Zero terminal attempt_receipt.json | 3a4cdb69facdd07b4be3126114e467f8dcb58ea91d1af7a7ad93852b03f87f83 |
| Nominal terminal attempt_receipt.json | 13a27d0af11db3c3080e3c695225dbf4fa9b68db1331fb39c992709c132186a5 |
| Alternative terminal attempt_receipt.json | 83c19513e4b48bd6aa18e9521369366799d359e5ed740ec1771d993dd5e1fa7b |
| Stage receipt containing the three nested terminal records | 9b906c008af8ff51f92bb55d4f1fe072f9a4ebdc48f4caf64c29feec58f0aa36 |

Each terminal record contains status REPLAYED but carries the launch-intent label G2_W2_V6_ATTEMPT_INTENT_v1; the distinct attempt_intent.json files remain intent records. Preserve all historical bytes and use the erratum interpretation downstream. No replacement schema identifier is invented because the historical contract did not declare one. A future producer revision should declare a distinct terminal-receipt schema.

## 6. Hash-bound source table

All entries below are in the 57-entry inventory v2. The full table includes transitive arithmetic/scorer sources, snapshots, bindings, G2 saved rows, and the stopped v2 execution evidence.

| Path | SHA-256 |
|---|---|
| validation/autonomous_w2/g4/v6_w2_worker_v3.py | a665d7a55e27b85eafaf45c4ecb0d83f500f7ae893f4f2ddfa8ee2fb112ceb9e |
| validation/autonomous_w2/g4/auer_w2_worker_v3.py | f364e7952f626f3e59dd56d66dc6475095c7632c04fe0aa5065169e8338a1a8e |
| validation/autonomous_w2/g4/preflight_matched_v6_v3.py | 161b2b23d8e1c2bfb4deab8ccee9aa848437f2861c43bcce4eb8ec5c8b18735c |
| validation/autonomous_w2/g4/auer_w2_adapter_v3.py | 21622bddf9060bea6066841dff95454f49c157e923cba6da8b2004e0b11b7cbd |
| validation/autonomous_w2/g4/matched_v6_common_v3.py | fb9d39d3a262210fd45d53863533359ca55e8a8778c32c4c12bff8e95ef5b46b |
| validation/autonomous_w2/g4/run_matched_v6_w2_v3.py | ea3650973dd6d703e2063f1c887673f93e008dbcab0c07e6659a516673bca281 |
| validation/autonomous_w2/g4/windows_job_supervisor_v3.py | 443fda557ef40ea6253996a329bc07f28ed017c1341a1114a8bfc8a09880354c0 |
| validation/g4/common_tube.py | 564c0ffe608be6d0413def643a5dff7b455613c61b56f0ea42684cc7c6874d25 |
| research/autonomous_w2/g4/matched_v6_task_development_v3/protocol_v3.json | 4bc3e1dff3bb29f8ed881add8cc103eb25dfab49b0d1766b9ea5a2ac31d5f896 |
| research/autonomous_w2/g4/matched_v6_task_development_v3/benchmark_v3.json | afb48622180ce526f2c4412a094d696d92dd4c84c2e80a0b8e8507f147c3be94 |
| research/autonomous_w2/g4/matched_v6_task_development_v3/auer_input_manifest_v3.json | b41b84247165d40940985b4398455682cba2fa814899220c74168046943156b9 |
| research/autonomous_w2/g4/matched_v6_task_development_v3/auer_bindings_v3.json | 7901b62b789b82660d2c738a82b8ea430499f4fab9ada969fc281240bf10550d |
| research/autonomous_w2/g4/matched_v6_task_development_v3/native_source_snapshot_v3.json | 6417ee7e27aed8bf95186229c6630f2eb1a828387aa4370119a0f08a1fee75b8 |
| coordination/autonomous_w2/g4/STATUS_W2_SEQUENCE_08.json | 06d77d3ed5cdb942c92df5826d0d2c80f4eac0dac6caee871685e0569bd4c309 |

The inventory was rehashed after capture; all 57 paths matched at that verification boundary. Any subsequent G4 edit changes the reviewed candidate and requires a fresh G4 source freeze and new hash-bound G2 review.

## 7. Counts, limits, and next action

- G2 native attempts: 24/24 consumed; this audit added 0; held-out rows 0.
- G4 work run by G2 in this continuation: 0 queries, 0 worker/producer calls, 0 fixtures, 0 replays, 0 preflight runner executions, 0 stages, 0 studies.
- G4 v2 preserved attempt: 1 v6 wrapper invocation, 0 native calls; 0 Auer worker attempts/calls; no retry.
- R5: 800/800 NOT_RUN; Auer 1,944 batch: NOT_RUN.
- No branch switch, commit, or push.

**Next action:** G4 should correct the physical/payload hash convention, benchmark pins, and source snapshot pointer; add Auer/scorer/eligibility mutation fixtures; then publish a new exact source/input closure and nonquery report. G2 should review that corrected hash-bound candidate before any G4 producer work. G2 has not authorized or performed any new query.

**Project disposition:** HOLD; G1 PASS_RESTRICTED_REDUCED_MODEL_SCOPE; G2/G3/G4 and physical-platform correspondence UNVERIFIED.
