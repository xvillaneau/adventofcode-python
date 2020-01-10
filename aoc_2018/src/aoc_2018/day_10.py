import re

import numpy as np

RE_VECT = re.compile(r'<\s*(-?\d+),\s*(-?\d+)>')

TEST = """
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
""".strip()


def parse_data(data: str):

    def parse_line(line):
        (x, y), (vx, vy) = RE_VECT.findall(line)
        return (int(x), int(y)), (int(vx), int(vy))

    data = np.array([parse_line(line) for line in data.splitlines()])
    return data[:, 0], data[:, 1]


def detect_message(data: str):
    pos, vel = parse_data(data)

    _ind = np.nonzero(vel)
    num = int(round(-np.average(pos[_ind] / vel[_ind])))

    a, b, c = (score(pos, vel, num + i) for i in (-1, 0, 1))
    while a < b or c < b:
        if a < b:
            num -= 1
            b, c = a, b
            a = score(pos, vel, num - 1)
        else:
            num += 1
            a, b = b, c
            c = score(pos, vel, num + 1)

    return pos + vel * num, num


def render_message(points):
    points -= np.min(points, axis=0)
    text = np.full(np.max(points, axis=0) + 1, " ")
    text[tuple(points.transpose())] = "#"
    return "\n".join("".join(line) for line in text.transpose())


def score(pos, vel, num):
    pos = pos + vel * num
    return np.sum(np.max(pos, axis=0) - np.min(pos, axis=0))


def main(data: str):
    points, steps = detect_message(data)
    yield "\n" + render_message(points)
    yield steps
