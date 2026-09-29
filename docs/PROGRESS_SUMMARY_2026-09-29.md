# Cập nhật tiến độ DDWMR — 2026-09-29

Repo: `NADUNGVN/ddwmr-actuator-safety`, nhánh `main`.
Mốc nghiên cứu được đối chiếu: `547061d2cc0ce1ea0c000de0ec66054034ec930f` (local và remote trùng nhau lúc kiểm tra).

Đây là bản tổng kết, không thay thế [MASTER v2.1](../research_context/MASTER_RESEARCH_CONTEXT_v2.md), không đổi giả định hay trạng thái gate. Nội dung PACE-Seg gửi nhầm không thuộc nghiên cứu này.

## 1. Những việc đã đạt được

| Hạng mục | Kết quả và phạm vi |
|---|---|
| Tổ chức dự án | Repo độc lập; AGENTS và bốn file context chuẩn; lịch sử quyết định và các vòng review được lưu trong Git. |
| Phản biện hướng ban đầu | Đã loại giả định relative degree 3 toàn cục của mô hình cũ; không dùng biên độ slip đơn thuần để biện minh các đạo hàm HOCBF; phân biệt khả thi tức thời, an toàn một hold và an toàn đệ quy. |
| Formulation v2.1 | Đã áp dụng sau GPT ACCEPT và người dùng đồng ý: mô hình rút gọn 9 trạng thái, đầu vào điện áp, tham số ẩn cố định suốt execution, contact capacity và miền contact admissibility rõ ràng. HOCBF là tùy chọn/baseline. |
| G1 | **PASS trong phạm vi nhất quán nội tại của mô hình rút gọn**: hình học, dấu lực/mômen, đơn vị, năng lượng, ràng buộc contact, thông tin trạng thái và quy ước actuator đã được review. Chưa xác thực tương ứng robot thật. |
| Khung G2 | Đã có bản phân tích predictor hữu hạn phụ thuộc điện áp, residual, tube so sánh, pose lifting và kiểm tra collision/contact suốt hold. Khung giải tích được review; khả năng tính toán tổng quát và hữu ích vẫn mở. |
| Case A | **GPT ACCEPT A.1–A.23** tại `d2cd854`: chứng chỉ hữu hạn bằng số hữu tỉ cho một trường hợp tổng hợp, bao phủ toàn thời gian và mọi capacity cố định trong tập đã khai báo. |
| Case B | **GPT ACCEPT B.1–B.25** tại `1da2166`: ma trận actuator phụ thuộc tham số, bảo toàn tương quan, chứng minh quỹ đạo mô hình đi qua ngưỡng thoát bão hòa; phép đánh giá refined cho CERTIFIED trong khi hai phép đánh giá thô đã cố định cho UNKNOWN. |
| Case C | **Đã soạn C.1–C.16 và có audit nội bộ Luna; đang chờ GPT review**. So sánh ba điện áp dưới cùng trạng thái, tập tham số, error envelope và quy tắc chứng nhận. |
| Literature | Có 24 mục ban đầu, ba bổ sung G2 và supplement về validated integration/predictor-validation. Đã ghi nhận overlap; mức truy cập nguồn được phân biệt. Chưa hoàn tất systematic novelty audit. |

## 2. Case C hiện ở đâu?

[Case C](../research/theorem_notes/G2_VOLTAGE_SELECTION_CASE_C_v1.md) đề xuất kết quả cho cùng một phép đánh giá đủ:

| Điện áp giữ | Đầu ra đề xuất — chưa được GPT ACCEPT |
|---|---|
| `(0,0)` | CERTIFIED |
| `(1/4,1/4)` | CERTIFIED |
| `(1,1)` | UNKNOWN |

Đây là ví dụ tổng hợp từ trạng thái nghỉ, hai bên khớp nhau và obstacle được đặt có chủ đích ở khoảng cách micromet. Zero voltage đã an toàn. UNKNOWN không chứng minh va chạm; ví dụ không chứng minh điện áp nhỏ là cần thiết, lợi ích tracking, tính hữu ích thực tế hay ưu thế trước phương pháp khác.

[Audit Luna](reviews/LUNA_G2_CASE_C_AUDIT_R4.md) chưa thấy lỗi chặn trong phạm vi đó. Sự đồng ý của reviewer không thay thế chứng minh hoặc review độc lập GPT.

## 3. Trạng thái chính thức

| Mục | Trạng thái |
|---|---|
| Tổng dự án | **HOLD** |
| G1 — Plant consistency | **PASS — restricted reduced-model scope** |
| G2 — Certified enclosure | **UNVERIFIED** |
| G3 — Useful recursive subset | **UNVERIFIED; chưa được phép xây dựng** |
| G4 — Novelty | **UNVERIFIED** |
| Novelty chỉ dựa trên predictor/residual/tube tổng quát | **BLOCKED** |
| Tương ứng mô hình với nền tảng vật lý | **UNVERIFIED** |
| Controller, simulator, interval solver, experiments | **Chưa được phép triển khai; chưa có kết quả thực nghiệm của dự án** |

Hai chứng chỉ tổng hợp được chấp nhận là tiến bộ giải tích có thật. Chúng chưa chứng minh một bộ tính enclosure tổng quát có ích trong miền vận hành nghiên cứu, tính khả thi đệ quy hoặc đóng góp mới đủ cho bài báo.

## 4. Bước tiếp theo

1. Gửi [GPT_G2_REVIEW_REQUEST_R4.md](GPT_G2_REVIEW_REQUEST_R4.md) để GPT review Case C trên mốc nghiên cứu `547061d2cc0ce1ea0c000de0ec66054034ec930f`, hoặc commit tài liệu mới hơn có cùng nội dung toán học. GPT cần ghi rõ commit thực sự đã đọc.
2. Nhận disposition độc lập, sửa lỗi được chỉ ra nếu có, rồi ghi nhận đúng phạm vi. Không tự nâng G2 thành PASS.
3. Chốt nghĩa vụ G2 tiếp theo từ review: miền trạng thái chuyển động/quay, dữ liệu tham số có cơ sở, độ bảo thủ có ích và cấu trúc tính hữu hạn. Runtime cần giai đoạn triển khai được cho phép sau này.
4. Tiếp tục đối chiếu phương pháp validated reachability trên cùng giả định để đánh giá novelty; nhiều ví dụ tổng hợp hơn tự nó không giải quyết G4.

## 5. Hồ sơ bằng chứng

- [G1 PASS](reviews/GPT_TO_CODEX_G1_REVIEW_8341014e_PASS.md).
- [G2 enclosure candidate](../research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md).
- [Case A acceptance](reviews/GPT_G2_R2_d2cd854_ACCEPT_RECORD.md).
- [Case B acceptance](reviews/GPT_G2_R3_1da2166_ACCEPT_RECORD.md).
- [Codex R4 response](reviews/CODEX_G2_R4_RESPONSE_AND_CASE_C.md).
- [Review gates](../research_context/REVIEW_GATE.md) và [decision log](../research_context/DECISION_LOG.md).

Lưu ý đọc context: câu tổng kết cuối MASTER về việc chưa có enclosure được chấp nhận phải được đọc cùng section 3/21 và REVIEW_GATE: khung giải tích và hai hand cases đã được review; **phương pháp tính enclosure tổng quát có ích** chưa được xác nhận. Bản tổng kết này không đưa ra một kết quả toán học mới.
