Session: DDWMR | LUNA-G2-SCOPE

# R25 source-backed operating-domain audit

**Date:** 2026-10-06  
**Disposition:** No defensible published/manufacturer-backed task and parameter envelope was found that can replace the R22–R24 synthetic scale while preserving MASTER v2.1's voltage and contact semantics. The sources provide useful attributed scales and one physical-platform lead, but neither candidate closes the task, fixed-parameter, driver, or contact requirements.  
**Execution:** No query, row, worker, stage, retry, manifest, or study entry was run or created. R5 remains `800/800 NOT_RUN`. No R3/R17 outcomes were inspected. Existing R17–R24 and G4 artifacts were not modified.

## 1. Scope and controlling model

This audit follows the R25 assignment, `AGENTS.md`, the four canonical `research_context` files, MASTER v2.1 §§5–12 and 20–23, and the accepted R24 review. R24 establishes that its paired ordering result is a narrow synthetic result and that a source-backed task/domain must be independently specified; its computed progress intervals do not supply a task threshold.

MASTER v2.1 requires one nine-state plant with independent body and wheel speeds, exact lateral kinematics, execution-fixed joint parameter labels, a known fixed longitudinal law

\[
F_j=C_j\phi(\sigma_j/v_s),\qquad F_j^2+Y_j^2\le C_j^2,
\]

and an ideal bidirectional four-quadrant winding-terminal voltage held for a fixed period. A candidate source must support a sound mapping to that model or a validated model-error enclosure over an independently declared task domain. Numerical parameter values alone do not provide that mapping.

The source classifications below distinguish **specified** values from **measured** values. A paper or product table is treated as a reported model/product specification unless it describes a measurement procedure. No unstated uncertainty range, correlation, hardware build, or convenient default is added.

## 2. Primary sources and access verification

### Candidate A — Tran and Vu's general DDWMR model

