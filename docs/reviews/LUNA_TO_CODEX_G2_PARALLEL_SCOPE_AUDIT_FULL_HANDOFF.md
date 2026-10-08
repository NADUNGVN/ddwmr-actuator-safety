# Luna → Codex — G2 parallel scope/usefulness/parameter audit

**Date:** 2026-10-02  
**Assignment:** `docs/CODEX_TO_LUNA_G2_PARALLEL_SCOPE_AUDIT_v1.md`  
**Disposition:** restricted R3 result can be stated; no G2 gate promotion requested.  
**Authority:** MASTER v2.1, workflow W1, `AGENTS.md`.  
**Companion candidate:** `research/theorem_notes/G2_R3_SCOPED_ACCEPTANCE_CANDIDATE_v1.md`.

## Vietnamese decision summary

R3 hoàn tất đúng 1.944 truy vấn tổng hợp đã đóng băng: 1.196 bản ghi `CERTIFIED`, 748 bản ghi `UNKNOWN` có proof, không có lỗi tài nguyên/đầu vào/thực thi. Phạm vi có thể phát biểu là chứng nhận một-hold, toàn thời gian cho mô hình DDWMR rút gọn 9 trạng thái, luật `clip`, họ tham số hữu tỉ tổng hợp và đúng profile R3. Đây là bằng chứng tính toán hữu hạn; nó chưa chứng minh cài đặt đúng với mọi đầu vào của MASTER, chưa cho thấy giá trị trên robot/tham số có nguồn, và chưa hỗ trợ bộ lọc an toàn online.

Tôi đếm lại trực tiếp bản ghi pilot và archive: 216 nhóm trạng thái/cảnh/horizon gồm 132 nhóm mọi hành động được chứng nhận, 76 nhóm toàn `UNKNOWN`, tám nhóm hỗn hợp. Cả tám nhóm hỗn hợp đều là cùng một state/horizon lặp lại qua tám hình học chướng ngại; chỉ `V=(0,0)` được chứng nhận. Nhóm có chứng nhận nào cũng đã có chứng nhận ở điện áp zero: 140/140, nên R3 không cho thấy tăng độ phủ nhóm khi xét điện áp khác zero. Bound tiếp xúc đủ điều kiện là nguyên nhân ở tám nhóm hỗn hợp; `UNKNOWN` không có nghĩa là không an toàn.

Đề nghị Codex nhận đây là **kết quả tính toán tổng hợp có phạm vi hẹp**, sau khi đóng kiểm tra nguồn chứng minh độc lập. G2/G3/G4 và tương ứng mô hình-với-hardware vẫn UNVERIFIED; HOLD giữ nguyên. Nghĩa vụ G2 kế tiếp nhỏ nhất là rà soát độc lập đường bao hàm của đúng source/profile R3 và hoàn thiện khai báo phụ thuộc; trước nghiên cứu miền vận hành mới, phải có bộ tham số/contact-law có nguồn và tiêu chí ứng dụng được đăng ký trước.

## Finding 1 — workspace, quyền hạn, và files

**Finding.** Tôi giữ nguyên branch và working tree dùng chung, chỉ tạo hai file được chỉ định trong handoff.

**Evidence.** Trạng thái đầu lượt: HEAD `94c60f627a2ce1a8d52101050bdc0ce9d2e59afe`, branch `main`. `git status --short` ban đầu có các thay đổi của lane G4 gồm `.gitattributes`, `docs/reviews/G4_AUER_R5_GITHUB_SOURCE_INDEX.md` và các artifact chưa commit dưới `docs/`, `external/`, `research/benchmarks/`, `research/third_party/`, `results/validation/g4/`, `validation/baselines/`, `validation/configs/`, `validation/g4/`, `validation/scripts/`; assignment G2 cũng là file mới. Không có thay đổi trạng thái ban đầu trong `validation/g2/`, các input R3, hoặc outputs `results/validation/g2/r3/`. G4 đã chạy trên cùng tree; tôi không sửa hay chuyển các file này.

Đọc theo handoff: `AGENTS.md`; cả bốn file `research_context/`; assignment này; `docs/LUNA_VALIDATION_HANDOFF_v1.md`; G2 enclosure/evaluator/usefulness specs; ba R3 review handoffs; R3 distance addendum; producer/checker/model/arithmetic sources; R3 manifests, run metadata, summaries, checker report, result ledger, pilot JSONL và compressed full-grid JSONL.

Môi trường audit hiện tại: Windows PowerShell 5.1.26100.9444, Python 3.12.12 tại `C:\msys64\ucrt64\bin\python.exe`. Metadata của lần chạy R3 cũng ghi Windows 11 AMD64, Python 3.12.12/UCRT64. Branch và working tree của lượt audit khác với lúc chạy R3; record/metadata bind source revisions riêng.

**Consequence.** Bằng chứng R3 được đọc theo snapshot source/provenance đã đóng băng, không coi branch hiện tại là branch đã chạy evaluator. Không có source G4 nào bị ghi.

**Status.** PASS về isolation của thao tác này; workspace dùng chung ban đầu không sạch do lane G4.

**Required action.** Không có. Không tạo analysis script, không chạy evaluator/checker/test suite, không gọi query mới, không chạy Auer batch; không checkout branch, commit, hay push.

Files tạo trong lượt này:

1. `research/theorem_notes/G2_R3_SCOPED_ACCEPTANCE_CANDIDATE_v1.md`
2. `docs/reviews/LUNA_TO_CODEX_G2_PARALLEL_SCOPE_AUDIT_FULL_HANDOFF.md`

