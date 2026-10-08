Session: DDWMR | LUNA-G4-AUER

# G4 Auer R21 — scientific triage of the preserved ten-pair pilot

**Date:** 2026-10-05  
**Disposition:** The R19 data are a retrospective, revalidated descriptive pilot. They do not justify the 1,944-query batch. I recommend a conditional future GO only for a small, prospectively selected and separately authorized comparison after the controls below are complete. This handoff grants no execution authority.  
**Gate state:** G4 remains UNVERIFIED and project HOLD remains in force.

## Finding

R20 revalidated the ten preserved R19 matched pairs after the original R19 checker had exited 2 on the guard/terminal path-string comparison. The R20 checker exited 0 and replayed the saved artifacts for all ten. R19 itself remains unchanged and its original checker failure remains part of the record.

In this selected set, R3 produced 6/10 final CERTIFIED results and Auer produced 9/10. There were three Auer CERTIFIED / R3 UNKNOWN pairs and no R3 CERTIFIED / Auer non-CERTIFIED pair. The three pairs are query indices 1, 5 and 8. Query index 2 is UNKNOWN for both methods, for different recorded reasons. The result is a descriptive outcome of these ten IDs only; the IDs were deliberately selected for this pilot and are not independent statistical samples. No confidence interval, significance test, or prevalence estimate is inferred.

The same frozen query IDs and the same common-profile SHA-256, 35731201512145219327ea862ffc7ef37c5a100f66740cde80dcdc5eb021adfe, appear across all 20 method result records. For the six R3-certified cases, R3 and Auer both pass the declared common predicate. The observed differences therefore arise in the enclosures and sufficient margins supplied to that predicate, rather than from a changed common threshold in the saved artifacts. Each method has its own method-input digest because its numerical proof input differs; the locked query identity and common-profile digest are shared.

UNKNOWN is inconclusive. A negative sufficient collision/contact margin means that the recorded enclosure did not establish the declared condition. It does not prove that the physical trajectory collided or that contact was unsafe.

## Pair outcomes and limiting margins

Margins are lower bounds from the saved proof/common-predicate artifacts. Decimal displays below are rounded for readability; exact rational values are retained in the machine-readable analysis JSON. For certified rows, values are the common-predicate replay margins. For R3 UNKNOWN rows, the common predicate was NOT_EVALUATED, so the table shows the R3 native proof lower bounds. Auer query 2 lists both supplied-tube segments.

| # | Exact query ID | R3 native / common / final | R3 reason and limiting collision / contact margin | Auer native / common / final | Auer limiting collision / contact margin |
|---:|---|---|---|---|---|
| 1 | state_high_mid__scene_d050_l+000__T_050__V_0_0 | UNKNOWN / NOT_EVALUATED / UNKNOWN | COLLISION_SUFFICIENT_MARGIN_NEGATIVE; −0.0006274194 / +1.580365 | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | +0.0008674327 / +1.769564 |
| 2 | state_high_pos__scene_d050_l+200__T_100__V_0_p1 | UNKNOWN / NOT_EVALUATED / UNKNOWN | CONTACT_SUFFICIENT_MARGIN_NEGATIVE; COLLISION_SUFFICIENT_MARGIN_NEGATIVE; −0.03191411 / −0.5771177 | PROOF_COMPLETE / UNKNOWN_ON_SUPPLIED_TUBE / PROOF_COMPLETE_COMMON_UNKNOWN | Segment 0: +0.03394828 / +1.653607; segment 1: −0.006612345 / +1.341276 |
| 3 | state_low_neg__scene_d100_l-200__T_020__V_p1_m1 | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | +0.1132906 / +1.838202 | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | +0.1133446 / +1.871995 |
| 4 | state_low_mid__scene_d100_l+000__T_050__V_p1_0 | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | +0.06989869 / +1.700397 | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | +0.07107793 / +1.836148 |
| 5 | state_low_pos__scene_d100_l+200__T_100__V_p1_p1 | UNKNOWN / NOT_EVALUATED / UNKNOWN | CONTACT_SUFFICIENT_MARGIN_NEGATIVE; +0.05895006 / −0.3093893 | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | +0.07670910 / +1.356184 |
| 6 | state_high_neg__scene_d200_l-200__T_020__V_m1_m1 | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | +0.2012249 / +1.736586 | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | +0.2012238 / +1.780700 |
| 7 | state_high_mid__scene_d200_l+000__T_050__V_m1_0 | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | +0.1493575 / +1.576874 | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | +0.1508674 / +1.768094 |
| 8 | state_high_pos__scene_d200_l+200__T_100__V_m1_p1 | UNKNOWN / NOT_EVALUATED / UNKNOWN | CONTACT_SUFFICIENT_MARGIN_NEGATIVE; +0.1094961 / −0.5835861 | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | Segment 0: +0.1766477 / +1.652144; segment 1: +0.1355008 / +1.331980 |
| 9 | state_low_neg__scene_d020_l-200__T_020__V_m1_0 | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | +0.03776146 / +1.838109 | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | +0.03782195 / +1.871949 |
| 10 | state_low_neg__scene_d020_l-200__T_020__V_m1_p1 | CERTIFIED / PASS_ON_SUPPLIED_TUBE / CERTIFIED | +0.03776087 / +1.837911 | PROOF_COMPLETE / PASS_ON_SUPPLIED_TUBE / CERTIFIED | +0.03782195 / +1.871869 |

