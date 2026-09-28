# v2.1 adoption-finalization review package

Prepared 2026-09-29. **REVIEW ARTIFACT ONLY — NOT APPLIED.** Authoritative formulation remains MASTER v2. G1 NEEDS REVISION; G2/G3/G4 UNVERIFIED; overall HOLD.

The [latest GPT handoff](../../reviews/GPT_TO_CODEX_REVIEW_12edd1b_R2_FULL_HANDOFF.md) accepts R2's formulation with three mandatory edits. Its §§0 and 45 explicitly require review of the final adoption text before authoritative application. This package follows that instruction. No G1 pass or implementation permission follows from formulation acceptance.

## Read the exact final text

- [Codex finalization response](../../reviews/CODEX_FINALIZATION_RESPONSE_12edd1b.md).
- [Future MASTER text](MASTER_v2_1_FINAL_TEXT.md).
- [Future DECISION_LOG text](DECISION_LOG_FINAL_TEXT.md).
- [Future REVIEW_GATE text](REVIEW_GATE_FINAL_TEXT.md).
- [Future LITERATURE_MATRIX text](LITERATURE_MATRIX_FINAL_TEXT.md).
- [Future AGENTS contract](AGENTS_FINAL_TEXT.md) and [future root README](PROJECT_README_FINAL_TEXT.md).
- [Exact six-file adoption diff](ADOPTION_FINALIZATION.patch).
- [Baseline hash manifest](BASELINE_SHA256.json).

The FINAL_TEXT files contain the exact intended target text, including future authoritative/adopted-version wording, so they match the patch without an extra banner. **Their placement in this proposal directory confers no authority.** Only the canonical files at repository root/research_context can become authoritative after explicit adoption. Links inside the target texts are relative to their intended final locations, not this preview directory.

The earlier R2 proposal and its pending patch remain unchanged as review history at `docs/proposals/v2_1/`. Do not apply both patches. This finalization patch replaces the earlier pending patch for adoption review.

## Scope of changes

1. Use “unknown fixed model-parameter vector” and consistent model-parameter terminology.
2. Remove the explicit finite-height normal-load diagnostic from the future MASTER. Its derivation remains in `docs/reviews/CODEX_RESPONSE_TO_GPT_G1_v2_1.md`, B3, and the incoming review history. Retain the effective-capacity/physical-correspondence caveat and the trajectory-inclusion warning.
3. Replace active pending/proposal metadata in the future context with v2.1 formulation wording; keep gate statuses open. Update root README and AGENTS together so session entry points do not describe the old model after adoption.

The C_j-based equations, core phi assumptions, parameter intervals/constancy, typed domains, voltage quantifiers and predecessor definitions remain those of R2. This is editorial/version finalization, not new G2/G3 work.

## Adoption date and authorization

There is no approved adoption event yet, so this package does not assign one. The target decision entry uses final decision wording and links the review evidence; it contains no invented calendar date or unresolved template token.

On explicit authorization, record the actual local adoption date (Asia/Saigon), authorizing user message and final review disposition in the adoption commit and a dated provenance line under the new v2.1 decision entry. This is an event record added only when the event occurs, not a change to the reviewed formulation. No today's-date assumption or predated adoption is permitted. If the actual application differs substantively from this diff, return the changed text for review.

## Apply only after explicit adoption is relayed

- Re-check the six baseline hashes and any intervening changes; do not overwrite unrelated work.
- Check the diff with `git apply --check`; it has not been applied by this preparation.
- Apply the reviewed finalization diff, add the actual adoption event record as above, and verify canonical text plus root session references.
- Keep HOLD, G1 NEEDS REVISION and G2/G3/G4 UNVERIFIED. Review the actual authoritative v2.1 text for G1 separately.
- Do not start G2/G3 constructions or implementation merely because the formulation is adopted.

## Message to the independent reviewer

```text
Review docs/proposals/v2_1_finalization/ADOPTION_FINALIZATION.patch
and its six FINAL_TEXT files, together with
docs/reviews/CODEX_FINALIZATION_RESPONSE_12edd1b.md.

Confirm the three mandatory edits from the 12edd1b R2 review:
model-parameter terminology; historical normal-load equation removed from
MASTER; adopted-version metadata ready for canonical application.
Check that the mathematical C_j core and all gate statuses are unchanged.

No adoption date is invented. The actual dated authorization/adoption
record will be added only when the user authorizes application.

Give explicit accept/modify/reject for this finalization text.
This is formulation adoption review only: no G1 pass, GO or implementation.
MASTER v2 remains authoritative until application is explicitly authorized.
```
