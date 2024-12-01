import copy
import functools


def parse_packet(data: str):
    # TODO: Try to make a real parser, this is lazy and bad practice
    return eval(data)


def parse_input(data: str):
    pairs_str = (
        pair.splitlines()
        for pair in data.strip().split("\n\n")
    )
    return [
        (parse_packet(left), parse_packet(right))
        for left, right in pairs_str
    ]


def compare(left, right):
    """
    Checks the order of two packets. Returns a negative value if the order is correct,
    positive if not, 0 if the packets are equal. It is recursive.
    """
    left = copy.copy(left)
    right = copy.copy(right)

    while len(left) > 0 and len(right) > 0:
        l0, r0 = left.pop(0), right.pop(0)
        res = CMP[(type(l0), type(r0))](l0, r0)
        if res != 0:
            return res

    return len(left) - len(right)


CMP = {
    (int, int): lambda a, b: a - b,
    (list, list): compare,
    (int, list): lambda a, b: compare([a], b),
    (list, int): lambda a, b: compare(a, [b]),
}


def part_1(pairs) -> int:
    in_order = (compare(*p) < 0 for p in pairs)
    return sum(i * r for i, r in enumerate(in_order, start=1))


def part_2(pairs):
    packets = [[[2]], [[6]]]
    # Flatten the list of packets
    for pl, pr in pairs:
        packets.append(pl)
        packets.append(pr)

    # We can convert compare to a key
    packets.sort(key=functools.cmp_to_key(compare))

    d2 = packets.index([[2]]) + 1
    d6 = packets.index([[6]]) + 1
    return d2 * d6

def main(data: str):
    pairs = parse_input(data)
    yield part_1(pairs)
    yield part_2(pairs)