For R3, query 1 loses on collision margin; query 2 loses on both collision and contact margins; queries 5 and 8 lose on contact margin. The Auer common predicate accepts the supplied tubes on queries 1, 5 and 8. On query 2 the Auer common predicate returns UNKNOWN because the collision lower bound on segment 1 is negative, even though both contact lower bounds and the other collision segment are positive. The Auer composition audit passes on that row because it independently replayed proof-to-common composition; that audit PASS does not turn the negative collision margin into a certificate.

## Cost measures and saved measurements

Definitions used in the tables:

- **Proof bytes:** actual byte length of the saved native proof.json file, checked against the reported serialized size.
- **Worker wall:** guard_result.elapsed_wall_seconds from the saved method worker guard, measured through worker exit and stdout flush. It excludes the later offline composition audit.
- **Worker peak memory:** peak process memory reported by the Windows Job guard for that matched method worker.
- **Audit wall:** outer_wall_seconds from the separate composition-audit guard. It measures the later read-only offline replay envelope and is reported separately from worker wall.
- **Audit peak memory:** peak_process_memory_bytes recorded for the separately guarded composition auditor. “N/A” means the R3 audit was correctly not launched because no complete proof/common/guard tuple existed.

All per-method resource caps were 1 GiB; recorded wall caps were 120 seconds. These are observed process measurements, not estimates from proof size.

| # | R3 proof B | R3 worker s | R3 worker peak B | Auer proof B | Auer worker s | Auer worker peak B |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 109,003 | 0.719 | 53,223,424 | 223,710 | 1.359 | 56,029,184 |
| 2 | 108,920 | 0.765 | 52,322,304 | 11,524,568 | 5.500 | 123,289,600 |
| 3 | 121,004 | 2.063 | 55,152,640 | 225,104 | 1.360 | 55,910,400 |
| 4 | 109,023 | 2.156 | 55,332,864 | 223,364 | 2.015 | 55,422,976 |
| 5 | 108,679 | 0.765 | 52,895,744 | 756,435 | 1.797 | 59,207,680 |
| 6 | 120,880 | 2.094 | 56,332,288 | 225,212 | 1.391 | 55,353,344 |
| 7 | 109,056 | 1.782 | 56,033,280 | 223,605 | 1.406 | 55,599,104 |
| 8 | 108,787 | 0.688 | 52,232,192 | 11,480,237 | 5.266 | 123,445,248 |
| 9 | 121,132 | 2.094 | 55,259,136 | 225,106 | 1.734 | 54,837,248 |
| 10 | 121,000 | 2.469 | 55,758,848 | 225,137 | 1.531 | 55,656,448 |

