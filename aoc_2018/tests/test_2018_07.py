from aoc_2018.day_07 import multi_run


EXAMPLE = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".strip().splitlines()


def test_multi_run():
    assert multi_run(EXAMPLE, workers=2, delay=0) == 15
