Session: DDWMR | LUNA-G2-SCOPE

# G2 R12 exact-scope GO-binding corrections — full handoff

**Date:** 2026-10-04  
**Assignment:** `docs/CODEX_TO_LUNA_G2_R12_EXACT_SCOPE_GO_BINDING_CORRECTIONS.md`  
**Prior review read:** `docs/reviews/CODEX_G2_R11_PICARD_CHECKER_AND_TRIGGER_REVIEW.md`  
**Disposition:** R12 exact-review content and candidate binding prepared in a separate namespace; awaiting Codex review. No execution authority was created.  
**Execution state:** 0/2 R12 real rows evaluated; 0 native query calls; R5 remains 800/800 `NOT_RUN`; no R6 input was evaluated; no R12 result directory, GO decision, or runnable authorization exists.

## Summary

R12 replaces the R11 self-reported `independent_codex_review.result="ACCEPT"` gate with a separate exact-scope decision object whose cited Markdown review is read, hashed, and parsed by both the production runner and public independent receipt auditor. The decision binds the exact R12 manifest and source closure, the runner, R11 Picard checker, receipt checker, stage ID, R5 rows 12 then 24, both query/input hashes, and the exact review Markdown path and raw hash.

The review Markdown links to the machine-readable decision by repository-relative path and contains a unique structured marker that repeats the same decision ID and all reviewed pins. The decision hashes the review Markdown. The review does not hash the decision, so there is no hash cycle between those two artifacts. A changed review or decision file is rejected, including after the decision has been copied into a stage.

The implementation uses new R12 files only. It preserves the reviewed R11 checker correction, its 36-cell decision table, and its one strong preparation-only trigger. The two rows remain development-overlap rows; no new safety or usefulness result follows.

## R12 decision and review contract

The machine-readable decision schema is `research/benchmarks/G2_R12_CODEX_SCOPE_DECISION_SCHEMA_v1.json`. The only checked-in decision object is `research/benchmarks/G2_R12_CODEX_SCOPE_DECISION_NO_GO_TEMPLATE_v1.json`; it says `execution_authority: NO_GO` and both gates reject it. The exact future decision path is `research/benchmarks/G2_R12_CODEX_SCOPE_DECISION_v1.json`; it does not currently exist. The fixed review path is `docs/reviews/CODEX_G2_R12_EXACT_SCOPE_GO_REVIEW.md`; it also does not currently exist.

The decision is the future runner authorization. A GO decision must carry:

- R12 manifest and closure repository-relative paths and raw SHA-256 hashes;
- raw hashes for `validation/g2/r12_stage_runner.py`, `validation/g2/whole_hold_picard_checker_r11.py`, and `validation/g2/r12_execution_checker.py`;
- stage ID `G2_R12_WHOLE_HOLD_PICARD_STAGE_CANDIDATE_V1`;
- exactly two ordered row pins: R5 index 12, then R5 index 24, each with query ID, canonical-query raw hash, and input-payload semantic hash;
- review ID, exact Markdown path, raw SHA-256 hash, and the decision artifact path the Markdown must link to;
- maximum two row calls, zero R5 study rows, zero native query calls, no retry, and the declared bounded worker timeout.

The Markdown marker and visible `Disposition: GO` line must agree with the machine decision and source-bound candidate. The runner checks the submitted decision path, current decision bytes, review bytes, exact marker fields, row order, source-component hashes, and review link before a durable row intent and rechecks the staged decision/review immediately before each intent. The public auditor independently repeats the semantic checks. It requires the stage's copied decision bytes to equal the live decision artifact bytes and rereads the cited Markdown hash. Explicit NO-GO text, an unrelated review, a wrong pin, or an edited file fails closed. The old `ACCEPT` field is not used as evidence.

The NO-GO template contains current manifest and source-component hashes as review aids. Its closure and review hash fields are all-zero sentinels. The template itself is included in the source closure, so placing the closure's own raw hash into the template would be circular. This has no execution effect: the template is rejected on `NO_GO` before candidate pins are considered. A future GO object is separate from the closure and must carry the actual closure and review hashes.

