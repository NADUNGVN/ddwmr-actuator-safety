# DDWMR — đối chiếu scope và tiến độ

**Ngày:** 2026-10-07. **HEAD kiểm tra:** `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`.

Đây là báo cáo đối chiếu bằng chứng và đề xuất thứ tự nghiên cứu. Báo cáo không sửa MASTER, nâng gate, cấp GO chạy query, hoặc thay đổi các artifact đã lưu. Không commit/push.

## A. Finding — đích nghiên cứu hiện hữu

Giữ MASTER v2.1: chứng nhận tránh va chạm và duy trì điều kiện tiếp xúc của **mô hình robot vi sai rút gọn**, với chín trạng thái, điện áp giữ cố định trong mỗi chu kỳ và tham số ẩn cố định trong toàn bộ thực thi. Chướng ngại vật của công thức hiện tại là hình tròn tĩnh; bán kính an toàn bao gồm toàn bộ footprint.

G2 chứng nhận toàn bộ một chu kỳ. Đích đầy đủ còn gồm G3: tập trạng thái hữu ích và quy tắc chọn điện áp để tiếp tục an toàn qua nhiều chu kỳ. G3 chưa được xây dựng. Scope một chu kỳ riêng lẻ chưa được thông qua làm đích paper thay thế.

Đây là hướng paper lý thuyết/phương pháp trên mô hình đã khai báo. MATLAB và phần cứng không phải điều kiện bắt buộc của hướng này. Một tuyên bố an toàn cho robot thật cần bằng chứng tương ứng mô hình–phần cứng riêng.

## B. Evidence — đối chiếu trực tiếp trong lượt này

Đã đọc AGENTS và bốn file canonical; đối chiếu các review R3, G2 R21/R26 và G4 R21/R22/R24. R26/R24 vẫn là các handoff mới nhất tại thời điểm kiểm tra.

| Bằng chứng | Kết quả đối chiếu | Phạm vi được hỗ trợ |
|---|---|---|
| G1 | PASS theo review độc lập đã lưu | Nhất quán nội bộ của mô hình rút gọn |
| Cases A/B/C | Các acceptance record vẫn có hiệu lực | Các ca tổng hợp cụ thể |
| R3 | Đếm lại 1.944 ID duy nhất, 1.944 proof object; 1.196 CERTIFIED, 748 UNKNOWN | Batch tổng hợp đã khai báo |
| R3 archive | Hash gzip, hash/size dữ liệu giải nén, số bản ghi và summary đều khớp: 6/6 đối chiếu | Toàn vẹn dữ liệu lưu trữ |
| R3 replay | Báo cáo cũ ghi 1.944/1.944 replay | Không chạy lại checker trong lượt này |
| R5 | Manifest vẫn có 800/800 NOT_RUN | Các hàng phát triển riêng không phải study completion |
| G4 pilot | Đếm lại 10 cặp; R3 6 CERTIFIED, Auer 9 CERTIFIED; 3 ca chỉ Auer chứng nhận, 0 ca ngược lại | Pilot có chủ đích, không phải mẫu thống kê |
| G4 provenance | Rehash 156/156 input artifact khớp cả SHA-256 và kích thước | Toàn vẹn artifact pilot |
| G2 R26 / G4 R24 | Hai hash handoff khớp review đã lưu | Tài liệu mới nhất không đổi |

Việc kiểm tra dùng đọc JSON/gzip, đếm bản ghi và tính hash; không gọi solver, worker, query, stage hay batch. Đây không phải một lượt chứng minh lại toàn bộ implementation.

## C. Consequence — nút khoa học còn lại

Nền tảng chứng nhận hữu hạn và công cụ lưu/replay bằng chứng đã có. Tuy nhiên, chưa chứng minh được **một cách chọn điện áp hữu ích cho nhiệm vụ** và **đóng góp vượt khỏi việc áp dụng phương pháp reachability chung**.

- Pilot Auer là bằng chứng bất lợi cho claim ưu thế coverage của R3 hiện tại. Nó không chứng minh Auer luôn trội hơn.
- G2 R21 đã phản chứng yêu cầu tiến độ của cặp R17 đã dùng: cải thiện enclosure không thể làm cặp đó đạt ngưỡng đã khóa.
- R22–R24 có một lemma xếp hạng hai điện áp trên miền tổng hợp hẹp. Lemma chưa cung cấp nhiệm vụ có ý nghĩa hoặc đóng góp mới đủ cho paper.
- CommonRoad R26 có vật cản chữ nhật chuyển động và mục tiêu nhiều bước; nó không phải benchmark phù hợp nguyên trạng với G2 hiện tại. Dừng nhánh tìm dữ liệu này.

