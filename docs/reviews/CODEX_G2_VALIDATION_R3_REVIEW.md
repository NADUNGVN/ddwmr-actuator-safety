# Codex review — completed G2 validation R3

2026-09-30. Repository: `NADUNGVN/ddwmr-actuator-safety`.
Branch: `luna/g2-validation-v1`.
Reviewed implementation/evidence commit: **`4fd0451146ab9567a51499183db5a08f20ae8de5`**.

## Disposition

**ACCEPT R3 as a completed, reproducible synthetic development batch and accept the inspected directed-distance correction in its stated scope.** No new mathematical blocker was identified in that correction. This review does not establish universal implementation correctness, practical online control, recursive safety, physical correspondence or novelty.

**HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED.** These canonical statuses are unchanged. G2 now has substantial computational evidence that was absent from the earlier hand cases. Independent scientific review should assess that evidence explicitly, without conflating G2 with G4 or inventing an acceptance threshold after observing results.

## Review method and evidence boundary

Codex read AGENTS and the four canonical context files, Luna's R3 handoff and addendum, source diffs, the evaluator/checker distance branches, rational primitives, provenance/runner/replay scripts, the new regression source, benchmark specification and existing G4 comparison contract.

Codex independently performed read-only artifact analysis using Python standard-library JSON, gzip, hashlib, Fraction and Git blob reads, without importing or invoking the repository evaluator/checker:

- recomputed all 21 result-ledger semantic hashes, raw hashes and sizes;
- decompressed the archive in memory and checked the original byte count/hash;
- checked original-query ID coverage and duplication, proof presence, outcome counts and action groups;
- checked the stored directed rounding identities, radicand enclosure and distance-endpoint inequalities using exact fractions for all 1,944 records;
- checked status against the signs of the recorded collision/contact lower margins;
- checked 24 specification/producer/checker commitment entries against immutable Git blobs (entries include paths repeated between roles);
- inspected action-level outcomes and recorded timing values.

Codex **did not** rerun the ODE enclosure evaluator, full certificate replay or test suite. The reported 1,944 full proof replays are Luna's execution evidence. The independent arithmetic checks above validate the stored distance witnesses, not the complete upstream pose/contact enclosure. No implementation, configuration or historical result was modified in this review.

## R3R-01 — directed dyadic distance

**Finding:** The correction supplies a sound enclosure of the predictor rectangle's minimum distance and avoids squaring its large exact denominators directly.

**Evidence:** For exact nonnegative gaps `g_x,g_y` and `p=24`, the evaluator uses numerator shifts and quotient/remainder to construct

\[
g_j^- = 2^{-p}\lfloor 2^p g_j\rfloor,
\qquad g_j^+ = 2^{-p}\lceil 2^p g_j\rceil.
\]

Hence `a_minus=sum((g_j^-)^2) <= d^2 <= a_plus=sum((g_j^+)^2)`. Validated root brackets yield `l <= d <= h`, and the sufficient collision margin is still `l-R_s-E_p`. The checker reconstructs the gaps and witnesses and checks root inequalities. The integer primitives are metered under the existing caps. The new branch does not modify the predictor or contact equations. Exact artifact checks found zero rounding/radicand/distance-endpoint inconsistencies across 1,944 records.

The coordinate-rounding loss alone is at most `sqrt(2)*2^-24 <= 2^-23`; root-bracketing loss is separate. The upper endpoint is an upper bound on the rectangle's **minimum distance**, not on all trajectory distances.

**Consequence:** The localized R2 distance arithmetic bottleneck is resolved on this batch without increasing its 16,384-bit cap. This correction is numerical validation engineering, not generic-method novelty.

**Status:** VALID — inspected formula and stored distance witnesses; scoped implementation acceptance.

**Required action:** Retain this versioned method and its checks. No further cap increase or repeat of the historical failed standalone positive fixture is needed to establish this batch's completion.

## R3R-02 — full-grid completion and archive

**Finding:** All original development queries are present, and the compressed artifact preserves the recorded full-grid continuation data.

**Evidence:** Independent parsing gives:

| Phase | Queries | CERTIFIED | Proof-complete UNKNOWN | Resource UNKNOWN |
|---|---:|---:|---:|---:|
| Pilot | 216 | 126 | 90 | 0 |
| Remaining IDs | 1,728 | 1,070 | 658 | 0 |
| Combined | 1,944 | 1,196 | 748 | 0 |

There are 1,944 unique IDs, exactly the manifest's original universe, with 1,944 proof objects and zero missing queries. The checker report contains 1,944 successful replay entries. All **21/21** artifact hashes/sizes match in this checkout. The gzip decompresses to **147,589,521 bytes**, SHA-256 `de339ffcb5ee5e0c83f8d25e3077d9fd9316f83293982189aaffba0bdcf3b196`, matching the archive manifest. No raw-data restoration was written during this review.

The conditional continuation and frozen profile precede the outputs in Git history. Producer/checker sources remained unchanged across the reported execution phases; later commits added archival/evidence files. The old R2 artifacts and canonical context were not changed.

**Consequence:** The former absence of a completed finite computational batch is superseded. The evidence is stronger than another synthetic singleton hand proof: it covers a declared finite grid of nonzero-width moving-state boxes and uncertain actuators. It remains a development grid, not a held-out study or a probability estimate of physical safety.

**Status:** VALID — completed batch and artifact integrity.

**Required action:** Use the counts above in subsequent reviews. Do not continue describing general computation as wholly uninstantiated, but do not extrapolate completion to arbitrary laws, cells, stiff parameters or horizons.

