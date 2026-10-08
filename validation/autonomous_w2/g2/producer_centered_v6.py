"""Producer for W2 G2 centered-matrix residual enclosure v6."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path
from typing import Any

from .producer_v4 import build_augmented_matrix, canonical_sha256, exp_range, parse_protocol, sha256_file
from .rational_interval_v3 import Budget, I, activate, configure_fixed_grid, configure_integer_string_limit, qs, sqrt_lower

ROOT=Path(__file__).resolve().parents[3]
STATE0=[F(0),F(0),F(0),F(3,10),F(0),F(1,4),F(1,4),F(0),F(0)]
CENTER_LABELS={name:F(1) for name in ("rho_L","rho_R","C_L","C_R","lambda_L","lambda_R","R_L","R_R","B_L","B_R","k_L","k_R")}

class InvalidInput(RuntimeError):
    pass

def sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def qmaxabs(x:I)->F:
    return max(abs(x.lo),abs(x.hi))

def floor_grid(x:F,bits:int)->F:
    scale=1<<bits
    n=(x.numerator*scale)//x.denominator
    return F(n,scale)

def ceil_grid(x:F,bits:int)->F:
    scale=1<<bits
    n=-((-x.numerator*scale)//x.denominator)
    return F(n,scale)

def interval_pair(x:I)->list[str]:
    return [qs(x.lo),qs(x.hi)]

def interval_hash(xs:list[I])->str:
    return canonical_sha256([[qs(x.lo),qs(x.hi)] for x in xs])

def _parameter_bounds(matrix:list[list[I]],center:list[list[I]])->tuple[F,F,F]:
    delta=F(0); mu_param=F(0); mu_aug=F(0)
    for i in range(6):
        delta_row=F(0)
        mu_row=matrix[i][i].hi
        center_aug_row=center[i][i].hi
        for j in range(7):
            d=max(abs(matrix[i][j].lo-center[i][j].hi),abs(matrix[i][j].hi-center[i][j].lo))
            delta_row+=d
            if j!=i:
                center_aug_row+=qmaxabs(center[i][j])
                if j<6:
                    mu_row+=qmaxabs(matrix[i][j])
        delta=max(delta,delta_row)
        mu_param=max(mu_param,mu_row)
        mu_aug=max(mu_aug,center_aug_row)
    # The final affine coordinate has derivative zero and logarithmic norm 0.
    mu_aug=max(mu_aug,F(0))
    return delta,mu_param,mu_aug

def _center_matrix(voltage:tuple[F,F])->list[list[I]]:
    if voltage[0]!=voltage[1]:
        raise InvalidInput("CENTERED_REFERENCE_REQUIRES_SYMMETRIC_HELD_VOLTAGE")
    z=I.point(0); one=I.point(1); two=I.point(2); three=I.point(3)
    v=I.point(voltage[0])
    # State [u,w,i,p_x,1] on the exact all-one symmetric reference.
    return [
        [-three,two,z,z,z],
        [one,-two,one,z,z],
        [z,-one,-one,z,v],
        [one,z,z,z,z],
        [z,z,z,z,z],
    ]

def _exp_scalar_upper(mu:F,hold:F,degree:int,bits:int,budget:Budget)->F:
    q=mu*hold
    if q<0 or q/F(degree+2)>=1:
        raise InvalidInput("CENTER_EXP_TAIL_RATIO")
    qi=I.point(q); power=I.point(1); series=I.point(1)
    for k in range(1,degree+1):
        power=power*qi
        series=series+power/math.factorial(k)
    tail=F(0) if q==0 else (q**(degree+1)/math.factorial(degree+1))/(1-q/F(degree+2))
    upper=ceil_grid(series.hi+tail,bits)
    budget.tick(q,tail,upper)
    return upper

def _check_reference_in_box(state:list[I])->F:
    e0=F(0)
    for idx,ref in enumerate(STATE0):
        if not state[idx].lo<=ref<=state[idx].hi:
            raise InvalidInput("SYMMETRIC_REFERENCE_NOT_IN_INITIAL_BOX")
    for idx,ref in zip(range(3,9),STATE0[3:9]):
        e0=max(e0,abs(state[idx].lo-ref),abs(state[idx].hi-ref))
    return e0

def _compute(protocol:dict[str,Any],profile:dict[str,Any],action:dict[str,Any],protocol_sha:str,profile_sha:str,budget:Budget)->dict[str,Any]:
    state,labels,actions,hold=parse_protocol(protocol)
    _validate_profile(profile)
    if action not in actions:
        raise InvalidInput("ACTION_NOT_FROM_LOCKED_PROTOCOL")
    voltage=(F(action["voltage"][0]),F(action["voltage"][1]))
    if voltage[0]!=voltage[1]:
        raise InvalidInput("UNSUPPORTED_ASYMMETRIC_REFERENCE_ACTION")
    if any(not cell.lo<=CENTER_LABELS[name]<=cell.hi for name,cell in labels.items()):
        raise InvalidInput("CENTER_LABEL_NOT_IN_FIXED_PARAMETER_IMAGE")
    e0=_check_reference_in_box(state)
    if hold!=F(2) or int(profile["center_time_slabs"])<=0:
        raise InvalidInput("HOLD_OR_CENTER_PARTITION")
    slabs=int(profile["center_time_slabs"])
    h=hold/slabs
    if F(profile["center_slab_duration_s"])!=h:
        raise InvalidInput("CENTER_SLAB_DURATION_MISMATCH")
    degree=int(profile["matrix_taylor_degree"])
    bits=int(profile["interval_fractional_bits"])
    labels_center={name:I.point(value) for name,value in CENTER_LABELS.items()}
    matrix=build_augmented_matrix(labels,voltage)
    matrix_center=build_augmented_matrix(labels_center,voltage)
    delta_a,mu_param,mu_aug=_parameter_bounds(matrix,matrix_center)
    mu=max(F(0),mu_param,mu_aug)
    exp_hi=_exp_scalar_upper(mu,hold,degree,bits,budget)
    radius=ceil_grid(exp_hi*(e0+hold*delta_a),bits)
    budget.tick(delta_a,mu_param,mu_aug,mu,exp_hi,e0,radius)

    a_center=_center_matrix(voltage)
    current=[I.point(F(3,10)),I.point(F(1,4)),I.point(0),I.point(0),I.point(1)]
    center_slabs=[]
    px_lo=F(0); px_hi=F(0); beta_center=F(0); uc=F(0)
    # Hash the canonical rational spelling, not Fraction objects: json.dumps has
    # no Fraction encoder and the independently implemented checker hashes the
    # same mathematical point as reduced q strings.
    center_label_sha=canonical_sha256({"order":protocol["model"]["fixed_label_order"],"values":{name:qs(value) for name,value in CENTER_LABELS.items()}})
    for index in range(slabs):
        start=index*h
        start_hash=interval_hash(current)
        partial,pdiag=exp_range(a_center,current,h,degree,partial=True)
        endpoint,ediag=exp_range(a_center,current,h,degree,partial=False)
        u_cell=partial[0]; w_cell=partial[1]; p_cell=partial[3]
        slip=w_cell-u_cell
        beta_center=max(beta_center,qmaxabs(slip))
        uc=max(uc,qmaxabs(u_cell))
        px_lo=min(px_lo,p_cell.lo); px_hi=max(px_hi,p_cell.hi)
        center_slabs.append({
            "index":index,"start_s":qs(start),"end_s":qs(start+h),
            "center_label_sha256":center_label_sha,
            "start_interval_state_sha256":start_hash,
            "partial_u_mps":interval_pair(u_cell),"partial_wheel_rate_radps":interval_pair(w_cell),
            "partial_current_A":interval_pair(partial[2]),"partial_p_x_m":interval_pair(p_cell),
            "partial_slip_LR":interval_pair(slip),
            "partial_taylor":pdiag,"endpoint_taylor":ediag,
            "endpoint_interval_state_sha256":interval_hash(endpoint),
        })
        current=endpoint
    center_j=current[3]
    if px_lo>0 or px_hi<0:
        raise InvalidInput("CENTER_POSITION_TUBE_OMITS_INITIAL_POINT")

    beta=ceil_grid(beta_center+3*radius,bits)
    clip_ok=beta<1
    theta0=max(abs(state[2].lo),abs(state[2].hi))
    px0=max(abs(state[0].lo),abs(state[0].hi))
    py0=max(abs(state[1].lo),abs(state[1].hi))
    theta_h=ceil_grid(theta0+hold*radius,bits)
    progress_error=ceil_grid(hold*radius+hold*uc*theta_h*theta_h/2,bits)
    px_error=ceil_grid(px0+progress_error,bits)
    py_error=ceil_grid(py0+hold*(uc+radius)*theta_h,bits)
    position_l1=ceil_grid(px_error+py_error,bits)

    obstacle=protocol["task"]["obstacle"]
    ox,oy=(F(v) for v in obstacle["center_m"])
    obs_r=F(obstacle["inflated_radius_m"])
    if px_lo<=ox<=px_hi:
        xgap=F(0)
    else:
        xgap=min(abs(ox-px_lo),abs(ox-px_hi))
    center_d2=xgap*xgap+oy*oy
    center_d_lower=floor_grid(sqrt_lower(center_d2,int(profile["sqrt_bisections"])),bits)
    collision_margin=floor_grid(center_d_lower-position_l1-obs_r,bits)
    collision_ok=collision_margin>0

    cmin=min(labels["C_L"].lo,labels["C_R"].lo)
    reserve_each=floor_grid(cmin*(1-beta*beta),bits) if clip_ok else F(0)
    reserve_total=floor_grid(2*reserve_each,bits)
    demand=ceil_grid((uc+radius)*radius,bits)
    contact_margin=floor_grid(reserve_total-demand,bits)
    contact_ok=clip_ok and contact_margin>=0
    progress_lo=floor_grid(center_j.lo-progress_error,bits)
    progress_hi=ceil_grid(center_j.hi+progress_error,bits)
    threshold=F(protocol["task"]["required_progress_m"])
    safety="CERTIFIED" if clip_ok and contact_ok and collision_ok else "UNKNOWN"
    task_eligible=safety=="CERTIFIED" and progress_lo>=threshold
    reasons=[]
    if not clip_ok: reasons.append("CENTERED_TUBE_DOES_NOT_PROVE_CLIP_INTERIOR")
    if clip_ok and not contact_ok: reasons.append("CONTACT_MARGIN_NOT_NONNEGATIVE")
    if not collision_ok: reasons.append("COLLISION_MARGIN_NOT_POSITIVE")
    if safety=="CERTIFIED" and not task_eligible: reasons.append("ENDPOINT_PROGRESS_LOWER_BELOW_TASK_THRESHOLD")
    if not reasons: reasons=["ALL_WHOLE_HOLD_AND_TASK_PREDICATES_PROVED"]
    parameter_sha=canonical_sha256({"order":protocol["model"]["fixed_label_order"],"bounds":protocol["model"]["fixed_label_bounds"],"maps":protocol["model"]["parameter_maps"]})
    return {
      "schema":"G2_W2_CENTERED_RESIDUAL_ROW_v6","protocol_id":protocol["protocol_id"],"protocol_sha256":protocol_sha,
      "profile_id":profile["profile_id"],"profile_sha256":profile_sha,"action_id":action["id"],"action_role":action["role"],
      "held_voltage_V":[qs(v) for v in voltage],"parameter_label_order":protocol["model"]["fixed_label_order"],
      "parameter_label_bounds":protocol["model"]["fixed_label_bounds"],"parameter_image_sha256":parameter_sha,
      "hold_s":qs(hold),"required_progress_m":qs(threshold),"initial_internal_reference_radius":qs(e0),
      "initial_pose_radii_m_rad":[qs(px0),qs(py0),qs(theta0)],
      "matrix_residual_norm_inf_upper":qs(delta_a),"internal_log_norm_upper":qs(mu_param),
      "center_augmented_log_norm_upper":qs(mu_aug),"common_log_norm_upper":qs(mu),
      "exp_growth_upper":qs(exp_hi),"internal_error_radius_full_hold":qs(radius),
      "center_time_coverage":{"slab_count":slabs,"covered_start_s":"0/1","covered_end_s":qs(hold),"contiguous":True,"fixed_center_label_sha256":center_label_sha},
      "center_u_abs_upper":qs(uc),"center_slip_abs_upper":qs(beta_center),"clip_beta_upper_full_domain":qs(beta),
      "clip_strict_interior_proved":clip_ok,"center_p_x_full_time_range_m":[qs(px_lo),qs(px_hi)],
      "center_progress_enclosure_m":interval_pair(center_j),"theta_abs_upper_full_hold":qs(theta_h),
      "progress_error_radius_m":qs(progress_error),"progress_enclosure_m":[qs(progress_lo),qs(progress_hi)],
      "position_error_x_upper_m":qs(px_error),"position_error_y_upper_m":qs(py_error),
      "position_error_l1_upper_m":qs(position_l1),"center_distance_lower_m":qs(center_d_lower),
      "collision_margin_lower_m":qs(collision_margin),"collision_certified":collision_ok,
      "contact_reserve_per_wheel_lower_N":qs(reserve_each),"contact_demand_upper_N":qs(demand),
      "contact_margin_lower_N":qs(contact_margin),"contact_certified":contact_ok,
      "safety_status":safety,"task_eligible":task_eligible,"uniform_task_ineligible_by_upper":progress_hi<threshold,
      "reason_codes":reasons,"slabs":center_slabs,
    }

def _validate_profile(profile:dict[str,Any])->None:
    expected={
      "profile_id":"G2_W2_CENTERED_RESIDUAL_TUBE_V6_256_SLABS",
      "center_time_slabs":256,"center_slab_duration_s":"1/128",
      "matrix_taylor_degree":20,"interval_fractional_bits":96,
      "rational_bit_cap":16384,"python_int_string_digit_cap":5000,
      "sqrt_bisections":48,"interval_operation_cap":5000000,
      "worker_wall_cap_seconds":60,"worker_memory_cap_bytes":1073741824,
      "worker_process_cap":1,"stdout_cap_bytes":8388608,
      "stderr_cap_bytes":1048576,"phase_wall_cap_seconds":7200,
    }
    for key,value in expected.items():
        if profile.get(key)!=value:
            raise InvalidInput(f"FROZEN_PROFILE_FIELD_MISMATCH:{key}")

def evaluate_bound_row(binding:dict[str,Any],action_id:str)->dict[str,Any]:
    protocol_path=ROOT/binding["protocol_path"]; profile_path=ROOT/binding["profile_path"]
    protocol=json.loads(protocol_path.read_text(encoding="utf-8")); profile=json.loads(profile_path.read_text(encoding="utf-8"))
    _validate_profile(profile)
    configure_integer_string_limit(int(profile["python_int_string_digit_cap"]),int(profile["rational_bit_cap"]))
    configure_fixed_grid(int(profile["interval_fractional_bits"]),int(profile["rational_bit_cap"]),int(profile["matrix_taylor_degree"]))
    if sha256_file(protocol_path)!=binding["protocol_sha256"] or sha256_file(profile_path)!=binding["profile_sha256"]:
        raise InvalidInput("FROZEN_PROTOCOL_OR_PROFILE_HASH_MISMATCH")
    for rel,expected in binding["source_files"].items():
        if sha256_file(ROOT/rel)!=expected: raise InvalidInput(f"SOURCE_CLOSURE_HASH_MISMATCH:{rel}")
    action_matches=[a for a in protocol["actions"] if a["id"]==action_id]
    if len(action_matches)!=1: raise InvalidInput("ACTION_ID_NOT_UNIQUE")
    budget=Budget(int(profile["interval_operation_cap"]),int(profile["rational_bit_cap"]))
    activate(budget)
    try:
        record=_compute(protocol,profile,action_matches[0],binding["protocol_sha256"],binding["profile_sha256"],budget)
        record["binding_sha256"]=sha256_file(ROOT/binding["binding_path"])
        record["arithmetic"]={"interval_operations":budget.operations,"max_rational_bits":budget.max_observed_bits,"operation_cap":budget.max_operations,"bit_cap":budget.max_bits,"rounded_endpoint_count":budget.rounded_endpoint_count}
        return record
    finally:
        activate(None)

def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument('--binding',required=True); parser.add_argument('--action-id',required=True); args=parser.parse_args()
    binding_path=Path(args.binding); binding_path=binding_path if binding_path.is_absolute() else ROOT/binding_path
    try:
        binding=json.loads(binding_path.read_text(encoding='utf-8'))
        out=evaluate_bound_row(binding,args.action_id)
        print(json.dumps(out,sort_keys=True,ensure_ascii=True,separators=(',',':')))
        return 0
    except BaseException as exc:
        print(json.dumps({"schema":"G2_W2_WORKER_FAILURE_v1","status":"INVALID_OR_RESOURCE_UNKNOWN","reason_code":f"{type(exc).__name__}:{exc}"},sort_keys=True))
        return 2

if __name__=='__main__':
    raise SystemExit(main())
