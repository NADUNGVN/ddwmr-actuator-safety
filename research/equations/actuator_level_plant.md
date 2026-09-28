> HISTORICAL / SUPERSEDED BY MASTER v2 (2026-09-28). Read [MASTER_RESEARCH_CONTEXT_v2.md](../../research_context/MASTER_RESEARCH_CONTEXT_v2.md), DECISION_LOG, LITERATURE_MATRIX and REVIEW_GATE first. This note records earlier analysis, not the current nine-state plant or an implementation authorization. Seven-state results must not be transferred to the current plant without a new derivation.

# Candidate actuator-level DDWMR plant

**Status:** preliminary alternatives; no physical slip model is frozen.  
**Claim type:** equations below are standard motor/rigid-body constructions or conditional reductions, not evidence that a particular platform obeys them. Platform identification and contact closure remain outstanding.

## 1. Signals and full-state candidates

The user-facing physical command is terminal armature voltage

\[
u=V=[V_L,V_R]^\top,\qquad |V_i|\le V_{\max}.
\]

The proposed reduced electromechanical state is

\[
X_7=[x,y,\theta,\omega_L,\omega_R,i_L,i_R]^\top.
\]

Here \(\omega_i\) are wheel-side angular speeds, \(i_i\) motor currents, \((x,y)\) a stated body reference point (preferably center of mass), and \(\theta\) its yaw. A realistic contact-force formulation usually needs at least

\[
X_{10}=[x,y,\theta,v_x,v_y,\Omega,\omega_L,\omega_R,i_L,i_R]^\top,
\]

where \((v_x,v_y,\Omega)\) are body-frame translational and yaw velocities. The reduced seven-state model is not automatically equivalent to the ten-state contact model.

## 2. DC motor and transmission equations

For motor side \(i\in\{L,R\}\), let gear ratio \(N_i>0\) map wheel speed to rotor speed, efficiency be \(\eta_i\), and use SI-consistent torque/back-EMF constants \(K_{t,i},K_{e,i}\):

\[
L_i\dot i_i=V_i-R_i i_i-N_i K_{e,i}\omega_i,
\qquad
\tau_{w,i}=\eta_i N_iK_{t,i}i_i.
\]

The state \(\omega_i\) is wheel-side speed throughout this document. Motor inertia is reflected through \(N_i^2J_{m,i}\), while motor torque and back EMF use \(N_i\). Do not mix a motor-shaft state with wheel-side mechanical equations. Parameters may be fixed uncertain constants in compact intervals or time-varying signals with explicitly bounded rates; those are different robust-control models.

The voltage box is an ideal terminal-voltage abstraction. Symmetric \(\pm V_{\max}\) assumes bidirectional drive and braking authority over the claimed operating range. A one-quadrant driver, asymmetric bridge, battery sag, regenerative braking restriction, bus coupling, dead zone, or current/thermal clamp changes \(\mathcal U\) and the model. These are not silently represented by \(|V_i|\le V_{\max}\). Current limits are not added as a contribution in this phase; they must be identified as hardware constraints if relevant.

## 3. Candidate A: ideal constrained no-slip mechanics

For a symmetric robot with wheel separation \(B\), wheel radius \(r\), body mass \(m\), yaw inertia \(I_z\), wheel inertia \(J_w\), motor inertia \(J_m\), and gear ratio \(N\), the ideal no-lateral-slip rolling map is

\[
v=\frac r2(\omega_L+\omega_R),\qquad
\Omega=\frac rB(\omega_R-\omega_L),\qquad
\dot p=v e(\theta),\quad \dot\theta=\Omega,
\]

where \(e(\theta)=(\cos\theta,\sin\theta)^\top\). This expression assumes the body center of mass lies at the axle midpoint, symmetric wheel geometry, and ideal rolling constraints. It is a nonholonomic velocity-constraint reduction, not a holonomic reduction; an offset center of mass requires corresponding cross and gyroscopic terms. With motor inertia reflected to the wheel, the constant effective inertia matrix is

\[
M_{\rm eff}= (J_w+N^2J_m)I_2
+\frac{mr^2}{4}\begin{bmatrix}1&1\\1&1\end{bmatrix}
+\frac{I_zr^2}{B^2}\begin{bmatrix}1&-1\\-1&1\end{bmatrix}.
\]

It is positive definite for positive reflected wheel inertia and physical masses/inertias. A candidate reduced mechanical equation is

\[
M_{\rm eff}\dot\omega
=\operatorname{diag}(\eta_iN_iK_{t,i})i-D_w\omega-\tau_{\rm loss}(\omega)-d_\tau,
\qquad \omega=[\omega_L,\omega_R]^\top.
\]

The off-diagonal entries matter: chassis translation and yaw couple the left/right wheel accelerations. Replacing \(M_{\rm eff}\) by two independent wheel inertias is an approximation and must be identified and bounded. The loss/load terms need a stated law and bounds. This ideal no-slip model contains motor lag and voltage authority but has no wheel slip.

The seven-state system can then be written conditionally as

\[
\dot X_7=f(X_7,\delta)+g(X_7,\delta)V,
\]

with \(\dot p,\dot\theta\) from the rolling map, \(\dot\omega=F(\omega,i,\delta)\), and the electrical equation above. In this exact reduced ideal-rolling closure, uncertainty in \(M_{\rm eff},K_t,R,L\), or load must be carried consistently through \(F\) and the input vector field.

