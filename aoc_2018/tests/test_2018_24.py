from aoc_2018.day_24 import *

EXAMPLE = """
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""".lstrip()


def test_parse_input():
    assert parse_input(EXAMPLE) == (
        {
            GroupStats(5390, 4507, "fire", 2, frozenset(["radiation", "bludgeoning"]), frozenset()): 17,
            GroupStats(1274, 25, "slashing", 3, frozenset(["slashing", "bludgeoning"]), frozenset(["fire"])): 989,
        },
        {
            GroupStats(4706, 116, "bludgeoning", 1, frozenset(["radiation"]), frozenset()): 801,
            GroupStats(2961, 12, "slashing", 4, frozenset(["fire", "cold"]), frozenset(["radiation"])): 4485,
        }
    )

def test_main():
    m = main(EXAMPLE)
    assert next(m) == 5216
    assert next(m) == 51
