from aoc_2019.day_03 import move, Point, path, intersections, part_1, part_2

def test_move():
    assert list(move(Point(0, 0), "U1")) == [(0, 1)]
    assert list(move(Point(3, 0), "L3")) == [(2, 0), (1, 0), (0, 0)]

def test_path():
    assert list(path(["U1", "R1", "D1", "L1"])) == [(0, 1), (1, 1), (1, 0), (0, 0)]

def test_intersections():
    w1, w2 = ["R8", "U5", "L5", "D3"], ["U7", "R6", "D4", "L4"]
    assert intersections(w1, w2) == {(3, 3), (6, 5)}

ex1 = ["R8,U5,L5,D3", "U7,R6,D4,L4"]
ex2 = ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]
ex3 = ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]

def test_part_1():
    assert part_1(ex1) == 6
    assert part_1(ex2) == 159
    assert part_1(ex3) == 135

def test_part_2():
    assert part_2(ex1) == 30
    assert part_2(ex2) == 610
    assert part_2(ex3) == 410
