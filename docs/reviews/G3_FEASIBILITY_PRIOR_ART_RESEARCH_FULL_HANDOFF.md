# DDWMR — G3 feasibility and prior-art research full handoff

**Session:** `DDWMR | G3-FEASIBILITY-RESEARCH`  
**Research date:** 2026-10-08  
**Reviewed repository:** `NADUNGVN/ddwmr-actuator-safety`  
**Pinned reviewed commit:** `857f204efaf12a583353dedc2b29f99a958664e4`  
**Final disposition:** `REVISE_HYPOTHESIS`  
**Project gate after this report:** **unchanged — HOLD**

---

## 1. Tóm tắt điều hành

Hướng **sampled recursive safety** vẫn có giá trị khoa học để khảo sát, nhưng **không nên triển khai G3 theo phát biểu hiện tại như một đóng góp độc lập**. Lý do chính không phải vì bài toán bất khả thi, mà vì phần logic tổng quát `K_T \subseteq \operatorname{Pre}_T^c(K_T)`, fixed-point predecessor, zero-order-hold invariance và backup/recoverability set đã có prior art trực tiếp. Đặc biệt, Mitchell–Kaynama–Chen–Oishi (2013) đã xây dựng discriminating kernel cho sampled-data với input giữ hằng giữa các mẫu và chính sách an toàn; Singletary–Chen–Ames (2020) đã chứng minh bất biến robust dưới ZOH và kiểm tra an toàn trong toàn khoảng giữ; Chen–Jankovic–Santillo–Ames (2021) đã xây dựng control-invariant recoverable set từ một backup policy. Vì vậy, chỉ ghép một evaluator một-hold với phép lặp predecessor cho DDWMR sẽ là **plant-specific adaptation của machinery đã biết**, chưa phải contribution bảo vệ được.

Điểm đáng tiếp tục là một giả thuyết hẹp và có thể bị phản chứng: **cấu trúc electromechanical/contact của DDWMR ở mức điện áp có thể tạo ra một recoverability/predecessor construction chặt hơn một baseline sampled-data generic, đủ để thay đổi ít nhất một quyết định điện áp hoặc mở rộng một miền moving-state đã khai báo trước, trong khi vẫn giữ đúng lượng từ `exists one voltage for all hidden fixed parameters`.** Nếu không chứng minh được một separation lemma kiểu này trước khi đầu tư implementation, G3 hiện tại nên dừng.

Điều chưa biết quan trọng nhất là liệu có tồn tại một moving robust seed/set có positive extent dưới independent left/right uncertainty mà không dựa vào một braking mode chưa được chứng minh. MASTER đã chỉ rõ `V=0` không phải mechanical brake, wheel-zero không phải lock mode, và positive capacity không đảm bảo stopping authority. Đây là blocker thực chất cho mọi backup/funnel argument đơn giản.

**Mốc chứng minh cụ thể tiếp theo:** trước bất kỳ G3 implementation nào, phải đưa ra một analytic feasibility note cho một compact moving cell/seed `B` với positive-width uncertainty, chứng minh hoặc phản chứng rằng có một state-only, non-oracle voltage rule sao cho với mọi `x in B` tồn tại **một** `V(x)` hợp lệ cho mọi `vartheta in Theta`, toàn bộ hold giữ collision/contact admissible và endpoint quay lại `B` hoặc một declared `K`. Sau đó phải chỉ ra một witness đã predeclare nơi construction plant-structured chứng nhận được action/state mà một baseline generic matched-assumption không chứng nhận được. Nếu bước đầu tiên thất bại hoặc chỉ còn rest/symmetric singleton cases, không có cơ sở để tiếp tục G3 hiện tại.

---

## 2. Snapshot và tài liệu đã đọc

### 2.1 Pinned snapshot

Tất cả nhận định về repository trong báo cáo này áp dụng cho commit:

`857f204efaf12a583353dedc2b29f99a958664e4`

Không dùng moving `main` làm snapshot thay thế.

### 2.2 Repository files read

Đã đọc các file bắt buộc sau tại pinned commit trước khi đưa ra disposition:

1. `AGENTS.md`
2. `research_context/MASTER_RESEARCH_CONTEXT_v2.md` — authoritative v2.1
3. `research_context/DECISION_LOG.md`
4. `research_context/LITERATURE_MATRIX.md`
5. `research_context/REVIEW_GATE.md`
6. `docs/reviews/autonomous_w2/CODEX_W2_FINAL_DISPOSITION_2026_10_08.md`
7. `docs/reviews/autonomous_w2/g2/LUNA_TO_CODEX_G2_W2_V6_FINAL_FROZEN_RESULT_AUDIT_FULL_HANDOFF_v1.md`
8. `docs/reviews/autonomous_w2/g4/LUNA_TO_CODEX_G4_W2_V6_FINAL_RESOURCE_ATTRIBUTION_FULL_HANDOFF_v1.md`
9. `docs/reviews/CODEX_DDWMR_SCOPE_PROGRESS_VERIFICATION_2026_10_07.md`
10. `docs/RESEARCH_PUBLICATION_2026_10_08.md`
11. `docs/RESEARCH_PUBLICATION_2026_10_08.json`
12. `docs/G3_FEASIBILITY_RESEARCH_ASSIGNMENT.md`

