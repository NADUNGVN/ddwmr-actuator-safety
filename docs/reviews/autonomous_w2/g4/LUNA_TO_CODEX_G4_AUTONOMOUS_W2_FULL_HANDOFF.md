Session: DDWMR | LUNA-G4-AUER

# G4 W2 — baseline/source audit and peer-release handoff

**Date:** 2026-10-07  
**Disposition:** `PARTIAL` — independent Auer/source audit and endpoint-progress derivation are documented; no immutable G2 W2 release was available to audit, so no matched comparison was ready or run.  
**Repository:** `main`, HEAD `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe` at start. The shared tree already contained extensive work from prior sessions; I preserved it and wrote only to G4-owned W2 prefixes.  
**Environment observed:** Windows 10.0.26200.0, PowerShell 5.1.26100.9444, Python 3.12.12 (other installed runtimes 3.14/3.11/3.10), .NET runtime 8.0.15; no .NET SDK reported.  
**Execution boundary:** zero new query/worker/stage/batch runs; no R19 ID retry; no compute lock acquired because no substantial numeric run occurred; no commit/push.

## Finding 1 — no G2 release exists to audit

**Evidence.** At the final boundary check, 2026-10-07 09:38:52 UTC, `coordination/autonomous_w2/g2/STATUS.json` remained at sequence 1 with `artifacts=[]`, `peer_release_consumed=null`, and next action still describing candidate derivation before implementation. The same status bytes/hash were observed at 09:34 UTC and again after a 30-second interval: SHA-256 `4F0982DE0FD671FA70DB2B69193342052F6ED601C8F4F8960947B7E9A00EBE63`. The G2 W2 namespace contained only STATUS. There was no release manifest/source/proof hash to bind. The file still says the peer G4 status was absent at start, so it has not been refreshed to observe the current G4 namespace.

**Consequence.** An audit decision of `ACCEPT_FOR_SCOPED_VALIDATION`, `REVISION_REQUIRED`, or `MATHEMATICAL_BLOCKER` would be unsupported without an exact immutable candidate release. I record `NOT_ISSUED_NO_IMMUTABLE_G2_RELEASE` in `coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v1.json`. The exact request and required audit bindings are in `coordination/autonomous_w2/g4/PEER_AUDIT_INPUT_v1.md`; no outside message was sent.

**Status.** G4 candidate audit is **AWAITING_PEER_INPUT**. This is not candidate acceptance and does not promote G4.

**Required action.** When G2 publishes, bind the exact release sequence/hash and re-audit proof, equations, source closure, task, endpoint output, arithmetic dependencies, resource stops, and failure taxonomy. Return routine defects through a versioned G4-owned file and continue W2 work without waiting for Codex GO.

## Finding 2 — Auer baseline identity and source fidelity

**Evidence.** I inspected the retained Auer–Kiel–Rauh 2013 primary text, §§4.1–4.2, the method contract v2, and the local R9 producer/RHS/clip/replayer plus R17 common adapter/composition code. The paper's Eq. (26) treats an autonomous IVP with interval initial values; its Eqs. (31)/(33)/(40) provide piecewise range/generalized-derivative handling; Eqs. (35)/(41) account for discontinuity gaps; §4.2 Eqs. (42)–(43), printed p. 742, describe a validated functional tube around an approximate path with VALENCIA-IVP. In the continuous clip specialization, the jump correction is zero, but the corner generalized derivative remains `[0,1]` and full residual/tube inclusion is still required.

The local implementation identifies itself as `AUER2013_PIECEWISE_RESIDUAL_RECONSTRUCTION_DDWMR_R4`; it integrates the nine physical states with twelve constant labels (21 coordinates). Its `rhs.py` maps the MASTER v2.1 equations; `piecewise.py` implements exact clip range/generalized derivative; `residual_ivp_g4_matched_v3_r9.py` constructs affine rational approximate paths, the interval Jacobian/residual, inclusion checks and endpoint; `replay_ivp.py` independently reconstructs those proof fields. The local producer and replayer share the `validation.g2` exact rational/interval arithmetic and rational Taylor trigonometric backend. `auer_common_adapter_v3_r17.py` reconstructs every per-slab full-time total hull; `verify_matched_composition_v3_r17.py` replays the native proof before recomputing common margins.

