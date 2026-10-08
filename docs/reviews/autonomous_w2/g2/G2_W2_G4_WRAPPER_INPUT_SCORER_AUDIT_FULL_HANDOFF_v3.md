Session: DDWMR | LUNA-G2-SCOPE

# G2 W2 handoff v3 — current G4 wrapper/input/scorer audit and v6 receipt erratum

**Date:** 2026-10-08 (Asia/Saigon). **Disposition:** PARTIAL; the digest defect identified in v2 is resolved and the saved G4 nonquery report says 47/47 PASS, but its source closure predates the current worker. The actual protocol/manifest benchmark pin and top-level Auer snapshot pointer remain inconsistent. **Audit mode:** read-only source, input, saved-report and hash inspection. G2 ran no query, worker, producer, fixture, replay, preflight, stage or study.

## 1. Current result and peer note

G2 completed a new static audit of the current G4 v3 wrapper, semantic inputs, bindings, common scorer, saved nonquery fixture report and v6 receipt erratum. Actionable G4 corrections are in [the G2 peer memo](../../../../coordination/autonomous_w2/g2/G4_WRAPPER_INPUT_SCORER_AUDIT_v3.md). The source/evidence snapshot is in [inventory v3](../../../../coordination/autonomous_w2/g2/G4_V3_WRAPPER_INPUT_SCORER_HASH_INVENTORY_v3.json), SHA-256 a5a5d2af2990c28c9d8572cb2b883fd1f854a4944ca43030095df62b9f35772a.

The current candidate is **not ready to freeze or run**. Actual semantic and payload hashes now agree with the worker's no-trailing-LF canonicalizer for all three inputs. G4's saved preflight report is 47/47 PASS with zero numeric calls, but its source-closure fixture binds an older Auer worker hash than the current worker. Separately, protocol and manifest benchmark pins remain stale, the top-level source-snapshot pointer in Auer bindings is stale and unchecked, and fixture preparation repairs the benchmark pin in an in-memory manifest override. G4 needs a new source-bound nonquery report after correcting these provenance inconsistencies.

G4's latest observed mutable STATUS and immutable sequence 8 still hash to 06d77d3ed5cdb942c92df5826d0d2c80f4eac0dac6caee871685e0569bd4c309 and remain ACTIVE. They predate the newer fixture report and worker edit. See [status provenance addendum v3](../../../../coordination/autonomous_w2/g2/G4_STATUS_POINTER_PROVENANCE_ADDENDUM_v3.md).

## 2. Source snapshot and current corrections

Repository remained on main at HEAD 94c60f627a2ce1a8d52101050bdc0ce9d2e59afe. Inventory v3 refreshed 57 existing paths and added all files under G4 nonquery_fixtures_v4, for 106 hash-bound entries. It passed its post-capture rehash. Selected current hashes:

| Object | SHA-256 |
|---|---|
| validation/autonomous_w2/g4/preflight_matched_v6_v3.py | 3022b7ad6a94ec3f256203b2b9ac7eb52a7b06d98ce6168ee2b18d09432bb768 |
| validation/autonomous_w2/g4/auer_w2_worker_v3.py | 4cb79dee97f5ceb168ee140397ea17c04bde3b514986102c723780f1631bb66c |
| validation/autonomous_w2/g4/matched_v6_common_v3.py | fb9d39d3a262210fd45d53863533359ca55e8a8778c32c4c12bff8e95ef5b46b |
| validation/g4/common_tube.py | 564c0ffe608be6d0413def643a5dff7b455613c61b56f0ea42684cc7c6874d25 |
| research/autonomous_w2/g4/matched_v6_task_development_v3/protocol_v3.json | 4bc3e1dff3bb29f8ed881add8cc103eb25dfab49b0d1766b9ea5a2ac31d5f896 |
| research/autonomous_w2/g4/matched_v6_task_development_v3/auer_input_manifest_v3.json | b41b84247165d40940985b4398455682cba2fa814899220c74168046943156b9 |
| research/autonomous_w2/g4/matched_v6_task_development_v3/auer_bindings_v3.json | 7901b62b789b82660d2c738a82b8ea430499f4fab9ada969fc281240bf10550d |
| G4 saved preflight_report_v3.json | 71562e7581ab252e50eb8e37d768298ded1aa5f5d83181759a3a47d458eb30bc |

