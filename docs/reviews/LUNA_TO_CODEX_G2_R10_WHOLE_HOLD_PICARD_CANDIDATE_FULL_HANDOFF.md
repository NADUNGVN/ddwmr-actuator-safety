Session: DDWMR | LUNA-G2-SCOPE

# G2 R10 whole-hold Picard candidate — full handoff

**Date:** 2026-10-04  
**Assignment:** docs/CODEX_TO_LUNA_G2_R10_WHOLE_HOLD_PICARD_CANDIDATE.md  
**Disposition:** mathematical proof contract, offline producer/checker pair, source-bound two-row development manifest, fixtures, and direct-source closure are prepared. The R10 candidate is **not frozen, not authorized, and not run**.  
**Execution:** 0 native query calls; 0 R10 evaluations of the two R6 inputs; 0 R6 reruns; R5 remains 800/800 NOT_RUN. No commit or push.

## 1. Result and evidence boundary

R10 replaces the R9 first-exit argument with a closed-slab Picard fixed-point proof. A completed record contains an ordered rational slab partition of the whole hold, internal-state enclosures and endpoint carry, pose tube and pose carry, per-slab collision/contact lower margins, and additive progress lower bound. The independent checker rebuilds and compares the complete record from the query and model, rather than accepting a proof-status flag or digest alone.

The mathematical argument is complete under the explicitly stated interval-RHS and fixed-parameter assumptions below. The implementation passed synthetic non-query fixtures, including an actual adaptive binary split. Neither locked R6 input was evaluated by the R10 producer. Thus there is no R10 inclusion sequence or R10 safety/task result for either input, and this handoff does not update the two stored R6 UNKNOWN outcomes. G2 remains UNVERIFIED; this work does not establish practical voltage-selection value or physical-platform correspondence.

The minimal-stage manifest preserves the two existing development inputs, their query and input hashes, and their consumed R6 UNKNOWN outcomes. It is PREPARED_NOT_FROZEN_NOT_AUTHORIZED_NOT_RUN. It grants no evaluation authority.

## 2. Whole-hold Picard theorem contract

### State, inputs, and quantifiers

Let the six internal coordinates be
\[
z=(u,r,\omega_L,\omega_R,i_L,i_R),
\qquad
\dot z=f(z,V;\vartheta)
=A(\vartheta)z+B(\vartheta)V+D(\vartheta)F(z;\vartheta).
\]
The model is the unchanged reduced v2.1 plant and clip law. The initial nine-state query box is projected to an internal box \(X_0\) and a pose box \(P_0=(P_x,P_y,\Theta)\). Each physical execution has one initial state in that box, one joint parameter label \(\vartheta\in\Theta\) held fixed for the complete execution, and one exact voltage vector \(V\) held over the complete declared horizon \(T\).

On every slab the interval model constructor uses the same full joint-label image and the same held voltage. Rational interval evaluation can forget correlations among labels, coefficient maps, and states. The resulting outer relaxation may be wider and may enclose combinations that do not correspond to any one physical label. This is an overapproximation effect; it does not assert that a physical parameter switches between slabs. R10 does not split the parameter-label set. If a later version does so, it must create stable leaf IDs once and carry each fixed leaf through every slab.

For a closed rational candidate box \(B_k\) and slab duration \(h_k>0\), the source-bound interval model must compute \(G_k\) satisfying
\[
f(z,V;\vartheta)\in G_k
\quad\text{for every }z\in B_k\text{ and every fixed }\vartheta\in\Theta.
\]
The source implementation uses exact rational interval evaluation of the matrix decomposition and clip law. Positive lower bounds on the denominators and physical coefficients are checked by the model constructor.

### Uniform Lipschitz bound

The clip law is globally 1-Lipschitz. In the scaled internal coordinates, the implementation computes the rational upper bound
\[
L=\max_i\left(
\sum_\ell \overline{|A_{i\ell}|}
+\sum_{j\in\{L,R\}}\overline{|D_{ij}|}
\frac{\overline C_j}{\underline v_s}
\sum_\ell\overline{|S_{j\ell}|}
\right).
\]
For each fixed \(\vartheta\), interval coefficient bounds therefore give
\[
\|f(z_1,V;\vartheta)-f(z_2,V;\vartheta)\|_\infty
\le L\|z_1-z_2\|_\infty .
\]
This is a uniform bound over the declared image, not a claim that the interval hull preserves parameter correlations.

