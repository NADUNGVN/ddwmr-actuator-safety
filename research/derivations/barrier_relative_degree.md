> HISTORICAL / SUPERSEDED BY MASTER v2 (2026-09-28). Read [MASTER_RESEARCH_CONTEXT_v2.md](../../research_context/MASTER_RESEARCH_CONTEXT_v2.md), DECISION_LOG, LITERATURE_MATRIX and REVIEW_GATE first. This note records earlier analysis, not the current nine-state plant or an implementation authorization. Seven-state results must not be transferred to the current plant without a new derivation.

# Circular-obstacle barrier: exact local derivative audit

**Status:** algebra derived for the conditional seven-state, frozen-slip model only. It is not yet the relative degree of a physically validated slip/contact plant.  
**Obstacle model:** one static circular keep-out set; robot footprint is absorbed into radius \(R_s\).

## 1. Conditional model and notation

Use the model from [the plant specification](../equations/actuator_level_plant.md), with frozen known slip parameters during a derivative calculation:

\[
q=p-p_o,\quad e=(\cos\theta,\sin\theta)^\top,\quad
e_\perp=(-\sin\theta,\cos\theta)^\top,
\]
\[
v=a^\top\omega,\quad \Omega=b^\top\omega,
\quad \dot p=ve,\quad \dot\theta=\Omega,
\]
\[
\dot\omega=F(\omega,i,\delta),\qquad
\dot i=L^{-1}\big(V-Ri-K_eN\omega\big).
\]

Here \(a,b\in\mathbb R^2\) are fixed wheel-to-body transmission columns for this calculation; \(L,R,K_e,N\) are diagonal or consistently dimensioned matrices. \(F\) is assumed \(C^1\) in \((\omega,i)\) and independent of voltage directly. The input is the terminal voltage \(V\in[-V_{\max},V_{\max}]^2\). Define

\[
h=q^\top q-R_s^2,\qquad \rho=q^\top e,\qquad \eta=q^\top e_\perp.
\]

## 2. Derivatives

Since \(\dot e=\Omega e_\perp\) and \(\dot e_\perp=-\Omega e\),

\[
\dot\rho=v+\eta\Omega,\qquad \dot\eta=-\rho\Omega.
\]

The position barrier derivatives are

\[
\boxed{\dot h=2\rho v},
\]
\[
\boxed{\ddot h=2v^2+2\eta\Omega v+2\rho\dot v},
\]
\[
\boxed{h^{(3)}=6v\dot v-2\rho\Omega^2v
+2\eta\dot\Omega v+4\eta\Omega\dot v+2\rho\ddot v}.
\]

For fixed \(a,b\),

\[
\dot v=a^\top F,\qquad \dot\Omega=b^\top F,
\]
\[
\ddot v=a^\top\left[F_\omega F+
F_iL^{-1}(V-Ri-K_eN\omega)\right],
\]

where \(F_\omega=\partial F/\partial\omega\) and \(F_i=\partial F/\partial i\). Thus the terms through \(\ddot h\) contain no voltage, while

\[
\boxed{\frac{\partial h^{(3)}}{\partial V}
=2\rho\,a^\top F_iL^{-1}.}
\]

If \(F=M_{\rm eff}^{-1}(K_m i-D\omega-\tau_{\rm loss})\) with constant motor gain \(K_m=\operatorname{diag}(\eta_iN_iK_{t,i})\), this row becomes

\[
2\rho\,a^\top M_{\rm eff}^{-1}K_mL^{-1}.
\]

This coefficient depends on obstacle geometry, frozen slip map, coupled mechanical inertia, motor torque constants, and winding inductances. A mistaken independent-wheel inertia model changes the input row and therefore the safety-filter constraint.

## 3. Relative-degree conclusion and singularities

For the smooth frozen-slip system, \(L_g h=0\) and \(L_gL_fh=0\). Voltage first appears in the third derivative on the regular domain

\[
\mathcal D_3=\{X:\rho\,a^\top F_iL^{-1}\ne0\}.
\]

The relative degree is **three on this domain**. It is not globally or uniformly three on the full collision-free state space. In particular, \(\rho=0\) (the robot heading is tangent to the obstacle-centered circle) makes the input row zero. Other parameter/geometry combinations may also make \(a^\top F_iL^{-1}=0\). For scalar \(h\) and two voltages, the coefficient is a 1-by-2 row: its rank is one where nonzero and zero where it vanishes.

The condition for a relative degree of four is not that one more pointwise derivative happens to contain voltage at a singular state. Relative degree is defined by Lie-derivative identities on a neighborhood with the required coefficient nonzero; at a zero of the third-order coefficient the degree may vary, and a regular degree-four neighborhood has not been established. A theorem using degree three must either restrict to an explicitly defined regular domain and prove trajectories do not leave it, or use a method valid across the degree-changing set.

