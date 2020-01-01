from collections import defaultdict

from libaoc.vectors import Walker2D, Direction, Vect2D
from .intcode import CodeRunner, EndProgram, parse_intcode


def run_robot(code, start_color=0):
    computer = CodeRunner(code)
    robot = Walker2D(0, 0, Direction.Up)
    colors = defaultdict(int)
    colors[Vect2D(0, 0)] = start_color
    painted = set()

    while True:
        try:
            computer.send(colors[robot.pos])
            new_color = next(computer)
            direction = next(computer)
        except EndProgram:
            break
        colors[robot.pos] = new_color
        painted.add(robot.pos)
        if direction:
            robot.rot_right()
        else:
            robot.rot_left()
        robot.move()

    return colors, painted


def part_1(code):
    return len(run_robot(code)[1])


def part_2(code):
    colors, _ = run_robot(code, 1)

    min_x = min(v.x for v in colors)
    max_x = max(v.x for v in colors)
    min_y = min(v.y for v in colors)
    max_y = max(v.y for v in colors)

    out = "\n"
    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            out += "#" if colors[(x, y)] else " "
        out += "\n"

    return out


def main(data: str):
    code = parse_intcode(data)
    yield part_1(code)
    yield part_2(code)
