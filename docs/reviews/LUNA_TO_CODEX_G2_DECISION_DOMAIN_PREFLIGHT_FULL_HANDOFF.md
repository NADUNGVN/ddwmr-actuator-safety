Session: DDWMR | LUNA-G2-SCOPE

# Luna → Codex — G2 decision-domain preflight full handoff

**Date:** 2026-10-03  
**Assignment:** docs/CODEX_TO_LUNA_G2_DECISION_DOMAIN_PREFLIGHT_v1.md  
**Repository:** D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety  
**Disposition:** R3 UNKNOWN causes and source gaps are documented; a candidate synthetic task study is specified; no new task evaluation was run. G2 remains UNVERIFIED and overall status remains HOLD.

## Finding 1 — workspace, scope, and isolation

**Finding.** The work stayed in the assigned G2 preflight scope on the shared working tree.

**Evidence.** At start, branch was main and HEAD was 94c60f627a2ce1a8d52101050bdc0ce9d2e59afe. The working tree was already non-clean, with active G4 edits and untracked G4 material. This pass did not switch branches, commit, push, or modify G4 sources, closures, manifests, or other G4 paths. It did not change validation/g2/, validation/g4/, validation/configs/, existing R3 inputs/records, research_context/, or previous reviews. The archive analysis only read frozen R3 inputs; the newly generated JSON/CSV hashes reproduce exactly. Source PDFs used for inspection were temporary files under tmp/pdfs; the four exact task-local PDF/text files were removed after source review, leaving the parent tmp tree intact.

Files delivered for this G2 scope:

1. validation/analysis/g2_decision_domain_v1/analyze_r3_decision_domain_v1.py
2. results/validation/g2/decision_domain_v1/r3_unknown_cause_summary_v1.json
3. results/validation/g2/decision_domain_v1/r3_record_margin_decomposition_v1.csv
4. research/benchmarks/G2_PARAMETER_CONTACT_PROVENANCE_MATRIX_v1.md
5. research/benchmarks/G2_DECISION_RELEVANT_STUDY_PROTOCOL_CANDIDATE_v1.md
6. docs/reviews/LUNA_TO_CODEX_G2_DECISION_DOMAIN_PREFLIGHT_FULL_HANDOFF.md

Each new Markdown report begins with the session line requested by the user. The handoff is the last path above.

**Consequence.** G4's same-tree work remains untouched by this G2 pass; the existing non-clean status must not be mistaken for a clean checkout.

**Status.** PASS for the assigned file/scope boundary. No commit or push.

**Required action.** Codex should review only the new G2 artifacts against the current tree; preserve all pre-existing G4 changes.

## Finding 2 — archive-analysis method and reproducibility

**Finding.** The R3 diagnosis is a read-only archive analysis, not an evaluator rerun or a fresh certificate.

**Evidence.** The script streams the pilot JSONL and gzip continuation, validates exact-byte input hashes, checks all frozen IDs and manifest partitions, parses proof rationals using Python Fraction, and writes display decimals only after exact comparison. It does not import G2 producer, evaluator, checker, or G4 code.

Python was 3.12.12 from C:/msys64/ucrt64/bin/python.exe. The command actually run was:

    & 'C:/msys64/ucrt64/bin/python.exe' 'validation/analysis/g2_decision_domain_v1/analyze_r3_decision_domain_v1.py' --workspace-root 'D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety'

The output hashes before and after rerunning that command were identical.

| Artifact | SHA-256 | Size |
|---|---|---:|
| validation/analysis/g2_decision_domain_v1/analyze_r3_decision_domain_v1.py | 49a155fd7a03c852a8c29a54f05466790a9a0991c63d8a61246699a538c31c15 | — |
| results/validation/g2/decision_domain_v1/r3_unknown_cause_summary_v1.json | ce642b8ebd34e679940e4a4e75c3e5bc97714814db33798c06ea1c32977ade1a | 453,273 bytes |
| results/validation/g2/decision_domain_v1/r3_record_margin_decomposition_v1.csv | ef402327839c4fbfa6ad3cf51abb5144083ac474eedc04100f3468d93f60b653 | 814,422 bytes |

