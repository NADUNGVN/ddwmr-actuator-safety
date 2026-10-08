Session: DDWMR | LUNA-G4-AUER

# G4 matched input mapping v5 — post-audit source correction

**Status:** semantic input mapping preserved from v4; current bytes/pointers rechecked after G2 audit v3. No native query/producer has run for this phase.

The three action pairs remain the exact consumed G2 release-v6 task inputs:

| Ordinal | G2 action | G4 v6 / local Auer IDs | Voltage | Shared physical-input SHA-256 |
|---:|---|---|---|---|
| 1 | `W2_G2_DEV_001_ZERO` | `W2_G4_V6_ZERO` / `W2_G4_AUER_ZERO` | `(0,0)` | `dc0dcda534dd56e7a1a409977efb5c0565e25c0ca976dcebae189609c4342fa6` |
| 2 | `W2_G2_DEV_001_NOMINAL` | `W2_G4_V6_NOMINAL` / `W2_G4_AUER_NOMINAL` | `(1/2,1/2)` | `80f15195b6a29757fa4bd03a20acc0f25b82a4f7e946d6f0308984ca9d6bec4b` |
| 3 | `W2_G2_DEV_001_ALTERNATIVE` | `W2_G4_V6_ALTERNATIVE` / `W2_G4_AUER_ALTERNATIVE` | `(1,1)` | `3d5844de37384fa3f0b52b1cea6a7580f42d1b4fd84fbc2e857e5aecc593d0bb` |

All pairs bind the same task protocol SHA `8bc1c8fd460a62dc3f7ff1c8e4bef2dbaddbcaffbadd75d6c2c487e9e311c15a`, full nine-state positive-width initial box, twelve fixed positive-width parameter labels, two-second hold, static inflated-circle obstacle, and `7/20 m` endpoint progress threshold. Canonical physical/payload hashes are sorted compact UTF-8 JSON without a trailing LF. Native proof-object envelopes use the Auer solver's separate sorted compact JSON plus LF digest rule.

Current path/hash corrections are in the v3 candidate finalizer and source audit request v2. G2 audit v3 is preserved as a historical pre-correction observation; any follow-up must bind the final frozen protocol, candidate bindings, nonquery report and source closure hashes. These are development inputs already observed by G2; they are not held-out confirmation inputs or a physical-mission benchmark.
