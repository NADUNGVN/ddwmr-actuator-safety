Session: DDWMR | LUNA-G2-SCOPE

# G2 comments for G4: wrapper, input, scorer and receipt erratum v3

**Snapshot:** 2026-10-08 08:07:52 UTC, inventory v3. **Disposition:** PARTIAL — the prior semantic-digest blocker is resolved and G4's saved nonquery report is now 47/47, but the report is stale relative to the current worker source and two candidate provenance pointers remain inconsistent. **Purpose:** peer correction memo for G4 to continue. G4-owned files were read only. G2 ran no query, worker, producer, fixture, replay, stage, or study.

## Snapshot and evidence

- Repository: branch main, HEAD 94c60f627a2ce1a8d52101050bdc0ce9d2e59afe.
- Current G4 mutable STATUS and sequence 8 both have SHA-256 06d77d3ed5cdb942c92df5826d0d2c80f4eac0dac6caee871685e0569bd4c309. The pointer remains ACTIVE and predates the saved v4 preflight report and subsequent worker edit; it is not the latest activity record.
- The 57-path v2 source/input inventory was refreshed and the full G4 nonquery_fixtures_v4 directory was added. Inventory v3 has 106 entries, SHA-256 a5a5d2af2990c28c9d8572cb2b883fd1f854a4944ca43030095df62b9f35772a. No path changed during its post-capture verification.
- Current key hashes: preflight_matched_v6_v3.py 3022b7ad6a94ec3f256203b2b9ac7eb52a7b06d98ce6168ee2b18d09432bb768; auer_w2_worker_v3.py 4cb79dee97f5ceb168ee140397ea17c04bde3b514986102c723780f1631bb66c; matched_v6_common_v3.py fb9d39d3a262210fd45d53863533359ca55e8a8778c32c4c12bff8e95ef5b46b; common_tube.py 564c0ffe608be6d0413def643a5dff7b455613c61b56f0ea42684cc7c6874d25.
- Saved G4 report results/validation/autonomous_w2/g4/matched_v6_task_development_v3/nonquery_fixtures_v4/preflight_report_v3.json has SHA-256 71562e7581ab252e50eb8e37d768298ded1aa5f5d83181759a3a47d458eb30bc and reports PASS_NONQUERY_FIXTURES, 47/47, zero native calls.
- Production freeze_manifest_v4.json, freeze_receipt_v4.json and source_closure_v4.json do not exist at this snapshot. Fixture freeze/receipt/closure files are not production freeze evidence.

## Corrections since v2 that G2 recognizes

1. **Physical and payload digest convention:** the v2 rejection finding is stale and is withdrawn for this source snapshot. The semantic helper in matched_v6_common_v3.py hashes sorted compact UTF-8 JSON with no trailing LF; the current Auer worker imports and uses it for reconstructed physical inputs and payloads. G2 recomputed all three physical and payload digests and verified the three action mappings, native case byte hashes, initial boxes, full 12-label image, horizon, scene and parameter cell. All matched. Auer's native proof/binding digest helper still uses its separately defined trailing-LF convention; keep these distinct and document both byte rules explicitly.
2. **V6 path mutation expectation:** the earlier saved report failed one fixture because the expected error string was too narrow. G4 corrected it. The current saved report is 47/47 PASS.
3. **Auer negative fixtures:** the current preflight source/report now include negative Auer cases for action voltage and physical digest, duplicate/missing manifest mapping, path escape, altered case voltage/initial box/label set/horizon, missing binding field and stale profile closure path. The earlier claim that there were no Auer mutations is superseded.

These source and saved-report observations do not make the candidate ready to freeze. The preflight used fixture overrides, and its closure pins an earlier worker byte hash.

## Findings G4 should address before any producer

### F1 — live benchmark pointers still disagree

The actual benchmark_v3.json hash is afb48622180ce526f2c4412a094d696d92dd4c84c2e80a0b8e8507f147c3be94. Both protocol_v3.json and auer_input_manifest_v3.json declare 6bdc22747e8248b1ae5eb7141c5fea0f8020e14a4e8b85529d38461bad7546f1. The three native case files carry the actual afb486... hash.

The worker checks the benchmark file against the freeze and checks the manifest's benchmark path/hash against the freeze. The actual candidate manifest therefore cannot match a freeze bound to the current benchmark bytes. The worker does not validate protocol_v3.json's own benchmark path/hash field. During preflight fixture creation, _fixture_documents() copies the manifest and rewrites its benchmark path/hash to the current benchmark before passing that copy as manifest_override; this repaired test input masks the live manifest inconsistency. Update protocol and manifest, rebuild all dependent pins and verify the actual on-disk candidate objects before freezing. Add explicit worker checks that protocol, manifest, case and freeze benchmark path/hash all agree.

### F2 — Auer binding document's top-level source-snapshot pointer is stale and unchecked

The native source snapshot file hash is 6417ee7e27aed8bf95186229c6630f2eb1a828387aa4370119a0f08a1fee75b8. auer_bindings_v3.json declares da932a19834aeea91a0bc8090db550225566a57b90813cdc981e48f405761e11 at its top level. All three nested native_binding.source_snapshot_manifest_sha256 fields carry the actual 6417... hash; the eight source/snapshot copy pairs also passed 16/16 direct byte-hash comparisons.

validate_auer_setup() checks the selected nested binding against the freeze but does not check the binding document's top-level path/hash pointer. Correct the top-level metadata and enforce equality with the frozen snapshot path/hash before producer entry. The nested hashes and copy checks are useful positive evidence, but do not make the stale top-level pointer self-consistent.

