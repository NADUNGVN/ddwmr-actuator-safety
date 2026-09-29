# Luna → Codex: G2/G4 validation handoff

**Ngày:** 2026-09-30
**Repo:** `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`
**Branch:** `luna/g2-validation-v1`
**Baseline:** `6956022e93bf7f3d503c9995735cb380162df437` (W1 authorization; working tree sạch trên `main`)
**Môi trường:** Windows PowerShell, Python 3.12.12, standard library; không cài dependency.
**Kết luận:** Bộ kiểm chứng hữu hạn và pilot đã được thực hiện một phần; evaluator và evidence pipeline tồn tại, nhưng 216/216 truy vấn của lần chạy đã sửa đều `UNKNOWN` do trần số bit. Không có certificate replay hoàn tất. Đây không phải G2/G4 PASS; giữ nguyên HOLD.

## 1. Tóm tắt điều hành

Đã đóng băng trước khi chạy benchmark 1.944 query IDs, selection 216 query cân bằng, profile phát triển và hash ledger. Đã triển khai fallback exact-rational cho lớp input hữu hạn `clip(q,-1,1)`, phép bao khoảng, predictor toàn hold độ sâu `n=1`, kiểm tra va chạm/tiếp xúc và checker riêng để replay proof records. Đã kiểm tra riêng 32 bất đẳng thức fixture A/B/C và 21 primitive/input/resource checks. Manifest và kiểm tra record coverage đều qua.

Lần chạy đầu dùng nguồn `d50b8db`; phát hiện dự toán bit tiền xử lý bỏ qua triệt tiêu GCD. Đã sửa phép dự toán, bổ sung kiểm tra hồi quy, sửa cách đếm checker để record resource-limited không bị tính là certificate replay, rồi chạy lại cùng manifest/profile, không đổi giới hạn. Lần chạy thứ hai vẫn cho 216 `UNKNOWN`, tất cả `RATIONAL_BIT_LIMIT`; estimate là 8.265–8.514 bit so với trần 8.192. Không có safety margin, enclosure width hay proof object nào hoàn tất; 1.728 query còn lại là `NOT_RUN`. Kết quả hiện không chứng minh được usefulness trên pilot, cũng không chứng minh query an toàn hay không an toàn.

## 2. Git, quyền và phạm vi

Trước khi sửa, `git status` là sạch trên `main`; HEAD là W1 commit nêu trên. Tạo branch `luna/g2-validation-v1` từ commit đó. Các commit:

| Commit | Nội dung |
|---|---|
| `27f76a2` | Freeze manifest, query selection, profile và pre-evaluation hashes |
| `d50b8db` | Exact-rational G2 fallback, records và checker |
| `add632c` | Sửa dự toán bit/GCD, resource replay accounting, summary |
| `c313c2f` | Lưu nguyên vẹn kết quả chạy đầu |
| `2f32fd0` | Lưu corrected replay, checker, ledgers và hash ledger |
| Báo cáo này | Commit sau khi chốt handoff |

Người dùng đã cho phép validation G2/G4 theo W1; phạm vi này không phải quyền thay đổi plant, gate hay triển khai điều khiển. MASTER v2.1, trạng thái G1/G2/G3/G4, physical correspondence và HOLD không bị sửa. Không làm K_T, controller, G3, closed-loop hay hardware. Không tạo agent hoặc gửi tin cho bên khác.

### Tài liệu đã đọc

- `AGENTS.md`; `research_context/MASTER_RESEARCH_CONTEXT_v2.md`, `DECISION_LOG.md`, `LITERATURE_MATRIX.md`, `REVIEW_GATE.md`.
- `docs/LUNA_VALIDATION_HANDOFF_v1.md`.
- `research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md`, `research/theorem_notes/G2_FINITE_EVALUATOR_SPEC_v1.md`.
- `docs/reviews/CODEX_WP1_DRAFT_AUDIT_v1.md`, `docs/reviews/G4_MATCHED_PRIOR_ART_COMPARISON_v1.md`, `docs/reviews/GPT_TO_CODEX_DDWMR_CONSOLIDATED_REVIEW_FULL_HANDOFF.md` (§§5, 10, 14), `research/benchmarks/G2_USEFULNESS_BENCHMARK_SPEC_v1.md`.
- Fixture/review A/B/C: `docs/reviews/LUNA_G2_AUDIT_v1.md`, `docs/reviews/LUNA_G2_CASE_A_AUDIT_R2.md`, `docs/reviews/LUNA_G2_CASE_B_AUDIT_R3.md`, `docs/reviews/LUNA_G2_CASE_C_AUDIT_R4.md`, `docs/reviews/GPT_G2_R2_d2cd854_ACCEPT_RECORD.md`, `docs/reviews/GPT_G2_R3_1da2166_ACCEPT_RECORD.md`, `docs/reviews/ACCEPTANCE_LEDGER.md`.