### Closed-slab inclusion and fixed point

Each accepted slab must satisfy both
\[
X_k\subseteq B_k,\qquad
X_k+[0,h_k]G_k\subseteq B_k. \tag{R10-P}
\]
Fix any one \(z_0\in X_k\) and any one fixed label \(\vartheta\in\Theta\). On the complete path space of continuous paths with values in the closed box \(B_k\), define
\[
(\mathcal Pz)(t)=z_0+\int_0^t f(z(s),V;\vartheta)\,ds .
\]
Since the exact vector field on \(B_k\) is enclosed by \(G_k\), coordinatewise integration gives
\[
(\mathcal Pz)(t)\in X_k+[0,h_k]G_k\subseteq B_k.
\]
Thus \(\mathcal P\) maps this path space into itself. In the Bielecki norm
\[
\|z\|_\lambda=\sup_{t\in[0,h_k]}e^{-\lambda t}\|z(t)\|_\infty
\]
choose the exact rational \(\lambda=L+1\). Then
\[
\|\mathcal Pz-\mathcal Pw\|_\lambda
\le \frac{L}{\lambda}(1-e^{-\lambda h_k})\|z-w\|_\lambda
<\|z-w\|_\lambda ,
\]
because \(L/(L+1)<1\). Banach's fixed-point theorem gives a solution on the **closed** slab that remains in \(B_k\). Integrating at the right endpoint yields
\[
X_{k+1}=X_k+h_kG_k
\]
as an enclosure of every possible endpoint.

This argument closes the boundary gap in the R9 first-exit proof: it requires no strict-interior inclusion and does not infer a contradiction merely from boundary membership.

### Whole-hold induction, pose carry, and progress

The deterministic traversal is left-to-right. The first slab starts from the projected declared initial internal box \(X_0\) and pose box \(P_0\). Each next internal start is exactly the preceding \(X_k+h_kG_k\); the next candidate box must contain that start. The next pose start is exactly the preceding rational pose endpoint. The accepted rational start times are contiguous, the durations sum exactly to \(T\), and every slab uses the same \(V\) and full parameter image. Induction over this finite list therefore encloses every fixed-label trajectory through the closed full hold.

For each slab, physical \(u,r\) intervals from \(B_k\) give the heading tube
\[
\Theta_k+[0,h_k]R_k.
\]
Rational Taylor outer bounds enclose sine and cosine on that interval. Multiplying them by the \(u\) interval gives \(U_x,U_y\), from which R10 forms the full local pose tube and the pose endpoint box. The endpoint is carried to the next slab. The collision lower margin is the directed distance from the entire rectangular position tube to the declared obstacle center minus the unchanged exclusion radius.

Contact uses the same internal slab and parameter image. The clipped normalized-slip absolute upper bounds give per-wheel support lower bounds
\[
\underline C_j\,\underline{\sqrt{1-\beta_{j,k}^2}},
\]
and the algebraic demand is upper-bounded by
\[
\overline m\,\sup_{B_k}|u|\,\sup_{B_k}|r|.
\]
Every slab must have nonnegative collision and contact lower margins for a safety certificate. These are sufficient tests of the declared reduced-model conditions; they do not validate tire or support mechanics on a physical platform.

The additive task-progress lower bound is
\[
J^-=\sum_k h_k\inf(U_k\cos\Theta_k).
\]
The unchanged threshold is \(1/20\) m. Safety certification requires the Picard sequence and all-slab safety margins; task eligibility additionally requires \(J^-\ge1/20\) m. A negative sufficient lower bound means the test did not establish the property; it is not evidence of a physical collision, contact failure, or negative actual displacement.

## 3. Deterministic candidate construction and outcome semantics