MASTER và bốn file `research_context/` được giữ là authoritative khi lịch sử cũ khác nhau.

---

## 3. Research question và formal assumptions

### 3.1 Plant and information model

State của adopted reduced DDWMR là

\[
x=[p_x,p_y,\theta,u,r,\omega_L,\omega_R,i_L,i_R]^\top,
\qquad V=[V_L,V_R]^\top.
\]

Điện áp terminal là physical input và được giữ hằng trong một hold cố định `T`:

\[
V(t)=V_k,\qquad t\in[kT,(k+1)T).
\]

Hidden parameter vector `vartheta in Theta` là fixed cho toàn execution, không reset giữa các hold. Controller quan sát chính xác chín state tại sampling instants nhưng không biết true `vartheta`; không được oracle-select voltage sau khi biết realization.

Longitudinal/contact core gồm

\[
F_j=C_j\phi(\sigma_j/v_s),
\]

và algebraic contact admissibility

\[
Y_L+Y_R=mur,\qquad F_j^2+Y_j^2\le C_j^2.
\]

Mỗi certified hold phải giữ collision safety và parameter-specific contact domain **liên tục** trên `[0,T]`.

### 3.2 Robust safe set and predecessor

Với `S_rob` là state-only robust intersection của geometric safety và mọi contact domain, MASTER định nghĩa

\[
\operatorname{Pre}_T^c(A)=\left\{x\in S_{rob}:\exists V\in\mathcal U\;\forall\vartheta\in\Theta:
\begin{array}{l}
x_\vartheta(t;x,V)\in\mathcal S\cap D_c(\vartheta),\quad\forall t\in[0,T],\\
x_\vartheta(T;x,V)\in A
\end{array}
\right\}.
\]

G3 target là một **useful moving** set

\[
K_T\subseteq S_{rob},\qquad K_T\subseteq\operatorname{Pre}_T^c(K_T),
\]

cùng action-selection map sử dụng chỉ thông tin quan sát được.

Quantifier phải là

\[
\forall x\in K_T\;\exists V(x)\in\mathcal U\;\forall\vartheta\in\Theta\;\forall t\in[0,T],
\]

không phải `forall vartheta exists V`.

### 3.3 Scope boundaries that materially affect G3

- `V=0` là zero-terminal-voltage RL boundary condition, không phải coast/open circuit hay mechanical brake.
- `omega_j=0` không cung cấp persistent wheel-lock mode.
- Positive `C_j` và sign-preserving `phi` không tự động cho stopping-distance theorem.
- Independent left/right capacity uncertainty nói chung phá straight-line symmetry.
- A moving useful set phải có positive extent ngoài rest states.
- Fixed-parameter history may contain information, nhưng MASTER G3 hiện tại là state-only robust target. Một information-state/history-dependent policy là scope proposal mới, không được nhập lén.

---

## 4. Fixed background from W2

W2 được coi là fixed background, không được diễn giải lại để tạo contribution mới.

- Final classification: `NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE`.
- Ba corrected v6 development rows replay thành công; `(0,0)` và `(1/2,1/2)` safety-certified nhưng task-ineligible; `(1,1)` đạt threshold progress `7/20 m` trong hai giây.
- Ba local Auer rows đều `RESOURCE_LIMIT` trước accepted step do pre-operation exact-rational width estimate vượt configured 32,768-bit cap.
- Kết quả Auer chỉ là local implementation/profile availability observation, không phải mathematical failure.
- Ba rows là reused development data, không phải held-out confirmation.
- Historical R3 1,944-row record: 1,196 `CERTIFIED`, 748 proof-complete `UNKNOWN`.
- Historical selected ten-pair Auer pilot: Auer 9 certified, R3 6; không có universal ordering.

Kết luận đối với G3: W2 cho thấy một one-hold proof pipeline có thể tạo finite certificates trong scope hẹp, nhưng **không cung cấp recursive seed, backup policy, novelty separation hoặc useful cross-method advantage**.

---

## 5. Prior-art audit

### 5.1 Screening method