### File được thêm

- `docs/reviews/LUNA_G2_VALIDATION_PREFLIGHT_v1.md` và báo cáo này.
- `validation/README.md`; `validation/configs/{benchmark_v1.json,dev_pilot_v1.json}`.
- `validation/g2/{rational.py,polynomial.py,model.py,interval.py,evaluator.py,checker.py}`.
- `validation/scripts/{generate_manifest.py,run_pilot.py,verify_records.py,summarize_pilot.py,hash_results.py}`.
- `validation/verification/{verify_manifest.py,verify_hand_cases.py,verify_primitives.py}`.
- Các `__init__.py` cho package con `validation`, `validation/g2`, `validation/scripts`, `validation/verification`.
- `results/validation/g2/`: manifest, hash ledgers, hai bộ run metadata/JSONL records/checker reports/summaries/UNKNOWN/failure ledgers.

Danh sách path được thêm đầy đủ:

- `docs/reviews/LUNA_G2_VALIDATION_PREFLIGHT_v1.md`; `docs/reviews/LUNA_TO_CODEX_G2_VALIDATION_FULL_HANDOFF.md`.
- `results/validation/g2/SHA256SUMS_PRE_EVAL.txt`; `results/validation/g2/SHA256SUMS_RESULTS.txt`.
- `results/validation/g2/development_manifest_v1.json`.
- Run đầu: `results/validation/g2/dev_pilot_records_v1.jsonl`; `results/validation/g2/dev_pilot_run_metadata_v1.json`; `results/validation/g2/dev_pilot_record_check_v1.json`; `results/validation/g2/dev_pilot_summary_v1.json`; `results/validation/g2/dev_pilot_unknown_ledger_v1.jsonl`; `results/validation/g2/dev_pilot_failure_ledger_v1.jsonl`.
- Corrected run: `results/validation/g2/dev_pilot_records_v1_replay2.jsonl`; `results/validation/g2/dev_pilot_records_v1_replay2_run_metadata.json`; `results/validation/g2/dev_pilot_records_v1_replay2_record_check.json`; `results/validation/g2/dev_pilot_records_v1_replay2_summary.json`; `results/validation/g2/dev_pilot_records_v1_replay2_unknown_ledger.jsonl`; `results/validation/g2/dev_pilot_records_v1_replay2_failure_ledger.jsonl`.
- `validation/README.md`; `validation/__init__.py`; `validation/configs/benchmark_v1.json`; `validation/configs/dev_pilot_v1.json`.
- `validation/g2/__init__.py`; `validation/g2/checker.py`; `validation/g2/evaluator.py`; `validation/g2/interval.py`; `validation/g2/model.py`; `validation/g2/polynomial.py`; `validation/g2/rational.py`.
- `validation/scripts/__init__.py`; `validation/scripts/generate_manifest.py`; `validation/scripts/hash_results.py`; `validation/scripts/run_pilot.py`; `validation/scripts/summarize_pilot.py`; `validation/scripts/verify_records.py`.
- `validation/verification/__init__.py`; `validation/verification/verify_hand_cases.py`; `validation/verification/verify_manifest.py`; `validation/verification/verify_primitives.py`.

Không có file ngoài phạm vi bị sửa hoặc xóa. Hash từng artifact có trong `results/validation/g2/SHA256SUMS_RESULTS.txt`.

## 3. Equation-to-code và effective class