The retained native VALENCIA seed source is `ValEncIA-IVP_0.92_2e.cpp`, not the 2013 extension or DDWMR solver. Its saved build disposition is `BLOCKED_BEFORE_LINK`: syntax-only compilation passed, but no full executable was built; the Windows rounding/backend configuration and missing 2013 piecewise extension remain explicit blockers. No claim here that the R19 Auer worker is the original VALENCIA binary, that a successful syntax build proves method fidelity, or that the paper supplied this DDWMR solver.

Key byte identities are tabulated in [the audit checklist and crosswalk](AUDIT_CHECKLIST_AND_SOURCE_CROSSWALK_v1.md). The R19 prospective closure declares 575 paths, SHA-256 `A50BC0452E6B8F164988A4AF8D669E563381F157F86188CA8C7EE1FB1518CA76`. The local-source snapshot v9 has SHA-256 `FE3309D5B17C6D2968C826EAF1A0759C3B9FBF848432B72842FFF5B4DB726D91` and predates later R9/R17 comparison modules; it is historical context, not a complete W2 source lock.

**Consequence.** The appropriate baseline label is a local Auer-method reconstruction using exact rational validation, not original VALENCIA software. Method-level fit is supported; source fidelity to the historical executable and novelty are not. Producer/replayer agreement has shared arithmetic trust dependencies.

**Status.** Source mapping **documented**. Existing native proof/replay evidence was not regenerated in this W2 pass.

**Required action.** A new W2 comparison must freeze a complete current source closure for both producers/checkers, disclose shared source/arithmetic, and use a new <=60 s / <=1 GiB worker/replay/audit envelope. Do not relabel or mutate R19 sources.

## Finding 3 — historical R19 closure rehash and the current context drift

**Evidence.** I added a read-only project-contained closure auditor at `validation/autonomous_w2/g4/audit_source_closure.py` and ran:

```powershell
python validation/autonomous_w2/g4/audit_source_closure.py --root . --manifest research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R19_PROSPECTIVE.json
```

The closure was checked twice: once with a one-off read-only hash loop and once with the reusable auditor above. Both reports were `MISMATCHES_FOUND`, with 571/575 dependency paths matching exact byte count and SHA-256. The four mismatches are all governing files that changed in the shared tree after the R19 closure was frozen:

| Path | R19 expected bytes / SHA-256 | Current bytes / SHA-256 |
|---|---|---|
| `AGENTS.md` | 4,589 / `d40542cc226351ec13b0adb85e16bc7702d5d1931520cd4ff49ac98b63a23f58` | 5,534 / `c080533679d7985a4b2925ef0a5546eb198a3805eb12c80be436e6a6faaf3abb` |
| `research_context/DECISION_LOG.md` | 14,681 / `6b37685aecbbc8959e35f64b5164a88d1f6e2095ba48fe88db24fc630f9a7fcb` | 16,711 / `74120d509abbc97d3f0513d2a0624b8aea2e2417a63e12ac9a122acc576a9a8f` |
| `research_context/MASTER_RESEARCH_CONTEXT_v2.md` | 42,311 / `ccc38759aac8f48cbb2cb1f70cfc4df4e1a17ddc53c76add204f17a1d451e422` | 44,512 / `f22985fb19aac2524a23a1720bfabeca150227f726fa814e6ee165c4708bc348` |
| `research_context/REVIEW_GATE.md` | 7,299 / `2eddbf554834167dce51f6a4eba6b8c3ad463d975296053e27f1eea7ad896a03` | 7,566 / `f0f8962a5e1661dea6c886335589468c582d4a66200abda7af2a3387dea493ad` |

The R9 solver, RHS, clip code, native replay, Auer adapter, common checker, composition auditor, and R3 adapter each match their R19 closure entries. The auditor did not write to the old closure or its dependencies. Its per-path containment check rejects root escapes and missing files.

**Consequence.** The old closure remains historical evidence with four known current-tree mismatches, not a hash-valid W2 release closure. These mismatches are not a conclusion that the pinned R19 scientific sources were altered; they reflect changed project instructions/context. New W2 source binding must include current authority and the exact method/checker code actually used.

