# DDWMR — Luna validation assignment v1

## 0. Chỉ đạo và quyền thực hiện

**Người dùng đã cho phép code kiểm chứng G2/G4.** Nguyên văn: “tôi không cấm, hãy setup và tôi sẽ giao cho luna, giờ tôi là chung gian giữa bạn và luna”, sau đó “thực hiện”. Authority được ghi trong MASTER §§3/32 và DECISION_LOG, workflow W1. Không chờ mọi gate PASS mới bắt đầu công việc dưới đây; không hỏi lại quyền đã cấp cho cùng phạm vi.

Người dùng trực tiếp giao file này cho **Luna max** và chuyển kết quả về Codex. Luna thực hiện code và ghi bằng chứng; Codex/GPT phản biện kết quả. Không tự tạo thêm agent hoặc tự gửi tin nhắn cho người khác. Codex không chạy implementation thay Luna trong lượt setup này.

**Mục tiêu đợt này:** tạo một bộ kiểm chứng hữu hạn có thể tái lập cho mô hình rút gọn, bắt đầu bằng fallback đã có đặc tả, đánh giá trung thực mức độ bảo thủ và chuẩn bị dữ liệu cho G2/G4. Không hứa coverage hoặc novelty trước khi chạy.

**Trạng thái:** MASTER plant v2.1; workflow W1; G1 PASS chỉ nhất quán mô hình rút gọn; Cases A/B/C ACCEPT trong phạm vi tổng hợp đã ghi; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED; HOLD. Quyền code không phải chấp nhận tính đúng của draft hay GO điều khiển robot.

## 1. Repository và thứ tự đọc

- Repo: `NADUNGVN/ddwmr-actuator-safety`, public.
- Local project: `D:\Research\Teacher_Vien\projects\ddwmr-actuator-safety`.
- Scientific draft baseline: `44e4f90a71e8e9192a92b88b17ec527eb8e322b6`.
- Start from the later commit containing **this assignment and workflow W1**. Record actual HEAD, branch and working-tree status in your returned report. Do not start from the older snapshot alone: it still contains the superseded blanket code rule.

Đọc theo thứ tự:

1. `AGENTS.md` và cả bốn file `research_context/`.
2. File assignment này.
3. `research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md`.
4. `research/theorem_notes/G2_FINITE_EVALUATOR_SPEC_v1.md`.
5. `docs/reviews/CODEX_WP1_DRAFT_AUDIT_v1.md`.
6. `research/benchmarks/G2_USEFULNESS_BENCHMARK_SPEC_v1.md`.
7. `docs/reviews/G4_MATCHED_PRIOR_ART_COMPARISON_v1.md`.
8. `docs/reviews/GPT_TO_CODEX_DDWMR_CONSOLIDATED_REVIEW_FULL_HANDOFF.md`, nhất là §§5,10,14; các kết luận khoa học còn giá trị, quy định chờ authorization đã được W1 thay thế.
9. A/B/C và review tương ứng khi dùng làm fixture kiểm chứng; không nhập kết quả của mô hình 7-state vào plant hiện hành.

Các câu “no implementation”, “pending authorization” trong tài liệu trước W1 là lịch sử về quyền thực hiện. Chúng không vô hiệu chỉ đạo mới. Ngược lại, các phần OPEN về toán, primitive, baseline và benchmark vẫn phải xử lý; authorization không tự đóng chúng.

## 2. Isolation và quyền sửa

Chỉ làm trong repo DDWMR. Trước khi sửa, ghi working-tree status; giữ nguyên thay đổi không thuộc bạn. Dùng branch `luna/g2-validation-v1` nếu chưa có; nếu đã có, kiểm tra provenance trước khi tiếp tục. Không reset/clean/force-push, không sửa repo khác hoặc cấu hình toàn máy. Nếu môi trường không dùng Git, xuất đúng patch/files và nói rõ.

Được tạo code, cấu hình và bằng chứng trong các đường dẫn sau; chỉ tạo khi có nội dung thật:

