Session: DDWMR | LUNA-G2-SCOPE

# G4 mutable STATUS pointer provenance addendum

**Issued:** 2026-10-08. This addendum records what was observed; it does not alter or repin any archived release, inventory, or status snapshot.

| Evidence boundary | G4 status observation | SHA-256 | Interpretation |
|---|---|---|---|
| G2 v6 evidence inventory `results/validation/autonomous_w2/g2/development_centered_v6/evidence_inventory_v1.json` (inventory SHA-256 `5de4f15150a0df2a2ce52c6eff047a9e886895b1d14814eff40c0072e7f0933f`) | G4 sequence 3 snapshot / then-current pointer | `38c88eaf048ec04478a1eb99bfd40977222b2149b10e84fced75d162c9468554` | Earlier inventory boundary. It predates G2 release v6 and is not a v6 audit decision. |
| G2 `STATUS_W2_SEQUENCE_18.json` (SHA-256 `5151843465cbfe9685a6fdcf2a80145471536063b9868087ac85d036219d1187`) | G4 sequence 4 snapshot / then-current pointer | `98d8f9f98200f32db2fd0a74975b21a1dc7df929bffbed4a4b9a37cb1c6d16c7` | G2 seq18 explicitly records sequence 4. This observation must remain attached to seq18. |
| Current observation for this audit | G4 `STATUS_W2_SEQUENCE_08.json`; mutable `STATUS.json` matched it at observation | `06d77d3ed5cdb942c92df5826d0d2c80f4eac0dac6caee871685e0569bd4c309` | Sequence 8 is `ACTIVE`, with the next action still stating candidate preparation, nonquery fixtures, and freeze. The pointer is mutable and may advance later. |

The G4 v2 freeze manifest and source closure are historical evidence bound to their own inputs; the G2 seq18 peer-status entry is not rewritten to sequence 8. G2 sequence 19 records sequence 8 as the current audit observation. Any later G4 pointer movement must be recorded as a new observation, not substituted into these hashes.

**Hash boundary:** the observations above are status/provenance evidence. They do not change the mathematical result, native-attempt accounting, or the bytes in the G2 v6 release and receipts.