| # | R3 audit status | R3 audit outer s | R3 audit peak B | Auer audit status | Auer audit outer s | Auer audit peak B |
|---:|---|---:|---:|---|---:|---:|
| 1 | AUDIT_NOT_APPLICABLE | N/A | N/A | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 7.656 | 55,181,312 |
| 2 | AUDIT_NOT_APPLICABLE | N/A | N/A | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 3.797 | 91,844,608 |
| 3 | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 3.719 | 55,582,720 | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 3.125 | 55,009,280 |
| 4 | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 5.750 | 55,574,528 | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 3.125 | 54,890,496 |
| 5 | AUDIT_NOT_APPLICABLE | N/A | N/A | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 3.594 | 58,302,464 |
| 6 | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 3.313 | 55,566,336 | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 2.890 | 55,721,984 |
| 7 | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 3.188 | 55,488,512 | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 2.985 | 55,697,408 |
| 8 | AUDIT_NOT_APPLICABLE | N/A | N/A | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 3.407 | 90,873,856 |
| 9 | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 4.016 | 55,111,680 | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 3.421 | 55,087,104 |
| 10 | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 4.219 | 55,218,176 | PASS_PROOF_TO_COMMON_COMPOSITION_REPLAYED | 4.063 | 54,800,384 |

Descriptive totals: R3 worker wall sums to 15.595 s and Auer to 23.359 s. Median worker wall is 1.9225 s for R3 and 1.6325 s for Auer. R3’s lower ten-row total is driven by fast UNKNOWN exits; among the six pairs certified by both methods, R3 worker wall sums to 12.658 s and Auer to 9.437 s. R3’s six applicable offline audits sum to 24.205 s; Auer’s audits on those same six pairs sum to 19.609 s. Auer additionally has four audits on its other method results, whereas R3 correctly has none for its four native UNKNOWN results.

Total serialized proof bytes are 1,137,484 for R3 and 25,332,478 for Auer. R3’s largest proof is 121,132 bytes; Auer’s two largest are 11,524,568 and 11,480,237 bytes on queries 2 and 8. Peak matched-worker memory is 56,332,288 bytes for R3 and 123,445,248 bytes for Auer. These figures suggest a proof-size and peak-memory advantage for R3 on this pilot, but do not show an efficiency/usefulness advantage: R3 covers fewer pairs, exits quickly on four UNKNOWNs, and uses more worker wall and audit wall on the six jointly certified pairs. These selected rows do not establish expected cost or coverage for the full universe.

## Per-pair result and proof hashes

The hashes below bind the exact IDs to their saved result and proof bytes. The accompanying JSON ledger contains the full SHA-256 inventory for all 156 referenced authority, stage, result, proof, guard, terminal, common-result, and audit artifacts.

