# Codex → Luna — G2 validation review and correction assignment R2

2026-09-30. Reviewed commit: **`ffc1aec4f10a9c3796f1e5317ad2da5758934116`**, branch `luna/g2-validation-v1`.

## 0. Tóm tắt cho người dùng và Luna

**Disposition: NEEDS REVISION; certificate-producing branch BLOCKED by an implementation error.** Đây là lỗi implementation của cận sai số, không phải phản ví dụ bác bỏ MASTER hay chứng minh enclosure đã được review. Ngoài lỗi này, còn một lỗi tái lập hash giữa Windows working copy và Git blob.

Các artifacts hiện có được giữ làm bằng chứng development: 216/216 query dừng với `RATIONAL_BIT_LIMIT`, 1728 NOT_RUN, không safety margins, không completed proof replay. Không có certificate dương hiện hành cần thu hồi; cũng không có bằng chứng safety/usefulness. G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED; **HOLD**.

Code validation vẫn được phép theo W1. Người dùng giao file này cho Luna trong cùng folder; Codex không sửa implementation hoặc tự gọi agent. Sửa tính đúng trước, sau đó chẩn đoán tài nguyên và chạy lại có version. Không mở G3, controller hoặc hardware.

## 1. Review ledger và giới hạn

Root đọc AGENTS và cả bốn canonical context, handoff/preflight Luna, evaluator/checker, rational/interval/model/polynomial modules, scripts run/verify/hash, primitive/hand-fixture code, profile và pilot summary/metadata. Diff từ `6956022` tới reviewed commit không sửa AGENTS/canonical context. Working tree sạch tại lúc bắt đầu review.

Root kiểm hash **read-only** của 18 path trong `SHA256SUMS_RESULTS.txt`: tất cả khớp working-copy bytes hiện tại. Root cũng đối chiếu raw Git blob bytes với hai config hashes; khác nhau như R2-04 dưới đây. Không chạy lại evaluator, không chạy test suite, không tạo thêm result hoặc sửa code trong review này. Số 32/21 là kết quả Luna đã báo; không được đọc như 53 phép kiểm root vừa chạy độc lập.

## R2-01 — chia factorial hai lần trong forced comparison series

**Finding**

`validation/g2/evaluator.py:120–128` tích lũy `t_power = T^(k+1)/(k+1)!` qua recurrence, rồi ở dòng 121–122 lại chia `factorial(k+1)`. Vì thế partial sum đang dùng

\[
\sum_{k=0}^{K}\frac{T^{k+1}}{((k+1)!)^2}N^k q
\]

thay vì cận đúng

\[
\sum_{k=0}^{K}\frac{T^{k+1}}{(k+1)!}N^k q.
\]

**Evidence**

`_radius_series`: `t_power=T`; mỗi bước sau nhân T và chia `(k+2)`. Dòng `coeff=t_power/factorial(k+1)` là phép chia thừa. Trong khi đó `checker.py:111–122` dùng `t_over_factorial` trực tiếp nên không có lỗi này.

Phản ví dụ exact rational: xét một component `N=1`, `q=1`, `T=1/10`, order K=1. Có thể nhúng vào ma trận 6×6 diagonal với chỉ một component forcing khác zero; D có hai cột và chỉ D[0,0]=1, force=(1,0).

- Partial code: `1/10 + 1/400 = 41/400 = 0.1025`.
- Tail code: `T*1*3*Q^2/3! = 1/2000 = 0.0005`, với Q=1/10.
- Tổng code: `103/1000 = 0.103`.
- Nghiệm comparison thật `exp(1/10)-1` lớn hơn `1/10+1/200=21/200=0.105`.

Vì `103/1000 < 21/200`, output không phải upper bound. Đây là phản ví dụ cho routine tổng quát trong phạm vi số không âm nó nhận; không phải một trajectory DDWMR được dựng mới. Lỗi coefficient cũng hiện diện ở order 16 của pilot; không có cơ sở coi tail của phần bị bỏ sau K bù được thiếu hụt ở các số hạng đã giữ.

**Consequence**