## Candidate and preserved lineage

R12 binds the same immutable ordered inputs as R11:

| Order | R5 index | Query | Canonical query SHA-256 | Input semantic SHA-256 | Lineage |
|---:|---:|---|---|---|---|
| 0 | 12 | `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_L0_R0` | `d5648569b11c576c8cc0ecb07c5096c21b06fe3a5e849358f254770649465471` | `422afd0448a184f4f67262c6338593c871739b41fb677e8ab1d6b566d18b93ac` | development overlap; consumed prior R6 `UNKNOWN` |
| 1 | 24 | `S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lp1_Rp1` | `105a0710185446312933ec8c92922acd1db0f3af0e999d67207ccd70534b4808` | `70301bc5df76aab2dfdb8bef5135592fbf0063af6799b0f0eb119f4873b2cf9a` | development overlap; consumed prior R6 `UNKNOWN` |

The R12 source closure has 202 direct inputs: all 186 R11 closure entries inherited byte-for-byte and 16 R12 additions. The R12 binder reloads the reviewed R11 candidate and verifies its manifest/closure identities, predecessor rows, source hashes, R5/R6 lineage, clip correction, complete 36-cell table, and sole preparation-only trigger. It also checks every R12 closure entry against the current file and checks the closure sidecar and manifest binding.

Preserved R11 identities are candidate manifest `9ed8c4709c7b398702d73877bfe32c58ca7097777bab08ee7b67e3055cb8708a`, source closure `6b4f1e144a7e9384e9c13f8e7edd8c67be41b97b3283f59de793886e32ae6f1e`, and Picard checker `2a794e8f46c4b029331a2548dccd1948b78d3f5d5d7a96efa118d9353ba56f7e`. The inherited closure and R11 loader cover the prior R3/R5/R6/R10 lineage; the R5 manifest remains `0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b`, and the consumed R6 publication remains `3e55c3b967b661f3a3c3b5aa70ae4bc7cf8e9bab463ec484a4e5865f3db5b33d`.

## One-shot and crash-boundary audit

The public auditor now inventories each stage file by raw hash and each stage directory by relative path. It rejects symlinks, special files, undeclared artifacts, and row-01 artifacts that appear before row-00 reaches a terminal. Interrupted/orphan files remain visible in the inventory; a record without a terminal is not treated as a checked row.

| Synthetic state | Read-only audit result | Retry interpretation |
|---|---|---|
| Decision copied; no row intent | `INCOMPLETE`; the copied decision is inventoried | No row call has been consumed |
| Row directory exists without intent | `INCOMPLETE`; the empty directory is inventoried | No row call has been consumed |
| Intent exists without terminal | `STOPPED_INTERRUPTED`; intent and any orphan record are inventoried | Intent consumed; runner refuses a second callback |
| R5 index 12 completes synthetically, then index 24 is interrupted | `STOPPED_INTERRUPTED`; decision, both row directories, row-12 record/terminal, row-24 intent, and synthetic orphan record are inventoried | Runner refuses to retry the consumed index-24 intent |

These crash states were made only in temporary directories using synthetic records/queries. The public audit was exercised on the synthetic paired interruption as well as the production gate validators. The public audit has no candidate-injection parameter in its production API.

## Non-query fixture evidence

`validation/scripts/verify_g2_r12_scope_gate_fixtures.py` passed all 18 declared groups. The suite includes:

- rejection of the inert NO-GO template;
- one clearly labeled GO-shaped decision accepted by both prospective validators in a temporary directory, with no row invocation;
- rejection by both gates of the actual R10 NO-GO review bytes with a forged legacy `ACCEPT`, both copied into the fixed R12 review slot and cited by the original R10 path;
- rejection of an unrelated review, explicit conflicting NO-GO text, missing receipt-checker pin, changed manifest pin, changed source-component pin, changed row input pin, and swapped row order;
- rejection of a changed review hash, review file changed after binding, and decision file changed after stage copy;
- all four crash-boundary cases above, including the orphan row-24 record hash and the no-retry checks.

