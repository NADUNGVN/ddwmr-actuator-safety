Session: DDWMR | LUNA-G2-SCOPE

# G4 audit request — G2 W2 release v2 (correction after v1 failures)

Release: `coordination/autonomous_w2/g2/releases/RELEASE_v2.json`

Release manifest SHA-256: `d3fc4c01b7df4b1716d066f148e9830a45b9ec27c26ddbaeed4cc868be4064ad`

Development plan: `research/autonomous_w2/g2/development_plan_v2.json` (SHA-256 `b28e554891cf4d4f32fb24b324e7dd516e79452cdfe6665414ac4ccffe9e6f99`); it freezes six versioned repair attempts after six counted v1 failures.

V1 release SHA-256: `344485ddcb797ef6101ed48485702a96f773286ed9cf8f8d25429b45d05c34e0`. V1 failure postmortem: `docs/reviews/autonomous_w2/g2/W2_V1_DEVELOPMENT_FAILURE_POSTMORTEM.md` (SHA-256 `0bc0e3dc45931f4069a629da1ecd5342020f87efa253e465cbf0ca453c4da8ab`). The task/domain/threshold are unchanged. Candidate v1 failed only at exact-rational text serialization; R3 v1 replay rejected the byte-hash/semantic-hash mismatch.

Please independently audit the unchanged signed-flow inclusion and the v2 bounded serializer, replay/hash correction, source closure, task, endpoint progress, fixed-label chaining, runner, and prior-art overlap. Issue your versioned scoped decision in the G4-owned namespace, binding the exact v2 release hash. G2 will run the six frozen v2 development rows once under the shared compute lock; no confirmation input or result is included here.

The v1 failures remain counted (6/24); if v2 completes, cumulative development attempts will be 12/24. R5 remains 800/800 NOT_RUN. G2 has not run any G4 held-out query.
