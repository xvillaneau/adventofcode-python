
def parse_ranges(data):
    ranges = []
    for line in data:
        start, stop = line.split('-')
        ranges.append(range(int(start), int(stop) + 1))
    return ranges

def unblocked_addresses(data):
    ranges = parse_ranges(data)
    address = 0
    while address <= 4_294_967_295:
        for r in ranges:
            if address in r:
                address = r.stop
                break
        else:
            yield address
            address += 1


def main(data: str):
    unblocked = unblocked_addresses(data.splitlines())
    yield next(unblocked)
    count = 1
    for _ in unblocked:
        count += 1
    yield count
