from aoc_2018.day_20 import *

EXAMPLES = [
    "^WNE$",
    "^ENWWW(NEEE|SSE(EE|N))$",
    "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$",
    "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$",
    "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$",
]


def test_parse_input():
    assert parse_input(EXAMPLES[0]) == ["WNE"]
    assert parse_input(EXAMPLES[1]) == [
        "ENWWW",
        ["NEEE", ["SSE", ["EE", "N"]]],
    ]
    assert parse_input(EXAMPLES[2]) == [
        "ENNWSWW",
        ["NEWS", ""],
        "SSSEEN",
        ["WNSE", ""],
        "EE",
        ["SWEN", ""],
        "NNN",
    ]
    assert parse_input(EXAMPLES[3]) == [
        "ESSWWN",
        ["E", ["NNENN", [["EESS", ["WNSE", ""], "SSS"], ["WWWSSSSE", ["SW", "NNNE"]]]]],
    ]
    assert parse_input(EXAMPLES[4]) == [
        "WSSEESWWWNW",
        [
            "S",
            [
                "NENNEEEENN",
                [["ESSSSW", ["NWSW", "SSEN"]], ["WSWWN", ["E", ["WWS", ["E", "SS"]]]]],
            ],
        ],
    ]


def test_build_map():
    assert build_map(EXAMPLES[0]) == {
        (0, 0): {(-1, 0)},
        (-1, 0): {(0, 0), (-1, 1)},
        (-1, 1): {(-1, 0), (0, 1)},
        (0, 1): {(-1, 1)},
    }
    assert build_map(EXAMPLES[1]) == {
        (0, 0): {(1, 0)},
        (1, 0): {(0, 0), (1, 1)},
        (1, 1): {(1, 0), (0, 1)},
        (0, 1): {(1, 1), (-1, 1)},
        (-1, 1): {(0, 1), (-2, 1)},
        (-2, 1): {(-1, 1), (-2, 2), (-2, 0)},
        (-2, 2): {(-2, 1), (-1, 2)},
        (-1, 2): {(-2, 2), (0, 2)},
        (0, 2): {(-1, 2), (1, 2)},
        (1, 2): {(0, 2)},
        (-2, 0): {(-2, 1), (-2, -1)},
        (-2, -1): {(-2, 0), (-1, -1)},
        (-1, -1): {(-2, -1), (-1, 0), (0, -1)},
        (-1, 0): {(-1, -1)},
        (0, -1): {(-1, -1), (1, -1)},
        (1, -1): {(0, -1)},
    }


def test_furthest_room():
    assert furthest_room(build_map(EXAMPLES[0])) == 3
    assert furthest_room(build_map(EXAMPLES[1])) == 10
    assert furthest_room(build_map(EXAMPLES[2])) == 18
    assert furthest_room(build_map(EXAMPLES[3])) == 23
    assert furthest_room(build_map(EXAMPLES[4])) == 31
