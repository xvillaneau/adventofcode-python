from aoc_2015.day_10 import look_and_say


def test_look_and_say():
    assert look_and_say("1") == "11"
    assert look_and_say("11") == "21"
    assert look_and_say("21") == "1211"
    assert look_and_say("1211") == "111221"
    assert look_and_say("111221") == "312211"
    assert look_and_say("312211") == "13112221"
    assert look_and_say("13112221") == "1113213211"
    assert look_and_say("1113213211") == "31131211131221"
    assert look_and_say("41111") == "1441"
