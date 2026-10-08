"""Outward fixed-grid rational intervals for the G2 W2 v3 producer/checker.

Each interval endpoint is rounded to a signed dyadic grid after every
primitive operation.  Inputs and every intermediate enclosure are therefore
outer bounds; unlike exact Fraction endpoint propagation, denominators do not
grow with the number of matrix products or time slabs.  The producer and
checker share this scalar trust root, which is disclosed in the release.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import sys
from typing import Any


class ArithmeticLimit(RuntimeError):
    pass


class Budget:
    def __init__(self, max_operations: int, max_bits: int) -> None:
        self.max_operations = max_operations
        self.max_bits = max_bits
        self.operations = 0
        self.max_observed_bits = 0
        self.rounded_endpoint_count = 0
        self.rounding_events = 0

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
_GRID_BITS = 96
_GRID = 1 << _GRID_BITS


def activate(budget: Budget | None) -> None:
    global _ACTIVE
    _ACTIVE = budget


def configure_fixed_grid(bits: int, rational_bit_cap: int, taylor_degree: int) -> None:
    """Set a dyadic precision with an a-priori scalar-tail bit bound.

    For the frozen profile h=1/8 and degree 20, q=||A||h has denominator at
    most 2**(bits+3); q**(degree+1), the factorial, and the geometric-tail
    denominator stay below the conservative cap checked here.
    """
    global _GRID_BITS, _GRID
    if _ACTIVE is not None:
        raise ArithmeticLimit("CANNOT_CHANGE_GRID_WITH_ACTIVE_BUDGET")
    if bits < 32 or taylor_degree < 0 or rational_bit_cap <= 0:
        raise ArithmeticLimit("FIXED_GRID_PROFILE_INVALID")
    # Include the 1/8 slab denominator, geometric-tail denominator, and a
    # generous factorial allowance; reject profiles that cannot fit the cap.
    conservative_tail_bits = (bits + 8) * (taylor_degree + 2) + 8 * (taylor_degree + 2)
    if conservative_tail_bits >= rational_bit_cap:
        raise ArithmeticLimit("FIXED_GRID_TAIL_EXCEEDS_RATIONAL_BIT_CAP")
    _GRID_BITS = bits
    _GRID = 1 << bits


def _floor_grid(value: Fraction) -> Fraction:
    numerator = value.numerator * _GRID
    return Fraction(numerator // value.denominator, _GRID)


def _ceil_grid(value: Fraction) -> Fraction:
    numerator = value.numerator * _GRID
    return Fraction(-((-numerator) // value.denominator), _GRID)


def q(value: Any) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    raise ValueError("RATIONAL_VALUE_MUST_BE_INTEGER_OR_STRING")


def qs(value: Fraction) -> str:
    if _ACTIVE:
        _ACTIVE.tick(value)
    return f"{value.numerator}/{value.denominator}"


def configure_integer_string_limit(decimal_digits: int, rational_bit_cap: int) -> None:
    required_digits = (rational_bit_cap * 30103 + 99999) // 100000 + 2
    if decimal_digits < required_digits or decimal_digits > 10000:
        raise ArithmeticLimit("INTEGER_STRING_DIGIT_CAP_INCONSISTENT_WITH_RATIONAL_BIT_CAP")
    if not hasattr(sys, "set_int_max_str_digits"):
        raise ArithmeticLimit("PYTHON_INTEGER_STRING_LIMIT_API_UNAVAILABLE")
    sys.set_int_max_str_digits(decimal_digits)


@dataclass(frozen=True)
class I:
    lo: Fraction
    hi: Fraction

    def __post_init__(self) -> None:
        raw_lo, raw_hi = q(self.lo), q(self.hi)
        if raw_lo > raw_hi:
            raise ValueError("EMPTY_INTERVAL")
        lo, hi = _floor_grid(raw_lo), _ceil_grid(raw_hi)
        if _ACTIVE:
            _ACTIVE.tick(raw_lo, raw_hi, lo, hi)
            _ACTIVE.rounded_endpoint_count += 2
            if lo != raw_lo or hi != raw_hi:
                _ACTIVE.rounding_events += 1
        object.__setattr__(self, "lo", lo)
        object.__setattr__(self, "hi", hi)

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
    """Exact rational bisection; returned value is proved no greater than sqrt."""
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
