# Codex disposition — GPT G4 Auer R2 strategy review

**Date:** 2026-09-30  
**GPT handoff:** `docs/reviews/GPT_TO_CODEX_G4_AUER_R2_STRATEGY_FULL_HANDOFF.md`  
**Local branch / HEAD:** `luna/g2-validation-v1` / `aac7a369d0cf0cfa4e9e9395b10e65ea3f093e46`.

## Decision

Accept GPT's **scientific strategy**: continue Auer 2013 as a **paper-faithful piecewise-smooth validated-IVP method reconstruction using certified interval arithmetic**. This is a bounded development target, not acceptance of the currently incomplete baseline. Do not describe the result as a reproduction of the original ValEncIA binary unless that separate claim is demonstrated.

The next package is one analytic branch-crossing IVP plus one predeclared DDWMR query-action with native full-time inclusion and endpoint proof, followed by common-check composition and one archived R3 proof fixture. The 1,944-query Auer batch remains stopped.

## Evidence boundary

GPT independently read the committed scientific context and primary method/arithmetic sources. GPT explicitly **could not access the local uncommitted R2 implementation, 681-member snapshot or nine fixtures** from its GitHub environment. Therefore its strategy review is not an independent source-code audit. Codex's local R2 review separately checked 681/681 listed snapshot hashes, manifest ID/status preservation and the supplied-hull checker source. Neither review has accepted a proof-backed Auer DDWMR tube.

The analytic fixture proposed by GPT is internally consistent. For `x' = 1`, `y' = clip(x,-1,1)`, `x(0)∈[0.9,0.91]`, `y(0)=0`, `T=0.2`, each trajectory crosses `x=1` at `t_c=1-x_0∈[0.09,0.10]`. Its exact endpoint ranges are `x(T)∈[1.10,1.11]` and `y(T)∈[0.195,0.19595]`. These are reference containment targets, not a complete solver validation by themselves.

MPFR-style directed arithmetic is an acceptable **method-level** substitution only if the implemented interval elementary functions, range reduction, exceptional values, input conversion and output serialization have a documented outward contract. Finite probes remain diagnostics. The current PROFIL/BIAS/glibc build is not a certificate backend.

## Work authorization and stop condition

W1 already authorizes this scoped offline G2/G4 implementation. The user requested no commit or push while the team shares one laptop. The exact Luna task is `docs/CODEX_TO_LUNA_G4_AUER_R3_PROOF_BACKED_SINGLE_CASE.md`.

If no defensible arithmetic path or native inclusion can be established within the declared small-case work profile, return `BLOCKED` with the failed premises and artifacts. Such a result is a reconstruction limit, not evidence that R3 is superior or that G4 passes. A later matched batch requires independent source and soundness review of the completed small-case package. Because GPT could not inspect the uncommitted R2 files, that later review must receive actual source/proof artifacts rather than a status summary alone.

**Project status remains HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED.** No G3, controller, hardware or GO work follows.
