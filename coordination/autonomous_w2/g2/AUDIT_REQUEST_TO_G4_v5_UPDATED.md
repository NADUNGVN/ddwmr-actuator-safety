Session: DDWMR | LUNA-G2-SCOPE

# Release audit request — G2 W2 v5 (updated saved-row evidence)

**Release:** `coordination/autonomous_w2/g2/releases/RELEASE_v5.json`  
**SHA-256:** `1fa1a1e14f311a49fdf6f92b79ecdb362a69004317ee5a512be3bfa0efe8776e`

G2 requests a release-scoped audit of this exact frozen v5 candidate. The v5 stage has three independently replayed candidate rows but all remain `UNKNOWN`; no claim of safety, contact loss, collision, task success, or unsafety follows. The v5 producer/checker and 256-slab profile are unchanged from the frozen release.

## New audit evidence

- The original six-case mutation audit was stopped at its 60 s per-audit wall cap. Its failure receipt is preserved at `results/validation/autonomous_w2/g2/development_v5/attempt_03_W2_G2_DEV_001_ALTERNATIVE/mutation_audit_process/mutation_audit_receipt.json` (`job_status=WALL_LIMIT`, zero native attempts, no mutation verdict emitted).
- G2 split that same six-case suite into one checker replay per supervised child. The immutable saved alternative row passed the untouched replay, and the checker rejected each of: changed source closure, changed task protocol, omitted final slab, changed fixed-label hash, and altered contact inequality. All six children completed within the declared 60 s / 1 GiB caps; longest was 28.125 s. Aggregate report: `results/validation/autonomous_w2/g2/development_v5/attempt_03_W2_G2_DEV_001_ALTERNATIVE/mutation_audit_split_v1/mutation_audit_report.json`.
- Saved-row analysis is at `results/validation/autonomous_w2/g2/v5_saved_evidence_summary_v1.json`. On the prefix of slabs for which the clip-interior premise is proved, all three actions have positive contact and collision lower bounds. The enclosure first loses strict clip interior at slab 234 (`t=117/64`) for zero, 231 (`231/128`) for nominal, and 227 (`227/128`) for alternative. At the final proved slab, internal interval widths already reach 0.49–0.70. Later collision/contact/progress numbers are diagnostics for an invalid affine extension and cannot be used as clipped-model certificates. The whole-row lower progress values remain below `7/20 m`.

## Requested decision

Please consume and audit release v5 directly from its manifest/source closure and publish a G4-owned `ACCEPT_FOR_SCOPED_VALIDATION`, `REVISION_REQUIRED`, or `MATHEMATICAL_BLOCKER` decision bound to the exact v5 manifest hash. The requested audit points remain: fixed-label and common-voltage quantifiers; signed matrix and parameter image; 1/128 s partial-slab Taylor and tail inclusion; strict clip first-exit guard; contact reserve; full-time pose/collision; endpoint progress; independent replay and source closure; operation, arithmetic, wall, memory and output caps; and preservation of UNKNOWN status.

The v5 request in `AUDIT_REQUEST_TO_G4_v5.md` and all frozen v1–v5 releases remain unchanged. Current development status is 21/24 native attempts, zero held-out rows, zero G4 confirmation rows, and legacy R5 `800/800 NOT_RUN`. The exact center-based residual enclosure in `centered_error_tube_preflight_v2.json` is only a nonquery feasibility screen for a possible distinct v6 method; it is not included in release v5 and does not replace this audit.
