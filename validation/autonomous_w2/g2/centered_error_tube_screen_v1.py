from __future__ import annotations
import json
from fractions import Fraction as F
from math import factorial
from pathlib import Path

from validation.autonomous_w2.g2.analytic_task_screen import screen as point_progress
from validation.autonomous_w2.g2.clip_branch_point_witness_v1 import H, N, taylor as point_taylor
from validation.autonomous_w2.g2.producer_v4 import LABEL_ORDER, build_augmented_matrix
from validation.autonomous_w2.g2.rational_interval_v3 import I, configure_fixed_grid

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/validation/autonomous_w2/g2/centered_error_tube_preflight_v2.json'
if OUT.exists():
    raise FileExistsError('PREFLIGHT_OUTPUT_ALREADY_EXISTS')
configure_fixed_grid(96, 16384, 20)
T = F(2)
LABEL_LO, LABEL_HI = F(9999,10000), F(10001,10000)
C_LO = LABEL_LO
Z0_RADIUS = F(1,10000)
POSE0_RADIUS = F(1,100000)
THETA0_RADIUS = F(1,100000)
OB_X, OB_Y, OB_R = F(1,2), F(1,10), F(3,50)
THRESHOLD = F(7,20)

def exp_upper(q: F, degree: int = 40) -> F:
    if q < 0 or q/(degree+2) >= 1:
        raise ValueError('EXP_UPPER_DOMAIN')
    total = sum((q**k/F(factorial(k)) for k in range(degree+1)), F(0))
    if q == 0:
        return total
    tail = q**(degree+1)/F(factorial(degree+1))/(1-q/F(degree+2))
    return total + tail

def sqrt_lower(x: F, bits: int = 64) -> F:
    if x < 0:
        raise ValueError('SQRT_NEGATIVE')
    lo, hi = F(0), max(F(1), x)
    for _ in range(bits):
        mid=(lo+hi)/2
        if mid*mid <= x: lo=mid
        else: hi=mid
    return lo

def qmax_abs(interval: I) -> F:
    return max(abs(interval.lo),abs(interval.hi))

def center_trajectory(voltage: F) -> dict[str, F | bool]:
    a = [
      [F(-3),F(2),F(0),F(0)],
      [F(1),F(-2),F(1),F(0)],
      [F(0),F(-1),F(-1),voltage],
      [F(0),F(0),F(0),F(0)],
    ]
    state=[(F(3,10),F(3,10)),(F(1,4),F(1,4)),(F(0),F(0)),(F(1),F(1))]
    pose_a=[[F(-3),F(2),F(0),F(0),F(0)],[F(1),F(-2),F(1),F(0),F(0)],[F(0),F(-1),F(-1),F(0),voltage],[F(1),F(0),F(0),F(0),F(0)],[F(0),F(0),F(0),F(0),F(0)]]
    pose_state=[(F(3,10),F(3,10)),(F(1,4),F(1,4)),(F(0),F(0)),(F(0),F(0)),(F(1),F(1))]
    umax=F(0); umin=None; betamax=F(0); pxmin=None; pxmax=None
    for _ in range(16):
        partial,_=point_taylor(a,state,partial=True)
        endpoint,_=point_taylor(a,state,partial=False)
        ulo,uhi=partial[0]
        umax=max(umax,abs(ulo),abs(uhi))
        umin=ulo if umin is None else min(umin,ulo)
        slip=(partial[1][0]-partial[0][1],partial[1][1]-partial[0][0])
        betamax=max(betamax,abs(slip[0]),abs(slip[1]))
        pose_partial,_=point_taylor(pose_a,pose_state,partial=True)
        pose_endpoint,_=point_taylor(pose_a,pose_state,partial=False)
        xlo,xhi=pose_partial[3]
        pxmin=xlo if pxmin is None else min(pxmin,xlo)
        pxmax=xhi if pxmax is None else max(pxmax,xhi)
        state=endpoint
        pose_state=pose_endpoint
    total,tail=point_progress(voltage)
    return {'u_abs_upper':umax,'u_lower':umin,'slip_abs_upper':betamax,'progress_center_lower':total-tail,'progress_center_upper':total+tail,'center_p_x_lower':pxmin,'center_p_x_upper':pxmax}

def matrix_screen(voltage: F) -> tuple[F,F,F,F]:
    labels={name:I(LABEL_LO,LABEL_HI) for name in LABEL_ORDER}
    center_labels={name:I.point(1) for name in LABEL_ORDER}
    v=(voltage,voltage)
    matrix=build_augmented_matrix(labels,v)
    center=build_augmented_matrix(center_labels,v)
    delta_norm=F(0); mu_interval=F(0); mu_center_aug=F(0)
    for i in range(6):
        delta_row=F(0); mu_row=matrix[i][i].hi
        center_row=center[i][i].lo
        mu_aug_row=center[i][i].lo
        for j in range(7):
            c=center[i][j].lo
            d=max(abs(matrix[i][j].lo-c),abs(matrix[i][j].hi-c))
            delta_row+=d
            if j != i:
                if j < 6: mu_row+=qmax_abs(matrix[i][j])
                mu_aug_row+=abs(c)
        delta_norm=max(delta_norm,delta_row)
        mu_interval=max(mu_interval,mu_row)
        mu_center_aug=max(mu_center_aug,mu_aug_row)
    return delta_norm,mu_interval,mu_center_aug,F(0)