The default construction starts from one rational slab of duration \(T\). For each start box \(X_k\), it computes \(G(X_k)\) and the deterministic seed radius
\[
\rho_{k,i}=h_k\left(\sup|G_i(X_k)|+s_k/64\right),
\qquad
s_k=\max(1,\|X_k\|_\infty).
\]
It tries the finite boxes
\[
B_k^{(j)}=X_k+[-2^j\rho_k,2^j\rho_k],
\quad j=0,\ldots,J-1,
\]
recomputing \(G_k\) and the Picard tube for each candidate. It accepts only after checking R10-P. If the declared expansion trials fail, it bisects the time slab exactly in half, processes the left child first, and starts the right child from the left endpoint enclosure. Exhausted split depth returns UNKNOWN.

The finite limits are:
- base slab count at most 8 (default 1);
- binary split depth at most 4, with at most 31 tree nodes per base slab;
- at most 8 candidate expansions per node;
- rational numerator/denominator bit cap 8192;
- rational operation cap 500,000;
- cooperative per-record wall cap 30 seconds;
- trigonometric Taylor degree at most 18;
- square-root bisection count at most 48.

The configured caps are serialized and replayed. Arithmetic-cap exhaustion is fail-closed. The wall limit is checked cooperatively during rational operations; a producer timeout returns UNKNOWN and a checker replay timeout is INVALID_RECORD because replay did not complete. A timed-out record cannot support a positive claim.

The record status distinction is:
- **CERTIFIED:** complete whole-hold Picard sequence and nonnegative collision/contact sufficient margins on every slab. The separate task_eligible field also checks the 1/20 m progress threshold.
- **UNKNOWN:** failed candidate inclusion, exhausted deterministic/resource budget, or a complete enclosure whose sufficient safety margins do not all pass. UNKNOWN never means a proven physical violation.
- **INVALID_RECORD:** checker outcome for malformed serialization, bad self-digest, source/query/model/voltage/initial-box mismatch, altered or missing/reordered slabs, broken endpoint/pose carry, incomplete time coverage, altered margins, or ambiguous/incomplete replay.

The returned CERTIFIED status is a mathematical reduced-model enclosure result only. No R10 record was generated for either R6 row in this assignment.

## 4. Implementation and independent replay

| Responsibility | R10 artifact | Check performed |
|---|---|---|
| Rational slab producer | validation/g2/time_slab_picard_r10.py | Computes fixed-label RHS intervals, candidate expansion/split tree, Picard inclusion, internal endpoints, pose/contact/collision margins, and progress. It does not call the R3 evaluator. |
| Independent checker | validation/g2/whole_hold_picard_checker_r10.py | Imports no R10 producer helpers. It independently rebuilds query bindings, model image, Lipschitz bound, every candidate and split, RHS, inclusion, carry, pose tube/endpoints, margins, progress, and final status. It compares the complete recomputed record to the submitted record after checking the digest. |
| Read-only source binder | validation/g2/r10_source_binding.py | Reconstructs the exact two allowed logical queries from R5/R6 lineage, validates the R10 and predecessor closures, verifies the consumed R6 evaluation/terminal/publication bindings, and checks R5's full 800-row NOT_RUN denominator. It has no native-query call. |
| Proof contract | research/benchmarks/G2_R10_WHOLE_HOLD_PICARD_CONTRACT_v1.md | Full assumptions, theorem, deterministic construction, resource caps, output meanings, and evidence boundary. |
| Two-row candidate manifest | research/benchmarks/G2_R10_WHOLE_HOLD_PICARD_CANDIDATE_MANIFEST_v1.json | Source-bound development pair, prior R6 outcomes, trigger, stop rules, and no-authority declaration. |
| Synthetic fixture declaration and runner | validation/configs/g2_r10_whole_hold_fixtures_v1.json; validation/scripts/verify_g2_r10_whole_hold_fixtures.py | Finite non-query positive, split, cap, and negative binding fixtures. |
| Read-only lineage audit | validation/scripts/audit_g2_r10_candidate_manifest.py | Checks both exact row bindings and reports zero R10/R6 reruns and 800 R5 rows not run. |
| Source closure builder | validation/scripts/build_g2_r10_source_closure.py | Extends the reviewed R9 source closure with the R10 contract, candidate artifacts, and implementation inputs. |

