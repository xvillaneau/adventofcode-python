from collections.abc import Generator as GeneratorABC
from functools import lru_cache
from logging import getLogger, WARNING, StreamHandler
from typing import Dict, Callable, List, Tuple


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


class CodeRunner(GeneratorABC):
    def __init__(self, code: List[int], *, name: str = None, log_level=WARNING):
        self.code = code.copy()
        self.name = name or f"id:{id(self)}"
        self.pointer = 0
        self.relative_base = 0

        self.log = getLogger(f"intcode.{type(self).__name__}.{self.name}")
        self.log.setLevel(log_level)
        self.log.addHandler(StreamHandler())

    def __iter__(self):
        return self

    def __repr__(self):
        if not self.name:
            return super().__repr__()
        return f"<{type(self).__name__} name={self.name!r} pointer={self.pointer}>"

    def copy(self, new_name: str = ""):
        runner = type(self)(self.code.copy(), name=new_name)
        runner.pointer = self.pointer
        runner.relative_base = self.relative_base
        return runner

    def throw(self, typ=None, val=None, tb=None):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def run_full(self):
        try:
            self.run()
        except StopIteration:
            return

    def __next__(self):
        try:
            self.run()
        except OutputInterrupt:
            return self._step(return_output=True)

    def send(self, value: int):
        try:
            self.run()
        except InputInterrupt:
            self._step(input_value=value)

    # Actual code processing

    def run(self):
        while True:
            self._step()

    def _step(self, *, return_output=False, input_value: int = None):
        self.log.debug("At pointer=%d, code=%d", self.pointer, self.code[self.pointer])
        action, args = self._get_action()

        if action is CodeRunner._io_input:
            if input_value is None:
                self.log.debug("Raising InputInterrupt")
                raise InputInterrupt

            self.log.debug(
                "Running action %s%s", action.__name__, tuple(args + [input_value])
            )
            action(self, *args, input_value)
            next_pointer, res = None, None
            self.log.info("Received input: %d", input_value)

        elif action is CodeRunner._io_output:
            if not return_output:
                self.log.debug("Raising OutputInterrupt")
                raise OutputInterrupt

            self.log.debug("Running action %s%s", action.__name__, tuple(args))
            res = action(self, *args)
            next_pointer = None
            self.log.info("Sending output: %d", res)

        else:
            self.log.debug("Running action %s%s", action.__name__, tuple(args))
            res = None
            next_pointer = action(self, *args)

        if next_pointer is None:
            self.pointer += len(args) + 1
        else:
            self.pointer = next_pointer

        return res

    # Instructions

    def _add(self, a: int, b: int, c: int):
        self[c] = self[a] + self[b]

    def _mul(self, a: int, b: int, c: int):
        self[c] = self[a] * self[b]

    def _jump_if_true(self, test, dest):
        if self[test] != 0:
            return self[dest]
        return None

    def _jump_if_false(self, test, dest):
        if self[test] == 0:
            return self[dest]
        return None

    def _less_than(self, a, b, c):
        self[c] = int(self[a] < self[b])

    def _equals(self, a, b, c):
        self[c] = int(self[a] == self[b])

    def _halt(self):
        raise EndProgram()

    def _io_input(self, address: int, value: int):
        self[address] = value

    def _io_output(self, a: int):
        return self[a]

    def _set_relative_base(self, a: int):
        self.relative_base += self[a]

    CODES: Dict[int, Tuple[int, Callable]] = {
        1: (3, _add),
        2: (3, _mul),
        3: (1, _io_input),
        4: (1, _io_output),
        5: (2, _jump_if_true),
        6: (2, _jump_if_false),
        7: (3, _less_than),
        8: (3, _equals),
        9: (1, _set_relative_base),
        99: (0, _halt),
    }

    # Tools

    class Address(int):
        def __repr__(self):
            return f"*{super().__repr__()}"

    class Relative(int):
        def __repr__(self):
            return f"%{super().__repr__()}"

    MODES_CLS = {
        0: Address,
        1: int,
        2: Relative,
    }

    def __getitem__(self, item: int):
        if isinstance(item, self.Relative):
            item = self.Address(self.relative_base + item)
        if isinstance(item, self.Address):
            if item >= len(self.code):
                return 0
            if item < 0:
                raise RuntimeError("Tried to read from negative address")
            return self.code[item]
        return item

    def __setitem__(self, key: int, value: int):
        if isinstance(key, self.Relative):
            key = self.Address(self.relative_base + key)
        if not isinstance(key, self.Address):
            raise RuntimeError("Must provide an address to write to")
        if key < 0:
            raise RuntimeError("Tried to write to negative address")
        if key >= len(self.code):
            diff = key - len(self.code) + 1
            self.code += [0] * diff
        self.code[key] = value

    @classmethod
    @lru_cache(maxsize=128)
    def _parse_code(cls, code: int):
        code, op = divmod(code, 100)
        n_args, action = cls.CODES[op]
        arg_modes = []
        for _ in range(n_args):
            code, mode = divmod(code, 10)
            arg_modes.append(mode)
        return action, arg_modes

    def _get_args(self, modes: List[int]):
        args = []
        for i, mode in enumerate(modes):
            value = self.code[self.pointer + i + 1]
            args.append(self.MODES_CLS[mode](value))
        return args

    def _get_action(self):
        action, modes = self._parse_code(self.code[self.pointer])
        args = self._get_args(modes)
        return action, args


class ASCIIRunner(CodeRunner):
    def goto_prompt(self):
        lines = []
        try:
            while True:
                lines.append(self.get_line())
        except InputInterrupt:
            return lines

    def goto_output(self):
        lines = []
        try:
            while True:
                lines.append(self.get_line())
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
