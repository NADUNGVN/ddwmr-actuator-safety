# Codex review — G2 decision-domain preflight

**Date:** 2026-10-03  
**Lane:** `LUNA-G2-SCOPE`  
**Input:** `LUNA_TO_CODEX_G2_DECISION_DOMAIN_PREFLIGHT_FULL_HANDOFF.md`  
**Repository:** `main` at `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`; shared working tree contains unrelated, unpublished G4 work.  
**Authority:** MASTER v2.1. **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.**

## Decision

**ACCEPT the R3 UNKNOWN-cause diagnosis as a reproducible, post-hoc analysis of the frozen synthetic archive.** Accept the provenance matrix as a careful statement that the sources examined do not supply a complete MASTER-compatible physical domain. **RETURN the 800-query decision protocol for revision; NO-GO to freeze or run it.** This review does not change any gate.

I read `AGENTS.md` and the four canonical `research_context/` files, the handoff, analysis source and outputs, provenance matrix, candidate protocol, and the preceding scoped R3 review. I did not run a new G2 query, edit archived records, or alter G4 work. I independently streamed the raw pilot and gzip continuation records to check the decisive counts and signs.

## 1. R3 archive diagnosis

**Finding.** The handoff's aggregate counts and UNKNOWN classification match the frozen records.

**Evidence.** Direct read-only parsing of the 216-row pilot and 1,728-row compressed continuation found 1,944 unique IDs: 1,196 `CERTIFIED`, 112 collision-only `UNKNOWN`, 343 contact-only `UNKNOWN`, and 293 both-negative `UNKNOWN`. The totals are 405 negative collision margins, 636 negative contact margins, and 748 `UNKNOWN`. Horizon counts are 621/27 at 0.02 s, 567/81 at 0.05 s, and 8/640 at 0.10 s (`CERTIFIED`/`UNKNOWN`). The 216 groups have certified-action counts 9 in 132 groups, 1 in eight groups, and 0 in 76 groups. Every one of the 140 groups with any certificate includes zero voltage. No archived `CERTIFIED` row has a negative sufficient margin, and no archived `UNKNOWN` row lacks one. Raw record SHA-256 values match the handoff: pilot `fdbce2ac5587247ababc0849c5fce8f9a596c3eb2175ed277545072c06acdc43`; gzip continuation `352b6c67480133350a7d1bfc89334a1beff1dc27c64cfda46391af27982fa874`. The five new analysis/document hashes also match the handoff.

**Consequence.** The diagnosis explains the recorded sufficient-test abstentions. It does not independently replay the enclosure proof or show actual collision/contact failure. The previous R3 source-to-inclusion review remains the basis of its narrowly accepted certificates.

**Status.** **VALID** as post-hoc archive accounting; no new G2 certificate or gate pass.

**Required action.** Preserve the 1,944 denominator, input hashes, and `UNKNOWN` meaning. Do not call this a held-out result.

## 2. Parameter and contact provenance

**Finding.** The R3 values and proposed task inputs remain synthetic. The examined sources provide fragments, not a coherent physical parameter/contact family for MASTER v2.1.

**Evidence.** The matrix maps every R3 parameter, unit and fixed-label relation to the benchmark config. It distinguishes paper-specific motor/body point values, product documentation and the missing joint uncertainty, wheel-side/terminal-voltage, slip-force, lateral reserve and support evidence. It does not combine values from different robots. The source locators and access status are recorded, but this review did not independently reopen every external PDF or product page; the supported conclusion is limited to what this source pass furnished. Failure to find a compatible family in these sources does not prove that none exists elsewhere.

**Consequence.** The proposed study can test a formal mathematical domain. It cannot establish hardware safety or practical parameter relevance.

**Status.** **VALID** synthetic/provenance boundary; physical-platform correspondence **UNVERIFIED**.

**Required action.** Keep the source-level distinctions and withhold all hardware and practical-domain claims.

## 3. Query universe and scientific question

**Finding.** The candidate defines a coherent finite, one-hold, common-voltage task grid, but it is an exploratory synthetic progress study.

**Evidence.** Four nine-state boxes, four circles, two fixed horizons per query, and 25 bounded voltage pairs give 32 groups and 800 rows, split 400/400 by scene. The initial intervals have positive width. The task metric `inf[p_x(T)-p_x(0)]` uses world-frame displacement and is distinct from full-hold collision/contact admissibility. Each query quantifies one voltage over its complete initial box and execution-fixed parameter image. The task is described as an “aisle” although only one circular obstacle is specified; there are no aisle walls. The 5 cm threshold and 8/16, +4 criteria are predeclared mathematical choices, without an external task requirement. The two horizons impose different average-speed requirements for the same 5 cm displacement. The held-out factor is scene geometry only, and R3 results were already inspected.

