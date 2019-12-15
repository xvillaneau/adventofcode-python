from functools import wraps
from time import perf_counter_ns


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


def simple_main(year: int, day: int, reader, part_1, part_2=None):
    print(f"Advent of Code year {year}, day {day}")
    day_input = reader(year, day)
    p1_res, p1_time = timed(part_1)(day_input)
    print("Part 1:", p1_res)
    print(f"\tRan in {p1_time:,} ns")
    if part_2 is not None:
        p2_res, p2_time = timed(part_2)(day_input)
        print("Part 2:", p2_res)
        print(f"\tRan in {p2_time:,} ns")


def iter_main(year: int, day: int, reader, generator):
    print(f"Advent of Code year {year}, day {day}")
    day_input = reader(year, day)
    results = generator(day_input)
    p1_res, p1_time = timed(lambda: next(results))()
    print("Part 1:", p1_res)
    print(f"\tRan in {p1_time:,} ns")
    p2_res, p2_time = timed(lambda: next(results))()
    print("Part 2:", p2_res)
    print(f"\tRan in {p2_time:,} ns")


def tuple_main(year, day, reader, parts):
    print(f"Advent of Code year {year}, day {day}")
    day_input = reader(year, day)
    (p1_res, p2_res), time = timed(parts)(day_input)
    print("Part 1:", p1_res)
    print("Part 2:", p2_res)
    print(f"\tRan in {time:,} ns")




def static(value):
    def func(*args):
        return value
    return func