Frozen input hashes and counts:

| Input | Raw SHA-256 | Semantic/decompressed SHA-256 | Records |
|---|---|---|---:|
| R3 pilot JSONL | fdbce2ac5587247ababc0849c5fce8f9a596c3eb2175ed277545072c06acdc43 | Same as raw | 216 |
| R3 continuation gzip | 352b6c67480133350a7d1bfc89334a1beff1dc27c64cfda46391af27982fa874 | Decompressed JSONL: de339ffcb5ee5e0c83f8d25e3077d9fd9316f83293982189aaffba0bdcf3b196 | 1,728 |
| Benchmark config | b2bc12cd578229cfb6df4b426f93e0f472d69f6be36929df93e797ff79396a9e | 21632e1eebf58a5d7fea14224254738d0ff11ba689b94343afa47adbccea166b | — |
| Development manifest | 794b314341e0c1ce7ff4fdbc7ddcde3f7d591e12b501e5ac7dd43175377be4e9 | e5c796fcfe8275b1b7106f112813d24b36d18626400ba149f29f4bee7b9c155d | 1,944 original IDs |
| Continuation manifest | ecddff5f5679534bc1204922029e93dc06b84508357b323d2cd218ca876d9dbb | 17cd7eefad56d74a2d487eae90298c6db62775945596a1946980198e52c9fe7a | 1,728 selected IDs |

The combined frozen universe is 1,944 unique queries with 1,944 proof-complete rows. The pilot plus continuation ID sets are disjoint and equal the original frozen ID universe. The JSON contains full status vectors for every state/scene/horizon group and summaries by state, horizon, scene, and action; the CSV contains one row per query with reason codes, collision/contact margins, decomposition fields, and stored elapsed time.

**Consequence.** The counts and decomposition are reproducible from the exact archive, but they do not independently replay or validate the enclosure mathematics.

**Status.** VALID as a deterministic archive audit. Not a fresh certificate, evaluator acceptance, or G2 PASS.

**Required action.** Keep the input and output hashes with any reuse. Do not describe the post-hoc archive as held-out or confirmatory task evidence.

## Finding 3 — cause of R3 UNKNOWN results

**Finding.** All 748 R3 UNKNOWN rows fail at least one sufficient lower-bound test: 405 have a negative collision margin and 636 have a negative contact margin; these sets overlap in 293 rows.

**Evidence.**

| UNKNOWN classification | Rows | Meaning of the record |
|---|---:|---|
| Collision-only | 112 | Collision sufficient lower margin is negative; contact sufficient margin is not negative. |
| Contact-only | 343 | Contact reserve sufficient margin is negative; collision sufficient margin is not negative. |
| Both | 293 | Both sufficient margins are negative. |
| Total UNKNOWN | 748 | 112 + 343 + 293; all have proof fields. |

The UNKNOWN decomposition by horizon is:

| Hold | Rows | CERTIFIED | UNKNOWN | Negative collision bounds | Negative contact bounds | Both |
|---|---:|---:|---:|---:|---:|---:|
| T=0.02 s | 648 | 621 | 27 | 27 | 0 | 0 |
| T=0.05 s | 648 | 567 | 81 | 81 | 0 | 0 |
| T=0.10 s | 648 | 8 | 640 | 297 | 636 | 293 |
| Total | 1,944 | 1,196 | 748 | 405 | 636 | 293 |

At T=0.02 and 0.05 s, every UNKNOWN is collision-only, and all contact lower margins remain positive (minimum margins +1.736508927536 N and +1.444164940030 N respectively). At T=0.10 s, the contact test is the dominant new failure: 636 of 648 rows have negative contact reserve margins. Across these rows the available-force lower bound is often zero because a whole-hold slip enclosure reaches a clip-saturated corner, while the lateral-demand upper bound remains positive. The median T=0.10 contact demand upper bound is 0.358046699151 N; the all-row contact-margin median is -0.358046699151 N. This is a conservative sufficient test, not an observation of physical loss of contact.

