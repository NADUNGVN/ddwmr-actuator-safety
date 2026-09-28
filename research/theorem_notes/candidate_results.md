> HISTORICAL / SUPERSEDED BY MASTER v2 (2026-09-28). Read [MASTER_RESEARCH_CONTEXT_v2.md](../../research_context/MASTER_RESEARCH_CONTEXT_v2.md), DECISION_LOG, LITERATURE_MATRIX and REVIEW_GATE first. This note records earlier analysis, not the current nine-state plant or an implementation authorization. Seven-state results must not be transferred to the current plant without a new derivation.

# Candidate theorem architecture and feasibility audit

Status: root's preliminary research architecture, written after Luna stopped at its usage limit. No theorem of novelty or chosen physical plant is frozen. Use the plant alternatives and independent review together with this document.

## Objects and assumptions

Let `C={X:h(X)>=0}` for a static obstacle with inflated radius. Let `U=[-Vmax,Vmax]^2`, `T>0`, and `D` be an operating domain. A candidate plant is `Xdot=f(X,delta)+g(X,delta)V`, where the uncertainty class specifies fixed parameters and/or measurable time-varying disturbances. The same held voltage must work for all admissible trajectories. Assume existence of absolutely continuous solutions, appropriate local state regularity, and no finite escape over certified holds. Such assumptions require checking against the chosen contact law; they do not follow from compact disturbance bounds alone.

For exact observed `X`, denote the reachable set at time `tau` under constant `V` by `R(tau;X,V)`. With uncertain state observation, replace `X` by the controller's initial information set and use one action for the whole set. Fixed uncertain parameters must remain fixed along each trajectory, not be silently resampled; allowing arbitrary switching is a conservative enlargement that must be disclosed.

## Lemma A0: all of C cannot generally be made invariant

For continuous body velocity, if `h(X0)=0` and `hdot(X0)<0` independently of voltage, every sufficiently short continuation leaves C. This applies to the conditional seven-state model at `rho*v<0`. Proof: differentiability gives `h(t)=t*hdot(0)+o(t)<0`. Thus an actuator-level safety result requires a stricter initial set. This is a counterexample to an overbroad formulation, not a novel DDWMR theorem.

## Lemma A1: conditional HOCBF implication

For a fixed smooth plant on a regular degree-three domain, define `psi0=h`, `psi1=hdot+alpha1(h)`, `psi2=psi1dot+alpha2(psi1)`. If the initial lower-order values are nonnegative, solutions stay in the domain, and `psi2dot+alpha3(psi2)>=0` holds almost everywhere with sufficient regularity for comparison, then `h(t)>=0` follows while those hypotheses hold. For uncertain/time-varying models all total derivatives and robust initial conditions must be correct for each admissible realization.

This is a standard conditional implication. It neither constructs a feasible input nor proves that a sampled QP satisfies the inequality during the hold. A proof cannot assume the very persistent feasibility it seeks to establish.

## Lemma B1: one-hold tube certificate

Suppose a computable outer enclosure `Rhat(tau;X,V)` contains every admissible trajectory for every `tau in [0,T]` and stays within the domain where its bounds are valid. If `Rhat([0,T];X,V) subset C`, then the held voltage is collision-safe for that interval.

For a position ball `||p(t)-phat(t)||<=epsilon_p(t)`, it is sufficient that

`||phat(t)-p_o||-R_s-epsilon_p(t)>=0` for every `t in [0,T]`.

The triangle inequality proves this implication. The missing research result is a tractable, physically justified, uniform enclosure and a certified continuous minimization bound. Sampling the inequality on a finite grid without a between-grid bound is insufficient. This tube logic already has extensive prior art and is not itself a novelty claim.

## Theorem B2: recursive sampled-state certification (conditional)

Let `K` be a nonempty subset of `C`. Suppose for every `X in K` the controller can select a common `V in U` such that

`Rhat([0,T];X,V) subset C` and `Rhat(T;X,V) subset K`.

Starting in K and selecting such an input at each update gives `X(kT) in K` for all k and `h(X(t))>=0` for all continuous t, provided concatenation of solutions remains well posed. Proof is induction over safe holds and endpoint return. With partial observations, the corresponding information-set update/return property is required.

This establishes sample-invariance of K and all-time safety in C. It does not establish continuous invariance of K. A continuously invariant description may require augmenting state with the held voltage and elapsed hold clock. The substantive open problem is to construct a useful K and prove this property, not merely state it.

## Proposition C1: one affine certificate under a voltage box

For known coefficients `c,a` independent of Vmax, the inequality `c+a^T V>=0` has a solution in U exactly when `c+Vmax||a||_1>=0`. Proof: maximize the linear form componentwise. If `a=0`, feasibility is `c>=0`. If `a!=0`, the minimum nonnegative box half-width is `max(0,-c/||a||_1)`.

This is instantaneous certificate feasibility. For multiple obstacles or uncertain coefficients use one common action satisfying every inequality. Separate support maxima are not sufficient. Example: `V_L>=1` and `V_L<=-1` are individually feasible in a sufficiently large box and jointly impossible. If margins depend on voltage authority, the apparent Vreq formula becomes implicit. Nonlinear hold constraints need not yield a QP.

## Candidate C2: structured authority result

Investigate [the straight-motion motor response probe](../../docs/reviews/PHYSICAL_AUTHORITY_PROBE.md). In its explicitly restricted symmetric mode, exact constant-voltage matrix-exponential evolution yields forward excursion D(t). Certifying `sup_[0,T] D(t)<=d0` proves one-hold safety for that maneuver. An all-time excursion bound for an admissible backup can define a sufficient backup region under the same assumptions.

Open obligations: mechanically justified effective inertia; known or uniformly bounded motor/load parameters; invariant symmetry; admissible braking; robust uncertainty enclosure; endpoint continuation; and comparison with turning. Failure of this sufficient braking test is not physical impossibility of collision avoidance. Full planar exact viability is not promised.

## Sampling and authority statements that can be justified

- Increasing Vmax enlarges the exact available-action set, so existential one-hold feasibility cannot shrink when all other assumptions are unchanged.
- Enlarging the admitted uncertainty class cannot enlarge the exact robust safe-action set.
- A shorter prefix of a safe held action remains safe. Endpoint-return requirements for a fixed K need not be monotone under arbitrary changes of T.
- Simple global monotonicity in speed or obstacle distance is not asserted for arbitrary heading/current/turning states. Derive such relations only for a stated reduced setting.

## Proof obligations before acceptance

Select the physical model and uncertainty class; close reachable-domain bounds without assuming safety; address all admitted singular states; construct a nontrivial K or backup set; identify controller observations; prove the actual optimization is feasible on that set; compare the constructed result against closest full-text prior art. Until then these are candidate statements and elementary implications, not completed deliverables of a publishable theorem package.
