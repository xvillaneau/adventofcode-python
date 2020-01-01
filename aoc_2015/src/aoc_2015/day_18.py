import numpy as np

FILTER = np.array(([1, 1, 1], [1, 0, 1], [1, 1, 1]))

def count_neighbors(lights):
    sub_shape = lights.shape
    m = np.pad(lights, 1)
    view_shape = tuple(np.subtract(m.shape, sub_shape) + 1) + sub_shape
    strides = m.strides + m.strides
    sub_matrices = np.lib.stride_tricks.as_strided(m, view_shape, strides)
    return np.einsum('ij,ijkl->kl', FILTER, sub_matrices)

def transform_lights(lights):
    neighbors = count_neighbors(lights)
    return (neighbors == 3) | (neighbors == 2) & lights

def load_lights(lights: str):
    chars = [list(line) for line in lights.strip().splitlines()]
    return np.array(chars) == '#'

def animate(start_lights: str, steps=100):
    lights = load_lights(start_lights)
    for _ in range(steps):
        lights = transform_lights(lights)
    return np.sum(lights)

def transform_stuck_corners(lights):
    neighbors = count_neighbors(lights)
    lights = (neighbors == 3) | (neighbors == 2) & lights
    lights[0, 0] = lights[-1, 0] = lights[0, -1] = lights[-1, -1] = True
    return lights

def animate_stuck(start_lights: str, steps=100):
    lights = load_lights(start_lights)
    lights[0, 0] = lights[-1, 0] = lights[0, -1] = lights[-1, -1] = True
    for _ in range(steps):
        lights = transform_stuck_corners(lights)
    return np.sum(lights)


def main(data: str):
    yield animate(data)
    yield animate_stuck(data)