**Status.** `571/575` historical entries verified; four context-file mismatches reproduced. Auditor exited nonzero because mismatches exist.

**Required action.** Preserve the R19 closure unchanged. For a new release, construct and verify a fresh closure; do not refresh this historical manifest in place.

## Finding 4 — DDWMR full-time and endpoint audit obligations

**Evidence.** The checked model equations are the MASTER v2.1 nine-state system with voltage as the input, common one-hold `V`, and fixed execution labels. The local Auer R9 source rejects incomplete label maps/out-of-range held voltage, evaluates `dot(label)=0`, requires a 21×21 interval Jacobian, tests residual derivative inclusion and integrated tube inclusion on each closed slab, chains step endpoint boxes and unchanged labels, and stores full-time hulls. Existing common code evaluates contact margin `sqrt(C_L^2-F_L^2)+sqrt(C_R^2-F_R^2)-|m u r|` conservatively and collision lower margin from full-footprint circle clearance on every closed segment. The common checker expressly says a pass applies only to the supplied tube; native IVP inclusion must be independently replayed first. The R19 profile's common predicate contains collision and contact, not task progress.

I independently derived the x-progress lower bound from the exact kinematics and checked the formula against the existing G2 R2 note, producer/checker source and accepted R2 review. If a replayed full-time tube encloses `u(t)∈U` and `r(t)∈R`, with full initial heading `Theta0` and exact `T>0`, then `Theta=Theta0+[0,T]R` encloses every heading. With `M=max(|Theta_-|,|Theta_+|)`, `cos(theta)∈[max(-1,1-M^2/2),1]`. The exact four-corner interval product of `U` and this cosine range yields `g_-`; therefore `p_x(T)-p_x(0)=∫u cos(theta)dt >= T g_-`. This is valid for either sign of `u`, uses no small-angle assumption, and cancels the common initial position through the integral identity. The derivation is recorded in the audit checklist.

For Auer, the common checker can form `U` and `R` as hulls across proof-replayed per-slab `u/r` ranges. For R3, reconstruct physical `u/r` ranges from the replayer-validated `P1_scaled`, `eta_physical`, and benchmark coordinate scales. This progress result remains a sufficient outer bound; lost correlations can make it inconclusive. It does not certify the upstream trajectory, collision/contact, recursive feasibility or physical movement. The threshold and progress axis must come from the prospective task, independently of certificate outcomes.

**Consequence.** Existing R19 endpoints are not enough to claim a task-progress decision: full-time collision/contact and endpoint task output are separate proof obligations. The two methods must be replayed against the same task-level progress threshold before counting an eligible action.

**Status.** Mathematical x-displacement inclusion **derived**; no task threshold or candidate-specific endpoint proof is available. W2 checklist C8 remains pending release.

**Required action.** Bind the G2 task's precise endpoint predicate and independent rationale, then implement/replay its exact rational lower bound for both proof formats. Do not use the old R2 5 cm threshold unless the new prospective task independently selects it before seeing matched outputs.

## Finding 5 — prior art and contribution falsification

**Evidence.** The accepted R23 audit establishes that paired IVPs sharing initial state/parameter latents are generic validated-reachability methodology; it does not establish numerical tightness or plant-specific benefit. The R24 review accepts the equation-level result that the frozen R23 synthetic matched-voltage ranking does not yield a common threshold across the widest cells and stops that branch as a proposed paper contribution. It does not rule out every DDWMR-specific contribution. The Auer 2013 full text supports the local residual/piecewise method reconstruction, not an exact DDWMR-specific bound. Literature-matrix rows 25–27 plus the primary-source audit record overlap from Arcak–Maidens (componentwise comparison and parameter augmentation), TIRA (growth-bound interval reachability), Houska–Villanueva–Chachuat (predictor-validation), and Flow* (partial retrieval only). Their assumptions and applicability differ; the current G2 candidate is needed for an equation-level claim comparison.

W2's first G2 hypothesis is a parameter-aware, time-local variation-of-constants enclosure retaining signed motor/body/slip dependence plus endpoint displacement. Exact motor propagation, residual validation, fixed-parameter augmentation, predictor comparison and tube inclusion are established techniques. A distinctive contribution, if any, must be an exact DDWMR-specific inequality or validated computational effect beyond restating those generic techniques. Without the G2 proof/source and an independently meaningful task, novelty and matched performance remain unresolved.

