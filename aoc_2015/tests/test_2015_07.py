from aoc_2015.day_07 import Gates

EXAMPLE = """
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
123 -> x
456 -> y
""".strip()

VALUES = {
    "d": 72,
    "e": 507,
    "f": 492,
    "g": 114,
    "h": 65412,
    "i": 65079,
    "x": 123,
    "y": 456,
}


def test_connect_wires():
    gates = Gates(EXAMPLE.splitlines())
    for wire, value in VALUES.items():
        assert gates[wire] == value