| Path | Purpose |
|---|---|
| `validation/g2/` | Arithmetic, parameter representation, model matrices, fallback predictor/radius, pose/contact/collision evaluator, record checker |
| `validation/configs/` | Rational input schemas, synthetic fixture/profile data, development/locked manifests |
| `validation/scripts/` | Deterministic entry points for checks, evaluator, benchmark and summaries |
| `validation/README.md` | Environment, commands, limitations and reproduction instructions |
| `validation/verification/` | Evidence-producing arithmetic/inclusion checks and expected fixture statements |
| `results/validation/g2/` | Actual output only: immutable manifests, certificates, UNKNOWN ledger, work/timing summaries |
| `docs/reviews/LUNA_G2_VALIDATION_PREFLIGHT_v1.md` | Equation-to-code audit and blockers |
| `docs/reviews/LUNA_TO_CODEX_G2_VALIDATION_FULL_HANDOFF.md` | Complete returned handoff |

Repo-local environment/dependency declarations and `.gitignore` edits are allowed when needed. Prefer a small, inspectable Python exact-rational reference using the standard library (`fractions`, integer arithmetic, JSON); do not install a new global toolchain. A different arithmetic backend needs an explicit correctness contract and dependency version record. No floating safety decisions with an arbitrary epsilon.

Do not edit canonical plant assumptions, gate statuses or archived reviews. Put substantive specification corrections in a new supporting revision with an exact diff and reason. Routine conservative implementation decisions within existing equations may be documented and performed without asking the user again. If a change would alter the model or theorem assumptions, stop that branch and return the exact proposal; continue independent authorized work.

## 3. Work packages — execute as one assignment

### L1. Preflight and traceability

Write `LUNA_G2_VALIDATION_PREFLIGHT_v1.md` before relying on certificate outputs. Map every implemented equation to the candidate/spec section and state coordinate scaling. Independently inspect:

- motor/current signs, parameter image and fixed labels;
- positive denominators, gear witness, scaled/physical transformations;
- exponential and forced-series tail bounds, including zero norm;
- fixed-panel versus partial-panel integration;
- nonnegative square-root bisection and trigonometric remainder;
- same-initial-state predictor semantics and residual upper bounds;
- nonnegative comparison domination, full-hold pose lift and contact reserve;
- termination/resource behavior and universal aggregation of all cells.

Use **Finding / Evidence / Consequence / Status / Required action**. An unresolved soundness defect disables CERTIFIED for the affected path. Do not silently weaken the mathematical target. The current whole-hold hull fallback is the initial implementation target; the sharper general global/refined variants are not completed specifications.

No external GPT acceptance is claimed or required merely to develop the authorized prototype. All resulting scientific claims remain candidates for Codex/GPT review.

### L2. Exact finite fallback and certificate checker

Implement the declared effective clip subclass in small inspectable modules. Keep controller code out of this package.

Required functions, with final names chosen and documented by Luna:

1. Parse and validate finite rational inputs and resource profiles.
2. Evaluate supported rational parameter maps with checked denominator/positivity and gear witnesses.
3. Build interval A/B/D/S, scaling maps and force-law bounds.
4. Bound matrix exponentials, sin/cos and roots with declared finite remainders.
5. Enclose finite predictor ranges, residual, comparison radius and pose over the entire hold.
6. Compute collision/contact sufficient lower bounds.
7. Aggregate all parameter/state cells with the same V and emit a certificate or inconclusive record.
8. Recheck exported certificate arithmetic/inclusions without trusting its status label.

You may support a strictly named subset of the proposed rational-map class first (constants, labels, arithmetic and reciprocals with checked signs). Reject unsupported expressions explicitly; do not advertise arbitrary rational-polynomial/Bernstein support without implementing its checker. Preserve actual benchmark correlations. Never parse mathematical input through unrestricted `eval`.

Use exact rational serialization, e.g. `{ "num": "1", "den": "20" }`; reduced fractions with positive denominator. JSON floating numbers may be display-only fields and must not determine safety predicates. Store source revision, specification hash, complete input/profile hashes, method/variant, all cell IDs, time coverage, outward primitive settings and sufficient margins. Records must distinguish center width, error radius and total enclosure width.

Semantics:

