from aoc_2021.day_04 import parse_input, run_board, get_rows_cols, run_game

EXAMPLE = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""".strip()


def test_parse_input():
    draw, boards = parse_input(EXAMPLE)
    assert draw[:5] == [7, 4, 9, 5, 11]
    assert len(boards) == 3
    assert all(boards[0][0] == [22, 13, 17, 11, 0])
    assert all(boards[1][2] == [19, 8, 7, 25, 23])
    assert all(boards[2][4] == [2, 0, 12, 3, 7])


def test_get_rows_cols():
    _, boards = parse_input(EXAMPLE)
    rows_cols = get_rows_cols(boards[0])
    assert len(rows_cols) == 10
    assert rows_cols[0] == {22, 13, 17, 11, 0}
    assert rows_cols[4] == {1, 12, 20, 15, 19}
    assert rows_cols[5] == {22, 8, 21, 6, 1}
    assert rows_cols[9] == {0, 24, 7, 5, 19}


def test_run_board():
    draw, boards = parse_input(EXAMPLE)
    rounds, score = run_board(draw, boards[2])
    assert rounds == 12
    assert score == 4512

def test_run_game():
    draw, boards = parse_input(EXAMPLE)
    scores = run_game(draw, boards)
    assert scores[0] == 4512
    assert scores[-1] == 1924
