# Codex review — G2 R18 two-row enclosure diagnosis

**Date:** 2026-10-05  
**Reviewed handoff:** `LUNA_TO_CODEX_G2_R18_TWO_ROW_ENCLOSURE_DIAGNOSIS.md`  
**Disposition:** **VALID as a saved-artifact diagnosis, with a causal qualification.** No new row, G2 gate change, or study GO follows.

I read `AGENTS.md`, all four canonical `research_context` files, the R18 assignment and handoff, the R17 result review, the R10 producer and R11 checker arithmetic, the pinned manifest, and both saved R17 records. I independently checked the raw SHA-256 of the R17 GO, candidate manifest, source closure, receipt, both records, and the R18 extraction script; all seven match the handoff. I read the input and output JSON directly. I did not run the R18 extraction script, native query, worker, stage, or 800-row study.

## A. Finding

The two saved R17 rows remain valid `UNKNOWN` results. The recorded full-time outer boxes are too broad for the present sufficient collision, contact, or progress tests. The R18 report correctly identifies the first **saved** coarse enclosure and the later interval operations where useful separation is lost. This does not establish that box inflation is the unique underlying cause or that a different enclosure will certify the same inputs.

## B. Evidence

The manifest binds R5 indices 62 and 74 to the same initial box, parameter cell, obstacle and `T=1/4`, with held voltages `(0,0)` and `(1,1)`. The initial pose box has coordinate gaps `199/1000` and `49/1000` from the obstacle center. Thus its squared distance lower bound is `21001/500000 > 1/25`, while the declared obstacle radius is `3/50`. From the input state box, the initial normalized-slip intervals are `[-27/100,1/20]` and `[-1/4,7/100]`; the exact reserve witness gives initial contact margin at least `383/200 > 0`. These calculations establish initial-box safety and contact admissibility only.

The R10 producer forms the candidate by expanding interval RHS-based radii and accepting interval Picard inclusion (`validation/g2/time_slab_picard_r10.py`, `_try_internal_slab`). Its saved slab expansion indices are 4, 4 and 1. It then projects each six-state candidate componentwise into pose and normalized-slip intervals (`_pose_contact`). The R11 checker independently repeats the collision/contact calculations (`validation/g2/whole_hold_picard_checker_r11.py`). The saved fields are:

| Row / slab | Collision distance lower | Collision margin lower | `beta_upper` | Reserve lower | Contact demand upper |
|---|---:|---:|---|---:|---:|
| 62 / 0 | `0` | `-3/50` | `(1,1)` | `0` | `23885717/4000000` |
| 74 / 0 | `1540220173689/70368744177664` | `-67047611924271/1759218604441600` | `(1,1)` | `0` | `25852257/16000000` |
| 74 / 1 | `0` | `-3/50` | `(1,1)` | `0` | `991988257/655360000` |

Every recorded slip interval spans the clip saturation threshold. Hence the implemented `abs_upper(clip(interval))` equals 1 for both wheels, the square-root reserve lower bound equals zero exactly, and the positive body-demand upper bound makes every contact margin lower bound negative. The pose rectangle has zero coordinate gaps to the obstacle center in row 62 slab 0 and row 74 slab 1. Row 74 slab 0 has a positive distance lower bound smaller than the radius. These are limitations of the saved outer representation and sufficient tests, not evidence of an actual collision or contact loss. The R17 independent replay accepted both records as `VALID_UNKNOWN`, and its fixed paired rule returned `NO_PREDECLARED_TASK_SELECTION_SEPARATION`.

**Causal qualification.** Expansion index 4 identifies the first *recorded candidate* whose projection fails the sufficient tests. The artifacts do not quantify the separate effects of interval RHS evaluation, geometric expansion, parameter dependency, endpoint carry, and pose projection. R18 appropriately presents a proposed structured tightening as a research obligation, not a proven remedy.

## C. Consequence

These rows are useful development examples for studying enclosure loss. Their initial positive margins do not prove full-hold safety, and two `UNKNOWN` outcomes do not demonstrate voltage-selection value. Indices 62 and 74 are consumed development-overlap evidence. The R5 study remains **800/800 `NOT_RUN`**, and its broader-study preparation trigger is false.

## D. Status

**VALID** for the read-only diagnosis and exact initial-time witnesses. **UNVERIFIED** for true full-hold safety, the effectiveness of any proposed tightening, decision-relevant voltage selection, physical correspondence and G2. Overall **HOLD**; G1 PASS only in the restricted reduced-model scope; G2/G3/G4 UNVERIFIED.

## E. Required action

Develop one source-backed enclosure improvement that targets both slip/contact and joint pose separation while retaining execution-fixed parameters and full-time coverage. Quantify which relaxation it tightens before proposing another query. Use the consumed R17 pair only for method development. Any later fresh evaluation requires a prospective challenge, independent replay and separate exact-scope authority. Do not launch the 800-row study from the R17 trigger.
