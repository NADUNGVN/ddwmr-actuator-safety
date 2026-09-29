# DDWMR — review WP1 và matched comparison trong một lượt

## Sản phẩm bắt buộc

Hãy trả về **một file Markdown có thể tải xuống**:

`GPT_TO_CODEX_DDWMR_WP1_REVIEW_FULL_HANDOFF.md`

Toàn bộ audit, sửa đổi chính xác và disposition phải nằm trong file. Chat cuối chỉ tóm tắt bằng tiếng Việt và cung cấp link tải. Nếu không thể tạo attachment, nói rõ và trả toàn bộ Markdown trong một code block để người dùng lưu; không nói đã tạo file khi chưa có.

## Authority và snapshot

Repository: <https://github.com/NADUNGVN/ddwmr-actuator-safety>, branch `main`. Ghi SHA thực tế đã đọc và read ledger. Không trộn các phiên bản. Đây là project DDWMR của thầy Viễn; PACE-Seg không thuộc phạm vi này.

MASTER v2.1 vẫn authoritative; G1 PASS trong phạm vi mô hình rút gọn; G2/G3/G4 UNVERIFIED, physical correspondence UNVERIFIED, tổng thể HOLD. Consolidated review trước đã ACCEPT Case C trong phạm vi hẹp. Các patch trong `docs/proposals/consolidated_review/` là **đề xuất chưa áp dụng**, trừ khi canonical log tại SHA bạn đọc ghi quyết định mới của người dùng. Đọc authority thực tế, không coi file patch là authorization.

## Thứ tự đọc

1. `AGENTS.md` và cả bốn file canonical trong `research_context/`.
2. `docs/reviews/GPT_TO_CODEX_DDWMR_CONSOLIDATED_REVIEW_FULL_HANDOFF.md`, nhất là §§5, 10, 12, 14.
3. `docs/reviews/CODEX_CONSOLIDATED_REVIEW_RESPONSE_v1.md`.
4. `research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md` — analytic dependency.
5. `research/theorem_notes/G2_FINITE_EVALUATOR_SPEC_v1.md`.
6. `research/benchmarks/G2_USEFULNESS_BENCHMARK_SPEC_v1.md`.
7. `docs/reviews/G4_MATCHED_PRIOR_ART_COMPARISON_v1.md` và các primary sources cần cho claim đang xét.
8. `docs/proposals/consolidated_review/README.md` và hai patch nếu vẫn pending.
9. `docs/reviews/CODEX_WP1_DRAFT_AUDIT_v1.md` — root findings, không thay thế audit độc lập.

A/B/C là các hand cases đã có review. Không mở lại toàn bộ số học nếu không phát hiện dependency mới. Tập trung audit khả năng chuyển từ ví dụ riêng lẻ sang một đặc tả hữu hạn có thể kiểm chứng.

## Audit đồng thời bốn phần

### I. Finite evaluator

- Input class có biểu diễn hữu hạn thật sự không? Tính dương, domain của mẫu số, gear correlations và fixed labels có được kiểm không?
- Phi được tính bằng primitive hữu hạn nào? Không dùng oracle cho một hàm Lipschitz tùy ý.
- Kiểm các bound series/remainder, interval operations, nested integral, variable upper limit và toàn bộ time slab. Nêu một primitive thiếu nếu có; không chấp nhận một lời hứa dùng validated library thay cho contract.
- Initial boxes là family các initial state chính xác. Predictor/error cần dùng cùng initial state trong mỗi fiber; error zero không hợp lệ nếu center chỉ là midpoint mà bỏ initial radius.
- Kiểm tổng hợp numerical enclosure error, predictor residual, comparison radius, pose và contact checker; tránh bỏ sai số hoặc đếm sai vai trò của chúng.
- Bounded-budget termination có trả UNKNOWN sound không? Tách INVALID_INPUT, lỗi implementation, margin không đủ và budget exhaustion.
- Kiểm soundness proposition và coverage của mọi initial/parameter/time cell. Không đòi completeness ở equality boundary.
- Endpoint output không được biến thành K_T/recursive result.

### II. Benchmark

- Có miền moving-state với bề rộng khác zero, independent left/right uncertainty, action list và obstacle/horizon cố định trước outputs không?
- Những stress cases và claim giới hạn có phù hợp nhau? Không mặc nhiên thêm yêu cầu hardware/stiffness vào MASTER.
- Unit scaling, synthetic provenance và gear witness có rõ không?
- Có ngăn tuning obstacle/tolerance sau khi thấy result và cherry-picking CERTIFIED cells không?
- Denominator, cell aggregation, subdivision, UNKNOWN và all-action-UNKNOWN có được định nghĩa nhất quán không?
- Không coi benchmark draft là kết quả usefulness, performance hoặc runtime.
- Đặc tả hiện mới có fallback hữu hạn; sharper global/refined variants, cấu hình resource và baseline ngoài còn OPEN. Hãy ra disposition riêng cho fallback và gói comparison, không ACCEPT cả gói từ việc fallback sound. Nêu chính xác phần cần bổ sung để lock.

### III. Matched prior art

- Các so sánh dùng cùng plant, law, initial/parameter cells, action, horizon và safety/contact checker hay không?
- Tách internal ablation khỏi external established baseline; regularity mismatch không phải ưu thế.
- Chỉ rõ baseline nào đã đủ specification, baseline nào còn OPEN. Nếu một generic fallback được dùng thì không gọi nó là full reproduction của một công cụ chưa audit.
- Nêu contribution hypothesis còn sống và bằng chứng cụ thể có thể bác bỏ nó. Generic predictor-validation novelty vẫn BLOCKED.

### IV. Readiness và authorization

Ra disposition riêng cho (a) sound analytic specification, (b) benchmark lock readiness, (c) baseline readiness, (d) scope có thể đề nghị validation-only implementation. **Không tự cấp quyền code.** Nếu chưa sẵn sàng, gom mọi sửa đổi bắt buộc thành một danh sách, chỉ rõ path/section và câu hoặc công thức cần đổi.

Không mở G3, không xây controller/solver, không nâng gate. Nếu policy chưa được user duyệt, giữ nguyên; review của GPT không thay thế quyết định người dùng.

## Format file output

1. Tóm tắt tiếng Việt và disposition.
2. Repo/SHA/read/source ledger; thiếu nguồn nào ghi rõ.
3. Equation/primitive audit.
4. Benchmark audit và lock disposition.
5. Matched-comparison/novelty disposition.
6. Bảng readiness: ACCEPT / NEEDS REVISION / BLOCKER / UNVERIFIED, phạm vi và bằng chứng thiếu.
7. Exact proposed edits; không sửa assumption ngầm.
8. **Một instruction tổng hợp cho Codex**: việc làm ngay, việc cần người dùng quyết định, việc vẫn bị chặn.

Mỗi finding dùng đúng **Finding / Evidence / Consequence / Status / Required action**. Ghi rõ gì đã kiểm bằng phương trình và gì chỉ là một đề xuất chưa có evaluator/result. Trả mọi blocker độc lập trong cùng lượt; không kết thúc bằng yêu cầu thêm một hand case không có tiêu chí đóng.

**Xuất file `GPT_TO_CODEX_DDWMR_WP1_REVIEW_FULL_HANDOFF.md` kèm link tải.**