Fixture result: `PASS_R12_SYNTHETIC_SCOPE_GATE_AND_CRASH_FIXTURES`; native calls 0, R6 inputs evaluated 0, R5 study rows evaluated 0, real R12 rows evaluated 0. `validation/scripts/audit_g2_r12_candidate_manifest.py` also passed its read-only source/lineage audit. It found the real R12 result directory absent and returned `INCOMPLETE` with an empty artifact inventory, as expected for an unrun stage. Python AST parsing passed for nine R12 Python files; JSON parsing passed for the six R12 schema/config/template files. The external `jsonschema` package is unavailable in this environment, so no third-party Draft 2020-12 meta-validation is claimed; runtime GO checks are enforced directly by both validators and exercised by the fixture suite.

## Source identities

| Artifact | Raw SHA-256 |
|---|---|
| R12 candidate manifest | `f0094dda957ba8e165fda21982fadee20bd2c5839ed309b1b377acc17764337f` |
| R12 manifest semantic JSON | `6b58d5c86487bbd082071207aaabe1bf872ac1c86e64688a63d275f0acd4e478` |
| R12 source closure | `adbde039053db9438e989f9d74987421aad3f5f46db4ee88af7d9d5c41c98d62` |
| R12 closure semantic JSON | `9a46f9e988853cb0ba17a7cf2cba57c3d0ad5cf68ee5ef5d7a2833745608b693` |
| R12 closure sidecar | `9f44163e5b570d993b8d6d60ae1c526b36e19b015c993d04ea89f326f5ebed30` |
| R12 runner | `a9f8582625b8ee0364d634a672dfae87e29d74cf3dd9f7b6481b024f830555e4` |
| R11 whole-hold Picard checker | `2a794e8f46c4b029331a2548dccd1948b78d3f5d5d7a96efa118d9353ba56f7e` |
| R12 independent receipt checker | `f4e6b2aa753802cf8649037b3a2b83d47f2d458eaf248dfdad18942e8a77e15f` |
| R12 source binder | `8d7f8cce01d873345b99b4a3bd2f61bee692be8aa650ff484d7c72eeb057533a` |
| R12 decision schema | `82770511cf217d8c71ca2b566945591a57e3b7b8e25dfad41f0c8aae2489c033` |
| R12 NO-GO template | `75e1c0d2270336f8dbd60f40475e380f916e147b98021d7f0ab0cf09f305e5d7` |
| R12 fixture declaration | `235afc61ec397f95669856d7598310a4c0f8fa14d1c4a912939badc4303e54b8` |
| R12 fixture script | `1923e203f4aca4104436468018eaa06219f5f54795311416f63d255b2037d57a` |

The manifest raw hash is pinned by the R12 binder. The closure raw hash is checked through the sidecar and is also a mandatory field in any future GO decision; it is deliberately not embedded in the candidate manifest.

## Limits and disposition

The review/decision mechanism is an exact local file-content and hash binding; it is not a cryptographic signature of the reviewer. The `decided_by` text is provenance metadata, not a signature. Codex must review the exact manifest, closure, runner, checker, schemas, fixture evidence, and this handoff before creating any later GO decision.

No real R12 row was assessed, no R5 study row ran, and no native query was invoked. R5 remains 800/800 `NOT_RUN`; the prior two R6 `UNKNOWN` observations remain consumed and unchanged. No G4 source or manifest was edited. No branch switch, commit, or push occurred. Preserve **HOLD; G1 restricted reduced-model PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED**. A future exact-scope GO, if separately issued after review, would authorize only the two locked offline row evaluations; the strong paired trigger remains preparation-only and cannot authorize the 800-row study.
