"""Finite rational interval primitives for matrices, trigonometry, and roots."""

from __future__ import annotations

import math
from fractions import Fraction

from .rational import Budget, Interval, InvalidInput


Matrix = list[list[Interval]]
Vector = list[Interval]


def identity(n: int, budget: Budget) -> Matrix:
    return [[Interval.point(Fraction(1 if i == j else 0), budget) for j in range(n)] for i in range(n)]


def matrix_add(A: Matrix, B: Matrix) -> Matrix:
    if len(A) != len(B) or any(len(a) != len(b) for a, b in zip(A, B)):
        raise InvalidInput("matrix shape mismatch")
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(A, B)]


def matmul(A: Matrix, B: Matrix) -> Matrix:
    if not A or not B or len(A[0]) != len(B):
        raise InvalidInput("matrix multiplication shape mismatch")
    budget = A[0][0].budget
    if B[0][0].budget is not budget:
        raise RuntimeError("matrix budgets differ")
    rows, inner, cols = len(A), len(B), len(B[0])
    out: Matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            total = Interval.point(Fraction(0), budget)
            for k in range(inner):
                total = total + A[i][k] * B[k][j]
            row.append(total)
        out.append(row)
    return out


def matvec(A: Matrix, v: Vector) -> Vector:
    if not A or len(A[0]) != len(v):
        raise InvalidInput("matrix-vector shape mismatch")
    budget = A[0][0].budget
    out = []
    for row in A:
        total = Interval.point(Fraction(0), budget)
        for a, x in zip(row, v):
            total = total + a * x
        out.append(total)
    return out


def vector_add(a: Vector, b: Vector) -> Vector:
    if len(a) != len(b):
        raise InvalidInput("vector shape mismatch")
    return [x + y for x, y in zip(a, b)]


def scale_vector(v: Vector, scalar: Interval) -> Vector:
    return [x * scalar for x in v]


def interval_matrix_exponential(A: Matrix, T: Fraction, degree: int) -> tuple[Matrix, Fraction, Fraction]:
    """Enclose exp(A(theta)*t), theta in its cell and t in [0,T]."""
    if T <= 0 or degree < 0:
        raise InvalidInput("exponential horizon and degree must be valid")
    budget = A[0][0].budget
    tau = Interval(Fraction(0), T, budget)
    K = [[entry * tau for entry in row] for row in A]
    q = Fraction(0)
    for row in K:
        row_norm = Fraction(0)
        for entry in row:
            row_norm = budget.add(row_norm, entry.abs_upper())
        q = max(q, row_norm)

    result = identity(len(A), budget)
    term = identity(len(A), budget)
    for k in range(1, degree + 1):
        term = matmul(term, K)
        reciprocal = budget.div(Fraction(1), Fraction(k))
        term = [[value.scale(reciprocal) for value in row] for row in term]
        result = matrix_add(result, term)

    if q == 0:
        remainder = Fraction(0)
    else:
        qpow = budget.pow(q, degree + 1)
        exponential_majorant = budget.pow(Fraction(3), (q.numerator + q.denominator - 1) // q.denominator)
        factor = budget.mul(exponential_majorant, qpow)
        remainder = budget.div(factor, Fraction(math.factorial(degree + 1)))
    symmetric = Interval(-remainder, remainder, budget)
    result = [[value + symmetric for value in row] for row in result]
    return result, q, remainder


def interval_power(value: Interval, exponent: int) -> Interval:
    if exponent < 0:
        return interval_power(value, -exponent).reciprocal()
    if exponent == 0:
        return Interval.point(Fraction(1), value.budget)
    b = value.budget
    if exponent % 2 == 0:
        upper_base = max(abs(value.lo), abs(value.hi))
        lower_base = Fraction(0) if value.lo <= 0 <= value.hi else min(abs(value.lo), abs(value.hi))
        return Interval(b.pow(lower_base, exponent), b.pow(upper_base, exponent), b)
    return Interval(b.pow(value.lo, exponent), b.pow(value.hi, exponent), b)


def interval_sine(value: Interval, degree: int) -> Interval:
    if degree < 1:
        raise InvalidInput("trigonometric Taylor degree must be positive")
    b = value.budget
    result = Interval.point(Fraction(0), b)
    for k in range((degree + 1) // 2):
        power = 2 * k + 1
        if power > degree:
            break
        coefficient = Fraction((-1) ** k, math.factorial(power))
        result = result + interval_power(value, power).scale(coefficient)
    max_angle = max(abs(value.lo), abs(value.hi))
    remainder = b.div(b.pow(max_angle, degree + 1), Fraction(math.factorial(degree + 1)))
    result = result + Interval(-remainder, remainder, b)
    return Interval(max(Fraction(-1), result.lo), min(Fraction(1), result.hi), b)


def interval_cosine(value: Interval, degree: int) -> Interval:
    if degree < 0:
        raise InvalidInput("trigonometric Taylor degree must be nonnegative")
    b = value.budget
    result = Interval.point(Fraction(0), b)
    for k in range(degree // 2 + 1):
        power = 2 * k
        if power > degree:
            break
        coefficient = Fraction((-1) ** k, math.factorial(power))
        result = result + interval_power(value, power).scale(coefficient)
    max_angle = max(abs(value.lo), abs(value.hi))
    remainder = b.div(b.pow(max_angle, degree + 1), Fraction(math.factorial(degree + 1)))
    result = result + Interval(-remainder, remainder, b)
    return Interval(max(Fraction(-1), result.lo), min(Fraction(1), result.hi), b)


def sqrt_lower(value: Fraction, bisections: int, budget: Budget) -> tuple[Fraction, Fraction]:
    if value < 0:
        raise InvalidInput("square-root radicand is negative")
    if bisections < 0:
        raise InvalidInput("square-root bisection count is negative")
    if value == 0:
        return Fraction(0), Fraction(0)
    lo, hi = Fraction(0), max(Fraction(1), value)
    for _ in range(bisections):
        mid = budget.div(budget.add(lo, hi), Fraction(2))
        square = budget.mul(mid, mid)
        if square <= value:
            lo = mid
        else:
            hi = mid
    return lo, hi


def matrix_to_json(A: Matrix) -> list[list[list[dict[str, str]]]]:
    return [[item.to_json() for item in row] for row in A]


def vector_to_json(v: Vector) -> list[list[dict[str, str]]]:
    return [item.to_json() for item in v]