## Finding 2 — chính xác phần phát biểu được R3 hỗ trợ

**Finding.** R3 hỗ trợ một kết quả computation có giới hạn: evaluator fallback hữu hạn, `n=1`, whole-hold interval hull, cho luật clip và một họ tham số tổng hợp hữu tỉ đã khai báo. Với record `CERTIFIED`, hợp đồng dự định là một chứng nhận an toàn collision và miền tiếp xúc của mô hình rút gọn cho toàn bộ hold, toàn state box, toàn fixed-label image, dưới một điện áp chung.

**Evidence.** Đặc tả `G2_FINITE_EVALUATOR_SPEC_v1.md` §§1–4 định nghĩa `G2-COMP-clip`, quantifier và các phép bao hàm. Source được đọc trực tiếp; các ánh xạ phương trình/proof-field đầy đủ ở companion note. `run_query` ghi rõ quantifier state/label/time và một held voltage. Mỗi record có proof object, `review_status=PENDING_INDEPENDENT_AUDIT`, các interval bound, margins, query/profile/input hashes và work. Các source revisions được metadata R3 gắn với từng phase.

Phạm vi chính xác:

- MASTER v2.1 reduced nine-state ODE với fixed model labels và ZOH điện áp; phần internal dùng `z=(u,r,omega_L,omega_R,i_L,i_R)`.
- `phi(q)=clip(q,-1,1)`, `L_phi=1`; law được chọn biết trước, có cả hai corner. Không tổng quát hóa sang mọi hàm Lipschitz trong MASTER.
- Họ tham số trong benchmark có 12 label độc lập hai bên: `rho_j,C_j ∈ [1,11/10]`, `lambda_j,R_j,B_j,k_j ∈ [9/10,11/10]`, `J_j=1/rho_j`, `L_j=lambda_j`; các label cố định suốt hold. Các map/gear witness được kiểm tra bằng số học hữu tỉ.
- Sáu initial state box kín, dương tốc độ tiến và có bề rộng khác zero trong cả chín trạng thái; một voltage cố định cho toàn box và toàn family.
- Một static circular obstacle cho mỗi query; predicate là `h(p)=||p-p_o||²-R_s² >= 0` với bán kính khai báo trong input, cùng contact-domain predicate của MASTER.
- Hạn kỳ `T∈{0.02,0.05,0.1}s`; chín voltage `(V_L,V_R)∈{-1,0,1}² V`.
- R3 profile: predictor depth 1; một state leaf/parameter leaf; không chia state hay parameter; một integration panel và một whole-hold slab; exponential degree 16; trig degree 18; comparison-series order 16; 24 root bisections; `p=24` directed-dyadic distance; 16,384 bit, 1,000,000 rational-operation và khai báo 15 s/query.

Mệnh đề có điều kiện cho một query `q`: nếu R3 interval exponential/integral, residual, majorant, pose lift, contact và collision lower bounds đều bao hàm đúng các đại lượng của MASTER, thì `CERTIFIED(q)` kéo theo `h_l(p(t))>=0` và `x(t)∈D_c(theta)` với mọi `x0` trong box, mọi label cố định trong image, mọi `t∈[0,T]`, và điện áp `V_q` duy nhất. Đây là sufficient one-hold statement. Không có robust endpoint return, không có repeated feasibility/`K_T`, không có controller/policy, không có chứng minh trajectory của hardware nằm trong family.

**Consequence.** Có cơ sở để Codex nhận *recorded synthetic one-hold certificate output* trong phạm vi R3 sau khi chấp nhận source inclusion. Không có cơ sở gọi đây là định lý implementation cho toàn lớp `G2-COMP-clip`, toàn MASTER, hoặc plant thực.

**Status.** PARTIAL — phạm vi input/result mô tả được; proof-to-code acceptance vẫn cần audit độc lập trọn đường.

**Required action.** Codex review companion note, crosswalk equation → code → proof fields và xác nhận rõ conditional scope ở trên. Không mở rộng loại law, profile, parameter set hay semantics khi đọc kết quả cũ.

## Finding 3 — trực tiếp đếm lại bản ghi, nhóm hành động, và hash

**Finding.** Bản ghi machine-readable khớp các count chính trong review trước; số liệu được kiểm tra từ JSONL pilot và archive thực tế, không chỉ sao chép từ summary.

**Evidence.** Tôi đọc `dev_pilot_records_r3_v1.jsonl` cùng stream giải nén của `conditional_full_grid_records_r3_v1.jsonl.gz`, giữ các trường ID/status/proof/reason/margin/time, rồi nhóm theo `(state_cell_id, scene_id, horizon_id)`. Không import `validation.g2`, evaluator, checker hay project verifier.

| Phase | Queries | CERTIFIED | proof-complete UNKNOWN | Resource/invalid/failure |
|---|---:|---:|---:|---:|
| Frozen pilot | 216 | 126 | 90 | 0 |
| Conditional remaining IDs | 1,728 | 1,070 | 658 | 0 |
| Combined original grid | 1,944 | 1,196 | 748 | 0 |

Kết quả trực tiếp từ record stream: 1,944 ID duy nhất; 1,944 record có proof; tất cả ghi `PENDING_INDEPENDENT_AUDIT`. Group distribution là 132 nhóm có 9 `CERTIFIED`, 76 nhóm có 0, tám nhóm có đúng 1. Có 140 nhóm có ít nhất một action certified và 140 nhóm có `V_0_0` certified; tập hai nhóm bằng nhau, nên có 0 nhóm chỉ được chứng nhận bởi voltage khác zero. Trong 1,196 certified rows, 1,056 là nonzero action rows nằm trong 132 all-certified groups.

