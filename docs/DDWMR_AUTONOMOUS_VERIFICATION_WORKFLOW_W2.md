# DDWMR — autonomous G2/G4 verification workflow W2

**Adopted:** 2026-10-07, from the owner's instruction: “ok vậy làm rỏ các đầu việc cần thực hiện để hoàn thiện, từ giờ tôi muốn 2 luna max tự đảm nhiệm 2 đầu việc kiểm chứng chứ không cần đợi bạn nữa”.

**Authority:** MASTER plant v2.1; workflow W2 extends W1. **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.**

## 1. Objective and autonomy

Two existing **Luna max** sessions own complete verification packages, including research, implementation, proof checking, routine corrections, versioning, bounded offline evaluation and a final scientific disposition. They do not return merely because a preflight is prepared or another routine Codex approval would previously have been needed.

| Session | Primary responsibility | Completion product |
|---|---|---|
| `DDWMR | LUNA-G2-SCOPE` | Sound and useful one-hold enclosure/action evidence | Proof, implementation/checker, feasibility analysis, reproducible development evidence and a qualified conclusion |
| `DDWMR | LUNA-G4-AUER` | Independent audit, prior-art falsification and matched comparison | Source crosswalk, adversarial replay, frozen comparison results and a defensible contribution verdict |

The owner starts/continues these sessions with the two linked assignments. Codex does not launch or message execution agents. The sessions exchange artifacts directly through this repository; the owner need not relay every correction. No browser automation or external messages are involved.

**No new Codex GO is required for ordinary G2/G4 work covered here.** A freeze/release receipt is an evidence record produced by the responsible Luna, not a request for permission. Final gate acceptance and any change to scientific assumptions remain separate from validation execution.

This supersedes earlier per-iteration instructions to wait for Codex review/GO for the same G2/G4 scope. It does not erase mathematical blockers, failed runs or historical authorization receipts. Old R5/800 and Auer/1,944 manifests and their counts remain unchanged; new work has a new namespace and denominator.

## 2. Scientific boundary and current evidence

Read AGENTS and all four canonical context files first. Work only in `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`.

- Nine-state reduced model, winding-terminal voltage, one common voltage during each hold, fixed hidden labels for the complete execution, static circular obstacle, full-hold collision and contact admissibility.
- A known clip-law subclass and explicit synthetic parameters may be used. State the supported subclass; do not imply all MASTER laws/configurations are implemented.
- Theoretical synthetic benchmarks are authorized. Luna may specify their task, domain and success rule prospectively without requiring hardware data from the owner. Such choices establish a formal benchmark, not physical/practical provenance.
- Keep G3 construction, operational control, closed-loop and hardware work outside these packages. Report a specific proposal if they become necessary.

Current evidence: Cases A/B/C accepted narrowly; R3 has 1,944 records, 1,196 CERTIFIED and 748 proof-complete UNKNOWN. R5 remains 800/800 NOT_RUN. The selected ten-pair Auer pilot has Auer 9 certified versus R3 6; this is adverse evidence for an R3 coverage claim, not universal dominance. G2 R21 refutes the strong R17 task target; R22–R24 provide only a narrow synthetic ranking lemma. R26 CommonRoad does not fit unchanged G2. Generic predictor/validation, parameter augmentation and paired-IVP expressibility are established methodology.

Use [the progress checkpoint](reviews/CODEX_DDWMR_SCOPE_PROGRESS_VERIFICATION_2026_10_07.md) and its linked reviews. Preserve their scientific qualifications.

## 3. File ownership and exchange

Both sessions stay in the existing working tree. Do not switch branches, reset, clean, commit or push. Do not modify canonical context, historical artifacts, the peer's sources or their snapshots. Copy a required legacy module into your own package before changing it; record its origin and new dependencies.

| Owner | Writable new prefixes |
|---|---|
| G2 | `research/autonomous_w2/g2/`, `validation/autonomous_w2/g2/`, `results/validation/autonomous_w2/g2/`, `docs/reviews/autonomous_w2/g2/`, `coordination/autonomous_w2/g2/` |
| G4 | Corresponding five prefixes ending in `g4/` |