The loss of coefficient at \(\rho=0\) is geometric, not unique to adding motor dynamics. A kinematic velocity-input barrier can have the same radial projection degeneracy. “We derived relative degree three” alone is not a novelty contribution.

## 4. What changes under time-varying slip

If the selected transmission map is \(a=a(s(t)),b=b(s(t))\), then

\[
\dot v=\dot a^\top\omega+a^\top F,\qquad
\dot\Omega=\dot b^\top\omega+b^\top F,
\]

and the next derivatives include \(\ddot a,\ddot b\). A bound on slip amplitude \(|s_i|\le\bar s\) supplies none of these derivative bounds. Randomly resampling bounded slip at each numerical integration step creates an implementation-specific jump process; it is not automatically a differentiable uncertainty model, and smooth HOCBF recursion cannot be applied across jumps without jump conditions.

Possible mathematical choices are distinct and require review:

1. Frozen uncertain \(s\) per hold or per run, with one common voltage for every admissible value.
2. Time-varying differentiable \(s(t)\) with stated bounds on the rates needed by each derivative and margin.
3. Measurable bounded disturbances/contact forces, treated by a differential inclusion or reachable-tube argument that does not differentiate them.

Do not claim all three with one symbol \(\bar s\).

## 5. HOCBF hierarchy and robust quantifiers

On a regular degree-three domain, for differentiable extended class-\(\mathcal K\) functions \(\alpha_j\), a candidate recursion is

\[
\psi_0=h,\qquad
\psi_1=\dot\psi_0+\alpha_1(\psi_0),\qquad
\psi_2=\dot\psi_1+\alpha_2(\psi_1),\qquad
\psi_3=\dot\psi_2+\alpha_3(\psi_2).
\]

\(\psi_3\) is affine in voltage where the regularity and relative-degree assumptions hold. The usual HOCBF implication requires the initial lower-order intersection \(\psi_0\ge0,\psi_1\ge0,\psi_2\ge0\), plus continued satisfaction of \(\psi_3\ge0\), and the relevant solution/regularity hypotheses. It does not assert invariance of every state in \(\{h\ge0\}\).

For unobserved uncertainty \(\delta\), a robust constraint must use a common voltage:

\[
\exists V\in\mathcal U\;\;\forall\delta\in\Delta:\quad
\psi_3(X,\delta,V)\ge0,
\]

and robust initial hierarchy membership must be specified as well if the theorem quantifies over all possible \(\delta\). Choosing a separate \(V(\delta)\) for each hidden realization gives the controller unavailable information. If \(L\) or \(K_t\) is uncertain, the voltage coefficient itself is uncertain; an endpoint or vertex reduction is justified only after the dependence and uncertainty set are proved to support it.

## 6. The sampled-hold problem is a separate derivation

The continuous-time HOCBF input condition checked at a single sample is not, by itself, a condition on the whole hold interval. With \(V(t)=V_k\) on \([t_k,t_k+T_s)\), a valid inter-sample result needs a bound or enclosure that covers every admissible trajectory during that hold.

One generic conditional route is a Taylor lower bound. If, for a reachable tube under \(V_k\), every admissible trajectory has \(h^{(3)}(t)\ge m_3(X_k,V_k)\) for the full interval, then

\[
h(t_k+\tau)\ge h_k+\dot h_k\tau+
\frac12\ddot h_k\tau^2+\frac16m_3\tau^3,
\qquad 0\le\tau\le T_s.
\]

Requiring the right-hand side to be nonnegative for every \(\tau\in[0,T_s]\) is sufficient for this one-hold safety claim. The hard part is a sound, state/input/uncertainty-dependent \(m_3\) over the reachable tube. Computing only \(h^{(3)}(X_k,V_k)\) is not that bound. Differentiating the third derivative to produce a Lipschitz margin requires still more smoothness (and, with varying slip, further slip derivatives); reachable-set enclosures may avoid that derivative assumption but are a different method.

Even when one hold maps every endpoint to a sampled certified set \(S\), this proves all-time collision safety over that hold and sample invariance of \(S\). It does not prove continuous-time invariance of \(S\) unless the tube stays in \(S\) or the model is augmented with hold-clock/input state and an invariant set is defined there.

## 7. Equation verification status

The algebra in Sections 2–3 is directly derived from the stated conditional model. It is not externally established as the final robot's relative degree. The TDTU MIMO electromechanical model and the closest generic sampled-data HOCBF papers are screened in the [literature matrix](../literature_matrix/closest_works.csv); full equation-level comparison for Lin et al. (2025), Xiong et al. (2025), and Bitar & Maalouf (2026) remains blocked by full-text access/evidence limitations recorded there.