The earlier v2 physical/payload digest rejection is superseded. matched_v6_common_v3.canonical_sha256 hashes sorted compact UTF-8 JSON with no final LF; the Auer worker now uses that helper for physical inputs and native payloads. G2 independently recomputed all three semantic and payload hashes. The separate Auer proof/native-binding helper uses a trailing LF, so the two conventions must remain explicitly named and must not be interchanged.

The v4 report also improves on the previous fixture snapshot: it contains valid Auer route-boundary cases for all three actions, a set of negative Auer mutation cases, common scorer tests for changed horizon and initial state, and stop-reason fixtures. The earlier expected-error mismatch is fixed; the saved report says 47/47 PASS. Those results are report inspection, not a G2-run test.

## 3. Live input audit

The semantic task matches the G2 saved protocol on all three consumed development actions: (0,0), (1/2,1/2), and (1,1), each linked to its G2 action ID and candidate-specific Auer ID. For each action, G2 checked the canonical physical object and its digest, payload and digest, voltage, native case file SHA, initial nine-state box, all twelve positive-width fixed-label ranges, two-second horizon, scene and parameter cell. Each checked mapping matched. These inputs are consumed development data, not fresh/held-out rows and not a physical task requirement.

The live byte provenance still fails:

| Pointer | Declared | Actual |
|---|---|---|
| protocol_v3.json benchmark SHA | 6bdc22747e8248b1ae5eb7141c5fea0f8020e14a4e8b85529d38461bad7546f1 | benchmark_v3.json is afb48622180ce526f2c4412a094d696d92dd4c84c2e80a0b8e8507f147c3be94 |
| auer_input_manifest_v3.json benchmark SHA | 6bdc22747e8248b1ae5eb7141c5fea0f8020e14a4e8b85529d38461bad7546f1 | benchmark_v3.json is afb48622180ce526f2c4412a094d696d92dd4c84c2e80a0b8e8507f147c3be94 |
| auer_bindings_v3.json top-level native snapshot SHA | da932a19834aeea91a0bc8090db550225566a57b90813cdc981e48f405761e11 | native_source_snapshot_v3.json is 6417ee7e27aed8bf95186229c6630f2eb1a828387aa4370119a0f08a1fee75b8 |

All three nested binding snapshot hashes equal 6417..., and all eight origin/copy pairs in the native snapshot map passed direct byte-hash comparison. However, validate_auer_setup() checks the selected nested pointer but not the top-level binding-document pointer. The worker checks freeze benchmark bytes and manifest-vs-freeze values, but not the protocol's own benchmark SHA. _fixture_documents() repairs benchmark_path and benchmark_sha256 in the in-memory manifest before passing it through manifest_override. Thus a valid fixture route does not prove that the actual candidate manifest will pass production setup.

The report's closure fixture SHA is d7ad8692427c3c6d92efbc7a47a54a2c84b5e80c35aa7b3a2d661c4d13bb6567. It pins the Auer worker to 13a1e0aebb47ff397a57f812e4f3016ac675b64ae46701ba10588f7cddef5e97, whereas the current worker is 4cb79dee97f5ceb168ee140397ea17c04bde3b514986102c723780f1631bb66c. The report timestamp precedes the worker edit by 19 seconds. The current report also omits the preflight script hash. It must be regenerated and source-bound after changes.

## 4. Wrapper, eligibility, and common scorer

Current V6 setup checks the outer action and voltage, saved-row/core binding, frozen mapping, task/profile semantics and fixed-label order before producer entry. Its eligibility no longer promotes a common geometry pass by itself: native replay, CERTIFIED status, strict clip-interior proof, contiguous full-hold coverage, common predicate/replay and the progress lower bound are all required.

