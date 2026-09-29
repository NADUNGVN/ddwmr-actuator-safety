# DDWMR — yêu cầu review tổng hợp và trả về một file Markdown

## 0. Yêu cầu của người dùng và sản phẩm phải trả về

Người dùng muốn gửi GPT **một lượt**, nhận lại **một file `.md` đầy đủ** để chuyển cho Codex. Hãy thực hiện toàn bộ phạm vi review dưới đây trong cùng một báo cáo, thay vì chỉ review Case C rồi lần lượt yêu cầu thêm các ví dụ nhỏ ở những lượt sau.

**Bắt buộc tạo file đính kèm có thể tải xuống:**

`GPT_TO_CODEX_DDWMR_CONSOLIDATED_REVIEW_FULL_HANDOFF.md`

- Ghi toàn bộ findings, kiểm tra phương trình, disposition, danh sách công việc còn lại, tiêu chí nghiệm thu và các đề xuất sửa chính xác vào file này. Không chỉ trả lời trong chat hoặc hứa sẽ tạo file.
- Chat cuối chỉ cần tóm tắt ngắn bằng tiếng Việt và cung cấp link tải file.
- Nếu môi trường thực sự không hỗ trợ tạo file, nói rõ giới hạn đó và trả toàn bộ nội dung Markdown trong **một code block duy nhất**, với tên file trên để người dùng lưu. Không được nói đã tạo attachment nếu chưa tạo.
- File phải tự đủ ngữ cảnh cho Codex: repo, commit đã đọc, authority, phạm vi đã review, bằng chứng, mục chưa truy cập được và trạng thái gate.
- Tóm tắt và hướng dẫn thực hiện bằng tiếng Việt; phần toán và thuật ngữ có thể dùng tiếng Anh.

## 1. Repository và snapshot

- Repository: <https://github.com/NADUNGVN/ddwmr-actuator-safety>
- Branch: `main`.
- Snapshot bằng chứng cho yêu cầu này: **`0156ddbe9dcba15a8beb20396467867839e7d233`**.
- Mốc toán học Case C: `547061d2cc0ce1ea0c000de0ec66054034ec930f`.
- Formulation authority: **MASTER v2.1**, giữ tên file `research_context/MASTER_RESEARCH_CONTEXT_v2.md`.

Hãy ghi **commit thực tế đã đọc**. Có thể đọc snapshot trên để tránh nhầm với cập nhật sau này. Nếu đọc main mới hơn, chỉ rõ thay đổi liên quan; không trộn phương trình từ nhiều phiên bản mà không ghi provenance.

Đây là nghiên cứu DDWMR của thầy Viễn. **PACE-Seg, segmentation, routing trên Hailo/TensorRT và bản thảo Image and Vision Computing không thuộc project này.**

## 2. Đọc bắt buộc, theo thứ tự

### A. Authority và trạng thái

1. `AGENTS.md`
2. `research_context/MASTER_RESEARCH_CONTEXT_v2.md`
3. `research_context/DECISION_LOG.md`
4. `research_context/LITERATURE_MATRIX.md`
5. `research_context/REVIEW_GATE.md`
6. `docs/PROGRESS_SUMMARY_2026-09-29.md`

### B. Kết quả giải tích và review trước

7. `research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md`
8. `docs/reviews/GPT_TO_CODEX_G2_REVIEW_7390942f_FULL_HANDOFF.md`
9. `research/theorem_notes/G2_FINITE_CERTIFICATE_CASE_A_v1.md`
10. `docs/reviews/GPT_G2_R2_d2cd854_ACCEPT_RECORD.md`
11. `research/theorem_notes/G2_CHALLENGE_CASE_B_v1.md`
12. `docs/reviews/GPT_G2_R3_1da2166_ACCEPT_RECORD.md`

Các ACCEPT_RECORD là bản ghi có cấu trúc của review người dùng chuyển lại, không phải transcript nguyên văn. Không cần kiểm lại mọi phép tính A/B nếu không có dependency hoặc mâu thuẫn mới; phải hiểu phạm vi chấp nhận của chúng.

### C. Case C đang chờ review

13. `research/theorem_notes/G2_VOLTAGE_SELECTION_CASE_C_v1.md`
14. `docs/reviews/CODEX_G2_R4_RESPONSE_AND_CASE_C.md`
15. `docs/GPT_G2_REVIEW_REQUEST_R4.md`
16. `docs/reviews/LUNA_G2_CASE_C_AUDIT_R4.md`

