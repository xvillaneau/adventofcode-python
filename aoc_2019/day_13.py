from aoc_2019.intcode import read_program, CodeRunner, EndProgram, InputInterrupt

from libaoc.vectors import Vect2D


TILES = {
    0: " ",
    1: "#",
    2: "%",
    3: "-",
    4: "o",
}


def get_tiles(code):
    runner = CodeRunner(code)
    tiles = {}
    while True:
        try:
            x = next(runner)
            y = next(runner)
            tile = TILES[next(runner)]
        except EndProgram:
            break
        tiles[Vect2D(x, y)] = tile
    return tiles


def part_1(code):
    tiles = get_tiles(code)
    return sum(t == "%" for t in tiles.values())


def part_2(code):
    runner = CodeRunner(code)
    runner.code[0] = 2
    score, ball_x, paddle_x = 0, 0, 0
    while True:
        try:
            x, y, c = next(runner), next(runner), next(runner)
            if (x, y) == (-1, 0):
                score = c
            elif c == 3:
                paddle_x = x
            elif c == 4:
                ball_x = x
        except InputInterrupt:
            delta = ball_x - paddle_x
            joystick = (delta > 0) - (delta < 0)
            runner.send(joystick)
        except EndProgram:
            break
    return score


if __name__ == '__main__':
    from libaoc import simple_main
    simple_main(2019, 13, read_program, part_1, part_2)
