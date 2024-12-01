from collections import Counter


def parse_input(data: str) -> tuple[list[int], list[int]]:
    list1, list2 = [], []
    for ln in data.strip().splitlines():
        n1, n2 = ln.split()
        list1.append(int(n1))
        list2.append(int(n2))
    return list1, list2


def part_1(list1: list[int], list2: list[int]) -> int:
    return sum(abs(a - b) for a, b in zip(sorted(list1), sorted(list2)))


def part_2(list1: list[int], list2: list[int]) -> int:
    counts = Counter(list2)
    return sum(n * counts[n] for n in list1)


def main(data: str):
    list1, list2 = parse_input(data)
    yield part_1(list1, list2)
    yield part_2(list1, list2)
