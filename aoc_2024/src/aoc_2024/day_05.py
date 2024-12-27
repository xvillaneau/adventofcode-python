import functools


class Rules:
    rules: dict[tuple[int, int], int]

    def __init__(self, data: str):
        self.rules = {}
        for ln in data.strip().splitlines():
            sa, _, sb = ln.partition("|")
            a, b = int(sa), int(sb)
            self.rules[a, a] = 0
            self.rules[b, b] = 0
            self.rules[a, b] = -1
            self.rules[b, a] = 1

    def cmp(self, a, b) -> int:
        return self.rules[a, b]

    @functools.cached_property
    def key(self):
        return functools.cmp_to_key(self.cmp)


def parse_input(data: str) -> tuple[Rules, list[list[int]]]:
    rules_str, updates_str = data.strip().split("\n\n")

    rules = Rules(rules_str)

    updates = []
    for ln in updates_str.splitlines():
        updates.append([int(x) for x in ln.split(",")])

    return rules, updates


def sort_sums(rules: Rules, updates: list[list[int]]):
    part_1, part_2 = 0, 0
    for up in updates:
        sup = sorted(up, key=rules.key)
        if up == sup:
            part_1 += up[len(up) // 2]
        else:
            part_2 += sup[len(sup) // 2]
    return part_1, part_2


def main(data: str):
    rules, updates = parse_input(data)

    yield from sort_sums(rules, updates)
