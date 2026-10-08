# G2 task and operating-domain inputs

R22 proves an exploratory synthetic progress gap of about 0.108 mm on a very narrow state/parameter cell. To test whether a voltage choice matters for a task, specify the task **without using that computed interval to choose its threshold**. Unknown fields may be marked `unknown`.

1. **Task:** desired direction, minimum displacement or other success measure, and time limit/hold duration. State the units and why this threshold matters.
2. **Initial operating domain:** expected intervals for pose, body speed/yaw rate, both wheel rates, and both currents at a decision time. State how those intervals are obtained.
3. **Actuation:** allowed terminal-voltage range and any admissible held actions; identify whether `V=0` is a closed zero-voltage RL condition on the intended driver.
4. **Scene:** obstacle positions, robot footprint/clearance radius, and whether the obstacle can move during the hold.
5. **Model data:** intervals and sources for mass, yaw inertia, wheel radius/track, motor inertia/damping, resistance, inductance, torque/back-EMF constant, known traction shape/scale, and effective per-wheel contact capacities. State known correlations; parameters must remain fixed for each formal execution.
6. **Claim scope:** theoretical reduced-model benchmark or a named physical platform. A physical-platform safety claim additionally needs support/contact and driver evidence or a certified model-error bound showing that the actual trajectories are included.
7. **Cost target, if relevant:** computation platform, update rate/deadline, and the baseline and cost metric to compare.

The first four fields are enough to begin task-focused screening if the model parameters are provisionally synthetic and explicitly labeled as such. No G2/G3/G4 gate changes follow from filling this form.
