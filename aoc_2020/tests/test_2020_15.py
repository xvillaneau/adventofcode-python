from aoc_2020.day_15 import memory_game


def test_memory_game():
    example = [0, 3, 6]
    first_16 = [memory_game(example, n + 1) for n in range(16)]
    assert first_16 == [0, 3, 6, 0, 3, 3, 1, 0, 4, 0, 2, 0, 2, 2, 1, 8]

    assert memory_game(example, 30_000_000) == 175594
