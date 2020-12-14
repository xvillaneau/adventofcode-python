from functools import reduce
from operator import itemgetter

from libaoc.math import extended_euclidian_algorithm


def parse_buses(data: str):
    arrival, schedule = data.splitlines()
    buses = [int(n) if n != "x" else None for n in schedule.split(",")]
    return int(arrival), buses


def wait_times(arrival, buses):
    for bus in buses:
        if bus is None:
            continue
        yield (bus, -(arrival % bus) % bus)


def bus_sync_step(acc, bus):
    period, start, wait = acc
    if bus is None:
        # Do nothing, just wait one more minute
        pass

    elif period == 0:
        # Initialize with the first specified bus
        period, start = bus, wait

    else:
        # The fun part
        a, _, f = extended_euclidian_algorithm(period, bus)
        if f != 1:
            raise ValueError("Co-prime buses are important!")

        # a is such that: a * period + n * bus = 1
        a *= -(start + wait)
        # Now: start + wait + a * period = n * bus
        # This mean that (start + a * period) now satisfies the bus sync
        # conditions; last step is to pick the first positive start.
        start = (a * period + start) % (bus * period)
        period *= bus

    return period, start, wait + 1


def sync_buses(buses):
    return reduce(bus_sync_step, buses, (0, 0, 0))[1]


def main(data: str):
    arrival, buses = parse_buses(data)

    bus, wait = min(wait_times(arrival, buses), key=itemgetter(1))
    yield bus * wait

    yield sync_buses(buses)