Reason codes của 748 `UNKNOWN`: `CONTACT_SUFFICIENT_MARGIN_NEGATIVE` xuất hiện 636 lần, `COLLISION_SUFFICIENT_MARGIN_NEGATIVE` 405 lần; một số record có cả hai. Tất cả certified rows trong audit có hai lower margin không âm. Negative sufficient margin chỉ làm checker không cấp certificate.

Tám group hỗn hợp, đã đếm lại:

| State | Horizon | Scene IDs | CERTIFIED action | `contact_margin_lower` (N) | collision margin |
|---|---|---|---|---:|---|
| `state_low_mid` | `T_100` | `scene_d050_l-200`, `scene_d050_l+200`, `scene_d100_l-200`, `scene_d100_l+000`, `scene_d100_l+200`, `scene_d200_l-200`, `scene_d200_l+000`, `scene_d200_l+200` | `V_0_0` only | `+0.127641589` | dương cho cả chín action |

Ở cả tám geometry, tám action còn lại có contact margins âm và reason duy nhất là `CONTACT_SUFFICIENT_MARGIN_NEGATIVE`. Rounded margin theo action: `(-1,-1) -0.211889782`; `(-1,0)`/`(0,-1) -0.103833460`; `(-1,+1)`/`(+1,-1) -0.213302737`; `(0,+1)`/`(+1,0) -0.108378014`; `(+1,+1) -0.213006908`. Contact bound không đổi giữa tám geometry. Đây là một state/horizon mechanism lặp qua tám cảnh, không phải tám cơ chế độc lập.

Timing field `elapsed_seconds_display_only` được đọc từ mọi record: min `0.109 s`, max `0.313 s`, upper median `0.203 s`, sum `360.991 s` (median trung bình của hai điểm giữa `0.1955 s`). Mỗi horizon có 648 query; từng query đều lâu hơn hold tương ứng (`0.02`, `0.05`, `0.1 s`). Không so timing này với deadline giả định chưa khai báo, không cộng thành thời gian controller đã triển khai.

Archive/hash audit chỉ dùng Python standard library: archive SHA-256 `352b6c67480133350a7d1bfc89334a1beff1dc27c64cfda46391af27982fa874`, 34,613,266 compressed bytes; giải nén trực tiếp cho 147,589,521 bytes, 1,728 newline records, SHA-256 `de339ffcb5ee5e0c83f8d25e3077d9fd9316f83293982189aaffba0bdcf3b196`. Pilot bytes 18,197,673, SHA-256 `fdbce2ac5587247ababc0849c5fce8f9a596c3eb2175ed277545072c06acdc43`. Các digest này khớp archive manifest và semantic record hashes R3.

**Consequence.** R3 cho thấy có certificate outputs trên moving nonzero-width cells có uncertain fixed labels. Tuy vậy, group coverage zero-only đã bằng coverage cả action grid; các status hỗn hợp chỉ do contact sufficient margin. Không có statistical denominator: 1,944 là grid được thiết kế, không phải mẫu độc lập của môi trường.

**Status.** VALID — direct count/hash audit; không phải replay chứng minh ODE enclosure.

**Required action.** Giữ nguyên denominator, mọi `UNKNOWN`, và phân biệt 1,056 certified nonzero rows trong all-certified groups với 0 nhóm được mở rộng độ phủ bởi nonzero voltage. Không gọi `UNKNOWN` là unsafe.

## Finding 4 — evidence layers và exact proof/code obligations

**Finding.** Bốn tầng evidence khác nhau: inclusion toán học; source implementation claim; replay của record; independent artifact review. R3 có bằng chứng ở cả bốn tầng với độ độc lập khác nhau, nhưng không có independent numerical engine.

**Evidence.**

1. **Derived mathematical inclusion.** `research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md` §§1–7.1 trình bày `A,B,D,S`, residual Lipschitz/amplitude bound, Metzler comparison, pose lift và sufficient continuous collision/contact inequalities. `G2_FINITE_EVALUATOR_SPEC_v1.md` thu hẹp lớp hữu hiệu sang clip/rational maps và recipe hữu hạn. Lập luận theo fixed fiber là đúng dạng cần có: một `V` cho cả state/label; label không resample; thời gian toàn `[0,T]`; UNKNOWN không hàm ý unsafe.
2. **Source-level implementation claim.** `model.py` tạo interval image và scaled matrix; `evaluator.py` tạo `P0/P1`, defect, `N`, radius, pose, contact và collision bounds; exact rational budget và Taylor/root primitives nằm trong `rational.py`/`interval.py`; R3 proof serialize các bound thành field hữu tỉ. Soát source không cho thấy lỗi inclusion cụ thể trong nhánh frozen clip/profile: interval hulls widen; full-hold range dùng `[0,T]`; contact beta dùng clip interval + `|S|eta/v_s`; collision dùng lower distance rồi trừ `R_s+E_p`; negative margins trở thành UNKNOWN.
3. **Recorded replay.** `full_grid_record_check_r3_v1.json` ghi `all_pass=true`, coverage 1,944/1,944 và 1,944/1,944 replay. Luna handoff ghi lệnh `python -m validation.scripts.verify_records_r3 --phase conditional-full-grid`. Checker dựng lại các trường proof/margins/status bằng equality. Đây là recorded execution, không phải replay được chạy lại trong audit này.
4. **Independent artifact review.** Codex R3 review báo đã phân tích độc lập JSON/hash/fraction bằng standard library, kiểm tra row coverage, margin signs và toàn bộ stored R3 directed-distance witness; chính review nói không chạy evaluator, checker full replay hay test suite. GPT R3 review đọc source path, thấy không có nhánh CERTIFIED sai trong scope đã soi, nhưng cũng không chạy evaluator/checker/archive decompression và gọi upstream contract PARTIAL. Audit này độc lập đếm rows/groups/timing và raw archive hash; không lặp phần kiểm tra proof arithmetic.