Mọi claim CERTIFIED phụ thuộc bán kính này chưa sound. Checker đúng có thể phát hiện mismatch trên completed nonzero-radius record, nhưng chưa record nào đi tới đó. Các UNKNOWN resource-only vẫn không khẳng định safety nên không bị đổi thành unsafe. Không tăng cap rồi dùng certificate từ code cũ.

**Status**

**BLOCKER — mathematical correctness of implemented radius.**

**Required action**

Chọn đúng một convention: (a) giữ t_power thuần T^(k+1) và chia factorial một lần khi dùng; hoặc (b) giữ coefficient T^(k+1)/(k+1)! và dùng trực tiếp. Sửa evaluator, đối chiếu checker với đặc tả, không sửa checker để tái tạo công thức sai. Thêm regression độc lập cho ví dụ trên và các K=0,1,2 cùng order16, N=0, q=0. Expected polynomial coefficients phải được dựng độc lập từ factorial/powers, không copy recurrence đang kiểm. Với fixture K=1, partial đúng 21/200, tail 1/2000, upper đúng 211/2000. Tail không phải exact solution; đừng kiểm nó bằng equality với nghiệm.

## R2-02 — verification chưa bao phủ đường tạo chứng nhận

**Finding**

Các checks đang qua không chứng minh correctness của radius hay end-to-end proof replay.

**Evidence**

`verify_primitives.py` kiểm clip, zero exponential, root, sign/scaling, input/caps, nhưng không gọi `_radius_series` hoặc so nó với `_replay_radius`. `verify_hand_cases.py` kiểm các bất đẳng thức số học được chọn riêng; một số là constant/sign/identity checks. Nó không exercise general fallback. `verify_records.py` chấp nhận resource UNKNOWN như record có cấu trúc hợp lệ, dù `replayed=false`; report có 0 completed replays.

**Consequence**

`all_pass` hiện là record-integrity/selected-fixture pass, không phải evaluator accepted hay positive-certificate validation. Checker có implementation độc lập cho recurrence là điểm tốt, nhưng chưa có bằng chứng thực thi nhánh phát hiện sai lệch.

**Status**

**NEEDS REVISION — coverage of verification evidence.**

**Required action**

Sau R2-01, tạo fixture phát sinh **completed proof object với nonzero residual/radius**, checker replay thành công, và fixture positive certificate end-to-end. Một exact-rest fixture có thể kiểm serialization/status nhưng không thay nonzero-radius regression. Fixture phát triển được khai báo riêng trước outputs, không sửa geometry/grid pilot để ép CERTIFIED. Không bắt buộc fixture positive phải là một query trong pilot nếu đó là kiểm tra plumbing được gắn nhãn riêng. Thêm tamper checks: giảm radius, tăng margin, đổi voltage/horizon/query/hash/coverage hoặc status phải bị reject. Một completed inconclusive record cũng cần replay. Tách `record_integrity_pass`, `proof_replay_pass`, và `positive_certificates_checked`; giữ khả năng diễn giải report cũ.

## R2-03 — bit budget và chẩn đoán nguyên nhân

**Finding**

`max_seen_bits=7935` thấp hơn cap8192 không chứng minh guard sai: guard kiểm upper estimate của phép toán kế tiếp, còn max_seen chỉ thống kê kết quả đã hoàn tất. Cơ chế có thể dừng bảo thủ hợp lệ. Chưa xác định được stage gây dừng từ artifact hiện tại.

**Evidence**

`rational.py` cộng bằng estimate LCM, nhân/chia sau cross-cancellation. Tổng bit lengths là upper estimate và có thể lớn hơn bit length thực. `Budget._tick` dừng trước operation, `_check_result` ghi max đã thấy. UNKNOWN record lưu estimate text và counters nhưng không có stage, operation type hoặc operand bit widths. Có thêm error đúng/sai coefficient R2-01 độc lập với resource cap.

**Consequence**

Không có căn cứ gọi toàn bộ UNKNOWN là “chỉ do cap quá thấp” hoặc “độ bảo thủ vật lý”. Nới cap không sửa R2-01 và có thể chỉ chuyển điểm bùng nổ số hữu tỉ sang stage sau.

