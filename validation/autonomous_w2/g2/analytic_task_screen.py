"""Exact-rational point feasibility screen; not a box query or certificate."""
from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction as F
from math import factorial


def mv(a: list[list[F]], x: list[F]) -> list[F]:
    return [sum((a[i][j] * x[j] for j in range(len(x))), F(0)) for i in range(len(a))]


def screen(v: F, degree: int = 100) -> tuple[F, F]:
    # MASTER symmetric point branch with all labels 1 and clip slip strictly
    # inside (-1,1): y=(u,w,i,1), y'=A_v*y, p_x' = u.
    a = [
        [F(-3), F(2), F(0), F(0)],
        [F(1), F(-2), F(1), F(0)],
        [F(0), F(-1), F(-1), v],
        [F(0), F(0), F(0), F(0)],
    ]
    y = [F(3, 10), F(1, 4), F(0), F(1)]
    total = F(0)
    T = F(2)
    for n in range(degree + 1):
        total += y[0] * T ** (n + 1) / factorial(n + 1)
        y = mv(a, y)
    norm = max(sum(abs(x) for x in row) for row in a)
    q = norm * T
    omitted_first_power = degree + 1
    # Integral-tail bound: T*||y0||*q^(N+1)/(N+2)! over a geometric ratio.
    tail = T * q ** omitted_first_power / factorial(omitted_first_power + 1)
    tail /= 1 - q / (omitted_first_power + 2)
    return total, tail


def main() -> None:
    getcontext().prec = 36
    print("point=(p,theta,r,i)=0; u=3/10; omega_L=omega_R=1/4; all labels=1; T=2")
    print("Meaning: exact-rational Taylor partial sum with a norm-tail bound for the conditional clip-interior linear branch; not a full-cell proof.")
    for v in (F(0), F(1, 2), F(1)):
        total, tail = screen(v)
        lo, hi = total - tail, total + tail
        lo_d = Decimal(lo.numerator) / Decimal(lo.denominator)
        hi_d = Decimal(hi.numerator) / Decimal(hi.denominator)
        print(f"V={v}: J in [{lo_d}, {hi_d}], tail={tail}")
    print("task threshold=7/20; threshold was declared before this screen and is not changed by these point bounds")


if __name__ == "__main__":
    main()
