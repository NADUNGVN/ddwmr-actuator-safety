# G4 matched comparison — WP3 research specification v1

2026-09-29. **DRAFT; G4 UNVERIFIED; generic-method novelty BLOCKED; HOLD.** This supplement does not upgrade the canonical matrix or authorize implementation. Read the consolidated GPT handoff and MASTER first.

## Finding

The existing enclosure architecture has direct prior art. The remaining hypothesis concerns an advantage from the DDWMR actuator/contact structure on a declared domain, not originality of prediction followed by validation.

## Evidence — bounded primary-source audit

The following passages were independently retrieved in this Codex pass. This is a targeted comparison, not a full systematic review or reproduction of these methods.

| Source and exact inspected location | Established scope | Comparison obligation |
|---|---|---|
| [Arcak and Maidens, arXiv:1709.06661v1](https://arxiv.org/html/1709.06661v1), §2 Prop. 1, Eqs. (3)–(4), Cor. 1 Eqs. (6)–(8) | C1 dynamics; componentwise growth bounds and matrix exponentials bound trajectory separation on a justified domain. | Our Lipschitz-force/Dini proof avoids a contact derivative, but a generic Lipschitz enclosure remains a fair comparator. A numerical reference trajectory must itself be validated. No priority claim for growth matrices. |
| [Houska, Villanueva and Chachuat, author manuscript](https://faculty.sist.shanghaitech.edu.cn/faculty/boris/paper/stableSetIntegrator.pdf), §3 A1–A3, Eqs. (3.1)–(3.4), Thm. 3.1 and Cor. 3.2 | Smooth/factorable parametric ODE and initial data, compact parameter enclosure; predictor-validation bounds the complete validated time segment. | Finite predictors and full-time residual validation are not new. A nonsmooth clip benchmark cannot be used as an unqualified test of this displayed smooth construction. Compare on a common supported law or document a sound extension. |
| [Lin and Stadtherr, author manuscript](https://academicweb.nd.edu/~markst/lin-stadtherr-vspode-apnum.pdf), §2 Eq. (1), §3.1 | Time-invariant uncertain parameters and initial intervals; stated state/parameter differentiability requirements; branch/abs/min/max excluded from the displayed representation. Directed outward arithmetic is explicit. | Fixed uncertainty and validated parametric integration are prior art. Their assumptions must be matched before timing or coverage comparisons. Do not convert a regularity mismatch into an advantage. |
| [Collins et al., Ariadne arXiv:2306.17541v2](https://arxiv.org/html/2306.17541v2), introduction and §6.2 as identified in prior R2 supplement | Rigorous function models and ODE-solving infrastructure. | This pass confirms the accessible primary version and general scope; exact installed solver/configuration support for the proposed law remains unverified. Do not present a tool-name comparison as an implemented matched baseline. |

The consolidated GPT review additionally identifies interval-CBF ACC 2022 (DOI `10.23919/ACC53348.2022.9867681`) and other sampled-data/robot sources. Those additions remain reviewer-reported leads in this supplement; they have not received a new equation-level audit here. Existing access limits for Flow*, WMR papers and earlier matrix entries remain in force.

## Consequence — admissible claim table

| Proposed claim | Disposition now | Evidence needed |
|---|---|---|
| Predictor plus certified residual is new | BLOCKED | No further hand case rescues this broad claim |
| Fixed parameters or all-time tube checking is new | BLOCKED | Remove as standalone novelty |
| The signed actuator kernel improves a chosen outward radius | Accepted for the specific A/B calculations only | Reusable construction, same-data comparison and finite arithmetic errors |
| Structured enclosure yields a useful certification advantage | UNVERIFIED | Locked moving-state benchmark, matched validated baseline, reproducible coverage/cost tradeoff |
| Method gives a useful recursive safe region | UNVERIFIED | Separately authorized G3 construction and its proof; not provided here |

## Status

**WP3 PARTIAL.** Source-level generic overlap is established; the application-specific contribution hypothesis is still untested. No priority, superiority or G4 PASS claim follows.

## Required action — matched-comparison contract

### 1. Common scientific problem

All compared methods must receive identical nine-state equations, fixed parameter-image labels and correlations, initial state cells, held voltage list, horizon, footprint/obstacles and contact-validity target. State cells describe a batch of exact initial states for verification; they do not introduce state-estimation uncertainty into MASTER. One action must work for all states in a reported certified cell and every hidden realization.

Keep parameter labels fixed over the entire hold. A method may overapproximate correlations but must label that relaxation and quantify its effect; a switching-parameter method must not be described as the exact fixed-parameter benchmark.

### 2. Baseline ladder

- **Internal ablations:** selected global comparison, exact-kernel refinement and finite fallback, all with outward error propagation. These isolate the kernel/refinement contribution; they do not substitute for an external prior-art comparison.
- **Generic Lipschitz baseline:** a full-state validated enclosure on the same piecewise-linear law, with a sound rough-domain inclusion and complete time coverage. Its algorithm and arithmetic must be specified and independently reviewed before use; merely naming interval Picard does not complete this obligation.
- **Established tool/method baseline:** audit one applicable validated integrator and its version/configuration. If a smooth-only baseline is selected, create a separate common smooth-law sub-benchmark for both methods, with its own validated primitive contract. Never smooth only the baseline plant or substitute floating integration.

The last baseline is still OPEN. Choosing a documented general method, demonstrating compatibility and reproducing it faithfully are prerequisites for any external superiority claim.

### 3. Common decision and reporting layer

Require enclosure of the full hold and apply a common sound collision/contact checker. If one representation enables a better checker, report enclosure-only and checker-inclusive comparisons separately; do not attribute their combined difference solely to the motor kernel. Endpoint enclosure is a separate output, not a recursive certificate.

For each predeclared original state-action cell, report CERTIFIED or UNKNOWN, lower collision/contact margins, pose/internal widths, label/time subdivisions, primitive counts and termination reason. Preserve the original cell denominator after refinement. INVALID_INPUT and implementation failure are separately reported, never silently excluded or relabeled as mathematical UNKNOWN. All-action UNKNOWN means no certified action found by this procedure.

Use two comparison views: (i) the same bounded work ladder for each method, and (ii) work required to obtain the same declared certification target, with resource caps and censored failures explicit. Equal interval order alone is not equal cost. Runtime is measured only after authorization; until then it is UNVERIFIED.

### 4. Locking and falsification

Review and version the benchmark before any outputs. Preserve all valid cells, including UNKNOWN. No method-specific obstacle placement, tolerance or action exclusions. Use separate development and locked comparison manifests if tuning is later authorized. A post-lock change creates a new protocol version and retains previous results.

If a matched general method achieves equal/better certification and comparable/better widths and cost, and no separate theorem advantage survives, report the structured-method advantage as unsupported on that domain. This is not a universal impossibility theorem. A mixed outcome requires a scoped claim rather than an aggregate winner chosen after inspection. Numerical superiority thresholds, if desired, must be justified and fixed before execution; no threshold has been invented in this document.

### 5. Remaining evidence

1. Reviewed finite evaluator and benchmark specification (WP1).
2. A selected, applicable, fully specified external baseline.
3. An authorization covering the exact validation work before coding/running WP2.
4. Machine-readable artifacts and independent audit of every claimed certificate after authorized implementation.
5. A final equation/theorem/source comparison against the surviving claim. This supplement alone does not close G4.