For the 405 negative collision rows, the bound compares minimum distance to the predictor's center-position rectangle against the inflated circle radius, then subtracts the pose-position error radius E_p. In 270 rows, center-rectangle clearance is already nonpositive. In 135 rows, center-rectangle clearance is positive but smaller than E_p. The median E_p among these rows is 0.023619060029 m and the median final collision margin is -0.030680766864 m. The center rectangle's location and extent are already represented in the distance-to-rectangle bound; its width is not an extra scalar penalty to subtract again.

The complete 216 group/action-vector result is 132 all-nine-certified groups, 76 all-UNKNOWN groups and eight mixed groups. All eight mixed groups are the same state/horizon pair, state_low_mid at T=0.10 s, repeated over eight scene geometries. Each has only V=(0,0) CERTIFIED; its contact margin is +0.127641589431 N. The other eight actions have negative contact margins, while all nine collision margins are positive in these groups. This is one repeated state/horizon contact-bound mechanism, not eight independent effects. Every one of the 140 groups with any certificate also certifies zero voltage. Thus R3 shows zero unique nonzero-voltage expansion of group certificate coverage.

Stored per-query elapsed time ranges from 0.109 to 0.313 seconds, with upper median 0.203 seconds. Each stored runtime exceeds the corresponding 0.02, 0.05, or 0.10 second hold duration. These are offline timing records on the recorded environment; they do not establish a real-time guarantee.

**Consequence.** R3 contains useful finite synthetic certificates on moving nonzero-width state boxes, but it does not show task value from choosing a nonzero voltage. Negative sufficient margins explain why the checker abstained; UNKNOWN is not a claim that the true trajectory violates safety or contact admissibility.

**Status.** Counts, reasons, exact margins and group pattern are reproduced from the archived records. The full per-state/scene/horizon/action vectors remain in the JSON and CSV artifacts.

**Required action.** Preserve every UNKNOWN and the complete 1,944 denominator. Interpret collision and contact margin failures as failures of the sufficient tests only.

## Finding 4 — parameter and contact-law provenance

**Finding.** R3's parameter domain is exact but wholly synthetic; the literature search did not find a source-backed family for MASTER v2.1's entire nine-state model and shared contact law.

**Evidence.** R3 stipulates m=I_z=R_w=b=c_u=c_r=v_s=V_max=1 with SI units assigned by the equations; phi(q)=clip(q,-1,1), L_phi=1; independent fixed left/right labels rho_j,C_j in [1,11/10] and lambda_j,R_j,B_j,k_j in [9/10,11/10]; J_j=1/rho_j and L_j=lambda_j. Its n=10 ideal gear witness is algebraic consistency only, not a motor/robot identification. No interval is a measured confidence range.

Primary-source checks:

