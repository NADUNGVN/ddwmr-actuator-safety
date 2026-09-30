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
        self.operation_attempts = 0
        self.completed_results = 0
        self.wall_seconds = wall_seconds
        self.deadline = time.monotonic() + float(wall_seconds) if wall_seconds is not None else None
        self.max_seen_bits = 0
        self.max_completed_result_bits = 0
        self.max_preoperation_estimate_bits = 0
        self.stage_id = "unclassified"
        self.failure_context: dict[str, Any] | None = None

    def set_stage(self, stage_id: str) -> None:
        if not isinstance(stage_id, str) or not stage_id:
            raise ValueError("resource diagnostic stage must be a nonempty string")
        self.stage_id = stage_id

    @staticmethod
    def _operand_width(value: Fraction) -> dict[str, int]:
        return {
            "numerator_bits": abs(value.numerator).bit_length(),
            "denominator_bits": value.denominator.bit_length(),
        }

    def _fail(
        self, kind: str, detail: str, *, primitive_id: str, estimate_kind: str,
        estimate_bits: int | None, operands: tuple[Fraction, ...], cap_name: str, cap_value: Any,
        extra_context: dict[str, Any] | None = None,
    ) -> None:
        self.failure_context = {
            "schema": "ddwmr-g2-resource-diagnostic-v1",
            "kind": kind,
            "stage_id": self.stage_id,
            "primitive_id": primitive_id,
            "estimate_kind": estimate_kind,
            "estimated_or_observed_bits": estimate_bits,
            "configured_cap_name": cap_name,
            "configured_cap_value": cap_value,
            "operand_bit_lengths": [self._operand_width(x) for x in operands],
            "operation_attempts": self.operation_attempts,
            "operations_started": self.operations,
            "completed_results": self.completed_results,
            "max_preoperation_estimate_bits": self.max_preoperation_estimate_bits,
            "max_completed_result_bits": self.max_completed_result_bits,
            "max_observed_result_bits": self.max_seen_bits,
        }
        if extra_context:
            self.failure_context.update(extra_context)
        raise ResourceLimit(kind, detail)

    def check_input(self, value: Fraction) -> Fraction:
        """Bound and observe a parsed rational without counting it as arithmetic work."""
        bits = max(abs(value.numerator).bit_length(), value.denominator.bit_length())
        self.max_seen_bits = max(self.max_seen_bits, bits)
        if bits > self.max_bits:
            self._fail(
                "RATIONAL_BIT_LIMIT", f"parsed rational input {bits} bits exceeds {self.max_bits}",
                primitive_id="fraction.parse", estimate_kind="input_observed",
                estimate_bits=bits, operands=(), cap_name="max_rational_bits", cap_value=self.max_bits,
            )
        return value

    def _tick(
        self, estimate: int = 0, *, primitive_id: str = "fraction.unknown",
        operands: tuple[Fraction, ...] = (),
    ) -> None:
        self.operation_attempts += 1
        self.max_preoperation_estimate_bits = max(self.max_preoperation_estimate_bits, estimate)
        if estimate > self.max_bits:
            self._fail(
                "RATIONAL_BIT_LIMIT", f"estimated rational intermediate {estimate} bits exceeds {self.max_bits}",
                primitive_id=primitive_id, estimate_kind="preoperation_intermediate_upper_estimate",
                estimate_bits=estimate, operands=operands, cap_name="max_rational_bits", cap_value=self.max_bits,
            )
        if self.operations >= self.max_operations:
            self._fail(
                "RATIONAL_OPERATION_LIMIT", f"operation cap {self.max_operations} exceeded",
                primitive_id=primitive_id, estimate_kind="operation_count", estimate_bits=None,
                operands=operands, cap_name="max_rational_operations", cap_value=self.max_operations,
            )
        self.operations += 1
        if self.deadline is not None and (self.operations & 255) == 0 and time.monotonic() > self.deadline:
            self._fail(
                "WALL_TIME_LIMIT", "per-query wall-time cap exceeded", primitive_id=primitive_id,
                estimate_kind="wall_time", estimate_bits=None, operands=operands,
                cap_name="wall_seconds_per_query",
                cap_value={"num": str(self.wall_seconds.numerator), "den": str(self.wall_seconds.denominator)},
            )

    def _check_result(self, value: Fraction, *, primitive_id: str, operands: tuple[Fraction, ...]) -> Fraction:
        bits = max(abs(value.numerator).bit_length(), value.denominator.bit_length())
        self.max_seen_bits = max(self.max_seen_bits, bits)
        self.completed_results += 1
        if bits > self.max_bits:
            self._fail(
                "RATIONAL_BIT_LIMIT", f"reduced rational result {bits} bits exceeds {self.max_bits}",
                primitive_id=primitive_id, estimate_kind="reduced_result", estimate_bits=bits,
                operands=operands, cap_name="max_rational_bits", cap_value=self.max_bits,
            )
        self.max_completed_result_bits = max(self.max_completed_result_bits, bits)
        return value

    def shift_left_nonnegative(self, value: int, shift: int, *, primitive_id: str) -> int:
        """Meter an exact nonnegative integer left shift before constructing it."""
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise InvalidInput("integer shift input must be a nonnegative integer")
        if not isinstance(shift, int) or isinstance(shift, bool) or shift < 0:
            raise InvalidInput("integer shift count must be a nonnegative integer")
        estimate = value.bit_length() + shift
        self._tick(estimate, primitive_id=primitive_id, operands=(Fraction(value),))
        result = value << shift
        return int(self._check_result(Fraction(result), primitive_id=primitive_id, operands=(Fraction(value),)))

    def divmod_nonnegative(self, numerator: int, denominator: int, *, primitive_id: str) -> tuple[int, int]:
        """Meter exact nonnegative integer division and observe both outputs."""
        if (not isinstance(numerator, int) or isinstance(numerator, bool) or numerator < 0
                or not isinstance(denominator, int) or isinstance(denominator, bool) or denominator <= 0):
            raise InvalidInput("integer divmod requires a nonnegative numerator and positive denominator")
        estimate = max(numerator.bit_length(), denominator.bit_length())
        operands = (Fraction(numerator), Fraction(denominator))
        self._tick(estimate, primitive_id=primitive_id, operands=operands)
        quotient, remainder = divmod(numerator, denominator)
        self._check_result(Fraction(quotient), primitive_id=primitive_id, operands=operands)
        remainder_bits = remainder.bit_length()
        self.max_seen_bits = max(self.max_seen_bits, remainder_bits)
        if remainder_bits > self.max_bits:
            self._fail(
                "RATIONAL_BIT_LIMIT", f"integer division remainder {remainder_bits} bits exceeds {self.max_bits}",
                primitive_id=primitive_id, estimate_kind="reduced_result", estimate_bits=remainder_bits,
                operands=operands, cap_name="max_rational_bits", cap_value=self.max_bits,
            )
        return quotient, remainder

    def increment_nonnegative(self, value: int, *, primitive_id: str) -> int:
        """Meter the exact +1 used by a nonintegral upward rounding."""
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise InvalidInput("integer increment input must be a nonnegative integer")
        estimate = max(1, value.bit_length() + 1)
        self._tick(estimate, primitive_id=primitive_id, operands=(Fraction(value),))
        result = value + 1
        return int(self._check_result(Fraction(result), primitive_id=primitive_id, operands=(Fraction(value),)))

    def dyadic_fraction(self, numerator: int, denominator: int, *, primitive_id: str) -> Fraction:
        """Construct a reduced rational from checked nonnegative integer parts."""
        if (not isinstance(numerator, int) or isinstance(numerator, bool) or numerator < 0
                or not isinstance(denominator, int) or isinstance(denominator, bool) or denominator <= 0):
            raise InvalidInput("dyadic rational requires a nonnegative numerator and positive denominator")
        operands = (Fraction(numerator), Fraction(denominator))
        estimate = max(numerator.bit_length(), denominator.bit_length())
        self._tick(estimate, primitive_id=primitive_id, operands=operands)
        return self._check_result(Fraction(numerator, denominator), primitive_id=primitive_id, operands=operands)

    def add(self, a: Fraction, b: Fraction) -> Fraction:
        if a == -b:
            self._tick(1, primitive_id="fraction.add.cancellation", operands=(a, b))
            return self._check_result(Fraction(0), primitive_id="fraction.add.cancellation", operands=(a, b))
        if a == 0 or b == 0:
            value = b if a == 0 else a
            estimate = max(abs(value.numerator).bit_length(), value.denominator.bit_length())
            self._tick(estimate, primitive_id="fraction.add.identity", operands=(a, b))
            return self._check_result(value, primitive_id="fraction.add.identity", operands=(a, b))
        common = math.gcd(a.denominator, b.denominator)
        a_scale = b.denominator // common
        b_scale = a.denominator // common
        num_estimate = max(
            abs(a.numerator).bit_length() + a_scale.bit_length(),
            abs(b.numerator).bit_length() + b_scale.bit_length(),
        ) + 1
        den_estimate = b_scale.bit_length() + b.denominator.bit_length()
        estimate = max(num_estimate, den_estimate)
        self._tick(estimate, primitive_id="fraction.add", operands=(a, b))
        return self._check_result(a + b, primitive_id="fraction.add", operands=(a, b))

    def mul(self, a: Fraction, b: Fraction) -> Fraction:
        if a == 0 or b == 0:
            self._tick(1, primitive_id="fraction.mul", operands=(a, b))
            return self._check_result(Fraction(0), primitive_id="fraction.mul.zero", operands=(a, b))
        if a in (1, -1) or b in (1, -1):
            value = b * a if a in (1, -1) else a * b
            estimate = max(abs(value.numerator).bit_length(), value.denominator.bit_length())
            self._tick(estimate, primitive_id="fraction.mul.identity", operands=(a, b))
            return self._check_result(value, primitive_id="fraction.mul.identity", operands=(a, b))
        cancel_left = math.gcd(abs(a.numerator), b.denominator)
        cancel_right = math.gcd(abs(b.numerator), a.denominator)
        left_num = abs(a.numerator) // cancel_left
        right_num = abs(b.numerator) // cancel_right
        left_den = a.denominator // cancel_right
        right_den = b.denominator // cancel_left
        estimate = max(
            left_num.bit_length() + right_num.bit_length(),
            left_den.bit_length() + right_den.bit_length(),
        )
        self._tick(estimate, primitive_id="fraction.mul", operands=(a, b))
        return self._check_result(a * b, primitive_id="fraction.mul", operands=(a, b))

    def div(self, a: Fraction, b: Fraction) -> Fraction:
        if b == 0:
            raise InvalidInput("division by zero")
        if a == b or a == -b:
            value = Fraction(1) if a == b else Fraction(-1)
            self._tick(1, primitive_id="fraction.div.cancellation", operands=(a, b))
            return self._check_result(value, primitive_id="fraction.div.cancellation", operands=(a, b))
        if a == 0:
            self._tick(1, primitive_id="fraction.div", operands=(a, b))
            return self._check_result(Fraction(0), primitive_id="fraction.div.zero", operands=(a, b))
        if b in (1, -1):
            value = a if b == 1 else -a
            estimate = max(abs(value.numerator).bit_length(), value.denominator.bit_length())
            self._tick(estimate, primitive_id="fraction.div.identity", operands=(a, b))
            return self._check_result(value, primitive_id="fraction.div.identity", operands=(a, b))
        cancel_numerators = math.gcd(abs(a.numerator), abs(b.numerator))
        cancel_denominators = math.gcd(a.denominator, b.denominator)
        left_num = abs(a.numerator) // cancel_numerators
        right_num = b.denominator // cancel_denominators
        left_den = a.denominator // cancel_denominators
        right_den = abs(b.numerator) // cancel_numerators
        estimate = max(
            left_num.bit_length() + right_num.bit_length(),
            left_den.bit_length() + right_den.bit_length(),
        )
        self._tick(estimate, primitive_id="fraction.div", operands=(a, b))
        return self._check_result(a / b, primitive_id="fraction.div", operands=(a, b))

    def pow(self, a: Fraction, exponent: int) -> Fraction:
        if a in (1, -1):
            value = Fraction(-1 if a == -1 and exponent % 2 else 1)
            self._tick(1, primitive_id="fraction.pow.unit_base", operands=(a,))
            return self._check_result(value, primitive_id="fraction.pow.unit_base", operands=(a,))
        if exponent == 0:
            self._tick(1, primitive_id="fraction.pow.zero_exponent", operands=(a,))
            return self._check_result(Fraction(1), primitive_id="fraction.pow.zero_exponent", operands=(a,))
        if exponent == 1:
            estimate = max(abs(a.numerator).bit_length(), a.denominator.bit_length())
            self._tick(estimate, primitive_id="fraction.pow.identity", operands=(a,))
            return self._check_result(a, primitive_id="fraction.pow.identity", operands=(a,))
        if exponent < 0:
            if a == 0:
                raise InvalidInput("zero to a negative power")
            return self.div(Fraction(1), self.pow(a, -exponent))
        estimate = max(abs(a.numerator).bit_length(), a.denominator.bit_length()) * exponent
        self._tick(estimate, primitive_id="fraction.pow", operands=(a,))
        return self._check_result(a**exponent, primitive_id="fraction.pow", operands=(a,))

    def diagnostic(self) -> dict[str, Any]:
        wall_limit = None
        if self.deadline is not None:
            wall_limit = {
                "enforced": True,
                "configured_seconds": {"num": str(self.wall_seconds.numerator), "den": str(self.wall_seconds.denominator)},
                "remaining_seconds_display_only": max(0.0, self.deadline - time.monotonic()),
            }
        return {
            "schema": "ddwmr-g2-resource-diagnostic-v1",
            "stage_id": self.stage_id,
            "configured_caps": {
                "max_rational_bits": self.max_bits,
                "max_rational_operations": self.max_operations,
                "wall_time": wall_limit or {"enforced": False},
            },
            "operation_attempts": self.operation_attempts,
            "operations_started": self.operations,
            "completed_results": self.completed_results,
            "max_preoperation_estimate_bits": self.max_preoperation_estimate_bits,
            "max_completed_result_bits": self.max_completed_result_bits,
            "max_observed_result_bits": self.max_seen_bits,
            "failure": self.failure_context,
        }


