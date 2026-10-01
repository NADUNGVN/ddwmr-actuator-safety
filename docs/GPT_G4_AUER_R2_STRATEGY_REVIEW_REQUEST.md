# Request to GPT — G4 Auer R2 scientific review and comparator decision

**Repository:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`  
**Branch / HEAD:** `luna/g2-validation-v1` / `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`  
**Authority:** MASTER v2.1; project **HOLD**.  
**Scope:** independent scientific review and one concrete next-comparator decision. No G3, hardware, GO, or gate promotion is proposed.

## Read in this order

1. `AGENTS.md` and all four canonical `research_context/` files.
2. `docs/reviews/GPT_TO_CODEX_G2_VALIDATION_R3_SCIENTIFIC_REVIEW_FULL_HANDOFF.md` and `docs/reviews/CODEX_G2_VALIDATION_R3_REVIEW.md` for the reason a matched comparator is needed.
3. `docs/reviews/CODEX_G4_AUER_PREFLIGHT_REVIEW.md` and `docs/CODEX_TO_LUNA_G4_AUER_BASELINE_R2.md`.
4. `docs/reviews/LUNA_TO_CODEX_G4_AUER_BASELINE_R2_FULL_HANDOFF.md` and `docs/reviews/CODEX_G4_AUER_BASELINE_R2_REVIEW.md`.
5. `docs/reviews/G4_AUER_SOURCE_AND_APPLICABILITY_v2.md`, `research/theorem_notes/G4_AUER_BASELINE_CONTRACT_v1.md`, and `research/benchmarks/G4_AUER_MATCHED_PROTOCOL_v2.md`.
6. Inspect source and artifacts as needed, especially `validation/g4/common_tube.py`, `validation/g4/verify_common_tube.py`, `validation/baselines/auer2013/`, `results/validation/g4/auer2013/source_snapshot_v2/snapshot_manifest.json`, and the retained Auer 2013 / Rauh–Auer 2011 primary papers.

## Established facts to audit, not assume

- R3 completed a **synthetic development batch** of 1,944 queries, with 1,196 CERTIFIED and 748 proof-complete UNKNOWN. It did not establish practical voltage-selection value or G2 PASS.
- Luna's Auer R2 has **zero matched query evaluations**. Its 1,944 IDs are all `NOT_RUN`. Codex independently verified the ID order and all 681 listed snapshot hashes; v2 manifest digest is `c78523df6616dc46c062841169a7e584fcb622d64acfa4cde1ba4b53c2cb6af1`.
- WSL2 PROFIL/BIAS 2.0.8 built and passed two dependency smoke checks. Nineteen finite arithmetic/trigonometric probes passed. The documented x86-64 glibc/libm caveat remains unresolved. The linked legacy smooth seed lacks the 2013 piecewise extension and stopped its own example at step 3062/3751 with `Condition not fulfilled`, despite process exit code 0.
- Python clip/RHS preflight and the common supplied-hull checker exist. Nine synthetic interface fixtures are reported. The Auer adapter does **not** replay a Picard/inclusion proof; the R3 adapter has no fixture using an actual historical R3 proof. No DDWMR full-time Auer tube or endpoint exists.
- The proposed protocol v2 is unapproved. Raising the step cap to 1,000 is only a resource allowance. Auer §5 has unresolved printed input ambiguity and no exact output table.

## Questions requiring one disposition

1. **Preflight judgment:** Is the R2 handoff accurately scoped as `BLOCKED/PARTIAL`? Identify any specific mathematical/source/interface defect in the existing clip/RHS/common-predicate layer, with exact file/equation evidence. Distinguish a defect from an unimplemented proof obligation.
2. **Comparator decision:** Should this project continue a source-faithful Auer 2013 reconstruction, or select a different published validated-IVP comparator with source and a practicable outward arithmetic path? Make **one recommended choice**. For a replacement, name the method/software and specify why its assumptions match the fixed-label, piecewise-clip, full-time DDWMR problem; describe any limits in calling it a comparison with Auer. For continued Auer work, specify a bounded, reviewable next milestone that would resolve source fidelity and full-time inclusion rather than another build-only preflight.
3. **Arithmetic proof:** State the minimum acceptable path past the PROFIL/BIAS glibc/libm limitation. Clarify whether a documented certified transcendental backend substitution preserves a fair Auer-method comparator, and what evidence it must carry. Do not infer global rounding correctness from finite probes.
4. **Common-check composition:** Review radius-once semantics, full-time collision/contact bounds, endpoint chaining, and the need to bind native proof records to the exact query/action/source snapshot. Say whether any correction is required before a small proof-backed IVP case can be reviewed.
5. **Reference and stop condition:** If §5 cannot be reproduced from authoritative data, define an acceptable independent IVP reference and how it must be labeled. State what evidence would authorize a later 1,944-query matched run, and what outcome would instead end this comparator branch without implying R3 superiority.
6. **Gate judgment:** Preserve or change the current scientific dispositions only with explicit evidence. Separate G2 usefulness, G4 novelty, and physical correspondence. Do not treat a failed comparator reproduction as an R3 win.

## Required output file

Create **`docs/reviews/GPT_TO_CODEX_G4_AUER_R2_STRATEGY_FULL_HANDOFF.md`** in the repository. The user will relay this one Markdown file to Codex. Include:

- an explicit ACCEPT / CORRECT / REJECT disposition for the R2 partial handoff;
- finding, evidence, consequence, status and required action for each material issue;
- **one selected comparator path** and a concrete next Luna work package with stopping criteria;
- exact scope of any common-checker correction and any reference-data limitation;
- the unchanged project status unless supported by new evidence: **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED**.

Do not run the 1,944-query comparison or ask for a commit/push as part of this review. Local files remain uncommitted because the team is sharing one laptop and the user requested no commit yet. Return the absolute path to the Markdown output file.
