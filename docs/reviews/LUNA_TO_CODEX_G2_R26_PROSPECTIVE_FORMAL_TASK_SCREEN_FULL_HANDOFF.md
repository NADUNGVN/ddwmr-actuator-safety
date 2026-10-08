Session: DDWMR | LUNA-G2-SCOPE

# R26 prospective formal-task screen

**Date:** 2026-10-06  
**Disposition:** `NEEDS_OWNER_INPUT` for one prospective, source-inspired CommonRoad task. The task's goal, initial kinematic state, scenario time grid, and sampled obstacle shapes are specified independently of any certificate result. The formal initial state, ego footprint, continuous-time obstacle occupancy, and voltage-hold domain are incomplete. This supports a task proposal, not a query or a physical-DDWMR claim.  
**Execution:** No saved R3/R17/R22–R24 certificate outcomes were opened for selection. Zero native rows, queries, workers, stages, retries, 800-row entries, Auer queries, or matched comparisons were run. No manifest was created; R5 remains `800/800 NOT_RUN`.

## 1. Search protocol declared before candidate inspection

Discovery terms declared before opening candidates:

- `mobile robot obstacle-avoidance benchmark goal region time horizon initial state obstacle geometry`
- `differential-drive navigation task start goal deadline footprint`
- `official robot navigation benchmark scenario specification`

Inclusion rule: admit at most three primary papers or official benchmark specifications if their accessible source states a goal/progress predicate, time window or deadline, obstacle geometry/behavior, and initial-state information. A capability limit, plotted trajectory, or reported result alone is not a task requirement. Missing values stay `unknown`; no value or threshold is selected from R22–R24 outputs. If a source's time or shape convention is ambiguous, do not silently infer a MASTER-compatible domain.

Two candidate task packages were screened. The CommonRoad task candidate was identified from the official scenario repository before parsing its state or obstacle values. Its selection did not use certificate outputs. A failed supplemental vehicle-model document retrieval is recorded below; it returned no document content and was not used as a task source.

## 2. Candidate 1 — CommonRoad scenario `DEU_Muc-1_1_T-1`

### Source and access

