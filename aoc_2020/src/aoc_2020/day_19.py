from abc import ABCMeta, abstractmethod
from collections import Iterator
from dataclasses import dataclass
from functools import cached_property


class Rule(metaclass=ABCMeta):

    def __add__(self, other) -> 'Rule':
        return AndRule([self, other])

    def __or__(self, other) -> 'Rule':
        return OrRule([self, other])

    @property
    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def matches(self, string: str) -> Iterator[int]:
        pass


@dataclass
class StrRule(Rule):
    value: str

    def __add__(self, other) -> 'Rule':
        if isinstance(other, StrRule):
            return StrRule(self.value + other.value)
        elif isinstance(other, AndRule):
            return AndRule([self, *other.rules])
        else:
            return AndRule([self, other])

    @cached_property
    def size(self):
        return len(self.value)

    def matches(self, string: str) -> Iterator[int]:
        if string.startswith(self.value):
            yield len(self.value)


@dataclass
class AndRule(Rule):
    rules: list['Rule']

    def __add__(self, other) -> 'Rule':
        if isinstance(other, AndRule):
            return AndRule(self.rules + other.rules)
        else:
            return AndRule([*self.rules, other])

    @cached_property
    def size(self):
        return sum(r.size for r in self.rules)

    def matches(self, string) -> Iterator[int]:
        offsets = {0}
        for rule in self.rules:
            next_offsets = set()
            for d in offsets:
                next_offsets.update(d + n for n in rule.matches(string[d:]))
            if not next_offsets:
                return
            offsets = next_offsets
        yield from offsets


@dataclass
class OrRule(Rule):
    rules: list['Rule']

    def __or__(self, other):
        if isinstance(other, OrRule):
            return OrRule(self.rules + other.rules)
        else:
            return OrRule([*self.rules, other])

    @cached_property
    def size(self):
        lengths = {r.size for r in self.rules}
        if len(lengths) != 1:
            raise ValueError("Variable length rule")
        return lengths.pop()

    def matches(self, string) -> Iterator[int]:
        for rule in self.rules:
            yield from rule.matches(string)


@dataclass
class Rule8(Rule):
    rule_42: 'Rule'

    @property
    def size(self):
        raise ValueError("Variable length rule")

    def matches(self, string) -> Iterator[int]:
        rule = self.rule_42
        while rule.size <= len(string):
            yield from rule.matches(string)
            if not any(self.rule_42.matches(string[rule.size:])):
                break
            rule = rule + self.rule_42


@dataclass
class Rule11(Rule):
    rule_42: 'Rule'
    rule_31: 'Rule'

    @property
    def size(self):
        raise ValueError("Variable length rule")

    def matches(self, string) -> Iterator[int]:
        rule = self.rule_42 + self.rule_31
        while rule.size <= len(string):
            yield from rule.matches(string)
            if not any(self.rule_42.matches(string[rule.size // 2:])):
                break
            rule = self.rule_42 + rule + self.rule_31


def parse_input(data: str, with_loops=False):
    data = iter(data.splitlines())

    rules_str: dict[int, str] = {}
    while (line := next(data)):
        num, _, desc = line.partition(': ')
        rules_str[int(num)] = desc

    messages = list(data)  # Remaining lines
    rules: dict[int, Rule] = {}

    def build_and(string: str):
        ids = [int(n) for n in string.split()]
        rule = get_rule(ids[0])
        for n in ids[1:]:
            rule = rule + get_rule(n)
        return rule

    def get_rule(id: int) -> Rule:
        if id in rules:
            return rules[id]

        if with_loops and id == 8:
            rule = Rule8(get_rule(42))
        elif with_loops and id == 11:
            rule = Rule11(get_rule(42), get_rule(31))
        else:
            string = rules_str[id]
            if string in ('"a"', '"b"'):
                rule = StrRule(string[1])
            else:
                left, _, right = string.partition(' | ')
                rule = build_and(left)
                if right:
                    rule = rule | build_and(right)

        rules[id] = rule
        return rule

    return get_rule(0), messages


def count_full_matches(rule: Rule, messages: list[str]) -> int:
    matches = 0
    for msg in messages:
        res = any(n == len(msg) for n in rule.matches(msg))
        matches += res
    return matches


def main(data: str):
    yield count_full_matches(*parse_input(data))
    yield count_full_matches(*parse_input(data, with_loops=True))