**Consequence.** A successful run could support a finite synthetic action-selection statement, with exact group numerators and paired comparisons. It would not by itself establish practical usefulness, statistical generalization, or online filtering.

**Status.** **VALID as a candidate synthetic question; NOT YET FROZEN.**

**Required action.** Describe the geometry as forward progress near a circle, or specify actual aisle boundaries. Justify the fixed-distance threshold and report outcomes separately by horizon. State the development/evaluation split as non-blind and scene-only.

## 4. Endpoint progress and implementation prerequisite

**Finding.** The primary task outcome currently has no reviewed computation or replayable proof.

**Evidence.** Archived R3 records certify full-hold collision and contact for different queries; they do not carry a sound lower bound for the correlated difference `p_x(T)-p_x(0)` on the proposed boxes. A full-time position hull alone does not establish this terminal metric. The candidate itself defers an endpoint enclosure/checker and has no 800-ID machine manifest. The preceding R3 review accepted the frozen clip profile only and noted incomplete transitive provenance and a cooperative, rather than hard, 15-second deadline check.

**Consequence.** Neither task eligibility nor a confirmatory denominator can presently be computed. A new profile must bind the full source closure, and any 15-second claim must reflect actual enforcement.

**Status.** **BLOCKER to freeze/run the decision study.**

**Required action.** Derive a rational outward lower bound for `p_x(T)-p_x(0)` for every initial state and one fixed parameter realization throughout each trajectory, then implement independent record replay for that bound. Review the inclusion argument and checker before any candidate-task evaluation. Generate and hash the exact 800-ID manifest and transitive dependencies after the protocol is corrected. Preserve the old R3 bytes.

## 5. Nominal-only criterion

**Finding.** The nominal-only comparison criterion has a logical defect as an acceptance rule.

**Evidence.** By definition the selector retains `V_nom` whenever it is eligible. Its candidate set also contains `V_nom`, so its task-success set contains the nominal-only success set. The proposed condition “at least two more groups, **or ties while retaining nominal**” automatically accepts a tie, yet rejects the case of exactly one additional successful group. A tie shows preservation, not value from alternative voltages. The primary comparison with zero-only is a separate question and is not affected by this observation.

**Consequence.** The current nominal-only row cannot support an improvement claim and does not consistently rank the possible finite outcomes.

**Status.** **NEEDS REVISION before protocol freeze.**

**Required action.** Report nominal retention as a policy invariant and exact count separately. For a claim that alternatives improve on nominal-only, require a predeclared positive paired gain (for example, at least two additional held-out groups); otherwise label a tie as preservation only. Preserve the zero-only and unique nonzero-certificate questions as distinct outcomes.

## 6. Longer holds and resource interpretation

**Finding.** The selected 0.25/0.5 s holds are a high-risk conservatism stress test, not yet evidence of usefulness.

**Evidence.** In the archived, shorter 0.10 s grid, 636/648 rows have negative sufficient contact margins. The proposed profile uses one whole-hold panel and the same exact-arithmetic caps. This does not prove that any new row will be `UNKNOWN`, because the new states and scenes differ; it does make the planned usefulness conclusion contingent on substantially longer-horizon enclosure behavior. The R3 code checks its 15-second deadline cooperatively, so “15 seconds per query” is not presently a hard cap.

**Consequence.** A negative or resource-limited 800-row result would still be reportable, but it would not establish the proposed usefulness claim. Timing cannot be described as a hard online deadline.

**Status.** **RISK / wording correction**, not a proof of protocol infeasibility.

**Required action.** Keep every outcome and cap hit in the fixed denominator, report by horizon, and call wall timing cooperative unless an outer process guard is added and reviewed. Do not alter evaluation cells after seeing their outputs.

## Final disposition

**G2 archive diagnosis ACCEPTED; candidate protocol RETURNED FOR REVISION; freeze/run NO-GO.** `LUNA-G2-SCOPE` should first correct the scientific acceptance logic and supply a reviewed terminal-progress inclusion/checker, then submit a new candidate manifest and source closure. G2, G3, G4 and physical correspondence remain UNVERIFIED; overall HOLD.

**Vietnamese forwarding summary:** Tôi xác nhận lại 1.944 dòng R3 và phân rã 748 `UNKNOWN`. Protocol 800 truy vấn có câu hỏi tổng hợp rõ, nhưng chưa có proof/checker cho tiến độ cuối hold và tiêu chí so nominal-only có lỗi logic. Chưa freeze/chạy. Giao `LUNA-G2-SCOPE` sửa protocol, chứng minh bound tiến độ, khóa manifest/source rồi gửi review lại; không nâng G2.
