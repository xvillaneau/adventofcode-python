import pytest

from aoc_2021.day_18 import parse_num, add_nums, do_homework, magnitude, largest_sum

PARSE_EXAMPLES = [
    "[1,2]",
    "[[1,2],3]",
    "[9,[8,7]]",
    "[[1,9],[8,5]]",
    "[[[[1,2],[3,4]],[[5,6],[7,8]]],9]",
    "[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]",
    "[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]",
]


@pytest.mark.parametrize("example", PARSE_EXAMPLES)
def test_parse_num(example):
    parse_num(example)


def test_add_nums():
    num_a = parse_num("[[[[4,3],4],4],[7,[[8,4],9]]]")
    num_b = parse_num("[1,1]")
    res = add_nums(num_a, num_b)
    assert res == parse_num("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")


HOMEWORK_1 = """
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
"""
HOMEWORK_2 = """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""
HOMEWORK = [
    (HOMEWORK_1, "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"),
    (HOMEWORK_2, "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]")
]


@pytest.mark.parametrize("homework,solution", HOMEWORK)
def test_do_homework(homework, solution):
    homework = [parse_num(ln) for ln in homework.strip().splitlines()]
    assert do_homework(homework) == parse_num(solution)


def test_magnitude():
    num = parse_num("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]")
    assert magnitude(num) == 4140


def test_largest_sum():
    homework = [parse_num(ln) for ln in HOMEWORK_2.strip().splitlines()]
    assert largest_sum(homework) == 3993
