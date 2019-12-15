from aoc_2019.day_06 import part_1, parse_map, part_2

MAP = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
""".strip().splitlines()

def test_parse_map():
    bodies = parse_map(MAP)
    assert len(bodies) == 12
    assert bodies['COM'].satellites == [bodies['B']]
    assert bodies['B'].satellites == [bodies['C'], bodies['G']]

def test_part_1():
    assert part_1(MAP) == 42

MAP_2 = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
""".strip().splitlines()

def test_part_2():
    assert part_2(MAP_2) == 4