Ưu tiên primary full text hoặc publisher/author full text. Với nguồn chỉ có abstract/landing page, báo cáo đánh dấu rõ access limitation và không suy diễn theorem không đọc được. Search cutoff là ngày research 2026-10-08.

### 5.2 Source-by-source table

| Source | Access / exact locator inspected | Plant / input / uncertainty | Safety / recursion coverage | Relevance to DDWMR G3; what is **not** established |
|---|---|---|---|---|
| I. M. Mitchell, S. Kaynama, M. Chen, M. M. K. Oishi, **“Safety Preserving Control Synthesis for Sampled Data Systems,”** *Nonlinear Analysis: Hybrid Systems* 10 (2013), 63–82. DOI: `10.1016/j.nahs.2013.04.003`. Author preprint: `https://people.ece.ubc.ca/kaynama/papers/NAHS12.pdf` | Full author preprint inspected. Abstract pp. 1–2; §4.2, Eq. (9)–(12), Lemma 1 and Proposition 2 around preprint pp. 10–11; policy discussion around §4.5 / pp. 18–20. | General continuous-state sampled-data systems. Controller gets periodic state feedback and selects a constant control between updates. Robust/discriminating-kernel formulation includes disturbance/adversarial dimensions. | Directly constructs a conservative approximation to the sampled-data discriminating kernel (maximal robust control invariant set) and a set-valued feedback policy preserving safety, accounting for inter-sample continuous evolution. Recursive one-sample operator is iterated. | This is the strongest generic overlap. A DDWMR fixed-point `Pre` iteration is not novel by itself. Source does **not** contain this nine-state voltage/contact model, the particular fixed hidden capacity semantics, or this contact algebra; therefore it does not rule out a plant-specific contribution. |
| A. Singletary, Y. Chen, A. D. Ames, **“Control Barrier Functions for Sampled-Data Systems with Input Delays,”** CDC 2020. DOI: `10.1109/CDC42340.2020.9304281`; arXiv `2005.06418`. | Full arXiv HTML inspected: Eq. (1), Def. 1, Eq. (3); ZOH backup Eq. (5), ZOH invariant set Eq. (6); full-step safety Eq. (8), reachable-set strengthening Eq. (9); Proposition 1 in §II-C. | General control-affine system, bounded input, ZOH; also state uncertainty and known input delay. | Eq. (8) explicitly requires safety for every `tau` in a sampling interval. Proposition 1 proves all-time invariance under a sequence of ZOH inputs satisfying the sampled-data robust CBF condition. | Direct threat to any claim that ZOH + inter-sample safety + recursion is new. Does not model fixed hidden DDWMR contact parameters or motor-voltage/wheel/current coupling. |
| Y. Chen, M. Jankovic, M. Santillo, A. D. Ames, **“Backup Control Barrier Functions: Formulation and Comparative Study,”** CDC 2021, 6835–6841. DOI: `10.1109/CDC45484.2021.9683111`; arXiv `2104.11332`. | Full arXiv HTML inspected: Definition 1; Eq. (9) at §III-A; Theorem 1; Lemma 1; Eq. (10). | General control-affine systems with bounded input and a fixed backup policy. | Eq. (9) defines states whose backup trajectory remains in the safe set over `[0,T]` and reaches a backup invariant set; Theorem 1 shows this constrained reachable set is control invariant. | A “backup recoverability funnel” is established generic machinery. DDWMR novelty could only lie in a nontrivial voltage/contact backup construction or certified advantage, not the backup-set logic itself. |
| Y. Li, J. Liu, **“Robustly complete synthesis of sampled-data control for continuous-time nonlinear systems with reach-and-stay objectives,”** *Nonlinear Analysis: Hybrid Systems* 44 (2022), 101170. DOI: `10.1016/j.nahs.2022.101170`. | Publisher abstract/highlights inspected; full theorem text not obtained in this pass. Locator supported by publisher: fixed-point synthesis description in abstract; validated high-order Taylor reachable-set approximation over one sampling period. | Continuous-time nonlinear systems; sample-and-hold strategy; perturbed dynamics for robust completeness. | Synthesizes reach-and-stay controller by fixed-point iteration over cells, using validated one-period reachable over-approximations. | Strong overlap with “validated one-hold reachability + fixed point”. Exact theorem assumptions were **not fully audited**, so no stronger exclusion claim is made. |
| X. Tan, E. Daş, A. D. Ames, J. W. Burdick, **“Zero-Order Control Barrier Functions for Sampled-Data Systems with State and Input Dependent Safety Constraints,”** ACC 2025. DOI: `10.23919/ACC63710.2025.11107720`; arXiv `2411.17079`. | Author arXiv v2 identified; repository literature audit previously inspected Definition 1/Eq. (4), Lemma 1/Eq. (5), Theorem 1 and method discussion. | General sampled-data systems; state- and input-dependent safety constraints; collision and uneven-terrain rollover examples. | Zero-order sampled-data safety conditions avoid derivative/relative-degree dependence and address inter-sample safety. | Makes “sampled-data barrier without derivatives/high relative degree” unavailable as novelty. Does not establish DDWMR’s exact fixed-parameter contact predecessor. |
| R. Liu, K. Hashimoto, **“Friction-Aware Force-Realizable Safety Control for Four-Wheel Independently Steered and Driven Mobile Robots,”** *International Journal of Robust and Nonlinear Control*, Early View, first published 2026-10-03. DOI: `10.1002/rnc.70772`. | Open-access publisher HTML inspected: abstract, introduction summary and conclusion. Full equation-level comparison was not completed in this pass. | 4ISD mobile robot; wheel-torque realization; tire-road friction limits; observer provides conservative friction lower bound; sampled-data barrier governor. | Couples friction-limited recoverability, sampled-data safety regulation and force-realizable dynamic control; reports sampled-data practical safety. | Very recent, close application threat: actuator/force-realizable robot safety under friction limits is already active. Different plant (4ISD, not DDWMR), different uncertainty semantics (observer/adaptation versus execution-fixed hidden set), and practical rather than MASTER’s exact robust predecessor target. No claim of exact overlap is made. |
| S. Liu, K. S. Yun, J. M. Dolan, C. Liu, **“Synthesis and Verification of Robust-Adaptive Safe Controllers,”** ECC 2024, pp. 2265–2272. Stable primary PDF: `https://www.paperhost.org/proceedings/controls/ECC24/files/0267.pdf`; arXiv `2311.00822`. | Full conference PDF inspected, especially abstract and Introduction p. 2258. | General polynomial systems with constant unknown parameters; robust-adaptive CBF, parameter estimation; examples up to 7D. | Synthesizes and verifies safety controllers for constant unknown parameters and explicitly seeks lower conservatism than a robust baseline. | A history/parameter-learning G3 extension is not empty prior-art space. Such an extension would also change MASTER’s state-only target. It remains possible that DDWMR-specific fixed-parameter inference has unique structure, but that must be independently justified. |
| M. Arcak, A. Maidens, **“Simulation-based reachability analysis for nonlinear systems using componentwise contraction properties,”** 2017 manuscript, arXiv `1709.06661`. | Primary author manuscript previously inspected in repository audit: §2 Proposition 1/Corollary 1; §3 Algorithm 1. | General nonlinear dynamics; componentwise bounds; parameter augmentation is compatible with constant labels. | Generic reachable-set enclosure machinery. | Blocks novelty from generic componentwise exponential bounds / constant-parameter augmentation alone. Does not settle a recursive DDWMR construction. |
| P. Meyer, M. Devonport, M. Arcak, **“TIRA: Toolbox for Interval Reachability Analysis,”** 2019 manuscript, arXiv `1902.05204`. | Primary manuscript previously inspected in repository audit: §3.1 Assumption 3, Eq. (4), Proposition 4 and remarks. | General nonlinear reachability with interval/growth-bound methods. | Established interval reachability machinery. | Reinforces that a G3 contribution cannot be “run generic interval predecessor on the plant”; plant-specific structure must change decision quality or tractability. |

