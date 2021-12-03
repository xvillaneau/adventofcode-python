from math import prod


def parse_instr(lines: list[str]) -> list[tuple[str, int]]:
    moves = []
    for line in lines:
        if not (line := line.strip()):
            continue
        mv, n = line.split()
        moves.append((mv, int(n)))
    return moves


def track_sub(moves: list[tuple[str, int]]) -> tuple[int, int]:
    pos, depth = 0, 0
    for move, n in moves:
        if move == "forward":
            pos += n
        elif move == "down":
            depth += n
        elif move == "up":
            depth -= n
    return pos, depth


def track_aim(moves: list[tuple[str, int]]) -> tuple[int, int]:
    pos, depth, aim = 0, 0, 0
    for move, n in moves:
        if move == "forward":
            pos += n
            depth += n * aim
        elif move == "down":
            aim += n
        elif move == "up":
            aim -= n
    return pos, depth


def main(data: str):
    moves = parse_instr(data.splitlines())
    yield prod(track_sub(moves))
    yield prod(track_aim(moves))