| Result | Meaning |
|---|---|
| `CERTIFIED` | Every required full-hold collision/contact check passes for all states and fixed labels under the same held V, according to this implementation; acceptance pending independent audit |
| `UNKNOWN` | Valid supported query not certified: inconclusive margin, budget exhaustion, loose enclosure or a declared mathematical prerequisite not established |
| `INVALID_INPUT` | Malformed/unsupported encoding or violated effective input contract; not a statement that the physical state is unsafe |
| execution failure | Crash, bug, corrupt artifact or environment failure; separately logged, not silently recast as a mathematical result |

Maintain a separate `review_status` such as `PENDING_INDEPENDENT_AUDIT`. Failure of an optional endpoint-target predicate must not erase a valid one-hold safety result: store the two predicates separately. Do not call endpoint containment G3.

Enforce finite operation, bit-length and splitting limits before expensive integer operations where possible. A wall-time abort produces a resource-limited inconclusive record with completed work, not a certificate. No uncapped recursive subdivision or refinement until success.

### L3. Verification evidence

Produce exact arithmetic/inclusion checks with recorded commands and outputs as part of this validation assignment. Cover sign changes, zero, contact saturation corners, nonzero initial widths, asymmetric parameter labels, scaling consistency, input rejection and resource exhaustion. Distinguish a finite fixture check from proof of the general algorithm.

Reproduce the **declared hand arithmetic** in accepted Cases A/B/C where feasible, with a separate path/name from the generic fallback. Do not special-case their answers inside the evaluator. The coarse generic fallback may return UNKNOWN on A/B/C even though their sharper hand proofs certify; that is not automatically an arithmetic bug. Compare it to its own specified bounds.

The record checker must recompute primitive bounds/margins and check complete cell coverage. Avoid circular verification that merely calls the evaluator and compares its output to itself. Be precise about shared trusted arithmetic code; do not claim an independent formal proof system. Ordinary time samples or floating ODE traces cannot establish all-time safety.

### L4. Benchmark tooling and honest pilot

Encode the synthetic benchmark draft as a machine-readable manifest: six moving nine-dimensional cells, 12 scenes, three horizons and nine actions, hence 1944 original queries per method/profile. Preserve all original IDs and denominator. Independent actuator/contact labels are fixed throughout a hold, never resampled between slabs.

The benchmark draft is **not yet a locked scientific comparison**. Implement its generator, schema validation and bounded development runner now. Before any development evaluation, freeze the development manifest, chosen finite work caps and selection rule in Git/hash records. Record choices without observing outcomes first. Development outputs are explicitly developmental and cannot later be relabeled untouched held-out results.

Start with an affordable, deterministic balanced pilot chosen from that manifest before outputs, covering both speed groups, both yaw signs, zero and nonzero voltages, all three horizons and more than one clearance. Specify exact IDs and the reason for the work cap. Report omitted original queries as NOT_RUN; do not divide pilot successes by 1944 or call the pilot the full grid. Expand within a declared cap if feasible, retaining partial results and all failure reasons.

For each evaluated query report margins, statuses, pose/internal widths, work counts, subdivisions, actual elapsed times and environment. Runtime is measured evidence only for that machine/configuration. Whole-hold hulls copied to more time slabs do not create a tighter method; report no-op settings honestly.

Before a formal matched comparison, close outstanding primitive/localized/refined specifications, applicable baseline choice, resource settings and acceptance criteria. Return a proposed lock manifest/diff for review. No need to stop independent implementation while these scientific items remain open. Do not manufacture coverage by moving obstacles after seeing results or discard all-action-UNKNOWN cells. No minimum coverage or practical deployment claim is assumed.

### L5. Matched comparison readiness

Internal global/refined/fallback variants are ablations; an external validated-reachability method is a separate baseline obligation. Do not rename the fallback “external baseline”. Implement a variant/adapter only if its actual mathematical/arithmetic assumptions are verified and documented. Otherwise record NOT_IMPLEMENTED with the exact missing proof/source/configuration.

