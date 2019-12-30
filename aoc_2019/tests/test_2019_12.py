from aoc_2019.day_12 import System, part_1

example = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""".strip().splitlines()


def test_load():
    system = System.from_input(example)

    assert system[0].pos == (-1, 0, 2)
    assert system[0].velocity == (0, 0, 0)
    assert system[1].pos == (2, -10, -7)
    assert system[1].velocity == (0, 0, 0)
    assert system[2].pos == (4, -8, 8)
    assert system[2].velocity == (0, 0, 0)
    assert system[3].pos == (3, 5, -1)
    assert system[3].velocity == (0, 0, 0)


def test_step():
    system = System.from_input(example)
    system.run_step()

    assert system[0].pos == (2, -1, 1)
    assert system[0].velocity == (3, -1, -1)
    assert system[1].pos == (3, -7, -4)
    assert system[1].velocity == (1, 3, 3)
    assert system[2].pos == (1, -7, 5)
    assert system[2].velocity == (-3, 1, -3)
    assert system[3].pos == (2, 2, 0)
    assert system[3].velocity == (-1, -3, 1)


example_2 = """
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
""".strip().splitlines()


def test_part_1():
    assert part_1(example, 10) == 179
    assert part_1(example_2, 100) == 1940


def test_find_repeat():
    system = System.from_input(example)
    assert system.find_repeat() == 2772

    system = System.from_input(example_2)
    assert system.find_repeat() == 4686774924