| Phần toán/đặc tả | Mã | Phạm vi đã mã hóa |
|---|---|---|
| MASTER §§5–11; sáu trạng thái `z=(u,r,ωL,ωR,iL,iR)`; parameter maps; A/B/D/S/QF | `validation/g2/model.py`, `polynomial.py` | JSON rational AST đóng: hằng, label, `+ − × ÷`; denominator phải có bao khoảng dương. Label giữ cố định toàn hold. Gear witness L/R xác minh bằng đồng nhất thức đa thức: `k=n·k_motor`, `J=J_wheel+n²J_motor`, `B=B_wheel+n²B_motor`. |
| G2 candidate/evaluator spec: exp, sin/cos, căn | `validation/g2/interval.py` | `Fraction`, Taylor rational và remainder hữu hạn, norm-tail cho ma trận mũ, root bisection có kiểm tra bình phương. `Q=0` chính xác. |
| Predictor, residual, comparison radius, scaling | `validation/g2/evaluator.py`, `model.py` | Một voltage hữu tỉ chung, một label cell, một initial cell; predictor độ sâu `n=1`, nguyên hold `[0,T]`, nonnegative comparison matrix/positive tail. Tính trong scale rồi trả về đơn vị vật lý trước kiểm tra pose/contact. |
| Full-hold pose, obstacle, contact sufficient bounds | `validation/g2/evaluator.py` | Box-to-circle distance, clip/contact reserve, aggregate trên cell và hold. Safety predicates dùng số hữu tỉ, không dùng float. |
| Serialization, status và proof replay | `evaluator.py`, `checker.py`, `scripts/verify_records.py` | `CERTIFIED` chỉ khi proof đầy đủ replay được và lower margins không âm; `UNKNOWN` gồm inconclusive/cạn tài nguyên. Checker không gọi evaluator cấp cao, nhưng chia sẻ rational/interval/model-map và exp/trig/root primitives. |

Pilot dùng `P_s=I`, law `clip(q,-1,1)` với `L_phi=1`; 12 label coordinates và quan hệ reciprocal/gear giữ trong AST. Không hỗ trợ mọi rational polynomial/Bernstein witness, arbitrary compact set, law tùy ý, voltage search, subdivision hay refined kernel. Interval matrix hull làm mất tương quan số học nhưng được ghi rõ là outer hull; không đổi label thành tham số vật lý biến thiên theo thời gian.

### Sửa và sai khác implementation

- Gear witness được khóa vào đúng danh tính motor/wheel trên cả hai phía; regression primitive xác nhận identity với rotor inertia dương.
- Run đầu dừng do estimate không tận dụng GCD. Commit `add632c` đổi phép cộng sang denominator chung theo LCM và ước lượng sau cross-cancellation cho nhân/chia; thêm hai primitive checks. Không đổi toán học, benchmark, profile hay query selection.
- Checker trước đó tính record `UNKNOWN` thiếu proof object như replay hoàn tất. Đã sửa thành `replayed=false`, `resource_limited=true`; summary tách reason counts, query có margins và nhóm chín action cùng resource-limited.
- Corrected replay vẫn bị budget chặn. Estimate tiền xử lý lớn hơn trần không tự chứng minh kết quả rút gọn sẽ vượt trần; tính bảo thủ của guard cần Codex audit. Không nới cap hậu nghiệm.

## 4. Manifest, pilot và kết quả

Benchmark có 6 cell trạng thái 9 chiều × 12 scene × 3 horizon × 9 action = **1.944** query/method/profile. Manifest `development_manifest_v1.json` giữ mọi ID gốc, chọn trước **216** query: bốn cell low/high-speed × yaw ±, hai scene clearance `0.05 m` và `0.2 m`/lateral offsets khai báo, ba horizon, chín voltage action; 24 nhóm state/scene/horizon. **1.728** ID còn lại là `NOT_RUN`. Pilot không phải held-out, full-grid hay comparison đã khóa.

Profile `DEV_FALLBACK_N1_PILOT_V1` đóng băng: `n=1`; Taylor exp degree 16, trig degree 18, comparison series order 16; 24 root bisections; không chia state/parameter; một whole-hold interval hull; tối đa 8.192 rational bits, 1.000.000 rational operations, 15 giây/query. Không có coverage threshold. Lặp cùng hull trên time panels không làm bound chặt hơn.

| Lần chạy | Source revision | Kết quả 216 query | Work và thời gian |
|---|---|---|---|
| Ban đầu | `d50b8db0f999d3def6849078a395c7bcf6938707` | 216 `UNKNOWN`, `RATIONAL_BIT_LIMIT`; estimate 8.307–9.504 bit | max observed 5.704 bit; operations 28.982–28.991/query; elapsed tổng 17.483 s, min/median/max 0.062/0.078/0.125 s |
| Corrected replay | `c313c2fd23ecab61a09549f7e5c4cb5cc7999100` | 216 `UNKNOWN`, `RATIONAL_BIT_LIMIT`; estimate 8.265–8.514 bit | max observed 7.935 bit; operations 29.001–29.016/query; elapsed tổng 15.390 s, min/median/max 0.062/0.078/0.079 s |