**Status**

**UNVERIFIED — runtime bottleneck; conservative guard not disproved by current statistics.**

**Required action**

Thêm stage/primitive identifiers, operand numerator/denominator bit lengths, estimate kind (pre-operation/result), configured cap và max completed bits trong failure records. Phân biệt cap intermediate với reduced-result cap. Audit zero/identity arithmetic để tránh công việc không cần thiết; giữ exact/outward bounds. Có thể thử một profile development mới với work caps định trước dưới quyền W1, sau correctness checks; không cần người dùng cấp lại cùng quyền. Dùng version/hash riêng, giữ input physics/scenes/actions cũ để so sánh. Không tăng cap lặp vô hạn tới lúc thành công.

Nếu cần backend bounded-precision, phải có contract làm tròn hướng ra ngoài và kiểm inclusion độc lập trước khi bật CERTIFIED. Ví dụ dyadic endpoint rounding cần lower=floor(2^p*l)/2^p, upper=ceil(2^p*u)/2^p với semantics đúng cho số âm; mọi scalar upper/lower bound cũng phải giữ đúng hướng. Đây là phương án có điều kiện, không phải instruction thay ngay toàn bộ arithmetic hoặc sửa model.

## R2-04 — hashes hiện phụ thuộc line endings

**Finding**

Raw-byte hashes khớp working copy Windows hiện tại nhưng khác raw Git blobs. Một checkout LF hợp lệ có thể thất bại frozen-input check dù nội dung JSON giống nhau.

**Evidence**

`git ls-files --eol` cho benchmark, pilot config và manifest: `i/lf w/crlf`, không có per-path text/eol rule. `.gitattributes` hiện chỉ bảo toàn một GPT handoff. `run_pilot.py`/`verify_records.py` hash `read_bytes()`.

| Config | Hash lưu trong manifest/working copy | SHA256 bytes Git blob tại ffc1aec |
|---|---|---|
| benchmark_v1.json | `b2bc12cd578229cfb6df4b426f93e0f472d69f6be36929df93e797ff79396a9e` | `3d13b1681ba89d54097f61cf59c18581b445531dc9361e9b6f7b0c0fcaf1c306` |
| dev_pilot_v1.json | `068e85fc3a9ecb2e85a4d4dd49773b76beada2e1afb85f012f48280c6be09a7c` | `56fd70f2d4ca7b5b31aaef95c6d28edbce14532edf8489158ff90adbabfaa12f` |

**Consequence**

Đây là portability/provenance blocker cho reproduction cross-checkout, không phải bằng chứng artifacts bị làm giả. Cả 18 raw hashes hiện tại khớp đúng môi trường ghi nhận.

**Status**

**NEEDS REVISION — reproducibility across Git checkout settings.**

**Required action**

Định nghĩa hash protocol mới có version: canonical JSON semantic hashes và/hoặc bytes LF được kiểm soát bằng repo-local attributes. Phân biệt byte-integrity hash của archive với semantic input hash. Giữ artifacts/ledgers v1 nguyên vẹn; đừng tái tạo chúng rồi gọi là bản cũ. Báo rõ line-ending convention cũ và cách kiểm legacy evidence. Thêm reproduction checks LF/CRLF mà không sửa global git config; runner mới không tự overwrite history. Dùng output/report names mới cho R2.

## R2-05 — checker contract và metadata cần kiểm chặt hơn

**Finding**

Checker recompute nhiều bound độc lập, nhưng chưa kiểm đầy đủ effective input và các field mô tả claim; replay entry point không tương đương validate toàn bộ query.

**Evidence**

`checker.py:155–162` parse T/voltage/state và build model, không thực hiện các constraint Vmax, state coordinate order và supported profile từ evaluator `_parse_input_query`. `verify_records.py` kiểm input hash/IDs nhưng không so các aliases `held_voltage`, `horizon`, `profile_id` với query; widths và reason consistency cũng không được re-evaluate. Nhánh proof dùng `(status=='CERTIFIED') != should_certify`, chưa whitelist mọi status. Metadata command trong runner hardcode `python validation/scripts/run_pilot.py`, không ghi đúng CLI/output args của replay2.

