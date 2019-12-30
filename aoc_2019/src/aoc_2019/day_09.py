from libaoc import BaseRunner
from .intcode import CodeRunner


def run_diagnostic(code):
    runner = CodeRunner(code)
    runner.send(1)
    output = list(runner)
    assert len(output) == 1, f"Got output: {output}"
    return output[0]


def run_boost(code):
    runner = CodeRunner(code)
    runner.send(2)
    return next(runner)


class AocRunner(BaseRunner):
    year = 2019
    day = 9
    parser = BaseRunner.int_list_parser(",")

    def run(self, code):
        yield run_diagnostic(code)
        yield run_boost(code)
