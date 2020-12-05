SEAT_ID_BIN = {
    ord('F'): '0', ord('B'): '1', ord('L'): '0', ord('R'): '1'
}

def seat_id(seat: str):
    return int(seat.translate(SEAT_ID_BIN), base=2)


def main(data: str):
    seats = sorted(seat_id(line) for line in data.splitlines())

    front, back = seats[0], seats[-1]
    yield back

    # Here's the trick: if all seat IDs were in the list, the sum of
    # all IDs would be exactly the some of the arithmetic sequence from
    # 'front' to 'back', for which there is a known formula. Therefore,
    # the ID of our (missing) seat must be the difference between the
    # full sum and the actual sum of all seat IDs.
    n_seats = back - front + 1
    full_sum = n_seats * (2 * front + n_seats - 1) // 2
    yield full_sum - sum(seats)
