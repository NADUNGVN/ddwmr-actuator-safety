"""Exact-rational piecewise derivative extension for the continuous clip law.

The interval and resource accounting primitives are shared with the project's
G2 validator (`validation.g2.rational`). This module implements only the Auer
piecewise-smooth function layer; it does not integrate an IVP.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from validation.g2.rational import Budget, Interval, InvalidInput


def clip_value(value: Fraction) -> Fraction:
    """The exact law clip(q,-1,1), including its continuous threshold values."""
    return max(Fraction(-1), min(Fraction(1), value))


def clip_interval(value: Interval) -> Interval:
    """Exact range of the monotone scalar clip function on an interval."""
    return Interval(clip_value(value.lo), clip_value(value.hi), value.budget)


def clip_derivative_interval(value: Interval) -> Interval:
    """Auer Eq. (33)/(40) specialization for clip's two continuous corners.

    Strictly saturated intervals have derivative {0}; intervals strictly
    inside (-1,1) have derivative {1}; every interval touching or crossing a
    threshold gets [0,1], the hull of the active one-sided branch derivatives.
    """
    if value.hi < -1 or value.lo > 1:
        return Interval.point(Fraction(0), value.budget)
    if value.lo > -1 and value.hi < 1:
        return Interval.point(Fraction(1), value.budget)
    return Interval(Fraction(0), Fraction(1), value.budget)


def contains(outer: Interval, inner: Interval) -> bool:
    outer._same(inner)
    return outer.lo <= inner.lo and inner.hi <= outer.hi


def clip_mean_value_record(domain: Interval, a: Fraction, b: Fraction) -> dict[str, Any]:
    """Produce a checkable exact witness record for the clip secant lemma."""
    if not domain.lo <= a <= domain.hi or not domain.lo <= b <= domain.hi:
        raise InvalidInput("clip secant endpoints must lie in the declared domain")
    slope = clip_derivative_interval(domain)
    delta = Interval.point(a - b, domain.budget)
    product = slope * delta
    difference = Interval.point(clip_value(a) - clip_value(b), domain.budget)
    return {
        "schema": "auer2013-clip-mean-value-lemma-record-v1",
        "domain": domain.to_json(),
        "a": {"num": str(a.numerator), "den": str(a.denominator)},
        "b": {"num": str(b.numerator), "den": str(b.denominator)},
        "derivative_interval": slope.to_json(),
        "delta_interval": delta.to_json(),
        "mean_value_product": product.to_json(),
        "function_difference": difference.to_json(),
        "included": contains(product, difference),
    }


def verify_clip_mean_value_record(record: Any, budget: Budget) -> bool:
    """Recompute, then compare every serialized field in a lemma record.

    This verifies only the elementary clip secant lemma represented by the
    record. It is not a checker for an IVP tube or VALENCIA proof.
    """
    if not isinstance(record, dict) or record.get("schema") != "auer2013-clip-mean-value-lemma-record-v1":
        return False
    try:
        domain = Interval.from_json(record["domain"], budget)
        a_raw, b_raw = record["a"], record["b"]
        if set(a_raw) != {"num", "den"} or set(b_raw) != {"num", "den"}:
            return False
        a, b = Fraction(int(a_raw["num"]), int(a_raw["den"])), Fraction(int(b_raw["num"]), int(b_raw["den"]))
        expected = clip_mean_value_record(domain, a, b)
    except (KeyError, TypeError, ValueError, ZeroDivisionError, InvalidInput):
        return False
    return record == expected and expected["included"] is True


@dataclass(frozen=True)
class DualInterval:
    """First-order interval AD value with an interval enclosure per coordinate."""

    value: Interval
    gradient: tuple[Interval, ...]

    def __post_init__(self) -> None:
        if any(item.budget is not self.value.budget for item in self.gradient):
            raise RuntimeError("dual value and derivative intervals must share one budget")

    @property
    def dimension(self) -> int:
        return len(self.gradient)

    @classmethod
    def constant(cls, value: Interval, dimension: int) -> "DualInterval":
        if dimension < 0:
            raise InvalidInput("dual dimension must be nonnegative")
        zero = Interval.point(Fraction(0), value.budget)
        return cls(value, (zero,) * dimension)

    @classmethod
    def variable(cls, value: Interval, dimension: int, index: int) -> "DualInterval":
        if dimension < 0 or not 0 <= index < dimension:
            raise InvalidInput("dual variable index is outside its dimension")
        zero, one = Interval.point(Fraction(0), value.budget), Interval.point(Fraction(1), value.budget)
        gradient = [zero] * dimension
        gradient[index] = one
        return cls(value, tuple(gradient))

    def _coerce(self, other: "DualInterval | Interval | Fraction | int") -> "DualInterval":
        if isinstance(other, DualInterval):
            if other.dimension != self.dimension or other.value.budget is not self.value.budget:
                raise RuntimeError("dual dimensions or budgets differ")
            return other
        if isinstance(other, Interval):
            if other.budget is not self.value.budget:
                raise RuntimeError("dual operand budget differs")
            interval = other
        else:
            interval = Interval.point(Fraction(other), self.value.budget)
        return DualInterval.constant(interval, self.dimension)

    def __add__(self, other: "DualInterval | Interval | Fraction | int") -> "DualInterval":
        rhs = self._coerce(other)
        return DualInterval(self.value + rhs.value, tuple(a + b for a, b in zip(self.gradient, rhs.gradient)))

    def __radd__(self, other: "DualInterval | Interval | Fraction | int") -> "DualInterval":
        return self + other

    def __neg__(self) -> "DualInterval":
        return DualInterval(-self.value, tuple(-item for item in self.gradient))

    def __sub__(self, other: "DualInterval | Interval | Fraction | int") -> "DualInterval":
        return self + (-self._coerce(other))

    def __rsub__(self, other: "DualInterval | Interval | Fraction | int") -> "DualInterval":
        return self._coerce(other) - self

    def __mul__(self, other: "DualInterval | Interval | Fraction | int") -> "DualInterval":
        rhs = self._coerce(other)
        value = self.value * rhs.value
        gradient = tuple(a * rhs.value + self.value * b for a, b in zip(self.gradient, rhs.gradient))
        return DualInterval(value, gradient)

    def __rmul__(self, other: "DualInterval | Interval | Fraction | int") -> "DualInterval":
        return self * other

    def reciprocal(self) -> "DualInterval":
        inverse = self.value.reciprocal()
        derivative_factor = -(inverse * inverse)
        return DualInterval(inverse, tuple(derivative_factor * item for item in self.gradient))

    def __truediv__(self, other: "DualInterval | Interval | Fraction | int") -> "DualInterval":
        return self * self._coerce(other).reciprocal()

    def __rtruediv__(self, other: "DualInterval | Interval | Fraction | int") -> "DualInterval":
        return self._coerce(other) * self.reciprocal()

    def clip(self) -> "DualInterval":
        slope = clip_derivative_interval(self.value)
        return DualInterval(clip_interval(self.value), tuple(slope * item for item in self.gradient))