### 5.3 Prior-art synthesis

The following elements are **already established generic machinery**:

1. sampled-data robust invariant/discriminating kernels with constant inputs between samples;
2. repeated one-step predecessor/fixed-point logic;
3. inter-sample safety requirements under ZOH;
4. backup-policy recoverability sets and invariant enlargement;
5. validated one-period reachability inside fixed-point synthesis;
6. adaptive/robust safety control for constant unknown parameters;
7. sampled-data robot safety with friction/force-realizability considerations.

Therefore a contribution statement of the form

> “Compute a certified one-hold reachable set, iterate a predecessor until a recursive safe set is obtained, and choose a safe held voltage”

is not defensible as novelty without an additional plant-specific theorem/computation.

---

## 6. Candidate construction screen

Only three candidates are screened, as required.

### Candidate A — State-only robust predecessor fixed point using certified joint tubes

**Construction.** Choose an initial robust domain `K_0 subset S_rob` and iterate

\[
K_{n+1}=K_n\cap\operatorname{Pre}_T^c(K_n),
\]

where each predecessor query uses a certified joint state/parameter tube for a common held voltage.

**1. Domain and safe set.** Nine-state `x`, execution-fixed `vartheta in Theta`, `S_rob` as in MASTER. Useful domain must include moving states and positive extent.

**2. Policy information.** `V=\pi(x)` depends only on sampled `x` and known `Theta`; true `vartheta` is unavailable.

