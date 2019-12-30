from abc import ABC, abstractmethod
from functools import partial, wraps
from pathlib import Path
from time import perf_counter_ns
from typing import Any, Callable, List


def static_input(data):
    def fake_reader(*_):
        return data
    return fake_reader


def timed(func):
    @wraps(func)
    def _timed(*args, **kwargs):
        start = perf_counter_ns()
        result = func(*args, **kwargs)
        stop = perf_counter_ns()
        return result, (stop - start)
    return _timed


def iter_main(year: int, day: int, reader, generator):
    print(f"Advent of Code year {year}, day {day}")
    day_input = reader(year, day)
    results = generator(day_input)

    p1_res, p1_time = timed(lambda: next(results))()
    print("Part 1:", p1_res)
    print(f"\tRan in {p1_time:,} ns")

    try:
        p2_res, p2_time = timed(lambda: next(results))()
        print("Part 2:", p2_res)
        print(f"\tRan in {p2_time:,} ns")
    except StopIteration:
        pass


def simple_main(year: int, day: int, reader, part_1, part_2=None):
    def _main_iter(day_input):
        yield part_1(day_input)
        if part_2 is not None:
            yield part_2(day_input)
    iter_main(year, day, reader, _main_iter)


def tuple_main(year, day, reader, parts):
    def _main_iter(day_input):
        return iter(parts(day_input))
    iter_main(year, day, reader, _main_iter)


AOC_ROOT = Path(__file__).parent.parent


class BaseRunner(ABC):
    year: int
    day: int

    def main(self):
        print("=====================================")
        print(f"Advent of Code year {self.year}, day {self.day}")
        results = self.run(self.read_data())

        p1_res, p1_time = timed(lambda: next(results))()
        print("Part 1:", p1_res)
        print(f"\tRan in {p1_time:,} ns")

        try:
            p2_res, p2_time = timed(lambda: next(results))()
            print("Part 2:", p2_res)
            print(f"\tRan in {p2_time:,} ns")
        except StopIteration:
            pass

        print()

    @abstractmethod
    def run(self, data):
        pass

    @property
    def data_path(self):
        return AOC_ROOT / f"aoc_{self.year}" / "data" / f"day_{self.day:02}.txt"

    def read_data(self):
        with open(self.data_path) as file:
            full_data = file.read()
        if self.parser is not None:
            return self.parser(full_data)
        return full_data

    @staticmethod
    def lines_parser():
        return staticmethod(parse_lines)

    @staticmethod
    def int_list_parser(delimiter=None):
        return staticmethod(partial(parse_int_list, delimiter=delimiter))

    @staticmethod
    def static_parser(result):
        def fake_parser(_):
            return result
        return fake_parser

    @staticmethod
    def _noop_parser(data):
        return data

    parser: Callable[[str], Any] = _noop_parser


def parse_lines(data: str) -> List[str]:
    return [
        safe_line
        for line in data.splitlines()
        if (safe_line := line.rstrip())
    ]


def parse_int_list(data: str, delimiter=None) -> List[int]:
    lines = parse_lines(data)
    if len(lines) == 1:  # Assume it's a single line of ints
        return [int(i) for i in lines[0].split(delimiter)]
    else:  # Assume it's one int per line
        return [int(i) for i in lines]
