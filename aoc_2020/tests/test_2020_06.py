from aoc_2020.day_06 import group_any_answer, group_all_answers

EXAMPLE = """
abc

a
b
c

ab
ac

a
a
a
a

b
""".strip().splitlines()


def test_group_any_answer():
    assert group_any_answer(EXAMPLE) == ['abc', 'abc', 'abc', 'a', 'b']


def test_group_all_answers():
    assert group_all_answers(EXAMPLE) == ['abc', '', 'a', 'a', 'b']
