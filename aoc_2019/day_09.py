from aoc_2019.intcode import CodeRunner, read_program

def run_diagnostic(code):
    runner = CodeRunner(code)
    runner.send(1)
    output = list(runner)
    assert len(output) == 1, f"Got output: {output}"
    return output[0]

def run_boost(code):
    runner = CodeRunner(code)
    runner.send(2)
    output = list(runner)
    assert len(output) == 1, f"Got output: {output}"
    return output[0]

if __name__ == '__main__':
    from libaoc import simple_main
    simple_main(2019, 9, read_program, run_diagnostic, run_boost)
