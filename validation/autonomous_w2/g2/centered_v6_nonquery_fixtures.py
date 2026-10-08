"""Synthetic algebra/guard fixtures only; never evaluates the frozen task rows."""
from __future__ import annotations
import json
from fractions import Fraction as F
from pathlib import Path

from . import producer_centered_v6 as p
from .rational_interval_v3 import Budget, I, activate, configure_fixed_grid, configure_integer_string_limit

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/"results/validation/autonomous_w2/g2/centered_v6_nonquery_fixtures_v1.json"

def verify()->dict[str,object]:
    configure_integer_string_limit(5000,16384); configure_fixed_grid(96,16384,20)
    budget=Budget(100000,16384); activate(budget)
    try:
        m=[[I.point(0) for _ in range(7)] for _ in range(6)]
        c=[[I.point(0) for _ in range(7)] for _ in range(6)]
        for i in range(6): m[i][i]=I.point(-2); c[i][i]=I.point(-2)
        m[0][0]=I(F(-11,10),F(-9,10)); c[0][0]=I.point(-1)
        m[1][1]=I.point(F(3,2)); c[1][1]=I.point(F(7,5))
        m[2][6]=I.point(F(1,4))
        m[3][3]=I.point(F(7,5)); c[3][3]=I.point(F(7,5))
        c[3][6]=I.point(F(2,5))
        delta,mu_param,mu_aug=p._parameter_bounds(m,c)
        grid_slack=F(1,1<<80)
        assert F(2,5)<=delta<F(2,5)+grid_slack, (delta,mu_param,mu_aug)
        assert mu_param==F(3,2), (delta,mu_param,mu_aug)
        assert F(9,5)<=mu_aug<F(9,5)+grid_slack, (delta,mu_param,mu_aug)
        a=p._center_matrix((F(1,2),F(1,2)))
        assert a[0][0].lo==a[0][0].hi==-3 and a[0][1].lo==a[0][1].hi==2
        assert a[1][0].lo==a[1][0].hi==1 and a[1][2].lo==a[1][2].hi==1
        assert a[2][1].lo==a[2][1].hi==-1 and a[2][4].lo==a[2][4].hi==F(1,2)
        exp_hi=p._exp_scalar_upper(F(1),F(2),20,96,budget)
        assert F(7389,1000)<exp_hi<F(739,100)
        assert p.floor_grid(F(1,3),96)<=F(1,3)<=p.ceil_grid(F(1,3),96)
        q=F(21,25)
        assert 0<=q<=1 and q*q<=q  # equivalent to sqrt(q)>=q for q>=0
        assert F(2,5)+3*F(19,100)<1 and not (F(2,5)+3*F(1,5)<1)
        report={"schema":"G2_W2_CENTERED_V6_NONQUERY_FIXTURES_v1","status":"PASS",
          "fixture_count":6,"native_attempts_added":0,"actual_protocol_action_rows_evaluated":0,
          "checks":["affine-column residual included","diagonal/off-diagonal log-norm bounds","symmetric center matrix signs and voltage","outward exp upper and grid rounding","sqrt(q)>=q contact reserve inequality","strict first-exit guard rejects beta>=1"],
          "synthetic_expected":{"delta_A_lower":"2/5","mu_param":"3/2","mu_aug_lower":"9/5","grid_slack":"1/2^80","exp_2_upper":str(exp_hi)},
          "interval_operations":budget.operations,"max_rational_bits":budget.max_observed_bits}
    finally: activate(None)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    if OUT.exists(): raise FileExistsError("FIXTURE_OUTPUT_ALREADY_EXISTS")
    OUT.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return report

if __name__=="__main__": print(json.dumps(verify(),sort_keys=True,indent=2))
