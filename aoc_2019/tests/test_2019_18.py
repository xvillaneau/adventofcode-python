import pytest
from aoc_2019.day_18 import day_18_part_1, day_18_part_2

example_1 = """
#########
#b.A.@.a#
#########
"""

example_2 = """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""

example_3 = """
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
"""

example_4 = """
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
"""

example_5 = """
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
"""

FEWEST_STEPS_1 = [
    (example_1, 8),
    (example_2, 86),
    (example_3, 132),
    (example_4, 136),
    (example_5, 81),
]


@pytest.mark.parametrize("data,steps", FEWEST_STEPS_1)
def test_part_1(data, steps):
    assert day_18_part_1(data) == steps


example_6 = """
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######
"""

example_7 = """
###############
#d.ABC.#.....a#
######...######
######.@.######
######...######
#b.....#.....c#
###############
"""

example_8 = """
#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############
"""

example_9 = """
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############
"""

FEWEST_STEPS_2 = [
    (example_6, 8),
    (example_7, 24),
    (example_8, 32),
    (example_9, 72),
]


@pytest.mark.parametrize("data,steps", FEWEST_STEPS_2)
def test_part_2(data, steps):
    assert day_18_part_2(data) == steps
