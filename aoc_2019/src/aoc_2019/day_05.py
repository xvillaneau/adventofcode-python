from libaoc import BaseRunner
from .intcode import CodeRunner


def run_diagnostic(code):
    runner = CodeRunner(code)
    runner.send(1)
    diagnostic = list(runner)
    assert all(n == 0 for n in diagnostic[:-1])
    return diagnostic[-1]


def run_thermals(code):
    runner = CodeRunner(code)
    runner.send(5)
    return next(runner)


class AocRunner(BaseRunner):
    year = 2019
    day = 5
    parser = BaseRunner.int_list_parser(",")

    def run(self, data):
        yield run_diagnostic(data)
        yield run_thermals(data)