**3. One-hold computation.** Any sound one-hold enclosure satisfying G2 semantics may act as a sufficient membership oracle for `Pre_T^c`.

**4. Continuous proof obligation.** For all hidden labels and every `t in [0,T]`, collision and contact domain constraints hold.

**5. Endpoint return.** Endpoint is in `K_n` for every hidden realization.

**6. Quantifier order.** `forall x exists V forall vartheta forall t`.

**7. Plant specificity.** In this raw form, insufficient. Replacing a generic flow/reachability oracle with the DDWMR evaluator does not change the mathematics of the predecessor fixed point.

**8. Smallest decisive proof/counterexample.** Show a declared moving cell `B` where a DDWMR-specific predecessor bound certifies a common action but a matched generic validated-reachability predecessor does not, **because of a specific preserved voltage/contact correlation**, not merely arithmetic tuning. Failure to produce such a witness reduces Candidate A to known generic machinery.

**Assessment:** mathematically plausible, but **not a defendable contribution as currently stated**.

---

### Candidate B — Voltage/contact backup recoverability funnel

**Construction.** Define a state-only backup voltage policy `pi_B(x)` and a small moving robust seed `B`. Construct states whose ZOH backup rollout stays collision/contact safe and reaches `B` in finite sampled steps; inside `B`, repeated holds keep the state in `B` or its certified recursive extension.

**1. Domain and safe set.** Same nine-state and `Theta`, with `B` required to contain moving states, positive width and independent-side uncertainty.

**2. Policy information.** `pi_B` may use sampled state but not hidden parameter realization.

**3. One-hold computation.** Certified tube under the common backup voltage at each sample.

**4. Continuous proof obligation.** Collision and algebraic contact constraints on every backup hold.

**5. Endpoint return.** Either endpoint returns to `B`, or decreases a rigorously defined finite-step recoverability rank and eventually reaches `B`.

**6. Quantifier order.** At each observed state, one voltage must work for all `vartheta` still in the declared robust set.

**7. Plant specificity.** Potentially meaningful if the backup law and invariant/recoverable geometry are derived from motor-current/wheel/body/contact coupling rather than generic braking intuition.

**8. Smallest decisive proof/counterexample.** Prove one nontrivial moving seed `B` and one non-oracle backup action law under positive-width **independent** side uncertainty. In particular, prove actuator-feasible evolution of slip/current and contact margin through the near-zero-speed region. A counterexample showing that every candidate common backup voltage exits collision/contact or cannot return on some allowed `vartheta` falsifies the candidate.

**Critical blocker.** Current MASTER explicitly denies the assumptions normally used to make this easy: `V=0` is not a brake, wheel zero is not a persistent lock, positive capacity does not imply stopping authority, and matched-side straight-line reduction does not survive general independent side uncertainty.

**Assessment:** scientifically the most promising current G3 form, but it is **unready** until the backup/seed theorem exists. Generic backup-set logic itself is prior art.

---

### Candidate C — History-dependent compatible-parameter information set

**Construction.** Carry a compatible parameter set `Theta_k` obtained from the complete observed sampled history and known applied voltages. Policies depend on `(x_k,Theta_k)` and exploit the fact that parameters are fixed across holds.

**1. Domain and safe set.** Augmented information state `(x,Theta_k)`; physical state remains nine-dimensional.

**2. Policy information.** No oracle: policy uses only measured history and set-membership inference.

**3. One-hold computation.** Tube over the current compatible fixed-label set, not the original `Theta` if data soundly narrows it.

**4. Continuous proof obligation.** Same collision/contact guarantee for every parameter compatible with history.

**5. Endpoint return.** Return to an invariant information-state set or satisfy a recursive information-state predecessor.

**6. Quantifier order.** `forall compatible history exists V forall vartheta in Theta_k`.

**7. Plant specificity.** Could exploit electromechanical excitation and fixed parameter correlations, but this changes the object from MASTER’s state-only `K_T` and enters robust-adaptive/set-membership safe-control literature.

**8. Smallest decisive proof/counterexample.** Exhibit two histories with the same sampled physical state but different sound compatible parameter sets that admit different safe voltage sets, and prove that using the narrower set strictly enlarges certified safe action availability without violating true-parameter containment.

**Assessment:** plausible **scope-revision alternative**, not current G3. Significant prior art exists for constant-unknown-parameter adaptive safe control, so novelty remains open.

---

## 7. Feasibility blockers and counterexamples

### 7.1 No generic contribution from predecessor induction

**Finding**

A state-only repeated predecessor or discriminating-kernel construction is not a new scientific contribution by itself.

**Evidence**