## 4. Candidate B: frozen-slip transmission map (phenomenological only)

One algebraic extension replaces the rolling gains by frozen factors \(\kappa_L=1-s_L\), \(\kappa_R=1-s_R\). The slip maps below are columns:

\[
a(s)=\frac r2[\kappa_L,\kappa_R]^\top,\qquad
b(s)=\frac rB[-\kappa_L,\kappa_R]^\top,
\]

\[
v=a(s)^\top\omega,\qquad \Omega=b(s)^\top\omega,\qquad
\dot p=ve(\theta),\qquad \dot\theta=\Omega.
\]

This can serve as a local, control-oriented transmission-uncertainty model if \(s_i\) are known constants (or if their derivative bounds are supplied). It must **not** be described as general tire slip/skid robustness. It forces body speed to zero when the wheel rates are zero, so it cannot represent a chassis continuing to slide during braking; a bounded multiplicative factor also becomes inadequate near wheel speed zero. Combining this map with an unrelated wheel-acceleration law is phenomenological until derived from contact mechanics. Its formulas are used only for the conditional relative-degree audit in the next document.

If \(s_i=s_i(t)\), then \(\dot v=\dot a^\top\omega+a^\top\dot\omega\). A bound on \(|s_i|\) gives no bound on \(\dot s_i\), much less higher derivatives. Classical differentiated HOCBFs and Taylor margins cannot silently treat arbitrary bounded slip as differentiable.

## 5. Candidate C: wheel-ground contact mechanics

To claim physical robustness to wheel slip and braking skid, a more defensible starting point includes body velocity and contact forces. In body coordinates, a planar rigid body with left/right contact points at lateral offsets \(\pm B/2\) may be written schematically as

\[
m(\dot v_x-\Omega v_y)=F_{x,L}+F_{x,R},
\]
\[
m(\dot v_y+\Omega v_x)=F_{y,L}+F_{y,R},
\]
\[
I_z\dot\Omega=\frac B2(F_{x,R}-F_{x,L})+\tau_{z,\rm other},
\]
\[
J_{w,i}^{\rm eq}\dot\omega_i=\eta_iN_iK_{t,i}i_i-r_iF_{x,i}-b_{w,i}\omega_i-\tau_{w,\rm loss,i},\qquad
J_{w,i}^{\rm eq}=J_{w,i}+N_i^2J_{m,i}.
\]

The pose satisfies \(\dot p=R(\theta)[v_x,v_y]^\top\), \(\dot\theta=\Omega\). A contact closure must define longitudinal slip velocity (for example \(r_i\omega_i-(v_x-\Omega y_i)\)), lateral slip, force generation, friction limits, normal-load range, and low-speed regularization. A tire law could be a verified bounded nonlinear force map; merely bounding an additive force disturbance is not the same as identifying wheel-slip physics.

With this explicit wheel-spin/current cascade, voltage may first enter the derivative of wheel force only after current responds. For ordinary algebraic tire forces depending on wheel/body slip, barrier relative degree may be four; that is only a generic expectation, not a result. Re-derive it for the chosen contact law, including force saturation/nonsmooth points and singularities. A torque/current-input reduction or \(L=0\) changes the order and requires an error/transient argument.

## 6. Uncertainty and information pattern (unresolved)

Keep separate:

1. **Static parameter uncertainty:** \(R,L,K_t,K_e,N,\eta,J_w,m,I_z,B,r\) in compact validated intervals.
2. **Wheel-slip/contact uncertainty:** either bounded slip states/signals with a regularity class, or uncertain contact parameters/forces obeying a physical contact law.
3. **External disturbance:** bounded load forces/torques, with the norm and time regularity stated.
4. **Measurement/estimation error:** bounds for pose, speed, current, and any slip/contact estimate, if the safety filter does not observe the true state.

For unobserved uncertainty, a robust command must be a **common voltage**:

\[
\exists V_k\in\mathcal U\quad\text{s.t.}\quad
\text{the condition holds for every admissible uncertainty realization}.
\]

The order is not \(\forall\delta\,\exists V(\delta)\), unless the controller actually observes \(\delta\) before choosing the voltage. If state estimates are set-valued, the controller uses one voltage over the state/parameter information set.

## 7. Model-choice questions that block freeze

- Is the target a no-slip electromechanical plant with bounded external/model disturbance, a narrow frozen transmission-loss model, or a wheel-ground tire-force model that includes skid?
- What is the robot reference point and geometry; are caster forces ignored, passive-wheel friction bounded, and wheel/motor inertias measured?
- Which voltage polarities and braking modes are available, and what terminal voltage actually reaches the motor under load?
- Which states are measured/estimated at each update? Are currents and wheel rates available, or must their uncertainty be propagated?
- Are slip/parameter uncertainties constant over a run, piecewise constant, Lipschitz, or merely measurable and bounded?
- Are voltage-channel coefficients known? Uncertain \(L\) changes the voltage input vector field; uncertain \(K_t\) changes the mechanical current coupling \(F\), and hence the voltage coefficient in the third barrier derivative.

Until these are answered and accepted by root/GPT reviewers, this document defines alternatives, not the implementation plant.