Luna audit là ý kiến reviewer phụ trợ, không phải bằng chứng thay cho phương trình.

### D. Novelty threats

17. `docs/reviews/G2_PRIOR_ART_AND_BLOCKERS_v1.md`
18. `docs/reviews/G2_PRIOR_ART_SUPPLEMENT_R2.md`

Nếu không truy cập được repo hoặc file quan trọng, ghi chính xác phần thiếu. Không giả vờ đã đọc và không nâng trạng thái dựa trên tên file hoặc bản tóm tắt. Gom mọi yêu cầu tài liệu thiếu vào một danh sách duy nhất trong output.

## 3. Trạng thái đầu vào — không được nhầm với kết quả mới

| Mục | Trạng thái hiện hành |
|---|---|
| G1 | PASS, chỉ nhất quán nội tại mô hình rút gọn |
| Case A A.1–A.23 | GPT ACCEPT, chứng chỉ hữu hạn tổng hợp |
| Case B B.1–B.25 | GPT ACCEPT, chứng chỉ hữu hạn tổng hợp và các kết luận hẹp đã nêu |
| Case C C.1–C.16 | Draft có audit Luna; chờ review GPT |
| G2/G3/G4 | UNVERIFIED |
| Generic-method novelty | BLOCKED |
| Physical-platform correspondence | UNVERIFIED |
| Tổng dự án | HOLD |

Mô hình hiện hành có 9 trạng thái `[p_x,p_y,theta,u,r,omega_L,omega_R,i_L,i_R]`, đầu vào `[V_L,V_R]`, tham số ẩn cố định suốt execution, known fixed contact law và fixed-period voltage ZOH. Phải giữ một điện áp chung cho mọi realization, không cho controller biết tham số thật. G1 không xác thực mô hình lốp, load transfer hoặc driver phần cứng.

Scope được phép ở lượt này: **review tổng hợp, nghiên cứu giải tích G2 và lập kế hoạch điều kiện cho các gate còn lại**. Đây không phải yêu cầu xây dựng G3, chạy solver, controller, simulator, experiment hay ban hành GO. Đề xuất chuyển giai đoạn phải tách khỏi việc đã được người dùng cho phép.

## 4. Năm phần phải xử lý trong cùng một lượt

### Phần I — Kết luận dứt điểm đối với Case C hiện có

Kiểm tra C.1–C.16 ở mức phương trình, bao gồm:

1. Parameter image và tương quan matched-side; chuẩn hóa đơn vị, gear witness, initial rest và quantifier.
2. Symmetry chính xác nhờ uniqueness; không gán symmetry cho toàn bộ error box hoặc cho độc lập bất định hai bên của mô hình chung.
3. C.3–C.6: dấu và bounds của motor kernel, predictor branch, sự phụ thuộc điện áp của body/pose center.
4. C.7–C.9: các hệ số residual, Delta r=0 của predictor và full six-state Metzler comparison; phân biệt signed row sums với induced norm.
5. C.10–C.13: generic pose lift, cùng error envelope cho cả ba action và full-hold directional center evaluation.
6. C.14–C.16: contact reserve, margin và proposition.

Các đầu ra đang được đề xuất là `(0,0): CERTIFIED`, `(1/4,1/4): CERTIFIED`, `(1,1): UNKNOWN`. Hãy kiểm độc lập ba margin `13/2000000`, `67/18000000`, `-83/18000000` m và contact lower bound `1999/1000` N.

Ra một disposition rõ: **ACCEPT trong phạm vi nào / NEEDS REVISION với lỗi chính xác / BLOCKER / UNVERIFIED vì thiếu gì**. Không đồng nhất UNKNOWN với unsafe. Exact rest, zero action đã an toàn, matched sides và engineered micrometer clearance phải xuất hiện trong kết luận.

### Phần II — Kiểm tra toàn bộ phần G2 còn thiếu

Không chỉ yêu cầu “làm Case D”. Hãy xác định **gói bằng chứng tối thiểu đủ để đóng G2** cho scope hiện hành:

