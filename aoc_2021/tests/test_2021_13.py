from aoc_2021.day_13 import parse_data, fold_paper, render_points

EXAMPLE = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""


def test_parse():
    points, folds = parse_data(EXAMPLE)
    assert len(points) == 18
    assert folds == [("y", 7), ("x", 5)]


def test_fold_paper():
    points_0, folds = parse_data(EXAMPLE)
    points_1 = fold_paper(points_0, folds[0])
    assert len(points_1) == 17
    points_2 = fold_paper(points_1, folds[1])
    assert len(points_2)


def test_render():
    points, folds = parse_data(EXAMPLE)
    for f in folds:
        points = fold_paper(points, f)
    render = render_points(points)
    assert len(render.splitlines()) == 5
