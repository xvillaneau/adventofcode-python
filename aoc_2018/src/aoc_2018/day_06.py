import numpy as np
from libaoc.parsers import parse_integer_table


def point_distances(point, mat_size):
    """
    :param point: 2-element 1D array (or tuple) with x,y coordinates of the point to process
    :param mat_size: 2-element 1D array (or tuple) representing the size of the output matrix
    :return: Matrix with the block distances to the point
    """
    (x, y), (mx, my) = point, mat_size
    sx = np.repeat(np.arange(mx+1)[np.newaxis] - x, my+1, 0).transpose()
    sy = np.repeat(np.arange(my+1)[np.newaxis] - y, mx+1, 0)
    return abs(sx) + abs(sy)


def score(territory):
    """
    :param territory: bool matrix showing the "territory" of a point
    :return: Score of a point's "territory", which is its size unless it's infinite
    """
    border = np.ones(territory.shape, dtype=int)
    border[1:-1, 1:-1] = 0
    return 0 if (territory & border).any() else territory.sum()


def main(data: str, safe_total=10000):
    """
    :param data: (nx2) matrix of all points, our puzzle input (as text)
    :param safe_total: Safe total distance, for part 2
    """
    points = parse_integer_table(data, delimiter=",")
    # Move points close to the axis
    moved_pts = points - points.min(axis=0)
    # Make 3D matrix where each layer is the distances to one point
    distances = np.array([point_distances(p, moved_pts.max(axis=0)) for p in moved_pts])
    # Get respectively the map of distances to the nearest point,
    # and the maps of ID of the corresponding layer (aka territories)
    closest_dist, territories = distances.min(axis=0), distances.argmin(axis=0)
    # Generate a bool map of places that have more than one closest point
    equidistant = (np.repeat(closest_dist[np.newaxis], len(points), 0) == distances).sum(axis=0) > 1
    # Calculate the size of the largest finite region
    yield max(score((territories == i) & ~equidistant) for i in range(len(points)))
    # Calculate how many places have a safe "total distance" to all points
    yield (distances.sum(axis=0) < safe_total).sum()


TEST = np.array([
    [1, 1],
    [1, 6],
    [8, 3],
    [3, 4],
    [5, 5],
    [8, 9]])
