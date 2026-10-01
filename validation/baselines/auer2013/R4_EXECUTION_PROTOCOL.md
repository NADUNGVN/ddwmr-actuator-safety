# R4 frozen run protocol

The `max_rhs_jacobian_evaluations_per_ivp` cap is enforced as one combined count
across the producer, independent native replay, and every proof tamper replay.
The worker reserves each evaluation before starting it and records per-stage and
combined counts, including partial checker failures. The common collision/contact
predicate does not evaluate the RHS/Jacobian and is counted separately.

The memory probe applies a separate 64 MiB Job Object limit and retains a
requested 256 MiB in 1 MiB chunks. It passes only when the worker reports a
graceful `MemoryError` after the cap is approached and Job Object peak usage is
between 75 percent of the cap and the cap itself.

Run from the project working tree using the exact source in `results/validation/g4/auer2013/source_snapshot_v10/project`. Output paths stay outside the frozen snapshot.

```powershell
$snapshot = 'D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety\results\validation\g4\auer2013\source_snapshot_v10'
$project = Join-Path $snapshot 'project'
$manifestHash = (Get-FileHash -Algorithm SHA256 (Join-Path $snapshot 'snapshot_manifest.json')).Hash.ToLowerInvariant()
$python = 'C:\msys64\ucrt64\bin\python.exe'
$results = 'D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety\results\validation\g4\auer2013'

# Verify Job Object process-memory enforcement before any IVP.
& $python -m validation.baselines.auer2013.process_limiter --project $project --probe --probe-limit-mib 64 --probe-allocation-mib 256 --guard-output (Join-Path $results 'r4_memory_enforcement_probe_v3.json') --stdout-output (Join-Path $results 'r4_memory_enforcement_probe_stdout_v3.log')

# Execute the analytic fixture first under the frozen v2 limits.
& $python -m validation.baselines.auer2013.process_limiter --project $project --profile (Join-Path $project 'validation\baselines\auer2013\small_case_resource_profile_v2.json') --case analytic --snapshot-manifest-sha256 $manifestHash --proof-output (Join-Path $results 'r4_analytic_fixture_native_v2.json') --evidence-output (Join-Path $results 'r4_analytic_fixture_evidence_v2.json') --guard-output (Join-Path $results 'r4_analytic_fixture_resource_guard_v2.json') --stdout-output (Join-Path $results 'r4_analytic_fixture_stdout_v2.log')

# Run only if the analytic native proof independently replays and its exact reference is contained.
$analyticEvidence = Get-Content -Raw (Join-Path $results 'r4_analytic_fixture_evidence_v2.json') | ConvertFrom-Json
if ($analyticEvidence.status -eq 'PROOF_COMPLETE_AND_REPLAYED') {
  & $python -m validation.baselines.auer2013.process_limiter --project $project --profile (Join-Path $project 'validation\baselines\auer2013\small_case_resource_profile_v2.json') --case ddwmr --snapshot-manifest-sha256 $manifestHash --proof-output (Join-Path $results 'r4_ddwmr_single_query_native_v2.json') --evidence-output (Join-Path $results 'r4_ddwmr_single_query_evidence_v2.json') --guard-output (Join-Path $results 'r4_ddwmr_single_query_resource_guard_v2.json') --stdout-output (Join-Path $results 'r4_ddwmr_single_query_stdout_v2.log')
}

# Verify the source snapshot after each completed run. Never run the 1,944-query batch here.
& $python validation\scripts\verify_auer_source_snapshot_v10.py --snapshot $snapshot --output (Join-Path $results 'source_integrity_post_run_v10.json')
```

Do not change the profile, precision, approximate path, input, action, or inclusion criteria after observing output. Every failed step and accepted step remains in the proof/attempt records. The 1,944-query matched batch is outside this package.
