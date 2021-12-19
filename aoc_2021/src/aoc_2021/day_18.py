from collections import Iterator
from copy import deepcopy
from dataclasses import dataclass
from itertools import combinations, permutations
from typing import Union


@dataclass
class SFInt:
    value: int

    def __repr__(self):
        return repr(self.value)

    def __eq__(self, other):
        if isinstance(other, SFInt):
            return self.value == other.value
        return False

    def __iadd__(self, other):
        if isinstance(other, int):
            self.value += other
        elif isinstance(other, SFInt):
            self.value += other.value
        else:
            raise NotImplementedError

@dataclass
class SFPair:
    left: "SFNum"
    right: "SFNum"

    def __repr__(self):
        return f"[{self.left!r},{self.right!r}]"

    def __eq__(self, other):
        if not isinstance(other, SFPair):
            return False
        return self.left == other.left and self.right == other.right


SFNum = Union[SFInt, SFPair]


def magnitude(elem: SFNum) -> int:
    if isinstance(elem, SFInt):
        return elem.value
    return magnitude(elem.left) * 3 + magnitude(elem.right) * 2


def parse_num(line: str) -> SFNum:

    def parse_pair(chars: Iterator[str]) -> SFNum:
        lc = next(chars)
        left = parse_pair(chars) if lc == "[" else SFInt(int(lc))
        assert next(chars) == ","
        rc = next(chars)
        right = parse_pair(chars) if rc == "[" else SFInt(int(rc))
        assert next(chars) == "]"
        new_pair = SFPair(left, right)
        left.parent = new_pair
        right.parent = new_pair
        return new_pair

    it_line = iter(line)
    assert next(it_line) == "["
    return parse_pair(it_line)


def traverse_pairs(elem: SFNum, depth: int = 1) -> Iterator[tuple[SFPair, int]]:
    if isinstance(elem, SFInt):
        return
    yield from traverse_pairs(elem.left, depth + 1)
    yield (elem, depth)
    yield from traverse_pairs(elem.right, depth + 1)


def split(elem: SFInt) -> SFPair:
    val = elem.value
    return SFPair(SFInt(val // 2), SFInt(val - val // 2))


def add_nums(num_a: SFNum, num_b: SFNum) -> SFNum:
    sum_num = SFPair(deepcopy(num_a), deepcopy(num_b))

    def check_explode(root: SFPair):
        prev_left = None
        add_right = None

        def check_child(pair: SFPair, depth: int, attr: str):
            nonlocal add_right, prev_left

            elem = getattr(pair, attr)
            if isinstance(elem, SFInt):
                if add_right is not None:
                    elem += add_right
                    return False
                elif depth <= 4:
                    prev_left = elem
                    return True
            if depth == 4 and add_right is None:
                setattr(pair, attr, SFInt(0))
                if prev_left is not None:
                    prev_left += elem.left
                add_right = elem.right
            return True

        for _pair, _depth in traverse_pairs(root):
            if not check_child(_pair, _depth, "left"):
                return False
            if not check_child(_pair, _depth, "right"):
                return False

        return add_right is None

    def check_split(root: SFPair):
        for pair, _ in traverse_pairs(root):
            if isinstance(pair.left, SFInt) and pair.left.value >= 10:
                pair.left = split(pair.left)
                return False
            if isinstance(pair.right, SFInt) and pair.right.value >= 10:
                pair.right = split(pair.right)
                return False
        return True

    while not (check_explode(sum_num) and check_split(sum_num)):
        pass
    return sum_num


def do_homework(numbers: list[SFNum]):
    sf_sum = numbers[0]
    for num in numbers[1:]:
        sf_sum = add_nums(sf_sum, num)
    return sf_sum


def largest_sum(numbers: list[SFNum]):
    return max(
        magnitude(add_nums(a, b)) for a, b in permutations(numbers, 2)
    )


def main(data: str):
    numbers = [parse_num(ln) for ln in data.strip().splitlines()]
    sf_sum = do_homework(numbers)
    yield magnitude(sf_sum)
    yield largest_sum(numbers)
