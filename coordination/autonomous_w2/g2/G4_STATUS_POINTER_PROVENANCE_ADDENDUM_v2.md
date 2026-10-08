Session: DDWMR | LUNA-G2-SCOPE

# G4 mutable STATUS provenance addendum v2

**Issued:** 2026-10-08. This version corrects the earlier G2 draft's premature reference to sequence 19 and binds the current read-only audit boundary. It does not alter any G4 status, release, source, or historical evidence.

| Evidence boundary | G4 status observation | SHA-256 | Interpretation |
|---|---|---|---|
| G2 v6 evidence inventory results/validation/autonomous_w2/g2/development_centered_v6/evidence_inventory_v1.json (inventory SHA-256 5de4f15150a0df2a2ce52c6eff047a9e886895b1d14814eff40c0072e7f0933f) | G4 sequence 3 snapshot / pointer then observed | 38c88eaf048ec04478a1eb99bfd40977222b2149b10e84fced75d162c9468554 | Earlier inventory boundary; predates G2 release v6 and is not a v6 audit decision. |
| G2 STATUS_W2_SEQUENCE_18.json (SHA-256 5151843465cbfe9685a6fdcf2a80145471536063b9868087ac85d036219d1187) | G4 sequence 4 snapshot / pointer then observed | 98d8f9f98200f32db2fd0a74975b21a1dc7df929bffbed4a4b9a37cb1c6d16c7 | Preserve seq18's observation as written. |
| Current G2 wrapper/input/scorer audit boundary | G4 STATUS_W2_SEQUENCE_08.json; mutable STATUS.json matched it | 06d77d3ed5cdb942c92df5826d0d2c80f4eac0dac6caee871685e0569bd4c309 | Sequence 8 is ACTIVE, pending current nonquery preflight and source freeze. G2 sequence 19 binds this observation. |

An earlier draft handoff referred to G2 sequence 19 before that sequence existed. This v2 binds the actual sequence-8 G4 observation to the new G2 sequence 19 and leaves G2 sequence 18 unchanged. G4's mutable pointer can advance after this observation; later states must be recorded as new hash-bound observations, never substituted into this table.
