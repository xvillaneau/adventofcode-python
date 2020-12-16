from collections import defaultdict
from math import prod
import re
from typing import Dict, List, Tuple

from libaoc.struct import SortedSet

Rules = Dict[str, Tuple[range, range]]
Ticket = List[int]


def parse_notes(notes: List[str]) -> Tuple[Rules, Ticket, List[Ticket]]:
    notes = iter(notes)

    rules = {}
    while (line := next(notes)):
        name, a1, a2, b1, b2 = re.match(
            r'^([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)$', line
        ).groups()
        rules[name] = (
            range(int(a1), int(a2) + 1),
            range(int(b1), int(b2) + 1),
        )

    while next(notes) != 'your ticket:':
        pass
    my_ticket = [int(n) for n in next(notes).split(',')]

    while next(notes) != 'nearby tickets:':
        pass
    tickets = []
    for line in notes:
        tickets.append([int(n) for n in line.split(',')])

    return rules, my_ticket, tickets


def filter_tickets(rules: Rules, tickets: List[Ticket]):
    valid_values: SortedSet[int] = SortedSet()

    for r1, r2 in rules.values():
        valid_values.update(r1)
        valid_values.update(r2)

    valid_tickets, invalid_values = [], []
    for ticket in tickets:
        invalid = [v for v in ticket if v not in valid_values]
        if invalid:
            invalid_values.extend(invalid)
        else:
            valid_tickets.append(ticket)

    return valid_tickets, invalid_values


def detect_fields(rules: Rules, tickets: List[Ticket]):

    def rule_valid(rule, val):
        r1, r2 = rules[rule]
        return val in r1 or val in r2

    candidates = defaultdict(set)
    field_ids = range(len(tickets[0]))
    for i in field_ids:
        fields = set(rules)
        for ticket in tickets:
            fields.intersection_update(
                f for f in fields if rule_valid(f, ticket[i])
            )
        for field in fields:
            candidates[field].add(i)

    fields = [""] * len(field_ids)
    missing = set(field_ids)
    while candidates:
        for name, ids in candidates.items():
            ids.intersection_update(missing)
            if len(ids) == 1:
                fields[(index := ids.pop())] = name
                missing.discard(index)
                candidates.pop(name)
                break

    return fields


def main(data: str):
    rules, my_ticket, tickets = parse_notes(data.splitlines())
    tickets, invalid = filter_tickets(rules, tickets)
    yield sum(invalid)

    fields = detect_fields(rules, tickets)
    yield prod(
        value
        for field, value in zip(fields, my_ticket)
        if field.startswith("departure")
    )
