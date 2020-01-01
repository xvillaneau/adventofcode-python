from dataclasses import dataclass
from itertools import combinations, product
from typing import NamedTuple, List

@dataclass
class Character:
    hit_points: int
    damage: int
    armor: int

    def attack(self, other: 'Character'):
        damage = max(1, self.damage - other.armor)
        other.hit_points -= damage

    @property
    def alive(self):
        return self.hit_points > 0

class Equipment(NamedTuple):
    cost: int
    damage: int
    armor: int

WEAPONS = {
    "Dagger": Equipment(8, 4, 0),
    "Shortsword": Equipment(10, 5, 0),
    "Warhammer": Equipment(25, 6, 0),
    "Longsword": Equipment(40, 7, 0),
    "Greataxe": Equipment(74, 8, 0),
}

ARMOR = {
    "Leather": Equipment(13, 0, 1),
    "Chainmail": Equipment(31, 0, 2),
    "Splintmail": Equipment(53, 0, 3),
    "Bandedmail": Equipment(75, 0, 4),
    "Platemail": Equipment(102, 0, 5),
}

RINGS = {
    "Damage +1": Equipment(25, 1, 0),
    "Damage +2": Equipment(50, 2, 0),
    "Damage +3": Equipment(100, 3, 0),
    "Defense +1": Equipment(20, 0, 1),
    "Defense +2": Equipment(40, 0, 2),
    "Defense +3": Equipment(80, 0, 3),
}

def sum_equipment(equipment: List[Equipment]) -> Equipment:
    cost, damage, armor = 0, 0, 0
    for eqp in equipment:
        cost += eqp.cost
        damage += eqp.damage
        armor += eqp.armor
    return Equipment(cost, damage, armor)

def equipement_iter():

    all_weapons = [[w] for w in WEAPONS.values()]

    def _iter_armor():
        yield []
        for armor in ARMOR.values():
            yield [armor]

    all_armor = list(_iter_armor())

    def _iter_rings():
        yield []
        for ring in RINGS.values():
            yield [ring]
        for r1, r2 in combinations(RINGS.values(), 2):
            yield [r1, r2]

    all_rings = list(_iter_rings())

    for weapons, armor, rings in product(all_weapons, all_armor, all_rings):
        yield sum_equipment(weapons + armor + rings)

def equip_player(equipment: Equipment, base_hp=100):
    return Character(base_hp, equipment.damage, equipment.armor)

def player_wins(player: Character, boss: Character):
    while True:
        player.attack(boss)
        if not boss.alive:
            return True
        boss.attack(player)
        if not player.alive:
            return False

BOSS = (103, 9, 2)

def part_1(boss):
    return min(
        eqp.cost for eqp in equipement_iter()
        if player_wins(equip_player(eqp), Character(*boss))
    )

def part_2(boss):
    return max(
        eqp.cost for eqp in equipement_iter()
        if not player_wins(equip_player(eqp), Character(*boss))
    )

if __name__ == '__main__':
    from libaoc import static_input, simple_main
    simple_main(2015, 21, static_input(BOSS), part_1, part_2)
