from collections import deque
from collections.abc import Generator as GeneratorABC
from functools import lru_cache
from typing import Callable, List, Tuple


class EndProgram(StopIteration):
    pass


class InputInterrupt(IOError):
    pass


class OutputInterrupt(IOError):
    pass


class NonAsciiOutput(IOError):
    def __init__(self, data: int):
        super().__init__(data)
        self.data = data


Argument = Tuple[int, int]
POSITION, IMMEDIATE, RELATIVE = 0, 1, 2


class CodeRunner(GeneratorABC):
    __slots__ = ("code", "name", "pointer", "base", "_in_queue", "_out_queue")

    def __init__(self, code: List[int], *, name: str = None):
        self.code = code.copy()
        self.name = name or f"id:{id(self)}"
        self.pointer = 0
        self.base = 0

        self._in_queue = deque()
        self._out_queue = deque()

        # self.log = getLogger(f"intcode.{type(self).__name__}.{self.name}")
        # self.log.setLevel(log_level)
        # self.log.addHandler(StreamHandler())

    def __iter__(self):
        return self

    def __repr__(self):
        if not self.name:
            return super().__repr__()
        return f"<{type(self).__name__} name={self.name!r} pointer={self.pointer}>"

    def copy(self, new_name: str = ""):
        runner = type(self)(self.code.copy(), name=new_name)
        runner.pointer = self.pointer
        runner.base = self.base
        runner._out_queue = self._out_queue.copy()
        runner._in_queue = self._in_queue.copy()
        return runner

    def throw(self, typ=None, val=None, tb=None):
        pass

    def close(self):
        pass

    def run_full(self):
        try:
            self.run()
        except StopIteration:
            return

    def __next__(self):
        if not self._out_queue:
            try:
                self.run()
            except OutputInterrupt:
                pass
        return self._out_queue.popleft()

    def send(self, value: int):
        self._in_queue.append(value)

    # Actual code processing

    def run(self):
        while True:
            self._step()

    def _step(self):
        # self.log.debug("At pointer=%d, code=%d", self.pointer, self.code[self.pointer])
        action, args = self._get_action()
        # self.log.debug("Running action %s%s", action.__name__, args)

        output_interrupt = action is CodeRunner._output
        next_pointer = action(self, *args)

        if next_pointer is None:
            self.pointer += len(args) + 1
        else:
            self.pointer = next_pointer

        if output_interrupt:
            raise OutputInterrupt

    # Instructions

    def _noop(self):
        pass

    def _add(self, a: Argument, b: Argument, c: Argument):
        self[c] = self[a] + self[b]

    def _mul(self, a: Argument, b: Argument, c: Argument):
        self[c] = self[a] * self[b]

    def _jpt(self, test: Argument, dest: Argument):
        if self[test] != 0:
            return self[dest]
        return None

    def _jpf(self, test: Argument, dest: Argument):
        if self[test] == 0:
            return self[dest]
        return None

    def _lt(self, a: Argument, b: Argument, c: Argument):
        self[c] = int(self[a] < self[b])

    def _eq(self, a: Argument, b: Argument, c: Argument):
        self[c] = int(self[a] == self[b])

    def _halt(self):
        raise EndProgram()

    def _input(self, address: Argument):
        if not self._in_queue:
            raise InputInterrupt
        # self.log.info("Received input: %d", value)
        self[address] = self._in_queue.popleft()

    def _output(self, a: Argument):
        # self.log.info("Sending output: %d", value)
        self._out_queue.append(self[a])

    def _rebase(self, a: Argument):
        self.base += self[a]

    # Build the list of operations and their argument count. The index
    # of each tuple is the op code of its action. Code 99 is processed
    # separately. NOOP was added to fill in the gap for code #0.
    CODES: List[Tuple[Callable, int]] = []
    for _op in [_noop, _add, _mul, _input, _output, _jpt, _jpf, _lt, _eq, _rebase]:
        CODES.append((_op, _op.__code__.co_argcount - 1))

    # Tools

    def __getitem__(self, item: Argument):
        value, mode = item
        if mode == IMMEDIATE:
            return value
        if mode == RELATIVE:
            value += self.base
        if value >= len(self.code):
            return 0
        if value < 0:
            raise RuntimeError("Tried to read from negative address")
        return self.code[value]

    def __setitem__(self, key: Argument, value: int):
        key, key_mode = key
        if key_mode == IMMEDIATE:
            raise RuntimeError("Must provide an address to write to")
        if key_mode == RELATIVE:
            key += self.base
        if key < 0:
            raise RuntimeError("Tried to write to negative address")
        if key >= len(self.code):
            diff = key - len(self.code) + 1
            self.code += [0] * diff
        self.code[key] = value

    @staticmethod
    @lru_cache(maxsize=128)
    def _parse_code(code: int):
        code, op = divmod(code, 100)
        if op == 99:
            return CodeRunner._halt, []
        action, n_args = CodeRunner.CODES[op]
        if not code:
            return action, [0] * n_args
        arg_modes = []
        for _ in range(n_args):
            code, mode = divmod(code, 10)
            arg_modes.append(mode)
        return action, arg_modes

    def _get_action(self):
        p = self.pointer
        action, modes = self._parse_code(self.code[p])
        args = self.code[p + 1:p + 1 + len(modes)]
        return action, list(zip(args, modes))


class ASCIIRunner(CodeRunner):
    def goto_prompt(self):
        lines = []
        try:
            while True:
                lines.append(self.get_line())
        except InputInterrupt:
            return lines

    def goto_output(self):
        try:
            while True:
                self.get_line()
        except NonAsciiOutput as out:
            return out.data

    def send_line(self, line: str):
        for byte in line.encode() + b"\n":
            self.send(byte)

    def get_line(self):
        line = ""
        while (char := self.get_char()) != "\n":
            line += char
        return line

    def get_char(self):
        if (char := next(self)) > 127:
            raise NonAsciiOutput(char)
        return chr(char)

    def program_run(self, program: List[str]):
        self.goto_prompt()
        for line in program:
            self.send_line(line)
        return self.goto_output()

    def interactive_run(self):
        while True:
            try:
                self._step()
            except InputInterrupt:
                self.send_line(input())
            except OutputInterrupt:
                print(self.get_line())


def read_program(year, day):
    from libaoc.files import read_full

    return list(map(int, read_full(year, day).strip().split(",")))