The official TUM CommonRoad XML format document, **Version 2018b**, was retrieved as a full PDF from the CommonRoad scenarios repository. Source: [`XML_commonRoad_2018b.pdf`](https://gitlab.lrz.de/tum-cps/commonroad-scenarios/-/raw/a0d1eb927e32128d6dfd658efae34ffa900ada35/documentation/XML_commonRoad_2018b.pdf), SHA-256 `b3262c06ffa772bc065521dbbe3166155fd3920b5d966808850ed660900297643`.

The specific official benchmark file was retrieved at pinned repository commit `a0d1eb927e32128d6dfd658efae34ffa900ada35`: [`DEU_Muc-1_1_T-1.xml`](https://gitlab.lrz.de/tum-cps/commonroad-scenarios/-/raw/a0d1eb927e32128d6dfd658efae34ffa900ada35/scenarios/hand-crafted/DEU_Muc-1_1_T-1.xml). GitLab reports file SHA-256 `c77a14d6df49d021cdba1296020bbac33ee1e51a5e2118d2b70e4902b7489bd8`, size `389,954` bytes. The raw file returned HTTP 200 and parsed as XML. Its root identifies `benchmarkID="DEU_Muc-1_1_T-1"`, `commonRoadVersion="2018b"`, `source="Bing Maps"`, `timeStepSize="0.1"`, and tags `urban multi_lane oncoming_traffic intersection lane_following comfort speed_limit`.

Exact format locators:

- CommonRoad Version 2018b, §1.1, printed p. 2: timestamps are integer indices; seconds are determined by the scenario's fixed root `timeStepSize`.
- §2.1, printed p. 4: all variables use SI-based decimals; the coordinate frame and angle convention are specified.
- §2.5.2, printed p. 11: a known-behavior dynamic obstacle carries a time-discrete trajectory; source trajectories may be dataset measurements, predictions, or hand-crafted.
- §2.6, printed p. 12: initial-state fields are exact; goal-state variables other than time are optional intervals; the ego vehicle shape is explicitly **not included** in the scenario file and depends on a separate vehicle parameter set.

Exact scenario locators are XML paths under the pinned `commonRoad` root: `@benchmarkID`, `@timeStepSize`, `/planningProblem[@id='800']/initialState`, `/planningProblem[@id='800']/goalState`, and `/obstacle`. This is an official benchmark instance; it is a road-traffic scenario, not a DDWMR platform specification.

### Source-transcribed task

| Task field | Source-backed value | Status and interpretation |
|---|---|---|
| **Initial position** | `planningProblem[@id=800]/initialState/position/point`: `(x,y)=(0,0) m`. | **Source-supported**, exact scenario initial state. Mapping this point to MASTER's COM/axle-midpoint reference is a new synthetic coordinate convention; the file does not identify a DDWMR axle/COM. |
| **Initial motion/orientation** | `velocity/exact=10 m/s`, `orientation/exact=-3.2079 rad`, `yawRate/exact=0`, `slipAngle/exact=0`, `time/exact=0`. | **Source-supported** as CommonRoad initial fields. If a source-inspired mathematical instance defines MASTER `p,theta` at the scenario point and aligns its forward axis to the scenario orientation, then `u(0)=10 m/s` and `r(0)=0` are a direct formal mapping because initial slip angle is zero. This is an explicit formal convention, not evidence about an actual DDWMR. |
| **Goal/success set** | Goal position is an oriented rectangle with `length=2.9859 m`, `width=1.9906 m`, `orientation=-3.0002 rad`, center `(-12.0833, 0.0519) m`. The allowed ego orientation interval is `[-3.3929,-2.6075] rad`. | **Source-supported** goal-set predicate. The task metric can be binary membership in this goal set; no extra minimum-displacement threshold is needed or added. The center-to-center displacement is descriptive geometry only, not a chosen threshold. |
| **Goal time** | Goal `time/intervalStart=0`, `intervalEnd=20` (integer scenario indices). Root `timeStepSize=0.1 s`. | **Source-supported** time window is indices `k=0,…,20`, i.e. `t=0,…,2.0 s`. Do not read the `20` as 20 seconds. The task's nominal deadline is 2 seconds. |
| **Obstacle scene** | The XML contains 147 lanelets and 12 obstacles, each with role `dynamic`. Their shapes are rectangles: nine cars of `4.8 × 2 m` and three trains of `15 × 2 m`. Each has an exact initial state at index 0 and 20 exact future trajectory states at indices 1–20. | **Source-supported** sampled geometry and trajectories for this benchmark file, through 2 seconds. There are no static obstacles in the XML's obstacle list. Lanelets are road-network geometry; the scenario does not separately declare a continuous hard lane-boundary safety predicate for this proposed MASTER task. |
| **Obstacle time semantics** | The format declares obstacle trajectories as time-discrete states; this file supplies samples at 0.1-second increments. | Values between sample times are **unknown** in the source. A sound continuous collision test needs an explicit interpolation/occupancy enclosure rule. No piecewise-linear motion or hold-constant rule is silently assigned. |
| **Ego footprint and clearance** | None in the scenario XML. The version-matched format specification §2.6, p. 12, says the ego shape is outside the scenario file. | **Unknown**. Obstacle rectangles are available, but the robot/ego footprint and reference offset are not. A point robot or selected radius would be a new synthetic choice, not source data. |
| **Independent scalar progress** | No scalar minimum displacement, distance threshold, or tracking error is stated. The benchmark defines goal-state membership within its time window. | Use the source's **goal-set reach predicate**. Do not turn the goal-center distance into a threshold. |

No task quantity above came from R22–R24. The screen therefore supplies an independent goal/scene anchor without implying that any voltage candidate succeeds.

### Prospective formal task mapping

An outcome-independent task predicate can be written as follows, conditional on owner choices for the missing domain fields:

1. Use the scenario's map coordinates and the exact initial pose/motion data listed above as the source-inspired nominal state. Missing MASTER wheel states and electrical currents remain unspecified until explicitly selected as synthetic initial intervals.
2. Require the MASTER trajectory to remain collision-free against all 12 scenario obstacles, and to satisfy its formal contact admissibility predicate `c(x(t),vartheta) >= 0`, continuously over the evaluation interval `[0,2 s]`.
3. Require goal-set membership at at least one CommonRoad time index `k ∈ {0,…,20}`: the robot reference position is in the source rectangle and its heading is in the stated orientation interval. The source does not require terminal velocity, so none is added.
4. Interpret the obstacles' discrete records over intervening continuous time only after selecting a documented outer-occupancy or interpolation rule. For a collision certificate, that rule must conservatively enclose the full moving obstacle footprint between samples.

This is a proposed **formal benchmark task definition**, not a result and not a claim that the CommonRoad ego vehicle obeys MASTER. The task geometry and kinematic labels are source-backed; the completion needed for a nine-state, continuous-time, fixed-voltage problem is not.

## 3. MASTER-domain mapping and readiness

| MASTER field | Classification for this task | Missing or synthetic completion |
|---|---|---|
| Goal, initial map position, heading, scalar speed, yaw rate, task time grid, sampled traffic-obstacle geometry | **source-supported** as benchmark scenario data | Map-reference semantics relative to MASTER COM/axle remain synthetic. Initial position/speed may be imported into a mathematical benchmark by convention. |
| Initial slip angle | **source-supported** as zero in the CommonRoad scenario | It does not define the post-initial MASTER longitudinal contact law. |
| Initial `omega_L, omega_R, i_L, i_R` | **unknown** | Must be set as explicit synthetic singleton/interval choices or separately supplied evidence. No no-slip wheel-speed conversion is inferred. |
| Ego footprint and reference-point offset | **unknown** | Choose and justify an explicit formal footprint around MASTER `p`; the source explicitly leaves ego shape to a separate vehicle set. |
| Obstacle trajectories between 0.1-second samples | **unknown** | Select a conservative continuous occupancy enclosure; sampled positions alone do not establish inter-sample collision safety. |
| Fixed hold period `T`, voltage bound `V_max`, action candidates, delay | **unknown / synthetic** | CommonRoad's `timeStepSize=0.1 s` describes the scenario time grid, not an actuator command hold. It must not be equated to MASTER's ZOH without a declared modeling choice. |
| `m,I_z,R_w,b,J_j,B_j,R_j,L_j,k_j,C_j`, fixed joint set `Theta`, and `phi,v_s` | **synthetic or unknown** | The scenario is not an actuator/contact source. A fully prospective reduced-model study may stipulate these, with explicit attribution, ranges, and execution-fixed correlations. No values are proposed from vehicle speed or obstacle outcome. |
| Lanelet constraints | **unknown as a formal safety requirement** | The map supplies lane geometry, but this screen does not invent a lane-keeping predicate. Owner/protocol must decide whether roads are contextual geometry or admissible-space boundaries. |

**Readiness: `NEEDS_OWNER_INPUT`.** The task-level goal and horizon are specific and outcome-independent, but the operating domain is not yet a complete MASTER initial set or full-hold collision problem. It is not `READY_FOR_PROTOCOL_REVIEW` until the missing initial wheel/current set, ego shape/reference, continuous obstacle occupancy rule, hold/action convention, and the synthetic parameter/contact family are prospectively closed. This candidate is **not** classified `INCOMPATIBLE`: as a synthetic reduced-model scenario its goal and obstacle geometry can be represented, but no physical vehicle correspondence is claimed.

## 4. Rejected search lead — differential-drive safe-navigation paper (access rejection)

**Candidate lead:** “A Safe Navigation Algorithm for Differential-Drive Mobile Robots by Using Fuzzy Logic Reward Function-Based Deep Reinforcement Learning,” DOI [10.3390/electronics14081593](https://doi.org/10.3390/electronics14081593), publisher URL <https://www.mdpi.com/2079-9292/14/8/1593>.

**Access:** publisher request returned HTTP 403 in this environment. No primary full text, figures, tables, or scenario parameters were available to inspect. Therefore exact page/equation/table/figure locator: **unavailable because no document content was returned**. No task values are transcribed from the search result or abstract metadata.

**Screen disposition:** excluded at source-access gate; no readiness category is assigned because no task evidence could be inspected. This is not a claim that the paper lacks a suitable task or is mathematically incompatible with MASTER. The source must not be used as evidence until its original task specification is accessible.

## 5. Candidate comparison and one recommended path

| Candidate | Readiness | Evidence-based conclusion |
|---|---|---|
| Official CommonRoad task `DEU_Muc-1_1_T-1` with version-matched XML schema | **`NEEDS_OWNER_INPUT`** | Supplies a fixed goal region, a 2-second benchmark time window, exact initial kinematic fields, map geometry, and sampled moving-obstacle shapes. It omits ego footprint and leaves obstacles time-discrete; it has no DDWMR wheel/current or contact/voltage family. |
| Safe-navigation differential-drive article lead, DOI 10.3390/electronics14081593 | **Excluded at access gate; no readiness classification** | HTTP 403 prevents verifying its task definition. No conclusion about its substantive compatibility follows. |

**Recommended path:** keep CommonRoad `DEU_Muc-1_1_T-1` as the one prospective *source-inspired synthetic task anchor*, stop the source-search branch here, and do not run a query yet. Do not start a fourth search cycle before an owner decision. The smallest owner decision is whether this use is acceptable **with all missing plant/domain quantities declared synthetic** (and no physical-platform claim), or whether the project requires a DDWMR-specific source-backed task instead. If approved as the synthetic anchor, the next protocol draft must explicitly choose: (i) the ego footprint/reference around `p` and treatment of lanelets, (ii) a conservative continuous occupancy rule between obstacle samples, and (iii) initial wheel/current sets plus `T`, `V_max`, allowed held actions, and a fixed correlated `Theta`/contact law. Those choices are not present in the source and must not be represented as source-backed.

The 2018b specification is used because the selected XML file declares `commonRoadVersion="2018b"`. The source-schema statement that the ego shape is excluded is sufficient to record that field as unknown.

## 6. Gate and execution status

**HOLD; G1 PASS — restricted reduced-model scope; G2/G3/G4 and physical correspondence UNVERIFIED.** R5 remains `800/800 NOT_RUN`. This screen neither opens a query manifest nor authorizes a query. It defines a possible task independently of certificate outcomes; Codex must review this task and any proposed synthetic completions before any protocol is frozen.

## Sources

1. Koschi, Manzinger & Althoff, *CommonRoad: Documentation of the XML Format*, version 2018b, especially §§1.1, 2.1, 2.5.2, 2.6, printed pp. 2, 4, 11–12. Official repository PDF and hash given above.
2. TUM CommonRoad official scenario file, `DEU_Muc-1_1_T-1.xml`, pinned commit and GitLab content hash given above.
3. MDPI differential-drive safe-navigation article, DOI 10.3390/electronics14081593; original publisher URL returned HTTP 403; no document locator can be verified.
