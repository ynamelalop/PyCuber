import numpy as np
from .constants import U, L, F, R, B, D, \
                       X, Y, Z


ROT = np.zeros((3, 6, 6), int)

rotation_patterns = np.array([
    [[F, D], [D, B], [B, U], [U, F], [L, L], [R, R]],
    [[L, F], [F, R], [R, B], [B, L], [U, U], [D, D]],
    [[L, D], [D, R], [R, U], [U, L], [F, F], [B, B]],
])

for i, pattern in enumerate(rotation_patterns):
    ROT[i][pattern[:, 0], pattern[:, 1]] = 1


def make_cubie(side_colour_map, **kwargs):
    side_colour_map = np.array(side_colour_map)

    cubie = np.ndarray((6,), "int8", **kwargs)

    if side_colour_map.shape == (6,):
        cubie[:] = side_colour_map
    else:
        cubie.fill(-1)
        if side_colour_map.shape != (0,):
            cubie[side_colour_map[:, 0]] = side_colour_map[:, 1]

    assert_is_cubie(cubie)

    return cubie


def assert_is_cubie(cubie):
    assert cubie.shape == (6,)
    assert (cubie != -1).sum() <= 3

    cubie_values = cubie[cubie != -1]
    assert np.in1d(cubie_values, np.arange(6)).all()
    assert cubie_values.shape == (0,) or \
        np.unique(cubie_values).shape == cubie_values.shape


def rotate_on(axis, original, k=1):
    return [rotate_on_X, rotate_on_Y, rotate_on_Z][axis](original, k)


def rotate_on_X(original, k=1):
    ret = original
    for i in range(k % 4):
        ret = ret.dot(ROT[X])
    return ret


def rotate_on_Y(original, k=1):
    ret = original
    for i in range(k % 4):
        ret = ret.dot(ROT[Y])
    return ret


def rotate_on_Z(original, k=1):
    ret = original
    for i in range(k % 4):
        ret = ret.dot(ROT[Z])
    return ret
