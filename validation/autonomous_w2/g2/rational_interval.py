"""Exact closed-rational interval primitive shared by the W2 producer/checker.

The producer and checker implement separate model, propagation, and predicate
logic. Sharing this scalar primitive is disclosed in the release manifest.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any


class ArithmeticLimit(RuntimeError):
    pass


class Budget:
    def __init__(self, max_operations: int, max_bits: int) -> None:
        self.max_operations = max_operations
        self.max_bits = max_bits
        self.operations = 0
        self.max_observed_bits = 0

    def tick(self, *values: Fraction) -> None:
        self.operations += 1
        if self.operations > self.max_operations:
            raise ArithmeticLimit("INTERVAL_OPERATION_CAP")
        for value in values:
            bits = max(abs(value.numerator).bit_length(), value.denominator.bit_length())
            self.max_observed_bits = max(self.max_observed_bits, bits)
            if bits > self.max_bits:
                raise ArithmeticLimit("RATIONAL_BIT_CAP")


_ACTIVE: Budget | None = None


def activate(budget: Budget | None) -> None:
    global _ACTIVE
    _ACTIVE = budget


def q(value: Any) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    raise ValueError("RATIONAL_VALUE_MUST_BE_INTEGER_OR_STRING")


def qs(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class I:
    lo: Fraction
    hi: Fraction

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError("EMPTY_INTERVAL")
        if _ACTIVE:
            _ACTIVE.tick(self.lo, self.hi)

    @staticmethod
    def point(value: Any) -> "I":
        v = q(value)
        return I(v, v)

    @staticmethod
    def coerce(value: Any) -> "I":
        return value if isinstance(value, I) else I.point(value)

    def __add__(self, other: Any) -> "I":
        o = I.coerce(other)
        lo, hi = self.lo + o.lo, self.hi + o.hi
        if _ACTIVE:
            _ACTIVE.tick(lo, hi)
        return I(lo, hi)

    __radd__ = __add__

    def __neg__(self) -> "I":
        return I(-self.hi, -self.lo)

    def __sub__(self, other: Any) -> "I":
        return self + (-I.coerce(other))

    def __rsub__(self, other: Any) -> "I":
        return I.coerce(other) - self

    def __mul__(self, other: Any) -> "I":
        o = I.coerce(other)
        products = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        if _ACTIVE:
            _ACTIVE.tick(*products)
        return I(min(products), max(products))

    __rmul__ = __mul__

    def reciprocal(self) -> "I":
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError("INTERVAL_DIVISOR_CONTAINS_ZERO")
        vals = (1 / self.lo, 1 / self.hi)
        if _ACTIVE:
            _ACTIVE.tick(*vals)
        return I(min(vals), max(vals))

    def __truediv__(self, other: Any) -> "I":
        return self * I.coerce(other).reciprocal()

    def __rtruediv__(self, other: Any) -> "I":
        return I.coerce(other) / self

    def abs_upper(self) -> Fraction:
        return max(abs(self.lo), abs(self.hi))

    def width(self) -> Fraction:
        return self.hi - self.lo

    def to_json(self) -> list[str]:
        return [qs(self.lo), qs(self.hi)]


def read_interval(value: Any) -> I:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("INTERVAL_MUST_HAVE_TWO_ENDPOINTS")
    return I(q(value[0]), q(value[1]))


def sqrt_lower(value: Fraction, bisections: int) -> Fraction:
    if value < 0:
        raise ValueError("NEGATIVE_SQRT_ARGUMENT")
    if value == 0:
        return Fraction(0)
    lo, hi = Fraction(0), max(Fraction(1), value)
    for _ in range(bisections):
        mid = (lo + hi) / 2
        if _ACTIVE:
            _ACTIVE.tick(mid)
        if mid * mid <= value:
            lo = mid
        else:
            hi = mid
    if lo * lo > value:
        raise ArithmeticError("SQRT_LOWER_WITNESS_FAILED")
    return lo


def max_abs(interval: I) -> Fraction:
    return interval.abs_upper()
