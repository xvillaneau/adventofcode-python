import pytest
from aoc_2016.day_17 import navigate_maze, exhaust_maze

def test_navigate_maze():
    assert navigate_maze("ihgpwlah") == "DDRRRD"
    assert navigate_maze("kglvqrro") == "DDUDRLRRUDRD"
    assert navigate_maze("ulqzkmiv") == "DRURDRUDDLLDLUURRDULRLDUUDDDRR"
    with pytest.raises(RuntimeError):
        navigate_maze("hijkl")

def test_exhaust_maze():
    assert exhaust_maze("ihgpwlah") == 370
    assert exhaust_maze("kglvqrro") == 492
    assert exhaust_maze("ulqzkmiv") == 830
    with pytest.raises(RuntimeError):
        exhaust_maze("hijkl")
