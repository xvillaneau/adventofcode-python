import pytest

from aoc_2021.day_10 import line_scores, completion_score, record_scores, completion_win_score

VALID_LINES = [
    "()",
    "[]",
    "([])",
    "{()()()}",
    "<([{}])>",
    "[<>({}){}[([])<>]]",
    "(((((((((())))))))))",
]
CORRUPT_LINES = ["(]", "{()()()>", "(((()))}", "<([]){()}[{}])"]


@pytest.mark.parametrize("line", VALID_LINES)
def test_lines_valid(line):
    assert line_scores(line) == (0, 0)


@pytest.mark.parametrize("line", CORRUPT_LINES)
def test_lines_corrupt(line):
    err_score, cmp_score = line_scores(line)
    assert err_score > 0
    assert cmp_score == 0


EXAMPLE = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""

def test_error_score():
    error_score, _ = record_scores(EXAMPLE.strip().splitlines())
    assert error_score == 26397


COMPLETIONS = [
    ("[({(<(())[]>[[{[]{<()<>>", "}}]])})]"),
    ("[(()[<>])]({[<{<<[]>>(", ")}>]})"),
    ("(((({<>}<{<{<>}{[]{[]{}", "}}>}>))))"),
    ("{<[[]]>}<{[{[{[]{()[[[]", "]]}}]}]}>"),
    ("<{([{{}}[<[[[<>{}]]]>[]]", "])}>"),
]

COMPLETIONS_SCORES = [
    ("}}]])})]", 288957),
    (")}>]})", 5566),
    ("}}>}>))))", 1480781),
    ("]]}}]}]}>", 995444),
    ("])}>", 294),
]

@pytest.mark.parametrize("line,completion", COMPLETIONS)
def test_completions(line, completion):
    err, cmp = line_scores(line)
    assert err == 0
    assert cmp == completion_score(completion)


@pytest.mark.parametrize("string,score", COMPLETIONS_SCORES)
def test_completion_scores(string, score):
    assert completion_score(string) == score


def test_completion_win_score():
    scores = [sc for _, sc in COMPLETIONS_SCORES]
    assert completion_win_score(scores) == 288957
