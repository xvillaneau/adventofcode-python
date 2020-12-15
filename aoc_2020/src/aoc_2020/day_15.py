from typing import List


def memory_game(start: List[int], nth: int):
    if nth <= len(start):
        return start[nth - 1]

    l_size = max(start) + 1
    memory = [0] * l_size
    for i, n in enumerate(start[:-1], start=1):
        memory[n] = i

    turn = len(start)
    last = start[-1]

    while turn < nth:
        if (count := memory[last]):
            count = turn - count

        memory[last] = turn
        last = count
        turn += 1

        while last >= l_size:
            # Allocate more space for our memory
            memory.extend([0] * l_size)
            l_size *= 2

    return last


def main(data: str):
    game_start = [int(n) for n in data.split(",")]

    yield memory_game(game_start, 2020)
    yield memory_game(game_start, 30_000_000)