Mapping then chốt (xem bảng chi tiết trong companion note):

| Premise | Code/proof anchor | Caveat |
|---|---|---|
| Fixed rational labels, denominator/positivity, gear witness | `model.py` functions `_checked_parameter_images`, `_check_gear_witness`, `build_model`; `polynomial.py` rational parser/equality; proof label/maps/matrices | Correlation bị interval hull quên đi, nhưng image vẫn là outer cover; không là parameter-switch theorem. |
| P0/P1 whole-hold ranges | `evaluator.py` `_predictor_level`; `interval.py` `interval_matrix_exponential`; proof `exp_range`, `P0_scaled`, `P1_scaled` | Predictor `n=1`; hull có thể lỏng, không phải một trajectory point. |
| Defect/residual/error | `evaluator.py` `_evaluate_bounds`, `_bound_model_matrices`, `_radius_series`; proof `delta_abs_scaled`, `residual_force_upper`, `N_nonnegative_majorant`, `eta_*` | `Q_F` dùng clip Lipschitz 1; residual còn chặn bởi `2C^+`; finite positive series có tail. |
| Full time pose | `evaluator.py` pose block; proof `center_*_range`, `E_theta`, `E_p` | Predictor rates/times/sin-cos được bao trên toàn hold; không phải endpoint check. |
| Contact corner/saturation | `evaluator.py` contact block; proof `beta_upper`, `contact_available_lower`, `contact_demand_upper`, `contact_margin_lower` | Reserve đủ điều kiện của lateral-force budget theo contact model; không phải tire law thực. |
| Collision/R3 distance | `evaluator.py` `_dyadic_gap_bound`, `_bounded_collision_distance`; `checker.py` `_checker_r3_distance_witness`; proof dyadic gaps/radicands/root brackets/`margin_lower` | Bound lower cho minimum distance tới predictor rectangle; upper endpoint không dùng làm max trajectory distance. |

### Exact unmet premises found

**Finding.** Không có counterexample số học cụ thể cho record R3 nào được tìm ra trong audit source-level này. Có các premise hẹp chưa đóng, một trong số đó ảnh hưởng chính xác nghĩa của resource limit.

**Evidence.**

- `validation/g2/checker.py` import `_parse_input_query`, `_validate_profile`, `canonical_hash`, `query_hash_payload` từ `evaluator.py`; nhưng `CHECKER_PATHS` trong `validation/scripts/verify_records_r3.py` không khai evaluator. `model.py` import `polynomial.py`, file cũng không nằm trong `PRODUCER_PATHS`/`CHECKER_PATHS`. Full Git source revision đóng các bytes này, nên đây là thiếu sót closure của path manifest, không phải bằng chứng R3 chạy code khác.
- `results/validation/g2/r3/specification_content_ledger_r3_v1.json` bind finite evaluator spec và usefulness protocol, nhưng không bind analytic `G2_ENCLOSURE_CANDIDATE_v1.md` vốn là nguồn các inclusion equations. Theorem-to-implementation relation phải được review riêng.
- `validation/g2/rational.py` dòng 110 kiểm tra deadline chỉ sau mỗi 256 metered operations. Successful `return record` ở `validation/g2/evaluator.py` không có final deadline check. Profile gọi 15 s/query, do đó source chỉ có stop hợp tác theo checkpoint; chậm sau checkpoint cuối vẫn có thể thoát thành record. Không có record R3 nào gần giới hạn: max đo được là 0.313 s, nên không thấy ảnh hưởng lên batch này.
- `checker.py` replay một path arithmetic khác của proof record, nhưng cùng `Budget`/Fraction, interval exp/trig/root, model constructor và import helpers từ producer evaluator. Docstring `shares only exact interval primitives/model map` hẹp hơn import thực. Đây không phải independent numerical engine.
- R3 supports only the exact frozen implementation/profile. Finite successes do not prove every valid rational query, every supported parameter expression or every future profile correct.

**Consequence.** Có thể giữ R3 count/integrity record và chấp nhận directed-distance witness riêng; không thể nói strict hard wall-cap guarantee hoặc universal implementation soundness đã đóng. Những điểm này không làm các query đã đo dưới 0.313 s mất hiệu lực.

**Status.** NEEDS REVISION — source-role closure/documentation và hard wall-cap semantics cho phiên bản sau; PARTIAL — end-to-end G2 soundness remains pending review.

**Required action.** Không sửa manifest/artifact R3 lịch sử. Với bản tiếp theo, bind transitive source call graph và analytic note; thêm check trước successful return hoặc đổi ý nghĩa/cách ghi của wall cap; cần reviewer độc lập rà đủ nguồn bao hàm trước khi nâng `CERTIFIED` thành claim được chấp nhận.

