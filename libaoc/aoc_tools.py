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
