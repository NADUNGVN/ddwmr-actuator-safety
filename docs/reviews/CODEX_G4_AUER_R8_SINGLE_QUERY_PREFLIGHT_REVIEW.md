# Codex review — G4 Auer R8 stopped single-query preflight

**Date:** 2026-10-03  
**Lane:** `LUNA-G4-AUER`  
**Input:** `LUNA_TO_CODEX_G4_AUER_R8_SINGLE_QUERY_FULL_HANDOFF.md` and `protocol_v3_r8_single_query_preflight_v1` ledger/receipt.  
**Authority:** MASTER v2.1. **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.**

## Decision

**ACCEPT the `STOP_NOT_RUN_PRECONDITION_HASH_PIN_MISMATCH` disposition.** The conditional R8 one-query authorization in `CODEX_G4_AUER_PROTOCOL_V3_R8_SOURCE_REVIEW.md` was not consumed because its pre-run identity condition failed. Both method arms remain `NOT_RUN`; the matched count remains **0/1,944**. **NO-GO for query 1 or batch on R8.** A versioned corrected candidate needs another review before either worker is invoked.

The earlier Codex R8 review checked outer file hashes and the 214 dependency hashes but missed the semantic cross-file pins inside the active profiles. That omission is corrected here. I did not invoke a worker, producer, common audit or query and did not modify G2 or existing R8 candidate/evidence bytes.

## 1. Five guard-profile pins are stale

**Finding.** The R8 guard profile's own SHA-256 matches the candidate, but five of its embedded source pins do not match the files they name.

**Evidence.** Independent SHA-256 comparison of each `source_path/source_sha256` pair in `g4_equal_resource_guard_v3_r8.json` reproduces Luna's five differences:

| Active source | Profile pin | Current file / R8 manifest |
|---|---|---|
| Auer worker | `f75646cb2cb0d6fbb064ce02257c9d0dbe5412095ebd83a05f231901796063c9` | `c81d80e58446107a429c3fbd76b1db514f790e5876b901632adc097da82569c2` |
| R3 worker | `5c6efc03b57de1115fa391b8a69b192756500b1a996853fe4a762a1af9cf4e61` | `b633344c2e76e42f80367d70599603b4fc90815b777c6ca7ce4d543e347c5f61` |
| Shared binding | `922b436e6eccccf9fb46c9d5f67fc63ac46462b6b057b3df83cdba2d38d52004` | `9331cc64b969bb05acae8de73f2e74458a98bc541420a65e5e388b662d0e1ca8` |
| Result validator | `fc52c866df453d5652117324ea7c421fd09ef9786c697bc994080015e2266ca6` | `5305cfb88e1e37c6a8491e4f9c3e6af248c919635712922d3ceb69e8bb250cf4` |
| Worker launcher | `95e0d3b8396483f789784bb3565456344887ba01cab865cf8262d2a8e228eb5d` | `040709b0ea85c265b4cd07c12f594de19badb24bbea1bf728abc57aeef65da85` |

The declared values equal the **R6** active-source hashes; they were carried into R7 and R8 profiles. The process-limiter and Python executable pins in the guard profile match their named files. The current five source hashes match the R8 closure and candidate manifest. Thus the mismatch is stale embedded metadata in a hash-locked profile, not evidence that the source files changed after R8 was built.

**Consequence.** Whole-file hash consistency does not establish that a profile's internal source declarations are true. The declared guard/source identity for a run would be contradictory.

**Status.** **CONFIRMED provenance blocker.**

**Required action.** Repair these pins in a new versioned profile/candidate, and add a builder/preflight check that fails when any active path/hash pair disagrees. Preserve the R8 profile and manifest bytes.

## 2. A sixth active pin is stale in the Auer profile

**Finding.** An independent scan of all four active R8 profiles found one additional mismatch outside Luna's five-field guard check.