| # | Query ID | R3 result SHA-256 | R3 proof SHA-256 | Auer result SHA-256 | Auer proof SHA-256 |
|---:|---|---|---|---|---|
| 1 | state_high_mid__scene_d050_l+000__T_050__V_0_0 | 6f169aeab9a969a94e0af8fd08079333b4cc1c6f73d8544a63405ae746cf660a | b6757cf9a9fb0239ace5d6e3bb8c98793646282977f7b654d4b3f1f0c9fb6292 | 513e3effd856c9da89e2b2a0bb7223b7d102ea8a1fa2afbdb15cfde3a8026682 | 19a33a9ed8b42f20a63cb49ba57250637449544e3233c0ae1e05e6c587ce424a |
| 2 | state_high_pos__scene_d050_l+200__T_100__V_0_p1 | 8f675fac5014ca904db7936fbbc8883c4db8888fa893ca987753f13b3b9badfe | be319941cdff569c5842afe3801c0a6b26092f34b151359a15f76f5f6f42871e | 4b5d0cf3ac0c22faa375d53c664e1cc94dcc08f62254d21f9e43e3abc5df617f | ba2858eace2208753791d90c7fd6e3990b1ad5a736ef74d0ce3dfb3686bb8c9a |
| 3 | state_low_neg__scene_d100_l-200__T_020__V_p1_m1 | 36dfc00ed90f3f7123483bb3a130cd5b4e4be7feb81743257fe5c9ee89f1f406 | af2460ef2da773fd2749c9749abf625e24a9d251f24a2ccddcb8c0bcb6428584 | 50dd11e61462cdd4acbcf1b108d303d532da338107592c543107cd6ba1514ee4 | beb31a8e88a84a314cdb7b5a97deb1a44ed511343564f734f60a6d5f4dc0bc01 |
| 4 | state_low_mid__scene_d100_l+000__T_050__V_p1_0 | 363c87dd3fac2745ff25fb69c2c5f2744f595de9f34f5a88ec33ec0c30692698 | 1bdea1159ca1514ef822cad2c7e130604d12c22bdf684ff7eff8a9d351cd22f8 | 2c2144071c53c86b1b7baaa32492b6eb5bedc41a7a16e9d88bef07a05f1e4ac6 | 81f581657879c8e9c4d77e40fa09ad75ab0dad6369292fd797e153bc68106b32 |
| 5 | state_low_pos__scene_d100_l+200__T_100__V_p1_p1 | d6fd3bb28f6c2cf138692c916fb7e206bd84dc9382af86d799fc00b0f6874426 | 2165983850d5138c02b56b9dd206960c4b2394bba7aa189d0b931095463575ff | 02435adffd8264264db1db0079ff33df0d0d483f7665ae4fc7e03a47af05e3a1 | 7f92488baa2bca20c28ffd1a83c817e4704dab6f7f12588fa0e3f38707c01a90 |
| 6 | state_high_neg__scene_d200_l-200__T_020__V_m1_m1 | 9bbddfeb0d6c0c5720a380433acdc07623a1926ba536c2b2d3f673be6c4aac7f | 7e95712909c7f22f9089ca593b4ac2dc870e6fac268aeb120f88a6eae8f6203f | 269f5169db240dedf30b4b2e190add591f694be7dc3be4b0502fda6a0af28edc | 5f10753b4ff891767dd57511c0df1bf86e2f82500b7ac8a8ed081e3133463d33 |
| 7 | state_high_mid__scene_d200_l+000__T_050__V_m1_0 | 76d141997ea912636d8257815bf9ce5c4325999b86abca1f0226401b4d8d9709 | f6926c55b88c4f364588fe4b831d81e7a56687b0a1e756aee7b2243557f8a6ac | 46b66f26197a0df66a5f96623bf63bf5881ddcbf0b53ea0886842e149b61c42c | 2c852378eb0f6ce415259a7bb3e7ee99a660ca777649fbe5448699fdc256b2b1 |
| 8 | state_high_pos__scene_d200_l+200__T_100__V_m1_p1 | 375356a9d5eaaba30cfce8740fd5f493e9134c4dac24c81e1b2f73cae316f79f | 18471b4c8c49c88d4cf6f319dab0638035aabc0d3f55643565b12ef52cdee070 | 7c2cd5ccefe5fdd2db4a08e4f9f9e01c20dbcb0af2fda1bdbc6a1135a0df221e | af9cc1bf6def865c507c54f625ef106b46673a54a296cc45dbfc8f4984f41657 |
| 9 | state_low_neg__scene_d020_l-200__T_020__V_m1_0 | 0b410ed95b109c7101192c0201e3bd0c7275fe536dd5a58f9e55dc1ccc691e55 | fd040b83b1d0235c5c6a1d63daaf5bb4dfb85f23ff55b6172d69bb4305ace0af | e3e267c38743cd32c12323ee15401e2ea50eb24c7c446cadbb7745dbcbb4257c | 62f3a45f149dd8a727a503c041691a93412fb8ac3c5346d0a9970eda1a5e0595 |
| 10 | state_low_neg__scene_d020_l-200__T_020__V_m1_p1 | 5cf342beab793997a1c48e4cd68e1756e96833f9a032afc8692df8632b045670 | b27c19ef5ad15cffc994619843f377961597ae4f28eace14d948284cf4356dff | b5f7071abec2432a8f97af9875ea9d3dac83e50dfbc3bcd6a05006528d353c10 | 63def7c130588f51d113d393fd978f0adf5fa5b1d83e9241fe87bfecb9673b74 |