## Finding 5 — usefulness, timing, G3 và G4 phải tách riêng

**Finding.** R3 nâng bằng chứng từ singleton/hand case lên grid state-box tổng hợp, nhưng chưa đưa ra lợi ích chọn điện áp có coverage gain và không đưa ra online/recursive guarantee.

**Evidence.** Zero alone covers the same 140 groups as all actions; eight mixed outcomes have identical state/horizon/contact margins over eight obstacle scenes. All recorded per-query computation times exceed each hold duration. Benchmark spec §§7–8 is marked not locked and itself says no coverage or runtime threshold has been justified. The batch is a development grid, not a held-out evaluation.

`UNKNOWN` có thể do collision/contact sufficient lower bound âm; nó không cho thấy trajectory unsafe. R3 không đo endpoint target/return, không xây `K_T`, không có policy lặp holds, và không thử estimator, scheduling, delays hay actuator driver. G3 vẫn ngoài phạm vi. Novelty của Picard/comparison/parameter augmentation cần G4 matched comparison; Auer comparison là lane riêng, không bù soundness/usefulness G2.

**Consequence.** Có thể phát biểu certificate-output variation trên synthetic moving cell, nhưng không nói một nonzero action là thiết yếu, phương pháp mở rộng safe-action coverage, filter chạy đúng hold deadline, hay theorem supports robot.

**Status.** VALID — descriptive result; practical usefulness PARTIAL/UNVERIFIED; online/G3 UNVERIFIED; G4 UNVERIFIED.

**Required action.** Giữ denominator và statuses như đã khóa. Đừng thêm query 1, chạy Auer, hay chỉnh clearance/actions/margins của R3 để tạo kết quả khác.

## Finding 6 — nguồn gốc tham số và khả năng đưa miền có cơ sở hơn

**Finding.** Toàn bộ giá trị R3 là thiết kế tổng hợp hữu tỉ có chủ đích. Trong nguồn primary/reference đã ghi tại repo, chưa có parameter/contact-law package tương thích để gán các giá trị đó cho DDWMR thật hoặc một reduced model có cơ sở thực nghiệm.

**Evidence.** `G2_USEFULNESS_BENCHMARK_SPEC_v1.md` §2 ghi rõ synthetic units/scale; §3–5 định nghĩa state boxes, obstacle scenes, horizons/actions. `benchmark_v1.json` mã hóa đúng các rational map đã liệt kê. JSON labels độc lập left/right nhưng fixed xuyên hold; `J=1/rho` và gear witness là tạo tương quan hình thức, không là quan hệ được đo. Không thấy trang/datasheet/equation/table nào gán đúng `m=I_z=R_w=b=v_s=c_u=c_r=1`, capacity `[1,1.1]N`, hoặc toàn bộ motor/wheel interval trên cho một robot.

| Nguồn/phần dữ liệu | Locator/access có trong repo | Units/compatibility | Disposition |
|---|---|---|---|
| R3 synthetic family | `research/benchmarks/G2_USEFULNESS_BENCHMARK_SPEC_v1.md` §2 (Git-blob SHA-256 `a16a55230754a915b21616392ce508a6d7f1abb8694ce4e25933ea1435523912`); `validation/configs/benchmark_v1.json` (semantic SHA-256 `21632e1eebf58a5d7fea14224254738d0ff11ba689b94343afa47adbccea166b`) | N, kg, kg·m², m, m/s, SI damping/electrical/motor units theo MASTER; mọi value tự chọn bằng rational | Dùng để kiểm theorem/arithmetic và mô tả chính batch R3; không dùng làm hardware identification, literature operating domain hoặc claim plausible robot range. |
| Wang, Zhang & Wang (2026), differential-drive tracking | `research_context/LITERATURE_MATRIX.md`, ID 13; PLOS One DOI `10.1371/journal.pone.0354699`; matrix nói đã xem publisher modeling/execution descriptions một phần | Matrix ghi velocity setpoint/servo; không xác nhận full electrical dynamics, slip-force law, contact capacity, inertia/actuator parameter table hay model inclusion | Primary source được ghi nhận nhưng model extraction còn pending; không có con số tương thích được trích cho R3. |
| Auer, Kiel & Rauh (2013), piecewise-smooth IVP example | `docs/reviews/G4_AUER_SOURCE_AND_APPLICABILITY_v1.md` ghi §5, Eqs. (45)–(47), Table 2; full article là nguồn comparator G4 | Friction/hysteresis example không phải MASTER DDWMR clip/contact law. Table 2 hiển thị `F_s=[0.15,0.03] N` với endpoints đảo; không có correction authority | Không lấy các số đó cho G2. Nguồn này phục vụ method comparison G4. |
| maxon manufacturer reference trong `docs/reviews/G1_PHYSICAL_MODEL_AUDIT_v2.md` | “Motor data and simulation,” constants; “Motors as Generators,” gear-motor combinations | Hỗ trợ quy ước SI về torque/back-EMF và lưu ý drive; không có motor part number/datasheet, robot geometry, fit, uncertainty range hay contact law tương ứng R3 | Không phải parameter dataset; cũng không tạo model-family inclusion. |

`MASTER_RESEARCH_CONTEXT_v2.md` §§8, 12.A3/A6, 14 định nghĩa `C_j` là effective tangential capacity N vừa scale force law vừa là reaction-envelope radius; nó không mặc định bằng `mu N`. Cần contact/support/actuation justification hoặc certified model-error inclusion để transfer sang platform. Một datasheet riêng cho motor không đủ xác nhận mass/yaw inertia/drag/contact law, và một fitted capacity riêng không chứng minh trajectory containment.

