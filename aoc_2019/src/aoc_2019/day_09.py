from .intcode import CodeRunner, parse_intcode


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


def main(data: str):
    code = parse_intcode(data)
    yield run_diagnostic(code)
    yield run_boost(code)