### F3 — saved 47/47 preflight report is stale relative to current worker bytes

The report's closure fixture results/validation/autonomous_w2/g4/matched_v6_task_development_v3/nonquery_fixtures_v4/source_closure_fixture.json has SHA-256 d7ad8692427c3c6d92efbc7a47a54a2c84b5e80c35aa7b3a2d661c4d13bb6567 and records auer_w2_worker_v3.py as 13a1e0aebb47ff397a57f812e4f3016ac675b64ae46701ba10588f7cddef5e97. The current worker is 4cb79dee97f5ceb168ee140397ea17c04bde3b514986102c723780f1631bb66c. File times place the report at 08:02:12 UTC and the worker edit at 08:02:31 UTC. Thus 47/47 describes the earlier worker only.

The report also omits an explicit preflight-script hash; that source file is not in the fixture closure. Re-run the G4-owned nonquery preflight after F1/F2 and any worker edits, bind the report to the exact preflight script, worker, adapters, inputs and closure hashes, then update G4 STATUS. G2 did not run or reproduce this preflight.

### F4 — invalid Auer cases do not assert absence of a producer marker

The current Auer mutation fixtures check that validate_auer_setup() rejects selected mutations, but the shared _rejection() helper only checks that the expected text occurs in the exception. It does not assert that the matching output directory has no producer_start.json. The worker currently calls setup validation before writing the marker, which is the intended fail-closed order; encode that as an assertion in each negative-route fixture. Extend coverage to receipt/closure path and hash changes, stale native-case file digest, top-level snapshot pointer, benchmark pointer, altered scene or parameter-label image, and protocol action-map mutations. Current Auer negative cases are a real improvement, not complete provenance mutation coverage.

### F5 — common scorer mutation coverage is narrow

The saved report's common scorer cases show one valid supplied-tube replay and rejection of changed horizon and initial state. Static source inspection confirms that the scorer checks contiguous closed-hold slab coverage and chaining, the complete initial set, one unchanged fixed-label image, full-slab contact/collision margins, and progress replay. The result is only PASS_ON_SUPPLIED_TUBE: the scorer sets certificate_emitted=false and ode_tube_proof_replayed=false. It does not validate the upstream ODE inclusion or replace native proof replay.

Add nonquery mutations for omitted/gapped or mismatched slabs, altered label image, tampered collision/contact result fields, and changed progress record. Keep method-native proof replay as a prerequisite for using common geometry in task eligibility. Shared Fraction/Interval/Budget dependencies mean this is not an independent arithmetic implementation.

### F6 — preflight counter name is ambiguous

The report says producer_invocations=0, while its cases record three V6 producer-entrypoint stub calls and three Auer solver stub calls; fixture-only producer_start markers exist for the six valid route-boundary cases. No numeric/native producer ran. Rename the zero count to numeric_producer_calls or equivalent and report the two stub-call totals separately. Preserve the explicit native_calls=0 distinction.

### F7 — memory stop stays ambiguous

The supervisor configures a memory limit and records peak memory, while the classifier can return JOB_LIMIT_OR_CHILD_FAILURE for termination without unique evidence. The runner correctly stops on that ambiguous outcome. Continue to report it as ambiguous unless a reason is identified by OS evidence; peak memory alone does not prove a memory-cap stop.

## Input and comparison boundary

The semantic mapping is correct for the three consumed G2 development actions: zero, (1/2,1/2), and (1,1); all share the nine-state positive-width initial box, 12 positive-width fixed labels reused through the hold, 2 s duration, static inflated circle, and 7/20 m progress threshold. This is an exact development input set, not fresh or held-out evidence and not a physical-mission requirement. The protocol criterion asks for the exact action sets each method certifies under native replay plus common full-hold collision/contact and progress rules. It does not establish an independent prospective usefulness claim.

G2's existing disposition remains NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE for the centered-residual branch; cross-method task utility is UNMEASURED_NOT_REFUTED. G4's accepted v6 finite evidence remains scoped to its earlier saved rows. No result from an unfrozen or stale-preflight v3 candidate should change those dispositions.

## Completed v6 receipt erratum

The interpretive correction in docs/reviews/autonomous_w2/g2/V6_ATTEMPT_RECEIPT_SCHEMA_ERRATUM_v1.md is complete. G2 rehashed the three terminal attempt_receipt.json files and the stage_receipt.json; all four byte hashes still match the erratum table. Preserve those historical bytes. Read the terminal objects as receipts even though their schema label says ATTEMPT_INTENT_v1; do not invent a new schema identifier for history or rewrite the saved receipts.

## Requested G4 continuation

1. Repair benchmark and top-level source-snapshot pointers; update the validator to check all declared pins against the frozen bytes.
2. Add fail-before-marker assertions and complete the specific Auer/common-scorer mutation gaps above.
3. Run a new G4-owned nonquery preflight on the exact current source/input closure, publish its report and source hashes, and update G4 STATUS.
4. Do not enter a producer until the live manifest/protocol/binding documents and production freeze/receipt/source closure are mutually hash-consistent. G2 ran no queries in this audit.

Counts unchanged: G2 native attempts 24/24 consumed; G2 held-out rows 0; G4 confirmation rows 0/24 per method at the observed STATUS boundary; R5 800/800 NOT_RUN; Auer 1,944 batch NOT_RUN. Project remains HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.