**Consequence**

Với frozen valid benchmark hiện tại, chưa chứng minh được safety sai do gap này; đó là hạn chế của checker được công bố cho general supported records. Một record có thể mang metadata mâu thuẫn hoặc query ngoài contract mà replay entry point không reject vì lý do đó. Đừng gọi validation toàn bộ record khi chỉ một subset được kiểm.

**Status**

**NEEDS REVISION — checker/input/claim provenance contract.**

**Required action**

Validate supported query domain trước replay, whitelist statuses, so tất cả safety-relevant aliases với hashed query; kiểm margins/radii/widths được xuất hoặc loại chúng khỏi scope được xác nhận một cách rõ ràng. Proof-less resource records chỉ được ghi integrity pass, không arithmetic replay. Hash/bind specification version và implementation revision; giữ shared trusted components minh bạch. Ghi executable/version thực bằng `sys.executable`/runtime hiện hành, actual argv và cwd; không dùng command string hardcoded. Lỗi checker phải trả report reject/inconclusive rõ thay vì vô tình được coi pass.

## 2. Phần đọc code chưa thấy sai công thức

Không phải acceptance trọn hệ thống: root thấy dấu A/B/D/S và coordinate scaling phù hợp decomposition; interval hull predictor, min(Lipschitz residual,2C), componentwise nonnegative majorant, Taylor exponential norm-tail, root bisection, scaled slip radius, physical pose lift và distance/contact tests có cấu trúc đúng với draft. Chưa thực thi paths trên completed proof và chưa chứng minh toàn bộ implementation không còn lỗi. R2-01 chặn sử dụng certificate path cho đến khi sửa và review.

## 3. Assignment R2 — thứ tự thực hiện trong cùng folder

Working directory: `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`.

1. Đọc current AGENTS + canonical context, file này và handoff v1. Kiểm Git status; giữ thay đổi người khác. Tiếp tục branch `luna/g2-validation-v1` sau commit chứa review này; không merge main.
2. Sửa R2-01 và bổ sung verification độc lập, rồi sửa checker contract R2-02/R2-05. Không nới cap trước correctness checks.
3. Sửa hash/version/provenance protocol R2-04, giữ dữ liệu v1 bất biến.
4. Instrument R2-03, freeze fixture/profile/selected IDs trước chạy mới. Thu ít nhất completed nonzero-radius proof và positive replay fixture nếu làm được; nếu không, báo chính xác blocker, không fabricate success.
5. Chạy development diagnostic/pilot có giới hạn với output R2 riêng. Giữ cùng 216 original pilot IDs cho comparison nếu chạy đủ; nếu chỉ chạy subset chẩn đoán thì công bố trước IDs và NOT_RUN. Ghi margins khi tính xong và telemetry khi abort. UNKNOWN vì negative sufficient margin khác UNKNOWN vì resource limit.
6. G4 baseline vẫn OPEN; chưa cần mở rộng sang external baseline trong đợt sửa correctness này. Không thêm controller, estimator, wheel lock hay thay MASTER.
7. Commit code + bằng chứng, push branch hiện có nếu được; không force-push/merge. Không ghi đè review root hoặc báo cáo Luna v1.

**File trả về bắt buộc:** `docs/reviews/LUNA_TO_CODEX_G2_VALIDATION_R2_FULL_HANDOFF.md`.

Report tự đủ ngữ cảnh: start/end SHA, từng R2 finding→fix→evidence→remaining limit, exact commands, new hash protocol, primitive/regression outputs, positive/negative/tampered proof replay counts, query/profile/version provenance, resource-stage statistics, margins/UNKNOWN/NOT_RUN denominators và file paths. Trả một đường dẫn tuyệt đối để người dùng chuyển về Codex. Nếu chưa đạt thì ghi PARTIAL/BLOCKED cụ thể.

**Không nâng gate.** W1 vẫn cho phép sửa validation; không cần xin lại quyền code cho phạm vi này. Người dùng vẫn là trung gian. Codex review code/bằng chứng sau khi Luna trả file; model agreement và checks riêng lẻ không thay proof.
