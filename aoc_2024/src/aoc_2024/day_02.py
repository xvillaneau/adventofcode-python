
def parse_input(data: str):
    return [
        [int(n) for n in ln.split()]
        for ln in data.strip().splitlines()
    ]


def is_safe(report: list[int]) -> bool:
    incr = report[-1] > report[0]
    prev = report[0]
    for this in report[1:]:
        if this == prev:
            return False
        if (this > prev) != incr:
            return False
        if abs(this - prev) > 3:
            return False
        prev = this
    return True


def is_safe_2(report: list[int]) -> bool:
    return is_safe(report) or any(
        is_safe(report[:i] + report[i + 1:])
        for i in range(len(report))
    )


def main(data: str):
    reports = parse_input(data)
    yield sum(is_safe(r) for r in reports)
    yield sum(is_safe_2(r) for r in reports)
