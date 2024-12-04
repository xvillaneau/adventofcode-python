import re

DO = object()
DONT = object()


def parse_mem(mem: str) -> list:
    tokens = []

    while mem:
        if mem[0] not in "md":
            mem = mem[1:]
            continue
        if mem.startswith("do()"):
            tokens.append(DO)
            mem = mem[4:]
            continue
        if mem.startswith("don't()"):
            tokens.append(DONT)
            mem = mem[7:]
            continue
        if mem.startswith("mul("):
            mem = mem[4:]
            if m := re.match(r"(\d+),(\d+)\)", mem):
                a, b = m.groups()
                tokens.append(int(a) * int(b))
                m_len = m.end() - m.start()
                mem = mem[m_len:]
            continue

        mem = mem[1:]

    return tokens


def sum_mul(tokens: list) -> tuple[int, int]:
    full_sum, state_sum = 0, 0
    enabled = True
    for tok in tokens:
        if tok is DO:
            enabled = True
        elif tok is DONT:
            enabled = False
        else:
            full_sum += tok
            if enabled:
                state_sum += tok

    return full_sum, state_sum


def main(data: str):
    pairs = parse_mem(data)
    p1, p2 = sum_mul(pairs)

    yield p1
    yield p2
