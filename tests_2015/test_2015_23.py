from aoc_2015.day_23 import run

example = """
inc a
jio a, +2
tpl a
inc a
""".strip().splitlines()

def test_run():
    regs = run(example)
    assert regs.a == 2
    assert regs.b == 0
