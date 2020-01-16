from typing import List

from libaoc.parsers import parse_integer_list


def trampolines(instructions: List[int]):
    stack = instructions.copy()
    i, n, end = 0, 0, len(stack)

    while 0 <= i < end:
        n += 1
        jump = stack[i]
        stack[i] += 1
        i += jump

    return n


def weird_trampolines(instructions: List[int]):
    stack = instructions.copy()
    i, n, end = 0, 0, len(stack)

    while 0 <= i < end:
        n += 1
        jump = stack[i]
        stack[i] += -1 if jump >= 3 else 1
        i += jump

    return n


def main(data: str):
    jumps = parse_integer_list(data)
    yield trampolines(jumps)
    yield weird_trampolines(jumps)