**Consequence.** No new Auer comparison would answer the contribution question today. The historical ten-pair pilot is adverse descriptive evidence against the old R3 coverage claim, but it cannot measure the new G2 effect, make a population inference, or establish universal Auer dominance.

**Status.** R23 generic paired-construction novelty **blocked**; frozen R23 action-order branch **stopped**; W2 candidate contribution **unresolved** pending exact G2 release and prospective task.

**Required action.** On receipt, audit the exact first G2 hypothesis against the closest primary sources at theorem/equation level. Run a fresh matched comparison only if the candidate is sound and a falsifiable task/coverage-or-cost criterion is frozen before either producer sees outcomes.

## Preserved pilot and execution accounting

- R19/R20's ten paired rows remain historical selected development evidence: Auer 9 `CERTIFIED`, R3 6 `CERTIFIED`; three Auer-only and zero R3-only. This is not a fresh W2 run, a statistical sample, or a common-margin comparison on the four R3-`UNKNOWN` rows.
- The original R19 checker failure and the separate R20 read-only retrospective replay remain preserved as distinct facts. No historical proof, result, review or source snapshot was modified or rewritten.
- W2 G4 native development/smoke attempts: **0/12 per method**. W2 confirmation rows: **0/24 per method**. This is because no G2 candidate/source release or primary comparison criterion is frozen, not because any new query failed.
- This pass performed two read-only source-closure audit executions over the same 575 paths (initial hash loop and reproducible auditor). It did not launch any method producer, IVP solver, proof replayer, common predicate, stage, retry, query or batch.
- No selected confirmation IDs, comparison inputs, output rule or resource profile were frozen. The 1,944-query Auer universe was not run or expanded. Historical legacy R5 remains `800/800 NOT_RUN`.

## Artifact ledger and exact reproduction

New files, all under G4-owned W2 prefixes:

1. `docs/reviews/autonomous_w2/g4/AUDIT_CHECKLIST_AND_SOURCE_CROSSWALK_v1.md` — source/equation map, C1–C12 audit checklist, endpoint derivation and literature limits.
2. `validation/autonomous_w2/g4/audit_source_closure.py` — read-only rehasher for project-contained source-closure manifests.
3. `coordination/autonomous_w2/g4/PEER_AUDIT_INPUT_v1.md` — direct file request for exact release/task/proof inputs from G2.
4. `coordination/autonomous_w2/g4/RELEASE_AUDIT_STATE_v1.json` — explicit no-release decision state; no candidate decision is implied.
5. This consolidated handoff.
6. `coordination/autonomous_w2/g4/STATUS.json` — updated W2 ownership, artifact hashes, environment, counts and next action.

Reproduce the read-only R19 closure audit from the repository root:

```powershell
python validation/autonomous_w2/g4/audit_source_closure.py --root . --manifest research/benchmarks/G4_AUER_MATCHED_SOURCE_CLOSURE_v3_R19_PROSPECTIVE.json
```

Expected structured result: `declared_dependency_count=575`, `verified_count=571`, `issue_count=4`, `result=MISMATCHES_FOUND`, with the four paths listed in Finding 3. The auditor reads but does not alter the manifest or source tree. No fixture or solver command was run in this turn.

## One next scientific decision

**When G2 publishes its first immutable W2 candidate, decide whether its signed, parameter-aware time-local bound changes the predeclared common safety-plus-progress task action set versus R3 and the Auer reconstruction under equal W2 resource limits.** If there is no exact proof or no task/threshold independently anchored before outcomes, do not run comparison; classify the tested candidate as lacking a supported contribution on that scope and finish the package with that limitation.

## Final gate disposition

**HOLD. G1 PASS only for the restricted reduced-model scope. G2/G3/G4 and physical-platform correspondence remain UNVERIFIED.** This handoff is not an acceptance of G2's candidate or a G4 PASS. G3 recursive safe-set/policy construction, operational control, hardware correspondence and final paper review remain separate work. No commit or push was made.
