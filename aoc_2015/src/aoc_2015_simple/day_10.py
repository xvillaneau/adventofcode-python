def look_and_say(string):
    """Run a single iteration of look-and-say"""
    result = ""
    previous, count = string[0], 1
    for char in string[1:]:
        if char != previous:
            result += str(count) + previous
            previous, count = char, 1
        else:
            count += 1
    result += str(count) + previous
    return result


def run_n_times(string, n):
    """Run look-and-say many times on an input string"""
    for _ in range(n):
        string = look_and_say(string)
    return string


def main(string):
    """Solve the puzzle: run look and say 40 times, then 50 times"""
    part_1 = run_n_times(string, 40)
    yield len(part_1)
    part_2 = run_n_times(part_1, 10)
    yield len(part_2)