**Consequence.** Nguồn hiện có không cùng nhau biện minh được operating domain thực hoặc luật contact. Không đề xuất bất kỳ real/literature numeric value nào; mọi số đã nêu là synthetic theo benchmark. Một future “literature-supported reduced-model” result có thể có ý nghĩa mà chưa cần hardware identification, nhưng phải source mọi thông số thiết yếu và chứng minh chúng phù hợp với reduced equations/contact semantics.

**Status.** UNVERIFIED — practical parameter relevance và physical correspondence.

**Required action.** Trước một study mới, lập parameter provenance matrix cho một DDWMR candidate: full citation/primary link; exact equation/table/page; unit; known/range status; shaft convention; support/contact law; map vào `m,I_z,b,R_w,J,B,L,R,k,C_j,v_s,phi`; uncertainty/correlation; lý do inclusion. Nếu nguồn không đưa ra hoặc không biện minh contact law/capacity, chặn physical-domain claim thay vì điền bằng số tổng hợp.

## Prospective admission criterion trước bất kỳ study/usefulness query mới nào

R3 đủ cho kết luận hữu hạn tổng hợp ở trên nhưng không đủ cho một G2 operating-domain claim có tính quyết định thực tế. Trước khi tạo query output ở miền mới, phải đăng ký trước: (i) một reduced-model domain có primary-source data hoặc được dán nhãn rõ là literature-supported mathematical domain; (ii) parameter map, units, contact law/capacity semantics và parameter correlations có căn cứ; (iii) operating state boxes, static obstacle geometry, hold values và task-driven action list; (iv) tiêu chí coverage/use do mục tiêu ứng dụng đặt ra, không suy ra từ kết quả R3.

Tiêu chí certificate tối thiểu cho mỗi accepted cell vẫn là toàn time/state/label dưới một common held voltage với strictly nonnegative outward collision **và** contact margins. Nếu claim “nonzero voltage selection expands coverage,” điều kiện falsifiable phải được đặt trước: ít nhất một query-group đã định nghĩa trước có nonzero action `CERTIFIED` và zero action không `CERTIFIED`. R3 không thỏa điều kiện này. Không đặt một tỉ lệ phần trăm generic hay chọn lại geometry/margins sau khi xem output.

## Decision matrix và nghĩa vụ G2 nhỏ nhất

| Item | Current disposition | Evidence | Required next action |
|---|---|---|---|
| Finite R3 batch completeness | Scoped computational result can be accepted | 1,944/1,944 IDs, proofs, hashes, zero resource/invalid/execution rows; this audit recounted statuses/IDs and decompressed digest | Preserve exact artifacts; không replay bằng cách sửa outputs cũ |
| Directed dyadic distance | ACCEPT in narrow role | Witness math plus stored-record checks in earlier Codex audit; this audit confirmed archive/output bindings | Keep lower-endpoint/minimum-distance interpretation |
| Soundness of exact R3 `CERTIFIED` path | PARTIAL | Source inspection consistent with candidate proof; prior reviewers found no false-cert branch; no fresh independent end-to-end replay | Smallest next theorem obligation: independent source-to-inclusion audit for one exact source/profile closure and proof fields; include `polynomial.py`/checker imports and wall cap semantics |
| Useful decision/action scope | PARTIAL | 140 groups with any cert; 140 with zero; eight contact-only mixed groups | Do not claim nonzero-action-only benefit; get primary-source domain + predeclared application criterion before any new study |
| Practical parameters / hardware | UNVERIFIED | No compatible primary-source parameter/contact package | Build provenance/inclusion matrix first; no synthetic-to-hardware extrapolation |
| Online timing, recursion, policy | UNVERIFIED / outside task | Query time exceeds holds; no endpoint or `K_T` | G3 separate; not required to restate R3 one-hold result |
| G4/Auer novelty | Separate lane; UNVERIFIED | Matched comparison is underway elsewhere | Not a substitute for closing G2 proof or data provenance |

**Finding.** No additional R3 evaluator query is the smallest useful next step. The currently missing G2 acceptance item is an independent review of the frozen proof/code inclusion path. For a decision-relevant domain, a source-backed reduced-model family is a separate prerequisite.

**Status.** G2 remains UNVERIFIED; overall HOLD unchanged.

## Commands and actual execution accounting

The result audit was read-only and used the following PowerShell pipeline with Python standard library; it streams the pilot JSONL and compressed remaining JSONL, counts IDs/status/proof/reasons/groups, tests exact margin signs with `Fraction`, and compares display times against each row's exact horizon:

