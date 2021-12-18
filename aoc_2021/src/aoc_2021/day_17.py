import re


def parse_target(data: str) -> tuple[int, int, int, int]:
    x0, x1, y0, y1 = re.fullmatch(
        r"target area: x=(\d+)\.\.(\d+), y=(-\d+)\.\.(-\d+)",
        data.strip()
    ).groups()
    return int(x0), int(x1), int(y0), int(y1)


def target_hit(x0, x1, y0, y1, dx0, dy0) -> bool:
    x, y, dx, dy = 0, 0, dx0, dy0
    while x <= x1 and y >= y0:
        if x >= x0 and y <= y1:
            return True
        x += dx
        y += dy
        dx = max(0, dx - 1)
        dy -= 1
    return False


def count_trajectories(x0: int, x1: int, y0: int, y1: int) -> int:
    assert 0 < x0 < x1
    assert y0 < y1 < 0

    min_dx = 0
    while (min_dx * (min_dx + 1)) // 2 < x0:
        min_dx += 1

    return sum(
        target_hit(x0, x1, y0, y1, dx0, dy0)
        for dy0 in range(y0, -y0)
        for dx0 in range(min_dx, x1 + 1)
    )

def main(data: str):
    x0, x1, y0, y1 = parse_target(data)
    yield y0 * (y0 + 1) // 2
    yield count_trajectories(x0, x1, y0, y1)
