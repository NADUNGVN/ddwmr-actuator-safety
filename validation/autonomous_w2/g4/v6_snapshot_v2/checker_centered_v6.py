"""Independent checker for W2 G2 centered-matrix residual enclosure v6."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path
from typing import Any

from .rational_interval_v3 import Budget, I, activate, configure_fixed_grid, configure_integer_string_limit, qs, sqrt_lower

# G4's immutable copy is nested one directory deeper than G2's source.
ROOT=Path(__file__).resolve().parents[4]
LABEL_ORDER=["rho_L","rho_R","C_L","C_R","lambda_L","lambda_R","R_L","R_R","B_L","B_R","k_L","k_R"]
STATE_ORDER=["p_x","p_y","theta","u","r","omega_L","omega_R","i_L","i_R"]
STATE0=[F(0),F(0),F(0),F(3,10),F(0),F(1,4),F(1,4),F(0),F(0)]
CENTER_LABELS={name:F(1) for name in LABEL_ORDER}

class ReplayReject(RuntimeError):
    pass

def sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical_sha(value:Any)->str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()).hexdigest()

def parse_q(value:Any)->F:
    return F(str(value))

def qmaxabs(x:I)->F:
    return max(abs(x.lo),abs(x.hi))

def floor_grid(x:F,bits:int)->F:
    scale=1<<bits
    return F((x.numerator*scale)//x.denominator,scale)

def ceil_grid(x:F,bits:int)->F:
    scale=1<<bits
    return F(-((-x.numerator*scale)//x.denominator),scale)

def pair(x:I)->list[str]: return [qs(x.lo),qs(x.hi)]
def state_hash(xs:list[I])->str: return canonical_sha([[qs(x.lo),qs(x.hi)] for x in xs])

def _validate_protocol(protocol:dict[str,Any])->tuple[list[I],dict[str,I],list[dict[str,Any]],F]:
    model=protocol.get("model",{})
    if protocol.get("protocol_id")!="G2_W2_VOF_TASK_V1" or protocol.get("protocol_state")!="FROZEN_FOR_DEVELOPMENT_NOT_CONFIRMATION":
        raise ReplayReject("PROTOCOL_ID_OR_STATE")
    if model.get("formulation")!="MASTER v2.1 reduced nine-state DDWMR" or model.get("phi")!="clip(s,-1,1)" or model.get("lipschitz_constant")!="1":
        raise ReplayReject("SUPPORTED_MODEL_OR_CLIP_LAW")
    if model.get("fixed_label_order")!=LABEL_ORDER or model.get("fixed_label_bounds")!=["9999/10000","10001/10000"]:
        raise ReplayReject("FIXED_LABEL_ORDER_OR_BOUNDS")
    if model.get("parameter_maps")!={"J_j":"1/rho_j","L_j":"lambda_j"}:
        raise ReplayReject("PARAMETER_MAP")
    const=model.get("fixed_constants",{})
    expected={"m":"1","I_z":"1","R_w":"1","b":"1","v_s":"1","c_u":"1","c_r":"1","V_max":"1"}
    if const!=expected: raise ReplayReject("FIXED_CONSTANTS")
    lo,hi=map(F,model["fixed_label_bounds"])
    labels={name:I(lo,hi) for name in LABEL_ORDER}
    if any(cell.lo<=0 or cell.lo>=cell.hi for cell in labels.values()): raise ReplayReject("PARAMETER_IMAGE_POSITIVE_WIDTH")
    task=protocol.get("task",{})
    if task.get("initial_box_state_order")!=STATE_ORDER: raise ReplayReject("STATE_ORDER")
    raw=task.get("initial_box")
    if not isinstance(raw,list) or len(raw)!=9: raise ReplayReject("INITIAL_STATE_DIMENSION")
    state=[I(parse_q(item[0]),parse_q(item[1])) for item in raw]
    if any(cell.lo>=cell.hi for cell in state) or state[3].lo<=0: raise ReplayReject("INITIAL_STATE_DOMAIN")
    if any(not cell.lo<=ref<=cell.hi for cell,ref in zip(state,STATE0)): raise ReplayReject("REFERENCE_NOT_IN_INITIAL_BOX")
    hold=parse_q(task.get("hold_s"))
    if hold!=2 or parse_q(task.get("required_progress_m"))!=F(7,20): raise ReplayReject("HOLD_OR_TASK_THRESHOLD")
    obs=task.get("obstacle",{})
    if obs.get("kind")!="static_circle" or len(obs.get("center_m",[]))!=2 or parse_q(obs.get("inflated_radius_m"))<=0: raise ReplayReject("STATIC_CIRCLE")
    actions=protocol.get("actions",[])
    expected_actions=[
      {"id":"W2_G2_DEV_001_ZERO","role":"zero","voltage":["0","0"]},
      {"id":"W2_G2_DEV_001_NOMINAL","role":"nominal","voltage":["1/2","1/2"]},
      {"id":"W2_G2_DEV_001_ALTERNATIVE","role":"alternative","voltage":["1","1"]},
    ]
    if actions!=expected_actions: raise ReplayReject("ACTION_SET_OR_ORDER")
    return state,labels,actions,hold

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
        if profile.get(key)!=value: raise ReplayReject(f"FROZEN_PROFILE_FIELD:{key}")

def _assemble(labels:dict[str,I],voltage:tuple[F,F])->list[list[I]]:
    one=I.point(1); zero=I.point(0)
    rho_l,rho_r=labels["rho_L"],labels["rho_R"]
    c_l,c_r=labels["C_L"],labels["C_R"]
    lam_l,lam_r=labels["lambda_L"],labels["lambda_R"]
    r_l,r_r=labels["R_L"],labels["R_R"]
    b_l,b_r=labels["B_L"],labels["B_R"]
    k_l,k_r=labels["k_L"],labels["k_R"]
    a=[[zero for _ in range(7)] for _ in range(7)]
    a[0][0]=-one-c_l-c_r; a[0][1]=c_l-c_r; a[0][2]=c_l; a[0][3]=c_r
    a[1][0]=c_l-c_r; a[1][1]=-one-c_l-c_r; a[1][2]=-c_l; a[1][3]=c_r
    a[2][0]=rho_l*c_l; a[2][1]=-(rho_l*c_l); a[2][2]=-(rho_l*b_l)-(rho_l*c_l); a[2][4]=rho_l*k_l
    a[3][0]=rho_r*c_r; a[3][1]=rho_r*c_r; a[3][3]=-(rho_r*b_r)-(rho_r*c_r); a[3][5]=rho_r*k_r
    a[4][2]=-(k_l/lam_l); a[4][4]=-(r_l/lam_l); a[4][6]=I.point(voltage[0])/lam_l
    a[5][3]=-(k_r/lam_r); a[5][5]=-(r_r/lam_r); a[5][6]=I.point(voltage[1])/lam_r
    return a

def _center_matrix(v:F)->list[list[I]]:
    z=I.point(0); o=I.point(1)
    return [[-I.point(3),I.point(2),z,z,z],[o,-I.point(2),o,z,z],[z,-o,-o,z,I.point(v)],[o,z,z,z,z],[z,z,z,z,z]]

def _matvec(a:list[list[I]],x:list[I])->list[I]:
    out=[]
    for row in a:
        value=I.point(0)
        for coef,cell in zip(row,x): value=value+coef*cell
        out.append(value)
    return out

def _norm_vec(x:list[I])->F: return max(qmaxabs(v) for v in x)
def _norm_mat(a:list[list[I]])->F: return max(sum((qmaxabs(v) for v in row),F(0)) for row in a)

def _flow(a:list[list[I]],initial:list[I],h:F,degree:int,partial:bool)->tuple[list[I],dict[str,str]]:
    qnorm=_norm_mat(a)*h
    if qnorm<0 or qnorm/F(degree+2)>=1: raise ReplayReject("TAYLOR_TAIL_RATIO")
    tail=F(0) if qnorm==0 else (qnorm**(degree+1)/math.factorial(degree+1))/(1-qnorm/F(degree+2))
    radius=tail*_norm_vec(initial)
    total=[I.point(0) for _ in initial]
    current=initial
    hpow=F(1)
    for n in range(degree+1):
        time_cell=I(F(0),hpow) if partial and n>0 else I.point(hpow)
        denom=math.factorial(n)
        total=[acc+val*time_cell/denom for acc,val in zip(total,current)]
        current=_matvec(a,current)
        hpow*=h
    for i in range(len(total)-1): total[i]=total[i]+I(-radius,radius)
    return total,{"q_norm_upper":qs(qnorm),"tail_norm_upper":qs(tail),"remainder_inf_upper":qs(radius),"degree":str(degree),"time_mode":"partial_[0,h]" if partial else "endpoint_h"}

def _matrix_bounds(matrix:list[list[I]],center:list[list[I]])->tuple[F,F,F]:
    delta=F(0); mu_param=F(0); mu_aug=F(0)
    for i in range(6):
        dr=F(0); mr=matrix[i][i].hi; ar=center[i][i].hi
        for j in range(7):
            dr+=max(abs(matrix[i][j].lo-center[i][j].hi),abs(matrix[i][j].hi-center[i][j].lo))
            if j!=i:
                ar+=qmaxabs(center[i][j])
                if j<6: mr+=qmaxabs(matrix[i][j])
        delta=max(delta,dr); mu_param=max(mu_param,mr); mu_aug=max(mu_aug,ar)
    return delta,mu_param,max(F(0),mu_aug)

def _exp_upper(mu:F,t:F,degree:int,bits:int)->F:
    q=mu*t
    if q<0 or q/F(degree+2)>=1: raise ReplayReject("EXP_UPPER_TAIL_RATIO")
    qi=I.point(q); power=I.point(1); total=I.point(1)
    for n in range(1,degree+1):
        power=power*qi; total=total+power/math.factorial(n)
    tail=F(0) if q==0 else (q**(degree+1)/math.factorial(degree+1))/(1-q/F(degree+2))
    return ceil_grid(total.hi+tail,bits)

def _reconstruct(protocol:dict[str,Any],profile:dict[str,Any],action:dict[str,Any],protocol_sha:str,profile_sha:str,budget:Budget)->dict[str,Any]:
    _validate_profile(profile)
    state,labels,actions,hold=_validate_protocol(protocol)
    if action not in actions: raise ReplayReject("ACTION_NOT_IN_PROTOCOL")
    voltage=(parse_q(action["voltage"][0]),parse_q(action["voltage"][1]))
    if voltage[0]!=voltage[1]: raise ReplayReject("ASYMMETRIC_CENTER_ACTION")
    e0=F(0)
    for cell,ref in zip(state[3:9],STATE0[3:9]): e0=max(e0,abs(cell.lo-ref),abs(cell.hi-ref))
    slabs=int(profile.get("center_time_slabs",0)); h=hold/slabs if slabs else F(0)
    if slabs<=0 or h!=parse_q(profile.get("center_slab_duration_s")): raise ReplayReject("CENTER_TIME_PARTITION")
    degree=int(profile["matrix_taylor_degree"]); bits=int(profile["interval_fractional_bits"])
    matrix=_assemble(labels,voltage)
    center_labels={name:I.point(1) for name in LABEL_ORDER}
    matrix0=_assemble(center_labels,voltage)
    delta_a,mu_param,mu_aug=_matrix_bounds(matrix,matrix0)
    mu=max(F(0),mu_param,mu_aug)
    exp_hi=_exp_upper(mu,hold,degree,bits)
    radius=ceil_grid(exp_hi*(e0+hold*delta_a),bits)

    a0=_center_matrix(voltage[0])
    current=[I.point(F(3,10)),I.point(F(1,4)),I.point(0),I.point(0),I.point(1)]
    center_slabs=[]; px_lo=F(0); px_hi=F(0); beta_center=F(0); uc=F(0)
    center_label_sha=canonical_sha({"order":LABEL_ORDER,"values":{name:"1/1" for name in LABEL_ORDER}})
    for index in range(slabs):
        start=index*h; start_hash=state_hash(current)
        partial,pdiag=_flow(a0,current,h,degree,True)
        endpoint,ediag=_flow(a0,current,h,degree,False)
        slip=partial[1]-partial[0]; px=partial[3]; u=partial[0]
        beta_center=max(beta_center,qmaxabs(slip)); uc=max(uc,qmaxabs(u))
        px_lo=min(px_lo,px.lo); px_hi=max(px_hi,px.hi)
        center_slabs.append({"index":index,"start_s":qs(start),"end_s":qs(start+h),"center_label_sha256":center_label_sha,
          "start_interval_state_sha256":start_hash,"partial_u_mps":pair(u),"partial_wheel_rate_radps":pair(partial[1]),
          "partial_current_A":pair(partial[2]),"partial_p_x_m":pair(px),"partial_slip_LR":pair(slip),
          "partial_taylor":pdiag,"endpoint_taylor":ediag,"endpoint_interval_state_sha256":state_hash(endpoint)})
        current=endpoint
    center_j=current[3]
    if px_lo>0 or px_hi<0: raise ReplayReject("CENTER_PATH_OMITS_INITIAL_POINT")
    beta=ceil_grid(beta_center+3*radius,bits); clip_ok=beta<1
    theta0=max(abs(state[2].lo),abs(state[2].hi)); px0=max(abs(state[0].lo),abs(state[0].hi)); py0=max(abs(state[1].lo),abs(state[1].hi))
    theta_h=ceil_grid(theta0+hold*radius,bits)
    ej=ceil_grid(hold*radius+hold*uc*theta_h*theta_h/2,bits)
    epx=ceil_grid(px0+ej,bits); epy=ceil_grid(py0+hold*(uc+radius)*theta_h,bits)
    epos=ceil_grid(epx+epy,bits)
    obs=protocol["task"]["obstacle"]; ox,oy=map(parse_q,obs["center_m"]); obs_r=parse_q(obs["inflated_radius_m"])
    xgap=F(0) if px_lo<=ox<=px_hi else min(abs(ox-px_lo),abs(ox-px_hi))
    dcenter=floor_grid(sqrt_lower(xgap*xgap+oy*oy,int(profile["sqrt_bisections"])),bits)
    coll=floor_grid(dcenter-epos-obs_r,bits); collision_ok=coll>0
    cmin=min(labels["C_L"].lo,labels["C_R"].lo)
    reserve=floor_grid(cmin*(1-beta*beta),bits) if clip_ok else F(0)
    demand=ceil_grid((uc+radius)*radius,bits)
    contact=floor_grid(2*reserve-demand,bits); contact_ok=clip_ok and contact>=0
    progress_lo=floor_grid(center_j.lo-ej,bits); progress_hi=ceil_grid(center_j.hi+ej,bits)
    threshold=parse_q(protocol["task"]["required_progress_m"])
    safety="CERTIFIED" if clip_ok and collision_ok and contact_ok else "UNKNOWN"
    task=safety=="CERTIFIED" and progress_lo>=threshold
    reasons=[]
    if not clip_ok: reasons.append("CENTERED_TUBE_DOES_NOT_PROVE_CLIP_INTERIOR")
    if clip_ok and not contact_ok: reasons.append("CONTACT_MARGIN_NOT_NONNEGATIVE")
    if not collision_ok: reasons.append("COLLISION_MARGIN_NOT_POSITIVE")
    if safety=="CERTIFIED" and not task: reasons.append("ENDPOINT_PROGRESS_LOWER_BELOW_TASK_THRESHOLD")
    if not reasons: reasons=["ALL_WHOLE_HOLD_AND_TASK_PREDICATES_PROVED"]
    parameter_sha=canonical_sha({"order":LABEL_ORDER,"bounds":protocol["model"]["fixed_label_bounds"],"maps":protocol["model"]["parameter_maps"]})
    return {
      "schema":"G2_W2_CENTERED_RESIDUAL_ROW_v6","protocol_id":protocol["protocol_id"],"protocol_sha256":protocol_sha,
      "profile_id":profile["profile_id"],"profile_sha256":profile_sha,"action_id":action["id"],"action_role":action["role"],
      "held_voltage_V":[qs(v) for v in voltage],"parameter_label_order":LABEL_ORDER,"parameter_label_bounds":protocol["model"]["fixed_label_bounds"],
      "parameter_image_sha256":parameter_sha,"hold_s":qs(hold),"required_progress_m":qs(threshold),"initial_internal_reference_radius":qs(e0),
      "initial_pose_radii_m_rad":[qs(px0),qs(py0),qs(theta0)],"matrix_residual_norm_inf_upper":qs(delta_a),
      "internal_log_norm_upper":qs(mu_param),"center_augmented_log_norm_upper":qs(mu_aug),"common_log_norm_upper":qs(mu),
      "exp_growth_upper":qs(exp_hi),"internal_error_radius_full_hold":qs(radius),
      "center_time_coverage":{"slab_count":slabs,"covered_start_s":"0/1","covered_end_s":qs(hold),"contiguous":True,"fixed_center_label_sha256":center_label_sha},
      "center_u_abs_upper":qs(uc),"center_slip_abs_upper":qs(beta_center),"clip_beta_upper_full_domain":qs(beta),
      "clip_strict_interior_proved":clip_ok,"center_p_x_full_time_range_m":[qs(px_lo),qs(px_hi)],
      "center_progress_enclosure_m":pair(center_j),"theta_abs_upper_full_hold":qs(theta_h),"progress_error_radius_m":qs(ej),
      "progress_enclosure_m":[qs(progress_lo),qs(progress_hi)],"position_error_x_upper_m":qs(epx),"position_error_y_upper_m":qs(epy),
      "position_error_l1_upper_m":qs(epos),"center_distance_lower_m":qs(dcenter),"collision_margin_lower_m":qs(coll),"collision_certified":collision_ok,
      "contact_reserve_per_wheel_lower_N":qs(reserve),"contact_demand_upper_N":qs(demand),"contact_margin_lower_N":qs(contact),"contact_certified":contact_ok,
      "safety_status":safety,"task_eligible":task,"uniform_task_ineligible_by_upper":progress_hi<threshold,"reason_codes":reasons,"slabs":center_slabs,
    }

def audit(binding_path:Path,record_path:Path)->dict[str,Any]:
    binding=json.loads(binding_path.read_text(encoding="utf-8"))
    protocol_path=ROOT/binding["protocol_path"]; profile_path=ROOT/binding["profile_path"]
    protocol=json.loads(protocol_path.read_text(encoding="utf-8")); profile=json.loads(profile_path.read_text(encoding="utf-8"))
    _validate_profile(profile)
    configure_integer_string_limit(int(profile["python_int_string_digit_cap"]),int(profile["rational_bit_cap"]))
    configure_fixed_grid(int(profile["interval_fractional_bits"]),int(profile["rational_bit_cap"]),int(profile["matrix_taylor_degree"]))
    if sha(protocol_path)!=binding["protocol_sha256"] or sha(profile_path)!=binding["profile_sha256"]: raise ReplayReject("FROZEN_PROTOCOL_OR_PROFILE_HASH")
    for rel,expected in binding["source_files"].items():
        if sha(ROOT/rel)!=expected: raise ReplayReject(f"SOURCE_CLOSURE_HASH:{rel}")
    record=json.loads(record_path.read_text(encoding="utf-8"))
    if record.get("binding_sha256")!=sha(binding_path): raise ReplayReject("BINDING_HASH_MISMATCH")
    actions=[a for a in protocol.get("actions",[]) if a.get("id")==record.get("action_id")]
    if len(actions)!=1: raise ReplayReject("RECORDED_ACTION_NOT_IN_PROTOCOL")
    budget=Budget(int(profile["interval_operation_cap"]),int(profile["rational_bit_cap"]))
    activate(budget)
    try:
        expected=_reconstruct(protocol,profile,actions[0],binding["protocol_sha256"],binding["profile_sha256"],budget)
    finally: activate(None)
    if record.get("held_voltage_V")!=expected["held_voltage_V"] or record.get("parameter_label_order")!=LABEL_ORDER:
        raise ReplayReject("HELD_INPUT_SEMANTICS")
    keys=list(expected)
    mismatches=[key for key in keys if record.get(key)!=expected.get(key)]
    if mismatches: raise ReplayReject("RECOMPUTED_FIELDS_MISMATCH:"+",".join(mismatches))
    slabs=record.get("slabs")
    if not isinstance(slabs,list) or len(slabs)!=int(profile["center_time_slabs"]): raise ReplayReject("CENTER_SLAB_COUNT")
    prev=F(0); prev_hash=None; label_hash=None
    for i,slab in enumerate(slabs):
        start=parse_q(slab["start_s"]); end=parse_q(slab["end_s"])
        if start!=prev or end<=start or slab.get("index")!=i: raise ReplayReject("CENTER_SLAB_GAP_OVERLAP_OR_ORDER")
        if prev_hash is not None and slab.get("start_interval_state_sha256")!=prev_hash: raise ReplayReject("CENTER_ENDPOINT_CHAIN")
        if label_hash is None: label_hash=slab.get("center_label_sha256")
        if slab.get("center_label_sha256")!=label_hash: raise ReplayReject("CENTER_REFERENCE_LABEL_CHANGED")
        prev=end; prev_hash=slab.get("endpoint_interval_state_sha256")
    if prev!=parse_q(protocol["task"]["hold_s"]): raise ReplayReject("CENTER_COVERAGE_DOES_NOT_REACH_HOLD")
    return {"schema":"G2_W2_CENTERED_RESIDUAL_REPLAY_v6","replayed":True,"recomputed_safety_status":expected["safety_status"],
      "recomputed_task_eligible":expected["task_eligible"],"recomputed_progress_enclosure_m":expected["progress_enclosure_m"],
      "recomputed_collision_margin_lower_m":expected["collision_margin_lower_m"],"recomputed_contact_margin_lower_N":expected["contact_margin_lower_N"],
      "recomputed_clip_beta_upper":expected["clip_beta_upper_full_domain"],"proof_fields_recomputed":len(keys),"center_slabs_recomputed":len(slabs),
      "fixed_center_reference_chaining_recomputed":True,"held_voltage_constant_recomputed":True,
      "shared_trust":["Python fractions.Fraction","validation.autonomous_w2.g2.rational_interval_v3.I/Budget/outward 96-bit arithmetic"]}

def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument('--binding',required=True); parser.add_argument('--record',required=True); args=parser.parse_args()
    def rooted(v:str)->Path:
        p=Path(v); return p if p.is_absolute() else ROOT/p
    try:
        out=audit(rooted(args.binding),rooted(args.record)); print(json.dumps(out,sort_keys=True,indent=2)); return 0
    except BaseException as exc:
        print(json.dumps({"schema":"G2_W2_CENTERED_RESIDUAL_REPLAY_FAILURE_v1","replayed":False,"rejection":f"{type(exc).__name__}:{exc}"},sort_keys=True)); return 2

if __name__=='__main__': raise SystemExit(main())
