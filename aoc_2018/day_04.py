
from dataclasses import dataclass
from datetime import datetime
import re
from typing import Tuple, Union

import numpy as np
from libaoc import files, tuple_main

RE_LINE = re.compile(r'\[(.*)\] (.*)')
RE_GUARD = re.compile(r'Guard #(\d+) begins shift')


@dataclass
class Guard:
    id: int


@dataclass
class Event:
    minute: int
    asleep: bool


def parse_line(line: str) -> Tuple[datetime, Union[Guard, Event]]:
    date_s, message = RE_LINE.search(line).groups()
    timestamp = datetime.strptime(date_s, '%Y-%m-%d %H:%M')
    if message == 'wakes up':
        event = Event(timestamp.minute, False)
    elif message == "falls asleep":
        event = Event(timestamp.minute, True)
    else:
        event = Guard(int(RE_GUARD.search(message).groups()[0]))
    return timestamp, event


def parse_schedule(lines):
    events = [parse_line(l) for l in lines]
    guards = list(sorted(set(g.id for _, g in events if isinstance(g, Guard))))

    asleep_times = np.zeros((len(guards), 61), dtype=int)
    asleep_times[:, 0] = guards

    line_num = 0
    sorted_events = (e for _, e in sorted(events, key=lambda t: t[0]))
    for event in sorted_events:
        if isinstance(event, Guard):
            line_num = guards.index(event.id)
        else:
            asleep_times[line_num, event.minute + 1:] += (1 if event.asleep else -1)
    return asleep_times


def most_asleep(lines):
    schedule = parse_schedule(lines)
    most_times = max(schedule, key=lambda l: l[1:].sum())
    most_total_line, most_total_min = divmod(schedule[:, 1:].argmax(), 60)
    return (most_times[0] * most_times[1:].argmax(), schedule[most_total_line, 0] * most_total_min)


if __name__ == '__main__':
    tuple_main(2018, 4, files.read_lines, most_asleep)
