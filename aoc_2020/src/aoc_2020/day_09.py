from collections import defaultdict
from typing import List


def find_invalid(message: List[int], buffer=25) -> int:
    tail = 0
    sums = defaultdict(int)

    for head, num in enumerate(message):
        if head - tail == buffer:
            if not sums[num]:
                return num

            removed = message[tail]
            for i in range(tail + 1, head):
                sums[removed + message[i]] -= 1
            tail += 1

        for i in range(tail, head):
            sums[num + message[i]] += 1

    return -1


def find_weakness(message: List[int], invalid_num: int) -> int:
    prev_sums = []
    for i, num in enumerate(message):
        for j, p_sum in enumerate(prev_sums):
            if num + p_sum == invalid_num:
                num_range = message[j:i + 1]
                return min(num_range) + max(num_range)
            prev_sums[j] += num
        prev_sums.append(num)
    return -1


def main(data: str):
    message = list(map(int, data.splitlines()))
    yield (invalid_num := find_invalid(message))
    yield find_weakness(message, invalid_num)
