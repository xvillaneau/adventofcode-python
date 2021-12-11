
CHUNK_PAIRS = {"(": ")", "<": ">", "[": "]", "{": "}"}
ERROR_POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137}
COMPLETE_POINTS = {")": 1, "]": 2, "}": 3, ">": 4}


def line_scores(line: str) -> tuple[int, int]:
    stack = []
    for char in line:
        if char in CHUNK_PAIRS:
            stack.append(CHUNK_PAIRS[char])
        else:
            expected = stack.pop()
            if char != expected:
                return ERROR_POINTS[char], 0

    return 0, completion_score("".join(stack[::-1]))


def completion_score(completion: str) -> int:
    score = 0
    for char in completion:
        score *= 5
        score += COMPLETE_POINTS[char]
    return score


def completion_win_score(scores: list[int]) -> int:
    scores = sorted(scores)
    return scores[len(scores) // 2]


def record_scores(lines: list[str]) -> tuple[int, int]:
    err_score, cmp_scores = 0, []
    for line in lines:
        e, c = line_scores(line)
        err_score += e
        if c > 0:
            cmp_scores.append(c)
    return err_score, completion_win_score(cmp_scores)


def main(data: str):
    lines = data.strip().splitlines()
    yield from record_scores(lines)