- Đã chứng minh gì tổng quát, gì chỉ đúng trong A/B/C, gì chưa có evaluator hữu hạn?
- Trên miền nào các primitive có thể tính với sai số bao ngoài được kiểm chứng? Cần dữ liệu hữu hạn nào cho phi, Theta và initial/input domain?
- Điều kiện đủ cho safety, khả năng kết thúc phép tính, và khả năng trả CERTIFIED trên miền có ích khác nhau thế nào? Không yêu cầu một sufficient test phải quyết định được mọi boundary case.
- “Useful conservatism” phải được đo/định nghĩa thế nào để không dựa vào obstacle tuning hoặc chỉ trạng thái nghỉ?
- Cần moving/turning states, uncertainty bất đối xứng hoặc stiff actuator ở mức nào? Phân biệt điều kiện bắt buộc của claim với stress test tùy chọn; không âm thầm yêu cầu tất cả như giả định MASTER mới.
- Dữ liệu tổng hợp có tài liệu benchmark rõ có đủ cho reduced-model paper không? Điều nào thực sự cần literature-supported parameters, điều nào cần platform identification riêng?
- Trường hợp mọi action trả UNKNOWN được xử lý/diễn giải ra sao, khi chưa có recursive backup?

**Kiểm tra vòng phụ thuộc trong gate:** code hiện bị chặn đến khi G1–G4 pass, nhưng runtime/general evaluator lại đang được liệt kê là nghĩa vụ G2. Hãy xác định có vòng phụ thuộc thật không. Nếu có, đề xuất chính xác cách tách analytic acceptance, validation-only implementation và controller implementation, hoặc cách giữ gate bằng một nghĩa vụ giải tích phù hợp. Đây chỉ là **đề xuất sửa gate chờ người dùng chấp thuận**, không phải cho phép tự code. Không giả định runtime đã được chứng minh từ hand certificate.

### Phần III — G3: đánh giá khoảng trống và điều kiện mở nhánh

G3 chưa được phép xây dựng. Lượt này chỉ review specification và đánh giá tính khả thi của hướng đi:

- Liệt kê chính xác lemma/assumption/endpoint obligation còn thiếu để có một tập K_T hữu ích với `K_T subset Pre_T^c(K_T)`.
- Kiểm tra có đang lén dùng finite stopping distance, sustained wheel lock, zero-voltage emergency brake, matched-side symmetry hoặc oracle knowledge không.
- Phân biệt one-hold certificate, sampled-state recursion và exact history-dependent viability.
- Xác định đầu vào G2 nào phải có trước khi mở G3; đề xuất tiêu chí nghiệm thu G3 có thể kiểm tra.
- Nếu scope hiện hành chưa có đường chứng minh đáng tin, ghi BLOCKER của nhánh liên quan và những lựa chọn reformulation **có điều kiện**, không thêm giả định vào MASTER.

Không dựng một K_T mới hoặc tuyên bố G3 PASS chỉ từ generic predecessor induction.

### Phần IV — G4: novelty audit tập trung và quyết định hướng nghiên cứu

Đọc các nguồn chính gần nhất trong khả năng truy cập, ưu tiên đối chiếu:

- componentwise/growth-matrix reachability;
- validated integration với fixed uncertain parameters;
- predictor-validation của Houska/Villanueva/Chachuat;
- Ariadne, Flow* hoặc công cụ phù hợp với regularity của phi đang xét;
- sampled-data/zero-order CBF và bounded-input feasibility khi thực sự liên quan đến claim.

Ghi source URL/DOI, phiên bản, equation/theorem/page/section đã kiểm và giới hạn truy cập. Không suy đoán tính bao phủ từ title; không coi nguồn không đọc được là không có kết quả tương tự.

Tạo bảng:

| Proposed claim | Closest prior result and locator | Matched assumptions | Actual difference supported | Remaining comparison | Verdict |
|---|---|---|---|---|---|

Trả lời thẳng: **còn contribution hypothesis nào đáng theo đuổi và bằng chứng nào có thể bác bỏ/xác nhận nó?** Nếu hiện chỉ là áp dụng công cụ có sẵn vào plant mới, hãy nói rõ. Không cứu novelty bằng số lượng simulations hoặc nhiều hand cases.

Thiết kế matched comparison tối thiểu ở mức đặc tả, chưa chạy: cùng model/law, parameter dependence, initial set, held input, horizon, arithmetic certification, collision/contact tests và tiêu chí UNKNOWN. Không chọn baseline không đáp ứng regularity rồi suy ra ưu thế giả.