The independent checker deliberately shares the audited exact rational/interval primitives, trigonometric/root primitives, and ModelIntervals parser with the producer. The proof transition, inclusion, state/pose carry, margins, aggregation, status derivation, and full-record comparison are separately implemented. This is algorithmic replay independence, not a claim of independent implementation for every arithmetic primitive or parser. Shared primitive/parser defects remain a review surface.

The source binder imports the read-only R6 adapter path to verify the existing lineage. That path imports the evaluator module for query-hash helpers, which defines run_query, but neither the binder nor this audit invokes run_query. The R10 producer, checker, and audit scripts contain no run_query call. No native evaluator or producer alias was executed.

The checker rejects the assignment's specified mutations. A deterministic operation-cap UNKNOWN was replayed successfully; an ambiguous wall-time replay is refused. The report does not claim runtime replay of a real R6 record.

## 5. Synthetic validation and read-only audit

Executed:
1. python -B validation/scripts/verify_g2_r10_whole_hold_fixtures.py — PASS_R10_SYNTHETIC_NONQUERY_FIXTURES.
2. python -B validation/scripts/audit_g2_r10_candidate_manifest.py — PASS_READ_ONLY_R10_SOURCE_AND_INPUT_BINDING.
3. python -B validation/scripts/build_g2_r10_source_closure.py — PASS_R10_SOURCE_CLOSURE_WRITTEN, 163/163 source inputs present and matching.
4. AST parsing of the six R10 Python producer/checker/binder/script files — PASS.

Fixture result:
- 12 declared groups, all finite synthetic/non-query or negative record checks;
- a two-slab synthetic whole-hold certificate independently replayed as CERTIFIED and task-eligible;
- a stiff zero-state case where the root-slab inclusion fails, one binary split creates two accepted half-slabs, and independent replay returns CERTIFIED;
- a 10-operation-cap case returns UNKNOWN and independently replays as UNKNOWN;
- 17 negative/mutation/binding records rejected as INVALID_RECORD, including a changed declared initial pose and a broken pose carry into the second slab;
- 0 native query calls and 0 R6 inputs evaluated.

Read-only row audit:
| Order | R5 index | Query | Canonical query SHA-256 | Input payload semantic SHA-256 | Preserved R6 result |
|---:|---:|---|---|---|---|
| 0 | 12 | S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_L0_R0 | d5648569b11c576c8cc0ecb07c5096c21b06fe3a5e849358f254770649465471 | 422afd0448a184f4f67262c6338593c871739b41fb677e8ab1d6b566d18b93ac | consumed UNKNOWN |
| 1 | 24 | S_LOW_NEG__D_NEAR_CENTER__T_250MS__V_Lp1_Rp1 | 105a0710185446312933ec8c92922acd1db0f3af0e999d67207ccd70534b4808 | 70301bc5df76aab2dfdb8bef5135592fbf0063af6799b0f0eb119f4873b2cf9a | consumed UNKNOWN |

The stored R6 evaluation raw hashes remain 8d8f48d4c8bd3c6840d09ed32579e3796f81499e58b7a8ed60fba3b825487306 and d93419ed11d68082c1f6676468326e88e66913d871c8edf1e37f003076686ece. The R5 manifest raw hash remains 0c5b4b42be56393676dc1c0570f437900dc6bdd354d143d4a657f7e05a49a81b; its 800 rows remain NOT_RUN. The R6 publication raw hash pinned in the manifest is 3e55c3b967b661f3a3c3b5aa70ae4bc7cf8e9bab463ec484a4e5865f3db5b33d.

## 6. Prepared two-action stage and decision trigger

The manifest retains R5 indices 12 then 24, their exact query/input hashes, and the two prior consumed R6 UNKNOWN records. They remain development-overlap observations selected after R5 UNKNOWN; they are not independent test or confirmatory rows. The prior R6 outcomes are lineage diagnostics, not new R10 attempts.