Anh-Minh Duc Tran and Tri-Vien Vu, “A Study on General State Model of Differential Drive Wheeled Mobile Robots,” *Journal of Advanced Engineering and Computation*, 7(3), 2023, DOI [10.55579/jaec.202373.417](https://doi.org/10.55579/jaec.202373.417). The DOI resolved to the publisher article page; the publisher PDF was retrieved directly from [JAEC](https://jaec.vn/index.php/JAEC/article/download/417/219) on 2026-10-06 (HTTP 200). SHA-256 of the retrieved PDF: `14e4133a6c780d616e703942b09eb5ecd8fd9b9110b6d1ab3c6ba3b1e189bc46`.

Exact source locators: the no-slip kinematics and motor equations are in Eqs. (1)–(7), printed pp. 175–176; the numerical values are in “Tab. 1: Specifications of the general DDWMR model,” printed **p. 178** (PDF page 5). The table page was rendered and visually checked. The earlier local provenance note's p. 177 locator is off by one; this report records the publisher PDF's printed page.

### Candidate B — TurtleBot3 Burger with the listed XL430-W250-T actuators

ROBOTIS [TurtleBot3 Features](https://emanual.robotis.com/docs/en/platform/turtlebot3/features/) and [DYNAMIXEL XL430-W250-T e-Manual](https://emanual.robotis.com/docs/en/dxl/x/xl430-w250/) are official manufacturer pages. Both returned HTTP 200 and were inspected on 2026-10-06.

Exact locators: the Features page's “Hardware Specifications” table and “Parts List” identify the Burger values and its two XL430-W250-T wheel actuators; the XL430 e-Manual §1, “Specifications,” lists actuator product values and modes; §2, “Control Table,” lists digital operating-mode and goal registers, including Operating Mode (11), Torque Enable (64), Goal PWM (100), and Goal Velocity (104). These are manufacturer specifications, not in-situ measurements or a certified joint uncertainty set.

## 3. Provenance matrix

| Required field | Candidate A — published general DDWMR model | Candidate B — TurtleBot3 Burger / XL430-W250-T |
|---|---|---|
| **Mass** | Tab. 1 p. 178 specifies robot body mass `m_b=15 kg`, right/left wheel masses `2.55/3.45 kg`. These are model-table values; measurement provenance is unstated. The article defines total system mass in its model text, but does not state that the listed masses exhaust every translating component. The arithmetic sum `21 kg` is only an inference under that unstated completeness assumption and is **not adopted** as MASTER `m`. [A] | Features table specifies Burger weight `1 kg` “(+ SBC + Battery + Sensors)” and maximum payload `15 kg`. Product weight is specified, not a measured interval. The exact installed load/build and mapping to MASTER `m` are **unknown**. [B1] |
| **Yaw inertia, wheel radius, track, COM geometry** | Tab. 1 p. 178 specifies robot-body `J_z=0.35 kg·m²`, half wheel-base `W=0.2 m`, right radius `R_wR=0.0675 m`, and left radius `R_wL=0.0825 m`. These are reported model points. The side-specific radii do not map to MASTER's single shared `R_w`; COM-projection/axle-midpoint equality is not established. Whether the tabulated body inertia includes all masses required by MASTER `I_z` is **unknown**. [A] | Features table gives overall Burger size `138 × 178 × 192 mm` (L × W × H), not wheel radius, wheel separation, or axle-to-COM geometry. Those values and yaw inertia are **unknown** from the inspected manufacturer pages. Overall size is not by itself a collision-footprint radius relative to MASTER's reference point. [B1] |
| **Wheel/motor inertia and damping** | Tab. 1 p. 178 specifies wheel inertias `J_wR=0.8×10⁻³ kg·m²`, `J_wL=1.8×10⁻³ kg·m²`, and motor viscous coefficients `B_mR=0.0132`, `B_mL=0.0088 N·m·s/rad`. Motor inertia is not listed. Gear-side reflection into MASTER's wheel-side `J_j,B_j` is **unknown**; the article also reports different gearbox efficiencies, so an ideal lossless reflection cannot be inferred. [A] | XL430 e-Manual gives a 57.2 g actuator mass and gear ratio, but not winding-rotor inertia or damping values that map to MASTER's `J_j,B_j`. Those values are **unknown**. [B2] |
| **Winding resistance and inductance** | Tab. 1 p. 178 specifies motor-armature `R_aR=0.7424 Ω`, `R_aL=1.1136 Ω`; `L_aR=0.0172 H`, `L_aL=0.0127 H`. These are reported model points with no stated tolerances or measurement provenance. [A] | XL430 product pages do not expose winding `R_j,L_j`; both are **unknown**. The integrated actuator's supply range does not determine winding parameters. [B2] |
| **Matched torque/back-EMF constant** | Tab. 1 p. 178 specifies motor-side torque constants `K_tR=0.6303`, `K_tL=0.5157 N·m/A`. Eq. (5), p. 176, uses the corresponding coefficient in the armature equation as well. This is evidence for the paper's motor-side model coefficient, not MASTER's wheel-side `k_j`: ratio/shaft convention and efficiency prevent an exact compatible map. No uncertainty interval is given. [A] | XL430 tables provide voltage/current-dependent output stall-torque figures, but no winding torque/back-EMF constant pair or motor-side mapping. Both MASTER constants are **unknown**. [B2] |
| **Reduction and side correlations** | Tab. 1 p. 178 reports gearbox ratios `i_gR=i_gL=2` and efficiencies `η_gR=97.75%`, `η_gL=72.25%`. Side asymmetry is specified, but an uncertainty correlation set is not. The non-unit/different efficiencies conflict with silently treating the mechanism as MASTER's ideal rigid, lossless, bidirectionally backdrivable reduction. [A] | XL430 e-Manual specifies a 258.5:1 product gear ratio. This does not identify the robot's effective wheel-side conversion, transmission loss, backlash, compliance, or joint correlations. No joint uncertainty set is supplied. [B1, B2] |
| **Voltage limit and driver semantics** | Eq. (5), p. 176, uses armature voltage variables, but no symmetric terminal-voltage limit, four-quadrant source/sink behavior, current/thermal limits, bus behavior, or driver implementation is specified. An armature-voltage symbol is not sufficient evidence for MASTER's ideal held terminal source. **Unknown/incompatible evidence.** [A] | XL430 specifies input supply `6.5–12.0 V` (recommended `11.1 V`), digital packet command over a TTL bus, and Velocity, Position, Extended Position, and PWM Control (“Voltage Control”) modes. Its control table exposes Goal PWM and Goal Velocity under an internal actuator control interface. The supply rating is **not** MASTER's ± winding-terminal `V_max`; the manual does not establish direct ideal terminal-voltage actuation, four-quadrant source/sink behavior, or access to winding current states. [B2] |
| **Sample/hold period and delay** | No fixed digital hold period, command delay, or exact sampled-state semantics are reported for the model values. **Unknown.** [A] | Digital packets and control modes are documented, but no fixed zero-delay period matching MASTER's ideal ZOH is specified in the inspected pages. Bus baud rate or product input voltage cannot stand in for a control hold period. **Unknown.** [B2] |
| **Initial-state uncertainty and provenance** | No intervals for pose, body speed/yaw rate, wheel speeds, or currents; no estimator or calibration error model. **Unknown.** [A] | No initial-state distribution/interval or estimator error bounds in the inspected product pages. **Unknown.** [B1, B2] |
| **Obstacle, footprint clearance, independent task metric** | No obstacle geometry, clearance requirement, task direction/displacement, or deadline is specified in the inspected model and numerical table. **Unknown.** [A] | The product's overall size and maximum speeds are specified. The Features page lists maximum translational velocity `0.22 m/s` and maximum rotational velocity `2.84 rad/s` for Burger; these are platform capability limits, not a required displacement/clearance by a deadline. No obstacle scene, safety clearance, task direction, or deadline is specified. **Task metric unknown.** [B1] |
| **Longitudinal traction shape/scale** | The paper assumes rolling without slipping and derives force/motion relations; it does not identify a measured slip-force curve, a known MASTER-compatible `φ`, regularization speed `v_s`, or calibration range. **Unknown.** [A] | No `φ`, `v_s`, or longitudinal slip-force curve is specified. The product documentation does not describe a MASTER-compatible slip law. **Unknown.** [B1, B2] |
| **Per-wheel effective tangential capacities and lateral reactions** | No fixed `C_j` values/bounds or lateral allocation law. The no-slip model's tractive forces are not a source for MASTER's shared longitudinal/lateral force budget `F_j²+Y_j²≤C_j²`. **Unknown.** [A] | No per-wheel tangential capacity, normal-load/support allocation, lateral-reaction envelope, or contact-validity domain. **Unknown.** [B1, B2] |
| **Execution-fixed joint uncertainty and correlations** | The article supplies point values used in its model, with left/right asymmetries. It does not supply a compact joint uncertainty set, data-derived ranges/correlations, or evidence that physical parameters stay in a fixed family for the complete execution. The point model itself can be read as fixed for its own calculation only. [A] | Product specs are not distributions or joint bounds. No family of correlated device/contact parameters or physical fixed-over-execution evidence is given. [B1, B2] |

**Epistemic note:** neither source labels its tabulated parameter values as measurements with a protocol or as validated uncertainty bounds. “Specified” above means the publisher/manufacturer reports the value; it does not mean measured, identified, calibrated, or guaranteed over a physical operating envelope.

## 4. Comparison to MASTER and source-backed task readiness

### Candidate A

This candidate can provide **attributed numerical scales for a theoretical stress benchmark only**. It is not a complete source-backed parameter envelope and does not identify a traceable robot build. Three direct incompatibilities prevent physical substitution under MASTER v2.1:

1. The paper explicitly assumes rolling without slip and kinematically relates body speed/yaw to wheel speeds (Eqs. (1)–(2), p. 175). MASTER keeps `u,r,ω_L,ω_R` independent and models slip through `σ_j`; a no-slip model cannot supply the missing force-slip law or prove inclusion of slip trajectories.
2. Its right/left radii differ (`0.0675 m` and `0.0825 m`), whereas MASTER has one `R_w`. Its reported gearbox efficiencies also differ by side and are not the ideal lossless reduction stipulated by MASTER. Averaging or absorbing these mismatches into new values would be an unsupported model change.
3. It supplies no fixed `C_j`, `φ`, `v_s`, lateral support/contact evidence, task domain, or joint uncertainty set. The reported motor numbers therefore cannot define a complete fixed-parameter `Θ` or `D_c(ϑ)`.

No measured discrepancy bound shows that an actual trajectory is contained in the MASTER family. A parameter-point substitution cannot repair omitted lateral/support dynamics or no-slip versus slip-model differences.

### Candidate B

The TurtleBot3 Burger is a manufacturer-documented two-wheel differential-drive platform and therefore a useful **hardware lead**, but the listed XL430-W250-T smart servos do not establish MASTER's direct winding-terminal voltage input. They accept digital operating-mode commands through an internal servo interface. In particular, the e-Manual's “PWM Control Mode (Voltage Control Mode)” and Goal PWM register do not by themselves prove a continuously held terminal-voltage signal with MASTER's symmetric bound, four-quadrant behavior, no delay, and exposed winding-current state. Treating the 6.5–12.0 V product input rating as MASTER's terminal `V_max` would silently change the actuator model.

The platform also has a ball caster in the Burger parts list, while MASTER's lateral reaction budget allocates the required lateral force across the two drive contacts. The source pages do not show that the caster/support forces can be omitted, that the COM projection lies exactly at the axle midpoint, or that the two drive contacts satisfy MASTER's shared `C_j` law. A nominal overall size is not a complete swept-footprint and obstacle-clearance model.

**Disposition as currently documented:** unsuitable as a direct physical counterpart under the unchanged MASTER assumptions. It may be reconsidered only after an exact-build instrumentation plan establishes the actuator interface or the plant formulation is versioned to include the actual servo/driver/support behavior. No such formulation change is made here.

### Task metric

Neither candidate source supplies an independently chosen collision-avoidance task with a direction, required displacement or clearance, and deadline. The TurtleBot3 maximum-speed entries are capabilities, not task success conditions. R22–R24's computed progress intervals cannot be repurposed as a task threshold; selecting a threshold from those outcomes would be circular and would not create an external task requirement.

## 5. Readiness decision and exact blockers

| Candidate | R25 category | What its sources can support now | Blocking evidence |
|---|---|---|---|
| A — Tran & Vu general DDWMR parameter table | **(a), limited to attributed synthetic/theoretical scales.** | A source-cited point-scale stress case for the tabled mass/inertia/geometry/motor values, if clearly labeled as a synthetic parameter comparison and if missing parameters are not filled in as though sourced. It does not provide intervals or a runnable complete domain. | Independent task metric; common-radius-compatible geometry; shaft/efficiency map; terminal-voltage limits and ZOH; initial-state intervals; contact `φ,v_s,C_j` and lateral/support basis; joint fixed-parameter uncertainty set; physical model-error/inclusion evidence. |
| B — TurtleBot3 Burger with XL430-W250-T | **(c), unsuitable as shipped under the current direct-voltage MASTER assumptions.** | Official variant, dimensions, nominal assembled weight, speed capabilities, actuator SKU, servo gear ratio, supply range, and command-interface facts. These support screening and planning measurements, not the current plant's parameter set. | Direct winding-voltage/current access or a sound servo/driver-inclusive revised model; exact build and mass/COM/inertia/track/radius; sample period/delay; motor parameters; two-drive-contact/caster support model; slip/contact law and capacities; state-estimator bounds; obstacle/footprint domain; independently specified task. |

No candidate currently qualifies as a source-backed physical task/domain for a voltage-selection G2 experiment. Candidate A is useful only for explicitly attributed synthetic stress testing; Candidate B is a hardware lead but its documented actuator semantics do not match the present plant.

## 6. Measurements/evidence needed before a physical-domain proposal

For a future exact TurtleBot3 Burger build (or another selected platform), the minimum named evidence is:

1. **Build and mechanics:** exact revision/BOM, sensors/battery/payload configuration, wheel loaded radii and track, total translating mass, COM projection relative to axle, yaw inertia, wheel and reflected rotor inertia/damping, gear ratio direction, backlash/compliance, and transmission losses. Include tolerances and cross-parameter correlations rather than independent convenient ranges.
2. **Actuation:** establish whether raw motor-terminal voltage can be commanded and measured. Characterize winding `R,L`, torque/back-EMF pair, current sensing/limits, source and regenerative-sink behavior in all used quadrants, voltage clipping, thermal protection, firmware and bus delay, and a fixed sample/hold period. If the integrated XL430 interface remains in use, identify a driver-inclusive plant instead of equating Goal PWM or supply voltage with winding `V`.
3. **Contact/support:** on the declared surface/load envelope, identify a fixed known regularized longitudinal slip law and its scale; estimate per-wheel effective tangential capacities and correlations; measure/justify lateral support allocation including the ball caster and load transfer; then produce a validated inclusion or sound model-error enclosure for the exact MASTER equations. A friction coefficient, normal-load estimate, peak traction measurement, or fit alone is insufficient to establish the same `C_j` in both the force law and force budget.
4. **Task and initial domain:** independently declare travel direction, minimum progress or clearance, deadline/hold duration, obstacle geometry/motion, robot swept footprint, and decision-time intervals for all nine states, each with provenance. These must be fixed before looking at any computed progress interval.

These are preconditions for proposing a task-specific domain; this audit does not authorize hardware work or create a manifest/query.

## 7. Recommendation and status

**Recommendation:** do not run another G2 task experiment or query from the current sources. The task threshold and compatible operating domain are both absent, and Candidate A's parameter points plus Candidate B's product ratings cannot close the missing input/contact semantics. Resume only after one exact candidate has an independently specified task and a source/measurement-backed, MASTER-compatible fixed-parameter family (or an explicitly reviewed model-error extension).

**Gate disposition unchanged:** **HOLD; G1 PASS — restricted reduced-model scope; G2/G3/G4 UNVERIFIED; physical-platform correspondence UNVERIFIED.** This source audit does not promote a gate, validate hardware, or make a novelty claim. No source, manifest, receipt, runner, R17–R24 artifact, or G4 artifact was changed. No commit or push was made.

## References

- [A] Tran & Vu (2023), JAEC 7(3), DOI [10.55579/jaec.202373.417](https://doi.org/10.55579/jaec.202373.417); publisher PDF: <https://jaec.vn/index.php/JAEC/article/download/417/219>.
- [B1] ROBOTIS, [TurtleBot3 Features](https://emanual.robotis.com/docs/en/platform/turtlebot3/features/).
- [B2] ROBOTIS, [DYNAMIXEL XL430-W250-T e-Manual](https://emanual.robotis.com/docs/en/dxl/x/xl430-w250/).
- Governing model and scope: `research_context/MASTER_RESEARCH_CONTEXT_v2.md`, §§5–12, 20–23; R25 assignment and accepted R24 review as cited above.
