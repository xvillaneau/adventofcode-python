import re
from typing import List

RE_REINDEER = re.compile(
    r"(\w+) can fly (\d+) km/s for (\d+) seconds, "
    r"but then must rest for (\d+) seconds\."
)

def parse_reindeer(list_reindeer):
    for line in list_reindeer:
        name, speed, t_fly, t_rest = RE_REINDEER.match(line).groups()
        speed, t_fly, t_rest = int(speed), int(t_fly), int(t_rest)
        yield name, speed, t_fly, t_rest

def calc_distance(time: int, speed: int, t_fly: int, t_rest: int):
    t_cycle = t_fly + t_rest
    d_cycle = speed * t_fly
    cycles, rem = divmod(time, t_cycle)
    d_rem = speed * min(rem, t_fly)
    return d_rem + cycles * d_cycle

def max_distance(reindeer: List[str], time=2503):
    return max(
        calc_distance(time, speed, t_fly, t_rest)
        for _, speed, t_fly, t_rest in parse_reindeer(reindeer)
    )

def reindeer_iter(speed: int, t_fly: int, t_rest: int):
    dist = 0
    while True:
        for _ in range(t_fly):
            dist += speed
            yield dist
        for _ in range(t_rest):
            yield dist

def max_points(reindeer: List[str], time=2503):
    reindeer = [
        reindeer_iter(speed, t_fly, t_rest)
        for _, speed, t_fly, t_rest in parse_reindeer(reindeer)
    ]
    points = [0] * len(reindeer)
    for _ in range(time):
        distances = [next(r) for r in reindeer]
        best = max(distances)
        for i, d in enumerate(distances):
            if d == best:
                points[i] += 1

    return max(points)


def main(data: str):
    reindeer = data.splitlines()
    yield max_distance(reindeer)
    yield max_points(reindeer)
