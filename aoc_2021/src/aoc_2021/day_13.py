
Point = tuple[int, int]
Fold = tuple[str, int]


def parse_data(data: str) -> tuple[set[Point], list[Fold]]:
    points, folds = set(), []
    s_points, _, s_folds = data.strip().partition("\n\n")
    for ln in s_points.splitlines():
        x, _, y = ln.partition(",")
        points.add((int(x), int(y)))
    for ln in s_folds.splitlines():
        folds.append((ln[11], int(ln[13:])))
    return points, folds


def fold_paper(points: set[Point], fold: Fold) -> set[Point]:
    axis, pos = fold
    if axis == "x":
        return {(2 * pos - x if x > pos else x, y) for x, y in points}
    else:
        return {(x, 2 * pos - y if y > pos else y) for x, y in points}


def render_points(points: set[Point]) -> str:
    max_x = max(x for x, _ in points)
    max_y = max(y for _, y in points)

    table = [
        ["  "] * (max_x + 1)
        for _ in range(max_y + 1)
    ]
    for x, y in points:
        table[y][x] = "##"
    return "\n".join("".join(line) for line in table)


def main(data: str):
    points, folds = parse_data(data)
    points = fold_paper(points, folds[0])
    yield len(points)
    for fold in folds[1:]:
        points = fold_paper(points, fold)
    yield "\n" + render_points(points)
