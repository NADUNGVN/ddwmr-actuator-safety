# GPT → CODEX DDWMR CONSOLIDATED RESEARCH REVIEW — FULL HANDOFF

**Repository:** `NADUNGVN/ddwmr-actuator-safety`  
**Branch:** `main`  
**Actual repository commit reviewed:** `c9ff32d45ad7f500cc2492c3bc7a69480c29c636`  
**Consolidated-request evidence snapshot named by the request:** `0156ddbe9dcba15a8beb20396467867839e7d233`  
**Case C mathematical milestone named by the request:** `547061d2cc0ce1ea0c000de0ec66054034ec930f`  
**Authority:** `research_context/MASTER_RESEARCH_CONTEXT_v2.md` — MASTER v2.1  
**Review date:** 2026-09-29  
**Overall authoritative project status:** **HOLD**  
**G1:** PASS — restricted reduced-model scope  
**G2/G3/G4:** UNVERIFIED  
**Physical-platform correspondence:** UNVERIFIED  
**Generic-method novelty:** BLOCKED  
**Implementation / G3 construction / GO:** NOT AUTHORIZED by this review

This document performs the complete consolidated review requested in `docs/GPT_CONSOLIDATED_RESEARCH_REVIEW_REQUEST.md`.

It does **not** silently amend MASTER, change the plant, open G3, authorize implementation, or declare GO.

---

# 1. EXECUTIVE SUMMARY — TIẾNG VIỆT

## Kết luận ngắn

Ba gate lớn còn lại **chưa đóng**:

\[
\boxed{\text{G2 UNVERIFIED,\quad G3 UNVERIFIED,\quad G4 UNVERIFIED}}
\]

và toàn dự án tiếp tục:

\[
\boxed{\textbf{HOLD}}.
\]

Review tổng hợp này có một kết quả mới cụ thể:

\[
\boxed{\textbf{ACCEPT Case C C.1--C.16 trong phạm vi tổng hợp rất hẹp đã khai báo}}
\]

Các phương trình của Case C, ba collision margin

\[
\frac{13}{2000000},\qquad
\frac{67}{18000000},\qquad
-\frac{83}{18000000}\ {\rm m},
\]

và contact lower bound

\[
\frac{1999}{1000}\ {\rm N}
\]

đều kiểm tra được.

Do đó, với **một rule chứng nhận đã khóa giống nhau**:

- \(V=(0,0)\): **CERTIFIED**;
- \(V=(1/4,1/4)\): **CERTIFIED**;
- \(V=(1,1)\): **UNKNOWN**.

Nhưng đây **không phải** bằng chứng rằng điện áp \(1/4\) “tốt hơn” theo nghĩa điều khiển. Trạng thái ban đầu là rest, \(V=0\) đã an toàn và còn có collision margin lớn hơn. Obstacle được đặt có chủ đích ở mức micromet để phân biệt output của certificate. Vì vậy Case C chứng minh được:

> certificate output có thể phụ thuộc vào biên độ điện áp thông qua center \(n=1\) dưới một phép đánh giá tổng hợp đã khóa.

Case C **không** chứng minh:

- voltage necessity;
- practical action selection;
- tracking benefit;
- \(n=1\) necessity;
- unsafety của action trả UNKNOWN;
- general usefulness;
- novelty.

## G2 — đạt gì và còn thiếu gì?

G2 đã có nền tảng giải tích đáng giữ:

- joint fixed-parameter enclosure;
- một common held voltage cho mọi hidden realization;
- finite predictor;
- residual tube;
- pose lift;
- collision/contact full-hold sufficient test;
- ba hand cases A/B/C, trong đó:
  - A: finite rational certificate;
  - B: actuator-parameter dependence + correlation + saturation exit;
  - C: same-rule voltage-dependent certificate-output distinction.

Nhưng:

\[
\boxed{\text{hand certificates} \neq \text{general useful certified evaluator}}
\]

G2 còn thiếu tối thiểu:

1. một **finite evaluator specification** cho một lớp input được định nghĩa hữu hiệu;
2. proof soundness + finite termination với output ít nhất `CERTIFIED` / `UNKNOWN`;
3. một benchmark domain được khóa **trước khi xem kết quả**, không chỉ exact rest hoặc obstacle tuning;
4. bằng chứng certificate hữu ích trên **state cells có độ rộng khác 0**, ít nhất chứa trạng thái đang chuyển động;
5. dữ liệu benchmark có provenance phù hợp với claim;
6. nếu “tractability/runtime” là tiêu chí gate, cần cho phép một nhánh **validation-only research implementation** riêng biệt.

Hiện có một dependency về quản trị:

> code bị cấm đến khi G1–G4 PASS, trong khi runtime/general evaluator/matched computational comparison đang được coi là nghĩa vụ để đánh giá G2/G4.

Đây không phải mâu thuẫn toán học, nhưng là **workflow dependency** thực sự.

Khuyến nghị: người dùng cân nhắc cho phép một loại:

> **validation-only research implementation**

chỉ gồm certified evaluator, arithmetic checks, baseline adapters và offline benchmark runner.

Nó **không** bao gồm controller, simulator deployment, hardware hay experiments và **không tự được phép bởi review này**.

## G3 — chưa được mở và chưa sẵn sàng

G3 chưa có:

\[
K_T\subseteq \operatorname{Pre}_T^c(K_T)
\]

được xây dựng.

Điểm chặn hiện tại để mở G3 không phải generic induction; mà là chưa có một G2 evaluator đủ tái sử dụng trên một **state-action region** để kiểm tra:

- full-hold safety/contact;
- endpoint return;
- mọi fixed hidden parameter;
- non-oracle voltage selection.

G3 không được phép dựa lén vào:

- finite stopping distance;
- sustained wheel lock;
- zero-voltage emergency brake;
- matched-side symmetry của auxiliary case;
- true-parameter oracle.

Nếu sau G2 vẫn không tìm được nontrivial recursive region, cần báo BLOCKER và cân nhắc reformulation có điều kiện; không tự thêm assumption.

## G4 — novelty

Các nhánh novelty sau đã bị chặn bởi prior art:

- componentwise/growth-matrix reachability;
- fixed-parameter augmentation;
- finite predictor + validation/residual tube nói chung;
- validated flowpipe nói chung;
- inter-sample sampled-data safety nói chung;
- WMR + CBF nói chung.

Contribution hypothesis còn đáng kiểm:

> một certificate/recursive construction **plant-specific** cho chuỗi  
> \(V\to i\to\omega\to\sigma\to F\to(u,r)\to p\),  
> bảo toàn fixed-parameter/contact structure, và cho **lợi thế được chứng minh** về certification coverage, tightness hoặc computation so với validated reachability phù hợp trên cùng model/data.

Hiện hypothesis này:

\[
\boxed{\textbf{UNVERIFIED}}
\]

Nó sẽ bị **falsify** nếu một generic validated method phù hợp:

- certifies cùng hoặc nhiều benchmark cells hơn;
- có tube không rộng hơn đáng kể;
- chi phí tương đương hoặc tốt hơn;
- và structured decomposition không tạo lợi thế có ý nghĩa.

Nếu vậy, không nên cứu novelty bằng nhiều simulation hoặc thêm nhiều hand cases.

## Khuyến nghị nghiên cứu

**Tiếp tục scope reduced-model hiện tại; chưa cần sửa plant.**

Dừng nhánh “generic reachability method is novel”.

Tập trung tiếp vào:

1. G2 finite evaluator + fixed benchmark protocol;
2. user decision về validation-only implementation;
3. matched baseline comparison;
4. G4 contribution decision;
5. chỉ sau G2 đủ mạnh và user cho phép mới mở G3 construction.

---

# 2. REPOSITORY / COMMIT / READ LEDGER

## 2.1 Commit provenance

Actual review was performed at:

`c9ff32d45ad7f500cc2492c3bc7a69480c29c636`

Commit message:

> `docs: bundle remaining research review with Markdown handoff requirement`

The consolidated request names evidence snapshot:

`0156ddbe9dcba15a8beb20396467867839e7d233`

and Case C mathematical milestone:

`547061d2cc0ce1ea0c000de0ec66054034ec930f`.

Independent blob-hash comparison showed that:

- all five canonical authority/context files;
- `docs/PROGRESS_SUMMARY_2026-09-29.md`;
- the Case C file;
- the Codex R4 response;
- the R4 review request;
- the Luna R4 audit

are byte-identical between the relevant request snapshot and the actual `c9ff32d...` review commit for the items compared.

In particular, Case C's blob SHA is:

`41acf599fda2390445a6d5b4bdc35e450b764b46`

at all of:

- `547061d...`;
- `0156ddbe...`;
- `c9ff32d...`.

Therefore this report does **not** mix Case C equations from different revisions.

## 2.2 Required repository files read

### Authority and status

- `AGENTS.md`
- `research_context/MASTER_RESEARCH_CONTEXT_v2.md`
- `research_context/DECISION_LOG.md`
- `research_context/LITERATURE_MATRIX.md`
- `research_context/REVIEW_GATE.md`
- `docs/PROGRESS_SUMMARY_2026-09-29.md`

### G2 analytic framework and prior accepted reviews

- `research/theorem_notes/G2_ENCLOSURE_CANDIDATE_v1.md`
- `docs/reviews/GPT_TO_CODEX_G2_REVIEW_7390942f_FULL_HANDOFF.md`
- `research/theorem_notes/G2_FINITE_CERTIFICATE_CASE_A_v1.md`
- `docs/reviews/GPT_G2_R2_d2cd854_ACCEPT_RECORD.md`
- `research/theorem_notes/G2_CHALLENGE_CASE_B_v1.md`
- `docs/reviews/GPT_G2_R3_1da2166_ACCEPT_RECORD.md`

### Case C package

- `research/theorem_notes/G2_VOLTAGE_SELECTION_CASE_C_v1.md`
- `docs/reviews/CODEX_G2_R4_RESPONSE_AND_CASE_C.md`
- `docs/GPT_G2_REVIEW_REQUEST_R4.md`
- `docs/reviews/LUNA_G2_CASE_C_AUDIT_R4.md`