rows={}
for role, voltage in (('ZERO',F(0)),('NOMINAL',F(1,2)),('ALTERNATIVE',F(1))):
    center=center_trajectory(voltage)
    delta_a,mu_param,mu_aug,_=matrix_screen(voltage)
    mu=max(F(0),mu_param,mu_aug)
    growth=exp_upper(mu*T)
    radius=growth*(Z0_RADIUS+T*delta_a)
    beta=center['slip_abs_upper']+3*radius
    theta=THETA0_RADIUS+T*radius
    uc=center['u_abs_upper']
    progress_error=T*radius+T*uc*theta*theta/2
    progress_lo=center['progress_center_lower']-progress_error
    progress_hi=center['progress_center_upper']+progress_error
    px_error=POSE0_RADIUS+progress_error
    py_error=POSE0_RADIUS+T*(uc+radius)*theta
    position_error=px_error+py_error
    if center['center_p_x_lower'] <= OB_X <= center['center_p_x_upper']:
        gap_x=F(0)
    else:
        gap_x=min(abs(OB_X-center['center_p_x_lower']),abs(OB_X-center['center_p_x_upper']))
    distance2=gap_x*gap_x+OB_Y*OB_Y
    distance_lower=sqrt_lower(distance2)
    collision_margin=distance_lower-position_error-OB_R
    contact_reserve=2*C_LO*(1-beta*beta) if beta<1 else F(-1)
    contact_demand=(uc+radius)*radius
    contact_margin=contact_reserve-contact_demand
    rows[role]={
      'voltage':str(voltage),
      'matrix_residual_norm_inf_exact':str(delta_a),
      'matrix_residual_norm_inf_decimal':float(delta_a),
      'parameter_log_norm_upper_exact':str(mu_param),
      'center_augmented_log_norm_exact':str(mu_aug),
      'common_growth_log_norm_exact':str(mu),
      'exp_growth_upper_at_hold_exact':str(growth),
      'internal_state_error_radius_full_hold_exact':str(radius),
      'internal_state_error_radius_full_hold_decimal':float(radius),
      'center_u_abs_upper_exact':str(uc),
      'center_u_lower_exact':str(center['u_lower']),
      'center_p_x_tube_exact_m':[str(center['center_p_x_lower']),str(center['center_p_x_upper'])],
      'center_slip_abs_upper_exact':str(center['slip_abs_upper']),
      'center_slip_abs_upper_decimal':float(center['slip_abs_upper']),
      'clip_beta_upper_exact':str(beta),
      'clip_strict_interior_proved':beta<1,
      'theta_abs_upper_exact':str(theta),
      'center_progress_exact_interval_m':[str(center['progress_center_lower']),str(center['progress_center_upper'])],
      'task_progress_error_radius_exact_m':str(progress_error),
      'full_domain_progress_enclosure_exact_m':[str(progress_lo),str(progress_hi)],
      'full_domain_progress_enclosure_decimal_m':[float(progress_lo),float(progress_hi)],
      'collision_center_distance_lower_exact_m':str(distance_lower),
      'position_error_l1_upper_exact_m':str(position_error),
      'collision_margin_lower_exact_m':str(collision_margin),
      'collision_proved':collision_margin>0,
      'contact_reserve_lower_exact_N':str(contact_reserve),
      'contact_demand_upper_exact_N':str(contact_demand),
      'contact_margin_lower_exact_N':str(contact_margin),
      'contact_proved':contact_margin>0,
      'progress_eligible':progress_lo>=THRESHOLD,
      'uniform_task_ineligible_by_upper':progress_hi<THRESHOLD,
    }

all_ok=all(r['clip_strict_interior_proved'] and r['collision_proved'] and r['contact_proved'] for r in rows.values())
summary={
 'schema':'G2_W2_CENTERED_VARIATION_OF_CONSTANTS_PREFLIGHT_v1',
 'session':'DDWMR | LUNA-G2-SCOPE',
 'classification':'nonquery exact/outward feasibility screen of a proposed centered-matrix residual theorem; not a certificate or native attempt',
 'assumptions':{'phi':'clip(s,-1,1)','fixed_labels':['9999/10000','10001/10000'],'one_fixed_voltage_per_hold':True,'T_s':'2','initial_internal_error_radius':'1/10000','initial_pose_and_heading_radius':'1/100000'},
 'theorem_screen':'For each fixed parameter image A_theta=A_0+Delta, ||Delta||_inf<=deltaA. With mu bounding the internal logarithmic norm of every A_theta and the augmented center logarithmic norm of A_0, D^+||z_theta-z_0||_inf<=mu||z_theta-z_0||_inf+deltaA||y_0||_inf. Since ||y_0(0)||_inf=1 and mu>=0, ||y_theta(t)-z_0(t)||_inf<=exp(mu*t)*(e0+t*deltaA) for 0<=t<=T.',
 'all_actions_center_safe_clip_contact':all_ok,
 'prospective_task_rule_possible':rows['ALTERNATIVE']['progress_eligible'] and rows['ZERO']['uniform_task_ineligible_by_upper'] and rows['NOMINAL']['uniform_task_ineligible_by_upper'],
 'rows':rows,
 'native_attempts_added':0,
}
OUT.write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,sort_keys=True,indent=2))