**Evidence.** `auer_g4_matched_profile_v3_r8.json` declares `matched_worker.versioned_solver_path=validation/baselines/auer2013/residual_ivp_g4_matched_v3_r8.py` and `versioned_solver_sha256=4add47d63ddfb513f3a59038a948ccf60fed4783caea18990d284bf149c1766d`. The named R8 solver actually hashes to `9ec23ccfe59b8e08ea54061a20f50501dd35a1a136c561347d38ff0ae5e56717`, which is also the R8 manifest/closure identity. The declared hash is the correct hash of the **R7** solver. The active R3 and common-predicate profiles showed no other local path/hash pairs in this scan. In total, six of the eight checked active profile pins mismatch: five guard source pins and one Auer solver pin.

**Consequence.** Updating only the five guard fields would leave the candidate internally inconsistent. Changing the Auer profile also changes its profile hash and potentially prospective query/input bindings, so all dependent identities need rebuilding.

**Status.** **ADDITIONAL CONFIRMED provenance blocker.**

**Required action.** Correct the Auer solver pin in the same new version. Audit every active path/hash pair, including executable and process-limiter references, and publish the machine-readable check result with the candidate.

## 3. Closure and stop evidence

**Finding.** Luna's stop was timely and the remaining checked R8 identities are intact.

**Evidence.** The handoff and ledger report 214/214 closure dependencies matching, the ordered 1,944-ID digest matching, the first-ID method inputs reconstructing in memory, and no worker/producer/audit calls. I recomputed the ledger SHA-256 `bb3c8554227425c8e50bc6a88b8673c3a8d625ffa2bc5398c8195b87244c014a` and receipt SHA-256 `6143710f0a0341b9e52d7ea1e9a37b47fc0cdc65f828f29f043899646e550336`. The receipt records zero matched evaluations and a precondition stop. The R8 guard profile itself remains the exact byte string bound by candidate manifest `263305153edd39b60110e1a275956391dd19da4ba2ee339c6cf53c4d31c3bb86`.

**Consequence.** No query result, performance comparison, safety certificate, or novelty evidence was lost or gained. R8's earlier focused RHS-accounting source correction remains accepted in its archived-fixture scope; the R8 package as a whole is not ready for a live run.

**Status.** **VALID stop evidence; query 1 NOT_RUN.**

**Required action.** Keep the R8 ledger, receipt, candidate and predecessor bytes as historical evidence. Do not describe the conditional authorization as a completed query.

## 4. Next review boundary

**Finding.** This is a versioned source/provenance correction, not a plant or mathematical-method amendment.

**Evidence.** All six mismatches concern references from active profiles to exact source bytes. The R8 builder hashes the profiles and dependencies but does not reject false path/hash assertions embedded in those profiles. A new profile hash and source closure will change downstream proof/input/fixture/probe bindings even if the mathematical formulas and frozen 1,944-ID order remain unchanged.

**Consequence.** A corrected candidate must be built and reviewed as a new version. The R8 single-query permission does **not** automatically transfer to that version.

**Status.** **RETURN FOR VERSIONED CORRECTION; NO-GO query 1 and batch.**

**Required action.** `LUNA-G4-AUER` should prepare an R9 review candidate with an executable active-pin integrity check, regenerated source closure/import audit, prospective input hashes, fixture/probe bindings and manifest. Keep all 1,944 rows `NOT_RUN` and all historical R8 artifacts unchanged. Submit a full Markdown handoff for independent review before any worker invocation.

## Vietnamese decision summary

Luna dừng đúng trước query 1. Ngoài năm hash cũ trong guard profile, tôi xác nhận thêm hash solver R7 bị giữ trong Auer profile R8. Vậy R8 có **sáu pin nội bộ sai** dù 214/214 hash file trong closure đều khớp. Cần `LUNA-G4-AUER` tạo candidate R9, tự động kiểm tra mọi cặp đường dẫn/hash đang hoạt động, dựng lại toàn bộ binding và gửi review; chưa chạy query nào. G4 vẫn UNVERIFIED, toàn dự án HOLD.
