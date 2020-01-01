from .intcode import CodeRunner, parse_intcode


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


def main(data: str):
    code = parse_intcode(data)
    yield run_diagnostic(code)
    yield run_thermals(code)
