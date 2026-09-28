> HISTORICAL / SUPERSEDED BY MASTER v2 (2026-09-28). Read [MASTER_RESEARCH_CONTEXT_v2.md](../research_context/MASTER_RESEARCH_CONTEXT_v2.md), DECISION_LOG, LITERATURE_MATRIX and REVIEW_GATE first. This note records earlier analysis, not the current nine-state plant or an implementation authorization. Seven-state results must not be transferred to the current plant without a new derivation.

# Quyết định nghiên cứu ban đầu

Ngày: 2026-09-28. **GO cho nghiên cứu nền tảng; HOLD cho freeze mô hình, định lý và triển khai controller.**

## Phạm vi giữ lại

- Một DDWMR; tránh vật cản tròn tĩnh; bán kính an toàn bao gồm kích thước robot và vật cản.
- Điện áp hai động cơ là đầu vào vật lý; giữ động lực học dòng điện khi chưa có chứng minh phép giảm bậc phù hợp với an toàn.
- Điện áp giới hạn, thực thi ZOH, uncertainty slip được định nghĩa cụ thể, và sai lệch tham số được chọn có chủ đích.
- Bảo đảm an toàn liên tục trên tập khởi tạo được chứng nhận; nghiên cứu khả năng thực thi của actuator và điều kiện duy trì khả thi.
- Tracker chuẩn; novelty phải nằm trong kết quả toán hoặc đặc trưng khả năng tránh va chạm do mô hình vật lý mang lại.
- HOCBF là phương án cần đánh giá. Không khóa phương pháp chỉ vì subtitle ban đầu đã nêu HOCBF.

## Những chỗ phải sửa trước khi chốt

| ID | Vấn đề | Điều kiện để đóng |
|---|---|---|
| G1 | Độ mới chưa xác nhận ở mức phương trình | Đọc và đối chiếu theorem/assumptions của các bài gần nhất; tách full text, abstract và lead chưa xác minh |
| G2 | Mô hình slip chưa đóng về vật lý | Chọn rõ slip truyền động hạn chế hay mô hình có vận tốc thân xe/lực tiếp xúc; không dùng mô hình bánh khóa => thân dừng để claim chống skid |
| G3 | Relative degree suy biến | Chứng minh miền áp dụng và hành vi ở biên miền, hoặc xây chứng nhận khác xử lý được singularity |
| G4 | Handoff gộp feasibility với viability | Tách tập khả thi tức thời, tập an toàn một hold, tập chứng nhận đệ quy, và viability kernel |
| G5 | Chưa có bảo đảm đệ quy mang tính xây dựng | Có tập khởi tạo không rỗng, action chung cho mọi uncertainty, safe hold và endpoint quay về tập chứng nhận, kèm chứng minh |
| G6 | Giả định chưa gắn với thông tin controller | Nêu rõ state/current/slip nào đo được, sai số nào được chặn, bounds lấy từ đâu, driver/phanh nào được giả định |

Phân tích cụ thể và phản ví dụ nằm trong [ROOT_MATH_REVIEW.md](reviews/ROOT_MATH_REVIEW.md). Bài toán con để đánh giá tác dụng thực sự của điện cảm và dòng điện ban đầu nằm trong [PHYSICAL_AUTHORITY_PROBE.md](reviews/PHYSICAL_AUTHORITY_PROBE.md).

## Claims hiện không được dùng

- Đã chứng minh toàn bộ `{h>=0}` bất biến dưới điện áp giới hạn.
- QP infeasible đồng nghĩa robot chắc chắn không còn tránh được va chạm.
- Mọi state trong tập khả thi tức thời đều an toàn vô hạn thời gian.
- Chỉ cần biên độ slip là đủ cho mọi đạo hàm HOCBF.
- Kết hợp đủ các keyword trong title tự động tạo novelty.
- Baseline dùng sai mô hình bị va chạm chứng minh theorem của baseline sai.
- Điểm tự chấm 85/100 là bằng chứng Q1-ready.

## Phân công được giữ

**Luna max:** soạn artifacts nghiên cứu giai đoạn 1; sau khi nền tảng được chấp nhận mới thực hiện toàn bộ specification, code, thí nghiệm và gói tái lập theo super task. Không tự thay giả định để làm QP chạy được.

**Root + GPT nghiên cứu:** phản biện mô hình, novelty, proof, fairness và kết quả; kiểm tra độc lập các kết luận quan trọng. GPT là đối tác phản biện trong workflow, không phải nguồn chứng minh.

**Người dùng/nhóm nghiên cứu:** chấp nhận formulation cụ thể trước khi mở giai đoạn triển khai theo yêu cầu trong handoff mục 22. Hiện chưa có formulation đạt điều kiện để đề nghị chấp nhận; tiếp tục xử lý các blocker nghiên cứu trước.

## Trạng thái phần mềm

Repo độc lập đã tạo. Chưa viết hay chạy controller/simulation. Chưa có kết quả collision, benchmark, Monte Carlo hoặc hardware. Deliverable 6 chưa được mở.
