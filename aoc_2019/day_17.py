import re
from typing import List, NamedTuple, Tuple

import numpy as np

from libaoc.primes import all_factors
from libaoc.vectors import Direction, Vect2D, StaticWalker
from aoc_2019.intcode import CodeRunner, read_program, InputInterrupt


def get_image(code) -> str:
    runner = CodeRunner(code)
    image = ""
    for char in runner:
        image += chr(char)
    return image.strip()


def find_intersections(image):
    """Use convolution to detect intersections"""
    img = np.array([[c != "." for c in line] for line in image])
    pattern = np.array(([0, 2, 0], [1, 0, 4], [0, 8, 0]))

    m = np.pad(img, 1)
    view_shape = tuple(np.subtract(m.shape, img.shape) + 1) + img.shape
    strides = m.strides + m.strides
    sub_matrices = np.lib.stride_tricks.as_strided(m, view_shape, strides)
    filtered = np.einsum('ij,ijkl->kl', pattern, sub_matrices)

    return np.where(img, filtered, 0)


def alignment_parameter(filtered_view):
    intersections = np.argwhere(filtered_view == 15)
    return np.sum(np.prod(intersections, axis=1))


def detect_segments(filtered_view):
    seg_filter = np.array([1, -1])

    def _find_segments(_mat):
        _segments = []
        for i, line in enumerate(_mat):
            conv = np.convolve(line, seg_filter)
            starts = np.argwhere(conv == 1)
            stops = np.argwhere(conv == -1) - 1
            for start, stop in np.concatenate((starts, stops), axis=1):
                _segments.append((i, start, stop))
        return _segments

    def _make_segment_map(_segments, _shape):
        _map = np.full(_shape, -1, dtype=int)
        for i, seg in enumerate(_segments):
            row, start, stop = seg
            _map[row, start:stop + 1] = i
        return _map

    horizontal = (filtered_view & 5) > 0
    hor_segments = _find_segments(horizontal)
    hor_map = _make_segment_map(hor_segments, horizontal.shape)

    vertical = ((filtered_view & 10) > 0).transpose()
    vert_segments = _find_segments(vertical)
    vert_map = _make_segment_map(vert_segments, vertical.shape)

    return hor_segments, hor_map, vert_segments, vert_map.transpose()


# NOTE: if the picture reference is x, y
# then the matrix reference in y, -x
READ_DIR = {
    "^": Direction.Left,
    ">": Direction.Up,
    "v": Direction.Right,
    "<": Direction.Down,
}


def find_robot(image):
    img = np.array([list(line) for line in image])
    no_wall = np.where(img == "#", ".", img)
    x, y = np.argwhere(no_wall != ".")[0]
    return Vect2D(x, y), READ_DIR[image[x][y]]


def detect_path(filtered_view, robot_start) -> List[str]:
    max_x, max_y = filtered_view.shape

    def _value(vect):
        return filtered_view[vect.x, vect.y]

    def _can_move(robot):
        ahead = robot.pos + robot.direction.vector
        if not (0 <= ahead.x < max_x and 0 <= ahead.y < max_y):
            return False
        return _value(ahead) > 0

    h_seg, h_map, v_seg, v_map = detect_segments(filtered_view)

    def _h_seg(pos: Vect2D):
        return h_seg[h_map[pos.x, pos.y]]

    def _v_seg(pos: Vect2D):
        return v_seg[v_map[pos.x, pos.y]]

    def _next_moves(robot: StaticWalker):
        if _can_move(robot):
            if robot.direction == Direction.Up:  # Facing Right
                moves = _h_seg(robot.pos)[2] - robot.pos.y
                yield robot.move(moves), str(moves)
            elif robot.direction == Direction.Down:  # Facing Left
                moves = robot.pos.y - _h_seg(robot.pos)[1]
                yield robot.move(moves), str(moves)
            elif robot.direction == Direction.Left:  # Facing Up
                moves = robot.pos.x - _v_seg(robot.pos)[1]
                yield robot.move(moves), str(moves)
            else:  # Facing Down
                moves = _v_seg(robot.pos)[2] - robot.pos.x
                yield robot.move(moves), str(moves)

        yield robot.rot_left(), "L"
        yield robot.rot_right(), "R"

    robot_init = StaticWalker(*robot_start)

    def _finished(robot: StaticWalker):
        return robot.pos != robot_init.pos and _value(robot.pos) in (1, 2, 4, 8)

    class RobotNode(NamedTuple):
        state: StaticWalker
        path: Tuple

    explored = {robot_init}
    frontier = [RobotNode(robot_init, ())]

    while frontier:
        node = frontier.pop()

        if _finished(node.state):
            return list(node.path)

        for next_state, command in _next_moves(node.state):
            if next_state in explored:
                continue
            explored.add(next_state)
            frontier.append(RobotNode(next_state, node.path + (command,)))


def split_path_pattern(path: List[str]):
    path_string = ''.join(path)

    def _match(string: str, patterns):
        while m := next((p for p in patterns if string.startswith(p)), ""):
            string = string[len(m):]
        return len(string) == 0

    def _try_patterns(string: str, can_create=2):
        if not string:
            return
        if not can_create:
            for n in all_factors(len(string)):
                yield (string[:n],)
            return
        for i in range(len(string)):
            pat = string[:i+1]
            for sub_match in _try_patterns(string.replace(pat, ""), can_create - 1):
                yield (pat,) + sub_match

    re_split_nums = re.compile(r'[^\d]+|\d+')

    def _as_routine(pattern):
        return ",".join(re_split_nums.findall(pattern))

    def _patterns_work(string, patterns):
        if not _match(string, patterns):
            return False
        if any(len(p) > 20 for p in patterns):
            return False
        return all(len(_as_routine(p)) <= 20 for p in patterns)

    a, b, c = next(
        p
        for p in _try_patterns(path_string)
        if _patterns_work(path_string, p)
    )
    main = path_string.replace(a, "A").replace(b, "B").replace(c, "C")
    return ",".join(main), _as_routine(a), _as_routine(b), _as_routine(c)


def run_robot(code, routine, func_a, func_b, func_c):
    feed = False
    data = "\n".join([routine, func_a, func_b, func_c, "ny"[feed], ""])

    runner = CodeRunner(code)
    runner.code[0] = 2
    for char in data:
        try:
            _ = list(runner)
        except InputInterrupt:
            runner.send(ord(char))

    if not feed:
        return next(n for n in runner if n > 127)

    while True:
        image, prev = "", -1
        while True:
            char = next(runner)
            if char > 127:  # Not ASCII
                return char
            if (char, prev) == (10, 10):
                break
            image += chr(char)
            prev = char
        print(image)


def day_17(code):
    image = get_image(code)
    filtered_view = find_intersections(image.splitlines())
    yield alignment_parameter(filtered_view)
    path = detect_path(filtered_view, find_robot(image.splitlines()))
    yield run_robot(code, *split_path_pattern(path))


if __name__ == '__main__':
    from libaoc import iter_main

    iter_main(2019, 17, read_program, day_17)
