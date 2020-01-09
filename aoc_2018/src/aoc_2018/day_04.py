from datetime import datetime
from heapq import heappush, heappop
from typing import Tuple

import numpy as np


Event = Tuple[datetime, int]


def parse_line(line: str) -> Event:
    timestamp = datetime.strptime(line[1:17], '%Y-%m-%d %H:%M')
    message = line[19:]
    if message == 'wakes up':
        return timestamp, -1
    elif message == "falls asleep":
        return timestamp, -2
    else:
        return timestamp, int(message[7:].partition(" ")[0])


def parse_schedule(data: str):

    events, guards, guard_ids = [], [], {}
    for line in data.splitlines():
        event = parse_line(line)
        heappush(events, event)

        if (n := event[1]) < 0 or n in guard_ids:
            continue
        guard_ids[n] = len(guards)
        guards.append(n)

    schedule = np.zeros((len(guards), 60), dtype=int)

    line_num = len(guards)
    while events:
        timestamp, event = heappop(events)
        if event >= 0:
            line_num = guard_ids[event]
        else:
            schedule[line_num, timestamp.minute:] += (1 if event == -2 else -1)

    return guards, schedule


def main(data: str):
    guards, schedule = parse_schedule(data)
    most_asleep = int(np.argmax(np.sum(schedule, axis=1)))
    yield guards[most_asleep] * np.argmax(schedule[most_asleep])
    most_total_line, most_total_min = divmod(schedule.argmax(), 60)
    yield guards[most_total_line] * most_total_min
