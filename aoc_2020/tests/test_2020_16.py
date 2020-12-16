from aoc_2020.day_16 import filter_tickets, parse_notes, detect_fields

EXAMPLE = """
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""".strip().splitlines()


def test_parse_notes():
    rules, my_ticket, tickets = parse_notes(EXAMPLE)

    assert rules == {
        "class": (range(1, 4), range(5, 8)),
        "row": (range(6, 12), range(33, 45)),
        "seat": (range(13, 41), range(45, 51)),
    }
    assert my_ticket == [7, 1, 14]
    assert tickets == [[7, 3, 47], [40, 4, 50], [55, 2, 20], [38, 6, 12]]


def test_filter_tickets():
    rules, _, tickets = parse_notes(EXAMPLE)
    new_tickets, invalid = filter_tickets(rules, tickets)
    assert new_tickets == [[7, 3, 47]]
    assert invalid == [4, 55, 12]


def test_detect_fields():
    rules, _, tickets = parse_notes(EXAMPLE)
    tickets, _ = filter_tickets(rules, tickets)
    assert detect_fields(rules, tickets) == ["row", "class", "seat"]
