# Codex review — G2 R24 paired bound and threshold audit

**Date:** 2026-10-06  
**Reviewed handoff:** `LUNA_TO_CODEX_G2_R24_PAIRED_BOUND_AND_THRESHOLD_ADVERSARIAL_AUDIT_FULL_HANDOFF.md`  
**Handoff SHA-256:** `e6ecbfe702ead5ce363a552e28651f82f49c8016f1280062b6c8466b1857f0c2`  
**Disposition:** **ACCEPT** the R24 independent audit in its exact synthetic scope. It confirms the R23 matched action-ordering result and the cross-state common-threshold blocker. No gate promotion or execution GO.

I checked the R24 derivation against MASTER v2.1 §§5–12, R22–R23, and the R23 Codex review. I independently recomputed the decisive rational subtractions. No native row, worker, stage, retry, 800-row study, or G4 comparison was run.

## A. Finding

R23's paired calculation proves `J_+(x_0,vartheta)>J_0(x_0,vartheta)` for every **matched** state and fixed parameter in its five-cell synthetic grid. It does not prove `sup J_0<inf J_+` across **different** admissible states. The latter is established by the separate R22 intervals only at `eta=10^-6`, is unresolved at `10^-5` and `10^-4`, and is false at `10^-3` and `10^-2`.

## B. Evidence

R24 rederives the slip and paired-difference equations directly from MASTER. The all-action force/slip bounds keep the selected `clip` law on its linear branch and give positive full-hold collision/contact margins. Its cone/heading calculation supports the exact matched bound

\[
J_+(x_0,\vartheta)-J_0(x_0,\vartheta)
>\frac1{25000}\;\mathrm m
\]

for the declared grid. Strict lower polynomial inequalities apply for `t>0`; at `t=0` both sides equal zero.

For the common-threshold counterexample, R24 selects one all-one fixed parameter realization and **different** allowed initial speeds: `+eta` for baseline voltage and `-eta` for positive voltage, all other states zero. Symmetry and the proven clip branch give the same linear system for both. The zero-voltage energy and first-exit argument yield a homogeneous displacement response `H>1/6`; the positive-voltage rest response has `G<=1/3072`. Thus

\[
J_{0,+\eta}-J_{+,-\eta}=2\eta H-G
>\frac{\eta}{3}-\frac1{3072}.
\]

At `eta=10^-3` the right side is `1/128000>0`; at `10^-2` it is `77/25600>0`. Both trajectories are covered by the proved whole-hold formal collision/contact margins. Therefore no common threshold can separate the entire two-action cells at those widths. This does **not** contradict the matched bound.

## C. Consequence

R23's scientific statement should be read with R24's erratum: scalar interval overlap at `10^-5` is merely inconclusive; at `10^-3` and `10^-2` the stronger common-threshold condition is actually false by witness, while matched ranking remains true. The exact-rest/near-rest synthetic family is now sufficiently characterized for this research question. More threshold-tuned micro-cell variants would not establish a meaningful operating domain.

The matched bound is a sound candidate for a **ranking** predicate and for studying correlation-preserving enclosures. It is not yet evidence that a task-aware safety filter makes a useful decision, nor evidence that the method has an advantage over generic validated reachability.

## D. Status

- **VALID:** R24 audit of R23 paired ordering and whole-hold formal safety/contact in the declared synthetic family.
- **BLOCKER:** common task-threshold separation at `eta=10^-3` and `10^-2` for this family.
- **UNVERIFIED:** common threshold at `10^-5` and `10^-4`; independently meaningful task/domain, practical conservatism/runtime, general G2 evaluator, physical correspondence, and G4 novelty.
- **UNCHANGED:** R5 `800/800 NOT_RUN`; overall **HOLD**; **G1 restricted PASS**; **G2/G3/G4 UNVERIFIED**.

## E. Required action

Pause new R22–R24 synthetic threshold variants and any full-grid execution. G2 should audit source-backed task and parameter operating domains, recording exact missing data without inventing values. G4 may now perform a **read-only, equation-level** overlap check for the paired-difference idea against Auer and other applicable validated-reachability methods; the unfavorable prior Auer pilot remains unchanged. Decide whether to build a paired evaluator only after those two audits identify a research claim worth testing. No G3 or operational controller work follows.
