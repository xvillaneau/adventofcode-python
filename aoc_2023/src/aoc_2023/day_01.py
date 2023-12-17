
def calibration_values(lines: list[str]):
    digits = set(str(d) for d in range(1, 10))
    for line in lines:
        values = [d for d in line if d in digits]
        yield int(values[0]+values[-1])


VALUES = {
    "one": 1, "two": 2, "three": 3,
    "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9,
    "1": 1, "2": 2, "3": 3,
    "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9,
}


def calibration_values_spelled(lines: list[str]):
    for line in lines:
        values = []
        for i in range(len(line)):
            ln = line[i:]
            for token, val in VALUES.items():
                if ln.startswith(token):
                    values.append(val)
                    break
        yield int(values[0] * 10 + values[-1])


def main(data: str):
    lines = data.strip().splitlines()
    yield sum(calibration_values(lines))
    yield sum(calibration_values_spelled(lines))
