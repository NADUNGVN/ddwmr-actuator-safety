"""Exact rational and interval arithmetic with explicit finite resource caps."""

from __future__ import annotations

import math
import re
import time
from dataclasses import dataclass
from fractions import Fraction
from typing import Any


class ResourceLimit(RuntimeError):
    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind
        self.detail = detail


class InvalidInput(ValueError):
    pass


class Budget:
    def __init__(self, max_bits: int, max_operations: int, wall_seconds: Fraction | None = None):
        if max_bits <= 0 or max_operations <= 0:
            raise InvalidInput("resource limits must be positive")
        self.max_bits = max_bits
        self.max_operations = max_operations
        self.operations = 0
        self.deadline = time.monotonic() + float(wall_seconds) if wall_seconds is not None else None
        self.max_seen_bits = 0

    def _tick(self, estimate: int = 0) -> None:
        if estimate > self.max_bits:
            raise ResourceLimit("RATIONAL_BIT_LIMIT", f"estimated rational intermediate {estimate} bits exceeds {self.max_bits}")
        self.operations += 1
        if self.operations > self.max_operations:
            raise ResourceLimit("RATIONAL_OPERATION_LIMIT", f"operation cap {self.max_operations} exceeded")
        if self.deadline is not None and (self.operations & 255) == 0 and time.monotonic() > self.deadline:
            raise ResourceLimit("WALL_TIME_LIMIT", "per-query wall-time cap exceeded")

    def _check_result(self, value: Fraction) -> Fraction:
        bits = max(abs(value.numerator).bit_length(), value.denominator.bit_length())
        self.max_seen_bits = max(self.max_seen_bits, bits)
        if bits > self.max_bits:
            raise ResourceLimit("RATIONAL_BIT_LIMIT", f"rational result {bits} bits exceeds {self.max_bits}")
        return value

    def add(self, a: Fraction, b: Fraction) -> Fraction:
        estimate = max(
            abs(a.numerator).bit_length() + b.denominator.bit_length(),
            abs(b.numerator).bit_length() + a.denominator.bit_length(),
        ) + 1
        estimate = max(estimate, a.denominator.bit_length() + b.denominator.bit_length())
        self._tick(estimate)
        return self._check_result(a + b)

    def mul(self, a: Fraction, b: Fraction) -> Fraction:
        estimate = max(
            abs(a.numerator).bit_length() + abs(b.numerator).bit_length(),
            a.denominator.bit_length() + b.denominator.bit_length(),
        )
        self._tick(estimate)
        return self._check_result(a * b)

    def div(self, a: Fraction, b: Fraction) -> Fraction:
        if b == 0:
            raise InvalidInput("division by zero")
        estimate = max(
            abs(a.numerator).bit_length() + b.denominator.bit_length(),
            a.denominator.bit_length() + abs(b.numerator).bit_length(),
        )
        self._tick(estimate)
        return self._check_result(a / b)

    def pow(self, a: Fraction, exponent: int) -> Fraction:
        if exponent < 0:
            if a == 0:
                raise InvalidInput("zero to a negative power")
            return self.div(Fraction(1), self.pow(a, -exponent))
        estimate = max(abs(a.numerator).bit_length(), a.denominator.bit_length()) * exponent
        self._tick(estimate)
        return self._check_result(a**exponent)


def parse_q(value: Any, budget: Budget | None = None) -> Fraction:
    if not isinstance(value, dict) or set(value) != {"num", "den"}:
        raise InvalidInput("rational must be an object with num and den strings")
    if not isinstance(value["num"], str) or not isinstance(value["den"], str):
        raise InvalidInput("rational numerator and denominator must be strings")
    if re.fullmatch(r"-?(0|[1-9][0-9]*)", value["num"]) is None or re.fullmatch(r"(0|[1-9][0-9]*)", value["den"]) is None:
        raise InvalidInput("rational integers must use canonical base-10 strings")
    if budget is not None:
        decimal_cap = int(budget.max_bits * math.log10(2)) + 3
        if max(len(value["num"].lstrip("+-")), len(value["den"])) > decimal_cap:
            raise ResourceLimit("RATIONAL_BIT_LIMIT", "rational input digit count exceeds the configured bit cap")
    try:
        n, d = int(value["num"]), int(value["den"])
    except ValueError as exc:
        raise InvalidInput("invalid integer in rational") from exc
    if d <= 0:
        raise InvalidInput("rational denominator must be positive")
    if math.gcd(n, d) != 1:
        raise InvalidInput("rational must be reduced")
    if budget is not None:
        budget._check_result(Fraction(n, d))
    return Fraction(n, d)


