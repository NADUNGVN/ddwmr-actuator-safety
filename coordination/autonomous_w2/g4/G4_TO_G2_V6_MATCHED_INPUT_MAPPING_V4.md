Session: DDWMR | LUNA-G4-AUER

# Final G4-to-G2 semantic check before the bounded matched comparison

The owner explicitly instructed G4 to compare v6 with Auer on the same task, at most three actions each, replay the evidence and report a conclusion. G4 treats this as the W2 matched-task **development falsification** using the same three G2 inputs already observed by G2. They are not fresh confirmation or held-out data. G2 remains at 24/24 native attempts; it must not run a producer.

## Final input and replay evidence

- Frozen-candidate protocol: `research/autonomous_w2/g4/matched_v6_task_development_v2/protocol_v2.json`, SHA-256 `262bde676e676fa10763295f329ae0134daa2264919e33156dcd3abd758d8ecc`.
- Common benchmark: `research/autonomous_w2/g4/matched_v6_task_development_v2/benchmark_v2.json`.
- Three-action mapping: `results/validation/autonomous_w2/g4/matched_v6_task_development_v2/mapping_preflight_v3.json`.
- All path/hash pair check: `results/validation/autonomous_w2/g4/matched_v6_task_development_v2/binding_preflight_v4.json`.
- Final read-only G2 proof replay: `results/validation/autonomous_w2/g4/matched_v6_task_development_v2/saved_replay_preflight_v8.json`.
- Auer case files and bindings: `research/autonomous_w2/g4/matched_v6_task_development_v2/auer_native_inputs/`, `auer_input_manifest_v2.json`, `auer_bindings_v2.json`.
- Semantic adapters/scorer: `validation/autonomous_w2/g4/v6_w2_adapter_v2.py`, `auer_w2_adapter_v2.py`, `matched_v6_common_v2.py`.

The action bijection is zero `(0,0)`, nominal `(1/2,1/2)`, alternative `(1,1)`, each paired to its exact G2 development row. Each carries the full nine-state positive-width initial box, twelve independent fixed labels `[0.9999,1.0001]`, clip law, 2 s hold, inflated static circle and `7/20 m` progress threshold. Only task-eligible action coverage is the primary criterion; margin, enclosure width and offline cost are descriptive. This is a three-action development comparison, not statistical evidence.

G2 may inspect the protocol and adapters directly and send a concrete semantic defect into `coordination/autonomous_w2/g2/`. G4 will record any response found at freeze time; routine peer review does not delay the bounded run. Do not edit G2 sources, releases, saved rows or STATUS.
