#!/usr/bin/env python
import argparse
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import sys

if sys.version_info < (3, 8):
    raise RuntimeError("Only Python >= 3.8 is supported")

YEARS = [2019]  # Add more over time
AOC_ROOT = Path(__file__).parent


def ask_or_abort(message: str):
    answer = input(message + " [y/N] ")
    if answer.lower() not in ["yes", "y", "true"]:
        print("Aborting")
        sys.exit(1)


def load_year(year: int):
    name = f"aoc_{year}"
    if name in sys.modules:
        return

    location = AOC_ROOT / name / "src" / name / "__init__.py"
    if not location.is_file():
        raise ImportError(f"Package for {name} does not exist")

    # Import magic
    spec = spec_from_file_location(name, location)
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)


def get_runner(year: int, day: int):
    module = import_module(f"aoc_{year}.day_{day:02}")

    if not hasattr(module, "AocRunner"):
        raise ImportError(f"AocRunner not found in {module}")

    return module.AocRunner()


def main(year: int, day: int, yes: bool):
    # Process the year input
    if year == -1:
        if not yes:
            ask_or_abort("This will run ALL the AoC solutions. Are you really sure?")
        years = YEARS
    else:
        assert year in YEARS
        years = [year]

    # Process the day input
    if day == -1:
        if year != -1 and not yes:
            ask_or_abort(f"This will run all solutions for AoC {year}, are you sure?")
        days = list(range(1, 26))
    else:
        assert 1 <= day <= 25
        days = [day]

    # Run the solutions!
    for year in years:
        # Load the package containing this year's code
        load_year(year)

        for day in days:
            try:
                runner = get_runner(year, day)
            except ImportError:
                print(f"Skipping {year} day {day}, import failed")
            else:
                runner.main()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, nargs="?", default=-1)
    parser.add_argument("day", type=int, nargs="?", default=-1)
    parser.add_argument("--yes", "-y", action="store_true")

    main(**vars(parser.parse_args()))
