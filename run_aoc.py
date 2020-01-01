#!/usr/bin/env python
import argparse
from functools import partial
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import sys
from time import perf_counter_ns

if sys.version_info < (3, 8):
    raise RuntimeError("Only Python >= 3.8 is supported")

YEARS = [2019]  # Add more over time
AOC_ROOT = Path(__file__).parent


def load_year(year: int, namespace=""):
    """
    Load the package with the year's code. Designed to work without
    having to install the code in the PYTHONPATH.
    """
    name = f"aoc_{year}"
    if name in sys.modules:
        return

    src_folder = f"{name}_{namespace}" if namespace else name
    location = AOC_ROOT / name / "src" / src_folder / "__init__.py"
    if not location.is_file():
        raise ImportError(f"Package for {name} does not exist")

    # Import magic
    spec = spec_from_file_location(name, location)
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)


def get_main(year: int, day: int):
    """
    Load the module for the given day (assuming the year's package was
    loaded with load_year), and look for a suitable main.
    """
    module = import_module(f"aoc_{year}.day_{day:02}")

    if hasattr(module, "main"):
        # Has a main function, expected to be a generator that takes
        # the full input file as argument.
        return partial(run_day_main, year, day, module.main)

    if hasattr(module, "AocRunner"):
        # Has an AocRunner class. This was a bad idea.
        return module.AocRunner().aoc_main

    raise ImportError(f"No compatible main found in {module}")


def timed_next(generator):
    """Get the next value from a generator and time how long it takes"""
    start = perf_counter_ns()
    result = next(generator)
    stop = perf_counter_ns()
    return result, (stop - start)


def run_day_main(year: int, day: int, day_main):
    print(f"Advent of Code year {year}, day {day}")

    data_path = AOC_ROOT / f"aoc_{year}" / "data" / f"day_{day:02}.txt"
    with open(data_path, "r") as file:
        main = day_main(file.read())

    p1_res, p1_time = timed_next(main)
    print("Part 1:", p1_res)
    print(f"\tRan in {p1_time:,} ns")

    try:
        p2_res, p2_time = timed_next(main)
        print("Part 2:", p2_res)
        print(f"\tRan in {p2_time:,} ns")
    except StopIteration:
        pass


def process_args(year: int, day: int, interactive: bool):
    """Select the years/days to run based on the input"""

    def ask_or_abort(message: str):
        answer = input(message + " [y/N] ")
        if answer.lower() not in ["yes", "y", "true"]:
            print("Aborting")
            sys.exit(1)

    # Process the year input
    if year == -1:
        if interactive:
            ask_or_abort("This will run ALL the AoC solutions. Are you really sure?")
        years = YEARS
    else:
        assert year in YEARS
        years = [year]

    # Process the day input
    if day == -1:
        if year != -1 and interactive:
            ask_or_abort(f"This will run all solutions for AoC {year}, are you sure?")
        days = list(range(1, 26))
    else:
        assert 1 <= day <= 25
        days = [day]

    return years, days


def aoc_main(year: int, day: int, interactive=True, namespace=""):
    years, days = process_args(year, day, interactive)

    # Run the solutions!
    for year in years:
        # Load the package containing this year's code
        load_year(year, namespace=namespace)

        for day in days:
            try:
                day_main = get_main(year, day)
            except ImportError:
                print(f"Skipping {year} day {day}, import failed")
            else:
                day_main()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, nargs="?", default=-1)
    parser.add_argument("day", type=int, nargs="?", default=-1)
    parser.add_argument("namespace", type=str, nargs="?", default="")
    parser.add_argument("--yes", "-y", dest="interactive", action="store_false")

    aoc_main(**vars(parser.parse_args()))
