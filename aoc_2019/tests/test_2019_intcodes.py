from operator import eq, lt
import pytest
from aoc_2019.intcode import CodeRunner


def test_add():
    runner = CodeRunner([1, 0, 0, 0, 99])
    runner.run_full()
    assert runner.code == [2, 0, 0, 0, 99]


def test_mul():
    runner = CodeRunner([2, 0, 0, 0, 99])
    runner.run_full()
    assert runner.code == [4, 0, 0, 0, 99]


def test_immediate_mode():
    runner = CodeRunner([1102, 71, 3, 9, 101, -1, 9, 9, 99, 0])
    runner.run_full()
    assert runner.code[-1] == 212

    # Test 2: This program should terminate normally
    runner = CodeRunner([1101, 100, -1, 4, 0])
    runner.run_full()


comparison_tests = [
    ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], eq),
    ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], lt),
    ([3, 3, 1108, -1, 8, 3, 4, 3, 99], eq),
    ([3, 3, 1107, -1, 8, 3, 4, 3, 99], lt),
]


@pytest.mark.parametrize("code,comp", comparison_tests)
@pytest.mark.parametrize("val", [7, 8])
def test_comparison(code, comp, val):
    runner = CodeRunner(code)
    runner.send(val)
    assert next(runner) == comp(val, 8)


jump_tests = [
    [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
    [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1],
]


@pytest.mark.parametrize("code", jump_tests)
@pytest.mark.parametrize("val", [0, 20])
def test_jump(code, val):
    runner = CodeRunner(code)
    runner.send(val)
    assert next(runner) == bool(val)


complex_jumps = [
    3,
    21,
    1008,
    21,
    8,
    20,
    1005,
    20,
    22,
    107,
    8,
    21,
    20,
    1006,
    20,
    31,
    1106,
    0,
    36,
    98,
    0,
    0,
    1002,
    21,
    125,
    20,
    4,
    20,
    1105,
    1,
    46,
    104,
    999,
    1105,
    1,
    46,
    1101,
    1000,
    1,
    20,
    4,
    20,
    1105,
    1,
    46,
    98,
    99,
]


@pytest.mark.parametrize("val,out", [(7, 999), (8, 1000), (9, 1001)])
def test_complex_jumps(val, out):
    runner = CodeRunner(complex_jumps)
    runner.send(val)
    assert next(runner) == out


def test_pos_0_after_run():
    code = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    runner = CodeRunner(code)
    runner.run_full()
    assert runner.code == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]


def test_relative_base():
    code = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    runner = CodeRunner(code)
    assert list(runner) == code


def test_large_ints():
    runner = CodeRunner([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
    assert next(runner) == 1219070632396864

    runner = CodeRunner([104, 1125899906842624, 99])
    assert next(runner) == 1125899906842624
