
from string import ascii_lowercase
from libaoc import files, simple_main


def reduce(polymer: str, ignored=frozenset([])):
    stack = []
    for c in polymer:
        if c in ignored:
            continue
        if not stack:
            stack.append(c)
            continue
        if c.lower() == stack[-1].lower() and c != stack[-1]:
            stack.pop()
        else:
            stack.append(c)
    return len(stack)


def remove_and_reduce(polymer: str):
    return min(reduce(polymer, frozenset([c, c.upper()])) for c in ascii_lowercase)


if __name__ == '__main__':
    simple_main(2018, 5, files.read_full, reduce, remove_and_reduce)
