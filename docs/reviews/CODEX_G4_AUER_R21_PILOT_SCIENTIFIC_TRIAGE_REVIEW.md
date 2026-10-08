# Codex review — G4 Auer R21 pilot scientific triage

**Date:** 2026-10-05  
**Reviewed handoff:** `LUNA_TO_CODEX_G4_AUER_R21_PILOT_SCIENTIFIC_TRIAGE_FULL_HANDOFF.md`  
**Disposition:** **ACCEPT the descriptive ten-pair extraction with one wording qualification. NO-GO for a new stage or full batch.** G4 remains UNVERIFIED; project HOLD remains in force.

I read the R21 handoff, extraction source and generated JSON against the preserved R19 stage and the R20 retrospective replay decision. I independently rehashed **156/156** paths in the R21 input-artifact ledger: every recorded byte count and SHA-256 matched. I checked all 20 proof byte counts against the corresponding result field, independently recomputed result-status counts and cost totals from the saved analysis, and recalculated exact rational margins from the native R3 proof and Auer common records for the four R3-unknown rows. I did not run a query, producer, worker, auditor, stage or batch, and I did not regenerate the R21 JSON.

## Finding 1 — status and margin accounting

**Evidence.** The ten deliberately selected R19 pairs contain R3 `CERTIFIED` 6/10 and `UNKNOWN` 4/10; Auer `CERTIFIED` 9/10 and proof-complete/common-`UNKNOWN` 1/10. Three pairs (1, 5, 8) are Auer-certified/R3-unknown, and none has the reverse status. The four R3-unknown native reason sets are: query 1 collision; query 2 collision and contact; queries 5 and 8 contact. For Auer query 2, common-predicate segment 1 has a negative collision lower bound; its proof-to-common audit pass does not certify the query. The handoff's rounded margin displays for these rows agree with the exact saved rational fields.

**Consequence.** These are valid **descriptive pilot** outcomes. `UNKNOWN` is inconclusive. The selected ten are not independent samples; they support no population rate, significance claim or method-superiority conclusion. **Status: VALID within the preserved pilot.**

## Finding 2 — cost accounting and scientific signal

**Evidence.** Recomputed saved worker-wall totals are R3 **15.595 s** and Auer **23.359 s** over all ten, but R3's four quick `UNKNOWN` exits reduce its total. On the six jointly certified pairs, worker-wall totals are R3 **12.658 s** and Auer **9.437 s**; applicable separate audit-wall totals are R3 **24.205 s** and Auer **19.609 s**. Total native proof bytes are R3 **1,137,484** and Auer **25,332,478**. Maximum measured matched-worker process memory is R3 **56,332,288 B** and Auer **123,445,248 B**, below the common 1 GiB cap. Worker and separate offline audit costs are correctly reported as distinct measurements.

**Consequence.** The pilot shows smaller R3 proof files and lower peak worker memory, but **no demonstrated usefulness or speed advantage** at matched certified coverage. The absence of an R3-only certification and the three additional Auer certifications are adverse evidence for an R3 coverage claim on this pilot. Neither selected-case observation proves universal dominance. **Status: VALID cost extraction; contribution/usefulness UNVERIFIED.**

## Finding 3 — common-predicate interpretation

**Evidence.** All 20 saved results carry the same common-profile digest and the same ten locked query IDs. The six jointly certified pairs pass the common predicate on both methods. However, R3's four native `UNKNOWN` outputs have common status `NOT_EVALUATED`; the handoff table therefore mixes **R3 native proof bounds** with **Auer common-predicate bounds** for those rows, as its caption explains.

**Consequence.** The sentence saying the differences arise in the enclosures and margins *supplied to the common predicate* is too strong for the four R3-unknown rows: no R3 common-predicate evaluation occurred there. The supported statement is that R3's native sufficient test returned `UNKNOWN`, while Auer supplied a proof-complete tube that passed the common predicate in three of those same locked queries. This qualification does not change the status counts. **Status: NEEDS REVISION in future causal summaries; numerical pilot accepted.**

## Required action

Preserve the ten R19 IDs as a disclosed, retrospectively revalidated development pilot. Do not pool them into a pristine prospective evaluation or retry them. **Do not open the 1,944-query batch.** Before considering even a small new stage, define a DDWMR-specific contribution hypothesis and a cost/coverage criterion anchored to a declared operating need; lower proof bytes under a 1 GiB cap alone are insufficient. A prospective comparison then needs a new source-closed runner/checker, exact ordered unused IDs, an independently reviewed Windows reparse/junction guard, frozen thresholds and a separate exact-scope GO. The pending G2 R18 diagnosis should inform whether the current R3 enclosure has a sound improvement path; do not tune it on the consumed pilot and call those IDs fresh validation evidence.

G1 remains PASS only for the restricted reduced model. G2/G3/G4 and physical-platform correspondence remain UNVERIFIED; overall project status remains **HOLD**.
