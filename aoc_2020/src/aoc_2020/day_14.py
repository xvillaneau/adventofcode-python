import re

MEM_MAX = (1 << 36) - 1


def parse_mask(mask: str):
    mask_0 = int(mask.replace("X", "1"), base=2)
    mask_1 = int(mask.replace("X", "0"), base=2)
    return mask_0, mask_1


def run_program(program):
    mask_0 = (1 << 36) - 1
    mask_1 = 0
    memory = {}

    for line in program:
        if line.startswith('mask = '):
            mask_0, mask_1 = parse_mask(line[7:])
        else:
            addr, val = re.match(r'^mem\[(\d+)] = (\d+)$', line).groups()
            memory[int(addr)] = (int(val) & mask_0) | mask_1

    return memory


def parse_mask_v2(mask: str):
    mask_1 = int(mask.replace("X", "0"), base=2)
    mask_x = int(mask.replace("1", "0").replace("X", "1"), base=2)

    floating, mask, power = [0], mask_x, 1
    while mask:
        if mask & 1:
            floating.extend([n | power for n in floating])
        mask >>= 1
        power <<= 1

    return mask_1, MEM_MAX - mask_x, floating


def run_program_v2(program):
    mask_1, mask_x, floating = 0, MEM_MAX, []
    memory = {}

    for line in program:
        if line.startswith('mask = '):
            mask_1, mask_x, floating = parse_mask_v2(line[7:])
        else:
            addr, val = re.match(r'^mem\[(\d+)] = (\d+)$', line).groups()
            addr, val = (int(addr) | mask_1) & mask_x, int(val)
            for n in floating:
                memory[addr | n] = val

    return memory


def main(data: str):
    program = data.splitlines()
    yield sum(run_program(program).values())
    yield sum(run_program_v2(program).values())
