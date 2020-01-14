import numpy as np

def parse_input(data: str):
    nanobots = []
    for line in data.splitlines():
        pos_str, radius = line.split(">, r=")
        x, y, z = pos_str[5:].split(",")
        nanobots.append((int(x), int(y), int(z), int(radius)))
    return np.array(nanobots)


def range_of_strongest(nanobots):
    ind_strongest = np.argmax(nanobots[:, 3])
    rel_pos = nanobots[:, :3] - nanobots[ind_strongest, :3]
    distances = np.sum(abs(rel_pos), axis=1)
    return np.sum(distances <= nanobots[ind_strongest, 3])


def best_position(nanobots):
    start = np.around(np.average(nanobots[:, :3], axis=0)).astype(int)


def main(data: str):
    nanobots = parse_input(data)
    yield range_of_strongest(nanobots)
