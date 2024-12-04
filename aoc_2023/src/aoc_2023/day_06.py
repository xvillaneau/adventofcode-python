import math


def ways_to_win(time: int, distance: int) -> int:
    # If x is the press duration, and T the time limit,
    # then the race distance d is:  d = x * (T - x)
    # We want to achieve a distance D so we want to solve:
    #  x² - T.x + D = 0
    delta = time*time - 4 * (distance + 1)
    x_min = math.ceil((time - math.sqrt(delta)) / 2.)
    return time - 2 * x_min + 1


def parse_input(data: str):
    lines = data.strip().splitlines()
    assert len(lines) == 2
    return lines[0].split()[1:], lines[1].split()[1:]


def parse_single(data: str):
    lines = data.strip().splitlines()
    assert len(lines) == 2
    _, _, lnt = lines[0].partition(":")
    _, _, lnd = lines[1].partition(":")
    time = int(lnt.replace(" ", ""))
    distance = int(lnd.replace(" ", ""))
    return time, distance


def main(data: str):
    times, distances = parse_input(data)
    yield math.prod(ways_to_win(int(t), int(d)) for t, d in zip(times, distances))
    yield ways_to_win(int(''.join(times)), int(''.join(distances)))
