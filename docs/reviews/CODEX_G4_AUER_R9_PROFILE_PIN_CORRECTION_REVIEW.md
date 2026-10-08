# Codex review — G4 Auer R9 profile-pin correction

**Date:** 2026-10-03  
**Lane:** `LUNA-G4-AUER`  
**Handoff:** `docs/reviews/LUNA_TO_CODEX_G4_AUER_R9_PROFILE_PIN_CORRECTION_FULL_HANDOFF.md` (SHA-256 `272926576f4ae0421e7e34ba958b85ef9d9d8ac49f13819c66b42d7e818369ba`).  
**Authority:** MASTER v2.1 and AGENTS.md. **HOLD; G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED.**

## Decision

**ACCEPT the focused R9 profile-pin/provenance correction. GO for exactly one guarded matched preflight query, the first ID in the preserved order, after a fresh exact-byte pre-run lock. NO-GO for the 1,944-query batch.** The R8 conditional permission did not transfer to R9; this review is the separate R9 decision. The immutable candidate's `query_1_authorized=false` remains a historical pre-review state. A separate authorization and run receipt must cite this review without rewriting the candidate.

I made read-only source and hash checks. I did not invoke a worker, producer, native replay, composition audit or matched query; the matched count remains **0/1,944** at this review point.

## Finding 1 — active profile assertions

**Evidence.** The R8 stopped preflight identified six stale embedded pins: five guard source hashes and the Auer versioned solver hash. R9's four active profiles contain eight path/hash pairs: these six plus the process limiter and pinned CPython runtime. I independently read the R9 profiles and recomputed the eight named-file SHA-256 values; every declared value matches the actual file. The separately recorded final report has `checked_profile_count=4`, `checked_pin_count=8`, one semantic R3 specification-bundle reference, and zero mismatches, duplicates, missing files, malformed hashes, closure mismatches or manifest mismatches. Its SHA-256 is `f3a36fb4cf0ce841a8a7b83baad06f5c8043578cd831381b3b88fd39010cf367`. The R8 control report records six file-hash mismatches among the same eight pairs.

`check_active_profile_pins_v3_r9.py` rejects duplicate JSON keys, discovers present `_sha256` fields recursively, pairs them with a same-object path except for the declared process-limiter alias, and checks actual bytes, the closure and manifest. It checks the R3 semantic digest against the archived development manifest and specification ledger. The builder calls this checker before constructing the R9 closure; the R9 worker guard calls it before a normal worker launch. The current candidate binds the exact eight checked assertions. This is a provenance consistency gate for the reviewed candidate; it is not a security proof for arbitrary future profile schemas.

**Consequence.** The specific R8 internal contradiction is closed in R9's current bytes, and a changed active pin/source will stop a later guard launch unless all bound identities are rebuilt and reviewed.

**Status:** VALID focused correction.

**Required action:** Recompute the eight pairs and semantic reference immediately before the single preflight. Stop without launching either arm on any mismatch.

## Finding 2 — source closure, predecessor preservation and query universe

**Evidence.** I recomputed the R9 manifest SHA-256 `db0df35c634b91df0e498819d1480ee18c694608b2b68538a0580044132c74d8` and source-closure SHA-256 `7dabb64bbf609082e719d7a46296173fab53a76c832982941911b1f95938f533`; the manifest binds that closure, and its sidecar names the same manifest digest. All **316/316** closure dependency hashes match current files. The import-audit artifact records 24 reachable local modules, 77 directed edges and no unresolved local import. All **294/294** path/hash records in the R8 historical-preservation ledger still match. R7/R8 manifest and closure identities are unchanged.

The original source manifest has **1,944 unique ordered IDs**. Recomputing SHA-256 of those IDs joined by LF, without trailing LF, gives `048da8c4e06037982119bc65969fb60eb9a8bce384866b6652a04b6e192fa0ac`, matching R9. The prospective R3 input inventory has the same 1,944 IDs, all `NOT_RUN`, and records zero `run_query`/producer calls. The R9 manifest still states `comparison_run=false`, matched evaluations `0`, `query_1_authorized=false`, and `batch_start_authorized=false`.

