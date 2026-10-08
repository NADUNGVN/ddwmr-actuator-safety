# G4 Auer protocol v3 R4 non-query contract fixture

**Disposition:** PASS for the listed source-contract and JSON-schema checks only. This is not a trajectory proof, query evaluation, native replay, or batch authorization.

- Source closure SHA-256: `33ec3437d55136117e9c322ce588458aa484060702e7fb46c579ccb47447762b`
- Frozen universe checked statically: `1944` unique IDs; ordered-ID digest `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`
- Inspected ID for input/binding reconstruction only: `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`
- Reconstructed Auer input SHA-256: `b59dc0f4bd05bf277384387115e7138d6df6450c187d2eefd38cae577a474e94`
- Matched worker invocations: `0`; solver proof calls: `0`; native replays: `0`
- Proof artifact written: `false`; trajectory proof produced: `false`

## Contract checks

| Check | Result |
|---|---|
| Helper emits v3-r4 input schema and versioned solver guard accepts it | PASS |
| Versioned solver guard rejects stale v3-r3 input schema | PASS |
| Producer `_seed_record` binding equals worker `expected_binding`, including matched profile path/hash | PASS |
| Producer action binding equals action reconstructed from the frozen query | PASS |
| Validator rejects historical `small_case_resource_profile_v2.json` proof path | PASS |
| Validator reads input digest from `proof.binding.input_sha256` and rejects missing binding digest | PASS |
| Validator rejects mutated `query_action_binding` | PASS |
| Schema accepts Auer result shapes for resource limit (proof-size and outer-memory), invalid input, proof-complete/common-UNKNOWN, and certified branches | PASS: RESOURCE_LIMIT_PROOF_SIZE, RESOURCE_LIMIT_OUTER_MEMORY, INVALID_INPUT, PROOF_COMPLETE_COMMON_UNKNOWN, CERTIFIED |
| Schema rejects undeclared `shared_common_source_sha256` | PASS |

The branch records and proof object exist only in memory to exercise source helpers and schema validation. No synthetic content was written as a proof or result artifact, and no branch was passed through native replay or the full artifact validator.
