from aoc_2019.intcode import read_program, CodeRunner

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

if __name__ == '__main__':
    from libaoc import simple_main
    simple_main(2019, 5, read_program, run_diagnostic, run_thermals)
