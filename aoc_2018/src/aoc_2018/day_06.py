import numpy as np
from libaoc.parsers import parse_integer_table


def point_distances(point, mat_size):
    """
    :param point: 2-element 1D array (or tuple) with x,y coordinates of the point to process
    :param mat_size: 2-element 1D array (or tuple) representing the size of the output matrix
    :return: Matrix with the block distances to the point
    """
    (x, y), (mx, my) = point, mat_size
    return np.sum(abs(np.mgrid[-x : mx - x + 1, -y : my - y + 1]), axis=0)


def main(data: str, safe_total=10000):
    """
    :param data: (nx2) matrix of all points, our puzzle input (as text)
    :param safe_total: Safe total distance, for part 2
    """
    # Parse the points, move their coordinates closer to the axis
    points = parse_integer_table(data, delimiter=",")
    points -= np.min(points, axis=0) - 1
    max_size = np.max(points, axis=0) + 1

    # Make 3D matrix where each layer is the distances to one point
    distances = np.array([point_distances(p, max_size) for p in points])

    # Transform that 3D matrix into booleans planes where True means
    # that the point on that place (on of) the closest
    closest = distances == np.min(distances, axis=0)

    # Generate a bool map of places that have more than one closest point
    equidistant = np.sum(closest, axis=0) > 1
    closest &= ~equidistant

    # Calculate the size of the largest finite region
    border = np.pad(np.zeros(max_size - 1, dtype=int), 1, constant_values=1)
    on_border = np.any(closest & border, axis=(1, 2))
    scores = np.sum(closest, axis=(1, 2)) * ~on_border
    yield np.max(scores)

    # Calculate how many places have a safe "total distance" to all points
    yield np.sum(np.sum(distances, axis=0) < safe_total)