Mitchell et al. (2013) already formulate sampled-data discriminating kernels under held inputs, iterate a one-sample operator, and synthesize set-valued safe feedback. Li–Liu (2022) likewise describe fixed-point sample-and-hold synthesis using validated one-period reachable sets. MASTER itself states generic enclosure/predecessor implications are not novelty.

**Consequence**

Implementing Candidate A without a plant-specific separation theorem risks spending substantial effort only to rediscover known machinery on a harder plant.

**Status**

`BLOCKER` to the **current generic G3 contribution claim**, not a blocker to mathematical feasibility.

**Required action**

Predeclare and prove a plant-specific difference in certified decision/coverage/tractability before implementation authorization.

---

### 7.2 Backup construction lacks a proved actuator/contact-safe brake or seed

**Finding**

The obvious backup-funnel route is not currently grounded by a valid backup policy for the general MASTER uncertainty set.

**Evidence**

MASTER A7 and §26 state that positive capacity does not guarantee stopping, wheel-zero is not a sustained lock, `V=0` is not a mechanical brake, and independent left/right capacity uncertainty breaks the symmetric straight-line reduction. No useful `K_T` or compatible braking policy is established.

**Consequence**

A backup/recoverability construction cannot assume monotone speed decrease or finite stopping distance. Without a moving seed and common voltage policy, it may collapse to rest cases or an invalid symmetric special case.

**Status**

`UNVERIFIED / BLOCKER` for Candidate B until the seed-policy lemma is proved.

**Required action**

Derive a compact moving seed with a common voltage action under positive-width independent uncertainty, including near-zero-speed and contact-admissibility analysis; or provide a counterexample and stop this branch.

---

### 7.3 Fixed hidden parameters create an information opportunity, but state-only G3 discards it

**Finding**

The physical execution keeps `vartheta` fixed, but the state-only robust predecessor rechecks the full `Theta` at each endpoint. This can be conservative relative to a sound history-dependent policy.

**Evidence**

MASTER explicitly distinguishes state-only robust recursion from history-dependent exact fixed-parameter viability. Robust-adaptive safe-control literature already treats constant unknown parameters and parameter estimates.

**Consequence**

If state-only G3 proves too conservative, the scientifically natural next idea is an information-state construction, but that is a **scope revision** and not automatically novel.

**Status**

`PLAUSIBLE SCOPE PROPOSAL`, not an accepted current contribution.

**Required action**

Only pursue after owner-approved scope change and a new prior-art audit; first establish a same-physical-state/different-information witness demonstrating decision relevance.

---

### 7.4 High dimension and contact boundary make a full kernel computationally risky

**Finding**

A nine-state robust kernel with positive-width labels is computationally demanding, and generic HJ/discriminating-kernel methods do not scale favorably.

**Evidence**

Mitchell et al. explicitly distinguish a nonlinear HJ implementation with poor dimension scaling and a linear ellipsoidal formulation. The DDWMR additionally has actuator/contact coupling and a contact margin whose square-root representation loses regularity at saturation. W2 also showed that proof availability is sensitive to arithmetic/profile choices, although that does not imply mathematical impossibility.

**Consequence**

A brute-force grid/kernel campaign is not justified. Scientific value must come from structure that reduces the problem or proves a targeted set, not merely a larger compute budget.

**Status**

`FEASIBILITY RISK`.

**Required action**

Use analytic seed/funnel or structured local cells first; do not launch a full nine-dimensional kernel computation before the separation lemma is established.

---

### 7.5 Very recent force-realizable friction-aware robot safety narrows application novelty

**Finding**

Actuator-/force-realizable sampled-data safety for friction-limited mobile robots is already an active published area as of October 2026.

**Evidence**

Liu–Hashimoto (2026) couples a sampled-data barrier governor with friction-limited recoverability and wheel-torque realization on a 4ISD platform.

**Consequence**

A broad claim such as “first mobile-robot sampled safety that accounts for friction and actuator force” would be unsafe. Any DDWMR contribution must be stated at equation/theorem level around the exact voltage/contact/fixed-uncertainty structure.

**Status**

`NOVELTY THREAT`, not proof of full overlap.

**Required action**

If the revised hypothesis survives, perform a line-by-line comparison to this and other force-realizable ground-robot safety papers before any first/novelty claim.

---

## 8. Contribution test

### Already established generic machinery

- Sampled-data robust invariant/discriminating kernels.
- ZOH all-time/inter-sample safety conditions.
- Fixed-point predecessor/reach-and-stay synthesis.
- Backup recoverability/control-invariant set enlargement.
- Generic validated reachability and parameter augmentation.
- Robust-adaptive safe control for constant unknown parameters.

### Plant-specific adaptation with no demonstrated advantage