def parse_q(value: Any, budget: Budget | None = None) -> Fraction:
    if not isinstance(value, dict) or set(value) != {"num", "den"}:
        raise InvalidInput("rational must be an object with num and den strings")
    if not isinstance(value["num"], str) or not isinstance(value["den"], str):
        raise InvalidInput("rational numerator and denominator must be strings")
    if re.fullmatch(r"-?(0|[1-9][0-9]*)", value["num"]) is None or re.fullmatch(r"(0|[1-9][0-9]*)", value["den"]) is None:
        raise InvalidInput("rational integers must use canonical base-10 strings")
    if budget is not None:
        num_digits = len(value["num"].lstrip("+-"))
        den_digits = len(value["den"])
        decimal_cap = math.floor(budget.max_bits * math.log10(2)) + 1
        if max(num_digits, den_digits) > decimal_cap:
            digit_upper_bits = math.ceil(max(num_digits, den_digits) * math.log2(10))
            budget._fail(
                "RATIONAL_BIT_LIMIT", "rational input digit count exceeds the configured bit cap",
                primitive_id="fraction.parse", estimate_kind="input_digit_width_upper_estimate",
                estimate_bits=digit_upper_bits, operands=(), cap_name="max_rational_bits", cap_value=budget.max_bits,
                extra_context={"input_digit_lengths": {"num": num_digits, "den": den_digits}},
            )
    try:
        n, d = int(value["num"]), int(value["den"])
    except ValueError as exc:
        raise InvalidInput("invalid integer in rational") from exc
    if d <= 0:
        raise InvalidInput("rational denominator must be positive")
    if math.gcd(n, d) != 1:
        raise InvalidInput("rational must be reduced")
    if budget is not None:
        budget.check_input(Fraction(n, d))
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