### Novelty evidence

- `docs/reviews/G2_PRIOR_ART_AND_BLOCKERS_v1.md`
- `docs/reviews/G2_PRIOR_ART_SUPPLEMENT_R2.md`

### Consolidated request

- `docs/GPT_CONSOLIDATED_RESEARCH_REVIEW_REQUEST.md`

## 2.3 Repository-access gaps

No required repository file listed above was inaccessible.

Tool-output truncation occurred when large multi-file fetches exceeded display size, but the relevant files/ranges were re-read separately where necessary.

## 2.4 External-source audit performed

Primary or author-hosted sources were independently rechecked where accessible. Important access limits are recorded in Section 7.

No inaccessible or partial source is treated as negative novelty evidence.

---

# 3. CASE C — EQUATION-LEVEL AUDIT

# 3.1 C.1–C.2 — matched-side parameter image, units, rest and quantifier

## Finding

The Case C parameter family is internally valid as an **auxiliary matched-side restriction** of MASTER v2.1.

The hidden-parameter quantifier remains correct.

## Evidence

Case C declares:

\[
(\rho,C)\in[1,11/10]^2,
\]

with:

\[
\rho_L=\rho_R=\rho,
\qquad
C_L=C_R=C,
\]

\[
J_L=J_R=L_L=L_R=\frac1\rho.
\tag{C.1}
\]

The equality of normalized \(J\) and \(L\) values does not imply equal physical units and is explicitly declared synthetic.

The ideal gear witness from Case B gives:

\[
n_g=10,\qquad k_m=\frac1{10},
\]

\[
J_{\rm wheel}=\frac1{10},
\qquad
J_{\rm motor}
=
\frac{1/\rho-1/10}{100}>0,
\]

hence:

\[
J_{\rm wheel}+n_g^2J_{\rm motor}
=
\frac1\rho.
\]

The electrical assignment:

\[
L=\frac1\rho
\]

is separately stipulated and is not incorrectly attributed to the gearbox.

Initial data:

\[
T=\frac1{10},
\quad
p_*=0,
\quad
\theta_*=0,
\quad
z_*=0.
\]

Candidate actions:

\[
V_a=(a,a),
\qquad
a\in\left\{0,\frac14,1\right\}.
\tag{C.2}
\]

Each candidate is held for the entire hold and is common to every hidden fixed \((\rho,C)\).

Thus the robust quantifier is still:

\[
\exists V_a
\quad
\forall(\rho,C)
\quad
\forall t\in[0,T].
\]

No candidate depends on the hidden realization.

## Consequence

Case C does not introduce oracle access or switching parameters.

Matched sides are a restriction of this example only and must not propagate into the general MASTER model.

## Status

**VALID**

## Required action

Retain the phrase that C.1 is an auxiliary matched-side family only.

---

# 3.2 Exact symmetry by uniqueness

## Finding

The exact equal-side symmetry argument is valid for the true formal ODE and finite predictors.

It does **not** imply symmetry of the generic error box or of general independent-side uncertainty.

## Evidence

At the declared initial condition:

\[
\omega_L=\omega_R,
\qquad
i_L=i_R,
\qquad
r=0.
\]

The left/right physical/model parameters and applied voltages are equal.

Therefore, if the equal-side subspace is entered:

\[
v_L=v_R=u,
\]

\[
\sigma_L=\sigma_R,
\]

\[
F_L=F_R,
\]

and:

\[
\dot r=F_R-F_L-r=0.
\]

The wheel/current equations on both sides also coincide.

The accepted G1 plant has a locally Lipschitz vector field, hence trajectory uniqueness applies. The reflected/equal-side trajectory is therefore the same trajectory.

Consequently:

\[
r(t)=0,\qquad
\theta(t)=0
\]

and left/right motor states remain equal for the exact Case C fibers.

No oddness of \(\phi\) is required.

However, the generic six-state error box used later still includes possible \(r\)-error and yaw-error directions. Case C correctly does not set those box components to zero.

## Consequence

The center symmetry is exact without illicitly shrinking the generic enclosure.

No statement follows for independently uncertain left/right MASTER realizations.

## Status

**VALID**

## Required action

No change.

---

# 3.3 C.3–C.4 — motor kernel and predictor branch

## Finding

The signs and upper/lower bounds in C.3–C.4 are correct.

## Evidence

At exact rest:

\[
F(z_*)=0.
\]

For one side:

\[
\omega_j^0=aI_s(t),
\qquad
i_j^0=aI_c(t),
\tag{C.3}
\]

where:

\[
I_s(t)
=
\int_0^t
\rho e^{-\rho s}\sin(\rho s)\,ds.
\]

For:

\[
0\le \rho s\le\frac{11}{100},
\]

use:

\[
e^{-x}\ge1-x\ge\frac{89}{100},
\]

and:

\[
\sin x
\ge
x\left(1-\frac{x^2}{6}\right)
\ge
\frac{99}{100}x.
\]

Their product exceeds:

\[
\frac45x.
\]

Therefore:

\[
I_s(t)
\ge
\int_0^t
\frac45\rho^2s\,ds
\ge
\frac25t^2.
\]

For the upper bound:

\[
e^{-\rho s}\le1,\qquad
\sin(\rho s)\le\rho s,
\]

hence:

\[
I_s(t)
\le
\frac{\rho^2t^2}{2}
\le
\frac{121}{200}t^2.
\tag{C.4}
\]

Since:

\[
a\le1,\qquad T=0.1,
\]

the predictor slip satisfies:

\[
0\le aI_s(t)<1.
\]

Thus for the predictor only:

\[
\phi(\sigma_j^0)=\sigma_j^0=aI_s.
\]

This branch fact is proved rather than assumed.

## Consequence

The voltage dependence of the predictor force is explicit and nonzero for \(a>0,t>0\) in this synthetic family.

No conclusion is transferred to the abstract MASTER \(\phi\)-class.

## Status

**VALID**

## Required action

None.

---

# 3.4 C.5–C.6 — voltage-dependent body/pose center

## Finding

The center formulas and all displayed bounds are correct.

## Evidence

Because both predictor forces are equal:

\[
u^1=aU(t),
\qquad
r^1=0,
\]

\[
p^1=(aP(t),0).
\tag{C.5}
\]

Here:

\[
U(t)
=
2C
\int_0^t
e^{-(t-s)}I_s(s)\,ds.
\]

Since:

\[
e^{-(t-s)}\ge\frac9{10},
\quad
C\ge1,
\quad
I_s(s)\ge\frac25s^2,
\]

we get:

\[
U(t)
\ge
2\frac9{10}\frac25
\frac{t^3}{3}
=
\frac6{25}t^3.
\]

For the upper bound:

\[
C\le\frac{11}{10},
\qquad
I_s(s)\le\frac{121}{200}s^2,
\]

hence:

\[
U(t)
\le
2\frac{11}{10}\frac{121}{200}
\frac{t^3}{3}
=
\frac{1331}{3000}t^3
<
\frac49t^3.
\]

Integration gives:

\[
\frac3{50}t^4
\le
P(t)
\le
\frac1{9}t^4.
\tag{C.6}
\]

Therefore the two positive-voltage centers differ for \(t>0\).

## Consequence

Case C genuinely propagates voltage through:

\[
V
\rightarrow
i
\rightarrow
\omega
\rightarrow
\sigma
\rightarrow
F
\rightarrow
u
\rightarrow
p.
\]

This is a center-response fact for the selected synthetic family, not a global lower-authority theorem.

## Status

**VALID**

## Required action

None.

---

# 3.5 C.7–C.8 — predictor differences and residual

## Finding

All residual coefficients are correct.

## Evidence

The predictor force is bounded by:

\[
F_j(z^0)
\le
\frac{11}{10}
\frac{121}{200}s^2
=
\frac{1331}{2000}s^2.
\]

Therefore:

\[
|\Delta u|
\le
2\frac{1331}{2000}
\int_0^t s^2ds
=
\frac{1331}{3000}t^3.
\]

Equal forces imply exactly:

\[
\Delta r=0.
\]

Using the wheel force kernel:

\[
|H_{\omega F}|\le\rho\le\frac{11}{10},
\]

gives:

\[
|\Delta\omega_j|
\le
\frac{14641}{60000}t^3.
\]

For the current kernel:

\[
|H_{iF}(\tau)|
\le
\rho^2\tau
\le
\frac{121}{100}\tau,
\]

and:

\[
\int_0^t(t-s)s^2ds=\frac{t^4}{12},
\]

so:

\[
|\Delta i_j|
\le
\frac{161051}{2400000}t^4.
\tag{C.7}
\]

The slip difference has:

\[
|S\Delta z|_j
\le
\frac{1331}{3000}t^3
+
\frac{14641}{60000}t^3
=
\frac{41261}{60000}t^3.
\]

Multiplying by:

\[
C\le\frac{11}{10}
\]

gives:

\[
d_{1,j}
\le
\frac{453871}{600000}t^3
<
\frac45t^3.
\tag{C.8}
\]

## Consequence

The shared residual envelope is a valid outward bound for all three actions.

## Status

**VALID**

## Required action

None.

---

# 3.6 C.9 — full six-state Metzler comparison

## Finding

C.9 is correct.

The proof uses signed row sums of a Metzler matrix, not an induced norm bound on \(M\).

## Evidence

For the full generic six-state comparison:

\[
M=A^\#+|D|Q.
\]

The body signed row sums are:

\[
-1+6C
\le
\frac{28}{5}.
\]

Wheel row sums satisfy:

\[
3\rho C
\le
\frac{363}{100}.
\]

Current row sums are zero.

Thus:

\[
M\mathbf1
\le
\frac{28}{5}\mathbf1.
\]

Since \(M\) is Metzler:

\[
e^{Mt}\mathbf1
\le
e^{(28/5)t}\mathbf1.
\]

