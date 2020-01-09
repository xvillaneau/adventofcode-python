from aoc_2015.day_05 import is_nice, is_nicer


def test_is_nice():
    assert is_nice("ugknbfddgicrmopn")
    assert is_nice("aaa")
    assert not is_nice("jchzalrnumimnmhp")
    assert not is_nice("haegwjzuvuyypxyu")
    assert not is_nice("dvszwmarrgswjxmb")


def test_is_nicer():
    assert is_nicer("qjhvhtzxzqqjkmpb")
    assert is_nicer("xxyxx")
    assert not is_nicer("uurcxstgmygtbstg")
    assert not is_nicer("ieodomkazucvgmuy")
