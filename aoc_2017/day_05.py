from typing import List


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


if __name__ == '__main__':
    from libaoc import simple_main, files
    simple_main(2017, 5, files.read_int_list, trampolines, weird_trampolines)
