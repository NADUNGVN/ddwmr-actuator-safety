# Erratum — R14 handoff R13 manifest hash

**Applies to:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_R14_STAGE_REPLAY_AND_GO_BINDING_FULL_HANDOFF.md`  
**Scope:** correction to one transcribed value in the R13 artifact table. The R14 handoff remains byte-for-byte unchanged.

The R14 handoff's R13 artifact table reports the R13 manifest SHA-256 as:

`a583703d84eb9285b1ff12647bbfb40c7a45e2d7d8cb23119f4ed1b8b12633`

That value is incorrect. The SHA-256 of the exact R13 manifest bytes is:

`a583703d84eb9285b1ff12647bbfb40c7a45e2b4b92cfba0035c8bbf49c4ba82`

The corrected value agrees with the R14 source-closure entry and the R14 checker's `EXPECTED_R13_MANIFEST_SHA256` constant. The R14 candidate lock itself was internally consistent. Use the corrected hash for provenance; retain the original R14 handoff unchanged and keep this erratum alongside it.
