# Literature matrix — v2 research register

**Cutoff: 2026-09-28. G4 OPEN.** Read MASTER and DECISION_LOG first. This consolidates existing handoff leads and sources inspected during the initial audit. It is a **24-entry preliminary register**, not 24 fully verified papers or a completed systematic review. New contact/traction scope requires additional searching; no novelty absence claim is justified.

The tables join on ID and together record MASTER §30 fields. `U` means unknown/not established from inspected evidence, never No. `H` = handoff lead, not independently checked here; `L` = secondary/GPT metadata lead; `A` = abstract inspected; `P` = primary full-text sections or publisher preview inspected, with locator/scope recorded below. P does not mean every theorem has been audited. `Y-A/Y-P` states only what that evidence supports. `N-model/N-assumption/N-study` is a limited scoped exclusion, not proof the paper discusses nothing related.

## Bibliographic register and contribution comparison

Citation details not supplied by reliable inspected material (all author names/pages etc.) remain pending rather than invented. DOI resolver links identify candidates; they do not establish that the cited content has been accessed.

| ID | Citation | DOI / primary candidate | Evidence | Plant | Input level | Exact contribution / inspected scope | Overlap risk / action |
|---|---|---|---|---|---|---|---|
| 01 | Ames et al. (2017), Control Barrier Function Based Quadratic Programs for Safety Critical Systems. IEEE TAC. | [10.1109/TAC.2016.2638961](https://doi.org/10.1109/TAC.2016.2638961) | H | General control-affine systems | U | Foundational CBF-QP; source claims await direct audit in this register. | Generic safety-filter logic cannot be claimed as new. |
| 02 | Xiao and Belta (2022), High-Order Control Barrier Functions. IEEE TAC. | [10.1109/TAC.2021.3105491](https://doi.org/10.1109/TAC.2021.3105491) | H | General nonlinear systems | U | HOCBF foundation; original equations/theorems pending. | Higher derivative order alone is not novelty. |
| 03 | Xiao, Belta and Cassandras (2022), Sufficient conditions for feasibility of optimal control problems using Control Barrier Functions. Automatica. | [10.1016/j.automatica.2021.109960](https://doi.org/10.1016/j.automatica.2021.109960) | H | General constrained systems | U | Feasibility threat identified by handoff; full-text audit pending. | Compare actual bounded-input feasibility construction. |
| 04 | Taylor, Dorobantu, Cosner, Yue and Ames (2022), Safety of Sampled-Data Systems with Control Barrier Functions via Approximate Discrete Time Models. IEEE CDC. | [10.1109/CDC51059.2022.9993226](https://doi.org/10.1109/CDC51059.2022.9993226) | H | Sampled-data nonlinear systems | U | Approximate-discrete-model approach identified by handoff. | Compare approximation errors and continuous safety object. |
| 05 | Lin, Fu, Tang and Wen (2025), High-Order Control Barrier Function-Based Robust Safety-Critical Control With Sampled-Data Input. IEEE TCyb. | [10.1109/TCYB.2025.3599645](https://doi.org/10.1109/TCYB.2025.3599645) | A | Uncertain nonlinear systems | U | Abstract describes robust sampled-data forward invariance; full theorem unavailable. | Critical overlap; equation-level novelty cannot be closed. |
| 06 | Xiong, Zhai and Xia (2025), Robust Whole-Body Safety-Critical Control for Sampled-Data Robotic Manipulators via Control Barrier Functions. IEEE TASE. | [10.1109/TASE.2025.3574342](https://doi.org/10.1109/TASE.2025.3574342) | H | Robotic manipulators (handoff) | U | Publisher page access did not expose usable theorem text in root audit. | Critical sampled-data robotic-safety overlap remains unresolved. |
| 07 | Ali, Shen and Hashim (2024), A Linear MPC with Control Barrier Functions for Differential Drive Robots. IET CTA. | [10.1049/cth2.12709](https://doi.org/10.1049/cth2.12709) | H | Differential-drive robot | U | Handoff lead; input transformation and guarantee need full text. | DDWMR obstacle safety is prior art. |
| 08 | Alavi Nasab, Badiei and Asemani (2025), Safe prescribed time controller for wheeled mobile robots by using control barrier functions as a safety filter. ISA Transactions. | [10.1016/j.isatra.2025.04.024](https://doi.org/10.1016/j.isatra.2025.04.024) | H | Wheeled mobile robot | U | Handoff lead; exact model/assumptions unverified. | Tracking plus CBF is insufficient novelty. |
| 09 | Rehman et al. (2026), Robust and safe control of mobile robots using control barrier functions: Experimental results. European Journal of Control. | [10.1016/j.ejcon.2026.101621](https://doi.org/10.1016/j.ejcon.2026.101621) | A | Wheeled mobile robot | Transformed/physical mapping U | Publisher abstract: robust tracking, observer and CBF-QP; full model pending. | Experimental WMR safety overlap; voltage/contact coverage unknown. |
| 10 | Yuan, Liu, Liu and Su (2024), Differential flatness-based adaptive robust tracking control for wheeled mobile robots with slippage disturbances. ISA Transactions. | [10.1016/j.isatra.2023.11.008](https://doi.org/10.1016/j.isatra.2023.11.008) | H | Wheeled mobile robot | U | Handoff lead; slip model and assumptions pending. | Slip robustness itself is prior-art territory. |
| 11 | Zheng et al. (2024), Adaptive fuzzy sliding mode control of uncertain nonholonomic wheeled mobile robot with external disturbance and actuator saturation. Information Sciences. | [10.1016/j.ins.2024.120303](https://doi.org/10.1016/j.ins.2024.120303) | H | Wheeled mobile robot | U | Handoff lead; physical saturation level pending. | Saturation plus robustness alone is insufficient. |
| 12 | Abadi et al. (2024), Robust Tracking Control of Wheeled Mobile Robot Based on Differential Flatness and Sliding Active Disturbance Rejection Control: Simulations and Experiments. Sensors. | [10.3390/s24092849](https://doi.org/10.3390/s24092849) | H | Wheeled mobile robot | U | Handoff lead; exact experimental/model details pending. | Separate tracking evidence from certified collision safety. |
| 13 | Wang, Zhang and Wang (2026), Event-triggered MPC-PID based trajectory tracking control for differential drive mobile robots. PLOS ONE 21(7), e0354699. | [10.1371/journal.pone.0354699](https://doi.org/10.1371/journal.pone.0354699) | P | Differential-drive robot | Velocity setpoint/servo | Accessible publisher text: tracking with lag, saturation and sampled execution. | Execution mismatch addressed; terminal-voltage/contact collision theorem not established by this comparison. |
| 14 | Vu, Tran, Nguyen and Tran (2023), Development of Decentralized Speed Controllers for a Differential Drive Wheel Mobile Robot. JAEC. | [10.55579/jaec.202372.399](https://doi.org/10.55579/jaec.202372.399) | H | Differential-drive robot | U | Handoff lineage lead; equations pending. | Useful modeling context; does not define international gap. |
| 15 | Tran and Vu (2023), A study on general state model of differential drive wheeled mobile robots. JAEC. | [10.55579/jaec.202373.417](https://doi.org/10.55579/jaec.202373.417) | H | Differential-drive robot | U | Handoff lineage lead; mechanics/gear conventions pending. | Compare model order, coordinates and contact assumptions. |
| 16 | Tran and Vu (2025), Robust MIMO LQR Control with Integral Action for Differential Drive Robots: A Lyapunov-Cost Function Approach. ETASR. | [10.48084/etasr.11583](https://doi.org/10.48084/etasr.11583) | H | Differential-drive robot | U | Handoff lineage lead; input and uncertainty need source audit. | Nominal tracker/model context, not novelty evidence. |
| 17 | Tran and Vu (2026), Constrained Pole Placement Optimization Using the Flower Pollination Algorithm for Velocity Tracking of Differential-Drive Mobile Robots. ETASR. | [10.48084/etasr.18761](https://doi.org/10.48084/etasr.18761) | H | Differential-drive robot | U | Handoff lineage lead; not independently bibliographically verified here. | Compare actual actuator constraints; do not import optimization as a contribution. |
| 18 | Tan, Daş, Ames and Burdick (2025 author version), Zero-Order Control Barrier Functions for Sampled-Data Systems with State and Input Dependent Safety Constraints. | [10.48550/arXiv.2411.17079](https://doi.org/10.48550/arXiv.2411.17079) | P | Control-affine systems; mobile robot examples | General; example-specific | Read v2 Definition 1/Eq.4, Lemma 1/Eq.5, Theorem 1 and method discussion. | Derivative-free flow conditions and inter-sample safety already exist. |
| 19 | Liu, Xiao and Belta (2025; revised 2026), Sampling-Aware Control Barrier Functions for Safety-Critical and Finite-Time Constrained Control. arXiv. | [10.48550/arXiv.2511.11897](https://doi.org/10.48550/arXiv.2511.11897) | P | Control-affine systems; unicycle example | General bounded input | Read v1 Definition 6/Eq.15 and Theorem 2; v2 model/preliminaries inspected. | High-order Taylor/ZOH tightening overlaps; v2 theorem audit still required. |
| 20 | Pagnini and Malis (2026), Segment-safe control barrier functions for model predictive control. European Journal of Control, 101582. | [10.1016/j.ejcon.2026.101582](https://doi.org/10.1016/j.ejcon.2026.101582) | P | Double integrator; nonlinear quadrotor | Model-specific | Publisher preview restricts formal guarantee to connecting segment. | Do not equate straight-segment safety with exact nonlinear-flow safety. |
| 21 | Ovalle, Gonzalez, Fridman and Haimovich (2026), Discrete implementations of sliding-mode controllers with barrier-function adaptations require a revised framework. Automatica 185, 112797. | [10.1016/j.automatica.2025.112797](https://doi.org/10.1016/j.automatica.2025.112797) | A | Adaptive sliding-mode systems; ball-and-plate | Model-specific | Publisher abstract relates actuator capacity, sampling and barrier width. | Adjacent authority/sampling result; performance barrier is not automatically collision CBF. |
| 22 | Bitar and Maalouf (2026, metadata lead), Time-Varying Robust Sampled-Data High-Order Control Barrier Functions With Variable Sampling. IEEE L-CSS. | [10.1109/LCSYS.2026.3701040](https://doi.org/10.1109/LCSYS.2026.3701040) | L | U | U | Only secondary discovery in root audit; primary full text not verified. | High-priority lead; do not claim theorem scope from the title. |
| 23 | Brunke, Zhou and Schoellig (2026), Preventing Inactive CBF Safety Filters Caused by Incorrect Relative Degree Assumptions. IEEE TAC 71(1), 700–707. | [10.1109/TAC.2025.3608258](https://doi.org/10.1109/TAC.2025.3608258) | P | Control-affine systems; quadrotor | General polytopic input | Author-hosted published PDF: Definition 3, §§III and V.A inspected. | Nonuniform relative degree, input effectiveness and sampled safety are direct prior art. |
| 24 | Ma et al. (2026, metadata lead), Enhanced safe control for arbitrary relative degree: A generalized discrete-time CBF approach. Automatica 189, 113026. | [10.1016/j.automatica.2026.113026](https://doi.org/10.1016/j.automatica.2026.113026) | L | U | U | GPT supplied metadata; root publisher fetch returned 403. | Treat as unverified variable-relative-degree threat until source read. |

## Physical model coverage

| ID | Electrical dynamics | Wheel rotational dynamics | Body inertia | Contact force | Longitudinal slip | Lateral slip | Input saturation/bounds |
|---|---|---|---|---|---|---|---|
| 01 | U | U | U | U | U | U | U |
| 02 | U | U | U | U | U | U | U |
| 03 | U | U | U | U | U | U | U |
| 04 | U | U | U | U | U | U | U |
| 05 | U | U | U | U | U | U | U |
| 06 | U | U | U | U | U | U | U |
| 07 | U | U | U | U | U | U | U |
| 08 | U | U | U | U | U | U | U |
| 09 | U | U | U | U | U | U | U |
| 10 | U | U | U | U | U | U | U |
| 11 | U | U | U | U | U | U | U |
| 12 | U | U | U | U | U | U | U |
| 13 | Lag-P; not full electrical | U | U | N-model | U | N-assumption | Y-P |
| 14 | U | U | U | U | U | U | U |
| 15 | U | U | U | U | U | U | U |
| 16 | U | U | U | U | U | U | U |
| 17 | U | U | U | U | U | U | U |
| 18 | U | U | U | U | U | U | Input set-P |
| 19 | U | U | U | U | U | U | Box-P |
| 20 | U | U | U | U | U | U | U |
| 21 | U | U | U | U | U | U | Y-A |
| 22 | U | U | U | U | U | U | U |
| 23 | U | U | U | U | U | U | Polytope-P |
| 24 | U | U | U | U | U | U | U |

## Safety and execution coverage

Full-text status describes actual access/inspection, not completion of the novelty audit.

| ID | Sampling/ZOH | Inter-sample guarantee | Reachability/tube | Recursive feasibility | Viability claim | CBF/HOCBF | Hardware | Full text verified |
|---|---|---|---|---|---|---|---|---|
| 01 | U | U | U | U | U | U | U | No |
| 02 | U | U | U | U | U | U | U | No |
| 03 | U | U | U | U | U | U | U | No |
| 04 | U | U | U | U | U | U | U | No |
| 05 | Y-A | Y-A | U | U | U | HOCBF-A | U | No |
| 06 | U | U | U | U | U | U | U | No |
| 07 | U | U | U | U | U | U | U | No |
| 08 | U | U | U | U | U | U | U | No |
| 09 | U | U | U | U | U | CBF-A | Y-A | No |
| 10 | U | U | U | U | U | U | U | No |
| 11 | U | U | U | U | U | U | U | No |
| 12 | U | U | U | U | U | U | U | No |
| 13 | Y-P | U | U | U | U | N-stated method | N-study | Partial sections/preview; not complete audit |
| 14 | U | U | U | U | U | U | U | No |
| 15 | U | U | U | U | U | U | U | No |
| 16 | U | U | U | U | U | U | U | No |
| 17 | U | U | U | U | U | U | U | No |
| 18 | Y-P | Y-conditional | Flow-P | U | U | ZOCBF-P | U | Partial sections/preview; not complete audit |
| 19 | Y-P | Y-conditional | Taylor-P | U | U | SACBF/HOCBF-P | U | Partial sections/preview; not complete audit |
| 20 | Y-P | Segment only-P | U | U | U | SSCBF-P | N-study | Partial sections/preview; not complete audit |
| 21 | Y-A | U | U | U | U | Adaptive BF; CBF U | Y-A | No |
| 22 | U | U | U | U | U | U | U | No |
| 23 | Y-P | Y-stated; theorem audit pending | U | U | U | CBF-P | Y-P | Partial sections/preview; not complete audit |
| 24 | U | U | U | U | U | U | U | No |

## Source locators actually inspected

- 05: [PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/40920528/); publication metadata/author abstract only, no full theorem text.
- 09: [Publisher abstract](https://www.sciencedirect.com/science/article/abs/pii/S0947358026001743); physical input mapping and sampled theorem not established.
- 13: [PLOS article](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0354699), abstract and modeling/execution descriptions. Root inspected publisher text; Luna reported no-lateral-slip/velocity-servo modeling. Exact model equation extraction still needs audit before baseline reproduction.
- 18: [Author full text v2](https://arxiv.org/html/2411.17079v2), Definition 1 Eq.4, Lemma 1 Eq.5, Theorem 1, Section IV. General flow/hold safety assumptions do not automatically establish DDWMR viability.
- 19: [v1](https://arxiv.org/html/2511.11897v1), Definition 6 Eq.15/Theorem 2 inspected; [v2](https://arxiv.org/html/2511.11897v2) model Eq.1–2/preliminaries inspected. Do not cite v1 locators as a completed v2 proof audit or invent a journal publication.
- 20: [Publisher preview](https://www.sciencedirect.com/science/article/pii/S0947358026001354), abstract, section descriptions and conclusion. Formal segment guarantee and empirical nonlinear-flow validation must remain distinct.
- 21: [Publisher abstract](https://www.sciencedirect.com/science/article/pii/S000510982500696X); full theorem comparison pending.
- 23: [Author-hosted published PDF](https://www.dynsyslab.org/wp-content/papercite-data/pdf/brunke-ral26.pdf), Definition 3, Sections III and V.A. Filename does not change venue: the document header states IEEE TAC January 2026.
- 06: [IEEE landing page](https://ieeexplore.ieee.org/document/11016805) did not return useful theorem text in root audit; leave detailed claims unknown.
- 22 and 24: primary verification remains pending; GPT statements are discovery leads, not verification evidence.

## Gaps introduced by the nine-state contact formulation

1. Add primary-source contact-aware/friction-limited ground-robot safety papers, distinguishing longitudinal slip velocity, braking skid, lateral grip and force constraints.
2. Add closest robust reachability/tube and recursive safety-filter constructions with bounded inputs. Existing generic results may cover the nine-state plant even if DDWMR is absent from the title.
3. Audit how uncertain friction and normal loads enter the contact/body/wheel system, and whether parameter dependence is fixed, measurable or observed.
4. Compare the enclosure and any later K_T construction at equation/theorem/computation level. The G2 analytic framework and finite synthetic Case A now have independent equation review; practical usefulness and originality remain unverified. No K_T has been constructed.

## Screening outcome

Already populated research areas include high-order/sampled-data certificates, flow-based inter-sample safety, bounded-input feasibility, nonuniform relative degree, mobile robot safety and actuator execution effects. What remains **unverified** is an original, useful construction for MASTER v2's voltage/body/contact model. Do not turn U cells into negative novelty evidence. Retain the problem-oriented working title provisionally; no method or first claim is accepted.

## v2.1 scope-specific screening obligations

This note records the adopted v2.1 scope. It changes screening obligations, not the evidence tiers or inspected content of the 24 existing entries. No new prior-art exclusion or novelty result is asserted.

- Distinguish fixed unknown per-wheel tangential contact capacity, hold-wise changes, arbitrary time-varying friction and spatial terrain variation. The proposed first core covers only parameters fixed for the complete execution.
- Distinguish a reduced nonholonomic model with algebraic force budgets from constitutive tire dynamics and physical normal-load/support balance. C_j is a force-scale/envelope parameter, not a proved instantaneous mu_j N_j product.
- Compare motor-voltage electromechanical actuation, joint state/parameter reachability, inter-sample collision/contact validity and recursive safe filtering at equation/theorem/computation level.
- Record whether dependence is preserved, switching or independent-box relaxations are used, and whether the policy learns fixed parameters. Do not equate state-only robust recursion with exact history-dependent viability.
- Review whether real-plant/model correspondence is established or assumed; fitting or bounding a capacity alone does not certify the longitudinal force law.
- Capacity reparameterization, removal of unused phi assumptions and generic inclusion/predecessor logic are not contributions. The narrowed problem may increase overlap with existing fixed-parameter constrained reachability; the novelty question remains open.

## G2 targeted additions - 2026-09-29

The original 24-entry register and its evidence tiers are unchanged. These additions screen the actual G2 candidate, not the entire international literature. `P` means the specified source sections were inspected; it does not mean full theorem verification or G4 closure.

| ID | Source | Evidence and locator | Overlap / scope of knowledge |
|---|---|---|---|
| 25 | Arcak and Maidens, *Simulation-based reachability analysis for nonlinear systems using componentwise contraction properties*, 2017 author manuscript | P: [arXiv PDF](https://arxiv.org/pdf/1709.06661), §2 Proposition 1/Corollary 1, §3 Algorithm 1 and Example 1 | Componentwise exponential bounds and constant-parameter augmentation directly overlap. The displayed result assumes C1 dynamics; this is not evidence that a Lipschitz variant is novel. DDWMR/contact/hardware coverage not determined by this screening. |
| 26 | Meyer, Devonport and Arcak, *TIRA: Toolbox for Interval Reachability Analysis*, 2019 author manuscript | P: [arXiv PDF](https://arxiv.org/pdf/1902.05204), §3.1 Assumption 3, Eq. (4), Proposition 4 and remarks | Growth-matrix interval reachability and integrated uncertainty forcing overlap the candidate's comparison step. Numerical certification and application-specific comparison remain open. |
| 27 | Chen, Abraham and Sankaranarayanan, Flow*: An Analyzer for Non-Linear Hybrid Systems, CAV 2013 | A/partial extraction: [author page](https://home.cs.colorado.edu/~srirams/papers/cav2013-flowstar.html), abstract and search-extracted PDF opening; direct PDF retrieval error | Validated flowpipes are established methodology. No full theorem/smoothness comparison completed in this pass. |

See `docs/reviews/G2_PRIOR_ART_AND_BLOCKERS_v1.md`. Novelty based solely on generic growth bounds, parameter augmentation or tube inclusion is BLOCKED. The candidate's usefulness and any additional original result remain UNVERIFIED; this is not G4 acceptance.

## G2 R2/R3 evidence index - 2026-09-29

The supporting [R2 prior-art supplement](../docs/reviews/G2_PRIOR_ART_SUPPLEMENT_R2.md) records additional targeted primary-source inspections, notably parametric validated integration, Ariadne and Houska/Villanueva/Chachuat predictor-validation. Its explicit access limits remain in force; this index does not upgrade the evidence tiers of the register above or count a partial retrieval as a completed theorem audit.

GPT's [Case A acceptance record](../docs/reviews/GPT_G2_R2_d2cd854_ACCEPT_RECORD.md) and [Case B acceptance record](../docs/reviews/GPT_G2_R3_1da2166_ACCEPT_RECORD.md) retain the generic-method novelty blocker. Both are accepted finite synthetic arithmetic evidence only. Neither establishes superiority over matched generic reachability methods. The Case C certificate-output example was accepted in narrow synthetic scope in the consolidated GPT review of `c9ff32d`; it makes no new prior-art exclusion claim. Matched-assumption comparison remains required before G4.
