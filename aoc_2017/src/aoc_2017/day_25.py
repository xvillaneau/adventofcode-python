from collections import defaultdict
from typing import Dict, Tuple
from parsimonious import Grammar

GRAMMAR = Grammar(r"""
program      = init state+ _
init         = begin_state step_count
state        = state_head state_branch state_branch
state_branch = branch_value branch_write branch_move branch_next

begin_state  = _ "Begin in state " STATE "."
step_count   = _ "Perform a diagnostic checksum after " NUMBER " steps."
state_head   = _ "In state " STATE ":"
branch_value = _ "If the current value is " VALUE ":"
branch_write = _ "- Write the value " VALUE "."
branch_move  = _ "- Move one slot to the " DIRECTION "."
branch_next  = _ "- Continue with state " STATE "."

_            = ~"\s+"
STATE        = ~"[A-Z]"
NUMBER       = ~"[0-9]+"
VALUE        = "0" / "1"
DIRECTION    = "left" / "right"
""")

Value = bool
Move = int
Pointer = int
StateName = str
Countdown = int
Action = Tuple[Value, Move, StateName]
State = Tuple[Action, Action]
States = Dict[StateName, State]
Progress = Tuple[Pointer, StateName, Countdown]
Program = Tuple[Progress, States]
Tape = Dict[int, Value]


def read_program(verbose_program: str) -> Program:
    tree = GRAMMAR.parse(verbose_program)

    def _get_text(subtree, nth):
        return subtree.children[nth].children[2].text

    def _get_int(subtree, nth):
        return int(_get_text(subtree, nth))

    def _get_bool(subtree, nth):
        return bool(_get_int(subtree, nth))

    def _get_dir(subtree, nth):
        return -1 if _get_text(subtree, nth) == "left" else 1

    def _read_action(act_tree) -> Tuple[Value, Action]:
        value = _get_bool(act_tree, 0)
        write = _get_bool(act_tree, 1)
        move = _get_dir(act_tree, 2)
        state = _get_text(act_tree, 3)
        return value, (write, move, state)

    def _read_state(state_tree) -> Tuple[StateName, State]:
        name = _get_text(state_tree, 0)

        v_a, act_a = _read_action(state_tree.children[1])
        v_b, act_b = _read_action(state_tree.children[2])
        assert v_a != v_b
        acts = (act_a, act_b) if v_b else (act_b, act_a)

        return name, acts

    init = tree.children[0]
    begin_state = _get_text(init, 0)
    begin_count = _get_int(init, 1)
    begin_progress = (0, begin_state, begin_count)

    state_trees = tree.children[1].children
    states = dict(_read_state(s) for s in state_trees)
    return begin_progress, states


def step(program: Program, status: Progress, tape: Tape) -> Progress:

    pos, state, count = status
    act_0, act_1 = program[1][state]
    write, move, new_state = act_1 if tape[pos] else act_0

    tape[pos] = write
    return pos + move, new_state, count - 1


def run(program: Program) -> Tape:

    tape = defaultdict(bool)
    pointer = program[0]

    while pointer[2] > 0:
        pointer = step(program, pointer, tape)

    return tape


def main(data):
    program = read_program(data)
    tape = run(program)
    yield sum(tape.values())