```powershell
@'
import gzip, json
from collections import Counter, defaultdict
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
root=Path('results/validation/g2/r3')
def q(x):
    if isinstance(x,list): x=x[0]
    return Fraction(int(x['num']),int(x['den']))
def iter_jsonl(path):
    op=gzip.open if path.suffix=='.gz' else open
    with op(path,'rt',encoding='utf-8') as f:
        for line in f: yield json.loads(line)
rows=[]
for path in (root/'dev_pilot_records_r3_v1.jsonl',root/'conditional_full_grid_records_r3_v1.jsonl.gz'):
    for r in iter_jsonl(path):
        rows.append({k:r[k] for k in ('query_id','state_cell_id','scene_id','horizon_id','horizon','action_id','held_voltage','status','proof','reason_codes','collision_margin_lower','contact_margin_lower','elapsed_seconds_display_only','review_status')})
counts=Counter(r['status'] for r in rows)
reasons=Counter(c for r in rows for c in r['reason_codes'])
groups=defaultdict(list)
for r in rows: groups[(r['state_cell_id'],r['scene_id'],r['horizon_id'])].append(r)
shape=Counter(sum(r['status']=='CERTIFIED' for r in rs) for rs in groups.values())
any_groups={k for k,rs in groups.items() if any(r['status']=='CERTIFIED' for r in rs)}
zero_groups={k for k,rs in groups.items() if any(r['action_id']=='V_0_0' and r['status']=='CERTIFIED' for r in rs)}
mixed=[]
for k,rs in groups.items():
    n=sum(r['status']=='CERTIFIED' for r in rs)
    if 0<n<9:
        mixed.append((k[0],k[1],k[2],[r['action_id'] for r in rs if r['status']=='CERTIFIED'],all(q(r['collision_margin_lower'])>0 for r in rs),sorted(set(c for r in rs if r['status']=='UNKNOWN' for c in r['reason_codes'])),{r['action_id']:round(float(q(r['contact_margin_lower'])),9) for r in rs}))
times=sorted(Decimal(str(r['elapsed_seconds_display_only'])) for r in rows)
print('rows/unique/groups',len(rows),len({r['query_id'] for r in rows}),len(groups))
print('statuses',dict(counts),'all_proofs',all(r['proof'] is not None for r in rows),'all_pending',all(r['review_status']=='PENDING_INDEPENDENT_AUDIT' for r in rows))
print('group_distribution',dict(sorted(shape.items())),'any_cert',len(any_groups),'zero_cert',len(zero_groups),'nonzero_only',len(any_groups-zero_groups))
print('reason_occurrences',dict(reasons),'unknown_negative_collision',sum(r['status']=='UNKNOWN' and q(r['collision_margin_lower'])<0 for r in rows),'unknown_negative_contact',sum(r['status']=='UNKNOWN' and q(r['contact_margin_lower'])<0 for r in rows))
print('mixed_groups',mixed)
print('timing_min/upper_median/max/sum',times[0],times[972],times[-1],sum(times))
for h in sorted({r['horizon_id'] for r in rows}):
    rs=[r for r in rows if r['horizon_id']==h]
    T=q(rs[0]['horizon'])
    print('timing_by_horizon',h,len(rs),'all_exceed_T',all(Decimal(str(r['elapsed_seconds_display_only']))>Decimal(T.numerator)/Decimal(T.denominator) for r in rs))
'@ | python -
```

The stream audit above returned `1944 1944 216`, statuses `CERTIFIED=1196, UNKNOWN=748`, group distribution `{0:76, 1:8, 9:132}`, any-cert/zero-cert `140/140`, nonzero-only `0`; contact/collision reason occurrences `636/405`; and timings recorded in Finding 3. One earlier exploratory draft treated `collision_margin_lower` as a scalar; R3 stores a one-element obstacle list, so that draft stopped with `TypeError` before reporting an audit. It was corrected to read the singleton list element and the complete stream audit then succeeded. It never called evaluator/checker and changed no files.

Archive byte audit command (also read-only):

```powershell
@'
import gzip, hashlib
from pathlib import Path
p=Path('results/validation/g2/r3/conditional_full_grid_records_r3_v1.jsonl.gz')
h=hashlib.sha256(); n=0; rows=0
with gzip.open(p,'rb') as f:
    while True:
        b=f.read(1024*1024)
        if not b: break
        h.update(b); n+=len(b); rows+=b.count(b'\n')
print(n,rows,h.hexdigest())
'@ | python -
```

Observed: `147589521 1728 de339ffcb5ee5e0c83f8d25e3077d9fd9316f83293982189aaffba0bdcf3b196`. I also recomputed the canonical semantic SHA-256 of parsed `benchmark_v1.json`, `dev_pilot_r3_v1.json`, and `development_manifest_r3_v1.json`; they matched the frozen values `21632e1e...`, `7a93c482...`, and `e5c796fc...` respectively. No new elapsed-time benchmark was run.

R3's recorded producer/checker commands (from stored run metadata/handoff, **not rerun here**) are `python -m validation.scripts.run_pilot_r3 --phase pilot`, `python -m validation.scripts.verify_records_r3 --phase pilot`, `python -m validation.scripts.run_pilot_r3 --phase conditional-full-grid --pilot-checker-report results/validation/g2/r3/dev_pilot_record_check_r3_v1.json`, and `python -m validation.scripts.verify_records_r3 --phase conditional-full-grid`. The archive checker record reports `all_pass=true`; this handoff does not represent that historical replay as a fresh audit run.

## Evidence index and hashes

### Results and run commitments