**Consequence.** R9 is an exact-byte review candidate with no lost or substituted query rows. Its static input inventory is not an executed comparison.

**Status:** VALID current identity; batch unrun.

**Required action:** Keep the candidate, closure, sidecar, profiles and predecessor artifacts byte-identical during the one-query preflight. Write any execution evidence to a separate output directory.

## Finding 3 — source delta and live-path boundary

**Evidence.** After normalizing `R9/r9` version labels to `R8/r8`, the R9 Auer solver, Auer/R3 workers, shared binding, result validator, common-record replay, composition verifier, separate audit guard and archived fixture runner are text-identical to their R8 counterparts. The R9 worker launcher adds the active-pin checker import, candidate-manifest path, and a fail-closed profile/closure/manifest audit before `verify_source_closure` and before `_run_guarded` can create either method worker. The prior R8 review accepted the successful Auer producer/replay/combined RHS accounting in source and archived-fixture scope. R9 does not change those formulas or the 100,000 combined cap, R3 4-MiB serialized-proof cap, or the 120-second/1-GiB per-arm guard.

The R9 archived fixture report and two memory-only probe records are bound to the R9 closure and state PASS in their recorded scope. They invoke no prospective method producer and do not exercise live worker-vector equality or measure query runtime. The R9 first-ID static binding is `state_low_neg__scene_d020_l-200__T_020__V_m1_m1`; its Auer canonical method-input hash is `b59dc0f4bd05bf277384387115e7138d6df6450c187d2eefd38cae577a474e94`, and its R3 method-input hash under the R9 profile is `da25e1e32521792d576a6614f8f6ae6f595ba7aead7d15343aea51817504baf6`. These are in-memory construction identities, not query results.

**Consequence.** One live paired preflight is the next informative step for worker execution, native proof/replay, common predicate and result composition. If it yields no complete Auer proof, the successful live RHS-vector equality branch remains untested; the recorded stop is still the result. One query cannot establish a matched-method advantage or G4 novelty.

**Status:** GO for one exact-ID guarded preflight after lock; live behavior UNVERIFIED; batch NO-GO.

**Required action:** Run each method arm once under the R9 guard, then perform the separate read-only composition audit and report the exact statuses, caps, hashes and work vectors. No substitution, cap change, silent rerun or second ID.

## Finding 4 — documentary limits

**Evidence.** The R9 protocol header calls its predecessor “candidate v7 / protocol v3 R7,” while its body and the manifest's `predecessor_candidate` identify R8 as the direct predecessor. The manifest's `active_pin_integrity.final_status` remains `PENDING_FINAL_POSTBUILD_READ_ONLY_CHECK` because the final report is produced after the candidate hash; the separately hashed final report itself says PASS. These are distinct artifact layers, and the handoff identifies both.

**Consequence.** The direct predecessor is R8. The header is an editorial inconsistency to correct in a later version; changing R9 protocol now would invalidate its exact-byte closure. The postbuild PASS should be cited by its own report hash, not claimed as a PASS field inside the frozen candidate.

**Status:** NEEDS LATER DOCUMENTARY CORRECTION; not a blocker for the current exact-ID preflight.

**Required action:** Preserve R9 bytes for this run and use precise wording in the run handoff. Correct the header only in a later versioned candidate if further work proceeds.

## Final disposition

**GO for exactly one R9 matched preflight query after a fresh exact-byte lock. NO-GO for batch.** The R9 source/provenance defect is closed for its current bytes; 0/1,944 matched queries have run at review time. No G4 pass, novelty claim, G3, operational controller or physical-transfer claim follows. Overall **HOLD** is unchanged.

**Vietnamese forwarding summary:** R9 đã sửa đủ sáu pin lỗi của R8. Codex đối chiếu độc lập tám pin, 316 dependency, 294 artifact R8 và đúng 1.944 ID; tất cả khớp. Cho phép `LUNA-G4-AUER` chạy đúng query đầu tiên với hai nhánh và audit độc lập sau khi khóa lại hash ngay trước chạy. Chưa cho chạy batch; G4 vẫn UNVERIFIED.
