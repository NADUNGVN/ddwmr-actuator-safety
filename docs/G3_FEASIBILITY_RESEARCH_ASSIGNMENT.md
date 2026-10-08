# DDWMR — independent G3 feasibility and prior-art research assignment

**Purpose:** decide whether the project should invest in a G3 construction for sampled recursive safety, before any G3 implementation or numerical campaign.

**Repository:** `NADUNGVN/ddwmr-actuator-safety`  
**Session:** `DDWMR | G3-FEASIBILITY-RESEARCH`  
**Authoritative model:** `research_context/MASTER_RESEARCH_CONTEXT_v2.md` (adopted v2.1)  
**Current gate:** `HOLD`; G1 restricted PASS; G2/G3/G4 and physical-platform correspondence UNVERIFIED.

**Owner request, 2026-10-08:** publish the current repository and prepare a research handoff so an independently started agent can decide whether this direction is worth continuing. This is an independent feasibility assessment. G3 is a proposed direction, not a contribution already selected or accepted.

Use the public repository at <https://github.com/NADUNGVN/ddwmr-actuator-safety>. Pin the full Git commit containing this assignment before research. If working from a checkout, report `git rev-parse HEAD`; if using browser access, use commit-specific source URLs. Do not treat a later moving `main` as the same reviewed snapshot.

## 1. Read first

Read these files in full before making a scientific claim:

1. `AGENTS.md`
2. `research_context/MASTER_RESEARCH_CONTEXT_v2.md`
3. `research_context/DECISION_LOG.md`
4. `research_context/LITERATURE_MATRIX.md`
5. `research_context/REVIEW_GATE.md`
6. `docs/reviews/autonomous_w2/CODEX_W2_FINAL_DISPOSITION_2026_10_08.md`
7. `docs/reviews/autonomous_w2/g2/LUNA_TO_CODEX_G2_W2_V6_FINAL_FROZEN_RESULT_AUDIT_FULL_HANDOFF_v1.md`
8. `docs/reviews/autonomous_w2/g4/LUNA_TO_CODEX_G4_W2_V6_FINAL_RESOURCE_ATTRIBUTION_FULL_HANDOFF_v1.md`
9. `docs/reviews/CODEX_DDWMR_SCOPE_PROGRESS_VERIFICATION_2026_10_07.md`
10. `docs/RESEARCH_PUBLICATION_2026_10_08.md` and its linked machine-readable inventory.

MASTER and the four `research_context/` files are authoritative when older notes disagree.

## 2. Evidence that must be treated as fixed background

The completed W2 package is accepted only as a finite, hash-bound synthetic development record. Its three corrected v6 rows replayed successfully; one action met the declared task threshold. The local Auer reconstruction stopped at a frozen exact-rational resource guard on the three reused development rows. The result is a scoped implementation/profile observation, not a claim of mathematical Auer failure, universal v6 superiority, physical safety, practical superiority or generic novelty.

The final W2 conclusion is `NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE`. Do not reopen the old 800-row or 1,944-row batches merely to increase counts. Do not present the W2 development rows as held-out confirmation data.

The scientific chronology matters:

| Evidence | Supported reading | Unresolved question |
|---|---|---|
| Cases A/B/C | Accepted finite synthetic hand certificates in their stated scopes | General useful computation and novelty |
| R3 archived batch | 1,944 replayed records: 1,196 `CERTIFIED`, 748 proof-complete `UNKNOWN` | Research-domain usefulness and method advantage |
| Selected ten-pair historical Auer pilot | Auer 9 certified versus R3 6 on that declared pilot | No universal coverage ordering follows |
| W2 corrected reused development task | Three v6 safety certificates; only `(1,1)` satisfies the `7/20 m` progress threshold over two seconds | Cross-method usefulness beyond local profile availability |
| W2 local Auer reconstruction | Three `RESOURCE_LIMIT` results before any accepted step | Mathematical ability is not determined by an exact-rational bit guard |

W2 uses a 96-bit outward grid in v6 and exact reduced rationals in Auer. Its resource-limited outputs do not isolate a mathematical-method advantage. The W2 final reports supersede the earlier progress checkpoint when interpreting current results. An older STATUS record that still says the peer audit was pending describes its issuance time; the final G2 audit and Codex disposition resolve that scientific review.

The original paper target includes a defended useful enclosure/contribution and recursive safety. A one-hold-only paper has not been adopted as a substitute. Assess whether the full target deserves further work; do not assume that adding a generic predecessor induction would supply novelty.

## 3. Research question

Assess whether there is a defensible, plant-specific G3 direction for the adopted nine-state reduced DDWMR model:

- motor-terminal voltage is the held input and is piecewise constant over a fixed hold;
- hidden model labels are fixed for the complete execution but unknown to the policy;
- hidden parameter uncertainty has positive width; a useful set must include moving states and have meaningful extent beyond rest states;
- collision and algebraic contact admissibility must hold continuously over the whole hold;
- the next state must return to a useful robust set for repeated operation.

The target is a **useful** set and policy, not merely a nonempty rest state:

\[
K_T \subseteq S_{\mathrm{rob}}, \qquad
K_T \subseteq \operatorname{Pre}^{c}_T(K_T).
\]

The policy must use information actually available to it. It may not select a voltage using an unobserved fixed parameter realization (oracle selection).