The predeclared design trigger is true only if the positive-voltage row is later certified and task-eligible at or above the fixed 1/20 m threshold while the zero-voltage row lacks that combined result. This is a future design trigger only; it is not evidence of usefulness, voltage necessity, physical safety, or G2 PASS.

One-shot stop rules:
1. No execution until Codex independently reviews and accepts the exact producer/checker/closure and issues separate exact-scope execution authorization.
2. Once intent is issued for either row, do not retry, replace, reorder, or select another input.
3. Stop on source/input/closure mismatch, malformed or partial output, checker rejection, resource cap, timeout, or publication failure.
4. If either row is UNKNOWN, checker-invalid, not task-eligible at 1/20 m, or has a negative collision/contact sufficient bound, the trigger is false; this pair does not authorize or motivate the 800-row study.
5. Keep both rows marked development_overlap; they are not independent or confirmatory observations.

The manifest explicitly says execution authority was not granted. The current assignment granted no R6 query, R10 row evaluation, or broader study.

## 7. Source identities

The R10 source closure inherits the reviewed R9 closure and adds the versioned R10 inputs. It contains 163 direct path/hash entries: 149 inherited from R9 and 14 R10 additions. The builder rehashed every entry and reported zero missing files and zero mismatches.

| Artifact | Raw SHA-256 |
|---|---|
| R9 parent source closure | 2bcb15b82158d01684b8ec043b7279b41e6e95952c6238fb24d2a54f76ec10fa |
| R10 candidate manifest | 0bddb54bc0c2ab97687921e44bb5f376807250277bd10192d70551f062fbd9e5 |
| R10 proof contract | 8d90491ad16e62431fe078545dfc9c640633179cd62eb5bc3eb23d6949d32a9f |
| Producer | e9fa6672649d675e27bb4f419e28259b9546b01bb6592f3388396ecd2a211c47 |
| Independent checker | 6ba67a808bc9e5125cbf8112265c3a074a9b005566ef02d06e6121825e150783 |
| Read-only source binder | c3e7057a4d02353c496fd7d0481a577834a53d5f45baa0f3f5f343bdd2176d05 |
| Fixture declaration | 0e8dc22cc06d7b0e5bb321b9befcc79c918ff002de655bec60156a89fd54a61d |
| Fixture runner | 7bccc5545efaecd7d49f762044c23443d367f5e784c177d01dbcc8e93f0a7af7 |
| Read-only manifest audit | 442f0b8d0cde5735364a705f063c2d4f3d40f78ef140465e661b1c1354f03f36 |
| Closure builder | 691b09c98b045ea1ad2410909f1926c0197aaa05d4fbf1fdbe1a7d66bbbc5123 |
| R10 source closure raw | 63a7af65317b683345c54a0bc377935cf907260a944d1b1234473193fcedf6d9 |
| R10 source closure semantic JSON | a2512ecb1246fbfd2b8b536fd05b55b9e514d5e073719b3ad0804549ada41dcc |
| R10 source-closure sidecar | 967fd8628bf4a99f012175ff3b5c2bb650489fc0f9a3a3ef223d63446b7d7c2f |

Writes for this task were limited to the assigned R10 G2 proof, producer/checker, binder, manifest, fixture, closure, and handoff paths. All 149 inherited R9 source entries rehashed successfully; no G4 source or manifest was edited, and the shared-tree G4 work was left untouched. No branch switch, commit, or push was performed.

## 8. Unresolved scope and conclusion

There is no remaining missing inequality in the stated whole-hold proof contract: the conditional Picard existence, self-inclusion, endpoint carry, full-time slab induction, pose carry, safety margins, and progress aggregation are specified and encoded. The remaining application evidence is intentionally absent because this assignment prohibited running the two R6 inputs. In particular, neither R6 row has any R10 candidate box, verified R10-P inclusion, whole-hold collision/contact margins, or new progress lower bound.

The next review should independently inspect the proof assumptions and source closure, pay particular attention to the shared interval/model primitives and resource-limit semantics, and decide whether this exact offline candidate merits any separate execution authorization. The stored R6 UNKNOWN results stay UNKNOWN, R5 stays 800/800 NOT_RUN, and G2 stays UNVERIFIED until later evidence is reviewed.