The already accepted rational exponential bound at \(T=0.1\) gives:

\[
e^{(28/5)T}<\frac95.
\]

Because:

\[
d_{1,j}\le\frac45t^3
\]

and the maximum row sum of \(|D|\) is two:

\[
\||D|d_1\|_\infty
\le
\frac85t^3.
\]

Therefore:

\[
\|E_{1,0}(t)\|_\infty
\le
\frac95
\frac85
\int_0^t s^3ds
=
\boxed{
\frac{18}{25}t^4
}.
\tag{C.9}
\]

## Consequence

The same full generic radius safely covers every Case C action and hidden label.

The exact center symmetry is not used to delete yaw error from the enclosure.

## Status

**VALID**

## Required action

None.

---

# 3.7 C.10–C.11 — generic pose lift

## Finding

The pose bounds are correct.

## Evidence

From C.9:

\[
E_\theta(t)
\le
\int_0^t
\frac{18}{25}s^4ds
=
\frac{18}{125}t^5.
\]

Using:

\[
|u^1(s)|\le\frac49s^3,
\]

the generic pose lift gives:

\[
E_p(t)
\le
\int_0^t
\left[
\frac{18}{25}s^4
+
\frac49s^3
\frac{18}{125}s^5
\right]ds.
\]

Thus:

\[
E_p(t)
\le
\frac{18}{125}t^5
+
\frac8{1125}t^9
\le
\frac3{20}t^5.
\tag{C.10}
\]

At:

\[
T=\frac1{10},
\]

\[
\bar E_p
=
\frac3{20}T^5
=
\boxed{
\frac3{2000000}
}\ {\rm m}.
\tag{C.11}
\]

## Consequence

The position error is certified without sampled trajectories.

## Status

**VALID**

## Required action

None.

---

# 3.8 C.12–C.13 — obstacle and three collision margins

## Finding

The obstacle geometry and all three collision margins are correct.

The obstacle is explicitly engineered, which is a major limitation of interpretation.

## Evidence

Case C uses:

\[
R_s=\frac12,
\qquad
d=\frac1{125000}=8\times10^{-6}\ {\rm m},
\]

\[
p_o=(R_s+d,0).
\tag{C.12}
\]

For each action:

\[
\mathcal P_a
=
\left[0,\frac{aT^4}{9}\right]\times\{0\}.
\]

The locked lower bound is:

\[
L_p(a)
=
d
-
\frac{aT^4}{9}
-
\bar E_p.
\tag{C.13}
\]

### \(a=0\)

\[
L_p(0)
=
\frac1{125000}
-
\frac3{2000000}
=
\boxed{
\frac{13}{2000000}
}>0.
\]

### \(a=1/4\)

\[
\frac{aT^4}{9}
=
\frac1{360000}.
\]

Hence:

\[
L_p(1/4)
=
\boxed{
\frac{67}{18000000}
}>0.
\]

### \(a=1\)

\[
\frac{aT^4}{9}
=
\frac1{90000}.
\]

Hence:

\[
L_p(1)
=
\boxed{
-\frac{83}{18000000}
}<0.
\]

Therefore the locked test returns:

| Held voltage | Output |
|---|---|
| \((0,0)\) | CERTIFIED |
| \((1/4,1/4)\) | CERTIFIED |
| \((1,1)\) | UNKNOWN |

The negative third lower bound means only that this sufficient evaluation cannot certify.

## Consequence

The same-rule certificate output is voltage-dependent.

However:

- zero voltage is already safe;
- zero has the largest certified collision margin;
- the obstacle clearance is deliberately micrometer-scale;
- no tracking or progress objective is present.

Thus this is not a decision-utility result.

## Status

**VALID arithmetic; usefulness UNVERIFIED**

## Required action

Always describe the third output as **UNKNOWN**, never unsafe/failure.

Keep the engineered-clearance limitation adjacent to any use of this example.

---

# 3.9 C.14–C.15 — full-tube contact certificate

## Finding

The contact bounds and final contact lower bound are correct.

## Evidence

At \(T=0.1\):

\[
\frac{121}{200}T^2
=
0.00605,
\]

\[
\frac{41261}{60000}T^3
\approx
0.000687683,
\]

and:

\[
3e_z(T)
=
3\frac{18}{25}10^{-4}
=
0.000216.
\]

Therefore:

\[
\beta_j
<
0.006953683
<
\frac7{1000}
<
\frac1{100}.
\tag{C.14}
\]

With \(C\ge1\), the two-wheel lateral reserve is bounded below by:

\[
\frac{9999}{5000}\ {\rm N}.
\]

The body bounds give:

\[
|u^1|+E_u
<
\frac3{5000},
\]

\[
|r^1|+E_r
<
\frac1{10000}.
\]

Hence:

\[
|mur|
<
\frac3{50000000}\ {\rm N}.
\]

Thus:

\[
g_c
>
\frac{9999}{5000}
-
\frac3{50000000}
>
\boxed{
\frac{1999}{1000}
}\ {\rm N}.
\tag{C.15}
\]

The full generic error box is used despite exact center yaw symmetry.

## Consequence

All three actions pass the ideal contact-domain test throughout the hold.

Collision, not contact capacity, distinguishes the locked outputs.

## Status

**VALID**

## Required action

None.

---

# 3.10 C.16 — Proposition C disposition

## Finding

Proposition C follows from C.1–C.15 in the exact narrow scope stated.

## Evidence

For every fixed:

\[
(\rho,C)\in[1,11/10]^2
\]

and every:

\[
t\in[0,0.1],
\]

one common candidate voltage is held.

For:

\[
V=(1/4,1/4),
\]

the full-hold locked certificate gives:

\[
g_p
\ge
\frac{67}{18000000}>0,
\]

\[
g_c
\ge
\frac{1999}{1000}>0.
\tag{C.16}
\]

The same locked evaluation also certifies:

\[
V=(0,0)
\]

and returns UNKNOWN for:

\[
V=(1,1).
\]

## Consequence

Case C establishes one finite same-state/same-rule certificate-output distinction tied to a voltage-dependent predictor center.

It establishes **none** of:

- physical necessity;
- unsafe alternatives;
- useful navigation;
- useful tracking tradeoff;
- \(n=1\) necessity;
- general voltage selection;
- method superiority;
- recursion.

## Status

\[
\boxed{\textbf{ACCEPT — exact synthetic narrow scope only}}
\]

## Required action

Record Case C only with all limitations above.

Do not change G2 status from UNVERIFIED.

---

# 4. CASE C OVERALL DISPOSITION

## Finding

Case C is mathematically sound in the submitted scope.

It is weaker as a usefulness example than its phrase “voltage-selection” may suggest.

## Evidence

The case starts from exact rest and:

\[
V=(0,0)
\]

keeps the formal plant at rest exactly.

The zero action is already certified with a larger collision margin than the nonzero action.

The obstacle is placed at:

\[
8\ \mu{\rm m}
\]

synthetic clearance to straddle the selected finite error budgets.

## Consequence

Recommended interpretation:

> **Case C is an accepted finite action-dependent certificate-output example, not a useful control-selection example.**

## Status

**ACCEPT for finite certification; UNVERIFIED for usefulness**

## Required action

Do not use Case C as the main evidence for practical usefulness.

Move G2 usefulness evidence to a benchmark domain with motion and a meaningful task/action tradeoff.

---

# 5. CONSOLIDATED G2 REVIEW

# 5.1 What has been proved generally?

## Finding

The current analytic G2 framework contains a sound general one-hold **sufficient enclosure/certificate theorem family** under the declared fixed-parameter reduced-model assumptions.

## Evidence

Previously reviewed G2.1–G2.22 establish, for each fixed hidden parameter realization and common held voltage:

1. six-state decomposition:
   \[
   \dot z=Az+BV+DF(z);
   \]
2. global Lipschitz force increment:
   \[
   |F(z)-F(w)|\le Q|z-w|;
   \]
3. finite predictor family;
4. residual bound;
5. Metzler/Dini error enclosure;
6. optional nonincreasing exact-kernel refinement;
7. pose lift;
8. joint state/parameter fiber tube;
9. full-hold collision sufficient check;
10. full-hold ideal contact sufficient check.