Each owner creates `coordination/autonomous_w2/<owner>/STATUS.json` at start. Publish immutable, versioned release manifests alongside it and update STATUS atomically. Record: workflow/session, phase, sequence/version, UTC time, current objective, artifact paths and SHA-256, exact peer release consumed, next action and any blocker. Use phases `ACTIVE`, `PUBLISHED`, `REVISION_REQUIRED`, `AWAITING_PEER_INPUT`, `FINISHED`, `OWNER_DECISION_NEEDED`.

A release binds the actual claim/proof, supported model, protocol, exact ordered IDs, source closure, arithmetic/resource profile and verification evidence. Hash executable scientific dependencies and the specifications they implement; an unrelated prose edit need not invalidate a scientific snapshot. No claim of a release existing before files and checks exist.

Read the peer's STATUS/releases to find work. G4 writes audit decisions in its own namespace, explicitly binding the G2 release hash. G2 consumes the decision, corrects its own package and publishes a new version. Never silently update a frozen release in place.

If peer input is unavailable, continue independent proof, fixtures, source audit or baseline preparation. Mark the dependency clearly. Do not busy-poll: check at work boundaries; a wait may be at most 30 seconds. Do not end the package just because peer work is in progress.

Use one exclusive repo-local compute lock at `coordination/autonomous_w2/COMPUTE.lock` for substantial numeric runs. Acquire it atomically and record owner/process/start time. Release only your lock; recover a stale lock only after establishing that its owning process is no longer running. Mathematical writing/source audit can proceed concurrently. Matched timing runs are sequential so the other session does not distort timings.

## 4. Work sequence without routine Codex intervention

1. **G2 develops a concrete candidate.** Screen task feasibility analytically; derive a signed/coupled actuator-contact enclosure and endpoint progress certificate. Show the exact proposed effect beyond R3. Treat a failed task as a scientific finding, not a reason to move its threshold after observing results.
2. **G4 audits it independently.** Check derivation, quantifiers, arithmetic, code mapping, checker independence and primary-source overlap. Classify soundness separately from novelty. Publish exact defects or `ACCEPT_FOR_SCOPED_VALIDATION` for the bound release.
3. **Both correct routine defects directly.** Preserve failed evidence. Stop certificate use only on an affected unsound path. A revised source/profile must be bound and rechecked before it runs; do not merely change stale pins to bless unknown code.
4. **G2 performs bounded development.** Every development configuration is hashed before its outputs. Native queries, fixture executions and arithmetic checks have separate counts. Debugging attempts remain visible and cannot become untouched confirmation data.
5. **G4 freezes and runs matched confirmation.** G4 controls the final workload, comparison rule and both frozen producers. G2 supplies its released producer and may independently replay resulting proofs; it does not separately evaluate the same held-out inputs before the matched run.
6. **Each returns its consolidated scientific disposition.** Proceed to the end of the package rather than stopping after every manifest/preflight correction. A counterexample or scoped negative result is a legitimate terminal result; it is not a successful contribution.

Independent checking must recompute inclusion/coverage, not trust an exported `CERTIFIED` label. Disclose shared model/arithmetic code. Two agents agreeing is not proof. A peer audit can accept a finite path for validation while G2/G4 gates remain UNVERIFIED.

## 5. Bounded work and freeze rules

First-cycle limits prevent another open-ended sequence of engineering preflights:

