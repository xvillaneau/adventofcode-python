from libaoc.parsers import parse_integer_list

_COUNTS = []

def fish_count(days: int):
    while (age := len(_COUNTS)) <= days:
        count = 1
        for child_age in range(age - 7, 0, -7):
            if child_age >= 2:
                count += _COUNTS[child_age - 2]
        _COUNTS.append(count)

    return _COUNTS[days]


def count_all_fish(fish: list[int], days: int):
    return sum(fish_count(days + 8 - d) for d in fish)


def main(data: str):
    fish = parse_integer_list(data, ",")
    yield count_all_fish(fish, 80)
    yield count_all_fish(fish, 256)
