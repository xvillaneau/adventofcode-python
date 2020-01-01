from itertools import permutations, cycle
from string import ascii_uppercase
from typing import List

from .intcode import CodeRunner, parse_intcode


def run_sequence(code: List[int], phase_settings: List[int]):
    signal = 0
    for setting in phase_settings:
        runner = CodeRunner(code)
        runner.send(setting)
        runner.send(signal)
        signal = next(runner)
    return signal


def max_signal(code: List[int], n_amp: int = 5):
    return max(run_sequence(code, settings) for settings in permutations(range(n_amp)))


def run_feedback(code: List[int], phase_settings: List[int]):
    amps = []
    for letter, setting in zip(ascii_uppercase, phase_settings):
        amps.append(CodeRunner(code, name=f"Amp {letter}"))
        amps[-1].send(setting)

    signal = 0
    for amp in cycle(amps):
        try:
            amp.send(signal)
            signal = next(amp)
        except StopIteration:
            return signal


def max_feedback(code):
    return max(run_feedback(code, settings) for settings in permutations(range(5, 10)))


def main(data: str):
    code = parse_intcode(data)
    yield max_signal(code)
    yield max_feedback(code)
