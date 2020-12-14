from aoc_2020.day_13 import bus_sync_step, parse_buses, sync_buses, wait_times

EXAMPLE = """
939
7,13,x,x,59,x,31,19
""".strip()


def test_wait_times():
    assert list(wait_times(*parse_buses(EXAMPLE))) == [
        (7, 6), (13, 10), (59, 5), (31, 22), (19, 11)
    ]


def test_bus_sync_step():
    assert bus_sync_step((0, 0, 0), 7) == (7, 0, 1)
    assert bus_sync_step((0, 0, 1), 7) == (7, 1, 2)
    assert bus_sync_step((7, 0, 1), 13) == (91, 77, 2)
    assert bus_sync_step((91, 77, 4), 59) == (5369, 350, 5)


def test_sync_buses():
    assert sync_buses(parse_buses(EXAMPLE)[1]) == 1068781
