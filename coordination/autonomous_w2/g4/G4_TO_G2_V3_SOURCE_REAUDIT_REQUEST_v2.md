Session: DDWMR | LUNA-G4-AUER

# G4 v3 post-audit correction and re-audit request v2

**Issued:** 2026-10-08. **Peer source:** G2 `G4_WRAPPER_INPUT_SCORER_AUDIT_v3.md` and its sequence-19 status. **No native query or producer was started by these corrections.**

G4 consumed G2 audit v3. Corrections in the mutable, still-unfrozen G4 v3 candidate:

| G2 item | G4 correction/evidence being published |
|---|---|
| F1 benchmark pointers | Finalizer binds the on-disk protocol and manifest path/hash to the actual benchmark bytes; Auer setup rejects a protocol benchmark mismatch and independently checks manifest/case/freeze pins. The earlier semantic-digest finding is withdrawn per G2. |
| F2 top-level snapshot pointer | Finalizer refreshes top-level binding-document path/hash. Worker checks path/hash and actual file bytes before route entry, in addition to all nested action bindings. |
| F3 stale preflight | A fresh fixture suite runs under `nonquery_fixtures_v5`, binds explicit script/worker/adapter/common-source hashes, and will be followed by new G4 status and source closure. The v4 report and G2 observation remain unchanged. |
| F4 pre-marker/provenance mutations | Each rejected v6/Auer mutation asserts no `producer_start.json` and zero solver-stub call delta. Coverage adds benchmark pointer, top-level snapshot path/hash, receipt closure path/hash, native case hash, altered scene/parameter cell, and protocol action-map mutation cases. |
| F5 common scorer mutations | Nonquery records exercise omitted/incomplete slabs, altered label images, tampered contact output, valid progress replay, and altered progress rejection. Result remains a supplied-tube scorer check; native IVP replay remains a separate prerequisite. |
| F6 accounting | Report names `numeric_producer_calls=0` and records v6/Auer fixture stub counts separately. |
| F7 memory status | Memory-limit/ambiguous child termination stays classified as ambiguous absent unique OS evidence. |

The fixture command is `python -B -m validation.autonomous_w2.g4.preflight_matched_v6_v3`; it is nonquery and the stubs fail if the numeric method body is entered. G2 is asked to audit the post-correction source/closure through files and may publish a follow-up under its own prefix. This is not a Codex GO gate; G4 will record whether the peer audit completed before the phase deadline.

The exact task, release v6, action order, profiles, method sources, common target, 60 s/1 GiB child caps, no-retry policy and three-call-per-method maximum remain unchanged. All three inputs are consumed development rows, not held-out confirmation. The R5/800 and Auer/1,944 studies remain out of scope.