### Phần V — Một kế hoạch tổng hợp có điểm dừng

Kết luận còn **ba gate G2/G3/G4**, nhưng không coi chúng là ba phép kiểm đơn giản hoặc hứa một review sẽ đóng tất cả.

Gom các nghĩa vụ thành số lượng work packages tối thiểu có dependencies rõ. Với mỗi package ghi:

| ID | Gate | Concrete deliverable | Required input | Acceptance criterion | Failure/reformulation criterion | Owner | Dependency | Authorization needed |
|---|---|---|---|---|---|---|---|---|

- Có thể giao Luna max soạn tài liệu/phần giải tích đã được cho phép; root Codex và GPT giữ vai trò review. Code chỉ được giao sau authorization phù hợp.
- Phân biệt mục bắt buộc để tiếp tục, mục chỉ cần trước submission, mục physical transfer và extension tùy chọn.
- Nêu những package có thể gộp thực hiện để giảm số lần chuyển tài liệu qua người dùng.
- Không bịa ước lượng thời gian hoặc hứa số vòng review cố định.
- Không kết thúc bằng một chỉ dẫn mơ hồ như “explore more”, “do more experiments” hay “make Case D”; mỗi mục phải có điều kiện đóng cụ thể.
- Ra một khuyến nghị nghiên cứu: tiếp tục scope hiện tại, cần sửa scope/gate, hoặc dừng một nhánh do blocker. Phân biệt khuyến nghị với trạng thái authoritative đã được áp dụng.

## 5. Cấu trúc bắt buộc của file output

1. **Executive summary bằng tiếng Việt**: đạt gì, còn gì, khuyến nghị và bước tiếp theo.
2. **Repository/commit/read ledger**: file nào đã đọc, nguồn nào không truy cập được.
3. **Case C equation-level audit** với disposition.
4. **Consolidated G2 findings**, bao gồm audit dependency của implementation gate.
5. **G3 readiness and missing obligations** — không construction hoặc PASS chưa có bằng chứng.
6. **G4 source-level comparison and novelty disposition**.
7. **Gate table**, tách trạng thái hiện tại, kết quả review mới, đề xuất thay đổi và authorization cần thiết.
8. **One consolidated work-package plan**, dependencies và tiêu chí đóng.
9. **Exact proposed document edits**, nếu cần, có path + section + old/new text hoặc unified diff; chỉ đề xuất, không mặc nhiên áp dụng. Tách lỗi metadata khỏi thay đổi giả định/formulation.
10. **Single Codex handoff instruction**: việc nào Codex có thể làm ngay trong quyền hiện có, việc nào cần người dùng quyết định, việc nào bị chặn; artifact names cụ thể.

Mỗi finding dùng đúng:

**Finding / Evidence / Consequence / Status / Required action**

Đồng thời có bảng tổng kết:

| Item | Analytic soundness | Finite certification | Usefulness | Novelty | Gate effect |
|---|---|---|---|---|---|

Đối với điểm chưa thể kiểm, ghi UNVERIFIED với bằng chứng còn thiếu. Nếu phát hiện lỗi, nêu hệ quả xuống các claim phụ thuộc; dừng nhánh đó và vẫn review các nhánh độc lập. Không tự sửa assumption để làm theorem đúng.

## 6. Kỷ luật kết luận

- Không lặp lại G1 từ đầu trừ khi có mâu thuẫn mới cụ thể.
- A/B ACCEPT không đồng nghĩa G2 PASS; Case C nếu ACCEPT cũng không tự đóng G2.
- Không nhận định physical safety từ reduced-model certificate.
- Không dùng model agreement, floating simulation hoặc sample-only checks làm proof.
- Không tuyên bố Q1 readiness, first, practical superiority hoặc recursive safety khi thiếu bằng chứng.
- Giữ HOLD cho đến khi các nghĩa vụ thật sự được giải quyết và quyết định cần thiết được ghi nhận đúng quy trình.
- Không đổi MASTER, không triển khai controller/simulator/solver/experiment, không mở G3 qua một câu kết luận review.

**Hãy hoàn thành review tổng hợp và xuất file `GPT_TO_CODEX_DDWMR_CONSOLIDATED_REVIEW_FULL_HANDOFF.md` ngay trong lượt trả lời này, kèm link tải.**