- Investigate at most **three explicitly recorded candidate hypotheses**. Choose the first concrete hypothesis in the G2 assignment; alternatives need a reason and separate evidence.
- At most **24 native development attempts for G2** and **12 smoke/development attempts per method for G4** in this W2 cycle. All attempts consume the allowance, including failures, retries and resource limits. Fixtures with known analytic expectations are separate and must not contain hidden benchmark evaluations.
- First confirmation: at most **eight task groups × three actions = 24 action rows per method**, using positive-width moving-state/parameter domains. Include zero, declared nominal and one declared alternative action, with actual values fixed in the protocol. G4 freezes the exact unused inputs/IDs before either producer sees their outcomes. Disclose the already observed development domain; do not call a small scene split independent statistical sampling.
- Per numeric worker and per replay/audit: **60 s wall cap and 1 GiB memory**. Each development or confirmation phase: **2 h wall cap**, including setup and replay. Profiles also predeclare arithmetic/operation/precision limits. Both methods use the same top-level resource envelope; internal approximation orders need not be identical and must be disclosed.
- Use smaller limits when adequate. No selective relaxation for difficult confirmation rows. Report proof-complete UNKNOWN, resource UNKNOWN, invalid/unsupported, execution/audit failure and NOT_RUN separately, preserving every denominator.
- Freeze task/threshold, model, common collision/contact/progress target, workload, sources, profile and primary cost/coverage criterion before confirmation. Do not set a task threshold from the computed action-gap interval or place an obstacle between observed certificate radii.
- A bug discovered during confirmation terminates that confirmation phase. Keep its outputs as interrupted/development evidence. Correct the bug and report the remaining readiness; do not recycle these inputs as pristine confirmation or silently reset the cycle's allowance.

These are finite offline research limits, not an online robot deadline or claimed operating requirement. At a limit, finish with the actual partial/negative finding and a concrete next proposal. Do not expand to the old 800/1,944 universes automatically.

## 6. Completion and scientific claims

G2 must determine whether a sound enclosure can certify a useful action on the declared formal task; G4 must determine whether the proposed effect is distinct from applicable generic methods and survives matched evaluation. Comparison can assess tighter useful bounds, certified action coverage, and computation/proof cost. Choose one primary hypothesis before outputs. Smaller proof files alone do not establish usefulness or novelty; a resource claim requires an independently justified binding budget.

Final joint recommendation: `ADVANCE_CANDIDATE`, `REVISE_METHOD`, `NO_SUPPORTED_CONTRIBUTION_ON_TESTED_SCOPE`, or `OWNER_DECISION_NEEDED`. These are package dispositions, not gate PASS or manuscript-ready decisions. Negative results are limited to the studied hypotheses/domain.

Owner input is needed only for a genuine scientific-scope/model change, G3/operational/hardware work, or extension beyond the stated cycle limits. Routine code corrections, synthetic task design, source inspection, freezes and covered offline runs do not require another permission request.

Create final, self-contained Markdown handoffs:

- G2: `docs/reviews/autonomous_w2/g2/LUNA_TO_CODEX_G2_AUTONOMOUS_W2_FULL_HANDOFF.md`
- G4: `docs/reviews/autonomous_w2/g4/LUNA_TO_CODEX_G4_AUTONOMOUS_W2_FULL_HANDOFF.md`

Include equations/assumptions, all changed files, commands, evidence/failed attempts, hashes, full counts, exact reproduction instructions, peer-release/audit bindings, limitations and the next scientific decision. Use Finding / Evidence / Consequence / Status / Required action for disputed claims. Conclude with HOLD and the unchanged gate statuses.

**Chat responses contain exactly three short lines:**

`Session: DDWMR | LUNA-G2-SCOPE` (or `LUNA-G4-AUER`)

`Status: <DONE / PARTIAL / NEGATIVE / OWNER_DECISION_NEEDED>; <one factual result>`

`Handoff: <absolute Markdown path>`

## 7. Assignments and future paper milestones

- [G2 assignment](CODEX_TO_LUNA_G2_AUTONOMOUS_COMPLETION_W2.md).
- [G4 assignment](CODEX_TO_LUNA_G4_AUTONOMOUS_COMPLETION_W2.md).

The full paper still needs a defended G2/G4 result, a useful recursive G3 construction/policy, and final manuscript/figures/review. W2 completes the two immediate verification packages. G3 is a subsequent separately assigned scientific stage; no automatic manuscript or real-robot safety claim follows.
