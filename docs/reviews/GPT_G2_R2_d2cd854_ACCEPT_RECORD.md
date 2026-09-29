# GPT G2 R2 review record — Case A accepted

Recorded 2026-09-29 from the complete 30-section review pasted by the user. Repository `NADUNGVN/ddwmr-actuator-safety`, branch `main`, reviewed commit `d2cd85407bb5ba4b4360836c49aa8a9c7ec83f28`.

**Provenance:** This is a structured disposition record, not a verbatim transcript or a new Codex verification. The user relayed GPT's full equation/arithmetic review and instructed that it be recorded. No GPT browser access was used.

## Findings accepted in the incoming review

| GPT sections | Result | Disposition |
|---|---|---|
| 1 | Corrected n=1 voltage-dependence wording; no guaranteed nonzero/monotone effect | VALID |
| 2 | A.1--A.3 clip function, L_phi, parameter box, units, initial slips, ideal-gear witness | VALID; synthetic only |
| 3--4 | A.4--A.9 motor exponential, predictors, a=77/160, c_d=847/960, full-cell ranges | VALID |
| 5--7 | A.10--A.12 Metzler semigroup comparison, rational exponential tail, global radius | VALID |
| 8--9 | A.13--A.16 refined body/wheel/current bounds and full-slab fallback | VALID |
| 10--11 | A.17--A.18 pose budgets and continuous collision margins | VALID |
| 12 | A.19 beta bounds; all certified slips lie in the linear branch of clip | VALID; important limitation |
| 13--14 | A.20--A.22 square-root reserve, ur demand, positive contact margin | VALID |
| 15 | A.23, common held voltage for every fixed capacity pair and every time | VALID / ACCEPT |
| 16--17 | Finite primitive ledger and existence of one fully instantiated hand certificate | VALID for this case; general evaluator unresolved |
| 18 | H/G=11/16 and F/G=4 describe upper budgets, not actual reachable-width ratios | VALID |
| 19 | Practical usefulness | UNVERIFIED |
| 20--21 | Generic predictor-validation/reachability originality | BLOCKED; overall novelty UNVERIFIED |
| 22--25 | Parameter-dependent actuator challenge, provenance, certificate usefulness, eventual tractability | Required G2-only research |
| 26--30 | Gate separation and next action | Case A ACCEPT; G2 UNVERIFIED; HOLD |

## Accepted scope

For the exact synthetic data in [Case A](../../research/theorem_notes/G2_FINITE_CERTIFICATE_CASE_A_v1.md), one common V=(1/2,-1/2) held on [0,1/10] gives, for every execution-fixed (C_L,C_R) in [1,11/10]^2 and every time in that interval,

\[
g_p\ge74867/1000000\ \mathrm m>0,\qquad
g_c\ge491949/250000\ \mathrm N>0.
\]

GPT accepted the proof as a finite, nonsampled certificate of collision and ideal-contact safety of the stipulated reduced model. It establishes no physical parameter identification, hardware safety, general solver, practical relevance, safe action necessity, recursion or originality.

## Finding

The independent review accepts A.1--A.23. The former absence of any finite instantiated certificate is now obsolete.

## Evidence

GPT checked every equation group and primitive, including independent exact arithmetic for the refined body bound 1310309/24000000000 and the positive collision/contact margins. The reviewed equations remain in Case A and its identified Git commit.

## Consequence

One finite hand-derived synthetic certificate exists. General certified evaluation, defensible data, useful conservatism, decision-relevant voltage dependence and tractability remain unresolved.

## Status

**VALID / ACCEPT for Case A only. G1 restricted PASS; G2/G3/G4 and physical correspondence UNVERIFIED; HOLD.** Generic-method novelty remains BLOCKED.

## Required action

- Record acceptance without promoting G2.
- Continue G2-only Case B with parameter-dependent actuator matrices and a joint fixed-parameter cell preserving gear/conversion correlations.
- Prefer reduced slack and nonlinear contact behavior. Seek a refined-certificate success versus a declared coarse-certificate UNKNOWN result; UNKNOWN never proves physical unsafety.
- Separate synthetic, literature/model-supported and platform-identified data.
- Only analytic finite-operation structure is currently permitted; runtime measurements await implementation authorization.
- Continue matched-assumption prior-art comparison. No plant amendment is requested.
- No G3 construction, controller, simulator, interval solver, experiments or GO is authorized.