## R3R-03 — what the eight mixed groups actually show

**Finding:** The eight certificate-status distinctions are all zero-voltage versus nonzero-voltage distinctions driven by the sufficient contact bound. They are repetitions of one state/horizon case across obstacle geometries.

**Evidence:** Across 216 groups of nine actions:

| Number of CERTIFIED actions in a group | Groups |
|---:|---:|
| 9 | 132 |
| 0 | 76 |
| 1 | 8 |

Every mixed group has state `state_low_mid`, horizon `T_100=0.1 s`, and its sole certified action is **`V_0_0`**. This state cell is moving: `u in [0.2,0.3] m/s`, with `r in [-0.05,0.05] rad/s`, nonzero wheel/current/pose widths and the full uncertain parameter cell. It is not an exact-rest case.

The eight scene suffixes are `d050_l-200`, `d050_l+200`, `d100_l-200`, `d100_l+000`, `d100_l+200`, `d200_l-200`, `d200_l+000`, `d200_l+200`. In all eight, every action has a positive collision lower margin. The eight nonzero actions return UNKNOWN solely because `CONTACT_SUFFICIENT_MARGIN_NEGATIVE`. Contact margins are identical across these geometries. Rounded values in newtons are:

| Voltage | Contact lower margin |
|---|---:|
| `(0,0)` | +0.127641589 |
| `(-1,-1)` | -0.211889782 |
| `(-1,0)`, `(0,-1)` | -0.103833460 |
| `(-1,+1)`, `(+1,-1)` | -0.213302737 |
| `(0,+1)`, `(+1,0)` | -0.108378014 |
| `(+1,+1)` | -0.213006908 |

More generally, the union of groups certified by any enumerated action equals the groups certified by zero voltage: **140 versus 140**. There is no group on this grid where a nonzero action is certified while zero is not.

**Consequence:** R3 establishes moving-cell voltage-dependent certificate output, specifically for the conjunction of collision safety and contact admissibility. It does not show that selecting a nonzero voltage expands certified group coverage over checking zero alone on this grid. Eight geometries are not eight independent mechanisms or statistical replications. Negative contact lower bounds establish neither actual contact violation nor unsafe actions. Zero voltage is the MASTER closed terminal-voltage condition, not an automatic stop or a proved backup policy.

**Status:** VALID — narrow descriptive separation. Practical action-selection benefit remains UNVERIFIED.

**Required action:** Preserve this stronger qualification. Compare against an applicable generic method before attributing the separation to a distinctive motor/contact construction. Do not force nonzero-action success by changing the already observed grid; a new domain, if justified, must be prospectively versioned and described as development.

## R3R-04 — finite runtime evidence and its limit

**Finding:** Offline finite execution is evidenced on this grid; this implementation has not demonstrated online timing feasibility for the evaluated holds.

**Evidence:** Recorded evaluator times across the 1,944 queries are **0.109–0.313 s**, upper median **0.203 s**, sum **360.991 s**. These are artifact timings, not fresh Codex measurements. All are greater than their respective `T` values of 0.02, 0.05 or 0.1 s. The values do not include a demonstrated online nine-action policy or its scheduling/latency model.

**Consequence:** “No runtime evidence exists” is now too strong. “The safety filter can run at the benchmark sampling periods” is unsupported. Offline precomputation is a possible future use, not a result already established here; no change to MASTER's ideal timing assumptions follows.

**Status:** VALID — finite offline batch timing; online feasibility UNVERIFIED.

**Required action:** Separate these claims in the G2 disposition. Do not add an estimator, delay model, controller or recursive construction to repair the runtime interpretation silently.

## R3R-05 — provenance improvement and remaining maintenance issue

**Finding:** Content-based specification commitments and distinct execution revisions resolve the earlier misleading configuration-only specification hash. The enumerated source manifests are not yet the complete transitive dependency list.

**Evidence:** The specification ledger binds immutable Markdown blobs and is checked against the manifest; 24 role/specification entries independently match their Git objects. However, `checker.py` imports query/profile/hash helpers from `evaluator.py`, which is absent from `CHECKER_PATHS`. `model.py` imports `polynomial.py`, absent from both explicit source lists. The full immutable producer/checker revision still identifies these files. No relevant conflicting changes to them were found for this returned batch. The checker module's opening “shares only” description is narrower than its actual imports; the handoff gives a fuller dependency disclosure.

**Consequence:** This is a future provenance-hardening issue, not evidence that R3's proofs were checked with incompatible code. Shared dependencies also mean replay is not an independently implemented second numerical engine.

**Status:** NEEDS REVISION — maintenance before a future comparison run; not a blocker to retaining R3 evidence.

**Required action:** In the next versioned validation work, include the actual transitive scientific dependencies and align the independence wording. Preserve the frozen R3 manifests. Do not rerun the completed grid solely to rename or expand provenance fields.

## Next scientific decision

There is no basis from this review for another automatic arithmetic-repair loop. The next review should decide:

1. Which precise G2 sub-obligations this supported clip-law computational construction now satisfies, and which useful-domain/general-contract proof obligations remain.
2. Which applicable external baseline and matched comparison can test the remaining scientific advantage, given that zero alone matches existential group coverage and current runtime is offline.

The existing generic-method novelty blocker remains. The current implementation is the conservative one-cell fallback; it must not be presented as evidence that an implemented sharper signed-kernel refinement outperforms prior art. Full-grid completion alone does not settle G4. No G3 authorization or construction is requested.

See `../GPT_G2_VALIDATION_R3_REVIEW_REQUEST.md` for the consolidated external review request and mandatory returned Markdown file.
