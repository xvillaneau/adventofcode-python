from bisect import bisect_left


def parse_bits(data: str):
    lines = data.strip().splitlines()
    return [list(map(int, ln)) for ln in lines]


def gamma_epsilon_rates(data: list[list[int]]) -> tuple[int, int]:
    tot, bits = len(data), len(data[0])
    # Count how many of each bit we have
    counts = [0] * bits
    for code in data:
        for i, c in enumerate(code):
            counts[i] += c
    # Build the Gamma value from binary
    gamma = 0
    for n in counts:
        gamma <<= 1
        gamma += n > tot // 2
    # epsilon = ~gamma, but we need leading zeros
    epsilon = gamma ^ ((1 << bits) - 1)
    return gamma, epsilon


def get_ratings(data: list[list[int]]) -> tuple[int, int]:
    def to_num(code: list[int]) -> int:
        num = 0
        for b in code:
            num <<= 1
            num += b
        return num

    bits = len(data[0])
    nums = [to_num(c) for c in data]
    nums.sort()

    def _get_rating(codes: list[int], bit: int = bits - 1, invert=False):
        """
        Recursive call to isolate the rating.
        Reduces the list of code at each step"""
        if len(codes) == 1:
            return codes[0]
        # Bit that we are selecting in this step
        mask = 1 << bit
        # Part of the rating that has already been fixed
        prev = codes[0] & ~(2 * mask - 1)
        # Find where the 0/1 transition is in the list of codes.
        # We can do that easily since the list is sorted,
        # and all the high bits are identical.
        # We are looking for XXX10...
        pivot = bisect_left(codes, prev + mask)
        # Based on the position of the limit,
        # figure out whether 0 or 1 is the most common value.
        common = pivot <= len(codes) / 2
        # Keep only numbers where the bit is correctly set
        # (most common for Oxygen, least common for CO2)
        codes = [c for c in codes if (c & mask == mask) == (common ^ invert)]
        # Repeat until only one value is left
        return _get_rating(codes, bit - 1, invert)

    return _get_rating(nums), _get_rating(nums, invert=True)


def main(data: str):
    codes = parse_bits(data)
    gamma, epsilon = gamma_epsilon_rates(codes)
    yield gamma * epsilon
    oxy, co2 = get_ratings(codes)
    yield oxy * co2
