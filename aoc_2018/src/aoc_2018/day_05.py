from string import ascii_lowercase


def reduce(polymer: str, ignored=""):
    stack = []
    for char in polymer:
        if char in ignored:
            continue
        n = ord(char)
        if stack and n ^ 32 == stack[-1]:
            stack.pop()
        else:
            stack.append(n)
    return len(stack)


def remove_and_reduce(polymer: str):
    return min(reduce(polymer, c + c.upper()) for c in ascii_lowercase)


def main(data):
    yield reduce(data)
    yield remove_and_reduce(data)
