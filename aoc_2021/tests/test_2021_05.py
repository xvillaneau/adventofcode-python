from aoc_2021.day_05 import parse_data, make_matrix, locate_vents, count_overlaps

EXAMPLE = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".strip()


def test_parse_data():
    lines = parse_data(EXAMPLE)
    assert len(lines) == 10
    assert lines[0] == ((0, 9), (5, 9))
    assert lines[4] == ((7, 0), (7, 4))
    assert lines[8] == ((0, 0), (8, 8))


def test_make_matrix():
    mat, offset = make_matrix([((2, 10), (8, 3))])
    assert mat.shape == (7, 8)
    assert offset == (2, 3)


def test_locate_vents():
    lines = parse_data(EXAMPLE)
    field_hv, field_dg = locate_vents(lines)

    assert field_hv.shape == (10, 10)
    assert all(field_hv[7, :] == [1, 1, 1, 1, 2, 0, 0, 0, 0, 0])
    assert all(field_hv[:, 9] == [2, 2, 2, 1, 1, 1, 0, 0, 0, 0])

    field = field_hv + field_dg
    assert all(field[7, :] == [1, 2, 1, 2, 2, 0, 0, 1, 0, 0])
    assert all(field[:, 4] == [0, 1, 1, 2, 3, 1, 3, 2, 1, 1])


def test_count_overlaps():
    lines = parse_data(EXAMPLE)
    field_hv, field_dg = locate_vents(lines)
    assert count_overlaps(field_hv) == 5
    assert count_overlaps(field_hv + field_dg) == 12