## Source, replay, and preservation ledger

The R19 stage authorization was exact-scope for r19_continuation_01 and the ten ordered IDs. Its bound candidate hashes were manifest 9f926ddc17b4a7711ba4a9e1d8658832ac5e21a50bb2a953d41adef3c6064c2c, source closure a50bc0452e6b8f164988a4af8d669e563381f157f86188ca8c7ee1fb1518ca76, and schedule 4271fd9339788e8372cdd4b8b48ecd9d61b7a0c10bdd7cebc7f79f9fcf1a5fd6. Ordered-ID digest: 555297305b09d9676e401c10b5e33772463e43e2379778c0ce806d2c7f9e649d. GO receipt SHA-256: 1ef1e7acbbb4376117737e0b1d601dbb7dd20185ac70a772b41418b23048fa51.

R20 accepted only retrospective replay. Its report records zero query/producer/auditor invocations for this verification and the following unchanged inventory comparisons: R19 stage, 282 files, inventory SHA-256 47c815b95cb5d0ab8ee8eb8c4259c6f2ad1c669d04fbf7171eac8b0fbf7d3a9a before and after; R19 candidate namespace, 99 files, 97056a0c96f23abca7c1c75095af93d902617b229311d2c4fc03aaf6dc2ab0d0 before and after; R19 source closure, 575 dependencies, c3f7df045eb7c34857da1276a3118376b623a7e4dde08ea77e9c88871152a4e7 before and after; and ten R19 pinned files, 948995f3a3241ebe0d5ef7f95c2c062af932ba339e85c9b4fbf6ee5452ee747e before and after. Codex R20 review also reports that no Windows reparse-point entries were present in the preserved R19 stage.

| Input artifact | Bytes | SHA-256 |
|---|---:|---|
| docs/CODEX_TO_LUNA_G4_AUER_R21_PILOT_SCIENTIFIC_TRIAGE.md | 2,629 | 82d945d90cdf17f515221901ac57b9d97265493d4d77878f2a0c7378bbcc156c |
| docs/reviews/CODEX_G4_AUER_R20_PATH_BINDING_REVIEW.md | 4,749 | ec7c9cc3e7f24e3f512595171a60269ee1ec7c40ba30337813030f36267412be |
| docs/reviews/LUNA_TO_CODEX_G4_AUER_R19_STAGE_01_EXECUTION_FULL_HANDOFF.md | 70,314 | 593f9de10a2a3fbc17532ff8827635882062a8e6f6425c535f30dcebb87ca6ce |
| docs/reviews/LUNA_TO_CODEX_G4_AUER_R20_PATH_BINDING_FULL_HANDOFF.md | 14,080 | ab62440511655173fe298a6f1345e4b46ca73731b9788fb935e79c2a4a4cd799 |
| R19 Stage 1 intent | 2,460 | 9604c9fae13d338eebe86d57b98839168f8007dc571496721b6c2f636a750ea8 |
| R19 Stage 1 terminal receipt | 3,405 | 662211f65c6b73449c86e2c2e3fdc0a0e2ba44c3f03682243df479130bbbd7a4 |
| R19 exact-scope GO receipt | 2,302 | 1ef1e7acbbb4376117737e0b1d601dbb7dd20185ac70a772b41418b23048fa51 |
| R20 read-only replay report | 21,369 | a192b662a0703014c55c3f68caaac857bf04ef73b9da10ac612b118271c7955b |

