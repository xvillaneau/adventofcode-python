from collections import Callable
from math import prod
from operator import add, mul
from typing import TypeVar

Op = Callable[[int, int], int]
T = TypeVar("T")


def computer(
        init: T,
        step: Callable[[Op, T, int], T],
        final: Callable[[T], int],
) -> Callable[[str], int]:

    def _computer(operation: str) -> int:
        return _compute(list(reversed(operation.replace(" ", ""))))

    def _compute(stack: list[str]) -> int:
        state, op = init, (lambda _, y: y)

        while stack:
            char = stack.pop()
            if char in '+*':
                op = add if char == '+' else mul
            elif char == ')':
                break
            else:
                val = _compute(stack) if char == '(' else int(char)
                state = step(op, state, val)

        return final(state)

    return _computer


compute_1 = computer(0, lambda op, head, new: op(head, new), lambda x: x)


def step_2(op, state, new):
    add_val, mul_val = state
    if op is not mul:
        add_val = op(add_val, new)
    else:
        mul_val *= add_val
        add_val = new
    return add_val, mul_val


compute_2 = computer((0, 1), step_2, prod)


def main(data: str):
    yield sum(compute_1(op) for op in data.splitlines())
    yield sum(compute_2(op) for op in data.splitlines())