- Plugging the nine-state DDWMR ODE into a generic predecessor iteration.
- Using the existing one-hold tube evaluator as the predecessor oracle.
- Defining a backup set by forward rollout without proving a DDWMR-specific backup policy.
- Replacing friction notation with `C_j` or preserving fixed parameter labels without a decision-relevant theorem.

### Plausible new construction

A **voltage/contact recoverability construction** whose proof explicitly uses electromechanical/contact correlations to certify a useful moving state set under one common voltage for all fixed hidden labels, and which produces a predeclared decision or coverage improvement over a matched generic sampled-data baseline.

The contribution cannot be the induction. It must be the specific theorem/computation that makes the DDWMR safe-action set meaningfully less conservative or tractable.

### Unsupported assertions to avoid

- “A braking backup always exists because `C_j>0`.”
- “Zero terminal voltage stops the robot safely.”
- “Independent side uncertainty can be replaced by matched-side symmetry.”
- “A finite one-hold certificate proves recursive safety.”
- “A generic predecessor on this plant is novel because the plant is detailed.”
- “W2 established v6 superiority over validated integration.”

### Obstructions / counterexample directions

1. Two allowed parameter realizations may require incompatible voltages at the same observed state; if so, that state cannot belong to state-only `K_T` even though each realization separately is viable.
2. Independent `C_L,C_R` can induce yaw during braking and defeat a straight-line collision argument.
3. Contact admissibility can fail before geometric braking succeeds; a collision-only stopping argument is insufficient.
4. Near zero speed, no undeclared wheel-lock mode may be invoked; the backup proof must remain inside the actual ODE and electrical dynamics.

---

## 9. Best revised hypothesis

The strongest defensible next hypothesis is:

> **H-G3-R:** For a predeclared compact moving-state domain with positive-width independent hidden parameter uncertainty, there exists a state-only non-oracle voltage/contact recoverability construction for the adopted nine-state DDWMR that (i) certifies continuous collision and contact admissibility over every hold, (ii) returns endpoints to a useful moving robust set, and (iii) because it preserves a specific electromechanical/contact correlation, certifies at least one predeclared state/action decision that a matched generic sampled-data predecessor/backup baseline under the same assumptions does not certify.

This is intentionally stronger than “there exists a recursive set.” It contains the **scientific discriminator** needed to justify further work.

### Decisive pre-implementation proof milestone

Before implementation, produce a short analytic artifact containing all of the following:

1. **Seed domain:** a compact `B` with positive extent, `|u|` bounded away from zero on at least a subset, positive-width independent `C_L,C_R` (or the full intended joint uncertainty), and declared obstacle geometry.
2. **Non-oracle action rule:** an explicit `V_B(x)` or finite action-selection relation using only sampled state and known `Theta`.
3. **Full-hold theorem:** for every `x in B`, one chosen voltage works for every hidden label; collision and contact conditions hold for all `t in [0,T]`.
4. **Return theorem:** all endpoints lie in `B` (one-step invariant seed) or in a rigorously ranked finite-step recoverability chain ending in `B`.
5. **Plant-specific mechanism:** identify the exact correlation/inequality from motor-current/wheel/body/contact coupling that makes the bound stronger than a generic baseline.
6. **Matched witness:** one predeclared witness cell/action where the plant-structured test is `CERTIFIED` and the generic matched baseline is `UNKNOWN`/excluded for a demonstrably structural reason, not a different resource cap or arithmetic precision.

If items 1–4 cannot be proved without symmetric parameters, zero-width uncertainty or rest states, `H-G3-R` is falsified for the intended scope. If 1–4 succeed but item 6 cannot be established after a fair baseline comparison, G3 may be a useful engineering adaptation but not the paper contribution currently sought.

---

## 10. Why the disposition is not `ADVANCE_G3`

`ADVANCE_G3` would authorize moving from feasibility research toward a concrete G3 construction. That is premature because the central scientific risk is not implementation: it is whether the construction can be distinguished from established sampled-data invariant/recoverability machinery and whether the DDWMR has a valid moving backup/seed under general uncertainty.

The repository already contains enough evidence to reject “generic predecessor induction” as the contribution, but not enough to reject every possible plant-specific G3. Therefore `STOP_G3` would be too strong. The correct intermediate decision is to **revise the hypothesis before construction**.

---

## 11. Alternative if state-only H-G3-R fails

At most one alternative is recommended:

**Information-state fixed-parameter safety hypothesis.** Exploit the fact that hidden parameters are fixed over the full execution by maintaining a sound compatible set `Theta_k` from observed sampled history and constructing a recursive safe set in `(x,Theta_k)`.

