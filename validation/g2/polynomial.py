"""Closed rational-expression parser and exact polynomial identity checks."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from .rational import Budget, Interval, InvalidInput, parse_q


MAX_POLY_TERMS = 20000
MAX_POLY_DEGREE = 64
MAX_AST_DEPTH = 80


@dataclass
class Poly:
    dim: int
    terms: dict[tuple[int, ...], Fraction]
    budget: Budget

    @classmethod
    def constant(cls, dim: int, c: Fraction, budget: Budget) -> "Poly":
        return cls(dim, {} if c == 0 else {(0,) * dim: c}, budget)

    @classmethod
    def variable(cls, dim: int, index: int, budget: Budget) -> "Poly":
        monomial = [0] * dim
        monomial[index] = 1
        return cls(dim, {tuple(monomial): Fraction(1)}, budget)

    def _check(self, other: "Poly") -> None:
        if self.dim != other.dim or self.budget is not other.budget:
            raise RuntimeError("incompatible polynomial operands")

    def __neg__(self) -> "Poly":
        return Poly(self.dim, {m: -c for m, c in self.terms.items()}, self.budget)

    def __add__(self, other: "Poly") -> "Poly":
        self._check(other)
        result = dict(self.terms)
        for monomial, coeff in other.terms.items():
            if monomial in result:
                value = self.budget.add(result[monomial], coeff)
                if value:
                    result[monomial] = value
                else:
                    del result[monomial]
            else:
                result[monomial] = coeff
        self._check_size(result)
        return Poly(self.dim, result, self.budget)

    def __sub__(self, other: "Poly") -> "Poly":
        return self + (-other)

    def __mul__(self, other: "Poly") -> "Poly":
        self._check(other)
        result: dict[tuple[int, ...], Fraction] = {}
        for ma, ca in self.terms.items():
            for mb, cb in other.terms.items():
                monomial = tuple(a + b for a, b in zip(ma, mb))
                if sum(monomial) > MAX_POLY_DEGREE:
                    raise InvalidInput("rational-map polynomial degree exceeds the supported limit")
                value = self.budget.mul(ca, cb)
                if monomial in result:
                    value = self.budget.add(result[monomial], value)
                if value:
                    result[monomial] = value
                else:
                    result.pop(monomial, None)
                self._check_size(result)
        return Poly(self.dim, result, self.budget)

    @staticmethod
    def _check_size(terms: dict[tuple[int, ...], Fraction]) -> None:
        if len(terms) > MAX_POLY_TERMS:
            raise InvalidInput("rational-map polynomial exceeds the supported term limit")

    def evaluate(self, variables: list[Interval]) -> Interval:
        if len(variables) != self.dim:
            raise RuntimeError("polynomial variable dimension mismatch")
        total = Interval.point(Fraction(0), self.budget)
        for monomial, coeff in self.terms.items():
            term = Interval.point(coeff, self.budget)
            for index, exponent in enumerate(monomial):
                if exponent:
                    term = term * interval_power(variables[index], exponent)
            total = total + term
        return total


def interval_power(value: Interval, exponent: int) -> Interval:
    if exponent < 0:
        return interval_power(value, -exponent).reciprocal()
    if exponent == 0:
        return Interval.point(Fraction(1), value.budget)
    budget = value.budget
    if exponent % 2 == 0:
        upper_base = max(abs(value.lo), abs(value.hi))
        lower = Fraction(0) if value.lo <= 0 <= value.hi else min(abs(value.lo), abs(value.hi))
        return Interval(budget.pow(lower, exponent), budget.pow(upper_base, exponent), budget)
    return Interval(budget.pow(value.lo, exponent), budget.pow(value.hi, exponent), budget)


@dataclass
class RationalFunction:
    numerator: Poly
    denominator: Poly

    @property
    def budget(self) -> Budget:
        return self.numerator.budget

    @property
    def dim(self) -> int:
        return self.numerator.dim

    def __neg__(self) -> "RationalFunction":
        return RationalFunction(-self.numerator, self.denominator)

    def __add__(self, other: "RationalFunction") -> "RationalFunction":
        return RationalFunction(
            self.numerator * other.denominator + other.numerator * self.denominator,
            self.denominator * other.denominator,
        )

    def __sub__(self, other: "RationalFunction") -> "RationalFunction":
        return self + (-other)

    def __mul__(self, other: "RationalFunction") -> "RationalFunction":
        return RationalFunction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other: "RationalFunction") -> "RationalFunction":
        return RationalFunction(self.numerator * other.denominator, self.denominator * other.numerator)

    def evaluate(self, variables: list[Interval]) -> Interval:
        numerator = self.numerator.evaluate(variables)
        denominator = self.denominator.evaluate(variables)
        if denominator.lo <= 0:
            raise InvalidInput("rational-map denominator lacks a strict positive interval witness")
        return numerator / denominator


def _constant(dim: int, value: Fraction, budget: Budget) -> RationalFunction:
    return RationalFunction(Poly.constant(dim, value, budget), Poly.constant(dim, Fraction(1), budget))


def parse_expression(
    raw: Any,
    label_order: list[str],
    label_box: dict[str, Interval],
    budget: Budget,
    depth: int = 0,
) -> RationalFunction:
    if depth > MAX_AST_DEPTH:
        raise InvalidInput("rational-map expression exceeds AST depth limit")
    budget._tick()
    dim = len(label_order)
    if isinstance(raw, dict) and set(raw) == {"num", "den"}:
        return _constant(dim, parse_q(raw, budget), budget)
    if not isinstance(raw, dict):
        raise InvalidInput("rational-map nodes must be exact JSON objects")
    if set(raw) == {"const"}:
        return _constant(dim, parse_q(raw["const"], budget), budget)
    if set(raw) == {"var"}:
        name = raw["var"]
        if name not in label_order or name not in label_box:
            raise InvalidInput(f"unknown parameter label {name!r}")
        return RationalFunction(Poly.variable(dim, label_order.index(name), budget), Poly.constant(dim, Fraction(1), budget))
    if set(raw) != {"op", "args"} or raw["op"] not in {"add", "sub", "mul", "div"}:
        raise InvalidInput("unsupported rational-map expression node")
    args = raw["args"]
    if not isinstance(args, list) or len(args) != 2:
        raise InvalidInput("binary rational-map operation requires exactly two arguments")
    left = parse_expression(args[0], label_order, label_box, budget, depth + 1)
    right = parse_expression(args[1], label_order, label_box, budget, depth + 1)
    op = raw["op"]
    if op == "add":
        return left + right
    if op == "sub":
        return left - right
    if op == "mul":
        return left * right
    divisor = right.evaluate([label_box[name] for name in label_order])
    if divisor.lo <= 0:
        raise InvalidInput("division node requires a checked strictly positive divisor")
    return left / right


def rational_functions_equal(left: RationalFunction, right: RationalFunction) -> bool:
    difference = left.numerator * right.denominator - right.numerator * left.denominator
    return not difference.terms
