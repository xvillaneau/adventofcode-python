from aoc_2020.day_02 import main, password_valid_1, password_valid_2


def test_password_valid_1():
    assert password_valid_1('a', 1, 3, 'abcde')
    assert not password_valid_1('b', 1, 3, 'cdefg')
    assert password_valid_1('c', 2, 9, 'ccccccccc')


def test_password_valid_2():
    assert password_valid_2('a', 1, 3, 'abcde')
    assert not password_valid_2('b', 1, 3, 'cdefg')
    assert not password_valid_2('c', 2, 9, 'ccccccccc')


EXAMPLE = """
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
""".strip()


def test_main():
    assert tuple(main(EXAMPLE)) == (2, 1)
