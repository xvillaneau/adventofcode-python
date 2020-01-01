from collections import defaultdict
from functools import partial
import re
from typing import List

import numpy as np

from libaoc.algo import DFSearch

ORE = 1_000_000_000_000


def parse_data_as_matrices(data: List[str]):
    produced, consumed = {}, defaultdict(list)
    for line in data:
        *inputs, (count_prod, name_prod) = re.findall(r"(\d+) ([A-Z]+)", line)
        produced[name_prod] = int(count_prod)
        for count_cons, name_cons in inputs:
            consumed[name_prod].append((name_cons, int(count_cons)))
    intermediates = [name for name in produced if name != "FUEL"]
    intermediates.sort()
    names = ["ORE"] + intermediates + ["FUEL"]

    _produced = np.array([produced.get(name, 0) for name in names], dtype=int)
    mat_produced = np.repeat(_produced[np.newaxis, :], len(names), axis=0) * np.eye(
        len(names), dtype=int
    )

    _consumed = []
    for name_prod in names:
        line = np.zeros(len(names), dtype=int)
        for name_cons, count_cons in consumed.get(name_prod, []):
            line[names.index(name_cons)] = count_cons
        _consumed.append(line)
    mat_consumed = np.array(_consumed, dtype=int)

    return mat_produced, mat_consumed


def next_steps_for_needed(prod, cons, inventory):
    result = []
    state = np.array(inventory)
    for i in np.argwhere(state[1:] < 0)[:, 0]:
        i += 1
        n = -(state[i] // prod[i, i])
        result.append(tuple(state + n * prod[i] - n * cons[i]))
    return result


def compute_required_ore(prod, cons, fuel=1):
    initial = (0,) * (len(prod) - 1) + (-fuel,)

    def complete(t):
        return all(n >= 0 for n in t[1:])

    solver = DFSearch(initial, complete, partial(next_steps_for_needed, prod, cons))
    return -solver.search().state[0]


def most_fuel_produced(prod, cons, fuel_ini=1, n_ore=ORE):
    prev_fuel, fuel, cost = 0, fuel_ini, 0
    while prev_fuel < fuel:
        cost = compute_required_ore(prod, cons, fuel)
        prev_fuel = fuel
        fuel = fuel * (n_ore // cost) + fuel * (n_ore % cost) // cost
    while cost <= n_ore:
        fuel += 1
        cost = compute_required_ore(prod, cons, fuel)
    return fuel - 1


def main(data: str):
    prod, cons = parse_data_as_matrices(data.splitlines())
    ore_for_1 = compute_required_ore(prod, cons)
    yield ore_for_1
    yield most_fuel_produced(prod, cons, fuel_ini=ORE // ore_for_1)