MASTER assumes exact state observation at sampling instants. Positive-width initial boxes are verification domains, not an unstated measurement-noise model. The robust action quantifier is state-dependent `for each sampled state, there exists one admissible voltage valid for every hidden label`; it is not a separate voltage for each label. If a proposed history-dependent information set improves fixed-parameter conservatism, explain how it differs from the MASTER state-only target and mark it as a scope proposal. Parameters are never reset when a hold is subdivided or another hold begins.

## 4. Required investigation

### A. Prior-art audit

Find and inspect primary sources that are close to this exact combination:

- sampled or zero-order-hold recursive safety;
- robust reachability or predecessor sets with fixed parameter uncertainty;
- inter-sample collision guarantees;
- actuator, motor-voltage or wheel/contact dynamics;
- state-only or observation-based safety-filter policies.

For every important source record:

- complete citation and DOI or stable URL;
- full-text access status;
- exact equation, theorem, algorithm or page locator;
- plant, input level, uncertainty model, contact model and safety guarantee;
- what is genuinely covered and what is not.

Do not infer a theorem from a title or abstract. Unknown coverage is not negative evidence.

### B. Candidate construction screen

Screen at most three clearly stated candidate constructions. For each candidate specify:

1. the state/parameter domain and the robust safe set;
2. the admissible voltage information and policy map;
3. the one-hold enclosure or predecessor computation;
4. the continuous collision/contact proof obligation;
5. the endpoint-return condition;
6. the quantifier order over initial states, fixed hidden labels and voltage;
7. why the construction is plant-specific rather than generic reachability with renamed variables;
8. the smallest proof or counterexample needed to decide feasibility.

Candidates may be rejected if they require unobservable parameters, assume a braking mode that was not proved, reduce to a symmetric special case without covering independent side uncertainty, or establish only instantaneous input feasibility.

### C. Contribution test

Separate the following labels:

- already established generic machinery;
- plant-specific adaptation with no demonstrated advantage;
- a plausible new construction;
- an unsupported assertion;
- an obstruction or counterexample.

Explain whether the proposed construction could change a safety/action decision or certified coverage under a predeclared criterion. A narrower bound, smaller proof file or one synthetic success is not by itself usefulness or novelty.

Prioritize robust sampled-data invariant sets, terminal/backup-set safety filters, constrained reachability and viability constructions alongside CBF work. The Auer IVP baseline is relevant to validating flows; it is not the only comparison needed for a recursive-set claim. Existing entries in the literature matrix are leads to recheck, not a complete or current novelty search. Include credible primary sources available up to the research date and disclose access limitations.

The analysis may derive necessary conditions, examine quantifiers, propose proof sketches and identify counterexamples. It should finish with one best hypothesis and a clear scientific decision. It need not deliver a complete G3 construction during this assessment. If G3 is not promising, identify at most one defensible alternative research hypothesis, or recommend stopping the present paper direction. Do not replace the failed W2 claim with a broad unsupported statement that no DDWMR contribution can exist.

## 5. Forbidden work in this stage

This is a research and prior-art feasibility stage only.

- Do not implement G3, a controller, a simulator, hardware experiment or safety filter.
- Do not run the legacy G2/Auer batches, solver workers or new numeric certificates.
- Do not change `MASTER_RESEARCH_CONTEXT_v2.md`, `DECISION_LOG.md`, `LITERATURE_MATRIX.md` or `REVIEW_GATE.md`.
- Do not alter W2 releases, historical results, gate statuses or source snapshots.
- Do not silently relax thresholds, uncertainty sets, contact assumptions or resource limits.
- Do not claim physical-robot safety, completed recursive safety, established novelty or paper readiness from this research assessment.

Writing a new report in the path below is permitted. Keep all other repository files read-only.

## 6. Required output

Write one self-contained Markdown report at:

`docs/reviews/G3_FEASIBILITY_PRIOR_ART_RESEARCH_FULL_HANDOFF.md`

The report must include:

- the exact repository commit and files read;
- a short Vietnamese executive summary: what is worth continuing, why, what remains unknown and the next concrete proof milestone;
- the research question and formal assumptions;
- the source-by-source prior-art table with locators;
- up to three candidate constructions and their quantifiers;
- feasibility blockers and any counterexamples;
- a clear distinction between established facts, derived results, conjectures and unknowns;
- one final disposition, chosen exactly from:
  - `ADVANCE_G3`
  - `REVISE_HYPOTHESIS`
  - `STOP_G3`
- the minimum next proof obligation if the disposition is `ADVANCE_G3`;
- limitations and claims that must not be made.

Use the headings **Finding**, **Evidence**, **Consequence**, **Status** and **Required action** for disputed or decisive claims. The report is an input to a later owner decision; `ADVANCE_G3` does not itself authorize implementation.

Return an actual `.md` file that the owner can send back to Codex. If repository writes are unavailable, provide a downloadable Markdown artifact with the same filename; do not leave the report only in chat. Conclude with unchanged gate statuses. Final chat reply should contain exactly three short lines:

```text
Session: DDWMR | G3-FEASIBILITY-RESEARCH
Status: ADVANCE_G3 / REVISE_HYPOTHESIS / STOP_G3; one factual reason
Handoff: path or download link to the completed .md file
```

## 7. Success criterion for this assignment

The assignment is complete only when an independent reader can answer:

> Is there a specific, non-oracle, plant-relevant recursive-safe-set construction worth authorizing and implementing under MASTER v2.1, and what exact proof would decide it?

If the answer is no or not yet, state that directly. A negative feasibility result is useful and should not be converted into another metadata or batch-preparation cycle.