Cả hai lần: 0 `CERTIFIED`, 0 `INVALID_INPUT`, 0 execution failure; 216/216 `UNKNOWN` ở cả 24 nhóm chín action. Không query nào hoàn tất safety margins; collision/contact margins, radius và enclosure widths không có. Không có state/parameter split; mọi query dừng trước safety result. Thời gian không phải safety predicate.

Corrected run checker: `all_pass=true`, exact manifest coverage, hash/source revision match, 216 records, 1.728 `NOT_RUN`, 216 resource-limited UNKNOWN, 0 invalid, 0 execution failures, **0 completed certificate replays**. Không có proof object để exercise checker trên positive certificate; đây là gap validation.

## 5. Verification commands và hashes

Đã chạy trên Python 3.12.12:

```powershell
python -m compileall -q validation
python -m validation.verification.verify_manifest
python -m validation.verification.verify_hand_cases
python -m validation.verification.verify_primitives
python -m validation.scripts.verify_records
python -m validation.scripts.run_pilot --output results/validation/g2/dev_pilot_records_v1.jsonl
python -m validation.scripts.run_pilot --output results/validation/g2/dev_pilot_records_v1_replay2.jsonl
python -m validation.scripts.verify_records --records results/validation/g2/dev_pilot_records_v1_replay2.jsonl --metadata results/validation/g2/dev_pilot_records_v1_replay2_run_metadata.json
python -m validation.scripts.summarize_pilot --records results/validation/g2/dev_pilot_records_v1_replay2.jsonl
python -m validation.scripts.hash_results
```

compileall exit 0; manifest all_pass=true (216 selected, 1.728 NOT_RUN); hand fixtures all_pass=true, 32 checks; primitives all_pass=true, 21 checks. Record checker cho cả hai runs all_pass=true, nhưng completed proof replays = 0. Không có assertion check nào thất bại. Evaluator cho kết quả resource-limited, không phải validation PASS.

SHA-256 quan trọng (đầy đủ trong SHA256SUMS_RESULTS.txt):

- benchmark: b2bc12cd578229cfb6df4b426f93e0f472d69f6be36929df93e797ff79396a9e
- pilot config: 068e85fc3a9ecb2e85a4d4dd49773b76beada2e1afb85f012f48280c6be09a7c
- manifest: 04190d23c9597348245cd93793f60e87476b35e8c43e0accaebdee525f3f172c
- run đầu JSONL: cd01b1c62dc89f8ef20fb78161ee16a634a3e0e12ede11dcb81b661622127128
- corrected replay JSONL: d79aeb0b4e387e160e05df55ce5f3f4e82e3150bec8d285fb62a6dfdff7e200f
- corrected summary: 1b8e758821a4a821e8de427a34d5d804625d32277a8db5c28c3b8ba4df652b9f
- checker record report: 124a19bc23dc6e903c6c7126a6764e60549bcc831f734a82ba8668cf8f6a4ca6
- corrected run metadata: 3260773d720336f16cb2161fcf023cef2279e172b03983613008e67b7b5b3763
- failure ledgers rỗng: SHA-256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.

## 6. Findings cần review và trạng thái

### W1-HO-01 — Budget ngăn pilot tạo safety margins

**Finding:** Corrected run vẫn vượt trần 8.192 bit ở preflight estimate cho mọi query. Estimate giảm so với run đầu nhưng vẫn cao hơn số bit tối đa quan sát; pilot không tạo margins.
**Evidence:** 216/216 RATIONAL_BIT_LIMIT; estimate 8.265–8.514 bit, max recorded 7.935 bit; 0 completed margins và 0 proof replay.
**Consequence:** Chưa đánh giá được usefulness/coverage; chưa có căn cứ về khoảng cách collision/contact trên pilot. Không diễn giải UNKNOWN thành unsafe.
**Status:** BLOCKED — usefulness evidence; độ chặt của implementation preflight cần audit.
**Required action:** Codex xác minh accounting bound có thể siết mà vẫn bảo toàn giới hạn tài nguyên; nếu đổi cap/algorithm, tạo profile/manifest revision mới và định nghĩa work-cap comparison trước run mới, không ghi đè artifacts này.

### W1-HO-02 — Checker chưa replay certificate dương