- Tran & Vu, “A Study on General State Model of Differential Drive Wheeled Mobile Robots,” JAEC 7(3), 2023, DOI 10.55579/jaec.202373.417: publisher full PDF, printed Eqs. (1)–(7), pp. 175–176 and Table 1, p. 177; inspected PDF SHA-256 14e4133a6c780d616e703942b09eb5ecd8fd9b9110b6d1ab3c6ba3b1e189bc46. Table values include body/yaw entries, asymmetric wheel radii/inertias, gear ratios and efficiencies, winding resistance/inductance, damping, and motor torque constants. The paper assumes rolling without slipping; the unequal radii and nonideal efficiency and unresolved shaft reflection prevent direct assignment to the MASTER common-radius/effective wheel-shaft family. It has no compatible C_j/phi/v_s or lateral reserve/support model.
- Vu et al., “Development of Decentralized Speed Controllers for a Differential Drive Wheel Mobile Robot,” JAEC 7(2), 2023, DOI 10.55579/jaec.202372.399: publisher full PDF, model pp. 78–80 and Table 1, p. 84; inspected PDF SHA-256 c28518e424987cafbc745f696135aeb6cb291a6192ad2a1e0417a9ed309ed303. It reports PMDC point values including 36 V rating, R_a=0.928 Ω, L_a=8.5 mH, J_m=0.015 kg·m² and K_T=K_E=0.573 in the listed units, plus body mass and half wheelbase. Its no-slip, identical-motor/half-weight model, incomplete yaw/wheel geometry, and controller/H-bridge semantics do not establish MASTER's direct terminal-voltage input or contact family.
- Wang, Zhang & Wang, “Event-triggered MPC-PID based trajectory tracking control for differential drive mobile robots,” PLOS ONE 21(7), e0354699 (2026), DOI 10.1371/journal.pone.0354699: full article HTML returned HTTP 200 on 2026-10-03. Eqs. (1)–(4) use kinematic relations without lateral wheel-ground slip; Eqs. (5)–(11) use reference velocity, inner PID and saturation. It is a control-structure source, not MASTER parameter/contact provenance.
- ROBOTIS TurtleBot3 Features and XL430-W250-T e-Manual returned HTTP 200 on 2026-10-03. The feature page identifies two smart servos; the actuator manual gives a 258.5:1 gear ratio and 6.5–12 V operating range. The exact XL430-to-selected-platform build mapping was not verified, and a packet-level smart-servo command is not winding-terminal voltage.
- The cited Maxon constants page returned HTTP 403 and was not used as newly verified evidence.

MASTER uses each C_j both to scale longitudinal force F_j=C_j phi(sigma_j/v_s) and to bound the combined longitudinal/lateral reaction through F_j²+Y_j²≤C_j². The sources provide no fixed per-wheel capacity range, measured slip curve or v_s, lateral reaction selection/validated ideal constraint, support/load-transfer model, or uncertainty/correlation bounds. They also do not close the common wheel-radius, wheel-shaft convention, bidirectional transmission, or terminal-voltage semantics for one platform.

**Consequence.** Literature supplies fragments only. Values from separate devices must not be spliced into an identified robot. The practical parameter/contact domain is BLOCKED/PARTIAL; the R3 synthetic result cannot be transferred to hardware.

**Status.** Full field-by-field mapping, locators, units, hashes, source access and missing fields are documented in research/benchmarks/G2_PARAMETER_CONTACT_PROVENANCE_MATRIX_v1.md.

**Required action.** Keep the candidate decision study explicitly synthetic. For any physical claim, select one exact build and obtain a compatible support/contact/actuation identification plus fixed-label correlations and a validated model-error enclosure.

## Finding 5 — prospective task study candidate

**Finding.** A decision-relevant synthetic one-hold protocol is specified without producing results on its proposed universe.

**Evidence.** research/benchmarks/G2_DECISION_RELEVANT_STUDY_PROTOCOL_CANDIDATE_v1.md specifies:

- Task: move at least 0.05 m along world +x during one hold near one static circle, with nominal request V_nom=(1,1) V.
- Four closed rational moving nine-state boxes, four static-circle placements with inflated radius 0.06 m, two holds (0.25 and 0.5 s), and 25 voltage pairs from {-1,-0.5,0,0.5,1}² V.
- Exact full universe: 4×4×2×25=800 action queries, or 32 state/scene/horizon task groups. Development and held-out evaluation each have 16 groups and 400 rows, split by scene.
- One common V per query for every state in its full box and every fixed label; collision and contact must both pass over the complete [0,T] hold.
- A nominal-preserving selector among CERTIFIED actions that also prove the robust terminal-progress lower bound. Zero-only and nominal-only comparators are separately defined. UNKNOWN means no certificate was obtained, not unsafe.
- Acceptance rules include at least 8/16 held-out task successes and at least four more than zero-only; a separate criterion compares to nominal-only. Certificate coverage, nominal retention, unique nonzero-versus-zero certificate coverage, and task progress are distinct outcomes.
- Rational manifest/hash freeze procedure, complete denominator, per-query and phase caps, offline timing, failure reporting and a no-retuning evaluation split.