Source-level audit and adapter preparation are authorized. Compare on the same plant/law, fixed-label semantics, initial cells, V, horizon and collision/contact targets. Do not give only the baseline a smoothed contact law, nominal parameters or a weaker time guarantee. A smooth-only method needs a separately declared common benchmark for both methods. Keep generic-method novelty BLOCKED and any practical superiority UNVERIFIED pending matched evidence.

### L6. Reproduction and return

Provide one documented command sequence for environment setup, arithmetic verification, fixture checks, selected pilot and summary regeneration. Prefer deterministic configuration over hidden mutable defaults. Explain where all inputs and artifacts are located. Do not commit environments, caches, credentials or huge unbounded traces. Keep small audit records and manifests in Git; large outputs need hashes and reproducible generation commands.

Commit only your work to `luna/g2-validation-v1`. Pushing that branch to this existing repo is authorized as part of the handoff; do not merge main or force-push. If credentials/network prevent pushing, return the commit/patch and say exactly what was not published. Never invent a remote commit.

## 4. Deliverable acceptance matrix

| Deliverable | Evidence to return | Not sufficient |
|---|---|---|
| Preflight | Equation mapping, explicit included/excluded subclass and blockers | “Looks correct” |
| Arithmetic/core | Inspectable finite bounds, exact records, resource handling | Floating samples or a library name alone |
| Evaluator | Common-V/all-label/all-time path, consistent physical units | Endpoint-only collision checks |
| Checker | Recomputed inclusions and coverage, shared trust disclosed | Repeating an exported status |
| Fixtures | Exact inequalities, commands, actual outcomes | Fabricated PASS or hand answers hardcoded into generic method |
| Pilot | Frozen input hashes, exact queried IDs, all outcomes/costs | Tuned clearances or omitted UNKNOWN rows |
| Comparison readiness | Matched assumptions and clearly listed remaining gaps | Unimplemented tool-name comparison |
| Handoff | One complete Markdown report plus code/artifact links | Chat summary without files |

Completion of this assignment is deliverable completion, **not G2/G4 PASS**. If a mathematical blocker prevents a deliverable, return a partial report with exact evidence; do not mislabel it complete. Continue unaffected packages. Always-UNKNOWN may reveal a useless enclosure; report it without inventing a fallback controller or changing plant assumptions.

## 5. Required returned file

Create **`docs/reviews/LUNA_TO_CODEX_G2_VALIDATION_FULL_HANDOFF.md`** and give the user a downloadable copy or direct link. If attachment creation is unavailable, return its full Markdown and the file location; do not falsely claim an attachment.

The report must be self-contained:

1. Executive summary in Vietnamese: completed/partial/blocked, not scientific gate promotion.
2. Starting/final commit, branch, environment, exact files read and changed.
3. Authority acknowledgement: W1 validation scope; MASTER plant unchanged.
4. Equation-to-code map; mathematical fixes and deviations with precise diff.
5. Supported input/primitive classes, resource limits and certificate semantics.
6. Actual verification commands, outputs and artifact hashes; failed checks included.
7. Pilot configuration, queried IDs/denominators, results and timings; UNKNOWN/NOT_RUN/invalid/failures separate.
8. Baseline/refinement readiness and unresolved soundness/usefulness/novelty items.
9. Exact reproduction commands and paths.
10. **Single Codex review request** listing what should be audited next and proposed changes requiring scientific judgment.

Use **Finding / Evidence / Consequence / Status / Required action** for every blocker or disputed claim. Keep overall HOLD and G2/G3/G4 UNVERIFIED. Do not build K_T, controller, closed-loop simulator or hardware deployment in this assignment.

## 6. Short prompt the user can send Luna

> Read AGENTS.md and all four research_context files in NADUNGVN/ddwmr-actuator-safety, then execute docs/LUNA_VALIDATION_HANDOFF_v1.md under workflow W1. I authorize the scoped G2/G4 validation code and will relay your result to Codex. Do not wait for all gates to pass before this validation work. Audit the draft bounds, implement the finite fallback and reproducible validation artifacts, report blocked branches explicitly, preserve MASTER assumptions and HOLD, and return LUNA_TO_CODEX_G2_VALIDATION_FULL_HANDOFF.md with code commits and evidence. Do not autonomously delegate or merge main.
