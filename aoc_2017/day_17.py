
from typing import List, Tuple

Buffer = List[int]


def circular_step(buffer: Buffer, pos: int, step: int) -> Tuple[Buffer, int]:
    new_val = len(buffer)
    new_pos = 1 + (pos + step) % new_val
    new_buff = buffer.copy()
    new_buff.insert(new_pos, new_val)
    return new_buff, new_pos


def circular_buff(step: int, lim: int = 2017) -> Buffer:
    buffer = [0]
    pos = 0

    for _ in range(lim + 1):
        buffer, pos = circular_step(buffer, pos, step)

    return buffer


def next_circular(step: int, lim: int = 2017) -> int:
    buffer = circular_buff(step, lim)
    pos = buffer.index(lim)
    return buffer[(pos + 1) % (lim + 1)]


def second_circular(step: int, lim: int = 50_000_000) -> int:
    second, pos = 0, 0
    for i in range(lim + 1):
        pos = 1 + (pos + step) % (i + 1)
        if pos == 1:
            second = i + 1
    return second


if __name__ == '__main__':
    from libaoc import static_input, simple_main
    simple_main(2017, 17, static_input(312), next_circular, second_circular)
