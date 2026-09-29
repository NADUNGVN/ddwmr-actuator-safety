# Hai quyết định sau review tổng hợp — CHƯA ÁP DỤNG

Nguồn: [GPT full handoff](../../reviews/GPT_TO_CODEX_DDWMR_CONSOLIDATED_REVIEW_FULL_HANDOFF.md), sections 12 và 14. Các đề xuất dựa trên context tại `c9ff32d45ad7f500cc2492c3bc7a69480c29c636`; không sửa phương trình plant hoặc A/B/C.

## A. Ghi nhận Case C

[CASE_C_STATUS_PENDING.patch](CASE_C_STATUS_PENDING.patch) ghi nhận GPT ACCEPT C.1–C.16 trong phạm vi certificate-output tổng hợp. G2/G3/G4 vẫn UNVERIFIED và HOLD; usefulness vẫn chưa đạt. Patch sửa metadata trong MASTER, gate, log, matrix và README, đồng thời làm rõ câu summary cũ dễ gây hiểu nhầm về kết quả giải tích đã được review.

Khi người dùng duyệt, ghi lại câu đồng ý và ngày thực tế vào DECISION_LOG; không để dòng provenance ở dạng pending. Các tài liệu review cũ giữ nguyên như lịch sử. File tổng kết ngày 2026-09-29 là snapshot trước review này; cập nhật tiến độ mới nằm trong Codex response kèm theo.

## B. Chính sách code kiểm chứng riêng

[VALIDATION_ONLY_POLICY_PENDING.patch](VALIDATION_ONLY_POLICY_PENDING.patch) tạo một loại authorization riêng cho evaluator có chứng nhận, kiểm tra số học bao ngoài, adapter baseline và benchmark offline phục vụ G2/G4.

Patch này **chỉ tạo loại quyền**, chưa khởi chạy WP2. Đặc tả evaluator và benchmark cần được review và được chỉ định trong quyết định cho phép code cụ thể. Controller, safety filter, G3, closed-loop simulation, hardware và GO vẫn bị chặn. Điều này tránh dùng một đề xuất chính sách để mở toàn bộ implementation.

Lý do phải xin quyết định: quy định hiện tại trong AGENTS và MASTER section 32 cấm mọi implementation trước G1–G4/GO; GPT không có quyền tự bỏ giới hạn này. Công việc tài liệu giải tích WP1 và đối chiếu nguồn WP3 tiếp tục theo quyền hiện có.

## Cách áp dụng sau khi có quyết định

Hai patch độc lập được soạn trên cùng base. `git apply --check` đã kiểm tra từng patch riêng. Nếu áp dụng cả hai theo thứ tự A rồi B, rebase các hunk context chung (đặc biệt DECISION_LOG) trên nội dung mới, giữ nguyên ý nghĩa đã duyệt; không force hoặc bỏ qua hunk lỗi. Ghi provenance riêng cho mỗi quyết định. Không tự coi `tiếp tục` trước khi có bản diff cụ thể là chấp thuận sửa chính sách.

Formulation vật lý vẫn v2.1. Nếu người dùng muốn mở validation implementation ngay, cần xác định rõ specification/benchmark nào được chấp nhận, phạm vi code và tiêu chí dừng; các draft WP1 chưa phải specification đã được GPT ACCEPT.