**Finding:** Checker kiểm tra manifest, hashes, schema/status/resource reasons; chưa kiểm chứng proof arithmetic/margin vì evaluator không xuất proof object.
**Evidence:** Cả hai reports ghi completed_certificate_replays=0; mọi record là resource UNKNOWN.
**Consequence:** Chưa có bằng chứng thực nghiệm rằng serialized inclusions/cell coverage của record CERTIFIED được checker xác minh end-to-end. Rational, interval, model-map và exp/trig/root primitives vẫn là shared trusted base.
**Status:** UNVERIFIED — checker-on-positive-record acceptance.
**Required action:** Cần proof-producing case để Codex audit/replay; nếu profile hiện tại không tạo được, xác định fixture/profile revision trước khi claim checker path exercised.

### W1-HO-03 — Fallback có thể quá rộng; phạm vi không tổng quát

**Finding:** Một whole-hold hull, không state/parameter splitting hay exact-kernel refinement; effective subset chỉ bao phủ rational AST hữu hạn và clip.
**Evidence:** n=1, nguyên [0,T], no-op time slab; độ rộng/margins không có do budget abort. Không hỗ trợ arbitrary compact Theta, arbitrary Lipschitz law, Bernstein witnesses hay endpoint/G3.
**Consequence:** Không khẳng định usefulness ngoài lớp hữu hạn; không thể suy rộng sang plant thực hoặc controller.
**Status:** OPEN/UNVERIFIED — usefulness và mở rộng phương pháp.
**Required action:** Báo riêng refinement/spec cần đóng; không coi lặp time panel trên cùng hull là cải thiện.

### W1-HO-04 — G4 matched comparison chưa thực hiện

**Finding:** Không có adapter/baseline external validated-reachability được chọn và tái lập; không có equal-work benchmark hoặc threshold định trước.
**Evidence:** Không có source/config/proof tương thích cho baseline trong output; pilot development-only, không held-out/locked.
**Consequence:** Không có kết luận superiority, novelty hay G4; internal ablation không thay external baseline.
**Status:** NOT_IMPLEMENTED; generic novelty BLOCKED; G4 UNVERIFIED.
**Required action:** Codex xác định baseline và nghĩa vụ tương thích (plant/law/fixed labels/V/time/collision-contact) cùng acceptance threshold trước comparison lock mới.

## 7. Reproduction

Từ repo root, xác minh artifacts đã commit:

```powershell
python -m validation.scripts.generate_manifest
```

Sau đó chạy các kiểm tra:

```powershell
python -m validation.verification.verify_manifest
python -m validation.verification.verify_hand_cases
python -m validation.verification.verify_primitives
python -m validation.scripts.verify_records --records results/validation/g2/dev_pilot_records_v1_replay2.jsonl --metadata results/validation/g2/dev_pilot_records_v1_replay2_run_metadata.json
python -m validation.scripts.summarize_pilot --records results/validation/g2/dev_pilot_records_v1_replay2.jsonl
python -m validation.scripts.hash_results
```

Evaluator rerun dùng đường dẫn mới để không ghi đè evidence:

```powershell
python -m validation.scripts.run_pilot --output results/validation/g2/dev_pilot_reproduction_v1.jsonl
python -m validation.scripts.verify_records --records results/validation/g2/dev_pilot_reproduction_v1.jsonl --metadata results/validation/g2/dev_pilot_reproduction_v1_run_metadata.json
python -m validation.scripts.summarize_pilot --records results/validation/g2/dev_pilot_reproduction_v1.jsonl
```

Runner cần working tree sạch để gắn record với revision bất biến. Không chạy lại trên đường dẫn đã tồn tại nếu không chủ ý dùng chế độ overwrite.

## 8. Một yêu cầu Codex review

**Đề nghị Codex review độc lập toàn bộ branch và artifact**, tập trung vào: (a) dấu/đơn vị/scaling, positivity/gear witness, Taylor và forced-series tails, predictor residual, outer-hull semantics, full-hold contact/collision và trusted base của checker; (b) tính chặt/an toàn của dự toán bit sau GCD và status/resource aggregation; (c) liệu cần algorithm hay profile mới để tạo pilot có margins; (d) baseline ngoài, refinement, benchmark work alignment/acceptance threshold cần chốt trước G4. Xin trả Finding/Evidence/Consequence/Status/Required action cho mỗi điểm. Mọi thay đổi cap, phương pháp, effective input class, benchmark lock hoặc tiêu chí khoa học cần review trước revision/run mới. Đến lúc đó giữ HOLD, G2/G3/G4 UNVERIFIED, physical correspondence UNVERIFIED.
