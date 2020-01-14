from heapq import heappush, heappop
from typing import Tuple
import numpy as np


def build_map(depth: int, target: Tuple[int, int]):
    tx, ty = target
    level_zero = depth % 20183

    levels = np.array([[level_zero]], dtype=int)
    levels = expand_area(levels, depth, target)
    levels[tx, ty] = level_zero
    return levels


def parse_input(data: str):
    l1, l2 = data.splitlines()
    depth = int(l1[7:])
    x, y = map(int, l2[8:].split(","))
    return depth, (x, y)


def risk_score(levels, target):
    x, y = target
    return np.sum((levels % 3)[:x+1, :y+1])


def expand_area(levels, depth, position):
    px, py = position
    mx, my = levels.shape
    if px < mx and py < my:
        return levels

    nx, ny, ne = 16807, 48271, 20183

    if px >= mx:
        new_levels = np.zeros((px+1, my))
        new_levels[:mx, :] = levels
        levels = new_levels

        for x in range(mx, px + 1):
            levels[x, 0] = (x * nx + depth) % ne
            for y in range(1, my):
                levels[x, y] = (levels[x - 1, y] * levels[x, y - 1] + depth) % ne
        mx = px + 1

    if py >= my:
        new_levels = np.zeros((mx, py + 1), dtype=int)
        new_levels[:, :my] = levels
        levels = new_levels

        for y in range(my, py + 1):
            levels[0, y] = (y * ny + depth) % ne
            for x in range(1, mx):
                levels[x, y] = (levels[x - 1, y] * levels[x, y - 1] + depth) % ne

    return levels


def shortest_hike(levels, depth: int, target: Tuple[int, int]):
    torch, gear, neither = 1, 2, 4
    supported_equipment = {
        0: torch | gear,
        1: gear | neither,
        2: torch | neither,
    }

    tx, ty = target
    sx, sy = levels.shape

    def get_terrain(x, y):
        nonlocal levels, sx, sy
        if x >= sx or y >= sy:
            levels = expand_area(levels, depth, (x, y))
            sx, sy = levels.shape
        return levels[x, y] % 3

    def can_move_to(equipped, x, y):
        terrain = get_terrain(x, y)
        return bool(supported_equipment[terrain] & equipped)

    def next_states(time: int, equipped: int, x: int, y: int):
        cur_terrain = get_terrain(x, y)

        # Move
        new_time = time + 1
        for nx, ny in [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]:
            if nx >= 0 and ny >= 0 and can_move_to(equipped, nx, ny):
                yield new_time, (equipped, nx, ny)

        # Gear switch
        other_gear = supported_equipment[cur_terrain] - equipped
        yield time + 7, (other_gear, x, y)

    start = (torch, 0, 0)
    end = (torch, *target)
    dist = abs(tx) + abs(ty)
    frontier, visited = [(dist, 0, start)], {start: 0}

    while frontier:
        _, _time, _state = heappop(frontier)
        if _state == end:
            return _time
        for n_time, n_state in next_states(_time, *_state):
            if n_state in visited and visited[n_state] <= n_time:
                continue
            visited[n_state] = n_time
            heuristic = n_time + abs(tx - n_state[1]) + abs(ty - n_state[2])
            heappush(frontier, (heuristic, n_time, n_state))


def main(data: str):
    depth, target = parse_input(data)
    levels = build_map(depth, target)
    yield risk_score(levels, target)
    yield shortest_hike(levels, depth, target)
