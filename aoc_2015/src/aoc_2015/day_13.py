from itertools import permutations
import re
from typing import Dict, List, Set, Tuple

ME = "Me"
RE_SEAT = re.compile(
    r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)."
)

def parse_seating(pref_list):
    happiness: Dict[Tuple[str, str], int] = {}
    attendees: Set[str] = set()
    for line in pref_list:
        person, affinity, score, neighbor = RE_SEAT.match(line).groups()
        score = int(score) * (1 if affinity == "gain" else -1)
        happiness[(person, neighbor)] = score
        attendees |= {person, neighbor}
    return happiness, attendees


def calc_happiness(seating: List[str], happiness):
    score = 0
    for a, b in zip(seating, seating[1:]):
        if a == ME or b == ME:
            continue
        score += happiness[(a, b)] + happiness[(b, a)]
    first, last = seating[0], seating[-1]
    if first != ME and last != ME:
        score += happiness[(first, last)] + happiness[(last, first)]
    return score


def max_happiness(pref_list: List[str]):
    preferences, attendees = parse_seating(pref_list)
    first = attendees.pop()
    return max(
        calc_happiness((first,) + seating, preferences)
        for seating in permutations(attendees)
    )

def max_with_me(pref_list: List[str]):
    preferences, attendees = parse_seating(pref_list)
    return max(
        calc_happiness((ME,) + seating, preferences)
        for seating in permutations(attendees)
    )

def main(data: str):
    pref_list = data.splitlines()
    yield max_happiness(pref_list)
    yield max_with_me(pref_list)