This alternative is only defensible if a same-physical-state witness proves that history soundly narrows safe-action uncertainty and changes a safety/action decision. It requires an explicit MASTER scope revision and fresh G4 comparison against robust-adaptive CBF, set-membership safe control and robust/adaptive MPC literature. It must not be presented as a minor implementation variant of current G3.

If neither `H-G3-R` nor this explicitly revised information-state hypothesis yields a predeclared decision-relevant separation from prior art, recommend stopping the present paper direction rather than launching another metadata or batch cycle.

---

## 12. Established facts, derived results, conjectures, unknowns

| Class | Statement |
|---|---|
| **Established in repository** | Adopted nine-state reduced model, fixed hidden parameters, exact sampled state, voltage ZOH, continuous collision/contact obligation, robust quantifier order, G1 restricted PASS, G2/G3/G4 UNVERIFIED, overall HOLD. |
| **Established in repository** | W2 is a finite synthetic development record with `NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE`; no recursive set was established. |
| **Established by prior art** | Generic sampled-data discriminating/invariant-set synthesis, ZOH robust invariance, backup recoverability sets, and fixed-point reach-and-stay methods exist. |
| **Derived in this assessment** | A generic `K <- K intersect Pre(K)` implementation with the DDWMR one-hold evaluator cannot by itself carry a defensible novelty claim. |
| **Derived in this assessment** | A valid backup/funnel G3 must first prove an actuator/contact-safe common backup action under general uncertainty; the current record does not supply one. |
| **Conjecture / revised hypothesis** | A DDWMR-specific voltage/contact correlation may allow a useful moving recoverability set and a matched-baseline certification separation. |
| **Unknown** | Whether such a moving seed exists for the full intended independent-side uncertainty domain. |
| **Unknown** | Whether the plant-specific construction would be computationally tractable beyond a local structured domain. |
| **Unknown** | Whether the construction would remain novel after full equation-level audit of all 2025–2026 force-realizable/sample-data safety literature. |
| **Unknown** | Physical correspondence of the reduced `C_j` model to a real robot. |

---

## 13. Claims that must not be made

This assessment does **not** support any of the following:

- G3 solved or recursively safe DDWMR established;
- physical robot safety;
- a valid universal braking or wheel-lock backup;
- `V=0` as a mechanical brake;
- generic superiority of the v6/G2 method over Auer or validated integration;
- held-out confirmation from W2;
- exact viability-kernel equality;
- first sampled-data safe-set, first backup-set, first friction-aware robot safety, or first fixed-unknown-parameter safe controller claim;
- novelty from predecessor induction, parameter augmentation, fixed labels, capacity renaming, or interval reachability alone;
- ability to replace independent side uncertainty with a symmetric special case;
- safety for changing terrain/time-varying friction outside MASTER;
- paper readiness.

---

## 14. Final decisive finding

**Finding**

There is a scientifically plausible G3 direction, but the current hypothesis is too generic to justify implementation: the recursive predecessor/backup logic is established prior art, while the DDWMR-specific moving backup/seed and decision-relevant advantage are unproved.

**Evidence**

The prior-art sources above directly cover sampled-data robust invariant kernels, ZOH invariance, inter-sample conditions, backup recoverability and fixed-point synthesis. The authoritative repository simultaneously records no useful `K_T`, no general braking policy, independent-side uncertainty and `NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE` for W2.

**Consequence**

Proceeding straight to a G3 implementation would risk producing a technically valid but scientifically generic adaptation. A smaller analytic falsification step can decide whether the plant has enough structure to justify the cost.

**Status**

`REVISE_HYPOTHESIS`

**Required action**

Adopt `H-G3-R` only as a research hypothesis and prove/falsify the six-item pre-implementation milestone in §9. Do not implement a controller, simulator, kernel campaign or new numerical certificate batch during this feasibility stage. If no moving robust seed/common backup and matched-baseline structural separation can be proved, stop current G3 rather than widening computation.

---

## 15. Final disposition and unchanged gates

**Final disposition: `REVISE_HYPOTHESIS`.**

Factual basis: the generic G3 recursion is already represented in sampled-data discriminating-kernel, fixed-point reach-and-stay and backup-invariant-set literature, while no DDWMR-specific moving backup/seed or matched-baseline decision advantage has yet been proved.

Gate/status record remains unchanged:

- **Overall:** `HOLD`
- **G1:** `PASS_RESTRICTED_REDUCED_MODEL_SCOPE`
- **G2:** `UNVERIFIED`
- **G3:** `UNVERIFIED`
- **G4:** `UNVERIFIED`
- **Physical-platform correspondence:** `UNVERIFIED`

This report is feasibility/prior-art input only. It does not authorize G3 implementation or alter any authoritative research-context file.
