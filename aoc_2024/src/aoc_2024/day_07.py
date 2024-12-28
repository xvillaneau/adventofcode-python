
def parse_input(data: str) -> list[tuple[int, list[int]]]:
    equations = []
    for ln in data.strip().splitlines():
        res, _, nums_s = ln.partition(": ")
        nums = [int(n) for n in nums_s.split()]
        equations.append((int(res), nums))
    return equations


def is_valid(result: int, nums: list[int], concat=False) -> bool:
    if not nums:
        raise ValueError

    right = nums[-1]
    if len(nums) == 1:
        return result == right

    d, r = divmod(result, right)
    if r == 0 and is_valid(d, nums[:-1], concat):
        return True

    diff = result - right
    if diff >= 0 and is_valid(diff, nums[:-1], concat):
        return True

    if concat:
        size = 10 ** len(str(right))
        d, r = divmod(result, size)
        if r == right and is_valid(d, nums[:-1], concat):
            return True

    return False


def main(data: str):
    equations = parse_input(data)
    yield sum(v for v, n in equations if is_valid(v, n))
    yield sum(v for v, n in equations if is_valid(v, n, True))