R21 extraction artifacts:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| validation/scripts/analyze_g4_auer_v3_r21_pilot.py | 11912 | a22afc6c979296cfb575413120257326d45f4eefe51b7d5dae00d81efe1d3df4 |
| results/validation/g4/auer2013/protocol_v3_r21_pilot_triage/pilot_artifact_analysis.json | 649,660 | 0ec6e9e8542deaa71c0686cf11fcc3e9058c30f7e895b709487d3cb862c14a5b |

The analysis script reads the exact R19 ten-pair stage and R20 replay report, checks the ordered attempted/completed IDs and per-method query/guard identities, records proof byte lengths, margins, worker/audit measurements, and calculates SHA-256 for every input artifact. It writes only the derived JSON ledger in the R21 triage namespace. It invokes no query, producer, worker, composition auditor, checker, stage runner, or batch entrypoint. The JSON has 156 path/size/hash ledger entries, including every saved result, proof, guard, terminal, available common result, and audit artifact used here.

## Fixed denominator and status

The fixed universe remains 1,944 IDs. Four historical IDs stay in their original strata, separate from R19. R19 Stage 1 consumed and completed ten matched IDs; 1,930 continuation IDs remain unattempted. This R21 analysis added zero queries. No ID was retried or substituted. No stage or full batch was run.

## Scientific recommendation

**Stop before any full 1,944-query batch. Conditionally support a future, limited prospective comparison** only after a new, separately versioned candidate and exact-scope GO process are reviewed. This pilot justifies asking whether R3’s much smaller proofs and lower peak memory can be converted into useful coverage under the existing common predicate. It does not yet show that result: R3 certified fewer selected cases, and on the six jointly certified rows its measured worker and audit wall were not lower than Auer’s.

Additional IDs should answer whether the observed difference persists on a prospectively selected set spanning the frozen schedule’s scenario/state strata, and whether any reduction in R3 resource use is worth its UNKNOWN rate. The exact ID selection, order, method versions, thresholds, and cost measures must be frozen before those outcomes are seen. Do not change either method or threshold in response to this pilot. If a new method version is developed, treat it as a separately identified candidate and evaluate it prospectively on IDs not used to tune it.

Evidence that could support a DDWMR-specific contribution would require a sound, reproducible method-specific construction and a prospective result showing useful common-predicate certification coverage with a clear and material computational advantage on the locked domain. Smaller proof files alone are insufficient. If the prospective comparison instead reproduces lower R3 coverage, no R3-only certifications, and negative contact/collision sufficient margins while Auer covers more at acceptable cost, that would strengthen the existing usefulness/novelty blocker. Neither outcome alone closes G4 literature review or proves physical-platform safety.

Before any future exact-scope GO, the prospective package must include:

1. A separately versioned runner and independent checker with a fail-closed exact-stage entrypoint, no-retry/no-substitution behavior, immutable output root, and saved stdout/stderr/intent/terminal records.
2. A frozen source closure with path, size, and SHA-256 pins for every runner, checker, method, common predicate, resource profile, and input artifact; rehash it before and after the stage.
3. A prospectively locked exact ordered ID schedule and manifest, with the authorization receipt bound to the candidate hashes, schedule digest, review decision, and resource limits.
4. Windows reparse-point protection for every path component, including directory junctions as well as symbolic links. The guard must verify the exact expected in-stage artifact and resolved target/file identity. Add a non-query negative fixture that creates or detects a junction/reparse point escaping the stage and proves rejection without relying on administrator-only symlink privileges; otherwise provide an independently reviewed equivalent Windows reparse-point check. Preserve the existing outside-stage, traversal, and wrong-in-stage-file fixtures.
5. A separate exact-scope Codex GO after review. This triage handoff is not that GO and authorizes no future stage.

No query, producer, worker, composition audit, stage, or batch was run for R21. R19 and R20 evidence remains unchanged. No commit or push was made.