Hướng gần hạn: phát biểu một cải tiến DDWMR cụ thể làm giảm độ rộng/bảo thủ của bound trên miền có chuyển động và bất định có độ rộng dương. Giữ tương quan, predictor và augmented parameters là các hướng kỹ thuật đã có prior art; bản thân chúng không phải novelty. Cải tiến phải có bất đẳng thức hoặc hiệu quả tính toán cụ thể có thể bị phản chứng.

## D. Status — tiến độ và giới hạn của con số

**HOLD; G1 restricted PASS; G2/G3/G4 và physical correspondence UNVERIFIED.** Chỉ một trong bốn gate đã PASS; các gate có lượng công việc khác nhau.

Ước lượng quản lý cho **đường tới paper đủ bằng chứng theo đích MASTER hiện hữu: khoảng 30–40%, điểm giữa 35%**. Đây không phải tỷ lệ gate hoàn thành, điểm chất lượng, xác suất nhận bài hay dự báo thời gian.

| Nhóm mốc | Trọng số đề xuất | Phần đã ghi nhận |
|---|---:|---:|
| Mô hình và phạm vi/G1 | 15 | 15 |
| Bound một chu kỳ, finite validation và usefulness/G2 | 25 | 15 |
| Đóng góp và so sánh prior art/G4 | 20 | 5 |
| Tập an toàn và chính sách nhiều chu kỳ/G3 | 25 | 0 |
| Kết quả cuối, hình, bản thảo và review | 15 | 0 |
| Tổng | 100 | 35 |

Trọng số là cách quản lý để minh bạch ước lượng, không phải quy tắc acceptance mới. Nếu cần đổi phương pháp/đích đóng góp, ước lượng có thể giảm. Tỷ lệ R3 CERTIFIED 1.196/1.944 ≈ 61,5% chỉ là coverage của batch đó.

## E. Required action — bốn mốc còn lại

1. **G2:** dùng một nhiệm vụ tổng hợp một chu kỳ phù hợp MASTER, công khai miền trạng thái/tham số, điện áp, hình học và tiêu chí thành công trước kết quả. Sàng lọc khả thi rồi chứng minh một bound DDWMR cải tiến có tác dụng lên quyết định điện áp. Existing 800-row proposal là dữ liệu phát triển; chưa mở batch và không hồi sinh cặp R17 đã bị phản chứng.
2. **G4:** audit đúng cải tiến đó ở mức phương trình, rồi so sánh matched với Auer trên workload mới đã khai báo tiêu chí coverage/cost trước. Chỉ mở thực thi khi có phương pháp đủ sound và câu hỏi so sánh cụ thể. Nếu không có đóng góp bảo vệ được, đổi hướng trước khi đầu tư G3.
3. **G3:** sau khi kết quả G2 đủ sound/hữu ích và có assignment riêng, xây dựng tập trạng thái cùng quy tắc chọn điện áp, chứng minh an toàn trong hold và endpoint quay về tập để nối tiếp nhiều chu kỳ.
4. **Paper:** đóng bằng chứng, protocol và artifact; viết câu chuyện khoa học, tạo hình từ dữ liệu, kiểm tra bản thảo/PDF và review độc lập.

Bước ngay của Codex là đặc tả một claim cải tiến có thể kiểm chứng và một phép thử khả thi, không tăng số query trước khi rõ claim. LUNA-G2-SCOPE phụ trách phân tích/candidate bound; LUNA-G4-AUER phụ trách kiểm tra overlap của claim đó. Hai phiên chưa nhận assignment thực thi mới từ báo cáo này.

## Nguồn đối chiếu

- [MASTER v2.1](../../research_context/MASTER_RESEARCH_CONTEXT_v2.md), §§15, 20–24, 28, 31–32.
- [R3 scientific acceptance](GPT_TO_CODEX_G2_VALIDATION_R3_SCIENTIFIC_REVIEW_FULL_HANDOFF.md).
- [R3 summary](../../results/validation/g2/r3/full_grid_summary_r3_v1.json).
- [G4 pilot review](CODEX_G4_AUER_R21_PILOT_SCIENTIFIC_TRIAGE_REVIEW.md).
- [G4 contribution falsification](CODEX_G4_AUER_R22_CONTRIBUTION_FALSIFICATION_REVIEW.md).
- [G2 task counterexample](CODEX_G2_R21_PAIR_FEASIBILITY_ADVERSARIAL_AUDIT_REVIEW.md).
- [G2 R26 task screen](CODEX_G2_R26_PROSPECTIVE_FORMAL_TASK_SCREEN_REVIEW.md).
- [G4 R24 prior-art review](CODEX_G4_AUER_R24_ACTION_ORDERING_PRIOR_ART_AUDIT_REVIEW.md).
