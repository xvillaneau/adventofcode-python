from functools import lru_cache
from typing import Tuple, NamedTuple, FrozenSet, Dict

from parsimonious import Grammar, NodeVisitor


GROUP_GRAMMAR = Grammar(r"""
armies       = army+
army         = ~"[A-Za-z ]+" ":\n" group+
group        = units hit_points modifiers attack initiative _?

units        = number "units each with"
hit_points   = number "hit points"
modifiers    = (_? "(" modifier+ ")")?
modifier     = "; "? (immunities / weaknesses)
immunities   = "immune to " (", "? string)+
weaknesses   = "weak to " (", "? string)+
attack       = " with an attack that does" number string "damage"
initiative   = " at initiative" number

_            = ~"\s+"
number       = _? ~"[0-9]+" _?
string       = _? ~"[a-z]+" _?
""")


class InputVisitor(NodeVisitor):
    @classmethod
    def visit_armies(cls, _, children):
        armies = {name: groups for name, groups in children}
        return armies["Immune System"], armies["Infection"]

    @classmethod
    def visit_army(cls, _, children):
        name = children[0].text
        groups = {stats: units for units, stats in children[2]}
        return name, groups

    @classmethod
    def visit_group(cls, _, visited_children):
        units, hp, (weak, immune), (atk, aty), ini = visited_children[:5]
        return units, GroupStats(hp, atk, aty, ini, weak, immune)

    @classmethod
    def visit_units(cls, _, visited_children):
        return visited_children[0]

    @classmethod
    def visit_hit_points(cls, _, visited_children):
        return visited_children[0]

    @classmethod
    def visit_modifiers(cls, _, children):
        if not children:
            return frozenset(), frozenset()
        weak, immune = set(), set()
        for mod, types in children[0][2]:
            if mod == "weak":
                weak.update(types)
            else:
                immune.update(types)
        return frozenset(weak), frozenset(immune)

    @classmethod
    def visit_modifier(cls, _, children):
        return children[1][0]

    @classmethod
    def visit_immunities(cls, _, children):
        return "immune", {c[1] for c in children[1]}

    @classmethod
    def visit_weaknesses(cls, _, children):
        return "weak", {c[1] for c in children[1]}

    @classmethod
    def visit_attack(cls, _, visited_children):
        return visited_children[1], visited_children[2]

    @classmethod
    def visit_initiative(cls, _, visited_children):
        return visited_children[1]

    @classmethod
    def visit_number(cls, _, visited_children):
        return int(visited_children[1].text)

    @classmethod
    def visit_string(cls, _, visited_children):
        return visited_children[1].text

    def generic_visit(self, node, visited_children):
        return visited_children or node


class GroupStats(NamedTuple):
    hit_points: int
    attack_damage: int
    attack_type: str
    initiative: int
    weak_to: FrozenSet[str] = frozenset()
    immune_to: FrozenSet[str] = frozenset()


Army = Dict[GroupStats, int]


def parse_input(data: str) -> Tuple[Army, Army]:
    tree = GROUP_GRAMMAR.parse(data)
    return InputVisitor().visit(tree)


def battle(immune_system: Army, infection: Army, immunity_boost=0):
    units: Dict[GroupStats, int] = {**infection, **immune_system}
    immune_system = set(immune_system)
    infection = set(infection)

    @lru_cache(maxsize=32)
    def adjusted_attack(group: GroupStats):
        bonus = 0 if group in infection else immunity_boost
        return group.attack_damage + bonus

    def effective_power(group: GroupStats):
        return adjusted_attack(group) * units[group]

    def damage_dealt(group_1: GroupStats, group_2: GroupStats):
        if group_1.attack_type in group_2.immune_to:
            return 0
        weak = group_1.attack_type in group_2.weak_to
        return effective_power(group_1) * (1 + weak)

    def attack(group_1: GroupStats, group_2: GroupStats):
        units[group_2] -= damage_dealt(group_1, group_2) // group_2.hit_points

    def selection_order(group: GroupStats):
        return -effective_power(group), -group.initiative

    def target_selector(group: GroupStats):
        def _key(target: GroupStats):
            return -damage_dealt(group, target), *selection_order(target)
        return _key

    def attack_order(pair: Tuple[GroupStats, GroupStats]):
        return -pair[0].initiative

    n_units = sum(n for n in units.values() if n > 0)
    while infection and immune_system:
        # Target selection
        attacks, picked = [], set()
        for attacker in sorted(infection | immune_system, key=selection_order):
            targets = (immune_system if attacker in infection else infection) - picked
            if not targets:
                continue
            defender = min(targets, key=target_selector(attacker))
            if damage_dealt(attacker, defender) <= 0:
                continue
            picked.add(defender)
            attacks.append((attacker, defender))

        for attacker, defender in sorted(attacks, key=attack_order):
            if units[attacker] <= 0:
                continue
            attack(attacker, defender)
            if units[defender] <= 0:
                clan = infection if defender in infection else immune_system
                clan.remove(defender)

        new_n_units = sum(n for n in units.values() if n > 0)
        if new_n_units == n_units:
            break
        n_units = new_n_units

    winner = "infection" if infection else "immune system"
    remaining_hp = sum(g.hit_points * n for g, n in units.items() if n > 0)
    return winner, remaining_hp, n_units


def main(data: str):
    immune_system, infection = parse_input(data)
    winner, rem_hp, rem_units = battle(immune_system, infection)
    yield rem_units

    max_loss = 0
    imm_sys_dmg = sum(g.attack_damage * n for g, n in immune_system.items())
    min_win = rem_hp // imm_sys_dmg
    winner, _, rem_units = battle(immune_system, infection, min_win)
    while winner == "infection":
        max_loss = min_win
        min_win *= 2
        winner, _, rem_units = battle(immune_system, infection, min_win)

    while min_win - max_loss > 1:
        pivot = (min_win + max_loss) // 2
        winner, _, rem_units = battle(immune_system, infection, pivot)
        if winner == "infection":
            max_loss = pivot
        else:
            min_win = pivot

    yield rem_units
