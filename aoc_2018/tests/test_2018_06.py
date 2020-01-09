from aoc_2018.day_06 import main


EXAMPLE = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""".lstrip()

def test_day_06():
    assert tuple(main(EXAMPLE, safe_total=32)) == (17, 16)