The task family reuses R3's synthetic parameter image unchanged; the candidate scene/state/task data are new and do not rewrite R3. The R3 archive was already inspected for the separate diagnosis before this candidate was written, so the candidate is not a blind preregistration. The proposed endpoint-progress metric is not established by archived records and needs a reviewed sound endpoint enclosure/checker. No evaluation manifest or evaluation output was created.

**Consequence.** The protocol provides a concrete reviewable design for testing task value, not evidence that voltage selection has already succeeded.

**Status.** GO for Codex review of the candidate; NO-GO for freezing/running it now. G2 remains UNVERIFIED, the physical domain is blocked, and endpoint progress proof/checker is missing.

**Required action.** Before any task query: review the R3 safety inclusion/checker path; implement and independently review the exact endpoint progress bound; approve the task thresholds and non-blind split caveat; create, validate and hash the 800-ID rational manifest and all source/dependency/profile inputs. Do not promote G2 based on completing this document.

## Finding 6 — artifact inventory and final disposition

**Finding.** The requested analysis, provenance matrix, task protocol and full handoff are present for Codex review.

**Evidence.**

| Artifact | SHA-256 |
|---|---|
| validation/analysis/g2_decision_domain_v1/analyze_r3_decision_domain_v1.py | 49a155fd7a03c852a8c29a54f05466790a9a0991c63d8a61246699a538c31c15 |
| results/validation/g2/decision_domain_v1/r3_unknown_cause_summary_v1.json | ce642b8ebd34e679940e4a4e75c3e5bc97714814db33798c06ea1c32977ade1a |
| results/validation/g2/decision_domain_v1/r3_record_margin_decomposition_v1.csv | ef402327839c4fbfa6ad3cf51abb5144083ac474eedc04100f3468d93f60b653 |
| research/benchmarks/G2_PARAMETER_CONTACT_PROVENANCE_MATRIX_v1.md | ca42cbe473cda5348dfcec35a204122518278f5aaf3d8cdffcfa517d58a73f27 |
| research/benchmarks/G2_DECISION_RELEVANT_STUDY_PROTOCOL_CANDIDATE_v1.md | 43cc2eac748747aed2e56401b2b0d70d47f4f367f4e42d19c50b29bed39976b9 |

**Consequence.** The artifacts preserve the evidence boundary between post-hoc archived R3 results, sourced literature fragments, synthetic protocol assumptions, and unverified claims.

**Status.** Handoff complete for review. G2 UNVERIFIED; practical domain BLOCKED/PARTIAL; overall HOLD.

**Required action.** Codex reviews this handoff and the two companion research documents. No commit or push was made.

## Vietnamese decision summary

Archive R3 có 1.196 CERTIFIED và 748 UNKNOWN trên đủ 1.944 truy vấn. Nguyên nhân là bound collision âm ở 405 dòng, bound contact âm ở 636 dòng, trong đó 293 dòng trùng; 8 nhóm hỗn hợp chỉ là một state/horizon lặp qua hình học. UNKNOWN chỉ nói rằng sufficient test không cấp chứng nhận.

Ma trận nguồn cho thấy bộ tham số và luật tiếp xúc R3 hoàn toàn tổng hợp; các bài báo và datasheet chỉ cho giá trị rời rạc, không tạo được một domain tương thích MASTER hoặc robot đã nhận dạng. Protocol candidate định nghĩa bài toán tiến 5 cm với nominal V=(1,1) V và so sánh bộ chọn với zero-only/nominal-only, nhưng chưa chạy. **GO để Codex review tài liệu; NO-GO để freeze/run; G2 vẫn UNVERIFIED, HOLD.**