| Artifact | Bytes | Hash/commitment |
|---|---:|---|
| `results/validation/g2/r3/dev_pilot_records_r3_v1.jsonl` | 18,197,673 | SHA-256 `fdbce2ac5587247ababc0849c5fce8f9a596c3eb2175ed277545072c06acdc43` |
| `results/validation/g2/r3/conditional_full_grid_records_r3_v1.jsonl.gz` | 34,613,266 | compressed SHA-256 `352b6c67480133350a7d1bfc89334a1beff1dc27c64cfda46391af27982fa874`; decompressed SHA-256 `de339ffcb5ee5e0c83f8d25e3077d9fd9316f83293982189aaffba0bdcf3b196` |
| `results/validation/g2/r3/full_grid_summary_r3_v1.json` | 1,264 | SHA-256 `45143813328c800d87443c68aad6fefd3f1f471af369af665e584241755709c2` |
| `results/validation/g2/r3/full_grid_action_group_summary_r3_v1.json` | 999,537 | SHA-256 `c85ace6865af81294d0ec4141f85265be1ae8df4fe1e74b1a5058a8cda15a564` |
| `results/validation/g2/r3/full_grid_record_check_r3_v1.json` | 4,817,666 | SHA-256 `701a21ccd4c47c69ec7f4fa1878bafaf7e1c77fe36ca2a2833ee91f41b106a9c` |
| `results/validation/g2/r3/conditional_full_grid_run_metadata_r3_v1.json` | 4,586 | SHA-256 `3ce14210519545d3ed588c2e1bd6b02fbb7129169bd549ce2f0981f75730f8e7` |
| `results/validation/g2/r3/conditional_full_grid_archive_manifest_r3_v1.json` | 1,123 | SHA-256 `052c12ba33e05820449d29796c567d90a9c6cf68cd17255f622744d8589b99ac` |
| `results/validation/g2/r3/SHA256SUMS_RESULTS_R3.json` | 6,351 | SHA-256 `ccca8ca9a78b8ae3a7ffa18a16910e5982fd9903340ef07a079740b6121a4592`; artifact ledger lists 21 result entries |
| `results/validation/g2/r3/specification_content_ledger_r3_v1.json` | 3,562 | SHA-256 `84928fe65dd788b7248d52e264832e4bcd3ca277633644ba3157cf16fb3efa45`; specification bundle `84b444d0be6e18c946697c3b95662ffd0f30dd228ae7ca5e742cee47d446c850` |

Input semantic hashes bound by R3: benchmark `21632e1eebf58a5d7fea14224254738d0ff11ba689b94343afa47adbccea166b`; pilot config `7a93c4824b859d8dbc5816c2d7edac005a7a87282399678fc8beebb49192b7b0`; profile `74cd7964c9e6d0f55c24269518034f8fdf0bc7a3124063ec4fb3900b5e8c0295`; development manifest `e5c796fcfe8275b1b7106f112813d24b36d18626400ba149f29f4bee7b9c155d`; original denominator 1,944. The conditional continuation contains the predeclared remaining 1,728 IDs; it is not held-out data.

### Source revisions and dependency integrity

R3 handoff reports starting commit `4df4dfef65a5addb040fbd2f059a62727189cd88`, R3 implementation/evidence snapshot `4fd0451146ab9567a51499183db5a08f20ae8de5`, pilot producer/checker revision `78aba4ddc100eb2fdb5c966e6d124ddac90ac8bc`, and conditional producer/checker revision `667a8e4a5e840ff33e823f353bed8c6328c0a443`. Full result evidence was assembled through `28e962ec6e2085656e4dd1b7bc254186835cefb8`; the R3 handoff itself is at `4fd045...` in the archived branch history.

The metadata binds exact Git revisions and per-file SHA-256 commitments; the companion note lists evaluator, checker, rational, interval, model, polynomial, hashing, provenance and runner digests. Current `validation/g2/evaluator.py`, `checker.py`, `model.py`, `rational.py`, `interval.py`, and `polynomial.py` content matches the R3 source snapshot checked by Git blob. The G2 Markdown files were compared by normalized Git blob identity because current checkout line endings can differ from frozen Git blob bytes; the frozen ledger SHA values above are the source-of-record. The explicit transitive closure omissions are documented in Finding 4.

## Final matrix and proposed next decision

**Finding.** There is a defensible, independently reviewable narrow statement for R3, but current evidence does not close a broad/useful G2 gate.

**Evidence.** Finite batch and directed distance have recorded plus prior independent artifact support. The code path maps to the sufficient inclusion with no unsound certification branch found in reviewed scope; exact wall cap/manifest closure and independent source-level inclusion review remain. The only physical parameter family is synthetic. Zero voltage already has the observed existential group coverage; batch runtimes exceed each hold.

**Consequence.** Retain the R3 certificate outputs as bounded synthetic evidence. Do not promote G2 or infer a viable online action. The Auer/G4 comparison cannot close G2 proof/data obligations.

**Status.** **HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical-platform correspondence UNVERIFIED.**

**Required action.** First have Codex independently close the frozen R3 source-to-equation/proof-field review, including shared trusted components, complete transitive source closure and soft wall-time handling. Then decide whether the current narrow synthetic result is accepted as a finite G2 computational result. For any decision-relevant operating-domain claim, obtain a source-backed parameter/contact-law family and freeze application-driven states/scenes/horizons/actions plus an acceptance criterion before outputs. Preserve old R3 artifacts and do not begin that study within this assignment.

### Short decision summary for forwarding

> R3 supplies 1,196 recorded certificates over a frozen, nonzero-width moving-state, uncertain-actuator **synthetic** grid, with 748 proof-complete UNKNOWN rows. This is bounded one-hold computation for the declared `G2-COMP-clip` profile. All 140 groups with any certificate also have `V=(0,0)` certified; the eight mixed groups repeat one contact-bound mechanism over different geometries. The result does not establish practical parameter relevance, nonzero-action coverage gain, hard online timing, G3, hardware correspondence, or G4 novelty. G2 remains UNVERIFIED pending independent source-to-inclusion acceptance; HOLD remains unchanged.

