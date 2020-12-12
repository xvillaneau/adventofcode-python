from typing import List

from libaoc.vectors import StaticWalker, Direction, Vect2D

DIRS = {
    'N': Direction.Up, 'E': Direction.Right,
    'S': Direction.Down, 'W': Direction.Left,
}


def move_ship(instructions: List[str]) -> Vect2D:
    state = StaticWalker(Vect2D(0, 0), Direction.Right)
    for instr in instructions:
        val = int(instr[1:])
        instr = instr[0]

        if instr == 'F':
            state = state.move(val)
        elif instr == 'L':
            while val > 0:
                state = state.rot_left()
                val -= 90
        elif instr == 'R':
            while val > 0:
                state = state.rot_right()
                val -= 90
        else:
            state = state.move(val, DIRS[instr])

    return state.pos


def move_with_waypoint(instructions: List[str]) -> Vect2D:
    ship, waypoint = Vect2D(0, 0), Vect2D(10, 1)

    for instr in instructions:
        val = int(instr[1:])
        instr = instr[0]

        if instr == 'F':
            ship += waypoint * val
        elif instr == 'L':
            while val > 0:
                waypoint = waypoint.rot_left()
                val -= 90
        elif instr == 'R':
            while val > 0:
                waypoint = waypoint.rot_right()
                val -= 90
        else:
            waypoint += DIRS[instr].vector * val

    return ship


def main(data: str):
    instr = data.splitlines()
    yield abs(move_ship(instr))
    yield abs(move_with_waypoint(instr))