def qobj(value: Fraction) -> dict[str, str]:
    return {"num": str(value.numerator), "den": str(value.denominator)}


def qtext(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction
    budget: Budget

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise InvalidInput("interval lower endpoint exceeds upper endpoint")

    @classmethod
    def point(cls, value: Fraction, budget: Budget) -> "Interval":
        return cls(value, value, budget)

    @classmethod
    def from_json(cls, value: Any, budget: Budget) -> "Interval":
        if not isinstance(value, list) or len(value) != 2:
            raise InvalidInput("interval must contain two rational endpoints")
        return cls(parse_q(value[0], budget), parse_q(value[1], budget), budget)

    def to_json(self) -> list[dict[str, str]]:
        return [qobj(self.lo), qobj(self.hi)]

    def _same(self, other: "Interval") -> None:
        if self.budget is not other.budget:
            raise RuntimeError("intervals from different resource budgets were mixed")

    def __add__(self, other: "Interval") -> "Interval":
        self._same(other)
        return Interval(self.budget.add(self.lo, other.lo), self.budget.add(self.hi, other.hi), self.budget)

    def __neg__(self) -> "Interval":
        return Interval(-self.hi, -self.lo, self.budget)

    def __sub__(self, other: "Interval") -> "Interval":
        return self + (-other)

    def __mul__(self, other: "Interval") -> "Interval":
        self._same(other)
        products = [
            self.budget.mul(self.lo, other.lo), self.budget.mul(self.lo, other.hi),
            self.budget.mul(self.hi, other.lo), self.budget.mul(self.hi, other.hi),
        ]
        return Interval(min(products), max(products), self.budget)

    def reciprocal(self) -> "Interval":
        if self.lo <= 0 <= self.hi:
            raise InvalidInput("interval denominator contains zero")
        one = Fraction(1)
        a = self.budget.div(one, self.lo)
        b = self.budget.div(one, self.hi)
        return Interval(min(a, b), max(a, b), self.budget)

    def __truediv__(self, other: "Interval") -> "Interval":
        self._same(other)
        return self * other.reciprocal()

    def scale(self, value: Fraction) -> "Interval":
        return self * Interval.point(value, self.budget)

    def abs_upper(self) -> Fraction:
        return max(abs(self.lo), abs(self.hi))

    def clipped_abs_upper(self, limit: Fraction) -> Fraction:
        return min(limit, self.abs_upper())


def iadd(a: Interval, b: Interval) -> Interval:
    return a + b


def isub(a: Interval, b: Interval) -> Interval:
    return a - b


def imul(a: Interval, b: Interval) -> Interval:
    return a * b


def idiv(a: Interval, b: Interval) -> Interval:
    return a / b


def isum(values: list[Interval], budget: Budget) -> Interval:
    result = Interval.point(Fraction(0), budget)
    for value in values:
        result = result + value
    return result


def interval_abs(value: Interval) -> Interval:
    if value.lo >= 0:
        return value
    if value.hi <= 0:
        return -value
    return Interval(Fraction(0), value.abs_upper(), value.budget)


def upper_abs(value: Interval) -> Fraction:
    return value.abs_upper()


def qmin(a: Fraction, b: Fraction) -> Fraction:
    return a if a <= b else b


def qmax(a: Fraction, b: Fraction) -> Fraction:
    return a if a >= b else b
