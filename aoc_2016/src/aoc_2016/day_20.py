
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

def day_20(data):
    unblocked = unblocked_addresses(data)
    yield next(unblocked)
    count = 1
    for _ in unblocked:
        count += 1
    yield count


if __name__ == '__main__':
    from libaoc import iter_main, files
    iter_main(2016, 20, files.read_lines, day_20)
