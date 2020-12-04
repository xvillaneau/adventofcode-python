from bisect import bisect_left

from libaoc.parsers import parse_integer_list

# Thanks to Michael Wilson Churvis for providing the initial double-
# pointer solution that inspired this. My previous solution was nowhere
# as fast as this version.


def find_pair(expenses, val=2020, start=0):
    """
    Look for a pair of numbers in the input such that their sum is equal
    to a given value. The input expenses MUST be a SORTED LIST. Return
    the product of those values. A start index for the search can be
    specified.
    """
    left = start
    # Save some time by skipping all the right-side values that are too
    # large for the smallest left-side value to work. Because the list
    # is sorted, we can use binary search to get there fast.
    right = bisect_left(expenses, val - expenses[left], lo=left)

    while left < right:
        v_left, v_right = expenses[left], expenses[right]
        if v_left + v_right == val:
            return v_left * v_right
        elif v_left + v_right < val:
            left += 1
        else:
            right -= 1

    return 0


def find_triplet(expenses, val=2020):
    """
    Find a triplet of numbers of which the sum is a given value. Returns
    the product of those numbers.
    """
    for i in range(len(expenses) - 2):
        pair_prod = find_pair(expenses, val - expenses[i], i + 1)
        if pair_prod > 0:
            return expenses[i] * pair_prod

    return 0


def main(data: str):
    expenses = sorted(parse_integer_list(data))
    yield find_pair(expenses)
    yield find_triplet(expenses)
