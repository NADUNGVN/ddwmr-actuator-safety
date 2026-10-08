# Codex review — G4 Auer matched protocol v3 R7

**Date:** 2026-10-03  
**Lane:** `LUNA-G4-AUER`  
**Input:** `LUNA_TO_CODEX_G4_AUER_PROTOCOL_V3_R7_PROFILE_CORRECTIONS_FULL_HANDOFF.md`  
**Repository:** `main`, inspected HEAD `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`  
**Disposition:** **PARTIAL; new RHS-accounting blocker.** No matched query is authorized by this review.  
**Research state:** **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.**

I read `AGENTS.md` and all four canonical `research_context/` files. This review used source reads, exact-byte artifact hashing, and one **read-only replay of the archived Auer proof**. I did not invoke a producer, matched worker, query 1, or the 1,944-query batch; I did not commit or push. The completed `LUNA-G2-SCOPE` lane has its separate Codex review.

## 1. R7 identity and restricted fixture evidence

**Finding.** The R7 candidate and reported non-query fixture have the declared byte identities.

**Evidence.** I recomputed SHA-256 for source closure `48006dcd4d1e1491e4cade78cf1fff4e895cebf30400764cbf384459f8fdbf9f`, manifest v7 `181dfad5ef58088fb192449ff8ebb31546c41dfb57c2d8a3e0768f78511ddc82`, fixture report `1a6b1c1a73bb103eba46ea1c27e3f3be7e0e7a1aa4f9b6644d69385ad2526d99`, and fixture guard `0c3415ef10ebf1af0569af94dfeef3eda6b7f4001ab395a1a71474d26693b40d`. All **120/120** source-closure dependency hashes match present files. Manifest v7 states 1,944 unique ordered rows, all `NOT_RUN`, `matched_query_evaluations=0`, `comparison_run=false`, `query_1_authorized=false`, and `batch_start_authorized=false`. The fixture report records archived proof composition and 13/13 expected mutation rejections; it is not a prospective worker result.

**Consequence.** The R7 artifact set is reviewable and its stored fixture evidence has a stable identity. No matched-method outcome exists yet.

**Status.** VALID for the exact-byte checks and the reported non-query scope.

**Required action.** Keep R7 and preceding versions byte-identical during correction.

## 2. R3 serialized-proof cap correction

**Finding.** The missing R6 profile key is present and the R7 R3 serialization path uses a finite profile cap consistently in the inspected source.

**Evidence.** `r3_g4_matched_profile_v3_r7.json` declares `max_serialized_proof_bytes=4,194,304` and the identical internal cap. `r3_matched_query_worker_v3_r7.py` checks both before the producer call, records the cap, and routes `OutputSizeLimitError` to `RESOURCE_LIMIT`. `matched_worker_common_v3_r7.py:90-103` computes the exact UTF-8 serialized byte count before writing; the size comparison is strict `>` so equality is admitted. The R7 schema and validator require/bind the cap, and the offline composition verifier checks the stored proof file size. The archived-record fixture serialized 120,847 bytes under the 4-MiB cap, then rejected the same bytes against a 120,846-byte fixture cap without writing the over-limit file. This is evidence about stored data and a helper path; the prospective producer was not called.

**Consequence.** The deterministic R6 missing-key failure is resolved in R7. The archived sizing evidence does not prove that every future native proof fits 4 MiB; an oversized proof is intended to become a resource stop.

**Status.** VALID source/profile/fixture correction in its stated scope; prospective query behavior UNVERIFIED.

**Required action.** Preserve the cap and its resource classification in the next version.

## 3. Auer RHS/Jacobian cap: enforcement repaired, successful accounting wrong

**Finding.** R7 seeds the independent native replay counter with the producer's recorded RHS count, but its **successful** offline audit reads replay counts from the wrong dictionary level. This produces false reported counts and a deterministic mismatch with a successful live worker result.

**Evidence.** `replay_ivp.py:616-629` returns `rhs_jacobian_replay_evaluations` and `rhs_jacobian_combined_count` as **top-level** fields on successful replay. Its nested `work` contains rational-operation fields only. In `verify_matched_composition_v3_r7.py:303-307`, the verifier instead sets nested replay/combined fields from `replay_work.get(...)`, defaulting to `0` and `producer_rhs`. The later `audit_artifact_bundle` live check (`:477-490`) compares these values with `method_native_work_vector`, while `auer_matched_query_worker_v3_r7.py:501-555` records its actual seeded counter after replay.

I independently replayed the unchanged archived Auer proof in memory through the R7 `_replay_auer_envelope` path, with no producer or matched query call. The native replay returned `replayed=true`, **top-level `replay=4`, `combined=8`**, but the verifier's nested `work` reported **`replay=0`, `combined=4`**. The stored R7 fixture report likewise states producer 4, offline replay 0, combined 4. Its boundary test sets the producer count to 100,000, so replay stops before the first RHS call; that test cannot exercise the successful nonzero replay count.

The seeded native replay still enforces its 100,000 combined call cap during actual replay; the defect is in successful-result reporting and the subsequent live equality check. A complete prospective Auer proof with positive replay RHS calls would carry the worker's actual count and be rejected by the offline audit as `RESULT_RHS_ACCOUNTING_MISMATCH` even if the proof and common predicates were otherwise valid.

**Consequence.** R7 cannot serve as the final matched protocol freeze. The successful Auer proof-to-common audit and its RHS work report are not correctly composed. The boundary fixture pass and the two memory-only probes do not resolve this case.

**Status.** **BLOCKER for successful prospective Auer audit, final freeze, and query 1 authorization.** The boundary rejection itself is VALID in its narrow scope.

**Required action.** In a new version, read the successful replay counts from its top-level fields, validate them as nonnegative integers, and verify `combined = producer + replay <= frozen cap`. Match the same numbers to the worker's work vector in the live audit. Add a non-query regression using the archived successful proof that explicitly asserts a **positive** replay count and correct combined total, alongside the existing at-cap boundary test. Rebuild closure, manifest and affected fixture/probe bindings; preserve all R7 bytes.

## 4. Resource and gate boundary

**Finding.** R7's 64-MiB probe commands and archived composition fixture remain separate from method-worker query measurements.

**Evidence.** The handoff reports two memory-probe `PASS` outcomes and zero matched worker/producer calls in the fixture. The candidate manifest remains at **0/1,944** queries. The Auer producer count in a complete proof is still a source-trusted work field: the producer increments its counter before RHS calls in `residual_ivp_g4_matched_v3_r7.py:296-320` and serializes that counter in `proof.work`. The offline auditor can check its declaration and replay budget, but cannot retroactively measure producer calls from a status string alone.

**Consequence.** No query-level runtime, memory, comparative usefulness or novelty conclusion follows. The G2 review does not substitute for this G4 audit.

**Status.** G4 UNVERIFIED; overall HOLD unchanged.

**Required action.** Send the focused correction to `LUNA-G4-AUER`. `LUNA-G2-SCOPE` has completed its separate assignment. Do not run query 1 or the batch from R7.
