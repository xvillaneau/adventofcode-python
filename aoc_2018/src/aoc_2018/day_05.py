
from string import ascii_lowercase


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


def main(data):
    yield reduce(data)
    yield remove_and_reduce(data)
