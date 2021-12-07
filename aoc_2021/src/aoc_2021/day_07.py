
from collections import Callable

from libaoc.parsers import parse_integer_list


def find_low_fuel(
    positions: list[int],
    cost: Callable[[int], int],
    slope: Callable[[int], float],
) -> int:

    def fuel_at(pos):
        return sum(cost(p - pos) for p in positions)

    bot, top = 0, max(positions)
    while top > bot + 1:
        pivot = (top + bot) // 2
        slp = sum(slope(pivot - p) for p in positions)
        if slp >= 0:
            top = pivot
        else:
            bot = pivot

    return min(fuel_at(bot), fuel_at(top))


def find_low_fuel_1(positions: list[int]) -> int:
    def lin_cost(move: int):
        return abs(move)

    def lin_slope(move: int):
        if move == 0:
            return 0
        return -1 if move < 0 else 1

    return find_low_fuel(positions, lin_cost, lin_slope)


def find_low_fuel_2(positions: list[int]) -> int:

    def cumulated_cost(move: int):
        move = abs(move)
        return move * (move + 1) // 2

    def cumulated_slope(move: int):
        return move + 0.5

    return find_low_fuel(positions, cumulated_cost, cumulated_slope)


def main(data: str):
    positions = parse_integer_list(data, ",")
    yield find_low_fuel_1(positions)
    yield find_low_fuel_2(positions)
