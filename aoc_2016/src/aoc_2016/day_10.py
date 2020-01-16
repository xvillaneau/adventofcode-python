from collections import defaultdict
from typing import Set, Union

from parsimonious import Grammar

GRAMMAR = Grammar(r"""
program      = instruction+
instruction  = ( initial / decision ) _?
initial      = "value " NUMBER " goes to " BOT
decision     = BOT " gives low to " receiver " and high to " receiver
receiver     = BOT / OUTPUT

_            = ~"\s+"
BOT          = "bot " NUMBER
OUTPUT       = "output " NUMBER
NUMBER       = ~"[0-9]+"
""")

TEST = """
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
"""


class NumThing:
    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return f'{self.__class__.__name__}({self.num})'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.num == other.num

    def __hash__(self):
        return hash(repr(self))


class Bot(NumThing):
    pass


class Output(NumThing):
    pass


def parse_program(text):
    tree = GRAMMAR.parse(text.strip())

    initial: defaultdict[Bot, Set[int]] = defaultdict(set)
    decisions = {}

    def _bot_num(bot_node):
        return Bot(int(bot_node.children[1].text))

    def _output_num(output_node):
        return Output(int(output_node.children[1].text))

    def _receiver(node):
        sub_node = node.children[0]
        name = sub_node.expr_name
        if name == 'BOT':
            return _bot_num(sub_node)
        elif name == 'OUTPUT':
            return _output_num(sub_node)
        else:
            raise ValueError(f"Unknown node {name}")

    for child in tree.children:
        instruction = child.children[0].children[0]
        if instruction.expr_name == 'initial':
            value = int(instruction.children[1].text)
            bot = _bot_num(instruction.children[3])
            initial[bot].add(value)
        elif instruction.expr_name == 'decision':
            bot = _bot_num(instruction.children[0])
            low = _receiver(instruction.children[2])
            high = _receiver(instruction.children[4])
            decisions[bot] = (low, high)

    return initial, decisions


def find_handler(program_text, find_chips: Set[int]):
    state, instructions = parse_program(program_text)
    outputs: defaultdict[Output, Set[int]] = defaultdict(set)

    def _handle_val(receiver: Union[Bot, Output], val: int):
        if isinstance(receiver, Bot):
            state[receiver].add(val)
        else:
            outputs[receiver].add(val)

    while True:
        if any(len(c) > 2 for c in state.values()):
            raise ValueError(f"There are bots with more than two chips: {state}")
        try:
            bot, chips = next((b, c) for b, c in state.items() if len(c) == 2)
        except StopIteration:
            return outputs
        if find_chips and chips == find_chips:
            return bot
        low_chip, high_chip = sorted(chips)
        low_receive, high_receive = instructions[bot]
        state[bot] = set([])
        _handle_val(low_receive, low_chip)
        _handle_val(high_receive, high_chip)


def mul_outputs(program_txt):
    outputs = find_handler(program_txt, find_chips=set([]))
    return outputs[Output(0)].pop() * outputs[Output(1)].pop() * outputs[Output(2)].pop()


def main(data: str):
    yield find_handler(data, {17, 61})
    yield mul_outputs(data)
