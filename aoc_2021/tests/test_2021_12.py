import pytest

from aoc_2021.day_12 import parse_map, find_paths, count_more_paths

EXAMPLE_1 = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""
EXAMPLE_2 = """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""
EXAMPLE_3 = """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""


def test_parse_map():
    rooms = parse_map(EXAMPLE_1)
    assert len(rooms) == 6
    assert set(rooms.keys()) == {"start", "end", "A", "b", "c", "d"}
    assert rooms["start"].neighbors == {rooms["A"], rooms["b"]}


N_PATHS = [(EXAMPLE_1, 10), (EXAMPLE_2, 19), (EXAMPLE_3, 226)]
MORE_PATHS = [(EXAMPLE_1, 36), (EXAMPLE_2, 103), (EXAMPLE_3, 3509)]


@pytest.mark.parametrize("data,n_paths", N_PATHS)
def test_find_paths(data, n_paths):
    rooms = parse_map(data)
    paths = list(find_paths(rooms))
    assert len(paths) == n_paths


@pytest.mark.parametrize("data,n_paths", MORE_PATHS)
def test_find_more_paths(data, n_paths):
    rooms = parse_map(data)
    assert count_more_paths(rooms) == n_paths