Current Auer setup reconstructs the expected task and checks the complete three-action mapping, voltage and semantic digest, native case, labels, initial box, horizon, scene, frozen paths and selected native-binding pins before writing producer_start.json. Its worker then runs native proof replay before common scoring; a supplied-tube common pass cannot replace the native proof.

The common scorer source statically preserves complete closed-hold coverage, slab chaining, initial-set containment, unchanged full fixed-label images, full-slab contact and collision checks, and a recomputed progress interval. It binds the serialized horizon and initial state to expected task values. Its reported PASS is only PASS_ON_SUPPLIED_TUBE; the record expressly says certificate_emitted=false and ode_tube_proof_replayed=false. Fraction/Interval/Budget and trigonometric helpers are shared with G2 and are not an independent arithmetic implementation. The current fixture report does not test omitted/gapped slabs, altered label chaining, tampered geometry check fields, or a changed progress record; G4 should add these offline mutations and assert no producer marker for every invalid Auer case.

The report top level gives producer_invocations=0, while per-case details record three V6 and three Auer stub calls, with fixture-only markers and zero numeric/native calls. Clarify the field name and separate stub invocations from numeric calls. Keep the supervisor's memory-limit/child-failure classification ambiguous unless OS evidence uniquely identifies a memory stop; the current stop behavior is conservative.

## 5. Completed v6 attempt-receipt erratum

The interpretive correction in [V6_ATTEMPT_RECEIPT_SCHEMA_ERRATUM_v1.md](V6_ATTEMPT_RECEIPT_SCHEMA_ERRATUM_v1.md) is complete. G2 rechecked all four historical receipt hashes and each still matches exactly:

| Object | SHA-256 |
|---|---|
| Zero terminal attempt receipt | 3a4cdb69facdd07b4be3126114e467f8dcb58ea91d1af7a7ad93852b03f87f83 |
| Nominal terminal attempt receipt | 13a27d0af11db3c3080e3c695225dbf4fa9b68db1331fb39c992709c132186a5 |
| Alternative terminal attempt receipt | 83c19513e4b48bd6aa18e9521369366799d359e5ed740ec1771d993dd5e1fa7b |
| Stage receipt containing terminal records | 9b906c008af8ff51f92bb55d4f1fe072f9a4ebdc48f4caf64c29feec58f0aa36 |

Historical terminal records remain unchanged and are interpreted as receipts even though their schema label names ATTEMPT_INTENT_v1. The separate attempt_intent.json files remain intents. No replacement schema ID was invented.

## 6. G4 requested continuation and scientific accounting

G4 should correct the benchmark and top-level snapshot pins; assert those pointers in setup validation; expand Auer and common-scorer fail-closed mutation coverage; rerun the nonquery preflight against the current source/input closure; bind its own source hash and publish a new immutable STATUS. No production freeze, receipt or source closure exists at this audit boundary. Do not start the producer until the actual on-disk candidate and freeze agree.

G2's tested-scope disposition remains NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE for the centered-residual branch. Cross-method task utility remains UNMEASURED_NOT_REFUTED. G4's earlier acceptance is limited to the three saved v6 development records. The v3 task criteria pair only the three already-consumed actions and cannot serve as fresh confirmation or establish general usefulness. HOLD remains; G1 restricted reduced-model scope PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.

Counts: G2 native attempts 24/24 consumed; this continuation added 0; held-out rows 0; G4 confirmation rows 0/24 per method at the observed status boundary; R5 800/800 NOT_RUN; Auer 1,944 batch NOT_RUN. The saved G4 nonquery report is G4-authored; G2 ran zero queries and zero fixtures. No branch switch, commit or push.

**Next action:** G4 fixes and freezes exact candidate bytes, completes and reruns its nonquery preflight, and publishes an updated immutable status. G2's audit support for this source snapshot is finished; any later changed G4 candidate needs a new hash-bound review.