The proof does not require \(\phi'\), oddness, monotonicity, or contact-margin differentiation.

## Consequence

The analytic theorem branch is not the principal remaining G2 weakness.

## Status

**VALID analytically**

## Required action

Promote it to an explicit reviewed theorem statement only after the computational input class and finite evaluation contract are finalized.

---

# 5.2 What is proved only in A/B/C?

## Finding

A/B/C do not constitute a general evaluator.

They instantiate finite proofs for specially selected synthetic data.

## Evidence

### Case A

Shows one finite rational certificate with:

- capacity uncertainty;
- unsaturated clip behavior;
- broad safety/contact margin.

### Case B

Adds:

- parameter-dependent \(A,B,D\);
- preserved correlations;
- independent side labels;
- nonzero body/yaw state;
- true saturation then exit;
- narrow locked refined-CERTIFIED / coarser-UNKNOWN separation.

### Case C

Adds:

- exact matched-side symmetry;
- rest initial state;
- same error envelope for three actions;
- voltage-dependent center;
- same-rule action-output distinction.

Each uses hand-selected analytic inequalities and a small finite parameter family.

## Consequence

The statement:

> “No finite certificate exists”

is obsolete.

But the statement:

> “A general useful certified evaluator exists”

is still unsupported.

## Status

**PARTIALLY RESOLVED**

## Required action

Build an effective evaluator specification and independent benchmark protocol.

---

# 5.3 Minimum finite input class needed for a computable evaluator

## Finding

MASTER's abstract assumptions alone are insufficient to define an algorithm.

G2 needs an explicit **computational input class** local to the theorem/evaluator.

This need not amend the plant.

## Evidence

MASTER permits:

- a generic compact correlated \(\Theta\);
- a known globally Lipschitz \(\phi\).

An arbitrary compact set and arbitrary mathematical Lipschitz function need not arrive with effective representations suitable for finite certified arithmetic.

A computational theorem therefore needs inputs such as:

1. a finite union/cover of parameter cells with preserved algebraic correlations;
2. certified positivity of denominators;
3. a validated evaluator for the selected \(\phi\);
4. a certified \(L_\phi\);
5. finite initial-state cells;
6. a held voltage \(V\) or finite/validated voltage-search cells;
7. hold \(T\);
8. obstacle/contact data;
9. outward arithmetic for exponentials, integrals, square roots and trigonometric quantities.

## Consequence

The mathematical plant may remain broad, while a computability theorem has a narrower effective input representation.

That distinction must be explicit.

## Status

**MISSING SPECIFICATION**

## Required action

Define a named effective input class, e.g. `G2-COMP`, without presenting it as a new physical assumption.

---

# 5.4 Soundness, finite termination and usefulness are different

## Finding

These are three independent obligations.

## Evidence

### Soundness

If evaluator returns:

`CERTIFIED`

then the exact formal trajectory must satisfy full-hold collision and contact constraints for every fixed hidden parameter.

### Finite termination

For every valid computational input, the procedure must halt after finitely many operations.

It does **not** need to decide every boundary case.

A legitimate finite output contract is:

- `CERTIFIED`;
- `UNKNOWN`;
- optionally `INVALID_INPUT` when declared computational assumptions are violated.

A bounded subdivision/refinement budget is acceptable if exhausting it returns `UNKNOWN`.

### Usefulness

A procedure that always terminates by returning `UNKNOWN` is sound and computable but useless.

Hand-certifying a micrometer-tuned rest example is also insufficient evidence of useful conservatism.

## Consequence

G2 must not be passed merely because a finite sound algorithm can be written.

## Status

**GENERAL SOUNDNESS STRONG; TERMINATION/USEFULNESS NOT YET ESTABLISHED FOR A GENERAL EVALUATOR**

## Required action

Write separate G2 acceptance tests for all three properties.

---

# 5.5 Proposed G2 finite-evaluator acceptance criterion

## Finding

A clear finite criterion can close the “computable” part without demanding completeness.

## Evidence

A sufficient G2 evaluator should have a theorem of the form:

> For every input in declared effective class \(\mathcal I_{\rm G2}\), the algorithm terminates in finitely many steps. If it returns CERTIFIED for \((X,V)\), then for all \(x_0\in X\), every fixed \(\vartheta\in\Theta\), and every \(t\in[0,T]\), the reduced-model trajectory stays in \(\mathcal S\cap D_c(\vartheta)\). UNKNOWN makes no safety or unsafety claim.

It must state:

- parameter-cell semantics;
- fixed labels across the hold;
- one common \(V\);
- outward rounding;
- time coverage;
- maximum subdivision/refinement behavior;
- all primitive inclusion rules.

## Consequence

This is a realistic mathematical closure criterion.

It does not require the sufficient test to classify every near-boundary case.

## Status

**PROPOSED ACCEPTANCE CRITERION**

## Required action

Codex/Luna may draft this specification under current G2 analytic authorization.

---

# 5.6 Proposed definition of useful conservatism

## Finding

Usefulness should be defined on a **predeclared benchmark domain**, not via obstacle tuning after seeing tube widths.

## Evidence

A defensible benchmark should contain:

### Mandatory for G2 usefulness evidence

- at least one non-rest moving state region;
- nonzero-width state cells, not only exact points;
- nonzero-width hidden-parameter cells;
- obstacles/clearance chosen independently of the compared method outputs;
- same certification rule across methods/actions;
- a meaningful candidate action or task context.

### Required if the claim is meant to represent the general MASTER state/uncertainty geometry

At least one test should avoid relying on matched-side symmetry, e.g.:

- asymmetric fixed parameters; or
- nonzero yaw rate / turning.

Case B already proves the theory can survive these features synthetically, but not that useful margins remain on defensible data.

### Optional stress tests unless explicitly claimed

- strong stiffness;
- saturation crossing;
- very large parameter width;
- extreme low-friction/contact-capacity regimes.

Do not silently convert optional stress tests into new MASTER assumptions.

## Consequence

“Useful” can be measured without pretending every possible operating regime must certify.

## Status

**PROPOSED ACCEPTANCE CRITERION**

## Required action

Lock the benchmark protocol before quantitative comparison.

---

# 5.7 Suggested G2 usefulness metrics

## Finding

A single tuned margin is not enough.

## Evidence

On a predeclared finite benchmark partition, record at least:

1. **certification coverage**
   \[
   \frac{\#\{\text{state-action cells CERTIFIED}\}}
        {\#\{\text{valid tested state-action cells}\}};
   \]

2. **strict full-hold margin**
   - collision lower margin;
   - contact lower margin;

3. **tube width**
   - position radius;
   - selected internal-state radii;

4. **refinement gain**
   - decrease from global to structured/refined enclosure under the same data;

5. **UNKNOWN rate**;

6. **finite work**
   - number of parameter cells;
   - time slabs;
   - refinements;
   - arithmetic operations / validated evaluations;

7. runtime only if validation-only implementation is authorized.

For fair comparison, obstacle positions must not be tuned separately to each method.

## Consequence

This separates useful conservatism from manufactured certificate separation.

## Status

**PROPOSED METRIC SET**

## Required action

Include these metrics in the G2/G4 benchmark specification.

---

# 5.8 Synthetic vs literature-supported vs platform-identified parameters

## Finding

Platform identification is **not mandatory** for a reduced-model theoretical paper, but parameter provenance must match the claim.

## Evidence

Three evidence tiers should remain separate:

### Synthetic benchmark

Suitable for:

- theorem illustration;
- arithmetic sanity;
- edge-case testing.

Not sufficient for claims of practical relevance.

### Literature-supported reduced-model benchmark

Suitable for:

- demonstrating plausible scales;
- computational/usefulness study of the reduced-model method;
- a theoretical reduced-model paper if clearly labeled.

### Platform-identified / experimentally bounded data

Needed when claiming:

- actual robot relevance;
- hardware safety;
- model-family inclusion for a specific platform.

Even platform identification does not automatically validate omitted tire/support physics.

## Consequence

G2 can, in principle, close for the reduced-model scope without hardware identification.

But a usefulness claim should not rest only on arbitrary dimensionless hand numbers.

## Status

**CLARIFIED**

## Required action

Obtain at least a documented reduced-model benchmark with provenance before claiming practical relevance.

Keep physical transfer as a separate obligation.

---

# 5.9 What if every candidate action returns UNKNOWN?

## Finding

The only correct current output is:

> no certified action found by this certificate.

## Evidence

The enclosure is sufficient, not necessary.

Therefore:

\[
\text{UNKNOWN}
\not\Rightarrow
\text{unsafe}
\]

and:

\[
\forall V\in\mathcal V_{\rm tested}:\text{UNKNOWN}
\]

does not prove unavoidable collision.

There is currently no proved emergency:

- zero-voltage brake;
- finite-stopping fallback;
- wheel-lock mode;
- recursive backup.

## Consequence

No controller is allowed to treat UNKNOWN as physical impossibility.

For future G3, a state at which the authorized selection procedure cannot certify any action cannot be included in the corresponding certified \(K_T\).

## Status

**VALID REQUIRED INTERPRETATION**

## Required action

Make `UNKNOWN` an explicit result state in every evaluator specification.

---

# 5.10 Implementation-gate dependency audit

## Finding

There is a **governance dependency**, though not a theorem contradiction.

## Evidence

Current operating rule:

> no implementation before G1–G4 pass and reviewed GO.

At the same time, the open research obligations increasingly include:

- general certified evaluator evidence;
- tractability;
- runtime;
- matched computational comparison against validated reachability baselines.

Those latter items cannot be honestly established by hand certificates alone.

Thus, if runtime/general executable comparison is required to pass G2/G4, the workflow forbids producing evidence required for the gates.

## Consequence

One of two policies must be selected explicitly.

No silent exception is acceptable.

## Status

\[
\boxed{\textbf{NEEDS USER GOVERNANCE DECISION}}
\]

## Required action

Choose one of the following.

### Option A — recommended

Create a separate category:

> **validation-only research implementation**

Allowed only after explicit user authorization.

Permitted:

- certified enclosure evaluator;
- interval/outward arithmetic tests;
- baseline adapters;
- offline benchmark runner;
- reproducibility scripts.

Still prohibited:

- controller deployment;
- safety filter integration;
- closed-loop simulator claims;
- robot/hardware experiments;
- G3 policy implementation unless separately authorized.

This validation code generates evidence; it does not constitute GO.

### Option B — no code until all gates pass

Then remove runtime/general executable comparison from **G2 acceptance**.

Require G2 only to prove:

- evaluator algorithm specification;
- soundness;
- finite termination;
- finite nontrivial hand/domain certificates.

Move runtime/tractability to a pre-submission obligation.

However, G4 computational superiority would remain difficult to establish without later executable evidence.

### Recommendation

Adopt Option A by explicit user decision.

This review does **not** itself authorize it.

---

# 5.11 Consolidated G2 disposition

## Finding

Case C adds valid finite evidence, but G2 is not yet closed.

## Evidence

Now accepted narrow evidence consists of:

- analytic G2 framework;
- Case A;
- Case B;
- Case C.

Still missing:

- effective general evaluator specification;
- finite termination contract;
- nontrivial benchmark-domain usefulness;
- defensible numerical provenance;
- tractability evidence if required.

## Consequence

The correct gate remains:

\[
\boxed{\textbf{G2 UNVERIFIED}}
\]

## Status

**UNVERIFIED**

## Required action

Complete Work Packages WP1–WP2 defined below.

---

# 6. G3 READINESS AND MISSING OBLIGATIONS

# 6.1 Current readiness

## Finding

The generic mathematical target is well-defined, but G3 is not ready for construction under the current evidence/workflow.

## Evidence

MASTER defines:

\[
\operatorname{Pre}_T^c(A)
\]

and the target:

\[
K_T\subseteq\operatorname{Pre}_T^c(K_T).
\]

However, no reusable state-set one-hold/endpoint evaluator has yet been demonstrated.

Cases A/B/C start from individual exact states.

## Consequence

The strongest present blocker to opening G3 is not the induction theorem; it is the absence of a reusable certified mapping from state/action regions to:

- full-hold safety;
- contact validity;
- endpoint enclosure.

## Status

**NOT READY / G3 UNVERIFIED**

## Required action

Do not construct \(K_T\) until G2 supplies the required reusable certificate and user separately authorizes G3.

---

# 6.2 Missing G3 theorem objects

## Finding

At least the following objects/lemmas are missing.

## Evidence

A valid G3 package needs:

### 1. Explicit state set representation

A nontrivial:

\[
K_T\subseteq\mathcal S_{\rm rob}.
\]

### 2. Robust certified action set

For every \(x\in K_T\), define/compute:

\[
\Gamma_T(x)
=
\left\{
V\in\mathcal U:
\begin{array}{l}
x_\vartheta(t;x,V)\in
\mathcal S\cap D_c(\vartheta),\\
\forall t\in[0,T],\ \forall\vartheta\in\Theta,\\
x_\vartheta(T;x,V)\in K_T
\end{array}
\right\}.
\]

Need to establish:

\[
\Gamma_T(x)\neq\varnothing
\quad
\forall x\in K_T.
\]

### 3. Allowed-information selection

A rule:

\[
\kappa(x)\in\Gamma_T(x)
\]

or another explicitly allowed nonanticipative selection.

It may use:

- exact sampled state;
- known \(\Theta\).

It may not use true hidden \(\vartheta\).

### 4. Endpoint return certificate

One-hold collision/contact safety alone is insufficient.

Need:

\[
x_\vartheta(T;x,\kappa(x))
\in K_T
\quad
\forall\vartheta.
\]

### 5. Recursive induction

Then the standard induction proves repeated safe holds.

This implication is generic and not novelty.

## Consequence

G3 is a constructive set/policy problem, not a wording change around the existing predecessor.

## Status

**MISSING**

## Required action

Use these as the future G3 acceptance skeleton after authorization.

---

# 6.3 Forbidden hidden assumptions in G3

## Finding

Several tempting “backup” arguments remain unavailable.

## Evidence

G1/G2 do not prove:

- finite stopping distance;
- a robust stopping policy;
- sustained wheel lock;
- mechanical brake behavior;
- zero terminal voltage as safe emergency braking;
- general matched-side straight invariance;
- known true parameter.

Therefore G3 cannot argue:

> if no normal action is certified, brake/lock/zero-voltage and remain safe

unless a separate theorem establishes that statement.

Likewise, Case C's matched-side rest symmetry cannot support the general independent-side recursive set.

## Consequence

Any G3 proof containing one of these implicit fallbacks is invalid for current MASTER.

## Status

**BLOCKER FOR ANY BRANCH THAT USES THEM**

## Required action

Reject such branches or prove the missing property under explicitly local assumptions.

---

# 6.4 One-hold safety vs recursion vs viability

## Finding

These objects must remain separate.

## Evidence

### One hold

\[
x\in\mathcal F_T^c
\]

means one common voltage keeps the exact reduced trajectory safe/contact-admissible for one hold.

### State-only robust recursion

\[
K_T\subseteq\operatorname{Pre}_T^c(K_T)
\]

rechecks the full parameter set from state alone at every sample.

### Exact fixed-parameter viability

\[
\mathcal V_T^c
\]

may use nonanticipative history and can exploit information accumulated about one fixed hidden parameter.

These objects need not be equal.

## Consequence

A state-only \(K_T\) may be conservative relative to exact history-dependent viability.

No equality should be claimed.

## Status

**VALID DISTINCTION**

## Required action

Retain the distinction in the future theorem statement.

---

# 6.5 G3 minimum useful-set criterion

## Finding

Rest equilibrium alone is insufficient.

## Evidence

A singleton rest state can satisfy recursion but would not demonstrate the research objective of useful mobile collision safety.

A defensible G3 acceptance criterion should require a declared nontrivial operating region, for example:

- nonzero-width state cells;
- nonzero forward velocity for at least part of the set;
- nonempty interior in a stated reduced slice; or
- another predeclared measure of mobility.

The exact measure should be chosen before constructing the set.

## Consequence

This prevents satisfying G3 with a mathematically correct but vacuous stationary set.

## Status

**PROPOSED G3 ACCEPTANCE CRITERION**

## Required action

Lock a nontriviality criterion when G3 is authorized.

---

# 6.6 G3 failure/reformulation criterion

## Finding

A failed state-only recursive construction may reflect conservatism, not physical impossibility.

## Evidence

The state-only predecessor:

\[
\operatorname{Pre}_T^c
\]

rechecks every parameter value after every hold.

Because the true parameter is fixed, this can discard useful history-dependent information.

## Consequence

If no useful \(K_T\) can be certified, options include:

1. accept that the state-only robust formulation is too conservative;
2. restrict the declared operating domain;
3. add a verified terminal subset;
4. consider history-dependent parameter-set refinement;
5. change the formulation only through explicit versioning.

None may be silently introduced.

## Status

**CONDITIONAL REFORMULATION PATH**

## Required action

If G3 construction fails, stop and present the failure before changing assumptions.

---

# 6.7 Explicit G3 acceptance criterion

A future G3 PASS should require all of:

- an explicit \(K_T\) representation;
- proof:
  \[
  K_T\subseteq\operatorname{Pre}_T^c(K_T);
  \]
- full-hold collision/contact certificate;
- robust endpoint return;
- one common voltage for all hidden fixed parameters;
- a selection rule using allowed information only;
- a predeclared nontriviality/usefulness property;
- no forbidden stopping/lock/oracle assumption;
- independent review of the actual construction.

Current status:

\[
\boxed{\textbf{G3 UNVERIFIED — construction not authorized}}
\]

---

# 7. G4 — SOURCE-LEVEL NOVELTY AUDIT

This is a focused audit, not a complete systematic review of all international literature.

Unknown or partially accessed sources remain unknown.

# 7.1 Primary-source ledger

## S1 — Arcak & Maidens

**Source:** Murat Arcak, John Maidens, *Simulation-based reachability analysis for nonlinear systems using componentwise contraction properties*.  
arXiv:1709.06661. Later chapter DOI: `10.1007/978-3-319-95246-8_4`.  
Primary URL inspected: `https://arxiv.org/abs/1709.06661`.

**Verified locators:**

- Section 2, Proposition 1;
- Eq. (3): componentwise growth/contraction matrix;
- Eq. (4): matrix exponential trajectory-separation bound;
- Corollary 1, Eqs. (6)–(8): reachable-set overapproximation;
- Section 3, Algorithm 1;
- Example 1, Eq. (13): constant uncertain parameter represented with zero dynamics.

**Access limit:** full arXiv HTML was accessible.

**Implication:** componentwise growth-matrix novelty and constant-parameter augmentation are directly blocked.

---

## S2 — Houska, Villanueva & Chachuat

**Source:** Boris Houska, Mario E. Villanueva, Benoît Chachuat, *Stable Set-Valued Integration of Nonlinear Dynamic Systems Using Affine Set-Parameterizations*. SIAM J. Numer. Anal. 53(5), 2015, 2307–2328.  
DOI: `10.1137/140976807`.  
Publisher URL: `https://epubs.siam.org/doi/10.1137/140976807`.  
Author-hosted PDF used in the repository audit: `https://faculty.sist.shanghaitech.edu.cn/faculty/boris/paper/stableSetIntegrator.pdf`.

**Verified locators:**

- Section 3 predictor-validation construction;
- Eqs. (3.1)–(3.4);
- Theorem 3.1;
- Corollary 3.2;
- theorem covers enclosures over the validated time segment, not merely a terminal sample.

**Access limit:** publisher metadata and author full text available; theorem assumptions are smooth/factorable and therefore do not automatically cover every nonsmooth clip representation.

**Implication:** generic predictor + validation/remainder + parametric set-valued integration is strong direct prior art.

---

## S3 — Lin & Stadtherr

**Source:** Youdong Lin, Mark A. Stadtherr, *Validated Solutions of Initial Value Problems for Parametric ODEs*. Applied Numerical Mathematics 57(10), 2007, 1145–1162.  
DOI: `10.1016/j.apnum.2006.10.006`.  
Author manuscript inspected: `https://academicweb.nd.edu/~markst/lin-stadtherr-vspode-apnum.pdf`.

**Verified locators:**

- Section 2, Eq. (1): ODE with time-invariant interval parameters;
- lines around Eq. (1) explicitly define \(\theta\) as time-invariant;
- Section 4 in the repository's prior supplement: Eqs. (18)–(23), validated full-step enclosure/tightening;
- interval arithmetic uses directed outward rounding.

**Important assumption:** the displayed method assumes differentiability sufficient for its Taylor expansions and explicitly excludes branch/abs/min/max expressions in the representation.

**Implication:** fixed-parametric validated ODE integration is established. The current Lipschitz/clip handling is an assumption-level difference, not by itself demonstrated novelty.

---

## S4 — Ariadne

**Source:** Pieter Collins et al., *Rigorous Function Calculi in Ariadne*.  
arXiv:2306.17541; LMCS 21(3), 2025, paper 28.  
DOI: `10.46298/lmcs-21(3:28)2025`.  
Primary sources:
- `https://arxiv.org/abs/2306.17541`
- `https://lmcs.episciences.org/16540`

**Verified scope:**

- rigorous/effective/validated function representations;
- polynomial function models;
- rigorous ODE solution;
- Picard/fixed-point based flow enclosure machinery;
- hybrid-system analysis support.

**Access limit:** full arXiv text is available; exact applicability of the current piecewise clip representation to a matched benchmark still needs an implementation/configuration audit.

**Implication:** “rigorous ODE evaluator” is not a new contribution.

---

## S5 — Flow*

**Source:** Xin Chen, Erika Ábrahám, Sriram Sankaranarayanan, *Flow*: An Analyzer for Non-linear Hybrid Systems*. CAV 2013, pp. 258–263.  
DOI: `10.1007/978-3-642-39799-8_18`.  
Author page: `https://home.cs.colorado.edu/~srirams/papers/cav2013-flowstar.html`.

**Verified scope:**

- guaranteed Taylor-model flowpipes;
- nonlinear/hybrid reachability;
- adaptive numerical machinery.

**Access limit:** in this consolidated pass, publisher/author metadata and abstract-level tool description were available; a complete theorem-level audit was not re-extracted.

**Implication:** Flow* is an active matched-baseline candidate only when the selected \(\phi\) can be represented fairly. It must not be deliberately handicapped by an incompatible regularity choice.

---

## S6 — Taylor et al. sampled-data CBF

**Source:** Andrew J. Taylor et al., *Safety of Sampled-Data Systems with Control Barrier Functions via Approximate Discrete Time Models*. CDC 2022.  
DOI: `10.1109/CDC51059.2022.9993226`.  
arXiv:2203.11470v2: `https://arxiv.org/abs/2203.11470`.

**Verified scope from primary arXiv metadata/full-text entry:**

- sampled-data safety problem;
- approximate discrete-time models;
- Sampled-Data CBF;
- relation to practical safety;
- convex controller construction.

**Implication:** inter-sample/sampled implementation safety is not itself novel.

---

## S7 — Tan, Daş, Ames & Burdick ZOCBF

**Source:** *Zero-order Control Barrier Functions for Sampled-Data Systems with State and Input Dependent Safety Constraints*.  
arXiv:2411.17079v2; ACC 2025.  
Primary URL: `https://arxiv.org/abs/2411.17079`.

**Previously inspected primary locators in the repository evidence:**

- Definition 1, Eq. (4);
- Lemma 1, Eq. (5);
- Theorem 1;
- all-time sampled-data safety construction without differentiating the barrier.

**Implication:** zero-order / all-time sampled-data safety is established prior art. It remains to compare exact assumptions and DDWMR/contact structure.

---

## S8 — CBF + interval analysis

**Source:** *Control Barrier Function Meets Interval Analysis: Safety-Critical Control with Measurement and Actuation Uncertainties*. ACC 2022.  
DOI: `10.23919/ACC53348.2022.9867681`.  
IEEE page inspected.

**Verified abstract-level result:**

- sampled-data control-affine systems;
- measurement and actuation uncertainty;
- interval Taylor-model reachable-set overapproximation;
- margin computation;
- safe-controller sufficient conditions;
- real-time Crazyflie experiment.

**Access limit:** consolidated pass used publisher abstract, not a complete theorem extraction.

**Implication:** combining interval reachability and sampled-data safety filtering is not generally new.

---

## S9 — WMR safety examples

Relevant recent WMR sources include:

### Ali et al., IET Control Theory & Applications 2024

*A linear MPC with control barrier functions for differential drive robots*.  
DOI: `10.1049/cth2.12709`.

Differential-drive safety/control is already populated.

### Alavi Nasab et al., ISA Transactions 2025

*Safe prescribed time controller for wheeled mobile robots by using control barrier functions as a safety filter*.  
DOI: `10.1016/j.isatra.2025.04.024`.

### Rehman et al., European Journal of Control 2026

*Robust and safe control of mobile robots using control barrier functions: Experimental results*.  
DOI: `10.1016/j.ejcon.2026.101621`.

Primary abstract explicitly reports WMR tracking + CBF-QP safety and experiments.

### Yuan et al., ISA Transactions 2024

WMR control with slippage disturbance.  
DOI: `10.1016/j.isatra.2023.11.008`.

### Zheng et al., Information Sciences 2024

WMR control with actuator saturation.  
DOI: `10.1016/j.ins.2024.120303`.

**Access limit:** for several WMR papers, only publisher abstracts/preview-level model information is currently verified. They cannot be used to claim absence of the present voltage/contact combination.

---

# 7.2 Proposed-claim comparison table

| Proposed claim | Closest prior result and locator | Matched assumptions | Actual difference currently supported | Remaining comparison | Verdict |
|---|---|---|---|---|---|
| Componentwise matrix-exponential enclosure is new | Arcak & Maidens, Prop. 1 Eq. (3)–(4), Cor. 1 Eq. (6)–(8), Algorithm 1 | Nonlinear ODE, growth matrices; their displayed result uses \(C^1\) Jacobian bounds | Current proof handles selected Lipschitz force law directly via Dini comparison | None needed to reject generic novelty | **BLOCKED** |
| Fixed unknown parameters carried through reachability is new | Arcak/Maidens Example 1 Eq. (13); Lin/Stadtherr Eq. (1) | Time-invariant uncertain parameters | Current joint fibers preserve parameter labels and correlations | Compare tightness/representation, not priority | **BLOCKED** |
| Finite predictor + validated residual tube is new | Houska et al. Sec. 3, Eqs. (3.1)–(3.4), Thm. 3.1, Cor. 3.2; Lin/Stadtherr Sec. 4 | Parametric ODE; predictor-validation; stronger smoothness/factorability in closest methods | Current residual proof only needs global Lipschitz \(\phi\) and exploits DDWMR linear electromechanical block | Need matched same-model tightness/cost comparison | **GENERIC NOVELTY BLOCKED; plant-specific benefit UNVERIFIED** |
| Rigorous flowpipe computation is new | Ariadne ODE solver; Flow* CAV 2013 | Validated nonlinear flows; tool-specific regularity | DDWMR decomposition/contact certificate may exploit structure | Run fair baseline with compatible \(\phi\) | **BLOCKED generically** |
| Inter-sample ZOH safety is new | Taylor et al. CDC 2022; Tan et al. ZOCBF; interval-CBF ACC 2022 | Sampled-data safety, bounded uncertainty in different forms | Current target explicitly includes voltage/current/wheel/slip/contact state chain and parameter-specific contact admissibility | Theorem-level matched assumption comparison | **BLOCKED generically; application-specific difference UNVERIFIED** |
| WMR collision safety with CBF is new | Ali 2024; Alavi Nasab 2025; Rehman 2026 | WMR obstacle safety but typically kinematic/transformed/servo-level models | Current formal plant includes voltage/current/wheel/body/contact chain | Full model-equation audit of closest WMR papers | **BLOCKED as broad claim** |
| A DDWMR-specific structured certificate is useful/tighter/cheaper than generic validated reachability | Houska/Ariadne/Flow*/Arcak are closest method threats | Must be made identical in model/law/uncertainty/horizon/safety test | No matched comparison yet | Required matched computational/analytic comparison | **POTENTIAL HYPOTHESIS — UNVERIFIED** |
| A nontrivial recursive safe subset for this voltage/contact plant is a contribution | Generic predecessor/viability literature + sampled-data safety literature | Generic recursion is known | No \(K_T\) exists yet | G3 construction + literature comparison | **POTENTIAL ONLY IF CONSTRUCTION IS NONTRIVIAL; UNVERIFIED** |

---

# 7.3 Novelty disposition

## Finding

The generic-method novelty branch is conclusively blocked by already identified prior art.

A narrower plant-specific hypothesis remains worth testing.

## Evidence

The most direct methodological overlaps already cover:

- componentwise reachability;
- constant uncertain parameters;
- predictor-validation;
- validated parametric integration;
- rigorous nonlinear flowpipes;
- sampled-data safety.

Current A/B/C evidence establishes correctness on synthetic examples but no matched-method advantage.

## Consequence

The only defensible current contribution hypothesis is approximately:

> **A structured certified one-hold (and potentially recursive) safety construction for the reduced voltage-driven DDWMR that exploits electromechanical/contact structure to obtain useful certified action decisions with materially better tightness or computation than a matched generic validated-reachability construction.**

This is not yet a result.

## Status

\[
\boxed{\textbf{G4 UNVERIFIED}}
\]

## Required action

Perform the matched comparison defined below and finish the primary-source audit before any originality claim.

---

# 7.4 Minimal matched comparison specification

All methods must use the same:

1. nine-state reduced plant;
2. selected contact law;
3. parameter dependence/correlations;
4. initial-state cells;
5. held voltage candidates;
6. horizon \(T\);
7. obstacles;
8. contact-validity condition;
9. outward-certification standard;
10. output semantics:
   - CERTIFIED;
   - UNKNOWN.

Do not compare:

- a certified proposed method against an uncertified floating baseline;
- a nonsmooth clip against a baseline that fundamentally cannot represent it and then call the failure an advantage.

For smooth-only baselines, either:

1. use a common admissible smooth benchmark law, e.g. a declared \(\tanh\) subcase, for both methods; or
2. use a validated baseline that genuinely supports the piecewise/Lipschitz law.

Compare:

- certified tube widths;
- collision/contact margins;
- certification coverage;
- number of cells/steps/refinements;
- runtime only after authorization;
- memory/complexity if available.

## Falsification criterion

The structured-method contribution hypothesis should be rejected or substantially reframed if a matched generic method:

- certifies the same or larger useful domain;
- gives comparable or tighter enclosures;
- has comparable or lower cost;
- and the structured DDWMR decomposition supplies no meaningful theorem or computational advantage.

In that case, the work may still be an application study, but not a new reachability method.

---

# 8. GATE TABLE

| Gate / item | Authoritative status before this review | New review result | Proposed change now? | Authorization required |
|---|---|---|---|---|
| G1 restricted model consistency | PASS | No contradiction found; not re-opened | None | None |
| Physical-platform correspondence | UNVERIFIED | Still UNVERIFIED | None | Separate future physical-validation decision |
| Case A | ACCEPT narrow | Preserved | None | None |
| Case B | ACCEPT narrow | Preserved | None | None |
| Case C | UNVERIFIED before this review | **ACCEPT narrow C.1–C.16** | Record review metadata only after user accepts | User acceptance/application of metadata |
| G2 | UNVERIFIED | **Remains UNVERIFIED** | No gate promotion | None to keep status; future evidence needed |
| G3 | UNVERIFIED; construction not authorized | Not ready; obligations specified | Do not open | Explicit user authorization later |
| G4 | UNVERIFIED | Generic branch BLOCKED; plant-specific hypothesis UNVERIFIED | No pass | More source/comparison evidence |
| Overall | HOLD | **HOLD** | None | GO only after all gates |
| Validation-only implementation policy | Not present; implementation globally blocked | Governance dependency identified | **Proposal only** | Explicit user approval required |
| Controller/simulator/hardware implementation | Blocked | Remains blocked | None | All gates + reviewed GO under current policy |

---

# 9. CONSOLIDATED SUMMARY TABLE

| Item | Analytic soundness | Finite certification | Usefulness | Novelty | Gate effect |
|---|---|---|---|---|---|
| G2 analytic framework | **VALID** in prior review | General evaluator still incomplete | UNVERIFIED | Generic machinery BLOCKED | G2 stays open |
| Case A | VALID | ACCEPT exact synthetic case | UNVERIFIED | No novelty | Evidence only |
| Case B | VALID | ACCEPT exact synthetic case | UNVERIFIED | No generic novelty | Evidence only |
| Case C | **VALID / ACCEPT narrow** | **ACCEPT exact synthetic case** | **UNVERIFIED** | No novelty | G2 stays open |
| General finite evaluator | Analytic specification partial | **UNVERIFIED** | UNVERIFIED | Infrastructure, not novelty | Major G2 obligation |
| Useful conservatism | N/A | Requires certified evaluator | **UNVERIFIED** | Can support contribution evidence | Major G2 obligation |
| Validation runtime | N/A | Not implemented | UNVERIFIED | Useful only in matched comparison | Governance decision needed |
| G3 recursive set | Specification exists | No construction | UNVERIFIED | Generic induction not novel | G3 UNVERIFIED |
| Generic reachability novelty | Sound machinery | Established prior art | N/A | **BLOCKED** | G4 remains open |
| Plant-specific structured advantage | Plausible hypothesis | No matched result | UNVERIFIED | **UNVERIFIED** | Central G4 question |
| Physical robot transfer | Outside formal proof | N/A | UNVERIFIED | N/A | Separate |

---

# 10. CONSOLIDATED WORK-PACKAGE PLAN

The goal is to minimize handoffs while keeping dependencies explicit.

## WP0 — Record Case C review + governance decision

| Field | Content |
|---|---|
| ID | WP0 |
| Gate | G2 metadata / governance |
| Concrete deliverable | Case C ACCEPT record; proposed status patch; explicit user decision on validation-only implementation policy |
| Required input | This consolidated review |
| Acceptance criterion | Case C scope recorded exactly; G2 remains UNVERIFIED; no assumption change; user explicitly approves or rejects policy split |
| Failure/reformulation criterion | If user does not accept Case C or policy split, preserve current canonical state |
| Owner | Codex prepares; GPT review if needed; user decides |
| Dependency | None |
| Authorization needed | User approval to apply canonical metadata/policy edits |

This package can be completed immediately without G3 or implementation.

---

## WP1 — G2 closure specification + benchmark protocol

| Field | Content |
|---|---|
| ID | WP1 |
| Gate | G2 |
| Concrete deliverable | One document defining `G2-COMP`: effective input class, finite evaluator algorithm, outward primitives, termination/output contract, and predeclared usefulness benchmark/metrics |
| Required input | G2 framework + accepted A/B/C |
| Acceptance criterion | Proof that every valid input halts with sound `CERTIFIED`/`UNKNOWN`; fixed parameter labels preserved; common voltage; all-time safety semantics; benchmark includes nonzero-width moving state cells and non-tuned obstacles |
| Failure/reformulation criterion | If no finite sound algorithm can be specified without hidden smoothness/independence assumptions, stop G2 method branch and report exact blocker |
| Owner | Luna may draft analytic document under existing role; root Codex integrates; GPT independently reviews |
| Dependency | WP0 not mathematically required; policy decision affects later computation |
| Authorization needed | Existing G2 analytic authorization is sufficient for document work; no code |

### WP1 mandatory benchmark properties

- benchmark chosen before method outputs are known;
- at least one moving non-rest state domain;
- state cell widths \(>0\);
- parameter widths \(>0\);
- fixed common obstacles and action set;
- no action-specific tolerance/refinement rule;
- UNKNOWN preserved as inconclusive.

### Optional stress tests

- stronger stiffness;
- contact saturation;
- very large uncertainty.

These are not new MASTER assumptions.

---

## WP2 — Validation-only evaluator + matched baseline study

| Field | Content |
|---|---|
| ID | WP2 |
| Gate | G2 + G4 |
| Concrete deliverable | Certified offline evaluator, arithmetic verification tests, matched baseline adapters, locked benchmark results |
| Required input | Accepted WP1; explicit user authorization of validation-only implementation |
| Acceptance criterion | Reproducible certified results on predeclared nontrivial benchmark; no floating samples used as proof; sound output semantics; certification coverage/margins/tube widths/cost reported; matched baseline uses same model/law/uncertainty/horizon |
| Failure/reformulation criterion | If proposed enclosure certifies no useful nontrivial domain, stop/revise G2 method. If generic baseline matches/dominates it, stop method-novelty hypothesis |
| Owner | Luna implementation role only after explicit authorization; root Codex audits; GPT reviews evidence |
| Dependency | WP1 |
| Authorization needed | **YES — explicit user authorization required** |

WP2 must not contain:

- controller implementation;
- safety-filter deployment;
- simulator performance claims;
- hardware experiments.

---

## WP3 — G4 source closure + contribution decision

| Field | Content |
|---|---|
| ID | WP3 |
| Gate | G4 |
| Concrete deliverable | Primary-source equation/theorem comparison matrix plus explicit claim decision: supported / blocked / application-only |
| Required input | Current source ledger; WP1; final computational distinction from WP2 if user authorizes it |
| Acceptance criterion | Every proposed contribution mapped to closest primary result with locator/access status; generic claims removed; surviving claim supported by actual difference, not title comparison |
| Failure/reformulation criterion | If no meaningful difference survives matched assumptions/computation, declare method novelty blocked and reframe or stop the branch |
| Owner | Codex/Luna may extend literature notes; GPT independent review |
| Dependency | Source audit can proceed in parallel with WP1; final novelty decision should consume WP2 when computational advantage is part of the claim |
| Authorization needed | Literature research is allowed by this consolidated request; code portion depends on WP2 authorization |

---

## WP4 — G3 authorization checkpoint and construction/proof

| Field | Content |
|---|---|
| ID | WP4 |
| Gate | G3 |
| Concrete deliverable | After authorization: explicit nontrivial \(K_T\), robust action set/selection, full-hold safety/contact proof, endpoint return proof and recursive induction |
| Required input | Reusable G2 evaluator or equivalent theorem over state/action regions; locked G3 nontriviality criterion |
| Acceptance criterion | \(K_T\subseteq\operatorname{Pre}_T^c(K_T)\); policy uses only allowed information; full fixed-parameter robustness; non-rest useful region; no emergency-brake/oracle shortcut |
| Failure/reformulation criterion | If only rest/singleton sets survive or no robust action exists, declare branch blocker and present conditional reformulation choices before changing MASTER |
| Owner | Not started; user must authorize G3. Luna may draft only after that; Codex/GPT review |
| Dependency | G2 evidence sufficiently mature; preferably G2 PASS |
| Authorization needed | **YES — explicit user authorization required** |

No G3 construction is performed in this report.

---

## WP5 — Optional physical-transfer package

| Field | Content |
|---|---|
| ID | WP5 |
| Gate | Separate physical validation / submission scope |
| Concrete deliverable | Support/contact mapping or certified model discrepancy; parameter identification/provenance; hardware-driver operating envelope |
| Required input | Specific platform/claim |
| Acceptance criterion | Actual trajectories justified to belong to modeled family or certified model-error enclosure on a declared domain |
| Failure/reformulation criterion | Retain reduced-model-only claims |
| Owner | Future |
| Dependency | Not required to prove reduced-model mathematics |
| Authorization needed | Separate hardware/experiment authorization |

WP5 is **not required** if the paper remains explicitly a reduced-model theoretical/computational paper and makes no physical-platform safety claim.

---

# 11. WHICH PACKAGES CAN BE COMBINED?

To reduce user relay burden:

- **WP0** should be one small governance/metadata exchange.
- **WP1 + the analytic half of WP3** can be drafted in one research bundle:
  - finite evaluator specification;
  - benchmark protocol;
  - updated primary-source claim table.
- **WP2** should be one separately authorized validation bundle because it requires code.
- **WP4** should be a separate future authorization because it opens G3.

Do not mix WP4 into WP2.

---

# 12. EXACT PROPOSED DOCUMENT EDITS — PROPOSAL ONLY

None of these edits are automatically authorized by this review.

# 12.1 Record Case C after user accepts this review

## File

`research_context/MASTER_RESEARCH_CONTEXT_v2.md`

## Section

`# 3. CURRENT DECISION`

### Existing text concept

> Current challenge artifact: `research/theorem_notes/G2_VOLTAGE_SELECTION_CASE_C_v1.md`, submitted for independent review...

### Proposed replacement

> Review evidence update (2026-09-29): GPT independently reviewed Case C C.1–C.16 on repository commit `c9ff32d45ad7f500cc2492c3bc7a69480c29c636`; the Case C mathematical file is byte-identical to the stated milestone `547061d2cc0ce1ea0c000de0ec66054034ec930f`. The exact synthetic matched-side hand certificate is ACCEPTED in its narrow scope: under one locked full-hold evaluation, \(V=(0,0)\) and \(V=(1/4,1/4)\) are CERTIFIED while \(V=(1,1)\) returns UNKNOWN. This is a certificate-output distinction only. Exact rest, the already-safe zero action, matched sides, synthetic/nonstiff data and engineered micrometer clearance prevent interpreting it as voltage necessity, practical usefulness, tracking benefit or method superiority. G2 remains UNVERIFIED.

No plant equation or assumption changes.

---

# 12.2 REVIEW_GATE Case C status

## File

`research_context/REVIEW_GATE.md`

## Current unchecked item

> Establish decision-relevant voltage-selection value: same state/parameters/locked evaluation, trace the action distinction through actuator/contact dynamics. Case C is a submitted minimal example, not accepted practical evidence.

## Proposed text

Keep the checkbox **unchecked** and replace the explanatory sentence with:

> Case C C.1–C.16 has passed independent equation review in its narrow synthetic scope and demonstrates a same-rule voltage-dependent certificate-output distinction. It does **not** satisfy this usefulness item because exact rest and \(V=0\) are already safe, the obstacle clearance is engineered, and no task/tracking tradeoff or useful operating domain is established.

This is an evidence/status clarification, not a new assumption.

---

# 12.3 DECISION_LOG Case C review record

## File

`research_context/DECISION_LOG.md`

## Proposed appended entry

> ## 2026-09-29 — HOLD — record independent Case C acceptance; G2 remains open
>
> - GPT reviewed repository commit `c9ff32d45ad7f500cc2492c3bc7a69480c29c636`; Case C's mathematical blob matches the earlier milestone `547061d2cc0ce1ea0c000de0ec66054034ec930f`.
> - C.1–C.16 are ACCEPTED as one synthetic finite hand certificate. Under the locked common evaluation, \(V=(0,0)\) and \(V=(1/4,1/4)\) are CERTIFIED and \(V=(1,1)\) is UNKNOWN.
> - UNKNOWN is inconclusive. Case C does not establish unsafe alternatives, voltage necessity, \(n=1\) necessity, practical action selection, physical-platform relevance or novelty.
> - G2/G3/G4 remain UNVERIFIED; overall HOLD. No G3 or implementation authorization follows.

Apply only after user accepts the review record.

---

# 12.4 PROGRESS_SUMMARY Case C status

## File

`docs/PROGRESS_SUMMARY_2026-09-29.md`

## Current text

> Case C — đã soạn ... đang chờ GPT review.

## Proposed new text

> Case C — **GPT ACCEPT C.1–C.16 trong phạm vi synthetic certificate-output hẹp**. Cùng một locked evaluation cho `(0,0): CERTIFIED`, `(1/4,1/4): CERTIFIED`, `(1,1): UNKNOWN`. Exact rest, zero action vốn đã an toàn, matched-side restriction và engineered micrometer clearance khiến ví dụ này không chứng minh practical voltage selection. G2 vẫn UNVERIFIED.

---

# 12.5 Proposed workflow-policy edit for validation-only implementation

**This is the most important governance proposal and requires explicit user approval.**

## File

`AGENTS.md`

## Current text

> No implementation before G1–G4 pass and reviewed GO is recorded in MASTER and DECISION_LOG.

## Proposed replacement

> Operational/controller implementation remains prohibited before G1–G4 pass and reviewed GO is recorded in MASTER and DECISION_LOG. A separate category, **validation-only research implementation**, may be authorized only by an explicit user decision recorded in MASTER and DECISION_LOG. That category is limited to certified enclosure evaluators, outward-arithmetic verification, matched baseline adapters and offline benchmark runners used to produce G2/G4 evidence. It does not authorize G3 policy construction, controller/safety-filter deployment, closed-loop performance claims, simulator validation, hardware experiments or physical-platform safety claims.

Do **not** apply without explicit user authorization.

---

## File

`research_context/MASTER_RESEARCH_CONTEXT_v2.md`

## Section

`# 3. CURRENT DECISION`

### Proposed addition only if user approves the policy

> Validation-only research implementation is a distinct evidence-generation phase from controller/operational implementation. When explicitly authorized by the user, it may contain certified enclosure evaluation, validated arithmetic, matched baseline adapters and offline benchmark execution solely for G2/G4 evidence. It does not open G3, authorize a controller/safety filter, simulator-performance claims, hardware experiments or GO. Operational implementation remains blocked until the governing gates and GO requirements are satisfied.

No formulation version increment is necessary **if** this is treated only as workflow/gate policy and no plant/theorem assumption changes. Record the user decision in DECISION_LOG.

---

## File

`research_context/REVIEW_GATE.md`

## Section

`## Review and implementation gate`

### Proposed replacement/addition

> G1 is resolved for the restricted model. G2 analytic research is authorized. G3 construction still requires separate explicit authorization. Validation-only research implementation, if separately authorized by the user and recorded canonically, is limited to certified evaluator/baseline/offline benchmark evidence for G2/G4 and is not GO or controller implementation. Controller/simulator deployment/hardware/experiment implementation remains prohibited until the governing gates pass and reviewed GO is recorded.

Again: proposal only.

---

# 12.6 G2 acceptance text proposal

After WP1/WP2 evidence exists — **not now** — `REVIEW_GATE.md` should use a criterion approximately:

> G2 PASS requires a reviewed sound finite evaluator over a declared effective input class, fixed-parameter/common-voltage semantics, full-hold collision/contact certification, finite termination with explicit UNKNOWN semantics, and evidence of nontrivial usefulness on a predeclared moving-state benchmark domain. Failure to certify a cell is inconclusive.

Do not mark it PASS now.

---

# 13. RESEARCH RECOMMENDATION

## Finding

The current reduced-model scope remains worth continuing.

No plant reformulation is justified by this consolidated review.

## Evidence

- G1 is internally coherent.
- G2 analytic theory survives independent review.
- A/B/C now stress distinct mechanisms.
- The unresolved issues are evaluator/usefulness/novelty/recursion, not a detected contradiction in the plant.

## Consequence

Continue current scope, but change the research question from:

> can we make more certificates?

to:

> can the structured DDWMR certificate be made reusable, useful and demonstrably distinct from matched validated reachability?

## Status

**CONTINUE CURRENT SCOPE**

with one branch stopped:

\[
\boxed{
\text{generic-method novelty branch = STOP / BLOCKED}
}
\]

## Required action

Execute WP1 and source-level WP3 now.

Seek user decision on validation-only implementation before WP2.

Do not open WP4/G3 construction yet.

---

# 14. SINGLE CODEX HANDOFF INSTRUCTION

Codex should interpret this report as follows.

## Work allowed immediately under current authority

1. Prepare a **Case C review-record/status patch** reflecting the narrow ACCEPT result, but do not apply it until the user authorizes canonical synchronization.
2. Draft **WP1**:
   - effective G2 computational input class;
   - finite evaluator algorithm;
   - soundness/termination theorem;
   - explicit `CERTIFIED` / `UNKNOWN` semantics;
   - locked benchmark protocol and metrics.
3. Continue **WP3 source work**:
   - fill theorem/equation locators;
   - keep access limitations;
   - maintain generic novelty blockers;
   - prepare the matched-comparison specification.
4. Prepare, but do not apply, the proposed workflow-policy diff for validation-only implementation.

Suggested artifact names:

- `research/theorem_notes/G2_FINITE_EVALUATOR_SPEC_v1.md`
- `research/benchmarks/G2_USEFULNESS_BENCHMARK_SPEC_v1.md`
- `docs/reviews/G4_MATCHED_PRIOR_ART_COMPARISON_v1.md`
- `docs/proposals/VALIDATION_ONLY_IMPLEMENTATION_GATE.patch`

## Decisions requiring the user

1. Accept/record Case C review metadata.
2. Approve or reject the **validation-only research implementation** gate split.
3. Later, after G2 is sufficiently mature, explicitly authorize G3 construction.

## Work currently blocked

- controller implementation;
- safety-filter implementation;
- G3 \(K_T\) construction;
- simulator performance claims;
- interval-solver coding unless validation-only implementation is explicitly authorized;
- hardware/experiment work;
- physical-platform safety claim;
- GO.

Do not promise that WP1–WP4 will necessarily pass their gates.

A failed benchmark or prior-art comparison is a valid research result and should stop/reframe the affected branch.

---

# 15. FINAL DISPOSITIONS

## Case C

\[
\boxed{
\textbf{ACCEPT C.1--C.16 — narrow synthetic certificate scope only}
}
\]

## G2

\[
\boxed{
\textbf{UNVERIFIED}
}
\]

Reason: general finite evaluator and useful benchmark evidence remain missing.

## G3

\[
\boxed{
\textbf{UNVERIFIED — construction not authorized}
}
\]

Reason: no useful \(K_T\), robust endpoint return or selection proof exists.

## G4

\[
\boxed{
\textbf{UNVERIFIED}
}
\]

with:

\[
\boxed{
\textbf{generic-method novelty BLOCKED}
}
\]

and one plant-specific contribution hypothesis still worth testing.

## Physical-platform correspondence

\[
\boxed{
\textbf{UNVERIFIED}
}
\]

## Overall

\[
\boxed{
\textbf{HOLD}
}
\]

No GO.

No G3 construction.

No controller/simulator/hardware implementation authorization.

No promise that the remaining gates will close.

---

# 16. BOTTOM LINE FOR CODEX

The research has moved beyond “no finite certificate exists”:

- analytic enclosure framework exists;
- A/B/C supply accepted finite synthetic evidence if the user records this Case C review.

But the central paper-level questions are still open:

\[
\boxed{
\text{Can the certificate be made generally finite and useful on a predeclared nontrivial domain?}
}
\]

\[
\boxed{
\text{Can it support a useful recursive safe subset without forbidden backup assumptions?}
}
\]

\[
\boxed{
\text{Does its DDWMR structure provide a real contribution beyond established validated reachability and sampled-data safety methods?}
}
\]

Those questions correspond to G2, G3 and G4 respectively.

The correct current scientific posture is therefore:

\[
\boxed{\textbf{continue the reduced-model research, preserve HOLD, and attack the remaining evidence gaps directly.}}
\]
