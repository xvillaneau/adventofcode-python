from aoc_2021.day_23 import smallest_cost, load_init, candidate_moves, apply_move

EXAMPLE = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""


def test_load_init():
    assert load_init(EXAMPLE) == (
        "", "", "AB", "", "DC", "", "CB", "", "AD", "", ""
    )


def test_candidate_moves():
    state0 = load_init(EXAMPLE)
    moves0 = set(candidate_moves(state0))
    pos = [0, 1, 3, 5, 7, 9, 10]
    assert moves0 == {
        *(("B", 2, i) for i in pos),
        *(("C", 4, i) for i in pos),
        *(("B", 6, i) for i in pos),
        *(("D", 8, i) for i in pos),
    }

    state1, _ = apply_move(state0, "B", 6, 3)
    moves1 = set(candidate_moves(state1))
    assert ("C", 4, 6) in moves1
    assert ("B", 2, 5) not in moves1
    assert ("B", 2, 4) not in moves1
    assert ("D", 8, 1) not in moves1


def test_apply_move_out():
    state0 = load_init(EXAMPLE)
    state1, cost = apply_move(state0, "B", 6, 3)
    assert state1 == ("", "", "AB", "B", "DC", "", "C", "", "AD", "", "")
    assert cost == 40


def test_apply_move_direct():
    state0 = load_init(EXAMPLE)
    state1, _ = apply_move(state0, "B", 6, 3)
    state2, cost = apply_move(state1, "C", 4, 6)
    assert state2 == ("", "", "AB", "B", "D", "", "CC", "", "AD", "", "")
    assert cost == 400


def test_smallest_cost():
    assert smallest_cost(EXAMPLE) == 12521


def test_smallest_cost_part_2():
    assert smallest_cost(EXAMPLE, part_2=True) == 44169

